import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests 
import json


with open('config.json', 'r') as f:
    config = json.load(f)


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.startswith('/exchange_token'):
            self.thankyou_page()
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"<html><head><title></title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(f"<a href=http://www.strava.com/oauth/authorize?client_id={config['strava_client_id']}&response_type=code&redirect_uri=http://localhost:9090/exchange_token&approval_prompt=force&scope=activity:read_all>Authorize here!</a>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    # After-verify page
    def thankyou_page(self):

        dicts = parse_qs(urlparse(self.requestline).query)
        try:
            code = dicts['code'][0]
        except KeyError:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"<html><head><title></title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes(f"<a href=http://www.strava.com/oauth/authorize?client_id={config['strava_client_id']}&response_type=code&redirect_uri=http://localhost:9090/exchange_token&approval_prompt=force&scope=activity:read_all>Authorize here!</a>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title></title></head>", "utf-8"))
        self.wfile.write(bytes("<body>Thank you for verifying!", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

        self.exchange_tokens(dicts)

    # first time token exchange
    def exchange_tokens(self, dicts):
        code = dicts['code'][0]
        params = {
                    'client_id': f"{config['strava_client_id']}",
                    'client_secret': f"{config['strava_client_secret']}",
                    'code': f"{code}",
                    'grant_type': "authorization_code"
                 }
        response = requests.post("https://www.strava.com/api/v3/oauth/token", params=params)
        jfile = response.json()
        with open('config.json', 'r') as f:
            config_new = json.load(f)
            config_new['strava_refresh_token'] = jfile['refresh_token']
            config_new['strava_access_token'] = jfile['access_token']
            config_new['strava_token_expiration'] = jfile['expires_at']
        with open('config.json', 'w') as f:
            json.dump(config_new, f)


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=9090):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

run()