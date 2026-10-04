from datetime import datetime

from kafka import KafkaAdminClient

from airflow.sdk import dag, task

KAFKA_SERVER = "industrial-iot-kafka:29092"

@dag(
    dag_id = "kafka_health_check",
    start_date = datetime(2026, 1, 1),
    schedule = "*/5 * * * *",
    catchup = False,
    tags = ["industrial-iot", "kafka", "monitoring"]
)

def kafka_health_check():
    @task
    def check_kafka():

        client = KafkaAdminClient(
            bootstrap_servers = KAFKA_SERVER,
            client_id="airflow-kafka-health-check",
        )

        topics = client.list_topics()

        print(f"Kafka topics: {topics}" )

        if "sensor-readings" not in topics:
            client.close()
            raise Exception(
                "Kafka topic 'sensor-readings' does not exist!"
            )
        print("Kafka broker is reachable.")
        print("sensor-readings topic exists.")

        client.close()
    check_kafka()

kafka_health_check()