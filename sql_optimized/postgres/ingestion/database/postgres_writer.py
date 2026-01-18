from sqlalchemy import create_engine, text
from postgres.ingestion.config.settings import POSTGRES_URI
import pandas as pd

engine = create_engine(POSTGRES_URI)


def write_locations(locations):
    with engine.connect() as conn:
        if not locations:
            return

        df = pd.DataFrame([{
            "id": l["id"],
            "city": l.get("locality") or l.get("name"),
            "country": l["country"]["code"] if l.get("country") else None,
            "latitude": l["coordinates"]["latitude"],
            "longitude": l["coordinates"]["longitude"]
        } for l in locations])

        existing_ids = pd.read_sql(
            text("SELECT id FROM location"),
            conn
        )["id"].tolist()

    df = df[~df["id"].isin(existing_ids)]

    if not df.empty:
        df.to_sql("location", engine, if_exists="append", index=False)

    print("Locations insérées :", len(df))


def write_sensors(sensors):
    with engine.connect() as conn:
        if not sensors:
            return

        df = pd.DataFrame([{
            "id": s["id"],
            "location_id": s["location_id"], 
            "parameter_id": s.get("parameter", {}).get("id"),
            "parameter": s.get("parameter", {}).get("name"),
        } for s in sensors])

        valid_locations = pd.read_sql(
            text("SELECT id FROM location"),
            conn
        )["id"].tolist()

    df = df[df["location_id"].isin(valid_locations)]

    print("Sensors insérés :", len(df))

    if not df.empty:
        df.drop_duplicates("id").to_sql(
            "sensor",
            engine,
            if_exists="append",
            index=False
        )

def write_measurements(df):
    if df.empty:
        return

    with engine.connect() as conn:
        valid_sensors = pd.read_sql(
            text("SELECT id FROM sensor"),
            conn
        )["id"].tolist()

    df = df[df["sensor_id"].isin(valid_sensors)]

    print("Measurements insérées :", len(df))

    if not df.empty:
        df.to_sql("measurement", engine, if_exists="append", index=False)
