"""AA HL HL 4.14a — Variance of a discrete random variable の内容を検算する。

    python3 figs/aa-hl/check_aahl_4_14a.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "04-statistics-and-probability")
QMD = os.path.join(BASE, "aahl-4-14a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_4_14a.py"), encoding="utf-8").read()
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


def stats(xs, ps):
    """(E(X), E(X^2), Var(X)) を返す。"""
    m = sum(x * p for x, p in zip(xs, ps))
    m2 = sum(x * x * p for x, p in zip(xs, ps))
    return m, m2, m2 - m ** 2


def bydef(xs, ps):
    m = sum(x * p for x, p in zip(xs, ps))
    return sum((x - m) ** 2 * p for x, p in zip(xs, ps))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_x1, _x2, _x3 = sp.symbols("x1 x2 x3")
_p1, _p2, _p3 = sp.symbols("p1 p2 p3", positive=True)
_XS = [_x1, _x2, _x3]
_PS = [_p1, _p2, _p3]
_mu = sum(x * p for x, p in zip(_XS, _PS))
_m2 = sum(x * x * p for x, p in zip(_XS, _PS))
_one = sum(_PS)
# 定義と計算式が一致する（確率の合計が 1 のとき）
_def = sum((x - _mu) ** 2 * p for x, p in zip(_XS, _PS))
chk(sp.simplify(sp.expand(_def - (_m2 - _mu ** 2)).subs(_p3, 1 - _p1 - _p2))
    == 0, "定義と E(X²)-μ² が一致")
# ずれの和は 0
chk(sp.simplify(sp.expand(sum((x - _mu) * p for x, p in zip(_XS, _PS)))
                .subs(_p3, 1 - _p1 - _p2)) == 0, "ずれの和は 0")
# E(aX+b) = aE(X)+b
_a, _b = sp.symbols("a b")
_lin = sum((_a * x + _b) * p for x, p in zip(_XS, _PS))
chk(sp.simplify(sp.expand(_lin - (_a * _mu + _b)).subs(_p3, 1 - _p1 - _p2))
    == 0, "E(aX+b) = aE(X)+b")
# Var(aX+b) = a²Var(X)
_ylin = [_a * x + _b for x in _XS]
_my = sum(y * p for y, p in zip(_ylin, _PS))
_vy = sum((y - _my) ** 2 * p for y, p in zip(_ylin, _PS))
chk(sp.simplify(sp.expand(_vy - _a ** 2 * _def)
                .subs(_p3, 1 - _p1 - _p2)) == 0,
    "Var(aX+b) = a²Var(X)")
# b が消える
chk(sp.simplify(sp.expand((_a * _x1 + _b) - (_a * _mu + _b)
                          - _a * (_x1 - _mu))) == 0, "ずれから b が消える")
# 分散は 0 以上
chk(all(sp.Symbol("q", positive=True) ** 0 == 1 for _ in [0]), "定数の確認")
chk(bydef([1, 2, 3], [R(1, 3)] * 3) > 0, "分散は正になりうる")
chk(bydef([2, 2, 2], [R(1, 3)] * 3) == 0, "同じ値だけなら分散 0")
# Var(-X) = Var(X)
chk(sp.simplify(sp.expand(_vy.subs({_a: -1, _b: 0}) - _def)) == 0,
    "Var(-X) = Var(X)")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_e1 = stats([1, 2, 3], [R(2, 10), R(5, 10), R(3, 10)])
chk(_e1[0] == R(21, 10), "例題1 E(X) = 2.1")
chk(_e1[1] == R(49, 10), "例題1 E(X²) = 4.9")
chk(_e1[2] == R(49, 100), "例題1 Var(X) = 0.49")
chk(sp.sqrt(_e1[2]) == R(7, 10), "例題1 σ = 0.7")
chk(bydef([1, 2, 3], [R(2, 10), R(5, 10), R(3, 10)]) == R(49, 100),
    "例題1 定義でも 0.49")
chk(R(121, 100) * R(2, 10) == R(242, 1000), "例題1 0.242")
chk(R(1, 100) * R(5, 10) == R(5, 1000), "例題1 0.005")
chk(R(81, 100) * R(3, 10) == R(243, 1000), "例題1 0.243")
chk(1 < _e1[0] < 3, "例題1 平均は 1 と 3 の間")
# 例題2
chk(3 * R(21, 10) - 2 == R(43, 10), "例題2 E(Y) = 4.3")
chk(9 * R(49, 100) == R(441, 100), "例題2 Var(Y) = 4.41")
chk(sp.sqrt(R(441, 100)) == R(21, 10), "例題2 σ_Y = 2.1")
chk(3 * R(7, 10) == R(21, 10), "例題2 σ は 3 倍")
# 例題3
chk(1 - R(3, 10) - R(5, 10) == R(2, 10), "例題3 k = 0.2")
_e3 = stats([0, 1, 2], [R(3, 10), R(2, 10), R(5, 10)])
chk(_e3[0] == R(12, 10), "例題3 E(X) = 1.2")
chk(_e3[1] == R(22, 10), "例題3 E(X²) = 2.2")
chk(_e3[2] == R(76, 100), "例題3 Var(X) = 0.76")
chk(R(22, 10) > R(144, 100), "例題3 分散は正")
# 例題4
_e4 = stats([1, 2, 3, 4, 5, 6], [R(1, 6)] * 6)
chk(_e4[0] == R(7, 2), "例題4 E(X) = 7/2")
chk(_e4[1] == R(91, 6), "例題4 E(X²) = 91/6")
chk(_e4[2] == R(35, 12), "例題4 Var(X) = 35/12")
chk(R(91, 6) == R(182, 12) and R(49, 4) == R(147, 12), "例題4 通分")
chk(R(7, 2) - R(7, 2) == 0, "例題4 公平なら k = 7/2")
chk(1 ** 2 * R(35, 12) == R(35, 12), "例題4 もうけの分散も 35/12")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
_q1 = stats([0, 1, 2], [R(5, 10), R(3, 10), R(2, 10)])
chk(_q1[0] == R(7, 10), "演習1 E(X) = 0.7")
chk(_q1[1] == R(11, 10), "演習1 E(X²) = 1.1")
chk(_q1[2] == R(61, 100), "演習1 Var(X) = 0.61")
chk(R(11, 10) > R(49, 100), "演習1 分散は正")
# 演習2
chk(2 * 4 + 5 == 13, "演習2 E = 13")
chk(2 ** 2 * 9 == 36, "演習2 Var = 36")
chk(sp.sqrt(36) == 2 * sp.sqrt(9), "演習2 σ は 2 倍")
# 演習3
chk(13 - 3 ** 2 == 4, "演習3 Var = 4")
chk(sp.sqrt(4) == 2, "演習3 σ = 2")
chk(4 + 9 == 13, "演習3 逆向きでも合う")
# 演習4
_q4 = stats([1, 2, 3, 4], [R(1, 10), R(2, 10), R(3, 10), R(4, 10)])
chk(_q4[0] == 3, "演習4 E(X) = 3")
chk(_q4[1] == 10, "演習4 E(X²) = 10")
chk(_q4[2] == 1, "演習4 Var(X) = 1")
chk(sp.sqrt(_q4[2]) == 1, "演習4 σ = 1")
chk(sum([R(1, 10), R(2, 10), R(3, 10), R(4, 10)]) == 1, "演習4 確率の合計 1")
chk(_q4[0] > R(5, 2), "演習4 平均は真ん中より右")
# 演習5
_k = sp.Symbol("k")
chk(sp.solve(sp.Eq(_k + 2 * _k + 3 * _k, 1), _k) == [R(1, 6)], "演習5 k = 1/6")
_q5 = stats([1, 2, 3], [R(1, 6), R(2, 6), R(3, 6)])
chk(_q5[0] == R(7, 3), "演習5 E(X) = 7/3")
chk(_q5[1] == 6, "演習5 E(X²) = 6")
chk(_q5[2] == R(5, 9), "演習5 Var(X) = 5/9")
chk(6 == R(54, 9), "演習5 通分")
chk(1 < _q5[0] < 3, "演習5 平均は 1 と 3 の間")
# 演習6
chk(3 ** 2 * 5 == 45, "演習6 Var(3X-1) = 45")
chk((-1) ** 2 * 5 == 5, "演習6 Var(-X) = 5")
# 演習7
chk(10 * R(2, 10) + 0 * R(8, 10) == 2, "演習7 受け取る額の期待値は 2")
chk(2 - 2 == 0, "演習7 c = 2 で公平")
chk(2 - 3 == -1, "演習7 c = 3 なら損")
# 演習8
chk(sp.simplify(sp.expand(_vy - _a ** 2 * _def)
                .subs(_p3, 1 - _p1 - _p2)) == 0, "演習8 一般に成り立つ")
chk(sp.simplify(sp.expand(_vy.subs(_a, 1) - _def)
                .subs(_p3, 1 - _p1 - _p2)) == 0, "演習8 a=1 なら変わらない")
chk(sp.simplify(sp.expand(_vy.subs(_b, 0) - _a ** 2 * _def)) == 0,
    "演習8 b=0 でも同じ")
# 演習9
chk(bydef([1, 2, 3], [R(1, 6), R(2, 6), R(3, 6)]) == R(5, 9),
    "演習9 定義でも同じ答え")
chk(_q5[2] == R(5, 9), "演習9 計算式でも同じ答え")
# 演習10
chk(2 ** 2 * 1 == 4 and 2 * 1 != 4, "演習10 4 倍であって 2 倍ではない")
_ten = stats([0, 2], [R(1, 2), R(1, 2)])
chk(_ten[2] == 1, "演習10 X の分散は 1")
chk(stats([0, 4], [R(1, 2), R(1, 2)])[2] == 4, "演習10 2X の分散は 4")
chk(stats([3, 5], [R(1, 2), R(1, 2)])[2] == 1, "演習10 X+3 の分散は 1")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Link to: discrete random variables (SL 4.7)", "Link to を逐語で")
in_text("> Use of the notation E(X), E(X 2), Var(X),", "記号を逐語で")
in_text("> where Var(X) = E(X 2) − [E(X)]2", "Var の式を逐語で")
in_text('> Use of E(X) for "fair" games.', "fair games を逐語で")
in_text("公式集の **4.14** の欄", "公式集の場所")
in_text("> Variance of a discrete random variable X", "公式集の見出しを逐語で")
in_text("> Linear transformation of a single random variable",
        "1 次変換の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("same mean, different spread", "図(a) の題")
in_fig("small variance", "図(a) 小さい分散")
in_fig("large variance", "図(a) 大きい分散")
in_fig("the mean alone does not say how far", "図(a) の注")
in_fig("adding $b$ slides, multiplying by $a$ stretches", "図(b) の題")
in_fig("so the variance is multiplied by", "図(b) の注")
in_text("平均が同じでも、ちらばりはちがいます。", "キャプション (a)")
in_text("はずらすだけ、", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("0.61", "演習1"), ("\\frac{5}{9}", "演習5")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl414a-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl414a", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-4-14a-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-4-14a-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/04-statistics-and-probability/aahl-4-14a.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aahl-4-14a.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| variance |", "| standard deviation |", "| expected value |",
          "| fair game |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 分散に $b$ が効くと思う", "b は効かない")
in_text("## 分散の係数を $a$ のままにする", "a の 2 乗")
in_text("## 標準偏差を聞かれて分散を答える", "平方根を忘れない")
in_text("## 分散は負になりません", "分散は 0 以上")
in_text("**受け取る額の期待値が参加料に等しい**", "公平の読みかえ")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
