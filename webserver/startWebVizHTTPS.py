#!/usr/bin/env python3
import http.server
import ssl
import os
import webbrowser
import argparse
import platform
import threading
from urllib.parse import quote
import subprocess

PORT = 4443
DELAY = 1.0                 # kp wie lang mange systeme brauchen
CERT_FILE = "webserver/cert.pem"      # selbst signiert - keine Kopfschmerzen mit Windows, einfach schon da
KEY_FILE = "webserver/key.pem"        # ansonsten halt wsl oder git bash und dann erstellen

def openBrowserInLinux(url):
    try:
        subprocess.run(['xdg-open', url], check=True)
    except Exception:
        try:
            subprocess.run(['gio', 'open', url], check=True)
        except Exception:
            print(f"INFO: ❌ Browser Start Fail.")
            print(f"INFO: Cursor over URl and press [Ctrl+Mouse1] or copy this url in browser address bar: \033[34m{url}\033[0m")

def initHTTPSServer(port, open_browser, filename):
    if not os.path.isfile(CERT_FILE) or not os.path.isfile(KEY_FILE):
        print(f"INFO: ❌ Certificate and/or key file not found: ({CERT_FILE}, {KEY_FILE}).")
        print("INFO: Create self-signed certificate with command:\n  openssl req -new -x509 -keyout key.pem -out cert.pem -days 365 -nodes")
        print("INFO: If you're on Windows, consider using WSL to create .pem files first and then opt out of WSL again.")
        return
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("localhost", port), handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    url = f"https://localhost:{port}"
    if filename:
        url += f"/{quote(filename)}"
    print(f"INFO: HTTPS-Server started at \033[34m{url}\033[0m")
    print("INFO: Self-signed certificate - browser may show warning.")
    print("INFO: Press [Ctrl+C] to shutdown server.")

    if open_browser:
        system = platform.system()
        if system == 'Windows':
            try:
                webbrowser.open(url)
            except RuntimeError:
                print(f"INFO: Browser could not be opened.")
                print(f"INFO: Copy URL in Browser: \033[34m{url}\033[0m")
        elif system == 'Linux':
            threading.Timer(DELAY, lambda: openBrowserInLinux(url)).start()
        else:
            print(f"INFO: Exotic OS '{system}', Browser not opened.")
            print(f"INFO: Open URL manually: {url}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown initiated...")
        httpd.shutdown()
        print("\n Server shutdown.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="INFO: Localhost HTTPS-Webserver for visualization.")
    parser.add_argument("-p", "--port", type=int, default=PORT, help=f"Port for Server (standard: {PORT}).")
    parser.add_argument("--no-browser", action="store_true", help="Option to not open browser automatically.")
    parser.add_argument("-f", "--file", type=str, default="index.html", help="Used html root file (standard: index.html).")
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    initHTTPSServer(args.port, not args.no_browser, args.file)
