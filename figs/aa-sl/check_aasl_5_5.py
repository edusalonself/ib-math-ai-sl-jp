# -*- coding: utf-8 -*-
"""AA SL 5.5 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_5.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-5.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_5.py")

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
X = sp.Symbol("x")
C = sp.Symbol("C")


def anti(f):
    """f の原始関数（+C なし）。"""
    return sp.simplify(sp.integrate(sp.expand(sp.together(f)), X))


def back(F, f):
    """F を微分して f にもどるか。"""
    return sp.simplify(sp.diff(F, X) - sp.simplify(f)) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.5 — Introduction to integration（原始関数・積分定数・面積） "
        "{#sec-aasl-5-5}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["anti", "plusc", "power", "sum",
                              "boundary", "area", "expression"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper）")
chk(TEXT.count("{.callout-important}") == 2,
    "callout-important 2（公式集 5.5 の 2 つ）")
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
chk(len(_qs) == 4, "Explain 系の問いは 4: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-5-idea.svg){#fig-aasl55-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl55-idea (a)", "図 (a) の参照")
in_text("@fig-aasl55-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == ["Students are expected to first write a correct expression "
                "before calculating the area."],
    "シラバスの引用は 1 本だけ: %s" % _quotes)
in_text("公式集の **5.5** の欄に、*Integral of $x^{n}$* として", "公式集 5.5 積分")
in_text("公式集の **5.5** の欄に、*Area between a curve $y = f(x)$ and the "
        "$x$-axis, where $f(x) > 0$* として", "公式集 5.5 面積")
in_text("**「$f(x) > 0$」という条件も、いっしょに印刷されています。**",
        "条件も公式集にある")
in_text("**@eq-aasl55-sum は公式集にありません。**", "和と定数倍は公式集にない")

in_text("\\int x^{n}\\,dx = \\frac{x^{n+1}}{n+1} + C, \\qquad n \\ne -1\n"
        "$$ {#eq-aasl55-power}", "べき乗の積分の式")
in_text("A = \\int_{a}^{b} y\\,dx\n$$ {#eq-aasl55-area}", "面積の式")
in_text("$$ {#eq-aasl55-def}", "積分の記号の式")
in_text("$$ {#eq-aasl55-sum}", "和と定数倍の式")
in_text("{#tbl-aasl55-bc}", "境界条件の表")
in_text("{#tbl-aasl55-we1}", "例題1 の表")
for _a in ("aasl-5-10a.qmd", "aasl-5-11a.qmd", "aasl-5-11b.qmd"):
    in_text(_a, "先のページへの参照 " + _a)
in_text("[SL 5.3](aasl-5-3.qmd#zeroderiv)", "5.3 への参照")
in_text("[SL 5.2](aasl-5-2.qmd#interval)", "5.2 への参照（区間）")

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) Why the constant is needed"', "図 (a) の題")
in_fig('"(b) Area under a curve that stays above the axis"', "図 (b) の題")
in_fig('"$+C$"', "図 (a) の +C")
in_fig('"the curves differ only by a vertical shift"', "図 (a) の説明")
in_fig("when $f(x) > 0$ ", "図 (b) の条件")
in_fig('"write the expression first, then work out its value"', "図 (b) の注意")
# 図の 3 本の曲線は、同じ x で同じ傾き
_g = X ** 3 - 2 * X
for _c in (R(3, 2), 0, R(-3, 2)):
    eq(sp.diff(_g + _c, X).subs(X, R(5, 4)),
       sp.diff(_g, X).subs(X, R(5, 4)), "図(a) 傾きは C によらない")
# 図(b) の曲線は a と b の間で正
_h = R(11, 50) * (X - R(11, 10)) ** 2 + R(23, 20)
for _v in (R(13, 10), 2, 3, R(39, 10)):
    chk(_h.subs(X, _v) > 0, "図(b) f(%s) > 0" % _v)
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("10.7", "7.33", "2x^{3}", "x^{4} - 3x^{2}", "6x + 3"):
    chk(_v not in _figmath, "図の数式に答え %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_f1 = 6 * X ** 2 - 4 * X + 5
eq(anti(_f1), 2 * X ** 3 - 2 * X ** 2 + 5 * X, "例題1 の原始関数")
chk(back(2 * X ** 3 - 2 * X ** 2 + 5 * X, _f1), "例題1 微分でもどる")
eq(R(6, 3), 2, "例題1 の係数 1")
eq(R(-4, 2), -2, "例題1 の係数 2")
in_text("2x^{3} - 2x^{2} + 5x + C", "例題1 の答え")

# 例題2  dy/dx = 4x^3 - 6x、x=2 で y=5
_f2 = 4 * X ** 3 - 6 * X
eq(anti(_f2), X ** 4 - 3 * X ** 2, "例題2 の原始関数")
chk(sp.solve(sp.Eq(anti(_f2).subs(X, 2) + C, 5), C) == [1], "例題2 C = 1")
eq((X ** 4 - 3 * X ** 2 + 1).subs(X, 2), 5, "例題2 条件を満たす")
chk(back(X ** 4 - 3 * X ** 2 + 1, _f2), "例題2 微分でもどる")
eq(2 ** 4, 16, "例題2 検算 2^4")
eq(3 * 2 ** 2, 12, "例題2 検算 3*2^2")
in_text("y = x^{4} - 3x^{2} + 1", "例題2 の答え")

# 例題3  y = x^2 + 1、1 から 3
_f3 = X ** 2 + 1
_A3 = sp.integrate(_f3, (X, 1, 3))
eq(_A3, R(32, 3), "例題3 の面積（正確な値）")
chk(abs(float(_A3) - 10.6667) < 1e-3, "例題3 の面積 ≈ 10.67")
chk(float("%.3g" % float(_A3)) == 10.7, "例題3 の 3 桁は 10.7")
for _v in (1, 2, 3):
    chk(_f3.subs(X, _v) > 0, "例題3 f(%s) > 0" % _v)
eq(_f3.subs(X, 1), 2, "例題3 左端の高さ")
eq(_f3.subs(X, 3), 10, "例題3 右端の高さ")
chk(2 * 2 < float(_A3) < 2 * 10, "例題3 長方形ではさむ")
in_text("A = \\int_{1}^{3} (x^{2} + 1)\\,dx", "例題3 の式")
in_text("A = 10.7 \\ (3 \\text{ s.f.})", "例題3 の値")

# 例題4  (x^3 + 2)/x^2
_f4 = (X ** 3 + 2) / X ** 2
eq(sp.simplify(_f4 - (X + 2 * X ** -2)), 0, "例題4 の書きかえ")
eq(anti(_f4), X ** 2 / 2 - 2 / X, "例題4 の原始関数")
chk(back(X ** 2 / 2 - 2 * X ** -1, _f4), "例題4 微分でもどる")
eq(-2 + 1, -1, "例題4 指数を 1 増やす")
eq(R(2, -1), -2, "例題4 新しい指数で割る")
eq(_f4.subs(X, 1), 3, "例題4 検算 x=1 もとの式")
eq((X + 2 * X ** -2).subs(X, 1), 3, "例題4 検算 x=1 直した式")

# ══════════════════════════════════════════════════════════
# 5. 演習の答え
# ══════════════════════════════════════════════════════════
_E = [("演習1", 4 * X + 3, 2 * X ** 2 + 3 * X),
      ("演習2", X ** 5 - 3 * X ** 2, X ** 6 / 6 - X ** 3),
      ("演習3", (X ** 4 + 3) / X ** 2, X ** 3 / 3 - 3 / X),
      ("演習4", 5 * X ** -3, R(-5, 2) * X ** -2),
      ("演習5", 6 * X - 2, 3 * X ** 2 - 2 * X),
      ("演習6", 3 * X ** 2 + 4 * X, X ** 3 + 2 * X ** 2),
      ("演習8", 3 * X ** 2, X ** 3)]
for _name, _f, _F in _E:
    eq(anti(_f), _F, "%s の原始関数" % _name)
    chk(back(_F, _f), "%s 微分でもどる" % _name)

chk(sp.solve(sp.Eq((3 * X ** 2 - 2 * X).subs(X, 2) + C, 7), C) == [-1],
    "演習5 C = -1")
eq((3 * X ** 2 - 2 * X - 1).subs(X, 2), 7, "演習5 条件を満たす")
chk(sp.solve(sp.Eq((X ** 3 + 2 * X ** 2).subs(X, 1) + C, 0), C) == [-3],
    "演習6 C = -3")
eq((X ** 3 + 2 * X ** 2 - 3).subs(X, 1), 0, "演習6 条件を満たす")
eq(R(-3, 3), -1, "演習2 の係数")
eq(-3 + 1, -2, "演習4 の指数")
eq(R(5, -2), R(-5, 2), "演習4 の係数")

# 演習7  y = 4 - x^2、-1 から 1
_f7 = 4 - X ** 2
_A7 = sp.integrate(_f7, (X, -1, 1))
eq(_A7, R(22, 3), "演習7 の面積（正確な値）")
chk(float("%.3g" % float(_A7)) == 7.33, "演習7 の 3 桁は 7.33")
for _v in (-1, 0, 1):
    chk(_f7.subs(X, _v) >= 3, "演習7 f(%s) >= 3 > 0" % _v)
chk(2 * 3 < float(_A7) < 2 * 4, "演習7 長方形ではさむ")
eq(2 * sp.integrate(_f7, (X, 0, 1)), _A7, "演習7 対称なので 2 倍")
in_text("A = \\int_{-1}^{1} (4 - x^{2})\\,dx", "演習7 の式")
in_text("$$A = 7.33$$", "演習7 の値")

# 演習8  生徒のまちがい
eq(sp.diff(6 * X, X), 6, "演習8 生徒の答えを微分すると 6")
chk(sp.simplify(sp.diff(6 * X, X) - 3 * X ** 2) != 0, "演習8 もとにもどらない")
eq(sp.diff(3 * X ** 2, X), 6 * X, "演習8 6x は 3x^2 の導関数")

# 演習10  y = x^3、1 から 2
_f10 = X ** 3
eq(sp.integrate(_f10, (X, 1, 2)), R(15, 4), "演習10 の面積（正確な値）")
for _v in (1, R(3, 2), 2):
    chk(_f10.subs(X, _v) > 0, "演習10 f(%s) > 0" % _v)
eq(_f10.subs(X, 1), 1, "演習10 左端")
eq(_f10.subs(X, 2), 8, "演習10 右端")
in_text("A = \\int_{1}^{2} x^{3}\\,dx", "演習10 の式")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("2x^{3} - 2x^{2} + 5x", "x^{4} - 3x^{2}", "10.7", "7.33",
           "2x^{2} + 3x", "\\frac{x^{6}}{6}", "6x + C", "x^{3} + 2x^{2}"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 6. ページに書いてある計算を、機械的にたしかめる
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
    if _before.endswith("\\times"):
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

# --- B1: 「導関数が 0 なら定数」に区間の条件がついている ----------
chk("**逆に、$1$ つの区間の上では、原始関数どうしのちがいは定数だけです。**"
    in TEXT, "Why it works: 区間の上での話だと書いている")
chk("**途切れのない $1$ つの区間**でどちらも $f$ の原始関数なら" in TEXT,
    "Why it works: 途切れのない区間という条件")
chk("**$x \\ne 0$ のように、$x$ の動ける範囲が $2$ つに分かれているときは、"
    "区間ごとに定数です。**" in TEXT, "Why it works: 分かれた範囲の但し書き")
chk("水平な直線、つまり定数です" not in TEXT,
    "結論を言いかえただけの文が消えている")
chk("aasl-5-2.qmd#sign" not in TEXT, "点についての節への誤った参照が消えている")

# --- M1: 見出しが、実際に示していることに合っている ----------------
chk("**なぜ、面積と原始関数がつながるのでしょうか。**" in TEXT,
    "Why it works の見出し")
chk("**なぜ、面積が定積分になるのでしょうか。**" not in TEXT,
    "定義から明らかなことを問う見出しが消えている")
chk("この面積の名前として使っています。" in TEXT,
    "Why it works: 記号は面積の名前だと断っている")

# --- M2: 直してから積分する目標と、それを練習する演習 ---------------
chk("- 分数を、**まず $ax^{n}$ の和の形に直してから**積分できる。" in TEXT,
    "目標: 直してから積分する")
chk("Find $\\displaystyle\\int \\frac{x^{4} + 3}{x^{2}}\\,dx$, for $x \\ne 0$."
    in TEXT, "演習3: 直してから積分する問題")
chk("\\frac{x^{4} + 3}{x^{2}} = x^{2} + 3x^{-2}" in TEXT, "演習3 の書きかえ")
chk("Find $\\displaystyle\\int 6\\,dx$." not in TEXT,
    "第4節の結果をそのまま問うていた古い演習3 が消えている")

# --- M3: 原始関数と面積のつながりを聞く部分がある -------------------
chk("State how an anti-derivative of $f$ is used to find that value."
    in TEXT, "演習9: 原始関数の使い方を聞いている")
chk("take any anti-derivative $F$ of $f$ and work out $F(b) - F(a)$" in TEXT,
    "演習9 の答え")

# --- M4: 演習10 の command term は Explain ----------------------
chk("Explain why the condition needed for that expression is satisfied here."
    in TEXT, "演習10: Explain")
chk("Interpret why the condition" not in TEXT,
    "IB が使わない Interpret why が消えている")

# --- M5: 電卓の callout の見出し --------------------------------
chk("## Paper 2 では、電卓で値を出します" in TEXT, "電卓の節の見出し")
chk("この項目では、定積分の**値そのものを電卓で出します**。" in TEXT,
    "電卓の節: 値そのものを出すと書いている")
chk("## Paper 2 では、電卓でこう確かめます" not in TEXT,
    "確かめに使うと読める見出しが消えている")

# --- m1: indefinite integral の英語を出している -------------------
chk("**indefinite integral**（不定積分）の答えには、必ず付けます。" in TEXT,
    "第2節: 不定積分の英語")

# --- m6: 面積の範囲に縦の直線が入っている -------------------------
chk("曲線 $y = f(x)$、$x$ 軸、直線 $x = a$、直線 $x = b$ でかこまれた部分の面積は"
    in TEXT, "第6節: かこむ 4 つ")

# --- m7: 負の指数のときの範囲 ------------------------------------
chk("**$n$ が負のときは、$x \\ne 0$ のところだけで使えます**" in TEXT,
    "第3節: 負の指数のときの範囲")
chk("この形の問題文に「for $x \\ne 0$」と書いてあるのは、そのためです。" in TEXT,
    "第3節: 問題文の but し書きの理由")

# --- m3/m4/m5: 中身のない検算を差しかえた -------------------------
chk("**検算（値で見当をつける）。**" in TEXT, "例題1: 値による検算")
chk("**検算（係数）。** $\\dfrac{6}{3} = 2$" not in TEXT,
    "表を書き写すだけの検算が消えている")
chk("**検算（対称を使って）。**" in TEXT, "演習7: 数の出る対称の検算")
chk("**検算（対称）。** $4 - x^{2}$ は $y$ 軸について対称なので、$0$ から"
    not in TEXT, "数の出ない検算が消えている")
chk("**検算（数で確かめる）。**" in TEXT, "演習9: 数で確かめる検算")
chk("**検算（面積として）。** 面積は $1$ つに決まる量です" not in TEXT,
    "結論を言いかえただけの検算が消えている")

print()
print("OK", OK, "/ NG", NG)
