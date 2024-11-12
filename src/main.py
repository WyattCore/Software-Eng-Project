#Module to handle UDP networking for the Photon laser tag system communication between the control console and the packs.

from typing import Dict, List
import socket
import time

from user import User

# Defining constants for transmitting and receiving codes
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 53
GREEN_BASE_SCORED_CODE: int = 43
BUFFER_SIZE: int = 1024
GAME_TIME_SECONDS: int = 360 # Seconds
BROADCAST_ADDRESS: str = "127.0.0.1"
RECEIVE_ALL_ADDRESS: str = "0.0.0.0"
TRANSMIT_PORT: int = 7500
RECEIVE_PORT: int = 7501

class Networking:
    def __init__(self) -> None:
        pass
    
    def set_sockets(self) -> bool:
        # Set up transmit and receive sockets
        try:
            self.transmit_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receive_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receive_socket.bind((RECEIVE_ALL_ADDRESS, RECEIVE_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def close_sockets(self) -> bool:
        # Close transmit and receive sockets
        try:
            self.transmit_socket.close()
            self.receive_socket.close()
            return True
        except Exception as e:
            print(e)
            return False

    def transmit_equipment_code(self, equipment_code: str) -> bool:
        # Enable broadcasts at the syscall level and priviledged process
        # Transmit provided equipment code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(equipment_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
    
    def transmit_start_game_code(self) -> bool:
        # Transmit start game code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(START_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            print("Transmitted")
            return True
        except Exception as e:
            print(e)
            return False
            
    def transmit_end_game_code(self) -> bool:
        # Transmit end game code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(END_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def traffic_listener(self) -> None:
        print("Listening for traffic")
        while True:
            try:
                received_data, address = self.receive_socket.recvfrom(BUFFER_SIZE)
                decoded_data = received_data.decode("utf-8")

                print(f"Received data: {decoded_data} from {address}")

                if decoded_data == str(END_GAME_CODE):
                    print("Game is over, done listening")
                    break
            except Exception as e:
                print(f"Error while receiving data: {e}")
                break
   
   
        # Transmit player hit code to the broadcast address
       
       
        # While the game is still running, receive data from the receive socket
        
            # If the red base is hit, attribute 100 points to green team and vice versa
            # If player was hit instead, attribute 10 points to the attacker
            
        # Once game ends, transmit end game code 3 times
       
    
