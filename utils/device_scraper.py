import asyncio
from bleak import BleakClient

ADDRESS = "D0:4D:00:43:1C:06"

async def main():
    client = BleakClient(ADDRESS, timeout=10.0)
    try:
        await client.connect()
        print("Connection successful!")
        for service in client.services:
            for char in service.characteristics:
                print(f"Service: {service.description}")
                print(f"    Characteristic: {char.uuid}, Properties: {char.properties}")
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        await client.disconnect()
asyncio.run(main())
