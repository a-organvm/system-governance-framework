# Repository Exposure Boundary

## Outcome

ORGANVM defaults reusable product code, specifications, examples, and documentation to public
open-source repositories. Credentials, personal data, client or partner records, unpublished
strategy, runtime state, raw agent/session history, and operational evidence stay in private
repositories or restricted stores.

Repository visibility is not a content-classification mechanism. A repository may become public
only after its current tree and complete reachable Git history pass the release gate below.

## Canonical split

When public product material and private operations share a repository, preserve the existing
repository as `<name>-operations-private` and publish a sanitized, fresh-history `<name>`
repository. The public repository owns product code, tests, generic fixtures, public docs,
governance, and release history from the split forward. The private companion owns customer or
partner records, operator notes, deployment state, evidence receipts, incident material, and
pre-split history.

`organvm/hospes` and `organvm/hospes-operations-private` are the reference implementation.

## Dispositions

| Disposition | Meaning | Permitted transition |
|---|---|---|
| `completed_split` | Public product and private operations are separated | Maintain both boundaries |
| `split_required` | Reusable product exists beside private or unreviewed history | Fresh-history public extraction |
| `public_candidate` | Likely reusable and low-risk, but not yet audited | Public only after the release gate |
| `keep_private` | Private material is the repository's purpose | Stay private; extract reusable modules separately |
| `archived_private` | Private historical or vendor-work artifact | Stay private or delete under a separate retention decision |

## Public release gate

Every visibility change or fresh-history publication requires one pull request or evidence record
showing all of the following:

1. **Purpose classification:** a named product boundary and repository owner.
2. **Tree audit:** no secrets, private keys, tokens, personal/contact data, client or partner data,
   private correspondence, raw session traces, machine-specific paths, or restricted datasets.
3. **History audit:** the same checks across every reachable commit, tag, branch selected for
   publication, and large-file pointer. If history cannot be proven clean, publish fresh history.
4. **Open-source surface:** approved license, notice where needed, README, security policy,
   contribution guide, code of conduct, generic fixtures, and reproducible tests.
5. **Dependency and provenance audit:** licenses and redistribution rights are compatible; vendored
   or generated assets identify their source.
6. **Verification:** tests and secret scanning pass, links and package metadata use the public
   location, and the private companion contains no public runtime dependency.
7. **Approval and receipt:** a maintainer approves the exact source commit, exclusions, destination,
   and resulting public commit. The receipt records hashes, not private contents.

Directly changing a private repository to public is allowed only when the complete-history audit
passes. Otherwise the required operation is a fresh-history split.

## Workstreams

### A — Public product extraction

Process `split_required` repositories in small product-family tranches. Freeze the source commit,
define exclusions, extract a clean tree, validate, publish, then redirect documentation and package
metadata. Do not move private issues, pull requests, discussions, Actions logs, or releases.

### B — Low-risk public candidates

Audit empty, skeletal, or clearly reusable repositories. Add the open-source surface and publish
only after history review. Empty does not automatically mean safe: repository settings, releases,
issues, and deleted history remain separate audit surfaces.

### C — Private operating systems

Keep repositories private when their purpose is personal state, relationship or engagement data,
application pipelines, browser/runtime/session state, security custody, or raw knowledge stores.
Extract genuinely reusable libraries into new public repositories instead of weakening the private
boundary.

### D — Archives and retention

Archived private repositories remain private by default. Archival, publication, and deletion are
separate decisions. A retention review may later delete redundant mirrors or publish a clean
derived artifact; neither happens as a side effect of this policy.

### E — Existing public estate

Existing public repositories remain public, but are not grandfathered out of secret, provenance,
license, and personal-data scanning. Any finding creates an incident response: contain current
exposure, rotate affected credentials, remove or replace sensitive material, and document the
limits of history rewriting and downstream clones.

## Operating order

1. Complete the content/history audit for one bounded tranche.
2. Review the exact split manifest and destinations.
3. Perform the publication or visibility changes.
4. Verify anonymously accessible clones, licenses, tests, and private-companion boundaries.
5. Record public/private commit hashes and close the tranche.

The machine-readable starting ledger is
[`config/repository-exposure.inventory.json`](../config/repository-exposure.inventory.json).

