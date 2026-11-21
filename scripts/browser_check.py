#!/usr/bin/env python3
"""Chromium responsive and interaction checks for the homepage and first five articles."""
from __future__ import annotations
import argparse, json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html","01.html","02.html","03.html","04.html","05.html"]
VIEWPORTS=[(1440,900),(768,1024),(390,844),(360,800)]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="artifacts/browser-qa")
    args=parser.parse_args()
    output=(ROOT/args.output).resolve(); output.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(QuietHandler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    base=f"http://127.0.0.1:{server.server_address[1]}"
    report={"pages":{},"viewports":VIEWPORTS,"interactions":{},"errors":[]}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            for name in PAGES:
                pr={"viewports":{},"console_errors":[],"page_errors":[]}
                page=browser.new_page()
                page.on("pageerror",lambda err,r=pr:r["page_errors"].append(str(err)))
                page.on("console",lambda msg,r=pr:r["console_errors"].append(msg.text) if msg.type=="error" else None)
                for width,height in VIEWPORTS:
                    page.set_viewport_size({"width":width,"height":height})
                    response=page.goto(f"{base}/{name}",wait_until="networkidle")
                    if not response or response.status!=200:
                        report["errors"].append(f"{name}: HTTP response not 200"); continue
                    metrics=page.evaluate("""() => ({width:innerWidth,docWidth:document.documentElement.scrollWidth,h1:document.querySelectorAll('h1').length,images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0}))})""")
                    pr["viewports"][f"{width}x{height}"]=metrics
                    if metrics["docWidth"]>metrics["width"]: report["errors"].append(f"{name}: horizontal overflow at {width}px")
                    if metrics["h1"]!=1: report["errors"].append(f"{name}: expected one H1 at {width}px")
                    for im in metrics["images"]:
                        if not im["loaded"]: report["errors"].append(f"{name}: image failed: {im['src']}")
                    if width in (1440,390,360): page.screenshot(path=str(output/f"{name[:-5]}-{width}.png"),full_page=True)
                if name=="01.html":
                    page.locator('[data-demo="transmission"] button[data-channel="credit"]').click()
                    result=page.locator('[data-demo="transmission"] [data-demo-output]').inner_text()
                    if "信贷渠道" not in result: report["errors"].append("01.html: transmission interaction failed")
                elif name=="02.html":
                    page.locator('[data-demo="money-functions"] button[data-function="store"]').click()
                    result=page.locator('[data-demo="money-functions"] [data-demo-output]').inner_text()
                    if "价值贮藏" not in result: report["errors"].append("02.html: money function interaction failed")
                elif name=="03.html":
                    page.locator('[data-demo="aggregate-classifier"] select').select_option("household_demand")
                    result=page.locator('[data-demo="aggregate-classifier"] [data-demo-output]').inner_text()
                    if "M1" not in result: report["errors"].append("03.html: aggregate classifier interaction failed")
                elif name=="04.html":
                    page.locator('[data-demo="regimes"] button[data-regime="floating"]').click()
                    result=page.locator('[data-demo="regimes"] [data-demo-output]').inner_text()
                    if "浮动汇率" not in result: report["errors"].append("04.html: regime interaction failed")
                elif name=="05.html":
                    page.locator('[data-demo="expected-loss"] input[name="pd"]').fill("5")
                    result=page.locator('[data-demo="expected-loss"] [data-demo-output]').inner_text()
                    if "¥20,000" not in result: report["errors"].append("05.html: expected-loss calculator failed")
                if name!="index.html": report["interactions"][name]=result
                page.emulate_media(media="print")
                pm=page.evaluate("() => ({width:innerWidth,docWidth:document.documentElement.scrollWidth})")
                if pm["docWidth"]>pm["width"]: report["errors"].append(f"{name}: print layout overflow")
                page.close()
                report["pages"][name]=pr
            browser.close()
    finally:
        server.shutdown(); server.server_close()
    for name,pr in report["pages"].items():
        if pr["page_errors"] or pr["console_errors"]: report["errors"].append(f"{name}: console/page errors")
    (output/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    if report["errors"]:
        print("BROWSER QA FAILED")
        for e in report["errors"]: print(f"- {e}")
        return 1
    print("BROWSER QA PASSED")
    print("- homepage + chapters 01–05")
    print("- 1440, 768, 390 and 360px viewports; print emulation")
    print("- one meaningful interaction per article")
    print(f"- artifacts: {output}")
    return 0

if __name__=="__main__": raise SystemExit(main())
