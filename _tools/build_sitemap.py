#!/usr/bin/env python3
"""Regenerate sitemap.xml with lastmod taken from git.

The sitemap was hand-maintained, so lastmod drifted: pages edited on Aug 7 still
declared Jul 23. A stale lastmod is a weak-but-real signal that content has not
changed, which is the opposite of what a site trading on "current Texas rules"
wants to tell Google.

Run before every deploy:  python3 _tools/build_sitemap.py
"""
import os
import re
import subprocess
import sys

REPO = os.path.expanduser("~/Sites/complianceghost")
BASE = "https://complianceghost.com"
SKIP_DIRS = {".git", "_tools", "checklist/pdfs"}

# Pages that carry the offer or the freshness claim get crawled more often.
PRIORITY = {
    "/": ("weekly", "1.0"),
    "/med-spa/": ("monthly", "0.9"),
    "/dental/": ("monthly", "0.9"),
    "/tattoo/": ("monthly", "0.9"),
    "/esthetician/": ("monthly", "0.9"),
    "/assessment/": ("monthly", "0.9"),
    "/checklist/": ("monthly", "0.8"),
    "/compliance-shield/": ("monthly", "0.8"),
    "/texas-compliance-penalties/": ("monthly", "0.8"),
}
DEFAULT = ("monthly", "0.7")
LOW = {"/privacy.html", "/terms.html"}


# A cache-bust deploy rewrites the ?v= hash in every HTML file, so the naive
# "last commit that touched this file" makes every page look edited on the same
# day. That is just as misleading as a stale date. Walk back until we find a
# commit that changed something a reader would notice.
# Asset-version churn, sitemap dates, and analytics tag lines are all changes a
# reader would never notice — none of them should reset a page's lastmod.
MECHANICAL = re.compile(
    r'^[+-].*?(\?v=[a-f0-9]{6,}|<lastmod>|gtag\(|dataLayer|googletagmanager)')


def _is_content_change(sha, path):
    diff = subprocess.run(["git", "-C", REPO, "show", sha, "--unified=0",
                           "--format=", "--", path],
                          capture_output=True, text=True).stdout
    for line in diff.splitlines():
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")):
            continue
        if MECHANICAL.match(line):
            continue
        return True          # a real edit
    return False             # asset-version churn only


def git_date(path):
    log = subprocess.run(["git", "-C", REPO, "log", "--format=%H %ad",
                          "--date=short", "--", path],
                         capture_output=True, text=True).stdout.strip()
    for line in log.splitlines():
        sha, date = line.split(" ", 1)
        if _is_content_change(sha, path):
            return date
    if log:
        return log.splitlines()[-1].split(" ", 1)[1]
    # Never committed — a new page in the working tree. Today is honest.
    return subprocess.run(["date", "+%Y-%m-%d"], capture_output=True,
                          text=True).stdout.strip()


def main():
    os.chdir(REPO)
    entries = []
    for root, dirs, files in os.walk("."):
        rel = root[2:]
        dirs[:] = [d for d in dirs
                   if d not in SKIP_DIRS and os.path.join(rel, d) not in SKIP_DIRS]
        for f in sorted(files):
            if not f.endswith(".html") or f == "404.html":
                continue
            path = os.path.join(rel, f) if rel else f
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            if re.search(r'<meta name="robots"[^>]*noindex', src):
                continue
            url = "/" + path.replace("index.html", "")
            freq, pri = PRIORITY.get(url, DEFAULT)
            if url in LOW:
                freq, pri = "yearly", "0.3"
            entries.append((url, git_date(path), freq, pri))

    entries.sort(key=lambda e: (-float(e[3]), e[0]))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, date, freq, pri in entries:
        out += ["  <url>", f"    <loc>{BASE}{url}</loc>",
                f"    <lastmod>{date}</lastmod>",
                f"    <changefreq>{freq}</changefreq>",
                f"    <priority>{pri}</priority>", "  </url>"]
    out.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")

    print(f"  {len(entries)} URLs written")
    for url, date, _, pri in entries:
        print(f"    {pri}  {date}  {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
