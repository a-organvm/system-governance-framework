"""Tests for the repository exposure disposition ledger."""

import importlib.util
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "config" / "repository-exposure.inventory.json"
SPEC = importlib.util.spec_from_file_location(
    "validate_repository_exposure", ROOT / "scripts" / "validate_repository_exposure.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def test_bundled_inventory_is_complete_and_valid():
    ledger = inventory()
    assert MODULE.validate(ledger) == []
    assert ledger["coverage"] == {"repositories": 323, "public": 239, "private": 84}


def test_duplicate_repository_is_rejected():
    ledger = inventory()
    duplicate = ledger["dispositions"]["public_candidate"][0]
    ledger["dispositions"]["keep_private"].append(duplicate)
    errors = "\n".join(MODULE.validate(ledger))
    assert "appears in both" in errors


def test_publication_tranche_cannot_bypass_candidate_audit():
    ledger = inventory()
    ledger["next_tranche"]["repositories"].append(
        ledger["dispositions"]["keep_private"][0]
    )
    errors = "\n".join(MODULE.validate(ledger))
    assert "only public_candidate" in errors


def test_reference_split_cannot_lose_completed_status():
    ledger = deepcopy(inventory())
    ledger["reference_split"]["status"] = "split_required"
    assert "reference split" in "\n".join(MODULE.validate(ledger))

