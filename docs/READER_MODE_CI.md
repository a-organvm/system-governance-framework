# Reader-mode documentation CI

This repository distributes the reusable enforcement layer for the ORGANVM
reader-mode documentation contract. It does not define the editorial standard,
the data contracts, or the audit runtime.

| Concern | Canonical authority |
|---|---|
| Editorial policy, templates, and rubric | [`organvm/editorial-standards`](https://github.com/organvm/editorial-standards) |
| Project-record and assertion schemas | [`organvm-iv-taxis/schema-definitions`](https://github.com/organvm-iv-taxis/schema-definitions) |
| Validation and audit runtime | [`organvm/organvm-engine`](https://github.com/organvm/organvm-engine) |
| Fleet adoption policy | [`organvm/.github`](https://github.com/organvm/.github) |
| Reusable GitHub Actions enforcement | This repository |
| Conversion waves and execution receipts | [`organvm-iv-taxis/orchestration-start-here`](https://github.com/organvm-iv-taxis/orchestration-start-here) |

The reusable workflow validates a repository's project record, follows its local
assertion references, validates those assertion records against both the
canonical schema and its semantic invariants, audits the documentation surface,
and uploads a JSON receipt. Remote assertion references fail closed in
`project-record.v1`: evidence must be local and therefore bound to the validated
repository commit. Nothing in the workflow generates or rewrites project
documentation.

## Thin caller

Add a caller workflow to a consumer repository. Pin the framework itself, the
runtime, and the schemas to full commit SHAs so their source revisions remain
traceable. The receipt also captures Python, runner, direct-install, and resolved
package versions; source SHAs alone do not make an un-hashed package-index
resolution bit-for-bit reproducible.

```yaml
name: Reader-mode documentation

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  documentation:
    uses: organvm-iv-taxis/system-governance-framework/.github/workflows/reusable-reader-mode-docs.yml@<FRAMEWORK_COMMIT_SHA>
    with:
      engine-ref: '<ORGANVM_ENGINE_COMMIT_SHA>'
      schema-ref: '<SCHEMA_DEFINITIONS_COMMIT_SHA>'
      strict-audit: true
```

Use `strict-audit: false` during an adoption pass. Project-record and assertion
integrity remain blocking, while low-scoring documentation is reported without
blocking the pull request. Set it to `true` when the repository is ready to treat
error-level audit findings as a merge gate.

Do not path-filter this caller. Assertion records may hash evidence anywhere in
the repository—including source, tests, manifests, or package metadata—so an
apparently unrelated byte change can invalidate a claim. A required claim-
integrity check must run on every proposed commit.

## Inputs

| Input | Default | Meaning |
|---|---|---|
| `engine-ref` | Required | Immutable `organvm-engine` commit SHA |
| `schema-ref` | Required | Immutable `schema-definitions` commit SHA |
| `project-record` | `project-record.yml` | Record path relative to the selected repository root |
| `project-schema` | `schemas/project-record-v1.schema.json` | Schema path in the schema checkout |
| `assertion-schema` | `schemas/assertion-evidence.v1.schema.json` | Assertion schema path in the schema checkout |
| `repository-root` | `.` | Consumer-repository subtree to inspect |
| `strict-audit` | `false` | Whether error findings make the audit command fail |
| `artifact-name` | `reader-mode-documentation-receipt` | Uploaded artifact name |
| `retention-days` | `30` | Receipt retention period |

All path inputs are resolved within their respective checkouts. Paths that escape
the consumer or schema checkout are rejected. For `repository_role: canonical`,
the workflow also requires `canonical_repository` to equal the actual
`GITHUB_REPOSITORY`. Mirror, deployment-artifact, and upstream-fork records must
name a distinct canonical repository.

The v1 workflow accepts only the canonical project and assertion schema paths
shown in the input table. The path inputs are retained for explicit receipts and
forward migration, not as a mechanism for substituting a weaker schema.

## Outputs and receipt

The workflow exposes `validation-status`, `audit-status`, and `overall-status` to
the caller. It also uploads four JSON files when the corresponding checks run:

- `project-record-validation.json` contains field, route, and assertion errors;
- `canonical-assertion-validation.json` records the pinned schema authority's
  schema and semantic result for every referenced assertion;
- `documentation-audit.json` contains the seven-dimensional audit and findings;
- `receipt.json` records the repository commit, immutable toolchain revisions,
  resolved execution environment, selected inputs, command status, and the three
  reports.

The receipt is the execution record, not substantive evidence for claims made by
the project. Project claims continue to resolve through the canonical
assertion-evidence records declared in `project-record.yml`.

## Local parity

Run the same checks locally with the exact schema checkout used in CI:

```bash
organvm docs validate project-record.yml \
  --schema ../schema-definitions/schemas/project-record-v1.schema.json \
  --assertion-schema ../schema-definitions/schemas/assertion-evidence.v1.schema.json \
  --root . \
  --actual-repository owner/repository \
  --require-git-tracked-evidence \
  --json

python ../schema-definitions/scripts/validate_governance_memory.py \
  docs/evidence/assertions/*.json \
  --schemas-dir ../schema-definitions/schemas

organvm docs audit . --format json --output documentation-audit.json --strict
```

The tracked-evidence flag is the CI boundary: it rejects `.git` internals,
untracked or ignored files, symlinks, and files hidden inside submodules. Omit
the flag only while authoring a pre-commit record locally; that mode verifies
repository-local bytes but does not claim that they are bound to a commit.
The reusable workflow supplies `${{ github.repository }}` as
`--actual-repository`; replace `owner/repository` above with the checkout's
GitHub identity to reproduce canonical-role and delivery-role binding locally.

The generic reusable CI workflow remains responsible for language tests and
coverage. The scheduled repository-health workflow remains responsible for broad
repository hygiene. Reader-mode validation is a separate, composable gate so
repository classes can adopt it on their own schedule.
