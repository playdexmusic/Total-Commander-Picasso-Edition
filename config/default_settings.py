
# default_settings.py
# This file contains the default settings for the application

import configparser
import os

DEFAULT_SETTINGS = {
    'General': {
        'maximizeOnStartup': True,
        'expandSectionsOnStartup': False,
    },
    'Logs': {
        'enableVerboseLogging': False,
        'saveLogsToFile': True,
        'maxLogFileSize': 10,  # in MB
        'rotateLogs': True,
        'compressOldLogs': False,
    },
    'Font': {
        'fontFamily': 'Arial',
        'fontSize': 12,
        'fontBold': False,
        'fontItalic': False,
        'fontUnderline': False,
        'fontColor': '#000000',  # Default black
        'fontSmoothing': True,
    },
    'Internal': {
        'cancelBehavior': 'go_to_main_app',  # Default behavior on cancel
    }
}



def create_default_ini(config_path='config/settings.ini'):
    # Ensure the config directory exists
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    config = configparser.ConfigParser()

    # Add the default settings to the config (excluding Internal settings)
    for section, settings in DEFAULT_SETTINGS.items():
        if section != 'Internal':  # Skip Internal settings
            config[section] = {}
            for key, value in settings.items():
                config[section][key] = str(value)

    # Write the settings to the ini file
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    print(f'Default settings.ini created at {config_path}')
