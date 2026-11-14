#!/usr/bin/env python3
"""Draw the README chart from results.json: python3 -I chart.py

One row per method, one column per scenario. Bar length = how many of the 6 blind
judgments ranked that method's draft closest to the held-out author sample. The
trained skill is the accent series; every other method is the de-emphasis gray.
The satire column uses the skill after two fix rounds (results-r3.json); the first
attempt, which lost, is in README.md next to this file.
Writes assets/voice-first-<lang>-<mode>.svg at the repository root.
"""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[3] / "assets"
ROWS = ["trained", "stopslop", "humanizer-samples", "humanizer", "direct"]
COLS = ["twain-essay", "tech-news", "restrained-satire"]
THEME = {
    "light": {"ink": "#0b0b0b", "ink2": "#52514e", "accent": "#2a78d6", "gray": "#c4c2b9", "rule": "#e4e2da"},
    "dark": {"ink": "#f0efec", "ink2": "#c3c2b7", "accent": "#3987e5", "gray": "#5c5b56", "rule": "#33322f"},
}
TEXT = {
    "en": {
        "title": "Whose draft sounds most like the author?",
        "sub": "Times blind judges ranked each method closest to the author, out of 6. Same model, same task.",
        "rows": ["Trained skill (this repo)", "stop-slop", "humanizer-zh + samples", "humanizer-zh", "No skill"],
        "cols": ["English humor essay", "Chinese tech news", "Chinese satire fiction"],
        "note": ["after Mark Twain", "after Wikinews", "after Lu Xun"],
    },
    "zh": {
        "title": "谁的稿子最像作者本人？",
        "sub": "6 次盲评里，每种做法被评为“最接近作者”的次数。同一个模型，同一个任务。",
        "rows": ["训练出的 skill（本仓库）", "stop-slop", "humanizer-zh + 样本", "humanizer-zh", "不用 skill"],
        "cols": ["英文幽默随笔", "中文科技新闻", "中文讽刺短篇"],
        "note": ["学马克·吐温", "学维基新闻", "学鲁迅"],
    },
}
WIDTH, LABEL_W, COL_W, BAR_MAX, ROW_H, TOP = 920, 232, 222, 150, 34, 132
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"


def bar(x: float, y: float, w: float, h: float, fill: str) -> str:
    """Bar anchored at x with a 4px rounded data end."""
    r = min(4, w / 2)
    return (f'<path d="M{x},{y}h{w - r}a{r},{r} 0 0 1 {r},{r}v{h - 2 * r}'
            f'a{r},{r} 0 0 1 -{r},{r}h-{w - r}z" fill="{fill}"/>')


def draw(lang: str, mode: str, firsts: dict[str, dict[str, int]]) -> str:
    c, t = THEME[mode], TEXT[lang]
    height = TOP + ROW_H * len(ROWS) + 18
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" font-family="{FONT}" role="img" '
        f'aria-label="{escape(t["title"])}">',
        f'<text x="0" y="28" font-size="22" font-weight="700" fill="{c["ink"]}">{escape(t["title"])}</text>',
        f'<text x="0" y="54" font-size="14" fill="{c["ink2"]}">{escape(t["sub"])}</text>',
    ]
    for j, sid in enumerate(COLS):
        x = LABEL_W + j * COL_W
        out.append(f'<text x="{x}" y="94" font-size="15" font-weight="600" fill="{c["ink"]}">{escape(t["cols"][j])}</text>')
        out.append(f'<text x="{x}" y="113" font-size="13" fill="{c["ink2"]}">{escape(t["note"][j])}</text>')
        out.append(f'<line x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{height - 14}" stroke="{c["rule"]}" stroke-width="1"/>')
    for i, cond in enumerate(ROWS):
        y = TOP + i * ROW_H
        accent = cond == "trained"
        out.append(f'<text x="0" y="{y + 16}" font-size="14" font-weight="{600 if accent else 400}" '
                   f'fill="{c["ink"] if accent else c["ink2"]}">{escape(t["rows"][i])}</text>')
        for j, sid in enumerate(COLS):
            x, n = LABEL_W + j * COL_W, firsts[sid][cond]
            w = BAR_MAX * n / 6
            if n:
                out.append(bar(x, y + 4, w, 16, c["accent"] if accent else c["gray"]))
            out.append(f'<text x="{x + w + 8}" y="{y + 17}" font-size="14" font-weight="{700 if n else 400}" '
                       f'fill="{c["ink"] if n else c["ink2"]}">{n}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    data = json.loads((HERE / "results.json").read_text(encoding="utf-8"))["scenarios"]
    firsts = {sid: {k: v["voice_first"] for k, v in data[sid]["conditions"].items()} for sid in COLS[:2]}
    r3 = json.loads((HERE / "results-r3.json").read_text(encoding="utf-8"))["conditions"]
    firsts[COLS[2]] = {k: v["voice_first"] for k, v in r3.items()}
    OUT.mkdir(exist_ok=True)
    for lang in TEXT:
        for mode in THEME:
            (OUT / f"voice-first-{lang}-{mode}.svg").write_text(draw(lang, mode, firsts), encoding="utf-8")
    print(firsts)


if __name__ == "__main__":
    main()
