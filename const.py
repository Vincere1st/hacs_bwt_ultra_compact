"""Constants for the BWT Ultra Compact Devstral integration."""
from __future__ import annotations

DOMAIN = "bwt_ultra_compact_devstral"

# BLE Constants
BLE_SERVICE_UUID = "D973F2E0-B19E-11E2-9E96-0800200C9A66"
BLE_BROADCAST_CHARACTERISTIC_UUID = "D973F2E3-B19E-11E2-9E96-0800200C9A66"

# Device info
DEFAULT_NAME = "BWT Ultra Compact Devstral"
MANUFACTURER = "BWT"

# Configuration
CONF_MAC_ADDRESS = "mac_address"
CONF_PASSKEY = "passkey"

# Default values
DEFAULT_PASSKEY = "123456"

# Sensor types
SENSOR_TYPES = {
    "salt_level": {
        "name": "Salt Level",
        "unit": "%",
        "icon": "mdi:salt",
        "device_class": None,
    },
    "water_consumption": {
        "name": "Water Consumption",
        "unit": "L",
        "icon": "mdi:water",
        "device_class": None,
    },
    "regen_count": {
        "name": "Regeneration Count",
        "unit": None,
        "icon": "mdi:refresh",
        "device_class": None,
    },
}

# Binary sensor types
BINARY_SENSOR_TYPES = {
    "connection_status": {
        "name": "Connection Status",
        "device_class": "connectivity",
        "icon": "mdi:bluetooth",
    },
    "salt_low": {
        "name": "Salt Low",
        "device_class": "problem",
        "icon": "mdi:alert",
    },
}
