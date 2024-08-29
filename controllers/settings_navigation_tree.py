
from config.shared_imports import *  # Adjusted to import from the config directory

# Custom Tree Widget for the Navigation
class SettingsNavigationTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)

    # Additional methods and customization here
