# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\management\commands\fetch_weather.py

import requests
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from weather.models import Weather, Location

# Initialize logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch weather data from OpenWeatherMap API and update the database'

    def handle(self, *args, **kwargs):
        api_key = "2cc1564957a2987505aa7406dda64843"  # ⚡ Replace with your real API key
        locations = Location.objects.all()

        if not locations.exists():
            self.stdout.write(self.style.WARNING("No locations found. Please add locations first."))
            return

        for location in locations:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={location.name}&appid={api_key}&units=metric"
                response = requests.get(url)
                response.raise_for_status()  # Raises exception for non-200 status codes
                data = response.json()

                # Update latitude and longitude if changed
                latitude = data['coord']['lat']
                longitude = data['coord']['lon']

                if location.latitude != latitude or location.longitude != longitude:
                    location.latitude = latitude
                    location.longitude = longitude
                    location.save()
                    logger.info(f"Updated coordinates for {location.name}")

                # Check if weather data already exists for today
                today = timezone.localtime(timezone.now()).date()

                weather_obj, created = Weather.objects.update_or_create(
                    location=location,
                    date_recorded__date=today,
                    defaults={
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure'],
                        'description': data['weather'][0]['description'],
                        'date_recorded': timezone.localtime(timezone.now())
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created new weather record for {location.name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated existing weather record for {location.name}"))

            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error while fetching weather for {location.name}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"HTTP error for {location.name}: {str(e)}"))
            except KeyError as e:
                logger.error(f"Missing key in API response for {location.name}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Missing data for {location.name}: {str(e)}"))
            except Exception as e:
                logger.error(f"Unexpected error for {location.name}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Unexpected error for {location.name}: {str(e)}"))
