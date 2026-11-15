# Provenance for evidence/screens/ (Deliverable 4f). Not part of the app or the tests.
# Needs Playwright in a separate venv: pip install playwright && playwright install --with-deps chromium
# Run with the demo app up: JOBSBOARD_DEMO=1 uvicorn jobsboard.api:app --app-dir src
#   python scripts/capture_screens.py http://127.0.0.1:8000 evidence/screens
"""Capture 4f screenshots from the running demo app's Swagger UI (/docs).

Usage: python capture_screens.py <base_url> <out_dir>
Each shot runs one real request through Swagger's "Try it out" -> "Execute" and screenshots
the operation block, which shows the request URL, the status code and the response body.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE, OUT = sys.argv[1], Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

RANKED = "#operations-default-ranked_postings__posting_id__ranked_get"
PIPELINE = "#operations-default-pipeline_postings__posting_id__pipeline_get"

SHOTS = [
    ("ac6.png", RANKED, "demo-ac6"),
    ("ac7.png", RANKED, "demo-ac7"),
    ("ac8-ranked.png", RANKED, "demo-ac8"),
    ("ac8-pipeline.png", PIPELINE, "demo-ac8"),
    ("ac21.png", RANKED, "demo-ac21"),
    ("ac22.png", RANKED, "demo-ac22"),
    ("ac23.png", RANKED, "demo-ac23"),
    ("empty.png", RANKED, "demo-empty"),
    ("404.png", RANKED, "no-such-posting"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, op, posting_id in SHOTS:
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(f"{BASE}/docs")
        block = page.locator(op)
        block.locator(".opblock-summary").click()
        block.get_by_role("button", name="Try it out").click()
        block.locator('input[placeholder="posting_id"]').fill(posting_id)
        block.get_by_role("button", name="Execute").click()
        block.locator(".live-responses-table .response-col_status").first.wait_for()
        page.wait_for_timeout(300)
        block.screenshot(path=str(OUT / name))
        print("saved", name)
        page.close()
    browser.close()
