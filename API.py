# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 22:08:43 2022

@author: xyyan
"""
import json
import requests
from datetime import datetime

class OpenWeather:
    """ documentation =  """
    endpoint_template = '/' + \
                        ''
    api_key = ''

    def __init__(self):
        self.endpoint = OpenWeather.endpoint_template.replace('{API key}', OpenWeather.api_key)

    def execute(self, city, mode='json', units='imperial'):
        endpoint = self.endpoint.replace('{city name}', city)
        endpoint = endpoint.replace('{mode}', mode)
        endpoint = endpoint.replace('{units}', units)

        r = requests.get(endpoint)
        if mode == 'json':
            r_as_json = json.loads(r.text)
            # print(json.dumps(r_as_json, indent=2))
            
            ts = r_as_json.get('dt', None)
            dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') if ts else None

            temp = r_as_json['main'].get('temp', None)
            feels_like = r_as_json['main'].get('feels_like', None)
            temp_min = r_as_json['main'].get('temp_min', None)
            temp_max = r_as_json['main'].get('temp_max', None)
            # pressure = r_as_json['main'].get('pressure', None)
            humidity = r_as_json['main'].get('humidity', None)
            temperature = (temp, feels_like, temp_min, temp_max, humidity)
            
            speed = r_as_json['wind'].get('speed', None)
            deg = r_as_json['wind'].get('deg', None)
            gust = r_as_json['wind'].get('gust', None)
            wind = (speed, deg, gust)
            
            longitude = r_as_json['coord'].get('lon', None)
            latitude = r_as_json['coord'].get('lat', None)
            location = (longitude, latitude)

            return dt, temperature, wind, location

f = open('city.list.json', 'r', encoding='UTF-8')
cities = json.load(f)

def main():
    open_weather = OpenWeather()
    for i in range(len(cities)):
        city = cities[i]['name']
        dt, temperature, wind, location = open_weather.execute(city)
        print(f'{city}: dt={dt}, T={temperature}; W={wind} ; L={location}')
    
main()

