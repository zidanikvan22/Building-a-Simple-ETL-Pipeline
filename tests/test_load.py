import pytest
import sys
import os
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
from utils.load import load_data

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Title": ["Product A", "Product B"],
        "Price": [160000.0, 248000.0],
        "Rating": [4.5, 3.8],
        "Colors": [3, 5],
        "Size": ["M", "L"],
        "Gender": ["Men", "Women"]
    })


def test_load_data_success(tmp_path, sample_df):
    # Simpan file ke direktori temporer
    file_path = tmp_path / "test_output.csv"
    load_data(sample_df, output_path=str(file_path))

    # memastikan file benar-benar tersimpan
    assert os.path.exists(file_path)

    # Baca kembali dan cocokkan isinya
    df_loaded = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df_loaded, sample_df)


def test_load_data_empty_df(tmp_path):
    df_empty = pd.DataFrame()
    file_path = tmp_path / "empty_output.csv"
    load_data(df_empty, output_path=str(file_path))

    # File tidak dibuat
    assert not os.path.exists(file_path)


def test_load_data_permission_error(monkeypatch, sample_df):
    # Simulasikan PermissionError
    def mock_to_csv(*args, **kwargs):
        raise PermissionError("Mocked permission error")

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    # Tidak harus error, hanya harus tidak membuat file
    load_data(sample_df, output_path="forbidden.csv")


def test_load_data_file_not_found(monkeypatch, sample_df):
    # Simulasikan FileNotFoundError
    def mock_to_csv(*args, **kwargs):
        raise FileNotFoundError("Mocked file not found")

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    load_data(sample_df, output_path="invalid_path/test.csv")