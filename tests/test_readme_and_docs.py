"""Sanity checks for README and docs presence/content."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_nova():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "NOVA by OpenLaunch" in readme


def test_docs_index_exists_and_is_linked():
    docs_index = ROOT / "docs" / "index.md"
    assert docs_index.is_file()
    text = docs_index.read_text(encoding="utf-8")
    assert "NOVA by OpenLaunch" in text
