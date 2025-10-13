import json
from urllib.parse import parse_qs
from models.currency_model import CurrencyModel
from views.json_view import json_response

class CurrencyController:
    @staticmethod
    def list(request):
        try:
            data = [dict(row) for row in CurrencyModel.all()]
            return json_response(data, 200)
        except Exception as e:
            return json_response({"message": str(e)}, 500)

    @staticmethod
    def get(request, code):
        if not code:
            return json_response({"message": "Missing code"}, 400)
        row = CurrencyModel.get_by_code(code)
        if not row:
            return json_response({"message": "Currency not found"}, 404)
        return json_response(dict(row), 200)

    @staticmethod
    def create(request, body):
        params = parse_qs(body)
        name = params.get("name", [None])[0]
        code = params.get("code", [None])[0]
        sign = params.get("sign", [None])[0]
        if not all([name, code, sign]):
            return json_response({"message": "Missing fields"}, 400)
        if CurrencyModel.get_by_code(code):
            return json_response({"message": "Currency exists"}, 409)
        new_id = CurrencyModel.insert(name, code, sign)
        row = CurrencyModel.get_by_code(code)
        return json_response(dict(row), 201)
