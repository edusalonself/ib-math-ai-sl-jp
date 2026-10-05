"""AA HL 3.11（三角関数の関係式とグラフの対称性） の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_11.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-11.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_11.py"), encoding="utf-8").read()
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

th, a = sp.symbols("theta a")
PI = sp.pi
S, C, T = sp.sin, sp.cos, sp.tan


def zero(e, msg):
    chk(sp.simplify(e) == 0, msg + "  (%s)" % e)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの関係式
# ══════════════════════════════════════════════════════════
zero(S(PI - th) - S(th), "sin(π-θ)")
zero(C(PI - th) + C(th), "cos(π-θ)")
zero(T(PI - th) + T(th), "tan(π-θ)")
zero(S(-th) + S(th), "sin(-θ)")
zero(C(-th) - C(th), "cos(-θ)")
zero(T(-th) + T(th), "tan(-θ)")
zero(S(PI + th) + S(th), "sin(π+θ)")
zero(C(PI + th) + C(th), "cos(π+θ)")
zero(T(PI + th) - T(th), "tan(π+θ)")
zero(S(PI / 2 - th) - C(th), "sin(π/2-θ)")
zero(C(PI / 2 - th) - S(th), "cos(π/2-θ)")
zero(S(PI / 2 + th) - C(th), "sin(π/2+θ)")
zero(C(PI / 2 + th) + S(th), "cos(π/2+θ)")
# 加法定理からの導出
chk(S(PI) == 0 and C(PI) == -1, "sin π = 0, cos π = -1")
zero(S(PI) * C(th) - C(PI) * S(th) - S(th), "§3 sin の導出")
zero(C(PI) * C(th) + S(PI) * S(th) + C(th), "§3 cos の導出")
chk(S(PI / 2) == 1 and C(PI / 2) == 0, "sin π/2 = 1, cos π/2 = 0")
# グラフの対称性としての読み
zero(S(PI / 2 + a) - S(PI / 2 - a), "§6 sin の線対称")
zero(C(PI / 2 + a) + C(PI / 2 - a), "§6 cos の点対称")
chk(sp.simplify((th + (PI - th)) / 2 - PI / 2) == 0, "2 角の平均は π/2")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
chk(S(2 * PI / 3) == sp.sqrt(3) / 2 and S(PI / 3) == sp.sqrt(3) / 2,
    "例題1 検算 sin")
chk(C(2 * PI / 3) == sp.Rational(-1, 2) and C(PI / 3) == sp.Rational(1, 2),
    "例題1 検算 cos")
chk(1 - sp.Rational(4, 9) == sp.Rational(5, 9), "例題2 cos^2")
chk(sp.sqrt(sp.Rational(5, 9)) == sp.sqrt(5) / 3, "例題2 √(5/9)")
chk(sp.Rational(4, 9) + sp.Rational(5, 9) == 1, "例題2 検算")
chk(PI - PI / 5 == 4 * PI / 5, "例題3 (a) の角")
chk(PI + PI / 5 == 6 * PI / 5, "例題3 (b) の角")
chk(PI / 2 - PI / 5 == 3 * PI / 10, "例題3 (c) の角")
chk(sp.simplify(S(4 * PI / 5) - S(PI / 5)) == 0, "例題3 (a)")
chk(sp.simplify(S(6 * PI / 5) + S(PI / 5)) == 0, "例題3 (b)")
chk(sp.simplify(C(3 * PI / 10) - S(PI / 5)) == 0, "例題3 (c)")
chk(C(PI / 3) == sp.Rational(1, 2) and C(2 * PI / 3) == sp.Rational(-1, 2),
    "例題4 検算")
chk(sp.simplify(PI / 2 - PI / 3 - (2 * PI / 3 - PI / 2)) == 0,
    "例題4 π/2 から等しく離れている")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(S(3 * PI / 4) == S(PI / 4), "演習1 検算 sin")
chk(T(3 * PI / 4) == -1 and T(PI / 4) == 1, "演習1 検算 tan")
chk(-sp.Rational(-1, 4) == sp.Rational(1, 4), "演習2 (a)")
chk(PI - PI / 7 == 6 * PI / 7 and PI + PI / 7 == 8 * PI / 7, "演習3 の角")
chk(PI / 2 - PI / 7 == 5 * PI / 14, "演習3 (c) の角")
chk(sp.simplify(S(6 * PI / 7) - S(PI / 7)) == 0, "演習3 (a)")
chk(sp.simplify(S(8 * PI / 7) + S(PI / 7)) == 0, "演習3 (b)")
chk(sp.simplify(C(5 * PI / 14) - S(PI / 7)) == 0, "演習3 (c)")
chk(5 * PI / 14 + PI / 7 == PI / 2, "演習3 検算（余角）")
chk(C(PI) == -1 and C(4 * PI / 3) == sp.Rational(-1, 2), "演習4 検算")
zero(S(PI - th) * C(-th) + C(PI - th) * S(-th) - S(2 * th), "演習5")
chk(sp.simplify(S(PI / 3) - sp.sqrt(3) / 2) == 0, "演習5 検算 π/6")
chk(T(2 * PI / 3) == -sp.sqrt(3) and T(PI / 3) == sp.sqrt(3), "演習6 検算")
chk(sp.solveset(sp.Eq(S(PI - th), C(th)), th, sp.Interval(0, 2 * PI))
    == sp.FiniteSet(PI / 4, 5 * PI / 4), "演習7 の解")
chk(S(PI / 6) == sp.Rational(1, 2) and S(5 * PI / 6) == sp.Rational(1, 2),
    "演習8 検算")
chk(S(PI / 2) == 1 and C(0) == 1, "演習9 検算 θ=0")
chk(S(PI) == 0 and C(PI / 2) == 0, "演習9 検算 θ=π/2")
chk(C(2 * PI / 3) == sp.Rational(-1, 2), "演習10 正しい値")
chk(-1 - sp.Rational(1, 2) == sp.Rational(-3, 2), "演習10 生徒の値")
chk(sp.Rational(-3, 2) < -1, "演習10 それは cos の値になりえない")

# ══════════════════════════════════════════════════════════
# 3. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Relationships between trigonometric functions and the symmetry"
        " properties of their graphs.", "シラバス本体を逐語で")
in_text("> $\\sin(\\pi - \\theta) = \\sin\\theta$", "Guidance sin を逐語で")
in_text("> $\\cos(\\pi - \\theta) = -\\cos\\theta$", "Guidance cos を逐語で")
in_text("> $\\tan(\\pi - \\theta) = -\\tan\\theta$", "Guidance tan を逐語で")
in_text("> Link to: the unit circle (SL3.5), odd and even functions (AHL2.14),"
        " compound angles (AHL3.10).", "Link to を逐語で")
in_text("## 公式集には、この項目の欄がありません", "公式集にないことを書く")
not_in_text("公式集の **3.11**", "ありもしない欄を書かない")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("$\\\\theta$ and $\\\\pi-\\\\theta$: same height, opposite across",
       "図(a) の題")
in_fig("the $y$-values agree, the $x$-values are negatives", "図(a) の要点")
in_fig("folds about", "図(b) の左")
in_fig("half turn", "図(b) の右")
in_text("$\\theta$ と $\\pi-\\theta$ は、高さが同じで横が逆です。", "キャプション (a)")
in_text("$\\sin$ は $x = \\dfrac{\\pi}{2}$ で折り返せ、"
        "$\\cos$ は $\\left(\\dfrac{\\pi}{2},\\ 0\\right)$ で半回転できます。",
        "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("\\dfrac{1}{4}", "演習2"), ("\\pi}{7}", "演習3"),
                    ("\\cos(\\pi+\\theta) = -\\cos\\theta$ を示", "演習4")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl311-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl311", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-11-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-11-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-11.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-11.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| symmetry property |", "| complementary angles |",
          "| supplementary angles |", "| in terms of |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("**$\\sin$ だけが符号を変えません。**", "sin はそのまま")
in_text("**$\\tan$ だけ、符号が戻ります。**", "tan は戻る")
in_text("## 迷ったら、$\\theta = \\dfrac{\\pi}{6}$ で試す", "確かめ方")
in_text("## $\\dfrac{\\pi}{2}-\\theta$ と $\\pi-\\theta$ を取りちがえる", "取りちがえ")
in_text("**式と図は、同じことの別の見方です。**", "式と図")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
