from pymongo import MongoClient
from config.settings import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db.measurements

def insert_measurements(measurements):
    if measurements:
        result = collection.insert_many(measurements)
