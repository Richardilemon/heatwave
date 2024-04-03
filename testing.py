import requests
import csv



def fetch_weather_data(api_key, cities):
    # OpenWeatherMap API endpoint for current weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={{city}}&appid={api_key}&units=metric"
    
    count = 0
    try:
        for city in cities:
            # Sending GET request to the API for each city
            response = requests.get(url.format(city=city))
            # Checking if the request was successful (status code 200)
            if response.status_code == 200:
                count += 1
                # Parsing JSON response
                data = response.json()
                # Extracting relevant weather information
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                perceived_temp = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                # Printing weather information for each city
                print(f"Weather in {city}:")
                print(f"Description: {weather_description}")
                print(f"Temperature: {temperature} °C")
                print(f"Perceived Temperature: {perceived_temp} °C")
                print(f"Humidity: {humidity}%")
                print(f"Wind Speed: {wind_speed} m/s")
                print()  # Adding empty line for readability
            else:
                print(f"Error: Failed to fetch weather data for {city}. Status code: {response.status_code}")
        print(count)
    except Exception as e:
        print(f"Error: {e}")





# API key for OpenWeatherMap
api_key = "1a729a0ad116278f1b587d8cd1166e52"
# file with list of cities in Nigeria for which weather data will be fetched
with open("nigerian_cities.csv", "r") as file:
    reader = csv.reader(file)
    first_values = [row[0] for row in reader]
    nigerian_cities = first_values

# Fetch weather data for Nigerian cities
fetch_weather_data(api_key, nigerian_cities)

