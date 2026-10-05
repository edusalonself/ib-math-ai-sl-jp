"""AA HL HL 3.14 — The vector equation of a line の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_14.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-14.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_14.py"), encoding="utf-8").read()
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


def mag(v):
    return sp.sqrt(v.dot(v))


def ang(u, v):
    return sp.acos(sp.Abs(u.dot(v)) / (mag(u) * mag(v)))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_l = sp.Symbol("lam")
_a = M(sp.symbols("a1 a2 a3"))
_b = M(sp.symbols("b1 b2 b3"))
_r = _a + _l * _b
# r - a は b のスカラー倍
chk(sp.simplify((_r - _a) - _l * _b) == M([0, 0, 0]), "r-a = λb")
# λ = 0 で a、λ = 1 で a+b
chk(sp.simplify(_r.subs(_l, 0) - _a) == M([0, 0, 0]), "λ=0 で a")
chk(sp.simplify(_r.subs(_l, 1) - (_a + _b)) == M([0, 0, 0]), "λ=1 で a+b")
# 媒介変数表示からデカルト形（λ を消す）
_x0, _y0, _z0, _L, _Mm, _N = sp.symbols("x0 y0 z0 l m n", nonzero=True)
_x, _y, _z = sp.symbols("x y z")
_sol = sp.solve(sp.Eq(_x, _x0 + _l * _L), _l)[0]
chk(sp.simplify(_sol - (_x - _x0) / _L) == 0, "λ = (x-x0)/l")
# 方向をスカラー倍しても、点の集まりは変わらない
_k = sp.Symbol("k", nonzero=True)
_mu = sp.Symbol("mu")
chk(sp.simplify((_a + _mu * (_k * _b)).subs(_mu, _l / _k) - _r)
    == M([0, 0, 0]), "b を k 倍しても同じ直線")
# なす角に a は出てこない
chk(sp.diff(sp.Abs(_b.dot(M([1, 0, 0]))), sp.Symbol("a1")) == 0, "角は a によらない")
# 2 点を通る直線：λ=0 で A、λ=1 で B
_pA = M(sp.symbols("A1 A2 A3"))
_pB = M(sp.symbols("B1 B2 B3"))
_two = _pA + _l * (_pB - _pA)
chk(sp.simplify(_two.subs(_l, 0) - _pA) == M([0, 0, 0]), "2 点：λ=0 で A")
chk(sp.simplify(_two.subs(_l, 1) - _pB) == M([0, 0, 0]), "2 点：λ=1 で B")
# 速さは |b|
_t = sp.Symbol("t", positive=True)
chk(sp.simplify(mag((_a + _t * _b).diff(_t)) - mag(_b)) == 0, "速さ = |b|")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1 A(1,2,-1), b = (2,-1,3)
_A1 = M([1, 2, -1])
_b1 = M([2, -1, 3])
chk(list(_A1 + 1 * _b1) == [3, 1, 2], "例題1 λ=1 で (3,1,2)")
chk(sp.Rational(3 - 1, 2) == 1 and sp.Rational(1 - 2, -1) == 1
    and sp.Rational(2 + 1, 3) == 1, "例題1 (c) デカルト形が 3 つとも 1")
# 例題2 A(1,0,2), B(3,-2,6)
_A2 = M([1, 0, 2])
_B2 = M([3, -2, 6])
chk(list(_B2 - _A2) == [2, -2, 4], "例題2 AB = (2,-2,4)")
chk(list((_B2 - _A2) / 2) == [1, -1, 2], "例題2 約分して (1,-1,2)")
chk(list(_A2 + 2 * M([1, -1, 2])) == [3, -2, 6], "例題2 λ=2 で B")
# 例題3 方向 (1,1,0) と (1,0,1)
_u3 = M([1, 1, 0])
_w3 = M([1, 0, 1])
chk(_u3.dot(_w3) == 1, "例題3 内積 1")
chk(mag(_u3) == sp.sqrt(2) and mag(_w3) == sp.sqrt(2), "例題3 大きさ √2")
chk(sp.simplify(ang(_u3, _w3) - PI / 3) == 0, "例題3 角 π/3")
chk(ang(_u3, _w3) < PI / 2, "例題3 鋭角")
# 例題4 r = (1,2,3)+t(2,-1,2)
_A4 = M([1, 2, 3])
_b4 = M([2, -1, 2])
chk(mag(_b4) == 3, "例題4 速さ 3")
chk(list(_A4 + 2 * _b4) == [5, 0, 7], "例題4 t=2 で (5,0,7)")
chk(sp.solve(sp.Eq(1 + 2 * _t, 4), _t) == [sp.Rational(3, 2)], "例題4 x から t=3/2")
chk(sp.solve(sp.Eq(2 - _t, 1), _t) == [1], "例題4 y から t=1")
chk(sp.Rational(3, 2) != 1, "例題4 t が合わないので通らない")
chk(list(_A4 + sp.Rational(3, 2) * _b4) == [4, sp.Rational(1, 2), 6],
    "例題4 t=3/2 の位置")
chk(list(_A4 + 1 * _b4) == [3, 1, 5], "例題4 t=1 の位置")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
_q1a = M([2, -1, 3])
_q1b = M([1, 4, -2])
chk(list(_q1a + 0 * _q1b) == [2, -1, 3], "演習1 λ=0 で通る点")
chk(list(_q1a + 1 * _q1b) == [3, 3, 1], "演習1 λ=1 で (3,3,1)")
chk(list(M([3, 3, 1]) - _q1a) == [1, 4, -2], "演習1 差が方向ベクトル")
# 演習2
_q2A = M([0, 1, 2])
_q2B = M([4, -1, 0])
chk(list(_q2B - _q2A) == [4, -2, -2], "演習2 AB = (4,-2,-2)")
chk(list((_q2B - _q2A) / 2) == [2, -1, -1], "演習2 約分して (2,-1,-1)")
chk(list(_q2A + 2 * M([2, -1, -1])) == [4, -1, 0], "演習2 λ=2 で B")
# 演習3
_q3A = M([1, 2, 3])
_q3b = M([2, -1, 4])
chk(list(_q3A + 1 * _q3b) == [3, 1, 7], "演習3 λ=1 で (3,1,7)")
chk(sp.Rational(3 - 1, 2) == 1 and sp.Rational(1 - 2, -1) == 1
    and sp.Rational(7 - 3, 4) == 1, "演習3 λ=1 でデカルト形が 1")
chk(list(_q3A - 1 * _q3b) == [-1, 3, -1], "演習3 λ=-1 で (-1,3,-1)")
chk(sp.Rational(-1 - 1, 2) == -1 and sp.Rational(3 - 2, -1) == -1
    and sp.Rational(-1 - 3, 4) == -1, "演習3 λ=-1 でデカルト形が -1")
# 演習4
_q4u = M([1, 1, 0])
_q4w = M([0, 1, 1])
chk(_q4u.dot(_q4w) == 1, "演習4 内積 1")
chk(sp.simplify(ang(_q4u, _q4w) - PI / 3) == 0, "演習4 角 π/3")
chk(sp.simplify(ang(_q4u, M([0, -1, -1])) - PI / 3) == 0, "演習4 逆向きでも π/3")
chk(ang(_q4u, _q4w) <= PI / 2, "演習4 鋭角")
# 演習5
_q5a = M([1, 1, -2])
_q5b = M([3, -3, 3])
_q5P = M([7, -5, 4])
chk(sp.solve([(_q5a + _l * _q5b)[i] - _q5P[i] for i in range(3)], _l)
    == {_l: 2}, "演習5 λ=2 で 3 成分とも合う")
chk(list(_q5a + 2 * _q5b) == [7, -5, 4], "演習5 代入で一致")
chk(sp.solve(sp.Eq(-2 + 3 * _l, 5), _l) == [sp.Rational(7, 3)],
    "演習5 (7,-5,5) なら z から 7/3")
chk(sp.Rational(7, 3) != 2, "演習5 その点は直線の上にない")
# 演習6
_q6b = M([1, 2, -2])
chk(mag(_q6b) == 3, "演習6 速さ 3")
chk(list(M([2, -1, 4]) + 1 * _q6b) == [3, 1, 2], "演習6 t=1 で (3,1,2)")
chk(list(M([3, 1, 2]) - M([2, -1, 4])) == [1, 2, -2], "演習6 1 秒の変位")
# 演習7
_q7A = M([3, 1])
_q7B = M([7, 9])
chk(list(_q7B - _q7A) == [4, 8], "演習7 差 (4,8)")
chk(sp.gcd(4, 8) == 4 and list((_q7B - _q7A) / 4) == [1, 2], "演習7 約分して (1,2)")
chk(list(_q7A + 4 * M([1, 2])) == [7, 9], "演習7 λ=4 で B")
chk(sp.Rational(9 - 1, 7 - 3) == 2, "演習7 傾き 2")
# 演習8
_q8u = M([2, -1, 2])
_q8w = M([1, 2, 0])
chk(_q8u.dot(_q8w) == 0, "演習8 内積 0")
chk(mag(_q8u) == 3 and mag(_q8w) == sp.sqrt(5), "演習8 大きさ 3 と √5")
chk(sp.simplify(ang(_q8u, _q8w) - PI / 2) == 0, "演習8 角 π/2")
chk(M([-2, 1, -2]).dot(_q8w) == 0, "演習8 向きを逆にしても 0")
# 演習9
_q9b = M([1, 1, 1])
chk(list(M([2, 2, 2])) == list(0 * _q9b + 2 * _q9b), "演習9 (2,2,2) は直線の上")
chk(sp.simplify(M([-3, -3, -3]) - (-3) * _q9b) == M([0, 0, 0]),
    "演習9 方向が平行")
chk(sp.solve([(_l * _q9b)[i] - M([0, 1, 0])[i] for i in range(3)], _l) == [],
    "演習9 (0,1,0) は直線の上にない")
# 演習10
_q10a = M([1, 0, 0])
_q10b = M([0, 1, 0])
chk(sp.simplify((_q10a + _mu * (2 * _q10b)).subs(_mu, _l / 2)
                - (_q10a + _l * _q10b)) == M([0, 0, 0]), "演習10 λ=2μ で一致")
chk(list(_q10a + 6 * _q10b) == list(_q10a + 3 * (2 * _q10b)),
    "演習10 λ=6 と μ=3 が同じ点")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Vector equation of a line in two and three dimensions:",
        "シラバス 1 行目を逐語で")
in_text("> $r = a + \\lambda b$.", "式を逐語で")
in_text("> Relevance of $a$ (position) and $b$ (direction).",
        "a と b の役割を逐語で")
in_text("> Knowledge of the following forms for equations of lines:",
        "Guidance を逐語で")
in_text("> Parametric form:", "媒介変数表示の見出しを逐語で")
in_text("> $x = x_{0} + \\lambda l$, $y = y_{0} + \\lambda m$,"
        " $z = z_{0} + \\lambda n$.", "媒介変数表示を逐語で")
in_text("> Cartesian form:", "デカルト形の見出しを逐語で")
in_text("> $\\dfrac{x-x_{0}}{l} = \\dfrac{y-y_{0}}{m} ="
        " \\dfrac{z-z_{0}}{n}$.", "デカルト形を逐語で")
in_text("> The angle between two lines.", "なす角を逐語で")
in_text("> Using the scalar product of the two direction vectors.",
        "内積で出すことを逐語で")
in_text("> Simple applications to kinematics.", "運動への応用を逐語で")
in_text("> Interpretation of $\\lambda$ as time and $b$ as velocity, with"
        " $\\lvert b \\rvert$ representing speed.", "λ と b の読み方を逐語で")
in_text("公式集の **3.14** の欄", "公式集の場所")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("start at", "図(a) の題")
in_fig("then slide along", "図(a) の題の後半")
in_fig("any point of the line is reached by one value of", "図(a) の注")
in_fig("The angle between two lines is the angle between their", "図(b) の題")
in_fig("take the acute angle", "図(b) の注")
in_text("$\\mathbf{a}$ から出発して、$\\mathbf{b}$ の向きに進みます。",
        "キャプション (a)")
in_text("$2$ 直線のなす角は、方向ベクトルのなす角です。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("\\frac{x-1}{2} = \\frac{y-2}{-1} = \\frac{z-3}{4}", "演習3"),
                    ("7 \\\\ -5 \\\\ 4", "演習5")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl314-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl314", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-14-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-14-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-14.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-14.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| vector equation |", "| direction vector |", "| parametric |",
          "| Cartesian |", "| speed |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 通る点と方向を、入れかえる", "点と方向")
in_text("## $2$ 直線のなす角を、鈍角のまま答える", "鈍角のまま")
in_text("## 点が直線上にあるかを、$1$ つの成分だけで確かめる", "1 成分だけ")
in_text("**引き算**です。", "2 点のときは引き算")
in_text("**その $\\lambda$ を残りの成分にも入れて、すべて合うか**", "全成分で確かめる")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
