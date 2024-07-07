import logging
import os


# Default project root for non-testing environment
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def setup_logging(level=logging.INFO, test=False):

    log_dir = os.path.join(PROJECT_ROOT, 'logs')
    if test:
        file = os.path.join(log_dir, 'calculator_test_log.txt')
    else:
        file = os.path.join(log_dir, 'calculator_log.txt')

    # Ensure the log file exists
    if not os.path.exists(file):
        open(file, 'w').close()  # Create an empty file if it doesn't exist
        print(f"Created file: {file}")


    logger = logging.getLogger()
    logger.setLevel(level)

    # Check if any handlers already exist, and remove them
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add a file handler
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s:: %(name)s:: %(levelname)s:: %(funcName)s:: %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

