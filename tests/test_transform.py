import pytest
import sys
import os
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
from utils.transform import transform_data

def test_transform_data_cleaning():
    data = {
        "Title": ["Product A", "Product B", "Unknown Product", "Product A"],
        "Price": ["$10.00", "$15.50", "$0.00", "$10.00"],
        "Rating": ["⭐ 4.5 / 5", "⭐ 3.8 / 5", "⭐ 0.0 / 5", "⭐ 4.5 / 5"],
        "Colors": ["3 Colors", "5 Colors", "1 Colors", "3 Colors"],
        "Size": ["Size: M", "Size: L", "Size: S", "Size: M"],
        "Gender": ["Gender: Men", "Gender: Women", "Gender: Unisex", "Gender: Men"]
    }
    df = pd.DataFrame(data)

    transformed_df = transform_data(df)

    # 1. Unknown Product harus terhapus
    assert "Unknown Product" not in transformed_df["Title"].values

    # 2. Tidak ada duplikat
    assert transformed_df.duplicated().sum() == 0

    # 3. Tidak ada nilai null
    assert transformed_df.isnull().sum().sum() == 0

    # 4. Kolom Price dikonversi ke float dalam Rupiah
    assert transformed_df["Price"].dtype == float
    assert transformed_df["Price"].iloc[0] == 160000.0  # $10 * 16000

    # 5. Kolom Rating dikonversi ke float
    assert transformed_df["Rating"].dtype == float
    assert transformed_df["Rating"].iloc[0] == 4.5

    # 6. Kolom Colors dikonversi ke int
    assert transformed_df["Colors"].dtype == int
    assert transformed_df["Colors"].iloc[0] == 3

    # 7. Size dan Gender dibersihkan dari prefix
    assert all(~transformed_df["Size"].str.contains("Size:"))
    assert all(~transformed_df["Gender"].str.contains("Gender:"))

    # 8. Panjang baris akhir seharusnya 2 (karena 1 unknown + 1 duplikat dihapus dari 4)
    assert len(transformed_df) == 2


def test_transform_empty_df():
    df = pd.DataFrame()
    result = transform_data(df)

    # Harus tetap kosong dan tidak error
    assert result.empty
