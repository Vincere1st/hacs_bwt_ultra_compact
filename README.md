# BWT Ultra Compact Devstral Home Assistant Integration

This is a custom Home Assistant integration for the BWT CPED Ultra Compact water softener.

## Features

- **Bluetooth Connection**: Connects to your BWT device via Bluetooth
- **Salt Level Monitoring**: Shows current salt level percentage
- **Water Consumption**: Tracks water usage (via regeneration count)
- **Regeneration Count**: Shows how many times the device has regenerated
- **Connection Status**: Monitors Bluetooth connection status
- **Low Salt Alerts**: Binary sensor for low salt warnings

## Installation

### Manual Installation

1. Copy the `bwt_ultra_compact_devstral` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Go to **Settings** > **Devices & Services** > **Add Integration**
4. Search for "BWT Ultra Compact Devstral" and add it
5. Enter your device's MAC address and passkey

### HACS Installation (Recommended)

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant
4. Follow the configuration steps above

## Configuration

You will need:
- **MAC Address**: The Bluetooth MAC address of your device (e.g., `03:12:00:21:00:53`)
- **Passkey**: The 6-digit passkey for your device (default is `123456`)

## Entities Created

### Sensors
- **Salt Level**: Percentage of salt remaining (0-100%)
- **Water Consumption**: Water usage in liters (via regeneration count)
- **Regeneration Count**: Number of regeneration cycles

### Binary Sensors
- **Connection Status**: Shows if the device is connected via Bluetooth
- **Salt Low**: Alerts when salt level is below 20%

## Troubleshooting

- Ensure Bluetooth is enabled on your Home Assistant host
- Make sure the device is within Bluetooth range
- Check that the MAC address and passkey are correct
- Restart Home Assistant if the integration doesn't appear

## Technical Details

This integration uses the BLE (Bluetooth Low Energy) protocol to communicate with the BWT CPED Ultra Compact device. It implements the same protocol used by the official BWT mobile app.

- **Service UUID**: `D973F2E0-B19E-11E2-9E96-0800200C9A66`
- **Characteristic UUID**: `D973F2E3-B19E-11E2-9E96-0800200C9A66`

## License

MIT License
