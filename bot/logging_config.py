import logging
import sys
from pathlib import Path


def setup_logging(log_file: str = "trading_bot.log") -> logging.Logger:

    # Get (or create) the named logger for this application
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)  # capture all levels; handlers filter independently

    # Clear any existing handlers to prevent duplicate log entries
    # when setup_logging() is called more than once in the same session
    logger.handlers.clear()

    # Unified format for both handlers:
    # timestamp | log level | logger name | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- File Handler ---
    # Writes all log levels (DEBUG and above) to the specified log file.
    # DEBUG captures full API request/response payloads for audit purposes.
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # --- Console Handler ---
    # Only prints INFO and above to keep terminal output clean.
    # Errors and warnings will still appear; verbose DEBUG lines will not.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Attach both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger