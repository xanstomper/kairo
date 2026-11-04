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

Each op emits a SEPARATE, CONCRETE vector with its own id/technique/proof/Δ
(`--expand` or `forge --expand`). ESCALATE variants keep the no-gain wall: the
write/grant proof is executed once and reversed. Chains: entry-class vectors
(AUTHBYPASS/ENTITLEMENT) → mid (REPLAY/STATEBYPASS) → value (MATH) — emitted in
3AM chain format `A→B→C:TAKEOVER`, TAKEOVER-CANDIDATE until the final hop's
decisive proof lands.

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

## The five genes — formal table (enforced by `gene --check`)

| Gene | Meaning | Where it comes from | What breaks without it |
|---|---|---|---|
| TRIGGER | the source finding that justifies the vector | ingest (undercroft/3AM/kairo states) | a vector aimed at nothing — fabrication |
| PRECONDITION | declared estate + the access the finding proved | the source finding's declaration | out-of-scope execution |
| PRIMITIVE | the class's mechanism (why it works) | the technique-class canon | a ritual with no theory — cannot adapt |
| IMPACT-GATE | the decisive proof condition | the class's proof shape | no way to tell hit from miss |
| **Δ** | the documented-class adaptation to THIS target | the operator's aiming | novel-weapon authorship (the wall) |

`kairo gene --check --target T` prints the per-vector gene table and exits 1 if
ANY vector misses a gene. NO Δ = NO VECTOR is not advice — it's an exit code.

## The five operators — formal definitions

| Op | Transform | Example | Wall note |
|---|---|---|---|
| SEAM | same primitive, adjacent trust seam (C↔E, B↔F, L↔M) | BOUNDARY on auth↔backend → same swap at edgefn↔db | seam is canon; primitive unchanged |
| FAMILY | same primitive, sibling flaw family (6↔2, 5↔1, 10↔3, 17↔16, 18↔14) | identifier-trust → trust-in-client-params | flaw families are canon |
| ESCALATE | read→write proof class (accepted→granted, 200→grants) | replay proof → duplicate-grant proof | still validation-only, reversed after |
| MIRROR | invert the trust direction (the seam's other side) | server-trusts-client → client-trusts-server check | same test family, opposite side |
| TRANSPOSE | same primitive, different domain surface | web BOUNDARY → HWFLASH slot-id trust | see the domain map below |

Each op emits a CONCRETE variant: own id, technique, proof, Δ — never a note.

## The TRANSPOSE domain map (web → metal)

| Web class | Metal analogue | The transposed probe |
|---|---|---|
| BOUNDARY | HWFLASH | scope-id trust on update/extract paths — swapped slot ids (lab, owned device) |
| REPLAY | HDRADIO | pairing/replay window — capture + replay ack frames (lab spectrum) |
| STATEBYPASS | HWFLASH | out-of-order OTA/bootloader stages — N+2 before N+1 |
| MATH | HDRADIO | precision drift in radio counters — worst values ×N |
| ENTITLEMENT | HWFLASH | provisioning order — entitlement flag before its check |
| AUTHBYPASS | HDRADIO | pairing-material entropy — effective bits from captures |

`kairo crossdomain --target T --from web --to hardware|radio` registers each as a
PROBED plane-ledger plan — lab-first, owned devices, never auto-CONFIRMED, never
distributed.

## Chain anatomy (`chain`, validated by `chain --validate`)

- Hops play roles: **entry** (AUTHBYPASS/ENTITLEMENT, order 0) → **mid**
  (BOUNDARY/REPLAY/STATEBYPASS/HDRADIO, order 1–2) → **value** (MATH/HWFLASH, order 3).
- The final hop MUST carry an impact gate — its decisive proof is what flips the
  chain to TAKEOVER; without the gate the chain is a PARTIAL (a named gap).
- `chain --validate` checks: every hop id exists in the vector pool · ordering
  respects entry→mid→value · final hop gated. Any failure → exit 1 with the
  broken chain list. Chains are emitted in 3AM format (`A→B→C:TAKEOVER`).