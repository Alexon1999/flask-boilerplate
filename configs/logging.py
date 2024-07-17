import logging
from datetime import datetime, timezone

import pytz
from flask import Flask


def configure_logging(app: Flask):
    # Create a logger instance
    logger = logging.getLogger(app.name)

    # Set the logging level
    LOG_LEVEL = app.config.get("LOG_LEVEL")
    logger.setLevel(LOG_LEVEL)

    # Set the timezone to Paris
    paris_timezone = pytz.timezone("Europe/Paris")

    # Configure logging with the Paris timezone
    logging.Formatter.converter = (
        lambda *args: datetime.now(timezone.utc)
        .astimezone(paris_timezone)
        .timetuple()
    )

    # Define the log format
    console_log_format = "%(asctime)s - %(levelname)s - %(message)s"
    file_log_format = (
        "%(asctime)s - %(levelname)s - %(message)s - (%(filename)s:%(lineno)d)"
    )

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(
        logging.Formatter(console_log_format, datefmt=app.config["DATE_FMT"])
    )
    logger.addHandler(console_handler)

    # Create a file handler
    file_handler = logging.FileHandler(
        filename=app.config["LOG_FILE_API"],
        encoding="utf-8",
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(
        logging.Formatter(file_log_format, datefmt=app.config["DATE_FMT"])
    )
    logger.addHandler(file_handler)

    # Set the logger to the app instance
    app.logger = logger
