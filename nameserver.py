from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def catch_all(path):
    # Logs incoming traffic from the game client
    print(f"[REC ROOM TRAFFIC] Method: {request.method} | Path: /{path} | Query: {request.args}")
    
    # Returns local endpoint mappings to catch game bootstrap calls
    return jsonify({
        "api": "http://127.0.0.1",
        "accounts": "http://127.0.0.1",
        "match": "http://127.0.0.1",
        "image": "http://127.0.0.1",
        "status": "online"
    })

if __name__ == "__main__":
    import sys
    print("[-] Starting local Rec Room nameserver on port 80...")
    try:
        app.run(host="0.0.0.0", port=80, debug=False)
    except PermissionError:
        print("\n[!] ERROR: Port 80 requires Administrator privileges on Windows!")
        print("[!] Open your Command Prompt or PowerShell as Administrator and run the script again.\n")
        sys.exit(1)
