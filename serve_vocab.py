import http.server, socket, os, sys, threading

port = 8080
file_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(file_dir, "vocab.html")

if not os.path.exists(html_path):
    print(f"File not found: {html_path}")
    sys.exit(1)

def get_lan_ip():
    ips = []
    try:
        hostname = socket.gethostname()
        for addr in socket.gethostbyname_ex(hostname)[2]:
            ips.append(addr)
    except:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.append(s.getsockname()[0])
        s.close()
    except:
        pass
    for ip in ips:
        if ip.startswith("192.168."):
            return ip
    for ip in ips:
        if not ip.startswith("172."):
            return ip
    return ips[0] if ips else "127.0.0.1"

local_ip = get_lan_ip()
os.chdir(file_dir)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        p = self.path.split('?')[0].rstrip('/')
        if p == '' or not os.path.exists(os.path.join(file_dir, p.lstrip('/'))):
            self.path = '/vocab.html'
        super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]} {args[2]}")

server = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
print(f"\n  ==============================")
print(f"  English Galaxy Server")
print(f"  Open on your phone:")
print(f"  http://{local_ip}:{port}")
print(f"  ==============================")
print(f"  On this PC: http://localhost:{port}")
print(f"  Press Ctrl+C to stop\n")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n  Server stopped.")
    server.server_close()
