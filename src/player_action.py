import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import pygame
import pygubu
import random
import threading
from networking import Networking
from user import User

Game_time = 30  # Game duration in seconds

def build_player_action_screen(root: tk.Tk, users: Dict[str, List[User]], network: Networking, main_frame: tk.Frame, return_to_entry_screen, builder, entry_ids, db, user_data) -> None:
    # Load the player action UI and set up the action screen
    builder = pygubu.Builder()
    builder.add_from_file("assets/ui/player_action.ui")
    
    action_frame = builder.get_object("action_frame", root)
    action_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Configure the team tables
    blue_team_tree = create_team_treeview(action_frame, "Blue Team", 0.05)
    red_team_tree = create_team_treeview(action_frame, "Red Team", 0.55)

    # Populate the teams
    populate_team_treeview(blue_team_tree, users.get("blue", []))
    populate_team_treeview(red_team_tree, users.get("red", []))

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
        args=(lambda shooter, target: update_scores(shooter, target, users, blue_team_tree, red_team_tree, network),),
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
                  blue_team_tree: ttk.Treeview, red_team_tree: ttk.Treeview, network: Networking) -> None:
    target_user = None
    for team_name, team_users in users.items():
        for user in team_users: 
            if user.user_id == target_id:
                target_user = user
    # Ensure no inconsistent spaces here
    for team_name, team_users in users.items():
        for user in team_users:
            if user.user_id == shooter_id and user.team != target_user.team and target_user != None:
                user.game_score += 10
                network.transmit_player_hit(target_id)
            elif user.user_id == shooter_id and user.team == target_user.team and target_user != None:
                user.game_score -= 10
                network.transmit_player_hit(target_id)


                
    refresh_team_treeview(blue_team_tree, users.get("blue", []))
    refresh_team_treeview(red_team_tree, users.get("red", []))

def refresh_team_treeview(treeview: ttk.Treeview, team_users: List[User]) -> None:
    for item in treeview.get_children():
        treeview.delete(item)
    populate_team_treeview(treeview, team_users)

def end_game(users: Dict[str, List[User]], network: Networking) -> None:
    stop_music()
    for _ in range(3):
        network.transmit_end_game_code()
    print("Game has ended!")
