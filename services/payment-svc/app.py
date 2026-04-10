import os
import time
import random
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Configurable failure/delay rates via env vars
ERROR_RATE = float(os.environ.get("ERROR_RATE", "0.2"))      # 20% errors
SLOW_RATE = float(os.environ.get("SLOW_RATE", "0.3"))        # 30% slow responses
SLOW_MIN = float(os.environ.get("SLOW_MIN", "2.0"))          # min delay seconds
SLOW_MAX = float(os.environ.get("SLOW_MAX", "3.0"))          # max delay seconds

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


@app.route("/payments", methods=["POST"])
def process_payment():
    data = request.get_json(force=True, silent=True) or {}
    order_id = data.get("order_id", "unknown")
    amount = data.get("amount", 0)

    # Artificial delay
    if random.random() < SLOW_RATE:
        delay = random.uniform(SLOW_MIN, SLOW_MAX)
        app.logger.info(f"Injecting delay: {delay:.1f}s for order {order_id}")
        time.sleep(delay)

    # Artificial error
    if random.random() < ERROR_RATE:
        app.logger.info(f"Injecting 503 error for order {order_id}")
        abort(503, description="Payment service temporarily unavailable")

    return jsonify({
        "order_id": order_id,
        "amount": amount,
        "status": "approved",
        "transaction_id": f"txn-{random.randint(100000, 999999)}",
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "payment-svc"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
