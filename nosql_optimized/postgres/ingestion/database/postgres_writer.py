import os, json, psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT")),
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD")
    )

def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type not serializable: {type(obj)}")

def insert_measurements_pg_nosql(docs):
    rows = []
    for d in docs:
        rows.append((
            d["timestamp"],
            float(d["value"]),
            json.dumps(d["sensor"]),
            json.dumps(d["location"]),
            json.dumps(d, default=json_serializer)
        ))

    sql = """
    INSERT INTO measurements (timestamp, value, sensor, location, raw)
    VALUES %s
    ON CONFLICT DO NOTHING;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, rows, page_size=2000)
