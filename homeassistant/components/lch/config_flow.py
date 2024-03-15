"""Config flow for Light Control Hub integration."""

from __future__ import annotations

import logging
from typing import Any

import serial
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PORT): str,
    }
)


class LightControlHub:
    def __init__(self, port) -> None:
        self.ser = serial.Serial(port, 115200)

    def send_command(self, command):
        self.ser.write(command.encode())

    def test_connection(self):
        try:
            self.send_command("I")
            return True
        except:
            return False


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    hub = LightControlHub(data[CONF_PORT])

    if not hub.test_connection():
        raise CannotConnect
    return {"title": "Light Control Hub"}


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Light Control Hub."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect"""
