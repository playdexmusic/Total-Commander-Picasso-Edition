import logging
import sys
import os

# Add the root directory of the project to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# ---------------------------
# PyQt6 Core Modules
# ---------------------------
from PyQt6.QtCore import Qt, QEvent, QTimer, pyqtSignal, QUrl
from PyQt6.QtGui import QIcon, QFont, QColor, QCursor, QPalette
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QTreeWidget,
    QTreeWidgetItem, QStackedWidget, QPushButton, QCheckBox, QFormLayout, QMessageBox, QLabel,
    QLineEdit, QComboBox, QTextEdit, QSpinBox, QColorDialog, QFontComboBox    # Ensure all necessary widgets are imported
)

# ---------------------------
# Project-Specific Modules
# ---------------------------
from config.default_settings import DEFAULT_SETTINGS, create_default_ini

# ---------------------------
# Standard Python Libraries
# ---------------------------
import json
import re
import random
import datetime
from collections import defaultdict, OrderedDict
import subprocess
import configparser  # Specific to settings management

# ---------------------------
# Logging Setup
# ---------------------------
from config.log_manager import logger  # Import the custom logger setup

# ---------------------------
# Example Logging Usage
# ---------------------------
logger.debug("shared_imports.py loaded successfully.")
