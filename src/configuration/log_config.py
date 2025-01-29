import logging
import os
from datetime import datetime

log_dir = "/Users/ElinaKlymovska/PycharmProjects/financial_forecast_analysis/financial_forecast_analysis/logs"


def configure_logging(process_name, log_dir=log_dir, level=logging.DEBUG):
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Generate a timestamped log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{process_name}_{timestamp}.log")

    # Configure logging
    logger = logging.getLogger(process_name)
    logger.setLevel(level)

    # Clear existing handlers to prevent duplicate messages
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Add handlers to logger
    logger.addHandler(file_handler)

    return logger
