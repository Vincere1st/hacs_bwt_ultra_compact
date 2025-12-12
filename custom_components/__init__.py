"""The BWT Ultra Compact integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_MAC_ADDRESS, CONF_PASSKEY
from .ble_coordinator import BWTCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BWT Ultra Compact from a config entry."""
    if DOMAIN not in hass.data:
        hass.data.setdefault(DOMAIN, {})

    # Check if entry already exists
    if entry.entry_id in hass.data[DOMAIN]:
        _LOGGER.warning("Entry %s already exists, cleaning up", entry.entry_id)
        await async_unload_entry(hass, entry)

    try:
        # Initialize coordinator
        coordinator = BWTCoordinator(
            mac_address=entry.data[CONF_MAC_ADDRESS],
            passkey=entry.data[CONF_PASSKEY]
        )

        hass.data[DOMAIN][entry.entry_id] = {
            "coordinator": coordinator
        }

        # Forward the setup to the sensor platform
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        return True

    except Exception as e:
        _LOGGER.error("Failed to setup BWT Ultra Compact: %s", e)
        if entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id)
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Disconnect from device
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    await coordinator.disconnect()

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
