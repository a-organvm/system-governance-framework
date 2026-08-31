# ADR-003: Kubernetes 1.37 Awareness and Adoption Gates

## Status

Accepted — do not migrate current products

## Date

2026-08-31

## Context

Kubernetes 1.37 shipped on 2026-08-26. Pod Certificates, Cluster Trust Bundles, Metrics API
definitions, Dynamic Resource Allocation improvements, and sandbox-creation status are relevant
to short-lived identity, trust distribution, accelerator health, and isolated agent workloads.

Those capabilities are substrate options, not a reason by themselves to add a cluster. No
verified workload profile or cost model currently shows that UCC, Styx, Hospes, or the control
plane needs Kubernetes. Adding it now would create control-plane, upgrade, observability,
security, and on-call work without a demonstrated product constraint.

## Decision

Keep UCC, Styx, Hospes, and near-term agent workers on the simplest managed deployment substrate
that meets their service-level and security requirements. Maintain Kubernetes 1.37 awareness,
but do not start a migration or platform build.

Reopen this decision only when at least one workload trigger and at least one economic or
security trigger below are evidenced, and every readiness prerequisite is satisfied.

## Workload triggers

At least one must be observed from production or a contracted deployment, not forecast alone:

1. Work must be scheduled across multiple compute nodes or failure domains, with either two or
   more accelerator classes or measurable device-health scheduling requirements.
2. Two or more tenants must share compute while requiring enforceable resource quotas,
   conflicting runtime dependencies, or isolation stronger than the current substrate provides.
3. Short-lived sandbox demand reaches 50 concurrent jobs at least weekly and the current
   substrate misses the documented queue-time or startup-time service objective.
4. Three or more independently deployed services require coordinated rollout, service
   discovery, policy enforcement, and autoscaling that the current platform cannot provide
   without product-specific glue.

## Economic triggers

At least one must be supported by a 90-day workload sample and a twelve-month fully loaded model:

1. Kubernetes lowers total cost by at least 20 percent after control-plane fees, observability,
   security tooling, incident response, upgrade work, and no less than 0.5 engineer-equivalent
   of platform operations are included.
2. A capacity or portability constraint on the current substrate blocks a contracted service
   objective or revenue opportunity whose twelve-month contribution exceeds twice the estimated
   migration and first-year operating cost.
3. Accelerator pooling or committed-compute economics yield a payback period of twelve months or
   less after migration, reliability, and staffing costs are included.

## Security and governance triggers

At least one must be a documented requirement that the current substrate cannot satisfy:

1. A client or regulator requires workload-bound, short-lived identity and centrally managed
   trust distribution equivalent to Pod Certificates and Cluster Trust Bundles.
2. Untrusted or customer-supplied code requires multi-tenant sandbox isolation, admission policy,
   network policy, auditable mutation controls, and bounded credentials in a shared compute pool.
3. Accelerator access requires device-class allocation, health-aware scheduling, or isolation
   controls for which Dynamic Resource Allocation is the selected and tested mechanism.

## Readiness prerequisites

All are required before an adoption proposal can be accepted:

- a named platform owner and on-call path;
- a 30-day workload profile and 90-day cost sample;
- explicit availability, queue-time, startup-time, recovery-time, and recovery-point objectives;
- a threat model and workload-identity design;
- a proof of concept with failure, upgrade, and rollback tests;
- an exit plan that preserves application portability and data recovery;
- a decision comparing a managed Kubernetes service with simpler managed alternatives.

## Consequences

### Positive

- Platform complexity is tied to measured product needs and buyer requirements.
- Kubernetes-specific identity, trust, sandbox, and device features remain available when they
  solve an evidenced constraint.
- UCC, Styx, and Hospes avoid an infrastructure migration that does not improve present product
  outcomes.

### Negative

- Some Kubernetes-specific operational learning is deferred.
- A later adoption, if triggered, will require a bounded proof of concept before migration.

## Review protocol

Review this ADR quarterly or when a trigger is evidenced. The reviewer must attach the workload
sample, cost model, security requirement, named owner, and proof-of-concept plan. A new ADR must
supersede this one before any production migration begins.

## References

- [Kubernetes 1.37 release, 2026-08-26](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/)
- [GitHub AI platform governance evidence inventory](../AI_PLATFORM_GOVERNANCE.md)
