import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        print("[WARNING] DataFrame kosong, tidak ada data untuk ditransformasi.")
        return df

    try:
        # 1. Drop baris dengan "Unknown Product"
        df = df[df["Title"] != "Unknown Product"]

        # 2. Drop nilai null
        df = df.dropna()

        # 3. Drop duplikat
        df = df.drop_duplicates()

        # 4. membersihkan kolom Price: menghilangkan simbol "$" dan konversi ke Rupiah (float)
        if "Price" in df.columns:
            df["Price"] = (
                df["Price"]
                .astype(str)
                .str.replace(r"[^0-9.]", "", regex=True)
                .astype(float)
                * 16000
            )
        else:
            print("[WARNING] Kolom 'Price' tidak ditemukan.")

        # 5. membersihkan kolom Rating: ambil angka dari format "4.5/5"
        if "Rating" in df.columns:
            df["Rating"] = df["Rating"].astype(str).str.extract(r"([0-5]\.\d)").astype(float)
        else:
            print("[WARNING] Kolom 'Rating' tidak ditemukan.")

        # 6. Bersihkan kolom Colors: ambil angka dari format "3 Colors"
        if "Colors" in df.columns:
            df["Colors"] = df["Colors"].astype(str).str.extract(r"(\d+)").astype(int)
        else:
            print("[WARNING] Kolom 'Colors' tidak ditemukan.")

        # 7. membersihkan kolom Size dan Gender dari teks tambahan jika ada
        if "Size" in df.columns:
            df["Size"] = df["Size"].astype(str).str.replace("Size:", "", regex=False).str.strip()
        else:
            print("[WARNING] Kolom 'Size' tidak ditemukan.")

        if "Gender" in df.columns:
            df["Gender"] = df["Gender"].astype(str).str.replace("Gender:", "", regex=False).str.strip()
        else:
            print("[WARNING] Kolom 'Gender' tidak ditemukan.")

        # 8. Reset index
        df = df.reset_index(drop=True)

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat transformasi data: {e}")

    return df
