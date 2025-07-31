import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Replace with your MySQL credentials
db_user = 'root'
db_password = 'Ashutosh@2002'
db_host = 'localhost'
db_name = 'ecommerce'

# SQLAlchemy connection string for MySQL
connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_str)

# Read the CSV file
df = pd.read_csv('products.csv')

# Drop rows with missing SKUs to avoid UNIQUE constraint errors
df.dropna(subset=['sku'], inplace=True)

# Load into MySQL
df.to_sql('products', con=engine, if_exists='append', index=False)

print("✅ Data loaded into MySQL successfully.")
