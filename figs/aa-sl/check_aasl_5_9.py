# -*- coding: utf-8 -*-
"""AA SL 5.9 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_9.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-9.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_9.py")

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
T = sp.Symbol("t", nonnegative=True)


def d1(f):
    return sp.expand(sp.diff(f, T))


def d2(f):
    return sp.expand(sp.diff(f, T, 2))


def same(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


def zeros(f):
    return sorted(sp.solve(sp.Eq(f, 0), T))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.9 — Kinematics（運動学） {#sec-aasl-5-9}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["three", "differentiate", "speed", "atrest",
                             "integrate", "distance", "units"],
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
    "callout-important 2（公式集 5.9 の 2 つ）")
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
chk(len(_qs) == 5, "Explain 系の問いは 5: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-9-idea.svg){#fig-aasl59-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl59-idea (a)", "図 (a) の参照")
in_text("@fig-aasl59-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == ["Speed is the magnitude of velocity."],
    "シラバスの引用は 1 本だけ: %s" % _quotes)
in_text("公式集の **5.9** の欄に、*Acceleration* として @eq-aasl59-a が"
        "印刷されています。", "公式集 5.9 加速度")
in_text("**@eq-aasl59-v は印刷されていません。**", "v = ds/dt は公式集にない")
in_text("*Displacement from $t_1$ to $t_2$* として @eq-aasl59-disp", "公式集 変位")
in_text("*Distance travelled from $t_1$ to $t_2$* として @eq-aasl59-dist",
        "公式集 道のり")
in_text("**絶対値の記号が付くのは distance のほうだけです。**", "絶対値は distance")

in_text("a = \\frac{dv}{dt} = \\frac{d^{2}s}{dt^{2}}\n$$ {#eq-aasl59-a}",
        "加速度の式")
in_text("\\text{displacement} = \\int_{t_{1}}^{t_{2}} v(t)\\,dt\n"
        "$$ {#eq-aasl59-disp}", "変位の式")
in_text("\\text{distance} = \\int_{t_{1}}^{t_{2}} |v(t)|\\,dt\n"
        "$$ {#eq-aasl59-dist}", "道のりの式")
for _r in ("{#eq-aasl59-v}", "{#eq-aasl59-speed}", "{#tbl-aasl59-three}",
           "{#tbl-aasl59-two}", "{#tbl-aasl59-units}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-1.qmd#limit", "aasl-5-2.qmd#zero", "aasl-5-5.qmd#anti",
           "aasl-5-5.qmd#boundary", "aasl-5-7.qmd#again",
           "aasl-5-7.qmd#notation", "aasl-5-7.qmd#meaning",
           "aasl-5-11a.qmd", "aasl-5-11b.qmd"):
    in_text(_a, "参照 " + _a)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) Reading a velocity-time graph"', "図 (a) の題")
in_fig('"(b) How $s$, $v$ and $a$ are linked"', "図 (b) の題")
in_fig("displacement $= A_{1} - A_{2} + A_{3}$", "図 (a) の変位")
in_fig("distance $= A_{1} + A_{2} + A_{3}$", "図 (a) の道のり")
in_fig("speed $= |v|$, so speed is never negative", "図 (b) の speed")
in_fig("at rest when $v = 0$, not when $a = 0$", "図 (b) の静止")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("8.17", "13", "1024", "t^{2}"):
    chk(_v not in _figmath, "図の数式に具体的な数・式 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_s1 = T ** 3 - 6 * T ** 2 + 9 * T
chk(same(d1(_s1), 3 * T ** 2 - 12 * T + 9), "例題1 の v")
chk(same(d2(_s1), 6 * T - 12), "例題1 の a")
chk(same(3 * (T - 1) * (T - 3), 3 * T ** 2 - 12 * T + 9), "例題1 の因数分解")
chk(zeros(d1(_s1)) == [1, 3], "例題1 v=0 の時刻: %s" % zeros(d1(_s1)))
eq(d1(_s1).subs(T, 0), 9, "例題1 v(0)")
eq(d1(_s1).subs(T, 2), -3, "例題1 v(2)")
eq(d1(_s1).subs(T, 4), 9, "例題1 v(4)")
chk(zeros(d2(_s1)) == [2], "例題1 a=0 は t=2")
chk(d1(_s1).subs(T, 2) != 0, "例題1 a=0 でも静止していない")

# 例題2
_v2 = T ** 2 - 6 * T + 8
chk(zeros(_v2) == [2, 4], "例題2 v=0 の時刻")
chk(same((T - 2) * (T - 4), _v2), "例題2 の因数分解")
chk(same(d1(_v2), 2 * T - 6), "例題2 の a")
eq(d1(_v2).subs(T, 1), -4, "例題2 a(1)")
eq(_v2.subs(T, 3), -1, "例題2 v(3)")
eq(abs(_v2.subs(T, 3)), 1, "例題2 t=3 の speed")
eq(_v2.subs(T, 0), 8, "例題2 v(0)")
chk(zeros(d1(_v2)) == [3], "例題2 a=0 は t=3")

# 例題3
_v3 = T ** 2 - 5 * T + 4
chk(same((T - 1) * (T - 4), _v3), "例題3 の因数分解")
chk(zeros(_v3) == [1, 4], "例題3 v=0 の時刻")
_disp3 = sp.integrate(_v3, (T, 0, 5))
_dist3 = sp.integrate(sp.Abs(_v3), (T, 0, 5))
eq(_disp3, R(-5, 6), "例題3 の変位（正確な値）")
eq(_dist3, R(49, 6), "例題3 の道のり（正確な値）")
chk(float("%.3g" % float(_dist3)) == 8.17, "例題3 の道のり 3 桁は 8.17")
chk(abs(float(_disp3) + 0.833) < 0.001, "例題3 の変位 ≈ -0.833")
chk(abs(float(_disp3)) < float(_dist3), "例題3 変位の大きさ < 道のり")
in_text("8.17 \\text{ m} \\ (3 \\text{ s.f.})", "例題3 の答え")

# 例題4
_a4 = 6 * T - 4
_v4 = 3 * T ** 2 - 4 * T + 5
_s4 = T ** 3 - 2 * T ** 2 + 5 * T + 2
chk(same(sp.integrate(_a4, T) + 5, _v4), "例題4 の v")
chk(same(sp.integrate(_v4, T) + 2, _s4), "例題4 の s")
chk(same(d1(_s4), _v4), "例題4 微分でもどる（s→v）")
chk(same(d1(_v4), _a4), "例題4 微分でもどる（v→a）")
eq(_v4.subs(T, 0), 5, "例題4 v(0)")
eq(_s4.subs(T, 0), 2, "例題4 s(0)")
eq(16 - 60, -44, "例題4 判別式")
chk(sp.solve(sp.Eq(_v4, 0), sp.Symbol("u", real=True)) == [] or
    not [r for r in sp.solve(sp.Eq(_v4, 0), T) if r.is_real],
    "例題4 v = 0 に実数解はない")

# ══════════════════════════════════════════════════════════
# 5. 演習
# ══════════════════════════════════════════════════════════
_E1 = T ** 3 - 3 * T ** 2
chk(same(d1(_E1), 3 * T ** 2 - 6 * T), "演習1 の v")
chk(same(d2(_E1), 6 * T - 6), "演習1 の a")
eq(d1(_E1).subs(T, 0), 0, "演習1 v(0)")
eq(d2(_E1).subs(T, 0), -6, "演習1 a(0)")

_E2 = 2 * T ** 3 - 15 * T ** 2 + 24 * T
chk(same(d1(_E2), 6 * T ** 2 - 30 * T + 24), "演習2 の v")
chk(same(6 * (T - 1) * (T - 4), 6 * T ** 2 - 30 * T + 24), "演習2 の因数分解")
chk(zeros(d1(_E2)) == [1, 4], "演習2 v=0 の時刻")
eq(d1(_E2).subs(T, 2), -12, "演習2 v(2)")
chk(same(d2(_E2), 12 * T - 30), "演習2 の a")
chk(zeros(d2(_E2)) == [R(5, 2)], "演習2 a=0 は t=2.5")

_E3 = 12 - 3 * T
chk(same(d1(_E3), -3), "演習3 の a")
chk(zeros(_E3) == [4], "演習3 v=0 は t=4")
eq(_E3.subs(T, 0), 12, "演習3 v(0)")
eq(_E3.subs(T, 5), -3, "演習3 v(5)")

_E4 = (T - 3) ** 2
chk(zeros(_E4) == [3], "演習4 v=0 は t=3 だけ")
eq(_E4.subs(T, 2), 1, "演習4 v(2)")
eq(_E4.subs(T, 4), 1, "演習4 v(4)")
chk(_E4.subs(T, 2) > 0 and _E4.subs(T, 4) > 0, "演習4 前後とも正（向きは変わらない）")
chk(all(sp.expand(_E4).subs(T, _u) >= 0 for _u in (0, 1, 3, 5)),
    "演習4 v は 0 以上")

_E5v = 3 * T ** 2 - 12
chk(same(sp.integrate(6 * T, T) - 12, _E5v), "演習5 の v")
chk(same(d1(_E5v), 6 * T), "演習5 微分でもどる")
chk(zeros(_E5v) == [2], "演習5 v=0 は t=2（t >= 0）")
eq(_E5v.subs(T, 0), -12, "演習5 v(0)")
eq(_E5v.subs(T, 3), 15, "演習5 v(3)")

_E6s = T ** 3 - 12 * T + 5
chk(same(sp.integrate(_E5v, T) + 5, _E6s), "演習6 の s")
eq(_E6s.subs(T, 0), 5, "演習6 s(0)")
eq(_E6s.subs(T, 3), -4, "演習6 s(3)")
eq(_E6s.subs(T, 3) - _E6s.subs(T, 0), -9, "演習6 の変位")

_E7 = T ** 2 - 4 * T
_dist7 = sp.integrate(sp.Abs(_E7), (T, 0, 3))
_disp7 = sp.integrate(_E7, (T, 0, 3))
eq(_dist7, 9, "演習7 の道のり（0 から 3）")
eq(_disp7, -9, "演習7 の変位（0 から 3）")
eq(abs(_disp7), _dist7, "演習7 変位の大きさ = 道のり")
chk(all(_E7.subs(T, _u) < 0 for _u in (R(1, 2), 1, 2, R(29, 10))),
    "演習7 0<t<3 で v < 0")
eq(_E7.subs(T, 1), -3, "演習7 v(1)")
eq(_E7.subs(T, 2), -4, "演習7 v(2)")
eq(sp.integrate(sp.Abs(_E7), (T, 0, 5)), 13, "演習7 0 から 5 なら 13")
eq(sp.integrate(_E7, (T, 0, 5)), R(-25, 3), "演習7 0 から 5 の変位")
chk(zeros(_E7) == [0, 4], "演習7 v=0 の時刻")

_E9v = T ** 2 - 10 * T + 30
chk(same(d1(_E9v), 2 * T - 10), "演習9 の a")
eq(_E9v.subs(T, 5), 5, "演習9 v(5)")
eq(100 - 120, -20, "演習9 判別式")
chk(not [r for r in sp.solve(sp.Eq(_E9v, 0), T) if r.is_real],
    "演習9 v = 0 に実数解はない")

_E10 = sp.expand((T - 2) * (T - 5))
chk(zeros(_E10) == [2, 5], "演習10 v=0 の時刻")
eq(_E10.subs(T, 0), 10, "演習10 v(0)")
eq(_E10.subs(T, 3), -2, "演習10 v(3)")
eq(_E10.subs(T, 6), 4, "演習10 v(6)")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("3t^{2} - 12t + 9", "6t - 12", "8.17", "3t^{2} - 4t + 5",
           "t^{3} - 2t^{2} + 5t + 2", "3t^{2} - 6t", "13 \\text{ m}",
           "3t^{2} - 12", "t^{3} - 12t + 5"):
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

# --- B1: a = 0 の意味 -----------------------------------------------
chk("**$a = 0$ は、その瞬間に速度が変わっていないという意味です。**" in TEXT,
    "第4節: a = 0 の意味")
chk("一定の速度で動きつづけている物体も $a = 0$ です。" in TEXT, "第4節: 反例")
chk("速度がその瞬間いちばん大きい（小さい）ことを表すだけです" not in TEXT,
    "無条件に偽の主張が消えている")
# v = t^3 - 3t^2 + 3t + 1 は a(1) = 0 だが極値ではない
_vx = T ** 3 - 3 * T ** 2 + 3 * T + 1
chk(sp.simplify(sp.diff(_vx, T) - 3 * (T - 1) ** 2) == 0, "反例の a")
chk(sp.diff(_vx, T).subs(T, 1) == 0, "反例で a(1) = 0")
chk(_vx.subs(T, 0) < _vx.subs(T, 1) < _vx.subs(T, 2), "反例で v は増えつづける")

# --- B2: 演習9 の検算 -------------------------------------------------
chk("$a(5) = 0$ が言うのは、$t = 5$ の瞬間に速度が変わっていない、ということ"
    "だけです ✓ 位置が変わっていない、ではありません。" in TEXT,
    "演習9: a=0 の意味")
chk("$t = 5$ で速度がいちばん小さいということだけです" not in TEXT,
    "偽の主張が消えている")

# --- B3: 演習8 の speed の検算 -----------------------------------------
chk("**検算（速さ）。** 前に進んでいるあいだも、もどっているあいだも speed は"
    "正です ✓ 符号がちがっても、大きさは足されます。" in TEXT,
    "演習8: speed の検算")
chk("speed が $0$ になるのは、向きが変わる瞬間だけです。" not in TEXT,
    "偽の主張が消えている")

# --- M1: Paper についての言い切り ---------------------------------------
chk("**$\\displaystyle\\int |v(t)|\\,dt$ の値は、このページでは電卓で出します**"
    in TEXT, "Paper の書き方")
chk("Paper 2 で電卓を使って出します。" not in TEXT, "言い切りが消えている")

# --- M2: 目標に「値を求める」がある ---------------------------------------
chk("- **まず式を書いてから**、その値を電卓で求められる。" in TEXT,
    "目標: 値を求める")

# --- M3: s の差と定積分をつないでいる -------------------------------------
chk("\\int_{t_{1}}^{t_{2}} v(t)\\,dt = s(t_{2}) - s(t_{1})" + chr(10)
    + "$$ {#eq-aasl59-diff}" in TEXT, "第6節: s の差")
chk("**位置の関数 $s$ がわかっているときは、引き算で出せます。**" in TEXT,
    "第6節: 引き算で出す")
chk("[SL 5.11a](aasl-5-11a.qmd) で扱います。" in TEXT, "5.11a へ送る")

# --- M4: 演習4 が「v=0 でも向きが変わらない」形 ----------------------------
chk("A particle moves along a straight line with velocity $v = (t - 3)^{2}$"
    in TEXT, "演習4: (t-3)^2")
chk("*the particle does not change direction*" in TEXT, "演習4 の答え")
chk("Find the speed of the particle when $t = 4$." not in TEXT,
    "例題2(c) と同型だった演習4 が消えている")

# --- M5: 演習7 が符号を変えない区間になった -------------------------------
chk("Explain why this value is equal to the magnitude of the displacement "
    "over the same interval." in TEXT, "演習7: 大きさが等しい理由")
chk("\\int_{0}^{3} |t^{2} - 4t|\\,dt = 9 \\text{ m}" in TEXT, "演習7 の答え")

# --- M6: 演習5 が 3 部、演習6 が単位の問題 ----------------------------------
chk("**(c)** [Find the displacement of the particle from $t = 0$ to $t = 3$.]"
    in TEXT, "演習5(c)")
chk("For the particle in question 5" not in TEXT, "別問への参照が消えている")
chk("Write down the units of the velocity and of the acceleration" in TEXT,
    "演習6: 単位の問題")
chk("*velocity: m s$^{-1}$, because $v = \\dfrac{ds}{dt}$ divides metres by "
    "seconds*" in TEXT, "演習6 の答え")

# --- M7: 演習1 に a = 0 の時刻が入った ---------------------------------------
chk("and find the time at which the acceleration is zero." in TEXT,
    "演習1: a = 0 の時刻")
chk("**検算（$a = 0$ は静止ではない）。**" in TEXT, "演習1: a=0 は静止でない検算")
chk(sp.solve(sp.Eq(6 * T - 6, 0), T) == [1], "演習1 a=0 は t=1")
eq((3 * T ** 2 - 6 * T).subs(T, 1), -3, "演習1 v(1)")

# --- M8: v = 0 でも向きが変わらない場合の書き方 --------------------------------
chk("**だから、$v = 0$ を解いただけでは足りません。**" in TEXT,
    "第4節: 符号を調べる")

# --- M9: 例題4 の検算 -----------------------------------------------------
chk("**検算（$D$ を落としていないか）。**" in TEXT, "例題4: D の検算")
chk("**検算（定数が $2$ つ要る）。**" not in TEXT, "言いかえだった検算が消えている")

# --- m1: 循環していた検算（例題3） ------------------------------------------
chk("**検算（区切って考えて）。**" in TEXT, "例題3: 区切る検算")
chk("**検算（符号）。** distance は正です ✓" not in TEXT, "言いかえが消えている")

# --- m2 + m3: 図 ------------------------------------------------------------
chk("$A_{1}$, $A_{2}$, $A_{3}$ are areas, so each one is positive" in FIG,
    "図: A は面積")
chk("A note says that these are areas, so each one is positive." in TEXT,
    "図の alt: A は面積")
chk("T1, T2, TEND = 1.0, 2.6, 4.2" in FIG, "図の交点が例題1 と重ならない")

# --- m4 + m5 + m6: 表記 -------------------------------------------------------
chk("**$t$ で積分すると、逆に $t$ の単位がかかります。**" in TEXT, "第7節: t で積分")
chk("**total distance travelled（動いた道のり）は" in TEXT, "第6節: 訳")
chk("correct to $3$ significant figures." in TEXT, "有効数字の書き方")

# --- m8: 演習2 の検算に値がある -------------------------------------------------
chk("$v(2.5) = 37.5 - 75 + 24 = -13.5 \\ne 0$ です ✓" in TEXT, "演習2 の検算")
eq((6 * T ** 2 - 30 * T + 24).subs(T, R(5, 2)), R(-27, 2), "演習2 v(2.5)")

# --- m9: 演習9 の英語 -----------------------------------------------------------
chk("A student writes that the acceleration is $a = 2t - 10$, and concludes "
    "that the particle is at rest when $t = 5$." in TEXT, "演習9 の英語")

print()
print("OK", OK, "/ NG", NG)
