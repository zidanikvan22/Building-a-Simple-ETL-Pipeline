import pandas as pd
import os

def load_data(df: pd.DataFrame, output_path: str = "product.csv"):
    if df.empty:
        print("[WARNING] DataFrame kosong, tidak ada data yang disimpan.")
        return

    try:
        # Menyimpan sebagai CSV di direktori saat ini
        df.to_csv(output_path, index=False)
        print(f"[INFO] Data berhasil disimpan di {os.path.abspath(output_path)}")

    except PermissionError:
        print(f"[ERROR] Tidak dapat menyimpan file. Periksa izin akses ke file {output_path}.")

    except FileNotFoundError:
        print(f"[ERROR] Direktori tujuan tidak ditemukan: {output_path}")

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat menyimpan data: {e}")
