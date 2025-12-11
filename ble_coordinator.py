"""BLE Coordinator for BWT Ultra Compact Devstral."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from bleak import BleakClient, BleakError
from bleak.backends.device import BLEDevice

from .const import (
    BLE_SERVICE_UUID,
    BLE_BROADCAST_CHARACTERISTIC_UUID,
)

_LOGGER = logging.getLogger(__name__)

class BWTCoordinator:
    """Class to manage BLE connection and data reading."""

    def __init__(self, mac_address: str, passkey: str) -> None:
        """Initialize the coordinator."""
        self.mac_address = mac_address
        self.passkey = passkey
        self._client: BleakClient | None = None
        self._device: BLEDevice | None = None
        self._connected = False
        self._data: dict[str, Any] = {}

    @property
    def connected(self) -> bool:
        """Return True if connected to device."""
        return self._connected

    @property
    def data(self) -> dict[str, Any]:
        """Return the latest data from device."""
        return self._data

    async def connect(self) -> bool:
        """Connect to the BLE device."""
        try:
            _LOGGER.debug("Connecting to BLE device %s", self.mac_address)
            self._client = BleakClient(self.mac_address)
            await self._client.connect()
            self._connected = True
            _LOGGER.info("Connected to BLE device %s", self.mac_address)
            return True
        except BleakError as e:
            _LOGGER.error("Failed to connect to BLE device: %s", e)
            self._connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from the BLE device."""
        if self._client and self._connected:
            try:
                await self._client.disconnect()
                self._connected = False
                _LOGGER.info("Disconnected from BLE device %s", self.mac_address)
            except BleakError as e:
                _LOGGER.error("Failed to disconnect from BLE device: %s", e)

    async def read_broadcast_data(self) -> dict[str, Any] | None:
        """Read broadcast data from the device."""
        if not self._client or not self._connected:
            _LOGGER.error("Not connected to device")
            return None

        try:
            _LOGGER.debug("Reading broadcast data")
            data = await self._client.read_gatt_char(BLE_BROADCAST_CHARACTERISTIC_UUID)
            if data:
                parsed_data = self._parse_broadcast_data(data)
                self._data = parsed_data
                _LOGGER.debug("Broadcast data: %s", parsed_data)
                return parsed_data
            return None
        except BleakError as e:
            _LOGGER.error("Failed to read broadcast data: %s", e)
            return None

    def _parse_broadcast_data(self, data: bytearray) -> dict[str, Any]:
        """Parse the broadcast data according to the Perla Blue protocol."""
        if len(data) < 15:
            _LOGGER.error("Invalid broadcast data length: %d", len(data))
            return {}

        bytes_data = bytearray(data)

        def get_word(offset: int, little_endian: bool = True) -> int:
            """Get 2-byte word from data."""
            if little_endian:
                return bytes_data[offset] + (bytes_data[offset + 1] << 8)
            return (bytes_data[offset] << 8) + bytes_data[offset + 1]

        UINT_MAX = 0xFFFF

        remaining = get_word(0, True) + get_word(2, True) * UINT_MAX
        total_capacity = get_word(10, True) * 1000
        bitmask = bytes_data[12] if len(bytes_data) > 12 else 0

        # Calculate salt percentage
        if total_capacity <= 0:
            salt_percentage = 0
        else:
            percentage = remaining / total_capacity
            if percentage > 500:  # Protect against int wrapping
                percentage = 0
            salt_percentage = max(0, min(1, percentage))

        return {
            "remaining_salt": remaining,
            "total_capacity": total_capacity,
            "salt_percentage": salt_percentage,
            "quarter_hours_idx": get_word(4, True),
            "days_idx": get_word(6, True),
            "regen_count": get_word(8, True),
            "alarm": bool(bitmask & 0x01),
            "quarter_hours_looped": bool(bitmask & 0x02),
            "days_looped": bool(bitmask & 0x04),
            "version": f"{bytes_data[13]}, {bytes_data[14]}" if len(bytes_data) > 14 else "Unknown",
        }

    async def update(self) -> None:
        """Update data from the device."""
        if not self._connected:
            await self.connect()

        if self._connected:
            await self.read_broadcast_data()
