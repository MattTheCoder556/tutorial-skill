#!/usr/bin/env python3
"""Draw a "click here" annotation over a live page, then screenshot it.

Import this when you are driving the UI with Playwright and capturing as you
go. It injects a pink box round the target element, a labelled tag above it, and
dims the rest of the page, so a reader looking at the figure cannot mistake
which of several similar buttons is meant.

    from highlight import mark, clear

    mark(page, "document.querySelector('button.create')", "1. Click + Create Form")
    page.screenshot(path="/tmp/shots/01.png")
    clear(page)

`selector_js` is evaluated as JavaScript, not passed to querySelector, so it can
reach anything the page can — an nth match, an element found by its text, a node
inside a shadow root:

    mark(page, "[...document.querySelectorAll('td')].find(e=>e.textContent.includes('V1'))", "Current version")

Position is read from the element's own bounding box, so the annotation cannot
drift out of register the way hand-entered coordinates can. When the capture
already exists, or the target has no element of its own (a group of columns, a
region of a canvas), use `annotate_screenshot.py` instead.

Always `clear()` before the next capture — the marks are ordinary DOM nodes and
will otherwise appear in every screenshot that follows.

The colour matches `annotate_screenshot.py` and `crop_highlights.py`'s default,
so all three agree and cropping finds the box.
"""

PINK = "#e6007e"
DIM = 0.35
CLASS = "zzhl"          # marker class, so clear() can find every node it made

_MARK_JS = """([js, label, pink, dim, cls]) => {
  document.querySelectorAll('.' + cls).forEach(e => e.remove());
  const el = eval(js);
  if (!el) return false;
  el.scrollIntoView({block: 'center'});
  const r = el.getBoundingClientRect();

  const box = document.createElement('div');
  box.className = cls;
  Object.assign(box.style, {
    position: 'fixed', left: (r.left - 5) + 'px', top: (r.top - 5) + 'px',
    width: (r.width + 10) + 'px', height: (r.height + 10) + 'px',
    border: '3px solid ' + pink, borderRadius: '6px',
    zIndex: 99999, pointerEvents: 'none',
    // One huge spread shadow is what dims the rest of the page.
    boxShadow: '0 0 0 9999px rgba(0,0,0,' + dim + ')'
  });

  const tag = document.createElement('div');
  tag.className = cls;
  tag.textContent = label;
  Object.assign(tag.style, {
    position: 'fixed', left: (r.left - 5) + 'px',
    top: Math.max(2, r.top - 34) + 'px',
    background: pink, color: '#fff', font: 'bold 14px sans-serif',
    padding: '4px 10px', borderRadius: '4px',
    zIndex: 100000, pointerEvents: 'none', whiteSpace: 'nowrap'
  });

  document.body.append(box, tag);
  return true;
}"""


def mark(page, selector_js, label):
    """Annotate the element `selector_js` evaluates to. True if it was found."""
    found = page.evaluate(_MARK_JS, [selector_js, label, PINK, DIM, CLASS])
    if not found:
        # Loud on purpose: a silent miss produces an unannotated screenshot that
        # looks fine until a reader cannot tell what it is pointing at.
        print(f"highlight: no element for {selector_js!r} — capture will be plain")
    return found


def clear(page):
    """Remove every annotation, before the next capture or a clean final shot."""
    page.evaluate(f"() => document.querySelectorAll('.{CLASS}').forEach(e => e.remove())")
