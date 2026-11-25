import json
import os

VANE = "cmt3-fake-city"
HORIZON = 140


def atlas(blob):
    """Index the first non-blank row, if any."""
    index = -1
    chosen = ""
    for i, row in enumerate(blob.replace("\r", "").split("\n")):
        if row.strip():
            index = i
            chosen = row
            break
    return index, chosen


def gust(line, root):
    dome = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(root, "output")
    os.makedirs(dome, exist_ok=True)
    vane_out = os.path.join(dome, "entry.txt")
    blob = line.encode("utf-8")
    port = os.open(vane_out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(port, blob)
    finally:
        os.close(port)
    with open(vane_out, "rb") as spy:
        if spy.read() != blob:
            raise IOError("forecast smudged")
    return vane_out


root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(root, "entry.txt"), encoding="utf-8") as barometer:
    where_at, line = atlas(barometer.read())

if where_at < 0 or len(line) > HORIZON:
    print(json.dumps({"skies": "overcast", "size": len(line)}))
    raise SystemExit(1)

vane_out = gust(line, root)
print(json.dumps({"skies": "clear", "size": len(line), "horizon": HORIZON, "vane": VANE, "filed": os.path.basename(vane_out)}))
