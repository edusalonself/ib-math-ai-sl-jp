"""AA SL 3.5b（正確な値と、あいまいな場合）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_5b.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-5b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_5b.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
PI = sp.pi


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(u - v) == 0, msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def sin_b(a, b, A):
    return sp.simplify(b * sp.sin(A) / a)


def count_triangles(a, b, A):
    """辺 a, b と、a の向かいの角 A から、できる三角形の数を数える。"""
    s = sp.simplify(b * sp.sin(A) / a)
    if s > 1:
        return 0
    if s == 1:
        return 1 if sp.simplify(A + PI / 2) < PI else 0
    B1 = sp.asin(s)
    B2 = PI - B1
    return sum(1 for B in (B1, B2) if sp.simplify(A + B) < PI)


# ══════════════════════════════════════════════════════════
# 0. 正確な値の表
# ══════════════════════════════════════════════════════════
TABLE = [(0, 0, 1, 0), (PI / 6, R(1, 2), sp.sqrt(3) / 2, sp.sqrt(3) / 3),
         (PI / 4, sp.sqrt(2) / 2, sp.sqrt(2) / 2, 1),
         (PI / 3, sp.sqrt(3) / 2, R(1, 2), sp.sqrt(3))]
for _a, _s, _c, _t in TABLE:
    eq(sp.sin(_a), _s, f"sin の表 ({_a})")
    eq(sp.cos(_a), _c, f"cos の表 ({_a})")
    eq(sp.tan(_a), _t, f"tan の表 ({_a})")
eq(sp.sin(PI / 2), 1, "sin(π/2) = 1")
eq(sp.cos(PI / 2), 0, "cos(π/2) = 0")
chk(sp.cos(PI / 2) == 0, "tan(π/2) はなし")
in_text("| $\\sin\\theta$ | $0$ | $\\dfrac{1}{2}$ | $\\dfrac{\\sqrt{2}}{2}$ | "
        "$\\dfrac{\\sqrt{3}}{2}$ | $1$ |", "表の sin の行")
in_text("| $\\cos\\theta$ | $1$ | $\\dfrac{\\sqrt{3}}{2}$ | $\\dfrac{\\sqrt{2}}{2}$ | "
        "$\\dfrac{1}{2}$ | $0$ |", "表の cos の行")
in_text("| $\\tan\\theta$ | $0$ | $\\dfrac{\\sqrt{3}}{3}$ | $1$ | $\\sqrt{3}$ | なし |",
        "表の tan の行")
# cos の行は sin の行の逆並び
chk([sp.sin(a_) for a_, *_ in TABLE] + [sp.sin(PI / 2)] ==
    list(reversed([sp.cos(a_) for a_, *_ in TABLE] + [sp.cos(PI / 2)])),
    "cos の行は sin の行の逆並び")
eq(sp.sqrt(3) / 3, 1 / sp.sqrt(3), "√3/3 = 1/√3")
eq(sp.sqrt(2) / 2, 1 / sp.sqrt(2), "√2/2 = 1/√2")
# 2 つの三角形
eq(sp.sqrt(1 ** 2 + 1 ** 2), sp.sqrt(2), "正方形の対角線 √2")
eq(sp.sqrt(2 ** 2 - 1 ** 2), sp.sqrt(3), "正三角形の高さ √3")
# 参照角
for _th, _q, _ref in [(PI / 6, 1, PI / 6), (2 * PI / 3, 2, PI / 3),
                      (5 * PI / 4, 3, PI / 4), (11 * PI / 6, 4, PI / 6)]:
    _r = {1: _th, 2: PI - _th, 3: _th - PI, 4: 2 * PI - _th}[_q]
    eq(_r, _ref, f"参照角 ({_th})")
    eq(abs(sp.sin(_th)), sp.sin(_ref), f"|sin| は参照角の sin ({_th})")
    eq(abs(sp.cos(_th)), sp.cos(_ref), f"|cos| は参照角の cos ({_th})")
in_text("| 参照角 | $\\theta$ | $\\pi - \\theta$ | $\\theta - \\pi$ | $2\\pi - \\theta$ |",
        "参照角の表")
# 本文の走る例
eq(sp.sin(5 * PI / 6), R(1, 2), "本文 sin(5π/6) = 1/2")
eq(sp.cos(5 * PI / 6), -sp.sqrt(3) / 2, "本文 cos(5π/6) = -√3/2")
eq(-PI / 4 + 2 * PI, 7 * PI / 4, "本文 -π/4 は 7π/4")
eq(sp.sin(-PI / 4), -sp.sqrt(2) / 2, "本文 sin(-π/4)")
eq(sp.cos(-PI / 4), sp.sqrt(2) / 2, "本文 cos(-π/4)")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  正確な値
# ══════════════════════════════════════════════════════════
eq(sp.sin(2 * PI / 3), sp.sqrt(3) / 2, "例題1(a) sin(2π/3)")
eq(sp.cos(5 * PI / 4), -sp.sqrt(2) / 2, "例題1(b) cos(5π/4)")
eq(sp.tan(11 * PI / 6), -sp.sqrt(3) / 3, "例題1(c) tan(11π/6)")
eq(sp.cos(5 * PI / 3), sp.cos(PI / 3), "例題1(d) cos(5π/3) = cos(π/3)")
eq(5 * PI / 3 - 2 * PI, -PI / 3, "例題1(d) 5π/3 - 2π = -π/3")
chk(abs(float(sp.sqrt(3) / 2) - 0.866) < 0.001, "例題1(a) 検算 約 0.87")
eq(sp.sin(5 * PI / 4) ** 2 + sp.cos(5 * PI / 4) ** 2, 1, "例題1(b) 検算 2 乗の和")
eq(sp.sin(5 * PI / 4), -sp.sqrt(2) / 2, "例題1(b) 検算 sin も -√2/2")
eq(sp.sin(11 * PI / 6) / sp.cos(11 * PI / 6), -sp.sqrt(3) / 3,
   "例題1(c) 検算 sin/cos")
eq(sp.sin(11 * PI / 6), R(-1, 2), "例題1(c) 検算 sin(11π/6)")
eq(sp.cos(11 * PI / 6), sp.sqrt(3) / 2, "例題1(c) 検算 cos(11π/6)")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  7π/6
# ══════════════════════════════════════════════════════════
chk(float(PI) < float(7 * PI / 6) < float(3 * PI / 2), "例題2(a) 第 3 象限")
eq(7 * PI / 6 - PI, PI / 6, "例題2(a) 参照角 π/6")
eq(sp.sin(7 * PI / 6), R(-1, 2), "例題2(b) sin(7π/6)")
eq(sp.cos(7 * PI / 6), -sp.sqrt(3) / 2, "例題2(b) cos(7π/6)")
eq(sp.tan(7 * PI / 6), sp.sqrt(3) / 3, "例題2(c) tan(7π/6)")
eq(sp.deg(7 * PI / 6), 210, "例題2 検算 210°")
eq(sp.sin(7 * PI / 6) ** 2 + sp.cos(7 * PI / 6) ** 2, 1, "例題2 検算 2 乗の和")
eq(sp.tan(PI / 6 + PI), sp.tan(PI / 6), "例題2 検算 tan(π/6+π)")
chk(sp.sin(7 * PI / 6) < 0 and sp.cos(7 * PI / 6) < 0 and sp.tan(7 * PI / 6) > 0,
    "例題2(d) 負を負で割ると正")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  あいまいな場合（2 つ）
# ══════════════════════════════════════════════════════════
eq(sin_b(4, 4 * sp.sqrt(2), PI / 6), sp.sqrt(2) / 2, "例題3(a) sin B = √2/2")
eq(sp.asin(sp.sqrt(2) / 2), PI / 4, "例題3(b) 鋭角の候補 π/4")
eq(PI - PI / 4, 3 * PI / 4, "例題3(b) 鈍角の候補 3π/4")
eq(PI - PI / 6 - PI / 4, 7 * PI / 12, "例題3(c) C = 7π/12")
eq(PI - PI / 6 - 3 * PI / 4, PI / 12, "例題3(c) C = π/12")
chk(count_triangles(4, 4 * sp.sqrt(2), PI / 6) == 2, "例題3 三角形は 2 つ")
chk(sp.simplify(PI / 6 + PI / 4) < PI and sp.simplify(PI / 6 + 3 * PI / 4) < PI,
    "例題3(d) どちらも和が π 未満")
eq(PI / 6 + PI / 4, 5 * PI / 12, "例題3(d) 5π/12")
eq(PI / 6 + 3 * PI / 4, 11 * PI / 12, "例題3(d) 11π/12")
eq(4 / sp.sin(PI / 6), 8, "例題3 検算 a/sinA = 8")
eq(4 * sp.sqrt(2) / (sp.sqrt(2) / 2), 8, "例題3 検算 b/sinB = 8")
eq(4 * sp.sqrt(2) * sp.sin(PI / 6), 2 * sp.sqrt(2), "例題3 検算 b sinA = 2√2")
chk(float(2 * sp.sqrt(2)) < 4 < float(4 * sp.sqrt(2)), "例題3 検算 bsinA < a < b")
eq(PI / 6 + PI / 4 + 7 * PI / 12, PI, "例題3 検算 角の和 1")
eq(PI / 6 + 3 * PI / 4 + PI / 12, PI, "例題3 検算 角の和 2")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  いくつできるか
# ══════════════════════════════════════════════════════════
eq(sin_b(4, 8, PI / 6), 1, "例題4(a) sin B = 1")
chk(count_triangles(4, 8, PI / 6) == 1, "例題4(a) 三角形は 1 つ")
eq(sp.asin(1), PI / 2, "例題4(a) B = π/2")
eq(8 * sp.sin(PI / 6), 4, "例題4(a) 検算 b sinA = a")
eq(sin_b(3, 8, PI / 6), R(4, 3), "例題4(b) sin B = 4/3")
chk(sin_b(3, 8, PI / 6) > 1, "例題4(b) 1 より大きい")
chk(count_triangles(3, 8, PI / 6) == 0, "例題4(b) 三角形は 0")
eq(sin_b(10, 8, PI / 6), R(2, 5), "例題4(c) sin B = 2/5")
chk(count_triangles(10, 8, PI / 6) == 1, "例題4(c) 三角形は 1 つ")
chk(sp.simplify(PI / 6 + (PI - sp.asin(R(2, 5)))) > PI,
    "例題4(c) 鈍角の候補では和が π を超える")
chk(sp.asin(R(2, 5)) < PI / 6, "例題4(c) 鋭角の候補は π/6 より小さい")
chk(R(2, 5) < R(1, 2), "例題4(c) 2/5 < 1/2")
# (d) 鈍角のときは多くても 1 つ
for _a, _b, _A in [(7, 5, 2 * PI / 3), (9, 4, 3 * PI / 4), (6, 5, 5 * PI / 6)]:
    chk(count_triangles(_a, _b, _A) <= 1, f"鈍角のとき 1 つ以下 ({_a},{_b})")
chk(count_triangles(5, 7, 2 * PI / 3) == 0, "鈍角で a < b なら 0")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(sp.cos(2 * PI / 3), R(-1, 2), "演習1 cos(2π/3)")
eq(PI - 2 * PI / 3, PI / 3, "演習1 参照角")
eq(sp.tan(5 * PI / 4), 1, "演習2 tan(5π/4)")
eq(sp.tan(PI / 4 + PI), sp.tan(PI / 4), "演習2 検算")
eq(sp.sin(4 * PI / 3), -sp.sqrt(3) / 2, "演習3 sin(4π/3)")
eq(sp.cos(4 * PI / 3), R(-1, 2), "演習3 検算 cos")
eq(sp.sin(4 * PI / 3) ** 2 + sp.cos(4 * PI / 3) ** 2, 1, "演習3 検算 2 乗の和")
eq(sp.cos(-PI / 6), sp.sqrt(3) / 2, "演習4 cos(-π/6)")
eq(-PI / 6 + 2 * PI, 11 * PI / 6, "演習4 検算 11π/6")
eq(sp.cos(11 * PI / 6), sp.sqrt(3) / 2, "演習4 検算 同じ値")
eq(sp.sin(13 * PI / 6), R(1, 2), "演習5 sin(13π/6)")
eq(13 * PI / 6 - 2 * PI, PI / 6, "演習5 2π を引くと π/6")
chk(float(13 * PI / 6) > float(2 * PI), "演習5 13π/6 は 2π より大きい")
eq(sin_b(5, 5 * sp.sqrt(3), PI / 6), sp.sqrt(3) / 2, "演習6 sin B = √3/2")
eq(sp.asin(sp.sqrt(3) / 2), PI / 3, "演習6 鋭角の候補 π/3")
eq(PI - PI / 3, 2 * PI / 3, "演習6 鈍角の候補 2π/3")
chk(count_triangles(5, 5 * sp.sqrt(3), PI / 6) == 2, "演習6 三角形は 2 つ")
eq(PI / 6 + PI / 3, PI / 2, "演習6 検算 和 1")
eq(PI / 6 + 2 * PI / 3, 5 * PI / 6, "演習6 検算 和 2")
eq(5 * sp.sqrt(3) * sp.sin(PI / 6), 5 * sp.sqrt(3) / 2, "演習6 検算 b sinA")
chk(float(5 * sp.sqrt(3) / 2) < 5 < float(5 * sp.sqrt(3)), "演習6 検算 2 つの条件")
eq(sin_b(4, 9, PI / 6), R(9, 8), "演習7 sin B = 9/8")
chk(sin_b(4, 9, PI / 6) > 1, "演習7 1 より大きい")
chk(count_triangles(4, 9, PI / 6) == 0, "演習7 三角形は 0")
eq(9 * sp.sin(PI / 6), R(9, 2), "演習7 検算 b sinA = 4.5")
chk(4 < R(9, 2), "演習7 検算 a < b sinA")
# 演習8：a ≥ b ならいつも 1 つ以下
for _a, _b, _A in [(7, 5, PI / 6), (6, 6, PI / 4), (10, 3, PI / 3),
                   (8, 5, PI / 6)]:
    chk(count_triangles(_a, _b, _A) <= 1, f"演習8 a ≥ b なら 1 つ以下 ({_a},{_b})")
eq(sin_b(7, 5, PI / 6), R(5, 14), "演習8 検算 sin B = 5/14")
chk(sp.simplify(PI / 6 + (PI - sp.asin(R(5, 14)))) > PI,
    "演習8 検算 鈍角の候補は和が π を超える")
eq(sin_b(7, 5, 2 * PI / 3), 5 * sp.sqrt(3) / 14, "演習9 sin B = 5√3/14")
chk(sin_b(7, 5, 2 * PI / 3) < 1, "演習9 1 より小さい")
chk(count_triangles(7, 5, 2 * PI / 3) == 1, "演習9 三角形は 1 つ")
chk(float(5 * sp.sqrt(3)) < 14, "演習9 検算 5√3 < 14")
chk(float(2 * PI / 3) > float(PI / 2), "演習9 A は鈍角")
eq(sin_b(6, 8, PI / 6), R(2, 3), "演習10 sin B = 2/3")
chk(count_triangles(6, 8, PI / 6) == 2, "演習10 三角形は 2 つ")
eq(8 * sp.sin(PI / 6), 4, "演習10 検算 b sinA = 4")
chk(4 < 6 < 8, "演習10 検算 bsinA < a < b")
chk(R(2, 3) > R(1, 2), "演習10 検算 2/3 > 1/2")
chk(sp.simplify(PI / 6 + (PI - sp.asin(R(2, 3)))) < PI,
    "演習10 鈍角の候補も三角形になる")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("\\sin\\frac{2\\pi}{3}", "例題1(a)"),
                ("\\cos\\frac{5\\pi}{4}", "例題1(b)"),
                ("\\tan\\frac{11\\pi}{6}", "例題1(c)"),
                ("\\sin\\frac{7\\pi}{6}", "例題2"),
                ("\\frac{7\\pi}{12}", "例題3(c)"),
                ("\\frac{11\\pi}{12}", "例題3(d)"),
                ("\\cos\\frac{2\\pi}{3}", "演習1"),
                ("\\tan\\frac{5\\pi}{4}", "演習2"),
                ("\\sin\\frac{4\\pi}{3}", "演習3"),
                ("\\sin\\frac{13\\pi}{6}", "演習5"),
                ("\\frac{5\\sqrt{3}}{14}", "演習9"),
                ("\\frac{9}{8}", "演習7"), ("\\frac{4}{3}", "例題4(b)")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **3.2** の欄に `Sine rule` として印刷されています。", "正弦定理の欄")
in_text("> $\\dfrac{a}{\\sin A} = \\dfrac{b}{\\sin B} = \\dfrac{c}{\\sin C}$",
        "正弦定理を逐語で")
chk(TEXT.count("\n> ") == 1, f"引用は公式集の 1 つだけ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 1, "公式集の callout は 1 つ")
not_in_text("Exact values of trigonometric ratios of", "シラバス本文は引かない")
not_in_text("Extension of the sine rule to the ambiguous case", "シラバス本文は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("**この表は公式集にはありません。** Paper 1 は電卓なしなので、覚える必要があります。",
        "表は公式集にない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("**大きさは表から、符号は象限から**、と覚えてください。", "大きさと符号")
in_text("$\\hat{A}$ が鋭角のときは、$\\sin B = \\dfrac{b\\sin A}{a}$ の値と、"
        "$a$ と $b$ の大小で決まります。", "表の前提は A が鋭角と、a と b の大小")
in_text("**$\\hat{A}$ が直角か鈍角のときは、$a > b$ なら $1$ つ、そうでなければ $0$ です。**",
        "A が鈍角のとき")
in_text("（$B = \\dfrac{\\pi}{2}$ のときだけ、この $2$ つが重なって $1$ つです）",
        "B = π/2 は例外")
in_text("**$2$ 辺とそのはさむ角なら、こうはなりません。**", "はさむ角ならあいまいでない")
in_text("## 符号を付け忘れる", "符号の注意")
in_text("## $\\pi - B$ を、確かめずに採用する", "確かめる注意")

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
in_text("**もう $1$ つの候補 $\\pi - B$ は、自分で書き足す必要があります。**",
        "電卓は 1 つしか返さない")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 8,
    f"model-answer が 8: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl35b-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk(TEXT.count("::: {.callout-warning}") == 7, "Common errors 6 + 本文の注意 1 で 7")
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
    _b = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _b), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl35b", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _tgt in ["aasl-3-2", "aasl-3-4", "aasl-3-5a"]:
    _TT = open(os.path.join(BASE, _tgt + ".qmd"), encoding="utf-8").read()
    for _a2 in set(re.findall(r"\]\(" + _tgt + r"\.qmd#([a-z0-9-]+)\)", TEXT)):
        chk(("{#" + _a2 + "}") in _TT, _tgt + " 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl35b-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl35b-exact", "tbl-aasl35b-ref", "tbl-aasl35b-count",
             "eq-aasl35b-sine", "eq-aasl35b-sinb"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-3-5b-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-5b-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) The two special triangles", "図(a) の題")
in_fig("half a square, and half an equilateral triangle", "図(a) の説明")
in_fig("every exact value comes from reading a ratio off one ", "図(a) の説明（続き）")
in_fig("(b) The ambiguous case", "図(b) の題")
in_fig("two sides and an angle that is not between them", "図(b) の説明")
in_fig("the circle of radius $a$ centred at $C$ can meet the ", "図(b) の説明（続き）")
in_fig("$b\\\\sin A$", "図(b) の高さ")
chk("$c\\\\sin A$" not in FIG, "図の高さは b sin A（c ではない）")
in_fig("$B_{1}$", "図(b) の交点 B1")
in_fig("$B_{2}$", "図(b) の交点 B2")
chk("$C_{1}$" not in FIG and "$C_{2}$" not in FIG, "交点の名前は B1, B2")
in_text("(a) The exact values come from two triangles: half a square",
        "キャプションが (a) を説明")
in_text("(b) In the ambiguous case two sides and a non-included angle are known: "
        "with $\\mathrm{AC} = b$ laid off along one arm, the circle of radius $a$ "
        "centred at $C$", "キャプションが (b) を説明")
chk(set(re.findall(r"\d+", FIGSTR)) <= {"1", "2", "3", "4", "6"},
    f"図の数字は辺の長さと π の分母だけ: {set(re.findall(chr(92) + 'd+', FIGSTR))}")
for _fr in ["6", "4", "3"]:
    chk(("frac{" + chr(92) * 2 + "pi}{" + _fr + "}") in FIGSTR,
        "図に角 π/" + _fr + " がある")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-5b.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-5a.qmd") < DRAFT.index("aasl-3-5b.qmd"),
    "並びが 3.5a → 3.5b")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-5b.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| reference angle |", "| ambiguous case |", "| exact value |",
           "| equilateral |", "| isosceles |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 図と本文の設定をそろえた（円の中心は C、高さは b sin A）--------------
in_text("$\\hat{A}$ の一方の辺に $\\mathrm{AC} = b$ を取り、$C$ を中心とする半径 $a$ の"
        "円が、$A$ から出るもう一方の半直線と $2$ 回交わっています。", "図の設定")
in_text("交点が $B_{1}$ と $B_{2}$ の $2$ とおりあるので", "交点は B1, B2")
in_text("$C$ から半直線 $\\mathrm{AB}$ までの距離は **$b\\sin A$** です。", "高さは b sinA")
not_in_text("$B$ を中心とする半径 $a$ の円", "中心が B という言い方は消した")
not_in_text("$c$ が分かっていないことが多いので", "c を持ち出す言い方は消した")
not_in_text("交点が $C_{1}$ と $C_{2}$", "交点の名前を直した")
# 幾何の確かめ：AC = b、CB = a、C から AB までの距離 = b sin A
_A5 = sp.rad(30)
_b5, _a5 = 5, 3
_Cy = _b5 * sp.sin(_A5)
eq(_Cy, _b5 * sp.sin(_A5), "C の高さは b sin A")
eq(_Cy, R(5, 2), "この図では b sin A = 2.5")
chk(_a5 > float(_Cy), "a > b sin A なので 2 回交わる")
_dx5 = sp.sqrt(_a5 ** 2 - _Cy ** 2)
chk(float(_dx5) > 0, "交点は 2 つ")

# --- a ≥ b の理由から、誤った不等式を落とした ----------------------------
in_text("$\\hat{B} \\le \\hat{A}$ となって $\\hat{B}$ が鈍角になれないので、鈍角のほうの"
        "候補が消えるからです。", "a ≥ b の理由")
not_in_text("$\\hat{B} \\le \\hat{A} < \\dfrac{\\pi}{2}$", "A が鋭角と決めつける式は消した")
# 反例：a ≥ b でも A は鈍角でありうる（演習9）
chk(7 >= 5 and float(2 * PI / 3) > float(PI / 2), "a ≥ b でも A が鈍角の例がある")
in_text("逆に $a > b$ のときは $\\sin B = \\dfrac{b\\sin A}{a} < \\sin A$ となり、鋭角の"
        "候補は $\\pi - \\hat{A}$ より小さいので、$\\hat{A} + \\hat{B} < \\pi$ となって"
        "三角形がちょうど $1$ つできます。", "鈍角のとき 1 つになる理由")
for _a, _b, _A in [(7, 5, 2 * PI / 3), (9, 4, 3 * PI / 4), (6, 5, PI / 2)]:
    chk(count_triangles(_a, _b, _A) == 1, f"鈍角・直角で a > b なら 1 つ ({_a},{_b})")
for _a, _b, _A in [(5, 5, 2 * PI / 3), (4, 6, 3 * PI / 4), (5, 5, PI / 2)]:
    chk(count_triangles(_a, _b, _A) == 0, f"鈍角・直角で a ≤ b なら 0 ({_a},{_b})")

# --- sin B = 1 の例外を第 5 節にも書いた --------------------------------
in_text("（$\\sin B = 1$ のときだけ、$\\dfrac{\\pi}{2}$ の $1$ つです）", "5 節の例外")
in_text("（$\\sin B = 1$ のときだけ $\\dfrac{\\pi}{2}$）", "GDC の例外")
in_text("電卓も、$1$ つ（ふつうは鋭角のほう）しか返しません。", "Common errors の言い方")

# --- 軸の上の値と、軸の上の角の扱い -------------------------------------
in_text("$0$ と $\\dfrac{\\pi}{2}$ の値は、単位円の**軸の上の点**から直接読みます",
        "軸の上の値の出どころ")
in_text("$\\theta$ が $0$、$\\dfrac{\\pi}{2}$、$\\pi$、$\\dfrac{3\\pi}{2}$ のように**軸の上**に"
        "あるときは、象限がないので参照角は使いません。", "軸の上では参照角を使わない")
eq(sp.cos(PI), -1, "cos π = -1")
eq(sp.sin(3 * PI / 2), -1, "sin(3π/2) = -1")
eq(sp.tan(PI), 0, "tan π = 0")

# --- 三角形の比と単位円の座標をつないだ ----------------------------------
in_text("斜辺が $1$ になるように縮めると、この三角形は単位円の中に入ります。", "縮める")
in_text("**辺の比がそのまま $\\sin$・$\\cos$ の値**になります。", "比が値になる")

# --- 2 乗の和の検算に、単位円の式と符号の但し書きを付けた ----------------
chk(TEXT.count("点は単位円 $x^{2}+y^{2}=1$ の上にあるはずです") == 3,
    f"3 か所に単位円の式: {TEXT.count('点は単位円 $x^{2}+y^{2}=1$ の上にあるはずです')}")
in_text("**ただし、この確かめでは符号までは分かりません。**", "符号は確かめられない")
in_text("**符号までは確かめられないので、象限も見てください。**", "象限も見る")

# --- 「ちょうど 1 つ」に角の和の確認を足した -----------------------------
in_text("also $\\hat{\\mathrm{A}} + \\hat{\\mathrm{B}} = \\dfrac{2\\pi}{3} < \\pi$",
        "例題4(a) の和")
in_text("The acute candidate does give a triangle, since $\\hat{\\mathrm{A}} + "
        "\\hat{\\mathrm{B}} < \\dfrac{\\pi}{3} < \\pi$.", "例題4(c) の和")
in_text("The acute candidate does give a triangle: $\\dfrac{5\\sqrt{3}}{14} < "
        "\\dfrac{7\\sqrt{3}}{14} = \\sin\\dfrac{\\pi}{3}$", "演習9 の和")
eq(PI / 6 + PI / 2, 2 * PI / 3, "例題4(a) 和は 2π/3")
eq(7 * sp.sqrt(3) / 14, sp.sin(PI / 3), "7√3/14 = sin(π/3)")
chk(5 * sp.sqrt(3) / 14 < sp.sin(PI / 3), "演習9 sinB < sin(π/3)")
chk(sp.asin(5 * sp.sqrt(3) / 14) < PI / 3, "演習9 B < π/3")
eq(PI - 2 * PI / 3, PI / 3, "π - A = π/3")

# --- 検算を余弦定理にした -----------------------------------------------
_c = sp.Symbol("c_", positive=True)


def cos_c(a_, b_, A_):
    """余弦定理 a² = b² + c² - 2bc cos A の、正の c の個数を返す。"""
    return sp.solve(sp.Eq(a_ ** 2, b_ ** 2 + _c ** 2 - 2 * b_ * _c * sp.cos(A_)), _c)


chk(cos_c(4, 8, PI / 6) == [4 * sp.sqrt(3)], f"例題4(a) c は 1 つ: {cos_c(4, 8, PI / 6)}")
chk(cos_c(3, 8, PI / 6) == [], f"例題4(b) 実数の c がない: {cos_c(3, 8, PI / 6)}")
chk(sorted(cos_c(5, 5 * sp.sqrt(3), PI / 6)) == [5, 10],
    f"演習6 c は 5 と 10: {cos_c(5, 5 * sp.sqrt(3), PI / 6)}")
chk(cos_c(4, 9, PI / 6) == [], f"演習7 実数の c がない: {cos_c(4, 9, PI / 6)}")
chk(cos_c(7, 5, 2 * PI / 3) == [3], f"演習9 c は 3 だけ: {cos_c(7, 5, 2 * PI / 3)}")
eq((8 * sp.sqrt(3)) ** 2 - 4 * 48, 0, "例題4(a) 判別式 0")
eq((8 * sp.sqrt(3)) ** 2 - 4 * 55, -28, "例題4(b) 判別式 -28")
eq((9 * sp.sqrt(3)) ** 2 - 4 * 65, -17, "演習7 判別式 -17")
eq(sp.expand((_c - 5) * (_c - 10)), _c ** 2 - 15 * _c + 50, "演習6 の因数分解")
eq(sp.expand((_c - 3) * (_c + 8)), _c ** 2 + 5 * _c - 24, "演習9 の因数分解")
in_text("**正弦定理を通らない道すじでも同じです。**", "例題4(a) の検算")
in_text("**正弦定理を通らない道すじでも $2$ つです。**", "演習6 の検算")
in_text("**正弦定理を通らない道すじでも $1$ つです。**", "演習9 の検算")

# --- 演習1 に基本の値を足した -------------------------------------------
in_text("[Write down the exact value of $\\cos\\dfrac{\\pi}{3}$, and hence find the exact "
        "value of $\\cos\\dfrac{2\\pi}{3}$.]{.q-en}", "演習1 は基本の値から")
eq(sp.cos(PI / 3), R(1, 2), "cos(π/3) = 1/2")

# --- 演習5 の検算の範囲をしぼった ----------------------------------------
in_text("**範囲をしぼって見ます。**", "演習5 の検算")
chk(sp.sin(PI / 6) < sp.sin(PI / 4), "sin(π/6) < sin(π/4)")
chk(abs(float(sp.sqrt(2) / 2) - 0.707) < 0.001, "√2/2 ≈ 0.71")
not_in_text("$\\sin$ は小さな正の値になるはずで", "ゆるい言い方は消した")

# --- 演習8 を、本文にない場合にした --------------------------------------
in_text("[8]{.ex-no} [In triangle $\\mathrm{ABC}$, $a = b = 5$ and $\\hat{\\mathrm{A}} = "
        "\\dfrac{\\pi}{4}$", "演習8 は a = b = 5")
in_text("leaving $\\hat{\\mathrm{C}} = 0$, which is not a triangle.", "第 3 の角が 0")
not_in_text("Explain why the ambiguous case cannot arise when $a \\ge b$.",
            "本文に答えのある演習8 は消した")
eq(sin_b(5, 5, PI / 4), sp.sqrt(2) / 2, "演習8 sin B = √2/2")
eq(PI / 4 + 3 * PI / 4, PI, "演習8 和はちょうど π")
chk(count_triangles(5, 5, PI / 4) == 1, "演習8 三角形は 1 つだけ")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
