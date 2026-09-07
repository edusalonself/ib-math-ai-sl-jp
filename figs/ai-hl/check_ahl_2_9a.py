"""AHL 2.9a（半減期・自然対数モデル・正弦モデル）の内容を検算する。

    python3 figs/ai-hl/check_ahl_2_9a.py

方針
  1. すべての数値・式を sympy で第一原理から出す
  2. 別の方法で交差検証する
  3. ページの本文がその結果と一致しているかを in_text で確かめる
  4. レビューで直した箇所は not_in_text で再発を防ぐ
  5. 構造（見出し・例題数・演習数・区切り）を確かめる
"""
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "02-functions", "ahl-2-9a.qmd")
TEXT = open(QMD, encoding="utf-8").read()

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def near(a, b, tol=5e-4, msg=""):
    chk(abs(float(a) - float(b)) < tol, msg + f"  ({float(a)} vs {float(b)})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


t, x, k = sp.symbols("t x k", positive=True)
N = lambda e: sp.N(e, 12)

# ══════════════════════════════════════════════════════════
# 1. half-life
# ══════════════════════════════════════════════════════════
M = 500 * sp.exp(-sp.Rational(12, 100) * t)
T = sp.log(2) / sp.Rational(12, 100)
near(T, 5.776226505, msg="ln2/0.12 = 5.7762")
chk(round(float(T), 2) == 5.78, "3 s.f. で 5.78")
near(M.subs(t, T), 250, msg="T で半分になる")
near(M.subs(t, 10), 150.5971, msg="M(10) = 150.60 → 151")
chk(round(float(M.subs(t, 10))) == 151, "M(10) は 151 mg")
near(sp.log(5) / sp.Rational(12, 100), 13.411983, msg="100 mg まで 13.4 年")
near(M.subs(t, sp.log(5) / sp.Rational(12, 100)), 100, msg="13.41 年で 100 mg")
chk(float(sp.log(5) / sp.Rational(12, 100)) > float(2 * T),
    "13.4 > 11.6（半減期 2 回ぶんより後）")
in_text("T = \\frac{\\ln 2}{0.12} = 5.7762\\ldots = 5.78 \\text{ 年}")
in_text("t = \\frac{-\\ln 0.2}{0.12} = \\frac{\\ln 5}{0.12} = 13.41\\ldots = 13.4 \\text{ 年}")

# 半減期は M0 によらない（記号で）
M0, kk, TT = sp.symbols("M0 kk TT", positive=True)
sol = sp.solve(sp.Eq(M0 * sp.exp(-kk * TT), M0 / 2), TT)
chk(sol == [sp.log(2) / kk], "T = ln2/k（M0 が消える）")
# ★ 2026-08: M0 > 0 をモデルの条件として明示した
in_text("M = M_0\\,e^{-kt}, \\qquad M_0 > 0, \\quad k > 0", "M0>0, k>0 を式に明示")
in_text("**量を表すモデルなので、はじめの量 $M_0$ は正**とします。")
in_text("です。$M_0 > 0$ なので、両辺を $M_0$ で割れます。", "M0>0 だから割れる")
in_text("$M = \\dfrac{1}{2}M_0$ がどの時刻でも成り立ってしまい、**half-life が $1$ つに決まりません。**")
not_in_text("（$M_0 \\neq 0$ なので割れます）", "M0≠0 では足りない")
# M0 = 0 なら M(t) = 0 で、M = M0/2 がすべての t で成り立つ
chk(all(abs(0 * math.exp(-0.12 * t) - 0.5 * 0) < 1e-15 for t in range(0, 50)),
    "M0=0 なら M = M0/2 がすべての t で成り立つ")
# M0 > 0 なら、half-life は ln2/k の 1 つだけ
chk(len({round(math.log(2) / 0.12, 9)}) == 1, "M0>0 なら half-life は 1 つ")

# カフェイン
kc = sp.log(2) / 5
near(kc, 0.1386294361, msg="k = ln2/5")
chk(round(float(kc), 3) == 0.139, "k は 3 s.f. で 0.139")
A12 = 200 * sp.exp(-kc * 12)
near(A12, 37.89291416, msg="A(12) = 37.89")
near(200 * 2 ** sp.Rational(-12, 5), 37.89291416, msg="(1/2)^{t/T} でも同じ")
chk(sp.simplify(sp.exp(-sp.log(2) / TT * t) - (sp.Rational(1, 2)) ** (t / TT)) == 0,
    "e の形と (1/2)^{t/T} は同じ式（独立な検算ではない）")
in_text("$T$ そのものを問題文から読みまちがえていると、**両方とも同じだけずれます。**",
        "レビュー12: 2 つの道は独立でない")
not_in_text("**$2$ つの道で同じ数が出れば、まず間違っていません。**",
            "レビュー12: 独立だと思わせる書き方")
# ★ レビュー1: 丸めた k の影響
near(200 * sp.exp(-sp.Rational(139, 1000) * 12), 37.7247873, msg="丸めた k では 37.72")
in_text("$37.72$ mg、$k$ をそのまま使うと $37.89$ mg です。", "レビュー1")
in_text("$3$ s.f. の答えが $37.7$ mg と $37.9$ mg に分かれてしまいます", "レビュー1")
not_in_text("計算すると $37.86$ mg", "レビュー1: 誤った数値")
not_in_text("答えが $0.03$ mg ずれます", "レビュー1: 誤ったずれ幅")
near(200 * sp.exp(-kc * 12) - 200 * sp.exp(-sp.Rational(139, 1000) * 12),
     0.16812686, msg="ずれは 0.17 mg")
near(sp.log(10) / kc, 16.60964047, msg="20 mg まで 16.6 時間")

# 演習 1-4
near(sp.log(2) / sp.Rational(5, 100), 13.86294361, msg="演習1 13.9 日")
near(sp.log(2) / 12, 0.05776226505, msg="演習2 k = 0.0578")
near(300 * 2 ** sp.Rational(-15, 6), 53.03300859, msg="演習3 53.0 mg")
near(300 * sp.exp(-sp.log(2) / 6 * 15), 53.03300859, msg="演習3 e の形でも同じ")
near(sp.log(2) / 6, 0.1155245301, msg="演習3 k = 0.11552453")
near(300 * sp.exp(-sp.Rational(11552, 100000) * 15), 53.0366124,
     msg="丸めた k では 53.0366")
in_text("$k = \\dfrac{\\ln 2}{6} = 0.1155245\\ldots$", "レビュー11")
in_text("**丸めた $0.11552$ を打つと $53.0366$ になります。**", "レビュー11")
not_in_text("$k = \\dfrac{\\ln 2}{6} = 0.11552$ で", "レビュー11: 等号のない丸め")
not_in_text("$$300e^{-0.11552 \\times 15} = 53.033\\ldots$$", "レビュー11: 合わない式")
not_in_text("200e^{-0.13862 \\times 12} = 37.892", "レビュー11: 合わない式")
in_text("$A_0 > 0$ and $k > 0$", "レビュー8: 演習4 の条件")
in_text("*Dividing both sides by $A_0$, which is not zero:*", "レビュー8")

# ══════════════════════════════════════════════════════════
# 2. 自然対数モデル
# ══════════════════════════════════════════════════════════
b = 6 / sp.log(4)
a = 7 - b * sp.log(2)
near(a, 4, msg="a = 4（ちょうど）")
near(b, 4.328085123, msg="b = 4.33")
near(a + b * sp.log(8), 13, msg="f(8) = 13")
near(a + b * sp.log(20), 16.96578428, msg="f(20) = 17.0")
chk(round(float(a + b * sp.log(20)), 1) == 17.0, "3 s.f. で 17.0")
near(a + sp.Rational(433, 100) * sp.log(20), 16.97152074,
     msg="丸めた b では 16.9715（3 s.f. は同じ）")
in_text("h(20) = 4 + \\frac{6}{\\ln 4}\\ln 20 = 17.0", "レビュー21: 丸めない解答例")
not_in_text("$$h(20) = 4 + 4.33\\ln 20 = 17.0 \\text{ cm}$$", "レビュー21")
near(3 + 5 * sp.log(4), 9.931471806, msg="演習5 f(4) = 9.93")
near(sp.exp(sp.Rational(17, 5)), 29.96410005, msg="演習5 x = 30.0")
chk(round(float(sp.exp(sp.Rational(17, 5))), 1) == 30.0, "3 s.f. で 30.0")
near(8 / sp.log(5), 4.970679476, msg="演習6 b = 4.97")
chk(sp.log(1) == 0, "ln 1 = 0")
# domain
chk(sp.limit(sp.log(x), x, 0, "+") == -sp.oo, "x→0+ で ln x → -∞")
# ★ 2026-08: b の符号で増減を分け、b=0 も関数として認める
in_text("@fig-ahl29a-decay の (b) は **$b > 0$ の場合**です。")
in_text("**$b < 0$ ならグラフの上下が反転します。** はじめは急に下がり、そのあと下がり方が緩やかになります。")
in_text("$b = 0$ なら $f(x) = a$ という **constant function**（定数関数）になり、$x$ による変化を表さないモデルになります。")
not_in_text("（$b = 0$ なら定数で、モデルになりません）", "b=0 を「モデルでない」と言わない")
not_in_text("**はじめは急に上がり、そのあと伸びが鈍っていきます。** ただし、上限はありません。伸び続けます。",
            "b>0 に限定していない旧文")
# b の符号と増減（数値で確かめる）
for _b, _label in ((2.0, "increasing"), (-2.0, "decreasing"), (0.0, "constant")):
    _v = [5 + _b * math.log(x) for x in (0.5, 1, 2, 5, 20)]
    _inc = all(a < b for a, b in zip(_v, _v[1:]))
    _dec = all(a > b for a, b in zip(_v, _v[1:]))
    _con = all(abs(a - _v[0]) < 1e-12 for a in _v)
    chk({"increasing": _inc, "decreasing": _dec, "constant": _con}[_label],
        "b=%g は %s" % (_b, _label))
# 増え方は緩やかになる（b>0 のとき差が縮む）
_d = [(5 + 2 * math.log(x + 1)) - (5 + 2 * math.log(x)) for x in (1, 2, 4, 8, 16)]
chk(all(a > b for a, b in zip(_d, _d[1:])), "b>0 では増え方が緩やかになる")
in_text("Since the number of words increases with age, $b > 0$", "レビュー15")

# ══════════════════════════════════════════════════════════
# 3. 正弦モデル
# ══════════════════════════════════════════════════════════
h = 8 * sp.sin(sp.pi / 6 * (t - 2)) + 12
chk(sp.periodicity(h, t) == 12, "period = 2π/(π/6) = 12")
near(h.subs(t, 5), 20, msg="最大 20 は t=5")
near(h.subs(t, 11), 4, msg="最小 4 は t=11")
near(h.subs(t, 0), 5.07179677, msg="h(0) = 5.07")
chk((20 - 4) / 2 == 8 and (20 + 4) / 2 == 12, "a=8, d=12")
chk(2 * abs(11 - 5) == 12, "period = 2|max時刻 − min時刻|")
near(2 / (sp.pi / 6), 3.819718634, msg="bt-c の shift は 3.82")
chk(sp.simplify(sp.pi / 6 * t - 2 - sp.pi / 6 * (t - 12 / sp.pi)) == 0,
    "π/6 t − 2 = π/6 (t − 12/π)")
# ★ レビュー2: period の式は絶対値つき、隣接条件つき
in_text("\\text{period} = 2 \\times \\lvert \\text{最大の時刻} - \\text{最小の時刻} \\rvert",
        "レビュー2")
in_text("**となり合う最大と最小のあいだが、ちょうど半周期**", "レビュー2")
not_in_text("\\text{period} = 2 \\times (\\text{最大の時刻} - \\text{最小の時刻})",
            "レビュー2: 符号が逆になる式")
near(h.subs(t, 23), 4, msg="t=23 も最小（隣接でない反例）")
chk(2 * abs(23 - 5) != 12, "隣接でない最大最小では周期が出ない")
# ★ レビュー6: b > 0 の条件
chk(sp.periodicity(sp.sin(-2 * x), x) == sp.pi, "sin(-2x) の周期は π")
in_text("$\\sin(-2x)$ の period は $\\pi$ で、$\\dfrac{2\\pi}{-2} = -\\pi$ ではありません",
        "レビュー6")
in_text("period $= \\dfrac{2\\pi}{b}$（$b > 0$）", "レビュー6: 表の条件")
# ★ レビュー7: a > 0 の条件
alt = -8 * sp.sin(sp.pi / 6 * (t - 8)) + 12
near(alt.subs(t, 5), 20, msg="a<0 の別表現でも最大 20 は t=5")
near(alt.subs(t, 11), 4, msg="a<0 の別表現でも最小 4 は t=11")
in_text("**以下、$a > 0$、$b > 0$ にとります。**", "レビュー7")
in_text("\\lvert a \\rvert = \\frac{\\text{最大} - \\text{最小}}{2}", "レビュー7")
in_text("$-8\\sin\\left(\\dfrac{\\pi}{6}(t-8)\\right)+12$ は、同じグラフです", "レビュー7")
in_text("$a > 0$、$b > 0$ のとき、$c$ は", "レビュー7")
# ★ レビュー16: c < 0 なら左
in_text("$c > 0$ なら右に $c$、$c < 0$ なら左に $\\lvert c \\rvert$ です", "レビュー16")
# 演習 8, 9, 10
h8 = 6 * sp.sin(sp.pi / 4 * (t - 1)) + 10
chk(sp.periodicity(h8, t) == 8, "演習8 period = 8")
near(h8.subs(t, 3), 16, msg="演習8 最大 16 は t=3")
near(360 / (sp.pi / 4), 458.3662361, msg="演習8 誤った 360/b は 458")
T9 = 7 * sp.sin(sp.pi / 12 * (t - 8)) + 19
near(T9.subs(t, 14), 26, msg="演習9 最高 26 は t=14")
near(T9.subs(t, 2), 12, msg="演習9 最低 12 は t=2")
chk(sp.periodicity(T9, t) == 24, "演習9 period = 24")
near(2 * sp.pi / 3, 2.094395102, msg="演習10 period = 2.09")
h10 = 5 * sp.sin(3 * t) + 2
near(h10.subs(t, sp.pi / 3), 2, msg="半周期でも h = 2（検算にならない）")
near(h10.subs(t, sp.Rational(1, 2)), 6.987474933, msg="t=0.5 で 6.99")
near(h10.subs(t, sp.Rational(1, 2) + 2 * sp.pi / 3), 6.987474933,
     msg="1 周期後も 6.99")
near(h10.subs(t, sp.Rational(1, 2) + sp.pi / 3), -2.987474933,
     msg="半周期後は -2.99")
in_text("半分の $1.047$ だけ進めると $-2.99$ で、もどっていません", "レビュー5")
not_in_text("$t = 2.0944$ で $h = 5\\sin(2\\pi)+2 = 2$ ✓ ちょうど $1$ 周してもどりました",
            "レビュー5: 半周期でも通る検算")
# ★ レビュー4: 度の記号の見分け方
in_text("**見分け方は、$\\sin$ の中の角に度の記号 $^{\\circ}$ が付いているかどうか**です",
        "レビュー4")
in_text("摂氏の $^{\\circ}\\text{C}$ は角の単位ではないので", "レビュー4")
not_in_text("**見分け方は、度の記号 $^{\\circ}$ があるかどうか**です", "レビュー4")
chk("^{\\circ}\\text{C}" in TEXT, "演習9 は摂氏を使っている")

# ══════════════════════════════════════════════════════════
# 4. GDC
# ══════════════════════════════════════════════════════════
in_text("doc → Settings → Document Settings", "角の設定")
in_text("ctrl + doc → 2: Add Graphs", "ページ追加")
in_text("menu → Analyze Graph → Intersection", "交点")
in_text("`ctrl` を押してから `var` キーで入ります", "レビュー9: sto キー")
not_in_text("**sto** キー（`ctrl` の下あたりの矢印キー）", "レビュー9")
in_text("## `e` と `π` は、キーで入れてください", "レビュー18")
in_text("### 3. 方程式は、graph の交点で解くのが確実です", "レビュー17")
in_text("CAS ではない CX II に `solve(` はありません", "レビュー17")
not_in_text("### 3. 方程式は Solve より graph の交点が確実です", "レビュー17")
in_text("`Zoom - Fit` は、**いまの $x$ の範囲に合わせて $y$ の範囲だけを合わせます。**",
        "レビュー10")
not_in_text("`Zoom - Fit` だけだと $y$ 方向が詰まって", "レビュー10")
in_text("電卓に $k$ という名前で保存しておく", "レビュー19: コードスパンに数式を入れない")

# ══════════════════════════════════════════════════════════
# 5. シラバス・公式集
# ══════════════════════════════════════════════════════════
in_text("## 公式集の AHL 2.9 の欄\n**$1$ 行だけあります。**")
in_text("**このページの $3$ つのモデルは、$1$ つも印刷されていません。**")
in_text("Content 欄は、導入の $1$ 行と、$5$ つのモデルからできています。")
in_text("Guidance 欄のうち、このページに関わるのは次の $5$ つです。")
in_text("Exponential models to calculate half-life.")
in_text("Natural logarithmic models: $f(x) = a + b\\ln x$")
in_text("Sinusoidal models: $f(x) = a\\sin\\bigl(b(x-c)\\bigr)+d$")
in_text("In radians, period is $\\dfrac{2\\pi}{b}$.")
in_text("**Natural logarithmic models の行は、Guidance 欄に対応する記述がありません。**")
in_text("Guidance の `Link to: modelling skills (SL2.6)` は、この項目全体にかかっています",
        "レビュー13")
not_in_text("シラバスの Guidance が `Link to: modelling skills (SL2.6)` と書いているとおり",
            "レビュー13")
not_in_text("Connections 欄が挙げている pH scale", "レビュー3: 帰属の取りちがえ")

# ══════════════════════════════════════════════════════════
# 6. 構造
# ══════════════════════════════════════════════════════════
heads = re.findall(r"(?m)^## (.+)$", TEXT)
need = ["What you should be able to do", "The idea", "Why it works",
        "Worked examples", "Common errors",
        "Using your GDC (TI-Nspire CX II)", "Exercises"]
for hh in need:
    chk(hh in heads, "見出しがない: " + hh)
chk([hh for hh in heads if hh in need] == need, "7 つの見出しの順序")
chk(len(re.findall(r"(?m)^---$", TEXT)) == 6, "--- は 6 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳は 14 個")
chk(TEXT.count("::: {.ex-sep}") == 9, ".ex-sep は 9 個")
chk(len(re.findall(r"::: \{#exm-ahl29a-[\w-]+\}", TEXT)) == 4, "worked example は 4 個")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習は 1..10 の連番")
idea = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(idea == [str(i) for i in range(1, 9)] + [str(i) for i in range(1, 6)],
    "The idea 1..8 と GDC 1..5 の連番: " + str(idea))
chk(TEXT.count("::: {.model-answer}") == 6, "model-answer は 6 個")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "確かめ。", "そのとおり"]:
    not_in_text(w, "禁止表現")
chk(TEXT.count("**検算。**") == 13, "検算。の個数: " + str(TEXT.count("**検算。**")))
for term in ["**half-life**（半減期）", "**natural logarithmic model**（自然対数モデル）",
             "**sinusoidal model**（正弦モデル）", "**amplitude**（振幅）",
             "**phase shift**（位相のずれ）", "**principal axis**（中心線）",
             "**vertical asymptote**（垂直漸近線）", "period（周期）",
             "domain（定義域）"]:
    in_text(term, "英語→日本語の順")
in_text("![Half-life, and a natural logarithmic model](img/ahl-2-9a-decay.svg)")
in_text("![The four letters of a sinusoidal model](img/ahl-2-9a-sine.svg)")
for svg in ["ahl-2-9a-decay.svg", "ahl-2-9a-sine.svg"]:
    chk(os.path.exists(os.path.join(HERE, "..", "..", "ai-hl", "02-functions",
                                    "img", svg)), "図がある: " + svg)
anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT)) | {"common-errors", "why-it-works"}
for anc in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(anc in anchors, "内部アンカーがない: #" + anc)
for m in re.findall(r"`[^`\n]*`", TEXT):
    chk("$" not in m, "コードスパンに $ が入っている: " + m[:50])
in_text("[AHL 2.9b](ahl-2-9b.qmd)", "対になるページへのリンク")
chk("@sec-" not in TEXT, "他ページを @ で参照していない")


# レビューで追加: 使いどころの記述も b>0 に限定
in_text("@eq-ahl29a-log の（$b > 0$ のときの）使いどころは、"
        "**「増えるけれど、だんだん増え方が鈍る」**場面です。")
not_in_text("@eq-ahl29a-log の使いどころは、"
            "**「増えるけれど、だんだん増え方が鈍る」**場面です。")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
