#third-party
from dotenv import load_dotenv
import requests

#built-in
from functools import wraps
from datetime import datetime
import os
import json
import time

load_dotenv()
weatherAPI = os.environ.get('weatherAPI')
RateLimit = 1000
TRACKER_FILE = "api_tracker.json"


def track_api_call(api_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Load usage log
            today = datetime.today().date()
            date_str = today.strftime("%Y-%m-%d")
            if os.path.exists(TRACKER_FILE):
                with open(TRACKER_FILE, "r") as f:
                    usage = json.load(f)
                    if usage["Date"] != date_str:
                        usage = {"total_calls": 0, "calls": [], "Date": date_str}
            else:
                usage = {"total_calls": 0, "calls": [], "Date": date_str}
            output = func(*args, *kwargs)
            # Update tracking
            usage["total_calls"] += 1
            usage["calls"].append({
                "timestamp": datetime.now().isoformat(),
                "API Name": api_name,
            })

            # Save usage log
            with open(TRACKER_FILE, "w") as f:
                json.dump(usage, f, indent=2)
            return output
        return wrapper
    return decorator

@track_api_call('Geocoding API')
def getCoordinates(city: str, limit=1):
    # Example API endpoint (OpenWeatherMap for London weather)
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": limit,
        "appid": weatherAPI
    }

    geoInfo = requests.get(url, params=params)
    if geoInfo.ok:
        lat = geoInfo.json()[0]['lat']
        lon = geoInfo.json()[0]['lon']
        return lat, lon
    else:
        print(geoInfo.text)
        return geoInfo.text

@track_api_call('Current Weather API')
def getToday(lat: float, lon: float):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": weatherAPI
    }

    weatherInfo = requests.get(url, params=params)

    print(weatherInfo.json())

lat, lon = getCoordinates('San Jose')
getToday(lat, lon)