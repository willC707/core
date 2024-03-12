from homeassistant.components.light import LightEntity

from .const import DOMAIN

class MyLight(LightEntity):
    def __init__(self, hass, entry):
        self._hass = hass
        self._entry = entry

    @property
    def name(self):
        return "My Light"
    
    @property
    def is_on(self):
        pass

    def turn_on(self, **kwargs):
        ser = self._hass.data[DOMAIN][self._entry.entry_id]
        ser.write(b'I')

    def turn_off(self, **kwargs):
        ser = self._hass.data[DOMAIN][self._entry.entry_id]
        ser.write(b'O')