import http.server
import json
import os

class RecRoomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"[GET Request] {self.path}")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        # Automatically grab your Render public URL
        render_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost")
        
        response = {
            "ApiBaseUrl": render_url,
            "ImagesBaseUrl": render_url,
            "MatchmakingUrl": render_url,
            "PhotonServerIp": "your-photon-server-ip:5055"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        print(f"[POST Request] {self.path}")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        response = {
            "success": True,
            "Token": "local_bypass_token",
            "Player": {"AccountID": 1, "Username": "Adam"}
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    # Render assigns a dynamic port via environment variables
    port = int(os.environ.get('PORT', 10000))
    
    # Must bind to 0.0.0.0 so Render can detect the port publicly
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, RecRoomHandler)
    
    print(f"Rec Room Cloud Backend active on port {port}")
    httpd.serve_forever()
