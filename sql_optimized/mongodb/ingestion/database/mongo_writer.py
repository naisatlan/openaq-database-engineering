from pymongo import MongoClient
from mongodb.ingestion.config.settings import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

locations_col = db.locations
sensors_col = db.sensors
measurements_col = db.measurements


def write_locations(locations):
    docs = []
    for l in locations:
        docs.append({
            "_id": l["id"],
            "city": l.get("locality") or l.get("name"),
            "country": l["country"]["code"] if l.get("country") else None,
            "coordinates": l["coordinates"]
        })

    for d in docs:
        locations_col.update_one({"_id": d["_id"]}, {"$set": d}, upsert=True)

    print("Locations insérées :", len(docs))


def write_sensors(sensors):
    docs = []
    for s in sensors:
        docs.append({
            "_id": s["id"],
            "location_id": s["location_id"],
            "parameter": s.get("parameter", {}).get("name")
        })

    for d in docs:
        sensors_col.update_one({"_id": d["_id"]}, {"$set": d}, upsert=True)

    print("Sensors insérés :", len(docs))


def write_measurements(df):
    docs = df.to_dict("records")
    if docs:
        measurements_col.insert_many(docs)
    print("Measurements insérées :", len(docs))
