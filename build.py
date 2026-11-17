#!/usr/bin/env python3
"""Inline data/hospitals.json into src/template.html and write index.html."""
import json, pathlib, sys

root = pathlib.Path(__file__).parent
CATS = {"pe", "corp", "ind", "trust"}
TYPES = {"Multi-speciality", "Medical college", "Eye care", "Mother & child",
         "Cancer care", "Heart care", "Fertility", "Other speciality"}

rows = json.loads((root / "data" / "hospitals.json").read_text(encoding="utf-8"))
errors, seen = [], set()
for r in rows:
    name = r.get("n", "?")
    for key in ("n", "a", "area", "ll", "cu", "k", "c", "o", "src"):
        if not r.get(key):
            errors.append(f"{name}: missing {key}")
    if r.get("c") not in CATS:
        errors.append(f"{name}: bad category {r.get('c')}")
    if r.get("k") not in TYPES:
        errors.append(f"{name}: bad type {r.get('k')}")
    ll = r.get("ll") or [0, 0]
    if not (8.1 <= ll[0] <= 12.9 and 74.8 <= ll[1] <= 77.5):
        errors.append(f"{name}: coordinates outside Kerala {ll}")
    if not str(r.get("src", "")).startswith("https://"):
        errors.append(f"{name}: source must be an https link")
    if name in seen:
        errors.append(f"{name}: duplicate name")
    seen.add(name)
if errors:
    sys.exit("\n".join(errors))

data = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
template = (root / "src" / "template.html").read_text(encoding="utf-8")
marker = "/*__DATA__*/[]"
assert template.count(marker) == 1
(root / "index.html").write_text(template.replace(marker, data), encoding="utf-8")
print(f"index.html written with {len(rows)} hospitals")
