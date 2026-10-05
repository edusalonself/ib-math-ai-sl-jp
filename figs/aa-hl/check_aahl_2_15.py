"""AA HL 2.15（g(x) >= f(x) を解く）の内容を検算する。

    python3 figs/aa-hl/check_aahl_2_15.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "02-functions")
QMD = os.path.join(BASE, "aahl-2-15.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_2_15.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x = sp.Symbol("x", real=True)
R = sp.S.Reals
oo = sp.oo


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


def solves(rel, want, msg):
    got = sp.solveset(rel, x, R)
    chk(got == want, "%s: %s のはずが %s" % (msg, want, got))


I, U = sp.Interval, sp.Union

# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a, _p, _q = sp.symbols("a p q", real=True, positive=True)
# 負の数を掛けると向きが変わる
chk(sp.simplify((3 > 1)) is sp.true and (-3 < -1), "負を掛けると向きが変わる")
# 2 乗の因数は符号を変えない
for _v in (-5, -3, -2.5, -1, 0, 1, 5):
    chk(((sp.Integer(1) * _v + 2) ** 2) >= 0, "(x+2)^2 >= 0: x=%s" % _v)
# 差にするのは同値
chk(sp.simplify(sp.Eq(sp.Gt(x ** 2, 4 * x), sp.Gt(x ** 2 - 4 * x, 0))) is not None,
    "差にしても同値（形式）")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
eq(sp.factor(x ** 2 - x - 2), (x - 2) * (x + 1), "§2 因数分解")
chk(sorted(sp.solve(sp.Eq(x + 2, x ** 2), x)) == [-1, 2], "§2 交点")
solves(x + 2 >= x ** 2, I(-1, 2), "§2")
solves(x ** 2 - x - 2 <= 0, I(-1, 2), "§4")
eq(sp.factor(x ** 3 - 4 * x), x * (x - 2) * (x + 2), "§5 因数分解")
solves(x ** 3 >= 4 * x, U(I(-2, 0), I(2, oo)), "§5")
solves(x ** 2 >= 4 * x, U(I(-oo, 0), I(4, oo)), "§3 の例")
solves((x + 1) * (x - 2) ** 2 >= 0, I(-1, oo), "§6")
solves(1 / x > 2, I.open(0, sp.Rational(1, 2)), "§7")
eq(sp.together(1 / x - 2), (1 - 2 * x) / x, "§7 1 つの分数に")
# §5 の符号の表（4 区間の積の符号）
for _pt, _sgn in ((-3, -1), (-1, 1), (1, -1), (3, 1)):
    _v = (_pt) * (_pt - 2) * (_pt + 2)
    chk(sp.sign(_v) == _sgn, "§5 符号の表: x=%s" % _pt)
for _pt, _sgn in ((-3, -1), (-1, 1), (1, -1), (3, 1)):
    chk(sp.sign(sp.Integer(_pt) + 2) == (1 if _pt > -2 else -1),
        "§5 x+2 の符号: x=%s" % _pt)

# ══════════════════════════════════════════════════════════
# 2. 例題
# ══════════════════════════════════════════════════════════
eq(sp.factor(x ** 2 - 3 * x - 4), (x - 4) * (x + 1), "例題1 因数分解")
solves(x ** 2 - 3 * x - 4 <= 0, I(-1, 4), "例題1")
chk((x ** 2 - 3 * x - 4).subs(x, 0) == -4, "例題1 検算 x=0")
chk((x ** 2 - 3 * x - 4).subs(x, 5) == 6, "例題1 検算 x=5")
chk((x ** 2 - 3 * x - 4).subs(x, -2) == 6, "例題1 検算 x=-2")
eq(sp.factor(x ** 2 - 2 * x - 3), (x - 3) * (x + 1), "例題2 因数分解")
solves(2 * x + 3 > x ** 2, I.open(-1, 3), "例題2")
chk((2 * x + 3).subs(x, 3) == 9 and (x ** 2).subs(x, 3) == 9, "例題2 端では等しい")
_C = x ** 3 + 2 * x ** 2 - 5 * x - 6
chk(_C.subs(x, -1) == 0, "例題3 P(-1) = 0")
eq(sp.factor(_C), (x + 1) * (x + 3) * (x - 2), "例題3 因数分解")
eq(sp.expand((x + 1) * (x ** 2 + x - 6)), _C, "例題3 割り算の確かめ")
solves(_C >= 0, U(I(-3, -1), I(2, oo)), "例題3")
for _pt, _sgn in ((-4, -1), (-2, 1), (0, -1), (3, 1)):
    chk(sp.sign(_C.subs(x, _pt)) == _sgn, "例題3 符号: x=%s" % _pt)
chk(_C.subs(x, -2) == 4 and _C.subs(x, 0) == -6 and _C.subs(x, 3) == 24,
    "例題3 検算の値")
chk(sorted(sp.solve(sp.Eq(x ** 3, 4 * x), x)) == [-2, 0, 2], "例題4 (a) 交点")
solves(4 * x >= x ** 3, U(I(-oo, -2), I(0, 2)), "例題4 (b)")
for _pt, _val in ((-3, -15), (-1, 3), (1, -3), (3, 15)):
    chk((x * (x - 2) * (x + 2)).subs(x, _pt) == _val,
        "例題4 model-answer の値: x=%s" % _pt)
chk((4 * x).subs(x, -3) == -12 and (x ** 3).subs(x, -3) == -27, "例題4 検算 x=-3")
chk((4 * x).subs(x, 3) == 12 and (x ** 3).subs(x, 3) == 27, "例題4 検算 x=3")

# ══════════════════════════════════════════════════════════
# 3. 演習
# ══════════════════════════════════════════════════════════
eq(sp.factor(x ** 2 - 5 * x + 6), (x - 2) * (x - 3), "演習1 因数分解")
solves(x ** 2 - 5 * x + 6 < 0, I.open(2, 3), "演習1")
chk((x ** 2 - 5 * x + 6).subs(x, sp.Rational(5, 2)) == sp.Rational(-1, 4),
    "演習1 検算 x=2.5")
chk((x ** 2 - 5 * x + 6).subs(x, 4) == 2, "演習1 検算 x=4")
solves(x ** 2 >= 9, U(I(-oo, -3), I(3, oo)), "演習2")
chk((x ** 2).subs(x, -4) == 16, "演習2 検算 x=-4")
eq(sp.factor(x ** 2 + 2 * x - 8), (x + 4) * (x - 2), "演習3 因数分解")
solves(x ** 2 + 2 * x - 8 >= 0, U(I(-oo, -4), I(2, oo)), "演習3")
chk((x ** 2 + 2 * x - 8).subs(x, -5) == 7, "演習3 検算 x=-5")
solves(3 * x + 4 >= x ** 2, I(-1, 4), "演習4")
chk((3 * x + 4).subs(x, 4) == 16 and (x ** 2).subs(x, 4) == 16, "演習4 端で等号")
chk((3 * x + 4).subs(x, 5) == 19 and (x ** 2).subs(x, 5) == 25, "演習4 x=5 は外れる")
eq(sp.factor(x ** 3 - 4 * x ** 2 + 3 * x), x * (x - 1) * (x - 3), "演習5 因数分解")
solves(x ** 3 - 4 * x ** 2 + 3 * x < 0, U(I.open(-oo, 0), I.open(1, 3)), "演習5")
chk((x ** 3 - 4 * x ** 2 + 3 * x).subs(x, -1) == -8, "演習5 検算 x=-1")
chk((x ** 3 - 4 * x ** 2 + 3 * x).subs(x, 2) == -2, "演習5 検算 x=2")
chk((x ** 3 - 4 * x ** 2 + 3 * x).subs(x, 4) == 12, "演習5 検算 x=4")
solves((x - 1) * (x + 2) ** 2 <= 0, I(-oo, 1), "演習6")
chk(((x - 1) * (x + 2) ** 2).subs(x, -3) == -4, "演習6 検算 x=-3")
chk(((x - 1) * (x + 2) ** 2).subs(x, 0) == -4, "演習6 検算 x=0")
chk(((x - 1) * (x + 2) ** 2).subs(x, 2) == 16, "演習6 検算 x=2")
chk(((x - 1) * (x + 2) ** 2).subs(x, -2) == 0, "演習6 x=-2 で 0")
chk(sorted(sp.solve(sp.Eq(3 * x, x ** 2 - 4), x)) == [-1, 4], "演習7 交点")
solves(3 * x >= x ** 2 - 4, I(-1, 4), "演習7")
chk((3 * x).subs(x, 5) == 15 and (x ** 2 - 4).subs(x, 5) == 21, "演習7 検算 x=5")
eq(sp.factor(x ** 3 - x), x * (x - 1) * (x + 1), "演習8 因数分解")
solves(x ** 3 <= x, U(I(-oo, -1), I(0, 1)), "演習8")
chk((x ** 3).subs(x, -2) == -8, "演習8 検算 x=-2")
chk((x ** 3).subs(x, sp.Rational(1, 2)) == sp.Rational(1, 8), "演習8 検算 x=0.5")
solves(1 / x > 2, I.open(0, sp.Rational(1, 2)), "演習9")
chk((1 / x).subs(x, sp.Rational(1, 4)) == 4, "演習9 検算 x=1/4")
chk((1 / x).subs(x, -1) == -1, "演習9 検算 x=-1 は入らない")
chk(not ((1 / x).subs(x, -1) > 2), "演習9 x=-1 は満たさない")
solves(x ** 2 > 4, U(I.open(-oo, -2), I.open(2, oo)), "演習10")
chk((x ** 2).subs(x, -3) == 9, "演習10 x=-3 は満たす")
chk(not (sp.Integer(-3) > 2), "演習10 x=-3 は x>2 を満たさない")
eq(sp.factor(x ** 2 - 4), (x - 2) * (x + 2), "演習10 因数分解")

# ══════════════════════════════════════════════════════════
# 4. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Solutions of $g(x) \\geq f(x)$, both graphically and analytically.",
        "シラバス本体を逐語で")
in_text("> Graphical or algebraic methods for simple polynomials up to degree 3."
        " Use of technology for these and other functions.", "Guidance を逐語で")
in_text("## 公式集には、この項目の欄がありません", "公式集にないことを書く")
not_in_text("公式集の **2.15**", "ありもしない欄を書かない")
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
in_text("`menu` → `Analyze Graph` → `Intersection`", "TI-Nspire のメニュー")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl215-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl215", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
not_in_text("aahl-2-16.qmd", "まだ書いていないページへのリンクは張らない")
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
in_text("### 1. Working with the difference（不等式は「差」で考える） "
        "{#difference}", "見出し 1")
in_text("### 2. Solving graphically（グラフで解く） {#graphical}", "見出し 2")
in_text("### 3. Solving analytically: three steps（式で解く：$3$ つの手順） "
        "{#analytic}", "見出し 3")
in_text("### 4. Quadratic inequalities（$2$ 次の不等式） {#quadratic}", "見出し 4")
in_text("### 5. Cubic inequalities and sign diagrams（$3$ "
        "次の不等式と符号の表） {#cubic}", "見出し 5")
in_text("### 6. When there is a repeated root（重解があるとき） {#repeated}", "見出し 6")
in_text("### 7. Inequalities with a fraction: do not multiply "
        "through（分数を含むとき：両辺に掛けない） {#fractions}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 6. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-2-15-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-2-15-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("The answer is the stretch where one graph is above the other", "図(a) の題")
in_fig("the ends of the shaded stretch are the crossing points", "図(a) の要点")
in_fig("A sign diagram: multiply the signs down each column", "図(b) の題")
in_fig("product", "図(b) の行")
in_text("答えは、片方のグラフがもう片方より上にある区間です。", "キャプション (a)")
in_text("因数ごとの符号を縦にかけると、積の符号が出ます。", "キャプション (b)")
for leak in ["-3 \\leq x", "x \\leq 1", "1/2"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 7. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("x^{2}-5x+6", "演習1"), ("x^{2}+2x-8", "演習3"),
                    ("x^{3}-4x^{2}+3x", "演習5"),
                    ("(x-1)(x+2)^{2}", "演習6"), ("x^{3} \\leq x", "演習8")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 8. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/02-functions/aahl-2-15.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-2-14.qmd") < DRAFT.index("aahl-2-15.qmd"),
    "サイドバーの並びが 2.14 → 2.15")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aahl-2-15.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| inequality |", "| critical value |", "| sign diagram |",
          "| interval |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 9. 見張り
# ══════════════════════════════════════════════════════════
in_text("## 両辺を $x$ で割ってはいけません", "x で割らない")
in_text("**「またぐたびに符号が変わる」は、因数が $1$ 回のときの話です。**",
        "重解の見張り")
in_text("**分母が $0$ になる $x$ は、答えに入れません。**", "分母の見張り")
in_text("## 答えを点で書く", "範囲で書く")
in_text("**手で解くのは $3$ 次まで**です。", "Guidance の範囲")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
