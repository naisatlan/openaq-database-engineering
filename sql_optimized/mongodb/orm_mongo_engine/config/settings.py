import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/openaq")

connect(host=MONGO_URI)