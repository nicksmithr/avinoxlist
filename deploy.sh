#!/usr/bin/env bash
set -euo pipefail

python build_html.py

git add index.html

if git diff --cached --quiet; then
  echo "No changes in index.html to commit."
  exit 0
fi

timestamp="$(date -u +"%Y-%m-%d %H:%M UTC")"
git commit -m "deploy: rebuild index.html ${timestamp}"
git push
