"""AA HL HL 5.13 — Limits and l'Hôpital's rule の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_13.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-13.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_13.py"), encoding="utf-8").read()
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
R = sp.Rational


def lim(f, a=0):
    return sp.limit(f, _x, a)


def lh(f, g, a=0):
    """l'Hôpital を 1 回。"""
    return sp.limit(sp.diff(f, _x) / sp.diff(g, _x), _x, a)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
# 0/0 でも極限はいろいろ
chk(lim(_x ** 2 / _x) == 0, "0/0 でも 0 になる例")
chk(lim(3 * _x / _x) == 3, "0/0 でも 3 になる例")
chk(sp.limit(_x / _x ** 2, _x, 0, "+") == sp.oo, "0/0 でも ∞ になる例")
# 接線での近似
_f = sp.Function("f")
_a = sp.Symbol("a")
chk(sp.series(sp.sin(_x), _x, 0, 2).removeO() == _x, "sin x ≒ x（1 次まで）")
chk(sp.simplify(sp.limit(sp.sin(_x) / _x, _x, 0) - 1) == 0,
    "sinθ/θ の極限は 1")
# ∞/∞ は 0/0 に直せる
chk(sp.limit((1 / _x) / (1 / _x ** 2), _x, sp.oo) == sp.oo,
    "1/x と 1/x² の比")
# 度で測ると 1 にならない
_d = sp.pi / 180
chk(sp.simplify(sp.limit(sp.sin(_d * _x) / _x, _x, 0) - _d) == 0,
    "度で測ると π/180 になる")
chk(sp.diff(sp.sin(_d * _x), _x).subs(_x, 0) == _d, "度の微分には π/180 が付く")
# 不定形でないときに使うとちがう答えになる
chk(lim((_x + 1) / (_x + 2)) == R(1, 2), "(x+1)/(x+2) の極限は 1/2")
chk(lh(_x + 1, _x + 2) == 1, "誤用すると 1 になる")
chk(R(1, 2) != 1, "この 2 つはちがう")
# 商の微分とはちがう
chk(sp.simplify(sp.diff(sp.sin(_x) / _x, _x)
                - (_x * sp.cos(_x) - sp.sin(_x)) / _x ** 2) == 0,
    "商の微分はこの形")
chk(sp.limit((_x * sp.cos(_x) - sp.sin(_x)) / _x ** 2, _x, 0) == 0,
    "その極限は 0 で、答えとはちがう")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(lim(sp.sin(3 * _x) / _x) == 3, "例題1 極限は 3")
chk(sp.diff(sp.sin(3 * _x), _x) == 3 * sp.cos(3 * _x), "例題1 分子の微分")
chk(sp.cos(0) == 1, "例題1 cos 0 = 1")
chk(sp.N(sp.sin(R(3, 100)) / R(1, 100), 6) > 2.99, "例題1 x=0.01 で約 3")
# 例題2
_f2 = sp.exp(_x) - 1 - _x
chk(lim(_f2 / _x ** 2) == R(1, 2), "例題2 極限は 1/2")
chk(sp.diff(_f2, _x) == sp.exp(_x) - 1, "例題2 1 回目の分子")
chk(sp.diff(_x ** 2, _x) == 2 * _x, "例題2 1 回目の分母")
chk(lim((sp.exp(_x) - 1) / (2 * _x)) == R(1, 2), "例題2 2 回目でも 1/2")
chk(_f2.subs(_x, 0) == 0, "例題2 分子は 0 から始まる")
# 例題3
_f3 = (3 * _x ** 2 + 2 * _x) / (_x ** 2 - 5)
chk(sp.limit(_f3, _x, sp.oo) == 3, "例題3 極限は 3")
chk(sp.limit((6 * _x + 2) / (2 * _x), _x, sp.oo) == 3, "例題3 1 回目のあとも 3")
chk(R(3, 1) == 3, "例題3 係数の比")
chk(sp.N(_f3.subs(_x, 100), 6) > 3, "例題3 x=100 で 3 より少し上")
# 例題4
_f4 = (_x - sp.sin(_x)) / _x ** 3
chk(lim(_f4) == R(1, 6), "例題4 極限は 1/6")
chk(lim((1 - sp.cos(_x)) / (3 * _x ** 2)) == R(1, 6), "例題4 1 回目のあと")
chk(lim(sp.sin(_x) / (6 * _x)) == R(1, 6), "例題4 2 回目のあと")
chk(sp.cos(0) / 6 == R(1, 6), "例題4 3 回目のあと")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(lim(sp.sin(5 * _x) / (2 * _x)) == R(5, 2), "演習1 5/2")
chk(sp.diff(sp.sin(5 * _x), _x) == 5 * sp.cos(5 * _x), "演習1 分子の微分")
chk(lim((1 - sp.cos(_x)) / _x ** 2) == R(1, 2), "演習2 1/2")
chk(lim(sp.sin(_x) / (2 * _x)) == R(1, 2), "演習2 1 回目のあと")
chk(sp.limit((2 * _x ** 2 - 1) / (5 * _x ** 2 + 3 * _x), _x, sp.oo)
    == R(2, 5), "演習3 2/5")
chk(sp.limit((4 * _x) / (10 * _x + 3), _x, sp.oo) == R(2, 5),
    "演習3 1 回目のあと")
chk(sp.limit((_x ** 3 - 1) / (_x - 1), _x, 1) == 3, "演習4 3")
chk(sp.factor(_x ** 3 - 1) == (_x - 1) * (_x ** 2 + _x + 1),
    "演習4 因数分解")
chk((_x ** 2 + _x + 1).subs(_x, 1) == 3, "演習4 約分してから代入")
chk(lim((sp.exp(2 * _x) - 1) / _x) == 2, "演習5 2")
chk(sp.diff(sp.exp(2 * _x), _x).subs(_x, 0) == 2, "演習5 導関数としても 2")
chk(lim(sp.tan(_x) / _x) == 1, "演習6 1")
chk(sp.diff(sp.tan(_x), _x) == sp.tan(_x) ** 2 + 1, "演習6 tan の導関数")
chk(sp.simplify(sp.sec(0) ** 2 - 1) == 0, "演習6 sec²0 = 1")
chk(sp.limit(sp.log(_x) / _x, _x, sp.oo) == 0, "演習7 0")
chk(sp.limit(1 / _x, _x, sp.oo) == 0, "演習7 1 回目のあと")
chk(lim((_x - sp.atan(_x)) / _x ** 3) == R(1, 3), "演習8 1/3")
chk(sp.simplify(1 - 1 / (1 + _x ** 2) - _x ** 2 / (1 + _x ** 2)) == 0,
    "演習8 分子をまとめる")
chk(sp.simplify(sp.diff(sp.atan(_x), _x) - 1 / (1 + _x ** 2)) == 0,
    "演習8 arctan の導関数")
chk(lim(1 / (3 * (1 + _x ** 2))) == R(1, 3), "演習8 約分したあと")
chk(lim((_x + 1) / (_x + 2)) == R(1, 2), "演習9 1/2")
chk((0 + 1) / (0 + 2) == 0.5, "演習9 代入で出る")
chk(lh(_x + 1, _x + 2) == 1, "演習9 誤用すると 1")
chk(lim(sp.sin(_x) / _x) == 1, "演習10 正しくは 1")
chk(sp.diff(sp.sin(_x), _x) == sp.cos(_x), "演習10 分子の微分")
chk(sp.limit((_x * sp.cos(_x) - sp.sin(_x)) / _x ** 2, _x, 0) == 0,
    "演習10 商の微分の極限は 0")

# ══════════════════════════════════════════════════════════
# 3. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> The indeterminate forms $\\dfrac{0}{0}$ and"
        " $\\dfrac{\\infty}{\\infty}$.", "不定形を逐語で")
in_text("> The evaluation of limits of the form"
        " $\\displaystyle\\lim_{x \\to a}\\frac{f(x)}{g(x)}$ and"
        " $\\displaystyle\\lim_{x \\to \\infty}\\frac{f(x)}{g(x)}$ using"
        " l'Hôpital's rule or the Maclaurin series.", "Content を逐語で")
in_text("> Repeated use of l'Hôpital's rule.", "くり返しを逐語で")
in_text("> Link to: horizontal asymptotes (SL2.8).", "水平漸近線への Link を逐語で")
in_text("> For example: $\\displaystyle\\lim_{\\theta \\to 0}"
        "\\frac{\\sin\\theta}{\\theta} = 1$.", "例を逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("near a common zero, each curve looks like its tangent", "図(a) の題")
in_fig("both are $0$ at $x = a$", "図(a) の注")
in_fig("has a hole at $x = 0$", "図(b) の題")
in_fig("the values approach $1$", "図(b) の注")
in_text("$0$ になる点の近くでは、曲線は接線とほぼ同じです。", "キャプション (a)")
in_text("に穴があり、値は $1$ に近づきます。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("\\frac{2}{5}", "演習3"), ("\\frac{5}{2}", "演習1")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl513-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl513", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-5-13-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-13-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/05-calculus/aahl-5-13.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-13.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| limit |", "| indeterminate form |", "| horizontal asymptote |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 不定形でないときは使えません", "条件の確認")
in_text("## 商の微分をしてしまう", "別々に微分")
in_text("## $1$ 回で止めてしまう", "くり返す")
in_text("## 度で計算する", "ラジアン")
in_text("**分子と分母を、別々に微分します。**", "別々に微分（本文）")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
