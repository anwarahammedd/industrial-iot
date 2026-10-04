# Industrial IoT Data Pipeline

End-to-end Industrial IoT pipeline simulating a PLC and processing sensor data in real time.

### Architecture

```text
Virtual PLC → OPC UA → Kafka → PostgreSQL → Grafana
                         ↓
                      Airflow
                         ↓
                  Monitoring & Alerts
```

### Tech Stack

**Python · OPC UA · Apache Kafka · PostgreSQL · Apache Airflow · Grafana · Docker · Mailpit**

### Features

* Virtual PLC with temperature, pressure, flow & motor status
* OPC UA industrial communication
* Real-time Kafka streaming
* PostgreSQL data storage
* Live Grafana dashboard
* Airflow health & data-quality monitoring
* Kafka & sensor freshness checks
* Failure/recovery detection with email alerts
* Persistent infrastructure with Docker
* Startup/stop automation scripts
* Environment-based configuration and secret protection

### Project Structure

```text
plc/        → Virtual PLC
opcua/      → OPC UA server/client
producer/   → Kafka producer
consumer/   → Kafka consumer
kafka/      → Kafka
postgres/   → PostgreSQL
airflow/    → Monitoring DAGs
grafana/    → Dashboard
mailpit/    → Email alerts
```

**Author:** Anwar Ahammed
