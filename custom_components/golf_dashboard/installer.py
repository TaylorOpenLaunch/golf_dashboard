"""Install bundled Golf Dashboard Lovelace dashboards into Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

import yaml

from homeassistant.core import HomeAssistant

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


async def async_install_dashboards(hass: HomeAssistant) -> None:
    """Install bundled Lovelace dashboards and register them in configuration.yaml."""
    config_dir = Path(hass.config.path())
    config_yaml = config_dir / "configuration.yaml"
    source_dir = Path(__file__).parent / "dashboards"

    _LOGGER.info("Golf Dashboard: installing Lovelace dashboards into %s", config_dir)

    if not source_dir.is_dir():
        _LOGGER.error("Golf Dashboard: dashboard source directory missing: %s", source_dir)
        return

    missing = [name for name in DASHBOARD_TEMPLATES.values() if not (source_dir / name).is_file()]
    if missing:
        _LOGGER.error("Golf Dashboard: missing dashboard template files: %s", ", ".join(missing))
        return

    for target_name, template_name in DASHBOARD_TEMPLATES.items():
        template = source_dir / template_name
        target = config_dir / target_name
        if target.exists():
            _LOGGER.info(
                "Golf Dashboard: dashboard file %s already exists, leaving it untouched",
                target_name,
            )
            continue

        await hass.async_add_executor_job(shutil.copyfile, template, target)
        _LOGGER.info("Golf Dashboard: installed dashboard template %s", target_name)

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
            else:
                _LOGGER.warning(
                    "Golf Dashboard: configuration.yaml was not a mapping; starting fresh"
                )
                config_data = {}
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Golf Dashboard: could not read configuration.yaml: %s", err)
            return
    else:
        config_modified = True

    lovelace = config_data.get("lovelace")
    if not isinstance(lovelace, dict):
        lovelace = {}
        config_modified = True
    dashboards = lovelace.get("dashboards")
    if not isinstance(dashboards, dict):
        dashboards = {}
        config_modified = True

    for key, dashboard_config in LOVELACE_DASHBOARDS.items():
        if key in dashboards:
            _LOGGER.info(
                "Golf Dashboard: lovelace dashboard %s already configured, leaving untouched", key
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

    await hass.async_add_executor_job(_write_config)
    _LOGGER.info("Golf Dashboard: configuration.yaml updated with Lovelace dashboards")
