import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Agentic AI Intelligent Wallet & Mobile Theft Recovery System")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./post_theft_recovery.db")


settings = Settings()
