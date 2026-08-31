"""Tests for the AI platform governance evidence inventory."""

from copy import deepcopy
from pathlib import Path

import pytest

from ai_platform_governance import InventoryError, load_inventory, validate_inventory

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "config" / "ai-platform-governance.inventory.json"


def test_bundled_inventory_is_valid():
    inventory = load_inventory(INVENTORY_PATH)
    assert len(inventory["controls"]) == 16
    assert len(inventory["scope"]["organizations"]) == 10
    assert inventory["scope"]["user_accounts"] == ["4444J99"]


def test_duplicate_control_ids_are_rejected():
    inventory = load_inventory(INVENTORY_PATH)
    duplicate = deepcopy(inventory["controls"][0])
    inventory["controls"].append(duplicate)
    assert "duplicate control id" in "\n".join(validate_inventory(inventory))


def test_unresolved_control_requires_next_action():
    inventory = load_inventory(INVENTORY_PATH)
    inventory["controls"][0]["next_action"] = ""
    assert "next_action is required" in "\n".join(validate_inventory(inventory))


def test_admin_control_needs_admin_export_before_verified():
    inventory = load_inventory(INVENTORY_PATH)
    control = inventory["controls"][0]
    control["status"] = "verified"
    errors = "\n".join(validate_inventory(inventory))
    assert "admin_export evidence" in errors


def test_invalid_status_is_rejected():
    inventory = load_inventory(INVENTORY_PATH)
    inventory["controls"][0]["status"] = "probably-fine"
    assert "status is invalid" in "\n".join(validate_inventory(inventory))


def test_non_json_inventory_has_actionable_error(tmp_path):
    path = tmp_path / "inventory.json"
    path.write_text("not-json", encoding="utf-8")
    with pytest.raises(InventoryError, match="Unable to load inventory"):
        load_inventory(path)
