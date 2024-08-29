import logging
from logging.handlers import RotatingFileHandler
import os
import gzip
import shutil

# Configuration Variables
LOG_FILE = 'application.log'
LOG_DIR = 'logs'
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5  # Number of backup files to keep
LOG_LEVEL = logging.DEBUG  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Full path to the log file
log_file_path = os.path.join(LOG_DIR, LOG_FILE)

# Set up rotating file handler with compression for old logs
class GzipRotator(RotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        # Compress the most recent log file (backupCount - 1)
        log_files = sorted([f for f in os.listdir(LOG_DIR) if f.startswith(LOG_FILE)])
        if len(log_files) > BACKUP_COUNT:
            oldest_log = os.path.join(LOG_DIR, log_files[-(BACKUP_COUNT + 1)])
            with open(oldest_log, 'rb') as f_in:
                with gzip.open(f'{oldest_log}.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(oldest_log)

# Create the logger
logger = logging.getLogger('my_logger')
logger.setLevel(LOG_LEVEL)

# Create the rotating file handler
handler = GzipRotator(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Example logging usage
def main():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

if __name__ == '__main__':
    main()
