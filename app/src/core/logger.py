import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Define the path: root/data/logs
# Since this file is in app/core/, we go up two levels to hit root
LOG_DIR = Path(__file__).resolve().parents[2] / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging():
    logger = logging.getLogger("fastapi_mvc")
    logger.setLevel(logging.INFO)

    # 1. Formatter: [Timestamp] [Level] [Module]: Message
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 2. Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 3. Timed Rotating File Handler (Every day at midnight)
    file_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "app.log",
        when="midnight",
        interval=1,
        backupCount=30,  # Keep logs for 30 days
        encoding="utf-8",
    )
    file_handler.suffix = "%Y-%m-%d"  # Result: app.log.2026-03-31
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Initialize once
logger = setup_logging()
