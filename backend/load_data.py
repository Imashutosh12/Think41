import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

db_user = 'root'
db_password = 'Ashutosh%402002'  # encode @ as %40
db_host = 'localhost'
db_name = 'ecommerce'

connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_str)

df = pd.read_csv('products.csv')
df.dropna(subset=['sku'], inplace=True)
df['department'] = df['department'].str.strip()

# 1. Insert unique departments
unique_departments = df['department'].unique()
conn = mysql.connector.connect(
    host=db_host, user=db_user, password="Ashutosh@2002", database=db_name
)
cur = conn.cursor()
for dep in unique_departments:
    cur.execute("INSERT IGNORE INTO departments (name) VALUES (%s)", (dep,))
conn.commit()

# 2. Map department names to IDs
cur.execute("SELECT id, name FROM departments")
dep_map = {name: id for (id, name) in cur.fetchall()}
df['department_id'] = df['department'].map(dep_map)
df = df.drop(columns=['department'])

product_columns = [
    'id', 'cost', 'category', 'name', 'brand', 'retail_price',
    'sku', 'distribution_center_id', 'department_id'
]
df_to_load = df[[col for col in product_columns if col in df.columns]]

df_to_load.to_sql('products', con=engine, if_exists='append', index=False)
print("✅ Data loaded into MySQL successfully with normalized departments!")

cur.close()
conn.close()
