#!/usr/bin/env python3
"""Draw "click here" annotations onto a screenshot: box, label, dimmed surroundings.

A plain screenshot shows the reader the page. It does not show them *which* of
the six similar buttons on that page to press. This draws the same annotation
`highlight.py` draws in a live browser — a pink box round the target, a labelled
tag above it, and the rest of the page dimmed — but onto a PNG you already have,
so captures taken before anyone thought about documentation can still be used.

Prefer `highlight.py` when you are driving the UI: it takes the target's real
position from the DOM, so it cannot be a few pixels out. Use this when the
capture already exists, when you need to point at something with no element of
its own (a group of table columns, a region of a canvas), or when one screenshot
has to illustrate two different steps.

The colour matches `crop_highlights.py`'s default, so the output can be fed
straight into it and cropped down to the annotation.

Usage:
    annotate_screenshot.py --spec figures.json
    annotate_screenshot.py in.png out.png --box 1315,131,129,29 --label "1. Click Create Form"
    annotate_screenshot.py in.png out.png --box 10,20,80,40 --label "1. First" \\
                                          --box 10,90,80,40 --label "2. Then this"

`figures.json` is a list of figures, in document order:

    [
      {
        "src": "/tmp/shots/forms.png",
        "out": "screenshots/01-create-form-button.png",
        "regions": [
          {"box": [1315, 131, 129, 29], "label": "1. Click + Create Form"}
        ]
      }
    ]

`box` is [x, y, width, height] in pixels of the source image. Several regions on
one figure are how you show an ordered pair of clicks — number the labels.

`label_pos` is "above" (default) or "below". Use "below" when a tag above would
land on top of another region: the annotation must never hide the thing the
reader is being asked to look at.

Needs Pillow (`pip install pillow`).
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  pip install pillow")

# Matched to highlight.py / hl.mark() so both routes produce the same picture,
# and to crop_highlights.py's default so its detector finds this.
PINK = (230, 0, 126)          # #e6007e
DIM = 0.35                    # how far the un-highlighted page is knocked back
BORDER = 3                    # box stroke width
INSET = -5                    # negative: the box sits just outside the target
RADIUS = 6
LABEL_SIZE = 15
LABEL_PAD_X, LABEL_PAD_Y = 10, 5
LABEL_GAP = 6                 # between the label tag and the box

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    # Bitmap fallback: ugly at this size, but a missing font must not stop a
    # document being produced.
    return ImageFont.load_default()


def text_size(draw, text, font):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def annotate(src, out, regions):
    im = Image.open(src).convert("RGB")
    w, h = im.size

    boxes = []
    for r in regions:
        x, y, bw, bh = (int(v) for v in r["box"])
        where = r.get("label_pos", "above")
        # Clamp to the image: a box hanging off the edge draws a stroke along
        # the border and looks like a rendering fault rather than a pointer.
        x0, y0 = max(0, x + INSET), max(0, y + INSET)
        x1, y1 = min(w, x + bw - INSET), min(h, y + bh - INSET)
        if x1 <= x0 or y1 <= y0:
            sys.exit(f"{src}: region {r['box']} is outside the {w}x{h} image")
        boxes.append(((x0, y0, x1, y1), r.get("label", ""), where))

    # Dim everything, then restore the targets — so the reader's eye lands on
    # the one place that is still at full brightness.
    shaded = Image.blend(im, Image.new("RGB", im.size, (0, 0, 0)), DIM)
    for (x0, y0, x1, y1), _, _ in boxes:
        shaded.paste(im.crop((x0, y0, x1, y1)), (x0, y0))

    draw = ImageDraw.Draw(shaded)
    font = load_font(LABEL_SIZE)

    for (x0, y0, x1, y1), label, where in boxes:
        draw.rounded_rectangle((x0, y0, x1, y1), radius=RADIUS,
                               outline=PINK, width=BORDER)
        if not label:
            continue

        tw, th = text_size(draw, label, font)
        tag_w, tag_h = tw + 2 * LABEL_PAD_X, th + 2 * LABEL_PAD_Y
        tag_x = min(max(0, x0), w - tag_w)
        above, below = y0 - tag_h - LABEL_GAP, y1 + LABEL_GAP
        # "below" is for the second of two stacked targets, where a tag above
        # would cover the first one — the thing the reader is meant to see.
        tag_y = below if where == "below" else above
        if tag_y < 0:
            tag_y = below
        tag_y = min(max(0, tag_y), h - tag_h)

        draw.rounded_rectangle((tag_x, tag_y, tag_x + tag_w, tag_y + tag_h),
                               radius=4, fill=PINK)
        draw.text((tag_x + LABEL_PAD_X, tag_y + LABEL_PAD_Y), label,
                  font=font, fill=(255, 255, 255))

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    shaded.save(out, "PNG")
    print(f"annotated {len(boxes)} region(s) -> {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", nargs="?", help="source PNG")
    ap.add_argument("out", nargs="?", help="annotated PNG to write")
    ap.add_argument("--box", action="append", default=[],
                    help="x,y,width,height of a target; repeatable")
    ap.add_argument("--label", action="append", default=[],
                    help="label for the matching --box; repeatable")
    ap.add_argument("--spec", help="JSON file of figures, processed in order")
    args = ap.parse_args()

    if args.spec:
        figures = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        for fig in figures:
            annotate(fig["src"], fig["out"], fig["regions"])
        return

    if not (args.src and args.out and args.box):
        ap.error("need src, out and at least one --box (or --spec)")
    if args.label and len(args.label) != len(args.box):
        ap.error(f"{len(args.box)} --box but {len(args.label)} --label; they pair up")

    regions = [
        {"box": [int(v) for v in b.split(",")],
         "label": args.label[i] if i < len(args.label) else ""}
        for i, b in enumerate(args.box)
    ]
    annotate(args.src, args.out, regions)


if __name__ == "__main__":
    main()
