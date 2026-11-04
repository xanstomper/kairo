#!/usr/bin/env python3
"""
KAIRO — offensive hardware/embedded engagement CLI. stdlib-only.

Tracks per-device inventory, plane coverage, findings, and the P5 report.
State: ~/.redteam/campaigns/<target>/hardware-state.json (survives sessions).

Commands:
  targets add   --name <device> --kind <router|panel|phone|radio|console|sensor|other>
                [--access <logical|serial|radio|physical|none>] [--desc "..."]
                [--target <campaign>]          register owned/declared hardware
  targets list  [--target <campaign>]
  phase         --target <t> --device <d> --plane 1-5 --status PROBED|N/A|CONFIRMED|EXHAUSTED
                [--test "<exact test>"] [--score N]     plane coverage + ledger
  notes         --target <t> --device <d> --add "<finding>" [--evidence "..."]
  report        --target <t> [--output F]                P5 deliverable
  verify        self-check: compile, subcommands, state schema

Exit codes: 0 ok · 2 usage/state error.
"""
import argparse
import json
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PLANES = {1: "firmware-storage", 2: "interfaces", 3: "radio-wireless",
          4: "protocol-logic", 5: "physical-supply"}
STATUSES = ("PROBED", "N/A", "CONFIRMED", "EXHAUSTED")
KINDS = ("router", "panel", "phone", "radio", "console", "sensor", "other")
ACCESS = ("logical", "serial", "radio", "physical", "none")


def state_path(target):
    return Path.home() / ".redteam" / "campaigns" / target / "hardware-state.json"


def load_state(target):
    p = state_path(target)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def save_state(target, state):
    p = state_path(target)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2) + "\n")


def cmd_targets(args):
    target = args.target or "kairo-workspace"
    st = load_state(target) or {"target": target, "devices": [], "ledger": [],
                                "created": datetime.now(timezone.utc).isoformat()}
    devs = st.setdefault("devices", [])
    if args.action == "add":
        if any(d.get("name") == args.name for d in devs):
            print(f"· device '{args.name}' already registered — skipping (anti-loop)")
            return 0
        if args.kind not in KINDS:
            print(f"✗ kind must be one of {KINDS}", file=sys.stderr)
            return 2
        if args.access not in ACCESS:
            print(f"✗ access must be one of {ACCESS}", file=sys.stderr)
            return 2
        devs.append({"name": args.name, "kind": args.kind, "access": args.access,
                     "desc": args.desc or "", "planes": {},
                     "added": datetime.now(timezone.utc).isoformat()})
        save_state(target, st)
        print(f"▸ registered device: {args.name} [{args.kind}, {args.access}] → "
              f"{state_path(target)}")
        return 0
    if args.action == "list":
        if not devs:
            print("· no devices registered")
            return 0
        for d in devs:
            covered = len(d.get("planes", {}))
            print(f"  {d['name']:24s} {d['kind']:8s} {d['access']:9s} "
                  f"planes {covered}/5  {d.get('desc', '')[:50]}")
        return 0
    return 2


def cmd_phase(args):
    st = load_state(args.target)
    if not st:
        print(f"✗ no state for '{args.target}' — add a target first", file=sys.stderr)
        return 2
    dev = next((d for d in st.get("devices", []) if d.get("name") == args.device), None)
    if not dev:
        print(f"✗ device '{args.device}' not registered", file=sys.stderr)
        return 2
    if args.plane not in PLANES or args.status not in STATUSES:
        print(f"✗ plane 1-5 ({list(PLANES.values())}) · status {STATUSES}", file=sys.stderr)
        return 2
    planes = dev.setdefault("planes", {})
    if planes.get(args.plane, {}).get("status") == "EXHAUSTED" and args.status != "EXHAUSTED":
        print("· plane already EXHAUSTED — re-probe only after a target change (canon)")
        return 0
    planes[args.plane] = {"status": args.status, "test": args.test or "",
                          "score": args.score or 0,
                          "at": datetime.now(timezone.utc).isoformat()}
    st.setdefault("ledger", []).append(
        {"device": args.device, "plane": args.plane, "plane_name": PLANES[args.plane],
         "status": args.status, "test": args.test or "",
         "at": datetime.now(timezone.utc).isoformat()})
    save_state(args.target, st)
    print(f"▸ {args.device} · {PLANES[args.plane]}: {args.status}"
          + (f" — {args.test[:90]}" if args.test else ""))
    return 0


def cmd_notes(args):
    st = load_state(args.target)
    if not st:
        print(f"✗ no state for '{args.target}'", file=sys.stderr)
        return 2
    dev = next((d for d in st.get("devices", []) if d.get("name") == args.device), None)
    if not dev:
        print(f"✗ device '{args.device}' not registered", file=sys.stderr)
        return 2
    notes = dev.setdefault("notes", [])
    notes.append({"finding": args.add, "evidence": args.evidence or "",
                  "at": datetime.now(timezone.utc).isoformat()})
    save_state(args.target, st)
    print(f"▸ note recorded on {args.device}: {args.add[:90]}")
    return 0


def cmd_report(args):
    st = load_state(args.target)
    if not st:
        print(f"✗ no state for '{args.target}'", file=sys.stderr)
        return 2
    out = args.output or f"{args.target}-kairo-report.md"
    L = [f"# KAIRO Report — {args.target}", ""]
    for d in st.get("devices", []):
        L.append(f"## {d['name']} ({d['kind']}, access: {d['access']})")
        if d.get("desc"):
            L.append(f"{d['desc']}")
        L.append("")
        planes = d.get("planes", {})
        if not planes:
            L.append("- no planes probed yet")
        for n in sorted(planes, key=int):
            p = planes[n]
            L.append(f"- **{PLANES[int(n)]}**: {p['status']}"
                     + (f" — {p['test']}" if p.get("test") else ""))
        for note in d.get("notes", []):
            L.append(f"- ⚑ {note['finding']}" + (f" (evidence: {note['evidence']})" if note.get("evidence") else ""))
        L.append("")
    Path(out).write_text("\n".join(L) + "\n")
    print(f"▸ report written: {out}")
    return 0


def cmd_verify(args):
    bad = []
    self = Path(__file__).resolve()
    r = subprocess.run([sys.executable, "-m", "py_compile", str(self)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        bad.append("compile")
    for want in ("targets", "phase", "notes", "report", "verify",
                 "ingest", "synthesize", "compile", "distribute"):
        out = subprocess.run([sys.executable, str(self), "--help"],
                             capture_output=True, text=True).stdout
        if want not in out:
            bad.append(f"subcommand {want}")
    tmpl = Path(__file__).resolve().parent.parent / "templates" / "hardware-state.json"
    if tmpl.exists():
        try:
            json.loads(tmpl.read_text())
        except Exception:
            bad.append("template json")
    for pl in (1, 2, 3, 4, 5):
        if pl not in PLANES:
            bad.append(f"plane {pl}")
    if bad:
        print(f"✗ KAIRO verify FAILED: {bad}")
        return 1
    print("✓ KAIRO verify: compile · subcommands · template · planes — ALL PASS")
    return 0


# ── v2.0.0 THE SYNTHESIZER: forge that arms the whole family ─────────────────

TECHNIQUE_CLASSES = {
    "BOUNDARY":    {"kw": ("org_id", "tenant", "workspace", "account_id", "plan", "seat"),
                    "primitive": "scope-id trust: server reads the id from the request, not the session",
                    "test": "fire the scoped request for {asset} with a swapped scope id (own ids)",
                    "proof": "foreign/unauthorized scope returns 200 or grants the resource",
                    "flaw": (6, "C"), "craft": "IDOR"},
    "REPLAY":      {"kw": ("webhook", "replay", "idempoten", "callback", "dedup"),
                    "primitive": "same logical request accepted twice (no idempotency gate)",
                    "test": "replay the captured {asset} request N×; diff effects",
                    "proof": "duplicate effect / distinct responses on identical request",
                    "flaw": (5, "B"), "craft": "STATE"},
    "STATEBYPASS": {"kw": ("state", "transition", "workflow", "order flow", "approval"),
                    "primitive": "transition accepts out-of-order jumps (guard skipped)",
                    "test": "fire the {asset} flow's later transition before its prerequisite",
                    "proof": "flow lands in an undocumented state",
                    "flaw": (5, "B"), "craft": "STATE"},
    "MATH":        {"kw": ("refund", "fee", "rounding", "precision", "conversion", "proration", "payout", "interest"),
                    "primitive": "float/rounding drift accumulates in the operator's favor",
                    "test": "run the worst crafted amount through {asset} ×N; reconcile",
                    "proof": "real balance drifts ≥1 smallest unit from exact math",
                    "flaw": (10, "C"), "craft": "MATH"},
    "ENTITLEMENT": {"kw": ("coupon", "trial", "promo", "bonus", "referral", "gift", "claim"),
                    "primitive": "grant flow order/inversion creates unearned value",
                    "test": "reorder/parallel-claim the {asset} grant flow (own account)",
                    "proof": "duplicate or unearned grant accepted",
                    "flaw": (1, "C"), "craft": "IDOR"},
    "AUTHBYPASS":  {"kw": ("token", "jwt", "session", "otp", "auth", "login", "cookie"),
                    "primitive": "token/session verify-order or entropy gap",
                    "test": "forge/replay the {asset} credential per documented class",
                    "proof": "unprivileged credential accepted as privileged",
                    "flaw": (1, "C"), "craft": "OTHER"},
    "HWFLASH":     {"kw": ("firmware", "uart", "jtag", "spi", "flash", "ota", "bootloader"),
                    "primitive": "device update/extract path lacks signature or rollback guard",
                    "test": "read/flash {asset} via the documented hardware path (lab, owned device)",
                    "proof": "unsigned image accepted / keys extracted read-only",
                    "flaw": (17, "L"), "craft": "OTHER"},
    "HDRADIO":     {"kw": ("ble", "rfid", "nfc", "radio", "sdr", "zigbee", "wifi"),
                    "primitive": "pairing/replay window on the radio plane",
                    "test": "observe then replay {asset} traffic per documented class (lab spectrum)",
                    "proof": "replay accepted / pairing bypassed on owned device",
                    "flaw": (18, "M"), "craft": "OTHER"},
}
SYNTH_OPS = ("SEAM", "FAMILY", "ESCALATE", "MIRROR", "TRANSPOSE")
CLASS_TO_FLAW_NAME = {6: "identifier-trust", 5: "state-machine-gaps", 10: "entropy/forge",
                      1: "validation-order", 17: "firmware-hardware", 18: "wireless-rf"}
CLASS_TO_SEAM_NAME = {"B": "client<->server-validation", "C": "auth<->backend-binding",
                      "L": "device-firmware", "M": "protocol-handshake"}


def _classify(finding_text):
    t = finding_text.lower()
    for cls, spec in TECHNIQUE_CLASSES.items():
        if any(k in t for k in spec["kw"]):
            return cls
    return "AUTHBYPASS"


def cmd_ingest(args):
    """Pull findings from ALL family states for this target into the synthesis queue."""
    camp = Path.home() / ".redteam" / "campaigns" / args.target
    st = load_state(args.target) or {
        "target": args.target, "devices": [], "ledger": [], "synthesis_queue": [],
        "vectors": [], "created": datetime.now(timezone.utc).isoformat()}
    queue = st.setdefault("synthesis_queue", [])
    known = {(q.get("source"), q.get("finding")) for q in queue}
    added = 0
    # UNDERCROFT state
    uc = camp / "undercroft-state.json"
    if uc.exists():
        u = json.loads(uc.read_text())
        for grp in ("code", "surface", "logic"):
            for x in u.get(grp, []):
                finding = x.get("seam") or x.get("endpoint") or x.get("asset") or ""
                proof = x.get("proof") or x.get("note") or ""
                status = x.get("status", "")
                if status == "EXHAUSTED":
                    continue
                key = ("undercroft", f"{finding}@{x.get('where', '')}")
                if finding and key not in known:
                    queue.append({"source": "undercroft", "finding": finding,
                                  "where": x.get("where") or x.get("file") or "",
                                  "proof": proof, "status": status,
                                  "at": datetime.now(timezone.utc).isoformat()})
                    known.add(key)
                    added += 1
    # 3AM state (exploit_intel block, if present)
    am = camp / "state.json"
    if am.exists():
        a = json.loads(am.read_text())
        ei = a.get("exploit_intel", {})
        for t in ei.get("teardowns", []):
            key = ("3am", str(t.get("cve") or t.get("id") or ""))
            if key[1] and key not in known:
                queue.append({"source": "3am", "finding": key[1],
                              "where": str(t.get("vector") or t.get("summary") or "")[:90],
                              "proof": "", "status": "PROBED",
                              "at": datetime.now(timezone.utc).isoformat()})
                known.add(key)
                added += 1
        for c in ei.get("chains", []):
            key = ("3am", str(c.get("chain") or ""))
            if key[1] and key not in known:
                queue.append({"source": "3am", "finding": key[1], "where": "chain",
                              "proof": str(c.get("status") or ""), "status": "PROBED",
                              "at": datetime.now(timezone.utc).isoformat()})
                known.add(key)
                added += 1
    # KAIRO hardware ledger (own domain)
    for e in st.get("ledger", []):
        if e.get("status") == "CONFIRMED":
            key = ("kairo", f"{e.get('device')}:{e.get('test', '')[:60]}")
            if key not in known:
                queue.append({"source": "kairo", "finding": f"{e.get('device')} plane {e.get('plane')}",
                              "where": e.get("test", "")[:90], "proof": "plane CONFIRMED",
                              "status": "CONFIRMED", "at": datetime.now(timezone.utc).isoformat()})
                known.add(key)
                added += 1
    save_state(args.target, st)
    print(f"▸ ingest: {added} new finding(s) into synthesis queue "
          f"({len(queue)} queued) — sources: undercroft · 3am · kairo")
    return 0


def cmd_synthesize(args):
    """Finding → attack vector: class-match, five-gene fill, sibling ops."""
    st = load_state(args.target)
    if not st:
        print(f"✗ no state for '{args.target}'", file=sys.stderr)
        return 2
    queue = st.get("synthesis_queue", [])
    if not queue:
        print("· queue empty — ingest first")
        return 0
    vectors = st.setdefault("vectors", [])
    known_v = {v.get("id") for v in vectors}
    n = 0
    for i, q in enumerate(queue):
        cls = _classify(q.get("finding", "") + " " + q.get("where", ""))
        spec = TECHNIQUE_CLASSES[cls]
        vid = f"SV-{args.target}-{i:03d}-{cls}"
        if vid in known_v:
            continue
        vec = {"id": vid, "source": q.get("source"), "class": cls,
               "target": q.get("finding"), "where": q.get("where", ""),
               "technique": spec["test"].format(asset=q.get("where") or q.get("finding")),
               "proof": spec["proof"], "delta": f"documented-class adaptation ({cls})",
               "gene": {"trigger": q.get("finding"), "precondition": "declared estate + access",
                        "primitive": spec["primitive"], "impact_gate": spec["proof"],
                        "delta": spec["test"].format(asset=q.get("where") or q.get("finding"))},
               "consumers": ["3am", "undercroft", "holyshit", "kairo"],
               "at": datetime.now(timezone.utc).isoformat()}
        vectors.append(vec)
        n += 1
        print(f"▸ {vid}: {cls} ← {q.get('source')}:{q.get('finding')}")
        print(f"    attack: {vec['technique'][:100]}")
        print(f"    proof:  {vec['proof'][:90]}")
        for op in SYNTH_OPS:
            if op in ("SEAM", "FAMILY"):
                print(f"    op/{op}: sibling variant available via flaw×seam transpose")
    save_state(args.target, st)
    print(f"▸ synthesized {n} attack vector(s) — compile next")
    return 0


def cmd_compile(args):
    """Vectors → per-consumer artifacts (3AM rows · undercroft crafts · recipes)."""
    st = load_state(args.target)
    if not st:
        print(f"✗ no state for '{args.target}'", file=sys.stderr)
        return 2
    vectors = st.get("vectors", [])
    if not vectors:
        print("· no vectors — synthesize first")
        return 0
    out3am, outuc, outrecipes = [], [], []
    for v in vectors:
        spec = TECHNIQUE_CLASSES[v["class"]]
        flaw, seam = spec["flaw"]
        out3am.append({"flaw": flaw, "seam": seam,
                       "probe": f"KAIRO SYNTH {v['class']} :: {v['technique'][:120]}",
                       "confirmed_when": v["proof"][:120]})
        outuc.append({"finding": v["id"], "request": v["technique"][:140],
                      "proof": v["proof"][:140], "class": spec["craft"]})
        outrecipes.append(f"### {v['id']} — {v['class']} (source: {v['source']})\n"
                          f"- target: {v['target']}\n- attack: {v['technique']}\n"
                          f"- proof: {v['proof']}\n- Δ: {v['delta']}\n")
    print(f"▸ compile: {len(vectors)} vector(s) →")
    print(f"    3AM:        {len(out3am)} learned-vector row(s)")
    print(f"    undercroft: {len(outuc)} craft entr(ies)")
    print(f"    holyshit:   {len(outrecipes)} recipe card(s)")
    print(f"    kairo:      hardware plans stay in the plane ledger")
    if args.write:
        learned = Path.home() / ".redteam" / "learned-vectors.jsonl"
        learned.parent.mkdir(parents=True, exist_ok=True)
        with learned.open("a") as f:
            for r in out3am:
                f.write(json.dumps(r) + "\n")
        print(f"    → wrote 3AM rows → {learned}")
        ucstate = Path.home() / ".redteam" / "campaigns" / args.target / "undercroft-state.json"
        if ucstate.exists():
            u = json.loads(ucstate.read_text())
            u.setdefault("pocs", []).extend(outuc)
            ucstate.write_text(json.dumps(u, indent=2) + "\n")
            print(f"    → wrote undercroft crafts → {ucstate}")
        recipes = Path.home() / ".redteam" / "synthesized-recipes.md"
        with recipes.open("a") as f:
            f.write("\n".join(outrecipes) + "\n")
        print(f"    → wrote recipe cards → {recipes}")
        for v in vectors:
            v["distributed"] = True
        save_state(args.target, st)
    else:
        print("    (dry run — add --write to distribute)")
    return 0


def cmd_distribute(args):
    """compile --write + confirm: the one-shot family supply drop."""
    args.write = True
    return cmd_compile(args)


def main():
    ap = argparse.ArgumentParser(description="KAIRO — family synthesizer + hardware CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ig = sub.add_parser("ingest", help="pull findings from undercroft/3am/kairo states")
    ig.add_argument("--target", required=True)
    sy = sub.add_parser("synthesize", help="findings → attack vectors (class + five-gene)")
    sy.add_argument("--target", required=True)
    cm = sub.add_parser("compile", help="vectors → per-consumer artifacts (dry run)")
    cm.add_argument("--target", required=True)
    cm.add_argument("--write", action="store_true", help="write to all consumers")
    ds = sub.add_parser("distribute", help="compile --write: one-shot family supply drop")
    ds.add_argument("--target", required=True)

    t = sub.add_parser("targets", help="register/list devices")
    t.add_argument("action", choices=("add", "list"))
    t.add_argument("--name")
    t.add_argument("--kind", choices=KINDS)
    t.add_argument("--access", choices=ACCESS)
    t.add_argument("--desc")
    t.add_argument("--target", default="kairo-workspace")

    p = sub.add_parser("phase", help="record plane coverage + ledger")
    p.add_argument("--target", required=True)
    p.add_argument("--device", required=True)
    p.add_argument("--plane", type=int, required=True)
    p.add_argument("--status", required=True, choices=STATUSES)
    p.add_argument("--test")
    p.add_argument("--score", type=int)

    n = sub.add_parser("notes", help="record a finding")
    n.add_argument("--target", required=True)
    n.add_argument("--device", required=True)
    n.add_argument("--add", required=True)
    n.add_argument("--evidence")

    r = sub.add_parser("report", help="P5 deliverable")
    r.add_argument("--target", required=True)
    r.add_argument("--output")

    v = sub.add_parser("verify", help="self-check")
    v.add_argument("--target")

    a = ap.parse_args()
    if a.cmd == "targets":
        return cmd_targets(a)
    if a.cmd == "phase":
        return cmd_phase(a)
    if a.cmd == "notes":
        return cmd_notes(a)
    if a.cmd == "report":
        return cmd_report(a)
    if a.cmd == "verify":
        return cmd_verify(a)
    if a.cmd == "ingest":
        return cmd_ingest(a)
    if a.cmd == "synthesize":
        return cmd_synthesize(a)
    if a.cmd == "compile":
        return cmd_compile(a)
    if a.cmd == "distribute":
        return cmd_distribute(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())