from config.shared_imports import *
from sections.settings_window import SettingsWindow  # Directly import SettingsWindow

APP_NAME = "Total Commander: Picasso Edition"

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

def main():
    clear_console()  # Clear the console on startup
    logger.info(f"Launching {APP_NAME}...")  # Use logger from shared imports
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
