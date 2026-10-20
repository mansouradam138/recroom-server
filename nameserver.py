import http.server
import json
import os

class RecRoomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # This print statement prints to your Render logs instantly:
        print(f"[GET Request] Someone visited path: {self.path}", flush=True)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        render_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost")
        
        response = {
            "ApiBaseUrl": render_url,
            "ImagesBaseUrl": render_url,
            "MatchmakingUrl": render_url,
            "PhotonServerIp": "your-photon-server-ip:5055"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        # This print statement handles incoming login/game requests:
        print(f"[POST Request] Game sent data to: {self.path}", flush=True)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        response = {
            "success": True,
            "Token": "local_bypass_token",
            "Player": {"AccountID": 1, "Username": "Adam"}
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, RecRoomHandler)
    
    # Print statement confirming the server is online:
    print(f"Rec Room Cloud Backend active on port {port}", flush=True)
    httpd.serve_forever()
