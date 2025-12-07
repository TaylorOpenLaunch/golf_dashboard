"""Install bundled Golf Dashboard Lovelace dashboards into Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

import yaml

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError

try:
    from homeassistant.config import load_yaml_config_file
except ImportError:  # pragma: no cover - fallback for older HA
    load_yaml_config_file = None

_LOGGER = logging.getLogger(__name__)

DASHBOARD_TEMPLATES: dict[str, str] = {
    "golf_dashboard.yaml": "nova_premium_analytics.yaml",
    "golf_coach.yaml": "nova_open_golfcoach.yaml",
}

LOVELACE_DASHBOARDS: dict[str, dict[str, Any]] = {
    "golf_dashboard": {
        "mode": "yaml",
        "filename": "golf_dashboard.yaml",
        "title": "Golf Dashboard",
        "icon": "mdi:golf",
    },
    "golf_coach": {
        "mode": "yaml",
        "filename": "golf_coach.yaml",
        "title": "Golf Coach",
        "icon": "mdi:account-tie",
    },
}


async def async_install_dashboards(hass: HomeAssistant, call: ServiceCall | None = None) -> None:
    """Install bundled Lovelace dashboards and register them in configuration.yaml."""
    config_dir = Path(hass.config.path())
    config_yaml = Path(hass.config.path("configuration.yaml"))
    golf_dashboard_path = Path(hass.config.path("golf_dashboard.yaml"))
    golf_coach_path = Path(hass.config.path("golf_coach.yaml"))
    source_dir = Path(__file__).parent / "dashboards"

    _LOGGER.info("Golf Dashboard: installing Lovelace dashboards into %s", config_dir)

    if not source_dir.is_dir():
        _LOGGER.error("Golf Dashboard: dashboard source directory missing: %s", source_dir)
        raise HomeAssistantError("Dashboard templates not found; reinstall the integration.")

    missing = [name for name in DASHBOARD_TEMPLATES.values() if not (source_dir / name).is_file()]
    if missing:
        _LOGGER.error("Golf Dashboard: missing dashboard template files: %s", ", ".join(missing))
        raise HomeAssistantError("Dashboard templates are missing; reinstall the integration.")

    template_mapping = {
        golf_dashboard_path: source_dir / DASHBOARD_TEMPLATES["golf_dashboard.yaml"],
        golf_coach_path: source_dir / DASHBOARD_TEMPLATES["golf_coach.yaml"],
    }

    for target, template in template_mapping.items():
        if target.exists():
            _LOGGER.debug("Golf Dashboard: %s already exists; leaving untouched", target.name)
            continue
        try:
            await hass.async_add_executor_job(shutil.copyfile, template, target)
            _LOGGER.info("Golf Dashboard: installed dashboard template %s", target.name)
        except OSError as err:
            _LOGGER.exception("Golf Dashboard: failed to copy %s to %s", template, target)
            raise HomeAssistantError(f"Failed to create {target.name}: {err}") from err

    config_data: dict[str, Any] = {}
    config_modified = False

    if config_yaml.exists():
        _LOGGER.info("Golf Dashboard: ensuring configuration.yaml contains lovelace dashboards")

        def _load_config() -> Any:
            if load_yaml_config_file:
                return load_yaml_config_file(config_yaml)
            with config_yaml.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f)

        try:
            loaded = await hass.async_add_executor_job(_load_config)
            if isinstance(loaded, dict):
                config_data = loaded
            elif loaded is None:
                config_data = {}
            else:
                _LOGGER.warning(
                    "Golf Dashboard: configuration.yaml is not a mapping; refusing to modify dashboards"
                )
                raise HomeAssistantError(
                    "configuration.yaml is not a mapping; please add dashboards manually."
                )
        except Exception as err:  # noqa: BLE001
            _LOGGER.exception("Golf Dashboard: failed to read configuration.yaml")
            raise HomeAssistantError(
                "Failed to update configuration.yaml. Please fix YAML or add dashboards manually."
            ) from err
    else:
        config_modified = True

    lovelace = config_data.get("lovelace")
    if lovelace is None:
        lovelace = {}
        config_modified = True
    if not isinstance(lovelace, dict):
        _LOGGER.warning(
            "Golf Dashboard: lovelace section is not a mapping; refusing to modify dashboards"
        )
        raise HomeAssistantError(
            "configuration.yaml lovelace section is not a mapping; please add dashboards manually."
        )

    dashboards = lovelace.get("dashboards")
    if dashboards is None:
        dashboards = {}
        config_modified = True
    if not isinstance(dashboards, dict):
        _LOGGER.warning(
            "Golf Dashboard: lovelace.dashboards is not a mapping; refusing to modify dashboards"
        )
        raise HomeAssistantError(
            "configuration.yaml lovelace.dashboards is not a mapping; please add dashboards manually."
        )

    for key, dashboard_config in LOVELACE_DASHBOARDS.items():
        if key in dashboards:
            _LOGGER.debug(
                "Golf Dashboard: lovelace dashboard %s already configured; leaving untouched", key
            )
            continue
        dashboards[key] = dashboard_config
        _LOGGER.info(
            "Golf Dashboard: registered lovelace dashboard %s with file %s",
            key,
            dashboard_config.get("filename"),
        )
        config_modified = True

    lovelace["dashboards"] = dashboards
    config_data["lovelace"] = lovelace

    if not config_modified and config_yaml.exists():
        _LOGGER.info("Golf Dashboard: configuration.yaml already contains required dashboards")
        _LOGGER.info("Golf Dashboard dashboards installed/updated successfully")
        return

    def _write_config() -> None:
        tmp_path = config_yaml.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                config_data,
                f,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
            )
        tmp_path.replace(config_yaml)

    try:
        await hass.async_add_executor_job(_write_config)
    except OSError as err:
        _LOGGER.exception("Golf Dashboard: failed to write configuration.yaml")
        raise HomeAssistantError(
            "Failed to write configuration.yaml. Please update it manually."
        ) from err

    _LOGGER.info("Golf Dashboard: configuration.yaml updated with Lovelace dashboards")
    _LOGGER.info("Golf Dashboard dashboards installed/updated successfully")
