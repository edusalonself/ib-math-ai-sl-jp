"""AA HL 2.14（偶関数・奇関数・逆関数・self-inverse）の内容を検算する。

    python3 figs/aa-hl/check_aahl_2_14.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "02-functions")
QMD = os.path.join(BASE, "aahl-2-14.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_2_14.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x, y, a, b, c, d, k = sp.symbols("x y a b c d k")


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


def parity(f, want, msg):
    even = sp.simplify(f.subs(x, -x) - f) == 0
    odd = sp.simplify(f.subs(x, -x) + f) == 0
    got = "even" if even and not odd else ("odd" if odd and not even else "neither")
    chk(got == want, "%s: %s のはずが %s" % (msg, want, got))


def inverse(f, want, msg):
    sols = sp.solve(sp.Eq(y, f), x)
    chk(len(sols) == 1, msg + ": x について 1 つに解ける")
    got = sp.simplify(sols[0].subs(y, x))
    chk(sp.simplify(got - want) == 0, "%s: 逆関数 %s（得た %s）" % (msg, want, got))
    chk(sp.simplify(f.subs(x, want) - x) == 0, msg + ": f(f^{-1}(x)) = x")


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_f = sp.Function("f")
# odd なら f(0) = 0（式で）
_odd = sp.Symbol("f0")
chk(sp.solve(sp.Eq(_odd, -_odd), _odd) == [0], "odd なら f(0) = 0")
# even かつ odd なら 0
chk(sp.solve(sp.Eq(_odd, -_odd), _odd) == [0], "even かつ odd なら 0")
# (ax+b)/(cx+d) の逆関数
_g = (a * x + b) / (c * x + d)
_gi = sp.simplify(sp.solve(sp.Eq(y, _g), x)[0].subs(y, x))
eq(_gi, (-d * x + b) / (c * x - a), "一般の逆関数の形")
# d = -a なら self-inverse
_sf = (a * x + b) / (c * x - a)
chk(sp.simplify(sp.simplify(_sf.subs(x, _sf)) - x) == 0,
    "(ax+b)/(cx-a) は self-inverse")
for _n in range(1, 7):
    parity(x ** (2 * _n), "even", "x^{%d} は even" % (2 * _n))
    parity(x ** (2 * _n - 1), "odd", "x^{%d} は odd" % (2 * _n - 1))

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
parity(x ** 2 - 4, "even", "§1 x^2-4")
parity(x ** 3 - x, "odd", "§1 x^3-x")
parity(x ** 2 + x, "neither", "§1 x^2+x")
eq((x ** 2 + x).subs(x, -x), x ** 2 - x, "§1 h(-x)")
chk((2 ** 2 == (-2) ** 2), "§5 f(2) = f(-2) = 4")
inverse((2 * x + 1) / (x - 3), (3 * x + 1) / (x - 2), "§4")
eq(sp.expand((x - 3) ** 2 - 4), x ** 2 - 6 * x + 5, "§5 平方完成")
chk(sp.solve(sp.Eq((x - 3) ** 2 - 4, y), x)
    == [3 - sp.sqrt(y + 4), 3 + sp.sqrt(y + 4)], "§5 ± の 2 つ")
# §3 の周期の例（f(x) = x for 0 <= x < 4）
chk(6 - 4 == 2 and -1 + 4 == 3, "§3 周期の計算")
# §7 self-inverse
chk(sp.simplify(sp.simplify(((x + 3) / (x - 1)).subs(x, (x + 3) / (x - 1))) - x) == 0,
    "§7 (x+3)/(x-1) は self-inverse")
eq(sp.expand((x + 3) + 3 * (x - 1)), 4 * x, "§7 分子")
eq(sp.expand((x + 3) - (x - 1)), 4, "§7 分母")

# ══════════════════════════════════════════════════════════
# 2. 例題
# ══════════════════════════════════════════════════════════
parity(x ** 4 - 3 * x ** 2, "even", "例題1 (a)")
parity(x ** 3 - 4 * x, "odd", "例題1 (b)")
parity(x ** 2 + x, "neither", "例題1 (c)")
chk((x ** 4 - 3 * x ** 2).subs(x, 1) == -2
    and (x ** 4 - 3 * x ** 2).subs(x, -1) == -2, "例題1 検算 (a)")
chk((x ** 3 - 4 * x).subs(x, 1) == -3
    and (x ** 3 - 4 * x).subs(x, -1) == 3, "例題1 検算 (b)")
chk((x ** 2 + x).subs(x, 1) == 2 and (x ** 2 + x).subs(x, -1) == 0,
    "例題1 検算 (c)")

inverse((3 * x + 2) / (x - 1), (x + 2) / (x - 3), "例題2")
chk(((3 * x + 2) / (x - 1)).subs(x, 2) == 8, "例題2 検算 f(2) = 8")
chk(((x + 2) / (x - 3)).subs(x, 8) == 2, "例題2 検算 f^{-1}(8) = 2")
eq(sp.simplify((3 * x + 2) / (x - 1)), 3 + 5 / (x - 1), "例題2 3 + 5/(x-1)")

_F3 = x ** 2 - 6 * x + 5
chk(_F3.subs(x, 2) == -3 and _F3.subs(x, 4) == -3, "例題3 (a) 同じ値")
eq(_F3, (x - 3) ** 2 - 4, "例題3 (b) 平方完成")
chk(sp.simplify((3 + sp.sqrt(x + 4) - 3) ** 2 - 4 - x) == 0, "例題3 (c) 逆関数")
chk(_F3.subs(x, 5) == 0 and (3 + sp.sqrt(0 + 4)) == 5, "例題3 検算 5 → 0 → 5")
chk(sp.minimum(_F3, x) == -4, "例題3 値域は y >= -4")

_F4 = (4 * x + 1) / (x - 4)
inverse(_F4, _F4, "例題4")
chk(sp.simplify(sp.simplify(_F4.subs(x, _F4)) - x) == 0, "例題4 f(f(x)) = x")
eq(sp.expand(4 * (4 * x + 1) + (x - 4)), 17 * x, "例題4 分子")
eq(sp.expand((4 * x + 1) - 4 * (x - 4)), 17, "例題4 分母")
chk(_F4.subs(x, 5) == 21 and _F4.subs(x, 21) == 5, "例題4 検算 5 → 21 → 5")

# ══════════════════════════════════════════════════════════
# 3. 演習
# ══════════════════════════════════════════════════════════
parity(3 * x ** 4 + x ** 2, "even", "演習1 f")
parity(x ** 5 - x, "odd", "演習1 g")
parity(x ** 3 + 1, "neither", "演習1 h")
chk((x ** 3 + 1).subs(x, 1) == 2 and (x ** 3 + 1).subs(x, -1) == 0, "演習1 検算 h")
chk((x ** 5 - x).subs(x, 2) == 30 and (x ** 5 - x).subs(x, -2) == -30,
    "演習1 検算 g")
inverse(2 * x - 5, (x + 5) / 2, "演習2")
chk((2 * x - 5).subs(x, 3) == 1 and ((x + 5) / 2).subs(x, 1) == 3, "演習2 検算")
inverse((4 * x - 1) / (x + 2), (2 * x + 1) / (4 - x), "演習3")
chk(((4 * x - 1) / (x + 2)).subs(x, 1) == 1, "演習3 検算 f(1) = 1")
chk(((4 * x - 1) / (x + 2)).subs(x, 0) == sp.Rational(-1, 2), "演習3 検算 f(0)")
chk(sp.simplify(((2 * x + 1) / (4 - x)).subs(x, sp.Rational(-1, 2))) == 0,
    "演習3 検算 戻る")
eq(x ** 2 + 4 * x + 7, (x + 2) ** 2 + 3, "演習4 平方完成")
chk(sp.simplify((-2 + sp.sqrt(x - 3) + 2) ** 2 + 3 - x) == 0, "演習4 逆関数")
chk((x ** 2 + 4 * x + 7).subs(x, 0) == 7 and (-2 + sp.sqrt(7 - 3)) == 0,
    "演習4 検算 0 → 7 → 0")
_F5 = (2 * x + 5) / (x - 2)
chk(sp.simplify(sp.simplify(_F5.subs(x, _F5)) - x) == 0, "演習5 self-inverse")
eq(sp.expand(2 * (2 * x + 5) + 5 * (x - 2)), 9 * x, "演習5 分子")
eq(sp.expand((2 * x + 5) - 2 * (x - 2)), 9, "演習5 分母")
chk(_F5.subs(x, 3) == 11 and _F5.subs(x, 11) == 3, "演習5 検算 3 → 11 → 3")
_F6 = x ** 3 + a * x ** 2 + b * x + c
eq(sp.expand(_F6.subs(x, -x) + _F6), 2 * a * x ** 2 + 2 * c, "演習6 odd の条件")
chk(sp.solve([sp.Eq(a, -a), sp.Eq(c, -c)], [a, c]) == {a: 0, c: 0}, "演習6 a=c=0")
parity((x ** 3 + b * x).subs(b, 5), "odd", "演習6 検算 a=c=0 なら odd")
chk(10 - 4 - 4 == 2 and (-3) + 4 == 1, "演習7 周期の計算")
chk(2 ** 2 == 4 and 1 ** 2 == 1, "演習7 値は 4 と 1")
chk(6 - 4 == 2, "演習7 検算 f(6) = f(2)")
eq(x ** 2 - 4 * x, (x - 2) ** 2 - 4, "演習9 平方完成")
chk(sp.simplify((2 - sp.sqrt(x + 4) - 2) ** 2 - 4 - x) == 0, "演習9 逆関数")
chk((x ** 2 - 4 * x).subs(x, 0) == 0 and (2 - sp.sqrt(0 + 4)) == 0,
    "演習9 検算 0 → 0 → 0")
chk((2 - sp.sqrt(5 + 4)) == -1, "演習9 値域は y <= 2")
chk((x ** 2).subs(x, -3) == 9 and sp.sqrt(9) == 3, "演習10 9 → 3")
chk(sp.sqrt(9) != -3, "演習10 -3 には戻らない")
chk(sp.sqrt(sp.Integer(3) ** 2) == 3, "演習10 x >= 0 なら戻る")

# ══════════════════════════════════════════════════════════
# 4. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Odd and even functions.", "シラバス（偶奇）を逐語で")
in_text("> Even: $f(-x) = f(x)$", "Guidance（even）を逐語で")
in_text("> Odd: $f(-x) = -f(x)$", "Guidance（odd）を逐語で")
in_text("> Includes periodic functions.", "Guidance（周期）を逐語で")
in_text("> Finding the inverse function, $f^{-1}(x)$, including domain"
        " restriction.", "シラバス（逆関数）を逐語で")
in_text("> Self-inverse functions.", "シラバス（self-inverse）を逐語で")
not_in_text("公式集の **2.14**", "ありもしない欄を書かない")
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
in_text("**ただし、定義域は画面に出ません。**", "電卓の限界")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl214-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl214", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
for _fwd in ("aahl-2-15.qmd", "aahl-2-16.qmd"):
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
in_text("### 1. Even and odd functions（偶関数と奇関数） {#even-odd}", "見出し 1")
in_text("### 2. The symmetry of the graph（グラフの対称性） {#symmetry}", "見出し 2")
in_text("### 3. Periodic functions（周期関数） {#periodic}", "見出し 3")
in_text("### 4. Finding the inverse function（逆関数を求める） {#inverse}", "見出し 4")
in_text("### 5. Restricting the domain（定義域を制限する） {#restriction}", "見出し 5")
in_text("### 6. Domain and range swap over（定義域と値域の入れかわり） "
        "{#domain-range}", "見出し 6")
in_text("### 7. Self-inverse functions（self-inverse な関数） "
        "{#self-inverse}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 6. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-2-14-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-2-14-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("even: $f(-x) = f(x)$", "図(a) even")
in_fig("odd: $f(-x) = -f(x)$", "図(a) odd")
in_fig("a mirror in the $y$-axis", "図(a) の要点")
in_fig("a half turn about the origin", "図(a) の要点 2")
in_fig("Cut the domain first, then reflect in $y=x$", "図(b) の題")
in_fig("the dotted part\\nis cut off", "図(b) の注")
in_text("even は $y$ 軸で折り返せて、odd は原点のまわりに半回転できます。",
        "キャプション (a)")
in_text("$x \\geq 0$ に切ってから折り返すと、逆関数になります。", "キャプション (b)")
for leak in ["3 + \\sqrt", "17", "9x"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 7. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("3x^{4}", "演習1"), ("4x-1}{x+2", "演習3"),
                    ("x^{2}+4x+7", "演習4"), ("2x+5}{x-2", "演習5"),
                    ("x^{2}-4x", "演習9")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 8. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/02-functions/aahl-2-14.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-2-13.qmd") < DRAFT.index("aahl-2-14.qmd"),
    "サイドバーの並びが 2.13 → 2.14")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aahl-2-14.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| even function |", "| odd function |", "| periodic function |",
          "| inverse function |", "| self-inverse |", "| one-to-one |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 9. 見張り
# ══════════════════════════════════════════════════════════
in_text("## 「どちらでもない」がふつうです", "neither の見張り")
in_text("## どちらに切ったかで、$f^{-1}$ の式が変わります", "± の見張り")
in_text("## $f^{-1}(x)$ を $\\dfrac{1}{f(x)}$ と取りちがえる", "逆数との取りちがえ")
in_text("**odd な関数が $x = 0$ で定義されていれば、$f(0) = 0$ です。**",
        "odd なら原点を通る")
in_text("**$\\pm$ のまま答えると、関数になりません。**", "± のまま答えない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
