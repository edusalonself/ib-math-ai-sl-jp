# -*- coding: utf-8 -*-
"""統合 パス 6：SL 4.6 と SL 4.11 のチェッカーを、新しい本文に合わせる。"""
import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, "figs", "aa-sl")

# ══════════════════════════════════════════════════════════
# SL 4.6
# ══════════════════════════════════════════════════════════
P6 = os.path.join(F, "check_aasl_4_6.py")
c = io.open(P6, encoding="utf-8").read()


def rep(old, new, label):
    global c
    assert c.count(old) == 1, "4.6 検査 %d 件: %s" % (c.count(old), label)
    c = c.replace(old, new, 1)
    print("  4.6:", label)


rep('chk([s[0] for s in _secs] == [str(i) for i in range(1, 7)],\n'
    '    "### の番号 1..6: %s" % [s[0] for s in _secs])\n'
    'chk([s[1] for s in _secs] == ["and-or", "venn", "addition", "exclusive",\n'
    '                              "table", "tree"],\n'
    '    "アンカー: %s" % [s[1] for s in _secs])',

    'chk([s[0] for s in _secs] == [str(i) for i in range(1, 9)],\n'
    '    "### の番号 1..8: %s" % [s[0] for s in _secs])\n'
    'chk([s[1] for s in _secs] == ["and-or", "venn", "addition", "exclusive",\n'
    '                              "table", "tree", "conditional",\n'
    '                              "independent"],\n'
    '    "アンカー: %s" % [s[1] for s in _secs])', "節の番号とアンカー")

rep('chk(TEXT.count("{.callout-important}") == 2, '
    '"callout-important 2（公式集 4.6 の 2 式）")',
    'chk(TEXT.count("{.callout-important}") == 3, '
    '"callout-important 3（公式集 4.6 の 3 式）")', "callout の数")

rep('chk(_idea46 == list(range(1, 7)), f"The idea が 1..6 で連番: {_idea46}")',
    'chk(_idea46 == list(range(1, 9)), f"The idea が 1..8 で連番: {_idea46}")',
    "連番")

# 例題 2（カード）は、もどさない樹形図の例題に差し替わった
rep('in_text("P(A) = \\\\frac{6}{20} = \\\\frac{3}{10}, \\\\qquad '
    'P(B) = \\\\frac{5}{20} "\n'
    '        "= \\\\frac{1}{4}", "例題2(a)")\n'
    'in_text("P(A \\\\cup B) = \\\\frac{6}{20} + \\\\frac{5}{20} - '
    '\\\\frac{1}{20} "\n'
    '        "= \\\\frac{10}{20} = \\\\frac{1}{2}", "例題2(c)")\n'
    'in_text("$3, 4, 6, 8, 9, 12, 15, 16, 18, 20$ の $10$ 個です", "例題2 の検算")',

    '# 例題 2 は「もどさない樹形図」に差し替えた（2026-10-05）\n'
    'in_text("::: {#exm-aasl46-without}", "例題 2 はもどさない樹形図")\n'
    'in_text("P(RR) = \\\\frac{5}{8} \\\\times \\\\frac{4}{7} = '
    '\\\\frac{20}{56} = \\\\frac{5}{14}", "例題2(b)")\n'
    'in_text("(img/aasl-4-6-without.svg){#fig-aasl46-without", "例題 2 の図")\n'
    'chk(os.path.exists(os.path.join(os.path.dirname(QMD), "img",\n'
    '                                "aasl-4-6-without.svg")),\n'
    '    "例題 2 の SVG がある")\n'
    'chk(F(5, 8) * F(4, 7) == F(5, 14), "5/8 × 4/7 = 5/14")\n'
    'chk(F(5, 8) * F(3, 7) + F(3, 8) * F(5, 7) == F(15, 28), "ちょうど 1 個赤")\n'
    'chk(F(5, 8) * F(4, 7) + F(5, 8) * F(3, 7) + F(3, 8) * F(5, 7)\n'
    '    + F(3, 8) * F(2, 7) == 1, "枝先の合計は 1")', "例題 2")

rep('in_text("スープは $23 + 12 = 35$ ✓、サラダは $16 + 12 = 28$ ✓", '
    '"演習8 の検算")',
    'in_text("さいころ $1$ 個を $1$ 回投げると、$1$ と $2$ が同時に出ることは'
    'ありません", "演習8（排反と独立）")', "演習 8 の検算")

rep('in_text("*even:* $6$ *outcomes; multiples of $3$:* $4$ *outcomes; '
    'both:* $6$ "\n        "*and* $12$", "m10")',
    'in_text("P(GG) = \\\\frac{4}{10} \\\\times \\\\frac{3}{9} = '
    '\\\\frac{12}{90} = \\\\frac{2}{15}", "演習2（もどさない）")\n'
    'chk(F(4, 10) * F(3, 9) == F(2, 15), "4/10 × 3/9 = 2/15")\n'
    'chk(1 - F(6, 10) * F(5, 9) == F(2, 3), "少なくとも 1 本緑は 2/3")', "m10")

rep('in_text("more than the $60$ customers who were asked.", "m11 演習8")',
    'in_text("Mutually exclusive events cannot both happen", "演習8 の答案例")',
    "m11 演習8")

ADD = (
    '\n'
    '# ══════════════════════════════════════════════════════════\n'
    '# 2026-10-05：SL 4.6b を統合した\n'
    '# ══════════════════════════════════════════════════════════\n'
    'not_in_text("aasl-4-6b", "4.6b への参照は残っていない")\n'
    'in_text("### 7. 条件によって確率が変わる {#conditional}", "第 7 節")\n'
    'in_text("### 8. independent events（独立な事象） {#independent}", "第 8 節")\n'
    'in_text("**条件が分かったら、その条件に合う場合だけを見て確率を'
    '考えます。**",\n'
    '        "第 7 節の書き出し")\n'
    'in_text("たとえば、赤玉 $3$ 個・青玉 $2$ 個の袋から、玉をもどさずに '
    '$2$ 個"\n'
    '        "引きます。$1$ 個目が赤だった場合、残りは赤玉 $2$ 個・青玉 '
    '$2$ 個です。",\n'
    '        "第 7 節の例")\n'
    'in_text("(img/aasl-4-6-idea-c.svg){#fig-aasl46-idea-c", "図 (c) の埋め込み")\n'
    'chk(os.path.exists(os.path.join(os.path.dirname(QMD), "img",\n'
    '                                "aasl-4-6-idea-c.svg")), "図 (c) がある")\n'
    'in_text("このような確率を **conditional probability**（条件付き確率）と'
    'いいます。"\n'
    '        "記号と公式は、[SL 4.11](aasl-4-11.qmd) で学びます。", "4.11 へ渡す")\n'
    'in_text("P(A \\\\cap B) = P(A)P(B)\\n$$ {#eq-aasl46-indep}", "独立の式")\n'
    'in_text("{#tbl-aasl46-compare}", "排反と独立の表")\n'
    '# 図 (c) の数（赤 3・青 2、もどさない）\n'
    'chk(F(3, 5) * F(2, 4) + F(3, 5) * F(2, 4)\n'
    '    + F(2, 5) * F(3, 4) + F(2, 5) * F(1, 4) == 1, "図 (c) の枝先は 1")\n'
    'chk(F(3, 5) * F(2, 4) == F(6, 20), "3/5 × 2/4 = 6/20")\n'
    'chk(F(2, 5) * F(1, 4) == F(2, 20), "2/5 × 1/4 = 2/20")\n'
    '# さいころの例：排反だが独立ではない\n'
    'chk(F(1, 6) * F(1, 6) != 0, "P(1)P(2) ≠ 0 なのに P(1∩2) = 0")\n'
)
k = c.rindex("\nprint()")
c = c[:k] + "\n" + ADD.rstrip() + "\n" + c[k:]
io.open(P6, "w", encoding="utf-8").write(c)
print("書き出し: check_aasl_4_6.py")

# ══════════════════════════════════════════════════════════
# SL 4.11
# ══════════════════════════════════════════════════════════
P11 = os.path.join(F, "check_aasl_4_11.py")
d = io.open(P11, encoding="utf-8").read()


def rep11(old, new, label):
    global d
    assert d.count(old) == 1, "4.11 検査 %d 件: %s" % (d.count(old), label)
    d = d.replace(old, new, 1)
    print("  4.11:", label)


rep11('chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],\n'
      '    "### の番号 1..7: %s" % [s[0] for s in _secs])',
      'chk([s[0] for s in _secs] == [str(i) for i in range(1, 9)],\n'
      '    "### の番号 1..8: %s" % [s[0] for s in _secs])', "節の番号")

rep11('chk([s[1] for s in _secs] == ["formal", "multiply", "three", "test",\n'
      '                              "solve", "total", "choose"],',
      'chk([s[1] for s in _secs] == ["formal", "table", "formula", "multiply",\n'
      '                              "test", "solve", "total", "choose"],',
      "アンカー")

rep11('in_text("P(A \\\\mid B) = \\\\frac{P(A \\\\cap B)}{P(B)}, '
      '\\\\qquad P(B) \\\\ne 0\\n$$", "条件付き確率の式")',
      'in_text("P(A \\\\mid B) = \\\\frac{P(A \\\\cap B)}{P(B)}, '
      '\\\\qquad P(B) > 0\\n$$", "条件付き確率の式")', "条件付き確率の式")

rep11("in_text('### 2. the multiplication rule（かけ算の形） {#multiply}', "
      '"見出しの英語: 2. the multiplication rule")',
      "in_text('### 4. the multiplication rule（かけ算の形） {#multiply}', "
      '"見出しの英語: 4. the multiplication rule")', "第 4 節の見出し")

rep11("in_text('### 6. $P(A)$ を組み立てる（the law of total probability） "
      "{#total}', \"見出しの英語: 6. $P(A)$ を組み立てる（the law o\")",
      "in_text('### 7. $P(A)$ を組み立てる（the law of total probability） "
      "{#total}', \"見出しの英語: 7. $P(A)$ を組み立てる（the law o\")",
      "第 7 節の見出し")

rep11("in_text('### 3. 独立の $3$ つの言い方 {#three}', \"その内容は本文にある\")",
      "not_in_text('### 3. 独立の $3$ つの言い方 {#three}', "
      '"独立の言い方は第 5 節にまとめた")', "旧第 3 節")

rep11("in_text('### 4. 独立性の判定 {#test}', \"その内容は本文にある\")",
      "in_text('### 5. 独立性の判定 {#test}', \"その内容は本文にある\")",
      "第 5 節の見出し")

for old, label in (
    ('chk("$0 < P(B) < 1$ のとき、次の $3$ つのどれで書いても同じです" in TEXT,\n'
     '    "第3節: 同値の条件 0 < P(B) < 1 を書いている")',
     "同値の条件"),
):
    pass

io.open(P11, "w", encoding="utf-8").write(d)
print("書き出し: check_aasl_4_11.py")
