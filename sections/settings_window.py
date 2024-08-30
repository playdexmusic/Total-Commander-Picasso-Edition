from config.shared_imports import *
from sections.settings_navigation_tree import SettingsNavigationTree
from sections.settings.general.font_settings import FontSettings

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
            logger.info('No .ini file found, creating default settings.ini using Python config.')
            create_default_ini(self.config_path)

        self.config.read(self.config_path)

        # Setup UI components
        self.setup_ui()

        # Load initial settings (after sections are added)
        self.load_settings()

        # Apply initial settings
        self.apply_initial_settings()

    def setup_ui(self):
        """Set up the main UI components."""
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Use SettingsNavigationTree for the navigation tree
        self.tree = SettingsNavigationTree()
        splitter.addWidget(self.tree)

        self.section_stack = QStackedWidget()
        splitter.addWidget(self.section_stack)
        splitter.setSizes([100, 850])  # Adjusted values to make the left panel narrower
        main_layout.addWidget(splitter)

        self.setup_buttons(main_layout)

        # Connect signals
        self.tree.currentItemChanged.connect(self.display_section)

        # Add sections to the stacked widget (Only the widgets, not the tree items)
        self.add_sections()

    def setup_buttons(self, layout):
        """Set up the bottom action buttons."""
        button_layout = QHBoxLayout()
        restore_button = QPushButton('Restore Defaults')
        apply_button = QPushButton('Apply')
        cancel_button = QPushButton('Cancel')
        ok_button = QPushButton('OK')

        restore_button.clicked.connect(self.restore_defaults)
        apply_button.clicked.connect(self.apply_settings)
        cancel_button.clicked.connect(self.cancel_changes)
        ok_button.clicked.connect(self.ok_and_close)

        button_layout.addWidget(restore_button)
        button_layout.addStretch()
        button_layout.addWidget(apply_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)

    def add_sections(self):
        """Create and add section widgets to the stacked widget."""
        self.sections_widgets = {}

        sections = {
            'General': ['Alerts', 'Fonts', 'Language', 'Logs', 'Shortcuts'],
            'View': ['Menu', 'Panel', 'Themes', 'Toolbar', 'UI'],
            'Table': ['Columns', 'Results', 'Search'],
            'Database': ['Directories', 'Extensions', 'Indexes'],  
            'Setup': ['Apps', 'Bookmarks', 'Filters', 'Groups', 'Highlights', 'Nukes', 'Paths', 'Rules', 'Sections', 'Sites', 'Skiplist', 'Tags'],
        }

        for section, subsections in sections.items():
            for subsection in subsections:
                if subsection == 'Fonts':
                    widget = FontSettings()
                elif subsection == 'Logs':
                    widget = self.create_logs_section()
                elif subsection == 'Alerts':
                    widget = self.create_general_section()
                else:
                    widget = self.create_placeholder_section(subsection)

                self.section_stack.addWidget(widget)
                self.sections_widgets[subsection] = widget

        logger.info('Sections added to the stack.')

    def create_general_section(self):
        """Create the General section widget."""
        general_widget = QWidget()
        general_layout = QFormLayout(general_widget)

        self.maximize_on_startup = QCheckBox("Maximize on Startup")
        self.expand_sections_on_startup = QCheckBox("Expand Sections on Startup")

        general_layout.addRow(self.maximize_on_startup)
        general_layout.addRow(self.expand_sections_on_startup)

        return general_widget

    def create_placeholder_section(self, subsection_name):
        """Create a placeholder section widget for unimplemented subsections."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(f"{subsection_name} settings are not yet implemented.")
        layout.addWidget(label)
        return widget

    def create_logs_section(self):
        """Create the enhanced Logs section widget."""
        logs_widget = QWidget()
        logs_layout = QVBoxLayout(logs_widget)

        # Log File Options
        logs_layout.addWidget(QLabel("Log File Options"))

        self.enable_verbose_logging = QCheckBox("Enable verbose logging")
        self.enable_verbose_logging.setToolTip("Toggle detailed logging output for troubleshooting.")

        self.save_logs_to_file = QCheckBox("Save logs to file")
        self.save_logs_to_file.setToolTip("Save logs to a file for later review.")

        self.max_log_file_size = QSpinBox()
        self.max_log_file_size.setSuffix(" MB")
        self.max_log_file_size.setRange(1, 100)
        self.max_log_file_size.setValue(10)
        self.max_log_file_size.setToolTip("Set the maximum size for log files before rotation.")

        self.rotate_logs = QCheckBox("Enable log rotation")
        self.rotate_logs.setToolTip("Automatically rotate log files when they reach the maximum size.")

        self.compress_old_logs = QCheckBox("Compress old log files")
        self.compress_old_logs.setToolTip("Compress old log files to save disk space.")

        logs_layout.addWidget(self.enable_verbose_logging)
        logs_layout.addWidget(self.save_logs_to_file)
        logs_layout.addWidget(QLabel("Max Log File Size:"))
        logs_layout.addWidget(self.max_log_file_size)
        logs_layout.addWidget(self.rotate_logs)
        logs_layout.addWidget(self.compress_old_logs)

        # Log Viewing
        logs_layout.addWidget(QLabel("View Recent Logs"))

        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setToolTip("View recent log entries.")
        logs_layout.addWidget(self.log_viewer)

        # Log Filtering
        logs_layout.addWidget(QLabel("Search and Filter Logs"))

        self.search_logs = QLineEdit()
        self.search_logs.setPlaceholderText("Search logs...")
        self.search_logs.setToolTip("Search log entries by keywords.")
        logs_layout.addWidget(self.search_logs)

        self.filter_log_level = QComboBox()
        self.filter_log_level.addItems(["All", "INFO", "WARNING", "ERROR", "DEBUG"])
        self.filter_log_level.setToolTip("Filter logs by severity level.")
        logs_layout.addWidget(QLabel("Filter by log level:"))
        logs_layout.addWidget(self.filter_log_level)

        # Connect signals for search and filter functionality
        self.search_logs.textChanged.connect(self.update_log_view)
        self.filter_log_level.currentIndexChanged.connect(self.update_log_view)

        return logs_widget

    def update_log_view(self):
        """Update the log viewer based on the search and filter criteria."""
        log_file_path = "logs/application.log"
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                logs = file.readlines()

            # Apply search filter
            search_term = self.search_logs.text().lower()
            filtered_logs = [log for log in logs if search_term in log.lower()]

            # Apply log level filter
            selected_level = self.filter_log_level.currentText()
            if selected_level != "All":
                filtered_logs = [log for log in filtered_logs if selected_level in log]

            self.log_viewer.setPlainText("".join(filtered_logs))
        else:
            self.log_viewer.setPlainText("No logs available.")

    def load_settings(self):
        """Load settings from the .ini file."""
        if self.config.has_section('General'):
            self.maximize_on_startup.setChecked(self.config.getboolean('General', 'maximizeOnStartup', fallback=False))
            self.expand_sections_on_startup.setChecked(self.config.getboolean('General', 'expandSectionsOnStartup', fallback=False))
            logger.info('Settings loaded from .ini file.')

        if self.config.has_section('Logs'):
            self.enable_verbose_logging.setChecked(self.config.getboolean('Logs', 'enableVerboseLogging', fallback=False))
            self.save_logs_to_file.setChecked(self.config.getboolean('Logs', 'saveLogsToFile', fallback=False))
            self.max_log_file_size.setValue(self.config.getint('Logs', 'maxLogFileSize', fallback=10))
            self.rotate_logs.setChecked(self.config.getboolean('Logs', 'rotateLogs', fallback=False))
            self.compress_old_logs.setChecked(self.config.getboolean('Logs', 'compressOldLogs', fallback=False))
            logger.info('Log settings loaded from .ini file.')

        if 'Fonts' in self.sections_widgets:
            self.sections_widgets['Fonts'].load_settings()
            logger.info('Font settings loaded from .ini file.')

    def restore_log_defaults(self):
        """Restore log settings to default values."""
        self.enable_verbose_logging.setChecked(False)
        self.save_logs_to_file.setChecked(True)
        self.max_log_file_size.setValue(10)
        self.rotate_logs.setChecked(True)
        self.compress_old_logs.setChecked(False)
        logger.info('Default log settings restored.')

    def apply_initial_settings(self):
        """Apply settings that should take effect on startup."""
        if self.maximize_on_startup.isChecked():
            self.showMaximized()
        if self.expand_sections_on_startup.isChecked():
            self.expand_all_sections()
        logger.info('Initial settings applied.')

    def apply_settings(self):
        """Save and apply current settings."""
        try:
            # Save General settings
            self.save_general_settings()

            # Save Logs settings
            self.save_logs_settings()

            # Save Font settings
            if 'Fonts' in self.sections_widgets:
                self.sections_widgets['Fonts'].save_settings()

            # Write all settings to the config file
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)

            logger.info('Settings applied and saved to the .ini file.')
            QMessageBox.information(self, 'Settings Applied', 'Your settings have been successfully applied.')

        except Exception as e:
            logger.error('Failed to save settings: %s', e)
            QMessageBox.warning(self, 'Warning', f'Failed to save settings: {e}')

    def save_general_settings(self):
        """Save General settings."""
        if not self.config.has_section('General'):
            self.config.add_section('General')

        self.config.set('General', 'maximizeOnStartup', str(self.maximize_on_startup.isChecked()))
        self.config.set('General', 'expandSectionsOnStartup', str(self.expand_sections_on_startup.isChecked()))

    def save_logs_settings(self):
        """Save Logs settings."""
        if not self.config.has_section('Logs'):
            self.config.add_section('Logs')

        self.config.set('Logs', 'enableVerboseLogging', str(self.enable_verbose_logging.isChecked()))
        self.config.set('Logs', 'saveLogsToFile', str(self.save_logs_to_file.isChecked()))
        self.config.set('Logs', 'maxLogFileSize', str(self.max_log_file_size.value()))
        self.config.set('Logs', 'rotateLogs', str(self.rotate_logs.isChecked()))
        self.config.set('Logs', 'compressOldLogs', str(self.compress_old_logs.isChecked()))

    def restore_defaults(self):
        """Restore settings to default values and apply them."""
        self.restore_general_defaults()
        self.restore_log_defaults()

        if 'Fonts' in self.sections_widgets:
            self.sections_widgets['Fonts'].load_settings()  # This will restore the font settings

        logger.info('Default settings restored.')
        self.apply_settings()

    def restore_general_defaults(self):
        """Restore general settings to default values."""
        self.maximize_on_startup.setChecked(DEFAULT_SETTINGS['General']['maximizeOnStartup'])
        self.expand_sections_on_startup.setChecked(DEFAULT_SETTINGS['General']['expandSectionsOnStartup'])

    def cancel_changes(self):
        """Revert to the last saved settings."""
        self.load_settings()
        logger.info('Changes canceled and settings reverted.')

        if self.cancel_behavior == 'go_to_main_app':
            logger.info('Transitioning to the main application...')
        else:
            self.close()  # Exit the application

    def ok_and_close(self):
        """Apply settings and close the application."""
        self.apply_settings()
        self.close()
        logger.info('Settings applied and window closed.')

    def expand_all_sections(self):
        """Expand all sections in the navigation tree."""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            item.setExpanded(True)
        logger.info('All sections expanded.')

    def display_section(self, current, previous):
        """Display the selected section in the stacked widget."""
        if current:
            section_name = current.text(0)
            logger.info('Displaying section: %s', section_name)
            if section_name in self.sections_widgets:
                self.section_stack.setCurrentWidget(self.sections_widgets[section_name])

def main():
    logger.info('Starting the application...')
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    logger.info('Application started successfully.')
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
