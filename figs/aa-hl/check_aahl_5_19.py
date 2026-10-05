"""AA HL HL 5.19 — Maclaurin series の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_19.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-19.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_19.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
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


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + "  (%s vs %s)" % (u, v))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])



_x = sp.Symbol("x", real=True)
_u = sp.Symbol("u", real=True)
_p = sp.Symbol("p")
R = sp.Rational


def mac(expr, n):
    """expr の Maclaurin 級数を x^n の項まで（多項式で返す）。"""
    return sp.expand(sp.series(expr, _x, 0, n + 1).removeO())


def coef(expr, n):
    """x^n の係数。"""
    return sp.expand(expr).coeff(_x, n)


def de_series(rhs, y0, n):
    """dy/dx = rhs(x, y)、y(0) = y0 から x^n までの Maclaurin 級数を作る。

    rhs は (x, y) を受け取る関数。くり返し微分して x = 0 の値を並べる。
    """
    _yf = sp.Function("yf")
    _expr = rhs(_x, _yf(_x))          # y' の式
    _vals = [sp.Integer(y0)]          # y(0), y'(0), ...
    for _k in range(n):
        _sub = _expr
        for _j in range(len(_vals) - 1, -1, -1):
            _sub = _sub.subs(sp.Derivative(_yf(_x), (_x, _j)) if _j else _yf(_x),
                             _vals[_j])
        _vals.append(sp.simplify(_sub.subs(_x, 0)))
        _expr = sp.diff(_expr, _x)
    return sp.expand(sum(_vals[_k] * _x ** _k / sp.factorial(_k)
                         for _k in range(n + 1)))


# ══════════════════════════════════════════════════════════
# 0. 公式集の 5 つの級数（@tbl-aahl519-standard）
# ══════════════════════════════════════════════════════════
eq(mac(sp.exp(_x), 3), 1 + _x + _x ** 2 / 2 + _x ** 3 / 6, "e^x の級数")
eq(mac(sp.log(1 + _x), 3), _x - _x ** 2 / 2 + _x ** 3 / 3, "ln(1+x) の級数")
eq(mac(sp.sin(_x), 5), _x - _x ** 3 / 6 + _x ** 5 / 120, "sin x の級数")
eq(mac(sp.cos(_x), 4), 1 - _x ** 2 / 2 + _x ** 4 / 24, "cos x の級数")
eq(mac(sp.atan(_x), 5), _x - _x ** 3 / 3 + _x ** 5 / 5, "arctan x の級数")
# 分母は sin/cos が階乗、ln/arctan はただの整数
chk(coef(mac(sp.sin(_x), 5), 3) == -R(1, sp.factorial(3)), "sin は 3! で割る")
chk(coef(mac(sp.atan(_x), 5), 3) == -R(1, 3), "arctan は 3 で割る")
chk(coef(mac(sp.cos(_x), 4), 4) == R(1, sp.factorial(4)), "cos は 4! で割る")
chk(coef(mac(sp.log(1 + _x), 3), 3) == R(1, 3), "ln(1+x) は 3 で割る")
# 奇数次・偶数次
chk(all(coef(mac(sp.sin(_x), 6), _k) == 0 for _k in (0, 2, 4, 6)),
    "sin は奇数次だけ")
chk(all(coef(mac(sp.atan(_x), 6), _k) == 0 for _k in (0, 2, 4, 6)),
    "arctan は奇数次だけ")
chk(all(coef(mac(sp.cos(_x), 5), _k) == 0 for _k in (1, 3, 5)),
    "cos は偶数次だけ")

# 係数は f^{(n)}(0)/n!（@eq-aahl519-maclaurin）
for _f in (sp.exp(_x), sp.sin(_x), sp.cos(_x), sp.log(1 + _x), sp.atan(_x)):
    for _n in range(4):
        chk(coef(mac(_f, 4), _n)
            == sp.diff(_f, _x, _n).subs(_x, 0) / sp.factorial(_n),
            "係数 = f^{(n)}(0)/n!: %s, n=%d" % (_f, _n))

# ══════════════════════════════════════════════════════════
# 1. 二項級数（@eq-aahl519-binomial）
# ══════════════════════════════════════════════════════════
_bin = (1 + _p * _x + _p * (_p - 1) / sp.factorial(2) * _x ** 2
        + _p * (_p - 1) * (_p - 2) / sp.factorial(3) * _x ** 3)
for _pv in (R(1, 2), R(-1, 1), R(3, 1), R(-1, 2), R(2, 3)):
    eq(_bin.subs(_p, _pv), mac((1 + _x) ** _pv, 3),
       "二項級数 p = %s" % _pv)
# p が正の整数なら止まる
chk(sp.expand((1 + _x) ** 3) == sp.expand(_bin.subs(_p, 3)),
    "p = 3 では 3 次で止まる")

# ══════════════════════════════════════════════════════════
# 2. 置きかえ・かけ算・微分積分（The idea の例）
# ══════════════════════════════════════════════════════════
eq(mac(sp.exp(_x ** 2), 4), 1 + _x ** 2 + _x ** 4 / 2, "e^{x²} の級数")
eq(mac(sp.exp(_x) * sp.sin(_x), 3), _x + _x ** 2 + _x ** 3 / 3,
   "e^x sin x の級数")
eq(mac(1 / (1 + _x ** 2), 4), 1 - _x ** 2 + _x ** 4, "1/(1+x²) の級数")
eq(sp.integrate(1 - _x ** 2 + _x ** 4, _x), mac(sp.atan(_x), 5),
   "項ごとに積分すると arctan")
chk(sp.atan(0) == 0, "arctan 0 = 0 なので C = 0")
# 階乗の出どころ: x^n を n 回微分すると n!
for _n in range(1, 5):
    chk(sp.diff(_x ** _n, _x, _n) == sp.factorial(_n),
        "x^%d を %d 回微分すると %d!" % (_n, _n, _n))

# ══════════════════════════════════════════════════════════
# 3. 例題
# ══════════════════════════════════════════════════════════
# 例題1 e^{2x}
_e1 = 1 + 2 * _x + 2 * _x ** 2 + R(4, 3) * _x ** 3
eq(mac(sp.exp(2 * _x), 3), _e1, "例題1 e^{2x}")
eq(sp.diff(_e1, _x), 2 + 4 * _x + 4 * _x ** 2, "例題1 微分すると 2+4x+4x²")
eq(sp.expand(sp.diff(_e1, _x) - 2 * (1 + 2 * _x + 2 * _x ** 2)), 0,
   "例題1 微分は 2 倍（x² まで）")
chk(_e1.subs(_x, 0) == 1, "例題1 x = 0 で 1")
# 例題2 ln(1+2x)
_e2 = 2 * _x - 2 * _x ** 2 + R(8, 3) * _x ** 3
eq(mac(sp.log(1 + 2 * _x), 3), _e2, "例題2 ln(1+2x)")
eq(sp.diff(_e2, _x), 2 - 4 * _x + 8 * _x ** 2, "例題2 微分すると 2-4x+8x²")
eq(mac(2 / (1 + 2 * _x), 2), 2 - 4 * _x + 8 * _x ** 2, "例題2 2/(1+2x) と一致")
chk(sp.solve(sp.Abs(2 * _x) < 1) is not None, "例題2 範囲 |2x| < 1")
eq(sp.Rational(1, 2), R(1, 2), "例題2 |x| < 1/2")
# 例題3 e^x sin x
_e3 = _x + _x ** 2 + _x ** 3 / 3
eq(mac(sp.exp(_x) * sp.sin(_x), 3), _e3, "例題3 e^x sin x")
chk(coef(_e3, 0) == 0, "例題3 定数項なし")
chk(R(1, 2) - R(1, 6) == R(1, 3), "例題3 1/2 - 1/6 = 1/3")
# 例題4 dy/dx = x + y, y(0) = 1
_e4 = de_series(lambda a, b: a + b, 1, 3)
eq(_e4, 1 + _x + _x ** 2 + _x ** 3 / 3, "例題4 級数")
eq(sp.expand(sp.diff(_e4, _x) - (_x + _e4)).coeff(_x, 0), 0, "例題4 検算 定数項")
eq(sp.expand(sp.diff(_e4, _x))
   - sp.expand(1 + 2 * _x + _x ** 2), 0, "例題4 微分は 1+2x+x²")
eq(sp.expand(_x + (1 + _x + _x ** 2)), 1 + 2 * _x + _x ** 2, "例題4 x+y も同じ")
chk(_e4.subs(_x, 0) == 1, "例題4 初期条件")
# 厳密解 y = 2e^x - x - 1 と一致する
eq(mac(2 * sp.exp(_x) - _x - 1, 3), _e4, "例題4 厳密解の級数と一致")

# ══════════════════════════════════════════════════════════
# 4. 演習
# ══════════════════════════════════════════════════════════
# 1 e^{-x}
_a1 = 1 - _x + _x ** 2 / 2 - _x ** 3 / 6
eq(mac(sp.exp(-_x), 3), _a1, "演習1 e^{-x}")
eq(sp.diff(_a1, _x), -1 + _x - _x ** 2 / 2, "演習1 微分")
eq(sp.expand((1 + _x + _x ** 2 / 2) * (1 - _x + _x ** 2 / 2)).coeff(_x, 1), 0,
   "演習1 e^x e^{-x} の x の係数は 0")
eq(sp.expand((1 + _x + _x ** 2 / 2) * (1 - _x + _x ** 2 / 2)).coeff(_x, 2), 0,
   "演習1 x² の係数も 0")
# 2 sin 2x
_a2 = 2 * _x - R(4, 3) * _x ** 3
eq(mac(sp.sin(2 * _x), 3), _a2, "演習2 sin 2x")
chk((2 * _x) ** 3 == 8 * _x ** 3, "演習2 (2x)³ = 8x³")
eq(R(8, 6), R(4, 3), "演習2 8/6 = 4/3")
chk(coef(_a2, 2) == 0, "演習2 x² の項はない")
eq(sp.diff(_a2, _x), 2 - 4 * _x ** 2, "演習2 微分は 2-4x²")
eq(mac(2 * sp.cos(2 * _x), 2), 2 - 4 * _x ** 2, "演習2 2cos2x と一致")
# 3 cos(x²)
_a3 = 1 - _x ** 4 / 2
eq(mac(sp.cos(_x ** 2), 4), _a3, "演習3 cos(x²)")
chk(_a3.subs(_x, 0) == 1, "演習3 x = 0 で 1")
chk(all(coef(mac(sp.cos(_x ** 2), 7), _k) == 0
        for _k in (1, 2, 3, 5, 6, 7)), "演習3 x⁰ と x⁴ だけ")
chk(sp.expand((_x ** 2) ** 4) == _x ** 8, "演習3 次は x^8")
# 4 √(1+x)
_a4 = 1 + _x / 2 - _x ** 2 / 8 + _x ** 3 / 16
eq(mac(sp.sqrt(1 + _x), 3), _a4, "演習4 √(1+x)")
eq(_bin.subs(_p, R(1, 2)), _a4, "演習4 二項級数 p = 1/2 と一致")
eq(sp.expand((1 + _x / 2 - _x ** 2 / 8) ** 2).coeff(_x, 2), 0,
   "演習4 2 乗の x² の係数は 0")
eq(sp.expand((1 + _x / 2 - _x ** 2 / 8) ** 2).coeff(_x, 1), 1,
   "演習4 2 乗の x の係数は 1")
chk(R(1, 4) - R(1, 4) == 0, "演習4 1/4 - 1/4 = 0")
# 5 ln(1-x)
_a5 = -_x - _x ** 2 / 2 - _x ** 3 / 3
eq(mac(sp.log(1 - _x), 3), _a5, "演習5 ln(1-x)")
chk(all(coef(_a5, _k) < 0 for _k in (1, 2, 3)), "演習5 符号はすべてマイナス")
eq(sp.diff(_a5, _x), -1 - _x - _x ** 2, "演習5 微分")
eq(mac(-1 / (1 - _x), 2), -1 - _x - _x ** 2, "演習5 -1/(1-x) と一致")
eq(mac(sp.log(1 + _x) + sp.log(1 - _x), 4),
   mac(sp.log(1 - _x ** 2), 4), "演習5 足すと ln(1-x²)")
eq(mac(sp.log(1 - _x ** 2), 2), -_x ** 2, "演習5 ln(1-x²) は -x²-…")
# 6 1/(1+x²) → arctan
_a6 = 1 - _x ** 2 + _x ** 4
eq(mac(1 / (1 + _x ** 2), 4), _a6, "演習6 1/(1+x²)")
_a6i = sp.integrate(_a6, _x)
eq(_a6i, _x - _x ** 3 / 3 + _x ** 5 / 5, "演習6 積分")
eq(_a6i, mac(sp.atan(_x), 5), "演習6 arctan の級数と一致")
chk(_a6i.subs(_x, 0) == 0, "演習6 C = 0")
eq(sp.diff(_a6i, _x), _a6, "演習6 微分でもどる")
# 7 x cos x
_a7 = _x - _x ** 3 / 2 + _x ** 5 / 24
eq(mac(_x * sp.cos(_x), 5), _a7, "演習7 x cos x")
chk(all(coef(_a7, _k) == 0 for _k in (0, 2, 4)), "演習7 奇数次だけ")
chk(_a7.subs(_x, 0) == 0, "演習7 x = 0 で 0")
chk(sp.factorial(2) == 2 and sp.factorial(4) == 24, "演習7 2! = 2, 4! = 24")
# 8 dy/dx = y², y(0) = 1
_a8 = de_series(lambda a, b: b ** 2, 1, 3)
eq(_a8, 1 + _x + _x ** 2 + _x ** 3, "演習8 級数")
eq(mac(1 / (1 - _x), 3), _a8, "演習8 厳密解 1/(1-x) の級数と一致")
_ye = 1 / (1 - _x)
eq(sp.diff(_ye, _x) - _ye ** 2, 0, "演習8 厳密解はもとの式を満たす")
chk(_ye.subs(_x, 0) == 1, "演習8 初期条件")
eq(R(6, sp.factorial(3)), 1, "演習8 6/3! = 1")
eq(R(2, sp.factorial(2)), 1, "演習8 2/2! = 1")
# y'' = 2yy', y''' = 2(y')² + 2yy''
_yg = sp.Function("yg")
eq(sp.diff(_yg(_x) ** 2, _x), 2 * _yg(_x) * sp.Derivative(_yg(_x), _x),
   "演習8 (y²)' = 2yy'")
eq(sp.diff(2 * _yg(_x) * sp.Derivative(_yg(_x), _x), _x),
   2 * sp.Derivative(_yg(_x), _x) ** 2
   + 2 * _yg(_x) * sp.Derivative(_yg(_x), (_x, 2)),
   "演習8 (2yy')' = 2(y')²+2yy''")
chk(2 * 1 ** 2 + 2 * 1 * 2 == 6, "演習8 y'''(0) = 6")
# 9 係数の取り出し
_aa = sp.symbols("a0:4")
_poly = sum(_aa[_k] * _x ** _k for _k in range(4))
chk(_poly.subs(_x, 0) == _aa[0], "演習9 x = 0 で a0")
chk(sp.diff(_poly, _x).subs(_x, 0) == _aa[1], "演習9 1 回微分で a1")
chk(sp.diff(_poly, _x, 2).subs(_x, 0) == 2 * _aa[2], "演習9 2 回微分で 2a2")
chk(sp.diff(_poly, _x, 3).subs(_x, 0) == 6 * _aa[3], "演習9 3 回微分で 6a3")
# 10 cos x の分母
_wrong = 1 - _x ** 2 / 2 + _x ** 4 / 4
_right = mac(sp.cos(_x), 4)
eq(_right, 1 - _x ** 2 / 2 + _x ** 4 / 24, "演習10 正しい cos の級数")
chk(coef(_wrong, 2) == coef(_right, 2), "演習10 x² の項は合っている")
chk(coef(_wrong, 4) != coef(_right, 4), "演習10 x⁴ の項はちがう")
chk(sp.factorial(4) == 24, "演習10 4! = 24")
eq(sp.diff(_right, _x), -_x + _x ** 3 / 6, "演習10 正しい級数の微分")
eq(mac(-sp.sin(_x), 3), -_x + _x ** 3 / 6, "演習10 それは -sin x")
eq(sp.diff(_wrong, _x), -_x + _x ** 3, "演習10 生徒の級数の微分")
chk(sp.expand(sp.diff(_wrong, _x) - mac(-sp.sin(_x), 3)) != 0,
    "演習10 生徒の級数は -sin x にならない")

# ══════════════════════════════════════════════════════════
# 5. 数え上げ（答えの重複を防ぐ）
# ══════════════════════════════════════════════════════════
_ans = [str(sp.expand(_e)) for _e in
        (_a1, _a2, _a3, _a4, _a5, _a6, _a7, _a8)]
chk(len(set(_ans)) == len(_ans), "演習の答えが重複していない")

# ══════════════════════════════════════════════════════════
# 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl519-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)] == list(range(1, 8)),
    "The idea が 1..7 で連番")
chk(TEXT.count("**検算") >= 12, "検算が十分ある: %d" % TEXT.count("**検算"))
not_in_text("**確かめ", "検算は「検算」で統一")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
_ce = TEXT[TEXT.index("\n## Common errors"):TEXT.index("\n## Exercises")]
chk(_ce.count("::: {.callout-warning}") == 6, "Common errors が 6 つ")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
chk(all("@eq-" not in TEXT.split("$$")[i] for i in range(1, len(TEXT.split("$$")), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    chk(not re.search(r"[ぁ-んァ-ン一-龥]",
                      _blk.replace("**試験ではこう書く**", "")),
        "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors", "exercises"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aahl519", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head, "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は 1 つだけ")
not_in_text("**この節ですること：", "節の頭の 1 文は置かない")
not_in_text("\\vec{", "ベクトルの記号は太字")
chk(len(re.findall(r"^::: ", TEXT, re.M)) == len(re.findall(r"^:::$", TEXT, re.M)),
    "::: の開閉が一致")
for _h in re.findall(r"^#{1,4} .+$", TEXT, re.M):
    chk(not re.search(r"\$\s*—", _h), "見出しで数式の直後に —: " + _h)
_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_j = TEXT.index(chr(10) + "## Worked examples", _i)
_wiw = TEXT[_i:_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
# ★ The idea の見出しは「英語（日本語）」の形（_AA-HL-PLAN.md の「決まったこと」5）
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)

# ══════════════════════════════════════════════════════════
# 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-5-19-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-19-idea-%s.svg)" % _n in TEXT,
        "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")

# ══════════════════════════════════════════════════════════
# 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/05-calculus/aahl-5-19.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-19.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| Maclaurin series |", "| power series |", "| binomial series |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 分母の階乗を落とす", "階乗を落とす")
in_text("## $\\ln(1+x)$ や $\\arctan x$ の分母を階乗にする", "分母の取りちがえ")
in_text("## 置きかえのときに $2$ 乗を忘れる", "2 乗を忘れる")
in_text("**分母に注意してください。**", "分母の注意")
in_text("**もとの $x$ のところに、まるごと入れます。**", "置きかえの注意")
in_text("$x^{n}$ の係数は $\\dfrac{f^{(n)}(0)}{n!}$", "係数の式")
in_text("**Maclaurin は中心が $0$**", "中心は 0")
in_text("e^{x^{2}} = 1+x^{2}+\\frac{x^{4}}{2!}+\\cdots", "シラバスの例")
in_text("$2! = 2$、$4! = 24$ です。", "階乗の値")
in_fig("more terms, a longer stretch that matches", "図 (a) の見出し")
in_fig("four ways to build a new series from a known one", "図 (b) の見出し")
in_fig("a series from the booklet", "図 (b) の出発点")
for _w in ("substitute", "multiply", "differentiate", "integrate"):
    in_fig('"%s"' % _w, "図 (b) の道: " + _w)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
