"""AA HL HL 5.18b — Homogeneous equations and the integrating factor の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_18b.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-18b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_18b.py"), encoding="utf-8").read()
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



_x = sp.Symbol("x", positive=True)
_y = sp.Function("y")
_v = sp.Function("v")
R = sp.Rational


def solve(rhs, x0=None, y0=None):
    eq = sp.Eq(_y(_x).diff(_x), rhs)
    if x0 is None:
        return sp.dsolve(eq, _y(_x)).rhs
    return sp.dsolve(eq, _y(_x), ics={_y(x0): y0}).rhs


def back(sol, rhs):
    """解を代入して、もとの式が成り立つか。"""
    return sp.simplify(sp.diff(sol, _x) - rhs.subs(_y(_x), sol)) == 0


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_vv = sp.Symbol("vv")
# y = vx の微分
chk(sp.simplify(sp.diff(_v(_x) * _x, _x)
                - (_v(_x) + _x * sp.Derivative(_v(_x), _x))) == 0,
    "y = vx の微分は v + x dv/dx")
# 積分因子の条件 dI/dx = I P
_P = sp.Function("P")
_I = sp.exp(sp.Integral(_P(_x), _x))
chk(sp.simplify(sp.diff(_I, _x) - _I * _P(_x)) == 0, "dI/dx = I P")
# I をかけると 1 つの導関数になる
_yy = sp.Function("yy")
chk(sp.simplify(sp.diff(_I * _yy(_x), _x)
                - (_I * sp.Derivative(_yy(_x), _x)
                   + _I * _P(_x) * _yy(_x))) == 0,
    "d/dx(Iy) = I y' + I P y")
# 積分定数は消える
_C = sp.Symbol("C")
chk(sp.simplify(sp.exp(_C) / sp.exp(_C) - 1) == 0, "e^C は両辺で約分される")
# 同次形の判定
chk(sp.simplify((_x + _x * _vv) / _x - (1 + _vv)) == 0, "(x+y)/x = 1+y/x")
chk(sp.simplify((_x ** 2 + (_vv * _x) ** 2) / (_x * _vv * _x)
                - (1 / _vv + _vv)) == 0, "(x²+y²)/(xy) = 1/v + v")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(sp.simplify(solve((_x + _y(_x)) / _x, 1, 0) - _x * sp.log(_x)) == 0,
    "例題1 y = x ln x")
chk(back(_x * sp.log(_x), (_x + _y(_x)) / _x), "例題1 代入で成り立つ")
chk((_x * sp.log(_x)).subs(_x, 1) == 0, "例題1 初期条件")
# 例題2
_s2 = solve((_x ** 2 + _y(_x) ** 2) / (_x * _y(_x)), 1, 1)
chk(sp.simplify(_s2 ** 2 - _x ** 2 * (2 * sp.log(_x) + 1)) == 0,
    "例題2 y² = x²(2ln x + 1)")
chk(sp.simplify(_s2.subs(_x, 1) - 1) == 0, "例題2 初期条件")
# 例題3
_s3 = solve(sp.exp(-_x) - 2 * _y(_x), 0, 2)
chk(sp.simplify(_s3 - (sp.exp(-_x) + sp.exp(-2 * _x))) == 0,
    "例題3 y = e^{-x} + e^{-2x}")
chk(sp.simplify(sp.diff(_s3, _x) + 2 * _s3 - sp.exp(-_x)) == 0,
    "例題3 もとの式を満たす")
chk(_s3.subs(_x, 0) == 2, "例題3 初期条件")
chk(sp.simplify(sp.exp(sp.integrate(2, _x)) - sp.exp(2 * _x)) == 0,
    "例題3 I = e^{2x}")
# 例題4
_s4 = solve(_x ** 2 - _y(_x) / _x, 1, 1)
chk(sp.simplify(_s4 - (_x ** 3 / 4 + 3 / (4 * _x))) == 0,
    "例題4 y = x³/4 + 3/(4x)")
chk(sp.simplify(_x * sp.diff(_s4, _x) + _s4 - _x ** 3) == 0,
    "例題4 もとの式を満たす")
chk(_s4.subs(_x, 1) == 1, "例題4 初期条件")
chk(sp.simplify(sp.exp(sp.integrate(1 / _x, _x)) - _x) == 0, "例題4 I = x")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(sp.simplify((2 * _x + 3 * _vv * _x) / _x - (2 + 3 * _vv)) == 0,
    "演習1 2 + 3(y/x)")
# 演習2
_q2 = solve((_y(_x) - _x) / _x, 1, 2)
chk(sp.simplify(_q2 - _x * (2 - sp.log(_x))) == 0, "演習2 y = x(2 - ln x)")
chk(back(_x * (2 - sp.log(_x)), (_y(_x) - _x) / _x), "演習2 代入で成り立つ")
chk(_q2.subs(_x, 1) == 2, "演習2 初期条件")
# 演習3
_q3 = solve(_y(_x) / _x + (_y(_x) / _x) ** 2, 1, 1)
chk(sp.simplify(_q3 - _x / (1 - sp.log(_x))) == 0, "演習3 y = x/(1-ln x)")
chk(_q3.subs(_x, 1) == 1, "演習3 初期条件")
chk(sp.solve(sp.Eq(1 - sp.log(_x), 0), _x) == [sp.E], "演習3 x=e で分母が 0")
# 演習4
chk(sp.simplify(sp.exp(sp.integrate(3, _x)) - sp.exp(3 * _x)) == 0,
    "演習4 I = e^{3x}")
chk(sp.simplify(sp.diff(sp.exp(3 * _x), _x) - 3 * sp.exp(3 * _x)) == 0,
    "演習4 dI/dx = 3I")
# 演習5
chk(sp.simplify(sp.exp(sp.integrate(2 / _x, _x)) - _x ** 2) == 0,
    "演習5 I = x²")
chk(sp.simplify(sp.diff(_x ** 2, _x) - _x ** 2 * (2 / _x)) == 0,
    "演習5 dI/dx = I P")
# 演習6
_q6 = solve(2 - _y(_x), 0, 5)
chk(sp.simplify(_q6 - (2 + 3 * sp.exp(-_x))) == 0, "演習6 y = 2 + 3e^{-x}")
chk(_q6.subs(_x, 0) == 5, "演習6 初期条件")
chk(sp.limit(_q6, _x, sp.oo) == 2, "演習6 x→∞ で 2")
# 演習7
_q7 = solve(_x - 2 * _x * _y(_x))
chk(sp.simplify(sp.diff(_q7, _x) + 2 * _x * _q7 - _x) == 0,
    "演習7 一般解が式を満たす")
chk(sp.simplify(sp.exp(sp.integrate(2 * _x, _x)) - sp.exp(_x ** 2)) == 0,
    "演習7 I = e^{x²}")
chk(sp.simplify(sp.integrate(_x * sp.exp(_x ** 2), _x)
                - sp.exp(_x ** 2) / 2) == 0, "演習7 右辺の積分")
# 演習8
_q8 = solve(_x - _y(_x) / _x)
chk(sp.simplify(_x * sp.diff(_q8, _x) + _q8 - _x ** 2) == 0,
    "演習8 一般解が式を満たす")
chk(sp.simplify(sp.exp(sp.integrate(1 / _x, _x)) - _x) == 0, "演習8 I = x")
# 演習9
chk(sp.simplify((1 + _vv) - _vv - 1) == 0, "演習9 例題1 では f(v)-v = 1")
chk(sp.simplify((1 / _vv + _vv) - _vv - 1 / _vv) == 0,
    "演習9 例題2 では f(v)-v = 1/v")
# 演習10
chk(sp.simplify(sp.exp(sp.integrate(2, _x)) - sp.exp(2 * _x)) == 0,
    "演習10 正しい I は e^{2x}")
chk(sp.simplify(sp.diff(sp.exp(4 * _x) * _yy(_x), _x)
                - (sp.exp(4 * _x) * sp.Derivative(_yy(_x), _x)
                   + 4 * sp.exp(4 * _x) * _yy(_x))) == 0,
    "演習10 e^{4x} だと係数が 4 になる")
chk(2 != 4, "演習10 標準形の P は 2")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Homogeneous differential equation $\\dfrac{\\mathrm{d}y}"
        "{\\mathrm{d}x} = f\\!\\left(\\dfrac{y}{x}\\right)$ using the"
        " substitution $y = vx$.", "同次形を逐語で")
in_text("> Solution of $y' + P(x)y = Q(x)$, using the integrating factor.",
        "積分因子を逐語で")
in_text("公式集の **5.18** の欄", "公式集の場所")
in_text("> Integrating factor for $y'+P(x)y = Q(x)$",
        "公式集の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("which method for a first order equation?", "図(a) の題")
in_fig("check them in this order", "図(a) の注")
in_fig("solutions of a linear equation", "図(b) の題")
in_fig("the term with $C$ dies away", "図(b) の注")
in_text("$3$ つの形を、この順に確かめます。", "キャプション (a)")
in_text("がちがっても、同じ曲線に近づきます。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("2 - \\log", "演習2"), ("1-\\ln x", "演習3")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl518b-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl518b", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-5-18b-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-18b-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/05-calculus/aahl-5-18b.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-18b.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| homogeneous |", "| integrating factor |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## $y = vx$ を微分するときに $v$ の項を落とす", "v の項")
in_text("## 標準形に直す前に $P$ を読む", "標準形が先")
in_text("## 積分因子に積分定数を付ける", "定数は不要")
in_text("## まず、この形に直します", "係数を 1 に")
in_text("**上から順に試す**のが確実です。", "順に試す")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
