"""AA HL 3.12（ベクトルの基本） の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_12.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-12.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_12.py"), encoding="utf-8").read()
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
k, t_, lam = sp.symbols("k t lambda")


def mag(v):
    return sp.sqrt(sum(x ** 2 for x in v))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_a = M(sp.symbols("a1 a2 a3"))
_b = M(sp.symbols("b1 b2 b3"))
_k = sp.Symbol("k", positive=True)
chk(sp.simplify(mag(_k * _a) - _k * mag(_a)) == 0, "|k v| = k |v| （k > 0）")
chk(sp.simplify(mag(_a / mag(_a)) - 1) == 0, "単位ベクトルの大きさは 1")
chk(sp.simplify((_b - _a) + (_a - _b)) == sp.zeros(3, 1), "AB と BA は逆向き")
chk(sp.simplify(mag(_b - _a) - mag(_a - _b)) == 0, "距離は向きによらない")
chk(sp.simplify((_a + _b) / 2 - _a - ((_b - _a) / 2)) == sp.zeros(3, 1),
    "中点：AM = (b-a)/2")
chk(sp.simplify(_b - (_a + _b) / 2 - ((_b - _a) / 2)) == sp.zeros(3, 1),
    "中点：MB = (b-a)/2")
# 平行なのに 1 成分だけでは決まらない例
chk(sp.simplify(M([4, 6]) - 2 * M([2, 4])) != sp.zeros(2, 1),
    "(2,4) と (4,6) は平行でない")
chk(sp.Rational(4, 2) != sp.Rational(6, 4), "その k が合わない")
# 三角不等式
for _u, _w in ((M([1, 0, 0]), M([-1, 0, 0])), (M([3, 0, 0]), M([0, 4, 0])),
               (M([1, 2, 2]), M([2, -1, 2]))):
    chk(mag(_u + _w) <= mag(_u) + mag(_w), "三角不等式: %s %s" % (_u.T, _w.T))
chk(mag(M([3, 0, 0]) + M([6, 0, 0])) == mag(M([3, 0, 0])) + mag(M([6, 0, 0])),
    "同じ向きなら等号")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
_A, _B = M([1, 2, -1]), M([4, 0, 3])
chk(_B - _A == M([3, -2, 4]), "例題1 (a)")
chk(mag(_B - _A) == sp.sqrt(29), "例題1 (b)")
chk(mag(_A - _B) == sp.sqrt(29), "例題1 検算")
chk(3 - (-1) == 4, "例題1 z 成分")
_v = M([2, -1, 2])
chk(mag(_v) == 3, "例題2 (a)")
chk(_v / 3 == M([sp.Rational(2, 3), sp.Rational(-1, 3), sp.Rational(2, 3)]),
    "例題2 (b)")
chk(mag(_v / 3) == 1, "例題2 検算")
_aa, _bb = M([2, -1, 3]), M([1, 0, -2])
chk(3 * _aa - 2 * _bb == M([4, -3, 13]), "例題3 (a)")
chk(3 * _aa == M([6, -3, 9]), "例題3 (b) の 3a")
chk(sp.solve(sp.Eq(6, 2 * k), k) == [3], "例題3 k = 3")
chk(3 * (-1) == -3, "例題3 t = -3")
# 例題4（中点の証明）を数で
_a4, _b4 = M([4, 0]), M([0, 6])
chk(_b4 / 2 - _a4 / 2 == (_b4 - _a4) / 2, "例題4 MN = AB/2")
chk(_b4 / 2 - _a4 / 2 == M([-2, 3]), "例題4 検算 MN")
chk(_b4 - _a4 == M([-4, 6]), "例題4 検算 AB")
chk(mag(M([-2, 3])) == sp.sqrt(13) and mag(M([-4, 6])) == 2 * sp.sqrt(13),
    "例題4 検算 長さ")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(M([5, 1, 0]) - M([2, -1, 4]) == M([3, 2, -4]), "演習1")
chk(mag(M([3, 2, -4])) == sp.sqrt(29), "演習1 距離")
chk(5 ** 2 < 29 < 6 ** 2, "演習1 √29 は 5 と 6 のあいだ")
chk(mag(M([3, 4])) == 5, "演習2")
chk(sp.Rational(3, 5) ** 2 + sp.Rational(4, 5) ** 2 == 1, "演習2 検算")
_q3 = 2 * M([1, -2, 2]) + M([3, 0, -1])
chk(_q3 == M([5, -4, 3]), "演習3")
chk(mag(_q3) == 5 * sp.sqrt(2), "演習3 大きさ")
chk(sp.simplify(mag(_q3) - (2 * 3 + sp.sqrt(10))) != 0, "演習3 和とはちがう")
chk(-2 * M([-1, 3, 3]) == M([2, -6, -6]), "演習4")
chk(sp.solve(sp.Eq(2, -k), k) == [-2], "演習4 k = -2")
_AB5 = M([3, -2, 4]) - M([1, 0, 2])
chk(_AB5 == M([2, -2, 2]), "演習5 AB")
chk(sp.solve(sp.Eq(-2, -2 * lam), lam) == [1], "演習5 λ = 1")
chk(sp.solve(sp.Eq(k - 3, 2), k) == [5], "演習5 k = 5")
chk(M([5, -4, 6]) - M([3, -2, 4]) == M([2, -2, 2]), "演習5 検算 BC")
chk(M([5, -4, 6]) - M([1, 0, 2]) == 2 * _AB5, "演習5 検算 AC")
chk(mag(M([2, -3, 6])) == 7, "演習6 大きさ")
chk(-M([2, -3, 6]) / 7
    == M([sp.Rational(-2, 7), sp.Rational(3, 7), sp.Rational(-6, 7)]), "演習6")
chk(mag(-M([2, -3, 6]) / 7) == 1, "演習6 検算")
_a7, _c7 = M([4, 0]), M([1, 3])
chk(_a7 + _c7 == M([5, 3]), "演習7 OB")
chk(_c7 - _a7 == M([-3, 3]), "演習7 AC")
_a8, _b8 = M([0, 0]), M([4, 6])
chk((_a8 + _b8) / 2 == M([2, 3]), "演習8 検算")
_a9, _b9 = M([4, 0]), M([0, 6])
chk((_a9 + _b9) / 2 == M([2, 3]), "演習9 OC の中点")
chk((_a9 + _b9) / 2 == (_a9 + _b9) / 2, "演習9 AB の中点も同じ")
chk(mag(M([1, 0, 0]) + M([-1, 0, 0])) == 0, "演習10 左辺は 0")
chk(mag(M([1, 0, 0])) + mag(M([-1, 0, 0])) == 2, "演習10 右辺は 2")
chk(mag(M([3, 0]) + M([0, 4])) == 5 and 3 + 4 == 7, "演習10 検算")
chk(mag(M([3, 0]) + M([6, 0])) == 9 and 3 + 6 == 9, "演習10 同じ向きなら等号")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Concept of a vector; position vectors; displacement vectors.",
        "シラバス 1 行目を逐語で")
in_text("> Representation of vectors using directed line segments.",
        "シラバス 2 行目を逐語で")
in_text("> Base vectors $\\mathbf{i}$, $\\mathbf{j}$, $\\mathbf{k}$.",
        "シラバス 3 行目を逐語で")
in_text("> Components of a vector:", "シラバス 4 行目を逐語で")
in_text("> - the sum and difference of two vectors", "Algebraic approaches 1")
in_text("> - the zero vector $\\mathbf{0}$, the vector $-\\mathbf{v}$",
        "Algebraic approaches 2")
in_text("> - multiplication by a scalar, $k\\mathbf{v}$, parallel vectors",
        "Algebraic approaches 3")
in_text("> - magnitude of a vector, $\\lvert\\mathbf{v}\\rvert$; unit vectors,"
        " $\\dfrac{\\mathbf{v}}{\\lvert\\mathbf{v}\\rvert}$",
        "Algebraic approaches 4")
in_text("> Proofs of geometrical properties using vectors.",
        "シラバス 最後の行を逐語で")
in_text("> Distance between points A and B is the magnitude of"
        " $\\overrightarrow{AB}$", "Guidance を逐語で")
in_text("公式集の **3.12** の欄", "公式集の場所")
in_text("> Magnitude of a vector", "公式集の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("From $O$ to $A$ and to $B$, then across from $A$ to $B$", "図(a) の題")
in_fig("go back along $\\\\mathbf{a}$, then out along $\\\\mathbf{b}$",
       "図(a) の要点")
in_fig("the parallelogram rule", "図(b) の左")
in_fig("a scalar keeps the line, not the length", "図(b) の右")
in_text("$O$ から $A$、$O$ から $B$、そして $A$ から $B$ へ。", "キャプション (a)")
in_text("平行四辺形の規則と、スカラー倍です。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("5 \\\\ 1 \\\\ 0", "演習1"), ("3\\mathbf{i}+4\\mathbf{j}", "演習2"),
                    ("5\\sqrt{2}", "演習3"), ("2 \\\\ -3 \\\\ 6", "演習6")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))

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
chk(len(re.findall(r"^::: \{#exm-aahl312-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl312", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head, "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は 1 つだけ")
not_in_text("**この節ですること：", "節の頭の 1 文は置かない")
chk(TEXT.count("\\vec{") == 2,
    "\\vec{ は手書きの話の 2 か所だけ: %d" % TEXT.count("\\vec{"))
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
    _p = os.path.join(BASE, "img", "aahl-3-12-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-12-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-12.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-12.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| position vector |", "| displacement vector |", "| base vector |",
          "| unit vector |", "| collinear |", "| bisect |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 手書きでは、太字が書けません", "手書きの注意")
in_text("**「後ろ引く前」ではなく「行き先引く出発点」**です。", "AB の向き")
in_text("**$1$ つの成分だけで決めないでください。**", "平行の判定")
in_text("## $2$ 点を結ぶベクトルだけは、矢印で書きます", "AB の書き方")
in_text("**大きさで割るだけ**です。", "単位ベクトル")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
