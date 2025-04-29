# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\serializers.py

from rest_framework import serializers
from .models import Location, Weather, Forecast, WeatherInsights

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'country']  # Including id, name, and country

class WeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Serialize the location as an embedded object

    class Meta:
        model = Weather
        fields = ['id', 'location', 'temperature', 'humidity', 'pressure', 'description', 'date_recorded']

class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'

class WeatherInsightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherInsights
        fields = '__all__'
