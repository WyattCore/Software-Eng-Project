from typing import Dict, List
from tkinter import messagebox
import tkinter as tk
import pygubu

from networking import Networking
from user import User
from database import Database  # Import the Database class
from player_action import build_player_action_screen


def on_tab(event: tk.Event, root: tk.Tk, entry_ids: Dict, users: Dict, builder: pygubu.Builder, db: Database) -> None:
    entry_field_id: str = entry_ids.get(event.widget.winfo_id())
    if entry_field_id is None:
        return

    # If the entry field ID is an equipment ID field, transmit equipment ID
    if "equipment_id" in entry_field_id:
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "Equipment ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        equipment_id: int = int(event.widget.get())

        if equipment_id < 0 or equipment_id > 100:
            messagebox.showerror("Error", "Equipment ID must be between 0 and 100")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        if equipment_id in [user.equipment_id for user in users["blue"]] or equipment_id in [user.equipment_id for user in users["red"]]:
            messagebox.showerror("Error", "Equipment ID has already been entered")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

    # If the entry field ID is a user ID field, query database for user with matching ID
    elif "user_id" in entry_field_id:
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "User ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        user_id: int = int(event.widget.get())
        matching_players = []  # Initialize matching_players here
        database_response = db.fetch_all_players()  # Fetch all players
        matching_players = [p for p in database_response if p[0] == user_id]  # Find matching user ID

        # If user already exists in the database, autofill codename entry field
        if matching_players:
            equipment_id: int = int(builder.get_object(entry_field_id.replace("user_id", "equipment_id"), root).get())
            codename: str = matching_players[0][1]  # Get codename

            if user_id in [user.user_id for user in users["blue"]] or user_id in [user.user_id for user in users["red"]]:
                messagebox.showerror("Error", "User ID has already been entered")
                event.widget.delete(0, tk.END)
                root.after_idle(lambda: event.widget.focus_set())
                return

            # Add user to dictionary, starting with score 0
            # Here is where we use after_idle to ensure we update the UI smoothly
            root.after_idle(lambda: users["blue"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, codename, "blue")) if "blue" in entry_field_id else users["red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, codename, "red")))

            # Autofill the codename entry field
            builder.get_object(entry_field_id.replace("user_id", "codename"), root).insert(0, codename)

            # Jump to the next row's equipment ID entry field if not on the last row
            row: int = int(entry_field_id.split("_")[-1])
            if row != 15:
                next_entry_field = builder.get_object(entry_field_id.replace(f"user_id_{row}", f"equipment_id_{row + 1}"), root)
                root.after_idle(lambda: next_entry_field.focus_set())

    # If the user tabs from the codename entry field, insert the user into the database if they don't already exist
    elif "codename" in entry_field_id:
        equipment_id: int = int(builder.get_object(entry_field_id.replace("codename", "equipment_id"), root).get())
        user_id_widget: tk.Entry = builder.get_object(entry_field_id.replace("codename", "user_id"), root)
        user_id: int = int(user_id_widget.get())

        codename = event.widget.get()

        # Throw error if codename already exists in users dictionary or database
        if codename in [user.codename for user in users["blue"]] or codename in [user.codename for user in users["red"]]:
            messagebox.showerror("Error", "Codename has already been entered")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        if any(codename == p[1] for p in db.fetch_all_players()):  # Check against database
            messagebox.showerror("Error", "Codename already exists in database")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Add user to dictionary
        users["blue" if "blue" in entry_field_id else "red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, codename, "blue" if "blue" in entry_field_id else "red"))

        # Attempt to insert the user into the database, display an error message if the insert fails
        try:
            db.insert_player(user_id, codename)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            user_id_widget.delete(0, tk.END)
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: user_id_widget.focus_set())
            return

def on_f12(main_frame: tk.Tk, entry_ids: Dict, users: Dict, builder: pygubu.Builder, db: Database) -> None:
    # Clear all entry fields
    for entry_id in entry_ids: 
        builder.get_object(entry_ids[entry_id], main_frame).delete(0, tk.END)

    # Refocus the first entry field 
    builder.get_object("blue_equipment_id_1", main_frame).focus_set()

    # Clear the users dictionary
    users["blue"].clear()
    users["red"].clear()
    

def on_f5(main_frame: tk.Tk, root: tk.Tk, users: Dict, network: Networking, db: Database, builder: pygubu.Builder, entry_ids: Dict) -> None:
    # Ensure at least 1 user per team
    if len(users["blue"]) < 1 or len(users["red"]) < 1:
        messagebox.showerror("Error", "There must be at least 1 user on each team")
        return

    # Insert users into the database
    try:
        for team in users:
            for user in users[team]:
                # Insert into database, assuming insert_player method exists
                db.insert_player(user.user_id, user.codename)
    except Exception as e:
        messagebox.showerror("Database Error", f"Error inserting player: {e}")
        return

    # Proceed with network transmission or other logic
    for team in users:
        for user in users[team]:
            network.transmit_equipment_code(user.equipment_id)

    # Hide the main frame and proceed to the action screen
    main_frame.place_forget()
    build_player_action_screen(root, users, network, main_frame, return_to_entry_screen, builder, entry_ids, db, users)

    
def build(root: tk.Tk, users: Dict[str, List[User]], network: Networking, db: Database) -> None:
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
    fields: List[str] = [
        "red_equipment_id_",
        "red_user_id_",
        "red_codename_",
        "blue_equipment_id_",
        "blue_user_id_",
        "blue_codename_"
    ]

    # Add each entry field ID to the dictionary of entry field IDs
    for i in range(1, 16):
        for field in fields:
            entry_ids[builder.get_object(f"{field}{i}", red_frame if "red" in field else blue_frame).winfo_id()] = f"{field}{i}"

    # Place focus on the first entry field
    builder.get_object("blue_equipment_id_1", blue_frame).focus_set()

    # Bind keys to lambda functions
    root.bind("<Tab>", lambda event: on_tab(event, root, entry_ids, users, builder, db))
    root.bind("<KeyPress-F12>", lambda event: on_f12(main_frame, entry_ids, users, builder, db))
    root.bind("<KeyPress-F5>", lambda event: on_f5(main_frame, root, users, network, db, builder, entry_ids))

    # Bind continue button to the action screen
    builder.get_object("submit", main_frame).configure(command=lambda: on_f5(main_frame, root, users, network, db, builder, entry_ids))
    builder.get_object("clear", main_frame).configure(command=lambda: on_f12(main_frame, entry_ids, users, builder, db))


def rebind_events(builder: pygubu.Builder, main_frame: tk.Tk, root: tk.Tk, users: Dict, network: Networking, entry_ids: Dict, db: Database) -> None:
    """Rebind all necessary events after returning to the player entry screen."""
    root.bind("<Tab>", lambda event: on_tab(event, root, entry_ids, users, builder, db))
    root.bind("<KeyPress-F12>", lambda event: on_f12(main_frame, entry_ids, users, builder, db))
    root.bind("<KeyPress-F5>", lambda event: on_f5(main_frame, root, users, network, db, builder, entry_ids))


def return_to_entry_screen(root: tk.Tk, action_screen, main_frame: tk.Frame, builder: pygubu.Builder, entry_ids: Dict, users: Dict, db: Database) -> None:
    # Hide the action screen
    action_screen.place_forget()

    # Re-add the player entry main frame to the root window
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Repopulate entry fields with current user data
    #root.after(100, repopulate_entry_fields, builder, main_frame, entry_ids, users)
    
    # Rebind events
    #rebind_events(builder, main_frame, root, users, entry_ids, db)

def repopulate_entry_fields(builder: pygubu.Builder, main_frame: tk.Frame, entry_ids: Dict, users: Dict) -> None:
    for team in users:
        for i, user in enumerate(users[team]):
            entry_prefix = f"{team}_"
            # Repopulate the fields with user data
            builder.get_object(f"{entry_prefix}equipment_id_{i+1}", main_frame).insert(0, str(user.equipment_id))
            builder.get_object(f"{entry_prefix}user_id_{i+1}", main_frame).insert(0, str(user.user_id))
            builder.get_object(f"{entry_prefix}codename_{i+1}", main_frame).insert(0, user.codename)
