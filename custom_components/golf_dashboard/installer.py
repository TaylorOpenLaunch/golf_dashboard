"""Install bundled Golf Dashboard Lovelace dashboards into Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util.yaml import load_yaml, save_yaml

_LOGGER = logging.getLogger(__name__)

TEMPLATE_FILES: tuple[str, ...] = (
    "nova_open_golfcoach.yaml",
    "nova_premium_analytics.yaml",
    "example_lovelace.yaml",
)

MAIN_DASHBOARD_CONTENT = """title: Golf Dashboard
icon: mdi:golf-tee

views:
  - !include golf_dashboard/dashboards/nova_open_golfcoach.yaml
  - !include golf_dashboard/dashboards/nova_premium_analytics.yaml
"""

DASHBOARD_ENTRY_DEFAULTS: dict[str, Any] = {
    "mode": "yaml",
    "title": "Golf Dashboard",
    "icon": "mdi:golf-tee",
    "show_in_sidebar": True,
    "filename": "golf_dashboard.yaml",
}


async def async_install_dashboards(hass: HomeAssistant, call: ServiceCall) -> None:
    """Install bundled Lovelace dashboards and register them in configuration.yaml."""
    config_root = Path(hass.config.path())
    source_dir = Path(__file__).parent / "dashboards"
    target_dir = Path(hass.config.path("golf_dashboard/dashboards"))
    main_dashboard_path = Path(hass.config.path("golf_dashboard.yaml"))
    config_path = Path(hass.config.path("configuration.yaml"))

    _LOGGER.info("Golf Dashboard: installing dashboards into %s", config_root)

    _ensure_templates(source_dir, target_dir)
    _ensure_main_dashboard(main_dashboard_path)
    await _ensure_configuration_dashboard(hass, config_path)

    _LOGGER.info("Golf Dashboard dashboards installed or updated successfully")


def _ensure_templates(source_dir: Path, target_dir: Path) -> None:
    """Copy bundled templates into /config/golf_dashboard/dashboards if missing."""
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


def _ensure_main_dashboard(main_path: Path) -> None:
    """Create /config/golf_dashboard.yaml if missing."""
    if main_path.exists():
        _LOGGER.debug("Golf Dashboard: %s already exists; leaving untouched", main_path)
        return
    try:
        main_path.write_text(MAIN_DASHBOARD_CONTENT, encoding="utf-8")
        _LOGGER.info("Golf Dashboard: created %s", main_path.name)
    except OSError as err:
        _LOGGER.exception("Golf Dashboard: failed to create %s", main_path)
        raise HomeAssistantError(f"Failed to create {main_path.name}: {err}") from err


async def _load_configuration_yaml(hass: HomeAssistant, path: Path) -> dict[str, Any]:
    """Load configuration.yaml using Home Assistant's YAML loader."""
    try:
        data = await hass.async_add_executor_job(load_yaml, path)
    except HomeAssistantError:
        raise
    except Exception as err:  # noqa: BLE001
        raise HomeAssistantError(f"Error reading {path.name}: {err}") from err

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise HomeAssistantError(
            f"Expected {path.name} to contain a mapping, got {type(data).__name__}"
        )
    return data


async def _ensure_configuration_dashboard(
    hass: HomeAssistant, config_path: Path
) -> None:
    """Ensure configuration.yaml registers the Golf Dashboard."""
    if config_path.exists():
        config = await _load_configuration_yaml(hass, config_path)
    else:
        config = {"lovelace": {"mode": "storage", "dashboards": {}}}

    lovelace = config.get("lovelace")
    if lovelace is None:
        lovelace = {}
        config["lovelace"] = lovelace
    if not isinstance(lovelace, dict):
        _LOGGER.error("Golf Dashboard: lovelace section is not a mapping; refusing to modify")
        raise HomeAssistantError(
            "Cannot update configuration.yaml: 'lovelace' section is not a mapping. Please update manually."
        )

    dashboards = lovelace.get("dashboards")
    if dashboards is None:
        dashboards = {}
        lovelace["dashboards"] = dashboards
    if not isinstance(dashboards, dict):
        _LOGGER.error("Golf Dashboard: lovelace.dashboards is not a mapping; refusing to modify")
        raise HomeAssistantError(
            "Cannot update configuration.yaml: 'dashboards' section is not a mapping. Please update manually."
        )

    entry = dashboards.get("golf_dashboard")
    if entry is None:
        dashboards["golf_dashboard"] = dict(DASHBOARD_ENTRY_DEFAULTS)
    elif isinstance(entry, dict):
        for key, value in DASHBOARD_ENTRY_DEFAULTS.items():
            dashboards["golf_dashboard"].setdefault(key, value)
    else:
        _LOGGER.error(
            "Golf Dashboard: dashboards.golf_dashboard is not a mapping; refusing to modify"
        )
        raise HomeAssistantError(
            "Cannot update configuration.yaml: dashboards.golf_dashboard is not a mapping. Please update manually."
        )

    try:
        await hass.async_add_executor_job(save_yaml, config_path, config)
        _LOGGER.info("Golf Dashboard: configuration.yaml updated with Lovelace dashboard entry")
    except OSError as err:
        _LOGGER.exception("Golf Dashboard: failed to write configuration.yaml")
        raise HomeAssistantError(
            "Failed to write configuration.yaml. Please update it manually."
        ) from err
