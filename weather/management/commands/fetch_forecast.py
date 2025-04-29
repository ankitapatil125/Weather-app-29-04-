# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\management\commands\fetch_forecast.py

import requests
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from weather.models import Forecast, Location

# Initialize logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch 5-day weather forecast from OpenWeatherMap API and update the database'

    def handle(self, *args, **kwargs):
        api_key = "2cc1564957a2987505aa7406dda64843"  # Replace with your real API key
        locations = Location.objects.all()

        if not locations.exists():
            self.stdout.write(self.style.WARNING("No locations found. Please add locations first."))
            return

        for location in locations:
            try:
                url = f"http://api.openweathermap.org/data/2.5/forecast?q={location.name}&appid={api_key}&units=metric"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                forecast_list = data.get('list', [])
                if not forecast_list:
                    self.stdout.write(self.style.WARNING(f"No forecast data available for {location.name}"))
                    continue

                # Process and save forecast for each day (we only want one record per day)
                daily_forecasts = {}

                for forecast in forecast_list:
                    forecast_time = timezone.make_aware(timezone.datetime.fromtimestamp(forecast['dt']))
                    date = forecast_time.date()

                    if date not in daily_forecasts:
                        daily_forecasts[date] = {
                            'temp_min': forecast['main']['temp_min'],
                            'temp_max': forecast['main']['temp_max'],
                            'humidity': forecast['main']['humidity'],
                            'description': forecast['weather'][0]['description']
                        }
                    else:
                        # Update min and max temps
                        daily_forecasts[date]['temp_min'] = min(daily_forecasts[date]['temp_min'], forecast['main']['temp_min'])
                        daily_forecasts[date]['temp_max'] = max(daily_forecasts[date]['temp_max'], forecast['main']['temp_max'])

                for date, values in daily_forecasts.items():
                    if date >= timezone.localtime(timezone.now()).date():
                        forecast_obj, created = Forecast.objects.update_or_create(
                            location=location,
                            date=date,
                            defaults={
                                'temperature_min': values['temp_min'],
                                'temperature_max': values['temp_max'],
                                'humidity': values['humidity'],
                                'description': values['description'],
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Created forecast for {location.name} on {date}"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Updated forecast for {location.name} on {date}"))

            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error while fetching forecast for {location.name}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"HTTP error for {location.name}: {str(e)}"))
            except KeyError as e:
                logger.error(f"Missing key in API response for {location.name}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Missing data for {location.name}: {str(e)}"))
            except Exception as e:
                logger.error(f"Unexpected error for {location.name}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Unexpected error for {location.name}: {str(e)}"))
