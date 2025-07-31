# app.py
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

@app.route('/api/products', methods=['GET'])
def get_products():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products LIMIT %s OFFSET %s", (per_page, offset))
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(products), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products WHERE id = 14157", (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
