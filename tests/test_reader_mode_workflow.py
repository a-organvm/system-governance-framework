"""Structural tests for the reusable reader-mode documentation workflow."""

import re
import subprocess
from pathlib import Path

import yaml

WORKFLOW_PATH = Path(".github/workflows/reusable-reader-mode-docs.yml")


def _workflow() -> dict:
    return yaml.load(WORKFLOW_PATH.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def test_workflow_exposes_pinned_authority_inputs() -> None:
    workflow_call = _workflow()["on"]["workflow_call"]
    inputs = workflow_call["inputs"]

    assert inputs["engine-ref"]["required"] == "true"
    assert inputs["schema-ref"]["required"] == "true"
    assert inputs["project-schema"]["default"] == "schemas/project-record-v1.schema.json"
    assert inputs["assertion-schema"]["default"] == "schemas/assertion-evidence.v1.schema.json"


def test_workflow_uses_canonical_schema_and_runtime_repositories() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    schema_checkout = next(step for step in steps if step.get("name") == "Checkout canonical schemas")
    install = next(step for step in steps if step.get("id") == "install")

    assert schema_checkout["with"]["repository"] == "organvm-iv-taxis/schema-definitions"
    assert "github.com/organvm/organvm-engine.git" in install["run"]
    consumer_checkout = next(step for step in steps if step.get("name") == "Checkout consumer repository")
    assert consumer_checkout["with"]["fetch-depth"] == "0"


def test_workflow_emits_receipt_before_enforcement() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    step_names = [step["name"] for step in steps]

    assert step_names.index("Write machine-readable receipt") < step_names.index(
        "Enforce documentation gate"
    )
    assert step_names.index("Upload validation receipt") < step_names.index(
        "Enforce documentation gate"
    )
    receipt = next(step for step in steps if step["name"] == "Write machine-readable receipt")
    assert "reader-mode-ci.receipt.v1" in receipt["run"]


def test_workflow_invokes_canonical_assertion_semantics() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    semantic = next(
        step for step in steps if step.get("name") == "Validate canonical assertion semantics"
    )

    assert "validate_governance_memory.py" in semantic["run"]
    assert "validator.validate_document" in semantic["run"]
    assert "remote assertion_ref" in semantic["run"]
    assert "project-record.v1 requires a local, commit-bound record" in semantic["run"]
    assert "EXPECTED_REPOSITORY" in semantic["env"]
    assert "repository_role canonical requires canonical_repository" in semantic["run"]
    assert '"mirror", "deployment-artifact", "upstream-fork"' in semantic["run"]
    validate = next(step for step in steps if step.get("id") == "validate")
    assert "--require-git-tracked-evidence" in validate["run"]
    assert "--actual-repository" in validate["run"]
    assert "${{ github.repository }}" in validate["env"]["ACTUAL_REPOSITORY"]


def test_semantic_validation_is_part_of_status_and_gate() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    status = next(step for step in steps if step.get("id") == "status")
    gate = next(step for step in steps if step.get("name") == "Enforce documentation gate")

    assert "SEMANTIC_OUTCOME" in status["env"]
    assert "SEMANTIC_OUTCOME" in status["run"]
    assert "SEMANTIC_OUTCOME" in gate["env"]
    assert "Canonical assertion semantic validation failed" in gate["run"]


def test_paths_are_passed_through_environment_and_control_chars_are_rejected() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    path_step = next(step for step in steps if step.get("id") == "paths")
    validate = next(step for step in steps if step.get("id") == "validate")
    audit = next(step for step in steps if step.get("id") == "audit")

    assert "contains a control character" in path_step["run"]
    assert "must be the canonical" in path_step["run"]
    assert "schemas/project-record-v1.schema.json" in path_step["run"]
    assert "schemas/assertion-evidence.v1.schema.json" in path_step["run"]
    assert "${{ steps.paths.outputs.record }}" in validate["env"]["PROJECT_RECORD_PATH"]
    assert "${{" not in validate["run"]
    assert "${{" not in audit["run"]


def test_receipt_captures_resolved_environment() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    receipt = next(step for step in steps if step["name"] == "Write machine-readable receipt")

    assert "pip freeze" not in receipt["run"]
    assert '"pip", "freeze", "--all"' in receipt["run"]
    assert 'direct_url("organvm-engine")' in receipt["run"]
    assert '"platform": platform.platform()' in receipt["run"]
    assert '"require_git_tracked_evidence": True' in receipt["run"]


def test_external_actions_are_immutable() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    external_actions = [step["uses"] for step in steps if "uses" in step]

    assert external_actions
    assert all(re.search(r"@[0-9a-fA-F]{40}$", action) for action in external_actions)


def test_embedded_scripts_parse() -> None:
    steps = _workflow()["jobs"]["reader-mode"]["steps"]
    for step in steps:
        script = step.get("run")
        if not script:
            continue
        shell_check = subprocess.run(
            ["bash", "-n"],
            input=script,
            text=True,
            capture_output=True,
            check=False,
        )
        assert shell_check.returncode == 0, f"{step['name']}: {shell_check.stderr}"
        for match in re.finditer(
            r"python - <<'PY'\n(.*?)\nPY(?:\n|$)",
            script,
            flags=re.DOTALL,
        ):
            compile(match.group(1), f"workflow:{step['name']}", "exec")
