---
trigger: glob
globs:
  - "infrastructure/**/*"
  - "deploy/**/*"
  - "terraform/**/*"
  - "cdk/**/*"
  - "Dockerfile*"
  - "**/docker-compose*.yml"
  - ".github/workflows/**/*"
description: AWS and deployment safety rules for MuniAudit-AI.
---

# AWS / Deployment Rules

## Service boundary

Use the currently approved services in `ARCHITECTURE.md`.

Do not add a cloud service for convenience or appearance.

A new service requires:
- reason
- cost impact
- security impact
- failure impact
- architecture approval

## Current facts

For unfamiliar or fast-changing AWS capabilities, verify current official AWS documentation before implementation.

Never invent:
- service names
- resource properties
- SDK methods
- quotas
- pricing

## Cost safety

Prefer the smallest resource configuration that supports the hackathon workload.

Avoid accidental:
- GPU endpoints
- search clusters
- NAT gateways
- uncontrolled autoscaling
- duplicated databases
- unnecessary managed services

## Secrets

Never commit keys, passwords, tokens, private certificates, or credentials.

## IAM

Prefer least privilege. Do not use wildcards when a narrower resource/action policy is feasible.

## Deployment

Before deployment:
1. inspect Git state
2. validate infrastructure
3. run relevant application tests
4. run security checks
5. verify required configuration
6. verify intended AWS account/region
7. present deployment plan
8. obtain required human approval

After deployment:
- record deployed version
- run health/smoke tests
- inspect logs
- verify URL/endpoint
- record actual result

Never call a build "deployed" until runtime evidence exists.

## Infrastructure drift

Every resource used by code must exist in the approved deployment configuration.

If code starts depending on an unprovisioned resource, stop and reconcile the mismatch.

## Rollback

Preserve logs and deployed version before rollback. Use explicit non-destructive rollback procedures.
