from typing import Dict, List
import os
import tkinter as tk
import psycopg2
from psycopg2 import sql

from networking import Networking
from database import Database  # Import the Database class
from user import User
import splash_screen
import player_entry

if os.name == "nt":
    import winsound


# Define PostgreSQL connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    'password': 'student',
    'host': 'localhost',
    'port': '5432'
}

# Initialize the Database instance
db = Database()
db.connect()  # Establish the connection

def build_root() -> tk.Tk:
    # Build main window, set title, make fullscreen
    root: tk.Tk = tk.Tk()
    root.title("Photon")
    root.configure(background="white")

    # Force window to fill screen, place at top left
    width: int = root.winfo_screenwidth()
    height: int = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")

    # Disable resizing
    root.resizable(False, False)
    return root

def destroy_root(root: tk.Tk, network: Networking) -> None:
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_ASYNC)
    network.close_sockets()
    db.close()  # Close the database connection
    root.destroy()

def main() -> None:
    # Declare dictionary for storing user information
    # Format: { team: [User, User, ...] }
    users: Dict[str, List[User]] = {
        "blue": [],
        "red": []
    }

    # Create networking object
    network: Networking = Networking()
    network.set_sockets()

    # Call build_root function to build the root window
    root: tk.Tk = build_root()

    # Bind escape key and window close button to destroy_root function
    root.bind("<Escape>", lambda event: destroy_root(root, network))
    root.protocol("WM_DELETE_WINDOW", lambda: destroy_root(root, network))

    # Build the splash screen
    splash: splash_screen = splash_screen.build(root)

    # After 3 seconds, destroy the splash screen and build the player entry screen
    # Pass the db object to player_entry.build
    root.after(3000, splash.destroy)
    root.after(3000, player_entry.build, root, users, network, db)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
