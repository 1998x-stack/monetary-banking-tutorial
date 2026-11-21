#!/usr/bin/env python3
"""Static validation for the monetary-banking tutorial."""
from __future__ import annotations
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [f"{n:02d}.html" for n in range(1, 29)]
STATUSES = {"verified", "derived", "illustrative", "unverified"}
BANNED = ("讲义介绍了", "课件介绍了", "上一章已经讲过", "如前文所述")

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set(); self.h1=0; self.images=[]; self.links=[]; self.scripts=[]; self.styles=[]; self.article=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag=="h1": self.h1+=1
        if tag=="img": self.images.append((a.get("src",""),a.get("alt","")))
        if tag=="a" and a.get("href"): self.links.append(a["href"])
        if tag=="script" and a.get("src"): self.scripts.append(a["src"])
        if tag=="link" and a.get("rel")=="stylesheet" and a.get("href"): self.styles.append(a["href"])
        if tag=="article": self.article=True

def local_target(source, url):
    p=urlsplit(url)
    if p.scheme or p.netloc or not p.path: return None
    return (source.parent/p.path).resolve()

def validate():
    errors=[]
    for name in ("README.md","AGENTS.md","index.html","courses.json","scripts/browser_check.py","tests/test_site.py"):
        if not (ROOT/name).is_file(): errors.append(f"Missing required file: {name}")
    for name in CHAPTERS:
        if not (ROOT/name).is_file(): errors.append(f"Missing chapter: {name}")
    try:
        data=json.loads((ROOT/"courses.json").read_text(encoding="utf-8")); entries=data["chapters"]
        if len(entries)!=28: errors.append(f"courses.json must contain 28 chapters; found {len(entries)}")
        for item in entries:
            if not (ROOT/item["file"]).is_file(): errors.append(f"Missing course target: {item.get('file')}")
    except Exception as exc:
        errors.append(f"courses.json invalid: {exc}")
    if (ROOT/"index.html").is_file():
        raw=(ROOT/"index.html").read_text(encoding="utf-8")
        if raw.count('class="chapter-card"')!=28: errors.append("index.html must contain 28 static chapter cards")
        if "fetch('courses.json')" in raw or 'fetch("courses.json")' in raw: errors.append("index.html must not fetch courses.json")
    for chapter in CHAPTERS[:5]:
        path=ROOT/chapter
        if not path.is_file(): continue
        raw=path.read_text(encoding="utf-8"); doc=Document(); doc.feed(raw)
        if doc.h1!=1: errors.append(f"{chapter}: expected one H1, got {doc.h1}")
        if not doc.article: errors.append(f"{chapter}: missing semantic article")
        if 'id="references"' not in raw: errors.append(f"{chapter}: missing references section")
        for phrase in BANNED:
            if phrase in raw: errors.append(f"{chapter}: banned meta phrase {phrase!r}")
        for src,alt in doc.images:
            if not alt.strip(): errors.append(f"{chapter}: empty image alt: {src}")
        for asset in doc.scripts+doc.styles:
            if asset.startswith(("http://","https://","//")): errors.append(f"{chapter}: remote runtime dependency: {asset}")
        for url in doc.links:
            target=local_target(path,url)
            if target is None: continue
            if not target.is_file(): errors.append(f"{chapter}: broken local link {url}")
        ledger=ROOT/"evidence"/f"chapter-{chapter[:2]}.json"
        if not ledger.is_file(): errors.append(f"{chapter}: missing evidence ledger"); continue
        try:
            evidence=json.loads(ledger.read_text(encoding="utf-8"))
            if evidence.get("article")!=chapter: errors.append(f"{ledger.name}: article path mismatch")
            if not evidence.get("claims"): errors.append(f"{ledger.name}: no claims")
            for claim in evidence.get("claims",[]):
                if claim.get("status") not in STATUSES: errors.append(f"{ledger.name}: invalid status for {claim.get('id')}")
                if claim.get("status")!="illustrative" and not claim.get("source_url"): errors.append(f"{ledger.name}: missing source for {claim.get('id')}")
        except Exception as exc: errors.append(f"{ledger.name}: invalid JSON: {exc}")
    for svg in (ROOT/"assets"/"diagrams").glob("*.svg"):
        raw=svg.read_text(encoding="utf-8")
        if "<title" not in raw or "<desc" not in raw or "viewBox=" not in raw: errors.append(f"{svg.relative_to(ROOT)}: SVG needs title, desc and viewBox")
    return errors

def main():
    errors=validate()
    if errors:
        print("SITE VALIDATION FAILED")
        for e in errors: print(f"- {e}")
        return 1
    print("SITE VALIDATION PASSED")
    print("- 28 chapter files and 28 course entries")
    print("- first five articles: structure, local links, references and evidence ledgers")
    print("- SVG accessibility metadata and offline runtime dependencies")
    return 0

if __name__=="__main__": sys.exit(main())
