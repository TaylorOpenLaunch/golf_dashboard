"""The Golf Dashboard integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_MANUFACTURER, CONF_MODEL, CONF_SERIAL
from .coordinator import GolfDashboardCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Golf Dashboard from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = GolfDashboardCoordinator(
        hass,
        host=entry.data[CONF_HOST],
        port=entry.data[CONF_PORT],
        name=entry.data[CONF_NAME],
        manufacturer=entry.data.get(CONF_MANUFACTURER),
        model=entry.data.get(CONF_MODEL),
        serial=entry.data.get(CONF_SERIAL),
    )

    # Start the coordinator (connects to device)
    await coordinator.async_start()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator: GolfDashboardCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_stop()

    return unload_ok
