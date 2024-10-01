import psycopg2
from psycopg2 import sql

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    # Uncomment the following lines if needed
    # 'password': 'student',
    # 'host': 'localhost',
    # 'port': '5432'
}

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**connection_params)
            self.cursor = self.conn.cursor()
            print("Connected to the database.")
        except Exception as error:
            print(f"Error connecting to PostgreSQL database: {error}")

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INT PRIMARY KEY,
                    codename VARCHAR(30)
                );
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def insert_player(self, player_id, codename):
        try:
            self.cursor.execute('''
                INSERT INTO players (id, codename)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;  -- Avoid duplicates
            ''', (player_id, codename))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting player: {e}")

    def fetch_all_players(self):
        try:
            self.cursor.execute("SELECT * FROM players;")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching players: {e}")
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
