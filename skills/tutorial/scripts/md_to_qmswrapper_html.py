#!/usr/bin/env python3
"""Render a how-to markdown into qmsWrapper Documentation-styled HTML."""
import base64, os, re, sys, html as H

md_path, out_html, shots_dir, logo_path = sys.argv[1:5]
base = os.path.dirname(os.path.abspath(md_path))
md = open(md_path, encoding='utf-8').read()

def b64(p):
    return base64.b64encode(open(p,'rb').read()).decode()

logo_uri = "data:image/png;base64," + b64(logo_path)

def inline(t):
    t = H.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    return t

lines = md.split('\n')
out, i = [], 0
title = None; lede_done = False
while i < len(lines):
    ln = lines[i]
    m_img = re.match(r'!\[(.*?)\]\((.+?)\)', ln.strip())
    if m_img:
        alt, src = m_img.group(1), m_img.group(2)
        p = os.path.join(base, src)
        if os.path.exists(p):
            out.append(f'<figure><img src="data:image/png;base64,{b64(p)}" alt="{H.escape(alt)}">'
                       f'<figcaption>{inline(alt)}</figcaption></figure>')
        i += 1; continue
    if ln.startswith('# '):
        title = ln[2:].strip(); out.append(f'<h1>{inline(title)}</h1>'); i += 1; continue
    if ln.startswith('## '):
        out.append(f'<h2>{inline(ln[3:].strip())}</h2>'); i += 1; continue
    if ln.startswith('### '):
        out.append(f'<h3>{inline(ln[4:].strip())}</h3>'); i += 1; continue
    if ln.strip() == '---':
        out.append('<hr>'); i += 1; continue
    if ln.startswith('> '):
        blk = []
        while i < len(lines) and (lines[i].startswith('> ') or lines[i].strip() == '>'):
            blk.append(lines[i][2:] if len(lines[i]) > 2 else '')
            i += 1
        paras, cur = [], []
        for b in blk:
            if re.match(r'^!\[', b.strip()):
                continue
            if not b.strip():
                if cur: paras.append(' '.join(cur)); cur = []
            else:
                cur.append(b.strip())
        if cur: paras.append(' '.join(cur))
        body = '<br><br>'.join(inline(x) for x in paras if x.strip())
        cls = 'callout check' if 'Can you do it' in body or '☐' in body else 'callout'
        out.append(f'<div class="{cls}">{body}</div>')
        continue
    if re.match(r'^\d+\. ', ln):
        start = int(re.match(r'^(\d+)\. ', ln).group(1))
        items = []
        while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
            cur = re.sub(r'^\d+\. ', '', lines[i]); i += 1
            while (i < len(lines) and lines[i].strip()
                   and not re.match(r'^(#{1,3} |> |\d+\. |- |\||!\[|---)', lines[i])):
                cur += ' ' + lines[i].strip(); i += 1
            items.append(inline(cur))
        out.append(f'<ol start="{start}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>')
        continue
    if ln.startswith('- '):
        items = []
        while i < len(lines) and lines[i].startswith('- '):
            cur = lines[i][2:]; i += 1
            while (i < len(lines) and lines[i].strip()
                   and not re.match(r'^(#{1,3} |> |\d+\. |- |\||!\[|---)', lines[i])):
                cur += ' ' + lines[i].strip(); i += 1
            items.append(inline(cur))
        out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>')
        continue
    if ln.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            rows.append(lines[i]); i += 1
        cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
        cells = [c for c in cells if not all(re.fullmatch(r':?-{2,}:?', x or '') for x in c)]
        if cells:
            head = ''.join(f'<th>{inline(c)}</th>' for c in cells[0])
            body = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in cells[1:])
            out.append(f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
        continue
    if ln.strip():
        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,3} |> |\d+\. |- |\||!\[|---)', lines[i]):
            para.append(lines[i]); i += 1
        text = inline(' '.join(x.strip() for x in para))
        cls = ' class="lede"' if (title and not lede_done) else ''
        if cls: lede_done = True
        out.append(f'<p{cls}>{text}</p>')
        continue
    i += 1

doc_title = title or os.path.basename(md_path)
CSS = """
@page { size: A4; margin: 18mm 16mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font-family: Ubuntu, 'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif;
  color:#1F2937; font-size:11.2pt; line-height:1.75; margin:0; background:#fff;
  -webkit-font-smoothing:antialiased; }
.brand { display:flex; align-items:center; gap:14px; padding-bottom:14px;
  border-bottom:1px solid #E5E7EB; margin-bottom:34px; }
.brand img { height:30px; width:auto; }
.brand span { font-size:12.5pt; color:#4B5563; font-weight:500;
  border-left:1px solid #D1D5DB; padding-left:14px; }
h1 { font-size:23pt; line-height:1.25; font-weight:700; color:#24272C; margin:0 0 14px; letter-spacing:-.2px; }
h2 { font-size:15.5pt; font-weight:700; color:#24272C; margin:34px 0 12px; break-after:avoid; }
h3 { font-size:12.6pt; font-weight:700; color:#24272C; margin:26px 0 8px; break-after:avoid; }
p { margin:0 0 14px; }
p.lede { font-size:12.6pt; color:#4B5563; line-height:1.65; margin-bottom:26px; }
strong { font-weight:700; color:#111827; }
code { font-family:'Ubuntu Mono',ui-monospace,Menlo,Consolas,monospace; font-size:.9em;
  background:#F3F4F6; padding:1px 5px; border-radius:3px; color:#374151; }
ol, ul { margin:0 0 14px; padding-left:22px; }
li { margin:0 0 6px; }
figure { margin:20px 0 24px; break-inside:avoid; }
figure img { width:100%; height:auto; display:block; border:1px solid #E5E7EB; border-radius:6px; }
figcaption { font-size:9.4pt; color:#6B7280; margin-top:7px; }
.callout { border-left:3px solid #D1D5DB; background:#F9FAFB; padding:11px 15px;
  margin:16px 0 18px; font-size:10.6pt; color:#374151; break-inside:avoid; border-radius:0 4px 4px 0; }
.callout.check { border-left-color:#B91C2C; background:#FDF6F7; }
table { width:100%; border-collapse:collapse; margin:14px 0 20px; font-size:10.4pt; break-inside:avoid; }
th { text-align:left; font-weight:700; color:#24272C; border-bottom:2px solid #E5E7EB; padding:7px 9px; }
td { border-bottom:1px solid #F3F4F6; padding:7px 9px; vertical-align:top; }
hr { border:0; border-top:1px solid #E5E7EB; margin:34px 0; }
h1,h2,h3 { break-after:avoid; }
"""
open(out_html,'w',encoding='utf-8').write(
 f"<!doctype html><html><head><meta charset='utf-8'>"
 f"<title>{H.escape(doc_title)} - qmsWrapper Documentation</title>"
 f"<style>{CSS}</style></head><body>"
 f"<div class='brand'><img src='{logo_uri}' alt='qmsWrapper'><span>Documentation</span></div>"
 + '\n'.join(out) + "</body></html>")
print("wrote", out_html, os.path.getsize(out_html)//1024, "kb")
