import os
from dotenv import load_dotenv

load_dotenv()

OPENAQ_BASE_URL = "https://api.openaq.org/v3"

COUNTRY = "FR"
PARAMETER = "pm10"
LIMIT = 200

POSTGRES_URI = os.getenv("POSTGRES_URI")
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")
