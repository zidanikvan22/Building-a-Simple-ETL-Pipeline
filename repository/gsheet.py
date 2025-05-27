import sys
import os
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import extract_products
from utils.transform import transform_data

def load_to_google_sheet(df: pd.DataFrame, sheet_name: str, creds_path: str = "google-sheets-api.json"):
    # Setup Google Sheets API
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(credentials)

    # Buka Google Sheet
    spreadsheet = client.open(sheet_name)
    worksheet = spreadsheet.sheet1  

    # membersihkan isi worksheet sebelum memasukkan data baru
    worksheet.clear()

    # Tulis DataFrame ke Google Sheet
    set_with_dataframe(worksheet, df)

    print(f"Data berhasil disimpan ke Google Sheet: {sheet_name}")

if __name__ == "__main__":
    # Ekstrak dan transformasi data
    df_raw = extract_products()
    df_clean = transform_data(df_raw)

    # Jalankan penyimpanan ke Google Sheets
    load_to_google_sheet(
        df=df_clean,
        sheet_name="proyek akhir_pemrosesan data",
        creds_path="google-sheets-api.json"
    )
