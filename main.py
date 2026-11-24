"""Charm the Commuter — one forecast for a city that is not on any map."""
import json
import os

FORECAST = "慢雾市明日多云转晴，雾比早班地铁慢十分钟；阳光预计九点后上岗，与通勤族默契同步，午后有零星拿铁香。"


def ship():
    spot = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(spot, exist_ok=True)
    path = os.path.join(spot, "entry.txt")
    with open(path, "w", encoding="utf-8") as pen:
        pen.write(FORECAST)
    with open(path, "r", encoding="utf-8") as eye:
        assert eye.read() == FORECAST
    print(json.dumps({"city": "slowfog", "sent": len(FORECAST), "forecast": True}))


ship()
