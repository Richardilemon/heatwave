import csv
import requests
from datetime import datetime, timedelta

def fetch_historical_weather_data(city_name, start_date, end_date, api_key):
    # OpenWeatherMap API endpoint for historical weather data
    url = f"https://history.openweathermap.org/data/2.5/history/city?q={city_name}&start={start_date}&end={end_date}&appid={api_key}&units=metric"
    
    try:
        # Sending GET request to the API
        response = requests.get(url)
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing JSON response
            data = response.json()
            # Extracting relevant weather information
            # Depending on the response structure, extract the necessary data
            # For example:
            weather_data = data['list']  # Assuming the data is in a 'list' field
            # Process weather_data further as needed
            return weather_data
        else:
            print(f"Error: Failed to fetch historical weather data for {city_name}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def collect_historical_weather_data(input_csv, output_csv, api_key):
    try:
        # Open the input CSV file to read city names, latitude, and longitude
        with open(input_csv, "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            city_data = [row for row in reader]

        # Collect historical weather data for each city
        with open(output_csv, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['City', 'Date', 'Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)', 'Weather Description'])
            # Collect data for each city
            for city_info in city_data:
                city_name, lat, lon = city_info
                # Assuming you want data for the past week
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                historical_data = fetch_historical_weather_data(city_name, start_date, end_date, api_key)
                if historical_data:
                    for data_point in historical_data:
                        date = data_point['dt_txt']  # Assuming the date is in a 'dt_txt' field
                        temperature = data_point['main']['temp']
                        humidity = data_point['main']['humidity']
                        wind_speed = data_point['wind']['speed']
                        weather_description = data_point['weather'][0]['description']
                        writer.writerow([city_name, date, temperature, humidity, wind_speed, weather_description])

        print(f"Historical weather data collected and saved in {output_csv}")
    except Exception as e:
        print(f"Error: {e}")

# Input CSV file containing city names, latitude, and longitude
input_csv = "nigerian_cities.csv"
# Output CSV file to save historical weather data
output_csv = "historical_weather_data.csv"
# API key for OpenWeatherMap
api_key = "1a729a0ad116278f1b587d8cd1166e52"

# Collect historical weather data and save to CSV file
collect_historical_weather_data(input_csv, output_csv, api_key)
