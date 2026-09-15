"""AA SL 2.7a（2 次方程式と 2 次不等式）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_7a.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-7a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_7a.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x")
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


def solve_ineq(rel, want, msg=""):
    chk(sp.solveset(rel, x, REALS) == want, "不等式: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. The idea の例
# ══════════════════════════════════════════════════════════
eq(sp.expand((x - 4) * (x - 5)), x ** 2 - 9 * x + 20, "第 2 節の因数分解")
roots(x ** 2 - 9 * x + 20, {4, 5}, "第 2 節の例")
# (x-4)(x-5) = 2 は x-4=2 でも x-5=2 でもない
chk(sp.solveset(sp.Eq((x - 4) * (x - 5), 2), x, REALS) != {6, 7},
    "積が 2 のときは同じ議論が使えない")
# x で割ると解が落ちる
roots(5 * x ** 2 - 15 * x, {0, 3}, "第 2 節 5x^2 = 15x")
chk(sp.solveset(sp.Eq(5 * x, 15), x, REALS) == {3}, "割ると 3 だけ")
eq(5 * 0 ** 2, 15 * 0, "x=0 ももとの式を満たす")
# 平方完成
eq(sp.expand((x + 2) ** 2 - 5), x ** 2 + 4 * x - 1, "第 3 節の平方完成")
roots(x ** 2 + 4 * x - 1, {-2 + sp.sqrt(5), -2 - sp.sqrt(5)}, "第 3 節の解")
# 解の公式の例
roots(2 * x ** 2 + 3 * x - 4,
      {R(-3, 4) + sp.sqrt(41) / 4, R(-3, 4) - sp.sqrt(41) / 4}, "第 4 節の例")
eq(9 - 4 * 2 * (-4), 41, "b^2-4ac = 41")
# 不等式
roots(x ** 2 - 2 * x - 3, {3, -1}, "第 6 節の例")
solve_ineq(x ** 2 - 2 * x - 3 > 0,
           sp.Union(sp.Interval.open(-sp.oo, -1), sp.Interval.open(3, sp.oo)),
           "第 6 節 > 0")
solve_ineq(x ** 2 - 2 * x - 3 >= 0,
           sp.Union(sp.Interval(-sp.oo, -1), sp.Interval(3, sp.oo)),
           "第 6 節 >= 0")
for _v, _pos in [(-2, True), (0, False), (4, True)]:
    chk(((x ** 2 - 2 * x - 3).subs(x, _v) > 0) == _pos, f"x={_v} の符号")
eq((x ** 2 - 2 * x - 3).subs(x, -2), 5, "x=-2 で 5")
eq((x ** 2 - 2 * x - 3).subs(x, 0), -3, "x=0 で -3")
eq((x ** 2 - 2 * x - 3).subs(x, 4), 5, "x=4 で 5")

# ══════════════════════════════════════════════════════════
# 1. 例題 1
# ══════════════════════════════════════════════════════════
eq(sp.expand((x - 3) * (x - 4)), x ** 2 - 7 * x + 12, "例題1(a) 因数分解")
roots(x ** 2 - 7 * x + 12, {3, 4}, "例題1(a)")
eq((x ** 2 - 7 * x + 12).subs(x, 3), 0, "検算 f(3) = 0")
eq((x ** 2 - 7 * x + 12).subs(x, 4), 0, "検算 f(4) = 0")
roots(2 * x ** 2 - 8 * x, {0, 4}, "例題1(b)")
eq(sp.factor(2 * x ** 2 - 8 * x), 2 * x * (x - 4), "共通因数")
eq(2 * 0 ** 2, 8 * 0, "x=0 は両辺 0")
eq(2 * 4 ** 2, 8 * 4, "x=4 は両辺 32")
eq(2 * 4 ** 2, 32, "= 32")
roots(3 * x ** 2 - 12, {2, -2}, "例題1(d)")
eq(3 * (-2) ** 2 - 12, 0, "x=-2 でも 0")

# ══════════════════════════════════════════════════════════
# 2. 例題 2
# ══════════════════════════════════════════════════════════
_f2 = x ** 2 + 6 * x - 2
eq(sp.expand((x + 3) ** 2 - 11), _f2, "例題2(a)")
roots(_f2, {-3 + sp.sqrt(11), -3 - sp.sqrt(11)}, "例題2(b)")
eq(_f2.subs(x, -3), -11, "例題2(c) 頂点の y")
eq((-3 + sp.sqrt(11)) + (-3 - sp.sqrt(11)), -6, "例題2(d) 和は -6")
eq(2 * (-3), -6, "軸の 2 倍")
eq(36 + 8, 44, "b^2-4ac = 44")
eq(sp.sqrt(44), 2 * sp.sqrt(11), "√44 = 2√11")
eq(sp.simplify((-6 + 2 * sp.sqrt(11)) / 2), -3 + sp.sqrt(11), "公式でも同じ")

# ══════════════════════════════════════════════════════════
# 3. 例題 3
# ══════════════════════════════════════════════════════════
_f3 = 2 * x ** 2 + 5 * x - 1
eq(25 - 4 * 2 * (-1), 33, "例題3 b^2-4ac = 33")
ne(25 - 8, 33, "c の符号を落とすと 17")
roots(_f3, {R(-5, 4) + sp.sqrt(33) / 4, R(-5, 4) - sp.sqrt(33) / 4}, "例題3(b)")
eq((R(-5, 4) + sp.sqrt(33) / 4) - (R(-5, 4) - sp.sqrt(33) / 4),
   sp.sqrt(33) / 2, "例題3(c) 差")
eq((R(-5, 4) + sp.sqrt(33) / 4) + (R(-5, 4) - sp.sqrt(33) / 4),
   -R(5, 2), "2 解の和")
eq(-R(5, 2 * 2) * 2, -R(5, 2), "軸の 2 倍")
eq(-R(5, 4), -R(5, 4), "軸は -5/4")
# a = 0 なら 1 次方程式
_b, _c = sp.symbols("b c", nonzero=True)
chk(sp.solve(sp.Eq(_b * x + _c, 0), x) == [-_c / _b], "1 次方程式の解は 1 つ")

# ══════════════════════════════════════════════════════════
# 4. 例題 4
# ══════════════════════════════════════════════════════════
_f4 = x ** 2 - x - 6
eq(sp.expand((x - 3) * (x + 2)), _f4, "例題4(a) 因数分解")
roots(_f4, {3, -2}, "例題4(a)")
solve_ineq(_f4 > 0,
           sp.Union(sp.Interval.open(-sp.oo, -2), sp.Interval.open(3, sp.oo)),
           "例題4(b)")
solve_ineq(_f4 <= 0, sp.Interval(-2, 3), "例題4(c)")
for _v, _pos in [(-3, True), (0, False), (4, True)]:
    chk((_f4.subs(x, _v) > 0) == _pos, f"例題4 x={_v} の符号")
eq(_f4.subs(x, -3), 6, "x=-3 で 6")
eq(_f4.subs(x, 4), 6, "x=4 で 6")
eq(_f4.subs(x, 0), -6, "x=0 で -6")
# 3 < x < -2 は空集合
chk(sp.Intersection(sp.Interval.open(3, sp.oo),
                    sp.Interval.open(-sp.oo, -2)) == sp.S.EmptySet,
    "3 < x かつ x < -2 を満たす数はない")
# (b) と (c) を合わせると実数全体
chk(sp.Union(sp.Union(sp.Interval.open(-sp.oo, -2), sp.Interval.open(3, sp.oo)),
             sp.Interval(-2, 3)) == REALS, "合わせると実数全体")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(sp.expand((x + 2) * (x + 3)), x ** 2 + 5 * x + 6, "演習1")
roots(x ** 2 + 5 * x + 6, {-2, -3}, "演習1")
eq((x ** 2 + 5 * x + 6).subs(x, -2), 0, "検算")
eq((x ** 2 + 5 * x + 6).subs(x, -3), 0, "検算")

roots(x ** 2 - 9 * x, {0, 9}, "演習2")
eq(sp.factor(x ** 2 - 9 * x), x * (x - 9), "共通因数")
eq(sp.Integer(9) ** 2, 9 * 9, "x=9 は両辺 81")

roots(2 * x ** 2 - 18, {3, -3}, "演習3")
eq(sp.factor(2 * x ** 2 - 18), 2 * (x - 3) * (x + 3), "因数分解でも")
eq(2 * (-3) ** 2 - 18, 0, "x=-3 でも 0")

eq(sp.expand((x - 2) ** 2 - 3), x ** 2 - 4 * x + 1, "演習4(a)")
roots(x ** 2 - 4 * x + 1, {2 + sp.sqrt(3), 2 - sp.sqrt(3)}, "演習4(b)")
eq(16 - 4, 12, "b^2-4ac = 12")
eq(sp.sqrt(12), 2 * sp.sqrt(3), "√12 = 2√3")

eq(sp.expand((3 * x + 1) * (x + 2)), 3 * x ** 2 + 7 * x + 2, "演習5")
roots(3 * x ** 2 + 7 * x + 2, {R(-1, 3), -2}, "演習5")
eq((3 * x ** 2 + 7 * x + 2).subs(x, -2), 0, "検算 x=-2")
eq((3 * x ** 2 + 7 * x + 2).subs(x, R(-1, 3)), 0, "検算 x=-1/3")

roots(x ** 2 + 3 * x - 5,
      {R(-3, 2) + sp.sqrt(29) / 2, R(-3, 2) - sp.sqrt(29) / 2}, "演習6")
eq(9 + 20, 29, "b^2-4ac = 29")
chk(sp.isprime(29), "29 は素数なので約分できない")
eq((R(-3, 2) + sp.sqrt(29) / 2) + (R(-3, 2) - sp.sqrt(29) / 2), -3, "2 解の和")

eq(sp.expand((x - 4) * (x + 2)), x ** 2 - 2 * x - 8, "演習7 因数分解")
solve_ineq(x ** 2 - 2 * x - 8 < 0, sp.Interval.open(-2, 4), "演習7")
for _v, _neg in [(-3, False), (0, True), (5, False)]:
    chk(((x ** 2 - 2 * x - 8).subs(x, _v) < 0) == _neg, f"演習7 x={_v}")
eq((x ** 2 - 2 * x - 8).subs(x, -3), 7, "x=-3 で 7")
eq((x ** 2 - 2 * x - 8).subs(x, -2), 0, "端では 0（< 0 ではない）")

solve_ineq(x ** 2 >= 16,
           sp.Union(sp.Interval(-sp.oo, -4), sp.Interval(4, sp.oo)), "演習8")
eq(sp.factor(x ** 2 - 16), (x - 4) * (x + 4), "演習8 因数分解")
chk(sp.Integer(-5) ** 2 >= 16, "x=-5 も満たす")
chk(not (sp.Integer(0) ** 2 >= 16), "x=0 は満たさない")
eq(sp.Integer(4) ** 2, 16, "端でも成り立つ")

eq(sp.expand(2 * (x ** 2 - 4 * x + 3)), 2 * x ** 2 - 8 * x + 6, "演習9 の関係")
chk(sp.solveset(sp.Eq(x ** 2 - 4 * x + 3, 0), x, REALS)
    == sp.solveset(sp.Eq(2 * x ** 2 - 8 * x + 6, 0), x, REALS), "演習9 同じ解")
roots(x ** 2 - 4 * x + 3, {1, 3}, "演習9 の解")
eq((2 * x ** 2 - 8 * x + 6).subs(x, 1), 0, "検算 x=1")
eq((2 * x ** 2 - 8 * x + 6).subs(x, 3), 0, "検算 x=3")

roots(x ** 2 - 5 * x, {0, 5}, "演習10")
eq(sp.Integer(0) ** 2, 5 * 0, "x=0 は両辺 0")
eq(sp.Integer(5) ** 2, 5 * 5, "x=5 は両辺 25")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("x^{2}-7x+12", "例題1"), ("(x-3)(x-4)", "例題1"),
                ("2x^{2} = 8x", "例題1"), ("x^{2}+6x-2", "例題2"),
                ("(x+3)^{2} - 11", "例題2"), ("\\sqrt{33}", "例題3"),
                ("x^{2}-x-6", "例題4"), ("(x-3)(x+2)", "例題4"),
                ("x^{2} + 5x + 6", "演習1"), ("x^{2} = 9x", "演習2"),
                ("2x^{2} - 18", "演習3"), ("x^{2} - 4x + 1", "演習4"),
                ("3x^{2} + 7x + 2", "演習5"), ("x^{2} + 3x - 5", "演習6"),
                ("x^{2} - 2x - 8", "演習7"), ("2x^{2} - 8x + 6", "演習9"),
                ("x^{2} = 5x", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この式は公式集にあります", "解の公式は公式集にある")
in_text("公式集の **2.7** の欄に `Solutions of a quadratic equation` として印刷されています。",
        "欄の名前")
in_text("> $ax^{2} + bx + c = 0 \\Rightarrow x = \\dfrac{-b \\pm \\sqrt{b^{2}-4ac}}{2a}$, "
        "$a \\neq 0$", "公式集を逐語で")
in_text("> Solutions may be referred to as roots of equations or zeros of functions.",
        "Guidance を逐語で")
chk(TEXT.count("\n> ") == 2, f"引用は 2 つだけ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.index("$$ {#eq-aasl27a-formula}") < TEXT.index("## この式は公式集にあります"),
    "公式集の callout は式の直後")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("が使えるのは、右辺が $0$ のときだけです", "AB=0 の条件")
in_text("## $x$ で割らないでください", "割ると解が落ちる")
in_text("$x$ で割れるのは $x \\neq 0$ のときだけです。", "条件")
in_text("## $\\pm$ を落とさないでください", "± の注意")
in_text("**$a \\neq 0$ も、公式集に書かれています。**", "a ≠ 0")
in_text("$a < 0$ なら逆になります。", "a < 0 の場合")
in_text("**$a > 0$ なら、これがそのまま $f(x)$ の符号**です。$a < 0$ なら、すべて逆になります。",
        "Why it works でも")
in_text("$\\sqrt{4a^{2}} = \\lvert 2a \\rvert$ ですが、$\\pm$ が付いているので", "絶対値にふれた")

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
chk(TEXT.count("{.model-answer}") == 5, "model-answer が 5")
chk(len(re.findall(r"^::: \{#exm-aasl27a-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl27a", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
for _lab in ["tbl-aasl27a-choose", "tbl-aasl27a-write", "fig-aasl27a-idea",
             "eq-aasl27a-zero", "eq-aasl27a-formula"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-7a-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-7a-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Three routes to the solutions", "図(a) の題")
in_fig("make one side $0$", "図(a) の出発点")
in_fig("factorising", "図(a) 因数分解")
in_fig("completing\\nthe square", "図(a) 平方完成")
in_fig("the quadratic\\nformula", "図(a) 解の公式")
in_fig("the same solutions", "図(a) の結論")
in_fig("(b) Reading a quadratic inequality", "図(b) の題")
in_fig("$f(x) > 0$ outside the roots", "図(b) 外側")
in_fig("$f(x) < 0$ between the roots", "図(b) 内側")
in_fig("for $a > 0$: above the axis outside the roots,", "図(b) の条件")
in_text("(a) Three routes to the solutions of a quadratic equation",
        "キャプションが (a) を説明")
in_text("(b) For $a>0$ the graph is above the $x$-axis outside the roots",
        "キャプションが (b) を説明")
# 図に具体的な数値を書いていない
chk(not re.search(r"\d\s*x", FIGSTR), "図に具体的な式を書いていない")
for leak in ["= 3", "= 4", "-2", "\\sqrt{33}"]:
    chk(leak not in FIGSTR, "図が答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-7a.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-6.qmd") < DRAFT.index("aasl-2-7a.qmd"), "並びが 2.6 → 2.7a")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-7a.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| solve |", "| inequality |", "| exact value |",
           "| zero product property |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
#     ここが元に戻ると誤りが復活するので、文字列で釘を刺しておく。
# ══════════════════════════════════════════════════════════

# --- 例題3 (b) の検算：循環をやめ、解をもとの式に入れ直した -------------
_a3 = (-5 + sp.sqrt(33)) / 4
eq(2 * _a3**2 + 5 * _a3 - 1, 0, "(-5+√33)/4 は 2x^2+5x-1=0 の解")
eq(_a3**2, (29 - 5 * sp.sqrt(33)) / 8, "x^2 = (29-5√33)/8")
eq(2 * _a3**2, (29 - 5 * sp.sqrt(33)) / 4, "2x^2 = (29-5√33)/4")
eq(5 * _a3, (-25 + 5 * sp.sqrt(33)) / 4, "5x = (-25+5√33)/4")
in_text("**検算（(b) について）。** **出した解を、もとの式に入れ直します。**",
        "例題3(b) の検算は代入")
in_text(r"x^{2} = \frac{25 - 10\sqrt{33} + 33}{16} = \frac{29 - 5\sqrt{33}}{8}",
        "例題3(b) 検算の x^2")
in_text(r"2x^{2} + 5x - 1 = \frac{29 - 5\sqrt{33} - 25 + 5\sqrt{33}}{4} - 1 = \frac{4}{4} - 1 = 0",
        "例題3(b) 検算の合計")
not_in_text(r"**$2$ 解の和で確かめます。**", "例題3(b) の循環検算は消した")
not_in_text(r"$b^{2}-4ac = 25 - 4(2)(-1) = 25 + 8 = 33$",
            "例題3(b) の同じ式の再計算は消した")

# --- 例題3 (c) の検算：平方完成という別の道 -----------------------------
eq(2 * (x + R(5, 4))**2 - R(33, 8), 2 * x**2 + 5 * x - 1,
   "2x^2+5x-1 = 2(x+5/4)^2 - 33/8")
eq(R(33, 8) / 2, R(33, 16), "(x+5/4)^2 = 33/16")
eq(2 * sp.sqrt(R(33, 16)), sp.sqrt(33) / 2, "差は √33/2")
in_text(r"2x^{2}+5x-1 = 2\left(x+\frac{5}{4}\right)^{2} - \frac{25}{8} - 1 = 2\left(x+\frac{5}{4}\right)^{2} - \frac{33}{8}",
        "例題3(c) 検算の平方完成")
in_text("**公式を通らずに同じ差が出ました。**", "例題3(c) の検算は独立")
not_in_text(r"**差は、対称の軸からのずれの $2$ 倍のはず**",
            "例題3(c) の言い換え検算は消した")

# --- 例題3 (d) の解答例を短くした ---------------------------------------
in_text("so a formula that produces two solutions cannot apply. This is why "
        "the formula booklet states the condition $a \\neq 0$.",
        "例題3(d) の解答例（短縮後）")
not_in_text("A linear equation with $b \\neq 0$ has exactly one solution",
            "例題3(d) の長い一文は消した")

# --- 例題2 (c)：(x+h)^2+k の頂点は (-h, k) ------------------------------
in_text(r"$(x+h)^{2}+k$ の頂点は $(-h,\ k)$ です。ここでは $h = 3$、$k = -11$ なので、$x$ 座標は $-3$ になります。",
        "例題2(c) の h の説明")
not_in_text("$h$ の位置の数は $-3$ です。", "「h の位置の数は -3」は消した")

# --- 例題2 (d) の検算：代入してから足す ---------------------------------
_b2 = -3 + sp.sqrt(11)
eq(_b2**2 + 6 * _b2 - 2, 0, "-3+√11 は x^2+6x-2=0 の解")
eq(_b2**2, 20 - 6 * sp.sqrt(11), "(-3+√11)^2 = 20-6√11")
eq(6 * _b2, -18 + 6 * sp.sqrt(11), "6x = -18+6√11")
in_text("**検算（(d) について）。** **足す前に、$2$ 解が本当に解かを確かめます。**",
        "例題2(d) の検算は代入")
in_text("**$2$ 解が正しいと分かってから足しています。**", "例題2(d) 検算の締め")
not_in_text("**$2$ 解の和は、対称の軸の $2$ 倍のはず**",
            "例題2(d) の必ず成り立つ検算は消した")

# --- 例題4：検算を (a)(b)(c) の順にし、(c) が見ていないことを書いた ------
_ia = TEXT.index("**検算（(a) について）。** もとの式に入れ直します。$f(3)")
_ib = TEXT.index("**検算（(b) について）。** **$3$ つの区間から $1$ つずつ数を入れます。**")
_ic = TEXT.index("**検算（(c) について）。** **(b) と合わせて、")
chk(_ia < _ib < _ic, "例題4 の検算は (a) → (b) → (c) の順")
in_text("**境目の数がここで確かめられたので、あとの検算はその外側・内側だけを見ればよくなります。**",
        "例題4(a) 検算の役割")
in_text("**ただしこの見方は、境目の数そのものが正しいかは見ていません**",
        "例題4(c) 検算の限界を書いてある")

# --- 演習1：符号の見当は実数解をもつ場合の話 ----------------------------
in_text("**実数解をもつ場合**、定数項が正なら $2$ 解の符号は同じで、$x$ の係数も正なら**どちらも負**のはずです",
        "演習1 の符号の見当（条件つき）")
in_text("（実数解があるかどうかは、これでは分かりません。）", "演習1 の但し書き")
not_in_text("定数項が正で $x$ の係数も正なので、**$2$ つの解はどちらも負**のはずです",
            "演習1 の無条件の言い切りは消した")

# --- 演習2の言い回し ----------------------------------------------------
in_text("**$2$ 次方程式の実数解は多くても $2$ つです。$1$ 見つけたら"
        .replace("$1$ 見つけたら", "$1$ つ見つけたら"),
        "演習2 の言い回し")
not_in_text("**$2$ 次方程式の解は、多くても $2$ つですが、$1$ つとは限りません。**",
            "演習2 の分かりにくい一文は消した")

# --- 演習6：検算を代入にし、「約分」の使い方を直した ---------------------
_c6 = (-3 + sp.sqrt(29)) / 2
eq(_c6**2 + 3 * _c6 - 5, 0, "(-3+√29)/2 は x^2+3x-5=0 の解")
eq(_c6**2, (19 - 3 * sp.sqrt(29)) / 2, "x^2 = (19-3√29)/2")
eq(3 * _c6, (-9 + 3 * sp.sqrt(29)) / 2, "3x = (-9+3√29)/2")
chk(sp.isprime(29), "29 は素数")
in_text("**検算。** **$+$ のほうの解を、もとの式に入れ直します。** "
        r"$x = \dfrac{-3+\sqrt{29}}{2}$ のとき",
        "演習6 の検算は代入")
in_text(r"**$\sqrt{29}$ はこれ以上簡単になりません。**", "演習6 の言い方（約分ではない）")
not_in_text(r"**$\sqrt{29}$ は約分できません。**", "「√29 は約分できません」は消した")
not_in_text("**$2$ 解の和で見ます。**", "演習6 の必ず成り立つ検算は消した")

# --- 先の査読分（p27aa）の釘 --------------------------------------------
in_text("**右辺を $0$ にしてから**でないと $A = 0$ または $B = 0$ と分けられない",
        "冒頭の箇条書き（積の形は右辺 0 が先）")
chk("| zero product property |" in open(
    os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read(),
    "対訳表に zero product property")
not_in_text("$0$ には、こういう「作り方」が $1$ 通りしかありません。",
            "「作り方が 1 通り」という誤りは消した")
in_text(r"\sqrt{4a^{2}} = \lvert 2a \rvert", "√(4a^2) = |2a| と書いてある")
in_text("右辺が $0$ 以上のとき、つまり **$b^{2}-4ac \\ge 0$ のとき**",
        "平方根をとる条件")
chk(TEXT.count("**$a$ と $c$ の符号がちがうので、$-4ac$ は正**") == 2,
    "「a と c の符号がちがうので」が 2 か所")
in_text("**$a$ と $c$ の符号がちがうと $-4ac$ が正**（足し算）になります。同符号なら負です。",
        "Common errors 側の言い方")
in_text("**$a$ と $c$ が同符号なら、$-4ac$ は負**です。", "同符号のときも書いてある")
not_in_text("$c$ が負なので $-4ac$ は足し算", "「c が負なので」という言い方は消した")
in_text("$x^{2} = 49$", "Common errors の例は x^2 = 49")
not_in_body("$x^{2} = 9$", "演習3 の答えが本文に漏れていない")
in_text("以下では、**$x$ 切片が $2$ つある場合**を扱います",
        "不等式の解き方の前提")
in_text("## 離れた $2$ つの区間は、$1$ つの不等式にまとめられません",
        "callout の見出し")
# 2026-09: 生徒は全員 TI-Nspire CX II なので、CAS／非CAS の区別には触れない
in_text("Polynomial Tools", "GDC の説明")
in_text("TI-Nspire CX II に `solve(` はありません。", "solve( はない")
not_in_text("CAS")
in_text("学校の DP コーディネーターに確認して", "C11 学校に確認")
in_text("Programme Resource Centre", "C11 PRC を案内")
in_text("**ここに書いていない機種の可否は、推測しないでください。**",
        "C11 推測しない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
