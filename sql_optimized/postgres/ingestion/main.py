from api.openaq_api import fetch_locations, fetch_sensors, fetch_measurements
from transform.normalizer import normalize_measurements
from database.postgres_writer import write_locations, write_sensors, write_measurements
from benchmark.timer import timer


def run_pipeline(
    pages_locations=1,
    pages_measurements=1,
    max_locations=30
):
    all_measurements = []
    all_sensors = []
    all_locations = []

    locations = fetch_locations(page=1)[:max_locations]

    for loc in locations:
        loc_id = loc["id"]
        all_locations.append(loc)
        
        sensors = fetch_sensors(loc_id)
        for sensor in sensors:
            sensor["location_id"] = loc_id
            all_sensors.append(sensor)

            for page in range(1, pages_measurements + 1):
                meas = fetch_measurements(sensor["id"], page)
                for m in meas:
                    m["sensor_id"] = sensor["id"]
                all_measurements.extend(meas)


    df_meas = normalize_measurements(all_measurements)

    write_locations(all_locations)
    write_sensors(all_sensors)
    write_measurements(df_meas)

    print(f"Locations récupérées : {len(all_locations)}")
    print(f"Sensors récupérés   : {len(all_sensors)}")
    print(f"Measurements récupérées : {len(all_measurements)}")



if __name__ == "__main__":
    bench = {}
    with timer("ingestion time", bench):
        run_pipeline()
    print(bench)