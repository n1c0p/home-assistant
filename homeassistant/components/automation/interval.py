"""
Offer time listening automation rules.

For more details about this automation rule, please refer to the documentation
at https://home-assistant.io/docs/automation/trigger/#time-trigger
"""
import logging

import voluptuous as vol

from homeassistant.core import callback
from homeassistant.const import CONF_PLATFORM
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_time_change

CONF_HOURS = 'hours'
CONF_MINUTES = 'minutes'
CONF_SECONDS = 'seconds'

_LOGGER = logging.getLogger(__name__)

TRIGGER_SCHEMA = vol.All(vol.Schema({
    vol.Required(CONF_PLATFORM): 'interval',
    CONF_HOURS: vol.Any(vol.Coerce(int), vol.Coerce(str)),
    CONF_MINUTES: vol.Any(vol.Coerce(int), vol.Coerce(str)),
    CONF_SECONDS: vol.Any(vol.Coerce(int), vol.Coerce(str)),
}), cv.has_at_least_one_key(CONF_HOURS, CONF_MINUTES, CONF_SECONDS))


async def async_trigger(hass, config, action, automation_info):
    """Listen for state changes based on configuration."""
    hours = config.get(CONF_HOURS)
    minutes = config.get(CONF_MINUTES)
    seconds = config.get(CONF_SECONDS)

    @callback
    def time_automation_listener(now):
        """Listen for time changes and calls action."""
        hass.async_run_job(action, {
            'trigger': {
                'platform': 'interval',
                'now': now,
            },
        })

    return async_track_time_change(hass, time_automation_listener,
                                   hour=hours, minute=minutes, second=seconds)
