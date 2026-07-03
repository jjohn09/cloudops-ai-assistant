# Troubleshooting Guide: Private Endpoint & Connectivity Issues

## Symptom: Application cannot reach a PaaS resource after Private Endpoint migration

### Step 1 — Confirm DNS resolution
Private Endpoints rely on Private DNS Zones. Resolve the resource's FQDN
from a VM inside the VNet. If it resolves to the public IP instead of the
private IP (10.x.x.x range), the Private DNS Zone is either not linked to
the VNet or a conflicting DNS entry exists.

### Step 2 — Verify the Private Endpoint connection state
Check the Private Endpoint resource in the portal. The connection state
must show "Approved." A "Pending" state means the resource owner has not
yet approved the private link connection request.

### Step 3 — Check NSG and route table rules
Confirm no NSG on the subnet is blocking outbound traffic on the relevant
port, and that no custom route table is forcing traffic through a device
that doesn't have a path to the private endpoint's subnet.

### Step 4 — Validate Azure Firewall rules (if traffic transits the hub)
If the spoke routes egress through the hub firewall, confirm an application
or network rule explicitly allows the destination FQDN/IP and port.

## Symptom: Intermittent 503 errors during large data transfers

Usually indicates throttling on the destination storage account.
- Check Azure Monitor metrics for `Ingress`/`Egress` and `Transactions`
  against the account's scale limits.
- Reduce azcopy concurrency (`AZCOPY_CONCURRENCY_VALUE`) or split the
  transfer into smaller parallel jobs scoped by folder.

## Symptom: Users losing access after Conditional Access Policy rollout

- Confirm the user's group membership matches the CAP's assignment scope.
- Check Entra ID sign-in logs for the specific "Conditional Access" failure
  reason (e.g., blocked legacy auth, MFA not satisfied, device compliance
  failure).
- Validate the CAP is not unintentionally scoped to "All users" without an
  appropriate exclusion group for break-glass accounts.
