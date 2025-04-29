# C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),  # <-- add this line
    path('weather_report/<str:location_name>/', views.weather_report, name='weather_report'),
    path('forecast/<str:location_name>/', views.weather_forecast, name='weather_forecast'),
    path('alerts/<str:location_name>/', views.weather_alerts, name='weather_alerts'),
]
