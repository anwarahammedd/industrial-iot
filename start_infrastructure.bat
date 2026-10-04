@echo off
title Industrial IoT Pipeline

echo ===================================
echo Industrial IoT Infrastructure
echo ===================================
echo.

cd /d A:\de\projects\industrial-iot-airflow

echo [1/8] Starting PostgreSQL...
docker compose -f postgres\docker-compose.yml up -d

echo.
echo [2/8] Starting Kafka...
docker compose -f kafka\docker-compose.yml up -d

echo.
echo Waiting for Infrastructure..
timeout /t 10 /nobreak >nul

echo.
echo [3/8] Starting MailPit...
cd /d A:\de\projects\industrial-iot-airflow\mailpit
docker compose up -d

echo.
echo [4/8] Starting Airflow...
cd /d A:\de\projects\industrial-iot-airflow\airflow
docker compose up -d

echo.
echo [5/8] Starting Grafana...
cd /d A:\de\projects\industrial-iot-airflow\grafana
docker compose up -d



echo.
echo [6/8] Starting OPC UA Server...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq OPC UA Server" | find /I "python.exe" > nul
if errorlevel 1 (
    start "OPC UA Server" cmd /k "cd /d A:\de\projects\industrial-iot-airflow && call .venv\Scripts\activate && python -m opcua.server"
) else (
    echo OPC UA Server is already running.
)

timeout /t 3 /nobreak > nul

echo.
echo [7/8] Starting Kafka Producer...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Kafka Producer" | find /I "python.exe" > nul
if errorlevel 1 (
    start "Kafka Producer" cmd /k "cd /d A:\de\projects\industrial-iot-airflow && call .venv\Scripts\activate && python -m producer.opcua_kafka_producer"
) else (
    echo Kafka Producer is already running
)

timeout /t 3 /nobreak >nul

echo.
echo [8/8] Starting Kafka Consumer...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Kafka Consumer" | find /I "python.exe" >nul
if errorlevel 1 (
    start "Kafka Consumer" cmd /k "cd /d A:\de\projects\industrial-iot-airflow && call .venv\Scripts\activate && python -m consumer.kafka_consumer"
) else (
    echo Kafka Consumer is already running.
)

echo.
echo ============================================================
echo              PIPELINE STARTED
echo ============================================================
echo.
echo Docker:
echo   Kafka       : localhost:9092
echo   PostgreSQL  : localhost:5433
echo.
echo Python:
echo   OPC UA Server
echo   Kafka Producer
echo   Kafka Consumer
echo.
echo ============================================================

pause