import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import pygubu

from networking import Networking
from user import User

def build_player_action_screen(root: tk.Tk, users: Dict[str, List[User]], network: Networking) -> None:
    # Load the UI file and create the builder for the player action screen
    builder: pygubu.Builder = pygubu.Builder()
    builder.add_from_file("assets/ui/player_action.ui")

    # Create the player action screen frame and place it in the root window
    action_frame: tk.Frame = builder.get_object("action_frame", root)
    action_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Configure team Treeviews for Blue and Red teams
    blue_team_tree = ttk.Treeview(action_frame, columns=("ID", "Codename"), show="headings")
    blue_team_tree.heading("ID", text="ID")
    blue_team_tree.heading("Codename", text="Codename")
    blue_team_tree.place(relx=0.05, rely=0.1, anchor=tk.NW)

    # Configure the red team Treeview
    red_team_tree = ttk.Treeview(action_frame, columns=("ID", "Codename"), show="headings")
    red_team_tree.heading("ID", text="ID")
    red_team_tree.heading("Codename", text="Codename")
    red_team_tree.place(relx=0.55, rely=0.1, anchor=tk.NW)

    # Set the background color of the tables
    blue_style = ttk.Style()
    blue_style.configure("BlueTeam.Treeview", background="lightblue", fieldbackground="lightblue")
    blue_team_tree.configure(style="BlueTeam.Treeview")

    red_style = ttk.Style()
    red_style.configure("RedTeam.Treeview", background="lightcoral", fieldbackground="lightcoral")
    red_team_tree.configure(style="RedTeam.Treeview")

    # Populate team tables with players
    for user in users.get('blue', []):
        blue_team_tree.insert("", "end", values=(user.user_id, user.codename))

    for user in users.get('red', []):
        red_team_tree.insert("", "end", values=(user.user_id, user.codename))

    # Bind the start game button to start countdown or the game
    play_button: tk.Button = builder.get_object("play_button", action_frame)
    play_button.configure(command=lambda: start_countdown(root, action_frame, users, network))
    
    # Bind F5 to start the countdown with correct arguments
    root.bind("<KeyPress-F5>", lambda event: start_countdown(root, action_frame, users, network))


def start_countdown(root: tk.Tk, action_frame: tk.Frame, users: Dict[str, List[User]], network: Networking, count: int = 5, countdown_label: Optional[tk.Label] = None) -> None:
    """Start the countdown timer on the player action screen."""
    if countdown_label is None:
        # Create the countdown label once
        countdown_label = tk.Label(action_frame, text=str(count), font=("Helvetica", 64))
        countdown_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    if count > 0:
        # Update the countdown label each second
        countdown_label.config(text=str(count))
        root.after(1000, start_countdown, root, action_frame, users, network, count - 1, countdown_label)
    else:
        # Countdown is complete, start the game
        countdown_label.config(text="GO!")
        root.after(1000, countdown_label.destroy)  # Destroy label after 1 second
        start_game(users, network)



def start_game(users: Dict[str, List[User]], network: Networking) -> None:
    """Logic to start the game after the countdown."""
    network.transmit_start_game_code()
    print("Game has started!")
    # Send signals via network or enable game controls here
