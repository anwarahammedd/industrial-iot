import json
import os

from dotenv import load_dotenv
from kafka import KafkaProducer

from opcua.client import sensor_data_stream

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers = KAFKA_SERVER,
        value_serializer = lambda value:
            json.dumps(value).encode("utf-8")
    )

async def main():
    producer = create_kafka_producer()

    print("=" * 60)
    print("Industrial IoT Kafka Producer")
    print("=" * 60)
    print(f"Kafka Server: {KAFKA_SERVER}")
    print(f"Kafka Topic: {KAFKA_TOPIC}")
    print("-" * 60)

    try:
        async for data in sensor_data_stream():
            print("OPC UA -> Kafka")
            print(data)

            future = producer.send(
                KAFKA_TOPIC,
                value=data
            )
            metadata = future.get(timeout=10)
            print(
                f"Sent successfully | "
                f"partition={metadata.partition} | "
                f"offset={metadata.offset}"
            )
            print("-" * 60)

    except KeyboardInterrupt:
        print()
        print("Kafka Producer stopped.")

    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())