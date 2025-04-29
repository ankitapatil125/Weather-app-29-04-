# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\utils.py

import requests
from .models import Location, Weather
from django.utils import timezone
import logging

# Set up logging
logger = logging.getLogger(__name__)

API_KEY = 'your_openweathermap_api_key'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather_data():
    """Fetch weather data for all locations stored in the database."""
    # Fetch all locations from the database
    locations = Location.objects.all()
    
    for location in locations:
        try:
            fetch_weather(location.name)  # use location.name, not location object itself
            
            # Fetch the latest weather data
            weather = Weather.objects.filter(location=location).last()
            if weather:
                print(f"Weather Data for {location.name}:")
                print(f"Temperature: {weather.temperature} °C")
                print(f"Humidity: {weather.humidity} %")
                print(f"Pressure: {weather.pressure} hPa")
                print(f"Description: {weather.description}")
                print(f"Recorded At: {weather.date_recorded}")
            else:
                print(f"No weather data found for {location.name}")
            
            logger.info(f"Weather data fetched for {location.name} at {datetime.now()}")

        except Exception as e:
            logger.error(f"Error fetching weather data for {location.name}: {e}")
            print(f"Error fetching weather data for {location.name}: {e}")
