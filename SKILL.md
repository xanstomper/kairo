---
name: kairo
description: "Trigger `kairo`. Offensive hardware, embedded, firmware, and wireless mandate — the metal branch of the HolyShit family."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, hardware, embedded, firmware, wireless, offensive-security, implant-analysis]
    related_skills: [holyshit-mode, 3am-shinjitsu, kernelcache-re, console-input-firmware]
---

# KAIRO (回路) — Offensive Hardware & Embedded Mandate

The metal branch of the HolyShit family tree. Where HolyShit is the book and 3AM
Shinjitsu is the engine, KAIRO is the touch: firmware, silicon, radios, and the
protocols that run on them. Software mandates read the wiring diagram; KAIRO opens
the enclosure.

## The Family Tree

```
                     ┌─────────────────────────────┐
                     │     THE HOLYSHIT FAMILY     │
                     │  (authorized assessment)    │
                     └─────────────┬───────────────┘
             ┌─────────────────────┼─────────────────────┐
             ▼                     ▼                     ▼
     HolyShit! (the book)   3AM Shinjitsu (the engine)   KAIRO (the metal)
     field-verified         speed · universal ·          firmware · silicon ·
     recipes · 65+ cases    synthesis · takeover ·        radios · embedded ·
     reliability stack      automation · growth loop      OT · implant analysis
```

- **HolyShit!** — offensive doctrine + session-verified recipes; the reliability stack
  (convergence, ledgers, case files).
- **3AM Shinjitsu (真実)** — Advanced Adversarial Assessment Mandate: the speed/factory
  branch. Universal coverage, synthesis engine, takeover layer, press-button loop.
- **KAIRO (回路, "circuit")** — THIS mandate: offensive security where electrons live.
  Everything not-a-webserver: firmware reverse engineering, embedded/RTOS exploitation,
  hardware interfaces (UART/JTAG/SWD/SPI/I²C), SDR/wireless (WiFi/BT/BLE/RFID/NFC),
  OT/ICS protocols (Modbus/DNP3/OPC-UA), update-path attacks, and implant/threat
  analysis on operator-owned devices.
- **Sibling canon:** kernelcache-re (iOS arm64e), console-input-firmware (game-input
  hardware), bloodbank-agy-asset-pipeline, swf-avm1-patching — all KAIRO-adjacent
  operational skills; load them when the target plane matches.

Each branch hunts COMPROMISE on authorized targets with evidence that survives.
Capability is universal across the tree; permission is never inferred.

## When to Use

Trigger `kairo` when the target has a body: routers, cameras, IoT, embedded panels,
game consoles, phones (jailbreak/RE), radios, BLE/WiFi/RFID badges, PLCs/RTUs,
firmware images, OTA update chains, UART/SWD/JTAG-accessible boards, or any
"smart" device that is operator-owned or explicitly operator-authorized.

Also use as the hardware lens inside 3AM engagements: when 3AM's U12 (Endpoint &
devices) or universal families 16–18 (mobile-device, firmware-hardware, wireless-rf)
confirm a signal, KAIRO is the depth module that takes it to control.

## Activation

Run the trigger sequence ONCE, then collect P0 via the agent's question feature:

```text
▸ KAIRO — HARDWARE MANDATE ARMED
  ═══════════════════════════════════
  [ OK ] silicon inventory loaded
  [ OK ] interface toolkit mapped
  [ OK ] radio stack online
  ⚡ KAIRO ARMED · STATUS: READY
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
  ─ waiting P0: device · access · objective
```

**P0 (clarify, zero documents):** device/asset list · access level (logical, serial,
radio, physical) · objective · authorization. The operator's recorded declaration is
the ENTIRE gate — no documents, manifests, or proofs are ever requested (OPSEC, family
canon). Declared estates are in scope on declaration. Physical-access work on a device
is opt-in per device via the P0 answer.

## The Five Planes (coverage contract)

Every engagement decomposes into the planes that apply to the device, each probed or
N/A'd with a concrete reason:

1. **Firmware & storage** — bootloader, flash/extraction (SPI/NAND/eMMC), filesystem,
   strings/secrets, update packages, signature verification, rollback.
2. **Interfaces** — UART (shell/panic logs), JTAG/SWD (debug unlock), SPI/I²C bus
   sniffing, USB (HID/DFU/device descriptors), crypto ICs (secure-element read).
3. **Radio & wireless** — WiFi (WPS/PMKID/rogue), BT/BLE (pairing, GATT, advertisement),
   RFID/NFC (cloning feasibility), SDR (ISR/rolling-code analysis), Zigbee/Z-Wave.
4. **Protocol & logic** — vendor protocols, MQTT/CoAP/modbus/DNP3/OPC-UA,
   cloud-device trust (device↔app↔cloud), update channels, licensing/dongles.
5. **Physical & supply** — chassis tamper evidence, debug headers, default credentials,
   secure-boot chain, supply-chain exposure (OEM/ODM images), implant analysis
   (on operator-owned devices only).

Same evidence standard as the family: CONFIRMED requires a minimal, non-destructive
proof; a compromise claimed without evidence is a violation, not a win.

## Decisive-test batteries

`references/offensive-hardware-batteries.md` — per-plane decisive tests with
confirmed-when conditions and the required kit. Load the plane file BEFORE probing it.
Every probe carries a score (family E/I/L/R/N, time-weighted per 3AM §14 when inside a
3AM engagement).

## Walls (family canon, no exceptions)

- **Documented-PoC adaptation only.** No novel weaponized exploit authoring, no
  malware, no destructive payload generation (§15 wall inherits from 3AM; kimiko-mode
  deleted references stay deleted).
- **Lab-first.** Radio/tx work, implant analysis, and brute force run against
  operator-owned hardware in the operator's own lab; never against third-party
  devices, networks, or spectrum beyond the declared estate.
- **No destruction.** Chip-off, decapping, and destructive extraction are documented
  as feasibility + revert plan, never executed without explicit per-device opt-in.
- **Validation-only compromise.** Prove control (shell, bus access, key read, replay
  feasibility), then STOP. Persistence/infection is never installed.
- **Physical/OT opt-in.** Physical access attacks execute only when the P0 record
  names the device and access level. Social engineering is never executed (family).

## Operating loop

```
P0 (clarify) → inventory (planes) → fingerprint (chips, firmware, radio) →
plane batteries → decisive test → CONFIRMED → control proof (read-only) →
chain to crown jewels (what does this device reach?) → report · ledger
```

Negatives are results: recorded with the exact test, never re-probed without a change.
Findings decay: re-verify firmware versions and radio state on re-entry.

## Tooling

`scripts/kairo.py` — stdlib CLI:
- `targets add --name <d> --kind <router|panel|phone|radio|console|sensor|other> --access <logical|serial|radio|physical|none>` — hardware inventory
- `phase --target <d> --plane <1-5> --status <PROBED|N/A|CONFIRMED|EXHAUSTED> --test "<exact test>"` — plane coverage + ledger
- `notes --target <d> --add "<finding>" [--evidence "..."]` — findings
- `report --target <d> [--output F]` — P5 deliverable
- `verify` — self-check (compile, subcommands, state schema)

State: `~/.redteam/campaigns/<target>/hardware-state.json` (campaign-style, survives
sessions).

## Files

- `SKILL.md` — this doctrine
- `references/offensive-hardware-batteries.md` — the five-plane decisive-test batteries
- `scripts/kairo.py` — inventory/phase/notes/report/verify CLI
- `templates/hardware-state.json` — per-target state starter

## Relations

- `holyshit-mode` — the book: offensive doctrine + session-verified recipes, normative
  by reference. Its case files name the devices that matter.
- `3am-shinjitsu` — the engine: universal coverage, synthesis matrix, takeover layer.
  KAIRO is 3AM's U12/16–18 depth module on the hardware plane.
- `kimiko-mode` — boundaries and artifact-first intake (normative).
- Sibling operational skills: `kernelcache-re`, `console-input-firmware`,
  `xbox-360-homebrew-porting`, `swf-avm1-patching` — load when the target plane
  matches the skill's domain.- `shukaku` — the harvester: KAIRO hardware-plane findings (device data, keys,
  firmware secrets) feed SHUKAKU's crown register. Tree: HolyShit (searcher) ·
  3AM (attacker) · SHUKAKU (harvester) · KAIRO (metal, support branch).
