import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.openaq_api import fetch_locations, fetch_sensors, fetch_measurements
from transform.normalizer import normalize_measurements
from database.mongo_writer import write_locations, write_sensors, write_measurements
from benchmark.timer import timer


def run_pipeline(max_locations=30):
    all_locations, all_sensors, all_measurements = [], [], []

    locations = fetch_locations()[:max_locations]

    for loc in locations:
        loc_id = loc["id"]
        all_locations.append(loc)

        sensors = fetch_sensors(loc_id)
        for sensor in sensors:
            sensor["location_id"] = loc_id
            all_sensors.append(sensor)

            meas = fetch_measurements(sensor["id"])
            for m in meas:
                m["sensor_id"] = sensor["id"]
            all_measurements.extend(meas)

    df_meas = normalize_measurements(all_measurements)

    write_locations(all_locations)
    write_sensors(all_sensors)
    write_measurements(df_meas)


if __name__ == "__main__":
    bench = {}
    with timer("ingestion time", bench):
        run_pipeline()
    print(bench)