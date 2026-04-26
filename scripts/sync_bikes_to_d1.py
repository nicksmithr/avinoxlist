#!/usr/bin/env python3
"""Sync embedded bike JSON from index.html into Cloudflare D1."""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="index.html")
    parser.add_argument("--sql-out", default="tmp/bikes-upsert.sql")
    parser.add_argument("--database", help="D1 database name (required with --apply)")
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def parse_bikes(index_path):
    text = Path(index_path).read_text(encoding="utf-8")
    match = re.search(r"const BIKES = (.*?);\s*const STATS =", text, re.S)
    if not match:
        raise RuntimeError("Could not locate BIKES JSON in index.html")
    return json.loads(match.group(1))


def sql_literal(value):
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def build_sql(bikes):
    lines = ["DELETE FROM bikes;"]
    for bike in bikes:
        values = [
            sql_literal(bike.get("brand")),
            sql_literal(bike.get("model")),
            sql_literal(bike.get("build")),
            sql_literal(bike.get("country")),
            sql_literal(bike.get("motor")),
            sql_literal(bike.get("peakW")),
            sql_literal(bike.get("peakNm")),
            sql_literal(bike.get("batteryWh")),
            sql_literal(bike.get("frame")),
            sql_literal(bike.get("weight")),
            sql_literal(bike.get("removable")),
            sql_literal(bike.get("source")),
        ]
        lines.append(
            "INSERT INTO bikes (brand, model, build, country, motor, peak_w, peak_nm, battery_wh, frame, weight, removable, source_url) "
            f"VALUES ({', '.join(values)});"
        )
    return "\n".join(lines) + "\n"


def main():
    args = parse_args()
    bikes = parse_bikes(args.index)
    sql = build_sql(bikes)
    sql_path = Path(args.sql_out)
    sql_path.parent.mkdir(parents=True, exist_ok=True)
    sql_path.write_text(sql, encoding="utf-8")
    print(f"Wrote SQL for {len(bikes)} bikes to {sql_path}")

    if args.apply:
        if not args.database:
            raise RuntimeError("--database is required when using --apply")
        if not shutil.which("wrangler") and not shutil.which("npx"):
            raise RuntimeError("wrangler is required. Install with: npm i -D wrangler")
        cmd = ["wrangler"] if shutil.which("wrangler") else ["npx", "wrangler"]
        subprocess.run(
            cmd + ["d1", "execute", args.database, "--remote", "--file", str(sql_path)],
            check=True,
        )


if __name__ == "__main__":
    main()
