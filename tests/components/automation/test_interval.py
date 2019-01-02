"""The tests for the time automation."""
import pytest

from homeassistant.setup import async_setup_component
import homeassistant.util.dt as dt_util
import homeassistant.components.automation as automation

from tests.common import (
    async_fire_time_changed, assert_setup_component, mock_component)
from tests.components.automation import common
from tests.common import async_mock_service


@pytest.fixture
def calls(hass):
    """Track calls to a mock serivce."""
    return async_mock_service(hass, 'test', 'automation')


@pytest.fixture(autouse=True)
def setup_comp(hass):
    """Initialize components."""
    mock_component(hass, 'group')


async def test_if_fires_when_hour_matches(hass, calls):
    """Test for firing if hour is matching."""
    assert await async_setup_component(hass, automation.DOMAIN, {
        automation.DOMAIN: {
            'trigger': {
                'platform': 'interval',
                'hours': 0,
            },
            'action': {
                'service': 'test.automation'
            }
        }
    })

    async_fire_time_changed(hass, dt_util.utcnow().replace(hour=0))
    await hass.async_block_till_done()
    assert 1 == len(calls)

    await common.async_turn_off(hass)
    await hass.async_block_till_done()

    async_fire_time_changed(hass, dt_util.utcnow().replace(hour=0))
    await hass.async_block_till_done()
    assert 1 == len(calls)


async def test_if_fires_when_minute_matches(hass, calls):
    """Test for firing if minutes are matching."""
    assert await async_setup_component(hass, automation.DOMAIN, {
        automation.DOMAIN: {
            'trigger': {
                'platform': 'interval',
                'minutes': 0,
            },
            'action': {
                'service': 'test.automation'
            }
        }
    })

    async_fire_time_changed(hass, dt_util.utcnow().replace(minute=0))

    await hass.async_block_till_done()
    assert 1 == len(calls)


async def test_if_fires_when_second_matches(hass, calls):
    """Test for firing if seconds are matching."""
    assert await async_setup_component(hass, automation.DOMAIN, {
        automation.DOMAIN: {
            'trigger': {
                'platform': 'interval',
                'seconds': 0,
            },
            'action': {
                'service': 'test.automation'
            }
        }
    })

    async_fire_time_changed(hass, dt_util.utcnow().replace(second=0))

    await hass.async_block_till_done()
    assert 1 == len(calls)


async def test_if_fires_when_all_matches(hass, calls):
    """Test for firing if everything matches."""
    assert await async_setup_component(hass, automation.DOMAIN, {
        automation.DOMAIN: {
            'trigger': {
                'platform': 'interval',
                'hours': 1,
                'minutes': 2,
                'seconds': 3,
            },
            'action': {
                'service': 'test.automation'
            }
        }
    })

    async_fire_time_changed(hass, dt_util.utcnow().replace(
        hour=1, minute=2, second=3))

    await hass.async_block_till_done()
    assert 1 == len(calls)


async def test_if_fires_periodic_seconds(hass, calls):
    """Test for firing periodically every second."""
    assert await async_setup_component(hass, automation.DOMAIN, {
        automation.DOMAIN: {
            'trigger': {
                'platform': 'interval',
                'seconds': "/2",
            },
            'action': {
                'service': 'test.automation'
            }
        }
    })

    async_fire_time_changed(hass, dt_util.utcnow().replace(
        hour=0, minute=0, second=2))

    await hass.async_block_till_done()
    assert 1 == len(calls)


async def test_if_fires_periodic_minutes(hass, calls):
    """Test for firing periodically every minute."""
    assert await async_setup_component(hass, automation.DOMAIN, {
        automation.DOMAIN: {
            'trigger': {
                'platform': 'interval',
                'minutes': "/2",
            },
            'action': {
                'service': 'test.automation'
            }
        }
    })

    async_fire_time_changed(hass, dt_util.utcnow().replace(
        hour=0, minute=2, second=0))

    await hass.async_block_till_done()
    assert 1 == len(calls)


async def test_if_fires_periodic_hours(hass, calls):
    """Test for firing periodically every hour."""
    assert await async_setup_component(hass, automation.DOMAIN, {
        automation.DOMAIN: {
            'trigger': {
                'platform': 'interval',
                'hours': "/2",
            },
            'action': {
                'service': 'test.automation'
            }
        }
    })

    async_fire_time_changed(hass, dt_util.utcnow().replace(
        hour=2, minute=0, second=0))

    await hass.async_block_till_done()
    assert 1 == len(calls)


async def test_if_not_working_if_no_values_in_conf_provided(hass, calls):
    """Test for failure if no configuration."""
    with assert_setup_component(0):
        assert await async_setup_component(hass, automation.DOMAIN, {
            automation.DOMAIN: {
                'trigger': {
                    'platform': 'interval',
                },
                'action': {
                    'service': 'test.automation'
                }
            }
        })

    async_fire_time_changed(hass, dt_util.utcnow().replace(
        hour=5, minute=0, second=0))

    await hass.async_block_till_done()
    assert 0 == len(calls)
