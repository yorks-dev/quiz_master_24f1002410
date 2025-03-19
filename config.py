import sys, os
from loguru import logger


class Config:
    """Base Configuration Class"""

    REQUIRED_VARS = ["FLASK_ENV", "SECRET_KEY"]

    def __init__(self, log_dir):
        """Check env vars and init logging"""

        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Default to INFO
        self.setup_logging(log_dir)  # Logger is set up first

        logger.info("Starting Development Config")

        self.check_env_vars()  # Check envs
        self.FLASK_ENV = os.getenv("FLASK_ENV")  # mandatory
        self.SECRET_KEY = os.getenv("SECRET_KEY")  # mandatory

        self.SQLALCHEMY_TRACK_MODIFICATIONS = False  # supress warnings

        # Log level warning
        if not os.getenv("LOG_LEVEL"):
            logger.warning("LOG_LEVEL is not set. Using default: INFO.")

    def check_env_vars(self):
        """check if important env variables exists and exit if missing"""
        for var in self.REQUIRED_VARS:
            if not os.getenv(var):
                logger.error(
                    f"Environment variable '{var}' is not read/set. Application cannot start."
                )
                sys.exit(1)

    def setup_logging(self, log_dir):
        """Loguru Setup for given log_dir"""
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception as e:
                print(f"Error creating log directory '{log_dir}': {e}")
                sys.exit(1)

        self.config_logger_path = os.path.join(log_dir, "config.log")

        logger.add(
            self.config_logger_path,
            level=self.LOG_LEVEL,
            rotation="500 MB",
            enqueue=True,
            format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {module}:{function}:{line} - {message}",
        )  # Log file for config using subclass dirname

        logger.info(f"Logger configured : {self.config_logger_path}")


class DevelopmentConfig(Config):
    """Development Configuration"""

    DEBUG = True

    def __init__(self):
        super().__init__(log_dir="logs_dir")

        # check Database but for dev give warning and use default.
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
        if not self.SQLALCHEMY_DATABASE_URI:
            logger.warning(
                "DEV_DATABASE_URL is not set. Using default SQLite database."
            )
            self.SQLALCHEMY_DATABASE_URI = "sqlite:///instance/dev.db"
        logger.info("Developemtn Config Coompleted Succesfully")


if __name__ == "__main__":
    # Example Usage (for testing the config and logging)
    # This will now do the environment variable check
    try:
        dev_config = DevelopmentConfig()
        logger.debug("This is a debug message from main")
        logger.info(f"Database URI: {dev_config.SQLALCHEMY_DATABASE_URI}")
    except SystemExit:
        # Catch the SystemExit exception if the script exits
        print("Application exited due to missing environment variables.")
