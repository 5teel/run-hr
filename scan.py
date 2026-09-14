"""Scan for BLE devices; flag anything advertising the Heart Rate Service (0x180D)."""
import asyncio
from bleak import BleakScanner

HR_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"


async def main():
    print("Scanning 10s... (wear the strap, wet the electrodes)")
    devices = await BleakScanner.discover(timeout=10, return_adv=True)
    for d, adv in devices.values():
        hr = HR_SERVICE in adv.service_uuids
        print(f"{'HR ' if hr else '   '} {d.address}  rssi={adv.rssi:4}  name={adv.local_name or d.name!r}  uuids={adv.service_uuids}")


asyncio.run(main())
