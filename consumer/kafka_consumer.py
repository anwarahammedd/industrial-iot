import json
import os

from dotenv import load_dotenv
from kafka import KafkaConsumer
import psycopg2

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def create_kafka_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="industrial-iot-consumer",
        value_deserializer=lambda value:
            json.loads(value.decode("utf-8"))
    )

def create_postgres_connection():

    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def save_to_postgres(connection, data):
    cursor = connection.cursor()

    query="""
        INSERT INTO sensor_readings(
            device_id,
            temperature,
            pressure,
            flow,
            motor_status
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            data["device_id"],
            data["temperature"],
            data["pressure"],
            data["flow"],
            data["motor_status"]
        )
    )
    connection.commit()
    cursor.close()

def main():
    consumer = create_kafka_consumer()
    postgres_connection = create_postgres_connection()

    print("=" * 60)
    print("Industrial IoT Kafka Consumer")
    print("=" * 60)
    print("Kafka        : Connected")
    print("PostgreSQL   : Connected")
    print("-" * 60)

    try:
        for message in consumer:

            data = message.value

            print("Message received from Kafka")
            print(data)
            save_to_postgres(
                postgres_connection,
                data
            )
            print("Saved to Postgres")
            print(
                f"Kafka offset: {message.offset}"
            )
            print("-" * 60)
    except KeyboardInterrupt:
        print()
        print("Kafka Consumer Stopped.")

    finally:
        consumer.close()
        postgres_connection.close()

if __name__ == "__main__":
    main()