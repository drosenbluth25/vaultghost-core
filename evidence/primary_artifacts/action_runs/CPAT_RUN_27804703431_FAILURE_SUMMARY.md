# CPAT Phase 1 Hard-Gate Run Failure Summary

## Run
- GitHub Actions run: 27804703431
- Workflow: CPAT Phase 1 Hard Gate
- Job: hardgate
- Job ID: 82282074374
- Run commit: 7ced6f87fb4cc3e97158b0b6aa5802a40a80dfd5
- Result: failure

## Observed failure point
The workflow job completed with failure before the hard gate could execute.

Step conclusions:
- Checkout repository: success
- Set up Python: success
- Install dependencies: failure
- Run hard gate: skipped
- Hash evidence: failure
- Upload hard-gate evidence: success

## Artifact result
Artifact `cpat-phase1-hardgate-evidence` was created, but the downloaded artifact contained only the pending reproducibility report template. No pytest log was produced by this run because the hard-gate step was skipped after dependency installation failure.

## Root-cause classification
- evidence_status: failed_gate_attempt
- failure_class: dependency_install_blocked_test_execution
- default_action: patch_dependency_pin_and_rerun

## Remediation performed
The dependency pin was corrected from `rfc8785==1.0.0` to `rfc8785==0.1.4` in commit `f190a25fd98162cb0cc5fffb648cb30c9c20360e`.

The workflow was also hardened in commit `7066c862162be15de775ac9249e440e39f2fc01e` so dependency install logs and pytest logs are preserved before final pass/fail evaluation.

## CPAT status impact
This failed run does not upgrade CPAT Phase 1.

Current status remains:

```text
UNRESOLVED
```

Upgrade remains gated on a successful hard-gate run with preserved logs, hashes, and reproducibility report.
