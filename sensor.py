"""Sensor platform for BWT Ultra Compact Devstral integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_TYPES,
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
    """Set up the BWT Ultra Compact Devstral sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    sensors = []
    for sensor_type, config in SENSOR_TYPES.items():
        sensors.append(
            BWTSensor(
                coordinator=coordinator,
                entity_description=SensorEntityDescription(
                    key=sensor_type,
                    name=f"{DEFAULT_NAME} {config['name']}",
                    native_unit_of_measurement=config["unit"],
                    icon=config["icon"],
                    device_class=config["device_class"],
                ),
                sensor_type=sensor_type,
            )
        )

    async_add_entities(sensors)

class BWTSensor(CoordinatorEntity[BWTCoordinator], SensorEntity):
    """Representation of a BWT Ultra Compact Devstral sensor."""

    def __init__(
        self,
        coordinator: BWTCoordinator,
        entity_description: SensorEntityDescription,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
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
        """Update the sensor."""
        await self.coordinator.update()

    @property
    def native_value(self) -> str | float | int | None:
        """Return the state of the sensor."""
        data = self.coordinator.data

        if self._sensor_type == "salt_level":
            return round(data.get("salt_percentage", 0) * 100, 1)
        elif self._sensor_type == "water_consumption":
            # This would need to be calculated from the readings
            # For now, return regen count as a placeholder
            return data.get("regen_count", 0)
        elif self._sensor_type == "regen_count":
            return data.get("regen_count", 0)

        return None
