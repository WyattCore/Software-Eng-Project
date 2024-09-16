##screen.py but updated with a table and database using sqlite3
import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout,  QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer


##deletes info in database
def clear_data():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()

#connect to SQLite database
conn = sqlite3.connect('players.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')
conn.commit();

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Splash Screen")
        self.label = QLabel(self)
        self.logo = QPixmap("logo.jpg")  # Load image
        self.showMaximized()

        QTimer.singleShot(3000, self.show_player_entry_screen) # Goes to player entry screen

    def resizeEvent(self, event):
        # Scales the image
        scaled_logo = self.logo.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(scaled_logo)

        # Center the image in the window
        self.label.resize(scaled_logo.width(), scaled_logo.height())
        self.label.move((self.width() - self.label.width()) // 2, (self.height() - self.label.height()) // 2)

    def show_player_entry_screen(self):
        # Close the splash screen
        self.close()

        # Open the player entry screen
        self.player_entry = PlayerEntryScreen()
        self.player_entry.showMaximized()

class PlayerEntryScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Player Entry Screen")

        # Label for the player entry screen
        self.label = QLabel("Enter Player Name", self)
        self.label.move(200, 200)

        ##player entry UI elements
        self.name_input = QLineEdit(self)
        self.name_input.move(300, 200)
        self.submit_button = QPushButton("Submit", self);
        self.submit_button.move(300, 225)
        ##Name display table
        self.table = QTableWidget(1,1)
        self.table.setHorizontalHeaderLabels(["Player"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Make the table non-editable

        self.table.move(200, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        ## connect button to insert player function
        self.submit_button.clicked.connect(self.insert_player)

        

    def insert_player(self):
        name = self.name_input.text()
        if name:
            cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
            conn.commit();
            self.name_input.clear()
            self.fill_table_data()

            
        ##method to fill table with data base info
    def fill_table_data(self):
        self.table.setRowCount(0)

        cursor.execute("SELECT * FROM players")
        rows = cursor.fetchall()

        for row in rows:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, QTableWidgetItem(row[1]))
            print(QTableWidgetItem(row[1]))


    
        

if __name__ == "__main__":
    laser_tag_app = QApplication(sys.argv)

    ##deletes info in database
    laser_tag_app.aboutToQuit.connect(clear_data)

    # Create and show the splash screen
    splash = SplashScreen()
    splash.show()

    # Start the application event loop
    sys.exit(laser_tag_app.exec())

    # #close the connection
    # conn.close()
    
