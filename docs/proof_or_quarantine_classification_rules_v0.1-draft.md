# Proof-or-Quarantine Classification Rules v0.1‑draft

This document defines semantic classification rules for VaultGhost‑adjacent Proof‑or‑Quarantine events.
It must be read alongside the JSON schema.  JSON Schema validates event shape, but these rules govern
whether classifications are logically valid.  A stored `claim_bucket` is never authoritative; the
validator must recompute or validate the bucket against these rules.

## Non‑negotiable rule

A claim cannot be classified as **`verified`** unless the evidence required for that claim type
was resolved, hash‑bound or independently replayed, and adequate for the specific claim being
made.  The presence of an evidence pointer, confidence score, model assertion, UI screenshot, or
vague citation does **not** establish verification.

## Derived‑classification rule

The validator must recompute `claim_bucket` from:

* `claim_type`
* `evidence_status`
* `evidence_type`
* `evidence_quality`
* `resolver_status`
* `artifact_hash`
* `risk_flags`
* claim‑type minimums (see below)
* ruleset version

A stored `claim_bucket` is not authoritative unless it matches the validator's recomputed result.

## Bucket invariants

The buckets are ordered by strength: `verified` > `provisionally_verified` > `inferred` > `quarantined`.
If multiple rules apply, the most restrictive bucket wins.  Confidence scores cannot upgrade a claim
above the maximum permitted bucket allowed by evidence and risk flags.

* **Verified** requires `evidence_status` to be `artifact_hash_bound` or `independently_replayed` **and**
  adequate evidence for the claim type.
* **Provisionally verified** allows `evidence_status` of `pointer_format_valid` or `artifact_resolved` but
  not `none_provided` or `self_reported_pointer_only`.
* **Inferred** is appropriate when evidence is weak, partial, indirect, or suggestive but insufficient
  for proof.
* **Quarantined** is required when a claim is unsupported, contradicted, overbroad, high‑risk,
  self‑reported only, or backed by weak evidence for its claim type.

## Risk‑flag upper bounds

Certain risk flags cap the maximum permitted bucket.  These ceilings must be applied during
recomputation.

| Risk flag                                                    | Maximum bucket allowed |
|-------------------------------------------------------------|-----------------------|
| `unsupported_factual_claim`                                 | `quarantined`         |
| `contradicted_by_evidence`                                  | `quarantined`         |
| `technical_claim_requires_byte_level_check` without adequate byte evidence | `quarantined` |
| `weak_evidence_type`                                        | `inferred`            |
| `intent_claim`                                              | `inferred`            |
| `legal_conclusion` without authoritative legal record       | `inferred`            |
| `causal_overclaim`                                          | `inferred`            |
| `destructive_action` without approval evidence              | `quarantined`         |

## Claim‑type minimums for `verified`

The following table provides minimum evidence required for a claim to be considered verified.
Anything less must be downgraded.

| Claim type | Example                          | Minimum evidence for `verified` |
|-----------|----------------------------------|----------------------------------||
| technical | `All tests pass`                 | command, environment, exit code, and full hashed output log |
| technical | `No hidden Unicode`              | raw byte or codepoint scan of the exact file blob |
| conclusion| `PR is safe to merge`            | commit SHA, diff review, CI status, branch protection state, and risk review |
| intent    | `Party acted in bad faith`       | generally not wrapper‑verifiable; should remain inferred or quarantined |
| legal     | `Court filing exists`            | docket entry, filing artifact, court record, or attorney‑confirmed exhibit |

## Summary invariants

`classification_summary` is derived metadata.  The validator must recompute:

* `total_claims`
* `verified_count`
* `provisionally_verified_count`
* `inferred_count`
* `quarantined_count`

The event fails validation if stored summary counts do not match the claims array.

## Evidence invariants

* `resolver_status = resolved_and_hashed` requires `artifact_hash`.
* `resolver_status = replayed` requires replay metadata or an independent replay artifact reference.
* Evidence type `model_asserted_pointer` and evidence status `self_reported_pointer_only` do **not**
  count as verified evidence.
* `visual_ui` and `file_view` are weak evidence for byte‑level claims; they cannot support
  verification.
* A byte‑level technical claim cannot be verified without byte‑level evidence (e.g. `git_blob`,
  `hashed_artifact`, `full_command_output`, or `independent_replay`).
* A legal or procedural claim cannot be verified without an authoritative record, filed
  artifact, attorney‑confirmed exhibit, or equivalent source.

## Prompt disclosure rule

Use `prompt_disclosure` to support selective disclosure:

* `raw` requires `prompt_text`.
* `redacted` may include partial or sanitized prompt text.
* `hash_only` must omit raw prompt text.
* All modes require `prompt_hash`.

## Captured‑boundary rule

Each event must state what it does and does not capture.  A Proof‑or‑Quarantine event may prove that
the wrapper classified claims under a stated ruleset.  It does not, by itself, prove hidden model
reasoning, unstored source truth, repository state, legal validity, or external‑world facts unless
those artifacts were resolved, hash‑bound, and included within the event's evidence scope.