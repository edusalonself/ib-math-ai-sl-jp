"""AA HL 3.10（加法定理と 2 倍角） の内容を検算する。

    python3 figs/aa-hl/check_aahl_3_10.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "aahl-3-10.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_3_10.py"), encoding="utf-8").read()
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

A, B, th = sp.symbols("A B theta")
PI = sp.pi
S, C, T = sp.sin, sp.cos, sp.tan


def zero(e, msg):
    chk(sp.simplify(e) == 0, msg + "  (%s)" % e)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの恒等式
# ══════════════════════════════════════════════════════════
zero(S(A + B) - (S(A) * C(B) + C(A) * S(B)), "sin(A+B)")
zero(S(A - B) - (S(A) * C(B) - C(A) * S(B)), "sin(A-B)")
zero(C(A + B) - (C(A) * C(B) - S(A) * S(B)), "cos(A+B)")
zero(C(A - B) - (C(A) * C(B) + S(A) * S(B)), "cos(A-B)")
zero(T(A + B) - (T(A) + T(B)) / (1 - T(A) * T(B)), "tan(A+B)")
zero(T(A - B) - (T(A) - T(B)) / (1 + T(A) * T(B)), "tan(A-B)")
zero(S(2 * th) - 2 * S(th) * C(th), "sin 2θ")
zero(C(2 * th) - (C(th) ** 2 - S(th) ** 2), "cos 2θ 形 1")
zero(C(2 * th) - (2 * C(th) ** 2 - 1), "cos 2θ 形 2")
zero(C(2 * th) - (1 - 2 * S(th) ** 2), "cos 2θ 形 3")
zero(sp.expand_trig(T(2 * th)) - 2 * T(th) / (1 - T(th) ** 2), "tan 2θ")
zero(C(3 * th) - (4 * C(th) ** 3 - 3 * C(th)), "cos 3θ")
zero((S(th) + C(th)) ** 2 - (1 + S(2 * th)), "(sin+cos)^2")
# sin(A+B) ≠ sin A + sin B
chk(sp.sin(PI) != sp.sin(PI / 2) + sp.sin(PI / 2), "sin(A+B) ≠ sin A + sin B")
chk(sp.sin(PI) == 0 and sp.sin(PI / 2) + sp.sin(PI / 2) == 2, "その値")
# 複号の確かめ（A = B = π/2）
chk(sp.cos(PI) == -1, "cos π = -1")
chk(C(PI / 2) * C(PI / 2) - S(PI / 2) * S(PI / 2) == -1, "cos(A+B) は - で合う")
chk(C(PI / 2) * C(PI / 2) + S(PI / 2) * S(PI / 2) == 1, "+ だと合わない")
# De Moivre からの導出
_th = sp.Symbol("th_real", real=True)
_z = sp.expand((sp.cos(_th) + sp.I * sp.sin(_th)) ** 2)
zero(sp.re(_z) - (sp.cos(_th) ** 2 - sp.sin(_th) ** 2), "De Moivre 実部")
zero(sp.im(_z) - 2 * sp.sin(_th) * sp.cos(_th), "De Moivre 虚部")
zero(_z - (sp.cos(2 * _th) + sp.I * sp.sin(2 * _th)), "De Moivre そのもの")
# tan 2θ の分母が 0 になる角
for _k in range(-2, 3):
    chk(sp.simplify(sp.tan(PI / 4 + _k * PI / 2) ** 2) == 1,
        "tan^2 = 1 の角: k=%d" % _k)

# ══════════════════════════════════════════════════════════
# 1. The idea と例題
# ══════════════════════════════════════════════════════════
chk(PI / 3 - PI / 4 == PI / 12, "§3 π/12 = π/3 - π/4")
chk(sp.simplify(C(PI / 3) * C(PI / 4) + S(PI / 3) * S(PI / 4)
                - (sp.sqrt(2) + sp.sqrt(6)) / 4) == 0, "例題1 cos(π/12)")
chk(sp.simplify(C(PI / 12) - (sp.sqrt(2) + sp.sqrt(6)) / 4) == 0, "例題1 検算")
chk(abs(float((sp.sqrt(2) + sp.sqrt(6)) / 4) - 0.9659) < 1e-3, "例題1 大きさ")
chk(sp.sqrt(1 - sp.Rational(9, 25)) == sp.Rational(4, 5), "例題2 cos A")
chk(sp.sqrt(1 - sp.Rational(25, 169)) == sp.Rational(12, 13), "例題2 sin B")
chk(sp.Rational(3, 5) * sp.Rational(5, 13) + sp.Rational(4, 5) * sp.Rational(12, 13)
    == sp.Rational(63, 65), "例題2 (a)")
chk(sp.Rational(4, 5) * sp.Rational(5, 13) - sp.Rational(3, 5) * sp.Rational(12, 13)
    == sp.Rational(-16, 65), "例題2 cos(A+B)")
chk(sp.Rational(63, 65) / sp.Rational(-16, 65) == sp.Rational(-63, 16), "例題2 (b)")
chk(sp.Rational(63, 65) ** 2 + sp.Rational(16, 65) ** 2 == 1, "例題2 検算")
chk(sp.solveset(sp.Eq(C(2 * th) + 3 * S(th), 2), th, sp.Interval(0, 2 * PI))
    == sp.FiniteSet(PI / 6, PI / 2, 5 * PI / 6), "例題3 の解")
eq(sp.expand((2 * sp.Symbol("s") - 1) * (sp.Symbol("s") - 1)),
   2 * sp.Symbol("s") ** 2 - 3 * sp.Symbol("s") + 1, "例題3 因数分解")
chk(C(PI / 3) + 3 * S(PI / 6) == 2, "例題3 検算 π/6")
chk(C(PI) + 3 * S(PI / 2) == 2, "例題3 検算 π/2")
_t = sp.Symbol("t")
chk(sp.solve(sp.Eq(_t ** 2 + 2 * _t - 1, 0), _t)
    == [-1 + sp.sqrt(2), -sp.sqrt(2) - 1], "例題4 の 2 解")
chk(sp.simplify(T(PI / 8) - (sp.sqrt(2) - 1)) == 0, "例題4 tan(π/8)")
chk(sp.expand((sp.sqrt(2) - 1) ** 2) == 3 - 2 * sp.sqrt(2), "例題4 t^2")
chk(sp.simplify((2 * (sp.sqrt(2) - 1)) / (1 - (3 - 2 * sp.sqrt(2))) - 1) == 0,
    "例題4 検算 2 倍角に戻す")
chk(-sp.sqrt(2) - 1 < 0 and sp.sqrt(2) - 1 > 0, "例題4 符号で捨てる")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(PI / 3 + PI / 4 == 7 * PI / 12, "演習1 の分解")
chk(sp.simplify(S(PI / 3) * C(PI / 4) + C(PI / 3) * S(PI / 4)
                - (sp.sqrt(2) + sp.sqrt(6)) / 4) == 0, "演習1")
chk(sp.simplify(S(7 * PI / 12) - S(5 * PI / 12)) == 0, "演習1 検算（補角）")
chk(sp.radsimp((sp.sqrt(3) - 1) / (1 + sp.sqrt(3))) == 2 - sp.sqrt(3), "演習2")
chk(sp.simplify(T(PI / 12) - (2 - sp.sqrt(3))) == 0, "演習2 検算")
chk(sp.expand((2 - sp.sqrt(3)) * (2 + sp.sqrt(3))) == 1, "演習2 検算（積が 1）")
chk(sp.simplify(T(5 * PI / 12) - (2 + sp.sqrt(3))) == 0, "演習2 tan(5π/12)")
chk(sp.sqrt(1 - sp.Rational(64, 289)) == sp.Rational(15, 17), "演習3 sin A")
chk(sp.sqrt(1 - sp.Rational(16, 25)) == sp.Rational(3, 5), "演習3 cos B")
chk(sp.Rational(8, 17) * sp.Rational(3, 5) + sp.Rational(15, 17) * sp.Rational(4, 5)
    == sp.Rational(84, 85), "演習3")
chk(8 ** 2 + 15 ** 2 == 17 ** 2, "演習3 三平方")
chk(S(PI / 2) == 1 and 2 * S(PI / 4) * C(PI / 4) == 1, "演習4 検算 π/4")
chk(sp.solveset(sp.Eq(C(2 * th), S(th)), th, sp.Interval(0, 2 * PI))
    == sp.FiniteSet(PI / 6, 5 * PI / 6, 3 * PI / 2), "演習5 の解")
eq(sp.expand((2 * sp.Symbol("s") - 1) * (sp.Symbol("s") + 1)),
   2 * sp.Symbol("s") ** 2 + sp.Symbol("s") - 1, "演習5 因数分解")
chk(C(3 * PI) == -1 and S(3 * PI / 2) == -1, "演習5 検算 3π/2")
chk(sp.solveset(sp.Eq(S(2 * th), C(th)), th, sp.Interval(0, 2 * PI))
    == sp.FiniteSet(PI / 6, PI / 2, 5 * PI / 6, 3 * PI / 2), "演習6 の解")
chk(S(PI) == 0 and C(PI / 2) == 0, "演習6 検算 π/2")
chk((S(PI / 4) + C(PI / 4)) ** 2 == 2 and 1 + S(PI / 2) == 2, "演習7 検算")
chk(sp.simplify(T(PI / 3) - sp.sqrt(3)) == 0, "演習8 検算 左辺")
chk(sp.radsimp((2 / sp.sqrt(3)) / (1 - sp.Rational(1, 3))) == sp.sqrt(3),
    "演習8 検算 右辺")
chk(C(0) == 1 and 4 * 1 - 3 * 1 == 1, "演習9 検算 θ=0")
chk(C(PI) == -1 and 4 * sp.Rational(1, 8) - 3 * sp.Rational(1, 2) == -1,
    "演習9 検算 θ=π/3")
chk(C(0) == 1, "演習10 左辺は 1")
chk(C(PI / 3) * C(PI / 3) - S(PI / 3) * S(PI / 3) == sp.Rational(-1, 2),
    "演習10 生徒の式は -1/2")
chk(C(PI / 3) * C(PI / 3) + S(PI / 3) * S(PI / 3) == 1, "演習10 正しい式は 1")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Compound angle identities.", "シラバス 1 行目を逐語で")
in_text("> Double angle identity for tan.", "シラバス 2 行目を逐語で")
in_text("> Derivation of double angle identities from compound angle"
        " identities.", "Guidance を逐語で")
in_text("> Link to: De Moivre's theorem (AHL1.14).", "Link to を逐語で")
in_text("公式集の **3.10** の欄", "公式集の場所")
in_text("> $\\sin(A \\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B$", "公式集 sin")
in_text("> $\\cos(A \\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B$", "公式集 cos")
in_text("> $\\tan(A \\pm B) = \\dfrac{\\tan A \\pm \\tan B}"
        "{1 \\mp \\tan A\\tan B}$", "公式集 tan")
in_text("> $\\tan 2\\theta = \\dfrac{2\\tan\\theta}{1 - \\tan^{2}\\theta}$",
        "公式集 tan 2θ")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("A picture behind $\\\\sin(A+B)$", "図(a) の題")
in_fig("it splits into two pieces, one from each triangle", "図(a) の要点")
in_fig("Put $B = A$ and the double angle identities drop out", "図(b) の題")
in_fig("the booklet prints the left column; the right one you derive",
       "図(b) の要点")
in_text("$\\sin(A+B)$ の図です。", "キャプション (a)")
in_text("加法定理に $B = A$ を入れると、$2$ 倍角が出ます。", "キャプション (b)")
for leak in ["63", "84", "sqrt(3)-1"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("7\\pi}{12", "演習1"), ("\\tan\\dfrac{\\pi}{12}", "演習2"),
                    ("8}{17", "演習3"), ("\\cos 2\\theta = \\sin\\theta", "演習5"),
                    ("4\\cos^{3}", "演習9")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl310-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl310", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-3-10-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-3-10-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/03-geometry-and-trigonometry/aahl-3-10.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry-and-trigonometry/aahl-3-10.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| compound angle identity |", "| double angle identity |",
          "| upper sign / lower sign |", "| quadrant |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## $\\sin(A+B)$ は $\\sin A + \\sin B$ ではありません", "分けられない")
in_text("## 迷ったら、$A = B = \\dfrac{\\pi}{2}$ で試す", "符号の確かめ方")
in_text("## $3$ つの形は、使い分けます", "cos 2θ の形")
in_text("**分母が $0$ になる $\\theta$ では使えません。**", "tan 2θ の注意")
in_text("**$\\sin$ は同じ、$\\cos$ は逆**と覚えておいてください。", "複号の覚え方")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
