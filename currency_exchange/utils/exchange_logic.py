from models.currency_model import CurrencyModel
from models.exchange_rate_model import ExchangeRateModel

def calculate_exchange(from_code, to_code, amount):
    base = CurrencyModel.get_by_code(from_code)
    target = CurrencyModel.get_by_code(to_code)
    if not base or not target:
        return None, "Currency not found"

    # Direct pair
    rate = ExchangeRateModel.get(base["ID"], target["ID"])
    if rate:
        return amount * rate["Rate"], rate["Rate"]

    # Reverse pair
    reverse = ExchangeRateModel.get(target["ID"], base["ID"])
    if reverse:
        inv = 1 / reverse["Rate"]
        return amount * inv, inv

    # Through USD
    usd = CurrencyModel.get_by_code("USD")
    if not usd:
        return None, "USD not in database"
    rate_a = ExchangeRateModel.get(usd["ID"], base["ID"])
    rate_b = ExchangeRateModel.get(usd["ID"], target["ID"])
    if rate_a and rate_b:
        derived = rate_b["Rate"] / rate_a["Rate"]
        return amount * derived, derived

    return None, "No conversion path found"
