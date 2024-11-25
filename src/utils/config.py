"""
Configuration settings for St Mary's Fitness Management System.
Provides application-level constants and settings.
"""

import os

class Config:
    """Centralized configuration settings for the application."""

    # Database configurations
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///app.db")
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", 10))

    # Logging configurations
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")

    # Application settings
    APP_NAME: str = "St Mary's Fitness Management System"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Email configurations
    EMAIL_SERVER: str = os.getenv("EMAIL_SERVER", "smtp.example.com")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "your_email@example.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"

    @classmethod
    def display(cls):
        """Display the current configuration settings."""
        settings = {key: getattr(cls, key) for key in dir(cls) if not key.startswith("_")}
        for key, value in settings.items():
            print(f"{key}: {value}")
