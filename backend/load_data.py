# load_data.py
import pandas as pd
from sqlalchemy import create_engine

db_user = 'root'
db_password = 'Ashutosh%402002'
db_host = 'localhost'
db_name = 'ecommerce'

connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_str)

df = pd.read_csv('products.csv')
df.dropna(subset=['sku'], inplace=True)
df.to_sql('products', con=engine, if_exists='append', index=False)

print("✅ Data loaded into MySQL successfully.")
