# Migration V1 to V5

[Lire en français](MIGRATION_V1_TO_V5.fr.md)

This migration adds controls without invalidating historical documents. Never retroactively fabricate an approval, a provenance entry, a baseline, or a receipt.

## From V1

1. Keep `MEMORY.md`, `PROJECT.md`, requirements, tasks, decisions, research, risks, and the changelog.
2. Add the V2 profile and project type, then run the validator to reveal gaps without silently fixing them.
3. Add structured provenance only for retrievable sources.
4. Declare only the integrations and jurisdictions that actually apply.
5. Install V4 governance with confirmed roles, RACI, and gate rules.
6. Create a migration baseline of the current state; do not claim it existed at the time of the original approval.

## From V2

Keep profiles, extensions, conflicts, and identifiers. Add V3 integration or provenance artifacts only when they are used, then apply V4 governance.

## From V3

Follow `MIGRATION_V3_TO_V4.md`, then adopt the V5 policies for untrusted content, localization, and evaluation.

## From V4

Update the plugin without modifying project baselines. Add the V5 policies, audit tools, and the new evaluation suite. V4 approvals remain valid for their exact version and hash.

## Verification

Run the local tests, the specification validator, the evaluation validator, the security audit, and native plugin validation. Projects marked `READY_FOR_IMPLEMENTATION` must continue to satisfy their V4 gates.

## Rollback

Keep the archive of the previous version. Reverting to an earlier plugin must never delete V3/V4/V5 artifacts; older versions may ignore them, but must not rewrite them.
