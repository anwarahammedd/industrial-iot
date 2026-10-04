from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv("/opt/airflow/.env")
import psycopg2

from airflow.sdk import dag, task

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

@dag(
    dag_id = "sensor_health_check",
    start_date = datetime(2026, 1,1),
    schedule = "*/5 * * * *",
    catchup = False,
    tags = ["industrial-iot", "monitoring"]
)

def sensor_health_check():

    @task
    def check_sensor_data():
        connection = psycopg2.connect(
            host = POSTGRES_HOST,
            port = POSTGRES_PORT,
            database = POSTGRES_DB,
            user = POSTGRES_USER,
            password = POSTGRES_PASSWORD,
        )
        
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM sensor_readings
            WHERE created_at >= NOW() - INTERVAL '2 minutes'
        """)
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        print(f"Sensor records received in last 2 minutes: {count}")

        if count == 0:
            raise Exception(
                "No sensor data received in the last 2 minutes!"
            )
        print("Sensor pipeline is healthy.")

    check_sensor_data()

sensor_health_check()
