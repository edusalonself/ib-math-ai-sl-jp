"""AA HL 2.12（多項式関数・因数定理・剰余定理・解の和と積）の内容を検算する。

    python3 figs/aa-hl/check_aahl_2_12.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "02-functions")
QMD = os.path.join(BASE, "aahl-2-12.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_2_12.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x, X, a, b, c, d, p, q = sp.symbols("x X a b c d p q")


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


def roots_of(poly):
    return sorted(sp.roots(sp.Poly(poly, x)).items(), key=lambda t: sp.re(t[0]))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの定理
# ══════════════════════════════════════════════════════════
# 剰余定理：P(x) = (x-a)Q(x) + P(a)
_Q = sp.Function("Q")
_gen = a * x ** 3 + b * x ** 2 + c * x + d
_r = sp.rem(sp.Poly(_gen, x), sp.Poly(x - p, x))
eq(_r.as_expr(), _gen.subs(x, p), "剰余定理（3 次、記号のまま）")
for _n in range(1, 7):
    _co = sp.symbols("c0:%d" % (_n + 1))
    _P = sum(_co[i] * x ** i for i in range(_n + 1))
    eq(sp.rem(sp.Poly(_P, x), sp.Poly(x - p, x)).as_expr(), _P.subs(x, p),
       "剰余定理（%d 次）" % _n)
# 解と係数：3 次
_al, _be, _ga = sp.symbols("alpha beta gamma")
_exp = sp.expand(a * (x - _al) * (x - _be) * (x - _ga))
eq(sp.Poly(_exp, x).coeff_monomial(x ** 2), -a * (_al + _be + _ga), "和の係数")
eq(sp.Poly(_exp, x).coeff_monomial(1), -a * _al * _be * _ga, "積の係数")
eq(sp.Poly(_exp, x).coeff_monomial(x),
   a * (_al * _be + _be * _ga + _ga * _al), "真ん中の係数")
# 一般次数：sum = -a_{n-1}/a_n, product = (-1)^n a_0 / a_n
for _n in range(2, 7):
    _rs = sp.symbols("r0:%d" % _n)
    _P = sp.expand(a * sp.prod([x - _ri for _ri in _rs]))
    _pl = sp.Poly(_P, x)
    eq(-_pl.coeff_monomial(x ** (_n - 1)) / a, sum(_rs), "和（%d 次）" % _n)
    eq((-1) ** _n * _pl.coeff_monomial(1) / a, sp.prod(_rs), "積（%d 次）" % _n)

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
_P0 = x ** 3 - 2 * x ** 2 - 5 * x + 6
eq(sp.factor(_P0), (x + 2) * (x - 1) * (x - 3), "§2 因数分解")
chk(sorted(sp.solve(_P0, x)) == [-2, 1, 3], "§2 解は -2, 1, 3")
chk(_P0.subs(x, 2) == -4, "§3 P(2) = -4")
chk(_P0.subs(x, 1) == 0, "§4 P(1) = 0")
eq(sp.expand((x - 1) * (x ** 2 - x - 6)), _P0, "§5 割ったあと")
eq(sp.factor(x ** 2 - x - 6), (x - 3) * (x + 2), "§5 2 次式の因数分解")
eq(sp.expand((x - 1) * (x ** 2 + p * x + q)),
   x ** 3 + (p - 1) * x ** 2 + (q - p) * x - q, "§5 係数くらべ")
chk(sp.solve([p - 1 + 2, -q - 6], [p, q]) == {p: -1, q: -6}, "§5 p = -1, q = -6")
chk((-2) + 1 + 3 == 2, "§6 和は 2")
chk((-2) * 1 * 3 == -6, "§6 積は -6")
eq(sp.expand((x + 2) * (x ** 2 + 3)), x ** 3 + 2 * x ** 2 + 3 * x + 6, "§5 の例")
chk(sp.discriminant(x ** 2 + 3, x) == -12, "x^2+3 の判別式は負")
chk(sp.solve(x ** 2 + 1, x) == [-sp.I, sp.I], "§2 x^2+1 に実数解はない")

# ══════════════════════════════════════════════════════════
# 2. 例題
# ══════════════════════════════════════════════════════════
_P1 = 2 * x ** 3 + a * x ** 2 - 5 * x + 6
chk(sp.solve(_P1.subs(x, 2), a) == [-3], "例題1 a = -3")
_P1v = 2 * x ** 3 - 3 * x ** 2 - 5 * x + 6
eq(sp.factor(_P1v), (x - 2) * (x - 1) * (2 * x + 3), "例題1 因数分解")
eq(sp.expand((x - 2) * (2 * x ** 2 + p * x + q)),
   2 * x ** 3 + (p - 4) * x ** 2 + (q - 2 * p) * x - 2 * q, "例題1 係数くらべ")
chk(sp.solve([p - 4 + 3, -2 * q - 6], [p, q]) == {p: 1, q: -3}, "例題1 p=1, q=-3")
eq(sp.factor(2 * x ** 2 + x - 3), (x - 1) * (2 * x + 3), "例題1 2 次式")
chk(sorted(sp.solve(_P1v, x)) == [sp.Rational(-3, 2), 1, 2], "例題1 解")
chk(sum(sp.solve(_P1v, x)) == sp.Rational(3, 2), "例題1 和は 3/2")
chk(sp.prod(sp.solve(_P1v, x)) == -3, "例題1 積は -3")
chk(_P1v.subs(x, 1) == 0, "例題1 検算 P(1) = 0")

_P2 = x ** 3 + a * x ** 2 + b * x + 6
_s2 = sp.solve([_P2.subs(x, 1), _P2.subs(x, -2) - 12], [a, b])
chk(_s2 == {a: 0, b: -7}, "例題2 a=0, b=-7: %s" % _s2)
_P2v = x ** 3 - 7 * x + 6
eq(sp.factor(_P2v), (x - 1) * (x - 2) * (x + 3), "例題2 因数分解")
chk(sorted(sp.solve(_P2v, x)) == [-3, 1, 2], "例題2 解")
chk(_P2v.subs(x, -2) == 12, "例題2 検算 P(-2) = 12")
chk(sum(sp.solve(_P2v, x)) == 0 and sp.prod(sp.solve(_P2v, x)) == -6,
    "例題2 和 0・積 -6")

_E3 = 2 * x ** 3 - 5 * x ** 2 + x + 3
chk(sum(sp.solve(_E3, x)) == sp.Rational(5, 2), "例題3 和 5/2")
chk(sp.simplify(sp.prod(sp.solve(_E3, x)) + sp.Rational(3, 2)) == 0, "例題3 積 -3/2")
eq(sp.expand(4 * _E3.subs(x, X / 2)), X ** 3 - 5 * X ** 2 + 2 * X + 12,
   "例題3 (b) 置きかえ")
_E3b = X ** 3 - 5 * X ** 2 + 2 * X + 12
chk(sum(sp.solve(_E3b, X)) == 5, "例題3 新しい和は 5")
chk(sp.simplify(sp.prod(sp.solve(_E3b, X)) + 12) == 0, "例題3 新しい積は -12")
chk(sorted(sp.solve(_E3b, X)) == sorted([2 * _r for _r in sp.solve(_E3, x)]),
    "例題3 解が本当に 2 倍")

eq(sp.expand((x - 2) ** 2 * (x + 2)), x ** 3 - 2 * x ** 2 - 4 * x + 8, "例題4 展開")
chk(sp.solve(sp.Eq(((x - 2) ** 2 * (x - p)).subs(x, 0), 8), p) == [-2], "例題4 p = -2")
chk((x ** 3 - 2 * x ** 2 - 4 * x + 8).subs(x, 0) == 8, "例題4 (0, 8) を通る")
chk(((x - 2) ** 2 * (x + 2)).subs(x, 1) == 3
    and ((x - 2) ** 2 * (x + 2)).subs(x, 3) == 5, "例題4 両側で正")
chk(sp.roots(sp.Poly(x ** 3 - 2 * x ** 2 - 4 * x + 8, x))[2] == 2, "例題4 x=2 は重解")

# ══════════════════════════════════════════════════════════
# 3. 演習
# ══════════════════════════════════════════════════════════
_Q1 = x ** 3 - 4 * x ** 2 + x + 6
chk(_Q1.subs(x, -1) == 0, "演習1 P(-1) = 0")
eq(sp.factor(_Q1), (x + 1) * (x - 2) * (x - 3), "演習1 因数分解")
eq(sp.expand((x + 1) * (x ** 2 + p * x + q)),
   x ** 3 + (p + 1) * x ** 2 + (q + p) * x + q, "演習1 係数くらべ")
chk(sum(sp.solve(_Q1, x)) == 4 and sp.prod(sp.solve(_Q1, x)) == -6, "演習1 和・積")
chk((x ** 4 - 3 * x ** 2 + 2 * x - 5).subs(x, 2) == 3, "演習2 余りは 3")
_Q3 = 2 * x ** 3 + x ** 2 + a * x + b
_s3 = sp.solve([_Q3.subs(x, 1), _Q3.subs(x, -2) + 18], [a, b])
chk(_s3 == {a: 1, b: -4}, "演習3 a=1, b=-4: %s" % _s3)
_Q3v = 2 * x ** 3 + x ** 2 + x - 4
eq(sp.expand((x - 1) * (2 * x ** 2 + 3 * x + 4)), _Q3v, "演習3 因数分解")
chk(sp.discriminant(2 * x ** 2 + 3 * x + 4, x) == -23, "演習3 判別式 -23")
chk(len([_r for _r in sp.solve(_Q3v, x) if _r.is_real]) == 1, "演習3 実数解は 1 つ")
chk(_Q3v.subs(x, 1) == 0 and _Q3v.subs(x, -2) == -18, "演習3 検算")
_Q4 = 3 * x ** 3 + 2 * x ** 2 - 7 * x + 4
chk(sp.simplify(sum(sp.solve(_Q4, x)) + sp.Rational(2, 3)) == 0, "演習4 和 -2/3")
chk(sp.simplify(sp.prod(sp.solve(_Q4, x)) + sp.Rational(4, 3)) == 0, "演習4 積 -4/3")
chk(sp.solve(sp.Eq(-p, 5), p) == [-5], "演習5 p = -5")
for _qv in (-30, 0, 2, 100):
    _e = x ** 3 - 5 * x ** 2 + _qv * x + 8
    chk(sp.simplify(sp.prod(sp.roots(sp.Poly(_e, x), multiple=True)) + 8) == 0,
        "演習5 q=%s でも積は -8" % _qv)
_Q6 = x ** 3 - 3 * x ** 2 + 4 * x - 2
eq(sp.expand(8 * _Q6.subs(x, X / 2)), X ** 3 - 6 * X ** 2 + 16 * X - 16, "演習6")
chk(sum(sp.solve(X ** 3 - 6 * X ** 2 + 16 * X - 16, X)) == 6, "演習6 新しい和 6")
chk(sp.simplify(sp.prod(sp.solve(X ** 3 - 6 * X ** 2 + 16 * X - 16, X)) - 16) == 0,
    "演習6 新しい積 16")
eq(sp.expand((x - 3) ** 2 * (x + 2)), x ** 3 - 4 * x ** 2 - 3 * x + 18, "演習7 展開")
chk(sp.solve(sp.Eq(9 * (-p), 18), p) == [-2], "演習7 p = -2")
chk((x ** 3 - 4 * x ** 2 - 3 * x + 18).subs(x, 3) == 0, "演習7 x=3 が解")
chk(sp.diff(x ** 3 - 4 * x ** 2 - 3 * x + 18, x).subs(x, 3) == 0, "演習7 x=3 は重解")
_Q8 = (x + 2) * (x - 1) ** 2 * (x - 3)
chk(sp.degree(sp.expand(_Q8), x) == 4, "演習8 次数は 4")
chk(_Q8.subs(x, 0) == -6 and _Q8.subs(x, 2) == -4, "演習8 x=1 の両側で負")
chk(_Q8.subs(x, -3) == 96 and _Q8.subs(x, 0) == -6, "演習8 x=-2 で符号が変わる")
chk(sp.roots(sp.Poly(sp.expand(_Q8), x))[1] == 2, "演習8 x=1 は 2 重")
for _n in range(1, 9):
    chk((x ** _n - 1).subs(x, 1) == 0, "演習9 n=%d で P(1)=0" % _n)
    chk(sp.rem(sp.Poly(x ** _n - 1, x), sp.Poly(x - 1, x)).as_expr() == 0,
        "演習9 n=%d で割り切れる" % _n)
eq(sp.factor(x ** 3 - 1), (x - 1) * (x ** 2 + x + 1), "演習9 検算 n=3")
eq(sp.factor(x ** 4 - 1), (x - 1) * (x + 1) * (x ** 2 + 1), "演習9 検算 n=4")
eq(sp.expand((x - 1) * (x ** 3 + x ** 2 + x + 1)), x ** 4 - 1, "演習9 n=4 の商")
_Q10 = x ** 3 + 2 * x ** 2 + 3 * x + 6
chk(_Q10.subs(x, -2) == 0, "演習10 正しい余りは 0")
chk(_Q10.subs(x, 2) == 28, "演習10 生徒の計算は 28")
eq(sp.factor(_Q10), (x + 2) * (x ** 2 + 3), "演習10 因数分解")

# ══════════════════════════════════════════════════════════
# 4. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Polynomial functions, their graphs and equations;"
        " zeros, roots and factors.", "シラバス（多項式）を逐語で")
in_text("> The factor and remainder theorems.", "シラバス（2 つの定理）を逐語で")
in_text("> Sum and product of the roots of polynomial equations.",
        "シラバス（和と積）を逐語で")
in_text("> Link to: complex roots of quadratic and polynomial equations"
        " (AHL 1.14).", "Link to を逐語で")
in_text("公式集の **2.12** の欄", "公式集の場所")
in_text("> Sum and product of the roots of polynomial equations of the form"
        " $\\sum\\limits_{r=0}^{n} a_{r}x^{r} = 0$", "公式集の見出しを逐語で")
in_text("> Sum is $\\dfrac{-a_{n-1}}{a_{n}}$ ;"
        " product is $\\dfrac{(-1)^{n}a_{0}}{a_{n}}$", "公式集の式を逐語で")
in_text("**ただし公式集には載っていません。**", "真ん中の対称式は公式集にない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 5. GDC / 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("`menu` → `Analyze Graph` → `Zero`", "TI-Nspire のメニュー")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve", "polyRoots"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl212-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl212", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
for _fwd in ("aahl-2-13.qmd", "aahl-2-14.qmd", "aahl-2-15.qmd", "aahl-2-16.qmd"):
    not_in_text(_fwd, "まだ書いていないページへのリンクは張らない: " + _fwd)
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
in_text("### 1. Polynomial functions（多項式関数） {#polynomials}", "見出し 1")
in_text("### 2. Zeros, roots and factors: three names for one "
        "thing（同じことの $3$ つの言い方） {#zeros-roots-factors}", "見出し 2")
in_text("### 3. The remainder theorem（剰余定理） {#remainder}", "見出し 3")
in_text("### 4. The factor theorem（因数定理） {#factor}", "見出し 4")
in_text("### 5. How to factorise a cubic（因数分解の進め方） {#factorising}", "見出し 5")
in_text("### 6. The sum and product of the roots（解の和と積） "
        "{#sum-product}", "見出し 6")
in_text("### 7. Repeated roots and the shape of the graph（重解とグラフの形） "
        "{#repeated}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 6. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-2-12-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-2-12-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Each crossing of the $x$-axis is one factor", "図(a) の題")
in_fig("three zeros, three linear factors", "図(a) の要点")
in_fig("How many times the factor appears decides the shape at $x=a$",
       "図(b) の題")
in_fig("touches and turns back", "図(b) の重解")
in_text("$x$ 軸との交点が $1$ つあれば、$1$ 次の因数が $1$ つあります。",
        "キャプション (a)")
in_text("因数が何回現れるかで、$x$ 軸での形が変わります。", "キャプション (b)")
for leak in ["2x^{3}", "x^{4}", "18", "28"]:
    chk(leak not in FIGSTR, "図が例題・演習の値を載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 7. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("x^{3}-4x^{2}+x+6", "演習1"), ("x^{4}-3x^{2}+2x-5", "演習2"),
                    ("2x^{3}+x^{2}", "演習3"), ("3x^{3}+2x^{2}-7x+4", "演習4"),
                    ("x^{3}-3x^{2}+4x-2", "演習6"),
                    ("x^{3}+ax^{2}+bx+18", "演習7")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))
chk("x^{3}+2x^{2}+3x+6" in _BODY, "演習10 の式は §5 で先に出してある（意図的）")

# ══════════════════════════════════════════════════════════
# 8. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/02-functions/aahl-2-12.qmd" in DRAFT, "draft に登録")
chk('- section: "Topic 2 — Functions"' in DRAFT, "Topic 2 の節がある")
chk(DRAFT.index("aahl-1-16.qmd") < DRAFT.index("aahl-2-12.qmd"),
    "サイドバーの並びが Topic 1 → Topic 2")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aahl-2-12.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| polynomial |", "| remainder theorem |", "| factor theorem |",
          "| degree |", "| double zero / repeated root |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 9. 見張り
# ══════════════════════════════════════════════════════════
in_text("## $(x+2)$ で割るときは $x = -2$ を入れます", "符号の見張り")
in_text("## 因数を探すときは、定数項の約数から", "探し方")
in_text("**奇数回ならまたぎ、偶数回なら接します。**", "重解の見分け")
in_text("## 積の符号は、次数で変わります", "(-1)^n の見張り")
in_text("**$n$ 次式の解は、複素数まで数えれば重解を込めてちょうど $n$ 個です。**",
        "解の個数")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
