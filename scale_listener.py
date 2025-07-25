import asyncio, datetime, sqlite3
from bleak import BleakClient, BleakScanner
from database_manager import DatabaseManager

ADDRESS = "D0:4D:00:43:1C:06"
CHARACTERISTIC_UUID = "0000fff1-0000-1000-8000-00805f9b34fb"
database = DatabaseManager('weight_data.db')
is_connecting = False

async def main():
    global scanner
    scanner = BleakScanner(detection_callback=detection_handler)

    await scanner.start()

    await asyncio.Event().wait()


async def detection_handler(device, advertisement_data):
    global is_connecting
    if device.address == ADDRESS and not is_connecting:
        try:
            is_connecting = True
            print("Connecting...")
            await scanner.stop()
            await deviceConnector(ADDRESS)
        finally:
            is_connecting = False


async def deviceConnector(address):
    client = BleakClient(ADDRESS, timeout=10.0)
    try:
        await client.connect()
        print("Connection successful!")
        await client.start_notify(CHARACTERISTIC_UUID, dataProcessor)    
        while client.is_connected:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        await client.disconnect()
        await scanner.start()


def dataProcessor(characteristic, data):
    EXPECTED_PACKET_LENGTH = 22
    FINAL_READING_BYTE = 19
    if len(data) != EXPECTED_PACKET_LENGTH:
        return
    if data[FINAL_READING_BYTE] != 1:
        return
    print("Processing data")
    weight = int.from_bytes(data[10:12], byteorder='little')
    high_weight_mode = data[12]
    if high_weight_mode:
        weight += 65536
    weight /= 1000
    weight *= 2.20462
    print("Attempting to store data")
    storeWeight(weight)


def storeWeight(weight):
    print("Weight read:", weight)
    database.add_reading(weight)
    


asyncio.run(main())
