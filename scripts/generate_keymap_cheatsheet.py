#!/usr/bin/env python3
"""Render this repository's numeric LAYOUT_universal layers using only stdlib."""

import argparse
import html
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
KEYBOARD = ROOT / "qmk_firmware/keyboards/keyball/keyball39"
KEYMAP = KEYBOARD / "keymaps/myKeymap/keymap.c"


def split_keys(text):
    """Split macro arguments without splitting nested LT/MT calls."""
    keys, start, depth = [], 0, 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            keys.append(text[start:index].strip())
            start = index + 1
        if depth < 0:
            raise ValueError("Unbalanced keycode parentheses")
    if depth:
        raise ValueError("Unbalanced keycode parentheses")
    keys.append(text[start:].strip())
    return keys


def parse_layers(source, key_count):
    source = re.sub(r"/\*.*?\*/|//[^\n]*", "", source, flags=re.S)
    match = re.search(r"\bkeymaps\s*\[.*?=\s*\{(.*?)\};", source, re.S)
    if not match:
        raise ValueError("Cannot find keymaps initializer")
    remaining = match.group(1).strip()
    layers = []
    while remaining:
        match = re.match(r"\[(\d+)\]\s*=\s*LAYOUT_universal\s*\(", remaining)
        if not match:
            raise ValueError("Expected numeric layer with LAYOUT_universal")
        start = match.end()
        depth, end = 1, start
        while end < len(remaining) and depth:
            if remaining[end] == "(":
                depth += 1
            elif remaining[end] == ")":
                depth -= 1
            end += 1
        if depth:
            raise ValueError("Unterminated layout macro")
        keys = split_keys(remaining[start:end - 1])
        if len(keys) != key_count:
            raise ValueError(f"Layer {match[1]}: expected {key_count} keys, got {len(keys)}")
        layer = int(match[1])
        if any(number == layer for number, _ in layers):
            raise ValueError(f"Duplicate layer {layer}")
        layers.append((layer, keys))
        remaining = remaining[end:].strip()
        if remaining:
            if not remaining.startswith(","):
                raise ValueError("Expected comma after layout")
            remaining = remaining[1:].strip()
    if not layers:
        raise ValueError("No layers found")
    return layers


ALIASES = {
    "NO": "Disabled", "TRNS": "Transparent", "SPC": "Space",
    "ENT": "Enter", "BSPC": "Backspace", "ESC": "Esc", "TAB": "Tab",
    "LNG1": "Lang 1", "LNG2": "Lang 2", "LGUI": "L GUI", "RGUI": "R GUI",
    "LCTL": "L Ctrl", "RCTL": "R Ctrl", "LALT": "L Alt", "RALT": "R Alt",
    "LSFT": "L Shift", "RSFT": "R Shift", "MINS": "-", "EQL": "=",
    "COMM": ",", "DOT": ".", "SLSH": "/", "BSLS": "\\", "GRV": "`",
    "LBRC": "[", "RBRC": "]", "LCBR": "{", "RCBR": "}", "SCLN": ";",
    "COLN": ":", "QUOT": "'", "DQUO": '"', "TILD": "~", "EXLM": "!",
    "AT": "@", "HASH": "#", "DLR": "$", "PERC": "%", "CIRC": "^",
    "AMPR": "&", "ASTR": "*", "LPRN": "(", "RPRN": ")", "UNDS": "_",
    "PLUS": "+", "PIPE": "|", "RGHT": "Right", "PGDN": "PgDn",
    "PGUP": "PgUp", "PSCR": "PrintScr", "SCRL": "ScrollLock", "PAUS": "Pause",
    "BTN1": "Mouse 1", "BTN2": "Mouse 2", "INS": "Insert",
}
MODIFIERS = {"LALT": "L Alt", "RALT": "R Alt", "LCTL": "L Ctrl",
             "RCTL": "R Ctrl", "LGUI": "L GUI", "RGUI": "R GUI",
             "LSFT": "L Shift", "RSFT": "R Shift"}


def label(code):
    code = re.sub(r"\s+", "", code)
    if code in ("XXXXXXX", "KC_NO"):
        return "Disabled", ""
    if code in ("_______", "KC_TRNS"):
        return "Transparent", ""
    call = re.fullmatch(r"(\w+)\((.*)\)", code)
    if call:
        name, body = call.groups()
        args = split_keys(body)
        if name == "LT" and len(args) == 2:
            return label(args[1])[0], f"Hold: Layer {args[0]}"
        if name.endswith("_T") and name[:-2] in MODIFIERS and len(args) == 1:
            return label(args[0])[0], f"Hold: {MODIFIERS[name[:-2]]}"
        if name in ("G", "C", "A", "S") and len(args) == 1:
            modifier = {"G": "GUI", "C": "Ctrl", "A": "Alt", "S": "Shift"}[name]
            return f"{modifier}+{label(args[0])[0]}", ""
    if code.startswith("KC_"):
        key = code[3:]
        return ALIASES.get(key, key), ""
    return code, ""


def render_svg(layers, positions):
    width, section = 1224, 384
    height = 96 + len(layers) * section
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">',
             '<title>Keyball39 myKeymap cheat sheet</title>',
             '<style>text{font-family:system-ui,sans-serif;fill:#172033}.heading{font-size:24px;font-weight:700}.key{font-size:15px}.hold{font-size:11px;fill:#365c9e}.note{font-size:14px;fill:#526075}</style>',
             f'<rect width="{width}" height="{height}" fill="#f5f7fb"/>',
             '<text x="24" y="36" class="heading">Keyball39 / myKeymap</text>',
             '<text x="24" y="64" class="note">Main label: tap / Hold: long press. GUI = Command (macOS) / Windows key.</text>']
    for index, (number, keys) in enumerate(layers):
        top = 96 + index * section
        parts.append(f'<text x="24" y="{top + 20}" class="heading">Layer {number}</text>')
        for position, code in zip(positions, keys):
            x, y = 24 + position["x"] * 98, top + 40 + position["y"] * 76
            main, hold = label(code)
            fill = "#e8ecf2" if main == "Disabled" else "#ffffff"
            parts.extend([f'<g><title>{html.escape(code)}</title>',
                          f'<rect x="{x}" y="{y}" width="92" height="68" rx="7" fill="{fill}" stroke="#c6cfdd"/>'])
            size = min(15, 138 / max(len(main), 1))
            parts.append(f'<text x="{x + 46}" y="{y + 28}" text-anchor="middle" class="key" style="font-size:{size:.1f}px">{html.escape(main)}</text>')
            if hold:
                parts.append(f'<text x="{x + 46}" y="{y + 49}" text-anchor="middle" class="hold">{html.escape(hold)}</text>')
            parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "tmp/keymap-cheatsheet")
    args = parser.parse_args()
    positions = json.loads((KEYBOARD / "info.json").read_text())["layouts"]["LAYOUT_no_ball"]["layout"]
    layers = parse_layers(KEYMAP.read_text(), len(positions))
    svg = render_svg(layers, positions)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "keyball39-myKeymap.svg").write_text(svg, encoding="utf-8")
    page = '''<!doctype html><html lang="ja"><meta charset="utf-8">
<title>Keyball39 myKeymap カンニングシート</title>
<style>body{max-width:1224px;margin:24px auto;padding:0 16px;font-family:system-ui,sans-serif}svg{width:100%;height:auto}@media print{body{margin:0;padding:0}svg{width:100%}}</style>
<h1>Keyball39 myKeymap カンニングシート</h1>
<p>keymap.c の全レイヤーを表示。キー上段はタップ、Hold は長押し時の動作です。
GUI は macOS の Command / Windows キー、Lang 1 / 2 は KC_LNG1 / KC_LNG2 です。</p>
<p>LAYOUT_universal の全42位置を表示しています。トラックボール搭載側の一部位置には物理キーがありません。
VIA / Remap で保存した配列は反映されません。未知のキーコードは元の表記で表示します。</p>
''' + svg + '</html>\n'
    (args.output / "index.html").write_text(page, encoding="utf-8")
    print(f"Generated {len(layers)} layers in {args.output}")


if __name__ == "__main__":
    main()
