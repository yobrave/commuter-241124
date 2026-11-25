"""Charm the Commuter: invented-city forecast line, gate + export."""
import json
import os
import pathlib

LIMIT_CHARS = 140
ROOT = pathlib.Path(__file__).parent
MARK = "cmm4-city-forecast-r4"


def read_entry():
    return (ROOT / "entry.txt").read_text(encoding="utf-8").strip()


def passes_gate(n):
    return n in range(1, LIMIT_CHARS + 1)


def export(text):
    dest = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out")) / "entry.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text + "\n", encoding="utf-8", newline="\n")


def main():
    line = read_entry()
    n = len(line)
    if not passes_gate(n):
        print(json.dumps({"verdict": "rejected", "chars": n}))
        return 1
    export(line)
    print(json.dumps({"verdict": "accepted", "chars": n, "mark": MARK, "limit": LIMIT_CHARS}))
    return 0


raise SystemExit(main())
