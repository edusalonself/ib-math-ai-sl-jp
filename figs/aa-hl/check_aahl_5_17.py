"""AA HL HL 5.17 — Areas with respect to the y-axis and volumes of revolution の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_17.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-17.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_17.py"), encoding="utf-8").read()
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



_x = sp.Symbol("x", positive=True)
_y = sp.Symbol("y", positive=True)
PI = sp.pi
R = sp.Rational


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_r, _h = sp.symbols("r h", positive=True)
# 円錐の公式が出る
chk(sp.simplify(PI * sp.integrate((_r / _h * _x) ** 2, (_x, 0, _h))
                - PI * _r ** 2 * _h / 3) == 0, "直線を回すと円錐の公式")
# 球の公式が出る
chk(sp.simplify(PI * sp.integrate(_r ** 2 - sp.Symbol("t") ** 2,
                                  (sp.Symbol("t"), -_r, _r))
                - R(4, 3) * PI * _r ** 3) == 0, "半円を回すと球の公式")
# 2 乗の差と差の 2 乗はちがう
chk(PI * (2 ** 2 - 1 ** 2) == 3 * PI, "2 乗の差は 3π")
chk(PI * (2 - 1) ** 2 == PI, "差の 2 乗は π")
chk(3 * PI != PI, "この 2 つはちがう")
# x 軸側と y 軸側で長方形になる
chk(sp.integrate(sp.sqrt(_y), (_y, 0, 4))
    + sp.integrate(_x ** 2, (_x, 0, 2)) == 8, "2 つの面積の和は長方形")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(sp.integrate(sp.sqrt(_y), (_y, 0, 4)) == R(16, 3), "例題1 面積 16/3")
chk(sp.integrate(_x ** 2, (_x, 0, 2)) == R(8, 3), "例題1 x 軸側は 8/3")
chk(R(16, 3) + R(8, 3) == 8, "例題1 足すと 8")
chk(sp.integrate(sp.sqrt(_y), _y) == R(2, 3) * _y ** R(3, 2),
    "例題1 √y の原始関数")
# 例題2
chk(PI * sp.integrate(_x ** 4, (_x, 0, 2)) == R(32, 5) * PI,
    "例題2 体積 32π/5")
chk(PI * 4 ** 2 * 2 == 32 * PI, "例題2 円柱なら 32π")
chk(sp.simplify(R(32, 5) * PI / (32 * PI) - R(1, 5)) == 0,
    "例題2 円柱の 1/5")
# 例題3
chk(PI * sp.integrate(_y, (_y, 0, 4)) == 8 * PI, "例題3 体積 8π")
chk(PI * 2 ** 2 * 4 == 16 * PI, "例題3 円柱なら 16π")
chk(sp.simplify(8 * PI / (16 * PI) - R(1, 2)) == 0, "例題3 円柱の半分")
# 例題4
chk(PI * sp.integrate(_x ** 2 - _x ** 4, (_x, 0, 1)) == R(2, 15) * PI,
    "例題4 体積 2π/15")
chk(PI * sp.integrate(_x ** 2, (_x, 0, 1)) == PI / 3, "例題4 外側だけなら π/3")
chk(PI * sp.integrate(_x ** 4, (_x, 0, 1)) == PI / 5, "例題4 内側だけなら π/5")
chk(sp.simplify(PI / 3 - PI / 5 - R(2, 15) * PI) == 0, "例題4 差が答え")
chk(R(1, 2) > R(1, 4), "例題4 x=1/2 では線が上")
chk(sp.solve(sp.Eq(_x, _x ** 2), _x) == [1], "例題4 交点（x>0 では 1）")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(sp.integrate(_y ** 2, (_y, 0, 2)) == R(8, 3), "演習1 面積 8/3")
chk(sp.integrate(sp.log(_y), (_y, 1, sp.E)) == 1, "演習2 面積 1")
chk(sp.simplify((_y * sp.log(_y) - _y).subs(_y, sp.E)
                - (_y * sp.log(_y) - _y).subs(_y, 1) - 1) == 0,
    "演習2 原始関数から 1")
chk(sp.simplify(sp.integrate(sp.exp(_x), (_x, 0, 1)) - (sp.E - 1)) == 0,
    "演習2 x 軸側は e-1")
chk(sp.simplify(1 + (sp.E - 1) - sp.E) == 0, "演習2 足すと e")
chk(PI * sp.integrate(_x, (_x, 0, 4)) == 8 * PI, "演習3 体積 8π")
chk(PI * 2 ** 2 * 4 == 16 * PI, "演習3 円柱なら 16π")
chk(PI * sp.integrate(4 * _x ** 2, (_x, 0, 3)) == 36 * PI, "演習4 体積 36π")
chk(sp.simplify(R(1, 3) * PI * 6 ** 2 * 3 - 36 * PI) == 0, "演習4 円錐の公式")
chk((2 * _x).subs(_x, 3) == 6, "演習4 底面の半径は 6")
chk(PI * sp.integrate(_y ** R(2, 3), (_y, 0, 8)) == R(96, 5) * PI,
    "演習5 体積 96π/5")
chk(sp.Integer(8) ** R(5, 3) == 32, "演習5 8^(5/3) = 32")
chk(PI * 2 ** 2 * 8 == 32 * PI, "演習5 円柱なら 32π")
chk(PI * sp.integrate(sp.sin(_x) ** 2, (_x, 0, PI)) == PI ** 2 / 2,
    "演習6 体積 π²/2")
chk(sp.simplify(sp.sin(_x) ** 2 - (1 - sp.cos(2 * _x)) / 2) == 0,
    "演習6 2 倍角")
chk(sp.sin(2 * PI) == 0 and sp.sin(0) == 0, "演習6 sin の項は消える")
chk(sp.integrate(sp.sqrt(_y), (_y, 1, 4)) == R(14, 3), "演習7 面積 14/3")
chk(R(16, 3) - R(2, 3) == R(14, 3), "演習7 引き算でも同じ")
chk(PI * sp.integrate(4 - _y, (_y, 0, 4)) == 8 * PI, "演習8 体積 8π")
chk(sp.solve(sp.Eq(4 - _x ** 2, 0), _x) == [2], "演習8 x 切片は 2")
chk(PI * 2 ** 2 * 4 == 16 * PI, "演習8 円柱なら 16π")
chk(sp.simplify(8 * PI / (16 * PI) - R(1, 2)) == 0, "演習8 ちょうど半分")
# 演習9
chk(sp.simplify(PI * _y ** 2 - PI * _y) != 0, "演習9 πy² と πy はちがう")
# 演習10
chk(PI * (2 ** 2 - 1 ** 2) * 3 == 9 * PI, "演習10 正しくは 9π")
chk(PI * (2 - 1) ** 2 * 3 == 3 * PI, "演習10 生徒の答えは 3π")
chk(PI * 2 ** 2 * 3 == 12 * PI, "演習10 外側の円柱は 12π")
chk(PI * 1 ** 2 * 3 == 3 * PI, "演習10 内側の円柱は 3π")
chk(12 * PI - 3 * PI == 9 * PI, "演習10 差は 9π")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Area of the region enclosed by a curve and the y-axis in a given"
        " interval.", "シラバス 1 行目を逐語で")
in_text("> Volumes of revolution about the x-axis or y-axis.",
        "回転体を逐語で")
in_text("公式集の **5.17** の欄", "公式集の場所")
in_text("> Area of region enclosed by a curve and y-axis",
        "公式集の面積の見出しを逐語で")
in_text("> Volume of revolution about the x or y-axes",
        "公式集の体積の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("area between a curve and the $y$-axis", "図(a) の題")
in_fig("each strip has area", "図(a) の注")
in_fig("a stack of circular discs", "図(b) の題")
in_fig("each disc has volume", "図(b) の注")
in_text("よこ長の細い長方形を積みます。", "キャプション (a)")
in_text("の円板を積みます。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("\\frac{96\\pi}{5}", "演習5"), ("\\frac{\\pi^{2}}{2}", "演習6")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl517-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl517", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-5-17-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-17-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/05-calculus/aahl-5-17.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-17.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| volume of revolution |", "| definite integral |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## $y$ を $2$ 乗するのを忘れる", "2 乗する")
in_text("## $\\pi$ を書き忘れる", "π を書く")
in_text("## 上端・下端に、もう一方の変数の値を使う", "上端・下端")
in_text("## $2$ 曲線のとき、差を $2$ 乗する", "2 乗の差")
in_text("**$2$ 乗してから引く**、と覚えてください。", "2 乗してから引く")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
