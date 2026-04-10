from flask import Flask, jsonify, abort

app = Flask(__name__)

USERS = {
    1: {"id": 1, "name": "Alice", "email": "alice@cloudmart.io", "tier": "premium"},
    2: {"id": 2, "name": "Bob", "email": "bob@cloudmart.io", "tier": "standard"},
    3: {"id": 3, "name": "Charlie", "email": "charlie@cloudmart.io", "tier": "premium"},
}


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = USERS.get(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "user-svc"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
