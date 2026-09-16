# Migration from V3 to V4

V4 keeps V3 documents and adds a governance layer. Do not recreate or rewrite a version that has already been approved.

## Project currently in scoping or review

1. Copy the new templates into the appropriate folders.
2. Define `governance/GOVERNANCE.md`, `RACI.md`, and `APPROVAL_POLICY.json` with the user.
3. Initialize `APPROVAL_LEDGER.json` without inventing a past approval.
4. Continue the workflow, then create the first baseline after approval.

## Project already approved in V3

1. Keep the version and its history.
2. Record existing approval evidence only if it is retrievable and attributable; otherwise mark it as legacy, to be confirmed.
3. Create an initial migration baseline, identified as such in the changelog.
4. Verify the hashes and run the V4 validator.
5. Do not claim the baseline was signed or existed at the time of the V3 approval.

## Handoff

Create the package only for a `READY_FOR_IMPLEMENTATION` version with a verified baseline. A handoff already completed before V4 remains historical; do not retroactively fabricate an acknowledgment of receipt.

## Compatibility

V3 research, provenance, jurisdiction, import, and synchronization files remain unchanged. External integrations still require a preview and authorization at write time.
