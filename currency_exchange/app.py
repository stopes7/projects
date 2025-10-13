from http.server import BaseHTTPRequestHandler, HTTPServer
from controllers.currency_controller import CurrencyController
from controllers.exchange_rate_controller import ExchangeRateController
from utils.exchange_logic import calculate_exchange
from urllib.parse import urlparse, parse_qs
from views.json_view import json_response

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        try:
            if path == "/currencies":
                body, status, headers = CurrencyController.list(self)
            elif path.startswith("/currency/"):
                code = path.split("/")[-1]
                body, status, headers = CurrencyController.get(self, code)
            elif path == "/exchangeRates":
                body, status, headers = ExchangeRateController.list(self)
            elif path.startswith("/exchangeRate/"):
                pair = path.split("/")[-1]
                body, status, headers = ExchangeRateController.get(self, pair)
            elif path.startswith("/exchange"):
                from_code = query.get("from", [None])[0]
                to_code = query.get("to", [None])[0]
                amount = float(query.get("amount", [0])[0])
                converted, rate = calculate_exchange(from_code, to_code, amount)
                if converted is None:
                    body, status, headers = json_response({"message": rate}, 404)
                else:
                    body, status, headers = json_response({
                        "from": from_code,
                        "to": to_code,
                        "rate": rate,
                        "amount": amount,
                        "convertedAmount": round(converted, 2)
                    }, 200)
            else:
                body, status, headers = json_response({"message": "Not found"}, 404)

            self.send_response(status)
            for k, v in headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body.encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"message": str(e)}).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        path = self.path

        if path == "/currencies":
            body, status, headers = CurrencyController.create(self, body)
        elif path == "/exchangeRates":
            body, status, headers = ExchangeRateController.create(self, body)
        else:
            body, status, headers = json_response({"message": "Not found"}, 404)

        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body.encode())

    def do_PATCH(self):
        path = self.path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        if path.startswith("/exchangeRate/"):
            pair = path.split("/")[-1]
            body, status, headers = ExchangeRateController.update(self, pair, body)
        else:
            body, status, headers = json_response({"message": "Not found"}, 404)
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body.encode())

def run(port=8080):
    server = HTTPServer(("localhost", port), RequestHandler)
    print(f"🚀 Server running at http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
