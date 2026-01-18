import sys
from pathlib import Path
from datetime import datetime

# Add the sql_optimized directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.openaq_api import fetch_locations, fetch_sensors, fetch_measurements
from database.mongo_writer import insert_measurements
from benchmark.timer import timer


def run_pipeline(max_locations=30, pages_measurements=1):

    docs = []
    locations = fetch_locations()[:max_locations]

    for loc in locations:
        sensors = fetch_sensors(loc["id"])

        for s in sensors:
            for page in range(1, pages_measurements + 1):
                measurements = fetch_measurements(s["id"], page)

                for m in measurements:
                    val = m.get("value")
                    ts = m["period"]["datetimeFrom"]["utc"]

                    if val is None or val < 0:
                        continue

                    docs.append({
                        "timestamp": datetime.fromisoformat(ts.replace("Z","+00:00")),
                        "value": float(val),

                        "sensor": {
                            "id": s["id"],
                            "parameter": s.get("parameter", {}).get("name")
                        },
                        "location": {
                            "id": loc["id"],
                            "city": loc.get("locality") or loc.get("name"),
                            "country": loc["country"]["code"],
                            "lat": loc["coordinates"]["latitude"],
                            "lon": loc["coordinates"]["longitude"]
                        }
                    })

    insert_measurements(docs)
    print("Inserted documents:", len(docs))


if __name__ == "__main__":
    bench = {}
    with timer("ingestion time", bench):
        run_pipeline()
    print(bench)
