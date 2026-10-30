# -*- coding: utf-8 -*-
"""A small, dependency-free Markdown renderer for the shipped documents.

The dossiers must be single self-contained files: no external CSS, no images, no
JavaScript. Rather than pulling a Markdown library (which would break the
zero-dependency promise) this module renders the subset that actually appears in
``data/seeds/*.md``, ``docs/reports/*.md`` and ``data/failures.md``: headings,
tables, lists, blockquotes, fenced code, horizontal rules, bold, inline code and
links.

Links are rendered as plain ``text (url)`` on purpose — the dossier is an
archived document, so it shows its sources as evidence instead of loading them.
"""
from __future__ import annotations

import html
import re
from typing import List

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_HR = re.compile(r"^\s*([-*_])\s*(?:\1\s*){2,}$")
_UL = re.compile(r"^\s*[-*+]\s+(.*)$")
_OL = re.compile(r"^\s*\d+[.)]\s+(.*)$")
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def esc(value: object) -> str:
    """HTML-escape any value (None becomes an empty string)."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def inline(source: str) -> str:
    """Render inline Markdown (escape first, then the safe subset)."""
    text = esc(source)
    text = _INLINE_CODE.sub(r"<code>\1</code>", text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _LINK.sub(r"\1 (\2)", text)
    return text


def _is_cjk(ch: str) -> bool:
    code = ord(ch)
    return (
        0x3400 <= code <= 0x4DBF
        or 0x4E00 <= code <= 0x9FFF
        or 0xF900 <= code <= 0xFAFF
        or 0x3000 <= code <= 0x303F
        or 0xFF00 <= code <= 0xFFEF
    )


def _join_paragraph(parts: List[str]) -> str:
    """Join wrapped lines; no space between CJK characters, space otherwise."""
    out = ""
    for part in parts:
        if not out:
            out = part
            continue
        if _is_cjk(out[-1]) or _is_cjk(part[0]):
            out += part
        else:
            out += " " + part
    return out


def _looks_like_table(lines: List[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return bool(_TABLE_SEP.match(lines[index + 1]))


def _cells(row: str) -> List[str]:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def _starts_block(line: str) -> bool:
    stripped = line.strip()
    return bool(
        not stripped
        or _HEADING.match(stripped)
        or _HR.match(stripped)
        or stripped.startswith(">")
        or stripped.startswith("```")
        or _UL.match(line)
        or _OL.match(line)
        or stripped.startswith("|")
    )


def md_to_html(text: str, base_level: int = 0) -> str:
    """Convert Markdown *text* to an HTML fragment."""
    if not text:
        return ""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: List[str] = []
    index = 0
    n = len(lines)
    while index < n:
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        # fenced code block
        if stripped.startswith("```"):
            info = stripped[3:].strip()
            index += 1
            code: List[str] = []
            while index < n and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            index += 1  # closing fence
            lang = f' class="language-{esc(info)}"' if info else ""
            out.append(f"<pre><code{lang}>{esc(chr(10).join(code))}</code></pre>")
            continue

        # heading
        match = _HEADING.match(stripped)
        if match:
            level = min(6, len(match.group(1)) + 1 + base_level)
            out.append(f"<h{level}>{inline(match.group(2).strip())}</h{level}>")
            index += 1
            continue

        # horizontal rule
        if _HR.match(stripped):
            out.append("<hr>")
            index += 1
            continue

        # table
        if stripped.startswith("|") and _looks_like_table(lines, index):
            header = _cells(stripped)
            index += 2  # header + separator
            rows: List[List[str]] = []
            while index < n and lines[index].strip().startswith("|"):
                rows.append(_cells(lines[index]))
                index += 1
            head_html = "".join(f"<th>{inline(cell)}</th>" for cell in header)
            body_html = []
            for row in rows:
                cells = "".join(f"<td>{inline(cell)}</td>" for cell in row)
                body_html.append(f"<tr>{cells}</tr>")
            out.append(
                '<div class="table-wrap"><table class="md-table">'
                f"<thead><tr>{head_html}</tr></thead>"
                f"<tbody>{''.join(body_html)}</tbody></table></div>"
            )
            continue

        # blockquote
        if stripped.startswith(">"):
            quoted: List[str] = []
            while index < n and lines[index].strip().startswith(">"):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[index]))
                index += 1
            inner = md_to_html("\n".join(quoted), base_level)
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        # unordered list
        if _UL.match(line):
            items: List[str] = []
            while index < n and _UL.match(lines[index]):
                items.append(_UL.match(lines[index]).group(1).strip())
                index += 1
            lis = "".join(f"<li>{inline(item)}</li>" for item in items)
            out.append(f"<ul>{lis}</ul>")
            continue

        # ordered list
        if _OL.match(line):
            items = []
            while index < n and _OL.match(lines[index]):
                items.append(_OL.match(lines[index]).group(1).strip())
                index += 1
            lis = "".join(f"<li>{inline(item)}</li>" for item in items)
            out.append(f"<ol>{lis}</ol>")
            continue

        # paragraph: gather until a blank line or the start of another block
        paragraph = [stripped]
        index += 1
        while index < n and not _starts_block(lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        out.append(f"<p>{inline(_join_paragraph(paragraph))}</p>")

    return "\n".join(out)
