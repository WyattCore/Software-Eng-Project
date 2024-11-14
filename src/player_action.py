import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import pygame
import pygubu
import threading
from networking import Networking
from user import User

Game_time = 10  # Game duration in seconds


def build_player_action_screen(root: tk.Tk, users: Dict[str, List[User]], network: Networking, main_frame: tk.Frame) -> None:
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
    back_button.configure(command=lambda: return_to_entry_screen(action_frame, main_frame))
    
    # Listener thread for receiving traffic
    print("HELLO")
    listener_thread = threading.Thread(
    target=network.traffic_listener,
    args=(lambda shooter, target: update_scores(shooter, target, users, blue_team_tree, red_team_tree),),
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


def return_to_entry_screen(action_screen: tk.Frame, main_frame: tk.Frame) -> None:
    stop_music()
    action_screen.destroy()
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def start_music() -> None:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/tracks/Track01.mp3")
    pygame.mixer.music.play(-1)


def stop_music() -> None:
    pygame.mixer.music.stop()


def start_countdown(root: tk.Tk, action_frame: tk.Frame, users: Dict[str, List[User]], network: Networking, count: int = 20, countdown_label: Optional[tk.Label] = None) -> None:
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


def update_scores(shooter_id: int, target_id: int, users: Dict[str, List[User]], blue_team_tree: ttk.Treeview, red_team_tree: ttk.Treeview) -> None:
    for team_name, team_users in users.items():
        for user in team_users:
            if user.user_id == shooter_id:
                user.game_score += 10
            elif user.user_id == target_id:
                user.game_score -= 10
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
