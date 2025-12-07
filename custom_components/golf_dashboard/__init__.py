"""The Golf Dashboard integration for NOVA launch monitors."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_MANUFACTURER,
    CONF_MODEL,
    CONF_SERIAL,
    CONF_INSTALL_DASHBOARDS,
    CONF_INSTALL_DASHBOARDS_AGAIN,
)
from .coordinator import GolfDashboardCoordinator
from .installer import async_install_dashboards

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Golf Dashboard integration and register services."""

    async def _handle_install_dashboards(call: ServiceCall) -> None:
        await async_install_dashboards(hass, call)

    hass.services.async_register(DOMAIN, "install_dashboards", _handle_install_dashboards)
    _LOGGER.info("Golf Dashboard: registered service %s.install_dashboards", DOMAIN)

    return True


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

    install_dashboards = entry.data.get(CONF_INSTALL_DASHBOARDS, False)
    if install_dashboards:
        _LOGGER.info("Golf Dashboard: auto-installing dashboards from config entry setup")
        try:
            await async_install_dashboards(hass, None)
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Golf Dashboard: dashboard install failed during setup: %s", err)

    install_again = entry.options.get(CONF_INSTALL_DASHBOARDS_AGAIN, False)
    if install_again:
        _LOGGER.info("Golf Dashboard: re-installing dashboards from options flow")
        try:
            await async_install_dashboards(hass, None)
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Golf Dashboard: dashboard re-install failed: %s", err)
        else:
            new_options = dict(entry.options)
            new_options[CONF_INSTALL_DASHBOARDS_AGAIN] = False
            hass.config_entries.async_update_entry(entry, options=new_options)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator: GolfDashboardCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_stop()

    return unload_ok
