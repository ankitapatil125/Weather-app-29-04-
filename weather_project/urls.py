# # C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather_project\urls.py
# from django.http import HttpResponse
# from django.urls import path, include

# def index(request):
#     return HttpResponse("Weather API is running. Use endpoints under /api/")

# urlpatterns = [
#     path('', index),  # Now visiting "/" won't throw 404
#     path('api/', include('weather.urls')),
# ]

# # C:\Users\AGT7.DESKTOP-GFAJ93V\my_weather_app\weather_project\urls.py
# weather_project/urls.py

from django.urls import path, include
from weather import views  # Import views from the weather app

urlpatterns = [
    path('', views.home_page),  # This will render the 'index.html' page at the root
    path('api/', include('weather.urls')),  # Include the 'weather' app's URLs
]
