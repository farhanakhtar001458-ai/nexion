#!/usr/bin/env bash
# Original RGPV question-paper PDFs (2009-2019) fetch karne ka script.
#
# Source: public community mirror of the rgpvonline.com paper archive
#         https://github.com/littlechampsacademy/rgpv-question-paper.littlechampsacademy.in
#
# Usage:  bash tools/fetch_originals.sh [target-dir]
# Default target-dir: papers/original-archive
#
# Ye script sirf first-year (BT-201..BT-205) ke physics-group PDFs sparse-checkout karta hai,
# phir unhe subject-wise folders me rename karke rakhta hai.

set -euo pipefail

MIRROR="https://github.com/littlechampsacademy/rgpv-question-paper.littlechampsacademy.in.git"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$HERE/../papers/original-archive}"
TMP="$(mktemp -d)"

echo "==> sparse clone mirror -> $TMP"
git clone --depth 1 --filter=blob:none --sparse "$MIRROR" "$TMP/lc"
cd "$TMP/lc"
git sparse-checkout set --no-cone \
  'be/be-201-*.pdf' 'be/be-203-*.pdf' 'be/be-204-*.pdf' 'be/be-205-*.pdf' \
  'be/bt-2001-*.pdf' 'be/bt-2002-*.pdf' 'be/bt-2003-*.pdf' 'be/bt-2004-*.pdf' 'be/bt-2005-*.pdf'

echo "==> organising into $TARGET"
python3 - "$TMP/lc/be" "$TARGET" <<'PY'
import os, re, shutil, sys
src, out = sys.argv[1], sys.argv[2]

rules = [
    ("be-201-",     "BT-201", "BT-201-Engineering-Physics"),
    ("bt-2001-",    "BT-201", "BT-201-Engineering-Physics"),
    ("be-202-engineering-mathematics-2-", "BT-202", "BT-202-Mathematics-II"),
    ("bt-2002-",    "BT-202", "BT-202-Mathematics-II"),
    ("be-203-basic-mechanical-engineering-", "BT-203", "BT-203-Basic-Mechanical-Engineering"),
    ("bt-2003-",    "BT-203", "BT-203-Basic-Mechanical-Engineering"),
    ("be-204-basic-civil-engineering-and-engineering-mechanics-", "BT-204", "BT-204-Basic-Civil-Engineering-Mechanics"),
    ("bt-2004-",    "BT-204", "BT-204-Basic-Civil-Engineering-Mechanics"),
    ("be-205-basic-computer-engineering-", "BT-205", "BT-205-Basic-Computer-Engineering"),
    ("bt-2005-",    "BT-205", "BT-205-Basic-Computer-Engineering"),
]
EXCLUDE = ["engineering-mechanics-dec-2011", "engineering-mechanics-jun-2009",
           "engineering-mechanics-jun-2010", "be-204-basic-mechanical-engineering",
           "be-205-basic-civil-engineering"]
MON = {"jun": "Jun", "dec": "Dec", "may": "May", "nov": "Nov"}

def session(fn):
    parts = fn[:-4].split("-")[-2:]
    if parts[0].lower() == "cbgs":
        return f"CBGS-{parts[1].capitalize()}"
    return f"{MON.get(parts[0].lower(), parts[0])}-{parts[1]}" if len(parts) == 2 else fn[:-4]

n = 0
for fn in sorted(os.listdir(src)):
    if not fn.endswith(".pdf") or any(x in fn for x in EXCLUDE):
        continue
    hit = next(((c, f) for p, c, f in rules if fn.startswith(p)), None)
    if not hit:
        continue
    code, folder = hit
    d = os.path.join(out, folder); os.makedirs(d, exist_ok=True)
    shutil.copy2(os.path.join(src, fn), os.path.join(d, f"{code}_{session(fn)}.pdf"))
    n += 1
print(f"copied {n} PDFs")
PY

rm -rf "$TMP"
echo "==> done"
