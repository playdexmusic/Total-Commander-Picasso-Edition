from config.shared_imports import *  # Import everything from shared_imports.py

class FontSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Initializing FontSettings UI.")
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components for the Font Settings section."""
        font_layout = QFormLayout(self)

        # Font Family
        self.font_family = QFontComboBox()
        self.font_family.setCurrentFont(QFont(DEFAULT_SETTINGS['Font']['fontFamily']))
        self.font_family.setToolTip("Select the font family to use in the application.")

        # Font Size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        self.font_size.setValue(DEFAULT_SETTINGS['Font']['fontSize'])
        self.font_size.setToolTip("Set the font size.")

        # Font Styles
        self.font_bold = QCheckBox("Bold")
        self.font_bold.setChecked(DEFAULT_SETTINGS['Font']['fontBold'])
        self.font_bold.setToolTip("Toggle bold font style.")

        self.font_italic = QCheckBox("Italic")
        self.font_italic.setChecked(DEFAULT_SETTINGS['Font']['fontItalic'])
        self.font_italic.setToolTip("Toggle italic font style.")

        self.font_underline = QCheckBox("Underline")
        self.font_underline.setChecked(DEFAULT_SETTINGS['Font']['fontUnderline'])
        self.font_underline.setToolTip("Toggle underline font style.")

        # Font Color
        self.font_color = QPushButton("Choose Font Color")
        self.font_color.setStyleSheet(f"background-color: {DEFAULT_SETTINGS['Font']['fontColor']}")
        self.font_color.setToolTip("Select the font color.")
        self.font_color.clicked.connect(self.choose_font_color)

        # Font Smoothing
        self.font_smoothing = QCheckBox("Enable Font Smoothing")
        self.font_smoothing.setChecked(DEFAULT_SETTINGS['Font']['fontSmoothing'])
        self.font_smoothing.setToolTip("Toggle font smoothing for better readability.")

        # Font Preview
        self.font_preview = QLabel("The quick brown fox jumps over the lazy dog")
        self.update_font_preview()
        self.font_preview.setToolTip("Preview of the selected font settings.")

        # Add widgets to layout
        font_layout.addRow(QLabel("Font Family:"), self.font_family)
        font_layout.addRow(QLabel("Font Size:"), self.font_size)
        font_layout.addRow(self.font_bold)
        font_layout.addRow(self.font_italic)
        font_layout.addRow(self.font_underline)
        font_layout.addRow(QLabel("Font Color:"), self.font_color)
        font_layout.addRow(self.font_smoothing)
        font_layout.addRow(QLabel("Preview:"), self.font_preview)

    def choose_font_color(self):
        """Open a color picker dialog to select the font color."""
        color = QColorDialog.getColor()
        if color.isValid():
            logger.info(f"Selected font color: {color.name()}")
            self.font_color.setStyleSheet(f"background-color: {color.name()}")
            self.update_font_preview()

    def update_font_preview(self):
        """Update the font preview based on the current settings."""
        font = QFont(self.font_family.currentFont())
        font.setPointSize(self.font_size.value())
        font.setBold(self.font_bold.isChecked())
        font.setItalic(self.font_italic.isChecked())
        font.setUnderline(self.font_underline.isChecked())
        self.font_preview.setFont(font)
        self.font_preview.setStyleSheet(f"color: {self.font_color.palette().button().color().name()}")
        logger.info("Font preview updated.")

    def load_settings(self):
        """Load settings from the configuration."""
        self.font_family.setCurrentFont(QFont(DEFAULT_SETTINGS['Font']['fontFamily']))
        self.font_size.setValue(DEFAULT_SETTINGS['Font']['fontSize'])
        self.font_bold.setChecked(DEFAULT_SETTINGS['Font']['fontBold'])
        self.font_italic.setChecked(DEFAULT_SETTINGS['Font']['fontItalic'])
        self.font_underline.setChecked(DEFAULT_SETTINGS['Font']['fontUnderline'])
        self.font_color.setStyleSheet(f"background-color: {DEFAULT_SETTINGS['Font']['fontColor']}")
        self.font_smoothing.setChecked(DEFAULT_SETTINGS['Font']['fontSmoothing'])
        self.update_font_preview()
        logger.info("Font settings loaded.")

    def save_settings(self):
        """Save the current settings to the configuration."""
        DEFAULT_SETTINGS['Font']['fontFamily'] = self.font_family.currentFont().family()
        DEFAULT_SETTINGS['Font']['fontSize'] = self.font_size.value()
        DEFAULT_SETTINGS['Font']['fontBold'] = self.font_bold.isChecked()
        DEFAULT_SETTINGS['Font']['fontItalic'] = self.font_italic.isChecked()
        DEFAULT_SETTINGS['Font']['fontUnderline'] = self.font_underline.isChecked()
        DEFAULT_SETTINGS['Font']['fontColor'] = self.font_color.palette().button().color().name()
        DEFAULT_SETTINGS['Font']['fontSmoothing'] = self.font_smoothing.isChecked()
        logger.info("Font settings saved.")

# Main function to run this module standalone for testing
if __name__ == '__main__':
    logger.info("Running FontSettings module standalone for testing.")
    app = QApplication(sys.argv)
    window = FontSettings()
    window.show()
    sys.exit(app.exec())
