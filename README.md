[![ORGAN-I: Theory](https://img.shields.io/badge/ORGAN--I-Theory-1a237e?style=flat-square)](https://github.com/organvm-i-theoria) [![Language: Shell](https://img.shields.io/badge/language-Shell-89e051?style=flat-square)](https://github.com/organvm-i-theoria/system-governance-framework) [![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE) [![Version: 3.0.0](https://img.shields.io/badge/version-3.0.0-orange?style=flat-square)](VERSION)

# System Governance Framework

> Repository exposure is governed by the
> [public/private boundary](docs/REPOSITORY_EXPOSURE_BOUNDARY.md) and its
> [machine-readable disposition ledger](config/repository-exposure.inventory.json).

[![CI](https://github.com/organvm-i-theoria/system-governance-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-i-theoria/system-governance-framework/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-pending-lightgrey)](https://github.com/organvm-i-theoria/system-governance-framework)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/organvm-i-theoria/system-governance-framework/blob/main/LICENSE)
[![Organ I](https://img.shields.io/badge/Organ-I%20Theoria-8B5CF6)](https://github.com/organvm-i-theoria)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/organvm-i-theoria/system-governance-framework)
[![Shell](https://img.shields.io/badge/lang-Shell-informational)](https://github.com/organvm-i-theoria/system-governance-framework)


**A theoretical and operational framework for autonomous system governance -- formalising the principles by which a multi-organ creative-institutional system regulates itself without centralised authority.**

---

## Why "Governance Framework" belongs in a Theory organ

The word *governance* is often reduced to a checklist: branch protection rules, code owners, stale-issue bots. This repository refuses that reduction. It treats governance as a *first-order epistemological problem*: how does a distributed system of creative, commercial, and communal organs arrive at decisions that are coherent, auditable, and self-correcting -- without collapsing into a single bottleneck of human approval?

The name *System Governance Framework* therefore signals two commitments. First, *system*: governance here is not repository-local but cross-organ, spanning the full eight-organ architecture (ORGAN I-VIII) and its ~79 repositories across eight GitHub organisations. Second, *framework*: the deliverable is not a finished policy but a composable grammar of rules, presets, and automation primitives that downstream organs -- particularly ORGAN-IV (Taxis / Orchestration) -- can instantiate for their own contexts.

This dual nature -- theoretical analysis plus operational scaffolding -- is precisely why the repository lives in ORGAN-I (Theoria) rather than ORGAN-IV. The orchestration organ *consumes* governance primitives; the theory organ *derives* them.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Core Concepts](#core-concepts)
  - [Governance as Epistemology](#1-governance-as-epistemology)
  - [Framework-as-Code](#2-framework-as-code)
  - [Defence-in-Depth Decision Layering](#3-defence-in-depth-decision-layering)
  - [Progressive Configuration](#4-progressive-configuration)
  - [AI-Conductor Orchestration](#5-ai-conductor-orchestration)
- [Architecture](#architecture)
  - [Layered Architecture](#layered-architecture)
  - [Repository Structure](#repository-structure)
  - [Data Flow](#data-flow)
- [Installation and Usage](#installation-and-usage)
  - [Quick Start](#quick-start)
  - [Configuration Presets](#configuration-presets)
  - [Manual Installation](#manual-installation)
- [Examples](#examples)
- [Downstream Implementation](#downstream-implementation)
- [Validation](#validation)
- [Roadmap](#roadmap)
- [Cross-References](#cross-references)
- [Contributing](#contributing)
- [License](#license)
- [Author and Contact](#author-and-contact)

---

## Problem Statement

A multi-organ creative-institutional system faces a governance dilemma that no single tool can resolve. Consider what breaks without a formal governance framework:

**Consistency collapse.** When 79 repositories across eight GitHub organisations each invent their own security policies, issue templates, and CI pipelines, the result is a patchwork of incompatible standards. A contributor moving from an ORGAN-II art repository to an ORGAN-III commercial product encounters different review norms, different labelling schemes, different quality gates. Cognitive load multiplies; contribution rates decline.

**Silent drift.** Without centralised governance primitives, individual repos accumulate configuration debt. Dependabot schedules diverge. Pre-commit hooks cover different subsets of checks. Security scanning tools are present in some repos and absent in others. The system drifts from its own standards without any single actor noticing, because no single actor holds the complete picture.

**Decision bottlenecks.** In a system where a human maintainer is the sole governance authority (bus factor of one), every merge, every policy change, every security response routes through a single point of failure. Autonomous governance means encoding decision criteria into machine-readable rules so that routine decisions execute without human intervention, while exceptional decisions surface clearly for human judgement.

**Governance theatre.** The worst failure mode is the presence of governance artefacts -- badges, templates, policy documents -- without the enforcement machinery to make them real. A `SECURITY.md` that provides no contact mechanism, a Dependabot configuration that monitors ecosystems with no corresponding dependency files, a CodeQL matrix that scans languages the project does not contain -- these are not governance. They are its simulation.

This repository exists to solve all four problems simultaneously: to provide a *theoretically grounded, operationally enforced* governance layer that is composable across organs, self-validating, and honest about its own coverage.

---

## Core Concepts

### 1. Governance as Epistemology

Traditional governance frameworks ask "what rules should we enforce?" This framework begins one level deeper: "how does a distributed system *know* that it is governed?" The question is epistemological -- it concerns the conditions under which governance claims are justified.

The answer this framework provides is *machine-verifiable evidence*. Every governance claim (security scanned, dependencies current, code reviewed) must be backed by a workflow that produces an auditable artefact. If the workflow has not run, the claim does not hold. If the workflow has run but failed, the claim is explicitly falsified. There is no middle state where governance is merely *assumed*.

This principle directly descends from ORGAN-I's broader epistemological commitments: knowledge must be recursively self-validating, and no claim survives without a mechanism for its own refutation.

### 2. Framework-as-Code

Version 3.0.0 of the System Governance Framework introduces a paradigm shift from *template* (copy files, maintain locally) to *Framework-as-Code* (import remotely, configure declaratively). The distinction matters:

| Aspect | Template Model | Framework-as-Code |
|--------|---------------|-------------------|
| Adoption | Fork and copy `.github/` files | Run installer; 2 workflow files + 1 config |
| Updates | Manual merge of upstream changes | Bump a version pin |
| Customisation | Edit workflow YAML directly | Edit a single `governance.yml` |
| Maintenance burden | Full: you own every workflow | Minimal: central repo owns logic |
| Upgrade path | Complex merge conflicts | Change one semver string |

Under Framework-as-Code, a consumer repository contains only thin wrapper workflows that call reusable workflows hosted in this repository. All decision logic, scanning configuration, and enforcement rules live here and are version-pinned by the consumer. The theoretical implication is that governance becomes a *dependency* -- versioned, auditable, and upgradeable -- rather than an ambient property of the repository.

### 3. Defence-in-Depth Decision Layering

Governance decisions in this framework pass through five distinct layers, each operating independently so that no single-layer failure compromises the whole:

```
Layer 1  Repository Settings     Branch protection, required reviews, signed commits
Layer 2  Automated Scanning      CodeQL, Semgrep, secret scanning, dependency scanning
Layer 3  Pre-commit Hooks        12+ local checks (syntax, keys, large files, formatting)
Layer 4  Manual Review           CODEOWNERS-routed review, security expert review
Layer 5  Monitoring              Security advisories, audit logs, traffic analysis
```

The design is deliberately redundant. A secret that escapes Layer 3 (pre-commit) is caught by Layer 2 (GitHub secret scanning). A dependency vulnerability missed by Layer 2 (Dependabot) is surfaced by Layer 5 (security advisory monitoring). Each layer addresses a different class of governance failure at a different point in the development lifecycle.

### 4. Progressive Configuration

Not every repository needs enterprise-grade compliance automation. The framework therefore provides three configuration presets that map to different governance intensities:

- **Minimal** -- Basic CI, essential linting, no security scanning. For prototypes, personal experiments, early-stage work.
- **Standard** -- Full CI with coverage, CodeQL security scanning, pre-commit hooks, weekly Dependabot. The recommended default for team projects and open-source repositories.
- **Enterprise** -- All Standard features plus Semgrep, license compliance, OSSF Security Scorecard, SOC2/GDPR/HIPAA compliance workflows, daily dependency updates with auto-merge for patches.

The configuration is declared in a single `governance.yml` file. Feature toggles control which pipelines run. The framework reads this file at workflow execution time and conditionally enables or disables entire job graphs. The result is that a minimal-preset repository pays no CI cost for features it does not use.

### 5. AI-Conductor Orchestration

The `.github/agents/` directory contains an AI agent coordination framework: a coordinator configuration, task templates, and handoff protocols that enable multiple AI agents to collaborate on governance tasks (documentation generation, review automation, validation passes) without conflicting modifications.

This is not a theoretical curiosity. The eight-organ system operates on an AI-conductor model where AI generates volume and humans review for accuracy. The agent orchestration layer ensures that when multiple AI sessions work on the same repository -- common during sprint-based documentation pushes -- their work is traceable, non-overlapping, and auditable through standardised handoff headers and footers.

---

## Architecture

### Layered Architecture

```
Presentation     GitHub UI | CLI | IDE extensions
                      |
API Gateway      GitHub REST / GraphQL / Webhooks
                      |
Orchestration    GitHub Actions: event triggers, job scheduling, runners
                      |
Processing       Security | Quality | Compliance | Release | AI Orchestration
                      |
Storage          Git repo | Issues | Projects | Action artefacts
```

The framework requires zero additional infrastructure. Everything runs on GitHub-native services: Actions for compute, Issues for tracking, Security tab for vulnerability management, git history for audit trail. This zero-infrastructure constraint is itself a governance decision -- it eliminates the attack surface and operational burden of external services.

### Repository Structure

```
system-governance-framework/
  .github/
    workflows/           14 automation workflows (CI, CodeQL, Semgrep, release, stale, ...)
    actions/             Composite actions (language detection, config loading)
    agents/              AI coordinator, task templates, handoff protocols
    ISSUE_TEMPLATE/      Bug report, feature request, question (YAML forms)
    CODEOWNERS           Ownership rules for all paths
    SECURITY.md          Vulnerability reporting policy with response SLAs
    dependabot.yml       Automated dependency update schedule
  config/
    schema.json          JSON Schema for governance.yml validation
    presets/             minimal.yml | standard.yml | enterprise.yml
  scripts/
    install-framework.sh Shell installer for consumer repositories
  ARCHITECTURE.md        Full technical architecture documentation
  ECOSYSTEM.md           Ecosystem overview, integration patterns, deployment models
  COMPREHENSIVE_CRITIQUE.md  Self-assessment: blindspots, shatterpoints, evolution path
  ROADMAP.md             Strategic roadmap through v4.0
  GOVERNANCE_ANALYSIS.md Audit log of governance improvements
```

### Data Flow

A pull request triggers the following parallel execution:

1. **CI Pipeline** -- pre-commit hooks, language-specific tests, coverage upload
2. **Security Scans** -- CodeQL semantic analysis, Semgrep rule-based scanning, secret detection
3. **Quality Checks** -- Super-Linter multi-language linting, markdown link validation
4. **License Validation** -- SPDX compliance, dependency license audit
5. **Community Checks** -- PR template compliance, CODEOWNERS assignment

Results aggregate into the PR status. All checks must pass before merge is permitted. The framework distinguishes between *blocking* checks (CI, security) and *advisory* checks (linting, stale management) so that critical governance gates cannot be bypassed while non-critical feedback remains informational.

---

## Installation and Usage

### Quick Start

From the root of any git repository:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/organvm-i-theoria/system-governance-framework/main/scripts/install-framework.sh)
```

The installer creates three files:

```
.github/
  governance.yml              <- Your configuration (edit this)
  workflows/
    governance-ci.yml         <- Thin wrapper calling reusable CI workflow
    governance-security.yml   <- Thin wrapper calling reusable security workflow
```

Commit and push. Governance is now active.

### Configuration Presets

Edit `.github/governance.yml` to select a preset and toggle features:

```yaml
framework:
  version: "3.0.0"
  preset: "standard"        # minimal | standard | enterprise

project:
  languages: [python, shell]  # auto-detected if omitted

features:
  ci:
    enabled: true
    test-coverage: true
  security:
    enabled: true
    codeql: true
    dependency-scan: true
  quality:
    enabled: true
    linting: true
    pre-commit: true
```

The full configuration schema is defined in `config/schema.json` and supports 12 programming languages, framework-specific optimisations, Slack/Discord notification integrations, and compliance automation toggles.

### Manual Installation

If you prefer not to use the installer, create the wrapper workflows manually. Each workflow is a single `uses:` call to the corresponding reusable workflow in this repository, pinned to a version tag:

```yaml
jobs:
  ci:
    uses: organvm-i-theoria/system-governance-framework/.github/workflows/reusable-ci.yml@v3.0.0
    with:
      config-path: '.github/governance.yml'
    secrets: inherit
```

---

## Examples

### Scenario 1: New ORGAN-II art repository

A generative art project in ORGAN-II (Poiesis) needs lightweight governance -- linting for Python notebooks, basic CI, no compliance overhead.

```yaml
framework:
  version: "3.0.0"
  preset: "minimal"
project:
  languages: [python]
features:
  ci: { enabled: true, test-coverage: false }
  security: { enabled: false }
  quality: { enabled: true, linting: true, pre-commit: false }
```

Result: one CI job runs on push. No security scanning overhead. Pre-commit hooks are not enforced, respecting the creative workflow.

### Scenario 2: ORGAN-III commercial SaaS product

A revenue-generating SaaS application requires full security scanning, license compliance, and SOC2 audit trails.

```yaml
framework:
  version: "3.0.0"
  preset: "enterprise"
project:
  languages: [typescript, python]
features:
  security: { enabled: true, codeql: true, semgrep: true, license-check: true }
  compliance: { enabled: true, soc2: true }
```

Result: every PR triggers CodeQL, Semgrep, license validation, and SOC2 evidence collection. The governance overhead is justified by the commercial and regulatory context.

### Scenario 3: Cross-organ governance audit

ORGAN-IV (Taxis) needs to verify that all 79 repositories meet minimum governance standards. The framework's config schema provides a machine-readable contract: any repository whose `governance.yml` validates against `config/schema.json` and whose preset is at least `standard` meets the baseline. The audit reduces to a single API call per repository.

---

## Downstream Implementation

This repository is a **source** in the ORGAN dependency graph. The flow is:

```
ORGAN-I (Theoria)                  ORGAN-IV (Taxis)
system-governance-framework   -->  agentic-titan (orchestration engine)
                              -->  petasum-super-petasum (routing mesh)
                              -->  universal-node-network (node graph)
```

ORGAN-IV consumes the governance primitives defined here -- reusable workflows, config schema, preset definitions -- and operationalises them across all eight organs. ORGAN-IV does not *define* governance policy; it *enforces* the policies that ORGAN-I theorises.

No back-edges exist in this dependency. ORGAN-III (Ergon) commercial repositories may consume governance workflows, but ORGAN-I never depends on ORGAN-III. This constraint preserves the epistemological independence of the theory organ: governance principles are derived from first principles, not from commercial requirements.

---

## Validation

The framework validates itself through four mechanisms:

1. **Pre-commit suite** -- 12 hooks covering YAML/JSON/TOML syntax, private key detection, large file prevention, merge conflict markers, case-insensitive filename conflicts, broken symlinks, and executable shebang lines.
2. **CI pipeline** -- Runs on every push and PR. Validates all configuration files, executes pre-commit hooks in CI, and reports results as PR status checks.
3. **Self-critique** -- `COMPREHENSIVE_CRITIQUE.md` is an exhaustive 7.2/10 self-assessment identifying blindspots (Template Paradox, single-maintainer bus factor, scope creep), shatterpoints (missing config files, badge dishonesty), and a four-horizon evolution plan.
4. **Schema validation** -- `config/schema.json` provides JSON Schema Draft-07 validation for all `governance.yml` files, ensuring that consumer repositories declare valid configurations.

---

## Roadmap

| Version | Target | Key Deliverables |
|---------|--------|-----------------|
| v3.0.0 | Current | Framework-as-Code architecture, config system, installer CLI, reusable workflows |
| v3.1.0 | Q2 2026 | Rust/Ruby/PHP native support, framework-specific presets (Django, Rails), notification integrations |
| v3.2.0 | Q3 2026 | Advanced Semgrep rules, supply-chain security (SLSA), performance regression detection |
| v3.3.0 | Q4 2026 | SOC2 automation, GDPR compliance checking, audit trail generation |
| v4.0.0 | Q1 2027 | AI-assisted code review, intelligent test generation, auto-fix for security vulnerabilities |

The long-term vision is a **Governance-as-Code platform**: a declarative policy DSL, continuous compliance monitoring, and federated governance across multiple Git platforms (GitHub, GitLab, Bitbucket).

---

## Cross-References

| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Full technical architecture with component diagrams and data flow |
| [ECOSYSTEM.md](./docs/ECOSYSTEM.md) | Ecosystem overview, integration patterns, deployment models |
| [COMPREHENSIVE_CRITIQUE.md](./docs/COMPREHENSIVE_CRITIQUE.md) | Self-assessment: logic audit, rhetorical analysis, blindspots, evolution plan |
| [ROADMAP.md](./docs/ROADMAP.md) | Strategic roadmap with success metrics and risk management |
| [GOVERNANCE_ANALYSIS.md](./docs/GOVERNANCE_ANALYSIS.md) | Audit log of governance improvements and validation results |
| [PRODUCT_ARCHITECTURE.md](./docs/PRODUCT_ARCHITECTURE.md) | Framework-as-Code product design and business model |
| [config/schema.json](config/schema.json) | JSON Schema for governance.yml validation |
| [ORGAN-IV: agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan) | Downstream orchestration engine consuming governance primitives |

**Within the eight-organ system:**

| Organ | Organisation | Relationship |
|-------|-------------|-------------|
| I -- Theoria | [organvm-i-theoria](https://github.com/organvm-i-theoria) | **Home organ.** Governance is derived here as theory. |
| IV -- Taxis | [organvm-iv-taxis](https://github.com/organvm-iv-taxis) | **Primary consumer.** Enforces governance across all organs. |
| III -- Ergon | [organvm-iii-ergon](https://github.com/organvm-iii-ergon) | Commercial repos consume enterprise preset. |
| VIII -- Meta | [meta-organvm](https://github.com/meta-organvm) | Umbrella org; governance standards flow through meta. |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full contributor guide.

Key points:

- **Fork and branch** from `main`.
- **Pre-commit hooks** are enforced; run `pre-commit install` after cloning.
- **Conventional commits** preferred (`feat:`, `fix:`, `chore:`, `docs:`).
- **All PRs** require passing CI and at least one code-owner review.
- Open an issue or discussion before starting large changes.

---

## License

[MIT License](LICENSE). Framework is free and open-source.

---

## Author and Contact

**[@4444J99](https://github.com/4444J99)**

Part of [ORGAN-I: Theoria](https://github.com/organvm-i-theoria) -- the epistemological and theoretical foundation of the eight-organ creative-institutional system.

For security vulnerabilities, see [SECURITY.md](.github/SECURITY.md).
For support, open a [GitHub Discussion](https://github.com/organvm-i-theoria/system-governance-framework/discussions) or [Issue](https://github.com/organvm-i-theoria/system-governance-framework/issues).
