import os
import time
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "ecommerce")
DB_USER = os.getenv("DB_USER", "ecommerce")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ecommercepass")


def get_connection():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        except psycopg2.OperationalError:
            time.sleep(2)

    raise Exception("Could not connect to PostgreSQL")


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price INTEGER NOT NULL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("""
            INSERT INTO products (name, price)
            VALUES
                ('Laptop', 60000),
                ('Smartphone', 30000),
                ('Headphones', 5000)
        """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/api/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return jsonify({
            "service": "ecommerce-backend",
            "status": "healthy",
            "database": "connected"
        })
    except Exception:
        return jsonify({
            "service": "ecommerce-backend",
            "status": "unhealthy",
            "database": "disconnected"
        }), 500


@app.route("/api/products")
def products():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, price FROM products ORDER BY id")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id": row[0], "name": row[1], "price": row[2]}
        for row in rows
    ])


@app.route("/api/revenue")
def revenue():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COALESCE(SUM(price), 0) FROM products")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({
        "currency": "INR",
        "total_revenue": total
    })


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
