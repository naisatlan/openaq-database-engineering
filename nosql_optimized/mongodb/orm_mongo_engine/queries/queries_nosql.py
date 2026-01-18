from models.measurement import Measurement
from mongoengine.queryset.visitor import Q
from datetime import datetime, timedelta
import pandas as pd

# Date de la dernière mesure disponible
def last_available_date():
    return Measurement.objects.order_by("-timestamp").first().timestamp

def last_measures(sensor_id: int, limit: int = 20):
    return list(
        Measurement.objects(sensor__id=sensor_id)
        .only("timestamp", "value", "location.city", "sensor.parameter")
        .order_by("-timestamp")
        .limit(limit)
        .as_pymongo()
    )


def station_profiles():
    pipeline = [
        { "$group": {
            "_id": "$sensor.id",
            "avg": { "$avg": "$value" },
            "std": { "$stdDevPop": "$value" }
        }}
    ]
    return pd.DataFrame(list(Measurement.objects.aggregate(*pipeline)))


def rolling_last_24h_available():
    last_date = last_available_date()
    since = last_date - timedelta(hours=24)

    pipeline = [
        { "$match": { "timestamp": { "$gte": since, "$lte": last_date }}},
        { "$group": {
            "_id": "$location.city",
            "avg_pm10": { "$avg": "$value" },
            "count": { "$sum": 1 }
        }},
        { "$sort": { "avg_pm10": -1 }}
    ]
    return pd.DataFrame(list(Measurement.objects.aggregate(*pipeline)))

def pollution_spikes(threshold=600):
    pipeline = [
        { "$match": { "value": { "$gte": threshold }}},
        { "$group": {
            "_id": {
                "city": "$location.city",
                "hour": { "$dateToString": { "format": "%Y-%m-%d %H", "date": { "$toDate": "$timestamp" }}}
            },
            "max_value": { "$max": "$value" },
            "count": { "$sum": 1 }
        }},
        { "$sort": { "max_value": -1 }}
    ]
    return pd.DataFrame(list(Measurement.objects.aggregate(*pipeline)))

