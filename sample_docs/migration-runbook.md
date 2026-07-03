# Runbook: File Share Data Migration (Cross-Tenant)

## Scenario
Migrating large-scale Azure file share data (multi-terabyte, millions of
files) between two Azure AD tenants as part of a platform consolidation.

## Pre-Migration Checklist
1. Confirm Private Endpoint connectivity is established between source and
   destination tenants — public internet transfer is not permitted for
   migration workloads.
2. Validate destination storage account quotas and throughput limits can
   support the expected transfer volume.
3. Schedule an initial baseline copy window during low-traffic hours.
4. Notify application owners of the planned cutover window.

## Migration Steps
1. Use `azcopy` with the `--recursive` and `--preserve-smb-permissions=true`
   flags to perform the initial full copy.
2. Run a delta sync pass close to the cutover window to capture files
   changed since the baseline copy. Delta sync windows should be reduced
   through file-list filtering and parallelized job batches rather than a
   single large job.
3. Validate file counts and checksums between source and destination before
   declaring the migration complete.
4. Update application configuration/connection strings to point to the new
   storage endpoint.
5. Monitor Azure Monitor diagnostic logs for throttling (HTTP 503) events
   during the transfer and adjust concurrency settings if seen.

## Rollback Plan
- Source file share remains read-only but available for 72 hours
  post-cutover.
- If validation fails, revert application connection strings to the
  original source endpoint and re-run delta sync after root-causing the
  discrepancy.

## Common Issues
- **Slow delta sync**: usually caused by a single large azcopy job scanning
  the entire tree. Split into parallel jobs scoped by top-level folder.
- **Permission mismatches after copy**: confirm `--preserve-smb-permissions`
  was set on the initial job; permissions cannot be reliably backfilled
  after the fact.
