"""AA HL 3.9（相反三角関数と逆三角関数） の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_9.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-9.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_9.py"), encoding="utf-8").read()
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

th = sp.Symbol("theta")
x = sp.Symbol("x", real=True)
PI = sp.pi
SEC, CSC, COT = sp.sec, sp.csc, sp.cot


def zero(e, msg):
    chk(sp.simplify(e) == 0, msg + "  (%s)" % e)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの恒等式
# ══════════════════════════════════════════════════════════
zero(1 + sp.tan(th) ** 2 - SEC(th) ** 2, "1+tan^2 = sec^2")
zero(1 + COT(th) ** 2 - CSC(th) ** 2, "1+cot^2 = cosec^2")
zero(SEC(th) - 1 / sp.cos(th), "sec = 1/cos")
zero(CSC(th) - 1 / sp.sin(th), "cosec = 1/sin")
zero(COT(th) - sp.cos(th) / sp.sin(th), "cot = cos/sin")
zero(COT(th) - 1 / sp.tan(th), "cot = 1/tan")
# 割って出すところ
zero(sp.expand((sp.cos(th) ** 2 + sp.sin(th) ** 2) / sp.cos(th) ** 2)
     - (1 + sp.tan(th) ** 2), "cos^2 で割ると 1+tan^2")
zero(sp.expand((sp.cos(th) ** 2 + sp.sin(th) ** 2) / sp.sin(th) ** 2)
     - (COT(th) ** 2 + 1), "sin^2 で割ると cot^2+1")
# |sec| >= 1
for _v in (sp.Rational(1, 6), sp.Rational(2, 5), 1, 2, 3):
    chk(abs(sp.sec(_v).evalf()) >= 1, "|sec| >= 1: θ=%s" % _v)
    chk(abs(sp.csc(_v).evalf()) >= 1, "|cosec| >= 1: θ=%s" % _v)
# 定義されない角
for _k in range(-2, 3):
    chk(sp.cos(PI / 2 + _k * PI) == 0, "sec が定義されない: k=%d" % _k)
    chk(sp.sin(_k * PI) == 0, "cosec と cot が定義されない: k=%d" % _k)
# 逆関数の domain・range
chk(sp.asin(-1) == -PI / 2 and sp.asin(1) == PI / 2, "arcsin の range の端")
chk(sp.acos(-1) == PI and sp.acos(1) == 0, "arccos の range の端")
chk(sp.limit(sp.atan(x), x, sp.oo) == PI / 2
    and sp.limit(sp.atan(x), x, -sp.oo) == -PI / 2, "arctan の漸近線")
for _v in (sp.Rational(-9, 10), 0, sp.Rational(1, 2), 1):
    chk(-PI / 2 <= sp.asin(_v) <= PI / 2, "arcsin の値は range の中: %s" % _v)
    chk(0 <= sp.acos(_v) <= PI, "arccos の値は range の中: %s" % _v)
    chk(abs(complex((sp.asin(_v) + sp.acos(_v) - PI / 2).evalf())) < 1e-12,
        "arcsin+arccos = π/2: x=%s" % _v)
chk(sp.solveset(sp.Eq(sp.sin(x), 2), x, sp.S.Reals) == sp.EmptySet,
    "sin θ = 2 に解はない")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
chk(sp.Rational(1, 1) / sp.Rational(3, 5) == sp.Rational(5, 3), "例題1 sec")
chk(1 - sp.Rational(9, 25) == sp.Rational(16, 25), "例題1 sin^2")
chk(sp.Rational(1, 1) / sp.Rational(4, 5) == sp.Rational(5, 4), "例題1 cosec")
chk(sp.Rational(3, 5) / sp.Rational(4, 5) == sp.Rational(3, 4), "例題1 cot")
chk(1 + sp.Rational(4, 3) ** 2 == sp.Rational(25, 9)
    and sp.Rational(5, 3) ** 2 == sp.Rational(25, 9), "例題1 検算")
zero(SEC(th) ** 2 + CSC(th) ** 2 - SEC(th) ** 2 * CSC(th) ** 2, "例題2")
zero(1 / sp.cos(th) ** 2 + 1 / sp.sin(th) ** 2
     - 1 / (sp.sin(th) ** 2 * sp.cos(th) ** 2), "例題2 通分")
chk(sp.sec(PI / 4) ** 2 == 2 and sp.csc(PI / 4) ** 2 == 2, "例題2 検算 π/4")
chk(sp.nsimplify(sp.sec(PI / 6) ** 2) == sp.Rational(4, 3), "例題2 検算 π/6 sec")
chk(sp.nsimplify(sp.csc(PI / 6) ** 2) == 4, "例題2 検算 π/6 cosec")
chk(sp.Rational(4, 3) + 4 == sp.Rational(16, 3)
    and sp.Rational(4, 3) * 4 == sp.Rational(16, 3), "例題2 検算 π/6 両辺")
chk(sp.solveset(sp.Eq(SEC(th) ** 2, 2 * sp.tan(th)), th,
                sp.Interval(0, 2 * PI)) == sp.FiniteSet(PI / 4, 5 * PI / 4),
    "例題3 の解")
eq(sp.expand((sp.tan(th) - 1) ** 2),
   sp.tan(th) ** 2 - 2 * sp.tan(th) + 1, "例題3 因数分解")
chk(sp.sec(PI / 4) ** 2 == 2 and 2 * sp.tan(PI / 4) == 2, "例題3 検算 π/4")
chk(sp.sec(5 * PI / 4) ** 2 == 2 and sp.tan(5 * PI / 4) == 1, "例題3 検算 5π/4")
chk(sp.asin(sp.Rational(-1, 2)) == -PI / 6, "例題4 arcsin(-1/2)")
chk(sp.acos(sp.Rational(-1, 2)) == 2 * PI / 3, "例題4 arccos(-1/2)")
chk(-PI / 6 + 2 * PI / 3 == PI / 2, "例題4 和は π/2")
chk(sp.sin(3 * PI / 4) == sp.sqrt(2) / 2, "例題4 sin(3π/4)")
chk(sp.asin(sp.sqrt(2) / 2) == PI / 4, "例題4 arcsin は π/4")
chk(sp.asin(sp.sin(3 * PI / 4)) == PI / 4, "例題4 3π/4 には戻らない")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(1 - sp.Rational(25, 169) == sp.Rational(144, 169), "演習1 cos^2")
chk(sp.Rational(1, 1) / sp.Rational(5, 13) == sp.Rational(13, 5), "演習1 cosec")
chk(sp.Rational(1, 1) / sp.Rational(12, 13) == sp.Rational(13, 12), "演習1 sec")
chk(sp.Rational(12, 13) / sp.Rational(5, 13) == sp.Rational(12, 5), "演習1 cot")
chk(1 + sp.Rational(12, 5) ** 2 == sp.Rational(169, 25), "演習1 検算")
chk(5 ** 2 + 12 ** 2 == 13 ** 2, "演習1 三平方")
zero(COT(th) ** 2 - sp.cos(th) ** 2 - COT(th) ** 2 * sp.cos(th) ** 2, "演習2")
chk(sp.nsimplify(sp.cot(PI / 4) ** 2) == 1
    and sp.cos(PI / 4) ** 2 == sp.Rational(1, 2), "演習2 検算 π/4")
chk(sp.nsimplify(sp.cot(PI / 3) ** 2) == sp.Rational(1, 3)
    and sp.cos(PI / 3) ** 2 == sp.Rational(1, 4), "演習2 検算 π/3")
chk(sp.Rational(1, 3) - sp.Rational(1, 4) == sp.Rational(1, 12)
    and sp.Rational(1, 3) * sp.Rational(1, 4) == sp.Rational(1, 12),
    "演習2 検算 両辺")
chk(sp.solveset(sp.Eq(sp.tan(th) ** 2, SEC(th) + 1), th,
                sp.Interval(0, 2 * PI))
    == sp.FiniteSet(PI / 3, PI, 5 * PI / 3), "演習3 の解")
eq(sp.expand((sp.Symbol("s") - 2) * (sp.Symbol("s") + 1)),
   sp.Symbol("s") ** 2 - sp.Symbol("s") - 2, "演習3 因数分解")
chk(sp.tan(PI / 3) ** 2 == 3 and sp.sec(PI / 3) + 1 == 3, "演習3 検算 π/3")
chk(sp.tan(PI) == 0 and sp.sec(PI) + 1 == 0, "演習3 検算 π")
chk(sp.solveset(sp.Eq(SEC(th) ** 2, 4), th, sp.Interval(0, 2 * PI))
    == sp.FiniteSet(PI / 3, 2 * PI / 3, 4 * PI / 3, 5 * PI / 3), "演習4 の解")
chk(sp.cos(2 * PI / 3) == sp.Rational(-1, 2), "演習4 検算 2π/3")
chk(sp.atan(sp.sqrt(3)) == PI / 3, "演習6 (a)")
chk(sp.acos(-sp.sqrt(2) / 2) == 3 * PI / 4, "演習6 (b)")
chk(sp.sin(5 * PI / 6) == sp.Rational(1, 2), "演習6 (c) sin")
chk(sp.asin(sp.sin(5 * PI / 6)) == PI / 6, "演習6 (c)")
chk(sp.asin(0) == 0 and sp.acos(0) == PI / 2, "演習7 検算 x=0")
chk(sp.asin(1) == PI / 2 and sp.acos(1) == 0, "演習7 検算 x=1")
zero(sp.cos(PI / 2 - sp.Symbol("alpha")) - sp.sin(sp.Symbol("alpha")),
     "演習7 cos(π/2-α) = sin α")
chk(sp.solveset(sp.Eq(3 * COT(th) ** 2, 1), th, sp.Interval.open(0, PI))
    == sp.FiniteSet(PI / 3, 2 * PI / 3), "演習9 の解")
chk(sp.nsimplify(sp.cot(2 * PI / 3) ** 2) == sp.Rational(1, 3), "演習9 検算")
chk(sp.sec(PI / 3) == 2, "演習10 sec(π/3) = 2")
chk(sp.solveset(sp.Eq(sp.cos(x), 2), x, sp.S.Reals) == sp.EmptySet,
    "演習10 cos θ = 2 に解はない")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Definition of the reciprocal trigonometric ratios $\\sec\\theta$,"
        " $\\operatorname{cosec}\\theta$ and $\\cot\\theta$.",
        "シラバス（定義）を逐語で")
in_text("> Pythagorean identities:", "シラバス（恒等式）を逐語で")
in_text("> $1 + \\tan^{2}\\theta = \\sec^{2}\\theta$", "1+tan^2 を逐語で")
in_text("> $1 + \\cot^{2}\\theta = \\operatorname{cosec}^{2}\\theta$",
        "1+cot^2 を逐語で")
in_text("> The inverse functions $f(x) = \\arcsin x$, $f(x) = \\arccos x$,"
        " $f(x) = \\arctan x$; their domains and ranges; their graphs.",
        "シラバス（逆関数）を逐語で")
in_text("公式集の **3.9** の欄", "公式集の場所")
in_text("> Reciprocal trigonometric identities", "公式集の見出しを逐語で")
in_text("> $\\sec\\theta = \\dfrac{1}{\\cos\\theta}$", "公式集の sec")
in_text("> $\\operatorname{cosec}\\theta = \\dfrac{1}{\\sin\\theta}$", "公式集の cosec")
in_text("**$\\cot\\theta$ は書かれていません。**", "cot は公式集にない")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("Where $\\\\cos x$ is zero, $\\\\sec x$ has an asymptote", "図(a) の題")
in_fig("never enters the strip", "図(a) の要点")
in_fig("The range is cut so that each input gives one output", "図(b) の題")
in_fig("$y=\\\\arctan x$", "図(b) の 3 枚目")
in_text("$\\cos x$ が $0$ になるところが、$\\sec x$ の漸近線です。", "キャプション (a)")
in_text("どの入力にも出力が $1$ つになるように、値域を切ってあります。",
        "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("13}{5", "演習1"), ("\\sec\\theta + 1", "演習3"),
                    ("\\sec^{2}\\theta = 4", "演習4"),
                    ("\\arctan\\sqrt{3}", "演習6"),
                    ("3\\cot^{2}\\theta", "演習9")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))

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
chk(len(re.findall(r"^::: \{#exm-aahl39-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl39", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-9-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-9-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-9.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-9.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| secant ($\\sec$) |", "| cosecant ($\\operatorname{cosec}$) |",
          "| cotangent ($\\cot$) |", "| inverse trigonometric function |",
          "| principal value |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 公式集にあるのは、$2$ つだけです", "cot が公式集にないことの見張り")
in_text("## $\\tan$ と $\\sec$ は組、$\\cot$ と $\\operatorname{cosec}$ は組", "組の見張り")
in_text("## $\\arcsin\\left(\\sin\\theta\\right)$ は、いつも $\\theta$ に戻るわけではありません",
        "戻らない場合の見張り")
in_text("**$\\lvert \\sec\\theta \\rvert \\geq 1$ と"
        " $\\lvert \\operatorname{cosec}\\theta \\rvert \\geq 1$ が、いつも成り立ちます。**",
        "大きさの見張り")
in_text("**端が入りません。**", "arctan の端")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
