"""Tiny YAML-subset parser (stdlib fallback).

Supports the subset MQAI job.yaml files use:
- key: value scalars (with type coercion: int, bool, null, quoted/plain strings)
- nested maps by indentation
- scalar lists (`- item`)
- folded/literal block scalars (`>` and `|`) captured as a single joined string
- full-line comments (`# ...`) and simple trailing comments (` # ...`) on scalar lines

NOT a full YAML implementation. Limitations (documented in docs/known_limits.md):
- no list-of-maps beyond shallow use, no anchors/aliases, no flow style ({}, []),
- trailing `#` inside unquoted values is treated as a comment.

If PyYAML is importable, `load()` uses it; otherwise it falls back to this parser.
"""
from __future__ import annotations

from typing import Any, List, Tuple


def _coerce(value: str) -> Any:
    v = value.strip()
    if v == "" or v == "~" or v.lower() == "null":
        return None
    if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
        return v[1:-1]
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        if v.isdigit() or (v[0] == "-" and v[1:].isdigit()):
            return int(v)
    except (ValueError, IndexError):
        pass
    return v


def _strip_comment(line: str) -> str:
    # Remove a trailing " # ..." comment when not inside quotes (naive, sufficient for our files).
    in_s = in_d = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif ch == "#" and not in_s and not in_d:
            if i == 0 or line[i - 1] == " ":
                return line[:i].rstrip()
    return line.rstrip()


class _Line:
    __slots__ = ("indent", "text", "raw")

    def __init__(self, indent: int, text: str, raw: str):
        self.indent = indent
        self.text = text
        self.raw = raw


def _tokenize(text: str) -> List[_Line]:
    out: List[_Line] = []
    for raw in text.splitlines():
        if raw.strip() == "" or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        out.append(_Line(indent, raw.strip(), raw))
    return out


def parse(text: str) -> Any:
    lines = _tokenize(text)
    obj, _ = _parse_block(lines, 0, lines[0].indent if lines else 0)
    return obj


def _block_scalar(lines: List[_Line], idx: int, parent_indent: int) -> Tuple[str, int]:
    """Collect indented raw lines after a `>`/`|` marker into one joined string."""
    collected: List[str] = []
    while idx < len(lines) and lines[idx].indent > parent_indent:
        collected.append(lines[idx].text)
        idx += 1
    return (" ".join(collected).strip(), idx)


def _parse_block(lines: List[_Line], idx: int, indent: int) -> Tuple[Any, int]:
    # Decide list vs map by first line at this indent.
    if idx >= len(lines):
        return {}, idx
    is_list = lines[idx].text.startswith("- ") or lines[idx].text == "-"
    if is_list:
        result_list: List[Any] = []
        while idx < len(lines) and lines[idx].indent == indent and (
            lines[idx].text.startswith("- ") or lines[idx].text == "-"
        ):
            item = lines[idx].text[1:].strip()
            idx += 1
            result_list.append(_coerce(item) if item else None)
        return result_list, idx

    result: dict = {}
    while idx < len(lines) and lines[idx].indent == indent:
        line = lines[idx]
        if ":" not in line.text:
            idx += 1
            continue
        key, _, rest = line.text.partition(":")
        key = key.strip()
        rest = _strip_comment(rest.strip())
        if rest in (">", "|", ">-", "|-"):
            idx += 1
            value, idx = _block_scalar(lines, idx, line.indent)
            result[key] = value
        elif rest == "":
            # Nested block (map or list) if next line is deeper, else null.
            if idx + 1 < len(lines) and lines[idx + 1].indent > line.indent:
                idx += 1
                value, idx = _parse_block(lines, idx, lines[idx].indent)
                result[key] = value
            else:
                result[key] = None
                idx += 1
        else:
            result[key] = _coerce(rest)
            idx += 1
    return result, idx


def load(text: str) -> Any:
    """Load YAML text. Uses PyYAML if available, else the subset parser."""
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except Exception:
        return parse(text)


def load_path(path) -> Any:
    from pathlib import Path

    return load(Path(path).read_text(encoding="utf-8"))
