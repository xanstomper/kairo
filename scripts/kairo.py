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
        for n in sorted(planes):
            p = planes[n]
            L.append(f"- **{PLANES[n]}**: {p['status']}"
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
    for want in ("targets", "phase", "notes", "report", "verify"):
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


def main():
    ap = argparse.ArgumentParser(description="KAIRO — offensive hardware engagement CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

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
    return 2


if __name__ == "__main__":
    sys.exit(main())