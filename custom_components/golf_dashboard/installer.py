"""Install bundled Golf Dashboard Lovelace dashboards into Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

import yaml
from yaml import YAMLError

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError

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
    templates_source = Path(__file__).parent / "dashboards"
    templates_target = Path(hass.config.path("golf_dashboard/dashboards"))
    main_dashboard_path = Path(hass.config.path("golf_dashboard.yaml"))
    configuration_path = Path(hass.config.path("configuration.yaml"))

    _LOGGER.info("Golf Dashboard: installing dashboards into %s", config_root)

    _ensure_templates(templates_source, templates_target)
    _ensure_main_dashboard(main_dashboard_path)
    await _ensure_configuration_dashboard(hass, configuration_path)

    _LOGGER.info("Golf Dashboard dashboards installed or updated successfully")


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


def _ensure_main_dashboard(main_path: Path) -> None:
    """Create /config/golf_dashboard.yaml if it does not exist."""
    if main_path.exists():
        _LOGGER.debug("Golf Dashboard: %s already exists; leaving untouched", main_path)
        return
    try:
        main_path.write_text(MAIN_DASHBOARD_CONTENT, encoding="utf-8")
        _LOGGER.info("Golf Dashboard: created %s", main_path.name)
    except OSError as err:
        _LOGGER.exception("Golf Dashboard: failed to create %s", main_path)
        raise HomeAssistantError(f"Failed to create {main_path.name}: {err}") from err


async def _ensure_configuration_dashboard(
    hass: HomeAssistant, config_path: Path
) -> None:
    """Ensure configuration.yaml registers the Golf Dashboard."""
    config: dict[str, Any] = {}

    if config_path.exists():
        def _load_config() -> Any:
            with config_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f)

        try:
            loaded = await hass.async_add_executor_job(_load_config)
        except YAMLError as err:
            _LOGGER.exception("Golf Dashboard: failed to parse configuration.yaml")
            raise HomeAssistantError(
                "Failed to parse configuration.yaml. Please fix YAML syntax and try again."
            ) from err
        except Exception as err:  # noqa: BLE001
            _LOGGER.exception("Golf Dashboard: failed to read configuration.yaml")
            raise HomeAssistantError("Failed to read configuration.yaml.") from err

        if loaded is None:
            config = {}
        elif isinstance(loaded, dict):
            config = loaded
        else:
            _LOGGER.error(
                "Golf Dashboard: configuration.yaml is not a mapping; refusing to modify dashboards"
            )
            raise HomeAssistantError(
                "Cannot update configuration.yaml: file is not a mapping. Please update manually."
            )
    else:
        config = {}

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

    def _write_config() -> None:
        tmp = config_path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                config,
                f,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
            )
        tmp.replace(config_path)

    try:
        await hass.async_add_executor_job(_write_config)
        _LOGGER.info("Golf Dashboard: configuration.yaml updated with Lovelace dashboard entry")
    except OSError as err:
        _LOGGER.exception("Golf Dashboard: failed to write configuration.yaml")
        raise HomeAssistantError(
            "Failed to write configuration.yaml. Please update it manually."
        ) from err
