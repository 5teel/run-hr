# HR Monitor

Repurposing an F45 LionHeart chest strap as a personal heart rate monitor with custom software for runs.

## Hardware facts
- Strap charges over USB (charge-only cable, no USB data device appears).
- Strap talks Bluetooth LE, standard Heart Rate Service (0x180D), HR Measurement char 0x2A37.
- Only advertises while worn with skin contact — wet the electrodes to test at a desk.
- PC radio: Intel Wireless Bluetooth (BLE capable).

## Stack
- Python 3.13 + `bleak` (BLE). Run from `C:\Development\HR Monitor` in PowerShell.
- `scan.py` — list nearby BLE devices, flags HR ones.
- `hr.py` — connect, print live BPM + RR intervals, log to `session_*.csv`.

## Learnings
- **[2026-09-14] USB hub shows nothing for the strap** — the USB connection is charge-only. All data is BLE.
