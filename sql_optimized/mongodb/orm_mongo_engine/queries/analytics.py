from mongodb.orm_mongo_engine.models.measurement import Measurement
from mongodb.orm_mongo_engine.models.sensor import Sensor
from mongodb.orm_mongo_engine.models.location import Location
import pandas as pd

def top10_locations_pm10():

    pipeline = [
        { "$lookup": {
            "from": "sensors",
            "localField": "sensor_id",
            "foreignField": "_id",
            "as": "sensor"
        }},
        { "$unwind": "$sensor" },

        { "$lookup": {
            "from": "locations",
            "localField": "sensor.location_id",
            "foreignField": "_id",
            "as": "location"
        }},
        { "$unwind": "$location" },

        { "$group": {
            "_id": "$location.city",
            "avg_pm10": { "$avg": "$value" }
        }},
        { "$sort": { "avg_pm10": -1 } },
        { "$limit": 10 }
    ]

    data = list(Measurement.objects.aggregate(pipeline))
    return pd.DataFrame(data)

def avg_by_city():
    pipeline = [
        { "$lookup": {
            "from": "sensors",
            "localField": "sensor_id",
            "foreignField": "_id",
            "as": "sensor"
        }},
        { "$unwind": "$sensor" },

        { "$lookup": {
            "from": "locations",
            "localField": "sensor.location_id",
            "foreignField": "_id",
            "as": "location"
        }},
        { "$unwind": "$location" },

        { "$group": {
            "_id": "$location.city",
            "avg_pm10": { "$avg": "$value" }
        }},
        { "$sort": { "avg_pm10": -1 } }
    ]

    return pd.DataFrame(list(Measurement.objects.aggregate(pipeline)))


def compare_rotterdam_santiago():
    pipeline = [
        { "$lookup": {
            "from": "sensors",
            "localField": "sensor_id",
            "foreignField": "_id",
            "as": "sensor"
        }},
        { "$unwind": "$sensor" },

        { "$lookup": {
            "from": "locations",
            "localField": "sensor.location_id",
            "foreignField": "_id",
            "as": "location"
        }},
        { "$unwind": "$location" },

        { "$match": {
            "location.city": { "$in": ["Rotterdam", "Santiago"] }
        }},

        { "$group": {
            "_id": "$location.city",
            "avg_pm10": { "$avg": "$value" }
        }}
    ]

    return pd.DataFrame(list(Measurement.objects.aggregate(pipeline)))


def daily_avg_city():
    pipeline = [
        { "$addFields": {
            "day": { "$substr": ["$timestamp", 0, 10] }
        }},

        { "$lookup": {
            "from": "sensors",
            "localField": "sensor_id",
            "foreignField": "_id",
            "as": "sensor"
        }},
        { "$unwind": "$sensor" },

        { "$lookup": {
            "from": "locations",
            "localField": "sensor.location_id",
            "foreignField": "_id",
            "as": "location"
        }},
        { "$unwind": "$location" },

        { "$group": {
            "_id": {
                "city": "$location.city",
                "day": "$day"
            },
            "avg_pm10": { "$avg": "$value" }
        }},
        { "$sort": { "_id.city": 1, "_id.day": 1 } }
    ]

    return pd.DataFrame(list(Measurement.objects.aggregate(pipeline)))

def monthly_avg_pm10():
    pipeline = [
        { "$addFields": {
            "month": { "$substr": ["$timestamp", 0, 7] }
        }},
        { "$group": {
            "_id": "$month",
            "avg_pm10": { "$avg": "$value" }
        }},
        { "$sort": { "_id": 1 } }
    ]

    return pd.DataFrame(list(Measurement.objects.aggregate(pipeline)))

