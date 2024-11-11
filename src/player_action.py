import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import pygame
import pygubu

from networking import Networking
from user import User

Game_time = 10

def build_player_action_screen(root: tk.Tk, users: Dict[str, List[User]], network: Networking, main_frame : tk.Frame) -> None:
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
    
    #back to player_entry screen button
    back_button: tk.Button = builder.get_object("back_button", action_frame)
    back_button.configure(command=lambda: return_to_entry_screen(action_frame, main_frame))
    
    # Bind F5 to start the countdown with correct arguments
    root.bind("<KeyPress-F5>", lambda event: start_countdown(root, action_frame, users, network))

def return_to_entry_screen(action_screen, main_frame: tk.Frame):
	stop_music()
	action_screen.destroy()
	main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
	


def start_music() -> None:
    """Plays the background track when the countdown reaches 14."""
    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load("assets/tracks/Track01.mp3")
    pygame.mixer.music.play(-1)  # Play the music on loop

def stop_music() -> None:
    """Stops the background track."""
    pygame.mixer.music.stop()

def start_countdown(root: tk.Tk, action_frame: tk.Frame, users: Dict[str, List[User]], network: Networking, count: int = 20, countdown_label: Optional[tk.Label] = None) -> None:
    """Start the countdown timer on the player action screen."""
    if countdown_label is None:
        # Create the countdown label once
        countdown_label = tk.Label(action_frame, text=str(count), font=("Helvetica", 64))
        countdown_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    if count == 15:
        start_music()

    if count > 0:
        # Update the countdown label each second
        countdown_label.config(text=str(count))
        root.after(1000, start_countdown, root, action_frame, users, network, count - 1, countdown_label)
    else:
        # Countdown is complete, start the game
        countdown_label.config(text="BEGIN!")
        root.after(1000, countdown_label.destroy)  # Destroy label after 1 second
        start_game(users, network)
        gameTimer(root, action_frame, users, network, Game_time)

def gameTimer(root: tk.Tk, action_frame: tk.Frame, users:Dict[str, List[User]], network: Networking, count: int = 10, gameplay_label: Optional[tk.Label] = None) -> None:
    #obtaining time format
    seconds = count % 60 
    minutes = count // 60 
    time = f"{minutes:02}:{seconds:02}"
    if gameplay_label is None:
        gameplay_label = tk.Label(action_frame, text = "Remaining Time: " + time, font=("Helveticia", 16))
        gameplay_label.place(relx= 1.0, rely = 1.0, anchor = "se")
    
    if count > 0:
        gameplay_label.config(text="Remaining Time: " + time)
        root.after(1000, gameTimer, root, action_frame, users, network, count - 1, gameplay_label) 
    else:
        gameplay_label.config(text="Time done!")
        root.after(1000, gameplay_label.destroy)
        end_game(users, network)
       # if network.transmit_end_game_code():
        #    print("Game done!)

def start_game(users: Dict[str, List[User]], network: Networking) -> None:
    """Logic to start the game after the countdown."""
    network.transmit_start_game_code()
    print("Game has started!")
    # Send signals via network or enable game controls here
    
def end_game(users: Dict[str, List[User]], network: Networking) -> None:
	stop_music()
	network.transmit_end_game_code()
	network.transmit_end_game_code()
	network.transmit_end_game_code()
	print("Game has ended!")

