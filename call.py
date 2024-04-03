import csv
import requests
import psycopg2
from datetime import datetime


DATABASE = 'weather'
USERNAME = 'ridata'
PASSWORD = 'Temitope001*'

print("Connecting to the database")
try:
    connection = psycopg2.connect(host='localhost', database=DATABASE, user=USERNAME, password=PASSWORD)
except Exception:
    print("Could not connect to database. Please check credentials")
else:
    print("Connected to database")
cursor = connection.cursor()

def fetch_city_data(city_name, api_key):
    # OpenWeatherMap API endpoint for current weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    try:
        # Sending GET request to the API
        response = requests.get(url)
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing JSON response
            data = response.json()
            # Extracting relevant weather information
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            perceived_temp = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            return weather_description, temperature, perceived_temp, humidity, wind_speed
        else:
            print(f"Error: Failed to fetch weather data for {city_name}. Status code: {response.status_code}")
            return None, None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None, None

def append_weather_data_to_csv(input_csv, output_csv, api_key):
    try:
        # Open the input CSV file to read city names, latitude, and longitude
        with open(input_csv, "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            city_data = [row for row in reader]

        # Fetch weather data for each city and append to CSV
        with open(output_csv, "a", newline='', encoding='utf-8') as file:
            file.write("\n")
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['City', 'Latitude', 'Longitude', 'Weather Description', 'Temperature (°C)', 'Perceived Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)', 'Timestamp'])
            # Append data for each city
            for city_info in city_data:
                city_name, lat, lon = city_info
                weather_description, temperature, perceived_temp, humidity, wind_speed = fetch_city_data(city_name, api_key)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([city_name, lat, lon, weather_description, temperature, perceived_temp, humidity, wind_speed, timestamp])

        print(f"Data appended and saved in {output_csv}")
    except Exception as e:
        print(f"Error: {e}")

# Input CSV file containing city names, latitude, and longitude
input_csv = "nigerian_cities.csv"
# Output CSV file to save appended data
output_csv = "nigerian_cities_with_weather.csv"
# API key for OpenWeatherMap
api_key = "1a729a0ad116278f1b587d8cd1166e52"

# Append weather data to CSV file and save
append_weather_data_to_csv(input_csv, output_csv, api_key)
