import requests
import json
from datetime import datetime

# Configuration
API_KEY = "2cc0774a23b84c6e55b1c6fa9ea1a7f9"  # Replace with your actual API key
CITY = "Bangalore"
COUNTRY_CODE = "IN"

def fetch_weather_data():
    """Fetch current weather data from OpenWeather API"""
    
    # API endpoint
    url = f"http://api.openweathermap.org/data/2.5/weather"
    
    # Parameters
    params = {
        'q': f'{CITY},{COUNTRY_CODE}',
        'appid': API_KEY,
        'units': 'metric'  # For Celsius
    }
    
    try:
        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for bad status codes
        
        # Parse JSON response
        data = response.json()
        
        # Extract relevant information
        weather_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'city': data['name'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'weather_main': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'cloudiness': data['clouds']['all']
        }
        
        # Print the data
        print("Weather Data Fetched Successfully!")
        print("=" * 50)
        for key, value in weather_info.items():
            print(f"{key}: {value}")
        print("=" * 50)
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

if __name__ == "__main__":
    # Fetch and display weather data
    weather_data = fetch_weather_data()
    
    if weather_data:
        print("\n✓ Data fetch successful!")
    else:
        print("\n✗ Data fetch failed!")