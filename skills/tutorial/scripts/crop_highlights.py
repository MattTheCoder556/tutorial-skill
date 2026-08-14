#!/usr/bin/env python3
"""Crop UI screenshots down to their annotation highlight, for how-to documents.

A full-window screenshot embedded in a document renders the button you are
pointing at a few pixels wide. This finds the annotation box drawn by
`hl.mark()` (or any solid-colour highlight) and crops around it with padding,
so the target stays legible while keeping enough surroundings to orient the
reader.

Usage:
    crop_highlights.py --map map.json --out /path/to/screenshots
    crop_highlights.py --map map.json --out /path/to/screenshots --colour 230,0,126

`map.json` maps source image path -> output basename (no extension), in the
order they appear in the document:

    {
      "/tmp/shots/step1.png": "01-create-form-button",
      "/tmp/shots/step2.png": "02-name-field"
    }

Images with no detectable highlight are copied whole rather than skipped — a
screenshot with nothing to point at is still a legitimate figure.

Output is always PNG: these are UI captures, so text and thin borders must stay
lossless, and flat UI colour is PNG's best case (it beats JPEG on size here as
well as on quality).

Needs Pillow (`pip install pillow`).
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install pillow")

# Padding around the detected highlight. Top gets less because hl.mark() puts
# its label directly above the box and we want it included, not centred.
PAD_X = 200
PAD_TOP = 90
PAD_BOTTOM = 140

# Never emit a crop smaller than this — a tiny image reads as a mistake even
# when it technically contains the target.
MIN_W = 700
MIN_H = 320

# Sample every Nth pixel when hunting for the highlight. 2 is plenty at normal
# screenshot sizes and roughly 4x faster than every pixel.
STEP = 2


def find_highlight(im, colour, tol=40):
    """Bounding box of pixels close to `colour`, or None."""
    px = im.convert("RGB").load()
    w, h = im.size
    tr, tg, tb = colour
    xs, ys = [], []
    for y in range(0, h, STEP):
        for x in range(0, w, STEP):
            r, g, b = px[x, y]
            if abs(r - tr) < tol and abs(g - tg) < tol + 30 and abs(b - tb) < tol + 10:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def crop_around(im, box):
    w, h = im.size
    x0, y0, x1, y1 = box
    cx0, cy0 = max(0, x0 - PAD_X), max(0, y0 - PAD_TOP)
    cx1, cy1 = min(w, x1 + PAD_X), min(h, y1 + PAD_BOTTOM)
    if cx1 - cx0 < MIN_W:
        extra = (MIN_W - (cx1 - cx0)) // 2
        cx0, cx1 = max(0, cx0 - extra), min(w, cx1 + extra)
    if cy1 - cy0 < MIN_H:
        extra = (MIN_H - (cy1 - cy0)) // 2
        cy0, cy1 = max(0, cy0 - extra), min(h, cy1 + extra)
    return im.crop((cx0, cy0, cx1, cy1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True, help="JSON: source path -> output basename")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--colour", default="230,0,126",
                    help="highlight RGB, default 230,0,126 (hl.mark pink)")
    args = ap.parse_args()

    colour = tuple(int(v) for v in args.colour.split(","))
    mapping = json.load(open(args.map))
    os.makedirs(args.out, exist_ok=True)

    total = 0
    for src, name in mapping.items():
        if not os.path.exists(src):
            print(f"  MISSING  {src}")
            continue
        im = Image.open(src)
        box = find_highlight(im, colour)
        if box:
            im = crop_around(im, box)
            note = ""
        else:
            note = "  (no highlight found - kept whole)"
        dest = os.path.join(args.out, name + ".png")
        im.save(dest, "PNG", optimize=True)
        kb = os.path.getsize(dest) // 1024
        total += kb
        print(f"  {name}.png  {im.size[0]}x{im.size[1]}  {kb}kb{note}")

    print(f"\n{len(mapping)} images, {total}kb total -> {args.out}")


if __name__ == "__main__":
    main()
