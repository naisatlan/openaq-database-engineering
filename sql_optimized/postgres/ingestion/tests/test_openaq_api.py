import unittest
from unittest.mock import patch, MagicMock
import json
from postgres.ingestion.api.openaq_api import fetch_locations, fetch_sensors, fetch_measurements


class TestOpenAQAPI(unittest.TestCase):
    #Tests unitaire pour l'API OpenAQ
    @patch('postgres.ingestion.api.openaq_api.requests.get')
    def test_fetch_locations_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": 1,
                    "name": "Paris",
                    "locality": "Paris",
                    "country": {"code": "FR"},
                    "coordinates": {"latitude": 48.8566, "longitude": 2.3522}
                }
            ]
        }
        mock_get.return_value = mock_response

        result = fetch_locations(page=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["name"], "Paris")

    @patch('postgres.ingestion.api.openaq_api.requests.get')
    def test_fetch_locations_empty(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        result = fetch_locations(page=1)

        self.assertEqual(len(result), 0)

    @patch('postgres.ingestion.api.openaq_api.requests.get')
    def test_fetch_locations_api_error_retry(self, mock_get):
        error_response = MagicMock()
        error_response.status_code = 500

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"results": []}

        mock_get.side_effect = [error_response, success_response]

        result = fetch_locations(page=1, retries=2)

        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(len(result), 0)

    @patch('postgres.ingestion.api.openaq_api.requests.get')
    def test_fetch_locations_all_retries_fail(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = fetch_locations(page=1, retries=2)

        self.assertEqual(len(result), 0)

    @patch('postgres.ingestion.api.openaq_api.requests.get')
    def test_fetch_sensors_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": 101,
                    "parameter": {"id": 5, "name": "pm10"}
                }
            ]
        }
        mock_get.return_value = mock_response

        result = fetch_sensors(location_id=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 101)
        self.assertEqual(result[0]["parameter"]["name"], "pm10")

    @patch('postgres.ingestion.api.openaq_api.requests.get')
    def test_fetch_measurements_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "value": 25.5,
                    "period": {"datetimeFrom": {"utc": "2024-01-01T10:00:00Z"}}
                }
            ]
        }
        mock_get.return_value = mock_response

        result = fetch_measurements(sensor_id=101, page=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], 25.5)


    @patch('postgres.ingestion.api.openaq_api.requests.get')
    def test_fetch_measurements_api_error_retry(self, mock_get):
        error_response = MagicMock()
        error_response.status_code = 429  # l'api bloque pour trop de requetes

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"results": []}

        mock_get.side_effect = [error_response, success_response]

        result = fetch_measurements(sensor_id=101, page=1, retries=2)

        self.assertEqual(mock_get.call_count, 2)


class TestOpenAQAPIIntegration(unittest.TestCase):
    #Tests d'intégration pour l'API OpenAQ (il faut pouvoir accéder à l'API en direct)
    @unittest.skip("Requires API access")
    def test_fetch_locations_live(self):
        result = fetch_locations(page=1)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()