import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logger():
    logger = logging.getLogger("devsecai")
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.hasHandlers():
        return logger

    # 🖥️ Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 📁 File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger