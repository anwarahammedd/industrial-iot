import asyncio

from asyncua import Client

OPC_UA_URL = "opc.tcp://localhost:4840/industrial-iot"

async def sensor_data_stream():
    async with Client(OPC_UA_URL) as client:
        objects = client.nodes.objects
        plc = await objects.get_child(
            ["2:VirtualPLC"]
        )

        temperature = await  plc.get_child(
            ["2:Temperature"]
        )

        pressure = await plc.get_child(
            ["2:Pressure"]
        )

        flow = await plc.get_child(
            ["2:Flow"]
        )

        motor_status = await plc.get_child(
            ["2:MotorStatus"]
        )
        print("OPC UA Client started.")
        print("Connected to:", OPC_UA_URL)
        print("-" * 50)
        while True:
            data = {
                "device_id": "P-101",
                "temperature": await temperature.read_value(),
                "pressure": await pressure.read_value(),
                "flow": await flow.read_value(),
                "motor_status": await motor_status.read_value(),
            }
            yield data

            await asyncio.sleep(5)

async def main():
    async for data in sensor_data_stream():
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
