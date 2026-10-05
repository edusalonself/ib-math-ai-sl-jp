"""AA HL HL 5.12 — Continuity, differentiability and first principles の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_12.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-12.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_12.py"), encoding="utf-8").read()
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
_h = sp.Symbol("h")
_n = sp.Symbol("n", positive=True, integer=True)


def fp(f):
    """第一原理で微分する。"""
    return sp.simplify(sp.limit((f.subs(_x, _x + _h) - f) / _h, _h, 0))


def quot(f):
    """約分したあとの商。"""
    return sp.simplify(sp.expand((f.subs(_x, _x + _h) - f)) / _h)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a, _b, _c = sp.symbols("a b c")
# 一般の 2 次式
chk(sp.expand(fp(_a * _x ** 2 + _b * _x + _c) - (2 * _a * _x + _b)) == 0,
    "ax²+bx+c の第一原理は 2ax+b")
chk(sp.expand(quot(_a * _x ** 2 + _b * _x + _c)
              - (2 * _a * _x + _a * _h + _b)) == 0, "約分後は 2ax+ah+b")
# 展開の形
chk(sp.expand((_x + _h) ** 2) == _x ** 2 + 2 * _x * _h + _h ** 2,
    "(x+h)² の展開")
chk(sp.expand((_x + _h) ** 3)
    == _x ** 3 + 3 * _x ** 2 * _h + 3 * _x * _h ** 2 + _h ** 3,
    "(x+h)³ の展開")
# 定数は消える
chk(sp.expand((_x ** 2 + _c).subs(_x, _x + _h) - (_x ** 2 + _c)
              - (2 * _x * _h + _h ** 2)) == 0, "定数項は引き算で消える")
# 片側極限がちがう（角）
chk(sp.limit(sp.Abs(_h) / _h, _h, 0, "+") == 1, "右からは 1")
chk(sp.limit(sp.Abs(_h) / _h, _h, 0, "-") == -1, "左からは -1")
chk(1 != -1, "左右がちがうので極限がない")
# 微分可能なら連続
chk(sp.limit(_h * (2 * _x + _h), _h, 0) == 0, "h×(有限)→0")
# 高次導関数の記号
chk(sp.diff(_x ** 5, _x, 3) == 60 * _x ** 2, "x⁵ の 3 階微分")
chk(sp.diff(_x ** 5, _x, 6) == 0, "5 次は 6 回で 0")
# e^{2x} の n 階微分
chk(sp.diff(sp.exp(2 * _x), _x, 4) == 16 * sp.exp(2 * _x), "e^{2x} の 4 階微分")
for _k in range(1, 6):
    chk(sp.simplify(sp.diff(sp.exp(2 * _x), _x, _k)
                    - 2 ** _k * sp.exp(2 * _x)) == 0,
        "e^{2x} の %d 階微分は 2^%d e^{2x}" % (_k, _k))

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(fp(_x ** 2) == 2 * _x, "例題1 x² → 2x")
chk(sp.expand(quot(_x ** 2) - (2 * _x + _h)) == 0, "例題1 約分後は 2x+h")
chk(sp.expand((_x + _h) ** 2 - _x ** 2 - _h * (2 * _x + _h)) == 0,
    "例題1 因数分解 h(2x+h)")
chk(sp.Rational(21, 10) == 2 + sp.Rational(1, 10), "例題1 h=0.1 で 2.1")
chk(sp.Rational(201, 100) == 2 + sp.Rational(1, 100), "例題1 h=0.01 で 2.01")
# 例題2
_f2 = 3 * _x ** 2 - 2 * _x + 1
chk(fp(_f2) == 6 * _x - 2, "例題2 → 6x-2")
chk(sp.expand(_f2.subs(_x, _x + _h) - _f2
              - _h * (6 * _x + 3 * _h - 2)) == 0, "例題2 因数分解")
chk(sp.diff(_f2, _x) == 6 * _x - 2, "例題2 公式と一致")
# 例題3
chk(fp(_x ** 3) == 3 * _x ** 2, "例題3 x³ → 3x²")
chk(sp.expand((_x + _h) ** 3 - _x ** 3
              - _h * (3 * _x ** 2 + 3 * _x * _h + _h ** 2)) == 0,
    "例題3 因数分解")
# 例題4
chk(sp.diff(sp.exp(2 * _x), _x) == 2 * sp.exp(2 * _x), "例題4 1 階")
chk(sp.diff(sp.exp(2 * _x), _x, 2) == 4 * sp.exp(2 * _x), "例題4 2 階")
chk(sp.diff(sp.exp(2 * _x), _x, 3) == 8 * sp.exp(2 * _x), "例題4 3 階")
chk(2 ** 3 == 8, "例題4 2³ = 8")
chk(2 ** 0 == 1, "例題4 2⁰ = 1")
chk(sp.simplify(sp.diff(2 ** sp.Symbol("k") * sp.exp(2 * _x), _x)
                - 2 ** (sp.Symbol("k") + 1) * sp.exp(2 * _x)) == 0,
    "例題4 帰納段階")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(fp(5 * _x - 2) == 5, "演習1 → 5")
chk(sp.expand((5 * (_x + _h) - 2) - (5 * _x - 2) - 5 * _h) == 0,
    "演習1 分子は 5h")
# 演習2
chk(fp(_x ** 2 + 3 * _x) == 2 * _x + 3, "演習2 → 2x+3")
chk(sp.expand((_x ** 2 + 3 * _x).subs(_x, _x + _h) - (_x ** 2 + 3 * _x)
              - _h * (2 * _x + _h + 3)) == 0, "演習2 因数分解")
chk((2 * _x + 3).subs(_x, 0) == 3, "演習2 x=0 で 3")
# 演習3
chk(fp(2 * _x ** 2 - 5) == 4 * _x, "演習3 → 4x")
chk(sp.expand((2 * _x ** 2 - 5).subs(_x, _x + _h) - (2 * _x ** 2 - 5)
              - _h * (4 * _x + 2 * _h)) == 0, "演習3 因数分解")
# 演習4
chk(fp(_x ** 3 - _x) == 3 * _x ** 2 - 1, "演習4 → 3x²-1")
chk(sp.solve(sp.Eq(3 * _x ** 2 - 1, 0), _x)
    == [-sp.sqrt(3) / 3, sp.sqrt(3) / 3], "演習4 f'=0 の解")
chk(sp.simplify(sp.sqrt(3) / 3 - 1 / sp.sqrt(3)) == 0, "演習4 1/√3 と同じ")
# 演習5
chk(sp.limit(sp.Abs(_h) / _h, _h, 0, "+") == 1, "演習5 右からは 1")
chk(sp.limit(sp.Abs(_h) / _h, _h, 0, "-") == -1, "演習5 左からは -1")
chk(sp.limit(sp.Abs(_x), _x, 0) == 0, "演習5 連続ではある")
chk(sp.diff(_x, _x) == 1, "演習5 x>0 では傾き 1")
# 演習6
chk(sp.diff(_x ** 5, _x) == 5 * _x ** 4, "演習6 1 階")
chk(sp.diff(_x ** 5, _x, 2) == 20 * _x ** 3, "演習6 2 階")
chk(sp.diff(_x ** 5, _x, 3) == 60 * _x ** 2, "演習6 3 階")
chk(5 * 4 * 3 == 60, "演習6 係数 60")
# 演習7
chk(sp.limit((_x ** 2 - 4) / (_x - 2), _x, 2) == 4, "演習7 極限は 4")
chk(sp.factor(_x ** 2 - 4) == (_x - 2) * (_x + 2), "演習7 因数分解")
chk(sp.Rational(401, 100) == sp.Rational(201, 100) + 2, "演習7 x=2.01 で 4.01")
chk(sp.diff(_x ** 2, _x).subs(_x, 2) == 4, "演習7 f'(2) = 4 でもある")
# 演習8
chk(sp.expand(fp(_a * _x ** 2 + _b * _x + _c) - (2 * _a * _x + _b)) == 0,
    "演習8 一般の 2 次式")
chk((2 * _a * _x + _b).subs({_a: 3, _b: -2}) == 6 * _x - 2, "演習8 例題2 と一致")
chk((2 * _a * _x + _b).subs(_a, 0) == _b, "演習8 a=0 なら 1 次式")
# 演習9
chk(sp.limit(2 * _x + _h, _h, 0) == 2 * _x, "演習9 約分後は代入してよい")
chk(sp.Rational(2001, 1000) == 2 + sp.Rational(1, 1000), "演習9 h=0.001 で 2.001")
# 演習10
chk(fp(_x ** 2) == 2 * _x, "演習10 正しくは 2x")
chk(sp.expand(quot(_x ** 2) - (2 * _x + _h)) == 0, "演習10 約分してから極限")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Understanding of limits (convergence and divergence).",
        "シラバスの極限を逐語で")
in_text("> In examinations, students will not be asked to test for"
        " continuity and differentiability.", "Guidance を逐語で")
in_text("> Use of this definition for polynomials only.",
        "多項式だけ、を逐語で")
in_text("> Familiarity with the notations $\\dfrac{\\mathrm{d}^{n}y}"
        "{\\mathrm{d}x^{n}}$, $f^{(n)}(x)$.", "記号を逐語で")
in_text("> Link to: proof by mathematical induction (AHL 1.15).",
        "帰納法への Link を逐語で")
in_text("公式集の **5.12** の欄", "公式集の場所")
in_text("> Derivative of $f(x)$ from first principles",
        "公式集の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("three ways a graph can fail to be smooth", "図(a) の題")
in_fig("a jump", "図(a) とび")
in_fig("a hole", "図(a) 穴")
in_fig("a corner", "図(a) 角")
in_fig("the gradient of the chord", "図(b) の題")
in_fig("the chord turns into the tangent", "図(b) の注")
in_text("なめらかでなくなる $3$ 通りです。", "キャプション (a)")
in_text("割線の傾きで、$h$ を $0$ に近づけます。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("3x^{2}-1", "演習4"), ("60x^{2}", "演習6")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl512-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl512", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-5-12-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-12-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/05-calculus/aahl-5-12.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-12.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| limit |", "| continuous |", "| derivative |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 約分する前に $h = 0$ を入れる", "先に約分")
in_text("## 連続なら微分できる、と考える", "向きは一方だけ")
in_text("## $f^{(n)}(x)$ を $n$ 乗だと読む", "記号の読み方")
in_text("**$h = 0$ を代入してはいけません。**", "代入しない")
in_text("**微分可能なら連続です。** 逆は成り立ちません。", "微分可能 ⇒ 連続")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
