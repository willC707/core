"""The Light Control Hub integration."""

from __future__ import annotations

import serial
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN



# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Light Control Hub from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    
    try:
        ser = serial.Serial(entry.data["port"])
        print(f"Using port {ser.name}")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return False
    
    hass.data[DOMAIN][entry.entry_id] = ser

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
