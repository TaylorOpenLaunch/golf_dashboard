import sys
import pathlib
from typing import Any, List

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DASHBOARD_DIR = REPO_ROOT / "custom_components" / "golf_dashboard" / "dashboards"


def iter_entities(node: Any, path: str = "root"):
    """Yield (entity_id, location_path) pairs from a Lovelace config structure."""
    if isinstance(node, dict):
        for key, value in node.items():
            new_path = f"{path}.{key}"
            if key == "entity" and isinstance(value, str):
                yield value, new_path
            else:
                yield from iter_entities(value, new_path)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            new_path = f"{path}[{idx}]"
            yield from iter_entities(item, new_path)


def main() -> int:
    errors: List[str] = []

    if not DASHBOARD_DIR.is_dir():
        print(f"Dashboard directory not found: {DASHBOARD_DIR}", file=sys.stderr)
        return 1

    yaml_files = sorted(DASHBOARD_DIR.glob("*.yaml"))
    if not yaml_files:
        print(f"No dashboard YAML files found under {DASHBOARD_DIR}", file=sys.stderr)
        return 1

    for yaml_path in yaml_files:
        try:
            text = yaml_path.read_text(encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{yaml_path}: failed to read file: {exc}")
            continue

        try:
            data = yaml.safe_load(text)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{yaml_path}: invalid YAML ({exc})")
            continue

        for entity_id, loc in iter_entities(data, path=yaml_path.name):
            if not isinstance(entity_id, str):
                continue

            if entity_id.startswith("sensor."):
                if not entity_id.startswith("sensor.nova_"):
                    errors.append(
                        f"{yaml_path}: {loc} uses non-NOVA sensor entity "
                        f"'{entity_id}' (expected sensor.nova_*)"
                    )
            elif entity_id.startswith("binary_sensor."):
                if not entity_id.startswith("binary_sensor.nova_"):
                    errors.append(
                        f"{yaml_path}: {loc} uses non-NOVA binary_sensor entity "
                        f"'{entity_id}' (expected binary_sensor.nova_*)"
                    )

    if errors:
        print("Dashboard validation failed with the following problems:")
        for msg in errors:
            print(f" - {msg}")
        return 1

    print("Dashboard YAML and entity IDs validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
