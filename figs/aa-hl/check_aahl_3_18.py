"""AA HL HL 3.18 — Intersections of lines and planes の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_18.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-18.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_18.py"), encoding="utf-8").read()
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



M = sp.Matrix
PI = sp.pi
_l, _t = sp.symbols("lam t")
_x, _y, _z = sp.symbols("x y z")


def dot(a, b):
    return M(a).dot(M(b))


def mag(v):
    return sp.sqrt(M(v).dot(M(v)))


def hit(a, b, n, d):
    """直線 a+λb と平面 r·n=d の交点の λ。"""
    return sp.solve(sp.Eq((M(a) + _l * M(b)).dot(M(n)), d), _l)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a = M(sp.symbols("a1 a2 a3"))
_b = M(sp.symbols("b1 b2 b3"))
_n = M(sp.symbols("n1 n2 n3"))
# 代入すると λ の 1 次式
_lhs = sp.expand((_a + _l * _b).dot(_n))
chk(sp.expand(_lhs - (_a.dot(_n) + _l * _b.dot(_n))) == 0,
    "(a+λb)·n = a·n + λ(b·n)")
chk(sp.degree(sp.Poly(_lhs, _l), _l) <= 1, "λ について 1 次")
chk(sp.expand(sp.diff(_lhs, _l) - _b.dot(_n)) == 0, "λ の係数は b·n")
# 余角の関係
_th = sp.Symbol("th", real=True)
chk(sp.simplify(sp.cos(PI / 2 - _th) - sp.sin(_th)) == 0,
    "cos(π/2 - θ) = sin θ")
# b·n = 0 なら λ が消える
_b0 = M([_n[1], -_n[0], 0])
chk(sp.expand(_b0.dot(_n) - _n[1] * _n[0] + _n[0] * _n[1]) == 0,
    "法線と垂直な向きの例")
chk(sp.expand(sp.diff((_a + _l * _b0).dot(_n), _l)) == 0,
    "b·n = 0 なら λ の係数が 0")
# 2 平面：未知数 3、式 2 なので 1 文字自由
_sol2 = sp.solve([_x + _y - 3, _y + _z - 5], [_x, _y, _z], dict=True)
chk(len(_sol2) == 1 and len(_sol2[0]) == 2, "2 平面の解は 1 文字残る")
# 平行な 2 平面で右辺が合わなければ解なし
chk(sp.solve([_x + _y + _z - 3, 2 * _x + 2 * _y + 2 * _z - 7],
             [_x, _y, _z], dict=True) == [], "平行で d が合わなければ解なし")
chk(sp.solve([_x + _y + _z - 3, 2 * _x + 2 * _y + 2 * _z - 6],
             [_x, _y, _z], dict=True) != [], "d が合えば解がある")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(hit([1, 0, 2], [2, 1, -1], [1, 1, 1], 7) == [2], "例題1 λ = 2")
chk(list(M([1, 0, 2]) + 2 * M([2, 1, -1])) == [5, 2, 0], "例題1 交点 (5,2,0)")
chk(dot([5, 2, 0], [1, 1, 1]) == 7, "例題1 交点は平面の上")
chk(dot([2, 1, -1], [1, 1, 1]) == 2, "例題1 b·n = 2")
chk(1 + 0 + 2 == 3, "例題1 定数項は 3")
# 例題2
_s2 = sp.solve([2 * _x + _y - _z - 3, _x - _y + _z], [_x, _y, _z], dict=True)
chk(_s2 == [{_x: 1, _y: _z + 1}], "例題2 x = 1, y = z+1")
chk(sp.expand(2 * 1 + (1 + _t) - _t - 3) == 0, "例題2 1 本目に入れると t が消える")
chk(sp.expand(1 - (1 + _t) + _t) == 0, "例題2 2 本目も成り立つ")
chk(dot([1, 1, 0], [2, 1, -1]) == 3 and dot([1, 1, 0], [1, -1, 1]) == 0,
    "例題2 通る点 (1,1,0) は両方の平面の上")
chk(dot([0, 1, 1], [2, 1, -1]) == 0 and dot([0, 1, 1], [1, -1, 1]) == 0,
    "例題2 方向は両方の法線と垂直")
# 例題3
chk(sp.simplify(sp.asin(sp.Abs(dot([1, 0, 0], [1, 1, 0]))
                        / (mag([1, 0, 0]) * mag([1, 1, 0]))) - PI / 4) == 0,
    "例題3 θ = π/4")
chk(sp.simplify(sp.acos(sp.Abs(dot([1, 0, 0], [1, 1, 0]))
                        / (mag([1, 0, 0]) * mag([1, 1, 0]))) - PI / 4) == 0,
    "例題3 法線との角 α = π/4")
chk(sp.simplify(PI / 4 + PI / 4 - PI / 2) == 0, "例題3 θ + α = π/2")
# 例題4
chk(dot([1, 1, 0], [1, 0, 1]) == 1, "例題4 法線の内積は 1")
chk(mag([1, 1, 0]) == sp.sqrt(2) and mag([1, 0, 1]) == sp.sqrt(2),
    "例題4 大きさはどちらも √2")
chk(sp.simplify(sp.acos(sp.Abs(dot([1, 1, 0], [1, 0, 1]))
                        / (mag([1, 1, 0]) * mag([1, 0, 1]))) - PI / 3) == 0,
    "例題4 θ = π/3")
chk(PI / 3 < PI / 2, "例題4 鋭角")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(hit([2, -1, 0], [1, 1, 1], [1, 2, 1], 4) == [1], "演習1 λ = 1")
chk(list(M([2, -1, 0]) + M([1, 1, 1])) == [3, 0, 1], "演習1 交点 (3,0,1)")
chk(dot([3, 0, 1], [1, 2, 1]) == 4, "演習1 交点は平面の上")
chk(dot([1, 1, 1], [1, 2, 1]) == 4, "演習1 b·n = 4")
# 演習2
chk(dot([1, -1, 0], [1, 1, 1]) == 0, "演習2 b·n = 0")
chk(dot([1, 1, 1], [1, 1, 1]) == 3, "演習2 点を入れると 3")
chk(3 != 10, "演習2 平面の上にない")
chk(hit([1, 1, 1], [1, -1, 0], [1, 1, 1], 10) == [], "演習2 交点なし")
# 演習3
chk(sp.simplify(sp.asin(sp.Abs(dot([1, 0, 1], [0, 0, 1]))
                        / (mag([1, 0, 1]) * mag([0, 0, 1]))) - PI / 4) == 0,
    "演習3 θ = π/4")
chk(mag([0, 0, 1]) == 1, "演習3 法線の大きさ 1")
# 演習4
chk(dot([1, 1, 1], [1, -1, 0]) == 0, "演習4 法線の内積 0")
chk(sp.simplify(sp.acos(sp.Abs(dot([1, 1, 1], [1, -1, 0]))
                        / (mag([1, 1, 1]) * mag([1, -1, 0]))) - PI / 2) == 0,
    "演習4 θ = π/2")
chk(mag([1, 1, 1]) == sp.sqrt(3) and mag([1, -1, 0]) == sp.sqrt(2),
    "演習4 大きさは √3 と √2")
chk(M([1, 1, 1]).cross(M([1, -1, 0])) != M([0, 0, 0]), "演習4 法線は平行でない")
# 演習5
chk(_sol2 == [{_x: _z - 2, _y: 5 - _z}], "演習5 x = z-2, y = 5-z")
chk(sp.expand((_t - 2) + (5 - _t) - 3) == 0, "演習5 1 本目が成り立つ")
chk(sp.expand((5 - _t) + _t - 5) == 0, "演習5 2 本目が成り立つ")
chk(dot([-2, 5, 0], [1, 1, 0]) == 3 and dot([-2, 5, 0], [0, 1, 1]) == 5,
    "演習5 通る点は両方の平面の上")
chk(dot([1, -1, 1], [1, 1, 0]) == 0 and dot([1, -1, 1], [0, 1, 1]) == 0,
    "演習5 方向は両方の法線と垂直")
# 演習6
chk(dot([1, 1, 1], [1, -1, 0]) == 0, "演習6 b·n = 0")
chk(dot([1, 0, 0], [1, -1, 0]) == 1, "演習6 点を入れると 1")
chk(sp.expand((1 + _l) - _l - 1) == 0, "演習6 一般の λ で成り立つ")
# 演習7
chk(list(M([2, 2, 2]) - 2 * M([1, 1, 1])) == [0, 0, 0], "演習7 法線は 2 倍")
chk(2 * 3 == 6, "演習7 1 本目を 2 倍すると右辺は 6")
chk(6 != 7, "演習7 右辺が合わない")
chk(sp.solve([_x + _y + _z - 3, _x - _y, 2 * _x + 2 * _y + 2 * _z - 7],
             [_x, _y, _z], dict=True) == [], "演習7 解なし")
chk(sp.solve([_x + _y + _z - 3, _x - _y, 2 * _x + 2 * _y + 2 * _z - 6],
             [_x, _y, _z], dict=True) != [], "演習7 右辺が 6 なら解がある")
# 演習8
chk(sp.expand(2 * _l + (1 - _l) - (2 + _l)) == -1, "演習8 代入すると -1")
chk(dot([1, -1, 1], [2, 1, -1]) == 0, "演習8 b·n = 0")
chk(dot([0, 1, 2], [2, 1, -1]) == -1, "演習8 点を入れると -1")
chk(hit([0, 1, 2], [1, -1, 1], [2, 1, -1], 0) == [], "演習8 交点なし")
# 演習9
chk(sp.simplify(sp.cos(PI / 2 - _th) - sp.sin(_th)) == 0, "演習9 余角の関係")
chk(sp.sin(PI / 2) == 1, "演習9 垂直なら sinθ = 1")
chk(sp.asin(0) == 0, "演習9 平行なら θ = 0")
# 演習10
chk(sp.solve(sp.Eq(0 * _l, 0), _l) == [], "演習10 0=0 は恒等式（解が全部）")
chk(sp.simplify(sp.Eq(0 * _l, 0)) is sp.true, "演習10 0=0 はいつでも正しい")
chk(sp.simplify(sp.Eq(0 * _l, 3)) is sp.false, "演習10 0=3 は成り立たない")
chk(hit([1, 0, 0], [0, 1, 0], [1, 0, 0], 1) == [], "演習10 中にある例は λ が消える")
chk(dot([1, 0, 0], [1, 0, 0]) == 1, "演習10 その点は x=1 の上")
chk(dot([1, 0, 0], [1, 0, 0]) != 2, "演習10 x=2 なら平行")

# ══════════════════════════════════════════════════════════
# 3. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Intersections of: a line with a plane; two planes; three planes.",
        "シラバス 1 行目を逐語で")
in_text("> Finding intersections by solving equations; geometrical"
        " interpretation of solutions.", "Guidance を逐語で")
in_text("> Angle between: a line and a plane; two planes.", "なす角を逐語で")
in_text("> Link to: solutions of systems of linear equations (AHL 1.16).",
        "1.16 への Link を逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("a line and a plane: three possibilities", "図(a) の題")
in_fig("one point", "図(a) 1 点")
in_fig("no point: parallel", "図(a) 平行")
in_fig("every point: the line is in the plane", "図(a) 中にある")
in_fig("two planes meet in a line", "図(b) の題")
in_fig("take the acute angle", "図(b) の注")
in_text("直線と平面は、$3$ 通りしかありません。", "キャプション (a)")
in_text("$2$ 平面のなす角は、法線どうしのなす角です。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("3 \\\\ 0 \\\\ 1", "演習1"),
                    ("-2 \\\\ 5 \\\\ 0", "演習5")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl318-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl318", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-18-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-18-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-18.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-18.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| intersect |", "| plane |", "| normal vector |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 直線と平面のなす角に $\\arccos$ を使う", "sin を使う")
in_text("## $2$ 平面のなす角に $\\arcsin$ を使う", "cos を使う")
in_text("**直線と平面は $\\sin$、平面と平面は $\\cos$**", "対にして覚える")
in_text("## $\\lambda$ が消えたとき、「解なし」と決めつける", "0=0 は中にある")
in_text("**右辺を見てください。**", "右辺で分かれる")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
