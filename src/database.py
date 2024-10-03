import psycopg2
from psycopg2 import sql

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    'password': 'student',  # Uncomment this line if password is required
    'host': 'localhost',    # Uncomment if needed
    'port': '5432'          # Uncomment if needed
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

    def table_exists(self, table_name):
        """Check if the table already exists in the database."""
        self.cursor.execute("""
            SELECT EXISTS (
                SELECT FROM pg_catalog.pg_tables
                WHERE schemaname = 'public' AND tablename = %s
            );
        """, (table_name,))
        return self.cursor.fetchone()[0]

    def create_table(self):
        table_name = 'players'
        try:
            # Check if the table exists
            if not self.table_exists(table_name):
                # If it doesn't exist, create the table
                self.cursor.execute('''
                    CREATE TABLE players (
                        id INT PRIMARY KEY,
                        codename VARCHAR(30) UNIQUE
                    );
                ''')
                self.conn.commit()
                print(f"Table '{table_name}' created successfully.")

                self.cursor.execute('''
                ALTER TABLE players ADD CONSTRAINT unique_user_id UNIQUE (id);
                ALTER TABLE players ADD CONSTRAINT unique_codename UNIQUE (codename);
                '''
                )
                self.conn.commit()  
            else:
                print(f"Table '{table_name}' already exists. No action taken.")

        except Exception as e:
            print(f"Error creating table or running additional SQL commands: {e}")

    def insert_player(self, player_id, codename):
        try:
            self.cursor.execute('''
                INSERT INTO players (id, codename)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;  -- Avoid duplicates based on ID
            ''', (player_id, codename))
            self.conn.commit()
            print("Player inserted successfully.")
        except Exception as e:
            print(f"Error inserting player: {e}")

    def fetch_all_players(self):
        try:
            self.cursor.execute("SELECT * FROM players;")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching players: {e}")
            return []

    def fetch_player_by_id(self, player_id):
        """Fetch a player by their ID."""
        try:
            self.cursor.execute("SELECT * FROM players WHERE id = %s;", (player_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching player: {e}")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
