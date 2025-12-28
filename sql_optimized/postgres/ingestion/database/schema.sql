CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY,
    city TEXT,
    country TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS sensor (
    id INTEGER PRIMARY KEY,
    location_id INTEGER REFERENCES location(id),
    parameter_id INTEGER,
    parameter TEXT
);

CREATE TABLE IF NOT EXISTS measurement (
    sensor_id INTEGER REFERENCES sensor(id),
    value DOUBLE PRECISION,
    unit TEXT,
    timestamp TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_measurement_time
ON measurement(timestamp);
