#!/usr/bin/env python3
"""Print a self-contained HTML how-to to PDF using Chrome's own print engine.

qmsWrapper documentation PDFs are produced by printing HTML from Chrome, not by
LaTeX. Matching that pipeline keeps new documents visually identical to the
existing set, and sidesteps LaTeX's problems with the characters these
documents use (checkboxes, arrows) and with fitting oversized screenshots.

Usage:
    html_to_pdf_chrome.py in.html out.pdf
    html_to_pdf_chrome.py in.html out.pdf --cdp http://127.0.0.1:9223
    html_to_pdf_chrome.py in.html out.pdf --landscape --scale 0.9

By default a headless Chromium is launched for the job. Pass --cdp to reuse a
browser you already have open (handy when one is already driving the app under
test).

Page margins are taken from the HTML's own `@page` rule, so styling stays in one
place; that is why the PDF margins here are set to zero.

Needs Playwright:  pip install playwright && playwright install chromium
"""

import argparse
import pathlib
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright is required:\n  pip install playwright\n  playwright install chromium")


def render(src_html, out_pdf, cdp=None, fmt="A4", landscape=False, scale=1.0):
    src = pathlib.Path(src_html).resolve()
    if not src.exists():
        sys.exit(f"no such file: {src}")

    with sync_playwright() as p:
        if cdp:
            browser = p.chromium.connect_over_cdp(cdp)
            ctx = browser.contexts[0] if browser.contexts else browser.new_context()
            page = ctx.new_page()
            close_browser = False
        else:
            browser = p.chromium.launch()
            page = browser.new_page()
            close_browser = True

        page.goto(src.as_uri(), wait_until="networkidle", timeout=120_000)
        # Images are inlined as data URIs by md_to_qmswrapper_html.py, so there is
        # nothing to fetch — this settle is for webfonts and layout only.
        page.wait_for_timeout(2500)

        page.pdf(
            path=out_pdf,
            format=fmt,
            landscape=landscape,
            scale=scale,
            print_background=True,
            # Margins live in the stylesheet's @page rule.
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        page.close()
        if close_browser:
            browser.close()

    print(f"wrote {out_pdf}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("pdf")
    ap.add_argument("--cdp", default=None,
                    help="reuse an existing Chrome, e.g. http://127.0.0.1:9223")
    ap.add_argument("--format", default="A4")
    ap.add_argument("--landscape", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    render(a.html, a.pdf, cdp=a.cdp, fmt=a.format, landscape=a.landscape, scale=a.scale)


if __name__ == "__main__":
    main()
