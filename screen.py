import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

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

if __name__ == "__main__":
    laser_tag_app = QApplication(sys.argv)

    # Create and show the splash screen
    splash = SplashScreen()
    splash.show()

    # Start the application event loop
    sys.exit(laser_tag_app.exec())