import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    DATABASE_URL: str = "sqlite:///./app.db"
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    EXPORT_DIR: str = "exports"
    IMAGES_DIR: str = "generated_images"

settings = Settings()

os.makedirs(settings.EXPORT_DIR, exist_ok=True)
os.makedirs(settings.IMAGES_DIR, exist_ok=True)
