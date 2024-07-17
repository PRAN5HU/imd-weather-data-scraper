import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL of the webpage containing the weather data
url = "https://city.imd.gov.in/citywx/city_weather_test_try.php?id=42174"
# Function to fetch and scrape weather data
def fetch_weather_data():
    # Fetch the webpage content
    response = requests.get(url)
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the past 24 hours weather data
    weather_table = soup.find('table', {'width': '715'})
    
    # Initialize variables to store scraped data
    max_temp = None
    min_temp = None
    rainfall = None
    humidity_0830 = None
    humidity_1730 = None
    
    # Find each row of data in the table
    rows = weather_table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 2:
            label = cells[0].text.strip()
            value = cells[1].text.strip()
    
            if "Maximum Temp" in label:
                max_temp = value
            elif "Minimum Temp" in label:
                min_temp = value
            elif "24 Hours Rainfall" in label:
                rainfall = value
            elif "Relative Humidity at 0830 hrs" in label:
                humidity_0830 = value
            elif "Relative Humidity at 1730 hrs" in label:
                humidity_1730 = value
    
    # Print the scraped data
    print(f"Maximum Temperature: {max_temp}")
    print(f"Minimum Temperature: {min_temp}")
    print(f"24 Hours Rainfall: {rainfall}")
    print(f"Relative Humidity at 0830 hrs: {humidity_0830}")
    print(f"Relative Humidity at 1730 hrs: {humidity_1730}")
    
    return [max_temp, min_temp, rainfall, humidity_0830, humidity_1730]

# Function to write data to CSV file
def write_to_csv(data):
    file_exists = os.path.isfile('pilani_temp.csv')
    
    with open('pilani_temp.csv', 'a', newline='') as csvfile:
        fieldnames = ['Max Temp', 'Min Temp', 'Rainfall', 'Humidity 0830 hrs', 'Humidity 1730 hrs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'Max Temp': data[0],
            'Min Temp': data[1],
            'Rainfall': data[2],
            'Humidity 0830 hrs': data[3],
            'Humidity 1730 hrs': data[4]
        })

# Function to update data every 10 hours
def update_weather_data():
    while True:
        weather_data = fetch_weather_data()
        write_to_csv(weather_data)
        print("Data updated in pilani_temp.csv")
        time.sleep(10 * 3600)  # Sleep for 10 hours

# Start the update process
if __name__ == "__main__":
    update_weather_data()
