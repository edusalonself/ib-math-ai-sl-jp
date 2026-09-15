"""AA SL 4.1（標本の取り方・かたより・外れ値）の内容を検算する。

    python3 figs/aa-sl/check_aasl_4_1.py
"""
import glob
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability")
QMD = os.path.join(BASE, "aasl-4-1.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_4_1.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.nsimplify(u) - sp.nsimplify(v)) == 0,
        msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 道具 — 四分位数と外れ値の境目（IB の手計算のやり方）
# ══════════════════════════════════════════════════════════
def med(a):
    a = sorted(a)
    m = len(a)
    return F(a[m // 2]) if m % 2 else (F(a[m // 2 - 1]) + F(a[m // 2])) / 2


def quartiles(d):
    """中央値を除いて下半分・上半分に分ける、IB の手計算のやり方。"""
    d = sorted(d)
    n = len(d)
    lo = d[:n // 2]
    hi = d[n // 2 + 1:] if n % 2 else d[n // 2:]
    return med(lo), med(d), med(hi)


def fences(d):
    q1, _m, q3 = quartiles(d)
    iqr = q3 - q1
    return q1 - F(3, 2) * iqr, q3 + F(3, 2) * iqr


def outliers(d):
    lo, hi = fences(d)
    return [x for x in sorted(d) if x < lo or x > hi]


# 道具そのものの検算
chk(med([1, 2, 3]) == 2, "道具: 奇数個の中央値")
chk(med([1, 2, 3, 4]) == F(5, 2), "道具: 偶数個の中央値")
chk(quartiles([1, 2, 3, 4, 5]) == (F(3, 2), 3, F(9, 2)), "道具: n=5")
chk(quartiles([1, 2, 3, 4]) == (F(3, 2), F(5, 2), F(7, 2)), "道具: n=4")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
# 層別の式
_N, _Ni, _n = sp.symbols("N N_i n", positive=True)
eq(sp.simplify(_n * _Ni / _N / _n), _Ni / _N, "層別は全体と同じ割合")
in_text("n \\times \\frac{N_i}{N}", "層別の式")
in_text("**この式は公式集にありません。**", "層別の式は公式集にない")
# 5 つの取り方が表にある
for _m in ["simple random", "convenience", "systematic", "quota", "stratified"]:
    chk(("| " + _m + " |") in TEXT, "表に取り方がある: " + _m)
in_text("{#tbl-aasl41-methods}", "表のラベル")
chk(TEXT.count("@tbl-aasl41-methods") >= 4, "表を本文から参照している")
# 外れ値の定義と境目
in_text("Q_1 - 1.5 \\times \\mathrm{IQR}", "下の境目")
in_text("Q_3 + 1.5 \\times \\mathrm{IQR}", "上の境目")
in_text("{#eq-aasl41-fences}", "境目のラベル")
in_text("{#eq-aasl41-strat}", "層別のラベル")
in_text("**平均からの距離ではありません。**", "平均は使わない")
in_text("境目そのものは outlier ではありません", "more than の意味")
in_text("$\\mathrm{IQR} = Q_3 - Q_1$", "IQR の定義")

# ══════════════════════════════════════════════════════════
# 2. Why it works — 1.5 倍の根拠
# ══════════════════════════════════════════════════════════
# 正規分布で Q3 は平均から何標準偏差か
_q = sp.sqrt(2) * sp.erfinv(R(1, 2))          # Phi^{-1}(0.75)
chk(abs(float(_q) - 0.6745) < 5e-5, f"Q3 は 0.6745σ: {float(_q)}")
_iqr = 2 * _q
chk(abs(float(_iqr) - 1.349) < 5e-4, f"IQR は 1.349σ: {float(_iqr)}")
_fence = _q + R(3, 2) * _iqr
chk(abs(float(_fence) - 2.698) < 5e-4, f"境目は 2.698σ: {float(_fence)}")
_tail = 2 * (1 - (1 + sp.erf(_fence / sp.sqrt(2))) / 2)
chk(abs(float(_tail) - 0.00698) < 5e-5, f"外に出る確率は約 0.7%: {float(_tail)}")
chk(abs(float(_tail) * 1000 - 7) < 0.1, "1000 個に 7 個くらい")
in_text("0.6745 + 1.5 \\times 1.349 = 2.698", "境目の計算")
eq(sp.Rational("0.6745") + R(3, 2) * sp.Rational("1.349"),
   sp.Rational("2.698"), "0.6745 + 1.5×1.349 = 2.698")
in_text("両側あわせて約 $0.7\\%$", "0.7%")
in_text("**$1000$ 個に $7$ 個くらい**", "1000 個に 7 個")
in_text("**$1.5$ は、そう決めてある約束です。**", "1.5 は約束")
in_text("## 参考：$1.5$ という数の出どころ", "C04: 数値はたたむ補足に移す")
in_text("ここから先は、標準偏差と normal distribution（正規分布）を"
        "学んだあとで読んでください。", "C04: 先に学ぶものを明示")
not_in_text("**$1.5$ は、こうして選ばれた約束です。**",
            "本文に数値の導出が残っていない")
# 平均・標準偏差だと外れ値自身に動かされる（実例で確かめる）
_base = [12, 15, 18, 20, 22, 25, 27, 30, 33, 38]
_with = _base + [75]
_m0 = sum(_base) / len(_base)
_m1 = sum(_with) / len(_with)
chk(_m1 > _m0, f"75 を入れると平均が上がる: {_m0} → {_m1}")


def sd(d):
    m = sum(d) / len(d)
    return (sum((x - m) ** 2 for x in d) / len(d)) ** 0.5


chk(sd(_with) > sd(_base), f"75 を入れると標準偏差が上がる: {sd(_base):.3f} → {sd(_with):.3f}")
chk(quartiles(_with)[0] == 18 and quartiles(_with)[2] == 33, "四分位数は 75 に動かされない")
# 75 を 7500 にしても四分位数は同じ
_huge = _base + [7500]
chk(quartiles(_huge)[0] == 18 and quartiles(_huge)[2] == 33,
    "7500 にしても四分位数は同じ")
in_text("いちばん大きい値が $75$ でも $7500$ でも、$Q_1$ と $Q_3$ は変わりません。",
        "順番だけで決まる")
in_text("**bias は、大きくしても小さくなりません。**", "bias は標本を大きくしても直らない")

# ══════════════════════════════════════════════════════════
# 3. 例題 1  convenience sampling
# ══════════════════════════════════════════════════════════
in_text("[Name the sampling method used.]{.q-en}", "例題1(c)")
in_text("*convenience sampling*", "例題1(c) の答え")
in_text("*continuous*", "例題1(b) の答え")
in_text("*all $750$ students in the school*", "例題1(a) の答え")

# ══════════════════════════════════════════════════════════
# 4. 例題 2  外れ値
# ══════════════════════════════════════════════════════════
D2 = [12, 15, 18, 20, 22, 25, 27, 30, 33, 38, 75]
chk(len(D2) == 11, "例題2 は 11 個")
chk(D2 == sorted(D2), "例題2 は小さい順に並んでいる")
_q1, _m2, _q3 = quartiles(D2)
eq(_m2, 25, "例題2 の中央値")
eq(_q1, 18, "例題2 の Q1")
eq(_q3, 33, "例題2 の Q3")
eq(_q3 - _q1, 15, "例題2 の IQR")
eq(F(3, 2) * 15, F(45, 2), "1.5×15 = 22.5")
_lo2, _hi2 = fences(D2)
eq(_hi2, F(111, 2), "例題2 の上の境目 55.5")
eq(_lo2, F(-9, 2), "例題2 の下の境目 -4.5")
chk(outliers(D2) == [75], f"例題2 の外れ値は 75 だけ: {outliers(D2)}")
chk(75 > _hi2, "75 > 55.5")
chk(38 < _hi2, "38 は外れ値ではない")
chk(min(D2) > _lo2, "小さいほうに外れ値はない")
# 定義そのもの（近いほうの四分位数からの距離）でも同じ結論になる
eq(75 - _q3, 42, "75 と Q3 の距離は 42")
chk(75 - _q3 > F(3, 2) * (_q3 - _q1), "42 > 22.5 なので外れ値")
chk((75 > _hi2) == (75 - _q3 > F(3, 2) * (_q3 - _q1)),
    "境目で見ても距離で見ても同じ結論")
chk(abs(75 - _q3) < abs(75 - _q1), "75 に近いのは Q3 のほう")
in_text("Q_3 + 22.5 = 33 + 22.5 = 55.5", "例題2(c) の境目")
in_text("$75 - 33 = 42$", "距離で見る検算")
# 四分位数の位置
chk(sorted(D2)[5] == 25, "6 番目が 25")
chk(sorted(D2)[2] == 18, "3 番目が 18")
chk(sorted(D2)[8] == 33, "9 番目が 33")
in_text("**中央値は $6$ 番目**", "6 番目")
chk(len([x for x in D2 if x < _q1]) == 2, "Q1 より下に 2 個")
chk(len([x for x in D2 if x > _q3]) == 2, "Q3 より上に 2 個")

# ══════════════════════════════════════════════════════════
# 5. 例題 3  ウェブ調査
# ══════════════════════════════════════════════════════════
in_text("[Suggest a sampling method that would reduce the bias, and describe "
        "how it would be carried out.]{.q-en}", "例題3(d)")
in_text("*simple random sampling: number all students on the school roll",
        "例題3(d) の答え")
in_text("**convenience sampling** です（@tbl-aasl41-methods）。学校が選んだのではなく、"
        "生徒が自分で選んでいます。", "例題3(b) の理由")

# ══════════════════════════════════════════════════════════
# 6. 例題 4  層別
# ══════════════════════════════════════════════════════════
TOT4, PARTS4, N4 = 750, [300, 250, 200], 60
chk(sum(PARTS4) == TOT4, "例題4 の内訳の合計")
_take4 = [F(N4 * p, TOT4) for p in PARTS4]
chk(_take4 == [24, 20, 16], f"例題4(a): {_take4}")
chk(sum(_take4) == N4, "例題4(a) の合計は 60")
eq(F(N4, TOT4), F(2, 25), "60/750 = 2/25")
eq(F(2, 25), sp.Rational("0.08"), "2/25 = 0.08")
for _t, _p in zip(_take4, PARTS4):
    eq(F(_t, _p), F(2, 25), f"どの群も 8%: {_t}/{_p}")
# 等分してしまった場合
eq(F(20, 200), F(1, 10), "等分だと Grade 11-12 は 10%")
chk(abs(float(F(20, 300)) - 0.0667) < 5e-4, "等分だと Grade 6-8 は約 6.7%")
in_text("$\\dfrac{20}{300} \\approx 6.7\\%$", "等分の反例")
in_text("\\frac{60}{750} = \\frac{2}{25} = 0.08 = 8\\%", "例題4(b)")
in_text("$24 + 20 + 16 = 60$", "例題4 の検算")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1  systematic、20000 個、200 個ごと
eq(F(20000, 200), 100, "演習1: 100 個が検査される")
in_text("$20\\,000 \\div 200 = 100$", "演習1 の検算")
in_text("*systematic sampling*", "演習1 の答え")
# 2  quota
in_text("*quota sampling*", "演習2 の答え")
in_text("*no*", "演習2 の答え（同じ確率ではない）")
# 3  systematic、600 人、10 人おき、4 番目から
eq(F(600, 10), 60, "演習3: 60 人")
chk(4 + 10 * 59 == 594, "最後は 594")
chk(594 <= 600 and 604 > 600, "次は名簿の外")
in_text("$594 = 4 + 10 \\times 59$", "演習3 の検算")
in_text("$$600 \\div 10 = 60$$", "演習3 の答え")
# 4  9 個の小包
D4 = [5, 7, 8, 8, 9, 11, 12, 14, 30]
chk(len(D4) == 9, "演習4 は 9 個")
_q1a, _m4, _q3a = quartiles(D4)
eq(_m4, 9, "演習4 の中央値")
eq(_q1a, F(15, 2), "演習4 の Q1 = 7.5")
eq(_q3a, 13, "演習4 の Q3 = 13")
eq(_q3a - _q1a, F(11, 2), "演習4 の IQR = 5.5")
eq(F(3, 2) * F(11, 2), F(33, 4), "1.5×5.5 = 8.25")
_lo4, _hi4 = fences(D4)
eq(_hi4, F(85, 4), "演習4 の上の境目 21.25")
eq(_lo4, F(-3, 4), "演習4 の下の境目 -0.75")
chk(outliers(D4) == [30], f"演習4 の外れ値は 30 だけ: {outliers(D4)}")
eq(F(7 + 8, 2), F(15, 2), "下半分の真ん中")
eq(F(12 + 14, 2), 13, "上半分の真ん中")
in_text("$$Q_1 = 7.5, \\quad Q_3 = 13, \\quad \\mathrm{IQR} = 5.5$$", "演習4 の答え")
in_text("$Q_1 - 8.25 = 7.5 - 8.25 = -0.75$", "演習4 の検算")
# 5  11 個の本
D5 = [1, 14, 15, 16, 18, 19, 20, 22, 24, 25, 44]
chk(len(D5) == 11, "演習5 は 11 個")
_q1b, _m5, _q3b = quartiles(D5)
eq(_m5, 19, "演習5 の中央値")
eq(_q1b, 15, "演習5 の Q1")
eq(_q3b, 24, "演習5 の Q3")
eq(_q3b - _q1b, 9, "演習5 の IQR")
_lo5, _hi5 = fences(D5)
eq(_lo5, F(3, 2), "演習5 の下の境目 1.5")
eq(_hi5, F(75, 2), "演習5 の上の境目 37.5")
chk(outliers(D5) == [1, 44], f"演習5 の外れ値は 1 と 44: {outliers(D5)}")
chk(14 > _lo5, "14 は外れ値ではない")
chk(25 < _hi5, "25 は外れ値ではない")
in_text("$$1 < 1.5 \\quad \\text{and} \\quad 44 > 37.5$$", "演習5 の判定")
in_text("*outliers: $1$ and $44$*", "演習5 の答え")
# 6  層別
TOT6, PARTS6, N6 = 1200, [480, 420, 300], 100
chk(sum(PARTS6) == TOT6, "演習6 の内訳の合計")
_take6 = [F(N6 * p, TOT6) for p in PARTS6]
chk(_take6 == [40, 35, 25], f"演習6: {_take6}")
chk(sum(_take6) == N6, "演習6 の合計は 100")
eq(F(N6, TOT6), F(1, 12), "100/1200 = 1/12")
for _t, _p in zip(_take6, PARTS6):
    eq(F(_t, _p), F(1, 12), f"どの群も 1/12: {_t}/{_p}")
in_text("$40 + 35 + 25 = 100$", "演習6 の検算")
in_text("$\\dfrac{40}{480} = \\dfrac{35}{420} = \\dfrac{25}{300} = \\dfrac{1}{12}$",
        "演習6 の割合")
# 9  平均±2σ と四分位数の規則がちがう答えを出す
MU9, SD9, Q1_9, Q3_9 = 40, 6, 34, 46
eq(Q3_9 - Q1_9, 12, "演習9 の IQR")
eq(F(3, 2) * 12, 18, "1.5×12 = 18")
eq(Q3_9 + 18, 64, "演習9 の上の境目 64")
chk(55 < 64, "55 は外れ値ではない")
eq(MU9 + 2 * SD9, 52, "平均 + 2σ = 52")
chk(55 > 52, "生徒の言い分では外れ値になる")
chk((55 > MU9 + 2 * SD9) != (55 > Q3_9 + F(3, 2) * (Q3_9 - Q1_9)),
    "2 つの規則は別の答えを出す")
in_text("$$Q_3 + 18 = 64, \\qquad 55 < 64$$", "演習9 の判定")
in_text("$40 + 2 \\times 6 = 52$", "演習9 の検算")
in_text("$55 - 46 = 9$", "距離で見る検算")
# 10  周期 25、歩幅 25
eq(F(600, 25), 24, "演習10: 24 人が選ばれる")
chk(24 * 25 == 600, "24 クラス × 25 人")
for _k in range(24):
    chk((1 + 25 * _k - 1) % 25 == 0, f"{1 + 25 * _k} 番目はクラスの 1 人目")
chk(1 + 25 == 26 and (26 - 1) % 25 == 0, "26 番目は 2 クラス目の 1 人目")
chk(1 + 50 == 51, "51 番目は 3 クラス目の 1 人目")
# 歩幅を 24 にするとずれる
_pos = sorted(set(((1 + 24 * _k - 1) % 25) for _k in range(24)))
chk(len(_pos) > 1, f"歩幅 24 ならクラス内の位置がずれる: {len(_pos)} 通り")
chk(len(set(((1 + 25 * _k - 1) % 25) for _k in range(24))) == 1,
    "歩幅 25 だと位置が 1 通りしかない")
in_text("$600 \\div 25 = 24$ 人が選ばれ、クラス数と同じです", "演習10 の検算")
in_text("**$25$ ではなく $24$ 人おきにすると**", "歩幅を変える検算")

# ══════════════════════════════════════════════════════════
# 8. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _leak, _m in [
        ("55.5", "例題2(c)"),
        ("21.25", "演習4"),
        ("37.5", "演習5"),
        ("= 24, \\qquad", "例題4(a)"),
        ("40 + 35 + 25", "演習6"),
        ("$8\\%$", "例題4(b)"),
        ("convenience sampling** です", "例題1(c)"),
        ("quota sampling", "演習2"),
        ("systematic sampling", "演習1・3"),
]:
    not_in_body(_leak, _m)

# ══════════════════════════════════════════════════════════
# 9. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk(TEXT.count("callout-important") == 1, "公式集の callout は 1 つ（IQR）")
in_text("$\\mathrm{IQR} = Q_3 - Q_1$ は、公式集の **4.2** の欄にあります。",
        "IQR は公式集の 4.2")
in_text("**$1.5 \\times \\mathrm{IQR}$ の規則のほうは、公式集にありません。**",
        "1.5 の規則は公式集にない")
_quotes = [l for l in TEXT.splitlines() if l.startswith("> ")]
chk(len(_quotes) == 1, f"シラバスの引用は 1 行だけ: {_quotes}")
chk(_quotes[0] == "> At SL the data set will be considered to be the population "
    "unless otherwise stated.", "引用は population の約束だけ")
not_in_text("Outlier is defined as a data item", "外れ値の定義は逐語で貼らない")
not_in_text("Sampling techniques and their effectiveness", "Content 欄は引用しない")
not_in_text("Reliability of data sources", "Content 欄は引用しない")

# ══════════════════════════════════════════════════════════
# 10. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("答案では、**どの向きにずれるかまで書きます。**", "向きまで書く")
in_text("**どちらかは、数字だけでは決められません。**", "場面で決める")
in_text("**記録の誤り** … 打ちまちがい、単位ちがい、機械の故障。", "記録の誤り")
in_text("**本物の値** …", "本物の値")

# ══════════════════════════════════════════════════════════
# 11. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "4.1 には GDC の節を置かない")
in_text("menu → Statistics → Stat Calculations → One-Variable Statistics",
        "One-Variable Statistics")
in_text("ctrl + doc → Add Lists & Spreadsheet", "リストの作り方")
in_text("`Q1X` と `Q3X`", "結果の読み方")
in_text("**手で出した四分位数と、電卓の値がちがうことがあります。**", "手と電卓のちがい")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 12. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 9,
    f"model-answer が 9: {TEXT.count('{.model-answer}')}")
_asks = len(re.findall(r"\[(?:[^\]]*?)(?:Explain|Justify|Comment|Interpret|Identify"
                       r"|Describe|Suggest)(?:[^\]]*?)\]\{\.q-en\}", TEXT))
chk(_asks == 9, f"説明を求める問いが 9: {_asks}")
chk(len(re.findall(r"^::: \{#exm-aasl41-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl41", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl41-idea") >= 2, "図を本文から 2 か所以上参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-4-1-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-4-1-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Population and sample", "図(a) の題")
in_fig("population: everyone we want to know about", "図(a) の population")
in_fig("measure the sample", "図(a) の矢印")
in_fig("say something about the population", "図(a) の矢印の先")
in_fig("if the sample is chosen badly", "図(a) の説明")
in_fig("(b) The two outlier boundaries", "図(b) の題")
in_fig("$Q_1 - 1.5\\\\,IQR$", "図(b) の下の境目")
in_fig("$Q_3 + 1.5\\\\,IQR$", "図(b) の上の境目")
in_fig("marked with", "図(b) の × の説明")
in_fig("a value beyond a boundary is an outlier; the ", "図(b) の説明")
# 図に例題・演習の数値が出ていないこと
for _bad in ["55.5", "21.25", "37.5", "75", "44", "30"]:
    chk(_bad not in FIGSTR, "図に答えの数値: " + _bad)
# 図の × が本当に境目の外にあること
_m = re.search(r"Q1, Q3 = ([0-9.]+), ([0-9.]+)", FIGCODE)
chk(_m is not None, "図の Q1, Q3 が読める")
_fq1, _fq3 = float(_m.group(1)), float(_m.group(2))
_fhi = _fq3 + 1.5 * (_fq3 - _fq1)
_mx = re.search(r"ax2\.plot\(\[([0-9.]+)\], \[1\.6\], marker=\"x\"", FIGCODE)
chk(_mx is not None, "図の × の位置が読める")
chk(float(_mx.group(1)) > _fhi,
    f"図の × は上の境目より外: {_mx.group(1)} vs {_fhi}")
in_text("(a) A sample is a part of the population", "キャプションが (a) を説明")
in_text("(b) The two boundaries used to decide whether a value is an outlier",
        "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 14. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/04-statistics-and-probability/aasl-4-1.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-8.qmd") < DRAFT.index("aasl-4-1.qmd"), "並びが 3.8 → 4.1")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aasl-4-1.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| population |", "| sample |", "| outlier |", "| bias |",
           "| stratified sampling |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 例題1 の答え (a)(b)(d) が本文に出ていた ----------------------------
in_text("町の $4000$ 世帯で「$1$ か月の電気の使用量」を知りたいなら、population は "
        "$4000$ 世帯です。", "§1 の例は電気の使用量")
not_in_text("$750$ 人の学校で「生徒の通学時間」を知りたいなら", "§1 の古い例は消した")
in_text("「牛乳パックの中身の量」は測るので continuous", "§2 の例は牛乳パック")
not_in_text("「通学時間」は測るので continuous", "§2 の古い例は消した")
not_in_text("「通学時間は $25$ 分」と書いてあっても", "§2 の古い注意は消した")
in_text("スーパーの入口で買い物客に「週に何回この店に来ますか」と聞けば、",
        "§5 の例はスーパー")
not_in_text("学校の門で早く来た生徒だけに通学時間を聞けば", "§5 の古い例は消した")
in_text("「よく来る人ほど声をかけられやすいので、平均は**多めに**出る」まで書きます。",
        "§5 の書き方の例もスーパー")
not_in_body("all $750$ students", "例題1(a) の答えは本文に出さない")
not_in_body("正門", "例題1 の場面は本文に出さない")
not_in_body("早く来た生徒", "例題1(d) の答えは本文に出さない")

# --- convenience の定義が、自分から応じた標本を外していた ----------------
in_text("| convenience | 手近な人を選ぶ／自分から応じた人が入る |", "表の convenience")
in_text("誰が標本に入るかが、**たまたま手近にいたか、自分から応じたか**で決まり、",
        "§4 の理由")
not_in_text("どちらも「誰が選ばれるか」を人が決めているので、選ぶ人のくせが",
            "古い理由は消した")

# --- 四分位数の手計算のやり方を本文に書いた -----------------------------
in_text("**中央値を境に下半分と上半分に分けます**", "分け方")
in_text("**中央値そのものはどちらにも入れません**", "奇数のときの約束")
in_text("**このページの例題と演習は、この方法で答えを出しています。**", "どちらの方法か明示")
in_text("（[第 6 節](#outlier)の手順 $1$）", "演習4 の参照先")
# 2 つのやり方で四分位数がちがうことを、実際に確かめる
def _q_incl(d):
    d = sorted(d); k = len(d)
    lo = d[:(k + 1) // 2]
    hi = d[k // 2:]
    return med(lo), med(hi)
for _d, _want in [(D2, (18, 33)), (D4, (F(15, 2), 13)), (D5, (15, 24))]:
    _a = quartiles(_d)
    chk((_a[0], _a[2]) == _want, f"除く方法: {(_a[0], _a[2])} vs {_want}")
chk(_q_incl(D2) != (18, 33), f"含める方法だと値がちがう: {_q_incl(D2)}")
chk(_q_incl(D4) != (F(15, 2), 13), f"演習4 も方法で変わる: {_q_incl(D4)}")
chk(_q_incl(D5) != (15, 24), f"演習5 も方法で変わる: {_q_incl(D5)}")
# ただし外れ値の判定はどちらの方法でも変わらない（ページの主張が壊れないこと）
def _out_incl(d):
    q1, q3 = _q_incl(d); iqr = q3 - q1
    return [x for x in sorted(d) if x < q1 - F(3, 2) * iqr or x > q3 + F(3, 2) * iqr]
for _d in (D2, D4, D5):
    chk(_out_incl(_d) == outliers(_d),
        f"外れ値はどちらの方法でも同じ: {_out_incl(_d)} vs {outliers(_d)}")

# --- 第 7 節が演習8 の答えを逆向きに出していた --------------------------
in_text("**その値がどうやって記録されたか**で決まります。", "記録のされ方で決まる")
not_in_text("「$0$ 分は記入もれと考えられるので外す」", "演習8 の答えは本文に出さない")
not_in_body("$0$ 分", "演習8 の場面は本文に出さない")

# --- 「必ず短く」は 1 つの標本については偽 ------------------------------
in_text("くり返すと population の平均より"
        "**平均として多めに出ます**", "M06: くり返したときの平均でずれる")
in_text("$1$ 回ごとには低めに出ることもありますが、"
        "**くり返したときの中心がずれています**", "M06: 1 回ごとは逆もある")
not_in_text("**必ず短く**なります", "「必ず」は消した")
not_in_text("population の平均より**いつも多めに出ます**",
            "M06: 「いつも」が消えている")
in_text("bias というのは、**同じやり方をくり返したときに、平均として一方向へ"
        "ずれる傾向**のことです。", "M06: bias の定義")
not_in_text("**同じやり方をくり返しても、いつも同じ向きにずれる**",
            "M06: 旧定義が消えている")
in_text("**simple random と stratified は、bias を小さくするしくみを"
        "もっています。**", "M06: 無作為でも保証ではない")
in_text("sampling variability（標本による偶然のばらつき）",
        "M06: 用語の初出（英語が先）")
not_in_text("**convenience と quota は信頼できません。**",
            "M06: 断定が消えている")

# --- C05: 四分位数は「絶対に変わらない」ではない ----------------------
in_text("$Q_1$ と $Q_3$ は、**並べたときの位置で決まります**。例題 $2$ の "
        "$11$ 個のデータなら", "C05: 例題に結び付けた")
in_text("**一般には、平均や標準偏差より、極端な値の影響を受けにくい**",
        "C05: 一般の言い方")
not_in_text("$Q_1$ と $Q_3$ は、**順番だけで決まります**",
            "C05: 旧断定が消えている")

# --- C07: かたよりの向きを問題文だけで断定しない ----------------------
in_text("and state what extra information would be needed to say in "
        "which direction the estimate is biased.", "C07: 例題1(d) の英語")
in_text("かたよりの向きを言うにはどんな情報が必要かを述べなさい。",
        "C07: 例題1(d) の訳")
in_text("**向きは、この問題文だけでは決まりません。**", "C07: 解説")
in_text("*only early arrivals are sampled and late arrivals are never "
        "sampled", "C07: 解答例")
not_in_text("students arriving first live closer, so their travel times "
            "are shorter and the mean is underestimated",
            "C07: 断定した解答例が消えている")
not_in_text("The students who arrive first are more likely to be those "
            "who live close to the school.",
            "C07: 断定した model answer が消えている")
not_in_text("短いほうにかたよる、で合っています。",
            "C07: 断定した検算が消えている")

# --- 1.5 の説明が直前の導出と矛盾していた -------------------------------
in_text("$1.5$ でなければならない理由はありません。$1.4$ でも $1.6$ でも、"
        "同じような線が引けます。", "1.4 でも 1.6 でも")
not_in_text("$1.5$ という数に深い理由はありません", "古い言い方は消した")

# --- 例題2 の 3 つ目の検算が、区別できない規則を発明していた -------------
in_text("**検算（(c) について、別の測り方）。** **近いほうの四分位数からの距離で見ます。**",
        "例題2 の 3 つ目の検算")
not_in_text("range で計算したらどうなるか見ます", "range の検算は消した")
not_in_text("$127.5$", "発明した規則の値は消した")

# --- 例題3(d) の model answer が乱数を N 個作らせていた ------------------
in_text("use technology to generate $120$ different random numbers between $1$ and $N$",
        "例題3(d) は 120 個")
not_in_text("generate that many different random numbers", "古い言い方は消した")
in_text("$1$ から $N$ までの異なる乱数を $120$ 個作り", "日本語の説明も 120 個")
chk(120 < 750, "標本は母集団より小さい")

# --- 演習6 で stratified を見分けさせる ---------------------------------
in_text("Name the sampling method, and show how the three numbers were obtained.",
        "演習6 は方法を見分けさせる")
not_in_text("A stratified sample of $100$ members is to be taken", "古い演習6 は消した")
in_text("*stratified sampling*", "演習6 の答え")
in_text("**quota と見分けてください。**", "quota との区別")
# 5 つの取り方が、どれも「名前を答えさせる問い」で 1 回は出てくること
for _nm in ["simple random", "convenience", "systematic", "quota", "stratified"]:
    chk(TEXT.count(_nm) >= 2, "取り方が本文と問いの両方に出る: " + _nm)

# --- 演習9 の 2 つ目の検算が循環していた --------------------------------
in_text("**検算（規則）。** **近いほうの四分位数からの距離で見ます。** $55$ に近いのは "
        "$Q_3 = 46$ で、$55 - 46 = 9$ です。", "演習9 の 2 つ目の検算")
not_in_text("$64 > 55 > 52$ なので、$2$ つの規則は**別の答えを出します**", "循環した検算は消した")
eq(55 - 46, 9, "55 - 46 = 9")
chk(9 < 18, "9 < 1.5×IQR = 18 なので外れ値ではない")
chk(abs(55 - 46) < abs(55 - 34), "55 に近いのは Q3")

# --- 演習10 の 2 つ目の検算が、歩幅 24 を言いすぎていた ------------------
in_text("クラス内の位置は $1$ 番目、$25$ 番目、$24$ 番目、$23$ 番目、… と "
        "$1$ つずつずれていきます", "歩幅 24 のときの位置")
_p24 = [((1 + 24 * _k - 1) % 25) + 1 for _k in range(4)]
chk(_p24 == [1, 25, 24, 23], f"歩幅 24 の位置は 1, 25, 24, 23: {_p24}")
chk(len([_k for _k in range(100) if 1 + 24 * _k <= 600]) == 25,
    "歩幅 24 だと 25 人選ばれる")
not_in_text("クラス内の位置が $1$ つずつずれていきます ✓ 周期と歩幅が一致している"
            "ことが原因です。", "古い言い方は消した")

# --- 図 (a) の標本を散らばらせた ----------------------------------------
in_fig("sample: spread over the whole population", "図(a) の標本のラベル")
in_fig("rng.choice(len(_pts), 13, replace=False)", "標本は無作為に散らす")
chk("Ellipse" not in FIGCODE, "かたまりの楕円は消した")
chk("_pts[i][0] - 6.4" not in FIGCODE, "位置で選ぶ書き方は消した")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
