@echo off
title Industrial IoT - Stop All

echo ==================================
echo    INDUSTRIAL IoT - STOP ALL
echo ==================================
echo.

cd /d A:\de\projects\industrial-iot-airflow

echo [1/4] Stopping OPC UA Server...
taskkill /FI "WINDOWTITLE eq Kafka Producer*" /T /F >nul 2>&1

echo.
echo [2/4] Stopping Kafka Producer...
taskkill /FI "WINDOWTITLE eq Kafka Producer*" /T /F >nul 2>&1

echo.
echo [3/4] Stopping Kafka Consumer...
taskkill /FI "WINDOWTITLE eq Kafka Consumer*" /T /F >nul 2>&1

timeout /t 2 /nobreak >nul

echo.
echo [4/4] Stopping Docker services...

echo.
echo Stopping Mailpit...
cd /d A:\de\projects\industrial-iot-airflow\mailpit
docker compose down

echo.
echo Stopping Airflow...
cd /d A:\de\projects\industrial-iot-airflow\airflow
docker compose down

echo.
echo Stopping Grafana...
cd /d A:\de\projects\industrial-iot-airflow\grafana
docker compose down

echo.
echo Stopping Kafka...
cd /d A:\de\projects\industrial-iot-airflow\kafka
docker compose down

echo.
echo Stopping PostgreSQL...
cd /d A:\de\projects\industrial-iot-airflow\postgres
docker compose down

echo.
echo ==========================================
echo       INDUSTRIAL IoT STOPPED
echo ==========================================
echo.

pause