import sqlite3
from datetime import datetime

def create_database():
    """Create SQLite database and weather table"""
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    
    # Create weather table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            city TEXT NOT NULL,
            temperature REAL,
            feels_like REAL,
            humidity INTEGER,
            pressure INTEGER,
            weather_main TEXT,
            weather_description TEXT,
            wind_speed REAL,
            cloudiness INTEGER
        )
    ''')
    
    conn.commit()
    print("✓ Database created successfully!")
    print(f"✓ Table 'weather' created/verified")
    
    # Show table structure
    cursor.execute("PRAGMA table_info(weather)")
    columns = cursor.fetchall()
    
    print("\nTable Structure:")
    print("=" * 60)
    for col in columns:
        print(f"Column: {col[1]:<20} Type: {col[2]}")
    print("=" * 60)
    
    conn.close()

if __name__ == "__main__":
    create_database()