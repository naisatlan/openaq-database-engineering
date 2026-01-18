import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from mongodb.orm_mongo_engine.queries.analytics import (
    top10_locations_pm10,
    avg_by_city,
    compare_rotterdam_santiago,
    daily_avg_city,
    monthly_avg_pm10,
)


class TestAnalytics(unittest.TestCase):
    @patch('mongodb.orm_mongo_engine.queries.analytics.Measurement')
    def test_top10_locations_pm10(self, mock_measurement):
        mock_measurement.objects.aggregate.return_value = [
            {"_id": "City A", "avg_pm10": 50.0},
        ]

        df = top10_locations_pm10()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertIn('avg_pm10', df.columns)

    @patch('mongodb.orm_mongo_engine.queries.analytics.Measurement')
    def test_avg_by_city(self, mock_measurement):
        mock_measurement.objects.aggregate.return_value = [
            {"_id": "City A", "avg_pm10": 30.0},
        ]

        df = avg_by_city()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)

    @patch('mongodb.orm_mongo_engine.queries.analytics.Measurement')
    def test_compare_rotterdam_santiago(self, mock_measurement):
        mock_measurement.objects.aggregate.return_value = [
            {"_id": "Rotterdam", "avg_pm10": 20.0},
            {"_id": "Santiago", "avg_pm10": 25.0},
        ]

        df = compare_rotterdam_santiago()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)

    @patch('mongodb.orm_mongo_engine.queries.analytics.Measurement')
    def test_daily_avg_city(self, mock_measurement):
        mock_measurement.objects.aggregate.return_value = [
            {"_id": {"city": "City A", "day": "2024-01-01"}, "avg_pm10": 15.0},
        ]

        df = daily_avg_city()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)

    @patch('mongodb.orm_mongo_engine.queries.analytics.Measurement')
    def test_monthly_avg_pm10(self, mock_measurement):
        mock_measurement.objects.aggregate.return_value = [
            {"_id": "2024-01", "avg_pm10": 12.0},
        ]

        df = monthly_avg_pm10()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)


if __name__ == '__main__':
    unittest.main()
