# HR Monitor

Repurposing an F45 LionHeart chest strap as a personal heart rate monitor with custom software for runs.

**Status (2026-09-14):** the product is now **Hearty**, a module inside Body Atlas (`C:\Development\Body Atlas`, route `/hearty`). This folder keeps the standalone prototype PWA (still live on GitHub Pages) and the desktop Python tools. New features go in Body Atlas, not here.

## Hardware facts
- Strap charges over USB (charge-only cable, no USB data device appears).
- Strap talks Bluetooth LE, standard Heart Rate Service (0x180D), HR Measurement char 0x2A37.
- Only advertises while worn with skin contact — wet the electrodes to test at a desk.
- PC radio: Intel Wireless Bluetooth (BLE capable).

## Stack
- **Phone app (the real product):** `index.html` + `manifest.json` + `sw.js` + `icon.svg` — single-file PWA using Web Bluetooth. Android Chrome only (iOS Safari has no Web Bluetooth). Sessions stored in localStorage, CSV export per run.
- **Desktop tools:** Python 3.13 + `bleak`. `scan.py` lists BLE devices and flags HR ones; `hr.py` connects, prints live BPM + RR, logs `session_*.csv`.

## Deploy
- Repo: https://github.com/5teel/run-hr (this folder is its own repo; parent `C:\Development` is a separate repo).
- GitHub Pages from `master` branch root → https://5teel.github.io/run-hr/
- Push to `master` = deploy. Web Bluetooth requires HTTPS, so always test on the Pages URL, not file://.
- Remote is HTTPS (no SSH key on this machine).

## Learnings
- **[2026-09-14] USB hub shows nothing for the strap** — the USB connection is charge-only. All data is BLE.
- **[2026-09-14] Android Chrome picker "stuck scanning"** — Chrome needs the "Nearby devices" permission (Android 12+) and Bluetooth + Location on; a dismissed prompt = endless scan. Also a strict `services:['heart_rate']` filter finds nothing if the strap omits 0x180D from its advert — filter by namePrefix too and keep a "Show all devices" fallback.
