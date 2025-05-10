#Third Party
from dotenv import load_dotenv
import duckdb
import requests
#Local
from utils.decorators import track_api_call
from config.logger_config import logger
from utils.conversions import *
# Standard Library
from pprint import pformat
from datetime import datetime
import json
import os

load_dotenv()
weatherAPI = os.environ.get('weatherAPI')


@track_api_call('Geocoding API')
def getCoordinates(city: str, limit=1, country: str = None):
    # Example API endpoint
    url = "http://api.openweathermap.org/geo/1.0/direct"
    if not country:
        params = {
            "q": city,
            "limit": limit,
            "appid": weatherAPI
        }
        try:
            geoInfo = requests.get(url, params=params)
            if geoInfo.ok:
                logger.info(f"Response from Geocoding API: {geoInfo.json()}")
                # Extract latitude and longitude from the response
                lat = geoInfo.json()[0]['lat']
                lon = geoInfo.json()[0]['lon']
                logger.debug(f"Coordinates for {city}: ({lat}, {lon})")
                return lat, lon
            else:
                logger.error(f"Error fetching coordinates for {city}, {geoInfo.json()}: {geoInfo.status_code} - {geoInfo.text}")
                return None, None
        except Exception as e:
            logger.error(f"Exception occurred while fetching coordinates for {city}: {str(e)}")
            return None, None
    else:
        params = {
            "q": city + "," + country,
            "limit": limit,
            "appid": weatherAPI
        }
        try:
            geoInfo = requests.get(url, params=params)
            if geoInfo.ok:
                lat = geoInfo.json()[0]['lat']
                lon = geoInfo.json()[0]['lon']
                logger.debug(f"Coordinates for {city}, {country}: ({lat}, {lon})")
                return lat, lon
            else:
                logger.error(f"Error fetching coordinates for {city}: {geoInfo.status_code} - {geoInfo.text}")
                return None, None
        except Exception as e:
            logger.error(f"Exception occurred while fetching coordinates for {city}: {str(e)}")
            return None, None

@track_api_call('Current Weather API')
def getCurrentWeather(lat: float, lon: float):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": weatherAPI
    }

    try:
        return pformat(requests.get(url, params=params).json())
    except Exception as e:
        logger.error(f"Exception occurred while fetching current weather: {str(e)}")
        return None


def addCurrentWeatherToDB(currentWeather: str):
    weatherInfo = {}
    city = ""
    country = ""
    lat = 0
    lon = 0
    description = ""
    temp = 0
    temp_max = 0
    temp_min = 0
    humidity = 0
    pressure = 0
    sunrise = datetime(1970, 1, 1)
    sunset = datetime(1970, 1, 1)
    wind_speed = 0
    wind_deg = 0
    wind_gust = 0
    sea_level = 0
    
    weatherInfo = json.loads(currentWeather.replace("'", '"'))

    try:
        city = weatherInfo['name']
        country = weatherInfo['sys']['country']
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")

    try:
        lat = weatherInfo['coord']['lat']
        lon = weatherInfo['coord']['lon']
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")

    try:
        description = weatherInfo['weather'][0]['description']
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")
    
    try:
        temp = kelvinToFarenheit(weatherInfo['main']['temp'])
        temp_max = kelvinToFarenheit(weatherInfo['main']['temp_max'])
        temp_min = kelvinToFarenheit(weatherInfo['main']['temp_min'])
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")
    
    try:
        humidity = weatherInfo['main']['humidity']
        pressure = weatherInfo['main']['pressure']
        sunrise = datetime.fromtimestamp(weatherInfo['sys']['sunrise'])
        sunset = datetime.fromtimestamp(weatherInfo['sys']['sunset'])
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")

    try:
        wind_speed = weatherInfo['wind']['speed']
        wind_deg = weatherInfo['wind']['deg']
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")

    try:
        wind_gust = weatherInfo['wind']['gust']
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")

    try:
        sea_level = weatherInfo['main']['sea_level']
    except KeyError as e:
        logger.error(f"KeyError: {e} - {currentWeather}")

    con = duckdb.connect(database='Weather Tracker.db')
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS '{city}' (
            timestamp TIMESTAMP PRIMARY KEY,
            country TEXT,
            temperature REAL,
            temp_max REAL,
            temp_min REAL,
            humidity INTEGER,
            pressure INTEGER,
            description TEXT,
            latitude REAL,
            longitude REAL,
            sunrise TIMESTAMP,
            sunset TIMESTAMP,
            wind_speed REAL,
            sea_level INTEGER,
            wind_deg INTEGER,
            wind_gust REAL
        )
    """)
    con.execute(f"""
        INSERT INTO '{city}' (timestamp, country, temperature, temp_max, temp_min, humidity, pressure, description, latitude, longitude, sunrise, sunset, wind_speed, sea_level, wind_deg, wind_gust)
        VALUES (CURRENT_TIMESTAMP, '{country}', {temp}, {temp_max}, {temp_min}, {humidity}, {pressure}, '{description}', {lat}, {lon}, '{sunrise}', '{sunset}', {wind_speed}, {sea_level}, {wind_deg}, {wind_gust})
    """)
    con.close()
    