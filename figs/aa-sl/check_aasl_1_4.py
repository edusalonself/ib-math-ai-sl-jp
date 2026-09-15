"""AA SL 1.4（financial applications）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_4.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-4.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_4.py"), encoding="utf-8").read()
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
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def FV(pv, r, k, n):
    """公式集の式から。r はパーセントの数字。"""
    return _S(pv) * (1 + sp.Rational(r, 100 * k)) ** (k * n)


def step(pv, factor, times):
    """1 期ずつ掛けた値の列（公式を使わない道すじ）。"""
    out, x = [], _S(pv)
    for _ in range(times):
        x = x * _S(factor)
        out.append(x)
    return out


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの
# ══════════════════════════════════════════════════════════
_pv, _r, _k, _n = sp.symbols("PV r k n", positive=True)
# k=1 なら (1+r/100)^n
eq(sp.simplify((_pv * (1 + _r / (100 * 1)) ** (1 * _n))
               - _pv * (1 + _r / 100) ** _n), 0, "k=1 のときの形")
# depreciation は r を負にしたもの
eq((1 + sp.Rational(-25, 100 * 1)), sp.Rational(3, 4), "r=-25 なら 0.75 倍")
eq((1 + sp.Rational(-20, 100)), sp.Rational(4, 5), "r=-20 なら 0.8 倍")
# real value：利率とインフレ率が同じなら PV に戻る
_f = sp.symbols("f", positive=True)
eq(sp.simplify(_pv * (1 + _f / 100) ** _n / (1 + _f / 100) ** _n - _pv), 0,
   "利率=インフレ率なら real value は PV")
# 割り戻しの指数は kn ではなく n（k=2 だと打ち消し合わない）
chk(sp.simplify(FV(1000, 20, 2, 2) / (1 + sp.Rational(20, 100)) ** 2 - 1000) != 0,
    "k=2 なら real value は PV に戻らない")
# 1 期ずつ掛けるのと、公式が一致する
for _pv0, _rr, _kk, _nn in [(2000, 10, 1, 3), (4000, 20, 2, 2),
                            (5000, 20, 1, 2), (2000, 20, 2, 2),
                            (1000, 20, 4, 1)]:
    eq(FV(_pv0, _rr, _kk, _nn),
       step(_pv0, 1 + sp.Rational(_rr, 100 * _kk), _kk * _nn)[-1],
       f"公式と 1 期ずつが一致: PV={_pv0}, r={_rr}, k={_kk}, n={_nn}")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
chk(step(1000, "1.1", 3) == [1100, 1210, 1331], "複利の表 1100,1210,1331")
eq(sp.Rational("1.1") ** 3, sp.Rational("1.331"), "1.1^3 = 1.331")
for k, word in [(1, "yearly"), (2, "half-yearly"), (4, "quarterly"),
                (12, "monthly")]:
    in_text(f"| {word} |", "k の表に " + word)
eq(sp.Rational(10, 100 * 1), sp.Rational("0.1"), "r=10, k=1 で 0.1")
# real value の例（2500, 20%, 2 年）
eq(FV(2500, 20, 1, 2), 3600, "2500×1.2^2 = 3600")
eq(3600 / sp.Rational("1.2") ** 2, 2500, "インフレ 20% で割ると 2500")
# 本文 第 7 節：何年で超えるか（1500, 10%）── 演習 8 とは別の数にした
eq(FV(1500, 10, 1, 2), 1815, "n=2 で 1815")
eq(FV(1500, 10, 1, 3), sp.Rational("1996.5"), "n=3 で 1996.50")
eq(FV(1500, 10, 1, 4), sp.Rational("2196.15"), "n=4 で 2196.15")
chk(FV(1500, 10, 1, 3) < 2000 < FV(1500, 10, 1, 4), "境目は 4 年目")
eq(sp.Rational("1.1") ** 2, sp.Rational("1.21"), "1.1^2 = 1.21")
eq(sp.Rational("1.21") * sp.Rational("1.1"), sp.Rational("1.331"),
   "1.21 に 1.1 を掛けると 1.331")
eq(sp.Rational("1.331") * sp.Rational("1.1"), sp.Rational("1.4641"),
   "1.331 に 1.1 を掛けると 1.4641")
in_text("$\\$1500$ が年 $10\\%$ で、いつ $\\$2000$ を超えるか",
        "第 7 節は 1500 と 10%")
not_in_text("$\\$2000$ が年 $20\\%$ で、いつ $\\$4000$ を超えるか",
            "第 7 節が演習 8 と同じ数のままになっていない")
# Why it works の 3 つ（800, 12%）── 演習 9 とは別の数にした
eq(FV(800, 12, 1, 1), 896, "k=1 で 896")
eq(FV(800, 12, 2, 1), sp.Rational("898.88"), "k=2 で 898.88")
_w4 = FV(800, 12, 4, 1)
chk(abs(float(_w4) - 900.407048) < 1e-6, f"k=4 で 900.4070…: {float(_w4)}")
in_text("900.4070\\ldots", "k=4 の値は 900.4070…")
not_in_text("900.4145", "誤った 900.4145 は残っていない")
chk(FV(800, 12, 1, 1) < FV(800, 12, 2, 1) < _w4, "k が大きいほど FV も大きい")
chk(_w4 - FV(800, 12, 1, 1) < 5, "増え方はごくわずか")
not_in_text("$\\$1000$、年 $20\\%$、$1$ 年で見ると",
            "Why it works が演習 9 と同じ数のままになっていない")
# 「はじめの 1 年は同じ」は k=1 のときだけ
in_text("**年 $1$ 回の複利（$k = 1$）なら、はじめの $1$ 年はまったく同じ**",
        "k=1 の条件を書いている")
not_in_text("**はじめの $1$ 年は、まったく同じ**です。", "無条件の言い切りは消した")
chk(FV(1000, 20, 2, 1) != 1000 + 1000 * sp.Rational(20, 100),
    "k=2 なら 1 年目から単利と差がつく")

# ══════════════════════════════════════════════════════════
# 2. 例題 1
# ══════════════════════════════════════════════════════════
eq(FV(2000, 10, 1, 3), 2662, "例題1(a) 2662")
chk(step(2000, "1.1", 3) == [2200, 2420, 2662], "1 年ずつでも 2662")
eq(2662 - 2000, 662, "例題1(b) 利息 662")
eq(2000 * sp.Rational("0.1") * 3, 600, "例題1(c) 単利 600")
eq(2000 * sp.Rational("1.1") ** 2, 2420, "1.1^2 と取りちがえたら 2420")
ne(2420, 2662, "その誤答は 1 年ずつと合わない")
not_in_text("指数を $1.1^{4}$ と取りちがえていたら $2928.20$",
            "例題 1 が演習 3 の答えを漏らしていない")
eq(2200 * sp.Rational("0.1"), 220, "2 年目の利息 220")
eq(2420 * sp.Rational("0.1"), 242, "3 年目の利息 242")
eq(200 + 220 + 242, 662, "利息を足しても 662")
eq((220 - 200) + (242 - 200), 62, "単利との差だけ足すと 62")
eq(662 - 600, 62, "その差は 62")

# ══════════════════════════════════════════════════════════
# 3. 例題 2
# ══════════════════════════════════════════════════════════
eq(FV(4000, 20, 1, 2), 5760, "例題2(a) 5760")
eq(FV(4000, 20, 2, 2), sp.Rational("5856.4"), "例題2(b) 5856.40")
eq(sp.Rational("1.1") ** 4, sp.Rational("1.4641"), "1.1^4 = 1.4641")
chk(step(4000, "1.1", 4) == [4400, 4840, 5324, sp.Rational("5856.4")],
    "半年ごとに追っても 5856.40")
eq(4000 * sp.Rational("1.1") ** 2, 4840, "分母だけ直した誤答 4840")
eq(4000 * sp.Rational("1.2") ** 4, sp.Rational("8294.4"), "指数だけ直した誤答 8294.40")
eq(sp.Rational("5856.4") - 5760, sp.Rational("96.4"), "差は 96.40")
chk(sp.Rational("96.4") / 5760 < sp.Rational(2, 100), "差は 5760 の 2% 足らず")

# ══════════════════════════════════════════════════════════
# 4. 例題 3（depreciation）
# ══════════════════════════════════════════════════════════
eq(sp.Rational(3, 4) ** 3, sp.Rational(27, 64), "(3/4)^3 = 27/64")
eq(12000 * sp.Rational(27, 64), sp.Rational("5062.5"), "例題3(a) 5062.50")
chk(step(12000, "0.75", 3) == [9000, 6750, sp.Rational("5062.5")],
    "1 年ずつでも 5062.50")
chk(sp.Rational("5062.5") < 6000, "例題3(b) 半分より安い")
eq(12000 * sp.Rational("0.75") ** 4, sp.Rational("3796.875"), "4 年後 3796.875")
chk(sp.Rational("5062.5") > 4000 > sp.Rational("3796.875"), "境目は 4 年目")
# (c) の検算は「1 年ずつ」ではなく累乗から（循環しない道すじ）
eq(sp.Rational("0.75") ** 4, sp.Rational(81, 256), "0.75^4 = 81/256")
eq(12000 * sp.Rational(81, 256), sp.Rational(972000, 256), "12000×81/256 = 972000/256")
eq(sp.Rational(972000, 256), sp.Rational("3796.875"), "972000/256 = 3796.875")
in_text("12\\,000 \\times (0.75)^{4} = 12\\,000 \\times \\frac{81}{256}",
        "(c) の検算が累乗から")
not_in_text("**検算（(c) について）。** 境目の両側を出しました。",
            "循環していた検算は消した")
# 金額は小数第 2 位まで
in_text("$3796.88$（正確には $3796.875$）", "表は 3796.88 と書く")
chk(float(sp.Rational("3796.875").evalf()) == 3796.875, "3796.875 は割り切れる")
chk(step(12000, "0.25", 3) == [3000, 750, sp.Rational("187.5")],
    "0.25 を掛けた誤答の列")

# ══════════════════════════════════════════════════════════
# 5. 例題 4（real value）
# ══════════════════════════════════════════════════════════
eq(FV(10000, 10, 1, 2), 12100, "例題4(a) 12100")
eq(12100 / sp.Rational("1.21"), 10000, "例題4(b) real value 10000")
eq(sp.Rational("1.1") ** 2, sp.Rational("1.21"), "1.1^2 = 1.21")
# 反例（利率とインフレ率がちがう場合）
eq(FV(8000, 10, 1, 2), 9680, "8000 の FV は 9680")
eq(sp.Rational("1.05") ** 2, sp.Rational("1.1025"), "1.05^2 = 1.1025")
_real = sp.Rational(9680) / sp.Rational("1.1025")
chk(abs(float(_real) - 8780.045) < 0.01, f"real value は 8780.04…: {float(_real)}")
eq(8000 * sp.Rational("1.1025"), 8820, "差の 5% で計算すると 8820")
chk(38 < float(8820 - _real) < 41, "そのずれは 40 ほど")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(FV(2500, 8, 1, 2), 2916, "演習1 2916")
chk(step(2500, "1.08", 2) == [2700, 2916], "1 年ずつでも 2916")
eq(sp.Rational("1.08") ** 2, sp.Rational("1.1664"), "1.08^2 = 1.1664")
eq(2500 * sp.Rational("1.16"), 2900, "1.16 とした誤答 2900")
ne(2900, 2916, "その誤答は合わない")
not_in_text("$$FV = 3000(1.1)^{3}", "古い演習 1 は残っていない")

eq(FV(5000, 20, 1, 2), 7200, "演習2(a) 7200")
eq(7200 - 5000, 2200, "演習2(b) 2200")
chk(step(5000, "1.2", 2) == [6000, 7200], "1 年ずつでも 7200")
eq(5000 * sp.Rational("0.2"), 1000, "1 年目の利息 1000")
eq(6000 * sp.Rational("0.2"), 1200, "2 年目の利息 1200")
eq(1000 + 1200, 2200, "利息の合計 2200")
eq(5000 * sp.Rational("0.2") * 2, 2000, "単利なら 2000")
eq(2200 - 2000, 200, "差は 200")

eq(FV(2000, 20, 2, 2), sp.Rational("2928.2"), "演習3 2928.20")
chk(step(2000, "1.1", 4) == [2200, 2420, 2662, sp.Rational("2928.2")],
    "半年ごとに追っても 2928.20")
eq(FV(2000, 20, 1, 2), 2880, "yearly なら 2880")
eq(sp.Rational("2928.2") - 2880, sp.Rational("48.2"), "差は 48.20")

eq(8000 * sp.Rational(27, 64), 3375, "演習4 3375")
chk(step(8000, "0.75", 3) == [6000, 4500, 3375], "1 年ずつでも 3375")
eq(sp.Rational("0.75") ** 3, sp.Rational("0.421875"), "0.75^3 = 0.421875")

chk(step(10000, "0.8", 4) == [8000, 6400, 5120, 4096], "演習5 の列")
chk(5120 > 5000 > 4096, "境目は 4 年目")
eq(sp.Rational("0.8") ** 4, sp.Rational("0.4096"), "0.8^4 = 0.4096")
eq(sp.Rational("0.8") ** 2, sp.Rational("0.64"), "0.8^2 = 0.64")
eq(sp.Rational("0.8") ** 3, sp.Rational("0.512"), "0.8^3 = 0.512")
chk(sp.Rational("0.512") > sp.Rational(1, 2), "3 年目はまだ半分より上")

eq(4000 * sp.Rational("0.1") * 3, 1200, "演習6(a) 単利 1200")
eq(FV(4000, 10, 1, 3) - 4000, 1324, "演習6(b) 複利 1324")
eq(1324 - 1200, 124, "演習6(c) 差 124")
chk([4000 * sp.Rational("0.1"), 4400 * sp.Rational("0.1"),
     4840 * sp.Rational("0.1")] == [400, 440, 484], "利息は 400,440,484")
eq(400 + 440 + 484, 1324, "足しても 1324")
eq(0 + 40 + 84, 124, "単利との差だけ足しても 124")

eq(FV(5000, 8, 1, 1), 5400, "演習7(a) 5400")
_r7 = sp.Rational(5400) / sp.Rational("1.04")
chk(abs(float(_r7) - 5192.3077) < 0.001, f"real value 5192.31: {float(_r7)}")
chk(round(float(_r7), 2) == 5192.31, "小数第 2 位まで 5192.31")
eq(sp.Rational("5192.31") * sp.Rational("1.04"), sp.Rational("5400.0024"),
   "掛け戻すと 5400.0024")
eq(5000 * sp.Rational("1.04"), 5200, "差の 4% で計算すると 5200")
eq(sp.Rational(540000, 104), sp.Rational(67500, 13), "540000/104 = 67500/13")
eq(13 * 5192 + 4, 67500, "13×5192 = 67496、余りは 4")
in_text("\\dfrac{67\\,500}{13}", "約分した形を書いている")
chk(abs(float(sp.Rational("5192.31") - 5200) + 7.69) < 0.01, "ずれは 7.69")

chk(step(2000, "1.2", 4) == [2400, 2880, 3456, sp.Rational("4147.2")],
    "演習8 の列")
chk(3456 < 4000 < sp.Rational("4147.2"), "境目は 4 年目")
eq(sp.Rational("1.2") ** 3, sp.Rational("1.728"), "1.2^3 = 1.728")
eq(sp.Rational("1.2") ** 4, sp.Rational("2.0736"), "1.2^4 = 2.0736")
eq(sp.Rational("1.2") ** 5, sp.Rational("2.48832"), "1.2^5 = 2.48832")

eq(FV(1000, 20, 1, 1), 1200, "演習9(a) 1200")
eq(FV(1000, 20, 2, 1), 1210, "演習9(b) 1210")
eq(1210 - 1200, 10, "差は 10")
eq(100 * sp.Rational("0.1"), 10, "半年後の利息 100 に付く 10% は 10")
eq(sp.Rational(10, 1000), sp.Rational(1, 100), "差は元金の 1%")

eq(5000 * sp.Rational("1.2") ** 4, 10368, "演習10 生徒の答え 10368")
eq(FV(5000, 20, 2, 2), sp.Rational("7320.5"), "正しい答え 7320.50")
chk(step(5000, "1.1", 4) == [5500, 6050, 6655, sp.Rational("7320.5")],
    "半年ごとに追っても 7320.50")
eq(FV(5000, 20, 1, 2), 7200, "yearly なら 7200")
chk(10368 > 2 * 5000, "生徒の答えは元金の 2 倍以上")
chk(FV(5000, 20, 1, 2) < FV(5000, 20, 2, 2) < 2 * 5000,
    "正しい値は yearly より上、元金の 2 倍より下")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.4** の欄に `Compound interest` として印刷", "公式集にある")
in_text("where $FV$ is the future value, $PV$ is the present value, $n$ is the"
        " number of years, $k$ is the number of compounding periods per year,"
        " $r\\%$ is the nominal annual rate of interest", "記号の説明を逐語で")
in_text("**depreciation の式は、公式集にありません。**", "載っていないものを明記")
in_text("> In examinations, questions that ask students to derive the formula"
        " will not be set.", "導出は問われない（Guidance）")
in_text("> Calculate the real value of an investment with an interest rate and"
        " an inflation rate.", "real value の Guidance")
in_text("`Compound interest can be calculated yearly, half-yearly, quarterly"
        " or monthly.`", "k の Guidance")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("## この式は公式集にありません", "割り戻しの式は載っていないと明記")
in_text("## 割り戻しの指数は $kn$ ではなく $n$", "指数の注意")
in_text("**年 $1$ 回の複利で、利率とインフレ率が同じなら、実質価値は最初の額のまま**",
        "real value は条件つきで述べる")
in_text("**growth factor**（増加倍率）", "growth factor の訳は「増加倍率」")
not_in_text("（成長率・増加倍率）", "「成長率」と併記しない")
in_text("**growth rate（増加率）とは別のもの**です。", "rate と factor を分ける")
in_text("| 数列 | arithmetic（等差数列） | geometric（等比数列） |", "表に訳を添えた")
in_text("$5760$ の $2\\%$ にも届きません", "2% ほど → 2% にも届かない")
# 英語の言い回し
not_in_text("the first year at the end of which", "「何年かかるか」に直した")
not_in_text("at a nominal annual rate of", "nominal annual interest rate にそろえた")
chk(TEXT.count("Find the number of years it takes for") == 3,
    "「何年かかるか」は 3 か所")
chk(TEXT.count("nominal annual interest rate") >= 3,
    "nominal annual interest rate が 3 か所以上")
in_text("$r\\%$ is the nominal annual rate of interest",
        "公式集の逐語引用はそのまま")

# ══════════════════════════════════════════════════════════
# 8. GDC
# ══════════════════════════════════════════════════════════
in_text("menu → Finance → Finance Solver", "Finance Solver の場所")
in_text("`N` | 期間の**回数**", "N は回数")
in_text("自分から出ていくお金は**負**", "符号のきまり")
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")

# ══════════════════════════════════════════════════════════
# 9. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 5, "model-answer が 5")
chk(len(re.findall(r"^::: \{#exm-aasl14-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(m) for m in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
# \$（通貨の $）は数式の区切りではないので、先に伏せる（tools/README.md）
_MASKED = TEXT.replace("\\$", "\uE000")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a in _anchors or _a in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl14", "他ページの @-ref: " + _r0)
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
# 10. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-4-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-4-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("simple interest", "図(a) の凡例")
in_fig("compound interest", "図(a) の凡例 2")
in_fig("smaller rate, more times", "図(b) の要点")
in_fig("same after 1 year ($k=1$)", "図(a) に k=1 の断り")
in_fig("nominal $12", "図(b) は名目 12%")
for _fx in ["1.12", "1.06", "1.03"]:
    in_fig(_fx, "図(b) の 1 期あたりの倍率 " + _fx)
eq(1 + sp.Rational(12, 100 * 1), sp.Rational("1.12"), "k=1 で 1.12 倍")
eq(1 + sp.Rational(12, 100 * 2), sp.Rational("1.06"), "k=2 で 1.06 倍")
eq(1 + sp.Rational(12, 100 * 4), sp.Rational("1.03"), "k=4 で 1.03 倍")
in_text("(b) One year split into k equal periods",
        "キャプションが (b) も説明している")
# 図の数値が本文と合っているか
eq(1000 * sp.Rational("1.1") ** 10, sp.Rational("2593.742460100"),
   "図(a) の 10 年後（複利）")
eq(1000 + 100 * 10, 2000, "図(a) の 10 年後（単利）")
for leak in ["2916", "7200", "2928.2", "3375", "4096", "1324", "5192",
             "4147.2", "1210", "7320.5", "10368"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-4.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-3.qmd") < DRAFT.index("aasl-1-4.qmd"), "並びが 1.3 → 1.4")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aasl-1-4.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_m = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_m is not None and int(_m.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| compound interest |", "| present value ($PV$) |",
          "| future value ($FV$) |", "| nominal annual rate |",
          "| inflation |", "| real value |", "| annual depreciation |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ── 用語と採点の言い方（★2026-09-07 の修正）──────────────
for t in ["| growth factor |", "| growth rate |"]:
    chk(t in GLO, "対訳表にある: " + t)
not_in_text("点を落とします", "採点の断定を弱めた")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
