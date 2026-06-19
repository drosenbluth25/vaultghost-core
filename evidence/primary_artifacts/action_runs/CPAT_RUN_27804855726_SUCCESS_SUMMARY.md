# CPAT Phase 1 Hard-Gate Run Success Summary

## Run
- GitHub Actions run: 27804855726
- Workflow: CPAT Phase 1 Hard Gate
- Job: hardgate
- Job ID: 82282652062
- Run commit: 5e145c15a139839447b3941c5ad23719a58abd54
- Result: success

## Step conclusions
- Checkout repository: success
- Set up Python: success
- Install dependencies and preserve install log: success
- Run hard gate and preserve pytest log: success
- Hash evidence: success
- Upload hard-gate evidence: success
- Finalize hard-gate result: success

## Artifact
- Artifact name: cpat-phase1-hardgate-evidence
- Artifact ID: 7741542848
- Artifact digest: sha256:a8d75859a8dd50de0e7bf083d0071643a533c5b94de475d747c767917b6c9ea7
- Artifact size: 6368 bytes
- Artifact created: 2026-06-19T04:12:35Z
- Artifact expires: 2026-09-17T04:12:27Z

## Preserved evidence files
- evidence/primary_artifacts/test_logs/run_commit.txt
- evidence/primary_artifacts/test_logs/os.txt
- evidence/primary_artifacts/test_logs/python_version.txt
- evidence/primary_artifacts/test_logs/pip_freeze.txt
- evidence/primary_artifacts/test_logs/pip_install.log
- evidence/primary_artifacts/test_logs/pip_install_exit_code.txt
- evidence/primary_artifacts/test_logs/test_run.log
- evidence/primary_artifacts/test_logs/test_exit_code.txt
- evidence/primary_artifacts/test_logs/test_run.sha256
- evidence/primary_artifacts/test_logs/file_manifest.sha256

## Observed result
```text
........                                                                 [100%]
8 passed in 0.04s
```

## Hash
```text
54d62a0149f447ee2867b9e102287fade45e0a057ff3b969489678c98884e9ae  evidence/primary_artifacts/test_logs/pytest_run.log
```

## CPAT status impact
This run upgrades CPAT Phase 1 within bounded CI evidence scope.

Status:

```text
PROVEN_WITHIN_CI_EVIDENCE
```

Scope:

```text
GitHub Actions hosted runner, specific commit, specific dependency set, specific pytest command, preserved logs and SHA-256 digest.
```

## What this does not prove
- Independent external validation
- Production readiness
- Security assurance
- Legal protectability
- Market adoption
- Patentability
