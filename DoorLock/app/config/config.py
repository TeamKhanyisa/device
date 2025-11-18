import os
from pathlib import Path
from dotenv import load_dotenv


# Load .env from project backend root
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    # Fallback: try default search
    load_dotenv()


# General settings
REGISTER_DIR = os.getenv("REGISTER_DIR", "landmarks")
MODEL_NAME = os.getenv("MODEL_NAME", "ArcFace")
ANGLE_COUNT = int(os.getenv("ANGLE_COUNT", "5"))


# Database
DB_URL = os.getenv("DB_URL")
