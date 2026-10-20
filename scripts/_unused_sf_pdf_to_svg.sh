#!/usr/bin/env bash
# Converts assets/sf-symbols/pdf/*.pdf → assets/sf-symbols/svg/*.svg (needs pdftocairo / poppler).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p assets/sf-symbols/svg
for f in assets/sf-symbols/pdf/*.pdf; do
  n=$(basename "$f" .pdf)
  pdftocairo -svg "$f" "assets/sf-symbols/svg/$n.svg"
done
ls assets/sf-symbols/svg | wc -l
