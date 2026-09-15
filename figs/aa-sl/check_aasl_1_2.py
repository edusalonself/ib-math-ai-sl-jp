"""AA SL 1.2（arithmetic sequences and series）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_2.py

方針は他のページのチェッカーと同じです。

  * 数値は sympy で第一原理から出し直す（本文の式を写さない）
  * 「こう間違えたら、こうなる」と書いた検算は、実際にその
    間違いをして、本当に別の値になることを確かめる
  * レビューで直した箇所には not_in_text の見張りを置く
  * 構成の不変量（★AA 版：`##` は 5 つ・例題 4・演習 10）を数える
  * 登録先（_quarto-draft.yml、aa-sl/index.qmd、glossary-aa.qmd）を見る
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-2.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_2.py"), encoding="utf-8").read()
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


def term(u1, d, n):
    """第 n 項。定義（d を n-1 回足す）から。"""
    return sp.nsimplify(u1) + (n - 1) * sp.nsimplify(d)


def brute_sum(u1, d, n):
    """はじめの n 項の和を、1 つずつ足して出す（公式を使わない）。"""
    return sum(term(u1, d, k) for k in range(1, n + 1))


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの（記号のまま）
# ══════════════════════════════════════════════════════════
_u1, _d, _n = sp.symbols("u1 d n")
_un = _u1 + (_n - 1) * _d
# 2 つの和の形が、記号のまま一致する
eq(sp.expand(_n / 2 * (2 * _u1 + (_n - 1) * _d) - _n / 2 * (_u1 + _un)), 0,
   "S_n の 2 つの形は同じ式")
# n = 1 を入れると u_1 に戻る（Common errors の確かめ方）
eq(_un.subs(_n, 1), _u1, "n=1 で u_1 に戻る")
ne((_u1 + _n * _d).subs(_n, 1), _u1, "u_1 + n d は n=1 で u_1 にならない（誤り）")
# u_q - u_p = (q-p) d
_p, _q = sp.symbols("p q")
eq(sp.expand((_u1 + (_q - 1) * _d) - (_u1 + (_p - 1) * _d) - (_q - _p) * _d), 0,
   "u_q - u_p = (q-p)d")
# 和の公式が、1 つずつ足した値と一致する（いくつかの n で）
for _u, _dd, _nn in [(5, 3, 5), (3, 5, 20), (7, 4, 12), (100, -7, 15),
                     (25, -2, 12), (4, 6, 30)]:
    eq(sp.Rational(_nn, 2) * (2 * _u + (_nn - 1) * _dd),
       brute_sum(_u, _dd, _nn), f"公式と足し上げが一致: u1={_u}, d={_dd}, n={_nn}")
# sigma 記法：ak+b は等差で、差は a
_a, _b, _k = sp.symbols("a b k")
eq(sp.expand((_a * (_k + 1) + _b) - (_a * _k + _b)), _a,
   "ak+b の差は a（k によらない）")

# ══════════════════════════════════════════════════════════
# 1. The idea の中の数
# ══════════════════════════════════════════════════════════
eq(term(5, 3, 5), 17, "5,8,11,14,17 の第 5 項")
eq(brute_sum(5, 3, 5), 55, "その 5 項の和は 55")
eq(sp.Rational(5, 2) * (5 + 17), 55, "公式でも 55")
chk([term(5, 3, i) for i in range(1, 6)] == [5, 8, 11, 14, 17],
    "はじめの 5 項が本文と合う")
chk([term(20, -3, i) for i in range(1, 5)] == [20, 17, 14, 11],
    "d が負の例（20,17,14,11）")
# 2, 5, 8, 13 は等差ではない
chk((5 - 2) != (13 - 8), "2,5,8,13 は等差でない（差が 3 と 5）")
# 2 項から決める（第 3 節。例題 2 とは別の数）
eq((41 - 11) / sp.Integer(5), 6, "u_7-u_2 = 5d から d = 6")
eq(11 - 6, 5, "u_1 = 5")
eq(term(5, 6, 2), 11, "確かめ: u_2 = 11")
eq(term(5, 6, 7), 41, "確かめ: u_7 = 41")
in_text("$u_2 = 11$、$u_7 = 41$ とします", "第 3 節の数（例題 2 と別）")
not_in_text("$u_3 = 17$、$u_8 = 42$ とします", "例題 2 と同じ数を本文で出していない")
# 個数の数え方（第 5 節。演習 5 とは別の数）
eq(sp.solve(sp.Eq(6 + (_n - 1) * 7, 202), _n)[0], 29, "6,13,...,202 は 29 項")
eq((202 - 6) / sp.Integer(7), 28, "間隔は 28 個")
not_in_text("`Find the sum of` $7 + 11 + 15", "演習 5 と同じ和を本文で解いていない")
# sigma
eq(sum(4 * k + 1 for k in range(1, 6)), 65, "Σ(4k+1), k=1..5 は 65")
eq(sp.Rational(5, 2) * (5 + 21), 65, "公式でも 65")
eq(20 - 3 + 1, 18, "k=3..20 は 18 項")
ne(20 - 3, 18, "20-3 は 18 ではない")
# 単利（第 7 節。例題 4 とは別の数）
eq(1500 * sp.Rational(6, 100), 90, "単利は年 90")
chk([1500 + 90 * y for y in range(4)] == [1500, 1590, 1680, 1770],
    "単利の表が合う")
not_in_text("元金 $2000$ 円、年利 $4\\%$", "例題 4 と同じ数を本文で出していない")
# ぴったり等差でないデータ
_h = [sp.Rational(str(x)) for x in ["12.1", "17.8", "23.6", "29.4", "35.2"]]
_diffs = [_h[i + 1] - _h[i] for i in range(4)]
chk([str(sp.nsimplify(x)) for x in _diffs]
    == ["57/10", "29/5", "29/5", "29/5"], f"差は 5.7, 5.8, 5.8, 5.8: {_diffs}")
eq((_h[-1] - _h[0]) / 4, sp.Rational("5.775"), "平均の差は 5.775")
chk(len(_h) - 1 == 4, "間隔は 4 つ")
in_text("= 5.775", "その値を本文に書いている")

# ══════════════════════════════════════════════════════════
# 2. 例題 1
# ══════════════════════════════════════════════════════════
eq(term(7, 4, 20), 83, "例題1(a) u_20 = 83")
eq(sp.expand(7 + (_n - 1) * 4), 4 * _n + 3, "例題1(b) u_n = 4n+3")
eq((4 * _n + 3).subs(_n, 20), 83, "(b) の式でも 83")
eq(sp.solve(sp.Eq(4 * _n + 3, 403), _n)[0], 100, "例題1(c) 403 は第 100 項")
eq(term(7, 4, 100), 403, "第 100 項は 403")
eq(sp.solve(sp.Eq(4 * _n + 3, 400), _n)[0], sp.Rational("99.25"),
   "例題1(d) 400 なら n = 99.25")
chk(not sp.Rational("99.25").is_Integer, "99.25 は整数でない")
eq(7 + 20 * 4, 87, "n を取りちがえた誤答は 87")
ne(87, 83, "その誤答は正しい式からは出ない")
# ★ (n-1)→n を思いこむと (b) の式も 7+4n になり、n=20 では一致してしまう
eq((7 + 4 * _n).subs(_n, 20), 87, "誤った式でも n=20 なら 87（一致してしまう）")
eq((4 * _n + 3).subs(_n, 1), 7, "n=1 なら正しい式は u_1 = 7")
eq((7 + 4 * _n).subs(_n, 1), 11, "誤った式は n=1 で 11（ここで捕まる）")
in_text("**$n = 1$ は、$(n-1)$ の誤りだけを狙い撃ちにする検算です。**",
        "n=1 の検算を書いている（レビュー B-2）")
not_in_text("これは別の形の式なので、$(n-1)$ を $n$ と取りちがえた誤りを捕まえます",
            "捕まえられない主張だった（レビュー B-2）")
eq(400 % 4, 0, "400 は 4 の倍数")
eq(403 % 4, 3, "403 は 4 で割ると 3 余る（どの項も同じ）")

# ══════════════════════════════════════════════════════════
# 3. 例題 2
# ══════════════════════════════════════════════════════════
eq(term(7, 5, 50), 252, "例題2(c) u_50 = 252")
eq(sp.Rational(50, 2) * (7 + 252), 6475, "例題2(d) S_50 = 6475")
eq(sp.Rational(50, 2) * (2 * 7 + 49 * 5), 6475, "もう 1 つの形でも 6475")
eq(brute_sum(7, 5, 50), 6475, "1 つずつ足しても 6475")
eq(25 * 259, 6475, "25×259 の計算")
# 間隔を 6 と取りちがえた誤答：u_3 は合ってしまい、u_8 が合わない
_db = sp.Rational(42 - 17, 6)
_u1b = 17 - 2 * _db
eq(_db, sp.Rational(25, 6), "誤った d = 25/6")
eq(_u1b, sp.Rational(26, 3), "そのときの u_1 = 26/3")
eq(term(_u1b, _db, 3), 17, "u_3 のほうは 17 に戻ってしまう")
eq(term(_u1b, _db, 8), sp.Rational(227, 6), "u_8 は 227/6")
ne(term(_u1b, _db, 8), 42, "u_8 が 42 にならない（検算が効く）")
in_text("$u_3$ のほうは $17$ に戻ってしまいます", "その事実を本文に書いている（レビュー A-2）")
not_in_text("$u_8$ が合いません。", "誤りだった説明（レビュー A-2）")

# ══════════════════════════════════════════════════════════
# 4. 例題 3
# ══════════════════════════════════════════════════════════
eq(sp.Rational(20, 2) * (2 * 3 + 19 * 5), 1010, "例題3(a) S_20 = 1010")
eq(brute_sum(3, 5, 20), 1010, "足し上げでも 1010")
eq(term(3, 5, 20), 98, "u_20 = 98")
eq(sp.Rational(20, 2) * (3 + 98), 1010, "右の形でも 1010")
eq(sp.Rational(31, 2) * (3 + 153), 2418, "例題3(b) S_31 = 2418")
eq(brute_sum(3, 5, 31), 2418, "足し上げでも 2418")
eq(31 * 78, 2418, "31×78")
eq(sp.Rational(30, 2) * (3 + 153), 2340, "n=30 とした誤答は 2340")
eq(2418 - 2340, 78, "その差は、最初と最後の平均 78")
eq(sp.Rational(3 + 153, 2), 78, "平均は 78")
eq(term(3, 5, 31), 153, "u_31 = 153（逆向きの確かめ）")
eq(term(3, 5, 30), 148, "u_30 = 148")
eq(term(3, 5, 32), 158, "u_32 = 158")
eq(31 * 3 + 5 * sum(range(31)), 2418, "公式を使わない足し上げでも 2418")
eq(sum(range(31)), 465, "0+1+...+30 = 465")
in_text("最初と最後の平均 $78$ だけ足りません", "平均だと書いている（レビュー A-3）")
not_in_text("$78$（$1$ 項ぶん）足りません", "1 項ぶんという誤り（レビュー A-3）")
eq(sum(4 * k - 1 for k in range(1, 26)), 1275, "例題3(c) Σ(4k-1) = 1275")
eq(4 * 1 - 1, 3, "その第 1 項は 3")
eq(4 * 25 - 1, 99, "第 25 項は 99")
eq(sp.Rational(25, 2) * (3 + 99), 1275, "公式でも 1275")
eq(25 * 51, 1275, "25×51")
eq(sum(4 * k - 1 for k in range(1, 5)), 36, "はじめの 4 項の和は 36")
eq(sp.Rational(4, 2) * (3 + 15), 36, "公式でも 36")
eq(sp.Rational(25, 2) * (2 * 3 + 24 * 4), 1275, "左の形でも 1275（u_25 を使わない）")
in_text("$u_{25} = 99$ を使っていないので", "答えを検算していると書いている（レビュー B-6）")

# ══════════════════════════════════════════════════════════
# 5. 例題 4（単利）
# ══════════════════════════════════════════════════════════
eq(2000 + 5 * 80, 2400, "例題4(b) 5 年後は 2400")
chk([2000 + 80 * y for y in range(6)]
    == [2000, 2080, 2160, 2240, 2320, 2400], "1 年ずつ追っても 2400")
_sol = sp.solve(sp.Eq(2000 + 80 * _n, 3000), _n)[0]
eq(_sol, sp.Rational("12.5"), "例題4(c) 境目は 12.5 年")
eq(2000 + 80 * 12, 2960, "12 年では 2960")
eq(2000 + 80 * 13, 3040, "13 年で 3040")
chk(2960 <= 3000 < 3040, "境目の両側で判定できる")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(term(5, 3, 12), 38, "演習1(a) u_12 = 38")
eq(sp.expand(5 + (_n - 1) * 3), 3 * _n + 2, "演習1(b) u_n = 3n+2")
eq((3 * _n + 2).subs(_n, 12), 38, "式でも 38")
eq((3 * _n + 2).subs(_n, 1), 5, "n=1 で u_1")
eq(5 + 12 * 3, 41, "誤答 41")
ne(41, 38, "誤答は式と合わない")
eq(5 + 1 * 3, 8, "その方法だと n=1 で 8 になる（u_1 と合わない）")

eq(9 - 2, 7, "演習2(a) d = 7")
chk((16 - 9) == 7 and (23 - 16) == 7, "差は 2 か所以上そろっている")
eq(term(2, 7, 15), 100, "演習2(b) u_15 = 100")
eq(sp.expand(2 + (_n - 1) * 7), 7 * _n - 5, "u_n = 7n-5")
eq((7 * _n - 5).subs(_n, 15), 100, "式でも 100")
eq(2 + 15 * 7, 107, "誤答 107")
eq((2 + 7 * _n).subs(_n, 15), 107, "誤った式でも n=15 なら 107（一致してしまう）")
eq((7 * _n - 5).subs(_n, 1), 2, "正しい式は n=1 で 2")
eq((2 + 7 * _n).subs(_n, 1), 9, "誤った式は n=1 で 9（ここで捕まる）")
in_text("**$n = 1$ を先に入れるのが要です。**", "n=1 を先に入れる（レビュー B-3）")

eq(sp.Rational(45 - 20, 5), 5, "演習3 d = 5")
eq(20 - 3 * 5, 5, "演習3 u_1 = 5")
eq(term(5, 5, 4), 20, "確かめ u_4")
eq(term(5, 5, 9), 45, "確かめ u_9")
_dbad3 = sp.Rational(45 - 20, 6)   # 間隔を 6 と取りちがえたときの d
_u1bad3 = 20 - 3 * _dbad3          # u_4 から逆算した u_1
eq(_u1bad3, sp.Rational("7.5"), "そのときの u_1 = 7.5")
eq(term(_u1bad3, _dbad3, 4), 20, "その u_1 なら u_4 は合ってしまう")
eq(term(_u1bad3, _dbad3, 9), sp.Rational(245, 6), "u_9 は 245/6 = 40.83…")
ne(term(_u1bad3, _dbad3, 9), 45, "u_9 が 45 にならない（検算が効く）")
in_text("$u_4$ のほうは $20$ に戻ってしまいます", "その事実を書いている（レビュー A-1）")

eq(sp.Rational(30, 2) * (2 * 4 + 29 * 6), 2730, "演習4 S_30 = 2730")
eq(brute_sum(4, 6, 30), 2730, "足し上げでも 2730")
eq(term(4, 6, 30), 178, "u_30 = 178")
eq(sp.Rational(30, 2) * (4 + 178), 2730, "右の形でも 2730")
eq(4 + 30 * 6, 184, "29 を 30 と取りちがえた誤答 184")
# ★ その誤りは 2 つの形の両方に入るので、見くらべでは捕まらない
eq(sp.Rational(30, 2) * (2 * 4 + 30 * 6), 2820, "左の形でも 2820")
eq(sp.Rational(30, 2) * (4 + 184), 2820, "右の形でも 2820（一致してしまう）")
eq((4 + 6 * _n).subs(_n, 1), 10, "n=1 なら誤った式は 10（u_1=4 と合わない）")
in_text("**これでは捕まりません。**", "捕まらないと書いている（レビュー B-1）")

eq(sp.solve(sp.Eq(7 + (_n - 1) * 4, 147), _n)[0], 36, "演習5 n = 36")
eq(sp.Rational(36, 2) * (7 + 147), 2772, "演習5 S = 2772")
eq(brute_sum(7, 4, 36), 2772, "足し上げでも 2772")
eq(sp.Rational(7 + 147, 2), 77, "平均は 77")
eq(77 * 36, 2772, "平均×個数でも 2772")
eq(sp.Rational(35, 2) * 154, 2695, "n=35 とした誤答は 2695")
eq(2772 - 2695, 77, "その差は、最初と最後の平均 77")
eq(term(7, 4, 36), 147, "u_36 = 147（逆向きの確かめ）")
eq(term(7, 4, 35), 143, "u_35 = 143")
eq(term(7, 4, 37), 151, "u_37 = 151")
eq(36 * 7 + 4 * sum(range(36)), 2772, "公式を使わない足し上げでも 2772")
eq(sum(range(36)), 630, "0+1+...+35 = 630")
chk(77 % 4 != 3, "77 はこの数列の項ではない（4 で割って 3 余らない）")

eq(sum(3 * k + 2 for k in range(4, 21)), 646, "演習6 = 646（k=4..20）")
eq(20 - 4 + 1, 17, "項数は 17")
eq(3 * 4 + 2, 14, "第 1 項 14")
eq(3 * 20 + 2, 62, "最後の項 62")
eq(sp.Rational(17, 2) * (14 + 62), 646, "公式でも 646")
eq(17 * 38, 646, "17×38")
eq(sum(3 * k + 2 for k in range(1, 21)), 670, "k=1..20 なら 670")
eq(sum(3 * k + 2 for k in range(1, 4)), 24, "はじめの 3 項は 24")
eq(670 - 24, 646, "引き算でも 646（別の道すじ）")
eq(sp.Rational(16, 2) * (14 + 62), 608, "n を 16 と数えると 8×76 = 608")
ne(608, 646, "そこで食いちがう（検算が効く）")

eq(sp.Rational(15, 2) * (2 * 100 + 14 * (-7)), 765, "演習7(a) S_15 = 765")
eq(brute_sum(100, -7, 15), 765, "足し上げでも 765")
eq(term(100, -7, 15), 2, "u_15 = 2")
eq(sp.Rational(15, 2) * (100 + 2), 765, "右の形でも 765")
_negsol = sp.solve(sp.Eq(100 - 7 * (_n - 1), 0), _n)[0]
chk(sp.Rational("15.2") < _negsol < sp.Rational("15.3"),
    f"はじめて負になるのは n>15.28…: {float(_negsol)}")
eq(term(100, -7, 16), -5, "演習7(b) u_16 = -5")
chk(term(100, -7, 15) > 0, "u_15 はまだ正")
chk(term(100, -7, 16) < 0, "u_16 は負")

# 演習 8：ろうそく（ぴったり等差でないデータ）
_c = [sp.Rational(str(x)) for x in ["18.6", "15.1", "11.7", "8.1", "4.6"]]
_cd = [_c[i + 1] - _c[i] for i in range(4)]
chk([str(x) for x in _cd] == ["-7/2", "-17/5", "-18/5", "-7/2"],
    f"差は -3.5, -3.4, -3.6, -3.5: {_cd}")
chk(len(set(_cd)) > 1, "差はそろっていない（等差でない）")
eq((_c[-1] - _c[0]) / 4, sp.Rational("-3.5"), "見積もった d は -3.5")
# 差の平均は、最初と最後から出したものと必ず同じ（別の道すじにならない）
eq(sum(_cd) / 4, (_c[-1] - _c[0]) / 4, "差の平均は同じ値になる（検算にならない）")
_recon = [_c[0] + sp.Rational("-3.5") * i for i in range(5)]
chk([str(x) for x in _recon] == ["93/5", "151/10", "58/5", "81/10", "23/5"],
    f"作り直すと 18.6, 15.1, 11.6, 8.1, 4.6: {_recon}")
_gaps = [abs(_recon[i] - _c[i]) for i in range(5)]
eq(max(_gaps), sp.Rational("0.1"), "実測とのずれは最大 0.1 cm")
eq(_c[-1] + sp.Rational("-3.5"), sp.Rational("1.1"), "6 時間目の予測は 1.1 cm")
eq(_c[-1] + 5 * sp.Rational("-3.5"), sp.Rational("-12.9"), "10 時間目は -12.9 cm")
chk(_c[-1] + 5 * sp.Rational("-3.5") < 0, "負になるので使えない")
in_text("**なお、$4$ つの差の平均を取るのは、別の道すじではありません。**",
        "平均は検算にならないと書いている")

eq(sp.Rational(12, 2) * (2 * 25 + 11 * (-2)), 168, "演習9(a) 168")
eq(brute_sum(25, -2, 12), 168, "足し上げでも 168")
eq(term(25, -2, 12), 3, "いちばん上の段は 3 本")
eq(sp.Rational(12, 2) * (25 + 3), 168, "右の形でも 168")
chk(12 * 3 <= 168 <= 12 * 25, "36 と 300 のあいだ（挟み込み）")
eq(sp.expand(25 - 2 * (_n - 1)), 27 - 2 * _n, "u_n = 27-2n")
eq((27 - 2 * _n).subs(_n, 14), -1, "演習9(b) 14 段目は -1 本")
eq((27 - 2 * _n).subs(_n, 13), 1, "13 段目は 1 本")
chk((27 - 2 * 13) > 0 and (27 - 2 * 14) < 0, "13 段が限界")

eq(term(6, 4, 10), 42, "演習10 正しい u_10 = 42")
eq(6 + 10 * 4, 46, "生徒の答えは 46")
eq(term(6, 4, 11), 46, "それは第 11 項")
eq(6 + 1 * 4, 10, "生徒の方法だと n=1 で 10（u_1 と合わない）")
chk([term(6, 4, i) for i in range(1, 11)]
    == [6, 10, 14, 18, 22, 26, 30, 34, 38, 42], "書き出しても 42")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.2** の欄に、`The nth term of an arithmetic sequence` として印刷",
        "公式集にあると書いている（1.2 の欄）")
in_text("`The sum of n terms of an arithmetic sequence`", "和の欄の見出し")
in_text("覚える必要はありません", "公式集にあるものを暗記させていない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("> Students will need to approximate common differences.",
        "Guidance の一文（近似）を引用ブロックで")

# ══════════════════════════════════════════════════════════
# 8. GDC（AI SL で検証済みの事実と合っているか）
# ══════════════════════════════════════════════════════════
in_text("menu → List & Spreadsheet → Sequence", "seq( の場所")
in_text("seq(5 + (n-1)*3, n, 1, 20)", "seq の例")
in_text("Press-to-Test（試験モード）でも $\\sum$ は使えます", "Σ は試験モードで使える")
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
    "--- は 6 本（front matter 2 + 例題 4）")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 6, "model-answer が 6")
chk(len(re.findall(r"^::: \{#exm-aasl12-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
_sections = [h for h in _h2 if h in _want]
chk(_sections and _sections[-1] == "Exercises", "Exercises で終わる")
_idea = [int(m) for m in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 9)), f"The idea が 1..8 で連番: {_idea}")
chk(TEXT.count("**検算") >= 14, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT,
    "検算の見出しに「確かめ。」を使っていない")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
for _blk in re.findall(r"\$\$(.*?)\$\$", TEXT, re.S):
    chk("✓" not in _blk and "✗" not in _blk,
        "表示数式の中に ✓/✗ がある: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", TEXT):
    chk("✓" not in _blk and "✗" not in _blk,
        "インライン数式の中に ✓/✗ がある: " + _blk[:40])
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body),
        "model-answer に日本語が混ざっている: " + _body[:40])
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a in _anchors or _a in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a)
for _r in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r == "aasl12", "他ページの @-ref を使っている: " + _r)
for _f in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f[0] + _f[1]) if _f[0] else \
        os.path.join(BASE, _f[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f[1])
# 冒頭は What you should be able to do だけ
_head = TEXT[:TEXT.index("## The idea")]
chk("シラバスが、この項目に求めていること" not in _head, "冒頭にシラバスを置いていない")
chk("公式集の" not in _head, "冒頭に公式集のブロックを置いていない")

# ══════════════════════════════════════════════════════════
# 10. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-2-idea.svg")
chk(os.path.exists(SVG), "図がある: aasl-1-2-idea.svg")
chk("](img/aasl-1-2-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("4 jumps, not 5", "図(a) の要点")
in_fig("every pair makes", "図(b) の要点")
# 図が演習の答えを載せていないか
for leak in ["38", "100", "2730", "2772", "670", "765", "4200", "168", "42",
             "3n + 2", "7n - 5"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-2.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("aasl-1-1.qmd") < DRAFT.index("aasl-1-2.qmd"),
    "サイドバーの並びが 1.1 → 1.2")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用の _quarto.yml は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("[SL 1.2 — Arithmetic sequences and series]"
    "(01-number-and-algebra/aasl-1-2.qmd)" in IDX, "index の一覧にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written),
    f"✅ の数 {len(_ticked)} と、書けたページ数 {len(_written)} が合う")
_m = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_m is not None and int(_m.group(1)) == len(_written),
    "index の「いまのところ N ページ」が合う")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| sequence |", "| term |", "| arithmetic sequence |",
          "| common difference |", "| series |", "| sigma notation |",
          "| first term |", "| simple interest |"]:
    chk(t in GLO, "対訳表にある: " + t)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
