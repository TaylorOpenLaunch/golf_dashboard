"""Basic validation for manifest.json and hacs.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_basic_fields():
    manifest_path = ROOT / "custom_components" / "golf_dashboard" / "manifest.json"
    manifest = load_json(manifest_path)

    assert manifest.get("domain") == "golf_dashboard"
    assert "version" in manifest
    assert isinstance(manifest.get("codeowners"), list)
    # SSDP should be present and a list for NOVA
    assert isinstance(manifest.get("ssdp"), list)


def test_hacs_json_basic_fields():
    hacs_path = ROOT / "hacs.json"
    hacs = load_json(hacs_path)

    assert hacs.get("filename") == "custom_components/golf_dashboard"
    assert "name" in hacs
    assert "homeassistant" in hacs
    assert isinstance(hacs.get("domains"), list)
