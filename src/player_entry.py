from typing import Dict, List
from tkinter import messagebox
import tkinter as tk
import pygubu

from networking import Networking
from user import User
from main import supabase_client

database_response = None
def on_tab(event: tk.Event, root: tk.Tk, entry_ids: Dict, users: Dict, builder: pygubu.Builder) -> None:
    # Make database response global for remembering previous on_tab call
    global database_response

    # Get the entry field ID
    # If key doesn't exist, do nothing
    entry_field_id: str = entry_ids.get(event.widget.winfo_id())
    if entry_field_id is None:
        return
    
    # If the entry field ID is an equipment ID field, transmit equipment ID
    if "equipment_id" in entry_field_id:
        # If equipment ID input is not an integer, display error message and refocus entry field to clear input
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "Equipment ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return
        
        # Get the equipment ID
        equipment_id: int = int(event.widget.get())

        # Check if equipment ID is between 0 and 100
        if equipment_id < 0 or equipment_id > 100:
            messagebox.showerror("Error", "Equipment ID must be between 0 and 100")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Check if equipment ID is already in use
        if equipment_id in [user.equipment_id for user in users["blue"]] or equipment_id in [user.equipment_id for user in users["red"]]:
            messagebox.showerror("Error", "Equipment ID has already been entered")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

    # If the entry field ID is a user ID field, query database for user with matching ID
    elif "user_id" in entry_field_id:
        # If entry field is empty or not an integer, display error message and refocus entry field to clear input
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "User ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Query the database for the user with the matching ID
        database_response = supabase_client.table("users").select("*").eq("id", event.widget.get()).execute()

        # If user already exists in the database, autofill username entry field
        if database_response.data:
            equipment_id: int = int(builder.get_object(entry_field_id.replace("user_id", "equipment_id"), root).get())
            user_id: int = int(database_response.data[0]["id"])
            username: str = database_response.data[0]["username"]
            
            # If user has already been entered, display error message and refocus entry field to clear input
            if user_id in [user.user_id for user in users["blue"]] or user_id in [user.user_id for user in users["red"]]:
                messagebox.showerror("Error", "User ID has already been entered")
                event.widget.delete(0, tk.END)
                root.after_idle(lambda: event.widget.focus_set())
                return

            # Add user to dictionary, starting with score 0
            users["blue" if "blue" in entry_field_id else "red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, username))

            # Autofill the username entry field
            builder.get_object(entry_field_id.replace("user_id", "username"), root).insert(0, username)

            # Jump to the next row's equipment ID entry field if not on the last row
            row: int = int(entry_field_id.split("_")[-1])
            if row != 15:
                next_entry_field = builder.get_object(entry_field_id.replace(f"user_id_{row}", f"equipment_id_{row + 1}"), root)
                root.after_idle(lambda: next_entry_field.focus_set())

    # If the user tabs from the username entry field, insert the user into the database if they don't already exist
    elif "username" in entry_field_id and database_response.data == []:

        # TODO: If the user goes back and deletes the username or user ID, remove the user from the users dictionary

        # Get equipment ID and user ID, user ID entry box for refocusing
        equipment_id: int = int(builder.get_object(entry_field_id.replace("username", "equipment_id"), root).get())
        user_id_widget: tk.Entry = builder.get_object(entry_field_id.replace("username", "user_id"), root)
        user_id: int = int(user_id_widget.get())

        # Get username from entry field
        username = event.widget.get()

        # Throw error if username already exists in users dictionary or database
        if username in [user.username for user in users["blue"]] or username in [user.username for user in users["red"]]:
            messagebox.showerror("Error", "Username has already been entered")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return
        
        if supabase_client.table("users").select("*").eq("username", username).execute().data:
            messagebox.showerror("Error", "Username already exists in database")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Add user to dictionary
        users["blue" if "blue" in entry_field_id else "red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, username))

        # Attempt to insert the user into the database, display an error message if the POST request fails
        try:
            supabase_client.table("users").insert({
                "id": user_id,
                "username": username
            }).execute()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            user_id_widget.delete(0, tk.END)
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: user_id_widget.focus_set())
            return

def on_f12(main_frame: tk.Tk, entry_ids: Dict, users: Dict, builder: pygubu.Builder) -> None:
    # Clear all entry fields
    for entry_id in entry_ids: 
        builder.get_object(entry_ids[entry_id], main_frame).delete(0, tk.END)

    # Refocus the first entry field 
    builder.get_object("blue_equipment_id_1", main_frame).focus_set()

    # Clear the users dictionary
    users["blue"].clear()
    users["red"].clear()

# f5 key to open play action screen and have 30 second timer before game starts and 6 minute game timer
def on_f5(main_frame: tk.Tk, root: tk.Tk, users: Dict, network: Networking) -> None:
    # If there is not at least 1 user for each team, display error message and return
    if len(users["blue"]) < 1 or len(users["red"]) < 1:
        messagebox.showerror("Error", "There must be at least 1 user on each team")
        return

    # Remove F5, F12, and Tab key bindings
    root.unbind("<Tab>")
    root.unbind("<KeyPress-F12>")
    root.unbind("<KeyPress-F5>")

    # For each equipment ID entry field, transmit the equipment ID
    for team in users:
        for user in users[team]:
            network.transmit_equipment_code(user.equipment_id)
    
    # Remove frame from screen without destroying it
    main_frame.destroy()


def build(root: tk.Tk, users: Dict, network: Networking) -> None:
    # Load the UI file and create the builder
    builder: pygubu.Builder = pygubu.Builder()
    builder.add_from_file("assets/ui/player_entry.ui")

    # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Get the team frames
    teams_frame: tk.Frame = builder.get_object("teams", main_frame)
    red_frame: tk.Frame = builder.get_object("red_team", teams_frame)
    blue_frame: tk.Frame = builder.get_object("blue_team", teams_frame)

    # Create a dictionary of process IDs and their corresponding entry field IDs
    entry_ids: Dict[int, str] = {}
    fields: List[str] = {
        "red_equipment_id_",
        "red_user_id_",
        "red_username_",
        "blue_equipment_id_",
        "blue_user_id_",
        "blue_username_"
    }

    # Add each entry field ID to the dictionary of entry field IDs
    for i in range(1, 16):
        for field in fields:
            entry_ids[builder.get_object(f"{field}{i}", red_frame if "red" in field else blue_frame).winfo_id()] = f"{field}{i}"

    # Place focus on the first entry field
    builder.get_object("blue_equipment_id_1", blue_frame).focus_set()

    # Bind keys to lambda functions
    root.bind("<Tab>", lambda event: on_tab(event, root, entry_ids, users, builder))
    root.bind("<KeyPress-F12>", lambda event: on_f12(main_frame, entry_ids, users, builder))
    root.bind("<KeyPress-F5>", lambda event: on_f5(main_frame, root, users, network))

    # Bind continue button to F5 function for moving on to play action screen
    cont_button: tk.Button = builder.get_object("submit", main_frame)
    cont_button.configure(command=lambda: on_f5(main_frame, root, users, network))