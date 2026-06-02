"""
Logging Configuration
"""

import logging
import os
from pathlib import Path
from pythonjsonlogger import jsonlogger


def setup_logger() -> logging.Logger:
    """
    Setup application logger
    """
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logs_dir = Path(os.getenv("DATA_DIR", "./data")) / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("hugo")
    logger.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_formatter = logging.Formatter(
        '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with JSON format
    file_handler = logging.FileHandler(
        logs_dir / "hugo.log"
    )
    file_handler.setLevel(getattr(logging, log_level))
    file_formatter = jsonlogger.JsonFormatter()
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


logger = setup_logger()
