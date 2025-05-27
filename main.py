from utils.extract import extract_products
from utils.transform import transform_data
from utils.load import load_data

df = extract_products()

print("Ini adalah hasil dari extract data")
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
print("jumlah duplikat adalah", df.duplicated().sum())

df_clean = transform_data(df)

print("==========================")
print("Ini adalah hasil dari transform data")
print(df_clean.head())
print(df_clean.info())
print(df_clean.describe())
print(df_clean.isnull().sum())
print("jumlah duplikat adalah", df_clean.duplicated().sum())

print("==========================")
print("Ini adalah hasil dari load data")
load_data(df_clean)

