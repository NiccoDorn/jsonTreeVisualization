#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import argparse
from urllib.parse import quote

PORT = 8000
DELAY = 1.0 # kp, wie lang manche systeme brauchen

def initServer(port, open_browser, filename):
    # dir = os.getcwd()
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}"
        if filename:
            url += f"/{quote(filename)}"
        print(f"INFO: Server gestartet auf {url}")
        print("INFO: STRG+C drücken, um den Server zu beenden.")
        
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever() # nice!
        except KeyboardInterrupt:
            print("\nINFO: Server wird beendet...")
            httpd.shutdown()

if __name__ == "__main__":
    # standard arg parsing
    parser = argparse.ArgumentParser(description="INFO: Localhost HTTP-Webserver Startup für Visualisierung")
    parser.add_argument("-p", "--port", type=int, default=PORT, help=f"Port für den Server (Standard: {PORT})")
    parser.add_argument("--no-browser", action="store_true", help="Browser nicht automatisch öffnen")
    parser.add_argument("-f", "--file", type=str, default="index.html", help="Verwendete HTML-Datei (Standard: index.html)")
    args = parser.parse_args()
    initServer(args.port, not args.no_browser, args.file)