import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application configuration settings.
    """
    # Base Paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"

    # API Keys
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY")

    # Model Configuration
    DEFAULT_MODEL_NAME: str = os.getenv("DEFAULT_MODEL_NAME", "gemini-1.5-flash")
    
    # Data Files
    CROP_YIELDS_FILE: Path = DATA_DIR / "crop_yields.json"
    
    # Weather Service
    WEATHER_API_BASE_URL: str = os.getenv("WEATHER_API_BASE_URL", "https://api.open-meteo.com/v1/forecast")

    @classmethod
    def validate(cls):
        """
        Validate critical configuration.
        """
        if not cls.GOOGLE_API_KEY:
            print("WARNING: GOOGLE_API_KEY is not set.")
        if not cls.TAVILY_API_KEY:
            print("WARNING: TAVILY_API_KEY is not set.")

settings = Settings()
