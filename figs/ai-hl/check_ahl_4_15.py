# -*- coding: utf-8 -*-
"""AHL 4.15（正規分布の一次結合）の検算。
   1. すべての確率を第一原理（erf）で計算する
   2. scipy による独立な実装と突き合わせる
   3. .qmd の本文が、その数値どおりに書かれているかを確かめる
   4. 改稿で直した表現が、あとで元に戻っていないかを見張る
   5. 構造の不変条件（fence の前の空行、code span の中身など）を確かめる
   実行: python3 figs/ai-hl/check_ahl_4_15.py
"""
import io
import math
import os
import re
import sys

from scipy.stats import norm

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "ahl-4-15.qmd")
TXT = io.open(QMD, encoding="utf-8").read()

OK = NG = 0


def eq(name, got, want):
    global OK, NG
    if got == want:
        OK += 1
    else:
        NG += 1
        print("NG  %s\n     got : %r\n     want: %r" % (name, got, want))


def close(name, got, want, tol=5e-4):
    global OK, NG
    if abs(got - want) <= tol:
        OK += 1
    else:
        NG += 1
        print("NG  %s  got %r want %r" % (name, got, want))


def in_text(s, times=None):
    global OK, NG
    c = TXT.count(s)
    if (c >= 1) if times is None else (c == times):
        OK += 1
    else:
        NG += 1
        print("NG  本文に無い/回数違い (%d): %r" % (c, s[:90]))


def not_in_text(s):
    global OK, NG
    if s not in TXT:
        OK += 1
    else:
        NG += 1
        print("NG  本文に残っている: %r" % (s[:90],))


# ══════════════════════════════════════════════════════════════
# 1. 正規分布の確率を、第一原理から（erf のみ）
# ══════════════════════════════════════════════════════════════
def Phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def P_gt(x, mu, sd):
    return 1.0 - Phi((x - mu) / sd)


def P_lt(x, mu, sd):
    return Phi((x - mu) / sd)


def P_between(a, b, mu, sd):
    return Phi((b - mu) / sd) - Phi((a - mu) / sd)


def sf3(x):
    """3 significant figures, as the book writes them."""
    if x == 0:
        return 0.0
    d = -int(math.floor(math.log10(abs(x)))) + 2
    return round(x, d)


# 独立な実装（scipy）と突き合わせる
for mu, sd, x in ((430, 10, 445), (3, 5, 0), (1000, 4, 995), (4.2, .39528, 4.5)):
    close("erf と scipy が一致 (%s,%s,%s)" % (mu, sd, x),
          P_gt(x, mu, sd), float(norm.sf(x, mu, sd)), 1e-12)

# ══════════════════════════════════════════════════════════════
# 2. 例題の数値
# ══════════════════════════════════════════════════════════════
# 例題1  M~N(250,8^2), S~N(180,6^2)
eq("例題1 E(T)", 250 + 180, 430)
eq("例題1 Var(T)", 8 ** 2 + 6 ** 2, 100)
eq("例題1 sd(T)", math.sqrt(100), 10.0)
close("例題1 (b) P(T>445)", sf3(P_gt(445, 430, 10)), 0.0668)
close("例題1 (c) P(420<T<445)", sf3(P_between(420, 445, 430, 10)), 0.775)
close("例題1 (b) を百分率にすると", round(100 * P_gt(445, 430, 10)), 7)
close("例題1 (c) を百分率にすると", round(100 * P_between(420, 445, 430, 10)), 77)

# 補足：コーヒー 2 杯
eq("補足 X1+X2 の分散", 2 * 8 ** 2, 128)
close("補足 sd", sf3(math.sqrt(128)), 11.3)
close("補足 P(X1+X2>510)", sf3(P_gt(510, 500, math.sqrt(128))), 0.188)
eq("補足 2X の分散", 4 * 64, 256)
close("補足 P(2X>510)", sf3(P_gt(510, 500, 16)), 0.266)

# 例題2  X~N(30,4^2), Y~N(27,3^2), D = X - Y
eq("例題2 E(D)", 30 - 27, 3)
eq("例題2 Var(D) は係数 -1 の 2 乗で足し算", 4 ** 2 + (-1) ** 2 * 3 ** 2, 25)
eq("例題2 sd(D)", math.sqrt(25), 5.0)
close("例題2 (b) P(D>0)", sf3(P_gt(0, 3, 5)), 0.726)
close("例題2 (c) P(D>=5)", sf3(P_gt(5, 3, 5)), 0.345)
close("例題2 (b) 百分率", round(100 * P_gt(0, 3, 5)), 73)
close("例題2 (c) 百分率", round(100 * P_gt(5, 3, 5)), 34)
eq("例題2 分散を引くのは誤り", 4 ** 2 - 3 ** 2, 7)

# 例題3  X~N(1000,12^2), n=9
eq("例題3 Var(Xbar)", 144 / 9, 16.0)
eq("例題3 sd(Xbar)", 12 / math.sqrt(9), 4.0)
close("例題3 (a) P(X<995)", sf3(P_lt(995, 1000, 12)), 0.338)
close("例題3 (b) P(Xbar<995)", sf3(P_lt(995, 1000, 4)), 0.106)

# 例題4  mu=4.2, sd=2.5, n=40
v = 2.5 ** 2 / 40
eq("例題4 Var(Xbar)", v, 0.15625)
close("例題4 sd(Xbar)", sf3(math.sqrt(v)), 0.395)
close("例題4 sd(Xbar) 5桁", round(math.sqrt(v), 5), 0.39528)
close("例題4 (b) P(Xbar>4.5)", sf3(P_gt(4.5, 4.2, math.sqrt(v))), 0.224)
close("例題4 (b) 百分率", round(100 * P_gt(4.5, 4.2, math.sqrt(v))), 22)
eq("例題4 (c) E(sum)", 40 * 4.2, 168.0)
eq("例題4 (c) Var(sum)", 40 * 2.5 ** 2, 250.0)
close("例題4 (c) sd(sum)", sf3(math.sqrt(250)), 15.8)
close("例題4 (c) sd(sum) 5桁", round(math.sqrt(250), 3), 15.811)
close("例題4 (c) P(sum>180)", sf3(P_gt(180, 168, math.sqrt(250))), 0.224)
# (b) と (c) が同じ事象であること（180 = 40 * 4.5）を数値でも確かめる
eq("180 = 40 x 4.5", 40 * 4.5, 180.0)
close("平均で解いた確率 = 合計で解いた確率",
      P_gt(4.5, 4.2, math.sqrt(v)), P_gt(180, 168, math.sqrt(250)), 1e-12)

# ══════════════════════════════════════════════════════════════
# 3. 演習の数値
# ══════════════════════════════════════════════════════════════
eq("Ex1 Var(X+Y) = Var(X-Y)", 5 ** 2 + 12 ** 2, 169)
eq("Ex1 sd", math.sqrt(169), 13.0)
eq("Ex1 E(X+Y)", 50 + 30, 80)
eq("Ex1 E(X-Y)", 50 - 30, 20)
close("Ex2 P(X+Y>95)", sf3(P_gt(95, 80, 13)), 0.124)
close("Ex2 分散を入れた誤答", sf3(P_gt(95, 80, 169)), 0.465)
eq("Ex3 sd(Xbar)", 5 / math.sqrt(16), 1.25)
close("Ex3 P(Xbar>21.5)", sf3(P_gt(21.5, 20, 1.25)), 0.115)
close("Ex3 1つの X なら", sf3(P_gt(21.5, 20, 5)), 0.382)
close("Ex4 Var(B+C)", 0.05 ** 2 + 0.2 ** 2, 0.0425, 1e-12)
close("Ex4 sd", sf3(math.sqrt(0.0425)), 0.206)
close("Ex4 sd 5桁", round(math.sqrt(0.0425), 5), 0.20616)
close("Ex4 P(B+C>3)", sf3(P_gt(3, 2.9, math.sqrt(0.0425))), 0.314)
close("Ex6 Var(Xbar)", 3.6 ** 2 / 50, 0.2592, 1e-12)
close("Ex6 sd", sf3(math.sqrt(3.6 ** 2 / 50)), 0.509)
close("Ex6 P(Xbar<8)", sf3(P_lt(8, 8.4, math.sqrt(3.6 ** 2 / 50))), 0.216)
eq("Ex8 Var(3X)", 3 ** 2 * 4, 36)
close("Ex8 P(3X>36)", sf3(P_gt(36, 30, 6)), 0.159)
eq("Ex8 Var(X1+X2+X3)", 3 * 4, 12)
close("Ex8 sd(sum)", sf3(math.sqrt(12)), 3.46)
close("Ex8 P(sum>36)", sf3(P_gt(36, 30, math.sqrt(12))), 0.0416)
eq("Ex9 sd(Xbar)", 20 / math.sqrt(25), 4.0)
close("Ex9 k = invNorm(0.95,500,4)", round(float(norm.ppf(0.95, 500, 4)), 3), 506.579)
eq("Ex9 k を3桁で", round(float(norm.ppf(0.95, 500, 4))), 507)
eq("Ex9 0.05 を入れた誤答", round(float(norm.ppf(0.05, 500, 4))), 493)
eq("Ex10 E(sum)", 8 * 72, 576)
eq("Ex10 Var(sum)", 8 * 100, 800)
close("Ex10 sd", sf3(math.sqrt(800)), 28.3)
close("Ex10 sd 5桁", round(math.sqrt(800), 3), 28.284)
close("Ex10 P(sum>620)", sf3(P_gt(620, 576, math.sqrt(800))), 0.0599)
eq("Ex10 Var(8X)", 8 ** 2 * 100, 6400)
eq("Ex10 sd(8X)", math.sqrt(6400), 80.0)

# Common errors の誤答
close("誤答 normCdf に分散 100 を入れると", sf3(P_gt(445, 430, 100)), 0.440)

# ══════════════════════════════════════════════════════════════
# 4. 本文が、その数値どおりに書かれているか
# ══════════════════════════════════════════════════════════════
in_text("P(T > 445) = 0.0668")
in_text("P(420 < T < 445) = 0.775")
in_text("$1$ 食の合計質量が $445$ g を超えるのは、およそ $100$ 食のうち $7$ 食です。")
in_text("$1$ 食のおよそ $77\\%$ が、$420$ g から $445$ g のあいだに入ります。")
in_text("ブランド A のほうが長持ちするのは、およそ $73\\%$ です。")
in_text("$5$ 時間以上長持ちするのは、およそ $34\\%$ です。")
in_text("$40$ 人の平均対応時間が $4.5$ 分を超える日は、およそ $22\\%$ です。")
in_text("P(D > 0) = 0.726")
in_text("P(D \\geq 5) = 0.345")
in_text("P(X < 995) = 0.338")
in_text("P(\\bar{X} < 995) = 0.106")
in_text("P(\\bar{X} > 4.5) = 0.224")
in_text("\\sigma_{\\bar{X}} = \\sqrt{0.15625} = 0.395")
in_text("\\text{Var}(\\bar{X}) = \\frac{2.5^{2}}{40} = \\frac{6.25}{40} = 0.15625")
in_text("正しい $0.0668$ とはまったく違う答えになります")
in_text("分散を入れると $0.440$")

# ══════════════════════════════════════════════════════════════
# 5. 改稿でそろえた表現（あとで戻っていないか）
# ══════════════════════════════════════════════════════════════
# 5-1 導入
in_text("平均と分散だけでは、確率は一意に決まりません")
in_text("確率を計算するには、normal など、**分布の種類も分かっている**必要があります")
not_in_text("しかし、平均と分散だけでは確率は出せません")
not_in_text("**分布の形が分からない**からです")
not_in_text("AHL 4.14 で足りなかった「形」が、ここで手に入ります")
# 冒頭から外し、GDC の直前へ移した 2 つ
gdc = TXT.index("## Using your GDC")
eq("公式集の注意は GDC の直前にある", TXT.index("AI HL の公式集は **4.14 の次が 4.17**") > gdc, True)
eq("z 値の注意は GDC の直前にある",
   TXT.index("standardized normal variable $z$") > gdc, True)

# 5-2 linear combination を先に定義してから一般式
i_def = TXT.index("linear combination**（一次結合）といいます")
i_gen = TXT.index("Y = a_1X_1 + \\cdots + a_nX_n")
eq("linear combination の定義が一般式より前にある", i_def < i_gen, True)
in_text("$X + Y$、$2X - Y$、$\\dfrac{X_1 + \\cdots + X_n}{n}$ のように、確率変数に定数をかけて足し合わせたもの")
in_text("**「和」「差」「標本平均」は、すべて一次結合の例です。**")

# 5-3 中心公式が 1 か所にまとまっている
blk = TXT[TXT.index("## 独立な normal random variables の linear combination も normal distribution にしたがう"):]
blk = blk[:blk.index(":::\n")]
for need in ("X_i \\sim N(\\mu_i,\\ \\sigma_i^{2})",
             "Y = a_1X_1 + \\cdots + a_nX_n",
             "E(Y) = a_1\\mu_1 + \\cdots + a_n\\mu_n",
             "\\text{Var}(Y) = a_1^{2}\\sigma_1^{2} + \\cdots + a_n^{2}\\sigma_n^{2}"):
    eq("中心公式の箱に %s がある" % need[:24], need in blk, True)
in_text("**平均では係数をそのまま使いますが、分散では係数を $2$ 乗します。**")

# 5-4 標準偏差：原則が先、3 段階、N の第2引数は分散
i_rule = TXT.index("standard deviation（標準偏差）を直接足すのではなく、まず variance（分散）を足します")
eq("原則が数値の前にある", i_rule < TXT.index("\\text{Var}(M + S) = 8^{2} + 6^{2} = 100"), True)
# 直角三角形の比喩と、その図は取り除いた
not_in_text("直角三角形")
not_in_text("{#pythagoras}")
not_in_text("{#eq-ahl415-sd}")
not_in_text("$8 + 6 = 14$ ではありません {#pythagoras}")
not_in_text("(#pythagoras)")
in_text("![Adding two independent normals gives another normal](img/ahl-4-15-sum.svg)")
in_text("@fig-ahl415-sum のとおり、$M$ と $S$ を足して出てくるのも normal distribution です。")
in_text("\\text{Var}(M + S) = 8^{2} + 6^{2} = 100")
in_text("\\sigma_{M+S} = \\sqrt{100} = 10")
in_text("M + S \\sim N(430,\\ 100)")
in_text("**$N(\\mu,\\ \\sigma^{2})$ のカッコの $2$ 番目は、分散です。**")
not_in_text("## 分散のまま計算して、最後に平方根をとってください")

# 5-5 3 ステップの型
in_text("| **1** | $E(Y)$ を求める（係数はそのまま使う） |")
in_text("| **2** | $\\text{Var}(Y)$ を求める（係数は $2$ 乗する） |")
in_text("$X_i$ が独立な normal であることを確かめて $Y \\sim N(\\mu,\\ \\sigma^{2})$ と書き、"
        "$\\sigma$ を GDC に入れる（もとが normal でない場合は[第8節](#when)）")
in_text("$M + S$ の例なら、$E = 430$ → $\\text{Var} = 100$ → $M + S \\sim N(430,\\ 100)$ と書いて、"
        "$\\sigma = 10$ を `normCdf` へ、という流れです。")
in_text("GDC の `normCdf` に入力するのは mean（平均）と standard deviation（標準偏差）です")
in_text("電卓に入れる前に、**求めた分布を $1$ 行書く**習慣をつけてください")

# 5-6 差：符号が消えるところまで
in_text("D = X + (-1)Y")
in_text("\\text{Var}(D) = \\text{Var}(X) + (-1)^{2}\\text{Var}(Y) = \\text{Var}(X) + \\text{Var}(Y)")
in_text("この式は、**$X$ と $Y$ が独立である場合**に使えます")
in_text("A > B \\iff A - B > 0 \\iff D > 0")
in_text("P(A > B) = P(A - B > 0) = P(D > 0)")

# 5-7 標本平均
in_text("\\bar{X} = \\frac{X_1 + \\cdots + X_n}{n}")
in_text("**各 $X_i$ の係数が $\\dfrac{1}{n}$ である linear combination**")
in_text("&= n\\left(\\frac{1}{n}\\right)^{2}\\sigma^{2} \\\\\n&= n \\cdot \\frac{1}{n^{2}}\\sigma^{2} \\\\\n&= \\frac{\\sigma^{2}}{n}")
in_text("\\sigma_{\\bar{X}} = \\sqrt{\\frac{\\sigma^{2}}{n}} = \\frac{\\sigma}{\\sqrt{n}}")
in_text("**standard error**（標準誤差）")
in_text("標本の数が増えると、偶然によるばらつきが平均の中で打ち消し合うため")

# 5-8 合計と平均を式でつなぐ
in_text("\\bar{X} > 4.5 &\\iff 40\\bar{X} > 40 \\times 4.5 \\\\\n&\\iff T > 180")
i_same = TXT.index("{#eq-ahl415-same}")
i_tbl = TXT.index("{#tbl-ahl415-total}")
eq("同値変形が表より前にある", i_same < i_tbl, True)

# 5-9 / 5-10 CLT の順番
i_clt = TXT.index("### 6. Central limit theorem（中心極限定理） {#clt}")
i_one = TXT.index("#### $1$ 回の測定値と sample mean は、別のものです {#one-vs-mean}")
i_fig = TXT.index("img/ahl-4-15-clt.svg")
i_state = TXT.index("これが **central limit theorem**（中心極限定理、CLT）です。")
i_bigger = TXT.index("#### $n$ が大きくなると、何が起こるのか {#bigger-n}")
i_notdata = TXT.index("#### CLT は「データが normal になる」とは言っていません {#not-data}")
i_n30 = TXT.index("#### どのくらいの $n$ が必要ですか {#n30}")
eq("CLT の順序 導入→測定値と平均→図→定理→n が大きいと→注意→n>30",
   i_clt < i_one < i_fig < i_state < i_bigger < i_notdata < i_n30, True)
# 節の順序：5 → 6 CLT → 7 平均と合計 → 8 exactly / approximately
eq("CLT は「平均で解いても合計で解いても同じ」より前",
   i_clt < TXT.index("### 7. 平均で解いても、合計で解いても同じです {#total}"), True)
eq("exactly / approximately は最後",
   TXT.index("### 7. 平均で解いても、合計で解いても同じです {#total}")
   < TXT.index("### 8. exactly normal と approximately normal {#when}"), True)
in_text("同じ population から独立に取り出した標本の sample mean $\\bar{X}$ は、sample size $n$ が"
        "十分に大きいとき、もとの population が normal でなくても、"
        "**approximately normal distribution**（近似的な正規分布）にしたがいます。")

# 5-11 n > 30 を絶対視しない
in_text("**ただし、これは数学的な境界ではありません。**")
in_text("分布の偏りが強い場合や外れ値が多い場合は、より大きな $n$ が必要になることがあります")
not_in_text("$n > 30$ のときは、もとの分布が normal でなくても、$\\bar{X}$ を normal として扱ってよい")
not_in_text("ただし試験では、**$n > 30$ なら十分**と決められています。")
not_in_text("この課程では答えを出せません")
not_in_text("この課程では、正規として扱えません")
not_in_text("**言えない。** この課程では扱いません")

# 5-12 判定フロー
in_text("**normal approximation（正規近似）を正当化できない**からです")
in_text("## 「分布が不明」と「normal ではない」は違います")

# 5-13 例題の解答形式
in_text("$1$ 食の合計質量を $T = M + S$ とおきます")
in_text("$M$ も $S$ も normal で、独立なので、$T$ は **exactly normal** です")
in_text("$X$ も $Y$ も normal で、独立なので、$D$ は **exactly normal** です")
in_text("$N(3,\\ 25)$ の $25$ は分散なので、標準偏差は $\\sigma = \\sqrt{25} = 5$ です")
in_text("もとの $X$ が normal なので、$n = 9$ でも $\\bar{X}$ は **exactly normal** です")
in_text("$n = 40$ は十分大きいため、CLT により $\\bar{X}$ は **approximately normal** です。"
        "「normal である」と断定しないでください。")
in_text("$\\bar{X}$ は approximately normal なので、$\\bar{X} \\sim N(4.2,\\ 0.15625)$ と書けます")

# 5-14 例題内の区別
in_text("## 補足：$2$ 杯のコーヒーなら、こうなります")
in_text("ここからは、この問題の解答ではなく、**同じ考え方を別の場面に使う話**です")
in_text("$1$ 袋の質量を $X$、$9$ 袋の標本平均を $\\bar{X}$ とします")
in_text("**(a)** $1$ 袋を選ぶ場合なので")
in_text("**(b)** $9$ 袋の**平均**を調べる場合なので")
not_in_text("$2$ つのばらつきは打ち消し合わずに重なる、という意味です")

# 5-15 Common errors は 4 項目
ce = TXT[TXT.index("## Common errors"):TXT.index("## このページの判断手順")]
eq("Common errors は 4 項目", ce.count("::: {.callout-warning}"), 4)
for t in ("## 標準偏差を直接足してしまう",
          "## 差を取るときに、分散まで引いてしまう",
          "## $N(\\mu,\\ \\sigma^{2})$ と、GDC の標準偏差を混同する",
          "## exactly normal と、CLT による approximately normal を混同する"):
    eq("Common errors に %s" % t[3:20], t in ce, True)
eq("各項目に「誤り」がある", ce.count("**誤り**"), 4)
eq("各項目に「正しくは」がある", ce.count("**正しくは**"), 4)

# 5-16 まとめは GDC の前
i_sumsec = TXT.index("## このページの判断手順")
eq("判断手順は Common errors の後", TXT.index("## Common errors") < i_sumsec, True)
eq("判断手順は GDC の前", i_sumsec < TXT.index("## Using your GDC"), True)
for t in ("① 求めたい量を、和・差・標本平均として式にする。",
          "② 平均は、係数をそのまま使って計算する。",
          "③ 分散は、係数を $2$ 乗して足す。",
          "⑤ 分散の平方根を取り、標準偏差を GDC に入れる。"):
    in_text(t)
in_text("[第3節の $3$ ステップ](#steps)は**計算の手順**、こちらは**normal と言ってよいかを確かめる手順**です")

# 5-17 表記の統一
for term in ("**normal distribution**（正規分布）", "**linear combination**（一次結合）",
             "**sample mean**（標本平均）", "**central limit theorem**（中心極限定理、CLT）",
             "**standard error**（標準誤差）"):
    in_text(term)
eq("standard deviation（標準偏差）の併記", "standard deviation（標準偏差）" in TXT, True)
eq("variance（分散）の併記", "variance（分散）" in TXT, True)
not_in_text("**正確に** normal")
not_in_text("ぴったり normal")
not_in_text("かなり正規に近づいて")

# ══════════════════════════════════════════════════════════════
# 6. 構造の不変条件
# ══════════════════════════════════════════════════════════════
bad = [m for m in re.findall(r"`[^`\n]+`", TXT) if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", bad, [])

L = TXT.split("\n")
nb = [i + 1 for i, l in enumerate(L)
      if re.match(r"^:{3,} *\{", l) and i > 0
      and L[i - 1].strip() != "" and not L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", nb, [])

eq("演習は 10 問", TXT.count("]{.ex-no}"), 10)
eq("区切りは 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 つ", TXT.count("::: {.exercise-block}"), 1)
eq("日本語訳の折りたたみ", TXT.count('<details class="jp-trans">'), 14)

# ページ内リンクの行き先が、すべて存在するか
anchors = set(re.findall(r"\{#([A-Za-z0-9\-]+)\}", TXT))
anchors |= set(re.findall(r"\{#(sec-[A-Za-z0-9\-]+)\}", TXT))
links = set(re.findall(r"\]\(#([A-Za-z0-9\-]+)\)", TXT))
eq("ページ内リンクの行き先がすべてある", sorted(links - anchors), [])

# 禁止語（_TEMPLATE.qmd）
for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"):
    not_in_text(w)

eq("検算が書かれている", TXT.count("**検算。**") >= 4, True)
eq("model-answer がある", TXT.count("::: {.model-answer}") >= 6, True)



# ══════════════════════════════════════════════════════════════
# 7. レビューで直した点（元に戻っていないか）
# ══════════════════════════════════════════════════════════════
# 7-1 Poisson の和と食い違わない
not_in_text("ほかの分布ではこうなりません")
in_text("独立な $2$ つの Poisson の和が Poisson になるのは、[AHL 4.17](ahl-4-17.qmd#sum) の別の規則です")

# 7-2 「1 つの値 X は normal にならない」を言い切らない
not_in_text("$1$ つの値 $X$ そのものは、$n$ をどれだけ大きくしても normal にはなりません")
in_text("**CLT が $1$ つの値 $X$ を normal にしてくれることはありません**")
in_text("もとの population が normal でなければ、$1$ 回の測定値 $X_i$ の分布も normal ではありません")

# 7-3 第6節：形を決めていないことを明示し、近似だと書く
in_text("$1$ 人分の待ち時間が normal distribution にしたがうとは分かっていません")
in_text("$n = 40 > 30$ なので、CLT により")
eq("CLT の節が「平均と合計」の節より前", TXT.index("{#clt}") < TXT.index("{#total}"), True)

# 7-4 2 乗すると「差が広がる」
not_in_text("小さいほうのばらつきは、$2$ 乗するとさらに小さくなる")
in_text("**ばらつきの差は、$2$ 乗すると広がります**")
eq("2乗で差が広がる（4倍→16倍）", (0.2 / 0.05) ** 2, 16.0)

# 7-5 Why it works の CLT が近似のまま
not_in_text("正規分布の形になる**——これが中心極限定理の内容です")
in_text("$n$ が大きくなるにつれて正規分布に近づいていきます**——これが中心極限定理の内容です")

# 7-6 例題3 (c) の英文
not_in_text("all the light bags would have to fail to be offset by heavier ones")
in_text("a light bag tends to be offset by a heavier one, so the mean falls below $995$ g only if the nine bags are light on average")

# 7-7 normal になる根拠は式番号ではなく節へのリンク
not_in_text("@eq-ahl415-main は使えません")
in_text("「独立な normal の一次結合は normal」という結果（[第1節](#lincomb)）は使えません")
in_text("$T$ は **exactly normal** です（[第1節](#lincomb)）")

# 7-8 公式集：載っていないものを載っていると書かない
not_in_text("4.15 の欄はありません。ただし、使う式はすべて 4.14 の欄にあります")
in_text("は印刷されていません。この $2$ つは覚える必要があります。**")

# 7-9 「この 8 人で」
not_in_text("この $8$ 人で積載量を超える")
in_text("$8$ 人が乗るたびに、$100$ 回に $6$ 回ほど積載量を超える")

# 7-10 差の分散は解答例でも (-1)^2 を見せる
eq("(-1)^2 を書いた式の回数", TXT.count("4^{2} + (-1)^{2} \\times 3^{2}"), 5)
not_in_text("\\text{Var}(D) = 4^{2} + 3^{2} = 25")
not_in_text("\\text{Var}(D) = 16 + 9 = 25")

# 7-11 例題4 は ans を使う（丸めた値を打ち込まない）
not_in_text("normCdf(4.5, ∞, 4.2, 0.39528)")
not_in_text("normCdf(180, ∞, 168, 15.811)")
# 2026-09: GDC の入力例は画面どおりの表示（根号・分数テンプレート）に変更
in_text(r"\sqrt{\dfrac{2.5^{2}}{40}} \ \to \ \texttt{ans}")
in_text(r"\texttt{normCdf}\left(4.5,\ \infty,\ 4.2,\ \texttt{ans}\right)")
in_text(r"\sqrt{250} \ \to \ \texttt{ans}")
in_text(r"\texttt{normCdf}\left(180,\ \infty,\ 168,\ \texttt{ans}\right)")
not_in_text("√(2.5^2/40)  →  ans")
not_in_text("√250  →  ans")

# 7-12 3 ステップの説明と表が食い違わない
not_in_text("$2$ と $3$ のあいだの「normal だと言ってよい」という一歩")
in_text("手順 $3$ の前半、「normal だと言ってよい」という一歩だけです")

# 7-13 英語でも normal approximation を正当化できない、と書く
not_in_text("so the central limit theorem cannot be applied")
not_in_text("so the central limit theorem does not apply")
eq("a normal approximation ... cannot be justified の回数",
   TXT.count("a normal approximation for the mean cannot be justified"), 2)

# 7-14 independent を落とさない
in_text("なら、独立な normal random variables の linear combination も normal なので")
in_text("| normal distribution（観測は独立） |")
in_text("| normal とは限らない（観測は独立） |")
in_text("$9$ 袋は独立で、もとの $X$ が normal なので")
in_text("The mean of $8$ independent observations")
in_text("The mean of $60$ independent observations")
in_text("独立な $8$ 個の観測値の平均")
in_text("独立な $60$ 個の観測値の平均")

# 7-15 例題4 (c) も approximately と書く
in_text("CLT は平均と合計の両方についての定理なので、合計も **approximately normal** です")
in_text("*By the central limit theorem the total is also approximately normal.*")

# 7-17 Common errors の各項目は 1 つの誤りだけ
not_in_text("標本平均でも同じで、$\\sigma_{\\bar{X}} = \\dfrac{\\sigma}{\\sqrt{n}}$ であり")

# 7-18 折りたたみの中へ直リンクしない
not_in_text("（[Why it works](#why-xbar)）")
in_text("途中式は「Why it works」を開くと出てきます")

# 7-19 見出しは _TEMPLATE の 7 つだけ
L2 = TXT.split("\n")
chapters = [l[3:] for i, l in enumerate(L2)
            if l.startswith("## ")
            and not (i and L2[i - 1].lstrip().startswith(":::"))]
want = ["The idea", "Why it works", "Worked examples",
        "Common errors", "Using your GDC (TI-Nspire CX II)", "Exercises"]
eq("章見出しは _TEMPLATE の順どおり", chapters, want)
in_text("::: {.callout-note}\n## What you should be able to do")
in_text("## このページの判断手順")

# 7-20 タイトル
in_text("# AHL 4.15 — Linear combinations of normal variables（正規分布にしたがう確率変数の一次結合）")

# 7-22 Inverse Normal の例が 5% の説明と合っている
# 2026-09: GDC の入力例は画面どおりの表示に変更
in_text(r"\texttt{invNorm}\left(0.95,\ 60,\ 2.5\right)")
not_in_text("invNorm(0.90, 60, 2.5)")
close("invNorm(0.95, 60, 2.5)", round(float(norm.ppf(0.95, 60, 2.5)), 1), 64.1)
in_text("「上から $5\\%$ に入る境目」を求めています")




# ══════════════════════════════════════════════════════════════
# 8. 説明を足した箇所（あとで抜け落ちていないか）
# ══════════════════════════════════════════════════════════════
in_text("## 独立な normal random variables の linear combination も normal distribution にしたがう")
in_text("ここで $Y$ は、$X_1,\\ \\ldots,\\ X_n$ にそれぞれ定数 $a_1,\\ \\ldots,\\ a_n$ を"
        "かけて足し合わせて作った、**新しい確率変数**です。")
in_text("この $Y$ も normal distribution にしたがい、")

# 第2節：語の対応と N(430, 10^2)
in_text("$2$ つの値の合計を表す**新しい確率変数** $M + S$ を考えます")
for s in ("**平均（expected value）**は、係数がどちらも $1$ なので足すだけです。",
          "次に、**分散（variance）**を求めます。$M$ と $S$ は独立なので、それぞれの分散を足します。",
          "**標準偏差（standard deviation）**は、分散の正の平方根です。",
          "したがって、$M + S$ がしたがう**分布（distribution）**は"):
    in_text(s)
in_text("M + S \\sim N(430,\\ 10^{2})")
in_text("$10^{2} = 100$ なので $N(430,\\ 100)$ と書いても同じ分布です")
in_text("ここで、$E$ は平均、$\\text{Var}$ は分散、$\\sigma$ は標準偏差を表します。")
in_text("**このページで新しく学ぶのは、それらをつなぐ部分**")

# 第4節：D が新しい確率変数
in_text("**差を表す新しい確率変数**です")
in_text("$D$ は「$1$ 回目の測定値と $2$ 回目の測定値の差」を表します")
in_text("**したがって、差の平均は引き算ですが、差の分散は足し算です。**")

# A > B の書きかえ
in_text("**$A$ のほうが大きい**という出来事と、**$D$ が正である**という出来事は、まったく同じものです")
in_text("$A$ と $B$ が独立な normal random variables なら、[第1節](#lincomb)より "
        "$D = A - B$ も normal distribution にしたがいます")
in_text("1. $D$ の平均を求める … $E(D) = E(A) - E(B)$")
in_text("2. $D$ の分散と標準偏差を求める")
in_text("3. `normCdf` で $P(D > 0)$ を求める")
in_text("「$A - B$ は $0$ より大きいか」という $1$ つの normal distribution の問題に変える")

# 第5節：random variable と observed value
in_text("$\\bar{X}$ は「エックス・バー」と読みます")
in_text("$n$ 回目の抽出で得られる値を表す **random variables**（確率変数）です")
in_text("選ぶ前は値が決まっていないので、$X_1$ は $1$ つの数値ではなく random variable であり")
in_text("**observed value**（観測値）")
in_text("population が normal distribution $N(\\mu,\\ \\sigma^{2})$ にしたがうなら、"
        "各 $X_i$ も同じ分布にしたがいます。")
in_text("X_i \\sim N(\\mu,\\ \\sigma^{2})")
in_text("この $n$ 個の値の平均を表す新しい確率変数が、sample mean $\\bar{X}$ です。")
in_text("\\bar{X} = \\frac{X_1 + \\cdots + X_n}{n} = \\frac{1}{n}X_1 + \\cdots + \\frac{1}{n}X_n")
in_text("E(\\bar{X}) &= \\frac{1}{n}\\mu + \\cdots + \\frac{1}{n}\\mu \\\\\n"
        "&= n\\left(\\frac{1}{n}\\right)\\mu \\\\\n&= \\mu")
in_text("\\text{Var}(\\bar{X}) &= \\left(\\frac{1}{n}\\right)^{2}\\text{Var}(X_1) + \\cdots + "
        "\\left(\\frac{1}{n}\\right)^{2}\\text{Var}(X_n)")
in_text("&= \\left(\\frac{1}{n}\\right)^{2}\\sigma^{2} + \\cdots + \\left(\\frac{1}{n}\\right)^{2}\\sigma^{2}")
in_text("**ここで大事なのは、分散では係数 $\\dfrac{1}{n}$ を $2$ 乗することです。**")
in_text("\\boxed{\\ \\text{Var}(\\bar{X}) = \\frac{\\sigma^{2}}{n}\\ }")
in_text("\\boxed{\\ \\bar{X} \\sim N\\!\\left(\\mu,\\ \\frac{\\sigma^{2}}{n}\\right)\\ }")
in_text("$n$ が大きいほど standard error は小さくなり、$\\bar{X}$ は population mean $\\mu$ の"
        "近くに集まりやすくなります。")
eq("Var(Xbar) の値（n=9, sigma=12）", 12 ** 2 / 9, 16.0)
eq("sd(Xbar) の値（n=9, sigma=12）", 12 / 3, 4.0)




# ══════════════════════════════════════════════════════════════
# 9. 節の入れかえ（5 → 6 CLT → 7 平均と合計 → 8 exactly/approximately）
# ══════════════════════════════════════════════════════════════
in_text(r"**これは、$\bar{X}$ の分布の「広がり」についての性質です。**")
in_text(r"一方、次に学ぶ **central limit theorem**（中心極限定理）は、$n$ が大きくなると "
        r"$\bar{X}$ の分布の「**形**」が normal distribution に近づくことを説明します。")

# 第6節 CLT
in_text(r"### 6. Central limit theorem（中心極限定理） {#clt}")
in_text(r"たとえば待ち時間の分布は、短い値が多く、右側に長く伸びた形になることがあります")
in_text(r"では、もとの分布が normal でない場合、sample mean $\bar{X}$ はどのような分布になるのでしょうか。")
in_text(r"\boxed{\ \bar{X} \approx N\!\left(\mu,\ \frac{\sigma^{2}}{n}\right)\ }", 2)
in_text(r"この $\dfrac{\sigma}{\sqrt{n}}$ が、[第5節](#xbar)で出てきた **standard error**（標準誤差）です。")
in_text(r"#### $n$ が大きくなると、何が起こるのか {#bigger-n}")
in_text(r"#### どのくらいの $n$ が必要ですか {#n30}")
in_text(r"## 答案での書き方")
in_text(r"*Since $n = 40 > 30$, by the central limit theorem, $\bar{X}$ is approximately normal.*")
in_text(r"もとの population が normal だと分かっている場合を除き、exactly normal とは言えません。")

# 第7節 平均と合計
in_text(r"### 7. 平均で解いても、合計で解いても同じです {#total}")
in_text(r"#### 方法1：平均で考える {#by-mean}")
in_text(r"#### 方法2：合計で考える {#by-total}")
in_text(r"#### なぜ $2$ つの確率は同じなのか {#same-event}")
in_text(r"T = X_1 + \cdots + X_{40}")
in_text(r"E(T) = 40 \times 4.2 = 168")
in_text(r"\text{Var}(T) = 40 \times 2.5^{2} = 250")
in_text(r"$T = 40\bar{X}$ なので、$\bar{X}$ が approximately normal なら $T$ も approximately normal です。")
in_text(r"T \approx N(168,\ 250)")
in_text(r"\boxed{\ P(\bar{X} > 4.5) = P(T > 180)\ }")
in_text(r"平均と合計では数値の尺度が違いますが、表している出来事は同じです。")
eq("E(T) の値", 40 * 4.2, 168.0)
eq("Var(T) の値", 40 * 2.5 ** 2, 250.0)
eq("Var(Xbar) の値（n=40）", 2.5 ** 2 / 40, 0.15625)
eq("40 x 4.5 = 180", 40 * 4.5, 180.0)

# 第8節 exactly / approximately
in_text(r"### 8. exactly normal と approximately normal {#when}")
in_text(r"#### population が normal の場合 {#small-n}")
in_text(r"#### population が normal とは限らない場合 {#approx-case}")
in_text(r"#### 最後に確認 {#flow}")
in_text(r"- population が normal なら、$\bar{X}$ は **exactly normal**")
in_text(r"- population が normal とは限らなければ、十分に大きな $n$ に対して **approximately normal**")
in_text(r"E(\bar{X}) = \mu, \qquad \text{Var}(\bar{X}) = \frac{\sigma^{2}}{n}")

# 節番号の参照が入れかわっている
in_text(r"使うのは **central limit theorem** です（[第6節](#clt)）。")
in_text(r"**言い方が違うだけの同じ出来事**です（[第7節](#total)）。")
in_text(r"`approximately` も忘れずに（[第6節](#n30)）。")
not_in_text(r"（[第7節](#clt)）")
not_in_text(r"（[第6節](#total)）")
not_in_text(r"（[第7節](#n30)）")



# 例題では、日本語訳の折りたたみの下に区切り線（---）を置く
i_we = TXT.index("## Worked examples")
i_ce = TXT.index("## Common errors")
_we = TXT[i_we:i_ce]
eq("例題の日本語訳の下に区切り線がある",
   _we.count("</details>\n\n---\n\n"), _we.count("</details>"))
eq("例題は 4 つ", _we.count("::: {#exm-"), 4)
eq("演習には区切り線を入れない", TXT[i_ce:].count("\n---\n"), 0)



# normCdf の端は ∞ / -∞ で書く（1E99 は注記のみ）
eq("code の中に 1E99 が残っていない",
   [l for l in TXT.split("\n")
    if "1E99" in l and (l.lstrip().startswith("normCdf")
                        or l.lstrip().startswith(r"$\texttt{normCdf}"))], [])
eq("∞ を使った normCdf がある",
   TXT.count("normCdf(") + TXT.count(r"\texttt{normCdf}") >= 10, True)
in_text("## $\infty$ の入れ方と、$1E99$ という書き方")
in_text("記号パレット")
# 2026-09: 記号パレットは π キー（∞・°）／ctrl + = （≤ ≥）に訂正
in_text("**`π` のキー**を押すと開く**記号パレット**")
not_in_text("`ctrl` と `k` を押すとパレットが開く")
in_text("| `Lower Bound` | 下の端。なければ $-\infty$ |")
in_text("| `Upper Bound` | 上の端。なければ $\infty$ |")


print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
