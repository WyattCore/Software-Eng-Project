class User:
    def __init__(self, username: str, team: str):
        self.username = username 
        self.team = team          

    def __repr__(self):
        return f"User(username={self.username}, team={self.team})"

    def get_info(self) -> str:
        """Returns a string with user information."""
        return f"{self.username} (Team: {self.team})"
