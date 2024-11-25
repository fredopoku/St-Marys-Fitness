"""
Main entry point for St Mary's Fitness Management System.
This script initializes and launches the application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils import Config

def main():
    """Main function to initialize and start the application."""
    # Load application configuration
    config = Config.load()

    # Initialize the application
    app = QApplication(sys.argv)
    main_window = MainWindow(config)

    # Display the main window
    main_window.show()

    # Start the application's event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
