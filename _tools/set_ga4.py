#!/usr/bin/env python3
"""Add (or change) the GA4 config line alongside the existing Google Ads tag.

The Ads tag AW-17988411942 has been live since March 2026 and stays — this adds
GA4 next to it so the 14 funnel events already firing through gtag() have a
property to land in. Nothing else changes.

Usage:  python3 _tools/set_ga4.py G-XXXXXXXXXX
        python3 _tools/set_ga4.py --remove
"""
import os
import re
import sys

REPO = os.path.expanduser("~/Sites/complianceghost")
ADS_LINE = "      gtag('config', 'AW-17988411942');"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    arg = sys.argv[1]
    removing = arg == "--remove"
    if not removing and not re.fullmatch(r"G-[A-Z0-9]{10}", arg):
        sys.exit(f"ABORT: '{arg}' is not a valid GA4 measurement id (expected G- plus 10 chars)")

    os.chdir(REPO)
    changed = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "_tools")]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            with open(p, encoding="utf-8") as fh:
                src = fh.read()
            if ADS_LINE not in src:
                continue
            # strip any previous GA4 line so re-running is safe
            out = re.sub(r"\n *gtag\('config', 'G-[A-Z0-9]{10}'\);", "", src)
            if not removing:
                out = out.replace(ADS_LINE, ADS_LINE + f"\n      gtag('config', '{arg}');", 1)
            if out != src:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(out)
                changed.append(p[2:])
    print(f"  {'removed from' if removing else 'added to'} {len(changed)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
