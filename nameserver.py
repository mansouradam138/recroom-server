import http.server
import ssl
import json
import os
import subprocess
import sys

cert_file = "server.pem"

if not os.path.exists(cert_file):
    print("Generating SSL certificate...")
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "cryptography", "--user"], check=True)
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"rec.net")])
    
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
        key.public_key()
    ).serial_number(x509.random_serial_number()).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"rec.net"), x509.DNSName(u"*.rec.net")]),
        critical=False,
    ).sign(key, hashes.SHA256())

    with open(cert_file, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print("SSL certificate generated!")

class RecRoomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"[HIT] GET: {self.path}")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {
            "ApiBaseUrl": "https://127.0.0.1",
            "ImagesBaseUrl": "https://127.0.0.1",
            "MatchmakingUrl": "https://127.0.0.1",
            "PhotonServerIp": "127.0.0.1:5055"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        print(f"[HIT] POST: {self.path}")
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
    server_address = ('127.0.0.1', 443)
    httpd = http.server.HTTPServer(server_address, RecRoomHandler)
    
    # Use modern SSLContext instead of deprecated wrap_socket
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_file)
    httpd.socket = context.wrap_socket(httpd.socket)
    
    print("HTTPS Rec Room Secure Backend active on port 443")
    httpd.serve_forever()