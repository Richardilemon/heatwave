import csv
import requests
import psycopg2
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
API_KEY = os.getenv('API_KEY')
INPUT_CSV = os.getenv('INPUT_CSV')

def get_postgres_container_ip():
    try:
        result = subprocess.run(["docker", "inspect", "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", "weather-postgres-1"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def connect_to_database():
    try:
        postgres_ip = get_postgres_container_ip()
        if postgres_ip:
            connection = psycopg2.connect(host=postgres_ip, port='5432', database=DATABASE, user=USERNAME, password=PASSWORD)
            print("Connected to database")
            return connection
        else:
            print("Error: Failed to retrieve PostgreSQL container IP address")
            return None
    except Exception as e:
        print(f"Error: Could not connect to database. {e}")
        return None

def create_nigerian_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Nigerian (
                id SERIAL PRIMARY KEY,
                city_name VARCHAR(255),
                latitude DECIMAL(9, 6),
                longitude DECIMAL(9, 6),
                weather_description VARCHAR(255),
                temperature DECIMAL,
                perceived_temperature DECIMAL,
                humidity INTEGER,
                wind_speed DECIMAL,
                timestamp TIMESTAMP
            )
        """)
        print("Table 'Nigerian' created successfully")
    except Exception as e:
        print(f"Error: Could not create table. {e}")

def fetch_city_data(city_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
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

def load_weather_data_to_database(connection, input_csv, api_key):
    cursor = connection.cursor()
    try:
        create_nigerian_table(cursor)  # Create table if not exists
        with open(input_csv, "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for city_info in reader:
                city_name, lat, lon = city_info
                weather_description, temperature, perceived_temp, humidity, wind_speed = fetch_city_data(city_name, api_key)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO Nigerian (city_name, latitude, longitude, weather_description, temperature, perceived_temperature, humidity, wind_speed, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (city_name, lat, lon, weather_description, temperature, perceived_temp, humidity, wind_speed, timestamp))
        connection.commit()
        print("Data loaded into the database")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

connection = connect_to_database()
if connection:
    load_weather_data_to_database(connection, INPUT_CSV, API_KEY)
    connection.close()
