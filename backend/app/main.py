from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 60000
    },
    {
        "id": 2,
        "name": "Smartphone",
        "price": 30000
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 5000
    }
]


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "ecommerce-backend"
    })


@app.route("/api/products")
def get_products():
    return jsonify(products)


@app.route("/api/revenue")
def revenue():
    total = sum(product["price"] for product in products)

    return jsonify({
        "total_revenue": total,
        "currency": "INR"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
