import sqlite3
from datetime import datetime

DB_NAME = "weather_data.db"

def view_all_records():
    """Display all weather records in the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM weather")
    count = cursor.fetchone()[0]
    
    print(f"\nTotal Records in Database: {count}")
    print("=" * 100)
    
    cursor.execute("""
        SELECT id, timestamp, temperature, feels_like, humidity, 
               weather_description, wind_speed 
        FROM weather 
        ORDER BY timestamp DESC
    """)
    
    records = cursor.fetchall()
    
    if records:
        print(f"{'ID':<5} {'Timestamp':<20} {'Temp(°C)':<10} {'Feels Like':<12} {'Humidity(%)':<12} {'Condition':<20} {'Wind(m/s)':<10}")
        print("-" * 100)
        
        for record in records:
            print(f"{record[0]:<5} {record[1]:<20} {record[2]:<10.1f} {record[3]:<12.1f} {record[4]:<12} {record[5]:<20} {record[6]:<10.1f}")
    else:
        print("No records found!")
    
    print("=" * 100)
    conn.close()

def get_statistics():
    """Calculate basic statistics from weather data"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_records,
            ROUND(AVG(temperature), 2) as avg_temp,
            ROUND(MIN(temperature), 2) as min_temp,
            ROUND(MAX(temperature), 2) as max_temp,
            ROUND(AVG(humidity), 2) as avg_humidity,
            ROUND(AVG(wind_speed), 2) as avg_wind_speed
        FROM weather
    """)
    
    stats = cursor.fetchone()
    
    print("\nWeather Statistics:")
    print("=" * 60)
    print(f"Total Records:        {stats[0]}")
    print(f"Average Temperature:  {stats[1]}°C")
    print(f"Min Temperature:      {stats[2]}°C")
    print(f"Max Temperature:      {stats[3]}°C")
    print(f"Average Humidity:     {stats[4]}%")
    print(f"Average Wind Speed:   {stats[5]} m/s")
    print("=" * 60)
    
    conn.close()

def get_weather_conditions():
    """Show distribution of weather conditions"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT weather_main, COUNT(*) as count
        FROM weather
        GROUP BY weather_main
        ORDER BY count DESC
    """)
    
    conditions = cursor.fetchall()
    
    print("\nWeather Conditions Distribution:")
    print("=" * 40)
    for condition in conditions:
        print(f"{condition[0]:<20} {condition[1]} times")
    print("=" * 40)
    
    conn.close()

def get_latest_record():
    """Display the most recent weather record"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM weather 
        ORDER BY timestamp DESC 
        LIMIT 1
    """)
    
    record = cursor.fetchone()
    
    if record:
        print("\nLatest Weather Record:")
        print("=" * 60)
        print(f"Timestamp:     {record[1]}")
        print(f"City:          {record[2]}")
        print(f"Temperature:   {record[3]}°C")
        print(f"Feels Like:    {record[4]}°C")
        print(f"Humidity:      {record[5]}%")
        print(f"Pressure:      {record[6]} hPa")
        print(f"Condition:     {record[7]} - {record[8]}")
        print(f"Wind Speed:    {record[9]} m/s")
        print(f"Cloudiness:    {record[10]}%")
        print("=" * 60)
    else:
        print("No records found!")
    
    conn.close()

def main_menu():
    """Interactive menu for analysis"""
    while True:
        print("\n" + "=" * 60)
        print("WEATHER DATA ANALYSIS MENU")
        print("=" * 60)
        print("1. View all records")
        print("2. Get statistics")
        print("3. Weather conditions distribution")
        print("4. View latest record")
        print("5. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            view_all_records()
        elif choice == '2':
            get_statistics()
        elif choice == '3':
            get_weather_conditions()
        elif choice == '4':
            get_latest_record()
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()