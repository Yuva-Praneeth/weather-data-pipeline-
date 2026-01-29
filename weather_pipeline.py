import requests
import sqlite3
from datetime import datetime

# Configuration
API_KEY = "Api Key Here"
CITY = "Bangalore"
COUNTRY_CODE = "IN"
DB_NAME = "weather_data.db"

def fetch_weather_data():
    """Fetch current weather data from OpenWeather API"""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f'{CITY},{COUNTRY_CODE}',
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        
        
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
        
        print("✓ Weather data fetched successfully!")
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching weather data: {e}")
        return None

def save_to_database(weather_info):
    """Save weather data to SQLite database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Insert data into table
        cursor.execute('''
            INSERT INTO weather (
                timestamp, city, temperature, feels_like, humidity, 
                pressure, weather_main, weather_description, 
                wind_speed, cloudiness
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather_info['timestamp'],
            weather_info['city'],
            weather_info['temperature'],
            weather_info['feels_like'],
            weather_info['humidity'],
            weather_info['pressure'],
            weather_info['weather_main'],
            weather_info['weather_description'],
            weather_info['wind_speed'],
            weather_info['cloudiness']
        ))
        
        conn.commit()
        print(f"✓ Data saved to database! (Record ID: {cursor.lastrowid})")
        
        # Show what was saved
        print("\nSaved Data:")
        print("=" * 60)
        for key, value in weather_info.items():
            print(f"{key}: {value}")
        print("=" * 60)
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False

def run_pipeline():
    """Run the complete ETL pipeline"""
    print("Starting Weather Data Pipeline...")
    print("=" * 60)
    
    # Extract
    print("\n[1/2] Extracting data from API...")
    weather_data = fetch_weather_data()
    
    if not weather_data:
        print("\n✗ Pipeline failed: Could not fetch weather data")
        return
    
    # Load
    print("\n[2/2] Loading data into database...")
    success = save_to_database(weather_data)
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Pipeline completed successfully!")
        print("=" * 60)
    else:
        print("\n✗ Pipeline failed: Could not save to database")

if __name__ == "__main__":
    run_pipeline()