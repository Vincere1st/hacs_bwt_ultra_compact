"""Config flow for BWT Ultra Compact Devstral integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    CONF_MAC_ADDRESS,
    CONF_PASSKEY,
    DEFAULT_PASSKEY,
    DEFAULT_NAME,
)

_LOGGER = logging.getLogger(__name__)

# TODO: Replace with your device-specific checks
async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # TODO: Validate MAC address format
    if not data[CONF_MAC_ADDRESS]:
        raise InvalidMacAddress

    # TODO: Validate passkey is numeric and 6 digits
    if not data[CONF_PASSKEY].isdigit() or len(data[CONF_PASSKEY]) != 6:
        raise InvalidPasskey

    # Return info that you want to store in the config entry.
    return {
        "title": f"{DEFAULT_NAME} ({data[CONF_MAC_ADDRESS]})",
    }

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BWT Ultra Compact Devstral."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_MAC_ADDRESS): str,
                    vol.Required(CONF_PASSKEY, default=DEFAULT_PASSKEY): str,
                }),
            )

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_MAC_ADDRESS): str,
                    vol.Required(CONF_PASSKEY, default=DEFAULT_PASSKEY): str,
                }),
                errors={"base": "cannot_connect"},
            )
        except InvalidMacAddress:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_MAC_ADDRESS): str,
                    vol.Required(CONF_PASSKEY, default=DEFAULT_PASSKEY): str,
                }),
                errors={"base": "invalid_mac_address"},
            )
        except InvalidPasskey:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_MAC_ADDRESS): str,
                    vol.Required(CONF_PASSKEY, default=DEFAULT_PASSKEY): str,
                }),
                errors={"base": "invalid_passkey"},
            )
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            return self.async_abort(reason="unknown")

        return self.async_create_entry(title=info["title"], data=user_input)

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidMacAddress(HomeAssistantError):
    """Error to indicate there is an invalid MAC address."""

class InvalidPasskey(HomeAssistantError):
    """Error to indicate there is an invalid passkey."""
