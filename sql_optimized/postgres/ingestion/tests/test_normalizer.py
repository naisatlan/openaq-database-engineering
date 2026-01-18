import unittest
import pandas as pd
from postgres.ingestion.transform.normalizer import normalize_measurements


class TestNormalizer(unittest.TestCase):
    def test_normalize_empty_measurements(self):
        result = normalize_measurements([])
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_normalize_none(self):
        result = normalize_measurements(None)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_normalize_valid_measurements(self):
        measurements = [
            {
                "sensor_id": 101,
                "value": 25.5,
                "period": {"datetimeFrom": {"utc": "2024-01-01T10:00:00Z"}}
            },
            {
                "sensor_id": 101,
                "value": 26.3,
                "period": {"datetimeFrom": {"utc": "2024-01-01T11:00:00Z"}}
            }
        ]

        result = normalize_measurements(measurements)

        self.assertFalse(result.empty)
        self.assertEqual(len(result), 2)
        self.assertIn("sensor_id", result.columns)
        self.assertIn("value", result.columns)
        self.assertIn("timestamp", result.columns)
        self.assertEqual(result["sensor_id"].iloc[0], 101)
        self.assertEqual(result["value"].iloc[0], 25.5)

    def test_normalize_removes_invalid_values(self):
        measurements = [
            {
                "sensor_id": 101,
                "value": 25.5,
                "period": {"datetimeFrom": {"utc": "2024-01-01T10:00:00Z"}}
            },
            {
                "sensor_id": 101,
                "value": -5.0,  # invalid value
                "period": {"datetimeFrom": {"utc": "2024-01-01T11:00:00Z"}}
            }
        ]

        result = normalize_measurements(measurements)

        self.assertEqual(len(result), 1)
        self.assertEqual(result["value"].iloc[0], 25.5)

    def test_normalize_removes_null_timestamps(self):
        measurements = [
            {
                "sensor_id": 101,
                "value": 25.5,
                "period": {"datetimeFrom": {"utc": "2024-01-01T10:00:00Z"}}
            },
            {
                "sensor_id": 102,
                "value": 20.0,
                "period": {"datetimeFrom": {"utc": "invalid-date"}}
            }
        ]

        result = normalize_measurements(measurements)

        self.assertEqual(len(result), 1)
        self.assertEqual(result["sensor_id"].iloc[0], 101)

    def test_normalize_handles_missing_sensor_id(self):
        measurements = [
            {
                "value": 25.5,
                "period": {"datetimeFrom": {"utc": "2024-01-01T10:00:00Z"}}
            }
        ]

        result = normalize_measurements(measurements)
        self.assertTrue(result.empty)

    def test_normalize_handles_missing_value(self):
        measurements = [
            {
                "sensor_id": 101,
                "period": {"datetimeFrom": {"utc": "2024-01-01T10:00:00Z"}}
            }
        ]

        result = normalize_measurements(measurements)

        self.assertTrue(result.empty)

    def test_normalize_converts_timestamp_to_datetime(self):
        measurements = [
            {
                "sensor_id": 101,
                "value": 25.5,
                "period": {"datetimeFrom": {"utc": "2024-01-01T10:00:00Z"}}
            }
        ]

        result = normalize_measurements(measurements)

        self.assertEqual(pd.api.types.is_datetime64_any_dtype(result["timestamp"]), True)


if __name__ == '__main__':
    unittest.main()
