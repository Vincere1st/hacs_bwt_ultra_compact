"""Binary sensor platform for BWT Ultra Compact Devstral integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    BINARY_SENSOR_TYPES,
    DEFAULT_NAME,
    MANUFACTURER,
)
from .ble_coordinator import BWTCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the BWT Ultra Compact Devstral binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    binary_sensors = []
    for sensor_type, config in BINARY_SENSOR_TYPES.items():
        binary_sensors.append(
            BWTBinarySensor(
                coordinator=coordinator,
                entity_description=BinarySensorEntityDescription(
                    key=sensor_type,
                    name=f"{DEFAULT_NAME} {config['name']}",
                    device_class=config["device_class"],
                    icon=config["icon"],
                ),
                sensor_type=sensor_type,
            )
        )

    async_add_entities(binary_sensors)

class BWTBinarySensor(CoordinatorEntity[BWTCoordinator], BinarySensorEntity):
    """Representation of a BWT Ultra Compact Devstral binary sensor."""

    def __init__(
        self,
        coordinator: BWTCoordinator,
        entity_description: BinarySensorEntityDescription,
        sensor_type: str,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{coordinator.mac_address}_{sensor_type}"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.mac_address)},
            "name": DEFAULT_NAME,
            "manufacturer": MANUFACTURER,
            "model": "CPED Ultra Compact",
            "sw_version": self.coordinator.data.get("version", "Unknown"),
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.connected and bool(self.coordinator.data)

    async def async_update(self) -> None:
        """Update the binary sensor."""
        await self.coordinator.update()

    @property
    def is_on(self) -> bool | None:
        """Return the state of the binary sensor."""
        data = self.coordinator.data

        if self._sensor_type == "connection_status":
            return self.coordinator.connected
        elif self._sensor_type == "salt_low":
            # Consider salt low if less than 20%
            return data.get("salt_percentage", 1) < 0.2

        return None
