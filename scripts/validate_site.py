#!/usr/bin/env python3
"""Static validation for the monetary-banking tutorial."""
from __future__ import annotations
import json, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [f"{n:02d}.html" for n in range(1, 29)]
REBUILT = CHAPTERS[:28]
STATUSES = {"verified", "derived", "illustrative", "unverified"}
BANNED = ("讲义介绍了", "课件介绍了", "上一章已经讲过", "如前文所述")

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set(); self.h1=0; self.images=[]; self.links=[]; self.scripts=[]; self.styles=[]; self.article_count=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag=="h1": self.h1+=1
        if tag=="img": self.images.append((a.get("src",""),a.get("alt","")))
        if tag=="a" and a.get("href"): self.links.append(a["href"])
        if tag=="script" and a.get("src"): self.scripts.append(a["src"])
        if tag=="link" and a.get("rel")=="stylesheet" and a.get("href"): self.styles.append(a["href"])
        if tag=="article": self.article_count+=1

def local_target(source, url):
    parts=urlsplit(url)
    if parts.scheme or parts.netloc: return None
    if not parts.path: return source.resolve()
    return (source.parent/parts.path).resolve()

def validate():
    errors=[]
    required=("README.md","AGENTS.md","index.html","courses.json","scripts/browser_check.py","tests/test_site.py","assets/js/article-demos.js")
    for name in required:
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
        if 'class="stat"><strong>28</strong>' not in raw: errors.append("index.html progress count should show 28 rebuilt chapters")
    for chapter in REBUILT:
        path=ROOT/chapter
        if not path.is_file(): continue
        raw=path.read_text(encoding="utf-8"); doc=Document(); doc.feed(raw)
        if len(raw)<5000: errors.append(f"{chapter}: article is unexpectedly short ({len(raw)} characters)")
        if doc.h1!=1: errors.append(f"{chapter}: expected one H1, got {doc.h1}")
        if doc.article_count!=1: errors.append(f"{chapter}: expected one semantic article, got {doc.article_count}")
        if 'id="references"' not in raw: errors.append(f"{chapter}: missing references section")
        if 'class="article-header"' not in raw or 'class="article-toc"' not in raw: errors.append(f"{chapter}: missing shared article structure")
        for phrase in BANNED:
            if phrase in raw: errors.append(f"{chapter}: banned meta phrase {phrase!r}")
        for src,alt in doc.images:
            if not alt.strip(): errors.append(f"{chapter}: empty image alt: {src}")
            target=local_target(path,src)
            if target and not target.is_file(): errors.append(f"{chapter}: missing image asset {src}")
        for asset in doc.scripts+doc.styles:
            if asset.startswith(("http://","https://","//")): errors.append(f"{chapter}: remote runtime dependency: {asset}")
            target=local_target(path,asset)
            if target and not target.is_file(): errors.append(f"{chapter}: missing runtime asset {asset}")
        for url in doc.links:
            target=local_target(path,url)
            if target is None: continue
            if not target.is_file():
                errors.append(f"{chapter}: broken local link {url}")
                continue
            fragment=urlsplit(url).fragment
            if fragment and target.suffix.lower()==".html":
                target_doc=Document(); target_doc.feed(target.read_text(encoding="utf-8"))
                if fragment not in target_doc.ids: errors.append(f"{chapter}: missing fragment #{fragment} in {target.relative_to(ROOT)}")
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
    for extra in ("examples/analyse_macro.py","examples/sample_macro_data.csv","examples/README.md","tests/test_macro_example.py"):
        if not (ROOT/extra).is_file(): errors.append(f"Missing capstone reproducibility file: {extra}")
    # Deep-audit knowledge graph: all 28 chapters, exactly three causal links each.
    graph_path = ROOT/"knowledge"/"concept-links.json"
    map_path = ROOT/"knowledge-map.html"
    if not graph_path.is_file(): errors.append("Missing knowledge/concept-links.json")
    else:
        try:
            graph=json.loads(graph_path.read_text(encoding="utf-8"))
            records=graph["chapters"]
            if len(records)!=28 or {item["chapter"] for item in records}!={f"{n:02d}" for n in range(1,29)}:
                errors.append("Knowledge graph must cover exactly chapters 01–28")
            seen=set()
            for item in records:
                chapter=item["chapter"]
                if chapter in seen: errors.append(f"Duplicate knowledge graph record {chapter}")
                seen.add(chapter)
                relations=item.get("related",[])
                if len(relations)!=3: errors.append(f"{chapter}: expected three curated cross-links")
                raw=(ROOT/f"{chapter}.html").read_text(encoding="utf-8")
                if raw.count('class="concept-link"')!=3:
                    errors.append(f"{chapter}: expected three rendered concept cards")
                if 'id="concept-bridge"' not in raw:
                    errors.append(f"{chapter}: missing concept bridge")
                for rel in relations:
                    target=ROOT/f"{rel['to']}.html"
                    if not target.is_file():
                        errors.append(f"{chapter}: missing linked article {rel['to']}")
                        continue
                    if rel["to"]==chapter: errors.append(f"{chapter}: must not self-link")
                    if len(rel.get("label","").strip())<5 or len(rel.get("why","").strip())<10:
                        errors.append(f"{chapter}: relation needs meaningful title and explanation")
                    dest=Document();dest.feed(target.read_text(encoding="utf-8"))
                    if rel["anchor"] not in dest.ids:
                        errors.append(f"{chapter}: bad graph fragment {rel['to']}.html#{rel['anchor']}")
                    if f'href="{rel["to"]}.html#{rel["anchor"]}"' not in raw:
                        errors.append(f"{chapter}: graph relation not rendered {rel['to']}#{rel['anchor']}")
        except Exception as exc: errors.append(f"Knowledge graph validation failed: {exc}")
    if not map_path.is_file(): errors.append("Missing knowledge-map.html")
    else:
        map_raw=map_path.read_text(encoding="utf-8")
        map_doc=Document();map_doc.feed(map_raw)
        if map_doc.h1!=1 or map_raw.count('class="knowledge-card"')!=28:
            errors.append("Knowledge map must have one H1 and 28 chapter cards")
        for href in map_doc.links:
            target=local_target(map_path,href)
            if target is None: continue
            if not target.is_file(): errors.append(f"Knowledge map broken link: {href}");continue
            fragment=urlsplit(href).fragment
            if fragment and target.suffix==".html":
                target_doc=Document();target_doc.feed(target.read_text(encoding="utf-8"))
                if fragment not in target_doc.ids:
                    errors.append(f"Knowledge map broken fragment: {href}")
    if (ROOT/"index.html").is_file() and 'href="knowledge-map.html"' not in (ROOT/"index.html").read_text(encoding="utf-8"):
        errors.append("Homepage must link the knowledge map")
    for svg in (ROOT/"assets"/"diagrams").glob("*.svg"):
        raw=svg.read_text(encoding="utf-8")
        if "<title" not in raw or "<desc" not in raw or "viewBox=" not in raw: errors.append(f"{svg.relative_to(ROOT)}: SVG needs title, desc and viewBox")
    return errors

def main():
    errors=validate()
    if errors:
        print("SITE VALIDATION FAILED")
        for error in errors: print(f"- {error}")
        return 1
    print("SITE VALIDATION PASSED")
    print("- 28 chapter files and course metadata")
    print("- chapters 01–28: standalone structure, local assets, links and evidence ledgers")
    print("- 84 cross-chapter concept links, 28 course-map cards and target anchors")
    print("- SVG accessibility metadata and offline runtime dependencies")
    return 0

if __name__=="__main__": sys.exit(main())
