import requests
import json
import datetime

with open('devices.json', 'r') as file:
    api = json.load(file)

api_key = api['weatherKey']
city = api['cityId']
url = "http://api.openweathermap.org/data/2.5/weather?id=" + city + "&APPID=" + api_key + "&units=metric"
url2 = "http://api.openweathermap.org/data/2.5/onecall?lat=50.4501&lon=-104.6178&APPID="\
       + api_key + "&units=metric&exclude=current,minutely,daily,alerts"

request = requests.get(url2)

response = request.json()


weather_result = response['hourly'][0]['weather'][0]['main']
temp_result = "Temperature: " + str(response['hourly'][0]['temp'])
feel_result = "Feels Like: " + str(response['hourly'][0]['feels_like'])
forecast_result = "Later today it will be: " + str(response['hourly'][5]['temp'])

