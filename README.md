# avinoxlist

Single-page comparison site for eMTBs running the DJI Avinox motor system.

## Stack

- Pure Python build script (`build_html.py`) renders a single self-contained HTML file
- No frameworks, no bundler, no runtime dependencies
- Vanilla JS, single CSS block, all in the output HTML
- Output: `index.html` (deployed via Cloudflare Pages)

## Files

| File | Purpose |
|---|---|
| `build_with_photos.py` | The bike dataset (~84 rows). Edit here to add or correct bikes. |
| `build_html.py` | The renderer. Holds `WEIGHT_OVERRIDES`, `PRICE_OVERRIDES`, `DIRECT_IMAGES`, and inline `bikes_data.append(...)` for variants not in the source dataset. |
| `index.html` | Build output. Don't edit by hand — regenerate via `python build_html.py`. |
| `deploy.sh` | One-shot: build + commit + push. |

## Build

```bash
python build_html.py
```

That's it. Writes `index.html` to the repo root.

## Deploy

```bash
./deploy.sh
```

Builds, commits with a timestamped message, and pushes to `main`. Cloudflare Pages auto-deploys ~20 seconds later.

## Domain

`avinoxlist.com` (Cloudflare-managed). The Pages project is connected directly via Cloudflare's custom-domain UI — no DNS records to copy by hand.

## Data conventions

A few rules baked into the build, worth knowing if you edit data:

- **Avinox 1500W** is only delivered with the FP700 (700Wh integrated) battery. Standard 800Wh integrated and the RS800 removable both cap at 1300W. Torque stays 150Nm. The build script enforces this — any M2S bike not on 700Wh gets bumped to 1300W automatically.
- **Removable battery** is restricted to Amflow PR Carbon. Every other bike gets `removable: "No"` and `batteryType: "Integrated"` regardless of source data, because most "removable" claims elsewhere are service-removable, not field-swappable.
- **Weight & price overrides** are unconditional — they replace dataset values rather than just filling gaps. This is so manufacturer-confirmed precise values always win over rough source-data estimates.

## Adding a bike

Two paths:

1. **Edit the source dataset** in `build_with_photos.py` (the `bikes` list).
2. **Append inline** in `build_html.py` after the loop, using the schema in the comment block. This is the path used for variants discovered after the source dataset was frozen.

Add image URLs to `DIRECT_IMAGES` keyed by `(brand, model, build)`. Use a list of URLs even for a single image — the modal supports a sliding gallery when there are multiple.

## Visual identity

- Background `#FEFEFE`, text `#2B2F31`, single accent `#FF002B`
- Inter font everywhere
- 3px border radius on the modal, white outline `rgba(255,255,255,0.2)` for subtle backlight
- Accent color reserved: M2S 1500W flagship badge (filled), M2S badge outline, full-power left border on cards/table, M2S motor tint, locale-default price highlight, hero "2026" word, ::selection
- Don't introduce new accent colors

## Coverage (latest build)

- 84 bikes across 27 brands (M1-only Rotwild R.EX excluded)
- 100% with real product photos
- ~70% with manufacturer-confirmed weights
- ~91% with at least one price
