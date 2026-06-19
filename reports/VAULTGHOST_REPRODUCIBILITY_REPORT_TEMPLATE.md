# VaultGhost Reproducibility Report — TEMPLATE
# Status: PENDING — fill in after hard-gate run

## Environment
- Git commit SHA: [INSERT: git rev-parse HEAD]
- OS: [INSERT]
- Python version: [INSERT: python --version]
- Dependency lock: [see pip_freeze.txt]

## Command
```
pytest -q
```

## Result
- Tests passing: [N]
- Tests failing: [M]
- Full log: evidence/primary_artifacts/test_logs/pytest_run.log
- Log SHA-256: [INSERT from pytest_run.sha256]

## Bounded Claim
At commit [SHA], on environment [OS/Python/deps], command `pytest -q`
produced [N] passing tests and [M] failures.
The full terminal log and SHA-256 digest are preserved in evidence/primary_artifacts/test_logs/.

## What This Proves
- The test suite executed on this machine at this commit.
- [N] tests passed under the conditions listed above.

## What This Does NOT Prove
- Independent external validation
- Production readiness
- Security assurance
- Legal protectability
- Market adoption
