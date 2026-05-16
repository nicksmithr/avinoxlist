#!/usr/bin/env python3
"""Seed expanded D1 schema from BIKES JSON in index.html."""

import argparse
import json
import re
import subprocess
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="index.html")
    parser.add_argument("--sql-out", default="tmp/seed-expanded.sql")
    parser.add_argument("--database", default="avinoxlist-bikes")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--schema", action="store_true", help="Also apply schema migration first")
    return parser.parse_args()


def parse_bikes(index_path):
    text = Path(index_path).read_text(encoding="utf-8")
    match = re.search(r"const BIKES = (.*?);\s*const STATS =", text, re.S)
    if not match:
        raise RuntimeError("Could not locate BIKES JSON in index.html")
    return json.loads(match.group(1))


def slugify(brand, model, build):
    model_words = set(model.lower().split())
    build_normalized = re.sub(r"[^a-z0-9 ]+", " ", build.lower())
    build_words = set(w for w in build_normalized.split() if w)
    model_subset = all(w in build_words for w in model_words)
    text = f"{brand} {build}" if model_subset else f"{brand} {model} {build}"
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


def sql_literal(value):
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def build_sql(bikes):
    lines = []

    for i, bike in enumerate(bikes, 1):
        slug = slugify(bike["brand"], bike["model"], bike["build"])

        cols = [
            "slug", "brand", "model", "build", "country", "status",
            "motor", "peak_w", "peak_nm", "battery_wh", "battery_type",
            "removable", "front_travel_mm", "rear_travel_mm", "frame", "wheels",
            "weight_kg", "weight_source", "fork", "shock", "drivetrain",
            "brakes", "wheelset", "dropper", "instagram", "notes", "source_url"
        ]
        vals = [
            sql_literal(slug),
            sql_literal(bike.get("brand")),
            sql_literal(bike.get("model")),
            sql_literal(bike.get("build")),
            sql_literal(bike.get("country")),
            sql_literal(bike.get("status", "NEW")),
            sql_literal(bike.get("motor")),
            sql_literal(bike.get("peakW")),
            sql_literal(bike.get("peakNm")),
            sql_literal(bike.get("batteryWh")),
            sql_literal(bike.get("batteryType")),
            sql_literal(bike.get("removable", "No")),
            sql_literal(bike.get("frontTravel")),
            sql_literal(bike.get("rearTravel")),
            sql_literal(bike.get("frame")),
            sql_literal(bike.get("wheels")),
            sql_literal(bike.get("weight")),
            sql_literal(bike.get("weightSource")),
            sql_literal(bike.get("fork")),
            sql_literal(bike.get("shock")),
            sql_literal(bike.get("drivetrain")),
            sql_literal(bike.get("brakes")),
            sql_literal(bike.get("wheelset")),
            sql_literal(bike.get("dropper")),
            sql_literal(bike.get("instagram")),
            sql_literal(bike.get("notes")),
            sql_literal(bike.get("source")),
        ]

        lines.append(
            f"INSERT INTO bikes ({', '.join(cols)}) VALUES ({', '.join(vals)});"
        )

        # Prices
        for cur in ["gbp", "eur", "usd", "cad", "aud"]:
            amount = bike.get(cur)
            if amount:
                source_url = bike.get("priceSource") or bike.get("source")
                lines.append(
                    f"INSERT INTO prices (bike_id, currency, amount, source_url, verified_at) "
                    f"VALUES ({i}, {sql_literal(cur)}, {sql_literal(amount)}, {sql_literal(source_url)}, datetime('now'));"
                )

        # Images
        images = bike.get("images") or []
        if not images and bike.get("photo"):
            images = [bike["photo"]]
        if not images and bike.get("directImage"):
            images = [bike["directImage"]]

        for j, url in enumerate(images):
            is_primary = 1 if j == 0 else 0
            alt = f"{bike['brand']} {bike['model']} {bike['build']}"
            lines.append(
                f"INSERT INTO images (bike_id, url, sort_order, is_primary, alt_text) "
                f"VALUES ({i}, {sql_literal(url)}, {j}, {is_primary}, {sql_literal(alt)});"
            )

        lines.append("")

    return "\n".join(lines) + "\n"


def run_wrangler(args, sql_file):
    cmd = ["wrangler"] if shutil.which("wrangler") else ["npx", "wrangler"]
    subprocess.run(
        cmd + ["d1", "execute", args.database, "--remote", "--file", str(sql_file)],
        check=True,
    )


def main():
    args = parse_args()
    bikes = parse_bikes(args.index)

    sql = build_sql(bikes)
    sql_path = Path(args.sql_out)
    sql_path.parent.mkdir(parents=True, exist_ok=True)
    sql_path.write_text(sql, encoding="utf-8")
    print(f"Wrote seed SQL for {len(bikes)} bikes to {sql_path}")

    if args.apply:
        if args.schema:
            schema_file = "cloudflare/d1/migrations/0001_expanded_schema.sql"
            print(f"Applying schema from {schema_file}...")
            run_wrangler(args, schema_file)
            print("Schema applied.")

        print(f"Applying seed data...")
        run_wrangler(args, str(sql_path))
        print("Seed data applied.")


if __name__ == "__main__":
    main()
