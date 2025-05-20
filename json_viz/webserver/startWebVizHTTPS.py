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
            print(f"INFO: Cursor über URL und [Strg+Mouse1] oder in Browser-Addresszeile kopieren: \033[34m{url}\033[0m")

def initHTTPSServer(port, open_browser, filename):
    if not os.path.isfile(CERT_FILE) or not os.path.isfile(KEY_FILE):
        print(f"INFO: ❌ Zertifikat oder Schlüssel nicht jefunden ({CERT_FILE}, {KEY_FILE}).")
        print("INFO: Erstelle Zert mit:\n  openssl req -new -x509 -keyout key.pem -out cert.pem -days 365 -nodes")
        print("INFO: Wenn du in Wundows bist, dann Git Bash oder WSL zuerst aktivieren.")
        return
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("localhost", port), handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    url = f"https://localhost:{port}"
    if filename:
        url += f"/{quote(filename)}"
    print(f"INFO: HTTPS-Server gestartet auf \033[34m{url}\033[0m")
    print("INFO: Selbstsigniertes Zertifikat - Browser zeigt ws. Warnung.")
    print("INFO: [STRG+C] drücken, um Server zu beenden.")

    if open_browser:
        system = platform.system()
        if system == 'Windows':
            try:
                webbrowser.open(url)
            except RuntimeError:
                print(f"INFO: Browser konnte nicht automatisch geöffnet werden.")
                print(f"INFO: URL in Browser kopieren \033[34m{url}\033[0m")
        elif system == 'Linux':
            threading.Timer(DELAY, lambda: openBrowserInLinux(url)).start()
        else:
            print(f"INFO: Exotisches Betriebssystem '{system}', Browser nicht geöffnet.")
            print(f"INFO: URL manuell öffnen: {url}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server Shutdown.")
        httpd.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="INFO: Localhost HTTPS-Webserver für lokale Visualisierung")
    parser.add_argument("-p", "--port", type=int, default=PORT, help=f"Port für den Server (Standard: {PORT})")
    parser.add_argument("--no-browser", action="store_true", help="Browser nicht automatisch öffnen")
    parser.add_argument("-f", "--file", type=str, default="index.html", help="Verwendete HTML-Datei (Standard: index.html)")
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    initHTTPSServer(args.port, not args.no_browser, args.file)
