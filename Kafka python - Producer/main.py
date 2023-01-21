from getApiData import WeatherApi
from kafkaProducer import Producer
import pandas as pd
import time

#cities = ['meknes','rabat','fes','casablanca','meknes','rabat','fes','casablanca','meknes','rabat','fes','casablanca','meknes','rabat','fes','casablanca','meknes','rabat','fes','casablanca']

#while 1:

# for city in cities:
#     data=WeatherApi.getData(city)
#     print(data)
#     Producer.sendData("weather",data)
#Producer.flushData()
print("preparing data")
cities_df = pd.read_excel('worldcities.xlsx', sheet_name=0)
cities_df = cities_df[cities_df['population'].notna()]
citiesFirst_3600_df = cities_df.head(n=3600) 
#cities_3600.query("country in ('Morocco')",inplace=True)
print('number of cities',citiesFirst_3600_df['city'].count())
cities=citiesFirst_3600_df['city'].to_list()
#print(cities)
while 1:
    limit=60
    for city in cities:
        data=WeatherApi.getData(city)
        if data == -1:
            continue
        print(data)
        Producer.sendData("weather",data)
        limit=limit-1
        if limit == 0:
            limit = 60
            time.sleep(60) #delay 1 minute because we reach the 60 api's call limit