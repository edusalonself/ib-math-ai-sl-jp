"""AA HL HL 3.15 — Coincident, parallel, intersecting and skew lines の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_15.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-15.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_15.py"), encoding="utf-8").read()
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


def mag(v):
    return sp.sqrt(v.dot(v))


def ang(u, v):
    return sp.acos(sp.Abs(u.dot(v)) / (mag(u) * mag(v)))


def par(b1, b2):
    """方向が平行か（外積が 0）。"""
    return M(b1).cross(M(b2)).norm() == 0


def meet(a1, b1, a2, b2):
    """交点の媒介変数。解がなければ空。"""
    a1, b1, a2, b2 = map(M, (a1, b1, a2, b2))
    return sp.solve([(a1 + _l * b1)[i] - (a2 + _m * b2)[i] for i in range(3)],
                    [_l, _m], dict=True)


def on_line(a1, b1, p):
    """点 p が直線 a1+λb1 の上にあるか。"""
    a1, b1, p = map(M, (a1, b1, p))
    return sp.solve([(a1 + _l * b1)[i] - p[i] for i in range(3)], _l, dict=True)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a1 = M(sp.symbols("p1 p2 p3"))
_b1 = M(sp.symbols("q1 q2 q3"))
_k = sp.Symbol("k", nonzero=True)
# 平行なら、方向を k 倍しても直線は変わらない
chk(sp.simplify((_a1 + _m * (_k * _b1)).subs(_m, _l / _k) - (_a1 + _l * _b1))
    == M([0, 0, 0]), "方向を k 倍しても同じ直線")
# 平行な 2 直線が 1 点を共有したら一致（点と向きで直線が決まる）
_c = sp.Symbol("c")
chk(sp.simplify((_a1 + _c * _b1) + _l * (_k * _b1)
                - (_a1 + (_c + _l * _k) * _b1)) == M([0, 0, 0]),
    "共有点をもつ平行な直線は同じ点の集まり")
# 同じ文字にすると別の条件になる
_a2 = M(sp.symbols("r1 r2 r3"))
_b2 = M(sp.symbols("s1 s2 s3"))
_same = [(_a1 + _l * _b1)[i] - (_a2 + _l * _b2)[i] for i in range(3)]
_diff = [(_a1 + _l * _b1)[i] - (_a2 + _m * _b2)[i] for i in range(3)]
chk(len(sp.Matrix(_same).free_symbols & {_l, _m}) == 1
    and len(sp.Matrix(_diff).free_symbols & {_l, _m}) == 2,
    "同じ文字だと未知数が 1 つに減る")
# 2 次元なら、平行でなければかならず解ける
_d1 = M([sp.Symbol("u1"), sp.Symbol("u2")])
_d2 = M([sp.Symbol("w1"), sp.Symbol("w2")])
_det = _d1[0] * (-_d2[1]) - (-_d2[0]) * _d1[1]
chk(sp.simplify(_det - (-(_d1[0] * _d2[1] - _d1[1] * _d2[0]))) == 0,
    "2 次元は行列式で決まる（平行でなければ 0 でない）")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1 平行だが一致でない
chk(par([2, -1, 4], [4, -2, 8]), "例題1 方向が平行")
chk(list(M([4, -2, 8]) - 2 * M([2, -1, 4])) == [0, 0, 0], "例題1 k = 2")
chk(sp.solve(sp.Eq(1 + 2 * _l, 0), _l) == [sp.Rational(-1, 2)],
    "例題1 x から λ = -1/2")
chk(2 - sp.Rational(-1, 2) == sp.Rational(5, 2), "例題1 そのとき y = 5/2")
chk(3 + 4 * sp.Rational(-1, 2) == 1, "例題1 そのとき z = 1")
chk(on_line([1, 2, 3], [2, -1, 4], [0, 0, 0]) == [], "例題1 原点は l1 の上にない")
chk(meet([1, 2, 3], [2, -1, 4], [0, 0, 0], [4, -2, 8]) == [], "例題1 交わらない")
# 例題2 交わる
chk(not par([1, 1, 0], [1, 1, 1]), "例題2 方向は平行でない")
_s2 = meet([1, 0, 1], [1, 1, 0], [4, 3, 3], [1, 1, 1])
chk(_s2 == [{_l: 1, _m: -2}], "例題2 λ=1, μ=-2")
chk(list(M([1, 0, 1]) + 1 * M([1, 1, 0])) == [2, 1, 1], "例題2 交点 (2,1,1)")
chk(list(M([4, 3, 3]) - 2 * M([1, 1, 1])) == [2, 1, 1], "例題2 l2 でも同じ点")
# 例題3 ねじれ
chk(not par([1, 1, 0], [0, 1, 1]), "例題3 方向は平行でない")
chk(meet([1, 2, 3], [1, 1, 0], [2, 0, 1], [0, 1, 1]) == [], "例題3 交わらない")
chk(sp.solve(sp.Eq(1 + _l, 2), _l) == [1], "例題3 x から λ = 1")
chk(sp.solve(sp.Eq(3, 1 + _m), _m) == [2], "例題3 z から μ = 2")
chk(2 + 1 != 2, "例題3 y が合わない（3 ≠ 2）")
chk(3 != 1 + 3, "例題3 μ=3 なら z が合わない")
# 例題4 一致
chk(par([1, 3, -2], [-2, -6, 4]), "例題4 方向が平行")
chk(list(M([-2, -6, 4]) + 2 * M([1, 3, -2])) == [0, 0, 0], "例題4 k = -2")
chk(on_line([2, -1, 4], [1, 3, -2], [4, 5, 0]) == [{_l: 2}], "例題4 λ=2 で一致")
chk(on_line([4, 5, 0], [-2, -6, 4], [2, -1, 4]) == [{_l: 1}], "例題4 逆も成り立つ")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(par([1, -2, 3], [-2, 4, -6]), "演習1 平行")
chk(list(M([-2, 4, -6]) + 2 * M([1, -2, 3])) == [0, 0, 0], "演習1 k = -2")
chk(not par([1, -2, 3], [-2, 4, -5]), "演習1 -5 なら平行でない")
chk(sp.Rational(-5, 3) != -2, "演習1 3 番目の比だけちがう")
# 演習2
chk(par([2, 0, 1], [4, 0, 2]), "演習2 平行")
chk(on_line([1, 1, 1], [2, 0, 1], [3, 1, 2]) == [{_l: 1}], "演習2 一致")
chk(on_line([3, 1, 2], [4, 0, 2], [1, 1, 1]) == [{_l: sp.Rational(-1, 2)}],
    "演習2 逆から見ても μ = -1/2 で合う")
# 演習3
chk(par([1, 1, 1], [1, 1, 1]), "演習3 平行")
chk(on_line([0, 1, 2], [1, 1, 1], [1, 0, 0]) == [], "演習3 一致ではない")
chk(not par([1, -1, -2], [1, 1, 1]), "演習3 2 点の差は方向と平行でない")
# 演習4
chk(not par([1, 2, 1], [2, -1, 0]), "演習4 平行でない")
_s4 = meet([1, -2, -1], [1, 2, 1], [1, 3, 1], [2, -1, 0])
chk(_s4 == [{_l: 2, _m: 1}], "演習4 λ=2, μ=1")
chk(list(M([1, -2, -1]) + 2 * M([1, 2, 1])) == [3, 2, 1], "演習4 交点 (3,2,1)")
chk(list(M([1, 3, 1]) + 1 * M([2, -1, 0])) == [3, 2, 1], "演習4 l2 でも同じ点")
# 演習5
chk(not par([1, 1, 0], [1, -1, 0]), "演習5 平行でない")
chk(meet([1, 0, 0], [1, 1, 0], [0, 0, 1], [1, -1, 0]) == [], "演習5 ねじれ")
chk(sp.solve([1 + _l - _m, _l + _m], [_l, _m], dict=True)
    == [{_l: sp.Rational(-1, 2), _m: sp.Rational(1, 2)}],
    "演習5 x と y だけなら解ける（影は交わる）")
chk(0 != 1, "演習5 z が 0 と 1 で合わない")
# 演習6
chk(par([1, -1, 2], [2, -2, 4]), "演習6 平行")
chk(on_line([2, 1, 3], [1, -1, 2], [5, -2, 9]) == [{_l: 3}], "演習6 λ=3 で一致")
chk(1 - 3 == -2 and 3 + 2 * 3 == 9, "演習6 残りの 2 成分も合う")
# 演習7
chk(not par([1, 0, 1], [0, 1, 1]), "演習7 平行でない")
_s7 = meet([1, 1, 0], [1, 0, 1], [2, 0, 0], [0, 1, 1])
chk(_s7 == [{_l: 1, _m: 1}], "演習7 λ=1, μ=1")
chk(list(M([1, 1, 0]) + 1 * M([1, 0, 1])) == [2, 1, 1], "演習7 交点 (2,1,1)")
chk(list(M([2, 0, 0]) + 1 * M([0, 1, 1])) == [2, 1, 1], "演習7 l2 でも同じ点")
chk(sp.simplify(ang(M([1, 0, 1]), M([0, 1, 1])) - PI / 3) == 0, "演習7 角 π/3")
chk(M([1, 0, 1]).dot(M([0, 1, 1])) == 1, "演習7 内積 1（鋭角）")
# 演習8
_kk, _cc = sp.symbols("kk cc")
_s8 = sp.solve([_kk - 2 * _cc, 2 - _cc, -2 + _cc], [_kk, _cc], dict=True)
chk(_s8 == [{_cc: 2, _kk: 4}], "演習8 k = 4, c = 2")
chk(par([2, 1, -1], [4, 2, -2]), "演習8 k=4 なら平行")
chk(on_line([1, 2, 3], [2, 1, -1], [0, 0, 0]) == [], "演習8 原点は l1 の上にない")
chk(2 - sp.Rational(1, 2) == sp.Rational(3, 2), "演習8 λ=-1/2 で y = 3/2")
chk(3 + sp.Rational(1, 2) == sp.Rational(7, 2), "演習8 λ=-1/2 で z = 7/2")
# 演習9
chk(sp.solve([_l - 0, 1 + _m - 0], [_l, _m], dict=True) == [{_l: 0, _m: -1}],
    "演習9 2 次元の例は交わる")
chk(meet([0, 0, 0], [1, 0, 0], [0, 1, 1], [0, 1, 0]) == [],
    "演習9 高さをずらすと交わらない")
# 演習10
chk(meet([0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]) == [{_l: 1, _m: -1}],
    "演習10 2 文字なら交わる")
chk(sp.solve([(M([0, 0, 0]) + _l * M([1, 0, 0]))[i]
              - (M([1, 1, 0]) + _l * M([0, 1, 0]))[i] for i in range(3)],
             _l, dict=True) == [], "演習10 同じ文字だと解が消える")
chk(list(M([0, 0, 0]) + 1 * M([1, 0, 0])) == [1, 0, 0], "演習10 交点は (1,0,0)")

# ══════════════════════════════════════════════════════════
# 3. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Coincident, parallel, intersecting and skew lines, distinguishing"
        " between these cases.", "シラバス 1 行目を逐語で")
in_text("> Points of intersection.", "シラバス 2 行目を逐語で")
in_text("> Skew lines are non-parallel lines that do not intersect in"
        " three-dimensional space.", "ねじれの位置の定義を逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("Two lines in three dimensions: four possibilities", "図(a) の題")
in_fig("coincident: the same line twice", "図(a) 一致")
in_fig("parallel, but not the same line", "図(a) 平行")
in_fig("intersecting: they meet once", "図(a) 交わる")
in_fig("skew: they never meet", "図(a) ねじれ")
in_fig("passes behind", "図(a) 奥を通る")
in_fig("How to tell the four cases apart", "図(b) の題")
in_fig("are the directions parallel?", "図(b) 最初の問い")
in_fig("the two parameters need different letters", "図(b) の注")
in_text("$2$ 直線の関係は $4$ 通りです。", "キャプション (a)")
in_text("流れ図にすると、判定は $2$ 段階です。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("3 \\\\ 2 \\\\ 1", "演習4"),
                    ("k = 4", "演習8")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl315-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl315", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-15-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-15-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-15.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-15.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| coincident |", "| skew lines |", "| intersect |",
          "| point of intersection |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## $2$ 直線に同じ文字の媒介変数を使う", "媒介変数は 2 文字")
in_text("## $2$ 本の式だけで「交わる」と結論する", "3 本目の確認")
in_text("## ねじれの位置を、$2$ 次元でも起こると考える", "2 次元にねじれはない")
in_text("**$3$ 本目を確かめて初めて**交わると言えます", "3 本目が要")
in_text("**ねじれの位置は、$3$ 次元になって初めて現れる場合**です", "3 次元だけ")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
