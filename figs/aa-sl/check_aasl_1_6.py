"""AA SL 1.6（簡単な演繹的証明）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_6.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-6.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_6.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x, n, m = sp.symbols("x n m")


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def _S(v):
    if isinstance(v, float):
        return sp.Rational(str(v))
    return sp.nsimplify(v, rational=True)


def eq(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) == 0, msg + f"  ({a} vs {b})")


def ne(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) != 0, msg + f"  ({a} vs {b})")


def ident(lhs, rhs, msg=""):
    """恒等式（すべての値で等しい）であることを確かめる。"""
    chk(sp.simplify(sp.expand(lhs) - sp.expand(rhs)) == 0, "恒等式でない: " + msg)


def not_ident(lhs, rhs, msg=""):
    chk(sp.simplify(sp.expand(lhs) - sp.expand(rhs)) != 0, "恒等式になってしまう: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
# 第 2 節・図(a) の見本
ident((x + 2) ** 2 - 4 * x, x ** 2 + 4, "(x+2)^2 - 4x = x^2 + 4")
eq(sp.expand((x + 2) ** 2), x ** 2 + 4 * x + 4, "(x+2)^2 の展開")
# 第 3 節：= と ≡
_sol = sp.solve(sp.Eq(2 * x + 1, 7), x)
chk(_sol == [3], f"2x+1 = 7 の解は x=3 だけ: {_sol}")
ne((2 * 0 + 1), 7, "x=0 では成り立たない")
ident((x + 1) ** 2, x ** 2 + 2 * x + 1, "(x+1)^2 は恒等式")
for _t in [-7, 0, 100]:
    eq((_t + 1) ** 2, _t ** 2 + 2 * _t + 1, f"x={_t} でも成り立つ")
# 第 4 節
eq(sp.Rational(1, 3) + sp.Rational(1, 6), sp.Rational(1, 2), "1/3 + 1/6 = 1/2")
eq(sp.Rational(2, 6) + sp.Rational(1, 6), sp.Rational(3, 6), "通分の途中")
chk(sp.Rational(1, 3) != sp.Rational("0.333"), "1/3 は 0.333 ではない")
# 第 5 節
eq(sp.Rational(1, 5) - sp.Rational(1, 6), sp.Rational(1, 30), "1/5 - 1/6 = 1/30")
eq(5 * 6, 30, "30 = 5×6")
ident(1 / n - 1 / (n + 1), 1 / (n * (n + 1)), "部分分数の恒等式")
eq(sp.simplify(((n + 1) - n)), 1, "分子は 1 になる")
# 第 6 節
ident(n + (n + 1) + (n + 2), 3 * (n + 1), "連続する 3 整数の和は 3(n+1)")
ident(n + (n + 1), 2 * n + 1, "連続する 2 整数の和は 2n+1")
ident((2 * n + 1) + (2 * n + 3), 4 * (n + 1), "連続する 2 奇数の和は 4(n+1)")
# 第 7 節
eq(sp.Rational(1, 5) - sp.Rational(1, 6), sp.Rational(1, 5 * 6), "n=5 の検算")
# 1 点で合っても恒等式ではない例
eq((0 + 3) ** 2, 0 ** 2 + 9, "x=0 では (x+3)^2 と x^2+9 が一致")
eq((1 + 3) ** 2, 16, "x=1 で (x+3)^2 = 16")
eq(1 ** 2 + 9, 10, "x=1 で x^2+9 = 10")
ne(16, 10, "x=1 では一致しない")
not_ident((x + 3) ** 2, x ** 2 + 9, "(x+3)^2 は x^2+9 ではない")

# ══════════════════════════════════════════════════════════
# 2. Why it works（-1 = 1 の落とし穴）
# ══════════════════════════════════════════════════════════
eq((-1) ** 2, 1 ** 2, "両辺を 2 乗すると 1 = 1")
ne(-1, 1, "しかし -1 = 1 ではない")

# ══════════════════════════════════════════════════════════
# 3. 例題 1（数の証明）
# ══════════════════════════════════════════════════════════
eq(sp.Rational(1, 4) + sp.Rational(1, 20), sp.Rational(3, 10), "例題1(a) 3/10")
eq(sp.Rational(5, 20) + sp.Rational(1, 20), sp.Rational(6, 20), "5/20 + 1/20")
eq(sp.Rational(6, 20), sp.Rational(3, 10), "6/20 = 3/10")
eq(sp.Rational(10, 40) + sp.Rational(2, 40), sp.Rational(12, 40), "分母 40 でも")
eq(sp.Rational(12, 40), sp.Rational(3, 10), "12/40 = 3/10")
eq(sp.Rational(1, 6) - sp.Rational(1, 7), sp.Rational(1, 42), "例題1(b) 1/42")
eq(sp.Rational(7, 42) - sp.Rational(6, 42), sp.Rational(1, 42), "通分の途中")
eq(6 * 7, 42, "42 = 6×7")
eq(sp.Rational(1, 6 * 7), sp.Rational(1, 42), "例題1(c) を n=6 で確かめる")
eq(sp.Rational(1, 2) - sp.Rational(1, 3), sp.Rational(1, 6), "n=2 でも")
eq(sp.Rational(1, 2 * 3), sp.Rational(1, 6), "n=2 の右辺")

# ══════════════════════════════════════════════════════════
# 4. 例題 2（部分分数の恒等式）
# ══════════════════════════════════════════════════════════
ident(1 / n - 1 / (n + 1), 1 / (n * (n + 1)), "例題2 の恒等式")
eq(sp.Rational(1, 3) - sp.Rational(1, 4), sp.Rational(1, 12), "n=3 の左辺")
eq(sp.Rational(1, 3 * 4), sp.Rational(1, 12), "n=3 の右辺")
eq(sp.Rational(4, 12) - sp.Rational(3, 12), sp.Rational(1, 12), "n=3 の通分")
eq(sp.Rational(1, 10) - sp.Rational(1, 11), sp.Rational(1, 110), "n=10 の左辺")
eq(sp.Rational(1, 10 * 11), sp.Rational(1, 110), "n=10 の右辺")
# 分子を足してしまう誤答
eq(sp.Rational(2 * 3 + 1, 3 * 4), sp.Rational(7, 12), "誤答は n=3 で 7/12")
ne(sp.Rational(7, 12), sp.Rational(1, 12), "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 5. 例題 3（展開）
# ══════════════════════════════════════════════════════════
ident((x - 4) ** 2 + 3, x ** 2 - 8 * x + 19, "例題3(a) の恒等式")
eq(sp.expand((x - 4) ** 2), x ** 2 - 8 * x + 16, "(x-4)^2 の展開")
eq(16 + 3, 19, "16 + 3 = 19")
eq((1 - 4) ** 2 + 3, 12, "x=1 の左辺")
eq(1 - 8 + 19, 12, "x=1 の右辺")
eq((5 - 4) ** 2 + 3, 4, "x=5 の左辺")
eq(25 - 40 + 19, 4, "x=5 の右辺")
eq(1 ** 2 - 13, -12, "誤答 x^2-13 は x=1 で -12")
ne(-12, 12, "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 6. 例題 4（整数）
# ══════════════════════════════════════════════════════════
ident(n + (n + 1) + (n + 2), 3 * n + 3, "例題4(a) 3n+3")
ident(3 * n + 3, 3 * (n + 1), "3n+3 = 3(n+1)")
eq(4 + 5 + 6, 15, "4+5+6 = 15")
eq(15, 3 * 5, "15 = 3×5")
eq(10 + 11 + 12, 33, "10+11+12 = 33")
eq(33, 3 * 11, "33 = 3×11")
eq(3 * (4 + 1), 15, "n=4 で 3(n+1) = 15")
eq(3 * 4, 12, "誤答 3n は n=4 で 12")
ne(12, 15, "その誤答は合わない")
eq(3 + 4, 7, "3+4 = 7（反例）")
chk(sp.Integer(7) % 2 == 1, "7 は奇数")
for _t in [-3, 0, 5, 12]:
    chk((_t + (_t + 1)) % 2 == 1, f"n={_t} でも和は奇数")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(sp.Rational(1, 2) + sp.Rational(1, 6), sp.Rational(2, 3), "演習1 2/3")
eq(sp.Rational(3, 6) + sp.Rational(1, 6), sp.Rational(4, 6), "3/6 + 1/6")
eq(sp.Rational(4, 6), sp.Rational(2, 3), "4/6 = 2/3")
eq(sp.Rational(6, 12) + sp.Rational(2, 12), sp.Rational(8, 12), "分母 12 でも")
eq(sp.Rational(8, 12), sp.Rational(2, 3), "8/12 = 2/3")

eq(sp.Rational(1, 3) - sp.Rational(1, 12), sp.Rational(1, 4), "演習2 1/4")
eq(sp.Rational(4, 12) - sp.Rational(1, 12), sp.Rational(3, 12), "4/12 - 1/12")
eq(sp.Rational(3, 12), sp.Rational(1, 4), "3/12 = 1/4")
eq(sp.Rational(1, 4) + sp.Rational(1, 12), sp.Rational(1, 3), "逆向きでも合う")

ident((x + 5) ** 2 - 10 * x, x ** 2 + 25, "演習3 の恒等式")
eq(sp.expand((x + 5) ** 2), x ** 2 + 10 * x + 25, "(x+5)^2 の展開")
eq((2 + 5) ** 2 - 20, 29, "x=2 の左辺")
eq(4 + 25, 29, "x=2 の右辺")
eq(2 ** 2 + 25 - 20, 9, "誤答は x=2 で 9")
ne(9, 29, "その誤答は合わない")

ident((2 * x - 1) ** 2 + 4 * x, 4 * x ** 2 + 1, "演習4 の恒等式")
eq(sp.expand((2 * x - 1) ** 2), 4 * x ** 2 - 4 * x + 1, "(2x-1)^2 の展開")
eq((2 * 3 - 1) ** 2 + 12, 37, "x=3 の左辺")
eq(4 * 9 + 1, 37, "x=3 の右辺")
eq(2 * 9 - 1 + 12, 29, "誤答は x=3 で 29")
ne(29, 37, "その誤答は合わない")

ident(1 / n - 1 / (n + 2), 2 / (n * (n + 2)), "演習5 の恒等式")
eq(sp.simplify((n + 2) - n), 2, "分子は 2 になる")
eq(sp.Rational(1, 4) - sp.Rational(1, 6), sp.Rational(1, 12), "n=4 の左辺")
eq(sp.Rational(2, 4 * 6), sp.Rational(1, 12), "n=4 の右辺")
eq(sp.Rational(2, 24), sp.Rational(1, 12), "2/24 = 1/12")
ne(sp.Rational(1, 24), sp.Rational(1, 12), "分子を 1 にした誤答は合わない")

ident((2 * n + 1) + (2 * n + 3), 4 * n + 4, "演習6 4n+4")
ident(4 * n + 4, 4 * (n + 1), "4n+4 = 4(n+1)")
ident((2 * n + 1) + (2 * n - 1), 4 * n, "2n±1 でも 4 の倍数")
eq(5 + 7, 12, "5+7 = 12")
eq(12, 4 * 3, "12 = 4×3")
eq(11 + 13, 24, "11+13 = 24")
eq(24, 4 * 6, "24 = 4×6")
eq(4 * (2 + 1), 12, "n=2 で 4(n+1) = 12")

ident((n + 3) ** 2 - (n + 1) ** 2, 4 * (n + 2), "演習7 の恒等式")
eq(sp.expand((n + 3) ** 2), n ** 2 + 6 * n + 9, "(n+3)^2 の展開")
eq(sp.expand((n + 1) ** 2), n ** 2 + 2 * n + 1, "(n+1)^2 の展開")
ident((n ** 2 + 6 * n + 9) - (n ** 2 + 2 * n + 1), 4 * n + 8, "差は 4n+8")
eq((1 + 3) ** 2 - (1 + 1) ** 2, 12, "n=1 の左辺")
eq(4 * 3, 12, "n=1 の右辺")
eq((5 + 3) ** 2 - (5 + 1) ** 2, 28, "n=5 の左辺")
eq(4 * 7, 28, "n=5 の右辺")
eq(4 * 1 + 10, 14, "誤答 4n+10 は n=1 で 14")
ne(14, 12, "その誤答は合わない")

ident(5 * x + 10, 5 * (x + 2), "演習8(a) は恒等式")
_s8 = sorted(sp.solve(sp.Eq(x ** 2 - 1, 0), x))
chk(_s8 == [-1, 1], f"演習8(b) の解は ±1: {_s8}")
not_ident(x ** 2 - 1, 0, "演習8(b) は恒等式ではない")
ident((x - 1) * (x + 1), x ** 2 - 1, "演習8(c) は恒等式")
eq(5 * 0 + 10, 10, "x=0 で (a) の左辺")
eq(5 * (0 + 2), 10, "x=0 で (a) の右辺")
eq(0 ** 2 - 1, -1, "x=0 で (b) の左辺")
ne(-1, 0, "x=0 で (b) は成り立たない")
eq((0 - 1) * (0 + 1), -1, "x=0 で (c) の左辺")

eq((0 + 3) ** 2, 9, "演習9 x=0 の左辺")
eq(0 ** 2 + 9, 9, "演習9 x=0 の右辺")
eq((1 + 3) ** 2, 16, "演習9 x=1 の左辺")
eq(1 ** 2 + 9, 10, "演習9 x=1 の右辺")
ne(16, 10, "x=1 で分かれる")

ident((x + 3) ** 2 - 6 * x, x ** 2 + 9, "演習10 の恒等式")
eq(sp.expand((x + 3) ** 2), x ** 2 + 6 * x + 9, "(x+3)^2 の展開")
eq((2 + 3) ** 2 - 12, 13, "x=2 の左辺")
eq(4 + 9, 13, "x=2 の右辺")

# ══════════════════════════════════════════════════════════
# 8. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の Topic 1 に、**1.6 の欄はありません。**", "公式集に欄がないと明記")
in_text("> LHS to RHS proofs require students to begin with the left-hand side"
        " expression and transform this using known algebraic steps into the"
        " expression on the right-hand side (or vice versa).",
        "LHS→RHS の Guidance を逐語で")
in_text("> Students will be expected to show how they can check a result"
        " including a check of their own results.", "検算の Guidance を逐語で")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**これは確かめであって、証明ではありません。**", "電卓は証明にならないと明記")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aasl16-", TEXT, re.M)) == 4, "例題が 4")
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
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
not_in_text("\\checkmark", "KaTeX の checkmark は使わない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl16", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-6-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-6-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("The safe layout: down one side only", "図(a) の題")
in_fig("start here", "図(a) の出発点")
in_fig("arrive here", "図(a) の行き先")
in_fig("avoid starting\\nfrom the answer", "図(a) の注意")
in_fig("Where the statement is true", "図(b) の題")
in_fig("true\\neverywhere", "図(b) の恒等式")
in_fig("true at\\none value", "図(b) の方程式")
in_text("(a) The layout expected in an examination runs down one side only",
        "キャプションが (a) を説明")
in_text("(b) An equation is true at particular values", "キャプションが (b) を説明")
# 図の数値が本文と合っているか
eq(sp.solve(sp.Eq(2 * x + 1, 7), x)[0], 3, "図(b) の x=3")
ident((x + 1) ** 2, x ** 2 + 2 * x + 1, "図(b) の恒等式")
for leak in ["29", "37", "13", "42", "110", "4(n+1)", "4(n+2)", "3(n+1)",
             "2/3", "1/12"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-6.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-5.qmd") < DRAFT.index("aasl-1-6.qmd"), "並びが 1.5 → 1.6")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aasl-1-6.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| identity |", "| deductive proof |", "| consecutive |",
          "| counterexample |", "| multiple |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ══════════════════════════════════════════════════════════
# 13. レビュー反映の見張り
# ══════════════════════════════════════════════════════════
# 例題 2 を、シラバス自身の形（和の形、m^2+m）に差しかえた
ident(1 / (m + 1) + 1 / (m ** 2 + m), 1 / m, "例題2 の恒等式（シラバスの形）")
ident(m ** 2 + m, m * (m + 1), "m^2 + m = m(m+1)")
in_text("[Show that $\\dfrac{1}{m+1} + \\dfrac{1}{m^{2}+m} \\equiv \\dfrac{1}{m}$,"
        " where $m \\neq 0$ and $m \\neq -1$.]{.q-en}", "シラバスの形を出題")
in_text("**$m^{2} + m = m(m+1)$ と因数分解するのが、最初の一歩です。**", "因数分解が要")
eq(sp.Rational(1, 4) + sp.Rational(1, 12), sp.Rational(1, 3), "(a) は m=3 の場合")
eq(sp.Rational(1, 3 + 1) + sp.Rational(1, 3 ** 2 + 3), sp.Rational(1, 3), "m=3 で確かめ")
eq(sp.Rational(1, 6) + sp.Rational(1, 30), sp.Rational(1, 5), "m=5 の検算")
eq(sp.Rational(5, 30) + sp.Rational(1, 30), sp.Rational(6, 30), "m=5 の通分")
eq(sp.Rational(1, 3) + sp.Rational(1, 6), sp.Rational(1, 2), "m=2 の検算")
in_text("**(a) は、(b) の $m = 3$ の場合です。**", "数の例が一般化のもとだと明記")
in_text("**(a) は (b) から作った場合なので、検算には使えません。**", "循環を避ける断り")
# 分数を含む恒等式の条件
in_text("## 分数を含むときは、分母が $0$ にならない値について", "≡ の意味を限定")
in_text("\\qquad (n \\neq 0, \\ n \\neq -1)", "部分分数に条件")
in_text("where $n \\neq 0$ and $n \\neq -2$", "演習 5 に条件")
# 出発点の説明を 1 か所に
in_text("出発点は $2$ つのどちらかです。", "LHS→RHS または逆向き")
not_in_text("出発点は決まっています。", "言い切りを直した")
in_text("**途中で向きを変えてはいけません。**", "向きは変えない")
# = と ≡ の表
in_text("$\\equiv$ が使える場面で $=$ を書くことはできます。**逆はできません。**", "表の下の注意")
in_text("| $=$ | equation（方程式）として |", "表の見出しを直した")
# 小数の警告
not_in_text("$0.333 + 0.167 = 0.5$", "たまたま合う例は消した")
in_text("$0.17 - 0.14 = 0.03$ です。**合っていません。**", "実際にずれる例")
chk(abs(float(sp.Rational(1, 6) - sp.Rational(1, 7)) - 0.0238095) < 1e-6, "1/42 = 0.0238…")
ne(sp.Rational("0.03"), sp.Rational(1, 42), "0.03 は 1/42 ではない")
eq(sp.Rational("0.33") * 3, sp.Rational("0.99"), "0.33 を 3 つ足すと 0.99")
ne(sp.Rational("0.99"), 1, "1 にならない")
not_in_text("**電卓で $0.5$ と出しても", "Paper 1 に電卓はない")
# 倍数の証明
in_text("**くくり出して、かっこの中が整数だと述べたところで、証明は終わりです。**", "両方要る")
in_text("$n = -1$ で $-1$、$n = 0$ で $1$ となり、**すべての奇数**を表せます。", "表現の一般性")
# 演習 9 の答えを本文から消した
not_in_text("$(x+3)^{2}$ も $x^{2} + 9$ も $9$ になります", "本文の例を差しかえた")
in_text("$(x+2)^{2}$ も $x^{2} + 4$ も $4$ になります", "差しかえ先")
eq((0 + 2) ** 2, 4, "x=0 で (x+2)^2 = 4")
eq(0 ** 2 + 4, 4, "x=0 で x^2+4 = 4")
eq((1 + 2) ** 2, 9, "x=1 で 9")
eq(1 ** 2 + 4, 5, "x=1 で 5")
ne(9, 5, "x=1 で分かれる")
not_ident((x + 2) ** 2, x ** 2 + 4, "(x+2)^2 は x^2+4 ではない")
# 検算の独立性
not_in_text("別の通分でも同じになるかを見ます", "同じ道すじの検算は消した")
eq(sp.Rational(3, 10) - sp.Rational(1, 4), sp.Rational(1, 20), "3/10 - 1/4 = 1/20")
eq(sp.Rational(6, 20) - sp.Rational(5, 20), sp.Rational(1, 20), "通分して 1/20")
eq(sp.Rational(2, 3) - sp.Rational(1, 6), sp.Rational(1, 2), "2/3 - 1/6 = 1/2")
in_text("**もともと (b) から作った式なので、これは検算になりません。**", "n=6 は使えない")
eq(sp.Rational(1, 4) - sp.Rational(1, 5), sp.Rational(1, 20), "n=4 の検算")
eq(sp.Rational(1, 4 * 5), sp.Rational(1, 20), "n=4 の右辺")
# 演習 2 の逆向きは検算であって答案ではない
in_text("## これは検算であって、答案の書き方ではありません", "両辺に足す書き方は不可")
in_text("\\text{RHS} = \\frac{1}{4} = \\frac{3}{12} = \\frac{4}{12} - \\frac{1}{12}"
        " = \\frac{1}{3} - \\frac{1}{12} = \\text{LHS}", "RHS→LHS の正しい書き方")
# 2 次式は 3 点で
in_text("**$2$ 次式どうしなら、$3$ つの値で合うところまで見てください。**", "2 点では足りない")
not_in_text("**$2$ つの値で合えば、展開ミスはまず見つかります。**", "言い過ぎを直した")
eq((2 - 4) ** 2 + 3, 7, "x=2 の左辺")
eq(4 - 16 + 19, 7, "x=2 の右辺")
_bad = 2 * x ** 2 - 14 * x + 24
eq(_bad.subs(x, 1), 12, "2 点で偶然そろう例（x=1）")
eq(_bad.subs(x, 5), 4, "同じく x=5")
ne(_bad.subs(x, 2), 7, "x=2 では分かれる")
# 命令語
in_text("[Suggest a general result, in terms of $n$, that part **(b)** illustrates.]{.q-en}",
        "Write down ではなく Suggest")
not_in_text("Write down the general result suggested", "命令語を直した")
# 演習 7 の文字
in_text("[7]{.ex-no} [Show that $(x+3)^{2} - (x+1)^{2} \\equiv 4(x+2)$.]{.q-en}",
        "演習 7 は x で書く")
ident((x + 3) ** 2 - (x + 1) ** 2, 4 * (x + 2), "演習7 の恒等式（x）")
in_text("**ここの $x$ は、整数とはかぎりません。**", "整数の断りは要らない")
eq((0 + 3) ** 2 - (0 + 1) ** 2, 8, "x=0 の左辺")
eq(4 * 2, 8, "x=0 の右辺")
# -1 = 1 の扱い
in_text("**$2$ 乗は符号のちがいを消してしまう**からです。", "可逆性を明示")
in_text("**生徒の式変形そのものは、まちがっていません。**", "生徒の計算自体は正しい")
not_in_text("works on both sides at once", "model-answer の取りちがえを直した")
in_text("Reducing it to $x^{2} + 9 = x^{2} + 9$ shows only that the claim implies"
        " something true", "何を示せたのかを正しく書く")
# グラフの重なり
in_text("**画面で重なって見えても、ちがう式のことがあります。**", "GDC の限界")
# 公式集に欄がない理由を決めつけない
not_in_text("証明のしかたに、覚える公式がないからです。", "IB の意図を決めつけない")


# ── 両辺を同時に変形する方法（★2026-09-07 の修正）────────
# 「常に無効」ではなく「同値変形かどうかを確かめる必要がある」に直した
in_text("## 両辺を同時に変形する方法には注意する", "見出しから強い禁止を外した")
not_in_text("## 両辺を同時にさわってはいけません", "古い見出しは残っていない")
not_in_text("証明としては認められません。", "「認められない」という断定は外した")
in_text("**この書き方が、それだけで誤りというわけではありません。**", "同値変形なら通る")
in_text("同値変形", "同値変形という語を使っている")
chk(TEXT.count("同値変形") >= 2,
    f"同値変形を、節と Why it works の両方で説明している: {TEXT.count('同値変形')}")
in_text("**IB の答案では、LHS だけを既知の代数の方法で変形して RHS にたどり着く書き方が、"
        "いちばん安全です。**", "試験で推奨する書き方")
# Why it works — 出発点そのものではなく、戻せない操作が問題
in_text("**なぜ、示したい式から出発する書き方に注意が要るのでしょうか。**", "問いの立て方")
not_in_text("**なぜ「示したいこと」から出発してはいけないのでしょうか。**", "古い問いは消した")
in_text("使った $2$ 乗が、**同値変形になっていない**ところです。", "何が問題かを名指し")
in_text("**両辺を同時に変形する書き方そのものが誤り、というわけではありません。**",
        "書き方そのものは誤りではない")
in_text("両辺に $3$ を足す、両辺から $x^{2}$ を引く、といった操作は逆向きにも成り立つ",
        "同値変形の例")
# Common errors も、禁止ではなく推奨に
in_text("## 示したい式から出発して、両辺をいじる", "Common error の見出し")
in_text("**この書き方が通るのは、使った変形がすべて逆向きにも成り立つときだけ**です",
        "条件つきの言い方")
in_text("**LHS か RHS のどちらか一方から出発してください。**", "推奨の言い方")
chk(TEXT.count("LHS か RHS のどちらか一方から出発してください") == 2,
    "Common errors と演習 10 の 2 か所で、同じ推奨をしている")
# 演習 10 の model-answer
not_in_text("A proof must begin from one side alone", "「must」を外した")
in_text("The layout expected in an examination begins from one side alone",
        "試験で期待される書き方、という言い方")
chk(TEXT.count("This is valid only if every step can be reversed") == 1,
    "解答例でも可逆性にふれている")
in_text("That is enough only if every step can be reversed", "model-answer でも同様")
# 採点の言い方
not_in_text("答えを書き写しただけでは点になりません", "採点の断定を弱めた")
in_text("求められていることをしたことになりません", "言いかえ")
in_text("> **採点されるのは、「なぜそうなるか」の道すじです。**", "同上")
in_text("そこまでの得点にとどまることがあります", "同上")
in_text("**$0.5$ とだけ書いても、示したことになりません。**", "同上")
in_text("必要な過程を示したことになりません", "同上")
for _ng in ["点になりません", "点にはなりません"]:
    not_in_text(_ng, "断定的な採点の言い方は残っていない: " + _ng)


not_in_text("違うのは**出発点**です", "出発点そのものを誤りとは言わない")
in_text("足りないのは、**その変形が逆向きにも成り立つという確認**です", "何が足りないのかを正しく書く")
print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
