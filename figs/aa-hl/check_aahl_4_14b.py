"""AA HL HL 4.14b — Continuous random variables and probability density functions の内容を検算する。

    python3 figs/aa-hl/check_aahl_4_14b.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "04-statistics-and-probability")
QMD = os.path.join(BASE, "aahl-4-14b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_4_14b.py"), encoding="utf-8").read()
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



R = sp.Rational
_x = sp.Symbol("x")
_m = sp.Symbol("m", positive=True)
_k = sp.Symbol("k")


def area(f, a, b):
    return sp.integrate(f, (_x, a, b))


def mean(f, a, b):
    return sp.integrate(_x * f, (_x, a, b))


def m2(f, a, b):
    return sp.integrate(_x ** 2 * f, (_x, a, b))


def var(f, a, b):
    return sp.simplify(m2(f, a, b) - mean(f, a, b) ** 2)


def median(f, a, b):
    return sp.solve(sp.Eq(sp.integrate(f, (_x, a, _m)), R(1, 2)), _m)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a = sp.Symbol("a")
_f = sp.Function("f")
# 幅 0 の積分は 0
chk(sp.integrate(_f(_x), (_x, _a, _a)) == 0, "幅 0 の積分は 0")
# 分散の 2 つの形が一致する（∫f = 1 のとき）
_g = sp.Symbol("g", positive=True)
_p, _q = sp.symbols("p q", real=True)
_mu = sp.Symbol("mu")
_dens = 2 * _x   # ∫_0^1 2x dx = 1
chk(area(_dens, 0, 1) == 1, "例の密度は面積 1")
_mu0 = mean(_dens, 0, 1)
chk(sp.simplify(sp.integrate((_x - _mu0) ** 2 * _dens, (_x, 0, 1))
                - (m2(_dens, 0, 1) - _mu0 ** 2)) == 0,
    "分散の 2 つの形が一致")
# f は 1 を超えてよい
chk(area(sp.Integer(2), 0, R(1, 2)) == 1, "f = 2 でも面積 1")
chk(area(sp.Integer(10), 0, R(1, 10)) == 1, "f = 10 でも面積 1")
# 線形変換は離散と同じ
_aa, _bb = sp.symbols("aa bb")
chk(sp.simplify(sp.integrate((_aa * _x + _bb) * _dens, (_x, 0, 1))
                - (_aa * _mu0 + _bb)) == 0, "E(aX+b) = aE(X)+b")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(sp.solve(sp.Eq(area(_k * _x, 0, 2), 1), _k) == [R(1, 2)], "例題1 k = 1/2")
chk(area(_x / 2, 0, 1) == R(1, 4), "例題1 P(X<=1) = 1/4")
chk(R(1, 2) * 2 * 1 == 1, "例題1 三角形の面積 1")
chk(R(1, 4) < R(1, 2), "例題1 左半分は半分未満")
# 例題2
_f2 = R(3, 8) * _x ** 2
chk(area(_f2, 0, 2) == 1, "例題2 面積 1")
chk(mean(_f2, 0, 2) == R(3, 2), "例題2 E(X) = 3/2")
chk(m2(_f2, 0, 2) == R(12, 5), "例題2 E(X²) = 12/5")
chk(var(_f2, 0, 2) == R(3, 20), "例題2 Var(X) = 3/20")
chk(median(_f2, 0, 2) == [2 ** R(2, 3)], "例題2 中央値 = 4^(1/3)")
chk(sp.simplify(2 ** R(2, 3) - sp.root(4, 3)) == 0, "例題2 2^(2/3) = ∛4")
chk(sp.N(sp.root(4, 3)) > R(3, 2), "例題2 中央値は平均より右")
chk(sp.diff(_f2, _x).subs(_x, 1) > 0, "例題2 f は増加、最頻値は右端")
# 例題3
_p1 = _x
_p2 = 2 - _x
chk(area(_p1, 0, 1) + area(_p2, 1, 2) == 1, "例題3 面積 1")
chk(area(_p1, 0, 1) == R(1, 2) and area(_p2, 1, 2) == R(1, 2),
    "例題3 それぞれ 1/2")
chk(mean(_p1, 0, 1) == R(1, 3), "例題3 左の寄与 1/3")
chk(mean(_p2, 1, 2) == R(2, 3), "例題3 右の寄与 2/3")
chk(mean(_p1, 0, 1) + mean(_p2, 1, 2) == 1, "例題3 E(X) = 1")
chk(sp.simplify((2 - _x).subs(_x, 1) - _x.subs(_x, 1)) == 0, "例題3 x=1 でつながる")
# 例題4
chk(area(4 - _x ** 2, 0, 2) == R(16, 3), "例題4 ∫(4-x²) = 16/3")
chk(sp.solve(sp.Eq(_k * R(16, 3), 1), _k) == [R(3, 16)], "例題4 k = 3/16")
_f4 = R(3, 16) * (4 - _x ** 2)
chk(area(_f4, 0, 2) == 1, "例題4 面積 1")
chk(mean(_f4, 0, 2) == R(3, 4), "例題4 E(X) = 3/4")
chk(m2(_f4, 0, 2) == R(4, 5), "例題4 E(X²) = 4/5")
chk(var(_f4, 0, 2) == R(19, 80), "例題4 Var(X) = 19/80")
chk(R(32, 3) - R(32, 5) == R(64, 15), "例題4 通分")
chk(sp.diff(_f4, _x).subs(_x, 1) < 0, "例題4 f は減少、最頻値は左端 0")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(sp.solve(sp.Eq(area(_k, 0, 4), 1), _k) == [R(1, 4)], "演習1 k = 1/4")
chk(area(R(1, 4), 1, 3) == R(1, 2), "演習1 P = 1/2")
chk(area(R(1, 4), 0, 2) == R(1, 2), "演習1 同じ幅ならどこでも同じ")
# 演習2
chk(sp.solve(sp.Eq(area(_k * _x ** 2, 0, 3), 1), _k) == [R(1, 9)],
    "演習2 k = 1/9")
chk(area(_x ** 2 / 9, 0, 3) == 1, "演習2 たしかに 1")
# 演習3
chk(area(_x ** 2 / 9, 0, 2) == R(8, 27), "演習3 P(X<=2) = 8/27")
chk(1 - R(8, 27) == R(19, 27), "演習3 残りは 19/27")
chk(R(8, 27) < R(1, 2), "演習3 半分未満")
# 演習4
_f4b = 3 * _x ** 2
chk(area(_f4b, 0, 1) == 1, "演習4 面積 1")
chk(mean(_f4b, 0, 1) == R(3, 4), "演習4 E(X) = 3/4")
chk(R(3, 4) > R(1, 2), "演習4 平均は真ん中より右")
# 演習5
chk(median(_f4b, 0, 1) == [2 ** R(2, 3) / 2], "演習5 中央値")
chk(sp.simplify(2 ** R(2, 3) / 2 - 1 / sp.root(2, 3)) == 0,
    "演習5 1/∛2 と同じ")
chk(sp.N(2 ** R(2, 3) / 2) > R(3, 4), "演習5 中央値は平均より右")
chk(0 < sp.N(2 ** R(2, 3) / 2) < 1, "演習5 0 と 1 の間")
# 演習6
_f6 = _x / 2
chk(area(_f6, 0, 2) == 1, "演習6 面積 1")
chk(mean(_f6, 0, 2) == R(4, 3), "演習6 E(X) = 4/3")
chk(m2(_f6, 0, 2) == 2, "演習6 E(X²) = 2")
chk(var(_f6, 0, 2) == R(2, 9), "演習6 Var(X) = 2/9")
chk(2 > R(16, 9), "演習6 分散は正")
# 演習7
_f7 = 6 * _x * (1 - _x)
chk(area(_f7, 0, 1) == 1, "演習7 面積 1")
chk(sp.solve(sp.diff(_f7, _x), _x) == [R(1, 2)], "演習7 最頻値 1/2")
chk(sp.diff(_f7, _x, 2) == -12, "演習7 上に凸")
chk(_f7.subs(_x, 0) == 0 and _f7.subs(_x, 1) == 0, "演習7 端では 0")
chk(mean(_f7, 0, 1) == R(1, 2), "演習7 平均も 1/2")
chk(R(1, 2) in median(_f7, 0, 1), "演習7 中央値も 1/2")
# 演習8
chk(sp.integrate(_f(_x), (_x, _a, _a)) == 0, "演習8 P(X=a) = 0")
_h = sp.Symbol("h", positive=True)
chk(sp.limit(area(R(1, 2), 1, 1 + _h), _h, 0) == 0, "演習8 幅を縮めると 0")
chk(area(R(1, 2), 1, 1 + _h) == _h / 2, "演習8 その面積は h/2")
# 演習9
chk(area(sp.Integer(2), 0, R(1, 2)) == 1, "演習9 f=2 の例")
chk(area(sp.Integer(10), 0, R(1, 10)) == 1, "演習9 f=10 の例")
chk(sp.Integer(2) > 1, "演習9 密度は 1 を超えてよい")
# 演習10
chk(median(_f2, 0, 2)[0] < 2, "演習10 中央値は最頻値 2 とちがう")
chk(R(1, 2) in median(_f7, 0, 1) and sp.solve(sp.diff(_f7, _x), _x)
    == [R(1, 2)], "演習10 対称なら一致")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Continuous random variables and their probability density"
        " functions.", "シラバス 1 行目を逐語で")
in_text("$\\displaystyle\\int_{-\\infty}^{\\infty} f(x)\\mathrm{d}x = 1$"
        " including piecewise functions.", "∫f = 1 を逐語で")
in_text("> For a continuous random variable, a value at which the"
        " probability density function has a maximum value is called a mode",
        "最頻値の定義を逐語で")
in_text("> and for the median: $\\displaystyle\\int_{-\\infty}^{m}"
        " f(x)\\mathrm{d}x = \\frac{1}{2}$.", "中央値の定義を逐語で")
in_text("公式集の **4.14** の欄", "公式集の場所")
in_text("> Expected value of a continuous random variable X",
        "公式集の平均を逐語で")
in_text("> Variance of a continuous random variable X",
        "公式集の分散を逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("probability is area under the", "図(a) の題")
in_fig("total area $= 1$", "図(a) の注")
in_fig("the mode is the peak; the median splits the area in half",
       "図(b) の題")
in_fig("they are different unless the curve is symmetric", "図(b) の注")
in_text("確率は、曲線の下の面積です。", "キャプション (a)")
in_text("最頻値は山の頂上、中央値は面積を半分にする値です。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("\\frac{8}{27}", "演習3"), ("\\frac{2}{9}", "演習6")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl414b-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl414b", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-4-14b-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-4-14b-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/04-statistics-and-probability/aahl-4-14b.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aahl-4-14b.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| continuous |", "| median |", "| mode |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## $f(x)$ は確率ではありません", "密度と確率")
in_text("## 区分的な関数を、$1$ 本の積分ですませる", "区間ごとに切る")
in_text("## 中央値と最頻値を取りちがえる", "中央値と最頻値")
in_text("## 最頻値を求めるのに、端を調べない", "端も見る")
in_text("**$1$ 点の確率は $0$** です。", "1 点の確率は 0")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
