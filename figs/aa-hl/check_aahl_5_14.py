"""AA HL HL 5.14 — Implicit differentiation, related rates and optimisation の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_14.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-14.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_14.py"), encoding="utf-8").read()
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



_x = sp.Symbol("x")
_y = sp.Function("y")(_x)
_t = sp.Symbol("t", positive=True)
R = sp.Rational


def imp(F):
    """F(x, y) = 0 から dy/dx を求める。"""
    return sp.simplify(sp.solve(sp.Eq(sp.diff(F, _x), 0),
                                sp.Derivative(_y, _x))[0])


def at(expr, a, b):
    return sp.simplify(expr.subs({_x: a, _y: b}))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_n = sp.Symbol("n", positive=True, integer=True)
# d/dx(y^n) = n y^{n-1} dy/dx
chk(sp.simplify(sp.diff(_y ** 3, _x)
                - 3 * _y ** 2 * sp.Derivative(_y, _x)) == 0,
    "d/dx(y³) = 3y² dy/dx")
# 積の微分
chk(sp.simplify(sp.diff(_x * _y, _x)
                - (_y + _x * sp.Derivative(_y, _x))) == 0,
    "d/dx(xy) = y + x dy/dx")
# 円は一般の半径でも同じ形
_r = sp.Symbol("r", positive=True)
chk(sp.simplify(imp(_x ** 2 + _y ** 2 - _r ** 2) + _x / _y) == 0,
    "x²+y²=r² なら dy/dx = -x/y")
# 接線と半径は垂直
_a, _b = sp.symbols("a b", positive=True)
chk(sp.simplify((-_a / _b) * (_b / _a) + 1) == 0, "傾きの積は -1")
# 解いてから微分しても同じ（xy = 6）
chk(sp.simplify(sp.diff(6 / _x, _x) + 6 / _x ** 2) == 0, "y=6/x の微分")
chk(sp.simplify((-(6 / _x) / _x) - (-6 / _x ** 2)) == 0, "-y/x と一致")
# 連鎖律（関連する変化率）
_V = sp.Function("V")
_rt = sp.Function("r")(_t)
chk(sp.simplify(sp.diff(R(4, 3) * sp.pi * _rt ** 3, _t)
                - 4 * sp.pi * _rt ** 2 * sp.Derivative(_rt, _t)) == 0,
    "dV/dt = 4πr² dr/dt")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_C1 = _x ** 2 + _y ** 2 - 25
chk(sp.simplify(imp(_C1) + _x / _y) == 0, "例題1 dy/dx = -x/y")
chk(at(imp(_C1), 3, 4) == R(-3, 4), "例題1 (3,4) で -3/4")
chk(3 ** 2 + 4 ** 2 == 25, "例題1 点は円の上")
chk(sp.simplify(R(-3, 4) * R(4, 3) + 1) == 0, "例題1 半径と垂直")
# 例題2
_C2 = _x ** 2 + _x * _y + _y ** 2 - 3
chk(sp.simplify(imp(_C2) + (2 * _x + _y) / (_x + 2 * _y)) == 0,
    "例題2 dy/dx = -(2x+y)/(x+2y)")
chk(at(imp(_C2), 1, 1) == -1, "例題2 (1,1) で -1")
chk(1 + 1 + 1 == 3, "例題2 点は曲線の上")
# 例題3
_rs = sp.Symbol("rs", positive=True)
chk(sp.diff(R(4, 3) * sp.pi * _rs ** 3, _rs) == 4 * sp.pi * _rs ** 2,
    "例題3 dV/dr = 4πr²")
chk((4 * sp.pi * _rs ** 2).subs(_rs, 5) == 100 * sp.pi, "例題3 r=5 で 100π")
chk(sp.simplify(sp.Integer(100) / (100 * sp.pi) - 1 / sp.pi) == 0,
    "例題3 dr/dt = 1/π")
chk(sp.N(1 / sp.pi, 4) < R(1, 2), "例題3 0.32 くらい")
# 例題4
_X = sp.Symbol("X")
_A = _X ** 2 / (4 * sp.pi) + (20 - _X) ** 2 / 16
_crit = sp.solve(sp.diff(_A, _X), _X)
chk(_crit == [20 * sp.pi / (sp.pi + 4)], "例題4 停留点は 20π/(π+4)")
chk(sp.simplify(sp.diff(_A, _X, 2) - (R(1, 2) / sp.pi + R(1, 8))) == 0,
    "例題4 A'' は定数で正")
chk(sp.diff(_A, _X, 2) > 0, "例題4 だから最小")
chk(_A.subs(_X, 0) == 25, "例題4 A(0) = 25")
chk(sp.simplify(_A.subs(_X, 20) - 100 / sp.pi) == 0, "例題4 A(20) = 100/π")
chk(sp.N(100 / sp.pi, 5) > 25, "例題4 A(20) のほうが大きい")
chk(sp.N(_A.subs(_X, _crit[0]), 5) < 25, "例題4 停留点の値はいちばん小さい")
chk(sp.N(_crit[0], 4) > 8 and sp.N(_crit[0], 4) < 9, "例題4 停留点は 8.8 くらい")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(sp.simplify(imp(_x ** 2 + _y ** 2 - 16) + _x / _y) == 0, "演習1 -x/y")
chk(at(imp(_x ** 2 + _y ** 2 - 16), 0, 4) == 0, "演習1 (0,4) で 0")
# 演習2
chk(sp.simplify(imp(_x ** 3 + _y ** 3 - 9) + _x ** 2 / _y ** 2) == 0,
    "演習2 -x²/y²")
chk(1 ** 3 + 2 ** 3 == 9, "演習2 (1,2) は曲線の上")
chk(at(imp(_x ** 3 + _y ** 3 - 9), 1, 2) == R(-1, 4), "演習2 (1,2) で -1/4")
# 演習3
chk(sp.simplify(imp(_x * _y - 6) + _y / _x) == 0, "演習3 -y/x")
chk(at(imp(_x * _y - 6), 2, 3) == R(-3, 2), "演習3 (2,3) で -3/2")
# 演習4
_C4 = _x ** 2 + 2 * _x * _y + 3 * _y ** 2 - 6
chk(sp.simplify(imp(_C4) + (_x + _y) / (_x + 3 * _y)) == 0,
    "演習4 -(x+y)/(x+3y)")
chk(at(imp(_C4), 1, 1) == R(-1, 2), "演習4 (1,1) で -1/2")
chk(1 + 2 + 3 == 6, "演習4 点は曲線の上")
# 演習5
chk(at(imp(_C1), 4, 3) == R(-4, 3), "演習5 (4,3) で -4/3")
chk(4 ** 2 + 3 ** 2 == 25, "演習5 点は円の上")
chk(sp.simplify(4 * 4 + 3 * 3 - 25) == 0, "演習5 4x+3y=25 を通る")
chk(sp.simplify(sp.Rational(-4, 3) * sp.Rational(3, 4) + 1) == 0,
    "演習5 半径と垂直")
# 演習6
_s = sp.Symbol("s", positive=True)
chk(sp.diff(_s ** 2, _s) == 2 * _s, "演習6 dA/ds = 2s")
chk(2 * 10 * 2 == 40, "演習6 40 cm²/s")
chk(sp.Rational(10201, 100) - 100 == sp.Rational(201, 100),
    "演習6 10.1 cm なら 102.01")
# 演習7
_xf = sp.Function("xf")(_t)
_yf = sp.Function("yf")(_t)
chk(sp.simplify(sp.diff(_xf ** 2 + _yf ** 2, _t)
                - (2 * _xf * sp.Derivative(_xf, _t)
                   + 2 * _yf * sp.Derivative(_yf, _t))) == 0,
    "演習7 両辺を t で微分")
chk(3 ** 2 + 4 ** 2 == 25, "演習7 x=3 なら y=4")
chk(sp.solve(sp.Eq(2 * 3 * R(1, 2) + 2 * 4 * sp.Symbol("dy"), 0),
             sp.Symbol("dy")) == [R(-3, 8)], "演習7 dy/dt = -3/8")
chk(R(-3, 8) < 0, "演習7 上端は下がる")
# 演習8
chk(sp.simplify(imp(_x ** 2 + _y ** 2 - _r ** 2) + _x / _y) == 0,
    "演習8 一般の半径でも -x/y")
chk(sp.simplify((-_a / _b) * (_b / _a) + 1) == 0, "演習8 積は -1")
chk(sp.simplify(R(-3, 4) * R(4, 3) + 1) == 0, "演習8 (3,4) の例")
# 演習9
chk(sp.diff(_x, _x) == 1, "演習9 f(x)=x の導関数は 1")
chk(sp.solve(sp.diff(_x, _x), _x) == [], "演習9 停留点がない")
_g = _x ** 3 - 3 * _x
chk(sp.solve(sp.diff(_g, _x), _x) == [-1, 1], "演習9 x³-3x の停留点")
chk(_g.subs(_x, 1) == -2 and _g.subs(_x, 3) == 18 and _g.subs(_x, 0) == 0,
    "演習9 [0,3] では x=3 が最大、x=1 が最小")
chk(18 > 0 > -2, "演習9 端のほうが大きい")
# 演習10
chk(sp.simplify(imp(_C1) + _x / _y) == 0, "演習10 正しい答え")
chk(sp.solve(sp.Eq(2 * _x + 2 * sp.Symbol("Y"), 0), sp.Symbol("Y"))
    == [-_x], "演習10 生徒の式は y = -x")

# ══════════════════════════════════════════════════════════
# 3. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Implicit differentiation.", "シラバス 1 行目を逐語で")
in_text("> Appropriate use of the chain rule or implicit differentiation,"
        " including cases where the optimum solution is at the end point.",
        "Guidance を逐語で")
in_text("> Optimisation problems.", "最適化を逐語で")
in_text("> including cases where the optimum solution is at the end point",
        "端点の一文を逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("a circle is not the graph of one function", "図(a) の題")
in_fig("one value of $x$ can give", "図(a) の注")
in_fig("related rates:", "図(b) の題")
in_fig("holds at every moment", "図(b) の注")
in_text("円は $1$ つの関数のグラフではありませんが、各点に接線があります。",
        "キャプション (a)")
in_text("は、はしごの長さで結ばれています。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("4x+3y = 25", "演習5"), ("\\frac{3}{8}", "演習7")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))

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
chk(len(re.findall(r"^::: \{#exm-aahl514-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl514", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-5-14-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-14-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/05-calculus/aahl-5-14.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-14.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| implicit |", "| related rates |", "| optimization |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## $y$ の項を微分するときに $\\dfrac{\\mathrm{d}y}{\\mathrm{d}x}$ を忘れる",
        "dy/dx を忘れない")
in_text("## 微分する前に数を代入する", "代入は最後")
in_text("## 端点を調べない", "端点も調べる")
in_text("## 値を代入するのは、微分したあとです", "順番")
in_text("**調べるべき点は $3$ 種類**です。", "3 種類の候補")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
