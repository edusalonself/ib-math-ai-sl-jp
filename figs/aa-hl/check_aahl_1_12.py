"""AA HL 1.12（複素数：Cartesian form）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_12.py
"""
import glob
import os
import re
import sys

import sympy as sp
from sympy import I
from sympy import Rational as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-12.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_12.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
z = sp.Symbol("z")
a, b = sp.symbols("a b", real=True)


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


# ══════════════════════════════════════════════════════════
# 0. 記号のままの恒等式
# ══════════════════════════════════════════════════════════
eq(I ** 2, -1, "i^2 = -1")
eq(sp.expand((a + b * I) * (a - b * I)), a ** 2 + b ** 2, "zz* = a^2+b^2")
eq((a + b * I) + (a - b * I), 2 * a, "z + z* = 2a")
chk(sp.im(sp.expand((a + b * I) * (a - b * I))) == 0, "zz* は実数")
chk(sp.simplify(sp.Abs(a + b * I) ** 2 - (a ** 2 + b ** 2)) == 0,
    "|z|^2 = a^2+b^2")
# 1/z が a+bi の形になる
_inv = sp.simplify(1 / (a + b * I))
eq(_inv, (a - b * I) / (a ** 2 + b ** 2), "1/z = z*/(a^2+b^2)")
eq(sp.simplify(_inv * (a + b * I)), 1, "1/z に z を掛けると 1")
# i の累乗は 4 周期
for _k in range(0, 25):
    eq(I ** _k, I ** (_k % 4), "i^k は 4 周期: k=%d" % _k)
chk([sp.expand(I ** _k) for _k in range(1, 5)] == [I, -1, -I, 1],
    "i, -1, -i, 1 の順")
eq(1 / I, -I, "1/i = -i")
# sqrt(-4)sqrt(-9) ≠ sqrt(36)
eq((2 * I) * (3 * I), -6, "(2i)(3i) = -6")
ne(-6, 6, "sqrt(36) = 6 とはちがう")
eq(sp.sqrt(36), 6, "sqrt(36) = 6")

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
chk(len([_r for _r in sp.solve(sp.Symbol("x") ** 2 + 1, sp.Symbol("x"))
         if _r.is_real]) == 0, "§1 x^2+1=0 に実数解はない")
eq(I ** 15, -I, "§1 i^15 = -i")
chk(15 % 4 == 3, "§1 15 を 4 で割った余りは 3")
eq(sp.re(3 + 2 * I), 3, "§2 Re(3+2i) = 3")
eq(sp.im(3 + 2 * I), 2, "§2 Im(3+2i) = 2")
ne(sp.im(3 + 2 * I), 2 * I, "§2 虚部は 2i ではない")
eq((3 + 2 * I) + (-2 + I), 1 + 3 * I, "§4 和")
eq(sp.expand((3 + 2 * I) * (-2 + I)), -8 - I, "§4 積")
eq(2 * I ** 2, -2, "§4 2i^2 = -2")
eq(sp.expand((3 + 2 * I) * (3 - 2 * I)), 13, "§5 zz* = 13")
eq((3 + 2 * I) + (3 - 2 * I), 6, "§5 z+z* = 6")
eq(sp.simplify((4 + 7 * I) / (3 + 2 * I)), 2 + I, "§6 商は 2+i")
eq(sp.expand((4 + 7 * I) * (3 - 2 * I)), 26 + 13 * I, "§6 分子")
eq(3 ** 2 + 2 ** 2, 13, "§6 分母")
eq(sp.Abs(3 + 2 * I), sp.sqrt(13), "§7 |3+2i| = sqrt(13)")
eq(sp.Abs(-1 + sp.sqrt(3) * I), 2, "§7 |-1+i√3| = 2")
eq(sp.arg(-1 + sp.sqrt(3) * I), 2 * sp.pi / 3, "§7 arg = 2π/3")
eq(sp.atan(sp.sqrt(3) / -1), -sp.pi / 3, "§7 arctan は -π/3 を返す")
ne(-sp.pi / 3, 2 * sp.pi / 3, "§7 それは偏角ではない")
eq(sp.pi - sp.pi / 3, 2 * sp.pi / 3, "§7 π - π/3 = 2π/3")
# 主値の範囲
chk(-sp.pi < sp.arg(-1 + sp.sqrt(3) * I) <= sp.pi, "§7 主値の範囲に入っている")

# ══════════════════════════════════════════════════════════
# 2. 例題 1〜4
# ══════════════════════════════════════════════════════════
_z1, _z2 = 4 + 3 * I, 1 - 2 * I
eq(_z1 + _z2, 5 + I, "例題1(a)")
eq(sp.expand(_z1 * _z2), 10 - 5 * I, "例題1(b)")
eq(sp.simplify(_z1 / _z2), R(-2, 5) + R(11, 5) * I, "例題1(c)")
eq(sp.expand((4 + 3 * I) * (1 + 2 * I)), -2 + 11 * I, "例題1(c) 分子")
eq(1 ** 2 + 2 ** 2, 5, "例題1(c) 分母")
eq(sp.simplify((10 - 5 * I) / _z2), _z1, "例題1 検算：割り戻すと z1")
eq(sp.expand((R(-2, 5) + R(11, 5) * I) * _z2), _z1, "例題1 検算：掛け戻すと z1")
eq(sp.simplify((sp.expand(-2 - 5 * I)) / _z2), sp.simplify((-2 - 5 * I) / _z2),
   "例題1 誤答の確認（形だけ）")
ne(-2 - 5 * I, 10 - 5 * I, "6i^2 の符号を落とした誤答は合わない")

_r2 = sp.solve(z ** 2 - 4 * z + 13, z)
chk(sorted([sp.re(_v) for _v in _r2]) == [2, 2], "例題2 実部は 2")
chk(sorted([sp.im(_v) for _v in _r2]) == [-3, 3], "例題2 虚部は ±3")
eq(sp.expand((2 + 3 * I) ** 2 - 4 * (2 + 3 * I) + 13), 0, "例題2 検算：代入して 0")
eq(sp.expand((2 - 3 * I) ** 2 - 4 * (2 - 3 * I) + 13), 0, "例題2 もう一方も 0")
eq(sp.expand((2 + 3 * I) ** 2), -5 + 12 * I, "例題2 (2+3i)^2")
eq((2 + 3 * I) + (2 - 3 * I), 4, "例題2 解の和は 4")
eq(sp.expand((2 + 3 * I) * (2 - 3 * I)), 13, "例題2 解の積は 13")
eq(16 - 52, -36, "例題2 判別式は -36")
eq(sp.sqrt(-36), 6 * I, "例題2 sqrt(-36) = 6i")
ne(6 * I, -6, "sqrt(-36) は -6 ではない")

eq(sp.Abs(5 - 12 * I), 13, "例題3(a) |z| = 13")
eq(sp.expand((5 - 12 * I) * (5 + 12 * I)), 169, "例題3(b) zz* = 169")
eq(13 ** 2, 169, "例題3 |z|^2 = zz*")
eq(sp.simplify(1 / (5 - 12 * I)), R(5, 169) + R(12, 169) * I, "例題3(c)")
eq(sp.simplify((R(5, 169) + R(12, 169) * I) * (5 - 12 * I)), 1, "例題3 検算：1 に戻る")
eq(25 + 144, 169, "25+144 = 169")
ne(5 - 12, 13, "|z| は a+b ではない")

eq(sp.Abs(-2 + 2 * I), 2 * sp.sqrt(2), "例題4(a)")
eq(sp.arg(-2 + 2 * I), 3 * sp.pi / 4, "例題4(b)")
eq(sp.atan(-1), -sp.pi / 4, "arctan(-1) = -π/4")
ne(-sp.pi / 4, 3 * sp.pi / 4, "例題4(c) それは偏角ではない")
eq(sp.simplify(2 * sp.sqrt(2) * sp.cos(3 * sp.pi / 4)), -2, "例題4 検算 rcosθ = -2")
eq(sp.simplify(2 * sp.sqrt(2) * sp.sin(3 * sp.pi / 4)), 2, "例題4 検算 rsinθ = 2")
eq(sp.simplify(2 * sp.sqrt(2) * sp.cos(-sp.pi / 4)), 2, "誤答なら rcosθ = 2")
eq(sp.simplify(2 * sp.sqrt(2) * sp.sin(-sp.pi / 4)), -2, "誤答なら rsinθ = -2")
eq(sp.arg(2 - 2 * I), -sp.pi / 4, "2-2i の偏角が -π/4")
chk(sp.im(-2 + 2 * I) / sp.re(-2 + 2 * I) == sp.im(2 - 2 * I) / sp.re(2 - 2 * I),
    "b/a は -2+2i と 2-2i で同じ")

# ══════════════════════════════════════════════════════════
# 3. 演習 1〜10
# ══════════════════════════════════════════════════════════
_q1, _q2 = 3 - I, -2 + 5 * I
eq(_q1 + _q2, 1 + 4 * I, "演習1(a)")
eq(_q1 - _q2, 5 - 6 * I, "演習1(b)")
eq(sp.expand(_q1 * _q2), -1 + 17 * I, "演習1(c)")
eq(-5 * I ** 2, 5, "演習1 -5i^2 = 5")
eq(sp.simplify((-1 + 17 * I) / _q2), _q1, "演習1 検算：割り戻す")
eq(sp.expand((-1 + 17 * I) * (-2 - 5 * I)), 87 - 29 * I, "演習1 検算の分子")
eq((-2) ** 2 + 5 ** 2, 29, "演習1 検算の分母")
ne(-11 + 17 * I, -1 + 17 * I, "-5i^2 を -5 とした誤答")

eq(sp.simplify((2 + 5 * I) / (1 - I)), R(-3, 2) + R(7, 2) * I, "演習2")
eq(sp.expand((2 + 5 * I) * (1 + I)), -3 + 7 * I, "演習2 の分子")
eq(1 ** 2 + (-1) ** 2, 2, "演習2 の分母")
eq(sp.expand((R(-3, 2) + R(7, 2) * I) * (1 - I)), 2 + 5 * I, "演習2 検算")
ne(1 ** 2 - (-1) ** 2, 2, "a^2-b^2 とした誤答は 0")

eq(I ** 27, -I, "演習3")
chk(27 % 4 == 3 and 27 // 4 == 6, "演習3 余り 3、商 6")
eq(I ** 28, 1, "演習3 i^28 = 1")
eq(sp.simplify(1 / I), -I, "演習3 検算：1/i = -i")

_q4 = sp.solve(z ** 2 + 2 * z + 10, z)
chk(sorted([sp.re(_v) for _v in _q4]) == [-1, -1], "演習4 実部は -1")
chk(sorted([sp.im(_v) for _v in _q4]) == [-3, 3], "演習4 虚部は ±3")
eq(4 - 40, -36, "演習4 判別式")
eq(sp.expand((-1 + 3 * I) ** 2 + 2 * (-1 + 3 * I) + 10), 0, "演習4 検算")
eq(sp.expand((-1 + 3 * I) ** 2), -8 - 6 * I, "演習4 (-1+3i)^2")
eq((-1 + 3 * I) + (-1 - 3 * I), -2, "演習4 解の和")
eq(sp.expand((-1 + 3 * I) * (-1 - 3 * I)), 10, "演習4 解の積")
ne(-1 + 6 * I, -1 + 3 * I, "実部だけ割った誤答")

eq(sp.Abs(7 + 24 * I), 25, "演習5(a)")
eq(sp.conjugate(7 + 24 * I), 7 - 24 * I, "演習5(b)")
eq(sp.expand((7 + 24 * I) * (7 - 24 * I)), 625, "演習5(c)")
eq(25 ** 2, 625, "演習5 |z|^2 = zz*")
eq(49 + 576, 625, "49+576 = 625")

_s6 = sp.solve([sp.Eq(2 * a + b, 5), sp.Eq(2 * b - a, 10)], [a, b], dict=True)[0]
chk(_s6[a] == 0 and _s6[b] == 5, "演習6 a=0, b=5")
eq(sp.expand((a + b * I) * (2 - I)), (2 * a + b) + (2 * b - a) * I, "演習6 展開")
eq(sp.expand(5 * I * (2 - I)), 5 + 10 * I, "演習6 検算：戻す")
eq(sp.simplify((5 + 10 * I) / (2 - I)), 5 * I, "演習6 割り算でも同じ")

eq(sp.Abs(-3 - 3 * I), 3 * sp.sqrt(2), "演習7(a)")
eq(sp.arg(-3 - 3 * I), -3 * sp.pi / 4, "演習7(b)")
eq(-sp.pi + sp.pi / 4, -3 * sp.pi / 4, "演習7 -π + π/4")
chk(-sp.pi < -3 * sp.pi / 4 <= sp.pi, "演習7 主値の範囲")
chk(not (-sp.pi < 5 * sp.pi / 4 <= sp.pi), "5π/4 は範囲の外")
eq(sp.simplify(3 * sp.sqrt(2) * sp.cos(-3 * sp.pi / 4)), -3, "演習7 検算 rcosθ")
eq(sp.simplify(3 * sp.sqrt(2) * sp.sin(-3 * sp.pi / 4)), -3, "演習7 検算 rsinθ")
eq(sp.simplify(3 * sp.sqrt(2) * sp.cos(sp.pi / 4)), 3, "誤答なら 3")

eq(sp.Abs(sp.sqrt(3) - I), 2, "演習8(a)")
eq(sp.arg(sp.sqrt(3) - I), -sp.pi / 6, "演習8(b)")
eq(sp.tan(sp.pi / 6), 1 / sp.sqrt(3), "tan(π/6) = 1/√3")
eq(sp.simplify(2 * sp.cos(-sp.pi / 6)), sp.sqrt(3), "演習8 検算 rcosθ")
eq(sp.simplify(2 * sp.sin(-sp.pi / 6)), -1, "演習8 検算 rsinθ")
eq(sp.sqrt(3) ** 2, 3, "(√3)^2 = 3")

for _zz in [3 + 2 * I, -3 - 3 * I, I, 7 + 24 * I, -1 + sp.sqrt(3) * I]:
    chk(sp.im(sp.expand(_zz * sp.conjugate(_zz))) == 0,
        "演習9 zz* が実数: %s" % _zz)
eq(sp.expand((3 + 2 * I) * (3 - 2 * I)), 13, "演習9 例：13")
eq(sp.expand((-3 - 3 * I) * (-3 + 3 * I)), 18, "演習9 例：18")
eq(sp.expand(I * (-I)), 1, "演習9 例：1")

eq(sp.expand((4 + 5 * I) ** 2), -9 + 40 * I, "演習10 正しい値")
eq(16 - 25, -9, "演習10 生徒の答えは -9")
eq(sp.re(sp.expand((4 + 5 * I) ** 2)), -9, "その -9 は実部と同じ")
ne(-9, -9 + 40 * I, "しかし答えではない")
eq(2 * 4 * 5, 40, "抜けたまん中の項は 40i")
eq(sp.simplify((-9 + 40 * I) / (4 + 5 * I)), 4 + 5 * I, "演習10 検算：割り戻す")
eq(sp.expand((-9 + 40 * I) * (4 - 5 * I)), 164 + 205 * I, "演習10 検算の分子")
eq(4 ** 2 + 5 ** 2, 41, "演習10 検算の分母")
eq(R(164, 41), 4, "164/41 = 4")
eq(R(205, 41), 5, "205/41 = 5")

# ══════════════════════════════════════════════════════════
# 4. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.12** の欄に、次の $1$ 行だけが印刷されています。", "公式集にある")
in_text("> Complex numbers $\\quad z = a + bi$", "公式集の行を逐語で")
in_text("> The complex plane is also known as the Argand diagram.",
        "Guidance を逐語で")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 5. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("TI-Nspire CX II は、複素数をそのまま計算できます。", "検証済みの事実だけ")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cAngle", "cPolar"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

# ══════════════════════════════════════════════════════════
# 6. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl112-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), "The idea が 1..7 で連番: %s" % _idea)
chk(TEXT.count("**検算") >= 12, "検算が十分ある: %d" % TEXT.count("**検算"))
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
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
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aahl112", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    _p0 = os.path.normpath(os.path.join(os.path.dirname(QMD),
                                        _href.split("#")[0]))
    chk(os.path.exists(_p0), "リンク先のページがない: " + _href)
chk(len(re.findall(r"\]\(\.\./\.\./aa-sl/", TEXT)) >= 4, "AA SL へのリンク")
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
for _line in TEXT.splitlines():
    if _line.startswith("|") and _line.endswith("|"):
        if re.fullmatch(r"[|:\- ]+", _line):
            continue
        for _cell in _line[1:-1].split(" | "):
            chk("|" not in _cell or "\\lvert" in _cell or "\\rvert" in _cell,
                "表のセルの中の裸の | :: " + _line[:60])

# Why it works
_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_j = TEXT.index(chr(10) + "## Worked examples", _i)
_wiw = TEXT[_i:_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
chk(_wiw.count("クリックすると開きます") == 1, "折りたたみは 1 つだけ")

# 節の見出し
# ★ The idea の見出しは「英語（日本語）」の形（_AA-HL-PLAN.md の「決まったこと」5）
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)
in_text("### 1. The number $i$（$i$ という数） {#i}", "見出し 1")
in_text("### 2. Cartesian form（$a+bi$ の形） {#cartesian}", "見出し 2")
in_text("### 3. The complex plane（複素平面） {#plane}", "見出し 3")
in_text("### 4. Adding, subtracting and multiplying（足す・引く・かける） "
        "{#arithmetic}", "見出し 4")
in_text("### 5. The conjugate（共役複素数） {#conjugate}", "見出し 5")
in_text("### 6. Division: making the denominator real（割り算：分母を実数にする） "
        "{#division}", "見出し 6")
in_text("### 7. Modulus and argument（絶対値と偏角） {#modulus-argument}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 7. 図
# ══════════════════════════════════════════════════════════
SVG_A = os.path.join(BASE, "img", "aahl-1-12-idea-a.svg")
SVG_B = os.path.join(BASE, "img", "aahl-1-12-idea-b.svg")
chk(os.path.exists(SVG_A), "図 (a) がある")
chk(os.path.exists(SVG_B), "図 (b) がある")
chk("](img/aahl-1-12-idea-a.svg)" in TEXT, "本文が図 (a) を貼っている")
chk("](img/aahl-1-12-idea-b.svg)" in TEXT, "本文が図 (b) を貼っている")
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Four complex numbers on the complex plane", "図(a) の題")
in_fig("mirror images", "図(a) の共役")
in_fig("Modulus and argument of $z = -1 + i\\\\sqrt{3}$", "図(b) の題")
in_fig("measured from", "図(b) の偏角の測り方")
in_text("$4$ つの複素数を置いたところ。$z_1$ と $z_4$ は実軸について対称です。",
        "キャプションが (a) を説明")
in_text("原点から $z$ までの長さが $r$、正の実軸から測った角が $\\theta$ です。",
        "キャプションが (b) を説明")
# 図の値が本文と合っている
for _pt in ["(3, 2,", "(-2, 1,", "(-1, -2,", "(3, -2,"]:
    in_fig(_pt, "図(a) の点 " + _pt)
eq(sp.conjugate(3 + 2 * I), 3 - 2 * I, "図(a) の z1 と z4 は共役")
chk("ZX, ZY = -1.0, np.sqrt(3.0)" in FIG, "図(b) の点は -1 + i√3")
# 図が例題・演習の答えを載せていないか
for leak in ["10 - 5i", "2 + 3i", "5 - 12i", "169", "625", "17i", "40i",
             "7+24i", "3\\sqrt{2}", "-\\frac{3\\pi}{4}"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 8. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("-1 + 17i", "演習1"), ("i^{27}", "演習3"),
                    ("-1 \\pm 3i", "演習4"), ("625", "演習5"),
                    ("3\\sqrt{2}", "演習7"), ("-\\frac{3\\pi}{4}", "演習7"),
                    ("-\\frac{\\pi}{6}", "演習8"), ("-9 + 40i", "演習10")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 9. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-12.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-1-11.qmd") < DRAFT.index("aahl-1-12.qmd"),
    "サイドバーの並びが 1.11 → 1.12")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-12.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
_ticked = re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), "✅ %d と ページ %d" % (len(_ticked), len(_written)))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|", IDX, re.M)) == 35,
    "一覧は 35 行")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| complex number |", "| imaginary unit |", "| real part |",
          "| imaginary part |", "| conjugate |", "| complex plane |",
          "| Argand diagram |", "| modulus |", "| argument |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written),
    "PLAN の進捗がページ数と合っている")

# ══════════════════════════════════════════════════════════
# 10. 見張り
# ══════════════════════════════════════════════════════════
in_text("**「存在しない数」という意味ではありません。**", "imaginary の言い方")
in_text("## 虚部は $2i$ ではなく $2$ です", "虚部は実数")
in_text("**この本では $z^{*}$ と書きます。**", "共役の記号を決めてある")
in_text("$-\\pi < \\theta \\leq \\pi$", "主値の範囲を書いてある")
in_text("**角は radian で書きます。**", "radian で書く")
in_text("## $\\arg z$ は、$\\arctan\\dfrac{b}{a}$ とはかぎりません", "象限の注意")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
