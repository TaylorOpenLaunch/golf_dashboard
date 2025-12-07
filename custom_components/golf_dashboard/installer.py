"""Install bundled Golf Dashboard Lovelace dashboards into Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)

TEMPLATE_FILES: tuple[str, ...] = (
    "nova_open_golfcoach.yaml",
    "nova_premium_analytics.yaml",
    "example_lovelace.yaml",
)

DASHBOARD_URL_PATH = "golf_dashboard"
DASHBOARD_TITLE = "Golf Dashboard"
DASHBOARD_ICON = "mdi:golf-tee"

DEFAULT_VIEW: dict[str, Any] = {
    "title": DASHBOARD_TITLE,
    "path": DASHBOARD_URL_PATH,
    "cards": [
        {
            "type": "vertical-stack",
            "cards": [
                {
                    "type": "entities",
                    "title": "Nova Metrics",
                    "entities": [
                        {"entity": "sensor.nova_ball_speed", "name": "Ball Speed"},
                        {"entity": "sensor.nova_carry_distance", "name": "Carry Distance"},
                        {"entity": "sensor.nova_spin_rate", "name": "Spin Rate"},
                    ],
                },
                {
                    "type": "markdown",
                    "content": (
                        "Edit this dashboard to personalize your Golf Dashboard views. "
                        "Run the installer again anytime; it won't overwrite your changes."
                    ),
                },
            ],
        }
    ],
}


async def async_install_dashboards(hass: HomeAssistant, call: ServiceCall) -> None:
    """Install bundled Lovelace dashboards using storage mode."""
    config_root = Path(hass.config.path())
    templates_source = Path(__file__).parent / "dashboards"
    templates_target = Path(hass.config.path("golf_dashboard/dashboards"))

    _LOGGER.info("Golf Dashboard: installing storage-mode dashboard into %s", config_root)

    _ensure_templates(templates_source, templates_target)
    dashboard = await _get_or_create_dashboard(hass)
    await _ensure_dashboard_has_view(dashboard)

    _LOGGER.info("Golf Dashboard storage dashboard installed or updated successfully")


def _ensure_templates(source_dir: Path, target_dir: Path) -> None:
    """Copy bundled template files to /config/golf_dashboard/dashboards if missing."""
    if not source_dir.is_dir():
        _LOGGER.error("Golf Dashboard: template source directory missing: %s", source_dir)
        raise HomeAssistantError("Dashboard templates missing; reinstall the integration.")

    target_dir.mkdir(parents=True, exist_ok=True)

    for filename in TEMPLATE_FILES:
        src = source_dir / filename
        dest = target_dir / filename

        if dest.exists():
            _LOGGER.debug("Golf Dashboard: %s already exists; leaving untouched", dest)
            continue
        if not src.is_file():
            _LOGGER.error("Golf Dashboard: template file missing: %s", src)
            raise HomeAssistantError(
                f"Template file {filename} is missing; reinstall the integration."
            )
        try:
            shutil.copyfile(src, dest)
            _LOGGER.info("Golf Dashboard: copied template %s", filename)
        except OSError as err:
            _LOGGER.exception("Golf Dashboard: failed to copy %s to %s", src, dest)
            raise HomeAssistantError(f"Failed to copy dashboard template {filename}: {err}") from err


def _get_dashboard_manager(hass: HomeAssistant) -> Any:
    """Return the Lovelace dashboard manager from hass.data."""
    data = hass.data.get("lovelace")
    if not data:
        _LOGGER.error("Golf Dashboard: Lovelace integration data is unavailable")
        raise HomeAssistantError("Lovelace dashboards are not available.")

    dashboards = data.get("dashboards")
    if dashboards is None:
        _LOGGER.error("Golf Dashboard: Lovelace dashboards manager is missing")
        raise HomeAssistantError("Lovelace dashboards manager is not available.")
    return dashboards


async def _get_or_create_dashboard(hass: HomeAssistant):
    """Return an existing storage dashboard or create a new one."""
    dashboards = _get_dashboard_manager(hass)

    try:
        dashboard = await dashboards.async_get_dashboard(DASHBOARD_URL_PATH)
    except Exception as err:  # noqa: BLE001
        _LOGGER.exception("Golf Dashboard: failed to access Lovelace dashboards")
        raise HomeAssistantError("Unable to access Lovelace dashboards.") from err

    if dashboard is not None:
        _LOGGER.info("Golf Dashboard: storage dashboard already exists; leaving it in place")
        return dashboard

    payload = {
        "url_path": DASHBOARD_URL_PATH,
        "title": DASHBOARD_TITLE,
        "icon": DASHBOARD_ICON,
        "mode": "storage",
        "show_in_sidebar": True,
        "require_admin": False,
    }

    try:
        await hass.services.async_call("lovelace", "create", payload, blocking=True)
    except Exception as err:  # noqa: BLE001
        _LOGGER.exception("Golf Dashboard: failed to create storage dashboard via service")
        raise HomeAssistantError("Failed to create Golf Dashboard.") from err

    dashboard = await dashboards.async_get_dashboard(DASHBOARD_URL_PATH)
    if dashboard is None:
        _LOGGER.error("Golf Dashboard: dashboard creation reported success but was not found")
        raise HomeAssistantError("Golf Dashboard creation did not complete.")

    return dashboard


async def _ensure_dashboard_has_view(dashboard: Any) -> None:
    """Ensure the dashboard has at least one view without overwriting user edits."""
    try:
        config = await dashboard.async_get_config()
    except Exception as err:  # noqa: BLE001
        _LOGGER.exception("Golf Dashboard: failed to load dashboard config")
        raise HomeAssistantError("Failed to load Golf Dashboard configuration.") from err

    if config is None:
        config = {}
    if not isinstance(config, dict):
        _LOGGER.error("Golf Dashboard: dashboard config is not a mapping; refusing to modify")
        raise HomeAssistantError("Dashboard configuration is invalid; please recreate it.")

    views = config.get("views") or []
    if views:
        _LOGGER.debug("Golf Dashboard: dashboard already has %s view(s); leaving untouched", len(views))
        return

    config["views"] = [DEFAULT_VIEW]

    try:
        await dashboard.async_save(config)
        _LOGGER.info("Golf Dashboard: added default view to storage dashboard")
    except Exception as err:  # noqa: BLE001
        _LOGGER.exception("Golf Dashboard: failed to save dashboard config")
        raise HomeAssistantError("Failed to update Golf Dashboard views.") from err
