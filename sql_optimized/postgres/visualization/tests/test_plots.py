import pandas as pd
from unittest.mock import patch
from pathlib import Path

from postgres.visualization.plots import generate_plots

import pytest

@pytest.fixture
def fake_df():
    return pd.DataFrame({
        "city": ["A", "B"],
        "avg_pm10": [10, 20],
        "month": ["2024-01", "2024-02"],
        "avg_value": [5, 7],
        "day": ["2024-01-01", "2024-01-02"]
    })

@patch("postgres.visualization.plots.pd.read_csv")
@patch("postgres.visualization.plots.plt.savefig")
def test_reads_all_csv_files(mock_savefig, mock_read_csv, fake_df):
    mock_read_csv.return_value = fake_df
    generate_plots(base_path=Path("dummy"))
    assert mock_read_csv.call_count == 4


@patch("postgres.visualization.plots.pd.read_csv")
@patch("postgres.visualization.plots.plt.savefig")
def test_saves_four_figures(mock_savefig, mock_read_csv, fake_df):
    mock_read_csv.return_value = fake_df
    generate_plots(base_path=Path("dummy"))
    assert mock_savefig.call_count == 4


@patch("postgres.visualization.plots.pd.read_csv")
@patch("postgres.visualization.plots.plt.savefig")
def test_expected_output_files(mock_savefig, mock_read_csv, fake_df):
    mock_read_csv.return_value = fake_df
    generate_plots(base_path=Path("dummy"))
    expected_files = {
        "top10_pm10_by_city.png",
        "monthly_trend_pm10.png",
        "comparison_pm10.png",
        "daily_avg_rotterdam.png",
    }
    saved_files = {call.args[0] for call in mock_savefig.call_args_list}

    assert saved_files == expected_files

