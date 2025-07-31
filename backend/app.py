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

# ----------- Products Endpoints ------------

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

# ----------- Departments API (Milestone 5) ------------

# List all departments and include product counts for each
@app.route('/api/departments', methods=['GET'])
def get_departments():
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True, buffered=True) as cur:
            cur.execute("""
                SELECT d.id, d.name, COUNT(p.id) AS product_count
                FROM departments d
                LEFT JOIN products p ON d.id = p.department_id
                GROUP BY d.id, d.name
            """)
            departments = cur.fetchall()
    finally:
        conn.close()
    return jsonify({"departments": departments}), 200

# Get details (name, id) for one department by id
@app.route('/api/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True, buffered=True) as cur:
            cur.execute("SELECT id, name FROM departments WHERE id = %s", (department_id,))
            department = cur.fetchone()
    finally:
        conn.close()
    if not department:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(department), 200

# Get all products for a given department id
@app.route('/api/departments/<int:department_id>/products', methods=['GET'])
def get_department_products(department_id):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True, buffered=True) as cur:
            # Get department name (for response)
            cur.execute("SELECT name FROM departments WHERE id = %s", (department_id,))
            dep = cur.fetchone()
            if not dep:
                return jsonify({"error": "Department not found"}), 404

            # Get all products in that department
            cur.execute("""
                SELECT p.id, p.name, p.category, p.brand, p.retail_price, p.sku
                FROM products p
                WHERE p.department_id = %s
            """, (department_id,))
            products = cur.fetchall()
    finally:
        conn.close()
    return jsonify({"department": dep["name"], "products": products}), 200

# ----------- General Error Handlers ------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
