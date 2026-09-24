import os
import sys
import psycopg2
from datetime import datetime

# Simulated incoming messy API data payload
mock_api_payload = [
    {"city": "Lagos", "temperature_c": 28.5, "humidity": 82, "recorded_at": "2026-09-24 10:00:00"},
    {"city": "Nairobi", "temperature_c": None, "humidity": 60, "recorded_at": "2026-09-24 10:00:00"}, # CRITICAL ERROR: Temperature is Missing!
    {"city": "London", "temperature_c": 15.2, "humidity": 75, "recorded_at": "2026-09-24 10:00:00"},
    {"city": "Sahara_Station", "temperature_c": 120.0, "humidity": 5, "recorded_at": "2026-09-24 10:00:00"} # CRITICAL ERROR: Out of bounds (>60C)!
]

def run_quality_checks(record):
    """
    SSIS Equivalent: Data Flow Error Output/Conditional Split
    Validates business logic rules before letting data pass to the warehouse.
    """
    # Rule 1: Check for Null Values in critical metrics
    if record["temperature_c"] is None:
        print(f"❌ REJECTED: Missing temperature field for city {record['city']}")
        return False
        
    # Rule 2: Out of Bound/Anomalous Data Check
    if record["temperature_c"] < -50 or record["temperature_c"] > 60:
        print(f"❌ REJECTED: Temperature value ({record['temperature_c']}°C) out of bounds for city {record['city']}")
        return False
        
    return True

def process_pipeline():
    conn = psycopg2.connect(
        host="localhost", database="weather_warehouse", user="data_engineer", password="password123"
    )
    cursor = conn.cursor()

    # Create target production table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staging_weather (
            city VARCHAR(100),
            temperature_c NUMERIC(5,2),
            humidity INT,
            recorded_at TIMESTAMP,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    print("🩺 Initializing Data Quality Validation Gateways...")
    
    accepted_rows = 0
    for record in mock_api_payload:
        if run_quality_checks(record):
            # If the row passes the quality gate, insert it
            cursor.execute("""
                INSERT INTO staging_weather (city, temperature_c, humidity, recorded_at)
                VALUES (%s, %s, %s, %s);
            """, (record["city"], record["temperature_c"], record["humidity"], record["recorded_at"]))
            accepted_rows += 1
            
    conn.commit()
    print(f"🏁 Pipeline Finished. Successfully loaded {accepted_rows} clean records into the warehouse.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    process_pipeline()
