# tutorial-skill

A Claude Code plugin that turns a feature you have driven — or a module guide —
into **end-user documentation with annotated screenshots**: what the module is
for, and how someone doing their job gets each task done.

It is the customer-facing counterpart to
[howto-skill](https://github.com/MattTheCoder556/howto-skill). Same house style,
same PDF pipeline, same filename convention — different reader.

Ships the same skill for **Claude Cowork** too.

## Install (Claude Code)

```bash
claude plugin marketplace add MattTheCoder556/tutorial-skill
claude plugin install tutorial@tutorial-skill
```

Restart Claude Code. You now have `/tutorial` in every project.

Update later with `claude plugin update tutorial`.

## Install (Claude Cowork)

Copy `cowork-skill/` into your Cowork skills directory as `tutorial/`.

## `tutorial` or `howto`?

They produce the same *kind* of artefact and share the whole screenshot and PDF
pipeline. What differs is who reads it, and that changes almost every editorial
decision:

| `howto` (tester) | `tutorial` (user) |
|---|---|
| `> **Can you do it?** ☐` closes every task | no checkboxes anywhere |
| Walks the reader into a known defect so they confirm it | never documents a path that does not work |
| "Tell us where you had to guess" is the real output | the document *is* the output; nothing is sent back |
| Sections numbered to match a validation sheet (`1.4`, `2.1`) | sections ordered by what the user is trying to do |
| Footer names which tasks are expected to fail | footer names the product version described |
| DEV banner and test data acceptable internally | clean tenant only, neutral sample data |
| Assumes the reader knows the module | opens by explaining what the module is for |

Use `howto` to find out whether people can use the software. Use `tutorial` to
tell them how.

## What it produces

Every run produces **both**, never one or the other:

- **PDF in the qmsWrapper *Documentation* house style** — logo header, near-black
  headings on white, humanist sans, full-width bordered screenshots
- **Markdown + a `screenshots/` folder** — the editable source the PDF is built
  from, and what you edit for the next revision

Word (`.docx`) and single-file HTML are available on request, in addition to
those two rather than instead of them.

Both files are named by the house convention, differing only in extension:

```
qmsWrapper_<Module>_<YYYY-MM-DD>_<HHMM>_v<N>.<ext>
qmsWrapper_FormBuilder_2026-08-14_1432_v1.pdf
qmsWrapper_FormBuilder_2026-08-14_1432_v1.md
```

`<Module>` comes from `reference/modules.md` — the module registry shared with
the validation and how-to skills — so a user guide can be tied back to the
module it documents. The modules formerly called *Form Editor* and *Process
Editor* are **Form Builder** and **Process Builder**.

The PDF is produced by **printing HTML from Chrome**, which is how the existing
qmsWrapper documentation PDFs were made. It is deliberately *not* pandoc +
LaTeX: `pdflatex` cannot render `→ ▾ ⚠` without a per-character preamble, needs
`adjustbox` to stop oversized screenshots overflowing, and the result looks like
a LaTeX article rather than product documentation.

## The document it writes

- **What this is for** — what the module does and when someone reaches for it.
  A tester knows already; a customer opening the guide may not.
- **Before you start** — role, permission, tier, and anything that must already
  exist. If the reader lacks one, what they will see instead and who to ask.
- **Terms you will see** — only where the product's vocabulary is not
  self-evident, and only the terms this document uses.
- **One section per task**, ordered the way a real user meets them — the common
  path first — not in the order a validation sheet happens to list them.
- **Tips and shortcuts** inline, marked optional so nobody mistakes one for a
  required step.
- **If something does not look right** — symptom, cause, what to do.
- **Where to go next**, then a footer naming the product version described.

## Four rules the skill will not bend

1. **Every navigation path is shown, not just written.** The moment the text
   says *Settings → Approvals*, a screenshot of that trail goes beside it with
   the route marked. An arrow chain is directions the reader has to translate
   into a screen they may never have opened; a picture of the menu is something
   they recognise at a glance. The written path stays in the prose too, so the
   document still works when someone searches it for "Approvals".
2. **It always includes screenshots, and every one is annotated.** Each figure
   carries a pink box and label on the target with the rest of the page dimmed,
   then is cropped to it — so the reader is never left searching a full-window
   capture for the button. If screenshots cannot be captured the skill says so
   and asks, rather than quietly shipping a wall of text.
3. **It always delivers the PDF and the Markdown together.** The format is not a
   question; only where the document goes is, and it asks that before writing
   anything. A PDF with no source to regenerate it from is not a deliverable.
4. **It never documents a path that does not work.** Where the product is
   broken, the order is: document a working route to the same outcome; failing
   that, document a supported workaround as normal procedure; failing that, drop
   the task and say which one was dropped and why. Telling a customer "this is a
   known defect, note what you saw" is not documentation. Nothing from the
   tester's copy reaches the reader — not the checkboxes, not the
   defect-confirmation callouts, and not the internal identifiers that tag them
   (validation test IDs like `MAN-03`, defect tickets like `QM-4`).

Image format is **PNG** and is not offered as a choice: lossless text so small
labels survive, flat UI colour is PNG's best case (it beats JPEG on size *and*
quality here), and it is supported everywhere.

## Scripts

| Script | Does |
|---|---|
| `highlight.py` | Draws the annotation on a **live** page you are driving with Playwright — pink box, label, rest of the page dimmed — before you capture. Position comes from the element's own bounding box. |
| `annotate_screenshot.py` | Draws the same annotation onto a PNG you **already have**. For captures that predate the document, targets with no element of their own (a pair of table columns), or one capture illustrating two steps. |
| `crop_highlights.py` | Finds the annotation highlight in a screenshot and crops around it with padding. A full-window capture renders the button ~8px wide once embedded; this fixes that. |
| `md_to_qmswrapper_html.py` | Markdown → self-contained styled HTML. Inlines every image as base64, so there are never missing-image boxes. |
| `html_to_pdf_chrome.py` | Drives Chrome's print engine to produce the PDF. Launches headless by default, or reuses an open browser with `--cdp`. |

All three annotation scripts agree on `#e6007e`, so annotate → crop chains
without configuration.

### Typical run

```bash
# 1. annotate — either while driving the UI (highlight.py, inside your script)
#    or afterwards, on captures you already have:
python3 scripts/annotate_screenshot.py --spec figures.json

# 2. crop each annotation down to its target
python3 scripts/crop_highlights.py --map map.json --out doc/screenshots

# 3. markdown -> styled, self-contained HTML
python3 scripts/md_to_qmswrapper_html.py \
        doc/qmsWrapper_FormBuilder_2026-08-14_1432_v1.md /tmp/out.html \
        screenshots assets/qmswrapper-logo.png

# 4. HTML -> PDF via Chrome, same name as the Markdown
python3 scripts/html_to_pdf_chrome.py /tmp/out.html \
        doc/qmsWrapper_FormBuilder_2026-08-14_1432_v1.pdf
```

`map.json` maps capture path → output basename, numbered in document order;
`figures.json` places the boxes:

```json
{
  "/tmp/shots/step1.png": "01-create-button",
  "/tmp/shots/step2.png": "02-name-field"
}
```

```json
[
  {"src": "/tmp/shots/step1.png", "out": "/tmp/annotated/01-create-button.png",
   "regions": [{"box": [1315, 130, 128, 29], "label": "1. Click + Create Form"}]}
]
```

## Requirements

- **Pillow** — `pip install pillow` (annotating and cropping)
- **Playwright + Chromium** — `pip install playwright && playwright install chromium` (PDF)
- **pandoc** — optional, only for `.docx` output

## Notes

- Keep the Markdown and its `screenshots/` folder together — image links are
  relative, and moving one without the other breaks the pictures.
- Regenerate the PDF from the Markdown after edits rather than editing the PDF.
- Capture on a clean tenant: no DEV banner, no test records, no colleagues'
  names. This is a hard rule here rather than a note — a customer reading their
  own documentation must see something that looks like their own system. Treat
  screenshots as controlled content that needs recapturing whenever the UI
  changes, and move the version footer with them.
- Tell the reader the pink boxes and dimming are added for the guide and are not
  part of the product, or someone will hunt for a pink box on their screen.
- `assets/qmswrapper-logo.png` is the brand mark used in the PDF header.

## Licence

MIT
