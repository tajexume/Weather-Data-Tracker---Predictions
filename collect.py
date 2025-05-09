#Third Party
from dotenv import load_dotenv
import requests
#Local
from utils.decorators import track_api_call
from config.logger_config import logger
# Standard Library
from pprint import pformat
import os

load_dotenv()
weatherAPI = os.environ.get('weatherAPI')


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
        logger.debug(f"Coordinates for {city}: ({lat}, {lon})")
        return lat, lon
    else:
        logger.error(f"Error fetching coordinates for {city}: {geoInfo.status_code} - {geoInfo.text}")
        return None, None

@track_api_call('Current Weather API')
def getToday(lat: float, lon: float):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": weatherAPI
    }

    weatherInfo = pformat(requests.get(url, params=params).json())

    return weatherInfo

lat, lon = getCoordinates('San Jose')
weatherToday = getToday(lat, lon)