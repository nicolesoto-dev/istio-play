import os
import time
import random
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

SLOW_MODE = os.environ.get("SLOW_MODE", "false").lower() == "true"
SLOW_MIN = float(os.environ.get("SLOW_MIN", "2.0"))
SLOW_MAX = float(os.environ.get("SLOW_MAX", "5.0"))

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

INVENTORY = {
    1: {"product_id": 1, "quantity": 150, "warehouse": "zone-a"},
    2: {"product_id": 2, "quantity": 300, "warehouse": "zone-a"},
    3: {"product_id": 3, "quantity": 50, "warehouse": "zone-b"},
    4: {"product_id": 4, "quantity": 200, "warehouse": "zone-b"},
    5: {"product_id": 5, "quantity": 500, "warehouse": "zone-a"},
}


@app.route("/inventory/<int:product_id>", methods=["GET"])
def get_inventory(product_id):
    # Slow mode: simulate degradation
    if SLOW_MODE:
        delay = random.uniform(SLOW_MIN, SLOW_MAX)
        app.logger.info(f"Slow mode: sleeping {delay:.1f}s for product {product_id}")
        time.sleep(delay)

    inv = INVENTORY.get(product_id)
    if not inv:
        abort(404, description="Inventory not found")
    return jsonify(inv)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "inventory-svc", "slow_mode": SLOW_MODE})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
