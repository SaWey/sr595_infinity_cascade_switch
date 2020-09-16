"""
Allows to configure a switch using sr595_infinity_cascade shield
Code borrowed from bbb_gpio switch component
"""
import wiringpi
import logging

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchDevice
from homeassistant.const import (DEVICE_DEFAULT_NAME, CONF_PLATFORM, CONF_ADDRESS, CONF_NAME, CONF_DEVICES)
from homeassistant.helpers.entity import ToggleEntity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_BASE_PIN =  'base_pin'
CONF_PIN_COUNT = 'pin_count'
CONF_DATA_PIN =  'data_pin'
CONF_CLOCK_PIN = 'clock_pin'
CONF_LATCH_PIN = 'latch_pin'

BASE_PIN = 100
PIN_COUNT = 32
DATA_PIN = 12
CLOCK_PIN = 14
LATCH_PIN = 10

DOMAIN = 'sr595_infinity_cascade_switch'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PLATFORM): DOMAIN,
        CONF_DEVICES: [{
            vol.Required(CONF_ADDRESS): cv.string,
            vol.Required(CONF_NAME): cv.string,
        }],
        vol.Optional(CONF_BASE_PIN, default=BASE_PIN): cv.positive_int,
        vol.Optional(CONF_PIN_COUNT, default=PIN_COUNT): cv.positive_int,
        vol.Optional(CONF_DATA_PIN, default=DATA_PIN): cv.positive_int,
        vol.Optional(CONF_CLOCK_PIN, default=CLOCK_PIN): cv.positive_int,
        vol.Optional(CONF_LATCH_PIN, default=LATCH_PIN): cv.positive_int,
    }
)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set pin configuration"""
    BASE_PIN = config.get(CONF_BASE_PIN)
    PIN_COUNT = config.get(CONF_PIN_COUNT)
    DATA_PIN = config.get(CONF_DATA_PIN)
    CLOCK_PIN = config.get(CONF_CLOCK_PIN)
    LATCH_PIN = config.get(CONF_LATCH_PIN)
    
    """Set up WiringPi"""
    _LOGGER.debug("Initialising wiringpi: %s", wiringpi.wiringPiSetup())
    wiringpi.sr595Setup(BASE_PIN, PIN_COUNT, DATA_PIN, CLOCK_PIN, LATCH_PIN)
    for i in range(0, PIN_COUNT):
      wiringpi.pinMode(BASE_PIN+i, 1)
      wiringpi.digitalWrite(BASE_PIN+i, 1)

    """Set up the sr595_infinity_cascade devices."""
    devs = config.get(CONF_DEVICES)
    add_devices([SR595ICSwitch(dev[CONF_ADDRESS], dev[CONF_NAME]) for dev in devs])

class SR595ICSwitch(ToggleEntity):
    """Representation of a sr595_infinity_cascade GPIO."""

    def __init__(self, pin, name):
        """Initialize the pin."""
        self._pin = int(pin)
        self._name = name
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self.write_output(self._pin, 0)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self.write_output(self._pin, 1)
        self._state = False
        self.schedule_update_ha_state()

    def write_output(self, pin, value):
        import wiringpi
        """Write a value to a GPIO."""
        # pylint: disable=import-error,undefined-variable
        wiringpi.digitalWrite(BASE_PIN+pin-1, value)
        #_LOGGER.debug("Writing output to: %s", BASE_PIN+pin)