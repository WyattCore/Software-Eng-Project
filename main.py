from typing import Dict, List
from dotenv import load_dotenv
import os
import tkinter as tk
import supabase

from dotenv import load_dotenv
from networking import Networking
from user import User
import splash_screen
import player_entry

if os.name == "nt":
    import winsound



# Load environment variables
load_dotenv("/home/student/Downloads/SOFTWARE NEW/Software-Eng-Project/src/dotenv.env")  # Adjust path if necessary

# Print the loaded environment variables for debugging
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))

# Create the Supabase client
try:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and key must be set in the environment variables.")

    supabase_client: supabase.Client = supabase.create_client(supabase_url, supabase_key)
    print("Supabase client created successfully.")
except Exception as e:
    print(f"Error creating Supabase client: {e}")

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
    # Play action screen will be built after F5 is pressed on player entry screen (see on_f5 function in src/player_entry.py)
    root.after(3000, splash.destroy)
    root.after(3000, player_entry.build, root, users, network)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()


