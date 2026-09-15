# -*- coding: utf-8 -*-
"""AA SL 5.10b のページを検算する。

    python3 figs/aa-sl/check_aasl_5_10b.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-10b.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_10b.py")

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


def eq(a, b, msg=""):
    chk(sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0,
        "%s :: %s != %s" % (msg, a, b))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: %s :: %s" % (msg, sub[:60]))


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: %s :: %s" % (msg, sub[:60]))


def in_fig(sub, msg=""):
    chk(sub in FIG, "図に見つからない: %s :: %s" % (msg, sub[:60]))


BODY = TEXT.split("## Worked examples")[0]


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "本文（例題より前）に残っている: %s :: %s" % (msg, sub[:60]))


R = sp.Rational
X = sp.Symbol("x", positive=True)


def anti(f, F):
    """F を微分すると f にもどるか。"""
    return sp.simplify(sp.diff(F, X) - f) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.10b — Reverse chain rule and substitution"
        "（逆連鎖律と置換積分） {#sec-aasl-5-10b}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["spot", "inspection", "substitution", "steps",
                              "constant", "logform", "choose"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper）")
chk(TEXT.count("{.callout-important}") == 0,
    "SL 5.10b に公式集の項目はない: %d" % TEXT.count("{.callout-important}"))
not_in_text("この式は公式集にあります", "公式集の callout は置かない")
chk(TEXT.count("**検算") >= 12, "検算 12 以上: %d" % TEXT.count("**検算"))

_d = 0
for _l in TEXT.split("\n"):
    _t = _l.strip()
    if _t.startswith(":::"):
        _d += -1 if _t[3:].strip() == "" else 1
chk(_d == 0, "::: の開閉が合う: %d" % _d)

_verbs = re.compile(r"Explain|Justify|Comment|Interpret|Identify|Describe|Suggest")
_qs = [q for q in re.findall(r"\[([^\[\]]*?)\]\{\.q-en\}", TEXT, re.S)
       if _verbs.search(q)]
chk(TEXT.count("{.model-answer}") == len(_qs),
    "model-answer %d = 問い %d" % (TEXT.count("{.model-answer}"), len(_qs)))
chk(len(_qs) == 3, "Explain 系の問いは 3: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-10b-idea.svg){#fig-aasl510b-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl510b-idea (a)", "図 (a) の参照")
in_text("@fig-aasl510b-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ページをまたぐ相互参照は使わない（Quarto が解決できない）
chk(not re.search(r"@(eq|tbl|fig)-aasl(?!510b)", TEXT),
    "他ページの @ 参照: %s" % re.findall(r"@(?:eq|tbl|fig)-aasl\w+", TEXT))

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "SL 5.10 に引用してよいシラバス文はない: %s" % _quotes)

# ══════════════════════════════════════════════════════════
# 3. 式そのもの
# ══════════════════════════════════════════════════════════
in_text("\\int k\\,g'(x)\\,f(g(x))\\,dx\n$$ {#eq-aasl510b-form}", "見分ける形")
in_text("\\int g'(x)\\,f(g(x))\\,dx = F(g(x)) + C, \\qquad F'= f\n"
        "$$ {#eq-aasl510b-inspection}", "逆連鎖律の式")
in_text("u = g(x), \\qquad \\frac{du}{dx} = g'(x), \\qquad du = g'(x)\\,dx\n"
        "$$ {#eq-aasl510b-du}", "du の式")
in_text("\\int \\frac{g'(x)}{g(x)}\\,dx = \\ln\\lvert g(x)\\rvert + C\n"
        "$$ {#eq-aasl510b-log}", "log の式")
in_text("\\int \\frac{\\sin x}{\\cos x}\\,dx = -\\ln\\lvert\\cos x\\rvert + C\n"
        "$$ {#eq-aasl510b-tan}", "tan の式")
for _r in ("{#tbl-aasl510b-steps}", "{#tbl-aasl510b-constant}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-5.qmd#sum", "aasl-5-6a.qmd#chain",
           "aasl-5-10a.qmd#linear", "aasl-5-10a.qmd#lnabs",
           "aasl-5-10a.qmd#rational"):
    in_text(_a, "参照 " + _a)

_u = sp.Symbol("u", positive=True)
_g = sp.Function("g")
_F = sp.Function("F")
chk(sp.simplify(sp.diff(_F(_g(X)), X)
                - sp.Derivative(_F(_g(X)), X).doit()) == 0, "連鎖律の形")
chk(anti(sp.sin(X) / sp.cos(X), -sp.log(sp.cos(X))), "tan の原始関数")
chk(anti(1 / _u.subs(_u, X), sp.log(X)), "1/u の原始関数")

# 定数を合わせる表（例題・演習と重ならない 3 つ）
chk(sp.diff(5 * X ** 2 - 1, X) == 10 * X, "表: 5x^2-1 の導関数")
chk(sp.diff(X ** 5 + 2, X) == 5 * X ** 4, "表: x^5+2 の導関数")
chk(sp.simplify(sp.diff(sp.exp(X) + 3, X) - sp.exp(X)) == 0,
    "表: e^x+3 の導関数")
eq(1, R(1, 5) * 5, "表: x^4 = (1/5) x 5x^4")

# ══════════════════════════════════════════════════════════
# 4. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) Spotting the pattern"', "図 (a) の題")
in_fig('"(b) Integration by substitution"', "図 (b) の題")
in_fig("the derivative\\nof the inside", "図 (a) の左のラベル")
in_fig("the inside,\\n$u = g(x)$", "図 (a) の右のラベル")
in_fig("with no such factor, this method does not apply", "図 (a) の注意")
in_fig("every $x$ must disappear before integrating in $u$", "図 (b) の注意")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("x^{2} + 5", "x^{3} + 1", "\\sin^{3}", "18", "\\frac{2}{9}"):
    chk(_v not in _figmath, "図の数式に具体的な数・式 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 5. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(anti(6 * X * (X ** 2 + 5) ** 3, 3 * (X ** 2 + 5) ** 4 / 4), "例題1")
eq(6, 3 * 2, "例題1 の 3")
in_text("\\frac{3\\left(x^{2} + 5\\right)^{4}}{4} + C", "例題1 の答え")
in_text("u = x^{2} + 5, \\quad du = 2x\\,dx", "例題1 の u と du")

# 例題2
chk(anti(X ** 2 * sp.sqrt(X ** 3 + 1), R(2, 9) * (X ** 3 + 1) ** R(3, 2)),
    "例題2")
eq(R(1, 3) * R(2, 3), R(2, 9), "例題2 の係数")
eq(R(1, 2) + 1, R(3, 2), "例題2 の指数")
in_text("\\frac{2}{9}\\left(x^{3} + 1\\right)^{\\frac{3}{2}} + C", "例題2 の答え")

# 例題3
chk(anti(X * sp.exp(X ** 2), sp.exp(X ** 2) / 2), "例題3(a)")
chk(sp.simplify(sp.diff(sp.log(X ** 2 + 3 * X + 1), X)
                - (2 * X + 3) / (X ** 2 + 3 * X + 1)) == 0, "例題3(b)")
eq(9 - 4, 5, "例題3(b) の判別式")
chk(sp.discriminant(X ** 2 + 3 * X + 1, X) == 5, "例題3(b) 判別式は 5")
_XR = sp.Symbol("xr", real=True)
chk(len(sp.solve(sp.Eq(_XR ** 2 + 3 * _XR + 1, 0), _XR)) == 2,
    "例題3(b) 分母は 0 になりうる")
chk((_XR ** 2 + 3 * _XR + 1).subs(_XR, -1) < 0, "例題3(b) x=-1 で分母が負")
in_text("\\frac{1}{2}e^{x^{2}} + C", "例題3(a) の答え")
in_text("\\ln\\lvert x^{2} + 3x + 1\\rvert + C", "例題3(b) の答え")

# 例題4
chk(anti(sp.sin(X) ** 3 * sp.cos(X), sp.sin(X) ** 4 / 4), "例題4")
in_text("\\frac{\\sin^{4}x}{4} + C", "例題4 の答え")
chk(sp.sin(0) == 0, "例題4 の x=0")
chk(sp.simplify(sp.diff(sp.cos(X), X) + sp.sin(X)) == 0, "例題4 cos の導関数")

# ══════════════════════════════════════════════════════════
# 6. 演習
# ══════════════════════════════════════════════════════════
chk(anti(12 * X ** 3 * (X ** 4 - 5) ** 2, (X ** 4 - 5) ** 3), "演習1")
eq(12, 3 * 4, "演習1 の 3")
in_text("\\left(x^{4} - 5\\right)^{3} + C", "演習1 の答え")

chk(anti(sp.cos(X) / (2 + sp.sin(X)), sp.log(2 + sp.sin(X))), "演習2")
chk(all((2 + sp.sin(_t)) >= 1 for _t in (0, sp.pi / 2, sp.pi, 3 * sp.pi / 2)),
    "演習2 の 2+sin x は 1 以上")
in_text("\\ln\\left(2 + \\sin x\\right) + C", "演習2 の答え")

chk(sp.simplify(sp.diff(sp.log(X ** 3 + 1), X)
                - 3 * X ** 2 / (X ** 3 + 1)) == 0, "演習3")
in_text("\\ln\\lvert x^{3} + 1\\rvert + C", "演習3 の答え")
chk((-2) ** 3 + 1 < 0, "演習3 x=-2 で中身が負")

chk(anti(sp.cos(X) * sp.exp(sp.sin(X)), sp.exp(sp.sin(X))), "演習4")
in_text("e^{\\sin x} + C", "演習4 の答え")

chk(anti(X / sp.sqrt(X ** 2 + 9), sp.sqrt(X ** 2 + 9)), "演習5")
eq(R(-1, 2) + 1, R(1, 2), "演習5 の指数")
eq(R(1, 2) * 2, 1, "演習5 の係数")
in_text("\\sqrt{x^{2} + 9} + C", "演習5 の答え")

chk(anti(sp.sin(X) * sp.cos(X) ** 4, -sp.cos(X) ** 5 / 5), "演習6")
in_text("-\\frac{\\cos^{5}x}{5} + C", "演習6 の答え")

chk(sp.simplify(sp.diff(sp.log(X ** 2 + 2 * X + 7) / 2, X)
                - (X + 1) / (X ** 2 + 2 * X + 7)) == 0, "演習7")
chk(sp.simplify((X + 1) ** 2 + 6 - (X ** 2 + 2 * X + 7)) == 0, "演習7 の平方完成")
eq(4 - 28, -24, "演習7 の判別式")
chk(sp.discriminant(X ** 2 + 2 * X + 7, X) == -24, "演習7 判別式は -24")
in_text("\\frac{1}{2}\\ln\\left(x^{2} + 2x + 7\\right) + C", "演習7 の答え")

chk(anti(6 * X ** 2 / (X ** 3 + 2) ** 2, -2 / (X ** 3 + 2)), "演習8")
eq(6, 2 * 3, "演習8 の 2")
eq(-1 + 1, 0, "演習8 の指数（-2 は -1 にならない）")
in_text("-\\frac{2}{x^{3} + 2} + C", "演習8 の答え")
in_text("2\\int u^{-2}\\,du", "演習8(b)")

chk(anti(X * (X ** 2 + 1) ** 3, (X ** 2 + 1) ** 4 / 8), "演習9 の正しい答え")
chk(sp.simplify(sp.diff((X ** 2 + 1) ** 4 / 4, X)
                - 2 * X * (X ** 2 + 1) ** 3) == 0, "演習9 の 1 人めは 2 倍")
eq(4 * 2, 8, "演習9 の分母")
in_text("\\dfrac{\\left(x^{2}+1\\right)^{4}}{8} + C$, is correct*",
        "演習9 の答え")

chk(sp.expand((X ** 2 + 1) ** 4)
    == X ** 8 + 4 * X ** 6 + 6 * X ** 4 + 4 * X ** 2 + 1, "演習10 の展開")
in_text("x^{8} + 4x^{6} + 6x^{4} + 4x^{2} + 1", "演習10 の展開の式")
chk(anti(2 * X * (X ** 2 + 1) ** 4, (X ** 2 + 1) ** 5 / 5), "演習10 の 1 つめ")

# ══════════════════════════════════════════════════════════
# 7. 答えを本文に出していないか
# ══════════════════════════════════════════════════════════
for _v in ("\\frac{3\\left(x^{2} + 5\\right)^{4}}{4}",
           "\\frac{2}{9}\\left(x^{3} + 1\\right)^{\\frac{3}{2}}",
           "\\frac{1}{2}e^{x^{2}}", "\\frac{\\sin^{4}x}{4}",
           "\\left(x^{2} - 3\\right)^{4}",
           "\\frac{\\left(x^{3} + 4\\right)^{6}}{18}",
           "-\\frac{\\cos^{5}x}{5}", "\\sqrt{x^{2} + 9} + C"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 8. ページに書いてある計算を、機械的にたしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(
    r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|[\d.(^]|\\(?!ldots|approx)))"
    % (_EXPR, _EXPR))


def _tonum(t):
    t = t.strip()
    m = re.fullmatch(r"\\[dt]?frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2)))
    return sp.Rational(t)


def _value(expr):
    total = sp.Integer(0)
    sign = 1
    for _tk in re.finditer(r"([+-])|(%s)" % _TERM, expr):
        if _tk.group(1):
            sign = 1 if _tk.group(1) == "+" else -1
        else:
            prod = sp.Integer(1)
            for _f in re.finditer(_ATOM, _tk.group(2)):
                prod *= _tonum(_f.group(0))
            total += sign * prod
    return total


_nstmt = 0
for _m in _STMT.finditer(TEXT):
    _before = TEXT[:_m.start()].rstrip()
    if _before and _before[-1] in "+-=)*/(":
        continue
    if _before.endswith("\\times") or _before.endswith("\\div"):
        continue
    if re.search(r"(\\(?:sin|cos|tan|ln|log|exp|sqrt)|[{^_])$", _before):
        continue
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 2, "ページの計算を %d 本たしかめた" % _nstmt)
print("  （計算 %d 本）" % _nstmt)

# ══════════════════════════════════════════════════════════
# 見直し（2026-09）で直したところ。もどってしまわないように。
# ══════════════════════════════════════════════════════════

# --- B1: 例題4(b)「u = cos x では解けない」は偽だった -------------------
chk("Explain why $u = \\sin x$ works here, but the same substitution does not "
    "help for $\\displaystyle\\int \\sin^{3}x\\,dx$." in TEXT, "例題4(b) の英語")
chk("Explain why $u = \\sin x$ works here but $u = \\cos x$ does not."
    not in TEXT, "偽だった設問が消えている")
chk("**検算（$u = \\cos x$ でも）。**" in TEXT, "例題4: u = cos x でも解ける")
# sin^4 x / 4 と cos^4 x / 4 - cos^2 x / 2 は定数 1/4 だけちがう
chk(sp.simplify(sp.cos(X) ** 4 / 4 - sp.cos(X) ** 2 / 2
                - (sp.sin(X) ** 4 / 4 - R(1, 4))) == 0,
    "u = cos x の答えとの差は 1/4")
chk(sp.simplify(sp.sin(X) ** 2 - (1 - sp.cos(X) ** 2)) == 0, "sin^2 = 1-cos^2")

# --- B2: 演習6 の検算も同じ理由で偽だった ---------------------------------
chk("**検算（$u = \\sin x$ ではうまくいかない）。**" in TEXT, "演習6 の検算")
chk("$u = \\sin x$ とすると $\\cos^{4}x$ が $u$ で書けません" not in TEXT,
    "偽だった検算が消えている")
chk(sp.simplify(sp.cos(X) ** 4 - (1 - sp.sin(X) ** 2) ** 2) == 0,
    "cos^4 は u で書ける")

# --- B3: 第7節の自己矛盾 -------------------------------------------------
chk("**中身が $ax+b$ でもなく、$g'(x)$ もかかっていないときは、置換以外の手を"
    "考えます。**" in TEXT, "第7節: 言い切りを直した")
chk("SL では出ません。" not in TEXT, "自己矛盾していた言い切りが消えている")

# --- B4: g(x) ≠ 0 と、絶対値を外してよい場合 -------------------------------
chk("**この形が使えるのは、$g(x) \\ne 0$ である区間の中です。**" in TEXT,
    "第6節: g(x) ≠ 0")
chk("**定義域から $g(x) > 0$ と分かるときだけ、絶対値を外して $\\ln g(x)$ と"
    "書けます**" in TEXT, "第6節: 絶対値を外してよい場合")
chk("**絶対値を落とさないでください。** $g(x)$ が負になる範囲もあるからです。"
    not in TEXT, "演習7 と矛盾していた言い切りが消えている")

# --- B5: 例題1 の「同じ関数になります」は偽 --------------------------------
chk("**検算（展開しても合うか）。**" in TEXT, "例題1: 展開して確かめる")
chk("それを積分しても同じ関数になります" not in TEXT, "定数を無視した文が消えている")
chk(sp.expand(6 * X * (X ** 2 + 5) ** 3)
    == 6 * X ** 7 + 90 * X ** 5 + 450 * X ** 3 + 750 * X, "例題1 の展開")
chk(sp.expand(3 * (X ** 2 + 5) ** 4 / 4)
    - (R(3, 4) * X ** 8 + 15 * X ** 6 + R(225, 2) * X ** 4 + 375 * X ** 2)
    == R(1875, 4), "例題1 の定数のちがい")
in_text("6x^{7} + 90x^{5} + 450x^{3} + 750x", "例題1 の展開の式")

# --- M1: 見て書く（inspection）を実際にやらせる ------------------------------
chk("by inspection, without writing a substitution. Verify your answer by "
    "differentiating it." in TEXT, "演習4: 見て書く + 微分して確かめる")
chk("$F' = f$ となる $F$ を使うと、$F(g(x))$ を微分したものが "
    "$g'(x)\\,f(g(x))$ です。" in TEXT, "第2節: F を使って正しく書いた")
chk("$f(g(x))$ を微分すると $g'(x)$ がかかるので" not in TEXT,
    "f と F を混同していた文が消えている")

# --- M2: 定数を合わせる表が、演習の答えを見せていた ----------------------------
chk("| $10x\\left(5x^{2}-1\\right)^{2}$ | $5x^{2}-1$ | $10x$ | そのまま |"
    in TEXT, "表の 1 行目")
chk("| $6x(x^{2}+5)^{3}$ |" not in TEXT, "例題1 の式が表から消えている")
chk("| $\\cos x\\,e^{\\sin x}$ |" not in TEXT, "演習4 の式が表から消えている")

# --- M3: Why it works・第7節・Common errors の例を分けた ----------------------
chk("$\\displaystyle\\int \\sqrt{x^{2}+1}\\,dx$ で $u = x^{2}+1$ と置くと"
    in TEXT, "Why it works の例")
chk("$\\displaystyle\\int \\left(x^{2}+3\\right)^{2}dx$ には $2x$ が"
    in TEXT, "第7節の例")
chk("$\\displaystyle\\int \\left(x^{2}+3\\right)^{2}dx$ には使えません。" in TEXT,
    "Common errors の例")
chk(BODY.count("(x^{2}+1)^{4}") == 0, "本文（例題より前）に演習10 の式が残っていない")

# --- M4: 演習の型がかたよっていた ----------------------------------------------
chk("Find $\\displaystyle\\int 12x^{3}\\left(x^{4} - 5\\right)^{2}dx$" in TEXT,
    "演習1 の英語")
chk("Find $\\displaystyle\\int \\frac{\\cos x}{2 + \\sin x}\\,dx$" in TEXT,
    "演習2 の英語（g'/g の三角の形）")
chk("Consider $\\displaystyle\\int \\frac{6x^{2}}{\\left(x^{3} + 2\\right)^{2}}"
    "\\,dx$." in TEXT, "演習8 の英語")
chk("Find $\\displaystyle\\int 8x\\left(x^{2} - 3\\right)^{3}dx$" not in TEXT,
    "例題1 と同型だった演習1 が消えている")
chk("Consider $\\displaystyle\\int 10x\\left(x^{2} + 1\\right)^{4}dx$"
    not in TEXT, "演習10 と重なっていた演習8 が消えている")

# --- M5: 循環していた検算 --------------------------------------------------------
chk("**検算（差で）。**" in TEXT, "例題4: 差で確かめる")
chk("**検算（値で）。** $x = 0$ では" not in TEXT, "C に依存する検算が消えている")
chk("**検算（$4$ 乗になる理由）。**" not in TEXT, "言いかえだった検算が消えている")
chk("**検算（定数を落としていないか）。**" in TEXT, "演習4: 定数の検算")
chk("**検算（定数の調整）。** $\\cos x$ がぴったりなので" not in TEXT,
    "言いかえだった検算が消えている（演習4）")

# --- M6: 答案の書き方が、解答例と矛盾していた --------------------------------------
chk("**置換で解いたときは、$u$ と $du$ を書いた行を答案に残してください。**"
    in TEXT, "Paper の callout")
chk("**答案には、$u$ と $du$ を書いた行を残してください。**" not in TEXT,
    "矛盾していた指示が消えている")

# --- M7: 「不定積分では」をやめた ---------------------------------------------------
chk("**最後に $u = g(x)$ をもどして、$x$ の式で答えを書きます。**" in TEXT,
    "第3節: もどす")
chk("**不定積分では、最後に $x$ にもどします。**" not in TEXT,
    "定積分を示唆していた文が消えている")

# --- m1 から m9 ---------------------------------------------------------------------
chk("- **integration by inspection**（見て書く逆連鎖律）で答えを書き、"
    in TEXT, "m1: 用語の順")
chk("**$g'(x)\\,dx$ のかたまりを、まるごと $du$ に置きかえるのが要点です。**"
    in TEXT, "m2: du の置きかえ")
for _r in ("@eq-aasl510b-du", "@eq-aasl510b-inspection", "@eq-aasl510b-tan",
           "@tbl-aasl510b-constant", "@eq-aasl510b-form",
           "@eq-aasl510b-log", "@tbl-aasl510b-steps"):
    chk(_r in TEXT, "m3: 参照 " + _r)
chk("$g'(x) = a$ が定数なので（$a \\ne 0$）" in TEXT, "m4: a ≠ 0")
chk("**検算（$3$ の出どころ）。** $3 \\times 2x = 6x$ です ✓" in TEXT,
    "m5: 恒等式で書く")
chk("$6x \\div 2x = 3$" not in TEXT, "割り算だった検算が消えている")
chk("$\\dfrac{1}{u}$ を $u^{n}$ と見ると $n = -1$ なので" in TEXT,
    "m6: 分母の指数の言い方")
chk("answer in $u$, add $+C$, then put $g(x)$ back" in FIG, "m7: 図に +C")
chk("with plus C added and g of x put back" in TEXT, "m7: alt に +C")
chk("シラバスがこの形をそのまま挙げています。" not in TEXT,
    "m8: シラバスに訴える言い方が消えている")
chk("シラバスは、この形の例として" not in TEXT,
    "m8: シラバスに訴える言い方が消えている（2）")
chk("Describe how differentiating shows which one is correct." in TEXT,
    "m9: 演習9 は Describe")
chk("A student writes $\\displaystyle\\int x\\left(x^{2} + 1\\right)^{3}dx"
    not in TEXT, "隣ページと同じ枠だった演習9 が消えている")

print()
print("OK", OK, "/ NG", NG)
