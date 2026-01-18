CREATE TABLE IF NOT EXISTS measurements (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ NOT NULL,
  value DOUBLE PRECISION NOT NULL CHECK (value >= 0),

  sensor JSONB NOT NULL,
  location JSONB NOT NULL,
  raw JSONB NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_measurement
  ON measurements ((raw->>'timestamp'), (raw->'sensor'->>'id'));

CREATE INDEX IF NOT EXISTS idx_measurements_ts
  ON measurements (timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_measurements_city
  ON measurements ((location->>'city'));
