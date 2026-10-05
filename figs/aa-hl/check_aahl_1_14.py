"""AA HL 1.14（共役な解・De Moivre の定理・n 乗根）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_14.py
"""
import glob
import os
import re
import sys

import sympy as sp
from sympy import I, pi
from sympy import Rational as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-14.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_14.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
z = sp.Symbol("z")
th = sp.Symbol("theta", real=True)
c, s_ = sp.cos(th), sp.sin(th)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + "  (%s vs %s)" % (u, v))


def ne(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) != 0, msg + "  (%s vs %s)" % (u, v))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def cart(r, t):
    return sp.simplify(sp.expand(r * (sp.cos(t) + I * sp.sin(t))))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの恒等式
# ══════════════════════════════════════════════════════════
# De Moivre（正の整数）
_TVALS = [R(1, 7), R(2, 5), R(11, 9), -R(3, 8), R(17, 6)]
for _n in range(1, 9):
    _d = sp.expand((sp.cos(th) + I * sp.sin(th)) ** _n
                   - (sp.cos(_n * th) + I * sp.sin(_n * th)))
    for _tv in _TVALS:
        chk(abs(complex(_d.subs(th, _tv).evalf())) < 1e-12,
            "De Moivre: n=%d, θ=%s" % (_n, _tv))
# 負の整数でも
for _n in range(1, 5):
    _d = ((sp.cos(th) + I * sp.sin(th)) ** (-_n)
          - (sp.cos(-_n * th) + I * sp.sin(-_n * th)))
    for _tv in _TVALS:
        chk(abs(complex(_d.subs(th, _tv).evalf())) < 1e-12,
            "De Moivre（負）: n=-%d, θ=%s" % (_n, _tv))
# 実数係数の多項式は、共役な解をもつ
_a0, _a1, _a2, _a3 = sp.symbols("a0 a1 a2 a3", real=True)
_P = _a3 * z ** 3 + _a2 * z ** 2 + _a1 * z + _a0
_w = sp.Symbol("w")
chk(sp.simplify(sp.conjugate(_P.subs(z, _w)) - _P.subs(z, sp.conjugate(_w))) == 0,
    "実数係数なら P(w)* = P(w*)")
# 係数が実数でないと崩れる（z^2 - i z）
_bad = sp.solve(z ** 2 - I * z, z)
chk(set(_bad) == {0, I}, "z^2 - iz = 0 の解は 0 と i")
chk(sp.conjugate(I) not in _bad, "共役な組になっていない")
# 共役な組の積は実数係数の 2 次式
_p, _q = sp.symbols("p q", real=True)
_prod = sp.expand((z - (_p + _q * I)) * (z - (_p - _q * I)))
chk(sp.im(sp.expand(_prod).coeff(z, 1)) == 0
    and sp.im(sp.expand(_prod).coeff(z, 0)) == 0, "共役な組の積は実数係数")
eq(_prod, z ** 2 - 2 * _p * z + (_p ** 2 + _q ** 2), "その 2 次式の形")

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
chk(set(sp.solve(z ** 2 - 6 * z + 25, z)) == {3 + 4 * I, 3 - 4 * I}, "§1 3±4i")
eq(36 - 100, -64, "§1 判別式")
eq(sp.sqrt(-64), 8 * I, "§1 √(-64) = 8i")
eq(sp.expand((z - (3 + 4 * I)) * (z - (3 - 4 * I))), z ** 2 - 6 * z + 25, "§2 2 次因数")
eq(sp.expand((z - 3) ** 2 - (4 * I) ** 2), z ** 2 - 6 * z + 25, "§2 (z-3)^2 - (4i)^2")
eq(sp.expand((z - 2) * (z ** 2 - 6 * z + 25)),
   z ** 3 - 8 * z ** 2 + 37 * z - 50, "§2 3 次式")
eq(sp.expand((1 + I) ** 8), 16, "§4 (1+i)^8 = 16")
eq(sp.Abs(1 + I), sp.sqrt(2), "§4 |1+i| = √2")
eq(sp.arg(1 + I), pi / 4, "§4 arg(1+i) = π/4")
eq(sp.exp(2 * pi * I), 1, "§4 e^{2πi} = 1")
eq((sp.sqrt(2)) ** 8, 16, "(√2)^8 = 16")
chk(set(sp.solve(z ** 3 - 8, z))
    == {2, -1 + sp.sqrt(3) * I, -1 - sp.sqrt(3) * I}, "§6 z^3 = 8 の 3 解")
eq(cart(2, 2 * pi / 3), -1 + sp.sqrt(3) * I, "§6 2e^{i2π/3}")
eq(cart(2, -2 * pi / 3), -1 - sp.sqrt(3) * I, "§6 2e^{-i2π/3}")
eq(4 * pi / 3 - 2 * pi, -2 * pi / 3, "§6 主値に直す")
for _n in range(2, 8):
    chk(len(sp.solve(z ** _n - 8, z)) == _n, "§6 z^n = 8 の解は n 個: n=%d" % _n)

# ══════════════════════════════════════════════════════════
# 2. 例題 1〜4
# ══════════════════════════════════════════════════════════
chk(set(sp.solve(z ** 3 - 7 * z ** 2 + 17 * z - 15, z)) == {3, 2 + I, 2 - I},
    "例題1 の 3 解")
eq(sp.expand((z - (2 + I)) * (z - (2 - I))), z ** 2 - 4 * z + 5, "例題1 の 2 次因数")
eq(sp.expand((z - 3) * (z ** 2 - 4 * z + 5)),
   z ** 3 - 7 * z ** 2 + 17 * z - 15, "例題1 検算：展開")
eq(-5 * 3, -15, "例題1 定数項")
eq((2 + I) + (2 - I) + 3, 7, "例題1 検算：解の和は 7")

eq(sp.Abs(-1 + I), sp.sqrt(2), "例題2 r")
eq(sp.arg(-1 + I), 3 * pi / 4, "例題2 θ")
eq(sp.expand((-1 + I) ** 6), 8 * I, "例題2(b)")
eq(sp.expand((-1 + I) ** 2), -2 * I, "例題2 検算：(-1+i)^2 = -2i")
eq(sp.expand((-2 * I) ** 3), 8 * I, "例題2 検算：(-2i)^3 = 8i")
eq((sp.sqrt(2)) ** 6, 8, "(√2)^6 = 8")
eq(9 * pi / 2 - 4 * pi, pi / 2, "例題2 主値に直す")
eq(sp.expand((-1 + I) ** 12), -64, "例題2(c)")
eq(sp.expand((8 * I) ** 2), -64, "例題2(c) 検算")

_r3 = sp.solve(z ** 3 - 27 * I, z)
chk(len(_r3) == 3, "例題3 は 3 解")
for _v in [cart(3, pi / 6), cart(3, 5 * pi / 6), cart(3, -pi / 2)]:
    chk(any(sp.simplify(_v - _u) == 0 for _u in _r3), "例題3 の解: %s" % _v)
eq(cart(3, -pi / 2), -3 * I, "例題3 3e^{-iπ/2} = -3i")
eq(sp.expand((-3 * I) ** 3), 27 * I, "例題3 検算：(-3i)^3 = 27i")
eq(pi / 6 + 2 * pi / 3, 5 * pi / 6, "例題3 k=1")
eq(pi / 6 + 4 * pi / 3, 3 * pi / 2, "例題3 k=2")
eq(3 * pi / 2 - 2 * pi, -pi / 2, "例題3 主値に直す")
eq(sp.Rational(27) ** R(1, 3), 3, "27^(1/3) = 3")
eq(5 * pi / 6 + 2 * pi / 3 - 2 * pi, -pi / 2, "例題3 等間隔")

eq(sp.expand(sp.re(sp.expand((c + I * s_) ** 3))), sp.expand(c ** 3 - 3 * c * s_ ** 2),
   "例題4(a) 実部")
eq(sp.simplify(sp.expand(c ** 3 - 3 * c * (1 - c ** 2)) - (4 * c ** 3 - 3 * c)), 0,
   "例題4(a) cos3θ = 4c^3-3c")
eq(sp.simplify(sp.cos(3 * th) - (4 * c ** 3 - 3 * c)), 0, "例題4(a) sympy でも一致")
eq(sp.expand(sp.im(sp.expand((c + I * s_) ** 3))), sp.expand(3 * c ** 2 * s_ - s_ ** 3),
   "例題4(b) 虚部")
eq(sp.simplify(sp.sin(3 * th) - (3 * s_ - 4 * s_ ** 3)), 0, "例題4(b) sin3θ")
eq(sp.cos(pi), -1, "例題4 検算：cos π = -1")
eq(4 * R(1, 8) - 3 * R(1, 2), -1, "例題4 検算：右辺も -1")
eq(sp.sin(pi / 2), 1, "例題4 検算：sin π/2 = 1")
eq(3 * R(1, 2) - 4 * R(1, 8), 1, "例題4 検算：右辺も 1")
chk(sp.sin(0) == 0, "θ=0 では s が消える")

# ══════════════════════════════════════════════════════════
# 3. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(sp.expand((z - (1 + 3 * I)) * (z - (1 - 3 * I))), z ** 2 - 2 * z + 10, "演習1")
eq(sp.expand((z - 1) ** 2 + 9), z ** 2 - 2 * z + 10, "演習1 (z-1)^2+9")
eq((1 + 3 * I) + (1 - 3 * I), 2, "演習1 解の和")
eq(sp.expand((1 + 3 * I) * (1 - 3 * I)), 10, "演習1 解の積")
eq(sp.expand((1 + 3 * I) ** 2), -8 + 6 * I, "演習1 (1+3i)^2")
eq(sp.expand((1 + 3 * I) ** 2 - 2 * (1 + 3 * I) + 10), 0, "演習1 検算：代入")

chk(set(sp.solve(z ** 3 - 5 * z ** 2 + 17 * z - 13, z)) == {1, 2 + 3 * I, 2 - 3 * I},
    "演習2 の 3 解")
eq(sp.expand((z - (2 + 3 * I)) * (z - (2 - 3 * I))), z ** 2 - 4 * z + 13, "演習2 の 2 次因数")
eq(sp.expand((z - 1) * (z ** 2 - 4 * z + 13)),
   z ** 3 - 5 * z ** 2 + 17 * z - 13, "演習2 検算：展開")
eq((2 + 3 * I) + (2 - 3 * I) + 1, 5, "演習2 検算：解の和")

eq(sp.expand((sp.sqrt(3) + I) ** 6), -64, "演習3")
eq(sp.Abs(sp.sqrt(3) + I), 2, "演習3 r = 2")
eq(sp.arg(sp.sqrt(3) + I), pi / 6, "演習3 θ = π/6")
eq(sp.expand((sp.sqrt(3) + I) ** 2), 2 + 2 * sp.sqrt(3) * I, "演習3 検算：2 乗")
eq(sp.expand((2 + 2 * sp.sqrt(3) * I) ** 2), -8 + 8 * sp.sqrt(3) * I, "演習3 検算：4 乗")
eq(sp.expand((2 + 2 * sp.sqrt(3) * I) * (-8 + 8 * sp.sqrt(3) * I)), -64, "演習3 検算：6 乗")
eq(2 ** 6, 64, "2^6 = 64")

eq(sp.expand((1 - I) ** 10), -32 * I, "演習4")
eq(sp.expand((1 - I) ** 2), -2 * I, "演習4 (1-i)^2 = -2i")
eq(sp.expand((-2 * I) ** 5), -32 * I, "演習4 検算：(-2i)^5")
eq((sp.sqrt(2)) ** 10, 32, "(√2)^10 = 32")
eq(sp.expand(I ** 5), I, "i^5 = i")
eq(-5 * pi / 2 + 2 * pi, -pi / 2, "演習4 主値に直す")

chk(set(sp.solve(z ** 3 + 8, z))
    == {-2, 1 + sp.sqrt(3) * I, 1 - sp.sqrt(3) * I}, "演習5 の 3 解")
eq(cart(2, pi / 3), 1 + sp.sqrt(3) * I, "演習5 2e^{iπ/3}")
eq(cart(2, -pi / 3), 1 - sp.sqrt(3) * I, "演習5 2e^{-iπ/3}")
eq(cart(2, pi), -2, "演習5 2e^{iπ} = -2")
eq(sp.expand((-2) ** 3), -8, "演習5 検算：実数解")
eq(sp.expand((1 + sp.sqrt(3) * I) ** 2), -2 + 2 * sp.sqrt(3) * I, "演習5 2 乗")
eq(sp.expand((1 + sp.sqrt(3) * I) ** 3), -8, "演習5 検算：3 乗")
eq(pi / 3 + 4 * pi / 3 - 2 * pi, -pi / 3, "演習5 k=2 を主値に")

chk(set(sp.solve(z ** 4 - 16, z)) == {2, -2, 2 * I, -2 * I}, "演習6 の 4 解")
eq(sp.expand((2 * I) ** 4), 16, "演習6 検算：(2i)^4")
eq(sp.expand((-2 * I) ** 4), 16, "演習6 検算：(-2i)^4")
eq(sp.expand((z ** 2 - 4) * (z ** 2 + 4)), z ** 4 - 16, "演習6 因数分解")
chk(len(sp.solve(z ** 2 - 4, z)) == 2, "z^2=4 では 2 つしか出ない")

eq(sp.expand(sp.re(sp.expand((c + I * s_) ** 4))),
   sp.expand(c ** 4 - 6 * c ** 2 * s_ ** 2 + s_ ** 4), "演習7 実部")
eq(sp.simplify(sp.cos(4 * th) - (8 * c ** 4 - 8 * c ** 2 + 1)), 0, "演習7")
eq(8 - 8 + 1, 1, "演習7 θ=0 の検算")
eq(sp.cos(4 * pi / 3), R(-1, 2), "演習7 cos 4π/3")
eq(8 * R(1, 16) - 8 * R(1, 4) + 1, R(-1, 2), "演習7 右辺も -1/2")

for _n in (3, 4, 5, 6):
    _sols = sp.solve(z ** _n - (2 + 3 * I), z)
    chk(len(_sols) == _n, "演習8 解は n 個: n=%d" % _n)
    _mods = [sp.simplify(sp.Abs(_v)) for _v in _sols]
    chk(all(sp.simplify(_m - _mods[0]) == 0 for _m in _mods),
        "演習8 絶対値がすべて同じ: n=%d" % _n)
_args = sorted(float(sp.arg(_v)) for _v in sp.solve(z ** 3 - 8, z))
_gaps = [_args[1] - _args[0], _args[2] - _args[1]]
chk(all(abs(_g - float(2 * pi / 3)) < 1e-9 for _g in _gaps), "演習8 等間隔")

eq(sp.Rational(27) ** R(2, 3), 9, "演習9 27^(2/3) = 9")
eq(R(2, 3) * pi / 2, pi / 3, "演習9 角")
eq(cart(9, pi / 3), R(9, 2) + 9 * sp.sqrt(3) * I / 2, "演習9")
eq(sp.expand(cart(9, pi / 3) ** 3), -729, "演習9 検算：3 乗")
eq(sp.expand(cart(27, pi / 2) ** 2), -729, "演習9 検算：z^2 も -729")
ne(27 * R(2, 3), 9, "27 × 2/3 = 18 は誤り")

chk(set(sp.solve(z ** 3 - 27, z))
    == {3, R(-3, 2) + 3 * sp.sqrt(3) * I / 2, R(-3, 2) - 3 * sp.sqrt(3) * I / 2},
    "演習10 の 3 解")
eq(cart(3, 2 * pi / 3), R(-3, 2) + 3 * sp.sqrt(3) * I / 2, "演習10 3e^{i2π/3}")
eq(sp.expand((R(-3, 2) + 3 * sp.sqrt(3) * I / 2) ** 2),
   R(-9, 2) - 9 * sp.sqrt(3) * I / 2, "演習10 検算：2 乗")
eq(sp.expand((R(-3, 2) + 3 * sp.sqrt(3) * I / 2) ** 3), 27, "演習10 検算：3 乗")
eq(3 - R(3, 2) - R(3, 2), 0, "演習10 検算：解の和は 0")
eq(R(27, 4) + R(81, 4), 27, "27/4 + 81/4 = 27")

# ══════════════════════════════════════════════════════════
# 4. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.14** の欄に、次の形で印刷されています。", "公式集にある")
in_text("> De Moivre's theorem", "見出しを逐語で")
in_text("> $[r(\\cos\\theta + i\\sin\\theta)]^{n} = r^{n}(\\cos n\\theta"
        " + i\\sin n\\theta) = r^{n}e^{in\\theta} = r^{n}\\,\\mathrm{cis}\\,n\\theta$",
        "公式集の式を逐語で")
in_text("> Complex roots occur in conjugate pairs.", "Guidance を逐語で")
in_text("> Includes proof by induction for the case where $n \\in \\mathbb{Z}^{+}$.",
        "帰納法の Guidance を逐語で")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 5. GDC / 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl114-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)] == list(range(1, 8)),
    "The idea が 1..7 で連番")
chk(TEXT.count("**検算") >= 12, "検算が十分ある: %d" % TEXT.count("**検算"))
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
_ce = TEXT[TEXT.index("\n## Common errors"):TEXT.index("\n## Exercises")]
chk(_ce.count("::: {.callout-warning}") == 6, "Common errors が 6 つ")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
chk(all("@eq-" not in TEXT.split("$$")[i] for i in range(1, len(TEXT.split("$$")), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    chk(not re.search(r"[ぁ-んァ-ン一-龥]",
                      _blk.replace("**試験ではこう書く**", "")),
        "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aahl114", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
# 1.15 は書けたので、リンクを張る
chk(len(re.findall(r"\]\(aahl-1-15\.qmd", TEXT)) == 2, "1.15 へのリンクが 2 本")
not_in_text("次の項目 **AHL 1.15**", "文字案内はリンクに直した")
chk(len(re.findall(r"\]\(aahl-1-1[23]\.qmd", TEXT)) >= 5, "1.12・1.13 へのリンク")
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head, "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は 1 つだけ")
not_in_text("**この節ですること：", "節の頭の 1 文は置かない")
not_in_text("\\vec{", "ベクトルの記号は太字")
chk(len(re.findall(r"^::: ", TEXT, re.M)) == len(re.findall(r"^:::$", TEXT, re.M)),
    "::: の開閉が一致")
for _h in re.findall(r"^#{1,4} .+$", TEXT, re.M):
    chk(not re.search(r"\$\s*—", _h), "見出しで数式の直後に —: " + _h)
_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_j = TEXT.index(chr(10) + "## Worked examples", _i)
_wiw = TEXT[_i:_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
# ★ The idea の見出しは「英語（日本語）」の形（_AA-HL-PLAN.md の「決まったこと」5）
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)
in_text("### 1. Conjugate roots（複素数の解は、共役な組で現れる） {#conjugate-roots}", "見出し 1")
in_text("### 2. Building a polynomial with real "
        "coefficients（実数係数の多項式を組み立てる） {#build}", "見出し 2")
in_text("### 3. De Moivre's theorem（De Moivre の定理） {#demoivre}", "見出し 3")
in_text("### 4. Finding powers（累乗を出す） {#powers}", "見出し 4")
in_text("### 5. Rational exponents（有理数の指数） {#rational}", "見出し 5")
in_text("### 6. The equation $z^{n} = w$ has exactly $n$ roots（$n$ "
        "乗根は $n$ 個あります） {#nth-roots}", "見出し 6")
in_text("### 7. How the $n$th roots are arranged（$n$ 乗根の並び方） "
        "{#roots-picture}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 6. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-1-14-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-1-14-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Each power turns by $\\\\theta$ and stretches by $r$", "図(a) の題")
in_fig("the argument becomes $n\\\\theta$", "図(a) の要点")
in_fig("The cube roots of a number, on one circle", "図(b) の題")
in_fig("same modulus, arguments", "図(b) の要点")
in_text("累乗するたびに、角が $\\theta$ ずつ増え、長さが $r$ 倍になります。", "キャプション (a)")
in_text("$3$ つの解は、同じ円の上に $\\dfrac{2\\pi}{3}$ おきに並びます。", "キャプション (b)")
chk("2.0 * np.pi / 3.0" in FIG, "図(b) の間隔は 2π/3")
for leak in ["8i", "-64", "-32i", "27i", "4\\cos", "8\\cos"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 7. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("z^{2}-2z+10", "演習1"), ("z^{2}-4z+13", "演習2"),
                    ("-32i", "演習4"), ("z^{3} = -8", "演習5"),
                    ("8\\cos^{4}", "演習7"), ("\\frac{9}{2}", "演習9"),
                    ("\\frac{3\\sqrt{3}}{2}i", "演習10")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 8. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-14.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-1-13.qmd") < DRAFT.index("aahl-1-14.qmd"),
    "サイドバーの並びが 1.13 → 1.14")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-14.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| De Moivre's theorem |", "| root of unity |", "| conjugate |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 9. 見張り
# ══════════════════════════════════════════════════════════
in_text("## 「係数が実数のとき」という条件が要ります", "条件を書いてある")
in_text("$z^{2} - iz = 0$ の解は $0$ と $i$ で、共役な組になっていません。",
        "反例を挙げてある")
in_text("**$k = 3$ にすると $k = 0$ と同じ点に戻ります。**", "k の範囲")
in_text("**$w = 0$ を除いてあるのは、$0$ には偏角がないからです。**", "w ≠ 0 の理由")
in_text("**$\\theta = 0$ で確かめても、あまり役に立ちません。**", "効かない検算を名指し")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
