"""AHL 2.9b（ロジスティックモデル・区分モデル）の内容を検算する。

    python3 figs/ai-hl/check_ahl_2_9b.py
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "02-functions", "ahl-2-9b.qmd")
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


t, x, h = sp.symbols("t x h", real=True)
L, C, k = sp.symbols("L C k", positive=True)

# ══════════════════════════════════════════════════════════
# 1. logistic の一般論
# ══════════════════════════════════════════════════════════
f = L / (1 + C * sp.exp(-k * x))
chk(sp.limit(f, x, sp.oo) == L, "x→∞ で L に近づく")
chk(sp.limit(f, x, -sp.oo) == 0, "x→-∞ で 0 に近づく")
chk(sp.solve(sp.Eq(f, L), x) == [], "f = L に解はない（達しない）")
chk(sp.simplify(f.subs(x, 0) - L / (1 + C)) == 0, "f(0) = L/(1+C)")
P0 = sp.Symbol("P0", positive=True)
chk(sp.simplify(sp.solve(sp.Eq(L / (1 + C), P0), C)[0] - (L / P0 - 1)) == 0,
    "C = L/f(0) − 1")
x0 = sp.log(C) / k
chk(sp.simplify(f.subs(x, x0) - L / 2) == 0, "x0 = lnC/k で L/2")
chk(sp.simplify(f.subs(x, x0 + h) + f.subs(x, x0 - h) - L) == 0,
    "点対称: f(x0+h)+f(x0-h) = L")
d2 = sp.simplify(sp.diff(f, x, 2))
chk(sp.solve(sp.Eq(d2, 0), x) == [sp.log(C) / k], "f'' = 0 は x0 だけ（いちばん急）")
chk(float(sp.log(sp.Rational(1, 2)) / sp.Rational(1, 2)) < 0,
    "C < 1 なら lnC/k は負（S の曲がり角が x<0）")
in_text("S の曲がり角が $x > 0$ に来るのは **$C > 1$**", "レビュー10")
in_text("$\\dfrac{\\ln C}{k}$ が正になるのは **$C > 1$** のときです", "レビュー10")
in_text("$L > 0$、$C > 0$、$k > 0$ なので（公式集の条件です）", "レビュー18")
not_in_text("$k > 0$、$C > 0$ なので、$Ce^{-kx}$ は**正の数**で", "レビュー18")
in_text("**$L$ と $C$ が同じなら、上限に速く近づく**", "レビュー7")
not_in_text("**上限まで速く到達する**、ということです", "レビュー7")
in_text("**$x$ を負にできる「関数として見たとき」の話**です", "レビュー16")

# 分母の定数項が 1 でない形（レビュー9）
g = 6000 / (2 + 3 * sp.exp(-sp.Rational(1, 2) * t))
chk(sp.limit(g, t, sp.oo) == 3000, "6000/(2+3e^-0.5t) の L は 3000")
near(g.subs(t, 0), 1200, msg="その P(0) は 1200")
in_text("$P = \\dfrac{6000}{2+3e^{-0.5t}}$ のように分母の定数項が $1$ でなければ",
        "レビュー9")
in_text("**$L = 3000$ で、$6000$ ではありません。**", "レビュー9")
not_in_text("**分子をそのまま読めば $L$ です。**", "レビュー9")
not_in_text("**分子をそのまま読めばよい**、と覚えておいてください", "レビュー9")

# ══════════════════════════════════════════════════════════
# 2. 魚の例
# ══════════════════════════════════════════════════════════
P = 2000 / (1 + 9 * sp.exp(-sp.Rational(3, 10) * t))
near(P.subs(t, 0), 200, msg="P(0) = 200")
chk(2000 / 200 - 1 == 9, "C = 9")
near(P.subs(t, 5), 664.8557235, msg="P(5) = 665")
chk(round(float(P.subs(t, 5))) == 665, "整数で 665")
th = sp.log(9) / sp.Rational(3, 10)
near(th, 7.324081924, msg="L/2 は t = 7.32")
near(P.subs(t, th), 1000, msg="そこで 1000")
t18 = sp.log(81) / sp.Rational(3, 10)
near(t18, 14.64816385, msg="1800 に達するのは 14.6 年")
near(P.subs(t, t18), 1800, msg="検算 1800")
chk(round(float(t18), 1) == 14.6, "3 s.f. で 14.6")
in_text("t = \\frac{\\ln 81}{0.3} = 14.648\\ldots = 14.6 \\text{ 年}")

# exponential との比較（レビュー11）
Ex = 200 * sp.exp(sp.Rational(3, 10) * t)
near(P.subs(t, 1), 260.8458, msg="t=1 logistic 261")
near(Ex.subs(t, 1), 269.9718, msg="t=1 exponential 270")
near(P.subs(t, 2), 336.7398, msg="t=2 logistic 337")
near(Ex.subs(t, 2), 364.4238, msg="t=2 exponential 364")
near(P.subs(t, 4), 538.9749, msg="t=4 logistic 539")
near(Ex.subs(t, 4), 664.0234, msg="t=4 exponential 664")
chk(float(Ex.subs(t, 4) / P.subs(t, 4)) > 1.2, "t=4 で 2 割以上ちがう")
in_text("$t = 4$ ではもう $539$ と $664$ で、$2$ 割以上ちがいます", "レビュー11")
not_in_text("**はじめのうちは、ほとんど同じ**です。", "レビュー11")

# 細菌の例
kb = sp.Rational(1, 4) * sp.log(sp.Rational(7, 2))
near(kb, 0.3131917, msg="k = 0.313")
B = 1200 / (1 + 7 * sp.exp(-kb * t))
near(B.subs(t, 0), 150, msg="B(0) = 150")
near(B.subs(t, 4), 400, msg="B(4) = 400")
chk(1200 / 150 - 1 == 7, "C = 7")

# 演習
Q = 500 / (1 + 4 * sp.exp(-sp.Rational(2, 10) * t))
near(Q.subs(t, 0), 100, msg="演習1 P(0) = 100")
tq = sp.log(4) / sp.Rational(2, 10)
near(tq, 6.931471806, msg="演習2 6.93 年")
near(Q.subs(t, tq), 250, msg="演習2 検算 250")
chk(float(tq) > 0, "演習2 C=4>1 なので lnC/k は正")
chk(1200 / 150 - 1 == 7, "演習3 C = 7")
R = 8000 / (1 + 15 * sp.exp(-sp.Rational(1, 4) * t))
near(R.subs(t, 10), 3585.394034, msg="演習4 N(10) = 3585")
tr = sp.log(45) / sp.Rational(1, 4)
near(tr, 15.22664996, msg="演習4 15.2 日")
near(R.subs(t, tr), 6000, msg="演習4 検算 6000")
near(sp.log(15) / sp.Rational(1, 4), 10.83226, msg="L/2 は 10.8 日（15.2 より前）")
chk(float(tr) > float(sp.log(15) / sp.Rational(1, 4)), "15.2 > 10.8")
in_text("**$3$ s.f. で答えるなら $3590$ 人**です", "レビュー17")
P10 = 3000 / (1 + 5 * sp.exp(-sp.Rational(4, 10) * t))
near(P10.subs(t, 0), 500, msg="演習10 P(0) = 500")
chk(sp.limit(P10, t, sp.oo) == 3000, "演習10 L = 3000")
near(P10.subs(t, 30), 2999.90814, msg="演習10 t=30 で 2999.9")
in_text("that $P(t)$ approaches as $t$ increases", "レビュー8")
not_in_text("the horizontal asymptote reached as $t$ increases", "レビュー8")

# ══════════════════════════════════════════════════════════
# 3. piecewise
# ══════════════════════════════════════════════════════════
a = sp.Symbol("a")
chk(sp.solve(sp.Eq(1 + 2, a * 2 ** 2 + 2), a) == [sp.Rational(1, 4)],
    "シラバスの Example: a = 1/4")
near(sp.Rational(1, 4) * 16 + 4, 8, msg="f(4) = 8")
near(1 * 4 + 2 - 3, 3, msg="a = 1 なら 3 のとび")
kk = sp.Symbol("kk")
chk(sp.solve(sp.Eq(3 * 2 + 1, kk * 2 ** 2 - 1), kk) == [2], "演習7 k = 2")
chk(sp.solve(sp.Eq(5 - 3, a * sp.sqrt(3 + 1)), a) == [1], "演習8 a = 1")
chk(2 * 3 + 1 == 7 and 10 - 3 == 7, "演習6 x=3 でどちらも 7")
chk(sp.diff(2 * x + 1, x) == 2 and sp.diff(10 - x, x) == -1,
    "演習6 傾きは 2 と -1（continuous だが角がある）")
near(20 + 3 * (9 - 5), 32, msg="C(9) = 32")
chk(sp.solve(sp.Eq(20 + 3 * (x - 5), 41), x) == [12], "C = 41 なら 12 GB")
near(20 + 3 * (5 - 5), 20, msg="x=5 でどちらも 20")
near(20 + 3 * (3 - 5), 14, msg="誤って下の式を使うと 14")
near(1.2 + sp.Rational(15, 100) * (15 - 8), 2.25, msg="演習9 d(15) = 2.25")
near(1.2 + sp.Rational(15, 100) * (20 - 8), 3, msg="演習9 d(20) = 3")
# ★ レビュー2: continuity の検算
in_text("**検算。** $x = 2$ で、$2$ つの式が同じ値を出すかを見ます。上の式は $1+2 = 3$",
        "レビュー2")
not_in_text("$f(2.1) = \\dfrac{1}{4}(4.41)+2.1 = 3.2025$", "レビュー2: 通ってしまう検算")
near(sp.Rational(26, 100) * 4 + 2 - 3, 0.04, msg="a=0.26 でも 0.04 のとびがある")
# ★ レビュー3: GDC の検算
in_text("どちらも $3$ です ✓ **同じ数がぴったり出るかどうか**が判定です", "レビュー3")
not_in_text("$2.999$ と $3$ で、ほぼ同じです", "レビュー3")
# ★ レビュー4: 定数の数と方程式の数
in_text("**「定数の数だけ方程式ができる」とはかぎりません。**", "レビュー4")
in_text("$a$ が両方に入っているので $a+1 = a+2$ となり", "レビュー4")
not_in_text("だから、未知の定数が $1$ つなら、方程式も $1$ つで足ります。", "レビュー4")
chk(sp.solve(sp.Eq(a + 1, a + 2), a) == [], "a+1 = a+2 に解はない")
# ★ レビュー5: 関数かどうか
in_text("どちらの区間にも入らない $x$ があるのは、関数として構いません", "レビュー5")
not_in_text("どちらにも入っていない値があったりする式は、関数になりません", "レビュー5")
# ★ レビュー6: 境目に入れられない式
in_text("**計算できない式**（分母が $0$、根号の中が負など）が混じっているときだけは",
        "レビュー6")
# ★ レビュー1: piecewise の条件は and
in_text("f1(x)=piecewise(1+x,x≥0 and x<2,x^2/4+x,x≥2)", "レビュー1")
in_text("**条件を $0 \\leq x < 2$ のようにつなげて書くことはできません。**", "レビュー1")
not_in_text("f1(x)=piecewise(1+x,0≤x<2,x^2/4+x,x≥2)", "レビュー1: 通らない構文")
# ★ レビュー13: 演習6 の警告
in_text("**$f(3)$ の値を決めるのは下の式です。**", "レビュー13")
not_in_text("**$f(3)$ で上の式を使わないでください。**", "レビュー13")
# ★ レビュー19: §6 に式を先に出す
chk(TEXT.index("20 + 3(x-5), & x > 5") < TEXT.index("C(3) = 20 \\quad"),
    "レビュー19: 式が C(3) の前にある")
# ★ レビュー20: window
in_text("**既定の window のままだと $f1$ も $f2$ も画面の外**", "レビュー20")
# ★ レビュー14: 検証できない主張
not_in_text("この項目でいちばんよく出る設問です", "採点・出題頻度の主張")
not_in_text("ここを取りちがえるのが、この項目でいちばん多い誤りです", "同上")

# ══════════════════════════════════════════════════════════
# 4. シラバス・公式集
# ══════════════════════════════════════════════════════════
in_text("## 公式集の AHL 2.9 の欄\n**$1$ 行あります。** logistic function です。")
in_text("piecewise model のほうは、公式集にありません。")
in_text("**式は配られるので、覚える必要はありません。**")
in_text("Logistic models: $f(x) = \\dfrac{L}{1+Ce^{-kx}}$; $L$, $C$, $k > 0$")
in_text("> Piecewise models.")
in_text("Guidance 欄で、logistic に付いているのは $2$ つです。")
in_text("piecewise に付いているのは $3$ つです。")
in_text("The formal definition of continuity is not required.")
in_text("このほかに、項目全体にかかる `Link to: modelling skills (SL2.6)` があります",
        "レビュー12b")
in_text("**この項目（AHL 2.9）では、解くことも覚えることも求められません。**",
        "レビュー12a")
in_text("C = \\dfrac{L}{P_0}-1", "Enrichment の C")

# ══════════════════════════════════════════════════════════
# 5. 構造
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
chk(len(re.findall(r"::: \{#exm-ahl29b-[\w-]+\}", TEXT)) == 4, "worked example は 4 個")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習は 1..10 の連番")
idea = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(idea == [str(i) for i in range(1, 9)] + [str(i) for i in range(1, 6)],
    "The idea 1..8 と GDC 1..5 の連番: " + str(idea))
chk(TEXT.count("::: {.model-answer}") == 5, "model-answer は 5 個")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "確かめ。", "そのとおり"]:
    not_in_text(w, "禁止表現")
chk(TEXT.count("**検算。**") == 10, "検算。の個数: " + str(TEXT.count("**検算。**")))
for term in ["**logistic model**（ロジスティックモデル）",
             "**carrying capacity**（環境収容力）",
             "**horizontal asymptote**（水平漸近線）",
             "**piecewise model**（区分モデル）",
             "**continuous**（つながっている）",
             "**point of inflexion**（変曲点）",
             "smooth（なめらか）"]:
    in_text(term, "英語→日本語の順")
in_text("![Reading a logistic model, and comparing it with an exponential](img/ahl-2-9b-logistic.svg)")
in_text("![Continuity, and a piecewise model in context](img/ahl-2-9b-piecewise.svg)")
for svg in ["ahl-2-9b-logistic.svg", "ahl-2-9b-piecewise.svg"]:
    chk(os.path.exists(os.path.join(HERE, "..", "..", "ai-hl", "02-functions",
                                    "img", svg)), "図がある: " + svg)
anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT)) | {"common-errors", "why-it-works"}
for anc in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(anc in anchors, "内部アンカーがない: #" + anc)
for m in re.findall(r"`[^`\n]*`", TEXT):
    chk("$" not in m, "コードスパンに $ が入っている: " + m[:50])
in_text("[AHL 2.9a](ahl-2-9a.qmd)", "対になるページへのリンク")
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
chk(TEXT.count("\\begin{cases}") == TEXT.count("\\end{cases}"), "cases の対応")


# ══════════════════════════════════════════════════════════
#  2026-08 の修正: L は達する maximum ではない
# ══════════════════════════════════════════════════════════
in_text("ですから、有限の $x$ に対して $f(x) < L$ です。")
in_text("**ですから、数学的には $f$ に maximum（最大値）はありません。**")
in_text("$L$ は **upper bound**（上界）であり、$x$ が大きくなるにつれて近づいていく "
        "**limiting value**（極限値）です。")
in_text("モデルの文脈では、この $L$ を **carrying capacity**、"
        "つまり実質的な上限として解釈します。")
in_text("**「最大値」ではなく「到達しない上限」**——これが $L$ の正体です。")
not_in_text("`Find the maximum population` と問われたら、"
            "答えは「$2000$ に近づくが達しない」という意味で $2000$ です。",
            "L を maximum と呼んでいた旧文")
# 問われ方と答え方の表
in_text("| `State the carrying capacity` | $L$ |")
in_text("| `State the limiting population` | $L$ |")
in_text("| `State the horizontal asymptote` | $y = L$ |")
in_text("| `Find when the population reaches L` | そのような有限の時刻は**存在しません** |")
in_text(": 問われ方と答え方 {#tbl-ahl29b-ask}")
chk("@tbl-ahl29b-ask" in TEXT, "表が参照されている")
# 有限の x では f(x) < L（達しない）ことを、丸めのない厳密計算で確かめる
import sympy as _sp
_t = _sp.symbols("t", real=True)
_P = _sp.Integer(2000) / (1 + 9 * _sp.exp(_sp.Rational(-3, 10) * _t))
for _v in (0, 1, 10, 50, 200, 1000):
    chk(_sp.simplify(_P.subs(_t, _v) - 2000) < 0, "t=%g で P(t) < 2000（厳密）" % _v)
chk(_sp.simplify(2000 - _P) > 0, "すべての実数 t で P(t) < 2000")
chk(_sp.limit(_P, _t, _sp.oo) == 2000, "t → ∞ の極限値は 2000")
chk(_sp.solve(_sp.Eq(_P, 2000), _t) == [],
    "P(t) = 2000 となる有限の t は存在しない")
# 上限であって最大値ではない: 2000 未満のどの値も、いつかは超えられる
for _target in (1999, _sp.Rational(19999, 10)):
    chk(_sp.solve(_sp.Eq(_P, _target), _t) != [],
        "P(t) = %s には解がある（2000 に「いくらでも近づく」）" % _target)


# レビューで追加: 定義域が閉区間なら maximum は存在しうる
in_text("| `Find the maximum` | （$x$ に上限がないかぎり）厳密には maximum は存在せず、"
        "**到達しない上限**が $L$ です |")
# 閉区間 [0, 10] では最大値が存在し、右端で取る
_vals = [float(_P.subs(_t, _v)) for _v in range(0, 11)]
chk(max(_vals) == _vals[-1], "閉区間 [0,10] なら最大値は右端で取る")
chk(max(_vals) < 2000, "その最大値も 2000 未満")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
