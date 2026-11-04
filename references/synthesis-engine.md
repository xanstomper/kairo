# KAIRO — Synthesis Engine (technique classes · five-gene · operators · formats)

The forge's canon. Synthesis = aiming and compiling DOCUMENTED technique classes at
the family's findings — never inventing new ones.

## The five genes (every vector carries all five)

| Gene | Content | Source |
|---|---|---|
| TRIGGER | the source finding (what was observed) | ingested from family states |
| PRECONDITION | declared estate + access level | P0 record |
| PRIMITIVE | the technique class's mechanism | the class table |
| IMPACT-GATE | the exact proof condition | the class table |
| Δ | the documented-class adaptation for THIS target | synthesized; no Δ = no vector |

## Technique classes (8, keyword-classified at ingest)

| Class | Keywords | Flaw/Seam (3AM) | Craft class (undercroft) |
|---|---|---|---|
| BOUNDARY | org_id, tenant, workspace, plan, seat | 6/C | IDOR |
| REPLAY | webhook, replay, idempoten, callback, dedup | 5/B | STATE |
| STATEBYPASS | state, transition, workflow, approval | 5/B | STATE |
| MATH | refund, fee, rounding, precision, conversion, payout | 10/C | MATH |
| ENTITLEMENT | coupon, trial, promo, bonus, referral, claim | 1/C | IDOR |
| AUTHBYPASS | token, jwt, session, otp, auth, cookie | 1/C | OTHER |
| HWFLASH | firmware, uart, jtag, spi, flash, ota | 17/L | OTHER |
| HDRADIO | ble, rfid, nfc, radio, sdr, zigbee | 18/M | OTHER |

Unclassifiable findings default to AUTHBYPASS and are flagged for operator review.

## Synthesis operators (sibling variants)

| Op | Meaning | Example |
|---|---|---|
| SEAM | retarget the primitive across a different trust seam | boundary primitive on the API plane → same on the webhook plane |
| FAMILY | transpose to the sibling flaw family | scope-trust (6/C) → identifier-trust sibling (6/E) |
| ESCALATE | same primitive, higher-impact gate | read-proof → write-proof (still validation-only) |
| MIRROR | the same seam from the other side | client-trusts-server → server-trusts-client |
| TRANSPOSE | same primitive, different domain surface | checkout state bypass → booking state bypass |

Each op emits a SEPARATE vector with its own Δ. Ops are applied on request
(`synthesize --ops SEAM,FAMILY`), never silently.

## Compilation formats (per consumer)

**3AM** (`~/.redteam/learned-vectors.jsonl`, schema-true):
```json
{"flaw": 6, "seam": "C", "probe": "KAIRO SYNTH BOUNDARY :: fire the scoped request…", "confirmed_when": "foreign scope returns 200…"}
```
→ 3AM `promote --apply --verified` merges into the living matrix.

**UNDERCROFT** (campaign `undercroft-state.json` → `pocs`):
```json
{"finding": "SV-…-BOUNDARY", "request": "fire the scoped request…", "proof": "…", "class": "IDOR"}
```

**HolyShit** (`~/.redteam/synthesized-recipes.md`):
```markdown
### SV-…-BOUNDARY — BOUNDARY (source: undercroft)
- target: …
- attack: …
- proof: …
- Δ: …
```

**KAIRO** (hardware vectors stay in the plane ledger — its own synthesis domain).

## Hygiene

- Vectors are marked `distributed` after a supply drop — never double-shipped.
- EXHAUSTED findings never enter the queue (negatives don't synthesize).
- Every compiled attack inherits its source finding's P0 scope. No scope, no ship.