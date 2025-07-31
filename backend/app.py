from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ashutosh@2002',
    'database': 'ecommerce'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Get paginated product list, joined to departments for readable names
@app.route('/api/products', methods=['GET'])
def get_products():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True, buffered=True) as cur:
            cur.execute("""
                SELECT p.id, p.name, p.category, p.brand, p.retail_price, p.sku,
                       p.distribution_center_id, p.department_id, d.name AS department
                FROM products p
                JOIN departments d ON p.department_id = d.id
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            products = cur.fetchall()
    finally:
        conn.close()
    return jsonify(products), 200

# Get single product by id, joined to departments
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True, buffered=True) as cur:
            cur.execute("""
                SELECT p.id, p.name, p.category, p.brand, p.retail_price, p.sku,
                       p.distribution_center_id, p.department_id, d.name AS department
                FROM products p
                JOIN departments d ON p.department_id = d.id
                WHERE p.id = %s
            """, (product_id,))
            product = cur.fetchone()
    finally:
        conn.close()
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

# List all unique departments (for admin or dropdowns)
@app.route('/api/departments', methods=['GET'])
def get_departments():
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True, buffered=True) as cur:
            cur.execute("SELECT id, name FROM departments")
            departments = cur.fetchall()
    finally:
        conn.close()
    return jsonify(departments), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
