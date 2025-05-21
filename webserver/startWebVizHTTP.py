#!/usr/bin/env python3
import os
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
        print(f"INFO: Server started at {url}.")
        print("INFO: press [Ctrl+C] to shutdown server.")
        
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever() # nice!
        except KeyboardInterrupt:
            print("\nINFO: Server shutdown initiated...")
            httpd.shutdown()
            print("\nINFO: Server shutdown.")

if __name__ == "__main__":
    # standard arg parsing
    parser = argparse.ArgumentParser(description="INFO: Localhost HTTP-Webserver startup for visualization.")
    parser.add_argument("-p", "--port", type=int, default=PORT, help=f"Port for the server (standard: {PORT}).")
    parser.add_argument("--no-browser", action="store_true", help="Option to not open browser automatically.")
    parser.add_argument("-f", "--file", type=str, default="index.html", help="Used root html file (standard: index.html)")
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    initServer(args.port, not args.no_browser, args.file)