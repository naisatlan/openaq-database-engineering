import requests

API_KEY = "1988cce29320e234e4cfc3dff73d3628ada567e860943e7bfba0257757772447"
BASE = "https://api.openaq.org/v3"

headers = {"X-API-Key": API_KEY}

# 1. locations
locs = requests.get(f"{BASE}/locations", headers=headers, params={"limit": 5}).json()["results"]
loc_id = locs[0]["id"]
print("location_id:", loc_id)

# 2. sensors
sensors = requests.get(f"{BASE}/locations/{loc_id}/sensors", headers=headers).json()["results"]
sensor_id = sensors[0]["id"]
print("sensor_id:", sensor_id)

# 3. measurements
meas = requests.get(f"{BASE}/sensors/{sensor_id}/measurements", headers=headers, params={"limit": 10})
print("status:", meas.status_code)
print("nb measurements:", len(meas.json()["results"]))
