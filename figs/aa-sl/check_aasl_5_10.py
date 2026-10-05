# -*- coding: utf-8 -*-
"""AA SL 5.10 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_10.py

このページは、2026-09-29 に SL 5.10a と SL 5.10b をまとめて作ったものです。
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-10.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_10.py")

TEXT = open(QMD, encoding="utf-8").read()
FIG = open(FIGP, encoding="utf-8").read()
FIGCODE = FIG.split('"""', 2)[-1]

OK = 0
NG = 0


def chk(cond, msg=""):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: %s :: %s" % (msg, sub[:60]))


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: %s :: %s" % (msg, sub[:60]))


def in_fig(sub, msg=""):
    chk(sub in FIG, "図に見つからない: %s :: %s" % (msg, sub[:60]))


X = sp.Symbol("x", positive=True)
XR = sp.Symbol("x", real=True)


def anti(F, f, v=X, msg=""):
    """F を微分すると f になる（＝ F は f の原始関数）。"""
    chk(sp.simplify(sp.diff(F, v) - f) == 0,
        "%s :: d/dx(%s) != %s" % (msg, F, f))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
in_text("# SL 5.10 — Standard integrals, reverse chain rule and substitution"
        "（標準的な不定積分・逆連鎖律・置換積分） {#sec-aasl-5-10}", "ページの題")
for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d+)\. (.*) \{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 9)],
    "### の番号 1..8: %s" % [s[0] for s in _secs])
chk([s[2] for s in _secs] == ["standard", "rational", "linear",
                              "inspection", "logform", "constant",
                              "substitution", "choose"],
    "アンカー: %s" % [s[2] for s in _secs])
for _n, _t, _ in _secs:
    chk(re.match(r"^[a-z]", _t), "見出し %s は英語で始まる: %s" % (_n, _t))

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk([int(x) for x in re.findall(r"^\[(\d+)\]\{\.ex-no\}", TEXT, re.M)]
    == list(range(1, 11)), "演習の番号が 1..10")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14 個")
chk(TEXT.count("## 解答例") == 14, "解答例 14 個")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭の --- は 6 本")
chk(TEXT.count("**検算") >= 12, "検算は 12 本以上: %d" % TEXT.count("**検算"))
chk(TEXT.count(":::") % 2 == 0, "::: の数が偶数")
chk("\n\n\n" not in TEXT, "空行が 2 つ続いていない")
for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)
for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

# ══════════════════════════════════════════════════════════
# 2. 式・表・図・参照
# ══════════════════════════════════════════════════════════
for _e in ("{#eq-aasl510-power}", "{#eq-aasl510-ln}", "{#eq-aasl510-trig}",
           "{#eq-aasl510-exp}", "{#eq-aasl510-linear}", "{#eq-aasl510-form}",
           "{#eq-aasl510-du}",
           "{#eq-aasl510-log}", "{#eq-aasl510-tan}"):
    in_text(_e, "式 " + _e)
for _t in ("{#tbl-aasl510-rational}", "{#tbl-aasl510-linear}",
           "{#tbl-aasl510-constant}"):
    in_text(_t, "表 " + _t)
for _f, _i in (("aasl-5-10-linear.svg", "fig-aasl510-linear"),):
    in_text("(img/%s){#%s width=100%%}" % (_f, _i), "図 " + _f)
    chk(os.path.exists(os.path.join(os.path.dirname(QMD), "img", _f)),
        "SVG がある: " + _f)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)
chk(not re.search(r"aasl-5-10[ab]", TEXT), "5.10a / 5.10b へのリンクは残っていない")
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a + "}") in TEXT or ("{#" + _a + " ") in TEXT
        or _a == "why-it-works", "ページ内リンクの行き先がある: #" + _a)
for _cm in re.finditer(r"^!\[(.*?)\]\(img/", TEXT, re.M):
    chk(0 < len(_cm.group(1)) <= 75,
        "図のキャプションは 75 字以内（%d 字）" % len(_cm.group(1)))

# ══════════════════════════════════════════════════════════
# 3. 2026-09-29：5.10a + 5.10b をまとめたときの決めごと
# ══════════════════════════════════════════════════════════
# 消した節
for _s in ("{#lnabs}", "{#signs}", "{#notlinear}", "{#tbl-aasl510-signs}",
           "### 3. $\\dfrac{1}{x}$ と絶対値", "### 4. $\\sin$ と $\\cos$ の符号",
           "### 7. この形が使えないとき", "aasl-5-10a-idea-a"):
    not_in_text(_s, "5.10a から消した: " + _s)
chk(not os.path.exists(os.path.join(os.path.dirname(QMD), "img",
                                    "aasl-5-10a-idea-a.svg")),
    "ln|x| の図は消した")
for _p in ("aasl-5-10a.qmd", "aasl-5-10b.qmd"):
    chk(not os.path.exists(os.path.join(os.path.dirname(QMD), _p)),
        "もとのページは消した: " + _p)
# 1/x の注意は第 1 節に 1 つだけ
in_text("**$\\dfrac{1}{x}$ だけは @eq-aasl510-power が使えません**"
        "（$n = -1$ とすると $0$ で割ることになります）。"
        "**絶対値が付いているのは $x < 0$ の側もふくめるためで、"
        "定義域が $x > 0$ と分かっているときは $\\ln x$ と書いてかまいません。**",
        "1/x の注意")
chk(TEXT.index("**$\\dfrac{1}{x}$ だけは @eq-aasl510-power が使えません**")
    < TEXT.index("### 2. rational exponents"), "1/x の注意は第 1 節の中")
# 「最後に微分して確かめる」は第 3 節の終わりに
in_text("**最後に、必ず微分して確かめてください。**", "微分して確かめる")
_i3 = TEXT.index("### 3. composing with $ax + b$")
_i4 = TEXT.index("### 4. reverse chain rule")
chk(_i3 < TEXT.index("**最後に、必ず微分して確かめてください。**") < _i4,
    "第 3 節の終わりにある")
# 5.10b はそのままつないである
in_text("### 4. reverse chain rule（chain rule の逆を考える） "
        "{#inspection}", "第 4 節")
in_text("### 8. choosing $u$（$u$ の選び方） {#choose}", "第 8 節")
_i10 = TEXT.index("### 8. choosing $u$（$u$ の選び方） {#choose}")
_iw = TEXT.index(chr(10) + "## Why it works")
_s10 = TEXT[_i10:_iw]
chk("## この項目は電卓なしで解きます" in _s10, "Paper の callout は第 8 節に")
chk(_s10.count("### ") == 1, "第 8 節が The idea の最後")
chk(_s10.count(":::") % 2 == 0, "第 8 節の ::: が閉じている")

# ══════════════════════════════════════════════════════════
# 4. 第 1〜3 節の公式
# ══════════════════════════════════════════════════════════
_n = sp.Symbol("n")
anti(X ** (_n + 1) / (_n + 1), X ** _n, X, "式 1: x^n の原始関数")
anti(sp.log(X), 1 / X, X, "式 2: 1/x の原始関数")
anti(-sp.cos(XR), sp.sin(XR), XR, "式 3: sin の原始関数")
anti(sp.sin(XR), sp.cos(XR), XR, "式 3: cos の原始関数")
anti(sp.exp(XR), sp.exp(XR), XR, "式 4: e^x の原始関数")
_a, _b = sp.symbols("a b", positive=True)
anti(sp.sin(_a * XR + _b) / _a, sp.cos(_a * XR + _b), XR, "式 5: cos(ax+b)")
anti(-sp.cos(_a * XR + _b) / _a, sp.sin(_a * XR + _b), XR, "式 5: sin(ax+b)")
anti(sp.exp(_a * XR + _b) / _a, sp.exp(_a * XR + _b), XR, "式 5: e^(ax+b)")
anti(sp.log(_a * X + _b) / _a, 1 / (_a * X + _b), X, "式 5: 1/(ax+b)")
# 表 1（分数の指数）
anti(sp.Rational(2, 3) * X ** sp.Rational(3, 2), sp.sqrt(X), X, "表 1: √x")
anti(2 * X ** sp.Rational(1, 2), 1 / sp.sqrt(X), X, "表 1: 1/√x")
anti(sp.Rational(3, 4) * X ** sp.Rational(4, 3), X ** sp.Rational(1, 3), X,
     "表 1: 3乗根")

# ══════════════════════════════════════════════════════════
# 5. 例題
# ══════════════════════════════════════════════════════════
anti(3 * sp.log(X) + 2 * sp.exp(X) + sp.cos(X),
     3 / X + 2 * sp.exp(X) - sp.sin(X), X, "例題1")
in_text("3\\ln|x| + 2e^{x} + \\cos x + C", "例題1 の答え")
anti(sp.sin(3 * XR - 1) / 3, sp.cos(3 * XR - 1), XR, "例題2(a)")
anti(sp.exp(5 * XR - 1) / 5, sp.exp(5 * XR - 1), XR, "例題2(b)")
anti(3 * (XR ** 2 + 5) ** 4 / 4, 6 * XR * (XR ** 2 + 5) ** 3, XR, "例題3")
anti(sp.exp(XR ** 2) / 2, XR * sp.exp(XR ** 2), XR, "例題4(a)")
_q = XR ** 2 + 3 * XR + 1
anti(sp.log(_q), (2 * XR + 3) / _q, XR, "例題4(b)")

# ══════════════════════════════════════════════════════════
# 6. 演習
# ══════════════════════════════════════════════════════════
anti(4 * sp.sqrt(X) - X ** 4 / 4, 2 / sp.sqrt(X) - X ** 3, X, "演習1")
anti((4 * X + 1) ** sp.Rational(3, 2) / 6, sp.sqrt(4 * X + 1), X, "演習2")
anti(sp.log(5 * X - 2) / 5, 1 / (5 * X - 2), X, "演習3")
anti(2 * sp.log(X) + sp.exp(X), 2 / X + sp.exp(X), X, "演習4")
chk(sp.simplify((2 * sp.log(1) + sp.exp(1) + (4 - sp.E)) - 4) == 0,
    "演習4 の C = 4 - e")
anti(sp.sin(2 * XR) / 2, sp.cos(2 * XR), XR, "演習5 の正しい答え")
chk(sp.simplify(sp.diff(2 * sp.sin(2 * XR), XR) - sp.cos(2 * XR)) != 0,
    "演習5 の生徒の答えはまちがい")
anti(sp.log(2 + sp.sin(XR)), sp.cos(XR) / (2 + sp.sin(XR)), XR, "演習6")
chk(sp.minimum(2 + sp.sin(XR), XR) == 1,
    "演習6 は 2 + sin x の最小が 1 > 0 なので絶対値が要らない")
anti(sp.exp(sp.sin(XR)), sp.cos(XR) * sp.exp(sp.sin(XR)), XR, "演習7")
anti(sp.sqrt(XR ** 2 + 9), XR / sp.sqrt(XR ** 2 + 9), XR, "演習8")
anti(-2 / (XR ** 3 + 2), 6 * XR ** 2 / (XR ** 3 + 2) ** 2, XR, "演習9")
# 演習10：2x(x^2+1)^4 は置換できるが、(x^2+1)^4 はできない
anti((XR ** 2 + 1) ** 5 / 5, 2 * XR * (XR ** 2 + 1) ** 4, XR, "演習10 の前半")
chk(sp.expand((XR ** 2 + 1) ** 4)
    == XR ** 8 + 4 * XR ** 6 + 6 * XR ** 4 + 4 * XR ** 2 + 1,
    "演習10: 後半は展開して積分する")
in_text("*the second integral is found by expanding the bracket instead*",
        "演習10 の答え")



# ══════════════════════════════════════════════════════════
# 2026-09-29（その 2）：第 3 節の書き出し／表 2 のあとの 2 段落／第 4 節の統合
# ══════════════════════════════════════════════════════════
in_text("**中身が $1$ 次式（$ax + b$）のとき**、つまり中身に $x^{2}$ や "
        "$\sin x$ のようなものが入っていないときは、最後に $\dfrac{1}{a}$ を"
        "かけます。", "第 3 節の書き出し")
not_in_text("**中身が $1$ 次式のときは、最後に", "前の書き出しは消した")
not_in_text("**この表は、$a$、$b$ が定数で $a \ne 0$ のときの形です。**",
            "表 2 のあとの定義域の段落は消した")
not_in_text("**$a$ が負でも同じです。**", "a が負の段落は消した")
in_text("**割るのは $a$ だけで、$b$ では割りません。**", "b では割らない（残す）")

# --- 第 4 節（見分ける形）は第 4 節（見て書く）にまとめた -----------------
not_in_text("{#spot}", "アンカー #spot は消した")
not_in_text("spotting the form", "見出しは消した")
not_in_text("aasl-5-10-idea-a", "図 (a) は消した")
chk(not os.path.exists(os.path.join(os.path.dirname(QMD), "img",
                                    "aasl-5-10-idea-a.svg")), "SVG も消した")
chk("ax1" not in FIG, "図をつくる側からも消した")
in_text("**このように、中身の導関数がかけ算でくっついている形を探します。**",
        "第 4 節の一般形へのつなぎ")
in_text("**$g(x)$ が「合成関数の中身」、$g'(x)$ が「中身の導関数」、"
        "$f$ が「外側の関数」です。** "
        "中身は、かっこの中、根号の中、$\sin$ や $e$ の右にあるものです。"
        "それを微分したものが（定数倍のちがいを除いて）かけてあるかどうかを"
        "見ます。**中身が $ax + b$ のときは、[第 3 節](#linear) の形で"
        "足ります。**", "中身と外側の見分け方")
in_text("$$\n\\int g'(x)\\,f(g(x))\\,dx\n$$ {#eq-aasl510-form}",
        "式 6 に k は入れない")
not_in_text("\\int k\\,g'(x)", "k つきの形は消した")
in_text("**この形は、chain rule で微分したあとの姿です**",
        "chain rule の逆だと言っている")
_i4a = TEXT.index("### 4. reverse chain rule（chain rule の逆を考える）"
                  " {#inspection}")
_i5a = TEXT.index("### 5. the $\\dfrac{g'(x)}{g(x)}$ form")
_s4 = TEXT[_i4a:_i5a]
for _s in ("{#eq-aasl510-form}",
           "**だから、外側だけを積分して、中身はそのままにします。**"):
    chk(_s in _s4, "第 4 節の中にある: " + _s)
chk(TEXT.count("[第 4 節](#inspection)") >= 2,
    "第 4 節への参照: %d 件" % TEXT.count("[第 4 節](#inspection)"))



# --- 2026-09-29：第 4 節の書き出しに具体例を 2 つ ------------------------
in_text("**たとえば、次の $2$ つです。**", "第 4 節の書き出し")
in_text("$$\n\\int 3x^{2}\\,\\bigl(x^{3} - 4\\bigr)^{5}dx, \\qquad "
        "\\int 4x\\,\\sin\\bigl(x^{2}\\bigr)\\,dx\n$$", "具体例 2 つ")
in_text("**$1$ つ目は、合成関数の中身が $x^{3} - 4$ で、その derivative"
        "（導関数）$3x^{2}$ がかけてあります。** $2$ つ目は、"
        "合成関数の中身が $x^{2}$ で、その導関数 $2x$ が、"
        "$2$ 倍された $4x$ の形でかけてあります。", "2 つの説明")
chk(TEXT.count("derivative（導関数）") == 1, "英語の併記は初出の 1 回だけ")
chk(TEXT.index("**たとえば、次の $2$ つです。**")
    < TEXT.index("{#eq-aasl510-form}"), "具体例は一般形より前")
# 具体例が本当にこの形であること（原始関数を微分してもどるか）
_E1 = (XR ** 3 - 4) ** 6 / 6
anti(_E1, 3 * XR ** 2 * (XR ** 3 - 4) ** 5, XR, "第 4 節の例 1")
_E2 = -2 * sp.cos(XR ** 2)
anti(_E2, 4 * XR * sp.sin(XR ** 2), XR, "第 4 節の例 2")
chk(sp.simplify(sp.diff(XR ** 3 - 4, XR) - 3 * XR ** 2) == 0,
    "例 1 の中身の導関数は 3x^2")
chk(sp.simplify(4 * XR - 2 * sp.diff(XR ** 2, XR)) == 0,
    "例 2 の 4x は 2x の 2 倍")



# ══════════════════════════════════════════════════════════
# 2026-09-29（その 3）：第 4 節から F を外し、対数の節を第 4 節の直後に
# ══════════════════════════════════════════════════════════
# --- F と式 7 は第 4 節から消えた（Why it works にだけ残る） -------------
_i4b = TEXT.index("### 4. reverse chain rule")
_i5b = TEXT.index("### 5. the $\\dfrac{g'(x)}{g(x)}$ form")
_s4b = TEXT[_i4b:_i5b]
for _bad in ("$F$", "F(g(x))", "$F' = f$", "**やり方は $2$ 歩です。**"):
    chk(_bad not in _s4b, "第 4 節に F まわりは残っていない: " + _bad)
not_in_text("eq-aasl510-inspection", "式 7 は消した")
chk("F(g(x))" in TEXT[TEXT.index("## Why it works"):],
    "F は Why it works にだけ残っている")
in_text("**この形は、chain rule で微分したあとの姿です**"
        "（[SL 5.6](aasl-5-6.qmd#chain)）。合成関数を微分すると、"
        "外側を微分したものに、中身の導関数 $g'(x)$ がかかります。"
        "かけてある $g'(x)$ は、その「微分したときに出てきた分」です。",
        "chain rule の逆の説明")
in_text("**だから、外側だけを積分して、中身はそのままにします。** "
        "$g'(x)$ は役目を終えるので、答えには残りません。", "やることの一文")
# --- 具体例でたどる ------------------------------------------------------
in_text("はじめの例 $\\displaystyle\\int 3x^{2}\\bigl(x^{3} - 4\\bigr)^{5}dx$ で"
        "やってみます。", "具体例でたどる")
in_text("$$\n\\int 3x^{2}\\bigl(x^{3} - 4\\bigr)^{5}dx "
        "= \\frac{\\bigl(x^{3} - 4\\bigr)^{6}}{6} + C\n$$", "具体例の答え")
in_text("$$\n\\frac{d}{dx}\\frac{\\bigl(x^{3} - 4\\bigr)^{6}}{6} "
        "= \\frac{6\\bigl(x^{3} - 4\\bigr)^{5} \\times 3x^{2}}{6} "
        "= 3x^{2}\\bigl(x^{3} - 4\\bigr)^{5}\n$$", "具体例の検算")
chk(sp.simplify(sp.diff((XR ** 3 - 4) ** 6 / 6, XR)
                - 3 * XR ** 2 * (XR ** 3 - 4) ** 5) == 0, "具体例の答えが正しい")
chk(sp.expand(6 * (XR ** 3 - 4) ** 5 * 3 * XR ** 2 / 6)
    == sp.expand(3 * XR ** 2 * (XR ** 3 - 4) ** 5), "検算の途中も正しい")

# --- 対数になる形は第 5 節（第 4 節の直後） ------------------------------
in_text("### 5. the $\\dfrac{g'(x)}{g(x)}$ form（対数になる形） {#logform}",
        "第 5 節は対数になる形")
in_text("### 7. integration by substitution（置換積分） {#substitution}",
        "第 7 節は置換積分")
chk(TEXT.index("{#logform}") < TEXT.index("{#substitution}"),
    "対数の節は置換の節より前")
# 移した節の中に置換積分は出てこない（置換の説明より前になるため）
_i5c = TEXT.index("### 5. the $\\dfrac{g'(x)}{g(x)}$ form")
_i6c = TEXT.index("### 6. adjusting the constant")
_s5c = TEXT[_i5c:_i6c]
for _bad in ("置換", "$u$ を置", "du", "substitution"):
    chk(_bad not in _s5c, "第 5 節に置換積分は出てこない: " + _bad)
chk("@eq-aasl510-form" in _s5c, "第 5 節は式 6 を参照している")

# --- 図 1（置換積分の流れ）は消した ---------------------------------------
not_in_text("aasl-5-10-idea-b", "図 1 は消した")
not_in_text("fig-aasl510-idea-b", "図 1 の参照も消した")
chk(not os.path.exists(os.path.join(os.path.dirname(QMD), "img",
                                    "aasl-5-10-idea-b.svg")), "SVG も消した")
chk("ax2" not in FIG and "fig2" not in FIG, "図をつくる側からも消した")
in_text("**[第 4 節](#inspection) で見て書いた積分は、別のやり方でも"
        "解けます。** それが integration by substitution（置換積分）です。"
        "**合成関数の中身を $u$ と置くのがコツです。**",
        "第 7 節の書き出し")
chk(TEXT.count("](img/") == 1, "図は 1 枚: %d" % TEXT.count("](img/"))

# --- 図の文字が枠の中にあるか（axL） --------------------------------------
_m = re.search(r"axL\.set_ylim\(([-\d.]+), ([-\d.]+)\)", FIG)
chk(_m is not None, "axL に set_ylim がある")
_lo, _hi = float(_m.group(1)), float(_m.group(2))
for _t in re.finditer(r"axL\.text\(\s*[-\d.]+\s*,\s*([-\d.]+)", FIG):
    _y = float(_t.group(1))
    chk(_lo <= _y <= _hi, "axL.text の y=%s は %s〜%s の中" % (_y, _lo, _hi))



# --- 2026-09-29：図の矢印にラベルを付け、中の公式を外した（方針 §21） ----
for _s in ('axL.text(5.0, 3.32, "differentiate:  $\\\\times a$"',
           'axL.text(5.0, 0.48, "integrate:  $\\\\times \\\\frac{1}{a}$"'):
    chk(_s in FIG, "図の矢印ラベル: " + _s[:40])
chk("\\\\int f'(ax + b)" not in FIG, "図の中に公式は置かない（方針 §21）")
chk("figsize=(6.6, 2.7)" in FIG, "図の縦を詰めた")
chk("\\dfrac" not in FIG, "mathtext は \\dfrac を読めない")



# ══════════════════════════════════════════════════════════
# 2026-09-29（その 4）：手順の節を削除、定数を合わせるを置換の前に
# ══════════════════════════════════════════════════════════
not_in_text("#steps", "手順の節のアンカーは消した")
not_in_text("the four steps", "手順の見出しは消した")
not_in_text("tbl-aasl510-steps", "手順の表は消した")
not_in_text("置換積分の手順", "手順の表の題も消した")
in_text("### 6. adjusting the constant（定数を合わせる） {#constant}",
        "第 6 節は定数を合わせる")
chk(TEXT.index("{#constant}") < TEXT.index("{#substitution}"),
    "定数を合わせるは置換積分より前")
chk(TEXT.index("{#logform}") < TEXT.index("{#constant}"),
    "対数になる形は定数を合わせるより前")

# --- 置換積分の節は、第 4 節と同じ例でたどる -----------------------------
_i7d = TEXT.index("### 7. integration by substitution")
_i8d = TEXT.index("### 8. choosing $u$")
_s7d = TEXT[_i7d:_i8d]
in_text("同じ例 $\\displaystyle\\int 3x^{2}\\bigl(x^{3} - 4\\bigr)^{5}dx$ で"
        "やってみます。中身が $x^{3} - 4$ なので、$u = x^{3} - 4$ と置きます。"
        "微分すると $\\dfrac{du}{dx} = 3x^{2}$ なので、$du = 3x^{2}\\,dx$ です。",
        "置換積分の具体例")
in_text("$$\n\\int \\bigl(x^{3} - 4\\bigr)^{5}\\,3x^{2}\\,dx "
        "= \\int u^{5}\\,du = \\frac{u^{6}}{6} + C\n$$", "置換積分の計算")
in_text("**最後に $u = x^{3} - 4$ をもどします。** 答えは "
        "$\\dfrac{\\bigl(x^{3} - 4\\bigr)^{6}}{6} + C$ で、"
        "[第 4 節](#inspection) で見て書いたものと同じです。", "答えが一致する")
chk("{#eq-aasl510-du}" in _s7d, "式 du は第 7 節の中")
# 2 つのやり方で同じ答えになる
_U = sp.Symbol("u")
chk(sp.simplify((_U ** 6 / 6).subs(_U, XR ** 3 - 4)
                - (XR ** 3 - 4) ** 6 / 6) == 0, "置換の答えは見て書いた答えと同じ")
chk(sp.simplify(sp.diff((XR ** 3 - 4) ** 6 / 6, XR)
                - 3 * XR ** 2 * (XR ** 3 - 4) ** 5) == 0, "その答えが正しい")



# ══════════════════════════════════════════════════════════
# 2026-09-29（その 5）：第 5 節の段落を削除、表 3 を不定積分の形に
# ══════════════════════════════════════════════════════════
not_in_text("**この形が使えるのは、$g(x) \ne 0$ である区間の中です。**",
            "g(x) ≠ 0 の段落は消した")
not_in_text("| 見えている形 | 中身 $g(x)$ | $g'(x)$ | 合わせ方 |",
            "「合わせ方」の列は消した")
not_in_text("そのまま |", "「そのまま」の行はもう置かない")
in_text("| 見えている形 | 中身 $g(x)$ | $g'(x)$ | 不定積分 |", "表 3 の見出し")
for _r in ("| $x\\left(x^{2}+1\\right)^{3}$ | $x^{2}+1$ | $2x$ | "
           "$\\dfrac{\\left(x^{2}+1\\right)^{4}}{8} + C$ |",
           "| $x^{4}\\left(x^{5}+2\\right)^{3}$ | $x^{5}+2$ | $5x^{4}$ | "
           "$\\dfrac{\\left(x^{5}+2\\right)^{4}}{20} + C$ |",
           "| $\\dfrac{x}{x^{2}+3}$ | $x^{2}+3$ | $2x$ | "
           "$\\dfrac{1}{2}\\ln\\left(x^{2}+3\\right) + C$ |"):
    in_text(_r, "表 3 の行: " + _r[:26])
in_text("**どれも、見えている形が $g'(x)$ の定数倍になっています。**",
        "そのままにならない例ばかりだと書いてある")
in_text("**$3$ つ目に絶対値が要らないのは、$x^{2}+3$ がつねに正だからです**",
        "絶対値が要らない理由")
# 表 3 の 3 行を、微分してもどるかで確かめる
for _F, _f, _lab in (((XR ** 2 + 1) ** 4 / 8, XR * (XR ** 2 + 1) ** 3, "1 行目"),
                     ((XR ** 5 + 2) ** 4 / 20, XR ** 4 * (XR ** 5 + 2) ** 3,
                      "2 行目"),
                     (sp.log(XR ** 2 + 3) / 2, XR / (XR ** 2 + 3), "3 行目")):
    chk(sp.simplify(sp.diff(_F, XR) - _f) == 0, "表 3 の " + _lab)
# どれも「そのまま」ではない（g' の係数が 1 ではない）
for _g, _seen, _lab in ((XR ** 2 + 1, XR, "1 行目"),
                        (XR ** 5 + 2, XR ** 4, "2 行目"),
                        (XR ** 2 + 3, XR, "3 行目")):
    chk(sp.simplify(sp.diff(_g, XR) / _seen) != 1,
        "表 3 の " + _lab + " はそのままでは合わない")
chk(sp.minimum(XR ** 2 + 3, XR) > 0, "x^2+3 はつねに正")

print()
print("OK", OK, "/ NG", NG)
