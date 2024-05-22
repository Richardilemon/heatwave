import csv
import json

def extract_ng_cities(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extracting the names and coordinates of cities with country code "NG"
        ng_cities = [(city['name'], city['coord']['lat'], city['coord']['lon']) for city in data if city['country'] == 'NG']

        # Writing the extracted data to a CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Writing header row
            writer.writerow(['City', 'Latitude', 'Longitude'])
            # Writing data rows
            writer.writerows(ng_cities)
        
        print(f"Extraction successful. {len(ng_cities)} cities extracted and saved in {output_file}.")
    except Exception as e:
        print(f"Error: {e}")

# Input file containing city data
input_file = "city.list.json"
# Output file to save extracted city names and coordinates as CSV
output_file = "nigerian_cities.csv"

# Extract names and coordinates of Nigerian cities and save to output file as CSV
extract_ng_cities(input_file, output_file)
