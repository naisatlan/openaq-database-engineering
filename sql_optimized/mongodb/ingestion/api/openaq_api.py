import requests
import time
from mongodb.ingestion.config.settings import OPENAQ_BASE_URL, OPENAQ_API_KEY, LIMIT

HEADERS = {"X-API-Key": OPENAQ_API_KEY}


def fetch_locations(page=1, retries=3):
    url = f"{OPENAQ_BASE_URL}/locations"
    params = {"limit": LIMIT, "page": page, "country": "FR", "parameters_id": 5}

    for attempt in range(retries):
        r = requests.get(url, headers=HEADERS, params=params)
        if r.status_code == 200:
            return r.json().get("results", [])

        print(f"API error {r.status_code}, retry {attempt + 1}")
        time.sleep(2)

    print("Locations fetch failed, skipping page.")
    return []


def fetch_sensors(location_id, retries=3):
    url = f"{OPENAQ_BASE_URL}/locations/{location_id}/sensors"

    for attempt in range(retries):
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("results", [])

        print(f"Sensors error {r.status_code} for location {location_id}, retry {attempt + 1}")
        time.sleep(2)

    print(f"Skipping sensors for location {location_id}")
    return []


def fetch_measurements(sensor_id, page=1, retries=2):
    url = f"{OPENAQ_BASE_URL}/sensors/{sensor_id}/measurements"
    params = {
        "limit": LIMIT,
        "page": page,
        "date_from": "2024-01-01",
        "date_to": "2024-02-01"
    }

    for attempt in range(retries):
        r = requests.get(url, headers=HEADERS, params=params)

        if r.status_code == 200:
            return r.json().get("results", [])

        if r.status_code == 500:
            print(f"OpenAQ 500 on sensor {sensor_id} page {page}, skipping.")
            return []

        print(f"Measurements error {r.status_code} on sensor {sensor_id}, retry {attempt + 1}")
        time.sleep(1)

    return []

