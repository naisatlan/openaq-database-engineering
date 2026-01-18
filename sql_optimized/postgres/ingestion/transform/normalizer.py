import pandas as pd

def normalize_measurements(raw_measurements):
    if not raw_measurements:
        return pd.DataFrame()

    df = pd.json_normalize(raw_measurements)

    if "sensor_id" not in df.columns or "value" not in df.columns:
        return pd.DataFrame()

    if "period.datetimeFrom.utc" in df.columns:
        time_col = "period.datetimeFrom.utc"
    elif "datetime" in df.columns:
        time_col = "datetime"
    else:
        print("Aucun champ temporel reconnu")
        print("Colonnes disponibles :", df.columns.tolist())
        return pd.DataFrame()

    df = df[["sensor_id", "value", time_col]]
    df = df.rename(columns={time_col: "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["sensor_id", "value", "timestamp"])
    df = df[df["value"] >= 0]
    after = len(df)

    print(f"Normalisation mesures : {before} → {after}")

    return df
