"""AA SL 2.8（逆数関数と分数関数）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_8.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-8.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_8.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, y = sp.symbols("x y")
a, b, c, d = sp.symbols("a b c d")
REALS = sp.S.Reals


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.together(u) - sp.together(v)) == 0, msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def va(expr):
    """垂直漸近線（分母の零点）"""
    num, den = sp.fraction(sp.together(expr))
    return sp.solveset(sp.Eq(den, 0), x, REALS)


def ha(expr):
    """水平漸近線"""
    return sp.limit(expr, x, sp.oo)


def xint(expr):
    num, den = sp.fraction(sp.together(expr))
    return sp.solveset(sp.Eq(num, 0), x, REALS)


def yint(expr):
    return expr.subs(x, 0)


def inverse(expr):
    sol = sp.solve(sp.Eq(y, expr), x)
    chk(len(sol) == 1, "逆関数が一意に出る")
    return sp.simplify(sol[0].subs(y, x))


# ══════════════════════════════════════════════════════════
# 0. 一般論そのもの
# ══════════════════════════════════════════════════════════
GEN = (a * x + b) / (c * x + d)
# 垂直漸近線 x = -d/c
eq((c * x + d).subs(x, -d / c), 0, "分母は x = -d/c で 0")
# 水平漸近線 y = a/c
chk(sp.limit(GEN, x, sp.oo).simplify() == (a / c).simplify(),
    "x → ∞ で a/c")
# 分けた形（@eq-aasl28-split）
eq(a / c + (b * c - a * d) / (c * (c * x + d)), GEN, "分けた形が一致する")
eq(a * (c * x + d) + b * c - a * d, c * (a * x + b), "通分の分子")
# 切片
eq(GEN.subs(x, 0), b / d, "y 切片は b/d")
eq((a * x + b).subs(x, -b / a), 0, "x 切片は -b/a")
# 1/x は self-inverse
eq((1 / (1 / x)), x, "f(f(x)) = x")
eq(inverse(1 / x), 1 / x, "1/x の逆関数は 1/x")

# 走る例 (x+5)/(x-2)
RUN = (x + 5) / (x - 2)
chk(va(RUN) == sp.FiniteSet(2), "走る例の垂直漸近線 x = 2")
eq(ha(RUN), 1, "走る例の水平漸近線 y = 1")
eq(yint(RUN), R(-5, 2), "走る例の y 切片 -5/2")
chk(xint(RUN) == sp.FiniteSet(-5), "走る例の x 切片 -5")
eq(1 + 7 / (x - 2), RUN, "走る例 = 1 + 7/(x-2)")
in_text(r"f(x) = \frac{x+5}{x-2}", "走る例の式")
in_text("**垂直漸近線 $x = 2$**", "走る例の垂直漸近線")
in_text("**水平漸近線 $y = 1$**", "走る例の水平漸近線")
in_text(r"\frac{x+5}{x-2} = 1 + \frac{7}{x-2}", "走る例の分けた形")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  f(x) = 1/x
# ══════════════════════════════════════════════════════════
E1 = 1 / x
chk(va(E1) == sp.FiniteSet(0), "例題1(a) x = 0")
eq(ha(E1), 0, "例題1(a) y = 0")
eq(E1.subs(x, R(1, 100)), 100, "例題1 検算 f(0.01) = 100")
eq(E1.subs(x, R(-1, 100)), -100, "例題1 検算 f(-0.01) = -100")
eq(E1.subs(x, 100), R(1, 100), "例題1 検算 f(100) = 0.01")
eq(E1.subs(x, 4), R(1, 4), "例題1 検算 f(4) = 1/4")
eq(E1.subs(x, R(1, 4)), 4, "例題1 検算 f(1/4) = 4")
chk(sp.solveset(sp.Eq(E1, 0), x, REALS) == sp.EmptySet, "1/x = 0 に解はない")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  f(x) = (2x+1)/(x-3)
# ══════════════════════════════════════════════════════════
E2 = (2 * x + 1) / (x - 3)
chk(va(E2) == sp.FiniteSet(3), "例題2(a) x = 3")
eq(ha(E2), 2, "例題2(b) y = 2")
eq(yint(E2), R(-1, 3), "例題2(c) y 切片 -1/3")
chk(xint(E2) == sp.FiniteSet(R(-1, 2)), "例題2(c) x 切片 -1/2")
eq(E2.subs(x, R(31, 10)), 72, "例題2 検算 f(3.1) = 72")
eq(E2.subs(x, R(29, 10)), -68, "例題2 検算 f(2.9) = -68")
eq(E2.subs(x, 103), R(207, 100), "例題2 検算 f(103) = 2.07")
eq(E2.subs(x, 1003), R(2007, 1000), "例題2 検算 f(1003) = 2.007")
eq(E2.subs(x, R(-1, 2)), 0, "例題2 検算 x 切片")
chk(R(-1, 3) < 3 and R(-1, 2) < 3, "例題2 の 2 切片は同じ枝（x < 3）")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  f(x) = (3x-6)/(x+2)
# ══════════════════════════════════════════════════════════
E3 = (3 * x - 6) / (x + 2)
chk(va(E3) == sp.FiniteSet(-2), "例題3(a) domain は x ≠ -2")
eq(ha(E3), 3, "例題3(b) range は y ≠ 3")
E3INV = -(2 * x + 6) / (x - 3)
eq(inverse(E3), E3INV, "例題3(c) 逆関数")
eq(sp.simplify(E3INV.subs(x, E3)), x, "f^-1(f(x)) = x")
chk(va(E3INV) == sp.FiniteSet(3), "例題3(c) 逆関数の domain は x ≠ 3")
eq(ha(E3INV), -2, "逆関数の水平漸近線 y = -2")
eq(E3.subs(x, 4), 1, "例題3 検算 f(4) = 1")
eq(E3INV.subs(x, 1), 4, "例題3 検算 f^-1(1) = 4")
chk(sp.solveset(sp.Eq(E3, 3), x, REALS) == sp.EmptySet, "f(x) = 3 に解はない")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  f(x) = (4x-1)/(2x+5)
# ══════════════════════════════════════════════════════════
E4 = (4 * x - 1) / (2 * x + 5)
chk(va(E4) == sp.FiniteSet(R(-5, 2)), "例題4(a) x = -5/2")
eq(ha(E4), 2, "例題4(b) y = 2")
chk(xint(E4) == sp.FiniteSet(R(1, 4)), "例題4(c) x 切片 1/4")
eq(E4.subs(x, R(1, 4)), 0, "例題4 検算 f(1/4) = 0")
chk(sp.solveset(sp.Eq(E4, 2), x, REALS) == sp.EmptySet, "例題4(d) f(x) = 2 に解はない")
eq(4 * x - 1 - 2 * (2 * x + 5), -11, "例題4(d) -1 = 10 の矛盾のもと")
eq(E4.subs(x, 10), R(39, 25), "例題4 検算 f(10) = 39/25")
eq(E4.subs(x, 100), R(399, 205), "例題4 検算 f(100) = 399/205")
chk(R(399, 205) < 2, "f(100) は 2 より小さい")
eq(2 - 11 / (2 * x + 5), E4, "例題4 検算の分けた形")
# 分子が定数なら y = 0（(b) の説明）
eq(ha(1 / (2 * x + 5)), 0, "分子が定数なら水平漸近線は 0")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1
eq(E1.subs(x, R(1, 1000)), 1000, "演習1 検算 f(0.001) = 1000")
eq(E1.subs(x, 1000), R(1, 1000), "演習1 検算 f(1000) = 0.001")
# 2
X2 = (x + 4) / (x - 1)
chk(va(X2) == sp.FiniteSet(1), "演習2 x = 1")
eq(ha(X2), 1, "演習2 y = 1")
eq(X2.subs(x, 101), R(105, 100), "演習2 検算 f(101) = 1.05")
eq(X2.subs(x, R(101, 100)), 501, "演習2 検算 f(1.01) = 501")
# 3
X3 = (2 * x - 6) / (x + 1)
eq(yint(X3), -6, "演習3 y 切片 -6")
chk(xint(X3) == sp.FiniteSet(3), "演習3 x 切片 3")
eq(X3.subs(x, 3), 0, "演習3 検算")
chk(va(X3) == sp.FiniteSet(-1), "演習3 の x = -1 は domain の外")
# 4
X4 = 5 / (x - 2)
chk(va(X4) == sp.FiniteSet(2), "演習4 domain は x ≠ 2")
eq(ha(X4), 0, "演習4 range は y ≠ 0")
chk(sp.solveset(sp.Eq(X4, 0), x, REALS) == sp.EmptySet, "演習4 5/(x-2) = 0 に解はない")
# 5
X5 = (3 * x + 4) / (x - 3)
eq(inverse(X5), X5, "演習5 (3x+4)/(x-3) は self-inverse")
eq(X5.subs(x, 4), 16, "演習5 検算 g(4) = 16")
eq(X5.subs(x, 16), 4, "演習5 検算 g(16) = 4")
chk(3 + (-3) == 0, "self-inverse の条件 a + d = 0")
# 6
X6 = (2 * x + 1) / (x - 4)
X6INV = (4 * x + 1) / (x - 2)
eq(inverse(X6), X6INV, "演習6 逆関数")
chk(va(X6INV) == sp.FiniteSet(2), "演習6 逆関数の domain は x ≠ 2")
eq(ha(X6), 2, "演習6 f の水平漸近線 y = 2")
eq(X6.subs(x, 5), 11, "演習6 検算 f(5) = 11")
eq(X6INV.subs(x, 11), 5, "演習6 検算 f^-1(11) = 5")
# 7
chk(sp.limit((a * x + 1) / (x - 3), x, sp.oo) == a, "演習7 水平漸近線は a")
eq((5 * x + 1) / (x - 3), ((a * x + 1) / (x - 3)).subs(a, 5), "演習7 a = 5")
eq(((5 * x + 1) / (x - 3)).subs(x, 103), R(516, 100), "演習7 検算 f(103) = 5.16")
# 8
X8 = (3 * x + 2) / (x - 1)
chk(sp.solveset(sp.Eq(X8, 3), x, REALS) == sp.EmptySet, "演習8 f(x) = 3 に解はない")
eq(3 * x + 2 - 3 * (x - 1), 5, "演習8 2 = -3 の矛盾のもと")
eq(ha(X8), 3, "演習8 水平漸近線 y = 3")
# 9
X9 = (4 - x) / (x + 2)
chk(va(X9) == sp.FiniteSet(-2), "演習9 x = -2")
eq(ha(X9), -1, "演習9 y = -1")
eq(X9.subs(x, 98), R(-94, 100), "演習9 検算 f(98) = -0.94")
# 10
X10 = (x + 2) / (2 * x - 6)
chk(va(X10) == sp.FiniteSet(3), "演習10 domain は x ≠ 3")
eq(X10.subs(x, 6), R(4, 3), "演習10 検算 f(6) = 4/3")
chk((2 * x - 6).subs(x, 6) != 0, "x = 6 で分母は 0 でない")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [(r"\frac{2x+1}{x-3}", "例題2"), (r"\frac{3x-6}{x+2}", "例題3"),
                (r"\frac{4x-1}{2x+5}", "例題4"),
                (r"\frac{x+4}{x-1}", "演習2"), (r"\frac{2x-6}{x+1}", "演習3"),
                (r"\frac{5}{x-2}", "演習4"), (r"\frac{2x+1}{x-4}", "演習6"),
                (r"\frac{ax+1}{x-3}", "演習7"), (r"\frac{3x+2}{x-1}", "演習8"),
                (r"\frac{4-x}{x+2}", "演習9"), (r"\frac{x+2}{2x-6}", "演習10"),
                (r"\frac{3x+4}{x-3}", "演習5"), (r"\dfrac{3x+4}{x-3}", "演習5"),
                (r"\frac{5}{x-2}", "演習4"), (r"\dfrac{5}{x-2}", "演習4"),
                (r"\dfrac{2x+1}{x-3}", "例題2"), (r"\dfrac{3x-6}{x+2}", "例題3"),
                (r"\dfrac{4x-1}{2x+5}", "例題4"),
                (r"\dfrac{x+4}{x-1}", "演習2"), (r"\dfrac{2x-6}{x+1}", "演習3"),
                (r"\dfrac{2x+1}{x-4}", "演習6"),
                (r"\dfrac{ax+1}{x-3}", "演習7"), (r"\dfrac{3x+2}{x-1}", "演習8"),
                (r"\dfrac{4-x}{x+2}", "演習9"), (r"\dfrac{x+2}{2x-6}", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk("::: {.callout-important}" not in TEXT,
    "2.8 は公式集に何もないので、公式集の callout は置かない")
not_in_text("公式集の **2.8**", "公式集に 2.8 の欄はない")
# ★ 答案の書き方を縛る Guidance の一文だけを引く
in_text("> Sketches should include all horizontal and vertical asymptotes "
        "and any intercepts with the axes.", "答案の書き方の一文")
chk(TEXT.count("\n> ") == 1, f"引用は 1 つだけ: {TEXT.count(chr(10) + '> ')}")
not_in_text("The reciprocal function $f(x)=\\frac1x", "シラバス本文は引かない")
not_in_text("Rational functions of the form", "シラバス本文は引かない")
not_in_text("Link to:", "Link to の行は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## asymptote は「近づく線」であって、グラフの一部ではありません", "漸近線の注意")
in_text("## 水平漸近線は $y = 0$ とはかぎりません", "y = 0 の思いこみ")
in_text("## 分数が $0$ になるのは、分子が $0$ のときだけです", "x 切片の注意")
in_text("## range に「$\\neq$」を書き忘れないでください", "range の注意")
in_text("**$c \\neq 0$、かつ $ad \\neq bc$** とします。", "c ≠ 0 と ad ≠ bc の断り")
in_text("**これが $0$ でなければ**", "分子が 0 でないという条件")
in_text("$bc - ad \\neq 0$ ならこの分数は $0$ になれない", "bc - ad ≠ 0 の条件")

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
in_text("**垂直漸近線のところに、縦の線が引かれてしまうことがあります。**",
        "電卓が引く見かけの縦線")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
_asks = len(re.findall(r"\[(?:Explain|Comment on|Identify|Justify|A student)",
                       TEXT))
chk(TEXT.count("{.model-answer}") == 7, f"model-answer が 7: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl28-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl28", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
for _lab in ["fig-aasl28-idea", "eq-aasl28-va", "eq-aasl28-ha",
             "eq-aasl28-split"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
# callout の開閉が合っているか
chk(TEXT.count("\n::: {") + TEXT.count("\n:::\n") * 0 >= 0, "（数え上げの土台）")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-8-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-8-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) The reciprocal function", "図(a) の題")
in_fig("$y = \\\\dfrac{1}{x}$", "図(a) の式")
in_fig("asymptote $x = 0$", "図(a) の垂直漸近線")
in_fig("asymptote $y = 0$", "図(a) の水平漸近線")
in_fig("$y = x$", "図(a) の対称の線")
in_fig("its own reflection in $y = x$", "図(a) の説明")
in_fig("(b) A rational function", "図(b) の題")
in_fig("$x = -\\\\dfrac{d}{c}$", "図(b) の垂直漸近線")
in_fig("$y = \\\\dfrac{a}{c}$", "図(b) の水平漸近線")
in_fig("axis intercepts", "図(b) の切片")
in_fig("must appear on a sketch", "図(b) の注意")
in_text("(a) The reciprocal function $y=1/x$ has the two axes as its asymptotes",
        "キャプションが (a) を説明")
in_text("(b) A rational function $y=(ax+b)/(cx+d)$ has a vertical asymptote",
        "キャプションが (b) を説明")
# 図に例題・演習の答えを書いていない
for leak in ["= 3", "= 2", "= -2", "\\frac{15}{4}", "x+5", "2x+1"]:
    chk(leak not in FIGSTR, "図が答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-8.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-7b.qmd") < DRAFT.index("aasl-2-8.qmd"), "並びが 2.7b → 2.8")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-8.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| asymptote |", "| reciprocal function |", "| rational function |",
           "| self-inverse |", "| branch |", "| undefined |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════

# --- 「漸近線に触れない」は、このページの 2 つの形についての話 ----------
in_text("**このページで扱う $\\dfrac{1}{x}$ と $\\dfrac{ax+b}{cx+d}$ では、"
        "グラフが漸近線に触れることはありません。**", "触れない主張の範囲を限定")
in_text("**垂直漸近線は、どんな関数でも横切れません**", "垂直漸近線は一般に横切れない")
in_text("いっぽう**水平漸近線は、ほかの形の関数ならグラフが横切ることもあります。**",
        "水平漸近線は横切ることがある")
not_in_text("**グラフが漸近線に触れることはありません。** 触れているようにかくと",
            "無条件の言い切りは消した")

# --- ad = bc（約分できる場合）を除いてある ------------------------------
chk(sp.simplify((2 * x + 4) / (x + 2)) == 2, "(2x+4)/(x+2) は定数 2")
chk(2 * 2 - 4 * 1 == 0, "その場合 ad - bc = 0")
in_text("**$c \\neq 0$、かつ $ad \\neq bc$** とします。", "ad ≠ bc の断り")
in_text(r"たとえば $\dfrac{2x+4}{x+2} = 2$（ただし $x \neq -2$）", "約分できる例")
in_text("**domain は、分母が $0$ になる $x$（＝垂直漸近線の $x$）を除いた実数全体**です。",
        "domain は分母基準で書く")

# --- 切片がない場合 -----------------------------------------------------
chk(sp.solveset(sp.Eq(sp.Integer(3), 0), x, REALS) == sp.EmptySet,
    "分子が定数なら x 切片はない")
in_text("**切片がない場合もあります。**", "切片がない場合を書いてある")
in_text(r"たとえば $f(x) = \dfrac{3}{x+1}$ では $3 = 0$ が解けないので、"
        "$x$ 切片はありません。", "a = 0 の例（演習4 とは別の式）")
in_text("つまり $x = -\\dfrac{b}{a}$（$a \\neq 0$ のとき）", "x 切片の条件")
in_text("シラバスが **any** intercepts と書いているのは、このためです。",
        "any intercepts の理由")
in_text("- **$y$ 切片**（$y$-intercept）", "y-intercept の英語")
in_text("- **$x$ 切片**（$x$-intercept）", "x-intercept の英語")

# --- 例題1(b)・演習5 の答えが本文に先出ししていない ----------------------
not_in_body(r"f(f(x)) = \frac{1}{\left(\dfrac{1}{x}\right)} = x",
            "例題1(b) の計算が本文にない")
in_text("$f(f(x)) = x$ という式でも確かめられます（例題 1 の (b) でやってみてください）。",
        "第 2 節は例題に送る")

# --- 変換の順序 ---------------------------------------------------------
in_text("$y = \\dfrac{1}{x}$ を**縦に $7$ 倍してから**、右に $2$、上に $1$ 動かした形です",
        "変換の順序（縦の拡大が先）")
not_in_text("右に $2$、上に $1$ 動かし、$7$ 倍に伸ばした形", "逆の順序は消した")

# --- 例題2(c)・演習3 の検算を独立した道すじにした ------------------------
eq(2 + 7 / (x - 3), (2 * x + 1) / (x - 3), "例題2 の分けた形")
eq(sp.Integer(2) - R(7, 3), R(-1, 3), "分けた形から y 切片 -1/3")
eq(2 - 8 / (x + 1), (2 * x - 6) / (x + 1), "演習3 の分けた形")
eq(sp.Integer(2) - 8, -6, "分けた形から y 切片 -6")
in_text(r"**$y$ 切片は、分けた形から出し直します。** $\dfrac{2x+1}{x-3} = 2 + \dfrac{7}{x-3}$",
        "例題2(c) の検算は分けた形")
in_text(r"**$y$ 切片は、分けた形から出し直します。** $\dfrac{2x-6}{x+1} = 2 - \dfrac{8}{x+1}$",
        "演習3 の検算は分けた形")
not_in_text("**求めた点を、もとの式に入れ直します。** $f(0) = \\dfrac{0+1}{0-3}",
            "例題2(c) の同じ計算の反復は消した")

# --- 命令語（command term）の使い方 -------------------------------------
in_text("[The domain of $f^{-1}$ is the range of $f$. Justify this statement.]",
        "例題3(d) は Justify this statement")
not_in_text("Justify why the domain", "Justify why という続け方はしない")
in_text("[Explain why $f(x) = \\dfrac{3x+2}{x-1}$ never takes the value $3$.]",
        "演習8 は f(x) が主語")
not_in_text("Explain why the graph of $f(x) = \\dfrac{3x+2}{x-1}$ never takes",
            "「グラフが値をとる」という言い方は消した")

# --- 電卓の説明（存在しない設定を書かない）------------------------------
in_text("**消す設定を探さないでください。**", "設定で消せるとは書かない")
not_in_text("`menu → Graph Entry` の設定を変える", "Graph Entry の誤った案内は消した")

# --- 例題2(d) の解答例を短くした ----------------------------------------
in_text("The sketch also omits the asymptotes $x = 3$ and $y = 2$, which a "
        "sketch must show.", "例題2(d) の解答例（短縮後）")
not_in_text("the sketch is wrong because it shows one connected curve",
            "同じ判断のくり返しは消した")


# ══════════════════════════════════════════════════════════
# E02  演習9 — 有理関数を最後までかく
# ══════════════════════════════════════════════════════════
in_text("[Sketch the graph of $f(x) = \\dfrac{2x+1}{x-1}$, showing the two "
        "asymptotes as dashed lines with their equations,",
        "E02 演習9 はスケッチ")
in_text("(img/aasl-2-8-ex9.svg){#fig-aasl28-ex9 width=100%}",
        "E02 演習9 の解答図")
in_text("$$x = 1, \\qquad y = 2$$", "E02 演習9 の漸近線")
in_text("$$\\left(-\\frac{1}{2}, \\ 0\\right), \\qquad (0, \\ -1)$$",
        "E02 演習9 の切片")
not_in_text("Find the equations of the asymptotes of the graph of "
            "$f(x) = \\dfrac{4-x}{x+2}$", "E02 旧演習9 が消えている")
_e02x = sp.Symbol("x")
_e02f = (2 * _e02x + 1) / (_e02x - 1)
chk(sp.limit(_e02f, _e02x, sp.oo) == 2, "E02 水平漸近線は y = 2")
chk(sp.solveset(sp.Eq(_e02x - 1, 0), _e02x) == sp.FiniteSet(1),
    "E02 垂直漸近線は x = 1")
chk(_e02f.subs(_e02x, 0) == -1, "E02 y 切片は -1")
chk(sp.solveset(sp.Eq(2 * _e02x + 1, 0), _e02x)
    == sp.FiniteSet(sp.Rational(-1, 2)), "E02 x 切片は -1/2")
chk(_e02f.subs(_e02x, 101) > 2, "E02 右の枝は y = 2 の上")
chk(_e02f.subs(_e02x, -99) < 2, "E02 左の枝は y = 2 の下")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
