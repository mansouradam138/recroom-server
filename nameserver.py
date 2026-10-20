import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Rec Room Revival Online Backend Active"
    })

# Client configuration manifest endpoint
@app.route("/api/config/v1/current", methods=["GET"])
@app.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "Config": {
            "ServerType": "OnlineCloud",
            "IsEnabled": True
        }
    })

# Authentication / Login endpoint
@app.route("/api/authenticator/v2/login", methods=["POST", "GET"])
def login():
    return jsonify({
        "Token": "online_revival_token_12345",
        "Account": {
            "AccountId": 1,
            "Username": "Player",
            "DisplayName": "Player",
            "IsJunior": False
        },
        "Error": None
    })

# Matchmaking room list endpoint
@app.route("/api/matchmaking/v1/getservers", methods=["GET", "POST"])
def get_servers():
    return jsonify({
        "Servers": []
    })

# Catch-all route to ensure any incoming game request returns valid JSON instead of a 404 crash
@app.route("/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def catch_all(subpath):
    print(f"[ONLINE TRAFFIC] Path: /{subpath} | Method: {request.method}")
    return jsonify({
        "Success": True,
        "Route": subpath,
        "Message": "Handled by online backend"
    })

if __name__ == "__main__":
    # Render assigns its own dynamic port via environment variables
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
