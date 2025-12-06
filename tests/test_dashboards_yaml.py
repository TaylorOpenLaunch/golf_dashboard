"""Validate dashboard YAML files parse correctly."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _yaml_files():
    dashboards_dir = ROOT / "dashboards"
    yield from dashboards_dir.glob("*.yaml")


def test_all_dashboard_yaml_is_valid():
    for yaml_path in _yaml_files():
        text = yaml_path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        assert isinstance(data, (dict, list))
