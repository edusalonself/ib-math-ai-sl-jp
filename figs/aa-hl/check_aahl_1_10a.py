"""AA HL 1.10a（counting principles）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_10a.py
"""
import glob
import os
import re
import sys

import sympy as sp
from sympy import binomial as C
from sympy import factorial as F
from sympy import Rational as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-10a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_10a.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
n, r_ = sp.symbols("n r", positive=True, integer=True)


def P(a, b):
    return F(a) / F(a - b)


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
# 0. 公式そのもの（記号のまま）
# ══════════════════════════════════════════════════════════
for _n in range(0, 11):
    for _r in range(0, _n + 1):
        # nPr = n!/(n-r)! が、素朴な「n から r 個ぶんのかけ算」と一致する
        _prod = sp.Integer(1)
        for _k in range(_r):
            _prod *= (_n - _k)
        eq(P(_n, _r), _prod, "nPr = n(n-1)...: n=%d r=%d" % (_n, _r))
        # nCr = nPr / r!
        eq(C(_n, _r), P(_n, _r) / F(_r), "nCr = nPr/r!: n=%d r=%d" % (_n, _r))
        # nPr = nCr * r!
        eq(P(_n, _r), C(_n, _r) * F(_r), "nPr = nCr r!: n=%d r=%d" % (_n, _r))
        # nPr >= nCr、等号は r <= 1 のときだけ
        chk(P(_n, _r) >= C(_n, _r), "nPr >= nCr: n=%d r=%d" % (_n, _r))
        chk((P(_n, _r) == C(_n, _r)) == (_r <= 1),
            "等号は r<=1 のときだけ: n=%d r=%d" % (_n, _r))
        # 対称性
        eq(C(_n, _r), C(_n, _n - _r), "nCr = nC(n-r): n=%d r=%d" % (_n, _r))
eq(F(0), 1, "0! = 1")
eq(F(1), 1, "1! = 1")
eq(F(2), 2, "2! = 2")
eq(F(3), 6, "3! = 6")
eq(F(4), 24, "4! = 24")
chk(F(10) > 3000000, "10! は 300 万を超える")
for _n in range(1, 9):
    eq(C(_n, 0), 1, "%dC0 = 1" % _n)
    eq(C(_n, _n), 1, "%dCn = 1" % _n)
    eq(P(_n, 0), 1, "%dP0 = 1" % _n)
# 0! = 1 でなければ nCn = 1 にならない
eq(C(5, 5), 1, "5C5 = 1")
eq(F(5) / (F(5) * F(0)), 1, "n!/(n! 0!) = 1")

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
eq(4 * 3, 12, "§1 4×3 = 12")
eq(3 + 2, 5, "§1 3+2 = 5")
eq(26 ** 2, 676, "§1 26^2 = 676")
eq(26 * 25, 650, "§1 26×25 = 650")
ne(676, 650, "くり返してよいかどうかで変わる")
eq(4 * 3 * 2 * 1, 24, "§2 4! = 24")
eq(P(8, 3), 336, "§3 8P3 = 336")
eq(8 * 7 * 6, 336, "§3 8×7×6 = 336")
eq(F(8) / F(5), 336, "§3 8!/5! = 336")
eq(C(8, 3), 56, "§4 8C3 = 56")
eq(R(336, 6), 56, "§4 336/6 = 56")
eq(sp.Integer(8 * 7 * 6) / 6, 56, "§4 上 3 つ／3! = 56")
eq(C(7, 3), 35, "§6 7C3 = 35")
eq(C(6, 2), 15, "§6 6C2 = 15")
eq(C(6, 3), 20, "§6 6C3 = 20")
eq(C(6, 2) + C(6, 3), C(7, 3), "§6 含む＋含まない = 全体")
eq(15 + 20, 35, "§6 15+20 = 35")
eq(F(3) * F(2), 12, "§6 3!×2! = 12")
eq(F(4), 24, "§6 4! = 24")
# 4 人の並びを実際に書き出して、B と C が隣り合うものを数える
import itertools
_adj = [p for p in itertools.permutations("ABCD")
        if abs(p.index("B") - p.index("C")) == 1]
chk(len(_adj) == 12, "§6 書き出しても 12 通り: %d" % len(_adj))
chk(len(list(itertools.permutations("ABCD"))) == 24, "§6 全体は 24 通り")
eq(C(6, 3) - C(4, 3), 16, "§6 少なくとも 1 人女子は 16")
eq(C(4, 3), 4, "§6 4C3 = 4")
eq(C(2, 1) * C(4, 2) + C(2, 2) * C(4, 1), 16, "§6 場合分けでも 16")
eq(R(16, 20), R(4, 5), "§7 16/20 = 4/5")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
# 山の大きさがそろっている：nPr を r! で割ると nCr
for _n in range(1, 9):
    for _r in range(0, _n + 1):
        chk(sp.Integer(P(_n, _r)) % sp.Integer(F(_r)) == 0,
            "nPr は r! で割り切れる: n=%d r=%d" % (_n, _r))
eq(F(5) / (F(5) * F(0)), C(5, 5), "0! = 1 でないと nCn = 1 にならない")

# ══════════════════════════════════════════════════════════
# 3. 例題 1（4 桁の code）
# ══════════════════════════════════════════════════════════
eq(10 ** 4, 10000, "例題1(a) 10000")
eq(10 * 9 * 8 * 7, 5040, "例題1(b) 5040")
eq(P(10, 4), 5040, "例題1(b) = 10P4")
eq(9 * 9 * 8 * 7, 4536, "例題1(c) 4536")
eq(R(5040, 10), 504, "検算：先頭が 0 のものは 504")
eq(5040 - 504, 4536, "検算：5040 - 504 = 4536")
eq(9 * 336, 3024, "誤答：残りを 8×7×6 とすると 3024")
ne(3024, 4536, "その誤答は合わない")
# 書き出しで確かめる（0-9 から 4 桁、すべて異なる、先頭が 0 でない）
_cnt = 0
for _p in itertools.permutations(range(10), 4):
    if _p[0] != 0:
        _cnt += 1
chk(_cnt == 4536, "例題1(c) を書き出しても 4536: %d" % _cnt)
chk(len(list(itertools.permutations(range(10), 4))) == 5040, "例題1(b) も書き出しで 5040")

# ══════════════════════════════════════════════════════════
# 4. 例題 2（club 10 人）
# ══════════════════════════════════════════════════════════
eq(P(10, 3), 720, "例題2(a) 720")
eq(10 * 9 * 8, 720, "例題2(a) = 10×9×8")
eq(C(10, 3), 120, "例題2(b) 120")
eq(C(9, 2), 36, "検算：9C2 = 36")
eq(C(9, 3), 84, "検算：9C3 = 84")
eq(C(9, 2) + C(9, 3), 120, "検算：36+84 = 120")
eq(C(10, 3) * F(3), 720, "検算：120×6 = 720")
eq(R(720, 120), 6, "(a) は (b) の 6 倍")
eq(F(3), 6, "3! = 6")
ne(720, 120, "2 つの答えは違う")

# ══════════════════════════════════════════════════════════
# 5. 例題 3（9 人から 4 人）
# ══════════════════════════════════════════════════════════
eq(C(5, 2), 10, "5C2 = 10")
eq(C(4, 2), 6, "4C2 = 6")
eq(C(5, 2) * C(4, 2), 60, "例題3(a) 60")
eq(C(9, 4), 126, "9C4 = 126")
eq(C(5, 4), 5, "5C4 = 5")
eq(126 - 5, 121, "例題3(b) 121")
eq(sum(C(4, _b) * C(5, 4 - _b) for _b in range(1, 5)), 121, "検算：男子の人数で足す")
eq(C(4, 1) * C(5, 3), 40, "4C1×5C3 = 40")
eq(C(4, 2) * C(5, 2), 60, "4C2×5C2 = 60")
eq(C(4, 3) * C(5, 1), 20, "4C3×5C1 = 20")
eq(C(4, 4) * C(5, 0), 1, "4C4×5C0 = 1")
eq(40 + 60 + 20 + 1, 121, "検算：40+60+20+1 = 121")
_dec = [C(5, _g) * C(4, 4 - _g) for _g in range(5)]
chk(list(_dec) == [1, 20, 60, 40, 5], "検算：女子の人数で分けると 1,20,60,40,5")
eq(sum(_dec), 126, "検算：合計は 9C4 = 126")
eq(1 + 20 + 60 + 40 + 5, 126, "1+20+60+40+5 = 126")
chk(_dec[2] == 60, "(a) は 3 番目")
eq(C(5, 2) + C(4, 2), 16, "誤答：足すと 16")
ne(16, 60, "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 6. 例題 4（8 冊の本）
# ══════════════════════════════════════════════════════════
eq(F(6) * F(3), 4320, "例題4(a) 4320")
eq(F(6), 720, "6! = 720")
eq(F(8), 40320, "8! = 40320")
eq(F(8) - F(6) * F(3), 36000, "例題4(b) 36000")
eq(6 * F(3) * F(5), 4320, "検算：席の位置から数えても 4320")
eq(F(5), 120, "5! = 120")
eq(R(F(6) * F(3), F(8)), R(3, 28), "(a) の割合は 3/28")
eq(1 - R(3, 28), R(25, 28), "(b) の割合は 25/28")
eq(F(8) * R(25, 28), 36000, "検算：40320×25/28 = 36000")
eq(R(40320, 28), 1440, "40320/28 = 1440")
eq(1440 * 25, 36000, "1440×25 = 36000")
eq(F(8) - F(6), 39600, "誤答：3! を掛け忘れると 39600")
ne(39600, 36000, "その誤答は合わない")
eq(F(8) - F(3), 40314, "誤答：8! - 3!")
ne(40314, 36000, "8! - 3! ではない")
# 書き出しで確かめる（8 個のうち 3 個が隣り合う並べ方）
_together = 0
for _p in itertools.permutations(range(8)):
    _pos = sorted(_p.index(_i) for _i in range(3))
    if _pos[2] - _pos[0] == 2:
        _together += 1
chk(_together == 4320, "例題4(a) を書き出しても 4320: %d" % _together)

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(5 ** 3 * (9 * 8), 9000, "演習1 9000")
eq(5 ** 3, 125, "5^3 = 125")
eq(9 * 8, 72, "9×8 = 72")
eq(P(9, 2), 72, "検算：9P2 = 72")
eq(P(5, 3), 60, "5P3 = 60（くり返し不可なら）")
ne(P(5, 3), 5 ** 3, "くり返してよいと順列ではない")

eq(P(7, 2), 42, "演習2(a) 42")
eq(7 * 6, 42, "7×6 = 42")
eq(C(7, 2), 21, "演習2(b) 21")
eq(C(7, 5), C(7, 2), "演習2(c) 7C5 = 7C2")
eq(6 + 5 + 4 + 3 + 2 + 1, 21, "検算：割り算を使わずに 21")
eq(21 * F(2), 42, "検算：21×2! = 42")

eq(P(11, 3), 990, "演習3 990")
eq(11 * 10 * 9, 990, "11×10×9 = 990")
eq(3 * (10 * 9), 270, "検算：Ravi が取る場合 270")
eq(10 * 9 * 8, 720, "検算：Ravi が取らない場合 720")
eq(270 + 720, 990, "検算：270+720 = 990")
eq(C(11, 3), 165, "誤答：11C3 = 165")
ne(165, 990, "その誤答は合わない")

eq(C(12, 4), 495, "演習4(a) 495")
eq(C(11, 3), 165, "演習4(b) 165")
eq(C(11, 4), 330, "検算：Aiko を含まないのは 330")
eq(165 + 330, 495, "検算：165+330 = 495")
eq(C(12, 3), 220, "誤答：12C3 = 220")
ne(C(12, 3), C(11, 3), "12C3 と 11C3 は違う")

eq(F(9), 362880, "演習5(a) 362880")
eq(F(8) * F(2), 80640, "演習5(b) 80640")
eq(8 * 2 * F(7), 80640, "検算：席の位置から数えても 80640")
eq(F(7), 5040, "7! = 5040")
eq(8 * 2, 16, "8×2 = 16")
eq(R(80640, 362880), R(2, 9), "隣り合う割合は 2/9")
ne(F(8), 80640, "2! を忘れると半分")
eq(F(8), 40320, "8! = 40320")

eq(C(5, 2) * C(4, 1) + C(5, 3), 50, "演習6 50")
eq(C(5, 2) * C(4, 1), 40, "5C2×4C1 = 40")
eq(C(5, 3), 10, "5C3 = 10")
eq(C(5, 1) * C(4, 2) + C(4, 3), 34, "検算：当てはまらないのは 34")
eq(C(5, 1) * C(4, 2), 30, "5C1×4C2 = 30")
eq(50 + 34, 84, "検算：50+34 = 84")
eq(C(9, 3), 84, "全体は 9C3 = 84")
eq(C(5, 2) * C(7, 1), 70, "誤答：重複して数えると 70")
eq(70 - 50, 20, "余分は 20")
eq(2 * C(5, 3), 20, "それは 5C3 を 2 回余分に数えたぶん")
ne(70, 50, "その誤答は合わない")

eq(F(8) - F(7) * F(2), 30240, "演習7 30240")
eq(F(7) * F(2), 10080, "7!×2! = 10080")
eq(R(14, 56), R(1, 4), "隣り合う割合は 1/4")
eq(8 * 7, 56, "8×7 = 56")
eq(7 * 2, 14, "7×2 = 14")
eq(F(8) * R(3, 4), 30240, "検算：40320×3/4 = 30240")
eq(F(8) - F(2), 40318, "誤答：8! - 2!")
ne(40318, 30240, "その誤答は合わない")
# 書き出しで確かめる（8 人のうち 2 人が隣り合わない）
_not_adj = 0
for _p in itertools.permutations(range(8)):
    if abs(_p.index(0) - _p.index(1)) != 1:
        _not_adj += 1
chk(_not_adj == 30240, "演習7 を書き出しても 30240: %d" % _not_adj)

_nn = sp.Symbol("nn")
_sol = sp.solve(sp.Eq(_nn * (_nn - 1) / 2, 45), _nn)
chk(sorted(int(v) for v in _sol) == [-9, 10], "演習8 解は -9 と 10: %s" % _sol)
eq(C(10, 2), 45, "演習8 検算：10C2 = 45")
eq(sp.Integer(10 * 9) / 2, 45, "10×9/2 = 45")
eq(C(9, 2), 36, "誤答：9C2 = 36")
ne(36, 45, "n=9 では合わない")
eq(sp.expand(_nn * (_nn - 1) / 2 - 45) * 2, sp.expand(_nn ** 2 - _nn - 90),
   "演習8 の 2 次方程式")
eq(sp.expand((_nn - 10) * (_nn + 9)), sp.expand(_nn ** 2 - _nn - 90), "因数分解")

eq(R(C(4, 2) * C(3, 1), C(7, 3)), R(18, 35), "演習9 18/35")
eq(C(4, 2), 6, "4C2 = 6")
eq(C(3, 1), 3, "3C1 = 3")
eq(C(7, 3), 35, "7C3 = 35")
eq(6 * 3, 18, "6×3 = 18")
eq(C(3, 3) + C(4, 1) * C(3, 2) + C(4, 2) * C(3, 1) + C(4, 3), 35,
   "検算：赤の個数で分けると合計 35")
eq(C(4, 1) * C(3, 2), 12, "4C1×3C2 = 12")
eq(1 + 12 + 18 + 4, 35, "1+12+18+4 = 35")
eq(R(1 + 12 + 18 + 4, 35), 1, "確率の合計は 1")
eq(P(7, 3), 210, "誤答：分母を 7P3 = 210 とすると")
ne(R(18, 210), R(18, 35), "その誤答は合わない")

eq(P(12, 3), 1320, "演習10 生徒の答えは 1320")
eq(12 * 11 * 10, 1320, "12×11×10 = 1320")
eq(C(12, 3), 220, "演習10 正しい答えは 220")
eq(R(1320, 6), 220, "1320/3! = 220")
eq(C(11, 2), 55, "検算：11C2 = 55")
eq(12 * 55, 660, "検算：12×55 = 660")
eq(R(660, 3), 220, "検算：660/3 = 220")
ne(1320, 220, "生徒の答えは 6 倍大きい")
eq(R(1320, 220), 6, "ちょうど 3! 倍")

# ══════════════════════════════════════════════════════════
# 8. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.10** の欄に、次の $2$ つが印刷されています。", "公式集にある")
in_text("> Combinations $^{n}\\mathrm{C}_{r} = \\dfrac{n!}{r!(n-r)!}$",
        "Combinations を逐語で")
in_text("> Permutations $^{n}\\mathrm{P}_{r} = \\dfrac{n!}{(n-r)!}$",
        "Permutations を逐語で")
chk(TEXT.count("> Not required: Permutations where some objects are identical."
               " Circular arrangements.") == 2,
    "Not required を逐語で 2 か所（第 3 節と Common errors）")
in_text("公式集の **4.5** の欄に、次の形で印刷されています。", "P(A) の欄")
in_text("P(A) = \\frac{n(A)}{n(U)}", "P(A) = n(A)/n(U)")
in_text("**公式集には印刷されていません。**", "かけ算の原理と n! は公式集にない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
not_in_text("Counting principles, including permutations and combinations.",
            "Content 欄は引用しない")

# ══════════════════════════════════════════════════════════
# 9. GDC（_方針変更-2026-09-15.md 第 18 節、_AA-HL-PLAN.md 決まったこと 3）
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("`menu → Probability → Permutations` を選ぶと `nPr(` が、", "Nspire のメニュー")
in_text("`nPr(8,3)`", "Nspire の入力の形")
in_text("`nCr(8,3)`", "Nspire の入力の形")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "8 nPr 3", "nDeriv"]:
    not_in_text(_m, "TI-Nspire 以外の機種・存在しない関数: " + _m)

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl110a-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk("## 解答例（答案用紙にはこう書く）" not in TEXT, "解答例の見出しをそろえた")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
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
    chk(_r0 == "aahl110a", "他ページの @-ref: " + _r0)
# ページをまたぐリンクは、ファイルが実在するか（_AA-HL-PLAN.md 決まったこと 4）
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    _p = os.path.normpath(os.path.join(os.path.dirname(QMD),
                                       _href.split("#")[0]))
    chk(os.path.exists(_p), "リンク先のページがない: " + _href)
chk(len(re.findall(r"\]\(\.\./\.\./aa-sl/", TEXT)) >= 3,
    "AA SL へのリンクが 3 本以上ある")
chk(not re.search(r"SL [0-9.]+[ab]? の第 \d+ 節", TEXT),
    "SL のページを節番号で呼んでいない")
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
not_in_text("**この節ですること：", "節の頭の 1 文は置かない（第 5 節の撤回）")
not_in_text("\\vec{", "ベクトルの記号は太字（決まったこと 1）")
chk(len(re.findall(r"^::: ", TEXT, re.M)) == len(re.findall(r"^:::$", TEXT, re.M)),
    "::: の開閉が一致")

# ══════════════════════════════════════════════════════════
# 11. Why it works は折りたたむ（_方針変更-2026-09-15.md 第 15 節）
# ══════════════════════════════════════════════════════════
_wiw_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_wiw_j = TEXT.index(chr(10) + "## Worked examples", _wiw_i)
_wiw = TEXT[_wiw_i:_wiw_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
chk(_wiw.count("クリックすると開きます") == 1, "折りたたみは 1 つだけ")

# ══════════════════════════════════════════════════════════
# 12. 節の見出しの英語（_方針変更-2026-09-15.md 第 17 節）
# ══════════════════════════════════════════════════════════
# ★ The idea の見出しは「英語（日本語）」の形（_AA-HL-PLAN.md の「決まったこと」5）
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)
in_text("### 1. The multiplication principle（かけ算で数える） "
        "{#multiplication}", "見出し 1")
in_text("### 2. Factorials: arranging all of them（階乗：全部を並べる） "
        "{#factorial}", "見出し 2")
in_text("### 3. Permutations: arranging some of them（順列：一部を並べる） "
        "{#permutation}", "見出し 3")
in_text("### 4. Combinations: choosing without order（組合せ：順番を問わずに選ぶ） "
        "{#combination}", "見出し 4")
in_text("### 5. Which one to use（順列と組合せ、どちらを使うか） {#which}", "見出し 5")
in_text("### 6. Counting with restrictions（条件が付いた数え方） "
        "{#restrictions}", "見出し 6")
in_text("### 7. From counting to probability（数え上げから確率へ） "
        "{#to-probability}", "見出し 7")
# 「—」を数式のすぐ後ろに置かない（第 16 節）
for _h in re.findall(r"^#{1,4} .+$", TEXT, re.M):
    chk(not re.search(r"\$\s*—", _h), "見出しで数式の直後に — がある: " + _h)

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG_A = os.path.join(BASE, "img", "aahl-1-10a-idea-a.svg")
SVG_B = os.path.join(BASE, "img", "aahl-1-10a-idea-b.svg")
chk(os.path.exists(SVG_A), "図 (a) がある")
chk(os.path.exists(SVG_B), "図 (b) がある")
chk("](img/aahl-1-10a-idea-a.svg)" in TEXT, "本文が図 (a) を貼っている")
chk("](img/aahl-1-10a-idea-b.svg)" in TEXT, "本文が図 (b) を貼っている")
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("One shirt and one pair of trousers", "図(a) の題")
in_fig("$4 \\\\times 3 = 12$ outfits", "図(a) の答え")
in_fig("one dot for each outfit", "図(a) の読み方")
in_fig("Choosing 3 people out of 8, then putting them in order", "図(b) の題")
in_fig("$^{8}\\\\mathrm{C}_{3} = 56$", "図(b) の選び方の数")
in_fig("$^{8}\\\\mathrm{P}_{3} = 336$", "図(b) の並べ方の数")
in_fig("$\\\\times\\\\ 3! = 6$", "図(b) の倍率")
in_text("shirt が $4$ 枚、trousers が $3$ 本。点の $1$ つずつが、$1$ 通りの組み合わせです。",
        "キャプションが (a) を説明")
in_text("$1$ つの選び方は $3!$ 通りに並びます。だから並べ方の数は、選び方の数の $3!$ 倍です。",
        "キャプションが (b) を説明")
# 図の値が本文と合っている
eq(4 * 3, 12, "図(a) の 4×3 = 12")
eq(C(8, 3) * F(3), P(8, 3), "図(b) の 56×3! = 336")
chk(len(set(["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"])) == int(F(3)),
    "図(b) の並べ方は 3! 通り")
for _perm in ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]:
    in_fig("$%s$" % _perm, "図(b) の並び " + _perm)
    chk(sorted(_perm) == ["A", "B", "C"], "図(b) の並びは同じ 3 人")
# 図が演習の答えを載せていないか
for leak in ["9000", "990", "495", "165", "362880", "80640", "30240",
             "220", "1320", "4536", "36000", "4320", "121", "10080"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 14. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("9000", "演習1"), ("$990$", "演習3"), ("495", "演習4(a)"),
                    ("362\\,880", "演習5(a)"), ("80\\,640", "演習5(b)"),
                    ("30\\,240", "演習7"), ("$220$", "演習10"),
                    ("$1320$", "演習10 の誤答")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))
# 逆に、本文で使った数は演習の答えになっていない
for _v in [12, 5, 676, 650, 24, 336, 56, 35, 15, 20, 16]:
    chk(_v not in [9000, 990, 495, 165, 362880, 80640, 50, 30240, 220],
        "本文の数が演習の答えと同じ: %d" % _v)

# ══════════════════════════════════════════════════════════
# 15. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-10a.qmd" in DRAFT, "draft に登録")
chk("HL 1.10a — Counting principles: permutations and combinations" in DRAFT,
    "サイドバーの text")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-10a.qmd)" in IDX, "index にある")
chk("まだ書いていません" not in IDX, "場所取りのページから差しかえた")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
_ticked = re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written),
    "✅ %d と ページ %d" % (len(_ticked), len(_written)))
_rows = re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|", IDX, re.M)
chk(len(_rows) == 35, "一覧は 35 行: %d" % len(_rows))
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
chk(_mm is not None and int(_mm.group(2)) == 35, "「全 35 ページ」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| counting principle |", "| multiplication principle |",
          "| permutation |", "| combination |", "| factorial |",
          "| arrangement |", "| selection |", "| at random |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
# 進捗は、書き上がったページ数から動的に見る（ページを足すたびに
# 直さずにすむように）。
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written),
    "PLAN の進捗がページ数と合っている")
chk("| AHL 1.10 | a | Counting principles（順列・組合せ）。`Not required:`"
    " 同じものを含む順列、円順列 | ✅ |" in PLAN, "PLAN の一覧に ✅")

# ══════════════════════════════════════════════════════════
# 16. 見張り（設計判断が戻っていないか）
# ══════════════════════════════════════════════════════════
in_text("**$^{n}\\mathrm{P}_{r}$ が $^{n}\\mathrm{C}_{r}$ より小さくなることはありません。**",
        "無条件の言い切りにしていない")
not_in_text("$^{n}\\mathrm{P}_{r}$ のほうが、いつも大きい", "旧：言い切り")
in_text("$r = 0$ と $r = 1$ では $r! = 1$ なので等しくなります。", "等号になる場合を書いた")
in_text("**どの山も同じ大きさであることが、この議論の要です。**", "割り算が使える条件")
in_text("**公式が合うためには $0! = 1$ 以外にない**", "0! = 1 の順序")
in_text("**これは検算になりません。**", "効かない検算を、効かないと書く")
chk(TEXT.count("検算になりません") + TEXT.count("検算にはなりません")
    + TEXT.count("検算としては弱い") >= 4,
    "効かない検算を 4 か所以上で名指し: %d" % (
        TEXT.count("検算になりません") + TEXT.count("検算にはなりません")
        + TEXT.count("検算としては弱い")))
in_text("同じものが混ざっているときの並べ方（`BANANA` の並べかえのような問題）",
        "範囲外を具体名で")
in_text("**同じ team を何度も数えているからです。**", "重複して数える誤り")
eq(C(4, 1) * C(8, 3), 224, "重複して数えた誤答は 224")
eq(C(8, 3), 56, "8C3 = 56")
ne(224, 121, "その誤答は合わない")
in_text("$^{4}\\mathrm{C}_{1} \\times {}^{8}\\mathrm{C}_{3} = 4 \\times 56 = 224$",
        "その誤答を数で示した")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
