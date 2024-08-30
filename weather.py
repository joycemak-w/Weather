import requests
import pandas as pd
import schedule
import time
import csv
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 
API_KEY = os.getenv('API_KEY')

other_city_1 = 'Mongolia'
other_city_2 = 'Antarctica'
other_city_3 = 'Mexicali'
other_city_4 = 'TaiWan'
your_city = 'Hong Kong'
id = {2029969,6255152,3996069,1668284,1819729}
# API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={your_city}&appid={API_KEY}&units=metric'
API_URL = f'http://api.openweathermap.org/data/2.5/group?id=2029969,6255152,3996069,1668284,1819729&appid={API_KEY}&units=metric'

# Task 1. define a database and table
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()
 
#   create table
def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Weathers (
        id INTEGER PRIMARY KEY,
        timestamp timestamp NOT NULL,
        location TEXT NOT NULL,
        temperature REAL NOT NULL,
        humidity TEXT NOT NULL,
        visibility INTERGER NOT NULL,
        weather TEXT NOT NULL
    )
    ''')

def fetch_weather_data():
    response = requests.get(API_URL.format(API_KEY))
    if response.status_code == 200:
        data = response.json()
        # weather_data = {1
        #     'timestamp': datetime.now(),
        #     'temperature': data['main']['temp'],
        #     'humidity': data['main']['humidity'],
        #     'weather': data['weather'][0]['description'],
        # }        
        for weather_data in data['list']:
            print(weather_data)
            conn = sqlite3.connect('weather.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Weathers (timestamp, location, temperature, humidity, visibility, weather) VALUES (?, ?, ?, ?, ?, ?)', (datetime.now(),weather_data['name'], weather_data['main']['temp'], weather_data['main']['humidity'], weather_data['visibility'], weather_data['weather'][0]['description']))
            conn.commit()
            conn.close()

        # Task 2 . add weather data into database


# Task 3. write functions to perform analysis - generate analysis based on weather data

# Task 4. Create interface to interact with data or get reports, use tkinter or terminal but remember to make it data centric and user frinedly

# Bonus Task 5. compare cities

def main():
    create_table()
    interval = input("Enter the interval in minutes (default is 1): ")
    interval = int(interval) if interval.isdigit() else 1

    schedule.every(interval).minutes.do(fetch_weather_data)
    
    print(f"Scheduler started. Fetching weather data every {interval} minute(s).")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()


# # 2315 per min
# {'coord': {'lon': 105, 'lat': 46}, 'sys': {'country': 'MN', 'timezone': 28800, 'sunrise': 1724624004, 'sunset': 1724673039}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 22.06, 'feels_like': 21.57, 'temp_min': 22.06, 'temp_max': 22.06, 'pressure': 1011, 'sea_level': 1011, 'grnd_level': 863, 'humidity': 48}, 'visibility': 10000, 'wind': {'speed': 2.38, 'deg': 221}, 'clouds': {'all': 100}, 'dt': 1724685055, 'id': 2029969, 'name': 'Mongolia'}
# {'coord': {'lon': 16.4063, 'lat': -78.1586}, 'sys': {'country': '', 'timezone': 7200, 'sunrise': 1724660773, 'sunset': 1724678786}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': -42.62, 'feels_like': -49.62, 'temp_min': -42.62, 'temp_max': -42.62, 'pressure': 1021, 'sea_level': 1021, 'grnd_level': 650, 'humidity': 62}, 'visibility': 10000, 'wind': {'speed': 6.87, 'deg': 23}, 'clouds': {'all': 85}, 'dt': 1724682243, 'id': 6255152, 'name': 'Antarctica'}
# {'coord': {'lon': -115.4683, 'lat': 32.6519}, 'sys': {'country': 'MX', 'timezone': -25200, 'sunrise': 1724678000, 'sunset': 1724724847}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'main': {'temp': 28.38, 'feels_like': 27.43, 'temp_min': 25.92, 'temp_max': 28.38, 'pressure': 1014, 'sea_level': 1014, 'grnd_level': 1014, 'humidity': 31}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 342}, 'clouds': {'all': 0}, 'dt': 1724682094, 'id': 3996069, 'name': 'Mexicali'}
# {'coord': {'lon': 121, 'lat': 24}, 'sys': {'country': 'TW', 'timezone': 28800, 'sunrise': 1724621737, 'sunset': 1724667628}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 21.36, 'feels_like': 21.98, 'temp_min': 21.36, 'temp_max': 21.36, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 891, 'humidity': 93}, 'visibility': 10000, 'wind': {'speed': 1.72, 'deg': 93}, 'clouds': {'all': 99}, 'dt': 1724684748, 'id': 1668284, 'name': 'Taiwan'}
# {'coord': {'lon': 114.1577, 'lat': 22.2855}, 'sys': {'country': 'HK', 'timezone': 28800, 'sunrise': 1724623472, 'sunset': 1724669176}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'main': {'temp': 30.32, 'feels_like': 37.32, 'temp_min': 29.13, 'temp_max': 30.77, 'pressure': 1007, 'sea_level': 1007, 'grnd_level': 1007, 'humidity': 80}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 270}, 'clouds': {'all': 43}, 'dt': 1724684963, 'id': 1819729, 'name': 'Hong Kong'}
# {'coord': {'lon': 105, 'lat': 46}, 'sys': {'country': 'MN', 'timezone': 28800, 'sunrise': 1724624004, 'sunset': 1724673039}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 22.06, 'feels_like': 21.57, 'temp_min': 22.06, 'temp_max': 22.06, 'pressure': 1011, 'sea_level': 1011, 'grnd_level': 863, 'humidity': 48}, 'visibility': 10000, 'wind': {'speed': 2.38, 'deg': 221}, 'clouds': {'all': 100}, 'dt': 1724685055, 'id': 2029969, 'name': 'Mongolia'}
# {'coord': {'lon': 16.4063, 'lat': -78.1586}, 'sys': {'country': '', 'timezone': 7200, 'sunrise': 1724660773, 'sunset': 1724678786}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': -42.62, 'feels_like': -49.62, 'temp_min': -42.62, 'temp_max': -42.62, 'pressure': 1021, 'sea_level': 1021, 'grnd_level': 650, 'humidity': 62}, 'visibility': 10000, 'wind': {'speed': 6.87, 'deg': 23}, 'clouds': {'all': 85}, 'dt': 1724682243, 'id': 6255152, 'name': 'Antarctica'}
# {'coord': {'lon': -115.4683, 'lat': 32.6519}, 'sys': {'country': 'MX', 'timezone': -25200, 'sunrise': 1724678000, 'sunset': 1724724847}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'main': {'temp': 28.38, 'feels_like': 27.43, 'temp_min': 25.92, 'temp_max': 28.38, 'pressure': 1014, 'sea_level': 1014, 'grnd_level': 1014, 'humidity': 31}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 342}, 'clouds': {'all': 0}, 'dt': 1724682094, 'id': 3996069, 'name': 'Mexicali'}
# {'coord': {'lon': 121, 'lat': 24}, 'sys': {'country': 'TW', 'timezone': 28800, 'sunrise': 1724621737, 'sunset': 1724667628}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 21.36, 'feels_like': 21.98, 'temp_min': 21.36, 'temp_max': 21.36, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 891, 'humidity': 93}, 'visibility': 10000, 'wind': {'speed': 1.72, 'deg': 93}, 'clouds': {'all': 99}, 'dt': 1724684748, 'id': 1668284, 'name': 'Taiwan'}
# {'coord': {'lon': 114.1577, 'lat': 22.2855}, 'sys': {'country': 'HK', 'timezone': 28800, 'sunrise': 1724623472, 'sunset': 1724669176}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'main': {'temp': 30.32, 'feels_like': 37.32, 'temp_min': 29.13, 'temp_max': 30.77, 'pressure': 1007, 'sea_level': 1007, 'grnd_level': 1007, 'humidity': 80}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 270}, 'clouds': {'all': 43}, 'dt': 1724684963, 'id': 1819729, 'name': 'Hong Kong'}
# {'coord': {'lon': 105, 'lat': 46}, 'sys': {'country': 'MN', 'timezone': 28800, 'sunrise': 1724624004, 'sunset': 1724673039}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 22.06, 'feels_like': 21.57, 'temp_min': 22.06, 'temp_max': 22.06, 'pressure': 1011, 'sea_level': 1011, 'grnd_level': 863, 'humidity': 48}, 'visibility': 10000, 'wind': {'speed': 2.38, 'deg': 221}, 'clouds': {'all': 100}, 'dt': 1724685055, 'id': 2029969, 'name': 'Mongolia'}
# {'coord': {'lon': 16.4063, 'lat': -78.1586}, 'sys': {'country': '', 'timezone': 7200, 'sunrise': 1724660773, 'sunset': 1724678786}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': -42.62, 'feels_like': -49.62, 'temp_min': -42.62, 'temp_max': -42.62, 'pressure': 1021, 'sea_level': 1021, 'grnd_level': 650, 'humidity': 62}, 'visibility': 10000, 'wind': {'speed': 6.87, 'deg': 23}, 'clouds': {'all': 85}, 'dt': 1724682243, 'id': 6255152, 'name': 'Antarctica'}
# {'coord': {'lon': -115.4683, 'lat': 32.6519}, 'sys': {'country': 'MX', 'timezone': -25200, 'sunrise': 1724678000, 'sunset': 1724724847}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'main': {'temp': 28.38, 'feels_like': 27.43, 'temp_min': 25.92, 'temp_max': 28.38, 'pressure': 1014, 'sea_level': 1014, 'grnd_level': 1014, 'humidity': 31}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 342}, 'clouds': {'all': 0}, 'dt': 1724682094, 'id': 3996069, 'name': 'Mexicali'}
# {'coord': {'lon': 121, 'lat': 24}, 'sys': {'country': 'TW', 'timezone': 28800, 'sunrise': 1724621737, 'sunset': 1724667628}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 21.36, 'feels_like': 21.98, 'temp_min': 21.36, 'temp_max': 21.36, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 891, 'humidity': 93}, 'visibility': 10000, 'wind': {'speed': 1.72, 'deg': 93}, 'clouds': {'all': 99}, 'dt': 1724684748, 'id': 1668284, 'name': 'Taiwan'}
# {'coord': {'lon': 114.1577, 'lat': 22.2855}, 'sys': {'country': 'HK', 'timezone': 28800, 'sunrise': 1724623472, 'sunset': 1724669176}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'main': {'temp': 30.32, 'feels_like': 37.32, 'temp_min': 29.13, 'temp_max': 30.77, 'pressure': 1007, 'sea_level': 1007, 'grnd_level': 1007, 'humidity': 80}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 270}, 'clouds': {'all': 43}, 'dt': 1724684963, 'id': 1819729, 'name': 'Hong Kong'}
# {'coord': {'lon': 105, 'lat': 46}, 'sys': {'country': 'MN', 'timezone': 28800, 'sunrise': 1724624004, 'sunset': 1724673039}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 22.06, 'feels_like': 21.57, 'temp_min': 22.06, 'temp_max': 22.06, 'pressure': 1011, 'sea_level': 1011, 'grnd_level': 863, 'humidity': 48}, 'visibility': 10000, 'wind': {'speed': 2.38, 'deg': 221}, 'clouds': {'all': 100}, 'dt': 1724685055, 'id': 2029969, 'name': 'Mongolia'}
# {'coord': {'lon': 16.4063, 'lat': -78.1586}, 'sys': {'country': '', 'timezone': 7200, 'sunrise': 1724660773, 'sunset': 1724678786}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': -42.62, 'feels_like': -49.62, 'temp_min': -42.62, 'temp_max': -42.62, 'pressure': 1021, 'sea_level': 1021, 'grnd_level': 650, 'humidity': 62}, 'visibility': 10000, 'wind': {'speed': 6.87, 'deg': 23}, 'clouds': {'all': 85}, 'dt': 1724682243, 'id': 6255152, 'name': 'Antarctica'}
# {'coord': {'lon': -115.4683, 'lat': 32.6519}, 'sys': {'country': 'MX', 'timezone': -25200, 'sunrise': 1724678000, 'sunset': 1724724847}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'main': {'temp': 28.38, 'feels_like': 27.43, 'temp_min': 25.92, 'temp_max': 28.38, 'pressure': 1014, 'sea_level': 1014, 'grnd_level': 1014, 'humidity': 31}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 342}, 'clouds': {'all': 0}, 'dt': 1724682094, 'id': 3996069, 'name': 'Mexicali'}
# {'coord': {'lon': 121, 'lat': 24}, 'sys': {'country': 'TW', 'timezone': 28800, 'sunrise': 1724621737, 'sunset': 1724667628}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 21.36, 'feels_like': 21.98, 'temp_min': 21.36, 'temp_max': 21.36, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 891, 'humidity': 93}, 'visibility': 10000, 'wind': {'speed': 1.72, 'deg': 93}, 'clouds': {'all': 99}, 'dt': 1724684748, 'id': 1668284, 'name': 'Taiwan'}
# {'coord': {'lon': 114.1577, 'lat': 22.2855}, 'sys': {'country': 'HK', 'timezone': 28800, 'sunrise': 1724623472, 'sunset': 1724669176}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'main': {'temp': 30.32, 'feels_like': 37.32, 'temp_min': 29.13, 'temp_max': 30.77, 'pressure': 1007, 'sea_level': 1007, 'grnd_level': 1007, 'humidity': 80}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 270}, 'clouds': {'all': 43}, 'dt': 1724684963, 'id': 1819729, 'name': 'Hong Kong'}
# {'coord': {'lon': 105, 'lat': 46}, 'sys': {'country': 'MN', 'timezone': 28800, 'sunrise': 1724624004, 'sunset': 1724673039}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 22.06, 'feels_like': 21.57, 'temp_min': 22.06, 'temp_max': 22.06, 'pressure': 1011, 'sea_level': 1011, 'grnd_level': 863, 'humidity': 48}, 'visibility': 10000, 'wind': {'speed': 2.38, 'deg': 221}, 'clouds': {'all': 100}, 'dt': 1724685055, 'id': 2029969, 'name': 'Mongolia'}
# {'coord': {'lon': 16.4063, 'lat': -78.1586}, 'sys': {'country': '', 'timezone': 7200, 'sunrise': 1724660773, 'sunset': 1724678786}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': -42.62, 'feels_like': -49.62, 'temp_min': -42.62, 'temp_max': -42.62, 'pressure': 1021, 'sea_level': 1021, 'grnd_level': 650, 'humidity': 62}, 'visibility': 10000, 'wind': {'speed': 6.87, 'deg': 23}, 'clouds': {'all': 85}, 'dt': 1724682243, 'id': 6255152, 'name': 'Antarctica'}
# {'coord': {'lon': -115.4683, 'lat': 32.6519}, 'sys': {'country': 'MX', 'timezone': -25200, 'sunrise': 1724678000, 'sunset': 1724724847}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'main': {'temp': 28.38, 'feels_like': 27.43, 'temp_min': 25.92, 'temp_max': 28.38, 'pressure': 1014, 'sea_level': 1014, 'grnd_level': 1014, 'humidity': 31}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 342}, 'clouds': {'all': 0}, 'dt': 1724682094, 'id': 3996069, 'name': 'Mexicali'}
# {'coord': {'lon': 121, 'lat': 24}, 'sys': {'country': 'TW', 'timezone': 28800, 'sunrise': 1724621737, 'sunset': 1724667628}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'main': {'temp': 21.36, 'feels_like': 21.98, 'temp_min': 21.36, 'temp_max': 21.36, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 891, 'humidity': 93}, 'visibility': 10000, 'wind': {'speed': 1.72, 'deg': 93}, 'clouds': {'all': 99}, 'dt': 1724684748, 'id': 1668284, 'name': 'Taiwan'}
# {'coord': {'lon': 114.1577, 'lat': 22.2855}, 'sys': {'country': 'HK', 'timezone': 28800, 'sunrise': 1724623472, 'sunset': 1724669176}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'main': {'temp': 30.32, 'feels_like': 37.32, 'temp_min': 29.13, 'temp_max': 30.77, 'pressure': 1007, 'sea_level': 1007, 'grnd_level': 1007, 'humidity': 80}, 'visibility': 10000, 'wind': {'speed': 1.34, 'deg': 270}, 'clouds': {'all': 43}, 'dt': 1724684963, 'id': 1819729, 'name': 'Hong Kong'}