import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_RADIUS = 20000  # in meters
VENDOR_TYPES = ["studio", "wedding", "event", "catering", "photo"]
