"""AA SL 2.7b（判別式と解の種類）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_7b.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-7b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_7b.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, k, c = sp.symbols("x k c")
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


def disc(a, b, cc):
    return sp.expand(b ** 2 - 4 * a * cc)


def nroots(expr, want, msg=""):
    chk(len(sp.solveset(sp.Eq(expr, 0), x, REALS)) == want,
        f"実数解の個数が {want}: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 判別式の意味そのもの
# ══════════════════════════════════════════════════════════
_a = sp.Symbol("a", nonzero=True)
_b, _c = sp.symbols("b c")
# Δ は解の公式の根号の中
_sols = sp.solve(sp.Eq(_a * x ** 2 + _b * x + _c, 0), x)
chk(len(_sols) == 2, "一般には解は 2 つ")
chk(all(sp.sqrt(_b ** 2 - 4 * _a * _c) in s.atoms(sp.Pow) or True
        for s in _sols), "根号の中は b^2-4ac")
# 頂点の y 座標 = -Δ/(4a)
eq(_c - _b ** 2 / (4 * _a), -(_b ** 2 - 4 * _a * _c) / (4 * _a),
   "頂点の y = -Δ/(4a)")
# 符号ごとの解の個数（具体例で）
for _e, _d, _n in [(x ** 2 - 1, 4, 2), (x ** 2, 0, 1), (x ** 2 + 1, -4, 0)]:
    _p = sp.Poly(_e, x).all_coeffs()
    while len(_p) < 3:
        _p.append(0)
    eq(disc(_p[0], _p[1], _p[2]), _d, f"Δ = {_d}")
    nroots(_e, _n, f"Δ = {_d} のとき")
# 本文（シラバスの例）
eq(disc(3 * k, 2, k), 4 - 12 * k ** 2, "本文 Δ = 4-12k^2")
chk(sp.solveset(sp.Eq(4 - 12 * k ** 2, 0), k, REALS)
    == {sp.sqrt(3) / 3, -sp.sqrt(3) / 3}, "本文 k = ±√3/3")
eq(1 / sp.sqrt(3), sp.sqrt(3) / 3, "有理化")
chk(sp.sqrt(3) / 3 != 0, "k ≠ 0 を満たす")

# ══════════════════════════════════════════════════════════
# 1. 例題 1
# ══════════════════════════════════════════════════════════
eq(disc(1, 4, 1), 12, "例題1(a) Δ = 12")
nroots(x ** 2 + 4 * x + 1, 2, "例題1(a)")
eq(disc(1, -6, 9), 0, "例題1(b) Δ = 0")
nroots(x ** 2 - 6 * x + 9, 1, "例題1(b)")
chk(sp.factor(x ** 2 - 6 * x + 9) == (x - 3) ** 2, "(x-3)^2")
eq(disc(2, 1, 3), -23, "例題1(c) Δ = -23")
nroots(2 * x ** 2 + x + 3, 0, "例題1(c)")
eq(-disc(2, 1, 3) / (4 * 2), R(23, 8), "例題1(c) 頂点の y = 23/8")
chk(R(23, 8) > 0, "正")
chk(not sp.sqrt(12).is_integer, "12 は平方数でない")
chk(sp.solveset(sp.Eq(x ** 2 + 4 * x + 1, 0), x, REALS)
    == {-2 + sp.sqrt(3), -2 - sp.sqrt(3)}, "例題1(a) の解")

# ══════════════════════════════════════════════════════════
# 2. 例題 2
# ══════════════════════════════════════════════════════════
eq(disc(k, 4, k), 16 - 4 * k ** 2, "例題2(a)")
chk(sp.solveset(sp.Eq(16 - 4 * k ** 2, 0), k, REALS) == {2, -2}, "例題2(b)")
nroots((2 * x ** 2 + 4 * x + 2), 1, "例題2(c) k=2 で 1 点")
chk(sp.factor(2 * x ** 2 + 4 * x + 2) == 2 * (x + 1) ** 2, "2(x+1)^2")
eq((2 * x ** 2 + 4 * x + 2).subs(x, -1), 0, "検算 x=-1")
nroots((-2 * x ** 2 + 4 * x - 2), 1, "k=-2 でも 1 点")
chk(sp.factor(-2 * x ** 2 + 4 * x - 2) == -2 * (x - 1) ** 2, "-2(x-1)^2")
# k = 0 なら 1 次
chk(sp.solveset(sp.Eq(4 * x, 0), x, REALS) == {0}, "k=0 なら解は 1 つ")
# Δ を 16-4k と誤ると k = 4
chk(sp.solveset(sp.Eq(16 - 4 * k, 0), k, REALS) == {4}, "誤ると k = 4")
eq(disc(4, 4, 4), -48, "その k では Δ = -48")
chk(-48 < 0, "実数解がない（条件と合わない）")

# ══════════════════════════════════════════════════════════
# 3. 例題 3
# ══════════════════════════════════════════════════════════
eq(disc(1, 6, c), 36 - 4 * c, "例題3(a)")
chk(sp.solveset(36 - 4 * c < 0, c, REALS) == sp.Interval.open(9, sp.oo),
    "例題3(b) c > 9")
chk(sp.solveset(sp.Eq(36 - 4 * c, 0), c, REALS) == {9}, "例題3(c) c = 9")
nroots(x ** 2 + 6 * x + 9, 1, "c=9 で 1 点")
chk(sp.factor(x ** 2 + 6 * x + 9) == (x + 3) ** 2, "(x+3)^2")
eq((x ** 2 + 6 * x + 9).subs(x, -3), 0, "検算 x=-3")
eq(-(36 - 4 * c) / 4, c - 9, "頂点の y = c-9")
eq(disc(1, 6, 10), -4, "c=10 で Δ = -4")
eq(disc(1, 6, 8), 4, "c=8 で Δ = 4")
chk(sp.minimum((x ** 2 + 6 * x + 10), x, REALS) == 1, "c=10 の最小は 1")

# ══════════════════════════════════════════════════════════
# 4. 例題 4
# ══════════════════════════════════════════════════════════
eq(sp.expand((x ** 2 + 3 * x + 4) - (2 * x + k)), x ** 2 + x + 4 - k, "例題4(a)")
eq(disc(1, 1, 4 - k), 4 * k - 15, "例題4 Δ = 4k-15")
chk(sp.solveset(sp.Eq(4 * k - 15, 0), k, REALS) == {R(15, 4)}, "例題4(b)")
chk(sp.solveset(4 * k - 15 < 0, k, REALS)
    == sp.Interval.open(-sp.oo, R(15, 4)), "例題4(c)")
eq(4 - R(15, 4), R(1, 4), "k=15/4 で定数項は 1/4")
eq(sp.expand((x + R(1, 2)) ** 2), x ** 2 + x + R(1, 4), "(x+1/2)^2")
nroots(x ** 2 + x + R(1, 4), 1, "接点は 1 つ")
eq(disc(1, 1, 4), -15, "k=0 では Δ = -15")
eq(disc(1, 1, -1), 5, "k=5 では Δ = 5")
chk(sp.solveset(4 * k - 15 > 0, k, REALS) == sp.Interval.open(R(15, 4), sp.oo),
    "2 点で交わるのは k > 15/4")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(disc(1, 5, 2), 17, "演習1")
nroots(x ** 2 + 5 * x + 2, 2, "演習1")
eq(-disc(1, 5, 2) / 4, -R(17, 4), "頂点の y は負")
chk(sp.isprime(17), "17 は素数")

eq(disc(1, -8, 16), 0, "演習2(a)")
eq(-(-8) / (2 * 1), 4, "演習2(b) x = 4")
chk(sp.factor(x ** 2 - 8 * x + 16) == (x - 4) ** 2, "(x-4)^2")
eq((x ** 2 - 8 * x + 16).subs(x, 4), 0, "検算")

eq(disc(3, 2, 5), -56, "演習3")
nroots(3 * x ** 2 + 2 * x + 5, 0, "演習3")
eq(-disc(3, 2, 5) / (4 * 3), R(14, 3), "頂点の y = 14/3")

eq(disc(1, k, 9), k ** 2 - 36, "演習4")
chk(sp.solveset(sp.Eq(k ** 2 - 36, 0), k, REALS) == {6, -6}, "演習4 k = ±6")
chk(sp.factor(x ** 2 + 6 * x + 9) == (x + 3) ** 2, "k=6 で (x+3)^2")
chk(sp.factor(x ** 2 - 6 * x + 9) == (x - 3) ** 2, "k=-6 で (x-3)^2")

eq(disc(2, 3, c), 9 - 8 * c, "演習5")
chk(sp.solveset(9 - 8 * c < 0, c, REALS) == sp.Interval.open(R(9, 8), sp.oo),
    "演習5 c > 9/8")
eq(disc(2, 3, 2), -7, "c=2 で Δ = -7")
eq(disc(2, 3, 1), 1, "c=1 で Δ = 1")
eq(disc(2, 3, R(9, 8)), 0, "境目で Δ = 0")

eq(disc(1, -4, k), 16 - 4 * k, "演習6")
chk(sp.solveset(16 - 4 * k > 0, k, REALS) == sp.Interval.open(-sp.oo, 4),
    "演習6 k < 4")
nroots(x ** 2 - 4 * x + 3, 2, "k=3 で 2 解")
chk(sp.factor(x ** 2 - 4 * x + 3) == (x - 1) * (x - 3), "(x-1)(x-3)")
nroots(x ** 2 - 4 * x + 4, 1, "k=4 で 1 点")
eq(disc(1, -4, 5), -4, "k=5 で Δ = -4")

eq(disc(1, 1, 1), -3, "演習7")
nroots(x ** 2 + x + 1, 0, "演習7")
eq(sp.expand((x + R(1, 2)) ** 2 + R(3, 4)), x ** 2 + x + 1, "平方完成でも")
eq(-disc(1, 1, 1) / 4, R(3, 4), "頂点の y = 3/4")

eq(sp.expand((x ** 2 + 3) - (x + 1)), x ** 2 - x + 2, "演習8")
eq(disc(1, -1, 2), -7, "演習8 Δ = -7")
nroots(x ** 2 - x + 2, 0, "出会わない")
eq(-disc(1, -1, 2) / 4, R(7, 4), "差の最小は 7/4 > 0")
chk(R(7, 4) > 0, "曲線が上")

eq(disc(2, 3, 5), -31, "演習9")
nroots(2 * x ** 2 + 3 * x + 5, 0, "演習9")
eq(-disc(2, 3, 5) / (4 * 2), R(31, 8), "頂点の y = 31/8")

eq(disc(1, k, 4), k ** 2 - 16, "演習10")
chk(sp.solveset(sp.Eq(k ** 2 - 16, 0), k, REALS) == {4, -4}, "演習10 k = ±4")
chk(sp.factor(x ** 2 + 4 * x + 4) == (x + 2) ** 2, "k=4 で (x+2)^2")
chk(sp.factor(x ** 2 - 4 * x + 4) == (x - 2) ** 2, "k=-4 で (x-2)^2")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("x^{2}+4x+1", "例題1"), ("x^{2}-6x+9", "例題1"),
                ("2x^{2}+x+3", "例題1"), ("16 - 4k^{2}", "例題2"),
                ("36 - 4c", "例題3"), ("4k - 15", "例題4"),
                ("\\frac{15}{4}", "例題4"),
                ("x^{2} + 5x + 2", "演習1"), ("x^{2} - 8x + 16", "演習2"),
                ("3x^{2} + 2x + 5", "演習3"), ("k^{2} - 36", "演習4"),
                ("9 - 8c", "演習5"), ("16 - 4k$", "演習6"),
                ("x^{2} + x + 1", "演習7"), ("x^{2} - x + 2", "演習8"),
                ("2x^{2} + 3x + 5", "演習9"), ("k^{2} - 16", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この式は公式集にあります", "判別式は公式集にある")
in_text("公式集の **2.7** の欄に `Discriminant` として印刷されています。", "欄の名前")
in_text("> $\\Delta = b^{2} - 4ac$", "公式集を逐語で")
# ★ シラバスの逐語引用はページに置かない（査読で 2 か所を削除）
not_in_text("the nature of the roots, that is,", "シラバスの逐語引用は置かない")
not_in_text("Example: Find $k$ given that", "シラバスの逐語引用は置かない")
not_in_text("シラバスは、", "「シラバスは」で始まる文は置かない")
chk(TEXT.count("\n> ") == 1, f"引用は公式集の 1 つだけ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.index("$$ {#eq-aasl27b-disc}") < TEXT.index("## この式は公式集にあります"),
    "公式集の callout は式の直後")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## 「$2$ 実解」と「ちがう $2$ 実解」はちがいます", "distinct の区別")
in_text("## $\\Delta < 0$ は「解がない」ではありません", "real を落とさない")
in_text("## 文字が $a$ の位置にあるときは、$a \\neq 0$ を確かめてください", "a ≠ 0")
in_text("$a > 0$ なら全部が上、$a < 0$ なら全部が下です。", "a の符号で場合分け")
in_text("$a < 0$ なら、すべて逆になります。", "Why it works でも")
in_text("**ただし、$\\Delta$ が $0$ にとても近いときは、画面では見分けられません。**",
        "電卓の限界")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
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
chk(TEXT.count("{.model-answer}") == 6, "model-answer が 6")
chk(len(re.findall(r"^::: \{#exm-aasl27b-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h_ for h_ in _h2 if h_ in _want] == _want, "5 つの見出しが所定の順")
chk([h_ for h_ in _h2 if h_ in _want][-1] == "Exercises", "Exercises で終わる")
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
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl27b", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
for _lab in ["tbl-aasl27b-nature", "tbl-aasl27b-graph", "tbl-aasl27b-line",
             "fig-aasl27b-idea", "eq-aasl27b-disc"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-7b-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-7b-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) The sign of the discriminant", "図(a) の題")
in_fig("two distinct\\nreal roots", "図(a) Δ>0")
in_fig("two equal\\nreal roots", "図(a) Δ=0")
in_fig("no real\\nroots", "図(a) Δ<0")
in_fig("$\\\\Delta = b^{2} - 4ac$", "図(a) の式")
in_fig("(b) A line and a curve", "図(b) の題")
in_fig("two points: $\\\\Delta > 0$", "図(b) 2 点")
in_fig("tangent: $\\\\Delta = 0$", "図(b) 接する")
in_fig("no point: $\\\\Delta < 0$", "図(b) 出会わない")
in_text("(a) The sign of the discriminant decides how many times",
        "キャプションが (a) を説明")
in_text("(b) Substituting a line into a curve gives a quadratic",
        "キャプションが (b) を説明")
# 図に k の値などを書いていない
chk(not re.search(r"k\s*=", FIGSTR), "図に k の値を書いていない")
for leak in ["15", "= 2", "= 9", "= 4"]:
    chk(leak not in FIGSTR, "図が答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-7b.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-7a.qmd") < DRAFT.index("aasl-2-7b.qmd"),
    "並びが 2.7a → 2.7b")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-7b.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| discriminant |", "| distinct |", "| tangent |",
           "| nature of the roots |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
#     -Δ/(4a) を使った「検算」は循環しているので、
#     平方完成や符号の変化といった独立した道すじに置きかえた。
# ══════════════════════════════════════════════════════════

# --- 循環していた検算が復活していないこと ------------------------------
_WHY = TEXT[TEXT.index("## Why it works"):TEXT.index("## Worked examples")]
chk(TEXT.count(r"\dfrac{\Delta}{4a}") == _WHY.count(r"\dfrac{\Delta}{4a}") == 1,
    "-Δ/(4a) を使うのは Why it works の 1 か所だけ（検算では使わない）")
chk(TEXT.count(r"-\frac{\Delta}{4a}") == 1,
    "-Δ/(4a) の導出は 1 か所")

# --- 例題1：検算の順と、独立した道すじ ----------------------------------
_ia = TEXT.index("**検算（(a) について）。** **$\\Delta$ を使わずに、解が $2$ つあることを確かめます。**")
_ib = TEXT.index("**検算（(b) について）。** **実際に解いて、$1$ 点になるかを見ます。**")
_ic = TEXT.index("**検算（(c) について）。** **判別式を通らない道でも見ます。**")
chk(_ia < _ib < _ic, "例題1 の検算は (a) → (b) → (c) の順")
for _v, _w in [(0, 1), (-1, -2), (-4, 1)]:
    eq((x**2 + 4 * x + 1).subs(x, _v), _w, f"例題1(a) 検算 f({_v})")
in_text("$f(0) = 1 > 0$、$f(-1) = 1-4+1 = -2 < 0$、$f(-4) = 16-16+1 = 1 > 0$",
        "例題1(a) の符号の変化")
eq(2 * (x + R(1, 4))**2 + R(23, 8), 2 * x**2 + x + 3, "例題1(c) の平方完成")
in_text(r"2x^{2}+x+3 = 2\left(x+\frac{1}{4}\right)^{2} - \frac{1}{8} + 3 = 2\left(x+\frac{1}{4}\right)^{2} + \frac{23}{8}",
        "例題1(c) 検算の平方完成")
not_in_text(r"$-\dfrac{\Delta}{4a} = -\dfrac{-23}{8}", "例題1(c) の循環検算は消した")
not_in_text("$12$ は平方数ではないので", "例題1(a) の平方数の話は差しかえた")

# --- 例題2：かけ忘れの説明 ----------------------------------------------
in_text("（$c$ が $k$ なのに $1$ として計算した誤り）", "例題2 の誤りの説明")
not_in_text("$c = k$ を $2$ 回かけ忘れた誤り", "「2 回かけ忘れ」は消した")

# --- 例題3：$c = c$、設問、解答例 ----------------------------------------
in_text("**(a)** $a = 1$、$b = 6$ で、定数項はそのまま $c$ です。", "例題3(a) の書き方")
not_in_text("$b = 6$、$c = c$ です", "「c = c」は消した")
in_text("[Find the set of values of $c$ for which the equation has no real roots.]",
        "例題3(b) は set of values")
eq((x + 3)**2 + sp.Symbol("c") - 9, x**2 + 6 * x + sp.Symbol("c"),
   "例題3(d) の平方完成 (x+3)^2 + c - 9")
in_text("*Completing the square gives $y = (x+3)^{2} + c - 9$. A square is never "
        "negative, so the smallest value of $y$ is $c - 9$, which is positive "
        "when $c > 9$.", "例題3(d) の解答例（自己完結）")
not_in_text("from part (b)", "例題3(d) は (b) を引かない")
not_in_text(r"\dfrac{4c-36}{4} = c-9 > 0", "例題3(d) の -Δ/(4a) は消した")

# --- 例題4：(a) の検算を独立にし、順を (a)(b)(c) にした ------------------
_ja = TEXT.index("**検算（(a) について）。** **$k$ に $1$ つ値を入れて、出た $x$ で")
_jb = TEXT.index("**検算（(b) について）。** **接点を実際に求めて、")
_jc = TEXT.index("**検算（(c) について）。** **範囲の中と外で、")
chk(_ja < _jb < _jc, "例題4 の検算は (a) → (b) → (c) の順")
chk(sp.factor(x**2 + x + 4 - 6) == (x + 2) * (x - 1), "k=6 で (x+2)(x-1)")
for _v in (-2, 1):
    eq(2 * _v + 6, _v**2 + 3 * _v + 4, f"k=6 のとき x={_v} で直線と曲線が一致")
in_text("- $x = 1$：直線は $y = 2(1)+6 = 8$、曲線は $y = 1+3+4 = 8$ ✓",
        "例題4(a) 検算の x=1")
in_text("- $x = -2$：直線は $y = 2(-2)+6 = 2$、曲線は $y = 4-6+4 = 2$ ✓",
        "例題4(a) 検算の x=-2")
not_in_text("この方程式の解を $x$ とすると、$x^{2}+3x+4$ と $2x+5$ の差は",
            "例題4(a) の循環検算は消した")
in_text("[Find the set of values of $k$ for which the line and the curve do not meet.]",
        "例題4(c) は set of values")
not_in_text("as found in part (c)", "例題4(d) は (c) を引かない")

# --- 第 5 節：「1 点で出会う」の但し書き --------------------------------
in_text("**放物線と直線が出会う点がちょうど $1$ つなら $\\Delta = 0$**、つまり接しています。",
        "第 5 節の言い方")
in_text("$x = 3$ のような**縦の直線**は、放物線と必ずちょうど $1$ 点で出会いますが、接してはいません。",
        "縦の直線の但し書き")
not_in_text("**「$1$ 点で交わる」も、放物線と直線なら", "古い言い方は消した")

# --- 第 6 節・Why it works：「f が 2 次関数のとき」----------------------
in_text("**$f$ が $2$ 次関数のとき**、すべてを片側に集めると **$2$ 次方程式**になります",
        "第 6 節の前提")
in_text("**$f$ が $2$ 次関数なら**、$f(x) = mx+c$ を片側に集めると",
        "Why it works の前提")

# --- Why it works：頂点がいちばん低い（高い）点だという段 ----------------
in_text("頂点は、**$a > 0$ ならグラフのいちばん低い点、$a < 0$ ならいちばん高い点**です",
        "頂点が端の点であること")
in_text("グラフが $x$ 軸に届くのはその $1$ 点だけで、**横切らずに接します**",
        "接する理由")

# --- 「x 軸上にある」（「x 軸の上にある」ではない）-----------------------
not_in_text("頂点が $x$ 軸の上にある", "「x 軸の上にある」は使わない")
chk(TEXT.count("頂点が $x$ 軸上にある") == 4, "「頂点が x 軸上にある」が 4 か所")

# --- two real roots の言い方をやわらげた --------------------------------
in_text("`distinct` の付かない `two real roots` は、ふつう $\\Delta \\ge 0$（等しい場合も含む）と読みます。",
        "two real roots の但し書き")
in_text("`distinct` があれば $\\Delta > 0$、なければふつう $\\Delta \\ge 0$ です",
        "Common errors 側も「ふつう」")

# --- GDC の callout -----------------------------------------------------
in_text("**値を入れていない変数は、そのまま文字として返ってきます**", "未定義変数の説明")
# 2026-09: 生徒は全員 TI-Nspire CX II なので、CAS／非CAS の区別には触れない
in_text("**$k$ を含む判別式を、電卓に解かせることはできません。**", "文字は手で")
not_in_text("CAS")
in_text("aasl-2-7a.qmd#write", "C11 2.7a への案内")
not_in_text("solve(b^2-4*a*c=0,k)", "CAS 前提の solve( は消した")
chk(TEXT.count("::: {.callout-tip collapse=\"true\"}\n## Paper 2 では") == 1,
    "GDC の callout は 1 つだけ")

# --- 演習1：符号の変化で見る -------------------------------------------
for _v, _w in [(0, 2), (-1, -2), (-5, 2)]:
    eq((x**2 + 5 * x + 2).subs(x, _v), _w, f"演習1 検算 f({_v})")
in_text("$f(0) = 2 > 0$、$f(-1) = 1-5+2 = -2 < 0$、$f(-5) = 25-25+2 = 2 > 0$",
        "演習1 の符号の変化")

# --- 演習2：**(a)** を .q-en の外に出した -------------------------------
in_text("[2]{.ex-no} **(a)** [Find the discriminant of $x^{2} - 8x + 16 = 0$.]{.q-en}",
        "演習2 の (a) は .q-en の外")

# --- 演習3：平方完成 -----------------------------------------------------
eq(3 * (x + R(1, 3))**2 + R(14, 3), 3 * x**2 + 2 * x + 5, "演習3 の平方完成")
in_text(r"3x^{2}+2x+5 = 3\left(x+\frac{1}{3}\right)^{2} - \frac{1}{3} + 5 = 3\left(x+\frac{1}{3}\right)^{2} + \frac{14}{3}",
        "演習3 検算の平方完成")

# --- 演習4：x^2+kx+25（k = ±10）------------------------------------------
_k = sp.Symbol("k")
eq(_k**2 - 4 * 1 * 25, _k**2 - 100, "演習4 の判別式")
chk(sp.solveset(sp.Eq(_k**2 - 100, 0), _k, REALS) == sp.FiniteSet(-10, 10),
    "演習4 の答えは k = ±10")
chk(sp.factor(x**2 + 10 * x + 25) == (x + 5)**2, "k=10 で (x+5)^2")
chk(sp.factor(x**2 - 10 * x + 25) == (x - 5)**2, "k=-10 で (x-5)^2")
in_text("[The equation $x^{2} + kx + 25 = 0$ has two equal real roots. "
        "Find the possible values of $k$.]", "演習4 の設問")
not_in_text("$x^{2} + kx + 9 = 0$", "演習4 の古い形は消した")
in_text(r"$$k = \pm 10$$", "演習4 の答え")

# --- 演習5・6：set of values --------------------------------------------
in_text("has no real roots. Find the set of values of $c$.]", "演習5 は set of values")
in_text("has two distinct real roots. Find the set of values of $k$.]",
        "演習6 は set of values")

# --- 演習7（E01）：重解と $(x-2)^2 > 0$ --------------------------------
not_in_text("平方完成の $k$ と一致しています", "「平方完成の k」は消した")
in_text("[Solve $(x-2)^{2} > 0$, and find the discriminant of "
        "$(x-2)^{2} = 0$.", "E01 演習7 の英語")
in_text("$(x-2)^{2} > 0$ を解き、$(x-2)^{2} = 0$ の判別式を"
        "求めなさい。", "E01 演習7 の訳")
in_text("$\\Delta = 0$ は**重解**（equal roots）です。", "E01 演習7 は重解")
in_text("$x < 2 \\quad \\text{or} \\quad x > 2$", "E01 演習7 の答え")
# (x-2)^2 = x^2-4x+4 で判別式は 0、解は x=2 以外のすべて
eq((x - 2)**2, x**2 - 4 * x + 4, "E01 (x-2)^2 の展開")
chk((-4)**2 - 4 * 1 * 4 == 0, "E01 演習7 の判別式は 0")
chk(all(((_v - 2)**2 > 0) for _v in (-1, 0, 1, 3, 5)),
    "E01 x=2 以外では正")
chk(((2 - 2)**2 > 0) is False, "E01 x=2 では成り立たない")

# --- 演習8：差の関数を平方完成で ----------------------------------------
eq((x - R(1, 2))**2 + R(7, 4), x**2 - x + 2, "演習8 の平方完成")
in_text(r"x^{2}-x+2 = \left(x-\frac{1}{2}\right)^{2} - \frac{1}{4} + 2 = \left(x-\frac{1}{2}\right)^{2} + \frac{7}{4}",
        "演習8 検算の平方完成")

# --- 演習9（E01）：解なし と 上に凸の不等式 ----------------------------
in_text("[Show that the inequality $x^{2} + 1 \\le 0$ has no "
        "solutions.]", "E01 演習9(a) の英語")
in_text("[Solve $-x^{2} + 4 > 0$.", "E01 演習9(b) の英語")
in_text("不等式 $x^{2}+1 \\le 0$ に解がないことを示しなさい。",
        "E01 演習9(a) の訳")
in_text("$-x^{2}+4 > 0$ を解きなさい。", "E01 演習9(b) の訳")
in_text("$$-2 < x < 2$$", "E01 演習9(b) の答え")
in_text("**$\\Delta < 0$ と $a > 0$ の両方がそろって、はじめて"
        "「つねに正」と言えます**", "E01 Δ<0 だけでは足りない")
# x^2+1 は実数で最小 1、-x^2+4 > 0 の解は -2 < x < 2
chk(0**2 - 4 * 1 * 1 == -4, "E01 x^2+1 の判別式は -4")
chk(sp.minimum(x**2 + 1, x) == 1, "E01 x^2+1 の最小値は 1")
chk(sp.solveset(-x**2 + 4 > 0, x, sp.S.Reals)
    == sp.Interval.open(-2, 2), "E01 -x^2+4>0 は 1 つの区間")
chk(sp.solveset(x**2 - 4 > 0, x, sp.S.Reals)
    == sp.Union(sp.Interval.open(-sp.oo, -2),
                sp.Interval.open(2, sp.oo)), "E01 下に凸なら 2 区間")
chk(0**2 - 4 * (-1) * 4 == 16, "E01 -x^2+4 の判別式は 16")

# --- 対訳表 --------------------------------------------------------------
_GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| discriminant |", "| distinct |", "| nature of the roots |",
           "| tangent |", "| repeated root |"]:
    chk(_t in _GLO, "対訳表にある: " + _t)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
