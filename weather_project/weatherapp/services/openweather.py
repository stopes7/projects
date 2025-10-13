import os
import requests

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
ONECALL_URL = "https://api.openweathermap.org/data/2.5/weather"

class OpenWeatherError(Exception):
    pass

class OpenWeatherClient:
    def __init__(self, api_key: str = OPENWEATHER_KEY, session: requests.Session = None):
        self.api_key = api_key
        self.session = session or requests.Session()

    def search_locations(self, q: str, limit: int = 10):
        params = {"q": q, "limit": limit, "appid": self.api_key}
        r = self.session.get(GEOCODING_URL, params=params, timeout=5)
        if r.status_code != 200:
            raise OpenWeatherError(f"Geocoding error: {r.status_code}")
        return r.json()

    def get_weather(self, lat: float, lon: float, units: str = "metric"):
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": units}
        r = self.session.get(ONECALL_URL, params=params, timeout=5)
        if r.status_code != 200:
            raise OpenWeatherError(f"Weather error: {r.status_code}")
        return r.json()
