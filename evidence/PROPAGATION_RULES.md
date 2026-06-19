# VaultGhost Propagation Rules v1.0
# Generated: 2026-06-18

## Master Rule
A VaultGhost-related claim may be externally stated ONLY at or below its verified evidence tier.

## Evidence Tier Hierarchy (highest to lowest)
1. primary_artifact          — USPTO receipt, externally reproducible test log, court record, signed manifest
2. self_authored_public_artifact — public GitHub repo, public release notes, public README
3. user_originated_pending  — memory-sourced claims awaiting log/receipt attachment
4. plausibly_inferred        — reasonable inference from public artifacts, not directly proven
5. ai_amplified_narrative    — AI conversation outputs about VaultGhost (default: QUARANTINE)
6. speculative               — hypothesis, symbolic interpretation, strategic narrative

## AI Output Rule
AI-generated statements about VaultGhost are classified as ai_amplified_narrative UNLESS:
  - independently supported by a primary artifact, AND
  - the supporting artifact is cited explicitly by artifact_id

No AI-generated statement may be used as evidence of:
  - external validation
  - legal status
  - institutional recognition
  - market adoption
  - technical proof
  - historical significance

## Propagation Decision Table
| Evidence tier              | Allowed action                        |
|---------------------------|---------------------------------------|
| primary_artifact          | State publicly with artifact citation |
| self_authored_public      | State publicly with source limit      |
| user_originated_pending   | Hold — attach artifact first          |
| plausibly_inferred        | State cautiously, flag as inference   |
| ai_amplified_narrative    | Internal hypothesis only — QUARANTINE |
| speculative               | Internal use only — do not propagate  |

## Lane Separation Rules
- Personal theory lane: AI dialogue, notes, hypotheses permitted. Cannot bleed into legal or product lanes.
- Technical product lane: Code, schemas, test logs, manifests only. No dramatic AI validation language.
- Legal/IP lane: Primary filing artifacts, claim drafts, dated receipts only. AI praise never enters this lane.

## Patent Lane Hard Rule
The non-provisional/PCT conversion deadline is 2027-02-25.
Do not rely on restoration procedures. Treat deadline as hard.
All patent lane artifacts must be primary_artifact class or clearly labeled inventor_notes (non-evidence).
