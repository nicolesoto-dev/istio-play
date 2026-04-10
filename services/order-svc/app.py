import os
import json
import uuid
from flask import Flask, jsonify, request, abort
import requests

app = Flask(__name__)

PRODUCT_SVC_URL = os.environ.get("PRODUCT_SVC_URL", "http://product-svc:8080")
PAYMENT_SVC_URL = os.environ.get("PAYMENT_SVC_URL", "http://payment-svc:8080")

# Istio trace headers to propagate
TRACE_HEADERS = [
    "x-request-id",
    "x-b3-traceid",
    "x-b3-spanid",
    "x-b3-parentspanid",
    "x-b3-sampled",
    "x-b3-flags",
    "x-ot-span-context",
    "traceparent",
    "tracestate",
]


def extract_trace_headers(req):
    headers = {}
    for h in TRACE_HEADERS:
        val = req.headers.get(h)
        if val:
            headers[h] = val
    return headers


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(force=True, silent=True) or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        abort(400, description="product_id is required")

    trace = extract_trace_headers(request)

    # 1. Verify product exists
    try:
        resp = requests.get(
            f"{PRODUCT_SVC_URL}/products/{product_id}",
            headers=trace,
            timeout=5,
        )
        if resp.status_code == 404:
            abort(404, description="Product not found")
        resp.raise_for_status()
        product = resp.json()
    except requests.exceptions.RequestException as e:
        abort(502, description=f"product-svc unavailable: {e}")

    # 2. Process payment
    amount = product["price"] * quantity
    try:
        resp = requests.post(
            f"{PAYMENT_SVC_URL}/payments",
            json={"order_id": str(uuid.uuid4()), "amount": amount},
            headers={**trace, "Content-Type": "application/json"},
            timeout=10,
        )
        resp.raise_for_status()
        payment = resp.json()
    except requests.exceptions.RequestException as e:
        abort(502, description=f"payment-svc unavailable: {e}")

    order = {
        "order_id": payment.get("order_id", str(uuid.uuid4())),
        "product": product,
        "quantity": quantity,
        "total": amount,
        "payment_status": payment.get("status", "unknown"),
    }
    return jsonify(order), 201


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "order-svc"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
