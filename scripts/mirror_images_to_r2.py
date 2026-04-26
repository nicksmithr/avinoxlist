#!/usr/bin/env python3
"""Mirror image URLs from index.html into Cloudflare R2 via Wrangler."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="index.html")
    parser.add_argument("--bucket", required=True, help="R2 bucket name")
    parser.add_argument(
        "--public-base-url",
        required=True,
        help="Public image domain, e.g. https://images.avinoxlist.com",
    )
    parser.add_argument("--download-dir", default="tmp/r2-image-cache")
    parser.add_argument("--download-only", action="store_true")
    return parser.parse_args()


def parse_bikes(index_path):
    text = Path(index_path).read_text(encoding="utf-8")
    match = re.search(r"const BIKES = (.*?);\s*const STATS =", text, re.S)
    if not match:
        raise RuntimeError("Could not find embedded BIKES JSON in index.html")
    return json.loads(match.group(1))


def file_ext(url):
    ext = os.path.splitext(urlparse(url).path.lower())[1]
    return ext if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"} else ".jpg"


def key_for_url(url):
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return f"bikes/{digest}{file_ext(url)}"


def download(url, local_path):
    request = urllib.request.Request(url, headers={"User-Agent": "avinoxlist-image-mirror/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        local_path.write_bytes(response.read())


def wrangler_upload(bucket, key, local_path):
    cmd = wrangler_cmd() + ["r2", "object", "put", f"{bucket}/{key}", "--file", str(local_path)]
    subprocess.run(cmd, check=True)


def wrangler_cmd():
    if shutil.which("wrangler"):
        return ["wrangler"]
    if shutil.which("npx"):
        return ["npx", "wrangler"]
    raise RuntimeError("wrangler is required. Install with: npm i -D wrangler")


def main():
    args = parse_args()
    bikes = parse_bikes(args.index)
    base_url = args.public_base_url.rstrip("/")
    download_dir = Path(args.download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    if not args.download_only:
        try:
            wrangler_cmd()
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)

    urls = set()
    for bike in bikes:
        for image in bike.get("images", []):
            if isinstance(image, str) and image.startswith("http"):
                urls.add(image)
        direct = bike.get("directImage")
        if isinstance(direct, str) and direct.startswith("http"):
            urls.add(direct)

    mapping = {}
    for idx, url in enumerate(sorted(urls), start=1):
        key = key_for_url(url)
        local_path = download_dir / os.path.basename(key)
        print(f"[{idx}/{len(urls)}] {url}")
        try:
            download(url, local_path)
            if not args.download_only:
                wrangler_upload(args.bucket, key, local_path)
            mapping[url] = f"{base_url}/{key}"
        except Exception as exc:  # noqa: BLE001
            print(f"Failed: {url} -> {exc}", file=sys.stderr)

    map_path = Path("tmp/r2-image-map.json")
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"Wrote {len(mapping)} mapped URLs to {map_path}")


if __name__ == "__main__":
    main()
