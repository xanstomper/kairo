---
name: kairo
description: "Trigger `kairo`. The Synthesizer — turns every mandate's findings into compiled attacks and distributes them: 3AM vectors, undercroft crafts, holyshit recipes. Hardware is one of its domains."
version: 2.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, offensive-security, synthesizer, exploit-synthesis, hardware, universal, authorized-testing]
    related_skills: [holyshit-mode, 3am-shinjitsu, undercroft]
---

# KAIRO — The Synthesizer

The family's supply chain. HolyShit **finds**, 3AM **performs**, UNDERCROFT
**descends** into the target's own skin — KAIRO **synthesizes**: it ingests every
mandate's findings, classifies them into documented technique classes, fills the
five-gene breakdown (TRIGGER / PRECONDITION / PRIMITIVE / IMPACT-GATE / Δ), applies
the synthesis operators, and **compiles the attacks into each consumer's native
format** — 3AM matrix rows, undercroft craft entries, holyshit recipe cards — then
distributes them in one shot.

The circuit (回路) metaphor still holds: KAIRO is the wiring that carries the
family's power from where it's generated to where it's used.

## The Family Tree (roles)

```
        HolyShit!          3AM Shinjitsu        UNDERCROFT          KAIRO
        (FINDER)           (PERFORMER)          (DESCENT)           (SYNTHESIZER)
        finds what's       performs the         attacks the         ingests all findings →
        there · recipes    sweep · takeover     target's own skin   vectors → compiles
        · canon            · growth loop        · crafts PoCs       attacks for ALL of them
                    ╲                │                ╱                 ▲
                     └───────────────┴─────── findings ─────────────────┘
                                    KAIRO distributes compiled attacks back
        SHIKI (command — conducts assaults): orchestrates the family as one assault
```

## When to Use

Trigger `kairo` when ANY mandate has findings and the family needs attacks:

- undercroft confirmed seams / scan hits that should become 3AM matrix vectors
- 3AM teardowns or chains that need sibling-variant synthesis (SEAM/FAMILY/ESCALATE)
- hardware plane confirmations (its OWN domain — firmware/radio findings synthesize
  into flash/replay plans)
- any moment the operator says "turn what we found into attacks"

## Activation

Run the trigger sequence ONCE, then collect P0 via the agent's question feature:

```text
▸ KAIRO — SYNTHESIZER ONLINE
  ═══════════════════════════════════
  [ OK ] family states readable
  [ OK ] technique classes loaded
  [ OK ] forge ready
  ⚡ KAIRO ARMED · STATUS: SYNTHESIZING
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
  ─ waiting P0: target campaign · authorization
```

**P0 (clarify, zero documents):** which campaign/target · authorization. The
recorded declaration = the entire gate (family canon). KAIRO synthesizes ONLY for
declared estates; compiled attacks inherit their source finding's scope.

## The Synthesis Engine

### Technique classes (documented, family canon)

| Class | Matches findings about… | Primitive | Decisive test shape |
|---|---|---|---|
| BOUNDARY | org/tenant/workspace/plan/seat ids | scope-id trust (server reads id from request) | swapped-id request → foreign scope 200 |
| REPLAY | webhooks/callbacks/idempotency | same logical request accepted twice | replay N× → duplicate effect |
| STATEBYPASS | order/workflow transitions | out-of-order jumps accepted | fire N+2 before N+1 → undocumented state |
| MATH | refunds/fees/rounding/conversion | float/rounding drift accumulates | worst amount ×N → balance drifts |
| ENTITLEMENT | coupons/trials/promos/seats | grant-flow order creates unearned value | reorder/parallel-claim → duplicate grant |
| AUTHBYPASS | tokens/sessions/OTP | verify-order or entropy gap | forged/replayed credential accepted |
| HWFLASH | firmware/UART/JTAG/SPI/OTA | update/extract path unguarded | unsigned image accepted / keys read |
| HDRADIO | BLE/RFID/NFC/SDR/Zigbee | pairing/replay window on radio | replay accepted on owned device |

### Five-gene fill (family canon)

Every synthesized vector carries: TRIGGER (the source finding) · PRECONDITION
(declared estate + access) · PRIMITIVE (the class's mechanism) · IMPACT-GATE (its
proof condition) · Δ (the documented-class adaptation). **No Δ = no vector.**

### Synthesis operators

SEAM · FAMILY · ESCALATE · MIRROR · TRANSPOSE — sibling variants of any vector
(flaw×seam transpose, mirrored side, escalated primitive, cross-domain transpose).
Applied on request; each variant is a separate vector with its own Δ.

### Compilation + distribution (the supply drop)

`kairo distribute --target T` ( = compile --write):
1. **3AM** — appends `{flaw, seam, probe, confirmed_when}` rows to
   `~/.redteam/learned-vectors.jsonl` (schema-true; `KAIRO SYNTH` prefix);
   3AM `promote --apply --verified` merges them into the living matrix.
2. **UNDERCROFT** — appends craft entries (finding/request/proof/class) to the
   campaign's `undercroft-state.json`.
3. **HolyShit** — appends recipe cards (target/attack/proof/Δ) to
   `~/.redteam/synthesized-recipes.md`.
4. **KAIRO** — hardware vectors stay as plane-ledger probe plans (its own domain).
Vectors are marked `distributed` — never double-shipped.

## Walls (family canon, no exceptions)

- Documented-PoC adaptation only: technique CLASSES are the canon above; synthesis
  adapts them to the target's specifics. Novel weapon classes are never authored —
  synthesis never creates a technique, it aims and compiles known ones.
- Validation-only + NO-GAIN: compiled proofs are one decisive request/transaction,
  reversible, nothing of value kept.
- Hardware domain: lab-first, per-device opt-in, no destruction (unchanged).
- Zero documents at P0; scope inherits the source finding's declaration.

## The Dangerous Forge (v2.1.0)

- **`forge --target T --expand`** — ONE command: ingest → synthesize with **real op
  expansion** (each base vector spawns SEAM/FAMILY/ESCALATE sibling variants with
  their own Δ — 1 finding can become 4 attacks) → distribute to every consumer.
  Verified: 2 findings → 8 vectors → family armed.
- **`chain --target T [--write]`** — synthesizes multi-hop attack chains from the
  vector pool (entry → mid → value ordering by class), emits 3AM chain format
  (`BOUNDARY→REPLAY:TAKEOVER`), marks TAKEOVER-CANDIDATE until the final hop's
  decisive proof lands.
- **`armory --target T`** — the family arsenal at a glance: vectors by class,
  op-variant counts, chains, distribution state, pending warnings.
- Op variants are CONCRETE (not notes): each carries its own id, technique, proof,
  and Δ; ESCALATE variants stay validation-only (write/grant proof, reversed after).

## The forge rhythm

```
P0 → ingest (all family states for the target) → synthesize (class + five-gene + ops)
→ distribute (compile per consumer, one shot) → 3AM promote --apply --verified
→ the whole family now carries the new attacks
```

Negatives don't synthesize: only PROBED/CONFIRMED findings enter the queue;
EXHAUSTED seams are skipped at ingest.

## Tooling

`scripts/kairo.py` — stdlib CLI:
- `ingest --target <t>` — pull findings from undercroft/3AM/kairo states → synthesis queue
- `synthesize --target <t>` — findings → attack vectors (class-match + five-gene + ops)
- `compile --target <t> [--write]` — vectors → per-consumer artifacts (dry run default)
- `distribute --target <t>` — one-shot supply drop to all consumers
- `forge --target <t> [--expand]` — one command: ingest → synthesize (variants) → distribute
- `chain --target <t> [--hops N] [--write]` — multi-hop attack-chain synthesis
- `armory --target <t>` — the family arsenal status
- `targets add|list` / `phase` / `notes` / `report` — the hardware domain (unchanged)
- `verify` — self-check

State: `~/.redteam/campaigns/<target>/hardware-state.json` (+ `synthesis_queue`, `vectors`).

## Files

- `SKILL.md` — this doctrine
- `references/offensive-hardware-batteries.md` — the hardware synthesis domain's batteries
- `references/synthesis-engine.md` — technique classes, five-gene, operators, compilation formats
- `scripts/kairo.py` — ingest/synthesize/compile/distribute + hardware CLI
- `templates/hardware-state.json` — state starter (incl. synthesis blocks)

## Relations

- `/cyberbomb` — THE DISPATCHER (v1.0.0): the family's front door — any agent loads it first, states the goal, and the router sends the right mandate(s); `cyberbomb run` = the full pipeline, `cyberbomb verify` checks all six engines. The web's center.


- `barbican` — THE FIRST LAYER (v1.1.0): operator-protection synthesizer — vantage, identity, artifacts, trail, timeline, cleanup. Runs BEFORE every engagement; 3AM's pacing inherits its timeline layer; zero-document gate enforced by it.


- `holyshit-mode` — the finder: its findings and case canon feed the forge; KAIRO
  writes synthesized recipe cards back into family canon.
- `3am-shinjitsu` — the performer: KAIRO's compiled rows feed its matrix
  (`learn`/`promote`); its BLOCKED verdicts and chains feed KAIRO's queue.
- `undercroft` — the descent: its CONFIRMED seams are KAIRO's richest input;
  KAIRO writes compiled crafts back into its ledger.
- `shiki` — THE COMMAND (v2.0.0): `shiki assault` runs the whole family in order — barbican gate → holyshit find → undercroft descend → kairo forge+chain → war board + joint verdict.
- Family doctrine: HolyShit (finder) · 3AM (performer) · UNDERCROFT (descent) ·
  KAIRO (synthesizer) · SHIKI (command). Every mandate attacks; KAIRO arms them all.