import requests, json
import time

class WeatherApi:

    api_key = "9d41bb0d410c976773d14920d063d5ab"
    baseUrl="https://api.openweathermap.org/data/2.5/weather?appid="+api_key+"&units=metric&q="
    @classmethod
    def getData(self,city):
        completeUrl = self.baseUrl+city
        response = requests.get(completeUrl)
        if response.status_code != 200:
            return -1
        response = response.json()
        city = response['name']
        temperature=response['main']['temp']
        humidity=response['main']['humidity']
        currentTime= time.strftime("%Y-%m-%d %H:%M:%S")
        lon=response['coord']['lon']
        lat=response['coord']['lat']
        return {"city":city,"temperature":temperature,"humidity":humidity,"currentTime":currentTime,"lon":lon,"lat":lat}
