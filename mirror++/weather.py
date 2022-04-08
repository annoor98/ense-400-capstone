"""Weather Script for obtaining forcast.
   Uses OpenWeatherMap API"""
import json
import requests

with open('devices.json', 'r') as file:
    api = json.load(file)

api_key = api['weatherKey']
lat = api['cityLat']
lon = api['cityLon']
url = "http://api.openweathermap.org/data/2.5/onecall?lat="\
      + lat + "&lon=" + lon + "&APPID="\
       + api_key + "&units=metric&exclude=current,minutely,daily,alerts"

request = requests.get(url)

response = request.json()


weather_result = response['hourly'][0]['weather'][0]['main']
temp_result = "Temperature: " + str(response['hourly'][0]['temp'])
feel_result = "Feels Like: " + str(response['hourly'][0]['feels_like'])
forecast_result = "Later today it will be: " + str(response['hourly'][5]['temp'])
