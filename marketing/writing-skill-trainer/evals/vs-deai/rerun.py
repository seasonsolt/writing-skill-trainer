#!/usr/bin/env python3
"""Later rounds, satire scenario only: python3 -I rerun.py prep|aggregate <round>

prep       builds work/judge-r<n>/set<k>-j<j>/restrained-satire/ with fresh random labels.
           The trained draft comes from work/out-r<n>/ (skill-v<n>); the other four are
           the round-1 drafts in work/out/. Mapping: work/judge-secret/mapping-r<n>.json.
aggregate  unblinds work/judge-r<n>/*/verdicts.json and writes results-r<n>.json.
"""

from __future__ import annotations

import json
import random
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
SID = "restrained-satire"
CONDITIONS = ["direct", "stopslop", "humanizer", "humanizer-samples", "trained"]
LABELS = "VWXYZ"
ROUND = int(sys.argv[2])
SECRET = WORK / "judge-secret" / f"mapping-r{ROUND}.json"


def prep() -> None:
    rng = random.Random(20261113 + ROUND)
    mapping = {}
    for k in (1, 2):
        for j in (1, 2, 3):
            name = f"set{k}-j{j}"
            dest = WORK / f"judge-r{ROUND}" / name / SID
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy(WORK / SID / "task.md", dest / "task.md")
            shutil.copy(WORK / SID / "holdout" / "holdout.md", dest / "ref.md")
            order = CONDITIONS[:]
            rng.shuffle(order)
            mapping[name] = dict(zip(LABELS, order))
            for label, cond in zip(LABELS, order):
                src = f"out-r{ROUND}" if cond == "trained" else "out"
                text = (WORK / src / f"{cond}-{k}" / f"{SID}.md").read_text(encoding="utf-8")
                text = re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)[0].strip()
                (dest / f"{label}.md").write_text(text + "\n", encoding="utf-8")
    SECRET.write_text(json.dumps(mapping, indent=1) + "\n")
    print("packets:", len(mapping))


def aggregate() -> None:
    mapping = json.loads(SECRET.read_text())
    ranks = defaultdict(lambda: defaultdict(list))
    flags = defaultdict(lambda: defaultdict(int))
    for packet, labels in mapping.items():
        v = json.loads((WORK / f"judge-r{ROUND}" / packet / "verdicts.json").read_text())[SID]
        for key in ("voice_ranking", "overall_ranking"):
            order = [labels[x] for x in v[key]]
            assert sorted(order) == sorted(CONDITIONS), (packet, key)
            for pos, cond in enumerate(order, 1):
                ranks[key][cond].append(pos)
        for label, items in v.get("fact_violations", {}).items():
            if items:
                flags[labels[label]][packet.split("-")[0]] += 1
    out = {"judgments_per_cell": 6, "scenario": SID, "conditions": {}}
    for cond in CONDITIONS:
        voice, overall = ranks["voice_ranking"][cond], ranks["overall_ranking"][cond]
        out["conditions"][cond] = {
            "voice_rank_mean": round(sum(voice) / len(voice), 2),
            "voice_first": voice.count(1),
            "voice_ranks": voice,
            "overall_rank_mean": round(sum(overall) / len(overall), 2),
            "overall_first": overall.count(1),
            "drafts_flagged_by_majority": sum(n >= 2 for n in flags[cond].values()),
        }
        print(cond, out["conditions"][cond])
    (HERE / f"results-r{ROUND}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    {"prep": prep, "aggregate": aggregate}[sys.argv[1]]()
