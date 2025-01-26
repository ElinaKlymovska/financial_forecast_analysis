import logging
import os
from datetime import datetime


def configure_logging(process_name, log_dir='logs', level=logging.INFO):
    """
    Configures logging for a specific process.

    Parameters:
    process_name (str): The name of the process (used to name the log file).
    log_dir (str): The directory where logs will be stored.
    level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
    """
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create a subdirectory for the process
    process_log_dir = os.path.join(log_dir, process_name)
    os.makedirs(process_log_dir, exist_ok=True)

    # Generate a timestamped log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(process_log_dir, f"{process_name}_{timestamp}.log")

    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
