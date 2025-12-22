import pandas as pd

def normalize_measurements(raw_measurements):
    if not raw_measurements:
        return pd.DataFrame()

    df = pd.json_normalize(raw_measurements)

    if "sensor_id" not in df.columns or "value" not in df.columns:
        return pd.DataFrame()

    time_col = None
    for candidate in [
        "period.datetimeFrom",
        "date.utc",
        "datetime",
        "period.datetimeTo"
    ]:
        if candidate in df.columns:
            time_col = candidate
            break

    if time_col is None:
        return pd.DataFrame()

    df = df[["sensor_id", "value", time_col]]
    df = df.rename(columns={time_col: "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["sensor_id", "value", "timestamp"])
    after = len(df)

    print(f"Normalisation mesures : {before} → {after}")

    return df
