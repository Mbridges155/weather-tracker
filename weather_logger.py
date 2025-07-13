import requests
import csv
import os
import time
import schedule
from datetime import datetime

# === CONFIG ===
API_KEY = "d87a7bfd5b2049f38c69103cfa4f2f69"
CITIES = ['Tokyo', 'Denver', 'Atlanta']
FILENAME = r"C:\Users\macke\OneDrive\Desktop\Weather_Scripts\weather_data.csv"

# === EXTRACT ===
def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'imperial'
    }
    response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)
    data = response.json()
    return data

# ===TRANSFORM ===
def transform_weather(data):
    city = data['name']
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    weather_desc = data['weather'][0]['description']
    wind_speed = data['wind']['speed']
    timestamp = datetime.now().isoformat()

    return {
        'city': city,
        'temperature': temp,
        'humidity': humidity,
        'description': weather_desc,
        'wind_speed': wind_speed,
        'timestamp': timestamp
    }

# === LOAD ===
def save_to_csv(data, filename=FILENAME):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'city', 'temperature', 'humidity', 'description', 'wind_speed', 'timestamp'
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# === JOB ===
def job():
    for city in CITIES:
        try:
            raw_data = get_weather(city)
            transformed = transform_weather(raw_data)
            save_to_csv(transformed)
            print(f"[{transformed['timestamp']}] Logged weather for {transformed['city']}")
        except Exception as e:
            print(f"Error during job: {e}")

# === SCHEDULER LOOP ===

schedule.every(30).minutes.do(job)

print(f"Logging weather for {', '.join(CITIES)} every thirty minutes. Press CTRL+C to stop.\n")

while True:
    schedule.run_pending()
    time.sleep(1)