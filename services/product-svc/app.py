import os
import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

VERSION = os.environ.get("VERSION", "v1")

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "electronics"},
    {"id": 2, "name": "Headphones", "price": 149.99, "category": "electronics"},
    {"id": 3, "name": "Backpack", "price": 79.99, "category": "accessories"},
    {"id": 4, "name": "Keyboard", "price": 129.99, "category": "electronics"},
    {"id": 5, "name": "Mouse", "price": 49.99, "category": "electronics"},
]

DISCOUNTS = {1: 10, 2: 5, 4: 15}  # product_id -> discount %


def enrich(product):
    """Add discount field for v2."""
    p = dict(product)
    if VERSION == "v2":
        p["discount"] = DISCOUNTS.get(p["id"], 0)
    return p


@app.route("/products", methods=["GET"])
def list_products():
    return jsonify([enrich(p) for p in PRODUCTS])


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return jsonify(enrich(p))
    abort(404, description="Product not found")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": VERSION})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
