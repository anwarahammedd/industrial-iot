from datetime import datetime

import psycopg2

from airflow.sdk import dag, task

POSTGRES_HOST = "host.docker.internal"
POSTGRES_PORT = 5433
POSTGRES_DB = "industrial_iot"
POSTGRES_USER = "iot_user"
POSTGRES_PASSWORD = "iot_password"

@dag(
    dag_id = "sensor_data_quality",
    start_date = datetime(2026, 1, 1),
    schedule = "*/5 * * * *",
    catchup = False,
    tags = ["industrial-iot", "quality"]
)

def sensor_data_quality():
    @task
    def check_data_quality():
        connection = psycopg2.connect(
            host = POSTGRES_HOST,
            port = POSTGRES_PORT,
            database = POSTGRES_DB,
            user = POSTGRES_USER,
            password = POSTGRES_PASSWORD,
        )

        cursor = connection.cursor()

        # Check records from the last 5 minutes
        cursor.execute("""
            SELECT
                COUNT(*),
                COUNT(temperature),
                COUNT(pressure),
                COUNT(flow),
                COUNT(motor_status)
            FROM sensor_readings
            WHERE created_at >= NOW() - INTERVAL '5 minutes'
        """)

        total, temperature_count, pressure_count, flow_count, motor_count = (
            cursor.fetchone()
        )

        print(f"Total records: {total}")
        print(f"Temperature values: {temperature_count}")
        print(f"Pressure values: {pressure_count}")
        print(f"Flow values: {flow_count}")
        print(f"Motor status values: {motor_count}")

        if total == 0:
            raise Exception("No sensor records found!")

        if temperature_count != total:
            raise Exception("Missing temperature values!")

        if pressure_count != total:
            raise Exception("Missing pressure values!")

        if flow_count != total:
            raise Exception("Missing flow values!")

        if motor_count != total:
            raise Exception("Missing motor status values!")

        # Check temperature range
        cursor.execute("""
            SELECT COUNT(*)
            FROM sensor_readings
            WHERE created_at >= NOW() - INTERVAL '5 minutes'
                AND (temperature < 20 OR temperature > 30)
        """)
        invalid_temperature = cursor.fetchone()[0]

        print(f"Invalid temperature records: {invalid_temperature}")

        if invalid_temperature > 0:
            raise Exception(
                f"Found {invalid_temperature} invalid temperature records!"
            )

        # Check pressure range
        cursor.execute("""
                    SELECT COUNT(*)
                    FROM sensor_readings
                    WHERE created_at >= NOW() - INTERVAL '5 minutes'
                      AND (pressure < 2.5 OR pressure > 3.5)
                """)

        invalid_pressure = cursor.fetchone()[0]

        print(f"Invalid pressure records: {invalid_pressure}")

        if invalid_pressure > 0:
            raise Exception(
                f"Found {invalid_pressure} invalid pressure records!"
            )

        # Check flow range
        cursor.execute("""
                    SELECT COUNT(*)
                    FROM sensor_readings
                    WHERE created_at >= NOW() - INTERVAL '5 minutes'
                      AND (flow < 100 OR flow > 130)
                """)

        invalid_flow = cursor.fetchone()[0]

        print(f"Invalid flow records: {invalid_flow}")

        if invalid_flow > 0:
            raise Exception(
                f"Found {invalid_flow} invalid flow records!"
            )

        cursor.close()
        connection.close()
        print("Sensor data quality check passed.")

    check_data_quality()

sensor_data_quality()

