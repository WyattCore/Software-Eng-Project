import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import pygame
import pygubu
import random
import threading
from networking import Networking
from user import User

Game_time = 360  # Game duration in seconds

def build_player_action_screen(root: tk.Tk, users: Dict[str, List[User]], network: Networking, main_frame: tk.Frame, return_to_entry_screen, builder, entry_ids, db, user_data) -> None:
    # Load the player action UI and set up the action screen
    builder = pygubu.Builder()
    builder.add_from_file("assets/ui/player_action.ui")
    
    action_frame = builder.get_object("action_frame", root)
    action_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Configure the team tables
    blue_team_tree = create_team_treeview(action_frame, "Blue Team", 0.05)
    red_team_tree = create_team_treeview(action_frame, "Red Team", 0.55)

    # Create and place cumulative score labels
    blue_team_score_label = tk.Label(action_frame, text="Blue Team Score: 0", font=("Helvetica", 12))
    blue_team_score_label.place(relx=0.05, rely=0.35, anchor=tk.NW)

    red_team_score_label = tk.Label(action_frame, text="Red Team Score: 0", font=("Helvetica", 12))
    red_team_score_label.place(relx=0.55, rely=0.35, anchor=tk.NW)

    # Get the action_textbox from the builder and set it up
    action_textbox: tk.Text = builder.get_object("action_textbox", action_frame)
    
    # Populate the teams
    populate_team_treeview(blue_team_tree, users.get("blue", []))
    populate_team_treeview(red_team_tree, users.get("red", []))

    # Create and place the leading team label
    leading_team_label = tk.Label(action_frame, text="Leading Team: None", font=("Helvetica", 14), fg="black")
    leading_team_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Update the score labels initially
    update_team_scores(blue_team_score_label, red_team_score_label, users, leading_team_label)
    
    # Configure buttons
    play_button: tk.Button = builder.get_object("play_button", action_frame)
    play_button.configure(command=lambda: start_countdown(root, action_frame, users, network))
    
    back_button: tk.Button = builder.get_object("back_button", action_frame)
    back_button.configure(
        command=lambda: return_to_entry_screen(root, action_frame, main_frame, builder, entry_ids, users, db)
    )

    # Listener thread for receiving traffic
    listener_thread = threading.Thread(
        target=network.traffic_listener,
        args=(lambda shooter, target: update_scores(shooter, target, users, blue_team_tree, red_team_tree, network, blue_team_score_label, red_team_score_label, leading_team_label, action_textbox),),
        daemon=True,
    )
    listener_thread.start()

def create_team_treeview(parent: tk.Frame, team_name: str, relx: float) -> ttk.Treeview:
    tree = ttk.Treeview(parent, columns=("Base", "ID", "Codename", "Score"), show="headings")
    for col in ("Base", "ID", "Codename", "Score"):
        tree.heading(col, text=col)
        tree.column(col, width=100 if col == "ID" else 150)
    tree.place(relx=relx, rely=0.1, anchor=tk.NW)
    
    # Styling
    style = ttk.Style()
    style.configure(f"{team_name}.Treeview", background="lightblue" if team_name == "Blue Team" else "lightcoral")
    tree.configure(style=f"{team_name}.Treeview")
    return tree

def populate_team_treeview(tree: ttk.Treeview, users: List[User]) -> None:
    for user in users:
        tree.insert("", "end", values=(user.has_hit_base, user.user_id, user.codename, user.game_score))

def start_music() -> None:
    pygame.mixer.init()

    # Create a list of available tracks
    track_list = [f"assets/tracks/Track0{i}.mp3" for i in range(1, 9)]
    # Randomly choose a track from the list
    chosen_track = random.choice(track_list)
    
    # Load and play the chosen track
    pygame.mixer.music.load(chosen_track)
    pygame.mixer.music.play(-1)

def stop_music() -> None:
    pygame.mixer.music.stop()

def start_countdown(root: tk.Tk, action_frame: tk.Frame, users: Dict[str, List[User]], network: Networking, count: int =20, countdown_label: Optional[tk.Label] = None) -> None:
    if countdown_label is None:
        countdown_label = tk.Label(action_frame, text=str(count), font=("Helvetica", 64))
        countdown_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    if count == 15:
        start_music()

    if count > 0:
        countdown_label.config(text=str(count))
        root.after(1000, start_countdown, root, action_frame, users, network, count - 1, countdown_label)
    else:
        countdown_label.destroy()
        start_game(users, network)
        game_timer(root, action_frame, users, network, Game_time)

def game_timer(root: tk.Tk, action_frame: tk.Frame, users: Dict[str, List[User]], network: Networking, count: int, gameplay_label: Optional[tk.Label] = None) -> None:
    minutes, seconds = divmod(count, 60)
    time_str = f"{minutes:02}:{seconds:02}"

    if gameplay_label is None:
        gameplay_label = tk.Label(action_frame, text=f"Remaining Time: {time_str}", font=("Helvetica", 16))
        gameplay_label.place(relx=1.0, rely=1.0, anchor="se")

    if count > 0:
        gameplay_label.config(text=f"Remaining Time: {time_str}")
        root.after(1000, game_timer, root, action_frame, users, network, count - 1, gameplay_label)
    else:
        gameplay_label.destroy()
        end_game(users, network)

def start_game(users: Dict[str, List[User]], network: Networking) -> None:
    network.transmit_start_game_code()
    print("Game has started!")

def update_scores(shooter_id: int, target_id: int, users: Dict[str, List[User]], 
                  blue_team_tree: ttk.Treeview, red_team_tree: ttk.Treeview, network: Networking, 
                  blue_team_score_label: tk.Label, red_team_score_label: tk.Label, 
                  leading_team_label: tk.Label, action_textbox: tk.Text) -> None:
    target_user = None
    
    # Only assign target_user if target_id is not "43" or "53"
    if target_id != 53 and target_id != 43:
        for team_name, team_users in users.items():
            for user in team_users: 
                if user.user_id == target_id:
                    target_user = user
                    break  # Exit the loop once we find the target_user
    
    # Special handling for target_id "43" or "53"
    if target_id == 43 or target_id == 53:
        for team_name, team_users in users.items():
            for user in team_users: 
                if user.user_id == shooter_id:
                    if target_id == 43 and user.team == "red":
                        user.game_score += 100
                        user.has_hit_base = True
                        network.transmit_player_hit(target_id)
                        event_message = f"Red Player {user.codename} hit base!"
                        user.codename = f"🅱 {user.codename}"
                        update_game_event(action_textbox, event_message)  # Log event
                    elif target_id == 53 and user.team == "blue": 
                        user.game_score += 100
                        user.has_hit_base = True
                        network.transmit_player_hit(target_id)
                        event_message = f"Blue Player {user.codename} hit base!"
                        user.codename = f"🅱 {user.codename}"
                        update_game_event(action_textbox, event_message)  # Log event
                    else:
                        network.transmit_player_hit(target_id)  # Corrected indentation

    else:
        # Normal handling for other target_ids
        if target_user is not None:
            for team_name, team_users in users.items():
                for user in team_users:
                    if user.user_id == shooter_id and user.team != target_user.team:
                        user.game_score += 10
                        network.transmit_player_hit(target_id)
                        event_message = f"Player {user.codename} hit Player {target_user.codename}!"
                        update_game_event(action_textbox, event_message)  # Log event
                    elif user.user_id == shooter_id and user.team == target_user.team:
                        user.game_score -= 10
                        network.transmit_player_hit(target_id)
                        event_message = f"Player {user.codename} hit their teammate {target_user.codename}!"
                        update_game_event(action_textbox, event_message)  # Log event

    refresh_team_treeview(blue_team_tree, users.get("blue", []))
    refresh_team_treeview(red_team_tree, users.get("red", []))

    # Update cumulative team scores
    update_team_scores(blue_team_score_label, red_team_score_label, users, leading_team_label)
    

def update_team_scores(blue_team_score_label: tk.Label, red_team_score_label: tk.Label, users: Dict[str, List[User]], leading_team_label: tk.Label) -> None:
    # Calculate cumulative score for Blue Team
    blue_score = sum(user.game_score for user in users.get("blue", []))
    red_score = sum(user.game_score for user in users.get("red", []))
    
    # Update the score labels
    blue_team_score_label.config(text=f"Blue Team Score: {blue_score}")
    red_team_score_label.config(text=f"Red Team Score: {red_score}")
    
    # Update the leading team label
    if blue_score > red_score:
        leading_team_label.config(text=f"Leading Team: Blue Team ({blue_score} points)", fg="blue")
    elif red_score > blue_score:
        leading_team_label.config(text=f"Leading Team: Red Team ({red_score} points)", fg="red")
    else:
        leading_team_label.config(text="Leading Team: Tie", fg="black")


def update_game_event(action_textbox: tk.Text, message: str) -> None:
    action_textbox.config(state=tk.NORMAL)  # Enable text widget for editing
    action_textbox.insert(tk.END, message + "\n")  # Add the event to the textbox
    action_textbox.yview(tk.END)  # Scroll to the bottom to show the latest event
    action_textbox.config(state=tk.DISABLED)  # Disable text widget to prevent editing

def refresh_team_treeview(treeview: ttk.Treeview, team_users: List[User]) -> None:
    for item in treeview.get_children():
        treeview.delete(item)
    # Sort users by score in descending order
    sorted_users = sorted(team_users, key=lambda user: user.game_score, reverse=True)
    populate_team_treeview(treeview, sorted_users)


def end_game(users: Dict[str, List[User]], network: Networking) -> None:
    stop_music()
    for _ in range(3):
        network.transmit_end_game_code()
    print("Game has ended!")
