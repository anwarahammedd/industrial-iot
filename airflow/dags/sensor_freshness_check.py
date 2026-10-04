from datetime import datetime

import psycopg2

from airflow.sdk import dag, task
from airflow.utils.email import send_email_smtp

POSTGRES_HOST = "host.docker.internal"
POSTGRES_PORT = 5433
POSTGRES_USER = "iot_user"
POSTGRES_PASSWORD = "iot_password"
POSTGRES_DB = "industrial_iot"

EMAIL_TO = "test@example.com"

def send_failure_email(latest_record, data_age):
    send_email_smtp(
        to=EMAIL_TO,
        subject="Sensor Pipeline FAILED",
        html_content=f"""
        <h2> Industrial IoT Alert </h2>
        
        <p><strong>Status:</strong> FAILED </p>
        
        <p><strong>Monitor:</strong> sensor_freshness</p>
        
        <p><strong>Latest sensor record:</strong>
        {latest_record}</p>
        
        <p><strong>Data age:</strong>
        {data_age}</p>
        
        <p>
        Sensor data has become stale.
        </p>
        """
    )

def send_recovery_email(latest_record, data_age):
    send_email_smtp(
        to=EMAIL_TO,
        subject="Sensor Pipeline RECOVERED",
        html_content=f"""
        <h2> Industrial IoT Recovery </h2>
        
        <p><strong>Status:</strong> RECOVERED </p>
        
        <p><strong>Monitor:</strong> sensor_freshness</p>
        
        <p><strong>Latest sensor record: </strong>
        {latest_record}</p>
        
        <p><strong>Data age:</strong>
        {data_age}</p>
        
        <p>
        Sensor data is flowing normally again.
        </p>
        """
    )

@dag(
    dag_id = "sensor_freshness_check",
    start_date = datetime(2026, 1, 1),
    schedule = "*/5 * * * *",
    catchup = False,
    tags=["industrial-iot", "monitoring"]
)

def sensor_freshness_check():
    @task
    def check_sensor_freshness():
        connection = psycopg2.connect(
            host = POSTGRES_HOST,
            port = POSTGRES_PORT,
            database = POSTGRES_DB,
            user = POSTGRES_USER,
            password = POSTGRES_PASSWORD
        )

        cursor = connection.cursor()

        # Get latest sensor data
        cursor.execute("""
            SELECT
                MAX(created_at),
                NOW() - MAX(created_at)
            FROM sensor_readings
        """)

        latest_record, data_age = cursor.fetchone()

        print(f"Latest sensor record: {latest_record}")
        print(f"Sensor data age: {data_age}")

        # Get previous monitoring state
        cursor.execute("""
            SELECT status
            FROM monitoring_state
            WHERE monitor_name = 'sensor_freshness'
        """)

        result = cursor.fetchone()

        if result is None:
            previous_status = "HEALTHY"
        else:
            previous_status = result[0]

        print(f"Previous Monitoring State: {previous_status}")

        # Determine current state
        if latest_record is None:
            current_status = "FAILED"

        elif data_age.total_seconds() >= 120:
            current_status = "FAILED"

        else:
            current_status = "HEALTHY"

        print(f"Current monitoring state: {current_status}")

        # --------------------------------
        # STATE CHANGED: HEALTHY -> FAILED
        # --------------------------------

        if (
            previous_status == "HEALTHY"
            and current_status == "FAILED"
        ):
            print("State Changed: HEALTHY -> FAILED")
            try:
                send_failure_email(
                    latest_record,
                    data_age
                )
            except Exception as email_error:
                print(
                    f"Failed to send failure email: {email_error}"
                )
        # --------------------------------
        # STATE CHANGED: FAILED -> HEALTHY
        # --------------------------------

        if (
            previous_status == "FAILED"
            and current_status == "HEALTHY"
        ):
            print("State changed: FAILED -> HEALTHY")

            try:
                send_recovery_email(
                    latest_record,
                    data_age
                )
            except Exception as email_error:
                print(
                    f"Failed to send recovery email: {email_error}"
                )

        # -----------------------
        # Update monitoring state
        # -----------------------
        cursor.execute("""
            UPDATE monitoring_state
            SET
                status = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE monitor_name = 'sensor_freshness'
        """, (current_status,))

        connection.commit()

        cursor.close()
        connection.close()

        # ----------------------------------------
        # Fail the Airflow task if sensor is stale
        # ----------------------------------------

        if current_status == "FAILED":
            raise Exception(
                f"Sensor data is stale! "
                f"Age: {data_age}"
            )
        print("Sensor data is fresh.")

    check_sensor_freshness()

sensor_freshness_check()

