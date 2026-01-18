import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
from postgres.ingestion.database.postgres_writer import write_locations, write_sensors, write_measurements


class TestPostgresWriter(unittest.TestCase):
    #Tests unitaires pour le writer Postgres
    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_locations_empty_list(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        pd.read_sql = MagicMock(return_value=pd.DataFrame({"id": []}))

        write_locations([])

        mock_engine.connect.assert_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_locations_valid_data(self, mock_engine):
        locations = [
            {
                "id": 1,
                "name": "Paris",
                "locality": "Paris",
                "country": {"code": "FR"},
                "coordinates": {"latitude": 48.8566, "longitude": 2.3522}
            }
        ]

        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        with patch('postgres.ingestion.database.postgres_writer.pd.read_sql') as mock_read:
            mock_read.return_value = pd.DataFrame({"id": []})

            write_locations(locations)

            mock_engine.connect.assert_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_sensors_empty_list(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        with patch('postgres.ingestion.database.postgres_writer.pd.read_sql') as mock_read:
            mock_read.return_value = pd.DataFrame({"id": [1]})

            write_sensors([])

            mock_engine.connect.assert_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_sensors_valid_data(self, mock_engine):
        sensors = [
            {
                "id": 101,
                "location_id": 1,
                "parameter": {"id": 5, "name": "pm10"}
            }
        ]

        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        with patch('postgres.ingestion.database.postgres_writer.pd.read_sql') as mock_read:
            mock_read.return_value = pd.DataFrame({"id": [1]})

            write_sensors(sensors)

            mock_engine.connect.assert_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_sensors_missing_location_id(self, mock_engine):
        sensors = [
            {
                "id": 101,
                "location_id": 999,  # Invalid location
                "parameter": {"id": 5, "name": "pm10"}
            }
        ]

        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        with patch('postgres.ingestion.database.postgres_writer.pd.read_sql') as mock_read:
            mock_read.return_value = pd.DataFrame({"id": []}) #filter out all

            write_sensors(sensors)

            mock_engine.connect.assert_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_measurements_empty_dataframe(self, mock_engine):
        df = pd.DataFrame()
        write_measurements(df)
        mock_engine.connect.assert_not_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_measurements_valid_data(self, mock_engine):
        df = pd.DataFrame({
            "sensor_id": [101, 102],
            "value": [25.5, 26.3],
            "timestamp": ["2024-01-01T10:00:00Z", "2024-01-01T11:00:00Z"]
        })

        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        with patch('postgres.ingestion.database.postgres_writer.pd.read_sql') as mock_read:
            mock_read.return_value = pd.DataFrame({"id": [101, 102]})

            write_measurements(df)

            mock_engine.connect.assert_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_measurements_invalid_sensor_id(self, mock_engine):
        df = pd.DataFrame({
            "sensor_id": [101, 999],  # 999 is invalid
            "value": [25.5, 26.3],
            "timestamp": ["2024-01-01T10:00:00Z", "2024-01-01T11:00:00Z"]
        })

        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        with patch('postgres.ingestion.database.postgres_writer.pd.read_sql') as mock_read:
            mock_read.return_value = pd.DataFrame({"id": [101]}) # only 101 is valid

            write_measurements(df)

            mock_engine.connect.assert_called()

    @patch('postgres.ingestion.database.postgres_writer.engine')
    def test_write_locations_deduplication(self, mock_engine):
        locations = [
            {
                "id": 1,
                "name": "Paris",
                "locality": "Paris",
                "country": {"code": "FR"},
                "coordinates": {"latitude": 48.8566, "longitude": 2.3522}
            }
        ]

        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        with patch('postgres.ingestion.database.postgres_writer.pd.read_sql') as mock_read:
            mock_read.return_value = pd.DataFrame({"id": [1]}) #location 1 existe déjà

            write_locations(locations)

            mock_engine.connect.assert_called()

if __name__ == '__main__':
    unittest.main()
