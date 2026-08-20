#!/usr/bin/env python3
"""Stamp ?v=<content-hash> on every asset reference.

Cloudflare caches /assets/* for 4 hours, so a deployed CSS or JS change stays
invisible to returning visitors until the edge expires. The version query makes
each deploy a distinct URL. HTML itself is never edge-cached, so new HTML always
ships immediately.

Run before every deploy, after any change to a file in assets/.
"""
import hashlib
import os
import re
import sys

REPO = os.path.expanduser("~/Sites/complianceghost")
ASSETS = ["assets/site.css", "assets/site.js", "assets/assessment.js", "assets/waves.js"]


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:8]


def main():
    os.chdir(REPO)
    versions = {a: digest(a) for a in ASSETS if os.path.exists(a)}
    changed = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "_tools")]
        for name in files:
            if not name.endswith(".html"):
                continue
            p = os.path.join(root, name)
            with open(p, encoding="utf-8") as fh:
                src = fh.read()
            out = src
            for asset, ver in versions.items():
                out = re.sub(r"(/?%s)(\?v=[a-f0-9]+)?\b" % re.escape(asset),
                             lambda m, v=ver: m.group(1) + "?v=" + v, out)
            if out != src:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(out)
                changed.append(p[2:])
    for a, v in sorted(versions.items()):
        print("  %-22s v=%s" % (a, v))
    print("  %d HTML files restamped" % len(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
