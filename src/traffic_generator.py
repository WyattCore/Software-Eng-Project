import socket
import random
import time
from typing import Tuple

# Declaring constants for socket communication info
BUFFER_SIZE: int = 1024
SERVER_ADDRESS_PORT: Tuple[str, int] = ("127.0.0.1", 7501)
CLIENT_ADDRESS_PORT: Tuple[str, int] = ("127.0.0.1", 7500)
START_CODE: str = "202"
END_CODE: str = "221"

# Function to get user input for player IDs
def get_player_id(color: str, player_number: int) -> str:
    return input(f"Enter equipment id of {color} player {player_number} ==> ")

# Function to wait for start code transmission from game software
def wait_for_start(sock: socket.socket) -> None:
    print("\nWaiting for start from game software")
    received_data: str = ""
    while received_data != START_CODE:
        received_data, address = sock.recvfrom(BUFFER_SIZE)
        received_data = received_data.decode("utf-8")
        print(f"Received from game software: {received_data}")

def main() -> None:
    # Print instructions, get plater IDs
    print("This program will generate some test traffic for 2 players\n"
            "on the blue team as well as 2 players on the red team.\n")
    
    print("Once the start code is received from the game software,\n"
            "the program will randomly select 2 players. The format\n"
            "of the message is player1:player2, meaning that player1\n"
            "has hit player2. If you wish to exit, type 'y' when prompted.\n")

    blue1: str = get_player_id("blue", 1)
    blue2: str = get_player_id("blue", 2)
    red1: str = get_player_id("red", 1)
    red2: str = get_player_id("red", 2)

    # Create sockets for server-side receiving and client-side transmitting
    UDPServerSocketReceive: socket.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocketReceive.bind(SERVER_ADDRESS_PORT)
    UDPClientSocketTransmit: socket.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    wait_for_start(UDPServerSocketReceive)

    while True:
        # Randomly select a blue and red player
        blueplayer: str = blue1 if random.randint(1, 2) == 1 else blue2
        redplayer: str = red1 if random.randint(1, 2) == 1 else red2
        message: str = f"{blueplayer}:{redplayer}" if random.randint(1,2) == 1 else f"{redplayer}:{blueplayer}"
        print(f"\n{message}")

        # If user wishes to continue, send message to game software
        if input("Exit? (y/n): ") == "y":
            exit(0)
        print(f"Sending to game software: {message}")
        UDPClientSocketTransmit.sendto(str.encode(str(message)), CLIENT_ADDRESS_PORT)

        # Receive data from game software
        received_data: str
        address: Tuple[str, int]
        received_data, address = UDPServerSocketReceive.recvfrom(BUFFER_SIZE)
        received_data = received_data.decode("utf-8")
        print(f"Received from game software: {received_data}")

        # If received data is the end code, break out of loop
        if received_data == END_CODE:
            break
        time.sleep(random.randint(1,3))

    print("Program complete")

if __name__ == "__main__":
    main()
