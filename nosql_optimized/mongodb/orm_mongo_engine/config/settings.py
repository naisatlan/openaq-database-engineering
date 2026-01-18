import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://openaq:openaq@localhost:27018/openaq?authSource=admin")
