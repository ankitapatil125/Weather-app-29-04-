# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\scheduler.py



import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import logging
from django.utils.timezone import make_aware
from weather.models import Location, Weather  # Ensure models are imported

# Initialize logger
logger = logging.getLogger(__name__)

def fetch_weather_data():
    """
    Fetch weather data from OpenWeatherMap API for each location
    in the Location model and update or create weather data in the database.
    """
    locations = Location.objects.all()  # Fetch all locations from the database

    for location in locations:
        try:
            # Define API URL with the required parameters
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location.name}&appid=your_api_key&units=metric"
            response = requests.get(url)
            data = response.json()

            # Check if the response status is OK (200)
            if response.status_code == 200:
                # Extract relevant data from the response
                latitude = data['coord']['lat']
                longitude = data['coord']['lon']
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                pressure = data['main']['pressure']
                description = data['weather'][0]['description']

                # Update or create weather data for today
                date_today = make_aware(datetime.now()).date()  # Ensure date is timezone-aware
                weather_data = Weather.objects.filter(location=location, date_recorded__date=date_today).first()

                if weather_data:
                    # If weather data exists for today, update it
                    weather_data.temperature = temperature
                    weather_data.humidity = humidity
                    weather_data.pressure = pressure
                    weather_data.description = description
                    weather_data.save()
                    logger.info(f"Updated weather data for {location.name}")
                else:
                    # If no weather data for today, create a new record
                    weather_data = Weather(
                        location=location,
                        temperature=temperature,
                        humidity=humidity,
                        pressure=pressure,
                        description=description,
                        date_recorded=make_aware(datetime.now())  # Timezone-aware datetime
                    )
                    weather_data.save()
                    logger.info(f"Created new weather data for {location.name}")
            else:
                logger.error(f"Failed to fetch weather data for {location.name}: {data.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"Error fetching weather data for {location.name}: {str(e)}")

def start_scheduler():
    """
    Start the APScheduler to fetch weather data every 30 minutes.
    """
    scheduler = BackgroundScheduler()
    print("Starting the scheduler...")  # Log when the scheduler starts

    # Schedule the `fetch_weather_data` function to run every 30 minutes
    scheduler.add_job(fetch_weather_data, 'interval', minutes=30, next_run_time=make_aware(datetime.now()))

    # Add listener to monitor job execution and handle success or failure
    def job_listener(event):
        if event.exception:
            logger.error(f"Job {event.job_id} failed")
        else:
            logger.info(f"Job {event.job_id} executed successfully")

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

# Start the scheduler when this script is executed
if __name__ == "__main__":
    start_scheduler()
