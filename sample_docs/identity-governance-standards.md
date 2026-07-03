# Operational Standard: Identity & Access Governance

## Group Structure
- Access groups follow the naming convention:
  `az-<subscription>-<role>-<environment>` (e.g., `az-prod-contributor-eastus`).
- Groups must map to a single Azure RBAC role at a single scope. Nesting
  multiple roles inside one group is not permitted, as it makes access
  reviews unreliable.

## Access Reviews
- All privileged groups undergo a quarterly access review owned by the
  resource/application owner.
- Reviewers must provide a justification for continued access; unreviewed
  members are automatically removed after the review period closes.
- Stale or duplicate groups identified during review consolidation should
  be merged or removed to keep the total group count manageable and
  auditable.

## Privileged Identity Management (PIM)
- Owner and Contributor roles on production subscriptions must be
  PIM-eligible, not permanently assigned.
- Activation requires justification text and is time-boxed to a maximum of
  8 hours.
- PIM activation triggers an alert to the security operations channel for
  visibility.

## Service Accounts
- Service accounts must not be members of interactive-sign-in-capable
  groups.
- Credentials for service accounts are stored in Key Vault and rotated on a
  90-day cycle at minimum.
- Any service account requiring Owner-level access requires a documented
  exception approved by the security team.

## Conditional Access Baseline
- MFA is required for all users accessing management endpoints.
- Legacy authentication protocols are blocked tenant-wide.
- Break-glass emergency access accounts are excluded from Conditional
  Access policies and monitored separately with alerting on any sign-in
  activity.
