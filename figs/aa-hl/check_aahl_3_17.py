"""AA HL HL 3.17 — The vector equation of a plane の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_17.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-17.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_17.py"), encoding="utf-8").read()
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
_l, _m = sp.symbols("lam mu")


def cr(a, b):
    return list(M(a).cross(M(b)))


def dot(a, b):
    return M(a).dot(M(b))


def mag(v):
    return sp.sqrt(M(v).dot(M(v)))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a = M(sp.symbols("a1 a2 a3"))
_b = M(sp.symbols("b1 b2 b3"))
_c = M(sp.symbols("c1 c2 c3"))
_k = sp.Symbol("k", nonzero=True)
_n = _b.cross(_c)
# 法線は 2 方向に垂直
chk(sp.expand(_b.dot(_n)) == 0, "b·(b×c) = 0")
chk(sp.expand(_c.dot(_n)) == 0, "c·(b×c) = 0")
# r·n = a·n
_r = _a + _l * _b + _m * _c
chk(sp.expand(_r.dot(_n) - _a.dot(_n)) == 0, "r·n = a·n")
chk(sp.expand((_r - _a).dot(_n)) == 0, "(r-a)·n = 0")
# b と c が平行だと直線になる
chk(sp.simplify((_l * _b + _m * (_k * _b)) - (_l + _k * _m) * _b)
    == M([0, 0, 0]), "平行なら λb+μc は b の倍数")
chk(sp.simplify(_b.cross(_k * _b)) == M([0, 0, 0]), "平行なら b×c = 0")
# 法線をスカラー倍しても同じ平面
chk(sp.expand(_r.dot(_k * _n) - _a.dot(_k * _n)) == 0, "n を k 倍しても成り立つ")
# デカルト形は内積そのもの
_x, _y, _z = sp.symbols("x y z")
_nn = M(sp.symbols("na nb nc"))
chk(sp.expand(M([_x, _y, _z]).dot(_nn)
              - (_nn[0] * _x + _nn[1] * _y + _nn[2] * _z)) == 0,
    "r·n = ax+by+cz")
# b+c は平面の中（演習10）
chk(sp.expand((_b + _c).dot(_n)) == 0, "(b+c)·n = 0、つまり平面の中")
# 直線が平面の中にある条件
_d0 = M(sp.symbols("d1 d2 d3"))
chk(sp.expand(((_a + _l * _d0).dot(_nn)) - _a.dot(_nn) - _l * _d0.dot(_nn))
    == 0, "直線を代入すると λ(d·n) が残る")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(cr([1, 0, 1], [0, 1, -1]) == [-1, 1, 1], "例題1 法線 (-1,1,1)")
chk(dot([1, 2, 3], [-1, 1, 1]) == 4, "例題1 d = 4")
chk(dot([1, 0, 1], [-1, 1, 1]) == 0, "例題1 法線と b が垂直")
chk(dot([0, 1, -1], [-1, 1, 1]) == 0, "例題1 法線と c が垂直")
chk(list(M([1, 2, 3]) + M([1, 0, 1])) == [2, 2, 4], "例題1 λ=1,μ=0 の点")
chk(dot([2, 2, 4], [-1, 1, 1]) == 4, "例題1 その点でも d = 4")
# 例題2
chk(cr([-1, 1, 0], [-1, 0, 1]) == [1, 1, 1], "例題2 法線 (1,1,1)")
chk(dot([1, 0, 0], [1, 1, 1]) == 1, "例題2 d = 1")
chk(dot([0, 1, 0], [1, 1, 1]) == 1, "例題2 B でも 1")
chk(dot([0, 0, 1], [1, 1, 1]) == 1, "例題2 C でも 1")
# 例題3
chk(2 * 2 - 1 + 3 == 6, "例題3 (a) は 6 で平面の上")
chk(2 * 1 - 1 + 1 == 2, "例題3 (b) は 2")
chk(2 != 6, "例題3 (b) は平面の上にない")
chk(6 - 2 == 4, "例題3 ずれは 4")
# 例題4
chk(3 * 4 + 2 * 0 - 0 == 12, "例題4 (4,0,0) は平面の上")
chk(dot([3, 2, -1], [2, -3, 0]) == 0, "例題4 1 本目は法線と垂直")
chk(dot([3, 2, -1], [1, 0, 3]) == 0, "例題4 2 本目は法線と垂直")
chk(cr([2, -3, 0], [1, 0, 3]) == [-9, -6, 3], "例題4 2 方向のベクトル積")
chk(list(M([-9, -6, 3]) + 3 * M([3, 2, -1])) == [0, 0, 0],
    "例題4 それは法線の -3 倍")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(cr([1, 1, 0], [0, 1, 1]) != [0, 0, 0], "演習1 2 方向は平行でない")
# 演習2
chk(cr([2, 0, 1], [1, 1, 0]) == [-1, 1, 2], "演習2 法線 (-1,1,2)")
chk(dot([2, 0, 1], [-1, 1, 2]) == 0, "演習2 垂直（その1）")
chk(dot([1, 1, 0], [-1, 1, 2]) == 0, "演習2 垂直（その2）")
# 演習3
chk(dot([1, 1, 1], [2, -1, 3]) == 4, "演習3 d = 4")
chk(2 * 2 - 0 + 0 == 4, "演習3 (2,0,0) も平面の上")
# 演習4
chk(list(M([5, -2, 1]) * 2) == [10, -4, 2], "演習4 スカラー倍も法線")
# 演習5
chk(3 + 2 * (-1) - 2 == -1, "演習5 平面の上")
chk(3 + 2 * (-1) - 1 == 0, "演習5 (3,-1,1) なら 0")
chk(0 != -1, "演習5 その点は平面の上にない")
# 演習6
_AB6 = M([1, -1, 1])
_AC6 = M([-1, 1, 3])
chk(list(_AB6.cross(_AC6)) == [-4, -4, 0], "演習6 AB×AC = (-4,-4,0)")
chk(list(M([-4, -4, 0]) + 4 * M([1, 1, 0])) == [0, 0, 0], "演習6 -4 倍")
chk(dot([1, 1, 0], [1, 1, 0]) == 2, "演習6 d = 2")
chk(2 + 0 == 2, "演習6 B でも 2")
chk(0 + 2 == 2, "演習6 C でも 2")
chk(M([1, 1, 0])[2] == 0, "演習6 z の係数が 0")
# 演習7
chk(2 * 2 + 0 - 0 == 4, "演習7 (2,0,0) は平面の上")
chk(dot([2, 1, -1], [1, -2, 0]) == 0, "演習7 1 本目は垂直")
chk(dot([2, 1, -1], [0, 1, 1]) == 0, "演習7 2 本目は垂直")
chk(cr([1, -2, 0], [0, 1, 1]) == [-2, -1, 1], "演習7 2 方向のベクトル積")
chk(list(M([-2, -1, 1]) + M([2, 1, -1])) == [0, 0, 0], "演習7 それは法線の -1 倍")
# 演習8
chk(1 - 0 + 1 == 2, "演習8 点は平面の上")
chk(dot([1, 1, 0], [1, -1, 1]) == 0, "演習8 方向は法線と垂直")
chk(sp.expand((1 + _l) - _l + 1 - 2) == 0, "演習8 一般の λ でも成り立つ")
chk(0 - 0 + 0 != 2, "演習8 原点を通る直線なら平面の外")
# 演習9
chk(sp.simplify((_l * _b + _m * (2 * _b)) - (_l + 2 * _m) * _b)
    == M([0, 0, 0]), "演習9 c=2b なら係数が 1 つにまとまる")
# 演習10
chk(list(M([1, 0, 0]) + M([0, 1, 0])) == [1, 1, 0], "演習10 和は (1,1,0)")
chk(cr([1, 0, 0], [0, 1, 0]) == [0, 0, 1], "演習10 ベクトル積は (0,0,1)")
chk(dot([1, 1, 0], [0, 0, 1]) == 0, "演習10 和は xy 平面の中")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Vector equations of a plane:", "シラバス 1 行目を逐語で")
in_text("> $r = a + \\lambda b + \\mu c$, where $b$ and $c$ are non-parallel"
        " vectors within the plane.", "ベクトル方程式を逐語で")
in_text("> $r \\cdot n = a \\cdot n$, where $n$ is a normal to the plane and"
        " $a$ is the position vector of a point on the plane.",
        "内積の形を逐語で")
in_text("> Cartesian equation of a plane $ax + by + cz = d$.",
        "デカルト方程式を逐語で")
in_text("公式集の **3.17** の欄", "公式集の場所")
in_text("> Vector equation of a plane", "公式集の見出しを逐語で")
in_text("> Equation of a plane", "公式集の 2 つ目の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("one point, two directions", "図(a) の題")
in_fig("must lie in the plane and must not be", "図(a) の注")
in_fig("every point of the plane has the same scalar product", "図(b) の題")
in_fig("lies in the plane, so", "図(b) の注")
in_text("$1$ つの点と、$2$ つの向きで平面が決まります。", "キャプション (a)")
in_text("平面の上のどの点でも、$\\mathbf{n}$ との内積は同じ値です。",
        "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("-1 \\\\ 1 \\\\ 2", "演習2"),
                    ("-4 \\\\ -4 \\\\ 0", "演習6")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl317-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl317", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-17-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-17-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-17.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-17.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| plane |", "| normal vector |", "| Cartesian |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 係数が、そのまま法線ベクトルです", "係数が法線")
in_text("## 法線を求めるのに内積を使う", "法線はベクトル積")
in_text("## 法線を約分したときに、$d$ を直し忘れる", "約分したら d も")
in_text("**$\\mathbf{b}$ と $\\mathbf{c}$ が平行でないからこそ、"
        "$\\mathbf{n} \\neq \\mathbf{0}$**", "平行でないから n が 0 でない")
in_text("**まずデカルト形に直す**ほうが速いです。", "デカルト形に直す")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
