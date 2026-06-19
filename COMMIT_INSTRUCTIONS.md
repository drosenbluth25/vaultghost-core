# VaultGhost Phase 0 Commit Instructions

Status: Phase 0 packet files have been added. CPAT Phase 1 remains UNRESOLVED until a hard-gate test run is executed, logs are preserved, hashes are generated, and the reproducibility report is filled.

## Files in this packet

- evidence/VAULTGHOST_EVIDENCE_LEDGER.json
- evidence/AI_OUTPUTS_QUARANTINE.json
- evidence/CLAIMS_REGISTER.json
- evidence/CPAT_PHASE1_STATUS.json
- evidence/PROPAGATION_RULES.md
- reports/VAULTGHOST_POSITIONING_STATEMENT.md
- reports/VAULTGHOST_REPRODUCIBILITY_REPORT_TEMPLATE.md

## Next local actions

1. Run the CPAT Phase 1 hard-gate commands in a local clone of the repository.
2. Preserve the git commit SHA, OS, Python version, dependency list, test log, test-log SHA-256 digest, and file manifest hash list under evidence/primary_artifacts/test_logs/.
3. Fill reports/VAULTGHOST_REPRODUCIBILITY_REPORT.md with the actual observed values.
4. Commit those generated logs and the filled report as a second, distinct commit.

Upgrade target after successful local run: PROVEN_WITHIN_LOCAL_EVIDENCE.

Upgrade scope: local machine, specific commit, specific environment, specific test command.

Patent/IP lane reminder: target non-provisional or PCT decision date is 2027-02-25. Treat this as a hard operational deadline and keep AI-generated praise out of the patent evidence lane.
