"""AA HL 2.13（有理関数のグラフ）の内容を検算する。

    python3 figs/aa-hl/check_aahl_2_13.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "02-functions")
QMD = os.path.join(BASE, "aahl-2-13.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_2_13.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x, k, a, b, c, m = sp.symbols("x k a b c m")


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


def vert(num, den, want, msg):
    """垂直漸近線（約分してから分母 = 0）が want であること。"""
    f = sp.cancel(num / den)
    d = sp.denom(sp.together(f))
    got = sorted(sp.solve(sp.Eq(d, 0), x))
    chk(got == sorted(want), "%s: 垂直漸近線 %s（得た %s）" % (msg, want, got))


def horiz(num, den, want, msg):
    for _s in (sp.oo, -sp.oo):
        chk(sp.limit(num / den, x, _s) == want,
            "%s: x→%s で y→%s" % (msg, _s, want))


def oblique(num, den, qw, rw, msg):
    q, r = sp.div(sp.expand(num), sp.expand(den), x)
    eq(q, qw, msg + " の商")
    eq(r, rw, msg + " の余り")
    chk(sp.limit(num / den - qw, x, sp.oo) == 0, msg + ": 差が 0 に近づく")


def xint(num, den, want, msg):
    got = sorted([s for s in sp.solve(sp.Eq(num, 0), x) if s.is_real
                  and den.subs(x, s) != 0])
    chk(got == sorted(want), "%s: x 切片 %s（得た %s）" % (msg, want, got))


def yint(num, den, want, msg):
    chk(den.subs(x, 0) != 0 and sp.simplify(num.subs(x, 0) / den.subs(x, 0) - want) == 0,
        "%s: y 切片 %s" % (msg, want))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_d, _e = sp.symbols("d e", positive=True)
chk(sp.limit((a * x + b) / (c * x ** 2 + _d * x + _e), x, sp.oo) == 0,
    "分母が 2 次なら y→0（記号のまま）")
_q, _r = sp.div(sp.expand(a * x ** 2 + b * x + c), _d * x + _e, x)
chk(sp.degree(_q, x) == 1, "分子が 2 次なら商は 1 次")
chk(sp.degree(sp.Poly(_r, x), x) <= 0, "余りは定数")
chk(sp.limit((a * x ** 2 + b * x + c) / (_d * x + _e) - _q, x, sp.oo) == 0,
    "商との差が 0 に近づく（記号のまま）")

# ══════════════════════════════════════════════════════════
# 1. The idea の関数
# ══════════════════════════════════════════════════════════
_N1, _D1 = x + 1, x ** 2 - x - 6
eq(sp.factor(_D1), (x - 3) * (x + 2), "§2 分母の因数分解")
vert(_N1, _D1, [-2, 3], "§2")
horiz(_N1, _D1, 0, "§3")
xint(_N1, _D1, [-1], "§5")
yint(_N1, _D1, sp.Rational(-1, 6), "§5")
chk(sp.cancel(_N1 / _D1) == _N1 / _D1, "§2 約分できない")
_N2, _D2 = x ** 2 - x - 2, x - 3
oblique(_N2, _D2, x + 2, 4, "§4")
eq(sp.expand((x + 2) * (x - 3) + 4), _N2, "§4 割り算の確かめ")
vert(_N2, _D2, [3], "§4")
chk((x ** 2 - x - 2).subs(x, 3) == 4, "§6 x=3 で分子は 4（符号の話）")
chk(sp.discriminant(x ** 2 + 1, x) == -4, "§7 x^2+1 の判別式")
horiz(2 * x + 1, x ** 2 + 1, 0, "§7")
chk(sp.solve(sp.Eq(x ** 2 + 1, 0)) == [-sp.I, sp.I], "§7 実数解なし")
eq(sp.cancel((3 * x + 6) / (x ** 2 + x - 2)), 3 / (x - 1), "§7 約分できる")
eq(sp.factor(x ** 2 + x - 2), (x + 2) * (x - 1), "§7 分母の因数分解")
chk(sp.limit((3 * x + 6) / (x ** 2 + x - 2), x, -2) == -1, "§7 x=-2 では -1 に近づく")

# ══════════════════════════════════════════════════════════
# 2. 例題
# ══════════════════════════════════════════════════════════
_N, _D = 2 * x - 4, x ** 2 - 9
eq(sp.factor(_D), (x - 3) * (x + 3), "例題1 分母")
vert(_N, _D, [-3, 3], "例題1")
horiz(_N, _D, 0, "例題1")
xint(_N, _D, [2], "例題1")
yint(_N, _D, sp.Rational(4, 9), "例題1")
chk(sp.nsimplify((_N / _D).subs(x, 10)) == sp.Rational(16, 91), "例題1 検算 x=10")

_N, _D = x ** 2 + 3 * x - 4, x + 2
oblique(_N, _D, x + 1, -6, "例題2")
eq(sp.expand((x + 1) * (x + 2) - 6), _N, "例題2 割り算の確かめ")
eq(sp.factor(_N), (x + 4) * (x - 1), "例題2 分子の因数分解")
vert(_N, _D, [-2], "例題2")
xint(_N, _D, [-4, 1], "例題2")
yint(_N, _D, -2, "例題2")
chk((_N / _D).subs(x, 10) == sp.Rational(21, 2), "例題2 検算 x=10 は 10.5")
chk(sp.Rational(21, 2) - 11 == sp.Rational(-1, 2), "例題2 漸近線から -0.5")

_N, _D = x ** 2 + k, x - 1
_q3, _r3 = sp.div(sp.expand(_N), _D, x)
eq(_q3, x + 1, "例題3 商")
eq(_r3, k + 1, "例題3 余り")
eq(sp.expand((x + 1) * (x - 1) + (k + 1)), _N, "例題3 割り算の確かめ")
vert(_N.subs(k, 3), _D, [1], "例題3 k=3")
chk(((_N / _D).subs(k, 3)).subs(x, 2) == 7, "例題3 検算 k=3, x=2")
chk((x + 1 + 4 / (x - 1)).subs(x, 2) == 7, "例題3 割り算の形でも 7")
eq(sp.cancel((x ** 2 - 1) / (x - 1)), x + 1, "例題3 k=-1 で約分")
chk(sp.limit((x ** 2 - 1) / (x - 1), x, 1) == 2, "例題3 k=-1 では 2 に近づく")
chk(((x ** 2 - 1) / (x - 1)).subs(x, 3) == 4, "例題3 検算 x=3")

_N, _D = 2 * x + 3, x ** 2 + 1
chk(sp.discriminant(_D, x) == -4, "例題4 判別式 -4")
horiz(_N, _D, 0, "例題4")
xint(_N, _D, [sp.Rational(-3, 2)], "例題4")
yint(_N, _D, 3, "例題4")
chk(_D.subs(x, sp.Rational(-3, 2)) == sp.Rational(13, 4), "例題4 検算 分母は 13/4")

# ══════════════════════════════════════════════════════════
# 3. 演習
# ══════════════════════════════════════════════════════════
_N, _D = x - 1, x ** 2 - 4
eq(sp.factor(_D), (x - 2) * (x + 2), "演習1 分母")
vert(_N, _D, [-2, 2], "演習1")
horiz(_N, _D, 0, "演習1")
xint(_N, _D, [1], "演習1")
yint(_N, _D, sp.Rational(1, 4), "演習1")

_N, _D = x + 3, x ** 2 + 2 * x - 8
eq(sp.factor(_D), (x + 4) * (x - 2), "演習2 分母")
vert(_N, _D, [-4, 2], "演習2")
horiz(_N, _D, 0, "演習2")
xint(_N, _D, [-3], "演習2")
yint(_N, _D, sp.Rational(-3, 8), "演習2")
chk(_D.subs(x, -3) == -5, "演習2 検算 分母は -5")

_N, _D = x ** 2 - 4, x + 1
oblique(_N, _D, x - 1, -3, "演習3")
eq(sp.expand((x - 1) * (x + 1) - 3), _N, "演習3 割り算の確かめ")
vert(_N, _D, [-1], "演習3")
xint(_N, _D, [-2, 2], "演習3")
yint(_N, _D, -4, "演習3")
chk((_N / _D).subs(x, 9) == sp.Rational(77, 10), "演習3 検算 x=9")

_N, _D = x ** 2 + 2 * x + 5, x - 1
oblique(_N, _D, x + 3, 8, "演習4")
eq(sp.expand((x + 3) * (x - 1) + 8), _N, "演習4 割り算の確かめ")
vert(_N, _D, [1], "演習4")
chk(sp.discriminant(_N, x) == -16, "演習4 判別式 -16")
xint(_N, _D, [], "演習4")
yint(_N, _D, -5, "演習4")

_N, _D = 2 * x - 1, x ** 2 + x + 1
chk(sp.discriminant(_D, x) == -3, "演習5 判別式 -3")
horiz(_N, _D, 0, "演習5")
xint(_N, _D, [sp.Rational(1, 2)], "演習5")
yint(_N, _D, -1, "演習5")
for _v in (-1, 0, 1):
    chk(_D.subs(x, _v) > 0, "演習5 分母は正: x=%s" % _v)

_s6 = sp.solve([sp.Rational(1, 1) * b / (-6) + 1, -3 * a + b], [a, b])
chk(_s6 == {a: 2, b: 6}, "演習6 a=2, b=6: %s" % _s6)
vert(2 * x + 6, x ** 2 - x - 6, [-2, 3], "演習6")
yint(2 * x + 6, x ** 2 - x - 6, -1, "演習6")
xint(2 * x + 6, x ** 2 - x - 6, [-3], "演習6")

_N, _D = x ** 2 + k * x + 9, x - 3
_q7, _r7 = sp.div(sp.expand(_N), _D, x)
eq(_q7, x + k + 3, "演習7 商")
eq(_r7, 3 * k + 18, "演習7 余り")
eq(sp.expand((x + k + 3) * (x - 3) + (3 * k + 18)), _N, "演習7 割り算の確かめ")
chk(sp.discriminant(_N, x) == k ** 2 - 36, "演習7 判別式 k^2-36")
eq(sp.factor(_N.subs(k, 6)), (x + 3) ** 2, "演習7 k=6")
eq(sp.factor(_N.subs(k, -6)), (x - 3) ** 2, "演習7 k=-6")
chk(sp.solve(sp.Eq(_N.subs(x, 3), 0), k) == [-6], "演習7 x=3 が解になるのは k=-6 だけ")
eq(sp.cancel(_N.subs(k, -6) / _D), x - 3, "演習7 k=-6 で約分")
for _kv in (-10, -8, 7, 9, 20):
    _rr = [s for s in sp.solve(sp.Eq(_N.subs(k, _kv), 0), x) if s.is_real
           and _D.subs(x, s) != 0]
    chk(len(_rr) == 2, "演習7 k=%s では x 切片 2 つ" % _kv)
for _kv in (-5, 0, 5):
    _rr = [s for s in sp.solve(sp.Eq(_N.subs(k, _kv), 0), x) if s.is_real]
    chk(len(_rr) == 0, "演習7 k=%s では x 切片 0 個" % _kv)
xint(_N.subs(k, 6), _D, [-3], "演習7 k=6")
xint(_N.subs(k, -6), _D, [], "演習7 k=-6")

_q8, _r8 = sp.div(sp.expand(x ** 2 + b * x + c), x - 2, x)
eq(_q8, x + b + 2, "演習8 商")
chk(sp.solve(sp.Eq(b + 2, 5), b) == [3], "演習8 b=3")
chk(sp.solve(sp.Eq(c / (-2), 4), c) == [-8], "演習8 c=-8")
oblique(x ** 2 + 3 * x - 8, x - 2, x + 5, 2, "演習8 検算")
yint(x ** 2 + 3 * x - 8, x - 2, 4, "演習8 検算")

_N, _D = x ** 2 + 1, x
oblique(_N, _D, x, 1, "演習9")
vert(_N, _D, [0], "演習9")
chk(sp.simplify(_N / _D - (x + 1 / x)) == 0, "演習9 x + 1/x")
chk((x + 1 / x).subs(x, 2) == sp.Rational(5, 2), "演習9 検算 x=2")
xint(_N, _D, [], "演習9")
chk(_D.subs(x, 0) == 0, "演習9 y 切片はない")

_N, _D = x ** 2 + 3 * x + 2, x + 2
eq(sp.factor(_N), (x + 1) * (x + 2), "演習10 分子の因数分解")
chk(_N.subs(x, -2) == 0, "演習10 分子も 0")
eq(sp.cancel(_N / _D), x + 1, "演習10 約分すると x+1")
chk(sp.limit(_N / _D, x, -2) == -1, "演習10 -1 に近づく")
chk(sp.nsimplify((_N / _D).subs(x, sp.Rational(-19, 10))) == sp.Rational(-9, 10),
    "演習10 検算 x=-1.9")
chk(sp.nsimplify((_N / _D).subs(x, sp.Rational(-21, 10))) == sp.Rational(-11, 10),
    "演習10 検算 x=-2.1")

# ══════════════════════════════════════════════════════════
# 4. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Rational functions of the form $f(x) = \\dfrac{ax+b}{cx^{2}+dx+e}$,"
        " and $f(x) = \\dfrac{ax^{2}+bx+c}{dx+e}$.", "シラバス本体を逐語で")
in_text("> The reciprocal function is a particular case.",
        "Guidance（逆数関数）を逐語で")
in_text("> Graphs should include all asymptotes (horizontal, vertical and oblique)"
        " and any intercepts with axes.", "Guidance（かくもの）を逐語で")
in_text("> Link to: rational functions (SL 2.8).", "Link to を逐語で")
in_text("## 公式集には、この項目の欄がありません", "公式集にないことを書く")
not_in_text("公式集の **2.13**", "ありもしない欄を書かない")
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
in_text("`menu` → `Window / Zoom`", "TI-Nspire のメニュー")
in_text("**漸近線は、電卓が引いてくれるわけではありません。**", "電卓の限界")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl213-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl213", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
for _fwd in ("aahl-2-14.qmd", "aahl-2-15.qmd", "aahl-2-16.qmd"):
    not_in_text(_fwd, "まだ書いていないページへのリンクは張らない: " + _fwd)
chk(len(re.findall(r"\]\(aahl-2-12\.qmd", TEXT)) >= 2, "2.12 へのリンク")
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
in_text("### 1. Which functions are meant（どんな関数か） {#idea}", "見出し 1")
in_text("### 2. Vertical asymptotes（垂直漸近線） {#vertical}", "見出し 2")
in_text("### 3. A quadratic denominator: the horizontal "
        "asymptote（分母が $2$ 次のとき：水平漸近線） {#horizontal}", "見出し 3")
in_text("### 4. A quadratic numerator: the oblique asymptote（分子が "
        "$2$ 次のとき：斜め漸近線） {#oblique}", "見出し 4")
in_text("### 5. Intercepts with the axes（軸との交点） {#intercepts}", "見出し 5")
in_text("### 6. The steps for sketching the graph（グラフをかく手順） "
        "{#sketching}", "見出し 6")
in_text("### 7. No vertical asymptote, and fractions that "
        "cancel（垂直漸近線がない場合と、約分できる場合） {#special}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 6. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-2-13-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-2-13-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("A quadratic denominator: two vertical asymptotes, and $y=0$", "図(a) の題")
in_fig("the degree on top is smaller", "図(a) の要点")
in_fig("A quadratic on top: one vertical asymptote, and a slanted one", "図(b) の題")
in_fig("divide first: the quotient is the slanted asymptote", "図(b) の要点")
in_text("分母のほうが次数が高いので、遠くでは $y$ が $0$ に近づきます。",
        "キャプション (a)")
in_text("割り算をすると、商が斜めの漸近線になります。", "キャプション (b)")
chk("t * t - t - 6.0" in FIG, "図(a) は §2 と同じ分母")
chk("t * t - t - 2.0" in FIG, "図(b) は §4 と同じ分子")
for leak in ["4/9", "x+1-", "13/4"]:
    chk(leak not in FIGSTR, "図が例題の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 7. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
# （x^2+x+1 は Common errors、x^2+bx+c はシラバスの引用、x^2+3x+2 は
#   例題 2 の展開の途中に出てくるので、ここでは見張らない）
for leak, where in [("x^{2}-4}{x+1", "演習3"), ("x^{2}+2x+5", "演習4"),
                    ("x^{2}+kx+9", "演習7"),
                    ("{x^{2}+3x+2}{x+2}", "演習10")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 8. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/02-functions/aahl-2-13.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-2-12.qmd") < DRAFT.index("aahl-2-13.qmd"),
    "サイドバーの並びが 2.12 → 2.13")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aahl-2-13.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| rational function |", "| asymptote |", "| oblique asymptote |",
          "| numerator |", "| denominator |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 9. 見張り
# ══════════════════════════════════════════════════════════
in_text("## 分子も同時に $0$ になるときは、垂直漸近線ではありません", "約分の見張り")
in_text("## 水平漸近線を横切ることもあります", "漸近線は交わってよい")
in_text("## 割り算の余りは、漸近線に入りません", "余りの見張り")
in_text("**$x$ 軸との交点は、分子だけ**を見ます。", "x 切片は分子")
in_text("**順番を守ってください。**", "因数分解 → 約分 → 漸近線")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
