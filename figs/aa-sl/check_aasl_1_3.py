"""AA SL 1.3（geometric sequences and series）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_3.py

方針は他のページのチェッカーと同じです。
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-3.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_3.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def _S(x):
    """float を、そのままの値の有理数にする（nsimplify の推測を避ける）。"""
    if isinstance(x, float):
        return sp.Rational(str(x))
    return sp.nsimplify(x, rational=True)


def eq(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) == 0, msg + f"  ({a} vs {b})")


def ne(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) != 0, msg + f"  ({a} vs {b})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def term(u1, r, n):
    """第 n 項。定義（r を n-1 回掛ける）から。"""
    return sp.nsimplify(u1) * sp.nsimplify(r) ** (n - 1)


def brute_sum(u1, r, n):
    """はじめの n 項の和を、1 つずつ足して出す（公式を使わない）。"""
    return sum(term(u1, r, k) for k in range(1, n + 1))


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの（記号のまま）
# ══════════════════════════════════════════════════════════
_u1, _r, _n = sp.symbols("u1 r n")
# 2 つの和の形が同じ式であること
eq(sp.simplify(_u1 * (_r ** _n - 1) / (_r - 1) - _u1 * (1 - _r ** _n) / (1 - _r)),
   0, "S_n の 2 つの形は同じ式")
# n = 1 で u_1 に戻る
eq((_u1 * _r ** (_n - 1)).subs(_n, 1), _u1, "n=1 で u_1 に戻る")
ne((_u1 * _r ** _n).subs(_n, 1), _u1, "u_1 r^n は n=1 で u_1 にならない（誤り）")
# u_q / u_p = r^(q-p)
_p, _q = sp.symbols("p q")
eq(sp.simplify((_u1 * _r ** (_q - 1)) / (_u1 * _r ** (_p - 1)) - _r ** (_q - _p)),
   0, "u_q/u_p = r^(q-p)")
# 導き方（rS - S）が、公式と一致する
_k = sp.symbols("k")
for _rr in [2, 3, sp.Rational(1, 2), sp.Rational(3, 4), -2]:
    for _nn in [1, 2, 5, 7]:
        eq(brute_sum(5, _rr, _nn),
           5 * (_rr ** _nn - 1) / (_rr - 1),
           f"公式と足し上げが一致: r={_rr}, n={_nn}")
# r = 1 のときは n u_1
eq(brute_sum(7, 1, 6), 6 * 7, "r=1 なら和は n u_1")
# u_1 r^{n-1} と (u_1 r)^{n-1} は別物
ne(3 * 2 ** 4, (3 * 2) ** 4, "3×2^4 と (3×2)^4 は別物")
eq(3 * 2 ** 4, 48, "3×2^4 = 48")
eq((3 * 2) ** 4, 1296, "(3×2)^4 = 1296")

# ══════════════════════════════════════════════════════════
# 1. The idea の中の数
# ══════════════════════════════════════════════════════════
chk([term(3, 2, i) for i in range(1, 6)] == [3, 6, 12, 24, 48],
    "3,6,12,24,48 が合う")
eq(term(3, 2, 5), 48, "u_5 = 48")
eq(brute_sum(3, 2, 5), 93, "5 項の和は 93")
eq(3 * (2 ** 5 - 1) / (2 - 1), 93, "公式でも 93")
chk([term(100, sp.Rational(1, 2), i) for i in range(1, 4)] == [100, 50, 25],
    "100,50,25（r=1/2）")
chk([term(7, 1, i) for i in range(1, 4)] == [7, 7, 7], "r=1 なら同じ数が並ぶ")
chk([term(-3, 2, i) for i in range(1, 4)] == [-3, -6, -12],
    "u_1<0 だと r>1 でも値は小さくなる")
not_in_text("$81, 27, 9, \\ldots$ は $r = \\frac{1}{3}$",
            "演習 2 の答えを本文で見せていない（レビュー6）")
# どちらもそろわない例
_x = [1, 2, 4, 7]
chk([_x[i+1]-_x[i] for i in range(3)] == [1, 2, 3], "1,2,4,7 の差は 1,2,3")
chk([sp.Rational(_x[i+1], _x[i]) for i in range(3)]
    == [2, 2, sp.Rational(7, 4)], "その比は 2,2,1.75")
chk([term(5, -2, i) for i in range(1, 5)] == [5, -10, 20, -40],
    "5,-10,20,-40（r=-2）")
# 2, 6, 18, 50 は等比ではない
ne(sp.Rational(50, 18), 3, "2,6,18,50 は等比でない")
# 第 3 節（例題 2 とは別の数）
eq(sp.Rational(80, 10), 8, "u_5/u_2 = 8")
eq(sp.root(8, 3), 2, "r = 2")
eq(sp.Rational(10, 2), 5, "u_1 = 5")
eq(term(5, 2, 2), 10, "確かめ u_2 = 10")
eq(term(5, 2, 5), 80, "確かめ u_5 = 80")
in_text("$u_2 = 10$、$u_5 = 80$ とします", "第 3 節の数（例題 2 と別）")
# 偶数乗は 2 通り
chk(sp.solve(sp.Eq(_r ** 2, 9), _r) == [-3, 3], "r^2=9 の解は ±3")
chk(sp.solve(sp.Eq(_r ** 3, 8), _r)[0] == 2, "r^3=8 の実数解は 2 だけ")
# 第 6 節
eq(sum(4 * 3 ** (k - 1) for k in range(1, 6)), 484, "Σ4·3^(k-1), k=1..5 は 484")
chk([4 * 3 ** (k - 1) for k in range(1, 6)] == [4, 12, 36, 108, 324],
    "その項が合う")
eq(4 * (3 ** 5 - 1) / (3 - 1), 484, "公式でも 484")
eq(4 * 3 ** 1, 12, "Σ4·3^k なら u_1 = 12")
# 第 7 節（％ から r へ）
for pct, rr in [(10, "1.1"), (25, "1.25"), (-10, "0.9"), (-25, "0.75")]:
    eq(1 + sp.Rational(pct, 100), sp.Rational(rr), f"{pct}% は r={rr}")
# 第 8 節（5,10,20,40 は等比）
_seq = [5, 10, 20, 40]
chk([_seq[i + 1] - _seq[i] for i in range(3)] == [5, 10, 20], "差はそろわない")
chk([sp.Rational(_seq[i + 1], _seq[i]) for i in range(3)] == [2, 2, 2],
    "比はそろう")

# ══════════════════════════════════════════════════════════
# 2. 例題 1
# ══════════════════════════════════════════════════════════
eq(term(3, 2, 8), 384, "例題1(a) u_8 = 384")
eq(2 ** 7, 128, "2^7 = 128")
chk([term(3, 2, i) for i in range(1, 9)]
    == [3, 6, 12, 24, 48, 96, 192, 384], "書き出しでも 384")
eq(3 * 2 ** 8, 768, "指数を 8 とした誤答は 768")
eq(term(3, 2, 9), 768, "それは 9 番目の値")
ne(768, 384, "誤答は書き出しと合わない")
eq(sp.solve(sp.Eq(3 * 2 ** (_n - 1), 1536), _n)[0], 10, "例題1(c) n = 10")
eq(2 ** 9, 512, "2^9 = 512")
eq(term(3, 2, 10), 1536, "第 10 項は 1536")
eq(sp.Rational(1000, 3), sp.Rational(1000, 3), "1000/3")
chk(not sp.Rational(1000, 3).is_Integer, "1000/3 は整数でない")
chk(1000 % 3 != 0, "1000 は 3 の倍数でない")
chk(all(term(3, 2, i) % 3 == 0 for i in range(1, 12)), "どの項も 3 の倍数")

# ══════════════════════════════════════════════════════════
# 3. 例題 2
# ══════════════════════════════════════════════════════════
eq(sp.Rational(96, 12), 8, "例題2(a) r^3 = 8")
eq(sp.Rational(12, 2), 6, "例題2(b) u_1 = 6")
eq(term(6, 2, 2), 12, "確かめ u_2（使った項なので必ず合う）")
eq(term(6, 2, 5), 96, "確かめ u_5（使わなかった項）")
eq(term(6, 2, 10), 3072, "例題2(c) u_10 = 3072")
eq(2 ** 9, 512, "2^9 = 512")
eq(6 * (2 ** 10 - 1) / (2 - 1), 6138, "例題2(d) S_10 = 6138")
eq(brute_sum(6, 2, 10), 6138, "足し上げでも 6138")
eq(6 * 1023, 6138, "6×1023")
eq(6 * (1 - 2 ** 10) / (1 - 2), 6138, "もう 1 つの形でも 6138")
# 指数を r^4 と取りちがえた誤答は u_5 が合わない
_rbad = sp.root(8, 4)
ne(term(12 / _rbad, _rbad, 5), 96, "r^4=8 とすると u_5 が合わない")

# ══════════════════════════════════════════════════════════
# 4. 例題 3
# ══════════════════════════════════════════════════════════
eq(3 ** 6, 729, "3^6 = 729")
eq(5 * (3 ** 6 - 1) / (3 - 1), 1820, "例題3(a) S_6 = 1820")
eq(brute_sum(5, 3, 6), 1820, "足し上げでも 1820")
chk([term(5, 3, i) for i in range(1, 7)] == [5, 15, 45, 135, 405, 1215],
    "その項が合う")
eq(5 * 364, 1820, "5×364")
eq(sp.Rational(6, 2), 3, "例題3(b) r = 3")
eq(sp.solve(sp.Eq(2 * 3 ** (_n - 1), 486), _n)[0], 6, "n = 6")
eq(3 ** 5, 243, "3^5 = 243")
eq(term(2, 3, 6), 486, "u_6 = 486（逆向きの確かめ）")
eq(term(2, 3, 5), 162, "u_5 = 162")
eq(term(2, 3, 7), 1458, "u_7 = 1458")
eq(2 * (3 ** 6 - 1) / (3 - 1), 728, "例題3(b) S_6 = 728")
eq(sum(2 ** k for k in range(1, 7)), 126, "例題3(c) Σ2^k = 126")
eq(2 * (2 ** 6 - 1) / (2 - 1), 126, "公式でも 126")
eq(1 * (2 ** 6 - 1) / (2 - 1), 63, "u_1 を 1 と取りちがえると 63")
eq(sp.Rational(126, 63), 2, "それはちょうど半分")
eq(brute_sum(7, 1, 5), 5 * 7, "r=1 の和は n u_1")

# ══════════════════════════════════════════════════════════
# 5. 例題 4（感染の広がり）
# ══════════════════════════════════════════════════════════
eq(term(4, 3, 6), 972, "例題4(a) u_6 = 972")
chk([term(4, 3, i) for i in range(1, 7)] == [4, 12, 36, 108, 324, 972],
    "表の値が合う")
eq(4 * 3 ** 6, 2916, "指数を 6 とした誤答は 2916")
eq(term(4, 3, 7), 2916, "それは 7 日目の値")
eq(4 * (3 ** 6 - 1) / (3 - 1), 1456, "例題4(b) S_6 = 1456")
eq(brute_sum(4, 3, 6), 1456, "足し上げでも 1456")
chk(972 < 1456 < 2 * 972, "合計は最後の項と、その 2 倍のあいだ")
_d15 = 4 * 3 ** 14
chk(sp.Integer(19000000) < _d15 < sp.Integer(20000000),
    f"15 日目はおよそ 1900 万: {_d15}")
in_text("$1900$ 万件の新規感染", "その桁を本文に書いている")
in_text("$4$ 件の新規感染が記録されました", "新規感染としてそろえた（レビュー1）")
not_in_text("$4$ 人が感染しています", "累積と読める書き方を直した（レビュー1）")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(term(2, 5, 6), 6250, "演習1(a) u_6 = 6250")
eq(5 ** 5, 3125, "5^5 = 3125")
chk([term(2, 5, i) for i in range(1, 7)] == [2, 10, 50, 250, 1250, 6250],
    "書き出しでも 6250")
eq(2 * 5 ** 6, 31250, "指数を 6 とした誤答")
eq(term(2, 5, 7), 31250, "それは 7 番目")
eq((2 * 5 ** (_n - 1)).subs(_n, 1), 2, "n=1 で u_1 = 2")
eq((2 * 5 ** _n).subs(_n, 1), 10, "誤った式は n=1 で 10")

eq(sp.Rational(27, 81), sp.Rational(1, 3), "演習2(a) r = 1/3")
chk(sp.Rational(9, 27) == sp.Rational(1, 3)
    and sp.Rational(3, 9) == sp.Rational(1, 3), "比が全部そろう")
eq(term(81, sp.Rational(1, 3), 7), sp.Rational(1, 9), "演習2(b) u_7 = 1/9")
eq(sp.Rational(1, 3) ** 6, sp.Rational(1, 729), "(1/3)^6 = 1/729")
chk([term(81, sp.Rational(1, 3), i) for i in range(1, 8)]
    == [81, 27, 9, 3, 1, sp.Rational(1, 3), sp.Rational(1, 9)],
    "書き出しでも 1/9")

# 演習 3：r が 2 通りになる（指数が偶数）
eq(sp.Rational(24, 6), 4, "演習3 r^2 = 4")
chk(sorted(sp.solve(sp.Eq(_r ** 2, 4), _r)) == [-2, 2], "r = ±2")
eq(sp.Rational(6, 2), 3, "r=2 なら u_1 = 3")
eq(sp.Rational(6, -2), -3, "r=-2 なら u_1 = -3")
chk([term(3, 2, i) for i in range(1, 5)] == [3, 6, 12, 24], "r=2 の数列")
chk([term(-3, -2, i) for i in range(1, 5)] == [-3, 6, -12, 24], "r=-2 の数列")
for _rr, _uu in [(2, 3), (-2, -3)]:
    eq(term(_uu, _rr, 2), 6, f"u_2 = 6（r={_rr}）")
    eq(term(_uu, _rr, 4), 24, f"u_4 = 24（r={_rr}）")
ne(term(3, 2, 3), term(-3, -2, 3), "u_3 は符号がちがう（12 と -12）")
in_text("**指数が偶数なので、$r$ は $2$ 通りあります。**", "±を書かせている（レビュー14）")

eq(4 * (2 ** 7 - 1) / (2 - 1), 508, "演習4 S_7 = 508")
eq(brute_sum(4, 2, 7), 508, "足し上げでも 508")
eq(2 ** 7, 128, "2^7 = 128")
chk(508 < 2 * 256, "合計は最後の項の 2 倍より小さい")

eq(sp.Rational(12, 3), 4, "演習5 r = 4")
eq(sp.solve(sp.Eq(3 * 4 ** (_n - 1), 3072), _n)[0], 6, "n = 6")
eq(4 ** 5, 1024, "4^5 = 1024")
eq(term(3, 4, 6), 3072, "u_6 = 3072（逆向き）")
eq(3 * (4 ** 6 - 1) / (4 - 1), 4095, "演習5 S_6 = 4095")
eq(4 ** 6 - 1, 4095, "約分すると 4^6 - 1")
eq(brute_sum(3, 4, 6), 4095, "足し上げでも 4095")

eq(sum(2 * 3 ** (k - 1) for k in range(1, 8)), 2186, "演習6 = 2186")
eq(3 ** 7, 2187, "3^7 = 2187")
eq(2 * (3 ** 7 - 1) / (3 - 1), 2186, "公式でも 2186")
chk([2 * 3 ** (k - 1) for k in range(1, 8)]
    == [2, 6, 18, 54, 162, 486, 1458], "全部並べると本文の値")
eq(sum([2, 6, 18, 54, 162, 486, 1458]), 2186, "足すと 2186")
# 古い検算（はじめの 4 項）は、u_1 の読みちがいを両側に通してしまう
eq(sum(6 * 3 ** (k - 1) for k in range(1, 5)), 240, "誤った u_1=6 なら 240")
eq(6 * (3 ** 4 - 1) / (3 - 1), 240, "その公式でも 240（一致してしまう）")
not_in_text("$2 + 6 + 18 + 54 = 80$", "捕まえられない検算だった（レビュー2）")
eq(6 * (3 ** 7 - 1) / (3 - 1), 6558, "u_1 を 6 とした誤答は 6558")
eq(sp.Rational(6558, 2186), 3, "それは 3 倍")

eq(term(64, sp.Rational(1, 2), 8), sp.Rational(1, 2), "演習7(a) u_8 = 1/2")
eq(64 * (1 - sp.Rational(1, 2) ** 8) / (1 - sp.Rational(1, 2)),
   sp.Rational(255, 2), "演習7(b) S_8 = 127.5")
eq(brute_sum(64, sp.Rational(1, 2), 8), sp.Rational(255, 2), "足し上げでも 127.5")
eq(64 * (sp.Rational(1, 2) ** 8 - 1) / (sp.Rational(1, 2) - 1),
   sp.Rational(255, 2), "上の形でも 127.5")
eq(128 * sp.Rational(255, 256), sp.Rational(255, 2), "128×255/256")

eq(sp.Rational("1.1") ** 2, sp.Rational("1.21"), "1.1^2 = 1.21")
eq(sp.Rational("1.1") ** 4, sp.Rational("1.4641"), "1.1^4 = 1.4641")
eq(30000 * sp.Rational("1.1") ** 4, 43923, "演習8(a) 43923")
eq(30000 * sp.Rational("1.1"), 33000, "2 年目 33000")
eq(30000 * sp.Rational("1.1") ** 2, 36300, "3 年目 36300")
eq(30000 * sp.Rational("1.1") ** 3, 39930, "4 年目 39930")
chk(36300 <= 39000 < 39930, "境目は 4 年目")
eq(39930 * sp.Rational("1.1"), 43923, "1 年ずつ掛けても 43923")

eq(sp.Rational(3, 4) ** 3, sp.Rational(27, 64), "(3/4)^3 = 27/64")
eq(20000 * sp.Rational(27, 64), sp.Rational("8437.5"), "演習9(a) 8437.5")
chk([20000 * sp.Rational(3, 4) ** i for i in range(4)]
    == [20000, 15000, 11250, sp.Rational("8437.5")], "1 年ずつでも 8437.5")
eq(20000 * sp.Rational(1, 64), sp.Rational("312.5"), "r を 1/4 とした誤答")
ne(sp.Rational("312.5"), sp.Rational("8437.5"), "その誤答は 1 年ずつと合わない")
chk(all(20000 * sp.Rational(3, 4) ** i > 0 for i in range(1, 60)),
    "どの年も値は正（0 にならない）")

eq(term(7, 2, 4), 56, "演習10 正しい u_4 = 56")
eq(7 * 2 ** 4, 112, "生徒の答えは 112")
eq(term(7, 2, 5), 112, "それは 5 番目")
eq(7 * 2 ** 1, 14, "生徒の方法だと n=1 で 14（u_1=7 と合わない）")
chk([term(7, 2, i) for i in range(1, 5)] == [7, 14, 28, 56], "書き出しでも 56")
not_in_text("$u_5$ for the geometric sequence with $u_1 = 3$",
            "本文で答えが見えていた問題を差し替えた（レビュー7）")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.3** の欄に、`The nth term of a geometric sequence` として印刷",
        "公式集にあると書いている")
in_text("`The sum of n terms of a finite geometric sequence`", "和の欄の見出し")
in_text("$r \\neq 1$ という条件まで込みで", "条件も印刷されている")
in_text("覚える必要はありません", "公式集にあるものを暗記させていない")
in_text("**$u_1 > 0$ で $r \\geq 2$ の等比数列では", "半分の主張に条件を付けた（レビュー8）")
chk(sum(term(-1, 2, k) for k in range(1, 4)) == -7, "u_1<0 の反例：S_3 = -7")
chk(term(-1, 2, 3) < sp.Rational(-7, 2), "そのとき最後の項は半分より小さい")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("**the spread of disease**", "場面の紹介")
in_text("**population growth**", "場面の紹介 2")
not_in_text("シラバスは、例として", "Guidance の引用として書かない（レビュー3）")
in_text("**電卓で数列や和を出したときも、$u_1$ と $r$ が何かを答案に書いてください。**",
        "技術を使っても u_1 と r を書く（Guidance）")

# ══════════════════════════════════════════════════════════
# 8. GDC
# ══════════════════════════════════════════════════════════
in_text("menu → List & Spreadsheet → Sequence", "seq( の場所")
in_text("3^(n-1)", "指数はかっこで囲む")
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")

# ══════════════════════════════════════════════════════════
# 9. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6,
    "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 5, "model-answer が 5")
chk(len(re.findall(r"^::: \{#exm-aasl13-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(m) for m in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 9)), f"The idea が 1..8 で連番: {_idea}")
chk(TEXT.count("**検算") >= 14, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT,
    "検算の見出しに「確かめ。」を使っていない")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
for _blk in re.findall(r"\$\$(.*?)\$\$", TEXT, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式の中に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", TEXT):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式の中に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body),
        "model-answer に日本語: " + _body[:40])
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a in _anchors or _a in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl13", "他ページの @-ref を使っている: " + _r0)
for _f in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f[0] + _f[1]) if _f[0] else \
        os.path.join(BASE, _f[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f[1])
_head = TEXT[:TEXT.index("## The idea")]
chk("シラバスが、この項目に求めていること" not in _head, "冒頭にシラバスを置いていない")
chk("公式集の" not in _head, "冒頭に公式集のブロックを置いていない")

# ══════════════════════════════════════════════════════════
# 10. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-3-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-3-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("4 multiplications, not 5", "図(a) の要点")
in_fig("the middle terms cancel", "図(b) の要点")
for leak in ["6250", "4095", "2186", "508", "127.5", "43923", "8437.5",
             "1/9", "56", "112"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-3.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-2.qmd") < DRAFT.index("aasl-1-3.qmd"), "並びが 1.2 → 1.3")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("[SL 1.3 — Geometric sequences and series]"
    "(01-number-and-algebra/aasl-1-3.qmd)" in IDX, "index の一覧にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_m = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_m is not None and int(_m.group(1)) == len(_written), "「いまのところ N」が合う")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| geometric sequence |", "| common ratio |", "| population growth |",
          "| spread of disease |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ── 公比を割り算で求める条件（★2026-09-07 の修正）────────
in_text("**この割り算を使うときは、分母になる項が $0$ でないことが必要です。**",
        "割る項は 0 でない")
in_text("このページでは、比を求めるときに割る項は $0$ でないものとして扱います。", "同上")
in_text("### 3. 項が $2$ つ分かれば、$r$ と $u_1$ を求められる {#two-terms}",
        "見出しから断定を外した")
not_in_text("### 3. 項が $2$ つ分かれば、数列が決まる", "古い見出しは残っていない")
in_text("**ここでも割り算を使うので、分母になる項が $0$ でないことが要ります。**",
        "第 3 節でも条件を書いた")
in_text("$u_2 = 0$ なら $\\dfrac{u_5}{u_2}$ が書けません。", "0 のときの例")
# 指数が偶数なら r は 2 通り、という説明は残す
in_text("## 指数が偶数のときは、$r$ が $2$ 通りになります", "±r の説明は残す")
in_text("問題文に「すべての項が正」などの断りがあれば、そこで $1$ つに絞ります。",
        "問題文で絞ることも残す")
# 採点の言い方
in_text("**$r = 2$ だけを答えていたら、得点が半分になることがあります。**", "断定を弱めた")
not_in_text("点を半分落とします", "古い言い方は残っていない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
