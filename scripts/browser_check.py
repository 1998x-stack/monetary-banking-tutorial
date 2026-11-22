#!/usr/bin/env python3
"""Chromium responsive and interaction checks for the homepage and chapters 01–28."""
from __future__ import annotations
import argparse, json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html"]+[f"{n:02d}.html" for n in range(1,29)]
VIEWPORTS=[(1440,900),(768,1024),(390,844),(360,800)]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

def check_interaction(page, name):
    actions={
      "01.html":('[data-demo="transmission"] button[data-channel="credit"]','click','信贷渠道'),
      "02.html":('[data-demo="money-functions"] button[data-function="store"]','click','价值贮藏'),
      "03.html":('[data-demo="aggregate-classifier"] select','select','M1'),
      "04.html":('[data-demo="regimes"] button[data-regime="floating"]','click','浮动汇率'),
      "05.html":('[data-demo="expected-loss"] input[name="pd"]','fill','¥20,000'),
      "06.html":('[data-demo="fisher"] input[name="nominal"]','fill','精确实际利率'),
      "07.html":('[data-demo="yield-curve"] button[data-shape="inverted"]','click','倒挂'),
      "08.html":('[data-demo="nim"] input[name="interest-income"]','fill','2.50%'),
      "09.html":('[data-demo="capital-ratio"] input[name="cet1"]','fill','5.00%'),
      "10.html":('[data-demo="central-bank"] button[data-operation="drain"]','click','回笼流动性'),
      "11.html":('[data-demo="repo-cost"] input[name="rate"]','fill','利息约'),
      "12.html":('[data-demo="bond-price"] input[name="yield"]','fill','折价'),
      "13.html":('[data-demo="fx-parity"] input[name="spot"]','fill','73,000'),
      "14.html":('[data-demo="nbfi-risk"] button[data-risk="leverage"]','click','杠杆与保证金'),
      "15.html":('[data-demo="money-multiplier"] input[name="currency-ratio"]','fill','乘数约'),
      "16.html":('[data-demo="money-demand"] input[name="interest-rate"]','fill','实际货币需求约为'),
      "17.html":('[data-demo="policy-tools"] button[data-tool="rrr"]','click','准备金率'),
      "18.html":('[data-demo="transmission-lab"] button[data-channel="credit"]','click','信贷渠道'),
      "19.html":('[data-demo="islm"] input[name="government-spending"]','fill','均衡产出'),
      "20.html":('[data-demo="inflation-rate"] input[name="current-index"]','fill','4.00%'),
      "21.html":('[data-demo="deflation"] input[name="expected-inflation"]','fill','实际利率约'),
      "22.html":('[data-demo="crisis-leverage"] input[name="shock"]','fill','100.00%'),
      "23.html":('[data-demo="report-reading"] button[data-kind="projection"]','click','成员预测'),
      "24.html":('[data-demo="fin-data-growth"] input[name="tsf-new"]','fill','增速差 4.00'),
      "25.html":('[data-demo="taylor-rule"] input[name="inflation"]','fill','6.50%'),
      "26.html":('[data-demo="digital-money"] button[data-kind="ecny"]','click','2026 年新框架'),
      "27.html":('[data-demo="stablecoin-cover"] input[name="haircut"]','fill','84.00%'),
      "28.html":('[data-demo="macro-scenarios"] button[data-scenario="supply"]','click','供给冲击情景')
    }
    selector, action, expected=actions[name]
    control=page.locator(selector)
    if action=="click": control.click()
    elif action=="select": control.select_option("household_demand")
    elif name=="05.html": control.fill("5")
    elif name=="06.html": control.fill("5")
    elif name=="08.html": control.fill("200")
    elif name=="09.html": control.fill("50")
    elif name=="11.html": control.fill("3")
    elif name=="12.html": control.fill("5")
    elif name=="13.html": control.fill("7.3")
    elif name=="15.html": control.fill("20")
    elif name=="16.html": control.fill("4")
    elif name=="19.html": control.fill("40")
    elif name=="20.html": control.fill("104")
    elif name=="21.html": control.fill("-3")
    elif name=="22.html": control.fill("20")
    elif name=="24.html": control.fill("440")
    elif name=="25.html": control.fill("4")
    elif name=="27.html": control.fill("20")
    result=page.locator('[data-demo-output]').last.inner_text()
    if expected not in result:
        raise AssertionError(f"{name}: expected interaction output containing {expected!r}, got {result!r}")
    return result

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
                page_report={"viewports":{},"console_errors":[],"page_errors":[]}
                page=browser.new_page()
                page.on("pageerror",lambda err,r=page_report:r["page_errors"].append(str(err)))
                page.on("console",lambda msg,r=page_report:r["console_errors"].append(msg.text) if msg.type=="error" else None)
                for width,height in VIEWPORTS:
                    page.set_viewport_size({"width":width,"height":height})
                    response=page.goto(f"{base}/{name}",wait_until="networkidle")
                    if not response or response.status!=200:
                        report["errors"].append(f"{name}: HTTP response not 200"); continue
                    metrics=page.evaluate("""() => ({width:innerWidth,docWidth:document.documentElement.scrollWidth,h1:document.querySelectorAll('h1').length,images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0}))})""")
                    page_report["viewports"][f"{width}x{height}"]=metrics
                    if metrics["docWidth"]>metrics["width"]: report["errors"].append(f"{name}: horizontal overflow at {width}px")
                    if metrics["h1"]!=1: report["errors"].append(f"{name}: expected one H1 at {width}px")
                    for image in metrics["images"]:
                        if not image["loaded"]: report["errors"].append(f"{name}: image failed: {image['src']}")
                    if width in (1440,390,360): page.screenshot(path=str(output/f"{name.replace('.html','')}-{width}.png"),full_page=True)
                if name!="index.html":
                    try: report["interactions"][name]=check_interaction(page,name)
                    except Exception as exc: report["errors"].append(str(exc))
                page.emulate_media(media="print")
                print_metrics=page.evaluate("() => ({width:innerWidth,docWidth:document.documentElement.scrollWidth})")
                if print_metrics["docWidth"]>print_metrics["width"]: report["errors"].append(f"{name}: print layout overflow")
                page.close(); report["pages"][name]=page_report
            browser.close()
    finally:
        server.shutdown(); server.server_close()
    for name,result in report["pages"].items():
        if result["page_errors"] or result["console_errors"]: report["errors"].append(f"{name}: console/page errors")
    (output/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    if report["errors"]:
        print("BROWSER QA FAILED")
        for error in report["errors"]: print(f"- {error}")
        print(f"Report: {output/'report.json'}")
        return 1
    print("BROWSER QA PASSED")
    print("- homepage + chapters 01–28")
    print("- 1440, 768, 390 and 360px viewports; print emulation")
    print("- 28 meaningful article interactions")
    print(f"- artifacts: {output}")
    return 0

if __name__=="__main__": raise SystemExit(main())
