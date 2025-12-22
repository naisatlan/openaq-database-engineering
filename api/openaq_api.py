import requests
import time
from config.settings import OPENAQ_BASE_URL, OPENAQ_API_KEY, LIMIT

HEADERS = {"X-API-Key": OPENAQ_API_KEY}


def fetch_locations(page=1, retries=3):
    url = f"{OPENAQ_BASE_URL}/locations"
    params = {"limit": LIMIT, "page": page, "country": "FR", "parameters_id": 5}

    for attempt in range(retries):
        r = requests.get(url, headers=HEADERS, params=params)
        if r.status_code == 200:
            return r.json()["results"]

        print(f"⚠️ API error {r.status_code}, retry {attempt + 1}")
        time.sleep(2)

    r.raise_for_status()


def fetch_sensors(location_id):
    url = f"{OPENAQ_BASE_URL}/locations/{location_id}/sensors"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["results"]


def fetch_measurements(sensor_id, page=1):
    url = f"{OPENAQ_BASE_URL}/sensors/{sensor_id}/measurements"
    params = {"limit": LIMIT, "page": page, "date_from": "2024-01-01", "date_to": "2024-02-01"}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()["results"]
