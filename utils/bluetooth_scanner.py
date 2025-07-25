import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Name: {device.name}, Address: {device.address}")

asyncio.run(main())
