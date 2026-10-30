# -*- coding: utf-8 -*-
"""Self-contained HTML shell and components for the rehearsal dossiers.

Everything is inlined: one ``<style>`` block, zero ``<script>``, zero external
requests, zero web fonts, zero images. A dossier can be attached to an email,
archived for a regulator, or opened from a USB stick on an air-gapped machine and
it renders identically.

The visual language is deliberately corporate: dark top bar, risk matrix table,
monospace evidence blocks, print-friendly.
"""
from __future__ import annotations

from typing import Iterable, List, Sequence

from .markdown import esc

CSS = """
:root{
  --ink:#0f172a; --ink-2:#1e293b; --muted:#64748b; --line:#e2e8f0;
  --bg:#f6f8fb; --card:#ffffff; --nav:#0b1220; --nav-ink:#e2e8f0;
  --accent:#0ea5e9; --accent-2:#0369a1;
  --ok-bg:#ecfdf5; --ok-ink:#047857; --ok-line:#a7f3d0;
  --warn-bg:#fffbeb; --warn-ink:#b45309; --warn-line:#fde68a;
  --bad-bg:#fef2f2; --bad-ink:#b91c1c; --bad-line:#fecaca;
  --info-bg:#eff6ff; --info-ink:#1d4ed8; --info-line:#bfdbfe;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",
  "PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif;}
a{color:var(--accent-2);text-decoration:none}
a:hover{text-decoration:underline}
code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
.topbar{background:var(--nav);color:var(--nav-ink);border-bottom:3px solid var(--accent);padding:14px 22px}
.topbar .inner{max-width:1120px;margin:0 auto;display:flex;align-items:center;
  justify-content:space-between;gap:16px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;letter-spacing:.2px}
.brand .mark{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;
  border-radius:7px;background:var(--accent);color:#04202f;font-weight:800;font-size:14px}
.topbar nav a{color:#cbd5e1;font-size:13px;margin-left:16px}
.topbar nav a:hover{color:#fff}
.wrap{max-width:1120px;margin:0 auto;padding:26px 22px 60px}
.hero{background:linear-gradient(180deg,#ffffff, #f1f5f9);border:1px solid var(--line);
  border-radius:14px;padding:26px 28px;box-shadow:0 1px 2px rgba(15,23,42,.04)}
.kicker{text-transform:uppercase;letter-spacing:.14em;font-size:11.5px;font-weight:700;
  color:var(--accent-2);margin:0 0 8px}
h1{font-size:29px;line-height:1.25;margin:0 0 8px;letter-spacing:-.2px}
.sub{color:var(--muted);margin:0;font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.chip{background:#fff;border:1px solid var(--line);border-radius:999px;padding:4px 11px;
  font-size:12.5px;color:var(--ink-2)}
.chip b{color:var(--muted);font-weight:600;margin-right:5px;text-transform:uppercase;
  font-size:10.5px;letter-spacing:.08em}
section.card{background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:22px 24px;margin-top:20px;box-shadow:0 1px 2px rgba(15,23,42,.04)}
section.card>h2{font-size:19px;margin:0 0 4px;letter-spacing:-.1px}
section.card>h2 .num{color:var(--accent);font-weight:800;margin-right:9px}
.section-sub{color:var(--muted);font-size:13.5px;margin:0 0 16px}
h3{font-size:16px;margin:20px 0 8px}
h4{font-size:14px;margin:16px 0 6px}
p{margin:8px 0}
ul,ol{margin:8px 0;padding-left:22px}
li{margin:3px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:14px 0}
.kpi{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.kpi .label{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);
  font-weight:700}
.kpi .value{font-size:24px;font-weight:750;margin-top:4px;letter-spacing:-.5px}
.kpi .note{font-size:12px;color:var(--muted);margin-top:2px}
.badge{display:inline-block;border-radius:999px;padding:2px 9px;font-size:11.5px;
  font-weight:700;letter-spacing:.03em;white-space:nowrap;border:1px solid}
.badge.ok{background:var(--ok-bg);color:var(--ok-ink);border-color:var(--ok-line)}
.badge.warn{background:var(--warn-bg);color:var(--warn-ink);border-color:var(--warn-line)}
.badge.danger{background:var(--bad-bg);color:var(--bad-ink);border-color:var(--bad-line)}
.badge.info{background:var(--info-bg);color:var(--info-ink);border-color:var(--info-line)}
.badge.neutral{background:#f1f5f9;color:var(--ink-2);border-color:var(--line)}
.callout{border:1px solid var(--line);border-left-width:4px;border-radius:10px;
  padding:14px 16px;margin:14px 0;background:#fff}
.callout .title{font-weight:700;margin-bottom:4px;font-size:14px}
.callout.info{border-left-color:var(--accent);background:var(--info-bg)}
.callout.warn{border-left-color:var(--warn-ink);background:var(--warn-bg)}
.callout.danger{border-left-color:var(--bad-ink);background:var(--bad-bg)}
.callout.ok{border-left-color:var(--ok-ink);background:var(--ok-bg)}
.table-wrap{overflow-x:auto;margin:14px 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:13.5px;background:#fff}
th{background:#f1f5f9;text-align:left;font-size:11.5px;text-transform:uppercase;
  letter-spacing:.07em;color:var(--muted);padding:9px 12px;border-bottom:1px solid var(--line);
  white-space:nowrap;vertical-align:bottom}
td{padding:9px 12px;border-bottom:1px solid #eef2f7;vertical-align:top}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:#f8fafc}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.risk-yes{color:var(--ok-ink);font-weight:700}
.risk-partial{color:var(--warn-ink);font-weight:700}
.risk-no{color:var(--bad-ink);font-weight:700}
pre{background:#0b1220;color:#e2e8f0;border-radius:10px;padding:14px 16px;overflow:auto;
  font-size:12.5px;line-height:1.55;border:1px solid #17233a}
pre.term{position:relative}
pre.term::before{content:"terminal";position:absolute;top:6px;right:10px;font-size:10px;
  text-transform:uppercase;letter-spacing:.14em;color:#64748b}
code{background:#eef2f7;color:#0f172a;border-radius:4px;padding:1px 5px;font-size:12.5px}
pre code{background:none;color:inherit;padding:0;font-size:inherit}
.evidence{background:#0b1220;color:#cbd5e1;border-radius:10px;padding:13px 15px;overflow-x:auto;
  font-size:12px;line-height:1.6;border:1px solid #17233a;margin:12px 0}
.evidence .k{color:#7dd3fc}
.evidence .v{color:#fde68a;word-break:break-all}
.mono{font-size:12.5px;word-break:break-all}
blockquote{margin:14px 0;padding:10px 16px;border-left:3px solid var(--accent);
  background:#f8fafc;color:var(--ink-2);border-radius:0 8px 8px 0}
blockquote p{margin:4px 0}
hr{border:none;border-top:1px solid var(--line);margin:22px 0}
.md-table code,.md-table td code{font-size:12px}
.doc h2{font-size:18px;margin:22px 0 8px}
.doc h3{font-size:15.5px}
.doc{font-size:14.5px}
.muted{color:var(--muted)}
.small{font-size:12.5px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media (max-width:760px){.two-col{grid-template-columns:1fr}h1{font-size:24px}}
footer{color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);margin-top:34px;
  padding-top:16px}
footer p{margin:4px 0}
.watermark{display:inline-block;border:1px solid var(--line);border-radius:8px;background:#fff;
  padding:6px 10px;font-size:12px;color:var(--ink-2)}
@media print{
  body{background:#fff}
  .topbar{background:#fff;color:#000;border-bottom:2px solid #000}
  .topbar nav{display:none}
  .wrap{max-width:none;padding:0}
  section.card{box-shadow:none;break-inside:avoid}
  pre,.evidence{background:#f8fafc;color:#0f172a;border:1px solid #cbd5e1}
  a{color:#000}
}
"""


def badge(text: str, kind: str = "neutral") -> str:
    return f'<span class="badge {esc(kind)}">{esc(text)}</span>'


def chips(items: Sequence) -> str:
    """``items`` is a sequence of (label, value) pairs."""
    out = []
    for label, value in items:
        out.append(f'<span class="chip"><b>{esc(label)}</b>{esc(value)}</span>')
    return f'<div class="chips">{"".join(out)}</div>'


def kpis(items: Iterable) -> str:
    """``items`` is an iterable of (label, value, note) triples."""
    out = []
    for label, value, note in items:
        note_html = f'<div class="note">{esc(note)}</div>' if note else ""
        out.append(
            f'<div class="kpi"><div class="label">{esc(label)}</div>'
            f'<div class="value">{value}</div>{note_html}</div>'
        )
    return f'<div class="grid">{"".join(out)}</div>'


def table(headers: Sequence[str], rows: Sequence[Sequence[str]], cls: str = "",
          numeric_columns: Sequence[int] = ()) -> str:
    """Build a table. Cell values are treated as already-escaped HTML."""
    numeric = set(numeric_columns)
    head = "".join(
        f'<th class="num">{esc(h)}</th>' if i in numeric else f"<th>{esc(h)}</th>"
        for i, h in enumerate(headers)
    )
    body = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            klass = ' class="num"' if i in numeric else ""
            cells.append(f"<td{klass}>{cell}</td>")
        body.append(f"<tr>{''.join(cells)}</tr>")
    return (
        f'<div class="table-wrap"><table class="{esc(cls)}">'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
    )


def callout(kind: str, title: str, body_html: str) -> str:
    title_html = f'<div class="title">{esc(title)}</div>' if title else ""
    return f'<div class="callout {esc(kind)}">{title_html}{body_html}</div>'


def evidence_block(rows: Sequence) -> str:
    """Monospace evidence block. ``rows`` is a sequence of (key, value) pairs."""
    lines = []
    for key, value in rows:
        lines.append(f'<span class="k">{esc(key)}</span>  <span class="v">{esc(value)}</span>')
    return f'<div class="evidence">{"<br>".join(lines)}</div>'


def section(number: str, title: str, body_html: str, subtitle: str = "",
            anchor: str = "") -> str:
    sub = f'<p class="section-sub">{esc(subtitle)}</p>' if subtitle else ""
    anchor_attr = f' id="{esc(anchor)}"' if anchor else ""
    num = f'<span class="num">{esc(number)}</span>' if number else ""
    return (
        f"<section class=\"card\"{anchor_attr}><h2>{num}{esc(title)}</h2>{sub}"
        f"{body_html}</section>"
    )


def page(*, title: str, kicker: str, heading: str, subtitle: str = "",
         chips_html: str = "", body: str, footer_html: str = "",
         nav_html: str = "", lang: str = "zh-CN") -> str:
    """A complete, standalone HTML document."""
    subtitle_html = f'<p class="sub">{esc(subtitle)}</p>' if subtitle else ""
    kicker_html = f'<p class="kicker">{esc(kicker)}</p>' if kicker else ""
    nav = f"<nav>{nav_html}</nav>" if nav_html else ""
    return f"""<!DOCTYPE html>
<html lang="{esc(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generator" content="crisis-rehearsal crh">
<meta name="robots" content="noindex">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header class="topbar"><div class="inner">
<div class="brand"><span class="mark">CR</span> Crisis Rehearsal Engine</div>
{nav}
</div></header>
<main class="wrap">
<section class="hero">
{kicker_html}
<h1>{heading}</h1>
{subtitle_html}
{chips_html}
</section>
{body}
{footer_html}
</main>
</body>
</html>
"""
