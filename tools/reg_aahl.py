# -*- coding: utf-8 -*-
"""ページを _quarto-draft.yml / index / PLAN に登録する。

    python3 ~/reg.py <stem> <dir> <sidebar text> <index title> <topic section>
例: python3 ~/reg.py aahl-3-9 03-geometry-and-trigonometry \
        "HL 3.9 — Reciprocal and inverse trigonometric functions" \
        "Reciprocal trigonometric ratios and the inverse trigonometric functions" \
        "Topic 3 — Geometry and trigonometry"
"""
import glob
import os
import re
import sys

ROOT = os.path.expanduser("~/mnt/ib-math-ai-sl-jp")
stem, d, sidebar, idx_title, section = sys.argv[1:6]
num = stem.replace("aahl-", "").replace("-", ".", 1)   # 3-9 -> 3.9
num = re.sub(r"^(\d+)\.(\d+)([ab]?)$", r"\1.\2\3", num)
label = "HL " + num

# 1) _quarto-draft.yml
p = os.path.join(ROOT, "_quarto-draft.yml")
t = open(p, encoding="utf-8").read()
entry = ('            - file: aa-hl/%s/%s.qmd\n              text: "%s"\n'
         % (d, stem, sidebar))
if entry not in t:
    # ★ aa-hl のサイドバーだけを見る（aa-sl にも同じ節名があるため）
    head = t.index("    - id: aa-hl")
    tail = len(t)
    for _m in re.finditer(r"^    - id: ", t[head + 10:], re.M):
        tail = head + 10 + _m.start()
        break
    blk = t[head:tail]
    sec = '        - section: "%s"\n          contents:\n' % section
    if sec in blk:
        i = blk.index(sec) + len(sec)
        while blk[i:i + 12] == "            ":
            i = blk.index("\n", blk.index("\n", i) + 1) + 1
        blk = blk[:i] + entry + blk[i:]
    else:
        mark = "\n        - file: glossary-aa.qmd"
        assert mark in blk, "aa-hl ブロックに glossary の行がない"
        blk = blk.replace(mark, "\n" + sec + entry + mark)
    t = t[:head] + blk + t[tail:]
    open(p, "w", encoding="utf-8").write(t)

# 2) index.qmd
p = os.path.join(ROOT, "aa-hl", "index.qmd")
t = open(p, encoding="utf-8").read()
link = "- [%s — %s](%s/%s.qmd)\n" % (label, idx_title, d, stem)
if link not in t:
    mark = "\n**いまのところ"
    t = t.replace(mark, link + mark, 1)
old_row = "| **%s** | %s |" % (label, idx_title)
new_row = "| **%s** | **[%s](%s/%s.qmd)** ✅ |" % (label, idx_title, d, stem)
assert old_row in t or new_row in t, "index に行がない: " + old_row
t = t.replace(old_row, new_row)
written = len(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
t = re.sub(r"いまのところ \d+ ページです", "いまのところ %d ページです" % written, t)
open(p, "w", encoding="utf-8").write(t)

# 3) _AA-HL-PLAN.md
p = os.path.join(ROOT, "_AA-HL-PLAN.md")
t = open(p, encoding="utf-8").read()
t = re.sub(r"\*\*\d+ / 35 ページ。\*\*", "**%d / 35 ページ。**" % written, t)
open(p, "w", encoding="utf-8").write(t)
print("registered:", stem, "->", written, "pages")
