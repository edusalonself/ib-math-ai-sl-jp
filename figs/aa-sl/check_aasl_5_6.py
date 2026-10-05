# -*- coding: utf-8 -*-
"""AA SL 5.6 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_6.py

このページは、2026-09-29 に SL 5.6a と SL 5.6b をまとめて作ったものです。
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-6.qmd")

TEXT = open(QMD, encoding="utf-8").read()

OK = 0
NG = 0


def chk(cond, msg=""):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(a, b, msg=""):
    chk(sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0,
        "%s :: %s != %s" % (msg, a, b))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: %s :: %s" % (msg, sub[:60]))


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: %s :: %s" % (msg, sub[:60]))


BODY = TEXT.split("## Worked examples")[0]


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "本文（例題より前）に残っている: %s" % msg)


X = sp.Symbol("x", real=True)
XP = sp.Symbol("x", positive=True)


def d(e, v=X):
    return sp.simplify(sp.diff(e, v))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
in_text("# SL 5.6 — Standard derivatives and the rules of differentiation"
        "（標準的な導関数と微分の規則） {#sec-aasl-5-6}", "ページの題")
for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. (.*) \{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 10)],
    "### の番号 1..9: %s" % [s[0] for s in _secs])
chk([s[2] for s in _secs] == ["rational", "standard", "composite", "chain",
                              "product", "quotient", "withchain",
                              "simplify", "spot"],
    "アンカー: %s" % [s[2] for s in _secs])
# 見出しはすべて 英語（日本語）（方針 第 17 節の ①②）
for _n, _t, _a in _secs:
    if _n == "4":
        chk(_t == "合成関数の微分＝chain rule", "第 4 節の見出し: " + _t)
        continue
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
chk(TEXT.count(":::") % 2 == 0, "::: の数が偶数: %d" % TEXT.count(":::"))
chk("\n\n\n" not in TEXT, "空行が 2 つ続いていない")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "5.6 でシラバスの引用は使わない: %s" % _quotes)

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

# ══════════════════════════════════════════════════════════
# 2. 式・表・図・参照
# ══════════════════════════════════════════════════════════
for _e in ("{#eq-aasl56-power}", "{#eq-aasl56-chain}", "{#eq-aasl56-chain2}",
           "{#eq-aasl56-product}", "{#eq-aasl56-quotient}"):
    in_text(_e, "式 " + _e)
not_in_text("{#eq-aasl56-wrong}", "書きまちがえの式は消した")
for _t in ("{#tbl-aasl56-root}", "{#tbl-aasl56-std}", "{#tbl-aasl56-io}",
           "{#tbl-aasl56-which}", "{#tbl-aasl56-uv}"):
    in_text(_t, "表 " + _t)
not_in_text("{#tbl-aasl56-steps}", "手順の表は消した")
for _s in ("aasl-5-6-idea", "fig-aasl56", "![" ):
    not_in_text(_s, "このページに図は置かない: " + _s)
for _p in ("aasl-5-6-idea-a.svg", "aasl-5-6-idea-b.svg"):
    chk(not os.path.exists(os.path.join(ROOT, "aa-sl", "05-calculus",
                                        "img", _p)), "図を消した: " + _p)
chk(not os.path.exists(os.path.join(HERE, "make_aasl_5_6.py")),
    "図をつくるスクリプトも消した")

in_text("[SL 5.3](aasl-5-3.qmd#power)", "5.3 への参照（べき乗）")
in_text("[SL 5.3](aasl-5-3.qmd#sum)", "5.3 への参照（和と定数倍）")
in_text("[SL 5.3](aasl-5-3.qmd#constant)", "5.3 への参照（定数倍）")
in_text("[SL 5.3](aasl-5-3.qmd#rewrite)", "5.3 への参照（先に直す）")
in_text("[SL 3.4](../03-geometry/aasl-3-4.qmd)", "3.4 への参照（ラジアン）")
in_text("[SL 2.5](../02-functions/aasl-2-5.qmd#order)", "2.5 への参照（合成）")
chk(not re.search(r"aasl-5-6[ab]", TEXT), "5.6a / 5.6b へのリンクは残っていない")
# ページ内リンクの行き先は、すべてこのページにある
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a + "}") in TEXT or ("#" + _a + " ") in TEXT
        or _a == "why-it-works", "ページ内リンクの行き先がある: #" + _a)

# ══════════════════════════════════════════════════════════
# 3. 2026-09-29：5.6a + 5.6b をまとめたときの決めごと
# ══════════════════════════════════════════════════════════
# (1) 消したもの
not_in_text("### 3. ラジアンで", "5.6a 第 3 節（ラジアンで）は節としては消した")
not_in_text("{#radian}", "アンカー #radian は消した")
not_in_text("{#order}", "アンカー #order は消した")
not_in_text("{#choose}", "アンカー #choose は消した")
not_in_text("{#sum}", "アンカー #sum は消した（和と定数倍は 5.3 へ）")
not_in_text("$\\sqrt{x}$ は $x \\geq 0$ でしか定義されません",
            "第 1 節の定義域の 1 文は消した")
not_in_text("連鎖律を使う順番", "「使う順番」の表は消した")
not_in_text("正確な値が要るときは", "Paper 1 の callout の角の一覧は消した")
not_in_text("$u$ と $v$ の決め方", "「u と v の決め方」は節としては消した")
not_in_text("分子の順番 {#", "「分子の順番」は節としては消した")
chk(not os.path.exists(os.path.join(ROOT, "aa-sl", "05-calculus",
                                    "aasl-5-6a.qmd")), "5.6a のページは消した")
chk(not os.path.exists(os.path.join(ROOT, "aa-sl", "05-calculus",
                                    "aasl-5-6b.qmd")), "5.6b のページは消した")
chk(not os.path.exists(os.path.join(ROOT, "aa-sl", "05-calculus", "img",
                                    "aasl-5-6a-idea.svg")),
    "5.6a の図（合成関数）は消した")

# (2) 移したもの
in_text("**$\\sin$ と $\\cos$ の derivative は、$x$ が radian（ラジアン）の"
        "ときの式です。**", "ラジアンの注意は第 2 節に")
chk(TEXT.index("radian（ラジアン）のときの式です")
    < TEXT.index("### 3. composite function"), "ラジアンの注意は第 2 節の中")
in_text("**いちばん多い誤りは、内側の derivative をかけ忘れることです。**",
        "連鎖律の注意は第 4 節に")
chk(TEXT.index("いちばん多い誤りは、内側の derivative")
    < TEXT.index("### 5. product rule"), "連鎖律の注意は第 4 節の中")
in_text("**分子は、$v\\dfrac{du}{dx}$ が先です。** 上を $u$、下を $v$ とします。",
        "分子の順番と u・v は第 6 節（商）に")
chk(TEXT.index("### 6. quotient rule")
    < TEXT.index("**分子は、$v\\dfrac{du}{dx}$ が先です。**")
    < TEXT.index("### 7. combining the rules"), "第 6 節の中にある")

# (3) 「導関数」は derivative に（題名と見出しの日本語はそのまま）
chk(TEXT.count("derivative（導関数）") == 1, "併記は 1 回だけ")
for _ln in TEXT.split("\n"):
    if _ln.startswith("# ") or _ln.startswith("### "):
        continue
    chk("導関数" not in _ln.replace("derivative（導関数）", ""),
        "本文に導関数が残っている: " + _ln.strip()[:50])
in_text("（標準的な導関数と微分の規則）", "題名の日本語は「導関数」のまま")
in_text("### 2. standard derivatives（標準的な導関数） {#standard}",
        "第 2 節の見出しの日本語は「導関数」のまま")
chk(not re.search(r"[぀-ヿ一-鿿]derivative", TEXT),
    "derivative の前に空白がある")
chk(not re.search(r"derivative[぀-ヿ一-鿿]", TEXT),
    "derivative のあとに空白がある")

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1  f(x) = 3√x
eq(d(3 * sp.sqrt(XP), XP), 3 / (2 * sp.sqrt(XP)), "例題1 の derivative")
eq(sp.Rational(3, 2) * XP ** sp.Rational(-1, 2), 3 / (2 * sp.sqrt(XP)),
   "例題1 の答えの書きかえ")
in_text("$$f'(x) = \\frac{3}{2}x^{-\\frac{1}{2}} = \\frac{3}{2\\sqrt{x}}$$",
        "例題1 の解答例")

# 例題2  (a) e^{x^2+5}  (b) sin(4x-3)  (c) ln(2x)
eq(d(sp.exp(X ** 2 + 5)), 2 * X * sp.exp(X ** 2 + 5), "例題2(a)")
eq(d(sp.sin(4 * X - 3)), 4 * sp.cos(4 * X - 3), "例題2(b)")
eq(d(sp.log(2 * XP), XP), 1 / XP, "例題2(c)")
eq(sp.log(2 * XP) - (sp.log(2) + sp.log(XP)), 0, "例題2(c) ln(2x) = ln2 + lnx")
in_text("$f'(x) = 2x\\,e^{x^{2} + 5}$", "例題2(a) の答え")
in_text("$g'(x) = 4\\cos(4x - 3)$", "例題2(b) の答え")

# 例題3  y = x^3 e^x（積）
eq(d(X ** 3 * sp.exp(X)), X ** 2 * sp.exp(X) * (X + 3), "例題3 の derivative")
in_text("$$\\frac{dy}{dx} = x^{3}e^{x} + 3x^{2}e^{x} = x^{2}e^{x}(x + 3)$$",
        "例題3 の解答例")

# 例題4  y = cos x / x（商）
eq(d(sp.cos(X) / X), (-X * sp.sin(X) - sp.cos(X)) / X ** 2, "例題4 の derivative")
in_text("\\frac{-x\\sin x - \\cos x}{x^{2}}", "例題4 の解答例")

# ══════════════════════════════════════════════════════════
# 5. 演習
# ══════════════════════════════════════════════════════════
eq(d(1 / sp.sqrt(XP), XP), -1 / (2 * XP * sp.sqrt(XP)), "演習1")
eq(-sp.Rational(1, 2) * XP ** sp.Rational(-3, 2), -1 / (2 * XP * sp.sqrt(XP)),
   "演習1 の書きかえ")
eq(d(5 * sp.sin(X)), 5 * sp.cos(X), "演習2")
chk(abs(float(sp.pi / 180) - 0.0175) < 0.0001, "演習2 度のときの係数 π/180")
eq(d((2 * X + 7) ** 4), 8 * (2 * X + 7) ** 3, "演習3")
eq(d(sp.exp(2 * X) + sp.sin(3 * X)), 2 * sp.exp(2 * X) + 3 * sp.cos(3 * X),
   "演習4")
eq(d(XP ** 2 * sp.log(XP), XP), XP + 2 * XP * sp.log(XP), "演習5")
eq(d((X + 1) / (X - 2)), -3 / (X - 2) ** 2, "演習6")
eq(d(sp.exp(2 * X) / (X + 1)), sp.exp(2 * X) * (2 * X + 1) / (X + 1) ** 2,
   "演習7")
eq(d(5 * sp.cos(X)), -5 * sp.sin(X), "演習8(a)")
eq(d(X * sp.sin(X)), X * sp.cos(X) + sp.sin(X), "演習8(b)")
eq((X ** 4 + X) / X ** 2, X ** 2 + X ** -1, "演習8(c) 先に整理できる")
eq(d(X ** 2 + X ** -1), 2 * X - X ** -2, "演習8(c)")
eq(d(X ** 2 / (X + 3)), (X ** 2 + 6 * X) / (X + 3) ** 2, "演習9 の正しい答え")
eq(((X + 3) * 2 * X - X ** 2) / (X + 3) ** 2,
   (X ** 2 + 6 * X) / (X + 3) ** 2, "演習9 の分子の整理")
chk(sp.simplify((X ** 2 - (X + 3) * 2 * X) / (X + 3) ** 2
                + (X ** 2 + 6 * X) / (X + 3) ** 2) == 0,
    "演習9 逆にすると符号が反対になる")
eq(sp.expand((2 * X + 1) * (X - 4)), 2 * X ** 2 - 7 * X - 4, "演習10 の展開")
eq(d((2 * X + 1) * (X - 4)), 4 * X - 7, "演習10")

# 表 1（根号を指数に）
for _a, _b in ((sp.sqrt(XP), XP ** sp.Rational(1, 2)),
               (1 / sp.sqrt(XP), XP ** sp.Rational(-1, 2)),
               (XP ** sp.Rational(1, 3), sp.root(XP, 3))):
    eq(_a, _b, "表 1 の書きかえ")
# 表 2（標準的な derivative）
eq(d(sp.sin(X)), sp.cos(X), "表 2 sin")
eq(d(sp.cos(X)), -sp.sin(X), "表 2 cos")
eq(d(sp.exp(X)), sp.exp(X), "表 2 e^x")
eq(d(sp.log(XP), XP), 1 / XP, "表 2 ln")
# 第 4 節の例（連鎖律）
eq(d((3 * X + 1) ** 4), 12 * (3 * X + 1) ** 3, "第 4 節 (3x+1)^4")
# 第 8 節の例
eq(d(sp.cos(4 * X)), -4 * sp.sin(4 * X), "第 8 節 cos(4x)")
# 第 9 節の例
eq((XP ** 5 + 1) / XP ** 3, XP ** 2 + XP ** -3, "第 9 節 先に分ける")
eq(sp.expand(X ** 2 * (X + 1)), X ** 3 + X ** 2, "第 9 節 先に展開する")
# 商の分子を逆にすると符号が反対（式 6）
_u, _v = sp.Function("u")(X), sp.Function("v")(X)
chk(sp.simplify((_u * sp.diff(_v, X) - _v * sp.diff(_u, X)) / _v ** 2
                + sp.diff(_u / _v, X)) == 0, "式 6：逆にすると符号が反対")
# 積の規則と商の規則そのもの
chk(sp.simplify(sp.diff(_u * _v, X)
                - (_u * sp.diff(_v, X) + _v * sp.diff(_u, X))) == 0,
    "式 4：積の微分法")
chk(sp.simplify(sp.diff(_u / _v, X)
                - (_v * sp.diff(_u, X) - _u * sp.diff(_v, X)) / _v ** 2) == 0,
    "式 5：商の微分法")


in_text("### 4. 合成関数の微分＝chain rule {#chain}", "第 4 節の見出し")
not_in_text("### 4. chain rule（連鎖律）", "前の見出しは消した")
in_text("合成関数を微分するときに使うのが、**chain rule**（連鎖律）です。",
        "第 4 節の書き出し")
not_in_text("です。これを **chain rule**（連鎖律）といいます。",
            "式のあとの重なった 1 文は消した")
chk(TEXT.index("合成関数を微分するときに使うのが")
    < TEXT.index("{#eq-aasl56-chain}"), "書き出しは式より前")



# ══════════════════════════════════════════════════════════
# 2026-09-29（その 2）：図を外す／説明を削る／節を並べかえる
# ══════════════════════════════════════════════════════════

# --- 第 5 節（積）---------------------------------------------------------
in_text("### 5. product rule（積の微分法） {#product}", "第 5 節の見出し")
in_text("微分したい関数が、$2$ つの関数の **product**（積）の形で表されている"
        "ときには、専用の規則があります。", "第 5 節の書き出し")
not_in_text("$2$ つの関数の**積**は、それぞれを微分してかけ算しても求まりません。",
            "前の書き出しは消した")
for _s in ("**$2$ 項できます。**", "**積では、どちらを $u$ にしても同じ答えに",
           "**ふつうは、左のかたまりを $u$ にします。**"):
    not_in_text(_s, "第 5 節から消した: " + _s[:26])
in_text("$u$ と $v$ の取り方の例です。", "表（積での u と v）の前置き")

# --- 第 6 節（商）---------------------------------------------------------
in_text("### 6. quotient rule（商の微分法） {#quotient}", "第 6 節の見出し")
in_text("微分したい関数が、**quotient**（商）の形、つまり分数の形で表されている"
        "ときにも、専用の規則があります。", "第 6 節の書き出し")
not_in_text("**わり算**の形にも、専用の規則があります。", "前の書き出しは消した")
for _s in ("**$v = 0$ になる $x$ は、はじめから定義域の外です。**",
           "**@eq-aasl56-wrong の左辺が", "**積のほうは、順番を気にしなくて",
           "入れかえて公式集の式に入れると"):
    not_in_text(_s, "第 6 節から消した: " + _s[:26])

# --- 第 7 節（組み合わせる）：具体例 --------------------------------------
in_text("### 7. combining the rules（規則を組み合わせる） {#withchain}",
        "第 7 節の見出し")
in_text("たとえば $y = x^{2}\\cos(4x + 1)$ を微分します。"
        "**全体はかけ算の形なので、まず積の微分法です。**", "第 7 節の例")
in_text("$$\nu = x^{2}, \\qquad v = \\cos(4x + 1)\n$$", "第 7 節 u と v")
in_text("\\frac{du}{dx} = 2x, \\qquad "
        "\\frac{dv}{dx} = -\\sin(4x + 1) \\times 4 = -4\\sin(4x + 1)",
        "第 7 節 du/dx と dv/dx")
in_text("\\frac{dy}{dx} = 2x\\cos(4x + 1) - 4x^{2}\\sin(4x + 1) "
        "= 2x\\bigl(\\cos(4x + 1) - 2x\\sin(4x + 1)\\bigr)", "第 7 節の答え")
not_in_text("たとえば $v = \\cos(4x)$ なら", "前の例は消した")
# 例の計算をたしかめる
_Y7 = X ** 2 * sp.cos(4 * X + 1)
eq(d(_Y7), 2 * X * sp.cos(4 * X + 1) - 4 * X ** 2 * sp.sin(4 * X + 1),
   "第 7 節の例 y = x^2 cos(4x+1)")
eq(2 * X * sp.cos(4 * X + 1) - 4 * X ** 2 * sp.sin(4 * X + 1),
   2 * X * (sp.cos(4 * X + 1) - 2 * X * sp.sin(4 * X + 1)),
   "第 7 節の例の因数分解")
eq(d(sp.cos(4 * X + 1)), -4 * sp.sin(4 * X + 1), "第 7 節 dv/dx")

# --- 第 9 節（どの規則を使うか）はいちばん最後 -----------------------------
in_text("### 9. choosing the rule（どの規則を使うか） {#spot}", "第 9 節の見出し")
chk(TEXT.index("### 8. simplify first") < TEXT.index("### 9. choosing the rule"),
    "「どの規則を使うか」は「先に整理する」のあと")
_i9 = TEXT.index("### 9. choosing the rule（どの規則を使うか） {#spot}")
_s9 = TEXT[_i9:TEXT.index(chr(10) + "## Why it works")]
chk("## この項目は Paper 1 に出ます" in _s9, "Paper 1 の callout は第 9 節に")
chk("## 電卓が使えるときは、こう確かめます" in _s9, "電卓の callout は第 9 節に")
chk(_s9.count("### ") == 1, "第 9 節が The idea の最後")
chk(_s9.count(":::") % 2 == 0, "第 9 節の ::: が閉じている")

# --- 表 4 の「使う規則」は英語 ---------------------------------------------
for _r in ("| *the product rule*（[第 5 節](#product)） |",
           "| *the quotient rule*（[第 6 節](#quotient)） |",
           "| *the chain rule*（[第 4 節](#chain)） |",
           "| *differentiate term by term*（[SL 5.3](aasl-5-3.qmd#sum)） |"):
    in_text(_r, "表（どの規則を使うか）の行: " + _r[:26])
for _r in ("| 積の微分法（", "| 商の微分法（", "| 連鎖律（", "| 項ごとに微分（"):
    not_in_text(_r, "日本語の規則名は消した: " + _r)



# --- 2026-09-29：第 4 節に u と置いてたどる手順を足した --------------------
in_text("**混乱するときは、最初に内側を $u$ と置いてください。** "
        "$y = (3x + 1)^{4}$ なら、$u = 3x + 1$ とすると", "u と置く")
in_text("$$\ny = u^{4}\n$$", "y = u^4")
in_text("$$\n\\frac{dy}{du} = 4u^{3}, \\qquad \\frac{du}{dx} = 3\n$$",
        "dy/du と du/dx")
in_text("\\frac{dy}{dx} = \\frac{dy}{du} \\times \\frac{du}{dx} "
        "= 4u^{3} \\times 3 = 12u^{3}", "連鎖律に入れる")
in_text("$$\n\\frac{dy}{dx} = 12(3x + 1)^{3}\n$$", "u をもどす")
chk(TEXT.index("**混乱するときは、最初に内側を $u$ と置いて")
    < TEXT.index("### 5. product rule"), "手順は第 4 節の中にある")
# 式は 1 つずつ改行して置いてある
chk(TEXT.count("$$\ny = u^{4}\n$$") == 1, "y = u^4 は独立した式")
# 手順の計算
_U = sp.Symbol("u")
eq(sp.diff(_U ** 4, _U), 4 * _U ** 3, "dy/du = 4u^3")
eq(sp.diff(3 * X + 1, X), 3, "du/dx = 3")
eq((4 * _U ** 3 * 3).subs(_U, 3 * X + 1), 12 * (3 * X + 1) ** 3,
   "u をもどすと 12(3x+1)^3")
eq(d((3 * X + 1) ** 4), 12 * (3 * X + 1) ** 3, "答えは直接微分したものと合う")



# ══════════════════════════════════════════════════════════
# 2026-09-29：図のキャプションは 1 行に収める（方針 第 23 節）
# ══════════════════════════════════════════════════════════
for _cm in re.finditer(r"^!\[(.*?)\]\(img/", TEXT, re.M):
    chk(0 < len(_cm.group(1)) <= 75,
        "図のキャプションは 75 字以内（%d 字）: %s"
        % (len(_cm.group(1)), _cm.group(1)[:50]))

print()
print("OK", OK, "/ NG", NG)
