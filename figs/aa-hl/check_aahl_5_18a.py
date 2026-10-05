"""AA HL HL 5.18a — Euler's method and separation of variables の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_18a.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-18a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_18a.py"), encoding="utf-8").read()
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
_t = sp.Symbol("t")
_y = sp.Function("y")
_N = sp.Function("N")
R = sp.Rational


def euler(f, x0, y0, h, n):
    out = [(x0, y0)]
    for _ in range(n):
        y0 = y0 + h * f(x0, y0)
        x0 = x0 + h
        out.append((x0, y0))
    return out


def solve(rhs, x0, y0, fn=None, var=None):
    fn = fn or _y
    var = var or _x
    return sp.dsolve(sp.Eq(fn(var).diff(var), rhs), fn(var),
                     ics={fn(x0): y0}).rhs


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a, _k, _n = sp.symbols("a k n", positive=True)
# ロジスティックの部分分数
chk(sp.simplify(1 / (_n * (_a - _n))
                - (1 / _a) * (1 / _n + 1 / (_a - _n))) == 0,
    "ロジスティックの部分分数")
# 1/(a-n) の積分にマイナス
chk(sp.simplify(sp.diff(-sp.log(_a - _n), _n) - 1 / (_a - _n)) == 0,
    "∫1/(a-n)dn = -ln(a-n)")
# 右辺は n = a/2 で最大
chk(sp.solve(sp.diff(_k * _n * (_a - _n), _n), _n) == [_a / 2],
    "増え方が最大なのは n = a/2")
# x+y は積の形に分けられない
chk(sp.simplify(sp.factor(_x + sp.Symbol("yy"))) == _x + sp.Symbol("yy"),
    "x+y は因数分解できない")
# Euler は接線による近似
_hh = sp.Symbol("hh", positive=True)
chk(sp.series(sp.exp(_hh), _hh, 0, 2).removeO() == 1 + _hh,
    "接線近似は 1 次まで")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_e1 = euler(lambda a, b: a + b, R(0), R(1), R(1, 10), 3)
chk(_e1[1][1] == R(11, 10), "例題1 y1 = 1.1")
chk(_e1[2][1] == R(61, 50), "例題1 y2 = 1.22")
chk(_e1[3][1] == R(681, 500), "例題1 y3 = 1.362")
chk(R(681, 500) == R(1362, 1000), "例題1 1.362")
chk(_e1[3][0] == R(3, 10), "例題1 x = 0.3 に着く")
# 例題2
chk(sp.simplify(solve(_x * _y(_x), 0, 2) - 2 * sp.exp(_x ** 2 / 2)) == 0,
    "例題2 y = 2e^{x²/2}")
chk(sp.simplify(sp.diff(2 * sp.exp(_x ** 2 / 2), _x)
                - _x * 2 * sp.exp(_x ** 2 / 2)) == 0, "例題2 微分でもどる")
chk((2 * sp.exp(_x ** 2 / 2)).subs(_x, 0) == 2, "例題2 初期条件")
# 例題3
chk(sp.simplify(solve(2 * _x * _y(_x) ** 2, 0, 1)
                - 1 / (1 - _x ** 2)) == 0, "例題3 y = 1/(1-x²)")
chk(sp.simplify(sp.diff(1 / (1 - _x ** 2), _x)
                - 2 * _x * (1 / (1 - _x ** 2)) ** 2) == 0,
    "例題3 微分でもどる")
chk((1 / (1 - _x ** 2)).subs(_x, 0) == 1, "例題3 初期条件")
# 例題4
_sol4 = sp.dsolve(sp.Eq(_N(_t).diff(_t), R(1, 10) * _N(_t) * (100 - _N(_t))),
                  _N(_t), ics={_N(0): 10}).rhs
chk(sp.simplify(_sol4 - 100 / (1 + 9 * sp.exp(-10 * _t))) == 0,
    "例題4 N = 100/(1+9e^{-10t})")
chk(_sol4.subs(_t, 0) == 10, "例題4 t=0 で 10")
chk(sp.limit(_sol4, _t, sp.oo) == 100, "例題4 t→∞ で 100")
chk(sp.simplify(sp.log(R(10, 90)) - sp.log(R(1, 9))) == 0,
    "例題4 C' = ln(1/9)")
chk(sp.simplify(1 / (sp.Symbol("NN") * (100 - sp.Symbol("NN")))
                - R(1, 100) * (1 / sp.Symbol("NN")
                               + 1 / (100 - sp.Symbol("NN")))) == 0,
    "例題4 部分分数（a = 100）")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
_q1 = euler(lambda a, b: a + b, R(0), R(1), R(1, 5), 2)
chk(_q1[1][1] == R(6, 5), "演習1 y1 = 1.2")
chk(_q1[2][1] == R(37, 25), "演習1 y2 = 1.48")
chk(_q1[2][0] == R(2, 5), "演習1 x = 0.4 に着く")
_q2 = euler(lambda a, b: b - a, R(0), R(2), R(1, 10), 2)
chk(_q2[1][1] == R(11, 5), "演習2 y1 = 2.2")
chk(_q2[2][1] == R(241, 100), "演習2 y2 = 2.41")
chk(sp.simplify(solve(3 * _x ** 2 * _y(_x), 0, 1)
                - sp.exp(_x ** 3)) == 0, "演習3 y = e^{x³}")
chk(sp.simplify(sp.diff(sp.exp(_x ** 3), _x)
                - 3 * _x ** 2 * sp.exp(_x ** 3)) == 0, "演習3 微分でもどる")
chk(sp.simplify(solve(_y(_x) / _x, 1, 2) - 2 * _x) == 0, "演習4 y = 2x")
chk(sp.simplify((2 * _x) / _x - 2) == 0, "演習4 y/x = 2")
chk(sp.simplify(solve(1 + _y(_x) ** 2, 0, 0) - sp.tan(_x)) == 0,
    "演習5 y = tan x")
chk(sp.simplify(sp.diff(sp.tan(_x), _x) - (1 + sp.tan(_x) ** 2)) == 0,
    "演習5 微分でもどる")
chk(sp.simplify(sp.exp(_x - _x) - 1) == 0, "演習6 y=x なら e^0 = 1")
chk(sp.diff(_x, _x) == 1, "演習6 y=x の微分は 1")
_A = sp.Symbol("A")
chk(sp.simplify(sp.diff(sp.sqrt(_x ** 2 + _A), _x)
                - _x / sp.sqrt(_x ** 2 + _A)) == 0, "演習7 y²=x²+A の検算")
_q8 = sp.dsolve(sp.Eq(_y(_x).diff(_x), _y(_x) * (1 - _y(_x))), _y(_x),
                ics={_y(0): R(1, 2)}).rhs
chk(sp.simplify(_q8 - 1 / (1 + sp.exp(-_x))) == 0, "演習8 y = 1/(1+e^{-x})")
chk(sp.simplify(_q8.subs(_x, 0) - R(1, 2)) == 0, "演習8 初期条件")
chk(sp.limit(_q8, _x, sp.oo) == 1, "演習8 x→∞ で 1")
chk(sp.simplify(1 / (sp.Symbol("yy") * (1 - sp.Symbol("yy")))
                - (1 / sp.Symbol("yy") + 1 / (1 - sp.Symbol("yy")))) == 0,
    "演習8 部分分数（a = 1）")
# 演習9
chk(R(681, 500) != R(37, 25), "演習9 h を小さくすると値がちがう")
chk(R(1, 10) < R(1, 5), "演習9 h が小さい")
# 演習10
chk(sp.simplify(sp.factor(_x + sp.Symbol("yy"))) == _x + sp.Symbol("yy"),
    "演習10 和は分けられない")
chk(sp.simplify(sp.factor(_x * sp.Symbol("yy"))
                - _x * sp.Symbol("yy")) == 0, "演習10 積なら分けられる")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> First order differential equations.", "シラバス 1 行目を逐語で")
in_text("> Numerical solution of $\\dfrac{\\mathrm{d}y}{\\mathrm{d}x}"
        " = f(x, y)$ using Euler's method.", "Euler 法を逐語で")
in_text("> $x_{n+1} = x_{n}+h$, where $h$ is a constant.",
        "刻み幅を逐語で")
in_text("> Variables separable.", "変数分離を逐語で")
in_text("> Example: the logistic equation $\\dfrac{\\mathrm{d}n}"
        "{\\mathrm{d}t} = kn(a-n)$, $a$, $k \\in \\mathbb{R}$",
        "ロジスティック方程式を逐語で")
in_text("> Link to: partial fractions (AHL1.11) and use of partial fractions"
        " to rearrange the integrand (AHL5.15).", "Link を逐語で")
in_text("公式集の **5.18** の欄", "公式集の場所")
in_text("> Euler's method", "公式集の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("Euler's method follows the slope field", "図(a) の題")
in_fig("each step uses the gradient at the point it starts", "図(a) の注")
in_fig("the logistic curve", "図(b) の題")
in_fig("growth slows as $n$ approaches $a$", "図(b) の注")
in_text("Euler 法は、傾きの場の上を直線でたどります。", "キャプション (a)")
in_text("ロジスティック曲線は S 字で、上限に近づきます。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("1.48", "演習1"), ("2.41", "演習2")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl518a-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl518a", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-5-18a-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-18a-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/05-calculus/aahl-5-18a.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-18a.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| differential equation |", "| general solution |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## Euler 法で、$f$ に $y$ を入れ忘れる", "f に y を入れる")
in_text("## Euler 法で、$h$ をかけ忘れる", "h をかける")
in_text("## 分けきる前に積分する", "積の形だけ")
in_text("## $\\ln(a-n)$ の符号を落とす", "マイナス")
in_text("**解は、数ではなく関数**です。", "解は関数")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
