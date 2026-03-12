# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CircuitPython application for a Raspberry Pi Pico W that displays the next train departure time on an SSD1306 OLED display. It queries the Entur journey planner GraphQL API (Norwegian public transit) for trips from NSR:StopPlace:337 to NSR:StopPlace:716, showing the expected departure time and minutes until departure.

## Hardware & Platform

- **Board**: Raspberry Pi Pico W (CircuitPython, board VID 0x239A / PID 0x8120)
- **Display**: SSD1306 128x64 OLED via I2C (GP0=SDA, GP1=SCL, address 0x3C, rotated 180°)
- **Runtime**: CircuitPython (not standard CPython) — uses `board`, `wifi`, `socketpool`, `displayio`, etc.

## Deploying Code

Copy `code.py` to the mounted CircuitPython volume:

```
./sync.sh        # copies code.py to /Volumes/CIRCUITPY/
```

CircuitPython auto-reloads when `code.py` changes on the device.

## WiFi Configuration

WiFi credentials are read from `settings.toml` on the device (not in this repo) via `os.getenv()`:
- `WIFI_SSID`
- `WIFI_PASSWORD`

## Dependencies

Libraries in `lib/` (vendored, not managed by a package manager):
- `adafruit_displayio_ssd1306` — SSD1306 display driver
- `adafruit_display_text` — text/label rendering
- `adafruit_requests` — HTTP requests
- `adafruit_connection_manager` — socket/connection pooling
- `adafruit_datetime` — datetime parsing

## Key Constraints

- CircuitPython has limited memory and no `pip` — all libraries must be pre-installed in `lib/`
- SSL requires an explicit root certificate embedded in `code.py` (Google Trust Services WR3)
- The Entur API uses GraphQL with `Content-Type: application/graphql`
- The main loop polls every 60 seconds
