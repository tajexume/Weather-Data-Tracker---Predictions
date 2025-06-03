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
from datetime import date
import json
import os

load_dotenv()
weatherAPI = os.environ.get('weatherAPI')


@track_api_call('Geocoding API')
def getCoordinates(city: str, limit=1, country: str = '') -> tuple:
    # Function to get coordinates of a city using OpenWeatherMap's Geocoding API
    """
    Get the latitude and longitude of a city using OpenWeatherMap's Geocoding API.
    If the country is not provided, it will search for the city globally.
    If the country is provided, it will search for the city within that country.
    :param city: Name of the city to search for.
    :param limit: Maximum number of results to return (default is 1).
    :param country: Country code (optional).            
    """

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
                country = geoInfo.json()[0]['country']
                logger.debug(f"Coordinates for {city}, {country}: ({lat}, {lon})")
                return lat, lon
            else:
                logger.error(f"Error fetching coordinates for {city}, {geoInfo.json()}: {geoInfo.status_code} - {geoInfo.text}")
                return None, None
        except Exception as e:
            logger.error(f"Exception occurred while fetching coordinates for {city}, {country}: {str(e)}")
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
        CREATE TABLE IF NOT EXISTS "{city}" (
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
    

def checkForNewCity(city: str, country:str, lat: float, lon: float):
    con = duckdb.connect(database='Weather Tracker.db')

    con.execute(f"""
    CREATE TABLE IF NOT EXISTS {country} (
        city TEXT UNIQUE,
        latitude REAL,
        longitude REAL
    )
""")

    # Check if the city already exists in the country table
    city_exists = con.execute(f"SELECT * FROM {country} WHERE city = ?", [city]).fetchall()

    if not city_exists:
        # Add the city with coordinates to the country table
        con.execute(
    f"""
    INSERT INTO '{country}' (city, latitude, longitude)
    VALUES (?, ?, ?)
    """,
    [city, lat, lon]
)
        logger.info(f"City {city} added to the {country} table.")
    try:
        result = con.execute(f"SELECT * FROM '{city}' LIMIT 1").fetchall()
        if result:
            logger.info(f"City {city} already exists in the database.")
            return True
        else:
            logger.info(f"City {city} does not exist in the database.")
            return False
    except Exception as e:
        logger.error(f"Exception occurred while checking for city {city}: {str(e)}")
        return False
    finally:
        con.close()


def getCoordinatesFromDB(country: str, city: str) -> tuple:
    try:
        con = duckdb.connect(database='Weather Tracker.db')
        query = f"SELECT latitude, longitude FROM {country} WHERE city = ?"
        result = con.execute(query, (city,)).fetchone()
        con.close()

        if result:
            return result[0], result[1]
        else:
            logger.error(f"City {city} not found in the {country} table.")
            return None, None
    except Exception as e:
        logger.error(f"Exception occurred while retrieving coordinates for {city} in {country}: {str(e)}")
        return None, None


@track_api_call('Weather API')
def weatherForDate(city: str = '', lon: float = 0.0, lat: float = 0.0, weatherDate: date = date.today()):
    url = 'https://api.openweathermap.org/data/3.0/onecall/day_summary'
    if city:
        lat, lon = getCoordinates(city) # type: ignore
        if lat is None or lon is None:
            logger.error(f"Could not retrieve coordinates for {city}.")
            return None
    elif not city and (lat == 0.0 or lon == 0.0):
        logger.error("No city or coordinates provided.")
        return None
    params = {
        'lat': lat,
        'lon': lon,
        'date': weatherDate.strftime('%Y-%m-%d'),
        'appid': weatherAPI
    }

    try:
        response = requests.get(url, params=params)
        if response.ok:
            weather_data = response.json()
            logger.info(f"Weather data for {city} on {weatherDate}: {weather_data}")
            return weather_data
        else:
            logger.error(f"Error fetching weather data for {city} on {weatherDate}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception occurred while fetching weather data for {city} on {weatherDate}: {str(e)}")
        return None