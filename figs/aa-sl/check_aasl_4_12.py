# -*- coding: utf-8 -*-
"""AA SL 4.12 のページを検算する。

    python3 figs/aa-sl/check_aasl_4_12.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability",
                   "aasl-4-12.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_12.py")

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


def close(a, b, tol, msg=""):
    chk(abs(float(a) - float(b)) < tol, "%s :: %s vs %s" % (msg, a, b))


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

# 標準正規分布の逆関数（sympy で正確に）
_z = sp.Symbol("z")


def Z(area):
    """P(Z < z) = area となる z。"""
    return float(sp.nsolve(sp.erf(_z / sp.sqrt(2)) / 2 + sp.Rational(1, 2)
                           - sp.Rational(str(area)), _z, 0.0))


def PHI(z):
    """P(Z < z)。"""
    return float(sp.erf(sp.Float(z) / sp.sqrt(2)) / 2 + sp.Rational(1, 2))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 4.12 — Standardization and unknown $\\mu$, $\\sigma$"
        "（標準化と、未知の平均・標準偏差） {#sec-aasl-4-12}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Using your GDC (TI-Nspire CX II)", "## Exercises"):
    in_text(_h, "節 " + _h)

# GDC の節は Exercises の直前
chk(TEXT.index("## Using your GDC") < TEXT.index("## Exercises"),
    "GDC の節は Exercises の前")
chk(TEXT.index("## Common errors") < TEXT.index("## Using your GDC"),
    "GDC の節は Common errors の後")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)] + ["1", "2", "3"],
    "### の番号 1..7 と GDC の 1..3: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["zvalue", "meaning", "back", "compare",
                              "unknown", "both", "writing",
                              "gdc-invnorm01", "gdc-nosolve", "gdc-check"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper 2）")
chk(TEXT.count("{.callout-important}") == 1,
    "callout-important 1（公式集 4.12 の z）")
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
chk(len(_qs) == 8, "Explain 系の問いは 8: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-4-12-idea.svg){#fig-aasl412-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl412-idea (a)", "図 (a) の参照")
in_text("@fig-aasl412-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "シラバスの引用は使わない: %s" % _quotes)
in_text("公式集の **4.12** の欄に、*Standardized normal variable* として",
        "公式集 4.12 の欄")
in_text("**@eq-aasl412-x は公式集にありません。**", "x = mu + z*sigma は公式集にない")
not_in_text("公式集の **4.9**", "4.9 には公式集の欄がない")

in_text("z = \\frac{x - \\mu}{\\sigma}\n$$ {#eq-aasl412-z}", "z の定義式")
in_text("x = \\mu + z\\sigma\n$$ {#eq-aasl412-x}", "x にもどす式")
in_text("$$ {#eq-aasl412-pair}", "連立の式")
in_text("$$ {#eq-aasl412-sigma}", "sigma の式")
in_text("{#tbl-aasl412-read}", "z の読み方の表")
in_text("{#tbl-aasl412-steps}", "手順の表")
in_text("{#tbl-aasl412-inv}", "invNorm に入れる面積の表")

for _a in ("#empirical", "#inverse"):
    in_text("[SL 4.9](aasl-4-9.qmd%s)" % _a, "4.9 への参照 " + _a)

# ══════════════════════════════════════════════════════════
# 3. 検証ずみの GDC の操作しか書いていないこと
# ══════════════════════════════════════════════════════════
in_text("menu → Statistics → Distributions", "Distributions のメニュー")
in_text("`invNorm(area, μ, σ)`", "invNorm の引数")
# 2026-09: 生徒は全員 TI-Nspire CX II なので、CAS／非CAS の区別には触れない
in_text("**TI-Nspire CX II に `solve(` はありません。**", "solve( はない")
not_in_text("非 CAS")
for _bad in ("Add Calculator", "Binomial Pdf", "X List", "Y List",
             "normalcdf", "invnorm(", "Normal Cdf", "One-Variable"):
    not_in_text(_bad, "検証していない GDC の記述: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 図
# ══════════════════════════════════════════════════════════
in_fig(r'r"$z = \frac{x - \mu}{\sigma}$"', "図 (a) の z の式")
in_fig(r'r"$x = \mu + z\sigma$ goes the other way"', "図 (a) の逆向き")
in_fig(r'r"$a = \mu + z_1\sigma$    and    $b = \mu + z_2\sigma$"',
       "図 (b) の連立")
in_fig("two equations, two unknowns", "図 (b) の説明")
# 図に数値の答えを出していないこと（座標の数は数えないよう、$...$ の中だけ見る）
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("1.5", "1.4", "1.1", "46.2", "9.42", "42.1", "13.7", "498",
           "0.15", "0.25"):
    chk(_v not in _figmath, "図の数式に答え %s は出さない" % _v)
for _v in ("invNorm", "normCdf", "46.2", "9.42", "42.1", "13.7", "22.6",
           "108", "497", "0.00135"):
    chk(_v not in FIGCODE, "図に答え %s は出さない" % _v)
# matplotlib mathtext が読めない記法を使っていないこと
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 5. 例題1  X ~ N(54, 8^2)
# ══════════════════════════════════════════════════════════
eq(R(66 - 54, 8), R("1.5"), "例題1(a) z")
eq(54 + R("-0.75") * 8, 48, "例題1(b) x")
eq(54 + R("1.5") * 8, 66, "例題1(a) 検算 もどす")
eq(R(54 - 48, 8), R("0.75"), "例題1(b) 検算 sigma いくつぶん")
chk(R(66 - 54, 8) > 0, "例題1 z は正")
in_text("z = \\frac{66 - 54}{8} = \\frac{12}{8} = 1.5", "例題1(a) の式")
in_text("x = 54 + (-0.75)(8) = 54 - 6 = 48", "例題1(b) の式")

# ══════════════════════════════════════════════════════════
# 6. 例題2  数学 N(58, 5^2) 65 点 / 理科 N(72, 10^2) 83 点
# ══════════════════════════════════════════════════════════
_zm = R(65 - 58, 5)
_zs = R(83 - 72, 10)
eq(_zm, R("1.4"), "例題2 数学の z")
eq(_zs, R("1.1"), "例題2 理科の z")
chk(_zm > _zs, "例題2 数学のほうが上")
chk(83 > 65, "例題2 生の点では理科が上（z で逆転する）")
chk(_zm > 0 and _zs > 0, "例題2 どちらも平均より上")
in_text("z_{\\text{maths}} = \\frac{65 - 58}{5} = \\frac{7}{5} = 1.4",
        "例題2 数学")
in_text("z_{\\text{science}} = \\frac{83 - 72}{10} = \\frac{11}{10} = 1.1",
        "例題2 理科")

# ══════════════════════════════════════════════════════════
# 7. 例題3  X ~ N(mu, 6^2), P(X < 40) = 0.15
# ══════════════════════════════════════════════════════════
_z3 = Z("0.15")
close(_z3, -1.0364334, 1e-6, "例題3(a) z = invNorm(0.15,0,1)")
chk(_z3 < 0, "例題3 面積 0.15 < 0.5 なので z < 0")
_mu3 = 40 - 6 * _z3
close(_mu3, 46.218600, 1e-5, "例題3(b) mu")
close(float("%.3g" % _mu3), 46.2, 1e-9, "例題3(b) 3 桁で 46.2")
chk(_mu3 > 40, "例題3(c) mu > 40")
close(PHI((40 - _mu3) / 6), 0.15, 1e-9, "例題3 もどすと 0.15")
# 丸めてから代入すると 3 桁目がずれること（本文の検算）
close(40 - 6 * (-1.04), 46.24, 1e-9, "例題3 z を丸めると 46.24")
chk(round(40 - 6 * (-1.04), 2) != round(_mu3, 2), "丸めると値がずれる")
in_text("z = -1.0364\\ldots", "例題3 の z")
in_text("\\mu = 40 + 6.2186\\ldots = 46.2186\\ldots", "例題3 の mu")

# ══════════════════════════════════════════════════════════
# 8. 例題4  P(X < 30) = 0.1, P(X > 50) = 0.2
# ══════════════════════════════════════════════════════════
_z1 = Z("0.1")
_z2 = Z("0.8")
close(_z1, -1.2815516, 1e-6, "例題4 z1")
close(_z2, 0.8416212, 1e-6, "例題4 z2")
chk(_z1 < 0 < _z2, "例題4 符号")
_sig4 = (50 - 30) / (_z2 - _z1)
_mu4 = 30 - _z1 * _sig4
close(_z2 - _z1, 2.1231728, 1e-6, "例題4 z2 - z1")
close(_sig4, 9.4198638, 1e-5, "例題4 sigma")
close(_mu4, 42.0720417, 1e-5, "例題4 mu")
close(float("%.3g" % _sig4), 9.42, 1e-9, "例題4 sigma 3 桁")
close(float("%.3g" % _mu4), 42.1, 1e-9, "例題4 mu 3 桁")
chk(_sig4 > 0, "例題4 sigma > 0")
chk(30 < _mu4 < 50, "例題4 mu は 30 と 50 の間")
chk(_mu4 - 30 > 50 - _mu4, "例題4 左の面積が小さいので 30 のほうが遠い")
close(PHI((30 - _mu4) / _sig4), 0.1, 1e-9, "例題4 もどすと 0.1")
close(1 - PHI((50 - _mu4) / _sig4), 0.2, 1e-9, "例題4 もどすと 0.2")
in_text("z_{1} = -1.2815\\ldots", "例題4 の z1")
in_text("z_{2} = 0.8416\\ldots", "例題4 の z2")
in_text("\\frac{20}{2.1231\\ldots} = 9.4198\\ldots", "例題4 の sigma")

# ══════════════════════════════════════════════════════════
# 9. 演習の答え
# ══════════════════════════════════════════════════════════
# 演習1
eq(R(49 - 40, 5), R("1.8"), "演習1 z")
eq(40 + R("1.8") * 5, 49, "演習1 もどす")
chk(R("1.8") < 2, "演習1 2 個ぶんには足りない")

# 演習2
eq(120 + R("-2.25") * 16, 84, "演習2 x")
eq(R(84 - 120, 16), R("-2.25"), "演習2 もどす")
eq(120 - 84, 36, "演習2 差は 36")
eq(R("2.25") * 16, 36, "演習2 2.25 sigma")

# 演習3
_ze1 = R(46 - 52, 4)
_ze2 = R(60 - 75, 12)
eq(_ze1, R("-1.5"), "演習3 レース1 の z")
eq(_ze2, R("-1.25"), "演習3 レース2 の z")
chk(_ze1 < _ze2, "演習3 レース1 のほうがよい（小さいほどよい量）")
chk(_ze1 < 0 and _ze2 < 0, "演習3 どちらも平均より速い")
chk(75 - 60 > 52 - 46, "演習3 秒数の差では逆に見える")

# 演習4  X ~ N(mu, 4^2), P(X > 25) = 0.10
_z4 = Z("0.9")
close(_z4, 1.2815516, 1e-6, "演習4 z")
_mu = 25 - 4 * _z4
close(_mu, 19.8737937, 1e-5, "演習4 mu")
close(float("%.3g" % _mu), 19.9, 1e-9, "演習4 mu 3 桁")
chk(_mu < 25, "演習4 mu < 25")
close(1 - PHI((25 - _mu) / 4), 0.10, 1e-9, "演習4 もどすと 0.10")

# 演習5  X ~ N(60, sigma^2), P(X < 52) = 0.025
_z5 = Z("0.025")
close(_z5, -1.9599640, 1e-6, "演習5 z")
_s5 = (52 - 60) / _z5
close(_s5, 4.0817077, 1e-5, "演習5 sigma")
close(float("%.3g" % _s5), 4.08, 1e-9, "演習5 sigma 3 桁")
chk(_s5 > 0, "演習5 sigma > 0")
close(PHI((52 - 60) / _s5), 0.025, 1e-9, "演習5 もどすと 0.025")
close(60 - 2 * 4.08, 51.84, 1e-9, "演習5 mu - 2 sigma は 51.84")

# 演習6  P(X < 12) = 0.05, P(X < 26) = 0.7
_z61 = Z("0.05")
_z62 = Z("0.7")
close(_z61, -1.6448536, 1e-6, "演習6 z1")
close(_z62, 0.5244005, 1e-6, "演習6 z2")
_s6 = (26 - 12) / (_z62 - _z61)
_m6 = 12 - _z61 * _s6
close(_z62 - _z61, 2.1692541, 1e-6, "演習6 z2 - z1")
close(_s6, 6.4538312, 1e-5, "演習6 sigma")
close(_m6, 22.6156076, 1e-5, "演習6 mu")
close(float("%.3g" % _s6), 6.45, 1e-9, "演習6 sigma 3 桁")
close(float("%.3g" % _m6), 22.6, 1e-9, "演習6 mu 3 桁")
chk(12 < _m6 < 26, "演習6 mu は 12 と 26 の間")
close(PHI((12 - _m6) / _s6), 0.05, 1e-9, "演習6 もどすと 0.05")
close(PHI((26 - _m6) / _s6), 0.7, 1e-9, "演習6 もどすと 0.7")

# 演習7  z = 0
eq(sp.Integer(0), 0, "演習7 z = 0 は x = mu")
close(PHI(0.0), 0.5, 1e-12, "演習7 P(X < mu) = 0.5")

# 演習8  P(Z > 3)
close(1 - PHI(3.0), 0.00134990, 1e-7, "演習8 P(Z > 3)")
chk(1 - PHI(3.0) > 0, "演習8 0 ではない")
close(PHI(3.0) - PHI(-3.0), 0.9973002, 1e-6, "演習8 3 sigma の中は約 99.7%")

# 演習9  X ~ N(mu, 12^2), P(X > 100) = 0.75
_z9 = Z("0.25")
close(_z9, -0.6744898, 1e-6, "演習9 z")
_m9 = 100 - 12 * _z9
close(_m9, 108.0938770, 1e-5, "演習9 mu")
close(float("%.3g" % _m9), 108.0, 1e-9, "演習9 mu 3 桁")
chk(_m9 > 100, "演習9 mu > 100")
close(1 - PHI((100 - _m9) / 12), 0.75, 1e-9, "演習9 もどすと 0.75")
close((_m9 - 100) / 12, 0.6744898, 1e-6, "演習9 sigma 1 個ぶんより小さい")

# 演習10  10% が 480 未満、5% が 520 より上
_za = Z("0.1")
_zb = Z("0.95")
close(_za, -1.2815516, 1e-6, "演習10 z1")
close(_zb, 1.6448536, 1e-6, "演習10 z2")
_s10 = (520 - 480) / (_zb - _za)
_m10 = 480 - _za * _s10
close(_zb - _za, 2.9264052, 1e-6, "演習10 z2 - z1")
close(_s10, 13.6686472, 1e-5, "演習10 sigma")
close(_m10, 497.5170762, 1e-5, "演習10 mu")
close(float("%.3g" % _s10), 13.7, 1e-9, "演習10 sigma 3 桁")
close(float("%.3g" % _m10), 498.0, 1e-9, "演習10 mu 3 桁")
chk(480 < _m10 < 520, "演習10 mu は 480 と 520 の間")
chk(520 - _m10 > _m10 - 480, "演習10 右の面積が小さいので 520 のほうが遠い")
close(PHI((480 - _m10) / _s10), 0.10, 1e-9, "演習10 もどすと 0.10")
close(1 - PHI((520 - _m10) / _s10), 0.05, 1e-9, "演習10 もどすと 0.05")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("46.2", "9.42", "42.1", "13.7", "6.45", "22.6", "19.9", "4.08",
           "108", "497", "1.8", "-1.25", "0.00135", "1.5", "1.4", "1.1",
           "1.036", "1.2815", "0.8416", "1.9599", "0.5244", "1.6448",
           "0.6744", "84"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 10. ページに書いてある計算を、機械的に全部たしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(
    r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|[\d.(]|\\(?!ldots|approx)))"
    % (_EXPR, _EXPR))


def _tonum(t):
    t = t.strip()
    m = re.fullmatch(r"\\[dt]?frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2)))
    return sp.Rational(t)


def _value(expr):
    """+ - かけ算だけの式を、かけ算を先に計算して評価する。"""
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
chk(_nstmt >= 12, "ページの計算を %d 本たしかめた" % _nstmt)
print("  （計算 %d 本）" % _nstmt)

# ══════════════════════════════════════════════════════════
# 見直し（2026-09）で直したところ。もどってしまわないように。
# ══════════════════════════════════════════════════════════

# --- B1: 許されていないシラバスの引用を貼らない -----------------
chk("Probabilities and values of the variable must be found using technology"
    not in TEXT, "許可されていないシラバスの引用がない")
chk("シラバスは、正規分布の確率と値を**GDC で求める**としています。"
    in TEXT, "引用ではなく言いかえになっている")

# --- M4: z は手でも出せる、と正しく書いてある -------------------
chk("$z$ の値も GDC で出します" not in TEXT, "「z も GDC で」は消えている")
chk("$z$ の値も答えも GDC で出します" not in TEXT, "同上（例題の前書き）")
chk("**GDC を使うのは、面積から $z$ を出すところです。**" in TEXT,
    "GDC を使うのは面積から z を出すところだと書いている")
chk("**GDC を使うのは、面積から $z$ を出すところです（Paper 2）。**" in TEXT,
    "例題の前書きも同じ")
chk("**単元全体が Paper 1 の対象外というわけではありません。**" in TEXT,
    "C10 4.12 単元全体ではない")
chk("## この項目は Paper 2 です" not in TEXT, "C10 4.12 断定が消えている")
chk("**GDC を使うのは $4$・$5$・$6$・$9$・$10$（面積から $z$ を"
    "出す問題）です。**" in TEXT, "C10 4.12 演習の区分")

# --- M5: 3 桁の言いかたが IB の規則に合っている -----------------
chk("**最後の答えは、割り切れるときはその値を、割り切れないときは"
    "有効数字 $3$ 桁で書きます。**" in TEXT, "第7節の丸めの規則")
chk("割り切れるときはその値を、割り切れないときは**有効数字 $3$ 桁**"
    in TEXT, "例題の前書きの丸めの規則")

# --- m3: 標準正規分布と Z を使う前に定義している -----------------
chk("これを **standard normal distribution**（標準正規分布）といい、"
    "その変数をふつう $Z$ と書きます。" in TEXT, "第5節で Z を定義している")
chk(TEXT.index("standard normal distribution") < TEXT.index("Z \\sim N(0,\\ 1^{2})"),
    "Z の定義は使う前にある")

# --- M1: Why it works の循環した説明を直した --------------------
chk("**この右辺は、$\\mu$ と $\\sigma$ を含みません。**" not in TEXT,
    "誤った（右辺に mu, sigma がないという）文が消えている")
chk("**書きかえで変わったのは、変数と境目だけです。**" in TEXT,
    "書きかえで変わったものを述べている")
chk("正規分布を平行移動して拡大・縮小したものはやはり正規分布なので、" in TEXT,
    "Z が N(0,1) に従う理由を述べている")
chk("**$\\mu$ と $\\sigma$ が残るのは、境目のほうだけです。**" in TEXT,
    "mu, sigma が残るのは境目だけ")

# --- M2: 6.2186（6.2185 は丸めてから掛けた値）------------------
chk("6.2186" in TEXT and "46.2186" in TEXT, "例題3 の途中の値は 6.2186")
chk("6.2185" not in TEXT and "46.2185" not in TEXT, "6.2185 は残っていない")

# --- B2: 「3 桁目がずれる」を正しく言いなおした -----------------
chk("$\\mu = 46.24$ で、$4$ 桁目からずれます" in TEXT,
    "例題3 の検算: 4 桁目からずれる、と正しく書いている")
chk("$\\sigma = 30$ なら、正しくは $71.1$、丸めてから入れると $71.2$ です。"
    in TEXT, "3 桁目までずれる例を挙げている")
chk("答えの $3$ 桁目がずれることがあります（[第 7 節](#writing)）" in TEXT,
    "Common errors も「ことがあります」")
chk("答えの $3$ 桁目がずれます（[第 7 節](#writing)）" not in TEXT,
    "断定した古い文が消えている")

# --- M3: GDC の検算に「どちら側の面積か」が入っている ------------
chk("**$a$ から見て $\\mu$ と反対側**の面積は $0.16$ ほど" in TEXT,
    "GDC の検算: どちら側の面積かを書いている")
chk("$|a - \\mu|$ が $\\sigma$ の $1$ 個ぶんくらいなら面積は $0.16$ ほど"
    not in TEXT, "側を書いていない古い文が消えている")

# --- B4: 目標がページの中身と合っている -------------------------
chk("- $z$ を使って、**平均や散らばりのちがう $2$ つの量**を比べられる。"
    in TEXT, "目標: 平均や散らばりのちがう量を比べる")

# --- B4/m1/m2: 演習3 は単位のちがう 2 つの量の比較 ---------------
chk("Identify which of the two results is further from its mean" in TEXT,
    "演習3: 平均からの離れかたを比べる問題")
chk("z_{\\text{swim}}" in TEXT and "z_{\\text{test}}" in TEXT,
    "演習3: 泳ぎと体力テストの z")
chk("**検算（単位を落としていないか）。**" in TEXT,
    "演習3: 単位の検算が入っている")
chk("Identify the race in which the runner performed better" not in TEXT,
    "演習3: 古い（同じ単位どうしの）問題が消えている")
chk("$6$ は $4$ の $1.5$ 個ぶん" not in TEXT, "演習3: 循環した検算が消えている")

# --- B3: 演習7 は答えが本文にない問題 ---------------------------
chk("the value $x = 44$ has standardized value $0$" in TEXT,
    "演習7: mu と sigma を求める問題になっている")
chk("Describe how your value of $\\sigma$ would change" in TEXT,
    "演習7: Describe の指示がある")
chk("Describe what this tells you about $x$" not in TEXT,
    "演習7: 古い（本文に答えがある）問題が消えている")

# --- m2: 演習9 の 2 つ目は例題3(c) と重ならない -----------------
chk("Explain what would happen to $P(X < 100)$ if $\\sigma$ were larger"
    in TEXT, "演習9: sigma を大きくしたときの問い")
chk("Explain why $\\mu$ must be greater than $100$." not in TEXT,
    "演習9: 例題3(c) と同じ問いが消えている")
chk("**検算（$\\sigma$ を大きくしてみる）。**" in TEXT,
    "演習9: sigma を変えた検算がある")

# --- m4: sigma の解釈をゆるめた ---------------------------------
chk("a typical packet differs from the mean mass" not in TEXT,
    "演習10: 「典型的なずれ」という言いかたが消えている")
chk("about $68\\%$ of packets have a mass between $484$ g and $511$ g"
    in TEXT, "演習10: 68% の区間で sigma を説明している")

# --- 例題3(c) と演習9 が別の問いであること ----------------------
chk(TEXT.count("must lie below the mean") <= 1,
    "同じ答えかたが 2 か所に出ていない")

print()
print("OK", OK, "/ NG", NG)
