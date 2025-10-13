import json
from urllib.parse import parse_qs
from models.currency_model import CurrencyModel
from models.exchange_rate_model import ExchangeRateModel
from views.json_view import json_response
from utils.exchange_logic import calculate_exchange

class ExchangeRateController:
    @staticmethod
    def list(request):
        rows = ExchangeRateModel.all()
        data = [dict(row) for row in rows]
        return json_response(data, 200)

    @staticmethod
    def get(request, pair):
        if not pair or len(pair) < 6:
            return json_response({"message": "Bad pair format"}, 400)
        base_code, target_code = pair[:3], pair[3:]
        base = CurrencyModel.get_by_code(base_code)
        target = CurrencyModel.get_by_code(target_code)
        if not base or not target:
            return json_response({"message": "Currency not found"}, 404)
        rate = ExchangeRateModel.get(base["ID"], target["ID"])
        if not rate:
            return json_response({"message": "Exchange rate not found"}, 404)
        return json_response(dict(rate), 200)

    @staticmethod
    def create(request, body):
        params = parse_qs(body)
        base_code = params.get("baseCurrencyCode", [None])[0]
        target_code = params.get("targetCurrencyCode", [None])[0]
        rate = params.get("rate", [None])[0]
        if not all([base_code, target_code, rate]):
            return json_response({"message": "Missing fields"}, 400)

        base = CurrencyModel.get_by_code(base_code)
        target = CurrencyModel.get_by_code(target_code)
        if not base or not target:
            return json_response({"message": "Currency not found"}, 404)

        if ExchangeRateModel.get(base["ID"], target["ID"]):
            return json_response({"message": "Pair exists"}, 409)

        ExchangeRateModel.insert(base["ID"], target["ID"], float(rate))
        data = ExchangeRateModel.get(base["ID"], target["ID"])
        return json_response(dict(data), 201)

    @staticmethod
    def update(request, pair, body):
        params = parse_qs(body)
        rate = params.get("rate", [None])[0]
        if not rate:
            return json_response({"message": "Missing rate"}, 400)
        base_code, target_code = pair[:3], pair[3:]
        base = CurrencyModel.get_by_code(base_code)
        target = CurrencyModel.get_by_code(target_code)
        if not base or not target:
            return json_response({"message": "Currency not found"}, 404)
        if not ExchangeRateModel.get(base["ID"], target["ID"]):
            return json_response({"message": "Pair not found"}, 404)
        ExchangeRateModel.update(base["ID"], target["ID"], float(rate))
        data = ExchangeRateModel.get(base["ID"], target["ID"])
        return json_response(dict(data), 200)
