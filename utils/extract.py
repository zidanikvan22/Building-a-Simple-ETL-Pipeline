import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def extract_products(max_pages=50):
    all_data = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")

        # URL dinamis
        url = "https://fashion-studio.dicoding.dev/" if page == 1 else f"https://fashion-studio.dicoding.dev/page{page}"

        try:
            response = requests.get(url, timeout=10)  # menambahkan timeout
            response.raise_for_status()  # memeriksa status kode HTTP
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Gagal mengambil data dari halaman {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("div", class_="collection-card")
        timestamp = datetime.now().isoformat()

        if not products:
            print(f"[WARNING] Tidak ada produk ditemukan di halaman {page}.")
            continue

        for product in products:
            try:
                title_tag = product.find("h3", class_="product-title")
                title = title_tag.get_text(strip=True) if title_tag else None

                price_tag = product.find("span", class_="price")
                price = price_tag.get_text(strip=True) if price_tag else None

                details = product.find_all("p")
                rating = colors = size = gender = None

                for p in details:
                    text = p.get_text(strip=True)
                    if text.startswith("Rating:"):
                        rating = text.replace("Rating:", "").strip()
                    elif "Colors" in text:
                        colors = text.strip()
                    elif "Size:" in text:
                        size = text.replace("Size:", "").strip()
                    elif "Gender:" in text:
                        gender = text.replace("Gender:", "").strip()

                all_data.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "timestamp": timestamp
                })
            except Exception as e:
                print(f"[ERROR] Gagal memproses produk pada halaman {page}: {e}")
                continue

    if not all_data:
        print("[ERROR] Tidak ada data produk yang berhasil diambil.")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong

    df = pd.DataFrame(all_data)
    return df
