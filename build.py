#!/usr/bin/env python3
"""Inline data/hospitals.json into src/template.html and write index.html."""
import json, pathlib, sys

root = pathlib.Path(__file__).parent
CATS = {"pe", "corp", "ind", "trust", "unk"}
TYPES = {"Multi-speciality", "Medical college", "Eye care", "Mother & child",
         "Cancer care", "Heart care", "Fertility", "Other speciality"}

rows = json.loads((root / "data" / "hospitals.json").read_text(encoding="utf-8"))
errors, seen = [], set()
for r in rows:
    name = r.get("n", "?")
    for key in ("n", "a", "area", "ll", "cu", "k", "c", "o"):
        if not r.get(key):
            errors.append(f"{name}: missing {key}")
    if r.get("c") not in CATS:
        errors.append(f"{name}: bad category {r.get('c')}")
    if r.get("k") not in TYPES:
        errors.append(f"{name}: bad type {r.get('k')}")
    ll = r.get("ll") or [0, 0]
    if not (8.1 <= ll[0] <= 12.9 and 74.8 <= ll[1] <= 77.5):
        errors.append(f"{name}: coordinates outside Kerala {ll}")
    if r.get("src") and not str(r["src"]).startswith("https://"):
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
districts = (root / "data" / "districts.json").read_text(encoding="utf-8").strip()
assert template.count("/*__DISTRICTS__*/null") == 1
page = template.replace(marker, data).replace("/*__DISTRICTS__*/null", districts)
(root / "index.html").write_text(page, encoding="utf-8")
print(f"index.html written with {len(rows)} hospitals")

# Optional: python3 build.py --standalone OUT MAPLIBRE_CSS
# Writes a variant for hosts that block outside tiles and stylesheets:
# the map library's CSS is inlined and the map draws district outlines only.
if len(sys.argv) == 4 and sys.argv[1] == "--standalone":
    import re
    css = pathlib.Path(sys.argv[3]).read_text(encoding="utf-8")
    alone = page.replace("/*__TILES__*/true", "false")
    alone = re.sub(r'<link rel="stylesheet" href="[^"]*maplibre-gl[^"]*">', lambda m: "<style>" + css + "</style>", alone)
    alone = re.sub(r'<link rel="preconnect"[^>]*>\n?', "", alone)
    alone = re.sub(r'<!doctype html>\n?|</?html[^>]*>\n?|</?head>\n?|</?body>\n?|<meta charset[^>]*>\n?|<meta name="viewport"[^>]*>\n?', "", alone)
    pathlib.Path(sys.argv[2]).write_text(alone, encoding="utf-8")
    print(f"{sys.argv[2]} written")
