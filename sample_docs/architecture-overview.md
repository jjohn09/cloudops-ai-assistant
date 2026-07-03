# Azure Landing Zone – Architecture Overview

## Purpose
This document describes the target-state architecture for enterprise workload
migration into the corporate Azure landing zone.

## Identity & Access
- Microsoft Entra ID is the single identity provider for all workloads.
- Access is granted via role-based groups only; no direct user-to-resource
  role assignments are permitted.
- Conditional Access Policies (CAP) enforce MFA for all administrative roles
  and block legacy authentication protocols.
- Privileged Identity Management (PIM) is required for any Owner or
  Contributor role — standing access is not permitted for production
  subscriptions.

## Network Architecture
- All workloads connect through Private Endpoints; public network access is
  disabled by default on PaaS resources (Storage, SQL, Key Vault).
- Hub-and-spoke topology: a central hub VNet hosts the Azure Firewall,
  VPN/ExpressRoute gateway, and shared DNS resolver. Spoke VNets are peered
  to the hub and contain workload-specific resources.
- Application Gateway (WAF_v2 tier) terminates inbound HTTPS traffic and
  forwards to backend App Services over private link.
- Network Security Groups (NSGs) are applied at the subnet level using a
  least-privilege, deny-by-default rule set.

## Observability
- All resources emit diagnostic logs to a centralized Log Analytics
  Workspace (LAW).
- Azure Monitor alert rules are defined for CPU, memory, failed
  authentication attempts, and NSG deny events.
- Azure Policy enforces that diagnostic settings are automatically applied
  to any newly created resource in scope.

## Data Tier
- SQL Managed Instances and SQL Servers use Private Endpoints exclusively.
- Backups are encrypted at rest and replicated to a secondary region.
- Storage accounts use Private Endpoints and are configured with
  soft-delete and versioning enabled.

## Governance
- Resource tagging is mandatory: `environment`, `owner`, `costCenter`,
  `application`.
- Azure Policy initiatives block deployment of any resource that does not
  meet the tagging and network isolation baseline.
