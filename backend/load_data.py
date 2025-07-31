# load_data.py (normalized departments version)
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

db_user = 'root'
db_password = 'Ashutosh%402002'
db_host = 'localhost'
db_name = 'ecommerce'

connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_str)

# 1. Load the CSV and clean
df = pd.read_csv('products.csv')
df.dropna(subset=['sku'], inplace=True)
df['department'] = df['department'].str.strip()  # remove whitespace from department names

# 2. Insert unique departments (ignore if already present)
unique_departments = df['department'].unique()
conn = mysql.connector.connect(
    host=db_host, user=db_user, password="Ashutosh@2002", database=db_name
)
cur = conn.cursor()
for dep in unique_departments:
    cur.execute("INSERT IGNORE INTO departments (name) VALUES (%s)", (dep,))
conn.commit()

# 3. Build department name -> id mapping
cur.execute("SELECT id, name FROM departments")
dep_map = {name: id for (id, name) in cur.fetchall()}

# 4. Add department_id to DataFrame
df['department_id'] = df['department'].map(dep_map)

# 5. Drop (now unused) department name column
df = df.drop(columns=['department'])

# (Optional) Fix any missing department_id (shouldn't happen if departments are correct)
if df['department_id'].isnull().any():
    raise Exception("Some products have unmatched departments!")

# 6. Write to MySQL, only the columns present in the DB
product_columns = [
    'id', 'cost', 'category', 'name', 'brand', 'retail_price',
    'sku', 'distribution_center_id', 'department_id'
]
# Filter columns based on what's in `products` table
df_to_load = df[[col for col in product_columns if col in df.columns]]

# If table was already populated, you may want to use 'replace', otherwise use 'append'.
df_to_load.to_sql('products', con=engine, if_exists='append', index=False)

print("✅ Data loaded into MySQL successfully with normalized departments!")

cur.close()
conn.close()
