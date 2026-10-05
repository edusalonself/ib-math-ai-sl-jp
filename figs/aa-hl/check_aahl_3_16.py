"""AA HL HL 3.16 — The vector product の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_16.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-16.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_16.py"), encoding="utf-8").read()
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
    return sp.sqrt(M(v).dot(M(v)))


def cr(v, w):
    return list(M(v).cross(M(w)))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_u = M(sp.symbols("u1 u2 u3"))
_v = M(sp.symbols("v1 v2 v3"))
_w = M(sp.symbols("w1 w2 w3"))
_k = sp.Symbol("k")
# 公式集の成分の形
chk(sp.simplify(_v.cross(_w) - M([_v[1] * _w[2] - _v[2] * _w[1],
                                  _v[2] * _w[0] - _v[0] * _w[2],
                                  _v[0] * _w[1] - _v[1] * _w[0]]))
    == M([0, 0, 0]), "公式集の成分の形と一致")
# 両方に垂直
chk(sp.expand(_v.dot(_v.cross(_w))) == 0, "v·(v×w) = 0")
chk(sp.expand(_w.dot(_v.cross(_w))) == 0, "w·(v×w) = 0")
# 反交換
chk(sp.simplify(_v.cross(_w) + _w.cross(_v)) == M([0, 0, 0]),
    "v×w = -w×v")
# 分配
chk(sp.simplify(_u.cross(_v + _w) - (_u.cross(_v) + _u.cross(_w)))
    == M([0, 0, 0]), "u×(v+w) = u×v + u×w")
# スカラー倍
chk(sp.simplify((_k * _v).cross(_w) - _k * _v.cross(_w)) == M([0, 0, 0]),
    "(kv)×w = k(v×w)")
# 自分自身
chk(sp.simplify(_v.cross(_v)) == M([0, 0, 0]), "v×v = 0")
# 平行なら 0
chk(sp.simplify((_k * _v).cross(_v)) == M([0, 0, 0]), "平行なら v×w = 0")
# Lagrange の恒等式（演習8 の内容）
chk(sp.expand(_v.cross(_w).dot(_v.cross(_w)) + _v.dot(_w) ** 2
              - _v.dot(_v) * _w.dot(_w)) == 0,
    "|v×w|² + (v·w)² = |v|²|w|²")
# 三角形は平行四辺形の半分（BA, BC からでも同じ大きさ）
_AB = M(sp.symbols("b1 b2 b3"))
_AC = M(sp.symbols("c1 c2 c3"))
chk(sp.simplify(_AB.cross(_AC - _AB) - _AB.cross(_AC)) == M([0, 0, 0]),
    "AB×BC = AB×AC")
chk(sp.simplify((-_AB).cross(_AC - _AB) + _AB.cross(_AC)) == M([0, 0, 0]),
    "BA×BC = -(AB×AC)（大きさは同じ）")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(cr([1, 2, 3], [4, 5, 6]) == [-3, 6, -3], "例題1 v×w = (-3,6,-3)")
chk(M([1, 2, 3]).dot(M([-3, 6, -3])) == 0, "例題1 v との内積 0")
chk(M([4, 5, 6]).dot(M([-3, 6, -3])) == 0, "例題1 w との内積 0")
# 例題2
chk(cr([2, -1, 3], [-4, 2, -6]) == [0, 0, 0], "例題2 a×b = 0")
chk(list(M([-4, 2, -6]) + 2 * M([2, -1, 3])) == [0, 0, 0], "例題2 b = -2a")
# 例題3
chk(cr([1, 0, 1], [0, 2, 1]) == [-2, -1, 2], "例題3 ベクトル積")
chk(mag([-2, -1, 2]) == 3, "例題3 面積 3")
chk(M([1, 0, 1]).dot(M([-2, -1, 2])) == 0, "例題3 内積 0（その1）")
chk(M([0, 2, 1]).dot(M([-2, -1, 2])) == 0, "例題3 内積 0（その2）")
chk(M([1, 0, 1]).dot(M([0, 2, 1])) == 1, "例題3 内積は 1")
chk(sp.simplify(mag([1, 0, 1]) * mag([0, 2, 1])
                * sp.sqrt(1 - (sp.Rational(1, 1) / (mag([1, 0, 1])
                                                    * mag([0, 2, 1]))) ** 2)
                - 3) == 0, "例題3 sinθ からも面積 3")
# 例題4
_A, _B, _C = M([1, 0, 0]), M([2, 1, 1]), M([0, 2, 1])
chk(list(_B - _A) == [1, 1, 1], "例題4 AB")
chk(list(_C - _A) == [-1, 2, 1], "例題4 AC")
chk(cr([1, 1, 1], [-1, 2, 1]) == [-1, -2, 3], "例題4 AB×AC")
chk(mag([-1, -2, 3]) == sp.sqrt(14), "例題4 大きさ √14")
chk(sp.simplify(mag([-1, -2, 3]) / 2 - sp.sqrt(14) / 2) == 0,
    "例題4 面積 √14/2")
chk(list(_A - _B) == [-1, -1, -1] and list(_C - _B) == [-2, 1, 0],
    "例題4 BA と BC")
chk(cr([-1, -1, -1], [-2, 1, 0]) == [1, 2, -3], "例題4 BA×BC")
chk(mag([1, 2, -3]) == sp.sqrt(14), "例題4 B から出しても √14")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
chk(cr([1, -1, 2], [3, 0, 1]) == [-1, 5, 3], "演習1 v×w")
chk(M([1, -1, 2]).dot(M([-1, 5, 3])) == 0, "演習1 内積 0（その1）")
chk(M([3, 0, 1]).dot(M([-1, 5, 3])) == 0, "演習1 内積 0（その2）")
# 演習2
chk(cr([2, 3, -1], [2, 3, -1]) == [0, 0, 0], "演習2 u×u = 0")
chk(sp.sin(0) == 0, "演習2 sin 0 = 0")
# 演習3
chk([-x for x in [2, -5, 1]] == [-2, 5, -1], "演習3 符号を変える")
chk(mag([2, -5, 1]) == mag([-2, 5, -1]) == sp.sqrt(30), "演習3 大きさ √30")
# 演習4
chk(cr([3, -6, 9], [-1, 2, -3]) == [0, 0, 0], "演習4 ベクトル積は 0")
chk(list(M([3, -6, 9]) + 3 * M([-1, 2, -3])) == [0, 0, 0], "演習4 -3 倍")
# 演習5
chk(cr([2, 0, 0], [0, 3, 0]) == [0, 0, 6], "演習5 ベクトル積")
chk(mag([0, 0, 6]) == 6, "演習5 面積 6")
chk(M([2, 0, 0]).dot(M([0, 3, 0])) == 0, "演習5 2 辺は垂直")
chk(2 * 3 * sp.sin(PI / 2) == 6, "演習5 長方形として 2×3")
# 演習6
chk(cr([1, 2, 0], [3, 1, 0]) == [0, 0, -5], "演習6 ベクトル積")
chk(sp.Rational(mag([0, 0, -5]), 2) == sp.Rational(5, 2), "演習6 面積 5/2")
chk(cr([3, 1, 0], [1, 2, 0]) == [0, 0, 5], "演習6 順番を変えると符号が逆")
chk(sp.Abs((1) * (1) - (2) * (3)) / 2 == sp.Rational(5, 2),
    "演習6 2 次元の公式でも 5/2")
# 演習7
chk(cr([1, 1, 0], [0, 1, 1]) == [1, -1, 1], "演習7 ベクトル積")
chk(M([1, 1, 0]).dot(M([1, -1, 1])) == 0, "演習7 内積 0（その1）")
chk(M([0, 1, 1]).dot(M([1, -1, 1])) == 0, "演習7 内積 0（その2）")
chk(mag([1, -1, 1]) == sp.sqrt(3), "演習7 大きさ √3")
# 演習8
_v8, _w8 = M([1, 2, 2]), M([2, -1, 0])
chk(_v8.cross(_w8).dot(_v8.cross(_w8)) + _v8.dot(_w8) ** 2 == 45,
    "演習8 左辺は 45")
chk(_v8.dot(_v8) * _w8.dot(_w8) == 45, "演習8 右辺も 45")
chk(_v8.dot(_v8) == 9 and _w8.dot(_w8) == 5, "演習8 9 と 5")
# 演習9
chk(M([1, 0, 0]).dot(M([0, 1, 0])) == 0, "演習9 垂直の例は内積 0")
chk(cr([1, 0, 0], [0, 1, 0]) == [0, 0, 1], "演習9 そのベクトル積は 0 でない")
chk(M([1, 0, 0]).dot(M([2, 0, 0])) == 2, "演習9 平行の例は内積 2")
chk(cr([1, 0, 0], [2, 0, 0]) == [0, 0, 0], "演習9 そのベクトル積は 0")
chk(sp.cos(PI / 2) == 0 and sp.sin(0) == 0 and sp.sin(PI) == 0,
    "演習9 cos と sin が 0 になる角")
# 演習10
chk(sp.simplify(_AB.cross(_AC - _AB) - _AB.cross(_AC)) == M([0, 0, 0]),
    "演習10 大きさは偶然合う")
chk(sp.Rational(1, 2) != 1, "演習10 1/2 のほうは合わない")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> The definition of the vector product of two vectors.",
        "シラバス 1 行目を逐語で")
in_text('> The vector product is also known as the "cross product".',
        "cross product を逐語で")
in_text("> $v \\times w = \\lvert v \\rvert \\lvert w \\rvert \\sin\\theta\\,"
        " n$, where $\\theta$ is the angle between $v$ and $w$, and $n$ is"
        " the unit normal vector whose direction is given by the right-hand"
        " screw rule.", "定義を逐語で")
in_text("> Properties of the vector product.", "性質の見出しを逐語で")
in_text("> $v \\times w = - w \\times v$;", "反交換を逐語で")
in_text("> $u \\times (v + w) = u \\times v + u \\times w$;", "分配を逐語で")
in_text("> $(kv) \\times w = k(v \\times w)$;", "スカラー倍を逐語で")
in_text("> $v \\times v = 0$.", "v×v を逐語で")
in_text("> For non-zero vectors $v \\times w = 0$ is equivalent to the"
        " vectors being parallel.", "平行の同値を逐語で")
in_text("> Geometric interpretation of $\\lvert v \\times w \\rvert$",
        "幾何的な意味を逐語で")
in_text("> Use of $\\lvert v \\times w \\rvert$ to find the area of a"
        " parallelogram (and hence a triangle).", "面積への応用を逐語で")
in_text("公式集の **3.16** の欄", "公式集の場所")
in_text("> Vector product", "公式集の見出しを逐語で")
in_text("> Area of a parallelogram", "公式集の面積を逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("the area of the parallelogram is", "図(a) の題")
in_fig("height", "図(a) の高さ")
in_fig("points at you", "図(a) の向き")
in_fig("a triangle is half of the parallelogram", "図(b) の題")
in_fig("other half", "図(b) のもう半分")
in_text("平行四辺形の面積が、ベクトル積の大きさです。", "キャプション (a)")
in_text("三角形は、平行四辺形の半分です。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("-1 \\\\ 5 \\\\ 3", "演習1"),
                    ("1 \\\\ -1 \\\\ 1", "演習7")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl316-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl316", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-16-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-16-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-16.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-16.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| vector product |", "| cross product |", "| parallelogram |",
          "| normal vector |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 答えを数で書く", "答えはベクトル")
in_text("## 平行の判定に内積を使う", "平行はベクトル積")
in_text("## 三角形で $\\dfrac{1}{2}$ を忘れる", "1/2 を忘れない")
in_text("**同じ頂点から出す**のがきまりです。", "同じ頂点から")
in_text("**$1 \\to 2 \\to 3 \\to 1$ の輪**", "添字の輪")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
