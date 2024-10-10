import tkinter as tk
from typing import Dict, List
from user import User
import pygubu

from networking import Networking


def build_player_action_screen(root: tk.Tk, users: Dict, network: Networking) -> None:
    # Load the UI file and create the builder for player action screen
    builder: pygubu.Builder = pygubu.Builder()
    builder.add_from_file("assets/ui/player_action.ui")

    # Create the player action screen frame and place it in the root window
    action_frame: tk.Frame = builder.get_object("action_frame", root)
    action_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Example: Display users on each team in labels
    for team in users:
        team_label: tk.Label = builder.get_object(f"{team}_label", action_frame)
        user_list = "\n".join([f"{user.codename} (ID: {user.user_id})" for user in users[team]])
        team_label.configure(text=user_list)

    # Example: Bind action buttons or game controls to this screen
    play_button: tk.Button = builder.get_object("play_button", action_frame)
    play_button.configure(command=lambda: start_game(users, network))  # start_game can be your next action
