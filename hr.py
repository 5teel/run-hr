"""Connect to the first BLE Heart Rate Service device, print live BPM, log to CSV.

Usage:  python hr.py            (auto-finds strap)
        python hr.py AA:BB:...  (connect to a specific address)
Ctrl+C to stop.
"""
import asyncio
import csv
import sys
import time
from datetime import datetime

from bleak import BleakClient, BleakScanner

HR_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb"


def parse_hr(data: bytes):
    """Bluetooth SIG Heart Rate Measurement characteristic."""
    flags = data[0]
    if flags & 0x01:
        bpm, i = int.from_bytes(data[1:3], "little"), 3
    else:
        bpm, i = data[1], 2
    contact = (flags >> 1) & 0x03  # 2 = supported+detected, 3 = supported+not detected
    if flags & 0x08:  # energy expended present
        i += 2
    rr = []
    if flags & 0x10:
        while i + 1 < len(data):
            rr.append(int.from_bytes(data[i:i + 2], "little") / 1024)
            i += 2
    return bpm, contact, rr


async def find_strap():
    print("Scanning for heart rate strap...")
    dev = await BleakScanner.find_device_by_filter(
        lambda d, adv: HR_SERVICE in adv.service_uuids, timeout=20
    )
    if not dev:
        sys.exit("No HR device found. Wear the strap, wet the electrodes, retry.")
    return dev


async def main():
    dev = sys.argv[1] if len(sys.argv) > 1 else await find_strap()
    log_path = datetime.now().strftime("session_%Y%m%d_%H%M%S.csv")
    with open(log_path, "w", newline="") as f:
        log = csv.writer(f)
        log.writerow(["time", "bpm", "contact", "rr_s"])
        start = time.time()

        def on_hr(_, data: bytearray):
            bpm, contact, rr = parse_hr(bytes(data))
            t = time.time() - start
            print(f"\r{t:7.1f}s  {bpm:3d} bpm  rr={rr}   ", end="", flush=True)
            log.writerow([f"{t:.2f}", bpm, contact, " ".join(f"{x:.3f}" for x in rr)])

        async with BleakClient(dev) as client:
            print(f"Connected to {dev}. Logging to {log_path}")
            try:
                batt = await client.read_gatt_char(BATTERY_LEVEL)
                print(f"Battery: {batt[0]}%")
            except Exception:
                pass
            await client.start_notify(HR_MEASUREMENT, on_hr)
            while client.is_connected:
                await asyncio.sleep(1)
            print("\nDisconnected.")


if __name__ == "__main__":
    # self-check on the parser
    assert parse_hr(bytes([0x00, 72])) == (72, 0, [])
    assert parse_hr(bytes([0x16, 60, 0x00, 0x04, 0x00, 0x04])) == (60, 3, [1.0, 1.0])
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
