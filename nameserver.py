import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def catch_all(path):
    print(f"[REC ROOM TRAFFIC] Method: {request.method} | Path: /{path} | Query: {request.args}")
    return jsonify({
        "api": "https://your-service-name.onrender.com",
        "accounts": "https://recroom-server-dg8n.onrender.com",
        "match": "https://recroom-server-dg8n.onrender.com",
        "image": "https://recroom-server-dg8n.onrender.com",
        "status": "online"
    })

if __name__ == "__main__":
    # Render automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
