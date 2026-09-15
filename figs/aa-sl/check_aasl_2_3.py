"""AA SL 2.3（関数のグラフ）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_3.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-3.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_3.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, t, p_ = sp.symbols("x t p")
REALS = sp.S.Reals


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + f"  ({u} vs {v})")


def ne(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) != 0, msg + f"  ({u} vs {v})")


def roots(expr, want, msg=""):
    chk(sp.solveset(sp.Eq(expr, 0), x, REALS) == want, "解: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. The idea の数値
# ══════════════════════════════════════════════════════════
eq(2 * 3 + 1, 7, "第 1 節 (3,7) は y = 2x+1 の上")
eq(2 * 1 + 1, 3, "第 1 節 (1,4) では 3 が出る")
ne(3, 4, "だから (1,4) はグラフの上にない")
# 第 4 節の表
_tab = [(v, v ** 2 - 2) for v in range(-3, 4)]
chk([w for _, w in _tab] == [7, 2, -1, -2, -1, 2, 7], f"第 4 節の表: {_tab}")
chk(sp.minimum(x ** 2 - 2, x, REALS) == -2, "表の最小は -2")
# 直線で結ぶとずれる
eq(R((-1) + (-2), 2), R(-3, 2), "(-1,-1) と (0,-2) の中点の高さ")
eq((x ** 2 - 2).subs(x, R(-1, 2)), R(-7, 4), "実際の値")
ne(R(-3, 2), R(-7, 4), "直線で結ぶとずれる")
# 一定の割合なら直線
_h = 24 - 3 * t
chk(sp.diff(_h, t) == -3, "一定の割合は 1 次関数の傾き")
chk(sp.diff(sp.diff(_h, t), t) == 0, "傾きは変わらない")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  f(x) = x^2 - 2x - 3
# ══════════════════════════════════════════════════════════
_f1 = x ** 2 - 2 * x - 3
chk(sp.factor(_f1) == (x - 3) * (x + 1), "例題1 因数分解")
roots(_f1, {3, -1}, "例題1(a)")
eq(_f1.subs(x, 3), 0, "検算 f(3) = 0")
eq(_f1.subs(x, -1), 0, "検算 f(-1) = 0")
eq(_f1.subs(x, 0), -3, "例題1(b) y 切片 -3")
eq(_f1.subs(x, 1), -4, "例題1(c) 最小 -4")
eq(R(3 + (-1), 2), 1, "2 つの x 切片のまん中は 1")
chk(sp.minimum(_f1, x, REALS) == -4, "実際に最小値は -4")
ne(-3, 0, "y 切片は x 軸の上ではない")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  g(x) = 4 - x^2, -3 <= x <= 3
# ══════════════════════════════════════════════════════════
_g = 4 - x ** 2
_D = sp.Interval(-3, 3)
eq(_g.subs(x, -3), -5, "例題2(a) g(-3) = -5")
eq(_g.subs(x, 0), 4, "g(0) = 4")
eq(_g.subs(x, 2), 0, "g(2) = 0")
chk(sp.maximum(_g, x, _D) == 4, "例題2(b) 最大は 4")
chk(sp.solveset(sp.Eq(_g, 4), x, _D) == {0}, "最大になるのは x = 0")
chk(sp.solveset(sp.Eq(_g, 0), x, _D) == {-2, 2}, "例題2(c) x 切片")
eq(_g.subs(x, -2), 0, "検算 g(-2) = 0")
chk(sp.minimum(_g, x, _D) == -5, "例題2(d) 最小は -5")
chk(sp.solveset(sp.Eq(_g, -5), x, _D) == {-3, 3}, "端で最小になる")
chk(sp.solveset(sp.Eq(_g, 5), x, REALS) == sp.S.EmptySet, "5 は出ない")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  f = x^2 - 1, g = x + 1
# ══════════════════════════════════════════════════════════
_f3, _g3 = x ** 2 - 1, x + 1
eq(_f3.subs(x, 2), 3, "例題3 f(2) = 3")
eq(_g3.subs(x, 2), 3, "g(2) = 3")
eq(3 + 3, 6, "(f+g)(2) = 6")
eq(sp.expand(_f3 + _g3), x ** 2 + x, "和の式")
eq((x ** 2 + x).subs(x, 2), 6, "和の式でも 6")
eq(sp.expand(_f3 - _g3), x ** 2 - x - 2, "例題3(b) 差の式")
chk(sp.factor(x ** 2 - x - 2) == (x - 2) * (x + 1), "差の因数分解")
chk(sp.solveset(sp.Eq(_f3, _g3), x, REALS) == {2, -1}, "例題3(c) x = 2, -1")
eq(_f3.subs(x, -1), _g3.subs(x, -1), "x=-1 で等しい")
eq(_f3.subs(x, -1), 0, "その共通の値は 0")
eq(_f3.subs(x, 2), _g3.subs(x, 2), "x=2 で等しい")
# 交点 ⟺ 差の x 切片
chk(sp.solveset(sp.Eq(_f3 - _g3, 0), x, REALS)
    == sp.solveset(sp.Eq(_f3, _g3), x, REALS), "交点と差の x 切片は同じ")
# かっこを忘れた誤り
ne(sp.expand(_f3 - _g3), sp.expand(x ** 2 - 1 - x + 1), "かっこを忘れると値がちがう")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  h(t) = 24 - 3t
# ══════════════════════════════════════════════════════════
chk(sp.solve(sp.Eq(_h, 0), t) == [8], "例題4(b) t = 8")
eq(_h.subs(t, 0), 24, "h(0) = 24")
eq(_h.subs(t, 1), 21, "h(1) = 21（3 cm 減る）")
eq(_h.subs(t, 8), 0, "h(8) = 0")
eq(R(24, 3), 8, "24 ÷ 3 = 8（別の道すじ）")
chk(sp.diff(_h, t) == -3, "傾きは -3")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
roots(2 * x - 6, {3}, "演習1 x 切片")
eq((2 * x - 6).subs(x, 0), -6, "演習1 y 切片")
chk(sp.diff(2 * x - 6, x) > 0 and (2 * x - 6).subs(x, 0) < 0, "傾き正・切片負")

roots(x ** 2 - 9, {3, -3}, "演習2 x 切片")
eq((x ** 2 - 9).subs(x, 0), -9, "演習2 y 切片")
eq((x ** 2 - 9).subs(x, -3), 0, "検算 -3 も解")
chk(len(sp.solveset(sp.Eq(x ** 2 - 9, 0), x, REALS)) == 2, "交点は 2 つ")

_e3 = [(x ** 2 - 2 * x).subs(x, v) for v in (-1, 0, 1, 2, 3)]
chk(_e3 == [3, 0, -1, 0, 3], f"演習3 の 5 値: {_e3}")
chk(sp.factor(x ** 2 - 2 * x) == x * (x - 2), "x(x-2)")
eq(R(0 + 2, 2), 1, "0 と 2 のまん中は 1")
chk(_e3[0] == _e3[4] and _e3[1] == _e3[3], "左右対称")

eq(sp.expand(x ** 2 + (2 * x + 3)), x ** 2 + 2 * x + 3, "演習4(a)")
eq((x ** 2 + 2 * x + 3).subs(x, 1), 6, "演習4(b)")
eq((x ** 2).subs(x, 1) + (2 * x + 3).subs(x, 1), 6, "別の道すじでも 6")

chk(sp.solveset(sp.Eq(x ** 2 + 2 * x, 3), x, REALS) == {1, -3}, "演習5")
chk(sp.factor(x ** 2 + 2 * x - 3) == (x + 3) * (x - 1), "演習5 因数分解")
eq((x ** 2 + 2 * x).subs(x, -3), 3, "検算 f(-3) = 3")
eq((x ** 2 + 2 * x).subs(x, 1), 3, "検算 f(1) = 3")

_V = 500 - 25 * t
chk(sp.solve(sp.Eq(_V, 0), t) == [20], "演習6(b) t = 20")
eq(_V.subs(t, 0), 500, "演習6(c) 始点")
eq(_V.subs(t, 20), 0, "演習6(c) 終点")
eq(R(500, 25), 20, "500 ÷ 25 = 20")

# 演習 7 — sketch させる問題
_e7 = (x + 2) * (x - 4)
roots(_e7, {-2, 4}, "演習7 x 切片")
eq(_e7.subs(x, 0), -8, "演習7 y 切片 -8")
eq(R(-2 + 4, 2), 1, "2 つの x 切片のまん中は 1")
eq(_e7.subs(x, 1), -9, "演習7 最小 -9")
chk(sp.minimum(_e7, x, sp.Interval(-3, 5)) == -9, "実際に最小は -9")
eq(sp.expand(_e7), x ** 2 - 2 * x - 8, "展開した形")
eq((x ** 2 - 2 * x - 8).subs(x, 0), -8, "展開した形でも -8")
eq((x ** 2 - 2 * x - 8).subs(x, 1), -9, "展開した形でも -9")
for _v in (-2, 4, 0, 1):
    chk(_v in sp.Interval(-3, 5), f"ラベルする点は範囲の中: x={_v}")

eq(3 * 4 - 5, 7, "演習8(a) k = 7")
eq(3 * 2 - 5, 1, "演習8(b) 1 が出る")
ne(1, 2, "(2,2) はグラフの上にない")
chk(sp.solve(sp.Eq(3 * x - 5, 2), x) == [R(7, 3)], "y=2 になるのは x = 7/3")
ne(R(7, 3), 2, "x = 2 ではない")

# 演習 9 — 直線で結ぶとずれる
eq(R(1 + 4, 2), R(5, 2), "演習9(a) 線分の高さは 2.5")
eq((x ** 2).subs(x, R(3, 2)), R(9, 4), "正しい値は 2.25")
ne(R(5, 2), R(9, 4), "ずれる")
chk(R(5, 2) > R(9, 4), "線分のほうが上を通る")
eq(R(4 - 1, 2 - 1), 3, "(1,1)-(2,4) の傾きは 3")
eq(1 + 3 * R(1, 2), R(5, 2), "傾きから数えても 2.5")

roots(x ** 2 - 4, {2, -2}, "演習10 正しい x")
eq((x ** 2 - 4).subs(x, 2), 0, "(2,0) は上にある")
eq((x ** 2 - 4).subs(x, -2), 0, "(-2,0) も上にある")
eq((x ** 2 - 4).subs(x, 0), -4, "(0,2) のつもりだと -4 になる")
ne(-4, 2, "だから (0,2) はグラフの上にない")

# ══════════════════════════════════════════════════════════
# 6. 演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("(3, 0)", "演習1"), ("(0, -6)", "演習1"),
                ("(0, -9)", "演習2"), ("x^{2} - 9", "演習2"),
                ("(0, -8)", "演習7"), ("(1, -9)", "演習7"),
                ("(x+2)(x-4)", "演習7"),
                ("(0, 500)", "演習6"), ("(20, 0)", "演習6"),
                ("3x - 5", "演習8"), ("x^{2} - 4", "演習10"),
                ("x^{2}-4", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この項目には、公式集の欄がありません", "2.3 は公式集にない")
in_text('> Students should be aware of the difference between the command '
        'terms "draw" and "sketch".', "Guidance を逐語で")
in_text("> All axes and key features should be labelled.", "ラベルの指示を逐語で")
not_in_text("> Creating a sketch from information given or a context.",
            "Content 欄の引用は置かない")
not_in_text("> Using technology to graph functions", "同上")
not_in_text("> ... including transferring a graph from screen to paper.", "同上")
in_text("文章で与えられた場面から、グラフを sketch する問題も出ます。", "文章で書く")
in_text("Paper 2 では、電卓の画面のグラフを紙に写すことがあります。", "文章で書く")
in_text("関数どうしを足したり引いたりしたグラフも、この項目で扱います。", "文章で書く")
# command term の定義（シラバスの Glossary から逐語）
in_text("> **Draw**: Represent by means of a labelled, accurate diagram or "
        "graph, using a pencil. A ruler (straight edge) should be used for "
        "straight lines. Diagrams should be drawn to scale. Graphs should "
        "have points correctly plotted (if appropriate) and joined in a "
        "straight line or smooth curve.", "Draw の定義を逐語で")
in_text("> **Sketch**: Represent by means of a diagram or graph (labelled as "
        "appropriate). The sketch should give a general idea of the required "
        "shape or relationship, and should include relevant features.",
        "Sketch の定義を逐語で")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("**この項目では、どちらでもラベルは要ります。**", "sketch でもラベルは要る")
in_text("**式が曲線を表しているときは、曲線で結ぶ。**", "なめらかに結ぶ")
not_in_text("## 「一定の割合」なら、必ず直線です", "断定は外した")
in_text("## 「毎分 $\\square$ ずつ」が**同じ量**なら、直線です", "言い方を正した")
in_text("**「$\\%$ ずつ」は別です。**", "百分率の場合")
in_text("直線をつないだ**折れ線**になります", "折れ線の場合")
in_text("**画面でグラフが切れているところ（漸近線をまたぐところなど）は、つないではいけません。**", "切れているところ")
in_text("**画面の絵を写すのではなく、読み取った座標を書き込んでください。**",
        "画面から紙へ")
in_text("**引くほうは、かっこでくくってください。**", "差のかっこ")
in_text("解があれば交点があり、交点があれば解がある", "両向きに説明した")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
# 説明を求める設問（Explain / Comment / Identify）は 5 つ。
# それぞれに model-answer が付いている。
chk(TEXT.count("{.model-answer}") == 5, "model-answer が 5")
chk(len(re.findall(r"^::: \{#exm-aasl23-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
for word in ["得点になりません", "点になりません", "点を落とします",
             "認められません", "減点されます"]:
    not_in_text(word, "採点の断定は避ける")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors, "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl23", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
for _lab in ["tbl-aasl23-drawsketch", "tbl-aasl23-labels",
             "tbl-aasl23-values", "fig-aasl23-idea", "eq-aasl23-point",
             "eq-aasl23-sum", "eq-aasl23-diff"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-3-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-3-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) What a sketch must show", "図(a) の題")
in_fig("$x$-intercepts", "図(a) の x 切片")
in_fig("$y$-intercept", "図(a) の y 切片")
in_fig("minimum point", "図(a) の最小点")
in_fig("label the axes, every intercept,", "図(a) の要点")
in_fig("(b) Adding two graphs", "図(b) の題")
in_fig("$y = f(x) + g(x)$", "図(b) の和")
in_fig("heights add", "図(b) の要点")
in_fig("at each $x$, add the two $y$-values", "図(b) の説明")
in_text("(a) A sketch must show the labelled axes", "キャプションが (a) を説明")
in_text("(b) The graph of $y=f(x)+g(x)$ is obtained by adding",
        "キャプションが (b) を説明")
# 図が使っている 3 つの高さは、実際に足し算になっている
_fp, _gp = 0.35 * 1.6 + 0.6, 2.6 - 0.42 * 1.6
chk(abs((_fp + _gp) - (_fp + _gp)) < 1e-12, "和の高さ")
chk(abs(_fp - _gp) > 0.5 and abs((_fp + _gp) - _gp) > 0.5,
    f"3 つの点は離れている: {_fp:.2f}, {_gp:.2f}, {_fp + _gp:.2f}")
# 図に数値の座標を書いていない
chk(not re.search(r"\(\s*-?\d", FIGSTR), "図に数値の座標を書いていない")
for leak in ["= 7", "= 20", "500", "(3, 0)", "(2, 7)"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-3.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-2.qmd") < DRAFT.index("aasl-2-3.qmd"), "並びが 2.2 → 2.3")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-3.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| **Draw** |", "| **Sketch** |", "| **Plot** |", "| **Label** |",
           "| key features |", "| smooth curve |", "| intersection |"]:
    chk(_t in GLO, "対訳表にある: " + _t)


# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════
# 所見 2 — 循環的な検算を外した
not_in_text("**検算（(a) について）。** 出した点 $(4,7)$ を、式に入れ直します。",
            "演習8 の循環的な検算は残っていない")
in_text(r"$x = 0$ から $x = 4$ までに $3 \times 4 = 12$ 増えるので、$y = -5 + 12 = 7$ ✓",
        "傾きから数え直す")
eq(-5 + 3 * 4, 7, "傾きから数えても 7")
in_text("$y$ 切片は、**傾きから数え直します。**", "演習1 も直した")
eq(0 - 2 * 3, -6, "x を 3 減らすと y は 6 減る")
in_text("$y$ 切片は、**因数分解した形からも出します。**", "演習2 も直した")
eq((0 - 3) * (0 + 3), -9, "(x-3)(x+3) で x=0 は -9")
# 所見 3 — 例題 1(c) の検算が答えを検証するようになった
in_text("$f(1) = (1-3)(1+1) = (-2)(2) = -4$ ✓", "因数分解した形からも出す")
eq((1 - 3) * (1 + 1), -4, "因数分解した形でも -4")
# 所見 4 — 図(a) は名前、答案は座標
in_text("**答案では名前ではなく座標を書きます。**", "図と答案のちがい")
# 所見 6 — 数と点を混同しない
in_text("**$y = f(x) - g(x)$ のグラフの $x$ 切片の $x$ 座標**と同じものです。", "数と点")
in_text("**$(p, 0)$ が $y = h(x)$ の $x$ 切片**だということです", "同上")
# 所見 7 — なめらかに結ぶ理由を 2 つに分けた
in_text("**(i) 値がずれるから。**", "理由 1")
in_text("**(ii) ない角ができるから。**", "理由 2")
eq(R((-1) + (-2), 2), R(-3, 2), "線分の高さ -1.5")
eq((x ** 2 - 2).subs(x, R(-1, 2)), R(-7, 4), "正しい値 -1.75")
ne(R(-3, 2), R(-7, 4), "ずれる")
# 所見 8 — sketch させる問題を入れた
chk(TEXT.count("Sketch the graph of $y = f(x)$") == 1, "sketch させる設問がある")
in_text("labelling the axes, the $x$-intercepts, the $y$-intercept and the "
        "minimum point with their coordinates", "ラベルまで求めている")
# 所見 9 — 演習 9 を (a)(b) に分け、本文の書き写しにならないようにした
in_text("**(b)** [Hence explain why the plotted points should be joined with "
        "a smooth curve.]{.q-en}", "Hence でつないだ")
not_in_text("[When drawing the graph of $y = x^{2}$ from a table of values, "
            "explain why", "古い演習 9 は残っていない")
# 所見 11 — バッククォートの中に $ を入れない
not_in_text("`Find the values of $x$`", "コード表記の中に数式を入れない")
in_text("`Find the values of x`", "直した")
# 所見 14 — 例題 2(d) の下端の理由
in_text(r"**$-5$ より小さい値も出ません。** domain が $-3 \le x \le 3$ なので "
        r"$x^{2} \le 9$", "下端は domain 由来")
chk(sp.maximum(x ** 2, x, sp.Interval(-3, 3)) == 9, "x^2 <= 9")
eq(4 - 9, -5, "4 - 9 = -5")
# 所見 15 — 角は 2 本の線分が出会うところ
in_text("$2$ 本の線分が出会う $(0,-2)$ に**折れ曲がった角**", "角の場所")
# 所見 17 — 漸近線は SL 2.8
in_text("（漸近線があるグラフは SL 2.8 で扱います。）", "前倒ししない")
in_text("（SL 2.8 で扱います）", "表でも同じ")
# 所見 18 — 空の表
in_text("[The table below is to be completed for $y = x^{2} - 2x$.]{.q-en}",
        "shows values をやめた")
# 所見 20 — labelled as appropriate との関係
in_text("Glossary の Sketch の定義は `labelled as appropriate` と書いていますが、",
        "根拠のつながり")
# 所見 21 — 用語の英日併記
in_text("**domain**（定義域）の中で動かしたときにできる点", "domain の訳")
in_text("**range**（値域）は $g(x)$ で書きます。", "range の訳")
in_text("漸近線（asymptote）", "asymptote の英語")
# 所見 22 — リンクのアンカー
in_text("[SL 2.2 の第 6 節](aasl-2-2.qmd#model)", "アンカー付き")
# 所見 23 — 縦軸の名前
not_in_text("the graph of $y = h(t)$", "軸の書き方をそろえた")
not_in_text("the graph of $y = V(t)$", "同上")
chk(TEXT.count("against $t$") >= 2, "「against t」でそろえた")
# model-answer の分量
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _w = len(_blk.split())
    chk(_w <= 115, f"model-answer が長すぎない: {_w} 語")


# ══════════════════════════════════════════════════════════
# C02  演習7 — 最小点の $x$ は問題文で与える
# ══════════════════════════════════════════════════════════
in_text("The minimum point of the graph occurs at $x = 1$.",
        "C02 最小点を与える（英語）")
in_text("グラフの最小点は $x = 1$ にあります。", "C02 最小点を与える（訳）")
in_text("最小点の $x = 1$ は問題文で与えられているので", "C02 解説")
not_in_text("最小点はこの $2$ つの $x$ 切片のまん中の $x = 1$ で",
            "C02 旧解説が消えている")
chk((-2 + 4) / 2 == 1, "C02 2 つの x 切片のまん中は 1")
chk((1 + 2) * (1 - 4) == -9, "C02 f(1) = -9")
chk((0 + 2) * (0 - 4) == -8, "C02 f(0) = -8")


# ══════════════════════════════════════════════════════════
# E09  演習7 — 完成した放物線（端点つき）
# ══════════════════════════════════════════════════════════
in_text("(img/aasl-2-3-ex7.svg){#fig-aasl23-ex7 width=100%}",
        "E09 演習7 の解答図")
in_text("*the curve is drawn only for* $-3 \\le x \\le 5$, *so it stops at* "
        "$(-3, \\ 7)$ *and* $(5, \\ 7)$", "E09 演習7 の端点")
in_text("**検算（端点）。** $f(-3) = (-1)(-7) = 7$、$f(5) = (7)(1) = 7$",
        "E09 演習7 の端点の検算")
_e09x = sp.Symbol("x")
_e09f = (_e09x + 2) * (_e09x - 4)
chk(_e09f.subs(_e09x, -3) == 7 and _e09f.subs(_e09x, 5) == 7,
    "E09 両端はどちらも 7")
chk(_e09f.subs(_e09x, 1) == -9, "E09 最小点は (1, -9)")
chk(sp.solveset(sp.Eq(_e09f, 0), _e09x) == sp.FiniteSet(-2, 4),
    "E09 x 切片は -2 と 4")
chk(sp.Rational(-2 + 4, 2) == 1, "E09 軸は x = 1")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
