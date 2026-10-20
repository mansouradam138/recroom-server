import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({
        "status": "Online",
        "message": "Rec Room Local Nameserver Active"
    })

# Core configuration endpoints requested during client boot
@app.route("/api/config/v1", methods=["GET"])
@app.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "ServerType": "LocalCustom",
        "APIEndpoint": "http://127.0.0.1",
        "AccountsEndpoint": "http://127.0.0.1",
        "MatchmakingEndpoint": "http://127.0.0.1",
        "ImageEndpoint": "http://127.0.0.1",
        "WebSocketEndpoint": "ws://127.0.0.1",
        "IsEnabled": True,
        "BuildVersion": "May 2022"
    })

# Authentication endpoints to bypass login validation
@app.route("/api/authenticator/v2/login", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    return jsonify({
        "Token": "local_dev_token_12345",
        "AccountID": 1,
        "Username": "LocalPlayer",
        "DisplayName": "Player",
        "IsSubscribed": True,
        "Success": True
    })

# Matchmaking endpoints to handle room/server lists
@app.route("/api/matchmaking/v1/getservers", methods=["GET", "POST"])
def get_servers():
    return jsonify({
        "Servers": [
            {
                "ServerID": "local-room-1",
                "IP": "127.0.0.1",
                "Port": 20001,
                "RoomName": "Home",
                "PlayerCount": 1
            }
        ]
    })

# Catch-all fallback for any other client requests so it never returns a 404 crash
@app.route("/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def catch_all(subpath):
    print(f"[TRAFFIC] Hit Route: /{subpath} | Method: {request.method} | Args: {request.args}")
    return jsonify({
        "success": True,
        "data": None,
        "path": subpath
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    print(f"[*] Starting full Rec Room Nameserver on port {port}...")
    try:
        app.run(host="0.0.0.0", port=port, debug=False)
    except PermissionError:
        print("\n[!] ERROR: Port 80 requires Administrator privileges on Windows!")
        print("[!] Run your Command Prompt as Administrator and restart the script.\n")
