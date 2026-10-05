"""AA HL 3.13（内積となす角） の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_13.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-13.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_13.py"), encoding="utf-8").read()
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
k, t_ = sp.symbols("k t")


def dot(u, v):
    return (u.T * v)[0]


def mag(v):
    return sp.sqrt(dot(v, v))


def ang(u, v):
    return sp.acos(sp.simplify(dot(u, v) / (mag(u) * mag(v))))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_u = M(sp.symbols("u1 u2 u3"))
_v = M(sp.symbols("v1 v2 v3"))
_w = M(sp.symbols("w1 w2 w3"))
_k = sp.Symbol("k")
chk(sp.simplify(dot(_v, _w) - dot(_w, _v)) == 0, "交換法則")
chk(sp.simplify(dot(_u, _v + _w) - dot(_u, _v) - dot(_u, _w)) == 0, "分配法則")
chk(sp.simplify(dot(_k * _v, _w) - _k * dot(_v, _w)) == 0, "スカラー倍")
chk(sp.simplify(dot(_v, _v) - mag(_v) ** 2) == 0, "v·v = |v|^2")
chk(sp.simplify(dot(_u + _w, _u - _w) - (mag(_u) ** 2 - mag(_w) ** 2)) == 0,
    "(u+w)·(u-w) = |u|^2-|w|^2")
# 余弦定理からの導出
chk(sp.simplify(mag(_v - _w) ** 2
                - (mag(_v) ** 2 + mag(_w) ** 2 - 2 * dot(_v, _w))) == 0,
    "|v-w|^2 = |v|^2+|w|^2-2 v·w")
# cos θ の範囲
for _p, _q in ((M([1, 0, 0]), M([0, 1, 0])), (M([1, 1, 0]), M([1, 0, 1])),
               (M([2, -1, 3]), M([1, 4, -2]))):
    chk(abs(float(dot(_p, _q) / (mag(_p) * mag(_q)))) <= 1, "|cos θ| <= 1")
# 内積の符号と角
chk(ang(M([1, 0]), M([1, 1])) < sp.pi / 2 and dot(M([1, 0]), M([1, 1])) > 0,
    "正なら鋭角")
chk(dot(M([1, 0]), M([0, 1])) == 0 and ang(M([1, 0]), M([0, 1])) == sp.pi / 2,
    "0 なら直角")
chk(dot(M([1, 0]), M([-1, 1])) < 0 and ang(M([1, 0]), M([-1, 1])) > sp.pi / 2,
    "負なら鈍角")
# 平行なら |v·w| = |v||w|
for _c in (2, -3, sp.Rational(1, 2)):
    _p = M([1, -2, 2])
    chk(sp.simplify(abs(dot(_p, _c * _p)) - mag(_p) * mag(_c * _p)) == 0,
        "平行なら |v·w| = |v||w|: k=%s" % _c)
chk(dot(M([1, 0, 0]), M([-2, 0, 0])) == -2, "向きが逆なら内積は負")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
_a, _b = M([2, -1, 3]), M([1, 4, -2])
chk(dot(_a, _b) == -8, "例題1 (a)")
chk(dot(_b, _a) == -8, "例題1 検算")
chk(dot(_a, _b) < 0, "例題1 (b) 鈍角")
_u2, _w2 = M([1, 1, 0]), M([1, 0, 1])
chk(dot(_u2, _w2) == 1, "例題2 内積")
chk(mag(_u2) == sp.sqrt(2) and mag(_w2) == sp.sqrt(2), "例題2 大きさ")
chk(ang(_u2, _w2) == sp.pi / 3, "例題2 角")
chk(sp.solve(sp.Eq(dot(M([2, k, -3]), M([4, -1, 2])), 0), k) == [2], "例題3")
chk(dot(M([2, 2, -3]), M([4, -1, 2])) == 0, "例題3 検算")
# 例題4（数で）
_a4, _b4 = M([3, 0]), M([0, 3])
chk(dot((_a4 + _b4) / 2, _b4 - _a4) == 0, "例題4 検算（等しいとき）")
_a4b, _b4b = M([4, 0]), M([0, 3])
chk(dot((_a4b + _b4b) / 2, _b4b - _a4b) != 0, "例題4 検算（等しくないとき）")
chk(sp.simplify(dot((_a4b + _b4b) / 2, _b4b - _a4b)
                - sp.Rational(1, 2) * (9 - 16)) == 0, "例題4 値は (|b|^2-|a|^2)/2")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(dot(M([3, -2, 1]), M([-1, 4, 2])) == -9, "演習1")
chk(ang(M([1, 0, 1]), M([0, 1, 1])) == sp.pi / 3, "演習2")
chk(dot(M([1, 0, 1]), M([0, 1, 1])) == 1, "演習2 内積")
chk(sp.solve(sp.Eq(dot(M([1, t_, 3]), M([2, 4, -2])), 0), t_) == [1], "演習3")
chk(dot(M([1, 1, 3]), M([2, 4, -2])) == 0, "演習3 検算")
chk(dot(M([1, 2, 2]), M([2, 1, -2])) == 0, "演習4")
chk(mag(M([1, 2, 2])) == 3 and mag(M([2, 1, -2])) == 3, "演習4 どちらも 0 でない")
chk(3 * 5 * sp.cos(sp.pi / 3) == sp.Rational(15, 2), "演習5")
chk(sp.Rational(15, 2) < 15, "演習5 平行より小さい")
_a6 = M([2, -1, 2])
chk(dot(_a6, _a6) == 9 and mag(_a6) == 3, "演習6")
chk(dot(M([1, 2, 2]), M([1, 2, 2])) == 9, "演習6 検算")
_A7, _B7, _C7 = M([1, 0, 0]), M([0, 1, 0]), M([0, 0, 1])
chk(ang(_B7 - _A7, _C7 - _A7) == sp.pi / 3, "演習7")
chk(mag(_B7 - _A7) == sp.sqrt(2) and mag(_C7 - _A7) == sp.sqrt(2),
    "演習7 どちらも √2")
chk(mag(_C7 - _B7) == sp.sqrt(2), "演習7 正三角形")
_a8, _b8 = M([3, 0]), M([0, 3])
chk(dot(_a8 + _b8, _a8 - _b8) == 0, "演習8 検算")
chk(dot(M([4, 0]), M([4, 0])) - dot(M([0, 3]), M([0, 3])) == 7,
    "演習8 等しくないとき")
_u9, _w9 = M([3, 0]), M([0, 4])
chk(dot(_u9 + _w9, _u9 - _w9) == -7, "演習9 検算")
chk(mag(_u9) ** 2 - mag(_w9) ** 2 == -7, "演習9 右辺")
chk(dot(M([1, 0, 0]), M([-2, 0, 0])) == -2, "演習10 正しい値")
chk(mag(M([1, 0, 0])) * mag(M([-2, 0, 0])) == 2, "演習10 大きさの積は 2")
chk(sp.cos(sp.pi) == -1, "演習10 cos π = -1")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> The definition of the scalar product of two vectors.",
        "シラバス 1 行目を逐語で")
in_text("> The angle between two vectors.", "シラバス 2 行目を逐語で")
in_text("> Perpendicular vectors; parallel vectors.", "シラバス 3 行目を逐語で")
in_text("> Applications of the properties of the scalar product",
        "Guidance の見出しを逐語で")
in_text("> $v \\cdot w = w \\cdot v$;", "交換法則を逐語で")
in_text("> $u \\cdot (v + w) = u \\cdot v + u \\cdot w$;", "分配法則を逐語で")
in_text("> $(kv) \\cdot w = k(v \\cdot w)$;", "スカラー倍を逐語で")
in_text("> $v \\cdot v = \\lvert v \\rvert^{2}$.", "v·v を逐語で")
in_text("> For non-zero vectors $v \\cdot w = 0$ is equivalent to the vectors"
        " being perpendicular", "垂直の同値を逐語で")
in_text("> for parallel vectors $\\lvert v \\cdot w \\rvert = \\lvert v \\rvert"
        " \\lvert w \\rvert$", "平行の性質を逐語で")
in_text("公式集の **3.13** の欄", "公式集の場所")
in_text("> Scalar product", "公式集の見出しを逐語で")
in_text("> Angle between two vectors", "公式集のなす角を逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("The angle between two vectors, and the shadow of one on the other",
       "図(a) の題")
in_fig("this shadow", "図(a) の要点")
in_fig("The sign of the scalar product tells you the kind of angle", "図(b) の題")
in_fig("obtuse", "図(b) の鈍角")
in_text("なす角と、片方をもう片方に落とした影です。", "キャプション (a)")
in_text("内積の符号で、角の種類が分かります。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("t \\\\ 3", "演習3"),
                    ("\\frac{15}{2}", "演習5")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl313-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl313", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-13-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-13-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-13.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-13.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| scalar product |", "| perpendicular |", "| commutative |",
          "| distributive |", "| rhombus |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 答えはスカラーです", "内積は数")
in_text("## 平行の判定には、内積を使いません", "平行の判定")
in_text("**絶対値が付いている**ところに気をつけてください。", "絶対値の見張り")
in_text("**向きをそろえる**ところが要です。", "三角形の角")
in_text("**ベクトルの割り算はありません。**", "割り算はない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
