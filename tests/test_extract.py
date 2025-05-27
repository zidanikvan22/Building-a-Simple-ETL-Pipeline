import pytest
import sys
import os
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch, Mock
from utils.extract import extract_products
import pandas as pd

mock_html = """
<html>
<body>
    <div class="collection-card">
        <h3 class="product-title">Cool Jacket</h3>
        <span class="price">$49.99</span>
        <p>Rating: ⭐ 4.7 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Unisex</p>
    </div>
</body>
</html>
"""

@patch("utils.extract.requests.get")
def test_extract_products_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html
    mock_get.return_value = mock_response

    df = extract_products(max_pages=1)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    expected_columns = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
    assert all(col in df.columns for col in expected_columns)

    row = df.iloc[0]
    assert row["Title"] == "Cool Jacket"
    assert row["Price"] == "$49.99"
    assert "4.7" in row["Rating"]  

@patch("utils.extract.requests.get")
def test_extract_products_fail(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found for url")
    mock_get.return_value = mock_response

    df = extract_products(max_pages=1)

    assert isinstance(df, pd.DataFrame)
    assert df.empty  # kosong jika halaman gagal dimuat
