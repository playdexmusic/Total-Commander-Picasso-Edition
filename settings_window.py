import sys
import logging
import configparser
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter, QTreeWidget, QStackedWidget, QPushButton, QHBoxLayout, QTreeWidgetItem, QCheckBox, QFormLayout, QMessageBox

from config.default_settings import DEFAULT_SETTINGS, create_default_ini
from config.shared_imports import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Total Commander: Picasso Edition Settings')
        self.resize(1200, 800)

        # Load internal setting for Cancel button behavior
        self.cancel_behavior = DEFAULT_SETTINGS['Internal']['cancelBehavior']

        # Initialize configuration parser
        self.config = configparser.ConfigParser()
        self.config_path = 'config/settings.ini'

        if not os.path.exists(self.config_path):
            logging.info('No .ini file found, creating default settings.ini using Python config.')
            create_default_ini(self.config_path)

        self.config.read(self.config_path)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # Hide header if not needed
        main_layout.addWidget(self.tree)

        self.add_tree_items()

        self.section_stack = QStackedWidget()
        self.add_sections()

        splitter.addWidget(self.tree)
        splitter.addWidget(self.section_stack)
        splitter.setSizes([100, 850])  # Adjusted values to make the left panel narrower
        main_layout.addWidget(splitter)

        button_layout = QHBoxLayout()
        restore_button = QPushButton('Restore Defaults')
        apply_button = QPushButton('Apply')
        cancel_button = QPushButton('Cancel')
        ok_button = QPushButton('OK')
        button_layout.addWidget(restore_button)
        button_layout.addStretch()
        button_layout.addWidget(apply_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        main_layout.addLayout(button_layout)

        # Connect signals
        self.tree.currentItemChanged.connect(self.display_section)
        apply_button.clicked.connect(self.apply_settings)
        cancel_button.clicked.connect(self.cancel_changes)
        ok_button.clicked.connect(self.ok_and_close)
        restore_button.clicked.connect(self.restore_defaults)

        # Load initial settings
        self.load_settings()

        # Apply initial settings
        if self.maximize_on_startup.isChecked():
            self.showMaximized()
        if self.expand_sections_on_startup.isChecked():
            self.expand_all_sections()

    def add_tree_items(self):
        # Clear the tree first to avoid any unwanted items
        self.tree.clear()

        # Define the hierarchical structure with the desired order
        sections = {
            'General': ['Alerts', 'Fonts', 'Language', 'Logs', 'Shortcuts'],
            'View': ['Menu', 'Panel', 'Themes', 'Toolbar', 'UI'],
            'Table': ['Columns', 'Results', 'Search'],
            'Database': ['Directories', 'Extensions', 'Indexes'],  
            'Setup': ['Apps', 'Bookmarks', 'Filters', 'Groups', 'Highlights', 'Nukes', 'Paths', 'Rules', 'Sections', 'Sites', 'Skiplist', 'Tags'],
        }

        self.tree_items = {}

        # Add the sections and subsections in the defined order
        for section, subsections in sections.items():
            logging.info(f'Adding section: {section}')  # Debugging line
            section_item = QTreeWidgetItem([section])
            self.tree_items[section] = section_item
            self.tree.addTopLevelItem(section_item)
            
            for sub_section in subsections:
                logging.info(f'Adding sub-section: {sub_section}')  # Debugging line
                sub_item = QTreeWidgetItem([sub_section])
                section_item.addChild(sub_item)
                self.tree_items[sub_section] = sub_item
                
        logging.info('Tree items added in specified order.')

    def add_sections(self):
        # Create a widget for the General section
        general_widget = QWidget()
        general_layout = QFormLayout(general_widget)

        # Add checkboxes for the General section
        self.maximize_on_startup = QCheckBox("Maximize on Startup")
        self.expand_sections_on_startup = QCheckBox("Expand Sections on Startup")

        general_layout.addRow(self.maximize_on_startup)
        general_layout.addRow(self.expand_sections_on_startup)

        # Add the General section widget to the stack
        self.section_stack.addWidget(general_widget)

        logging.info('General section with checkboxes added.')

    def load_settings(self):
        # Load settings from .ini file
        if self.config.has_section('General'):
            self.maximize_on_startup.setChecked(self.config.getboolean('General', 'maximizeOnStartup', fallback=False))
            self.expand_sections_on_startup.setChecked(self.config.getboolean('General', 'expandSectionsOnStartup', fallback=False))
            logging.info('Settings loaded from .ini file.')
        else:
            # If no settings are found in the .ini, fall back to defaults
            self.maximize_on_startup.setChecked(DEFAULT_SETTINGS['General']['maximizeOnStartup'])
            self.expand_sections_on_startup.setChecked(DEFAULT_SETTINGS['General']['expandSectionsOnStartup'])
            logging.info('No settings found in .ini, loaded defaults.')

    def apply_settings(self):
        try:
            # Save current settings to the .ini file
            if not self.config.has_section('General'):
                self.config.add_section('General')
            self.config.set('General', 'maximizeOnStartup', str(self.maximize_on_startup.isChecked()))
            self.config.set('General', 'expandSectionsOnStartup', str(self.expand_sections_on_startup.isChecked()))

            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)

            logging.info('Settings applied and saved to the .ini file.')

            # Show info alert on success
            QMessageBox.information(self, 'Settings Applied', 'Your settings have been successfully applied.')

        except Exception as e:
            logging.error('Failed to save settings: %s', e)
            # Show warning alert on error
            QMessageBox.warning(self, 'Warning', f'Failed to save settings: {e}')

    def restore_defaults(self):
        # Restore settings to default values and apply them
        self.maximize_on_startup.setChecked(DEFAULT_SETTINGS['General']['maximizeOnStartup'])
        self.expand_sections_on_startup.setChecked(DEFAULT_SETTINGS['General']['expandSectionsOnStartup'])
        logging.info('Default settings restored.')

        # Optionally save the default settings to the .ini file immediately
        self.apply_settings()

    def cancel_changes(self):
        # Revert to the last saved settings
        self.load_settings()
        logging.info('Changes canceled and settings reverted.')

        if self.cancel_behavior == 'go_to_main_app':
            logging.info('Transitioning to the main application...')
            # Placeholder for transitioning to the main app
        else:
            self.close()  # Exit the application

    def ok_and_close(self):
        # Apply settings and close the application
        self.apply_settings()
        self.close()
        logging.info('Settings applied and window closed.')

    def expand_all_sections(self):
        for section_item in self.tree_items.values():
            section_item.setExpanded(True)
        logging.info('All sections expanded.')

    def display_section(self, current, previous):
        if current:
            section_name = current.text(0)
            logging.info('Displaying section: %s', section_name)
            # You can expand this to handle each sub-section uniquely

def main():
    logging.info('Starting the application...')
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    logging.info('Application started successfully.')
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
