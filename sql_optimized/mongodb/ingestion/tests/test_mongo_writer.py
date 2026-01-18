import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from mongodb.ingestion.database.mongo_writer import write_locations, write_sensors, write_measurements


class TestMongoWriter(unittest.TestCase):
    @patch('mongodb.ingestion.database.mongo_writer.locations_col')
    def test_write_locations_empty_list(self, mock_locations_col):
        write_locations([])
        # no update_one calls for empty list
        mock_locations_col.update_one.assert_not_called()

    @patch('mongodb.ingestion.database.mongo_writer.locations_col')
    def test_write_locations_valid_data(self, mock_locations_col):
        locations = [
            {
                "id": 1,
                "name": "Paris",
                "locality": "Paris",
                "country": {"code": "FR"},
                "coordinates": {"latitude": 48.8566, "longitude": 2.3522}
            }
        ]

        write_locations(locations)

        mock_locations_col.update_one.assert_called()

    @patch('mongodb.ingestion.database.mongo_writer.sensors_col')
    def test_write_sensors_empty_list(self, mock_sensors_col):
        write_sensors([])
        mock_sensors_col.update_one.assert_not_called()

    @patch('mongodb.ingestion.database.mongo_writer.sensors_col')
    def test_write_sensors_valid_data(self, mock_sensors_col):
        sensors = [
            {
                "id": 101,
                "location_id": 1,
                "parameter": {"id": 5, "name": "pm10"}
            }
        ]

        write_sensors(sensors)

        mock_sensors_col.update_one.assert_called()

    @patch('mongodb.ingestion.database.mongo_writer.sensors_col')
    def test_write_sensors_missing_location_id(self, mock_sensors_col):
        sensors = [
            {
                "id": 101,
                "location_id": 999,
                "parameter": {"id": 5, "name": "pm10"}
            }
        ]

        write_sensors(sensors)

        mock_sensors_col.update_one.assert_called()

    @patch('mongodb.ingestion.database.mongo_writer.measurements_col')
    def test_write_measurements_empty_dataframe(self, mock_measurements_col):
        df = pd.DataFrame()
        write_measurements(df)
        mock_measurements_col.insert_many.assert_not_called()

    @patch('mongodb.ingestion.database.mongo_writer.measurements_col')
    def test_write_measurements_valid_data(self, mock_measurements_col):
        df = pd.DataFrame({
            "sensor_id": [101, 102],
            "value": [25.5, 26.3],
            "timestamp": ["2024-01-01T10:00:00Z", "2024-01-01T11:00:00Z"]
        })

        write_measurements(df)

        mock_measurements_col.insert_many.assert_called()
