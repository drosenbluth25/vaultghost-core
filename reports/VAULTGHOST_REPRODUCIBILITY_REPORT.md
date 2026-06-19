# VaultGhost Reproducibility Report
# Status: GENERATED FROM GITHUB ACTIONS HARD-GATE RUN

## Run Identity
- GitHub Actions run: 27804855726
- Workflow: CPAT Phase 1 Hard Gate
- Job: hardgate
- Job ID: 82282652062
- Artifact ID: 7741542848
- Artifact digest: sha256:a8d75859a8dd50de0e7bf083d0071643a533c5b94de475d747c767917b6c9ea7

## Environment
- Git commit SHA: 5e145c15a139839447b3941c5ad23719a58abd54
- OS: Linux runnervm7b5n9 6.17.0-1018-azure #18~24.04.1-Ubuntu SMP Thu May 28 16:39:11 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
- Python version: Python 3.11.15
- Dependency lock: evidence/primary_artifacts/test_logs/pip_freeze.txt

## Command
```bash
pytest -q
```

## Result
- Tests passing: 8
- Tests failing: 0
- Pytest exit code: 0
- Pip install exit code: 0
- Full log: evidence/primary_artifacts/test_logs/test_run.log
- Log SHA-256: 54d62a0149f447ee2867b9e102287fade45e0a057ff3b969489678c98884e9ae

## Bounded Claim
At commit `5e145c15a139839447b3941c5ad23719a58abd54`, on the GitHub Actions hosted runner environment recorded above, command `pytest -q` produced 8 passing tests and 0 failures. The terminal log and SHA-256 digest are preserved in `evidence/primary_artifacts/test_logs/`.

## What This Proves
- The test suite executed successfully on the GitHub Actions runner at the commit listed above.
- The observed test result is preserved in a log file with a SHA-256 digest.
- CPAT Phase 1 has passed within the bounded CI evidence scope defined by this report.

## What This Does NOT Prove
- Independent external validation
- Production readiness
- Security assurance
- Legal protectability
- Market adoption
- Patentability
