import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

connect(
    host=os.getenv("MONGO_URI"),
    alias="default",
    db=os.getenv("MONGO_DB"),
    uuidRepresentation="standard"
)
