---
name: tutorial
description: >-
  Turn a feature you have driven — or a module guide — into user documentation
  with annotated screenshots: what the module is for, and how someone doing
  their job gets each task done. Same qmsWrapper house style as a validation
  how-to, but written for the customer rather than the tester: no checkboxes,
  no defect confirmations, no feedback to send back. Always includes
  screenshots; always delivers three files — a .pdf in the qmsWrapper house
  style, the self-contained .html it was printed from, and the .md that
  produced both.
  Trigger: the user types `/tutorial`, or says "write user documentation",
  "write the manual page for <X>", "document this feature for customers",
  "make an end-user guide".
---

# /tutorial — feature → end-user documentation with screenshots

Produces the document a customer reads to get their work done: what the module
is for, what they need before they start, and how to complete each task without
anyone sitting next to them.

**Two things are non-negotiable: it always contains screenshots, and it always
comes out as three files — a `.pdf`, the `.html` it was printed from, and the
`.md` that produced both.**

The PDF is the readable artefact — house style, circulated, published, filed as
a controlled record. The HTML is the same document for the web: one
self-contained file with every screenshot inlined, so it can be attached to a
ticket, dropped into a knowledge base or opened in a browser with no
`screenshots/` folder beside it. The Markdown is the editable source, and the
`screenshots/` folder belongs with it. Ship the PDF without the Markdown and the
next revision has nowhere to start from: nobody edits a PDF, they regenerate it.

## Not the same document as `/howto`

`/howto` writes a *validation* how-to: it walks a tester through a matrix,
closes every task with a **Can you do it?** box, warns them that a step is a
known defect and asks them to confirm it, and treats the friction they report
as the real output.

None of that belongs in front of a customer. Here the reader is not being
tested and is not reporting back — they are trying to finish a job. So:

| `/howto` (tester) | `/tutorial` (user) |
|---|---|
| `> **Can you do it?** ☐` closes every task | no checkboxes anywhere |
| Walks the reader into a known defect to confirm it | never documents a path that does not work — see §4 |
| "Tell us where you had to guess" is the point | the document is the deliverable; no feedback ask |
| Sections numbered to match a validation sheet (`1.4`, `2.1`) | sections ordered by what the user is trying to do |
| Footer names which tasks are expected to fail | footer names the product version the document describes |
| DEV banner and test data acceptable internally | clean tenant only — see §2 |
| Assumes the reader knows the module | opens by explaining what the module is for |

If what is actually wanted is a validation pass — "can users do this unaided?"
— that is `/howto`, and this skill is the wrong one. Say so rather than
producing a customer document with checkboxes bolted on.

## 1. Gather the source

In order of preference:

1. **A session where you drove the UI** — the click paths are known to be real,
   and so is what the screens actually say. This is the best case.
2. **Module guides or the QMS manual** — good for what a module is *for* and
   the vocabulary the product uses; check the click paths still hold.
3. **A validation sheet** (`… Use Requirements.xlsx`) — usable as a checklist of
   what exists, but do not inherit its shape. Requirement order is not user
   order, and requirement wording is not user wording.

Never invent a click path. If you have not seen the screen and no document
describes it, the honest move is to drive the UI and find out, or leave that
task out and say so.

**Never carry a defect across as an instruction.** If the source records a
failure, see §4 — the handling is the opposite of `/howto`'s.

## 2. Screenshots — always, and take them yourself

A guide without pictures is a list of guesses about what the user is looking at.
Capture them.

**What to shoot.** Every click that is not obvious from the page: the entry
point, anything easy to confuse with a neighbour, any multi-step interaction,
and the result the reader should end up looking at. Skip screenshots of typing
into a plainly-labelled text box.

**Every navigation path gets a picture.** The moment the text says *Settings →
Approvals*, *Project → Members*, or any other trail through the menus, a
screenshot of that trail goes beside it. An arrow chain is a set of directions
the reader has to translate into a screen they may never have opened; a picture
of the menu with the route marked is something they recognise at a glance. This
is the most common place a reader stalls, and one capture removes it.

Shoot the menu open at the step being named, with the target marked. Where the
path runs several levels deep, either mark every level on one capture and number
the labels in order, or give a capture per level — whichever reads faster. Keep
the written path in the prose as well: the picture is *in addition to* the
words, never instead of them, so the document still works when someone searches
it for "Approvals".

**Every figure must point at something.** A plain screenshot shows the reader
the page; it does not show them *which* of six similar buttons to press. So each
one gets a pink box round the target, a labelled tag, and the rest of the page
dimmed. The dimming is what removes the ambiguity — the eye goes to the one
place still at full brightness. A screenshot with nothing marked on it is a
screenshot the reader has to search.

Two ways to draw it, same output either way:

**a. While you drive the UI** — `scripts/highlight.py`:

```python
from highlight import mark, clear
mark(page, "document.querySelector('button.create')", "1. Click + Create Form")
page.screenshot(path="/tmp/shots/01.png")
clear(page)                     # or it appears in every later capture
```

The position comes from the element's own bounding box, so it cannot be a few
pixels out. Prefer this whenever you have a live page. `mark()` returns False
and says so when the selector finds nothing — do not ship that capture.

**b. On a capture you already have** — `scripts/annotate_screenshot.py`:

```bash
python3 scripts/annotate_screenshot.py --spec figures.json
python3 scripts/annotate_screenshot.py in.png out.png \
        --box 1315,130,128,29 --label "1. Click + Create Form"
```

Use it when the screenshot predates the document, when the target has no element
of its own (a pair of table columns, a region of a canvas), or when one capture
has to illustrate two different steps. Several regions on one figure show an
ordered pair of clicks — number the labels, and set `"label_pos": "below"` on
the second when a tag above it would cover the first.

Coordinates are hand-entered here, so **look at the result** before shipping it.
A box a hundred pixels off points confidently at the wrong thing, which is worse
than no box at all.

**Then crop to the control, not the window.** A 1600px screenshot renders the
button about 8px wide once embedded. `scripts/crop_highlights.py` finds the pink
and crops around it with padding:

```bash
python3 scripts/crop_highlights.py --map map.json --out <doc-dir>/screenshots
```

where `map.json` is `{"/tmp/shot1.png": "01-create-button", ...}` — numbered in
document order so the folder reads in sequence. Keep enough surroundings that
the reader can tell where they are (a nav tab, a page heading).

All three agree on `#e6007e`, so annotate → crop chains without configuration.

**Always tell the reader the annotation is yours.** Put a note near the top:
the pink box, the pink label and the dimming are added for the guide and are not
part of the product, or someone will hunt for a pink box on their screen.

**Capture on a clean tenant. This is a hard rule here.** No DEV banner, no
`test123` records, no colleague's name in an assignee column, no obviously
throwaway data. A customer reading their own documentation must see something
that looks like their own system — internal debris in a published guide reads as
carelessness and leaks how the company tests. Use plausible sample data with
neutral names. If you only have test-environment captures, say so and ask
whether to recapture or hold the document; do not publish them.

**Image format is PNG.** Do not offer this as a choice — it is settled:

- lossless text, so small labels and thin borders survive; JPEG puts halos on
  exactly the high-contrast edges UI is made of
- UI is large flat colour areas, PNG's best case — it beats JPEG on *size* here
  as well as quality
- universal support: Word, Confluence, Obsidian, GitHub, PDF export

WebP is ~25% smaller but still trips older tooling, which is a poor trade for a
controlled document. Only revisit if the user raises a specific constraint.

## 3. Write the document

**Voice.** Address the reader directly. Short numbered steps, one action each.
Name what they should end up seeing, not just what to click — *"You should end
up in the form builder, with Version: 1 under the name"* — because that is what
lets someone self-correct. Explain *why* a step exists when the reason affects
what they choose; do not narrate the obvious.

**Use the product's own words.** Whatever the button says is what you call it.
A guide that invents its own vocabulary sends the reader looking for something
that is not on screen.

**Structure.**

- **What this is for** — two or three sentences on what the module does and when
  someone would reach for it. A tester knows already; a customer opening the
  guide may not. This is the section `/howto` has no use for and a user guide
  cannot do without.
- **Before you start** — the role or permission needed, the tier or plan, and
  anything that must already exist (a project, a template, an approver). If the
  reader lacks one of these, say what they will see instead and who to ask.
- **Terms you will see** — only where the product's vocabulary is not
  self-evident, and only the terms used in this document. Skip the section
  rather than padding it.
- **One section per task**, ordered the way a real user meets them — the common
  path first, the occasional one later — not in the order a validation sheet
  happens to list them. Give each a short imperative heading: *Create a form*,
  *Send it for approval*.
- **Tips and shortcuts** inline, where they apply, clearly marked as optional so
  nobody mistakes one for a required step.
- **If something does not look right** — a short troubleshooting list of the
  genuine confusions: what it means when the button is greyed out, why a record
  is not in the list, what an empty state means. Symptom first, then cause, then
  what to do.
- **Where to go next** — the related tasks or documents that usually follow.
- **A footer** naming the product version the document describes, the build
  date, and that the PDF is generated from the Markdown.

**Warn at the point of danger, not in a preamble.** A step that is easy to get
wrong, or that cannot be undone, gets its warning immediately above it, in bold.
Deleting, submitting, approving, anything that notifies other people, and
anything that locks a record are all worth a line.

**Mark optional sections** where they depend on tier, role or org
configuration, and say what the reader will see instead.

## 4. Where the product is broken

The `/howto` rule is *warn the tester, then have them confirm the defect*. **The
rule here is the opposite: a user document never contains a path that does not
work.** The reader is trying to finish a job, not gather evidence, and telling a
customer "this is a known defect, please note what you saw" is not
documentation.

**Nothing from the tester's copy reaches the reader.** Not the `Can you do it?`
boxes, not the defect-confirmation callouts ("this is a known defect, you are
confirming it, not diagnosing it"), not the *what appeared: ………* blanks, and not
the internal identifiers that tag them — validation test IDs (`MAN-03`), defect
tickets (`QM-4`) and matrix references are the test record's vocabulary and mean
nothing to a customer. Where a document is adapted from a validation how-to,
strip all of it; a single leftover checkbox tells the reader they were handed
somebody else's paperwork.

So, in order:

1. **Is there a working route to the same outcome?** Document that one, without
   commentary about the broken one.
2. **Is there a supported workaround?** Document it as the normal procedure —
   plainly, with no apology and no reference to the underlying fault.
3. **Neither?** Leave the task out of the document, and **tell the requester
   which task you dropped and why**, so it can be tracked and added once fixed.

Never quietly ship steps you know fail, and never soften them into vagueness to
avoid the problem. Behaviour that is merely *surprising* but correct is
different — that is a §3 troubleshooting entry, not a defect.

## 5. Write it, then produce all three files

**The output is settled: `.pdf` + `.html` + `.md`. Do not ask which format.**
The only question is **where it goes** — ask that, and ask it before you write
anything.

Every run leaves four things behind, together in one directory:

| | |
|---|---|
| `qmsWrapper_<Module>_<date>_<time>_v<N>.md` | the working source, with relative `screenshots/…` links |
| `screenshots/` | the annotated PNGs from §2 |
| `qmsWrapper_<Module>_<date>_<time>_v<N>.html` | the self-contained web version, every image inlined |
| `qmsWrapper_<Module>_<date>_<time>_v<N>.pdf` | the house-style PDF, printed from that HTML |

Write the Markdown first, build the HTML from it, and print the PDF from the
HTML — never the other way round, and never author the HTML by hand. The
Markdown is what gets edited when the UI changes; the HTML and the PDF are both
regenerated from it. All three carry the same stamp.

**The HTML is a deliverable, not scaffolding.** It is the one file that travels
on its own: `md_to_qmswrapper_html.py` inlines every screenshot as base64, so it
opens correctly with no `screenshots/` folder beside it and nothing to break when
it is forwarded. Hand it over with the other two; do not leave it in a temp
directory and do not bin it after the PDF is made.

**If the PDF step fails**, say so plainly, hand over the Markdown, the HTML and
the screenshots, and name what is missing (Playwright, a Chrome on the CDP port,
the logo asset). The HTML is still a complete, readable document, so say that
too — but do not present it as though the PDF had been produced.

**If the HTML step fails**, the PDF cannot be built either, since it is printed
from that HTML. Hand over the Markdown and the screenshots and say what broke.

### Filename convention

```
qmsWrapper_<Module>_<YYYY-MM-DD>_<HHMM>_v<N>.<ext>
qmsWrapper_FormBuilder_2026-08-14_1432_v1.pdf
qmsWrapper_FormBuilder_2026-08-14_1432_v1.md
```

| Field | Rule |
|---|---|
| `qmsWrapper` | Fixed prefix, this exact casing. |
| `<Module>` | The module's filename token — CamelCase, no spaces, from `reference/modules.md`. Never invent one. |
| `<YYYY-MM-DD>` | The date the document was built. |
| `<HHMM>` | 24-hour build time, so two runs on one day never collide. |
| `v<N>` | Version, from 1, bumped on each redraft of the same document. |

**All three files share a name**, differing only in extension — they are one
document in three formats, and a reader holding the PDF or the HTML has to be
able to find the source that produced it. Stamp the time once and use it for all
three; do not let them pick up timestamps minutes apart.

The `screenshots/` folder keeps its plain name beside them — it is shared by
every version of the document, so it takes no timestamp.

A guide spanning several modules takes the module it is *about*; if there is
genuinely no single one, ask which to file it under rather than inventing a
compound token.

No spaces, and no underscore inside any field: the name splits on `_` into
exactly five parts.

### Name the module, exactly

`<Module>` is not yours to phrase. Take it from **`reference/modules.md`**, the
registry lifted from the Validation Test Matrix workbook, which lists every
module's exact name and its filename token. A user guide filed under a name the
matrix does not use cannot be tied back to the module it documents, and a
customer-facing document that calls a screen something the product does not call
it is worse still.

| Do not write | Write |
|---|---|
| Form Editor, Forms, Forms (Builder & Submissions) | **Form Builder** |
| Process Editor, Process / Workflow Engine, Workflow Engine | **Process Builder** |

This applies to the prose as well as the filename. **If the module is not in the
registry, stop and ask** — never invent a name to get a document out.

### Other formats

Word is an **extra, produced only if the user explicitly asks** — and in
addition to the three outputs, never instead of them:

```bash
pandoc tutorial.md -o tutorial.docx --resource-path=.
```

Do not use pandoc to make the HTML. The deliverable HTML is the house-style one
from `md_to_qmswrapper_html.py` — the same file the PDF is printed from — so
that the web version and the PDF cannot drift apart.

### PDF — use the house style, not pandoc's default

qmsWrapper documentation PDFs have an established look: a logo +
"Documentation" header rule, near-black headings on white, humanist sans body at
generous line-height, and full-width screenshots with a hairline border. They are
produced by **printing HTML from Chrome**, not by LaTeX.

Match it with the two scripts here:

```bash
python3 scripts/md_to_qmswrapper_html.py <doc.md> <out.html> <screenshots-dir> assets/qmswrapper-logo.png
python3 scripts/html_to_pdf_chrome.py <out.html> <out.pdf>     # needs a CDP Chrome on :9223
```

The first inlines every image as base64, so the HTML is self-contained and the
PDF never has missing-image boxes — that self-containment is also what makes the
HTML worth shipping in its own right. The second drives Chrome's own print
engine, which is what produced the reference PDFs. Write the HTML straight to
the delivery directory under its house filename, not to a temp path: it is one
of the three outputs, not a by-product.

**Do not reach for `pandoc --pdf-engine=pdflatex`.** It cannot render `→`, `▾`
or `⚠` without a per-character `\DeclareUnicodeCharacter` preamble, it needs
`adjustbox` to stop oversized images overflowing, and the result looks like a
LaTeX article rather than product documentation.

Tell the reader the PDF is generated: it must be rebuilt from the Markdown when
the UI changes, not edited in place.

## Rules

- **This is a customer document.** No `Can you do it?` boxes, no defect
  confirmations, no "tell us where you struggled", no expected-to-fail footer,
  and no internal identifiers — no test IDs, defect tickets or matrix
  references. If those are wanted, the skill is `/howto`.
- **All three files, every time.** A guide is a `.pdf`, the `.html` it was
  printed from, *and* the `.md` that produced both, delivered together with
  `screenshots/`. Do not ask which format, do not ship one alone, and do not
  treat the PDF as the document and the rest as by-products — the Markdown is the
  source of the next revision, and the HTML is the copy that travels on its own.
- **The module name comes from the registry**, character-for-character, in the
  filename and in the prose. Not in `reference/modules.md`? Stop and ask. It is
  **Form Builder** and **Process Builder** — never "Editor".
- **Filenames follow `qmsWrapper_<Module>_<YYYY-MM-DD>_<HHMM>_v<N>`**, the
  `.pdf`, `.html` and `.md` differing only in extension.
- **Every screenshot is annotated**, by `highlight.py` on a live page or
  `annotate_screenshot.py` on an existing capture, then cropped to the target.
  An unmarked full-window capture is not a figure — it is homework for the
  reader. Check hand-entered boxes by eye before shipping.
- **Screenshots are mandatory**, and from a clean tenant with neutral sample
  data — no DEV banner, no test records, no real colleagues' names. If you
  cannot capture them, say so plainly and ask whether to proceed without.
- **Every navigation path is shown, not just written.** Any `A → B` trail
  through the menus gets a screenshot with the route marked, alongside the text.
- **Never invent a click path.** Every step must come from a screen you drove or
  a document that describes it.
- **Never document a path that does not work.** Working route, or supported
  workaround, or leave the task out and say which one you dropped.
- **Use the product's own words** for every screen, button and field.
- **Relative image links** (`screenshots/…`) so the document and its folder
  travel together. Warn that moving one without the other breaks the pictures.
- **Warn before anything destructive or irreversible**, immediately above the
  step.
- **Do not blame the reader.** If a task needs a warning, the design needs the
  warning — write it as a property of the software, not a caution about them.
- **Screenshots are controlled content**: they need recapturing whenever the UI
  changes, and the document's version footer must move with it.
