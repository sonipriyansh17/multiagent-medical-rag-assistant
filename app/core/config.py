# backend/app/core/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "MedAssist RAG API"
    PROJECT_VERSION: str = "1.0.0"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Security settings for JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_in_env") # It's better to generate a real secret key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
