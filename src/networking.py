from typing import Callable
import socket
import time

# Defining constants for transmitting and receiving codes
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 53
GREEN_BASE_SCORED_CODE: int = 43
BUFFER_SIZE: int = 1024
GAME_TIME_SECONDS: int = 360  # Seconds
BROADCAST_ADDRESS: str = "127.0.0.1"
RECEIVE_ALL_ADDRESS: str = "0.0.0.0"
TRANSMIT_PORT: int = 7500
RECEIVE_PORT: int = 7501


class Networking:
    def __init__(self) -> None:
        self.transmit_socket: socket.socket = None
        self.receive_socket: socket.socket = None

    def set_sockets(self) -> bool:
        # Set up transmit and receive sockets
        try:
            self.transmit_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receive_socket.bind((RECEIVE_ALL_ADDRESS, RECEIVE_PORT))
            return True
        except Exception as e:
            print(f"Error setting up sockets: {e}")
            return False

    def close_sockets(self) -> bool:
        # Close transmit and receive sockets
        try:
            if self.transmit_socket:
                self.transmit_socket.close()
            if self.receive_socket:
                self.receive_socket.close()
            return True
        except Exception as e:
            print(f"Error closing sockets: {e}")
            return False

    def transmit_equipment_code(self, equipment_code: str) -> bool:
        # Transmit provided equipment code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str(equipment_code).encode(), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(f"Error transmitting equipment code: {e}")
            return False

    def transmit_start_game_code(self) -> bool:
        # Transmit start game code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str(START_GAME_CODE).encode(), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            print("Transmitted")
            return True
        except Exception as e:
            print(f"Error transmitting start game code: {e}")
            return False

    def transmit_end_game_code(self) -> bool:
        # Transmit end game code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str(END_GAME_CODE).encode(), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(f"Error transmitting end game code: {e}")
            return False

    def traffic_listener(self, update_scores_callback: Callable[[int, int], None]) -> None:
        print("Listening for traffic")
        while True:
            try:
                received_data, address = self.receive_socket.recvfrom(BUFFER_SIZE)
                decoded_data = received_data.decode("utf-8")

                print(f"Received data: {decoded_data} from {address}")

                if ":" in decoded_data:
                    shooter_id, target_id = map(int, decoded_data.split(":"))
                    update_scores_callback(shooter_id, target_id)

                if decoded_data == str(END_GAME_CODE):
                    print("Game over, listener stopped")
                    break
            except Exception as e:
                print(f"Error while receiving data: {e}")
                break

    def transmit_player_hit(self,target_id) -> bool:
        # Transmit player hit code to the broadcast address
        
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str(target_id).encode(), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(f"Error transmitting player hit: {e}")
            return False
