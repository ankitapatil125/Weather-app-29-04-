# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\models.py


from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ['name', 'country']  # Ensures uniqueness of location based on name and country

    def __str__(self):
        return f"{self.name}, {self.country}"

class Weather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='weather')
    temperature = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    description = models.CharField(max_length=100)
    date_recorded = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for fast lookup

    def __str__(self):
        return f"Weather in {self.location.name} on {self.date_recorded}"

class Forecast(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='forecasts')
    date = models.DateField()
    temperature_max = models.FloatField()
    temperature_min = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=100)

    class Meta:
        unique_together = ['location', 'date']  # Prevents duplicate forecasts for the same location and date

    def __str__(self):
        return f"Forecast for {self.location.name} on {self.date}"

class WeatherInsights(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='insights')
    date = models.DateField()
    average_temperature = models.FloatField()
    highest_temperature = models.FloatField()
    lowest_temperature = models.FloatField()
    avg_humidity = models.FloatField()

    def __str__(self):
        return f"Insights for {self.location.name} on {self.date}"

class WeatherAlerts(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=100)  # E.g., "Heatwave", "Storm", "Flood"
    severity = models.CharField(max_length=50)  # E.g., "High", "Moderate", "Low"
    description = models.TextField()
    alert_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.location.name} - {self.alert_type} ({self.severity})"
