import pandas as pd
import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import extract_products
from utils.transform import transform_data
from sqlalchemy import create_engine


df = extract_products()
df_clean = transform_data(df)

# Koneksi ke PostgreSQL
host = 'localhost'
port = '5432'
database = 'tesdb'
username = 'xxxxxxx'
password = '*******' 

# Membuat engine SQLAlchemy
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

# Simpan ke tabel baru di PostgreSQL 
table_name = 'products'
df_clean.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data berhasil dimasukkan ke tabel '{table_name}' di database '{database}'.")
