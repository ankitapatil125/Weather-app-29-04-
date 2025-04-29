from django.apps import AppConfig

class WeatherConfig(AppConfig):
    name = 'weather'

    def ready(self):
        # Import and start the scheduler when the app is ready
        from .scheduler import start_scheduler
        start_scheduler()
