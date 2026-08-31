# AI Platform Governance Evidence Inventory

## Outcome

This control pack turns GitHub AI and repository-platform settings into an evidence-backed
operating record. It does not infer that a setting is disabled, enabled, or compliant merely
because a repository integration cannot see it.

The machine-readable record is
[`config/ai-platform-governance.inventory.json`](../config/ai-platform-governance.inventory.json).
Validate it with:

```bash
python scripts/validate_ai_platform_governance.py
```

## Control boundary

| Control | Automation can establish | Admin evidence still required |
|---|---|---|
| Copilot seats and billing | Vendor change announcement | Assigned, active, inactive, and cancellation counts; payment state |
| Model permissions | Global-policy announcement | Effective allow/deny set, exceptions, test of one allow and one deny |
| Conversation retention | Retention-change announcement | Effective workspace behavior, deletion/export path, data-class policy |
| Code review default | Default-change announcement | Effective mode, overrides, sampled quality and usage impact |
| Spend controls | Presence or absence of a versioned record | Budget, alert threshold, limit type, recipients, exception approver |
| Repository rulesets | Repository endpoint response | Effective organization rules and bypass actors |
| Branch protection | Successful API response, when authorized | Admin export when the integration returns 403 |

`partial`, `announcement_only`, `needs_admin_verification`, and `blocked` are unresolved states.
Every unresolved control must name an owner role, next action, evidence source, and review date.

## Initial findings on 2026-08-31

- Organization-level controls cover all ten organization installations: `a-organvm`,
  `organvm-i-theoria`, `organvm-ii-poiesis`, `organvm-iii-ergon`, `organvm-iv-taxis`,
  `organvm-v-logos`, `organvm-vi-koinonia`, `organvm-vii-kerygma`, `meta-organvm`, and
  `organvm`.
- `4444J99` is a personal account installation, not an organization. Its plan, model,
  retention, review, and spend boundaries are tracked separately under `GH-PERSONAL-*`; personal
  settings must not be treated as organization policy.
- The repository ruleset endpoints for `system-governance-framework`,
  `orchestration-start-here`, and `organvm-engine` each returned an empty array. This is a
  narrow API observation, not evidence that organization-level rules are absent.
- The GitHub App received `403 Resource not accessible by integration` for all three
  main-branch protection reads. Those controls remain blocked pending an organization-owner
  export.
- Copilot seat, model, retention, review-default, and spend facts require organization-admin
  verification. Vendor announcements are recorded as announcements, not as effective policy.

## Admin verification packet

Complete one packet for each of the ten organizations in scope. Complete the separate
`GH-PERSONAL-*` owner-verification packet for `4444J99`; do not fold personal subscription or
usage facts into organization totals.

1. Export aggregate seat counts: assigned, active in the last 30 days, inactive, pending
   cancellation, and unassigned capacity.
2. Record the effective model allowlist, denylist, exception path, owner, and timestamp. Test
   one permitted and one denied model from a managed seat.
3. Record conversation-history retention, export, deletion, legal-hold, and permitted
   data-class rules.
4. Record the effective code-review mode and overrides. Sample ten representative pull
   requests for usage, useful findings, noise, and escaped defects before fixing a fleet-wide
   default.
5. Record monthly budget, warning threshold, hard or soft limit, alert recipients,
   premium-request policy, and exception approver.
6. Export effective repository rulesets and branch protection for the control repositories.
   Confirm required checks, deletion and force-push protection, bypass actors, and scope.

Seat-level identities, billing exports, and private policy screenshots must remain in a
restricted store. Commit only aggregate values, timestamps, a content digest, and a reference
to the restricted artifact.

## Ownership and cadence

| Responsibility | Role |
|---|---|
| Accountable | GitHub organization owner |
| Responsible | Platform engineering owner |
| Consulted | Product and repository owners |
| Evidence custodian | Governance maintainer |

Review weekly while the billing and policy rollout is changing. Move to monthly after every
control has a verified baseline. Any change in seats, model policy, retention, review mode,
budgets, rulesets, or branch protection requires a dated inventory update through pull request.

## Decision rules

- Do not expand agent seats until `GH-AI-001` and `GH-AI-005` have verified baselines.
- Do not claim centrally governed model access until `GH-AI-002` has an effective-policy export
  and allow/deny test evidence.
- Do not put client, resident, filing, or account data into durable chat history until
  `GH-AI-003` has a documented data-class rule and deletion path.
- Do not apply a fleet-wide review default until `GH-AI-004` has a ten-pull-request quality and
  usage sample.
- Coordinate branch-protection expansion with
  [`organvm-engine#61`](https://github.com/organvm/organvm-engine/issues/61); do not treat a 403
  read as proof of either protection or exposure.

## Source changes tracked

- [Copilot policies and billing announcement, 2026-08-28](https://github.blog/changelog/2026-08-28-upcoming-changes-to-github-copilot-policies-and-billing/)
- [Global model policy generally available, 2026-08-26](https://github.blog/changelog/2026-08-26-global-model-policy-generally-available/)
