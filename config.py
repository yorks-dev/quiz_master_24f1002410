import sys, os
from loguru import logger


class Config:
    """Base Configuration Class"""

    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_APP = os.getenv("FLASK_APP", "run.py")

    # Setup loguru level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Supress warnings

    def __init__(self):
        """Configure logger and check env vars"""
        self.check_env_vars()

    def configure_logger(self):
        """Loguru Setup"""
        log_level = self.LOG_LEVEL
        log_dir = "logs"
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception as e:
                print(f"Error creating log directory '{log_dir}': {e}")
                sys.exit(1)

        self.config_logger_path = os.path.join(log_dir, "config.log")

        logger.add(
            self.config_logger_path,
            level=log_level,
            rotation="500 MB",
            enqueue=True,
            format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {module}:{function}:{line} - {message}",
        )  # Log file for config

        logger.info("Logger configured for config", file=self.config_logger_path)

    def check_env_vars(self):
        """check if important env variables exists and exit if missing"""
        required_vars = ["SECRET_KEY"]
        for var in required_vars:
            if not os.getenv(var):
                logger.error(
                    f"Environment variable '{var}' is not set. Application cannot start."
                )
                exit(1)
