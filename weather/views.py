# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\views.py
from rest_framework.reverse import reverse

from django.http import JsonResponse
from .models import Location, Weather, Forecast, WeatherAlerts

# Weather report view
def weather_report(request, location_name):
    try:
        # Fetch the Location by name
        location = Location.objects.get(name=location_name)

        # Get the latest weather data for the location
        weather = Weather.objects.filter(location=location).latest('date_recorded')  # Get the latest weather

        # Structure the weather data to return as a JSON response
        weather_data = {
            'location': location.name,
            'temperature': weather.temperature,
            'humidity': weather.humidity,
            'pressure': weather.pressure,
            'description': weather.description,
            'date_recorded': weather.date_recorded.isoformat(),  # ISO format for date
        }

        # Return the weather data as a JSON response
        return JsonResponse(weather_data)
    
    except Location.DoesNotExist:
        # If location doesn't exist, return an error response
        return JsonResponse({'error': 'Location not found'}, status=404)
    
    except Weather.DoesNotExist:
        # If weather data doesn't exist for the location, return an error response
        return JsonResponse({'error': 'Weather data not found for this location'}, status=404)


# Weather forecast view
def weather_forecast(request, location_name):
    try:
        # Fetch the Location by name
        location = Location.objects.get(name=location_name)

        # Fetch all forecasts for the location ordered by date
        forecasts = Forecast.objects.filter(location=location).order_by('date')

        # Structure the forecast data into a list of dictionaries
        forecast_data = [
            {
                'date': forecast.date,
                'temperature_max': forecast.temperature_max,
                'temperature_min': forecast.temperature_min,
                'humidity': forecast.humidity,
                'description': forecast.description,
            }
            for forecast in forecasts
        ]

        # Return the forecast data as a JSON response
        return JsonResponse({'forecast': forecast_data})

    except Location.DoesNotExist:
        # If location doesn't exist, return an error response
        return JsonResponse({'error': 'Location not found'}, status=404)


# Weather alerts view
def weather_alerts(request, location_name):
    try:
        # Fetch the Location by name
        location = Location.objects.get(name=location_name)

        # Fetch all alerts for the location ordered by alert_time (latest first)
        alerts = WeatherAlerts.objects.filter(location=location).order_by('-alert_time')

        # Structure the alerts data into a list of dictionaries
        alerts_data = [
            {
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'description': alert.description,
                'alert_time': alert.alert_time.isoformat(),  # ISO format for date
            }
            for alert in alerts
        ]

        # Return the alerts data as a JSON response
        return JsonResponse({'alerts': alerts_data})

    except Location.DoesNotExist:
        # If location doesn't exist, return an error response
        return JsonResponse({'error': 'Location not found'}, status=404)

# in weather/views.py
from django.shortcuts import render
def home_page(request):
    return render(request, 'index.html')



def api_root(request):
    return JsonResponse({
        'weather_report': reverse('weather_report', args=['London'], request=request),
        'forecast': reverse('weather_forecast', args=['London'], request=request),
        'alerts': reverse('weather_alerts', args=['London'], request=request),
    })