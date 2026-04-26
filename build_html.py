"""Build a single self-contained HTML page for the Avinox bike comparison."""
import json
import hashlib
import os
from urllib.parse import urlparse
from datetime import datetime, timezone
from build_with_photos import bikes, IG, SPECIFIC_IG, SECONDARY_IG

R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL", "").rstrip("/")
R2_IMAGE_MAP_PATH = os.getenv("R2_IMAGE_MAP_PATH", "tmp/r2-image-map.json")
NEWSLETTER_ACTION_URL = os.getenv(
    "NEWSLETTER_ACTION_URL",
    "https://avinoxlist-email.nicksm10.workers.dev/subscribe",
)
SKIMLINKS_ACCOUNT_ID = os.getenv("SKIMLINKS_ACCOUNT_ID", "ACCOUNT_ID")
CF_WEB_ANALYTICS_TOKEN = os.getenv("CF_WEB_ANALYTICS_TOKEN", "")

R2_IMAGE_MAP = {}
if os.path.exists(R2_IMAGE_MAP_PATH):
    try:
        with open(R2_IMAGE_MAP_PATH, "r", encoding="utf-8") as map_file:
            R2_IMAGE_MAP = json.load(map_file)
    except Exception:
        R2_IMAGE_MAP = {}


def _file_ext_from_url(url):
    path = urlparse(url).path.lower()
    ext = os.path.splitext(path)[1]
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}:
        return ext
    return ".jpg"


def _to_r2_image_url(source_url):
    if not R2_PUBLIC_BASE_URL or not source_url:
        return source_url
    if source_url in R2_IMAGE_MAP:
        return R2_IMAGE_MAP[source_url]
    # If this source did not upload successfully, preserve the original URL.
    # This avoids broken cards when a remote host rate-limits downloads.
    if R2_IMAGE_MAP:
        return source_url
    digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()
    ext = _file_ext_from_url(source_url)
    return f"{R2_PUBLIC_BASE_URL}/bikes/{digest}{ext}"


def _normalize_external_url(url):
    if not url or not isinstance(url, str):
        return url
    value = url.strip()
    if value.startswith(("http://", "https://", "mailto:", "tel:")):
        return value
    if value.startswith("//"):
        return f"https:{value}"
    if value.startswith("www.") or "." in value:
        return f"https://{value}"
    return value

# Convert bikes list to dict structure for JSON embedding
keys = [
    "brand", "model", "build", "country", "status",
    "motor", "peakW", "peakNm",
    "batteryWh", "batteryType", "removable",
    "frontTravel", "rearTravel",
    "frame", "wheels",
    "weight", "weightSource",
    "fork", "shock", "drivetrain", "brakes", "wheelset", "dropper",
    "gbp", "eur", "usd", "cad", "aud",
    "photo", "instagram",
    "notes", "source"
]

bikes_data = []
# Weight overrides confirmed via manufacturer pages or magazine reviews (April 2026)
WEIGHT_OVERRIDES = {
    ("Atherton", "S.170E", "Build 1 (top)"): (24.0, "athertonbikes.com (size 8)"),
    ("Atherton", "S.170E", "Build 2"): (24.0, "athertonbikes.com (size 8)"),
    ("Atherton", "S.170E", "Build 3 (entry)"): (24.0, "athertonbikes.com (size 8)"),
    # BH iLynx+ DL — 9.8 confirmed at 22.4 kg by user; others estimated from component deltas
    ("BH", "iLynx+ DL", "Enduro 9.0 (Alloy entry)"): (23.5, "estimated from component spec vs 9.8"),
    ("BH", "iLynx+ DL", "Enduro 9.1 (Alloy)"): (23.7, "estimated from component spec vs 9.8"),
    ("BH", "iLynx+ DL", "Carbon 9.5"): (23.2, "estimated from component spec vs 9.8"),
    ("BH", "iLynx+ DL", "Carbon 9.6"): (23.5, "estimated from component spec vs 9.8"),
    ("BH", "iLynx+ DL", "Carbon 9.7"): (22.6, "estimated from component spec vs 9.8"),
    # Megamo Reason — verified from megamo.com (mid-range of ribblevalley-e-bikes ranges, size L)
    # Carbon: ~21–21.5 kg, AL: ~22.5–23 kg, Reason Air: ~20–21.5 kg
    ("Megamo", "Reason", "AL 07 (entry alloy)"): (22.8, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "AL 05"): (22.8, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "AL 03"): (23.0, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "AL 03 AXS"): (23.0, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "CRB 07 (entry carbon)"): (21.4, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "CRB 05"): (21.4, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "CRB 03"): (21.6, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "CRB 03 AXS"): (21.5, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "CRB 02"): (21.3, "megamo.com / dealer ranges (size L)"),
    ("Megamo", "Reason", "CRB 01 (top)"): (21.0, "megamo.com (claimed, size L)"),
    # Mondraker Zendit — XR is the new top trim user supplied
    ("Mondraker", "Zendit", "RR (entry)"): (22.8, "mondraker.com (claimed)"),
    ("Forestal", "e-Siryon V2", "Halō"): (22.0, "bike-magazin.de (medium)"),
    ("Thömus", "Oberrider", "Enduro (configurable)"): (19.5, "thoemus.ch / ebike-mtb.com (from)"),
    # Steppenwolf Tundra — confirmed from official spec sheets
    ("Steppenwolf", "Tundra", "9.0 (entry M2S)"): (21.7, "steppenwolf-bicycles.com (incl. battery)"),
    ("Steppenwolf", "Tundra", "10.0"): (21.7, "steppenwolf-bicycles.com (incl. battery)"),
    ("Steppenwolf", "Tundra", "11.0 (top)"): (19.8, "steppenwolf-bicycles.com (incl. battery)"),
    # Olympia Hekton
    ("Olympia", "Hekton 180", "Evo-R"): (22.95, "olympiacicli.it"),
    ("Olympia", "Hekton 160", "Evo-R"): (22.95, "olympiacicli.it (same chassis as 180)"),
    ("Olympia", "Hekton 160", "Pro"): (22.95, "olympiacicli.it (same chassis as 180)"),
    # Forbidden Druid E — user-supplied Pinkbike specs in lbs (we store kg primary, lbs displayed alongside)
    ("Forbidden", "Druid E", "Tier 1 Vitalogy (600Wh)"): (22.32, "pinkbike (49.2 lb)"),
    ("Forbidden", "Druid E", "Tier 1 Vitalogy (800Wh)"): (23.18, "pinkbike (51.1 lb)"),
    ("Forbidden", "Druid E", "Tier 2 Purple Haze (600Wh)"): (22.36, "pinkbike (49.3 lb)"),
    ("Forbidden", "Druid E", "Tier 2 Purple Haze (800Wh)"): (23.22, "pinkbike (51.2 lb)"),
    ("Forbidden", "Druid E", "Tier 3 EVOO (600Wh)"): (22.54, "pinkbike (49.7 lb)"),
    ("Forbidden", "Druid E", "Tier 3 EVOO (800Wh)"): (23.40, "pinkbike (51.6 lb)"),
    ("Forbidden", "Druid E", "Tier 4 Sandstorm (600Wh)"): (22.00, "pinkbike (48.5 lb)"),
    ("Forbidden", "Druid E", "Tier 4 Sandstorm (800Wh)"): (22.41, "pinkbike (49.4 lb)"),
    # Commencal Meta Power SX Avinox — confirmed from commencal.com
    ("Commencal", "Meta Power SX Avinox", "Origin (entry)"): (24.1, "commencal.com (53.13 lb)"),
    ("Commencal", "Meta Power SX Avinox", "Race (top, est.)"): (25.0, "commencal.com (55.12 lb)"),
    # Raymon Tarok — confirmed from raymon-bicycles.com (all M2S Carbon, 150mm, after rename in loop)
    ("Raymon", "Tarok", "Pro"): (22.3, "raymon-bicycles.com"),
    ("Raymon", "Tarok", "Ultra"): (22.0, "raymon-bicycles.com"),
}

# Price overrides — confirmed from official manufacturer spec sheets
PRICE_OVERRIDES = {
    # Steppenwolf Tundra
    ("Steppenwolf", "Tundra", "9.0 (entry M2S)"): {"eur": 5199},
    ("Steppenwolf", "Tundra", "10.0"): {"eur": 7999},
    ("Steppenwolf", "Tundra", "11.0 (top)"): {"eur": 9999},
    # BH iLynx+ DL — GBP from bhbikes.com (en_GB)
    ("BH", "iLynx+ DL", "Enduro 9.0 (Alloy entry)"): {"gbp": 4900},
    ("BH", "iLynx+ DL", "Enduro 9.1 (Alloy)"): {"gbp": 5500},
    ("BH", "iLynx+ DL", "Carbon 9.5"): {"gbp": 5500},
    ("BH", "iLynx+ DL", "Carbon 9.6"): {"gbp": 6400},
    ("BH", "iLynx+ DL", "Carbon 9.7"): {"gbp": 7300},
    ("BH", "iLynx+ DL", "Carbon 9.8 (Top)"): {"gbp": 8200},
    # Megamo Reason — verified EUR prices from megamo.com 2027 spec sheets
    ("Megamo", "Reason", "AL 05"): {"eur": 5999},
    ("Megamo", "Reason", "AL 03"): {"eur": 6999},
    ("Megamo", "Reason", "AL 03 AXS"): {"eur": 7499},
    ("Megamo", "Reason", "CRB 05"): {"eur": 7099},
    ("Megamo", "Reason", "CRB 02"): {"eur": 8999},
    ("Megamo", "Reason", "CRB 01 (top)"): {"eur": 10999},
    # Mondraker Zendit — verified from mondraker.com /uk/en/
    ("Mondraker", "Zendit", "RR (entry)"): {"gbp": 7399},
    ("Mondraker", "Zendit", "RR S (top)"): {"gbp": 9299},
    # Forbidden Druid E — user-supplied CAD pricing per Pinkbike
    ("Forbidden", "Druid E", "Tier 1 Vitalogy (600Wh)"): {"cad": 16199},
    ("Forbidden", "Druid E", "Tier 1 Vitalogy (800Wh)"): {"cad": 16499},
    ("Forbidden", "Druid E", "Tier 2 Purple Haze (600Wh)"): {"cad": 13199},
    ("Forbidden", "Druid E", "Tier 2 Purple Haze (800Wh)"): {"cad": 13499},
    # Pivot Shuttle AMP'd — GBP from biketart.com (UK Pivot distributor)
    ("Pivot", "Shuttle AMP'd", "Team XX Eagle Transmission"): {"gbp": 13499},
    ("Pivot", "Shuttle AMP'd", "Pro X0 Eagle Transmission"): {"gbp": 11999},
    # Raymon Tarok — verified from raymon-bicycles.com (after rename in loop)
    ("Raymon", "Tarok", "Pro"): {"eur": 5999},
    ("Raymon", "Tarok", "Ultra"): {"eur": 7499},
}

for b in bikes:
    rec = dict(zip(keys, b))
    # Skip M1 bikes — user requested removal
    if rec.get("motor") == "M1":
        continue
    # Skip Reason AIR placeholder — replaced with proper per-build variants below
    if rec["brand"] == "Megamo" and rec["model"] == "Reason AIR":
        continue
    # Skip Canyon placeholder — unannounced TBA row
    if rec["brand"] == "Canyon":
        continue
    # Apply specific IG post URL
    key = (rec["brand"], rec["model"])
    if key in SPECIFIC_IG:
        rec["instagram"] = SPECIFIC_IG[key]
    if key in SECONDARY_IG:
        rec["notes"] = (rec["notes"] or "") + " || " + SECONDARY_IG[key]
    # Fix Raymon Tarok Pro: dataset has motor=M2 but raymon-bicycles.com confirms all 4 trims are M2S Carbon
    if rec["brand"] == "Raymon" and rec["model"] == "Tarok" and rec["build"] == "Pro (M2)":
        rec["motor"] = "M2S"
        rec["peakW"] = 1300
        rec["peakNm"] = 150
        rec["build"] = "Pro"
    if rec["brand"] == "Raymon" and rec["model"] == "Tarok" and rec["build"] == "Ultra (M2S)":
        rec["build"] = "Ultra"
    # Apply weight overrides (always — override even if dataset has a value, since these are user-supplied precise values)
    bk = (rec["brand"], rec["model"], rec["build"])
    if bk in WEIGHT_OVERRIDES:
        rec["weight"], rec["weightSource"] = WEIGHT_OVERRIDES[bk]
    # Apply price overrides (unconditional — replace dataset values with verified manufacturer prices)
    if bk in PRICE_OVERRIDES:
        for cur, val in PRICE_OVERRIDES[bk].items():
            rec[cur] = val
    # Avinox motor reality check: M2S only delivers full 1500W with the FP700 (700Wh integrated).
    # The standard 800Wh integrated and the RS800 removable both cap at 1300W. Torque stays 150Nm.
    if rec.get("motor") == "M2S" and rec.get("batteryWh") != 700 and rec.get("peakW") == 1500:
        rec["peakW"] = 1300
    # Removable battery: only the Amflow PR is genuinely field-swappable. Most other "removable"
    # claims in the source data are service-removable only (require tools, not field-swappable).
    if not (rec.get("brand") == "Amflow" and rec.get("model") == "PR Carbon"):
        rec["removable"] = "No"
        if rec.get("batteryType") and "Removable" in rec["batteryType"]:
            rec["batteryType"] = "Integrated"
    bikes_data.append(rec)

# Append new builds added via supplementary research (not in source dataset)
# Schema reminder: brand, model, build, country, status, motor, peakW, peakNm, batteryWh, batteryType,
# removable, frontTravel, rearTravel, frame, wheels, weight, weightSource, fork, shock, drivetrain,
# brakes, wheelset, dropper, gbp, eur, usd, cad, aud, photo, instagram, notes, source

# Mondraker Zendit XR — new top-spec trim (UK pricing per mondraker.com/uk/en/zendit-xr)
bikes_data.append({
    "brand": "Mondraker", "model": "Zendit", "build": "XR (flagship)",
    "country": "Spain", "status": "NEW",
    "motor": "M2S", "peakW": 1300, "peakNm": 150,
    "batteryWh": 800, "batteryType": "Integrated", "removable": "No",
    "frontTravel": 170, "rearTravel": 165,
    "frame": "Carbon", "wheels": "Mullet (29/27.5)",
    "weight": 22.4, "weightSource": "estimated (top trim, full carbon)",
    "fork": "FOX 38 Factory", "shock": "FOX X2 Factory", "drivetrain": "SRAM XX T-Type AXS",
    "brakes": "SRAM Maven Ultimate", "wheelset": "Carbon", "dropper": "FOX Transfer",
    "gbp": 10999, "eur": None, "usd": None, "cad": None, "aud": None,
    "photo": None, "instagram": None,
    "notes": "Mullet wheels, 170/165mm travel, M2S, integrated 800Wh.",
    "source": "mondraker.com/uk/en/zendit-xr",
})

# Forbidden Druid E Tier 3 EVOO and Tier 4 Sandstorm — already in source dataset.
# Existing rows have correct CAD pricing. We only need to update Tier 1/2 weight precision via WEIGHT_OVERRIDES.

# Megamo Reason AIR 2027 — 4 carbon variants verified from megamo.com + 2 alloy (Megamo says 6 total)
# Carbon: CRB 00 (€11,999), CRB 03 AXS (€8,499), CRB 05 (€6,499), CRB 07 (€5,499)
# Alloy: AL variants are part of the 2027 line per E-Mountainbike Magazine but exact SKUs/prices unconfirmed
REASON_AIR_VARIANTS = [
    {"build": "AIR CRB 07 (entry carbon)", "frame": "Carbon", "weight": 21.4, "eur": 5499,
     "fork": "FOX 34 Float AWL 140mm", "shock": "FOX Float Rhythm",
     "drivetrain": "Shimano XT 12-sp", "brakes": "Shimano XT 4-Piston"},
    {"build": "AIR CRB 05", "frame": "Carbon", "weight": 21.0, "eur": 6499,
     "fork": "FOX 36 Float SL Performance 140mm", "shock": "FOX Float Performance",
     "drivetrain": "SRAM 90 Eagle 12-sp", "brakes": "Shimano XT 4-Piston"},
    {"build": "AIR CRB 03 AXS", "frame": "Carbon", "weight": 20.7, "eur": 8499,
     "fork": "FOX 36 Float SL Factory 140mm", "shock": "FOX Float Factory",
     "drivetrain": "SRAM S1000 AXS T-Type", "brakes": "Shimano XT 4-Piston"},
    {"build": "AIR CRB 00 (flagship)", "frame": "Carbon", "weight": 20.0, "eur": 11999,
     "fork": "FOX 36 Float SL Factory 140mm", "shock": "FOX Float Factory",
     "drivetrain": "SRAM XX AXS T-Type", "brakes": "Shimano XTR 4-Piston"},
]
for v in REASON_AIR_VARIANTS:
    bikes_data.append({
        "brand": "Megamo", "model": "Reason AIR", "build": v["build"],
        "country": "Spain", "status": "NEW",
        "motor": "M2S", "peakW": 1300, "peakNm": 150,
        "batteryWh": 800, "batteryType": "Integrated", "removable": "No",
        "frontTravel": 140, "rearTravel": 140,
        "frame": v["frame"], "wheels": "29/29",
        "weight": v["weight"], "weightSource": "megamo.com / dealer ranges (size L)",
        "fork": v["fork"], "shock": v["shock"],
        "drivetrain": v["drivetrain"], "brakes": v["brakes"],
        "wheelset": "DT Swiss", "dropper": None,
        "gbp": None, "eur": v["eur"], "usd": None, "cad": None, "aud": None,
        "photo": None, "instagram": None,
        "notes": "Reason AIR — Megamo's mid-travel (140mm) M2S build.",
        "source": "megamo.com/en/e-bike/e-full-suspension/reason",
    })

# Raymon Tarok — Ultimate (top) and Comp (entry) — not in source dataset
# Confirmed from raymon-bicycles.com/en/modelle/tarok and individual product pages
bikes_data.append({
    "brand": "Raymon", "model": "Tarok", "build": "Ultimate",
    "country": "Germany", "status": "NEW",
    "motor": "M2S", "peakW": 1300, "peakNm": 150,
    "batteryWh": 800, "batteryType": "Integrated (HSC)", "removable": "No",
    "frontTravel": 150, "rearTravel": 150,
    "frame": "Carbon", "wheels": "Mullet (29/27.5)",
    "weight": 20.4, "weightSource": "raymon-bicycles.com (size L)",
    "fork": "FOX 38 Factory", "shock": "FOX Float X2 Factory",
    "drivetrain": "SRAM X0 AXS T-Type 12-sp", "brakes": "SRAM Maven",
    "wheelset": "Carbon", "dropper": "RockShox Reverb AXS",
    "gbp": None, "eur": 9999, "usd": None, "cad": None, "aud": None,
    "photo": None, "instagram": None,
    "notes": "Top trim. HSC Carbon, fixed battery. 12-speed AXS.",
    "source": "raymon-bicycles.com/en/modelle/tarok",
})
bikes_data.append({
    "brand": "Raymon", "model": "Tarok", "build": "Comp",
    "country": "Germany", "status": "NEW",
    "motor": "M2S", "peakW": 1300, "peakNm": 150,
    "batteryWh": 800, "batteryType": "Integrated", "removable": "No",
    "frontTravel": 150, "rearTravel": 150,
    "frame": "Carbon", "wheels": "Mullet (29/27.5)",
    "weight": None, "weightSource": "raymon-bicycles.com (not published)",
    "fork": None, "shock": None,
    "drivetrain": "Shimano CUES 11-sp", "brakes": None,
    "wheelset": None, "dropper": None,
    "gbp": None, "eur": 4999, "usd": None, "cad": None, "aud": None,
    "photo": None, "instagram": None,
    "notes": "Entry trim. Carbon, 11-speed Cues groupset.",
    "source": "raymon-bicycles.com/en/modelle/tarok",
})

# Hand-picked direct image URLs (verified hotlink-friendly CDNs)
# Some bikes have multiple images for a sliding gallery
DIRECT_IMAGES = {
    # Amflow - cdn.amflowbikes.com (Stormsend CDN, hotlink-friendly)
    ("Amflow", "PX Carbon", "PX Carbon"): [
        "https://cdn.amflowbikes.com/stormsend/uploads/986fcc03-73bc-4617-8d7b-e42c4f2ac5a8/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/61b7bfc5-de5d-4f6c-ba02-e2d704f0d5f3/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/c1d1f2c0-b8ec-4022-90aa-99beedfa28b1/default/xl.jpg",
    ],
    ("Amflow", "PX Carbon", "PX Carbon Pro"): [
        "https://cdn.amflowbikes.com/stormsend/uploads/70eaf868-16e2-43f5-99f4-92fedd5c159a/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/61b7bfc5-de5d-4f6c-ba02-e2d704f0d5f3/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/6f3e4588-84ad-4eab-9488-ba285a562cda/default/xl.jpg",
    ],
    ("Amflow", "PR Carbon", "PR Carbon (M2)"): [
        "https://cdn.amflowbikes.com/stormsend/uploads/fa50fe12-d3a7-45a8-b5b4-88aadad51fda/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/1732c1a9-c215-42f1-9e46-ea9ab64034d0/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/11d84579-24ff-4406-8e79-73653a9fe481/default/xl.jpg",
    ],
    ("Amflow", "PR Carbon", "PR Carbon Pro"): [
        "https://cdn.amflowbikes.com/stormsend/uploads/18f890dc-c284-49b6-9a27-6186ad2c9866/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/1732c1a9-c215-42f1-9e46-ea9ab64034d0/default/xl.jpg",
        "https://cdn.amflowbikes.com/stormsend/uploads/11d84579-24ff-4406-8e79-73653a9fe481/default/xl.jpg",
    ],
    # Lee Cougan - s2api.it (Stardue WordPress)
    ("Lee Cougan", "Flö", "Carbon (entry)"): [
        "https://s2api.it/wp-content/uploads/2026/04/Flo_Stonewave_Carbon_.webp",
    ],
    ("Lee Cougan", "Flö", "Carbon Pro"): [
        "https://s2api.it/wp-content/uploads/2026/04/Flo_Pure-Black_Carbon-Pro_-2.webp",
    ],
    # Atherton - high-res from athertonbikes.com category page CDN
    ("Atherton", "S.170E", "Build 1 (top)"): [
        "https://www.athertonbikes.com/media/catalog/category/EMTB_Launch/Category_Page/4.jpg",
    ],
    ("Atherton", "S.170E", "Build 2"): [
        "https://www.athertonbikes.com/media/catalog/category/EMTB_Launch/Category_Page/build_2_carousel.jpg",
    ],
    ("Atherton", "S.170E", "Build 3 (entry)"): [
        "https://www.athertonbikes.com/media/catalog/category/EMTB_Launch/Category_Page/build_3_carousel.jpg",
    ],
    # Crussis - bunny CDN (crussis.cz)
    ("Crussis", "e-Full 11.11", "(800Wh)"): [
        "https://www.crussis.cz/files/thumbs/mod_eshop/produkty/e-full-11-11-2.1025759333.webp?t=1750144811",
    ],
    ("Crussis", "e-Full 11.11", "(600Wh)"): [
        "https://www.crussis.cz/files/thumbs/mod_eshop/produkty/e-full-11-11-2.1025759333.webp?t=1750144811",
    ],
    ("Crussis", "e-Full 12.11", "(800Wh)"): [
        "https://www.crussis.cz/files/thumbs/mod_eshop/produkty/e-full-12-11-grey-2.1025759333.webp?t=1751547938",
    ],
    ("Crussis", "e-Full 12.11 PRO X", "(top spec carbon)"): [
        "https://www.crussis.cz/files/thumbs/mod_eshop/produkty/e-full-pro-x-1-2.1025759333.webp?t=1750777735",
    ],
    ("Crussis", "e-Hard 11.11 PRO", "(160mm hardtail)"): [
        "https://www.crussis.cz/files/thumbs/mod_eshop/produkty/e-hard-11-11-pro-3.1025759333.webp?t=1750146415",
    ],
    # Mondraker Zendit — verified per-build images from cdn.mondraker.com
    ("Mondraker", "Zendit", "RR (entry)"): [
        "https://cdn.mondraker.com/storage/cache/images/2ec/1773836831-750_69ba9a1f80922052833265-zendit-rr-p.jpg",
    ],
    ("Mondraker", "Zendit", "RR S (top)"): [
        "https://cdn.mondraker.com/storage/cache/images/374/1775633512-750_69d6046855790898751386-zendit-rr-s-p.jpg",
    ],
    ("Mondraker", "Zendit", "XR (flagship)"): [
        "https://cdn.mondraker.com/storage/cache/images/dd0/1775633463-750_69d604379ec60378105912-zendit-xr-p.jpg",
    ],
    # Megamo Reason — per-build verified from megamo.com 2027 spec sheets
    ("Megamo", "Reason", "AL 07 (entry alloy)"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31359_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "AL 05"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31359_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "AL 03"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_32404_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "AL 03 AXS"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_32480_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "CRB 07 (entry carbon)"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31233_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "CRB 05"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31233_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "CRB 03"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31229_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "CRB 03 AXS"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31205_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "CRB 02"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_32469_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason", "CRB 01 (top)"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31221_W_1200_Q_100.PNG",
    ],
    # Reason AIR per-build images
    ("Megamo", "Reason AIR", "AIR CRB 00 (flagship)"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31238_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason AIR", "AIR CRB 05"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31246_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason AIR", "AIR CRB 03 AXS"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31242_W_1200_Q_100.PNG",
    ],
    ("Megamo", "Reason AIR", "AIR CRB 07 (entry carbon)"): [
        "https://www.megamo.com/tmp/images/BIBLIOTECA_FOTOS_ERP_31250_W_1200_Q_100.PNG",
    ],
    # Rotwild R.EXC — verified from kirby.rotwild.com
    ("Rotwild", "R.EXC", "Pro (M2S)"): [
        "https://kirby.rotwild.com/media/pages/r-exc-ultra/71908ae4b5-1774617732/rexc-ultram2_dsc_2952_srgb-2400x.webp",
    ],
    ("Rotwild", "R.EXC", "Ultra (M2S)"): [
        "https://kirby.rotwild.com/media/pages/r-exc-ultra/71908ae4b5-1774617732/rexc-ultram2_dsc_2952_srgb-2400x.webp",
    ],
    # Forestal e-Siryon V2 — Halō and Diōde verified from forestal.com S3 CDN
    ("Forestal", "e-Siryon V2", "Halō"): [
        "https://forestal.s3.eu-central-1.amazonaws.com/builds/media/XGsoNoeiaMWkGpz77xJsCrePI4jJuRO3yGaU06Xw.png",
        "https://forestal.s3.eu-central-1.amazonaws.com/builds/media/8EiSSvtC7TBbIdiBiVrap900vHnRSWTXIA9vQrbX.png",
        "https://forestal.s3.eu-central-1.amazonaws.com/builds/media/HEs82he3HyxIrsNeyRQVSxn6TJbTjaGXj9tjUxFt.png",
    ],
    ("Forestal", "e-Siryon V2", "Diōde (top)"): [
        "https://forestal.s3.eu-central-1.amazonaws.com/builds/media/9dQQpb55OQE1efGFr3ZGdNcTGYHUB1lGdLH8wOMq.png",
    ],
    # Forbidden Dreadnought E — official launch teaser
    ("Forbidden", "Dreadnought E", "(pre-order)"): [
        "https://forbiddenbike.com/wp-content/uploads/2026/04/Dreadnought-E-Pick-Your-Poison.png",
    ],
    # Raymon Tarok — per-build verified from b2b.raymon-bicycles.com
    ("Raymon", "Tarok", "Ultimate"): [
        "https://b2b.raymon-bicycles.com/media/82/d2/2f/1775649923/019d6cfba27570edad63942274e299f7.png",
    ],
    ("Raymon", "Tarok", "Ultra"): [
        "https://b2b.raymon-bicycles.com/media/f3/59/e3/1775649918/019d6cfb8c617214aa96c139846b01ad.png",
    ],
    ("Raymon", "Tarok", "Pro"): [
        "https://b2b.raymon-bicycles.com/media/2e/fa/f5/1775649909/019d6cfb6c9171a699e7dfb4fc8982c1.png",
    ],
    ("Raymon", "Tarok", "Comp"): [
        "https://b2b.raymon-bicycles.com/media/f1/1a/ef/1775649902/019d6cfb4e3e7328bf15d3b00ba7ae8e.png",
    ],
    # MMR Lyth — Shopify CDN, verified URL
    ("MMR", "Lyth", "(single build at launch)"): [
        "https://mmrbikes.com/cdn/shop/files/LYTH-FADE-00-WEB_84ccd832-c34d-4e27-909c-19237652de95.jpg?v=1775658340&width=1500",
    ],
    # Forbidden Druid E — per-tier Pinkbike images (user-supplied), shared across battery sizes
    ("Forbidden", "Druid E", "Tier 1 Vitalogy (600Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552921/p5pb29552921.jpg",
    ],
    ("Forbidden", "Druid E", "Tier 1 Vitalogy (800Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552921/p5pb29552921.jpg",
    ],
    ("Forbidden", "Druid E", "Tier 2 Purple Haze (600Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552922/p5pb29552922.jpg",
    ],
    ("Forbidden", "Druid E", "Tier 2 Purple Haze (800Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552922/p5pb29552922.jpg",
    ],
    ("Forbidden", "Druid E", "Tier 3 EVOO (600Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552923/p5pb29552923.jpg",
    ],
    ("Forbidden", "Druid E", "Tier 3 EVOO (800Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552923/p5pb29552923.jpg",
    ],
    ("Forbidden", "Druid E", "Tier 4 Sandstorm (600Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552924/p5pb29552924.jpg",
    ],
    ("Forbidden", "Druid E", "Tier 4 Sandstorm (800Wh)"): [
        "https://ep1.pinkbike.org/p5pb29552924/p5pb29552924.jpg",
    ],
    # Thömus Oberrider — HubSpot CDN, user-supplied
    ("Thömus", "Oberrider", "Enduro (configurable)"): [
        "https://144060947.fs1.hubspotusercontent-eu1.net/hubfs/144060947/Landingpage_OBERRIDER/farben1.webp",
    ],
    ("Thömus", "Oberrider", "Trail (configurable)"): [
        "https://144060947.fs1.hubspotusercontent-eu1.net/hubfs/144060947/Landingpage_OBERRIDER/farben2.webp",
    ],
    # Pivot Shuttle AMP'd — per-build verified from biketart.com Shopify CDN (Pivot UK distributor)
    ("Pivot", "Shuttle AMP'd", "Team XX Eagle Transmission"): [
        "https://www.biketart.com/cdn/shop/files/shuttle-amp-d-team-xx-2027-burgundy-berry-freeze-l-team-xx-1231647208.jpg?v=1775724223&width=1780",
    ],
    ("Pivot", "Shuttle AMP'd", "Pro X0 Eagle Transmission"): [
        "https://www.biketart.com/cdn/shop/files/shuttle-amp-d-pro-x0-2027-burgundy-berry-freeze-s-pro-x0-1231647209.jpg?v=1775724201&width=1780",
    ],
    ("Pivot", "Shuttle AMP'd", "Ride GX Eagle Transmission"): [
        "https://www.biketart.com/cdn/shop/files/shuttle-amp-d-team-xx-2027-burgundy-berry-freeze-l-team-xx-1231647208.jpg?v=1775724223&width=1780",
    ],
    # Teewing Flux — wpdns CDN
    ("Teewing", "Flux One", "Pro"): [
        "https://zv9lm0hjjd.wpdns.site/wp-content/uploads/2026/03/teewing-flux-2026-black-gold.webp",
    ],
    ("Teewing", "Flux One", "A (entry)"): [
        "https://zv9lm0hjjd.wpdns.site/wp-content/uploads/2026/03/teewing-flux-2026-blue-silver.webp",
    ],
    # Teewing Turbo Force — single dataset row, 2 colour options
    ("Teewing", "Turbo Force", "(US-only)"): [
        "https://zv9lm0hjjd.wpdns.site/wp-content/uploads/2026/02/teewing-turbo-force-2026-black-gold-1024x580.webp",
        "https://zv9lm0hjjd.wpdns.site/wp-content/uploads/2026/02/teewing-turbo-force-2026-blue-1024x580.webp",
    ],
    # YT Decoy X — Pinkbike-hosted launch image (replaces yt-industries.com URL)
    ("YT", "Decoy X", "Launch Edition"): [
        "https://c02.purpledshub.com/uploads/sites/39/2026/04/YT-Decoy-X.jpg?webp=1&w=1200",
    ],
    # Crestline RS 181.2 — verified CDN image (replaces placeholder)
    ("Crestline", "RS 181.2", "(single build est.)"): [
        "https://crestlinebikes.com/wp-content/uploads/2026/03/crestline-rs181-forged-carbon-avinox-190225-00405-A-scaled.jpg",
    ],
    # Whyte Karve EVO — Shopify CDN, per-build
    ("Whyte", "Karve EVO", "RS (entry)"): [
        "https://whytebikes.com/cdn/shop/files/Whyte-Karve-EVO-RS_0a6f393d-bd38-4d1a-87bf-9009e1cd9408_1100x.jpg?v=1775715623",
    ],
    ("Whyte", "Karve EVO", "RSX (top)"): [
        "https://whytebikes.com/cdn/shop/files/Whyte-Karve-EVO-RSX_1f1bf01a-f2e3-4e6b-8830-2954853184be_1100x.jpg?v=1775715623",
    ],
    # MAXX FAB.4 ELA — same hero shot for both configs
    ("MAXX", "FAB.4 ELA", "Configurable base"): [
        "https://www.maxx.de/_thumbnails_/10/3612_Fab4_ELA_5000x3400.webp?m=1775650112",
    ],
    ("MAXX", "FAB.4 ELA", "Configurable + 800Wh"): [
        "https://www.maxx.de/_thumbnails_/10/3612_Fab4_ELA_5000x3400.webp?m=1775650112",
    ],
    # Unno Mith — official imgix-served PNG
    ("Unno", "Mith", "(updated M2S)"): [
        "https://www.unno.com/_next/image?url=https%3A%2F%2Fm.unno.com%2F2f6b692259e731d57de52c386890abf22ea1ac7a-3000x2000.png%253Ffit%253Dmin%2526auto%253Dformat%2526w%253D3000%2526q%253D100&w=2048&q=90",
    ],
    # Velduro Rogue R — Shopify CDN
    ("Velduro", "Rogue R", "(complete bike)"): [
        "https://www.velduro.com/cdn/shop/files/velduro-rogue-r-m2-1_opt.webp?v=1775686713&width=1080",
    ],
    # Commencal Meta Power SX Avinox — per-build images from commencal.com
    ("Commencal", "Meta Power SX Avinox", "Origin (entry)"): [
        "https://www.commencal.com/on/demandware.static/-/Sites-commencal-master/default/dw16f0cc72/images/BT5MSXPWDJSGEU1.jpg",
    ],
    ("Commencal", "Meta Power SX Avinox", "Race (top, est.)"): [
        "https://www.commencal.com/on/demandware.static/-/Sites-commencal-master/default/dw41a8f92d/images/BT6MSXPWDJPOEU1.jpg",
    ],
    # Steppenwolf Tundra
    ("Steppenwolf", "Tundra", "9.0 (entry M2S)"): [
        "https://www.steppenwolf-bicycles.com/wp-content/uploads/2026/02/Tundra-9-web-new.png",
    ],
    ("Steppenwolf", "Tundra", "10.0"): [
        "https://www.steppenwolf-bicycles.com/wp-content/uploads/2026/02/Tundra-10-web-new-1-uai-720x480.png",
    ],
    ("Steppenwolf", "Tundra", "11.0 (top)"): [
        "https://www.steppenwolf-bicycles.com/wp-content/uploads/2025/06/Tundra-11-Mossgreen-MattGlossy-scaled.jpg",
    ],
    # Crussis — newer .com URLs supplied by user
    ("Crussis", "e-Hard 1.11", "(entry hardtail)"): [
        "https://www.crussis.com/files/thumbs/mod_eshop/produkty/e-hard-11-11.4060581292.webp?t=1750145930",
    ],
    ("Crussis", "e-Full 12.11 PRO", "(800Wh)"): [
        "https://www.crussis.com/files/thumbs/mod_eshop/produkty/e-full-12-11-pro-2.4060581292.webp?t=1750145482",
    ],
    # Apache Eagle — apache-bike.cz product images
    ("Apache", "Eagle", "1 (top)"): [
        "https://ims.apache-bike.cz/f9/36/f936418fc8816e13f775e502da1947a0_eagle-1-avinox-800-wh_1200e-800e.webp",
    ],
    ("Apache", "Eagle", "2"): [
        "https://ims.apache-bike.cz/90/a1/90a159295206f888ad839a92dff487c7_eagle-2-avinox-800-wh_1200e-800e.webp",
    ],
    ("Apache", "Eagle", "3 (entry)"): [
        "https://ims.apache-bike.cz/e1/ec/e1ecb6e310345ea02111b7148e2ff65b_eagle-3-avinox-800-wh_1200e-800e.webp",
    ],
    # Olympia Hekton — verified from olympiacicli.it product pages
    ("Olympia", "Hekton 180", "Evo-R"): [
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-180_CC16_EvoR.jpg",
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-180_CC10_EvoR.jpg",
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-180_CC04_EvoR.jpg",
    ],
    ("Olympia", "Hekton 160", "Evo-R"): [
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-160_CC08_Pro.jpg",
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-160_CC28_Pro.jpg",
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-160_CC16_Pro.jpg",
    ],
    ("Olympia", "Hekton 160", "Pro"): [
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-160_CC08_Pro.jpg",
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-160_CC28_Pro.jpg",
        "https://www.olympiacicli.it/wp-content/uploads/2025/10/026_Hekton-160_CC16_Pro.jpg",
    ],
    # BH iLynx+ DL — per-build product images from bhbikes.b-cdn.net (user-supplied)
    ("BH", "iLynx+ DL", "Enduro 9.0 (Alloy entry)"): [
        "https://bhbikes.b-cdn.net/cache/general/94db70/ed907_nsn_n1.jpg",
    ],
    ("BH", "iLynx+ DL", "Enduro 9.1 (Alloy)"): [
        "https://bhbikes.b-cdn.net/cache/general/94db70/ed907_nsn_n1.jpg",
    ],
    ("BH", "iLynx+ DL", "Carbon 9.5"): [
        "https://bhbikes.b-cdn.net/cache/general/b131ad/ed957_nsn_n1.jpg",
    ],
    ("BH", "iLynx+ DL", "Carbon 9.6"): [
        "https://bhbikes.b-cdn.net/cache/general/2538f2/ed967_nsn_n1.jpg",
    ],
    ("BH", "iLynx+ DL", "Carbon 9.7"): [
        "https://bhbikes.b-cdn.net/cache/general/a83896/ed977_nsn_n1.jpg",
    ],
    ("BH", "iLynx+ DL", "Carbon 9.8 (Top)"): [
        "https://bhbikes.b-cdn.net/cache/general/079802/ed987_sns_n1.jpg",
    ],
}

# Megamo Reason — same hero for all builds (alloy and carbon)
MEGAMO_REASON_HERO = [
    "https://www.megamo.com/biblioteca/arxius/MY27/Reason/images/reason-my27-2.png?=v2",
]

# Forbidden Druid E - same hero image for all 8 builds
FORBIDDEN_DRUID_E_HERO = [
    "https://forbiddenbike.com/wp-content/uploads/2026/04/druidE_desktop-2048x1152.jpg",
]
# Pivot Shuttle AMP'd - same Cloudinary gallery for all 3 builds (8 images!)
PIVOT_AMPD_GALLERY = [
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-1",
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-2",
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-3_563039388",
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-4",
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-5",
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-6",
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-7",
    "https://res.cloudinary.com/dh826anba/image/upload/w_1200,f_webp,q_auto,dpr_auto/ampd-image-carousel-8",
]

for rec in bikes_data:
    rec["source"] = _normalize_external_url(rec.get("source"))
    rec["photo"] = _to_r2_image_url(_normalize_external_url(rec.get("photo")))
    rec["instagram"] = _normalize_external_url(rec.get("instagram"))
    k = (rec["brand"], rec["model"], rec["build"])
    if k in DIRECT_IMAGES:
        rec["images"] = [_to_r2_image_url(url) for url in DIRECT_IMAGES[k]]
        rec["directImage"] = rec["images"][0]
    elif rec["brand"] == "Pivot" and rec["model"] == "Shuttle AMP'd":
        rec["images"] = [_to_r2_image_url(url) for url in PIVOT_AMPD_GALLERY]
        rec["directImage"] = rec["images"][0]
    else:
        rec["images"] = []
        rec["directImage"] = None

# Compute summary stats
brands = sorted(set(b["brand"] for b in bikes_data))
countries = sorted(set(b["country"] for b in bikes_data))
weights = [b["weight"] for b in bikes_data if b["weight"]]
prices_gbp = [b["gbp"] for b in bikes_data if b["gbp"]]

stats = {
    "totalBuilds": len(bikes_data),
    "totalBrands": len(brands),
    "totalCountries": len(countries),
    "lightestKg": min(weights) if weights else None,
    "lightestBike": next((f'{b["brand"]} {b["model"]} {b["build"]}' for b in bikes_data if b["weight"] == min(weights)), None) if weights else None,
    "cheapestGBP": min(prices_gbp) if prices_gbp else None,
    "cheapestBike": next((f'{b["brand"]} {b["model"]} {b["build"]}' for b in bikes_data if b["gbp"] == min(prices_gbp)), None) if prices_gbp else None,
    "removableCount": sum(1 for b in bikes_data if b["removable"] == "Yes"),
    "fullPowerCount": sum(1 for b in bikes_data if b["peakW"] == 1500),
}

# Inject data as JSON
bikes_json = json.dumps(bikes_data, ensure_ascii=False)
stats_json = json.dumps(stats, ensure_ascii=False)
brands_json = json.dumps(brands, ensure_ascii=False)
countries_json = json.dumps(countries, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AVINOX // 2026 — Full e-MTB index</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #FEFEFE;
  --bg-alt: #F7F7F7;
  --surface: #FFFFFF;
  --surface-2: #FAFAFA;
  --surface-3: #F0F0F0;
  --border: #E5E5E5;
  --border-soft: #EFEFEF;
  --text: #2B2F31;
  --text-2: #6B6F71;
  --text-3: #9CA0A2;
  --accent: #FF002B;
  --accent-soft: rgba(255,0,43,0.08);
  --green: #2B2F31;
  --green-soft: rgba(43,47,49,0.06);
  --blue: #2B2F31;
  --blue-soft: rgba(43,47,49,0.06);
  --amber: #2B2F31;
  --amber-soft: rgba(43,47,49,0.06);
  --red: #FF002B;
  --red-soft: rgba(255,0,43,0.08);
}

html, body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  scroll-behavior: smooth;
  font-feature-settings: 'cv11','ss01','ss03';
}

body {
  background-image: none;
  min-height: 100vh;
  overflow-x: hidden;
}

::selection { background: var(--accent); color: var(--bg); }

/* === HEADER === */
.hero {
  padding: 60px 32px 30px;
  border-bottom: 1px solid var(--border);
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0,0,0,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  mask-image: linear-gradient(180deg, var(--bg) 0%, transparent 100%);
  -webkit-mask-image: linear-gradient(180deg, var(--bg) 0%, transparent 100%);
}
.hero-inner {
  max-width: 1600px; margin: 0 auto; position: relative;
}
.hero-eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  letter-spacing: 0.16em;
  color: var(--text-3);
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 16px;
}
.hero h1 {
  font-family: 'Inter', sans-serif;
  font-size: clamp(56px, 10vw, 160px);
  font-weight: 900;
  letter-spacing: -0.05em;
  line-height: 0.85;
}
.hero h1 .accent { color: var(--accent); }
.hero h1 .slash { color: var(--text-3); margin: 0 0.02em; font-weight: 300; }
.hero-meta-inline {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  color: var(--text-3);
  margin-top: 24px;
  letter-spacing: 0.02em;
  font-feature-settings: 'tnum';
  display: flex; gap: 24px; flex-wrap: wrap;
  border-top: 1px solid var(--border);
  padding-top: 16px;
}
.hero-meta-inline strong {
  color: var(--text); font-weight: 600;
  font-feature-settings: 'tnum';
}
.hero-meta-inline span { display: inline-flex; gap: 4px; align-items: baseline; }
.hero-tagline {
  font-family: 'Inter', sans-serif;
  font-size: 17px;
  color: var(--text-2);
  margin-top: 20px;
  max-width: 640px;
  font-weight: 400;
  line-height: 1.55;
}

/* === NEWSLETTER === */
.newsletter {
  border-bottom: 1px solid var(--border);
  background: var(--bg);
  padding: 22px 32px;
}
.newsletter-inner {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  gap: 14px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}
.newsletter-copy {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  color: var(--text-2);
}
.newsletter-form {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.newsletter-input {
  min-width: 280px;
  border: 1px solid var(--border);
  border-radius: 3px;
  background: #FEFEFE;
  color: var(--text);
  padding: 10px 12px;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  outline: none;
}
.newsletter-input:focus { border-color: var(--text); }
.newsletter-submit {
  border: 1px solid var(--accent);
  border-radius: 3px;
  background: var(--accent);
  color: #FEFEFE;
  padding: 10px 14px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-weight: 600;
  cursor: pointer;
}
.newsletter-submit:disabled {
  opacity: 0.65;
  cursor: wait;
}
.newsletter-status {
  min-height: 18px;
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  color: var(--text-3);
}

/* === STATS BAR === */
.stats {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  border-bottom: 1px solid var(--border);
  background: var(--bg-alt);
}
.stat {
  padding: 24px 32px;
  border-right: 1px solid var(--border);
  position: relative;
}
.stat:last-child { border-right: none; }
.stat-label {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--text-3);
  margin-bottom: 8px;
}
.stat-value {
  font-family: 'Inter', sans-serif;
  font-size: 36px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1;
}
.stat-value .unit {
  font-size: 14px;
  color: var(--text-3);
  font-weight: 400;
  margin-left: 6px;
}
.stat-detail {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  color: var(--text-3);
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* === FILTERS === */
.filters {
  position: sticky; top: 0; z-index: 50;
  background: rgba(254,254,254,0.92);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 16px 32px;
}
.filters-inner {
  max-width: 1600px; margin: 0 auto;
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
}
.filter-group {
  display: flex; align-items: center; gap: 6px;
}
.filter-label {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  letter-spacing: 0.04em;
  color: var(--text-3);
  margin-right: 4px;
  font-weight: 500;
}
.chip {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text-2);
  padding: 7px 14px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 500;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.12s ease;
  white-space: nowrap;
  font-feature-settings: 'tnum';
}
.chip:hover {
  border-color: var(--text);
  color: var(--text);
  background: var(--surface);
}
.chip.active {
  background: var(--text);
  border-color: var(--text);
  color: var(--surface);
}
.search-input {
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text);
  padding: 8px 14px; font-family: 'Inter', sans-serif;
  font-size: 12px; min-width: 200px;
  outline: none; transition: border-color 0.15s;
  border-radius: 999px;
}
.search-input::placeholder { color: var(--text-3); }
.search-input:focus { border-color: var(--text); }

select.chip {
  appearance: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path fill='%239CA0A2' d='M0 0l5 6 5-6z'/></svg>");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 30px;
}

.clear-btn {
  background: transparent; border: 1px solid var(--border);
  color: var(--text-3);
  padding: 7px 14px; font-family: 'Inter', sans-serif;
  font-size: 12px; cursor: pointer;
  font-weight: 500;
  border-radius: 999px;
  transition: all 0.15s;
}
.clear-btn:hover { color: var(--text); border-color: var(--text); }

.view-toggle {
  margin-left: auto;
  display: flex;
  border: 1px solid var(--border);
  border-radius: 999px;
  overflow: hidden;
}
.view-toggle button {
  background: var(--surface); border: none;
  color: var(--text-3);
  padding: 7px 16px; font-family: 'Inter', sans-serif;
  font-size: 12px; cursor: pointer;
  font-weight: 500;
}
.view-toggle button.active {
  background: var(--text); color: var(--surface);
}

/* === RESULTS COUNT === */
.results-bar {
  padding: 20px 32px;
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  display: flex;
  align-items: center;
  gap: 12px;
}
.results-bar strong { color: var(--text); font-size: 13px; }

/* === FEATURED CAROUSEL === */
.featured {
  padding: 0 0 30px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 30px;
}
.featured-header {
  padding: 0 32px 16px;
  display: flex; align-items: center; justify-content: space-between;
}
.featured-title {
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  font-weight: 600;
}
.featured-title .small {
  font-size: 11px;
  font-family: 'Inter', sans-serif;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-left: 12px;
  font-weight: 400;
}
.carousel-controls {
  display: flex; gap: 8px;
}
.carousel-btn {
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text-2);
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.15s;
  font-family: monospace; font-size: 14px;
}
.carousel-btn:hover {
  background: var(--text); color: var(--surface); border-color: var(--text);
}
.carousel {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  padding: 0 32px 12px;
  scrollbar-width: thin;
  scrollbar-color: var(--surface-3) var(--bg);
}
.carousel::-webkit-scrollbar { height: 4px; }
.carousel::-webkit-scrollbar-track { background: var(--bg); }
.carousel::-webkit-scrollbar-thumb { background: var(--surface-3); }

.feat-card {
  flex: 0 0 320px;
  scroll-snap-align: start;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 20px;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
  display: flex; flex-direction: column;
  overflow: hidden;
}
.feat-card::before {
  content: ''; position: absolute;
  right: -60px; top: -60px;
  width: 180px; height: 180px;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 50%;
  pointer-events: none;
}
.feat-card.card-art-m2s::before { border-color: rgba(255,0,43,0.18); }
.feat-card.card-art-m2::before { border-color: rgba(0,0,0,0.08); }
.feat-card.card-art-m1::before { border-color: rgba(0,0,0,0.06); }
.feat-card.card-art-removable::before { border-color: rgba(0,0,0,0.08); }
.feat-card:hover {
  border-color: var(--text);
  background: var(--surface-2);
  transform: translateY(-2px);
}
.feat-card-tag {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 10px;
  font-weight: 500;
}
.feat-card-brand {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 4px;
}
.feat-card-title {
  font-family: 'Inter', sans-serif;
  font-size: 24px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: -0.01em;
  line-height: 1.05;
  margin-bottom: 4px;
}
.feat-card-build {
  font-size: 12px;
  color: var(--text-2);
  margin-bottom: 16px;
}
.feat-card-num {
  font-family: 'Inter', sans-serif;
  font-size: 56px;
  font-weight: 700;
  letter-spacing: -0.04em;
  color: var(--text);
  line-height: 0.9;
  margin: auto 0 4px;
}
.feat-card-num .unit {
  font-size: 16px;
  color: var(--text-2);
  margin-left: 4px;
  font-weight: 400;
  letter-spacing: 0;
}
.feat-card-detail {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* === BIKE GRID === */
.section {
  padding: 30px 32px;
  max-width: 1600px;
  margin: 0 auto;
}
.section-title {
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  font-weight: 600;
  margin-bottom: 4px;
}
.section-sub {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 24px;
}

.brand-group {
  margin-bottom: 40px;
  border-top: 1px solid var(--border);
  padding-top: 24px;
}
.brand-header {
  display: flex; align-items: baseline; gap: 16px;
  margin-bottom: 16px;
}
.brand-name {
  font-family: 'Inter', sans-serif;
  font-size: 32px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: -0.02em;
}
.brand-meta {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.bike-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.bike-card {
  background: var(--surface);
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
  display: flex; flex-direction: column;
  position: relative;
}
.bike-card:hover {
  border-color: var(--text);
  background: var(--surface-2);
}
.bike-card.removable { border-left: 3px solid var(--text); }
.bike-card.full-power { border-left: 3px solid var(--accent); }
.bike-card.preorder { border-left: 3px solid var(--text-3); }
.bike-card.m1 { border-left: 3px solid var(--text-3); }

.bike-card-image {
  height: 180px;
  position: relative;
  overflow: hidden;
  display: flex; align-items: center; justify-content: center;
  --motor-color: rgba(0,0,0,0.02);
  background:
    radial-gradient(circle at 30% 30%, var(--motor-color), transparent 60%),
    linear-gradient(135deg, #FFFFFF 0%, #F7F7F7 100%);
}
.bike-card-image::before {
  content: ''; position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
  background-size: 24px 24px;
  pointer-events: none;
  /* Grid fades out toward top-right corner */
  mask-image: radial-gradient(ellipse 110% 110% at 0% 100%, #000 30%, transparent 80%);
  -webkit-mask-image: radial-gradient(ellipse 110% 110% at 0% 100%, #000 30%, transparent 80%);
}
.bike-card-image::after {
  content: ''; position: absolute; right: -40px; bottom: -40px;
  width: 180px; height: 180px;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 50%;
  pointer-events: none;
}
.bike-card-image img {
  width: 100%; height: 100%; object-fit: cover;
  transition: transform 0.3s; position: relative; z-index: 1;
}
.bike-card:hover .bike-card-image img { transform: scale(1.04); }

.card-art {
  position: relative; width: 100%; height: 100%;
  display: flex; flex-direction: column; justify-content: center; align-items: flex-start;
  padding: 18px 20px; z-index: 2;
}
.card-art-brand {
  font-family: 'Inter', sans-serif;
  font-size: clamp(26px, 5vw, 40px);
  font-weight: 900;
  letter-spacing: -0.05em;
  line-height: 0.85;
  color: var(--text);
  margin-bottom: 4px;
  word-break: break-word;
  max-width: 100%;
  position: relative; z-index: 2;
}
@media (min-width: 1400px) {
  .card-art-brand { font-size: 32px; }
}
@media (min-width: 1800px) {
  .card-art-brand { font-size: 28px; }
}
.card-art-brand .accent-letter { color: var(--motor-accent, var(--text)); }
.card-art-model {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--text-3);
  font-weight: 600;
}
.card-art-divider {
  width: 32px; height: 2px;
  background: var(--text-3);
  margin: 8px 0 6px;
}

.card-art-spec {
  position: absolute; right: 14px; top: 14px;
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  letter-spacing: 0.1em;
  color: var(--text-3);
  text-transform: uppercase;
  text-align: right;
  line-height: 1.5;
  z-index: 2;
  font-feature-settings: 'tnum';
}
.card-art-spec strong { color: var(--motor-accent, var(--text)); font-weight: 600; }

/* Real product image sits on a clean white surface. Procedural brand backdrop is hidden
   when image is present — brand identification moves to the card body below. */
.card-art-img {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: contain;
  object-position: center;
  padding: 12px;
  box-sizing: border-box;
  z-index: 1;
  transition: transform 0.5s ease;
  background: transparent;
  mix-blend-mode: darken;
  pointer-events: none;
}
.bike-card:hover .card-art-img:not(.failed) { transform: scale(1.04); }
.card-art-img.failed { display: none; }
/* When image is loaded, hide the procedural typographic backdrop entirely */
.bike-card-image:has(.card-art-img:not(.failed)) .card-art,
.bike-card-image:has(.card-art-img:not(.failed)) .card-art-spec {
  opacity: 0;
}
.bike-card-image:has(.card-art-img:not(.failed))::after { display: none; }
.bike-card-image:has(.card-art-img:not(.failed)) {
  background: linear-gradient(135deg, #FFFFFF 0%, #F7F7F7 100%);
}
.bike-card-image:has(.card-art-img:not(.failed)) .bike-card-tags {
  z-index: 3;
}

/* Motor-coded subtle tints — only M2S gets red, others stay neutral */
.card-art-m2s { --motor-color: rgba(255,0,43,0.04); --motor-accent: var(--accent); }
.card-art-m2  { --motor-color: rgba(0,0,0,0.025); --motor-accent: var(--text); }
.card-art-m1  { --motor-color: rgba(0,0,0,0.02); --motor-accent: var(--text-2); }
.card-art-removable { --motor-color: rgba(0,0,0,0.025); --motor-accent: var(--text); }

.bike-card-tags {
  position: absolute; top: 8px; left: 8px;
  display: flex; gap: 4px; flex-wrap: wrap;
  z-index: 2;
}
.bike-tag {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  padding: 3px 7px;
  background: rgba(254,254,254,0.92);
  border: 1px solid var(--text);
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text);
  border-radius: 999px;
}
.bike-tag.green { color: var(--text); border-color: var(--text); }
.bike-tag.blue { color: var(--text); border-color: var(--text); }
.bike-tag.amber { color: var(--text); border-color: var(--text); }
.bike-tag.red { color: var(--text); border-color: var(--text); background: rgba(255,255,255,0.95); }
.bike-tag.m2s-flagship { color: var(--surface); border-color: var(--accent); background: var(--accent); }

.bike-card-body { padding: 16px; flex: 1; }
.bike-card-eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin-bottom: 6px;
  font-weight: 600;
}
.bike-card-build {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  color: var(--text-2);
  margin-bottom: 12px;
  font-weight: 500;
}
.bike-card-name {
  font-family: 'Inter', sans-serif;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.05;
  margin-bottom: 4px;
  color: var(--text);
}
.bike-card-stats {
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
  margin-bottom: 12px;
}
.bike-stat {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
}
.bike-stat-label {
  color: var(--text-3); font-size: 9px;
  text-transform: uppercase; letter-spacing: 0.12em;
  margin-bottom: 2px;
}
.bike-stat-value {
  color: var(--text); font-weight: 500;
}
.bike-card-price {
  font-family: 'Inter', sans-serif;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--text);
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  display: flex; align-items: baseline; gap: 8px;
}
.bike-card-price-currency { font-size: 12px; color: var(--text-3); font-weight: 400; }
.bike-card-price-na { color: var(--text-3); font-size: 13px; font-family: 'Inter', sans-serif; font-weight: 400; }

/* === TABLE VIEW === */
.table-wrap {
  overflow-x: auto;
  border: 1px solid var(--border);
  background: var(--surface);
  scrollbar-width: thin;
  scrollbar-color: var(--surface-3) var(--bg);
}
table.bikes {
  border-collapse: collapse;
  width: 100%;
  min-width: 1400px;
  font-family: 'Inter', sans-serif;
  font-size: 11px;
}
table.bikes thead {
  background: var(--bg-alt);
  position: sticky; top: 0; z-index: 5;
}
table.bikes th {
  padding: 12px 10px;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 10px;
  font-weight: 500;
  color: var(--text-2);
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
  cursor: pointer;
}
table.bikes th:hover { color: var(--text); }
table.bikes th.sorted-asc::after { content: ' ↑'; color: var(--text); }
table.bikes th.sorted-desc::after { content: ' ↓'; color: var(--text); }
table.bikes td {
  padding: 12px 10px;
  border-bottom: 1px solid var(--border-soft);
  color: var(--text);
  vertical-align: middle;
}
table.bikes tr:hover { background: var(--surface-2); cursor: pointer; }
table.bikes tr.removable td:first-child { border-left: 3px solid var(--text); }
table.bikes tr.full-power td:first-child { border-left: 3px solid var(--accent); }
table.bikes tr.preorder td:first-child { border-left: 3px solid var(--text-3); }
table.bikes tr.m1 td:first-child { border-left: 3px solid var(--text-3); }
.t-brand { font-weight: 600; color: var(--text); }
.t-num { color: var(--text); font-variant-numeric: tabular-nums; }

/* === MODAL === */
.modal-bg {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  z-index: 100;
  display: none;
  align-items: center; justify-content: center;
  padding: 24px;
  overflow: hidden;
}
.modal-bg.open { display: flex; animation: fadeIn 0.2s; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.modal {
  background: var(--bg);
  border: 1px solid var(--border);
  outline: 2px solid rgba(255,255,255,0.2);
  outline-offset: 0;
  border-radius: 3px;
  max-width: 960px; width: 100%;
  max-height: calc(100vh - 48px);
  position: relative;
  display: flex; flex-direction: column;
  animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
}
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.modal-close {
  position: absolute; top: 16px; right: 16px;
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text);
  width: 36px; height: 36px;
  cursor: pointer; font-family: 'Inter', sans-serif; font-size: 18px;
  display: flex; align-items: center; justify-content: center;
  z-index: 4;
  transition: all 0.15s;
  border-radius: 50%;
}
.modal-close:hover { background: var(--red); border-color: var(--red); color: var(--surface); }

.modal-hero {
  height: 240px;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--border);
  transition: height 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  --motor-color: rgba(0,0,0,0.025);
  background:
    radial-gradient(circle at 20% 20%, var(--motor-color), transparent 50%),
    linear-gradient(135deg, #FFFFFF 0%, #F7F7F7 100%);
}
/* When tech section is open, shrink hero to give the spec table room */
.modal.tech-open .modal-hero { height: 120px; }
.modal-body {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}
.modal-hero::before {
  content: ''; position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
  mask-image: radial-gradient(ellipse 110% 110% at 0% 100%, #000 30%, transparent 80%);
  -webkit-mask-image: radial-gradient(ellipse 110% 110% at 0% 100%, #000 30%, transparent 80%);
}
.modal-hero::after {
  content: ''; position: absolute;
  right: -80px; bottom: -80px;
  width: 320px; height: 320px;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 50%;
}
.modal-hero img {
  width: 100%; height: 100%; object-fit: contain;
  position: relative; z-index: 1;
}
.modal-hero-art {
  position: relative; height: 100%; padding: 40px 48px;
  display: flex; flex-direction: column; justify-content: flex-end;
  z-index: 1;
}
.modal-hero.card-art-m2s { --motor-color: rgba(255,0,43,0.04); --motor-accent: var(--accent); }
.modal-hero.card-art-m2  { --motor-color: rgba(0,0,0,0.025); --motor-accent: var(--text); }
.modal-hero.card-art-m1  { --motor-color: rgba(0,0,0,0.02); --motor-accent: var(--text-2); }
.modal-hero.card-art-removable { --motor-color: rgba(0,0,0,0.025); --motor-accent: var(--text); }
.modal-hero-art-brand {
  font-family: 'Inter', sans-serif;
  font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--motor-accent, var(--text));
  margin-bottom: 8px;
  font-weight: 600;
}
.modal-hero-art-name {
  font-family: 'Inter', sans-serif;
  font-size: clamp(48px, 8vw, 96px);
  font-weight: 900; letter-spacing: -0.05em;
  line-height: 0.85;
  margin-bottom: 12px;
  color: var(--text);
}
.modal-hero-art-build {
  font-family: 'Inter', sans-serif;
  font-size: 12px; color: var(--text-2);
  letter-spacing: 0.05em;
}

/* Sliding image gallery inside modal hero */
.modal-hero-gallery {
  position: absolute; inset: 0;
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  z-index: 2;
  scrollbar-width: none;
}
.modal-hero-gallery::-webkit-scrollbar { display: none; }
.modal-hero-gallery img {
  flex: 0 0 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  padding: 24px;
  box-sizing: border-box;
  scroll-snap-align: start;
  background: linear-gradient(135deg, #FFFFFF 0%, #F7F7F7 100%);
  mix-blend-mode: darken;
}
.modal-hero-gallery img.failed { display: none; }
/* In the modal, keep the procedural art visible underneath too — darken blend lets it show through */
.modal-hero.has-images .modal-hero-art {
  display: block;
}
.modal-hero-dots {
  position: absolute; bottom: 16px; left: 50%;
  transform: translateX(-50%);
  display: flex; gap: 6px;
  z-index: 3;
}
.modal-hero-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: rgba(255,255,255,0.55);
  border: 1px solid rgba(0,0,0,0.15);
  cursor: pointer;
  transition: all 0.2s;
}
.modal-hero-dot.active {
  background: var(--text);
  border-color: var(--text);
  width: 18px;
  border-radius: 3px;
}
.modal-hero-nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  width: 40px; height: 40px;
  background: rgba(254,254,254,0.85);
  border: 1px solid var(--border);
  color: var(--text);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 500;
  z-index: 3;
  transition: all 0.15s;
  border-radius: 50%;
}
.modal-hero-nav:hover { background: var(--text); color: var(--surface); border-color: var(--text); }
.modal-hero-nav.prev { left: 12px; }
.modal-hero-nav.next { right: 12px; }
.modal-hero-counter {
  position: absolute; top: 16px; right: 16px;
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  background: rgba(254,254,254,0.85);
  border: 1px solid var(--border);
  padding: 4px 10px;
  letter-spacing: 0.08em;
  color: var(--text-2);
  z-index: 3;
  border-radius: 999px;
  font-feature-settings: 'tnum';
  font-weight: 500;
}
/* When images present, hide procedural backdrop — bike photo is the visual */
.modal-hero.has-images .modal-hero-art,
.modal-hero.has-images::before,
.modal-hero.has-images::after {
  display: none;
}
.modal-tags {
  position: absolute; top: 16px; left: 16px;
  display: flex; gap: 6px; flex-wrap: wrap;
}

.modal-body { padding: 28px 32px; }

/* Technical specifications toggle — collapsible */
.modal-tech-toggle {
  display: flex; align-items: center; justify-content: space-between;
  width: 100%;
  margin-top: 20px;
  padding: 14px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  cursor: pointer;
  transition: all 0.15s;
}
.modal-tech-toggle:hover { border-color: var(--text); }
.modal-tech-toggle-icon {
  font-family: 'Inter', sans-serif;
  font-size: 18px;
  font-weight: 300;
  color: var(--text-3);
  transition: transform 0.2s, color 0.15s;
}
.modal-tech-toggle[aria-expanded="true"] .modal-tech-toggle-icon {
  transform: rotate(45deg);
  color: var(--accent);
}
.modal-tech-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}
.modal-tech-toggle[aria-expanded="true"] + .modal-tech-content {
  max-height: 1000px;
  margin-top: 12px;
}
.modal-eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.18em;
  margin-bottom: 8px;
  font-weight: 600;
}
.modal-title {
  font-family: 'Inter', sans-serif;
  font-size: 38px;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 0.95;
  margin-bottom: 6px;
}
.modal-build {
  font-size: 14px; color: var(--text-2); margin-bottom: 20px;
}

.modal-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  margin-bottom: 24px;
}
.modal-stat {
  background: var(--surface);
  padding: 16px;
}
.modal-stat-label {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 6px;
}
.modal-stat-value {
  font-family: 'Inter', sans-serif;
  font-size: 26px; font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1;
}
.modal-stat-value .unit {
  font-size: 12px; color: var(--text-3); margin-left: 4px;
  font-family: 'Inter', sans-serif; font-weight: 400;
}
.modal-stat-value.accent { color: var(--text); }
.modal-stat-value .weight-lb {
  font-size: 11px;
  color: var(--text-3);
  font-weight: 500;
  margin-left: 4px;
  font-feature-settings: 'tnum';
}

.modal-spec-table {
  border: 1px solid var(--border); border-collapse: collapse;
  width: 100%; margin-bottom: 24px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
}
.modal-spec-table th {
  text-align: left;
  padding: 10px 14px;
  background: var(--bg-alt);
  border-bottom: 1px solid var(--border);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 10px;
  color: var(--text-3);
  font-weight: 500;
  width: 30%;
}
.modal-spec-table td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-soft);
  color: var(--text);
}
.modal-spec-table tr:last-child th, .modal-spec-table tr:last-child td { border-bottom: none; }

.modal-prices {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px; margin-bottom: 24px;
}
.modal-price {
  background: var(--surface); padding: 14px; border: 1px solid var(--border);
  text-align: center;
  border-radius: 8px;
}
.modal-price.locale-default { border-color: var(--accent); border-width: 1.5px; }
.modal-price-currency {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  letter-spacing: 0.12em;
  color: var(--text-3);
  margin-bottom: 4px;
  font-weight: 600;
  text-transform: uppercase;
}
.modal-price.locale-default .modal-price-currency { color: var(--accent); }
.modal-price-amount {
  font-family: 'Inter', sans-serif;
  font-size: 22px; font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
  font-feature-settings: 'tnum';
}

.modal-notes {
  background: var(--surface); padding: 16px;
  border: 1px solid var(--border);
  font-size: 13px; color: var(--text-2);
  line-height: 1.6; margin-bottom: 16px;
  font-family: 'Inter', sans-serif;
}
.modal-notes strong { color: var(--text); font-weight: 500; }

.modal-links {
  display: flex; gap: 12px; flex-wrap: wrap;
  margin-top: 28px;
}
.modal-link {
  flex: 1; min-width: 150px;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  background: var(--surface); border: 1px solid var(--border);
  padding: 14px; color: var(--text);
  text-decoration: none;
  font-family: 'Inter', sans-serif;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em;
  transition: all 0.15s;
}
.modal-link:hover {
  background: var(--text); color: var(--surface); border-color: var(--text);
}
.modal-link svg { width: 14px; height: 14px; }

/* === FOOTER === */
.footer {
  padding: 60px 32px 40px;
  border-top: 1px solid var(--border);
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  color: var(--text-3);
  text-align: center;
}
.footer .accent { color: var(--text-2); }

/* === EMPTY STATE === */
.empty {
  padding: 80px 32px; text-align: center;
}
.empty h3 {
  font-family: 'Inter', sans-serif;
  font-size: 32px; text-transform: uppercase; letter-spacing: -0.02em;
  margin-bottom: 8px;
}
.empty p { color: var(--text-2); }

@media (max-width: 768px) {
  .hero { padding: 40px 20px 24px; }
  .newsletter { padding: 16px 20px; }
  .newsletter-input { min-width: 100%; }
  .hero-inner { grid-template-columns: 1fr; }
  .hero-meta { text-align: left; }
  .stat { padding: 16px 20px; border-right: none; border-bottom: 1px solid var(--border); }
  .filters { padding: 12px 16px; }
  .section { padding: 24px 16px; }
  .featured-header { padding: 0 16px 12px; }
  .carousel { padding: 0 16px 12px; }
  .feat-card { flex: 0 0 280px; }
  .modal-body { padding: 20px; }
  .modal-title { font-size: 28px; }
  .modal-hero { height: 200px; }
}
</style>
</head>
<body>

<header class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow">Live index — April 2026</div>
    <h1>Avinox<span class="slash">/</span><span class="accent">2026</span></h1>
    <p class="hero-tagline">Every M2S, M2 and lingering M1 e-MTB build that's shipping or in pre-order. Deep specs, live filters, the configurations that actually matter.</p>
    <div class="hero-meta-inline">
      <span>Updated <strong id="meta-refresh">…</strong></span>
    </div>
  </div>
</header>

<section class="newsletter">
  <div class="newsletter-inner">
    <p class="newsletter-copy">New Avinox launches, price drops, and weight updates. Monthly. No spam.</p>
    <form class="newsletter-form" id="newsletter-form" action="__NEWSLETTER_ACTION_URL__" method="post">
      <input class="newsletter-input" id="newsletter-email" type="email" name="email" placeholder="you@example.com" required>
      <button class="newsletter-submit" id="newsletter-submit" type="submit">Subscribe</button>
      <span class="newsletter-status" id="newsletter-status" aria-live="polite"></span>
    </form>
  </div>
</section>

<nav class="filters">
  <div class="filters-inner">
    <span class="filter-label">Motor</span>
    <button class="chip active" data-filter="motor" data-value="all">All</button>
    <button class="chip" data-filter="motor" data-value="M2S">M2S</button>
    <button class="chip" data-filter="motor" data-value="M2">M2</button>

    <span class="filter-label" style="margin-left:8px;">Frame</span>
    <button class="chip active" data-filter="frame" data-value="all">All</button>
    <button class="chip" data-filter="frame" data-value="carbon">Carbon</button>
    <button class="chip" data-filter="frame" data-value="alloy">Alloy</button>

    <span class="filter-label" style="margin-left:8px;">Power</span>
    <button class="chip active" data-filter="power" data-value="all">All</button>
    <button class="chip" data-filter="power" data-value="1500">1500W</button>
    <button class="chip" data-filter="power" data-value="1300">1300W</button>
    <button class="chip" data-filter="power" data-value="1100">1100W</button>

    <input type="search" class="search-input" id="search-input" placeholder="Search brand or model…">

    <span class="filter-label" style="margin-left:8px;">Sort</span>
    <select class="chip" id="sort-select">
      <option value="weight-asc">Weight ↑</option>
      <option value="weight-desc">Weight ↓</option>
      <option value="battery-desc">Battery ↓</option>
      <option value="battery-asc">Battery ↑</option>
      <option value="peakW-desc">Peak power ↓</option>
      <option value="peakW-asc">Peak power ↑</option>
      <option value="rearTravel-desc">Rear travel ↓</option>
      <option value="rearTravel-asc">Rear travel ↑</option>
      <option value="price-asc">Price ↑</option>
      <option value="price-desc">Price ↓</option>
    </select>

    <button class="clear-btn" id="clear-filters">Clear</button>

    <div class="view-toggle">
      <button class="active" data-view="cards">Cards</button>
      <button data-view="table">Table</button>
    </div>
  </div>
</nav>

<div class="results-bar">
  <span>Showing <strong id="results-count">0</strong> of <span id="total-count">0</span> builds</span>
</div>

<main class="section" id="main">
  <div id="bike-list"></div>
</main>

<footer class="footer">
  <p>AVINOX // 2026 — Independently compiled from manufacturer pages, press releases and review-site measurements. Pricing in pre-order may shift. <span class="accent">Verify before purchase.</span></p>
</footer>

<div class="modal-bg" id="modal-bg">
  <div class="modal" id="modal"></div>
</div>

<script>
const BIKES = __BIKES_JSON__;
const STATS = __STATS_JSON__;
const COUNTRIES = __COUNTRIES_JSON__;

// === LOCALE & CURRENCY DETECTION ===
const LOCALE = navigator.language || 'en-GB';
const REGION = (LOCALE.split('-')[1] || LOCALE.toUpperCase()).toUpperCase();
const REGION_TO_CURRENCY = {
  GB: 'gbp', UK: 'gbp', IE: 'eur',
  US: 'usd', CA: 'usd',
  AU: 'aud', NZ: 'aud',
  DE: 'eur', FR: 'eur', ES: 'eur', IT: 'eur', NL: 'eur', BE: 'eur',
  AT: 'eur', PT: 'eur', FI: 'eur', LU: 'eur', GR: 'eur', SK: 'eur',
  SI: 'eur', LV: 'eur', LT: 'eur', EE: 'eur', MT: 'eur', CY: 'eur',
  SE: 'eur', NO: 'eur', DK: 'eur', PL: 'eur', CZ: 'eur', HU: 'eur',
  CH: 'eur', RO: 'eur', BG: 'eur', HR: 'eur',
};
const DEFAULT_CURRENCY = REGION_TO_CURRENCY[REGION] || 'eur';
const CURRENCY_SYM = { gbp: '£', eur: '€', usd: '$', aud: 'A$' };
const CURRENCY_LABEL = { gbp: 'GBP', eur: 'EUR', usd: 'USD', aud: 'AUD' };
// Order to try when picking a price for a bike: locale first, then sensible fallbacks
const CURRENCY_FALLBACK = {
  gbp: ['gbp', 'eur', 'usd', 'aud'],
  eur: ['eur', 'gbp', 'usd', 'aud'],
  usd: ['usd', 'eur', 'gbp', 'aud'],
  aud: ['aud', 'eur', 'gbp', 'usd'],
};

// === STATE ===
const filters = {
  motor: 'all',
  frame: 'all',
  power: 'all',
  search: '',
};
let view = 'cards';
let sortKey = null;
let sortDir = 'asc';
let cardSortKey = 'weight-asc'; // default sort by lightest first

// Global image error handlers
window.handleImgError = function(img) {
  const initial = img.dataset.initial || '';
  const brand = img.dataset.brand || '';
  const wrap = img.parentElement;
  if (!wrap) return;
  wrap.innerHTML = wrap.querySelector('.bike-card-tags')?.outerHTML || '';
  const ph = document.createElement('div');
  ph.className = 'bike-card-image-placeholder';
  ph.setAttribute('data-label', brand);
  ph.textContent = initial;
  wrap.appendChild(ph);
};
window.handleHeroError = function(img) {
  const initial = img.dataset.initial || '';
  img.outerHTML = '<div class="modal-hero-placeholder">' + initial + '</div>';
};

// === HELPERS ===
const $ = (sel, root=document) => root.querySelector(sel);
const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));
const fmtPrice = (n) => n ? n.toLocaleString(LOCALE) : '—';
const fmtWeight = (kg) => {
  if (!kg) return '—';
  const lb = (kg * 2.20462).toFixed(1);
  return `${kg.toFixed(1)} kg <span class="weight-lb">/ ${lb} lb</span>`;
};
const fmtWeightShort = (kg) => {
  if (!kg) return '—';
  const lb = Math.round(kg * 2.20462 * 10) / 10;
  return `${kg.toFixed(1)}kg · ${lb}lb`;
};
const safeText = (s) => (s == null) ? '—' : String(s);

// Pick best price for a bike given locale; returns {sym, value, code} or null
function pickPrice(b) {
  const order = CURRENCY_FALLBACK[DEFAULT_CURRENCY];
  for (const cur of order) {
    if (b[cur]) return { sym: CURRENCY_SYM[cur], value: b[cur], code: CURRENCY_LABEL[cur] };
  }
  return null;
}

function bikeCardClass(b) {
  const isPreorder = (b.notes && b.notes.includes('PRE-ORDER')) ||
                     (b.build && (b.build.includes('TBA') || b.build.includes('unannounced')));
  if (isPreorder) return 'preorder';
  if (b.removable === 'Yes') return 'removable';
  if (b.motor === 'M1') return 'm1';
  if (b.peakW === 1500) return 'full-power';
  return '';
}

function buildTags(b) {
  const tags = [];
  // The flagship: M2S + full 1500W gets the filled red badge (only 700Wh integrated unlocks 1500W)
  if (b.motor === 'M2S' && b.peakW === 1500) tags.push({txt: 'M2S 1500W', cls: 'm2s-flagship'});
  else if (b.motor === 'M2S') tags.push({txt: 'M2S', cls: 'red'});
  if (b.motor === 'M2') tags.push({txt: 'M2', cls: ''});
  return tags;
}

// === STATS BAR ===
function renderStats() {
  const ww = (v, u='') => v ? `${v}<span class="unit">${u}</span>` : '—';
  const items = [
    { label: 'Total builds', value: ww(STATS.totalBuilds), detail: 'across the lineup' },
    { label: 'Brands', value: ww(STATS.totalBrands), detail: 'global manufacturers' },
    { label: 'Lightest measured', value: ww(STATS.lightestKg, 'kg'), detail: STATS.lightestBike || '' },
    { label: 'Cheapest GBP', value: STATS.cheapestGBP ? `£${ww(fmtPrice(STATS.cheapestGBP))}` : '—', detail: STATS.cheapestBike || '' },
    { label: 'Removable battery', value: ww(STATS.removableCount), detail: 'configurations' },
    { label: 'Full 1500W peak', value: ww(STATS.fullPowerCount), detail: 'M2S + FP700 only' },
  ];
  $('#stats').innerHTML = items.map(s => `
    <div class="stat">
      <div class="stat-label">${s.label}</div>
      <div class="stat-value">${s.value}</div>
      <div class="stat-detail">${s.detail}</div>
    </div>
  `).join('');
  $('#meta-total').textContent = STATS.totalBuilds;
  $('#meta-brands').textContent = STATS.totalBrands;
  $('#meta-countries').textContent = STATS.totalCountries;
}

// === FILTERED ===
function applyFilters() {
  return BIKES.filter(b => {
    if (filters.motor !== 'all' && b.motor !== filters.motor) {
      // M2S? counts under M2S
      if (!(filters.motor === 'M2S' && b.motor === 'M2S?')) return false;
    }
    if (filters.frame !== 'all') {
      const f = (b.frame || '').toLowerCase();
      if (filters.frame === 'carbon' && !f.includes('carbon')) return false;
      if (filters.frame === 'alloy' && !(f.includes('alloy') || f.includes('alu') || f.includes('aluminium'))) return false;
    }
    if (filters.power !== 'all' && String(b.peakW) !== filters.power) return false;
    if (filters.search) {
      const q = filters.search.toLowerCase();
      const hay = `${b.brand} ${b.model} ${b.build} ${b.frame||''} ${b.fork||''} ${b.drivetrain||''}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}

// === CAROUSEL (Standout picks) ===
function pickStandouts() {
  const picks = [];
  // Lightest
  const byWeight = BIKES.filter(b => b.weight).sort((a,b) => a.weight - b.weight);
  if (byWeight[0]) picks.push({...byWeight[0], _tag: 'Lightest measured', _stat: byWeight[0].weight, _unit: 'kg'});
  // Cheapest M2S
  const cheapM2S = BIKES.filter(b => b.motor === 'M2S' && b.gbp).sort((a,b) => a.gbp - b.gbp);
  if (cheapM2S[0]) picks.push({...cheapM2S[0], _tag: 'Cheapest M2S (£)', _stat: '£' + cheapM2S[0].gbp.toLocaleString(), _unit: ''});
  // Full power 1500W in £
  const fp = BIKES.filter(b => b.peakW === 1500 && b.gbp).sort((a,b) => a.gbp - b.gbp);
  if (fp[0]) picks.push({...fp[0], _tag: 'Cheapest 1500W', _stat: '£' + fp[0].gbp.toLocaleString(), _unit: ''});
  // Removable battery options - sort by price ascending
  const rem = BIKES.filter(b => b.removable === 'Yes' && b.gbp).sort((a,b) => a.gbp - b.gbp);
  if (rem[0]) picks.push({...rem[0], _tag: 'Cheapest removable', _stat: '£' + rem[0].gbp.toLocaleString(), _unit: ''});
  // Most travel
  const travel = BIKES.filter(b => b.rearTravel).sort((a,b) => b.rearTravel - a.rearTravel);
  if (travel[0]) picks.push({...travel[0], _tag: 'Longest travel', _stat: travel[0].rearTravel, _unit: 'mm rear'});
  // Highest peak power
  const power = BIKES.filter(b => b.peakNm).sort((a,b) => b.peakNm - a.peakNm);
  if (power[0]) picks.push({...power[0], _tag: 'Most torque', _stat: power[0].peakNm, _unit: 'Nm'});
  return picks;
}

function renderCarousel() {
  const picks = pickStandouts();
  $('#carousel').innerHTML = picks.map((b, i) => `
    <div class="feat-card" data-idx="${BIKES.indexOf(BIKES.find(x => x.brand === b.brand && x.model === b.model && x.build === b.build))}">
      <div class="feat-card-tag">${b._tag}</div>
      <div class="feat-card-brand">${b.brand}</div>
      <div class="feat-card-title">${b.model}</div>
      <div class="feat-card-build">${b.build}</div>
      <div class="feat-card-num">${b._stat}<span class="unit">${b._unit}</span></div>
      <div class="feat-card-detail">${b.motor} · ${b.batteryWh}Wh · ${b.weight ? fmtWeightShort(b.weight) + ' · ' : ''}${b.country}</div>
    </div>
  `).join('');
  $$('#carousel .feat-card').forEach(card => {
    card.addEventListener('click', () => {
      const idx = parseInt(card.dataset.idx);
      if (idx >= 0) openModal(BIKES[idx]);
    });
  });
}

// === MAIN VIEW: CARDS ===
function renderCards(filtered) {
  if (filtered.length === 0) {
    $('#bike-list').innerHTML = '<div class="empty"><h3>No builds match</h3><p>Try clearing filters.</p></div>';
    return;
  }
  // Always sort by current sortKey (default weight-asc); no brand grouping, no header
  const sorted = sortBikesFlat(filtered, cardSortKey || 'weight-asc');
  $('#bike-list').innerHTML = `<div class="bike-grid">${sorted.map(b => renderCard(b)).join('')}</div>`;

  $$('.bike-card').forEach(card => {
    card.addEventListener('click', () => {
      const idx = parseInt(card.dataset.idx);
      openModal(BIKES[idx]);
    });
  });
}

function sortBikesFlat(bikes, key) {
  // key format: "field-asc" / "field-desc" / "field" (default asc)
  const parts = key.split('-');
  const field = parts[0];
  const dir = parts[1] === 'desc' ? -1 : 1;
  const val = (b) => {
    if (field === 'price') {
      const pp = pickPrice(b);
      return pp ? pp.value : Infinity * dir; // missing prices sink to bottom
    }
    if (field === 'weight') return b.weight || Infinity * dir;
    if (field === 'battery') return b.batteryWh || -Infinity * dir;
    if (field === 'peakW') return b.peakW || -Infinity * dir;
    if (field === 'rearTravel') return b.rearTravel || -Infinity * dir;
    return 0;
  };
  return [...bikes].sort((a, b) => {
    const va = val(a), vb = val(b);
    if (va === vb) return a.brand.localeCompare(b.brand);
    return (va - vb) * dir;
  });
}

function sortLabelFor(key) {
  const map = {
    'weight-asc': 'weight (lightest first)',
    'weight-desc': 'weight (heaviest first)',
    'battery-desc': 'battery (largest first)',
    'battery-asc': 'battery (smallest first)',
    'peakW-desc': 'peak power (highest first)',
    'peakW-asc': 'peak power (lowest first)',
    'rearTravel-desc': 'rear travel (longest first)',
    'rearTravel-asc': 'rear travel (shortest first)',
    'price-asc': `price (cheapest first, ${CURRENCY_LABEL[DEFAULT_CURRENCY]})`,
    'price-desc': `price (priciest first, ${CURRENCY_LABEL[DEFAULT_CURRENCY]})`,
  };
  return map[key] || key;
}

function cardArtClass(b) {
  if (b.removable === 'Yes') return 'card-art-removable';
  if (b.motor === 'M2S') return 'card-art-m2s';
  if (b.motor === 'M2') return 'card-art-m2';
  if (b.motor === 'M1') return 'card-art-m1';
  return '';
}

function chainringSVG() {
  // Removed per design — keep stub so existing callers don't break
  return '';
}

function renderCard(b) {
  const idx = BIKES.indexOf(b);
  const cls = bikeCardClass(b);
  const artCls = cardArtClass(b);
  const tags = buildTags(b);
  const tagsHTML = tags.slice(0, 2).map(t => `<span class="bike-tag ${t.cls}">${t.txt}</span>`).join('');

  // Stat in top-right corner of art area
  const topSpec = `<div class="card-art-spec">
    <strong>${b.motor || '—'}</strong><br>
    ${b.peakW ? b.peakW + 'W' : '—'}<br>
    ${b.batteryWh ? b.batteryWh + 'Wh' : '—'}${b.removable === 'Yes' ? ' ⇄' : ''}
  </div>`;

  // Image overlay (if available) — covers the art, fades to art on error
  const imgOverlay = b.directImage
    ? `<img class="card-art-img" src="${b.directImage}" alt="${b.brand} ${b.model}" loading="lazy" onerror="this.classList.add('failed')">`
    : '';

  // Pricing display: locale-aware
  const pp = pickPrice(b);
  let priceHTML = pp
    ? `${pp.sym}${fmtPrice(pp.value)} <span class="bike-card-price-currency">${pp.code}</span>`
    : `<span class="bike-card-price-na">Price TBA</span>`;

  return `
    <article class="bike-card ${cls}" data-idx="${idx}">
      <div class="bike-card-image ${artCls}">
        <div class="bike-card-tags">${tagsHTML}</div>
        ${chainringSVG()}
        ${topSpec}
        <div class="card-art">
          <div class="card-art-brand">${b.brand}</div>
          <div class="card-art-divider"></div>
          <div class="card-art-model">${b.model}</div>
        </div>
        ${imgOverlay}
      </div>
      <div class="bike-card-body">
        <div class="bike-card-eyebrow">${b.brand}</div>
        <div class="bike-card-name">${b.model}</div>
        <div class="bike-card-build">${b.build}</div>
        <div class="bike-card-stats">
          <div class="bike-stat">
            <div class="bike-stat-label">Motor / Peak</div>
            <div class="bike-stat-value">${b.motor || '—'} · ${b.peakW ? b.peakW+'W' : '—'}</div>
          </div>
          <div class="bike-stat">
            <div class="bike-stat-label">Battery</div>
            <div class="bike-stat-value">${b.batteryWh ? b.batteryWh+'Wh' : '—'}${b.removable === 'Yes' ? ' ⇄' : ''}</div>
          </div>
          <div class="bike-stat">
            <div class="bike-stat-label">Travel F/R</div>
            <div class="bike-stat-value">${b.frontTravel || '—'}/${b.rearTravel || '—'}mm</div>
          </div>
          <div class="bike-stat">
            <div class="bike-stat-label">Weight</div>
            <div class="bike-stat-value">${b.weight ? fmtWeightShort(b.weight) : '—'}</div>
          </div>
        </div>
        <div class="bike-card-price">${priceHTML}</div>
      </div>
    </article>
  `;
}

// === TABLE VIEW ===
function renderTable(filtered) {
  if (filtered.length === 0) {
    $('#bike-list').innerHTML = '<div class="empty"><h3>No builds match</h3><p>Try clearing filters.</p></div>';
    return;
  }
  // Sort
  let data = [...filtered];
  if (sortKey) {
    data.sort((a,b) => {
      let av = a[sortKey], bv = b[sortKey];
      if (av == null) return 1;
      if (bv == null) return -1;
      if (typeof av === 'number') return sortDir === 'asc' ? av - bv : bv - av;
      return sortDir === 'asc' ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
    });
  }
  const cols = [
    { k: 'brand', label: 'Brand' },
    { k: 'model', label: 'Model' },
    { k: 'build', label: 'Build' },
    { k: 'country', label: 'Country' },
    { k: 'motor', label: 'Motor' },
    { k: 'peakW', label: 'Peak W', n: true },
    { k: 'peakNm', label: 'Nm', n: true },
    { k: 'batteryWh', label: 'Wh', n: true },
    { k: 'removable', label: 'Removable' },
    { k: 'frontTravel', label: 'F mm', n: true },
    { k: 'rearTravel', label: 'R mm', n: true },
    { k: 'weight', label: 'Kg', n: true },
    { k: 'gbp', label: '£', n: true },
    { k: 'eur', label: '€', n: true },
  ];
  const head = cols.map(c => {
    let cls = '';
    if (sortKey === c.k) cls = sortDir === 'asc' ? 'sorted-asc' : 'sorted-desc';
    return `<th class="${cls}" data-key="${c.k}">${c.label}</th>`;
  }).join('');
  const rows = data.map((b, i) => {
    const idx = BIKES.indexOf(b);
    const cls = bikeCardClass(b);
    return `<tr class="${cls}" data-idx="${idx}">
      <td class="t-brand">${b.brand}</td>
      <td>${b.model}</td>
      <td>${b.build}</td>
      <td>${b.country}</td>
      <td>${b.motor || '—'}</td>
      <td class="t-num">${b.peakW || '—'}</td>
      <td class="t-num">${b.peakNm || '—'}</td>
      <td class="t-num">${b.batteryWh || '—'}</td>
      <td>${b.removable || '—'}</td>
      <td class="t-num">${b.frontTravel || '—'}</td>
      <td class="t-num">${b.rearTravel || '—'}</td>
      <td class="t-num">${b.weight || '—'}</td>
      <td class="t-num">${b.gbp ? fmtPrice(b.gbp) : '—'}</td>
      <td class="t-num">${b.eur ? fmtPrice(b.eur) : '—'}</td>
    </tr>`;
  }).join('');
  $('#bike-list').innerHTML = `
    <div class="table-wrap">
      <table class="bikes">
        <thead><tr>${head}</tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
  $$('.bikes th').forEach(th => {
    th.addEventListener('click', () => {
      const k = th.dataset.key;
      if (sortKey === k) {
        sortDir = sortDir === 'asc' ? 'desc' : 'asc';
      } else {
        sortKey = k; sortDir = 'asc';
      }
      render();
    });
  });
  $$('.bikes tbody tr').forEach(tr => {
    tr.addEventListener('click', () => {
      const idx = parseInt(tr.dataset.idx);
      openModal(BIKES[idx]);
    });
  });
}

// === MODAL ===
function openModal(b) {
  const tags = buildTags(b);
  const tagsHTML = tags.map(t => `<span class="bike-tag ${t.cls}">${t.txt}</span>`).join('');
  const artCls = cardArtClass(b);
  const hasImages = b.images && b.images.length > 0;

  // Procedural art (always rendered as backdrop, hidden when images load)
  const heroArt = `
    <div class="modal-hero-art">
      ${chainringSVG().replace('card-art-cog', 'modal-hero-art-cog')}
      <div class="modal-hero-art-brand">${b.brand} · ${b.country}</div>
      <div class="modal-hero-art-name">${b.model}</div>
      <div class="modal-hero-art-build">${b.build}</div>
    </div>
  `;

  // Sliding image gallery (when we have real photos)
  let gallery = '';
  if (hasImages) {
    const imgs = b.images.map((src, i) => `<img src="${src}" alt="${b.brand} ${b.model} ${i+1}" loading="${i === 0 ? 'eager' : 'lazy'}" onerror="this.classList.add('failed')">`).join('');
    const dots = b.images.length > 1 ? `
      <div class="modal-hero-dots" id="modal-hero-dots">
        ${b.images.map((_, i) => `<div class="modal-hero-dot${i === 0 ? ' active' : ''}" data-idx="${i}"></div>`).join('')}
      </div>
    ` : '';
    const nav = b.images.length > 1 ? `
      <button class="modal-hero-nav prev" id="modal-hero-prev">‹</button>
      <button class="modal-hero-nav next" id="modal-hero-next">›</button>
      <div class="modal-hero-counter" id="modal-hero-counter">01 / ${String(b.images.length).padStart(2, '0')}</div>
    ` : '';
    gallery = `<div class="modal-hero-gallery" id="modal-hero-gallery">${imgs}</div>${dots}${nav}`;
  }

  // Pick top 2 prices: locale-default first, then a sensible second
  const allPrices = [
    {c: 'GBP', sym: '£', v: b.gbp, key: 'gbp'},
    {c: 'EUR', sym: '€', v: b.eur, key: 'eur'},
    {c: 'USD', sym: '$', v: b.usd, key: 'usd'},
    {c: 'CAD', sym: 'C$', v: b.cad, key: 'cad'},
    {c: 'AUD', sym: 'A$', v: b.aud, key: 'aud'},
  ].filter(p => p.v);
  const prices = [...allPrices].sort((a, b2) => {
    if (a.key === DEFAULT_CURRENCY) return -1;
    if (b2.key === DEFAULT_CURRENCY) return 1;
    return 0;
  });
  const priceLead = prices[0];

  const stats = [
    { label: 'Motor / Peak', value: `${b.motor}${b.peakW ? ' · ' + b.peakW + 'W' : ''}`, valid: !!b.motor },
    { label: 'Battery', value: b.batteryWh, unit: 'Wh' },
    { label: 'Travel F/R', value: (b.frontTravel && b.rearTravel) ? `${b.frontTravel}/${b.rearTravel}` : null, unit: 'mm', valid: !!(b.frontTravel && b.rearTravel) },
    { label: 'Peak torque', value: b.peakNm, unit: 'Nm' },
    { label: 'Weight', value: b.weight, unit: 'kg', weight: true },
    { label: 'Frame', value: b.frame, valid: !!b.frame },
    priceLead ? { label: priceLead.c, value: `${priceLead.sym}${fmtPrice(priceLead.v)}`, valid: true, accent: true } : null,
    prices[1] ? { label: prices[1].c, value: `${prices[1].sym}${fmtPrice(prices[1].v)}`, valid: true } : null,
  ].filter(s => s && (s.valid !== false) && s.value != null && s.value !== '');

  const statsHTML = stats.map(s => {
    if (s.weight) {
      return `<div class="modal-stat">
        <div class="modal-stat-label">${s.label}</div>
        <div class="modal-stat-value">${fmtWeight(s.value)}</div>
      </div>`;
    }
    return `<div class="modal-stat">
      <div class="modal-stat-label">${s.label}</div>
      <div class="modal-stat-value ${s.accent ? 'accent' : ''}">${s.value}${s.unit ? `<span class="unit">${s.unit}</span>` : ''}</div>
    </div>`;
  }).join('');

  // Tech section toggles open: pushes hero smaller, reveals spec table
  // Skip motor/battery/wheels/weightSource since those are in the main stat grid or trivial
  const specRows = [
    ['Frame detail', b.frame !== priceLead?.label && b.frame !== stats.find(s=>s.label==='Frame')?.value ? b.frame : null],
    ['Wheels', b.wheels],
    ['Fork', b.fork],
    ['Rear shock', b.shock],
    ['Drivetrain', b.drivetrain],
    ['Brakes', b.brakes],
    ['Wheelset', b.wheelset],
    ['Dropper', b.dropper],
    ['Battery type', b.batteryType],
    ['Removable battery', b.removable],
    ['Weight source', b.weightSource],
  ].filter(([k,v]) => v && v !== 'TBD' && v !== '—');
  const specHTML = specRows.map(([k,v]) => `<tr><th>${k}</th><td>${v}</td></tr>`).join('');

  // Price block removed — prices are now in the main stat grid
  const pricesHTML = '';

  const links = [];
  if (b.source) links.push({url: b.source, label: 'Manufacturer page'});
  if (b.photo && b.photo.startsWith('http')) links.push({url: b.photo, label: 'Photo / spec page'});
  if (b.instagram && b.instagram.startsWith('http')) links.push({url: b.instagram, label: 'Instagram'});
  const linksHTML = links.map(l => `
    <a class="modal-link" href="${l.url}" target="_blank" rel="noopener">
      ${l.label}
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M7 17 17 7M7 7h10v10"/>
      </svg>
    </a>
  `).join('');

  $('#modal').innerHTML = `
    <button class="modal-close" onclick="closeModal()">×</button>
    <div class="modal-hero ${artCls}${hasImages ? ' has-images' : ''}" id="modal-hero">
      <div class="modal-tags">${tagsHTML}</div>
      ${heroArt}
      ${gallery}
    </div>
    <div class="modal-body">
      <div class="modal-eyebrow">${b.brand} · ${b.country}</div>
      <h2 class="modal-title">${b.model}</h2>
      <div class="modal-build">${b.build}</div>
      <div class="modal-grid">${statsHTML}</div>
      ${specHTML ? `
        <button class="modal-tech-toggle" id="tech-toggle" aria-expanded="false">
          <span>Technical specifications</span>
          <span class="modal-tech-toggle-icon">+</span>
        </button>
        <div class="modal-tech-content" id="tech-content">
          <table class="modal-spec-table">${specHTML}</table>
        </div>
      ` : ''}
      ${linksHTML ? `<div class="modal-links">${linksHTML}</div>` : ''}
    </div>
  `;

  // Wire technical toggle: expanding tech shrinks the hero
  const techToggle = $('#tech-toggle');
  if (techToggle) {
    techToggle.addEventListener('click', () => {
      const expanded = techToggle.getAttribute('aria-expanded') === 'true';
      techToggle.setAttribute('aria-expanded', !expanded);
      $('#modal').classList.toggle('tech-open', !expanded);
    });
  }

  // Wire gallery navigation if multi-image
  if (hasImages && b.images.length > 1) {
    const gal = $('#modal-hero-gallery');
    const dots = $$('#modal-hero-dots .modal-hero-dot');
    const counter = $('#modal-hero-counter');
    const updateActive = () => {
      const idx = Math.round(gal.scrollLeft / gal.clientWidth);
      dots.forEach((d, i) => d.classList.toggle('active', i === idx));
      if (counter) counter.textContent = `${String(idx+1).padStart(2,'0')} / ${String(b.images.length).padStart(2,'0')}`;
    };
    gal.addEventListener('scroll', updateActive);
    dots.forEach((d, i) => {
      d.addEventListener('click', () => gal.scrollTo({ left: i * gal.clientWidth, behavior: 'smooth' }));
    });
    $('#modal-hero-prev').addEventListener('click', () => gal.scrollBy({ left: -gal.clientWidth, behavior: 'smooth' }));
    $('#modal-hero-next').addEventListener('click', () => gal.scrollBy({ left: gal.clientWidth, behavior: 'smooth' }));
  }
  $('#modal-bg').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  $('#modal-bg').classList.remove('open');
  document.body.style.overflow = '';
}

// === RENDER ===
function render() {
  const filtered = applyFilters();
  $('#results-count').textContent = filtered.length;
  $('#total-count').textContent = BIKES.length;
  if (view === 'cards') renderCards(filtered);
  else renderTable(filtered);
}

// === EVENTS ===
$$('.chip[data-filter]').forEach(chip => {
  chip.addEventListener('click', () => {
    const f = chip.dataset.filter;
    const v = chip.dataset.value;
    filters[f] = v;
    $$(`.chip[data-filter="${f}"]`).forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    render();
  });
});

$('#search-input').addEventListener('input', e => {
  filters.search = e.target.value.trim();
  render();
});

$('#sort-select').addEventListener('change', e => {
  cardSortKey = e.target.value;
  render();
});

$('#clear-filters').addEventListener('click', () => {
  Object.keys(filters).forEach(k => filters[k] = k === 'search' ? '' : 'all');
  $$('.chip[data-filter]').forEach(c => {
    if (c.dataset.value === 'all') c.classList.add('active');
    else c.classList.remove('active');
  });
  $('#search-input').value = '';
  $('#sort-select').value = 'weight-asc';
  cardSortKey = 'weight-asc';
  render();
});

$$('.view-toggle button').forEach(btn => {
  btn.addEventListener('click', () => {
    view = btn.dataset.view;
    $$('.view-toggle button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    render();
  });
});

$('#modal-bg').addEventListener('click', e => { if (e.target === $('#modal-bg')) closeModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

const newsletterForm = $('#newsletter-form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const emailInput = $('#newsletter-email');
    const submitBtn = $('#newsletter-submit');
    const status = $('#newsletter-status');
    const email = (emailInput?.value || '').trim();
    if (!email) return;

    submitBtn.disabled = true;
    status.textContent = 'Submitting...';
    try {
      const response = await fetch(newsletterForm.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (!response.ok) throw new Error('Subscription failed');
      status.textContent = 'Thanks - check your inbox for confirmation.';
      newsletterForm.reset();
    } catch (err) {
      status.textContent = 'Subscription failed. Please try again.';
    } finally {
      submitBtn.disabled = false;
    }
  });
}

// === INIT ===
// Last-refresh relative time
(function() {
  const buildTs = "__BUILD_TIMESTAMP__";
  const t = new Date(buildTs);
  if (isNaN(t.getTime())) return;
  const diffMs = Date.now() - t.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  const diffHr = Math.floor(diffMs / 3600000);
  const diffDay = Math.floor(diffMs / 86400000);
  let label;
  if (diffMin < 2) label = 'just now';
  else if (diffMin < 60) label = `${diffMin} minutes ago`;
  else if (diffHr < 2) label = '1 hour ago';
  else if (diffHr < 24) label = `${diffHr} hours ago`;
  else if (diffDay < 2) label = '1 day ago';
  else label = `${diffDay} days ago`;
  const el = document.getElementById('meta-refresh');
  if (el) el.textContent = label;
})();

render();
</script>
__SKIMLINKS_SCRIPT__
__CF_BEACON_SCRIPT__
</body>
</html>
"""

html_out = HTML.replace("__BIKES_JSON__", bikes_json)
html_out = html_out.replace("__STATS_JSON__", stats_json)
html_out = html_out.replace("__COUNTRIES_JSON__", countries_json)
html_out = html_out.replace("__BUILD_TIMESTAMP__", datetime.now(timezone.utc).isoformat())
html_out = html_out.replace("__NEWSLETTER_ACTION_URL__", NEWSLETTER_ACTION_URL)
html_out = html_out.replace(
    "__SKIMLINKS_SCRIPT__",
    f'<script async src="https://s.skimresources.com/js/{SKIMLINKS_ACCOUNT_ID}.skimlinks.js"></script>',
)
if CF_WEB_ANALYTICS_TOKEN:
    cf_beacon = (
        "<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
        f"data-cf-beacon='{{\"token\": \"{CF_WEB_ANALYTICS_TOKEN}\"}}'></script>"
    )
else:
    cf_beacon = "<!-- Set CF_WEB_ANALYTICS_TOKEN to enable Cloudflare Web Analytics -->"
html_out = html_out.replace("__CF_BEACON_SCRIPT__", cf_beacon)
out_path = 'index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_out)

print(f"Saved {out_path}")
print(f"Bikes: {len(bikes_data)}")
print(f"File size: {os.path.getsize(out_path) / 1024:.1f} KB")
