import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8080")
DATA_PATH = os.getenv("DATA_PATH", "./data")
