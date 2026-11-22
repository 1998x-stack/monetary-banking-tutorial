#!/usr/bin/env python3
"""Audit all evidence URLs without mislabeling syntactic checks as live verification.

Default offline mode is deterministic and suitable for every PR.
Optional --live checks HTTP response codes, classifying bot blocking and temporary
errors separately from confirmed success. It never modifies source ledgers.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
VALID_STATES = {"verified", "derived", "illustrative", "unverified"}


def allowed_url(url: str) -> bool:
    try:
        parsed = urlsplit(url)
        if parsed.scheme not in {"https", "http"} or not parsed.hostname:
            return False
        host = parsed.hostname.lower()
        if host in {"localhost", "localhost.localdomain"} or host.endswith((".local", ".internal", ".test")):
            return False
        try:
            ipaddress.ip_address(host)
            return False  # Evidence must cite public provider hostnames, not raw IP literals.
        except ValueError:
            return "." in host
    except ValueError:
        return False


def collect(root: Path = ROOT) -> dict:
    errors = []
    records = []
    for chapter in range(1, 29):
        file = root / "evidence" / f"chapter-{chapter:02d}.json"
        if not file.is_file():
            errors.append(f"Missing ledger: {file.name}")
            continue
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            if data.get("article") != f"{chapter:02d}.html":
                errors.append(f"{file.name}: incorrect article reference")
            ids = set()
            for claim in data["claims"]:
                claim_id = claim.get("id")
                if not claim_id or claim_id in ids:
                    errors.append(f"{file.name}: missing or duplicate claim ID {claim_id!r}")
                ids.add(claim_id)
                status = claim.get("status", "")
                if status not in VALID_STATES:
                    errors.append(f"{file.name}/{claim_id}: unknown evidence status {status!r}")
                url = (claim.get("source_url") or "").strip()
                if url and not allowed_url(url):
                    errors.append(f"{file.name}/{claim_id}: invalid external source URL")
                if status in {"verified", "derived"} and not url:
                    errors.append(f"{file.name}/{claim_id}: sourced claim without external reference")
                records.append({"chapter": f"{chapter:02d}", "claim_id": claim_id, "status": status, "url": url})
            if not any(c.get("id") == "second-pass-worked-case" for c in data["claims"]):
                errors.append(f"{file.name}: missing second-pass worked case evidence")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{file.name}: invalid JSON ledger: {exc}")
    urls = sorted({x["url"] for x in records if x["url"]})
    domains = Counter(urlsplit(u).hostname for u in urls)
    return {
        "mode": "offline",
        "chapter_count": 28,
        "claims": len(records),
        "unique_urls": len(urls),
        "urls": urls,
        "domains": dict(domains.most_common()),
        "errors": errors,
        "warning": "Offline mode verifies ledger structure and URL syntax only, not HTTP reachability or source content.",
    }


def check_live(url: str, timeout: float) -> dict:
    if not allowed_url(url):
        return {"url": url, "state": "invalid"}
    headers = {"User-Agent": "MonetaryBankingTutorialSourceAudit/1.0 (GitHub Pages educational source-checker)"}
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return {"url": url, "state": "reachable", "status": response.status, "method": method}
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403, 429):
                if method == "HEAD":
                    continue
                return {"url": url, "state": "blocked_or_rate_limited", "status": exc.code}
            if exc.code in (405, 501) and method == "HEAD":
                continue
            if 400 <= exc.code < 500:
                return {"url": url, "state": "http_client_error", "status": exc.code}
            return {"url": url, "state": "http_server_error", "status": exc.code}
        except (urllib.error.URLError, TimeoutError, OSError, socket.timeout) as exc:
            if method == "HEAD":
                continue
            return {"url": url, "state": "unreachable_or_timeout", "error": type(exc).__name__}
    return {"url": url, "state": "not_verified"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Make external HTTP requests (not run in standard PR CI).")
    parser.add_argument("--limit", type=int, default=0, help="Number of unique links checked live; 0 means all.")
    parser.add_argument("--timeout", type=float, default=7.0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON audit report path.")
    args = parser.parse_args()
    report = collect()
    if args.live and not report["errors"]:
        links = report["urls"][:args.limit] if args.limit > 0 else report["urls"]
        with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 10))) as pool:
            results = list(pool.map(lambda url: check_live(url, args.timeout), links))
        report["mode"] = "live"
        report["live_checked"] = len(results)
        report["live_states"] = dict(Counter(x["state"] for x in results))
        report["live_results"] = results
        report["warning"] = ("HTTP reachable does not verify the cited proposition. 403/429 and timeouts are "
                             "NOT evidence of a dead link; compare original publications manually.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"EVIDENCE AUDIT: {report['mode']} | claims={report['claims']} "
          f"unique_urls={report['unique_urls']} errors={len(report['errors'])}")
    for err in report["errors"]:
        print("- "+err)
    if args.live:
        print("Live HTTP states: "+json.dumps(report.get("live_states", {}), ensure_ascii=False))
    print(report["warning"])
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
