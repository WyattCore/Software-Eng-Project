class User:
    row: int 
    equipment_id: int
    user_id: int
    codename: str  # Updated from username to codename
    game_score: int
    has_hit_base: bool
    
    # Passing in row of entry from GUI, equipment ID, user ID, and codename
    def __init__(self, row: int, equipment_id: int, user_id: int, codename: str) -> None:
        self.row = row
        self.equipment_id = equipment_id
        self.user_id = user_id
        self.codename = codename  # Updated from username to codename
        self.game_score = 0
        self.has_hit_base = False

    # String representation of User object
    def __str__(self) -> str:
        return (f"Codename: {self.codename}\n"  # Updated from username to codename
                f"Equipment ID: {self.equipment_id}\n"
                f"User ID: {self.user_id}\n"
                f"Game Score: {self.game_score}\n"
                f"Has Hit Base: {self.has_hit_base}\n\n")
