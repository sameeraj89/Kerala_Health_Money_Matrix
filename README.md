# Kerala Health Money Matrix

A map of who owns Kerala's private hospitals: private equity–backed, corporate, family-owned or not-for-profit. Entries link a public source where one is available.

- `index.html` is the whole site (static; host it anywhere, for example Vercel or GitHub Pages).
- `data/hospitals.json` holds the hospitals. Edit it, then run `python3 build.py` to regenerate `index.html`.
- `src/template.html` is the page layout and map code.

Each hospital has: `n` name, `a` locality and town, `area` district, `ll` [lat, lng], `cu` speciality, `k` type, `beds`, `c` category (`pe`, `corp`, `ind`, `trust`, or `unk` for owner not recorded), `o` owner, `y` year, `note`, `src` source link, `ap` when the map pin is approximate, `le` registered entity, `nabh` when NABH-accredited, and `sl` when the link is only a directory listing.

Ownership is as reported publicly in November 2026 and was compiled from search-result summaries and desk research; check an entry's source before relying on it. Entries with an empty `src` have no public source linked.

## Map fallback

`data/districts.json` holds simplified district outlines (© OpenStreetMap contributors, ODbL).
If the street tiles cannot load, the map draws these outlines instead.

`python3 build.py --standalone OUT.html MAPLIBRE.css` writes a variant with the map
library's CSS inlined and outlines only, for hosts that block outside tiles and stylesheets.

## Hosting

The site is a single `index.html` at the repository root, so GitHub Pages can serve it
straight from the branch (Settings → Pages → Deploy from a branch → `/ (root)`).
