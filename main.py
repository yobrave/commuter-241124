"""Commuter forecast entry: audit the invented-city line, publish to gate output."""
import json
import os
import sys

FORECAST = "entry.txt"
SKY_CAP = 140


def audit_city(text: str) -> dict:
    clean = " ".join(text.split())
    return {
        "glyph_budget": len(clean),
        "kilo_bytes": len(text.encode("utf-8")),
        "fits_kiosk": len(clean) <= SKY_CAP,
        "not_vacant": bool(clean),
        "mono_line": "\n" not in text.strip() and len(text.encode("utf-8")) < SKY_CAP + 2,
    }


def publish() -> int:
    with open(FORECAST, encoding="utf-8") as handle:
        raw = handle.read()
    stamp = audit_city(raw)
    stamp["greenlit"] = stamp["fits_kiosk"] and stamp["not_vacant"] and stamp["mono_line"]
    kiosk = os.environ.get("MAKEFUN_OUTPUT_DIR", "kiosk")
    os.makedirs(kiosk, exist_ok=True)
    with open(os.path.join(kiosk, FORECAST), "wb") as handle:
        handle.write(raw.encode("utf-8"))
    print(json.dumps({"forecast": "grimsbottom", "audit": stamp, "kiosk": kiosk}))
    return 0 if stamp["greenlit"] else 1


if __name__ == "__main__":
    sys.exit(publish())
