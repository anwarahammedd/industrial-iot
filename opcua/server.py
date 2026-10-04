import asyncio
from asyncua import Server
from plc.virtual_plc import VirtualPLC

OPC_UA_URL = "opc.tcp://0.0.0.0:4840/industrial-iot"

NAMESPACE_URI = "http://industrial-iot-airflow"

async def main():

    # Create Virtual PLC
    plc_device = VirtualPLC()

    # Create OPC UA server
    server = Server()

    # Configure server endpoint
    server.set_endpoint(OPC_UA_URL)


    await server.init()
    # Create our own namespace
    namespace_index = await server.register_namespace(
        NAMESPACE_URI
    )

    # create objects folder
    objects = server.nodes.objects

    # Create Virtual PLC object
    plc = await objects.add_object(
        namespace_index,
        "VirtualPLC"
    )
    # Create OPC UA variables
    temperature = await plc.add_variable(
        namespace_index,
        "Temperature",
        25.0
    )
    pressure = await plc.add_variable(
        namespace_index,
        "Pressure",
        3.0
    )
    flow = await plc.add_variable(
        namespace_index,
        "Flow",
        110.0
    )
    motor_status = await plc.add_variable(
        namespace_index,
        "MotorStatus",
        True
    )

    print("=" * 50)
    print("Industrial IoT OPC UA Server")
    print("=" * 50)
    print(f"Endpoint: {OPC_UA_URL}")
    print("Device : VirtualPLC")
    print("=" * 50)

    # Start OPC UA Server
    async with server:
        while True:
            # Get new values from Virtual PLC
            data = plc_device.generate_sensor_data()

            # Publish PLC values through OPC UA
            await temperature.write_value(
                data["temperature"]
            )
            await pressure.write_value(
                data["pressure"]
            )
            await flow.write_value(
                data["flow"]
            )
            await motor_status.write_value(
                data["motor_status"]
            )

            print(
                f"Temperature = {data['temperature']} °C  | "
                f"Pressure = {data['pressure']} bar  | "
                f"Flow = {data['flow']} L/min  | "
                f"Motor = {data['motor_status']}  "
            )
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())