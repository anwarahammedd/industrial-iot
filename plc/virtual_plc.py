import random
import time
import asyncio

class VirtualPLC:
    def __init__(self):
        self.temperature = 25.0
        self.pressure = 3.0
        self.flow = 110.0
        self.motor_status = True

    def generate_sensor_data(self):
        self.temperature = round(
            random.uniform(20, 30), 2
        )

        self.pressure = round(
            random.uniform(2.5, 3.5), 2
        )

        self.flow = round(
            random.uniform(100, 120), 2
        )

        self.motor_status = random.choice(
            [True, False]
        )
        return {
            "temperature": self.temperature,
            "pressure": self.pressure,
            "flow": self.flow,
            "motor_status": self.motor_status
        }

async def main():

    plc = VirtualPLC()

    print("Virtual PLC started.")
    print("Device: P-101")
    print("-" * 40)

    while True:
        data = plc.generate_sensor_data()

        print(
            f"Temperature: {data["temperature"]} °C"
        )

        print(
            f"Pressure: {data["pressure"]} bar"
        )
        print(
            f"Flow: {data["flow"]} L/min"
        )
        print(
            f"Motor: {data["motor_status"]}"
        )

        print("=" * 50)

        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())