import pytest
from unittest.mock import patch, MagicMock

from mongodb.ingestion.main import run_pipeline

def fake_location(id=1):
    return {
        "id": id,
        "name": f"City {id}",
        "locality": f"City {id}",
        "country": {"code": "FR"},
        "coordinates": {"latitude": 0.0, "longitude": 0.0},
    }
    
@patch("mongodb.ingestion.main.write_measurements")
@patch("mongodb.ingestion.main.write_sensors")
@patch("mongodb.ingestion.main.write_locations")
@patch("mongodb.ingestion.main.normalize_measurements")
@patch("mongodb.ingestion.main.fetch_measurements")
@patch("mongodb.ingestion.main.fetch_sensors")
@patch("mongodb.ingestion.main.fetch_locations")
def test_pipeline_happy_path(
    fetch_locations,
    fetch_sensors,
    fetch_measurements,
    normalize,
    write_locations,
    write_sensors,
    write_measurements,
):
    fetch_locations.return_value = [fake_location(1)]
    fetch_sensors.return_value = [{"id": 101}]
    fetch_measurements.return_value = [{"value": 25.5}]
    normalize.return_value = MagicMock()

    run_pipeline(max_locations=1)

    write_locations.assert_called_once()
    write_sensors.assert_called_once()
    write_measurements.assert_called_once()

@patch("mongodb.ingestion.main.write_measurements")
@patch("mongodb.ingestion.main.write_sensors")
@patch("mongodb.ingestion.main.write_locations")
@patch("mongodb.ingestion.main.fetch_locations")
def test_pipeline_stops_when_no_locations(
    fetch_locations,
    write_locations,
    write_sensors,
    write_measurements,
):

    fetch_locations.return_value = []

    run_pipeline(max_locations=1)

    fetch_locations.assert_called_once()

@patch("mongodb.ingestion.main.write_measurements")
@patch("mongodb.ingestion.main.write_sensors")
@patch("mongodb.ingestion.main.write_locations")
@patch("mongodb.ingestion.main.fetch_measurements")
@patch("mongodb.ingestion.main.fetch_sensors")
@patch("mongodb.ingestion.main.fetch_locations")
def test_pipeline_multiple_measurement_pages(
    fetch_locations,
    fetch_sensors,
    fetch_measurements,
    write_locations,
    write_sensors,
    write_measurements,
):

    fetch_locations.return_value = [fake_location(1)]
    fetch_sensors.return_value = [{"id": 101}]

    fetch_measurements.side_effect = [
        [{"value": 25.5}],
        [{"value": 26.3}],
    ]

    # run_pipeline in mongodb version calls fetch_measurements once per sensor (no pages arg)
    run_pipeline(max_locations=1)

    assert fetch_measurements.call_count >= 1

@patch("mongodb.ingestion.main.write_measurements")
@patch("mongodb.ingestion.main.write_sensors")
@patch("mongodb.ingestion.main.write_locations")
@patch("mongodb.ingestion.main.fetch_measurements")
@patch("mongodb.ingestion.main.fetch_sensors")
@patch("mongodb.ingestion.main.fetch_locations")
def test_pipeline_no_sensors(
    fetch_locations,
    fetch_sensors,
    fetch_measurements,
    write_locations,
    write_sensors,
    write_measurements,
):

    fetch_locations.return_value = [fake_location(1)]
    fetch_sensors.return_value = []

    run_pipeline(max_locations=1)

    fetch_sensors.assert_called_once()
    fetch_measurements.assert_not_called()

@patch("mongodb.ingestion.main.write_measurements")
@patch("mongodb.ingestion.main.write_sensors")
@patch("mongodb.ingestion.main.write_locations")
@patch("mongodb.ingestion.main.fetch_measurements")
@patch("mongodb.ingestion.main.fetch_sensors")
@patch("mongodb.ingestion.main.fetch_locations")
def test_pipeline_respects_max_locations(
    fetch_locations,
    fetch_sensors,
    fetch_measurements,
    write_locations,
    write_sensors,
    write_measurements,
):
    # 10 locations returned by the fake API
    fetch_locations.return_value = [fake_location(i) for i in range(1, 11)]
    fetch_sensors.return_value = [{"id": 101}]
    fetch_measurements.return_value = [{"value": 25.5}]

    run_pipeline(max_locations=3)

    # We should only process 3 locations
    assert fetch_sensors.call_count == 3
