"""AA HL 2.16（絶対値・逆数などのグラフと、絶対値の方程式・不等式）の内容を検算する。

    python3 figs/aa-hl/check_aahl_2_16.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "02-functions")
QMD = os.path.join(BASE, "aahl-2-16.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_2_16.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x = sp.Symbol("x", real=True)
R = sp.S.Reals
oo = sp.oo
I, U, FS = sp.Interval, sp.Union, sp.FiniteSet


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


def solves(rel, want, msg):
    got = sp.solveset(rel, x, R)
    chk(got == want, "%s: %s のはずが %s" % (msg, want, got))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_A, _k = sp.symbols("A k", real=True)
# |A| = k の 2 通り
for _kv in (1, 3, 7):
    chk(sp.solveset(sp.Eq(abs(_A), _kv), _A, R) == FS(-_kv, _kv),
        "|A| = %d の解は ±%d" % (_kv, _kv))
chk(sp.solveset(sp.Eq(abs(_A), -2), _A, R) == sp.EmptySet, "|A| = -2 に解はない")
chk(sp.solveset(sp.Eq(abs(_A), 0), _A, R) == FS(0), "|A| = 0 の解は 1 つ")
chk(sp.solveset(abs(_A) > -2, _A, R) == R, "|A| > -2 はすべての実数")
# |A| < k と -k < A < k
for _kv in (1, 4):
    chk(sp.solveset(abs(_A) < _kv, _A, R) == I.open(-_kv, _kv),
        "|A| < %d はあいだ" % _kv)
    chk(sp.solveset(abs(_A) > _kv, _A, R)
        == U(I.open(-oo, -_kv), I.open(_kv, oo)), "|A| > %d は外側" % _kv)
# f(|x|) は even
_ff = x ** 2 - 2 * x - 3
_g = _ff.subs(x, abs(x))
for _v in (-4, -2.5, -1, 0, 1, 2.5, 4):
    chk(sp.simplify(_g.subs(x, _v) - _g.subs(x, -_v)) == 0,
        "f(|x|) は even: x=%s" % _v)
# 逆数は大小を入れかえる（同符号）
for _a, _b in ((1, 2), (2, 5), (-5, -2), (-9, -5)):
    chk((sp.Rational(1, _a) > sp.Rational(1, _b)) == (_a < _b),
        "逆数で大小が逆: %s, %s" % (_a, _b))
# |A|^2 = A^2
eq(abs(_A) ** 2, _A ** 2, "|A|^2 = A^2")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
eq(sp.factor(_ff), (x - 3) * (x + 1), "§ 例の因数分解")
chk(sorted(sp.solve(_ff, x)) == [-1, 3], "§ 例の零点")
chk(sorted(sp.solve(sp.Eq(_ff.subs(x, abs(x)), 0), x)) == [-3, 3],
    "§2 f(|x|) の零点は ±3")
chk(_ff.subs(x, abs(x)).subs(x, -1) == -4, "§2 x=-1 では 0 でない")
# §3 の例 f(x) = x-2
chk(sp.solve(sp.Eq(x - 2, 0), x) == [2], "§3 垂直漸近線 x=2")
chk(sp.solve(sp.Eq(x - 2, 1), x) == [3] and sp.solve(sp.Eq(x - 2, -1), x) == [1],
    "§3 交点は x=1, 3")
chk(sp.limit(1 / (x - 2), x, oo) == 0, "§3 水平漸近線 y=0")
# §4 中身が 0 になる x
_a, _b, _p = sp.symbols("a b p")
chk(sp.solve(sp.Eq(_a * x + _b, _p), x) == [(_p - _b) / _a], "§4 中身の式")
# §6・§7 の例
solves(sp.Eq(abs(2 * x - 3), 5), FS(-1, 4), "§6")
solves(abs(x - 2) < 3, I.open(-1, 5), "§7")
solves(abs(2 * x + 1) >= 5, U(I(-oo, -3), I(2, oo)), "§7 の 2 つ目")

# ══════════════════════════════════════════════════════════
# 2. 例題
# ══════════════════════════════════════════════════════════
chk(sorted(sp.solve(_ff, x)) == [-1, 3], "例題1 (a)")
eq(sp.expand(_ff.subs(x, -x)), x ** 2 + 2 * x - 3, "例題1 左側の枝")
eq(sp.factor(x ** 2 + 2 * x - 3), (x - 1) * (x + 3), "例題1 左側の因数分解")
chk(sorted(sp.solve(sp.Eq(_ff.subs(x, abs(x)), 0), x)) == [-3, 3], "例題1 (b)")
chk(_ff.subs(x, 3) == 0 and _ff.subs(x, 1) == -4, "例題1 検算")
chk(sp.solve(sp.Eq(2 * x + 1, -1), x) == [-1]
    and sp.solve(sp.Eq(2 * x + 1, 3), x) == [1], "例題2 (a)")
for _v in (-1, 1):
    chk((2 * _v + 1) in (-1, 3), "例題2 検算 x=%s" % _v)
chk(sp.solve(sp.Eq((x + 1) ** 2 * (x - 3) ** 2, 0), x) == [-1, 3],
    "例題2 (b) 零点は変わらない")
for _v in (-2, 0, 4):
    chk(((_v + 1) ** 2 * (_v - 3) ** 2) > 0, "例題2 (b) 2 乗は正: x=%s" % _v)
solves(sp.Eq(abs(2 * x - 3), 5), FS(-1, 4), "例題3 (a)")
solves(sp.Eq(abs(x - 1), abs(2 * x + 3)), FS(-4, sp.Rational(-2, 3)), "例題3 (b)")
chk(abs(sp.Integer(-4) - 1) == 5 and abs(2 * sp.Integer(-4) + 3) == 5,
    "例題3 検算 x=-4")
chk(abs(sp.Rational(-2, 3) - 1) == sp.Rational(5, 3)
    and abs(2 * sp.Rational(-2, 3) + 3) == sp.Rational(5, 3),
    "例題3 検算 x=-2/3")
solves(abs(3 * x - 1) < 5, I.open(sp.Rational(-4, 3), 2), "例題4 (a)")
solves(abs(x + 2) >= 4, U(I(-oo, -6), I(2, oo)), "例題4 (b)")
chk(abs(3 * sp.Integer(0) - 1) == 1, "例題4 検算 x=0")
chk(abs(3 * sp.Integer(2) - 1) == 5, "例題4 端では 5")

# ══════════════════════════════════════════════════════════
# 3. 演習
# ══════════════════════════════════════════════════════════
chk(abs(sp.Integer(0) - 3) == 3, "演習1 y 切片は 3")
chk(abs(sp.Integer(3) - 3) == 0, "演習1 頂点は (3, 0)")
chk(abs(sp.Integer(5) - 3) == 2 and abs(sp.Integer(1) - 3) == 2, "演習1 検算")
chk(sp.solve(sp.Eq(abs(x), 2), x) == [-2, 2], "演習2 零点は ±2")
chk(sp.solveset(sp.Eq(abs(x), -4), x, R) == sp.EmptySet, "演習2 -4 は使われない")
chk(sp.solve(sp.Eq(3 * x, 1), x) == [sp.Rational(1, 3)]
    and sp.solve(sp.Eq(3 * x, 5), x) == [sp.Rational(5, 3)], "演習3 (a)")
chk(sp.solve(sp.Eq(x - 2, 1), x) == [3]
    and sp.solve(sp.Eq(x - 2, 5), x) == [7], "演習3 (b)")
solves(sp.Eq(abs(4 * x + 1), 9), FS(sp.Rational(-5, 2), 2), "演習4")
chk(abs(4 * sp.Rational(-5, 2) + 1) == 9, "演習4 検算")
solves(sp.Eq(abs(2 * x - 5), abs(x + 1)), FS(sp.Rational(4, 3), 6), "演習5")
chk(abs(2 * sp.Rational(4, 3) - 5) == sp.Rational(7, 3)
    and abs(sp.Rational(4, 3) + 1) == sp.Rational(7, 3), "演習5 検算")
solves(abs(x - 4) <= 2, I(2, 6), "演習6")
chk(abs(sp.Integer(7) - 4) == 3, "演習6 検算 x=7")
solves(abs(3 * x + 2) > 7, U(I.open(-oo, -3), I.open(sp.Rational(5, 3), oo)),
       "演習7")
chk(abs(3 * sp.Integer(-4) + 2) == 10 and abs(3 * sp.Integer(0) + 2) == 2,
    "演習7 検算")
_F8 = x ** 2 - 9
chk(sorted(sp.solve(_F8, x)) == [-3, 3], "演習8 (a) 垂直漸近線")
chk(sp.limit(1 / _F8, x, oo) == 0, "演習8 (a) 水平漸近線")
chk(_F8.subs(x, 0) == -9 and sp.Rational(1, -9) == sp.Rational(-1, 9),
    "演習8 (b) x=0 では -1/9")
chk(_F8.subs(x, 2) == -5, "演習8 検算 f(2) = -5")
chk(sp.Rational(-1, 9) > sp.Rational(-1, 5), "演習8 -1/9 のほうが大きい")
chk(sp.nsimplify(_F8.subs(x, sp.Rational(29, 10))) == sp.Rational(-59, 100),
    "演習8 検算 x=2.9")
chk(sp.Rational(-100, 59) < sp.Rational(-1, 9), "演習8 漸近線に近いほど小さい")
solves(abs(x - 1) < abs(x + 3), I.open(-1, oo), "演習9")
eq(sp.expand((x - 1) ** 2), x ** 2 - 2 * x + 1, "演習9 左辺の 2 乗")
eq(sp.expand((x + 3) ** 2), x ** 2 + 6 * x + 9, "演習9 右辺の 2 乗")
chk(abs(sp.Integer(0) - 1) == 1 and abs(sp.Integer(0) + 3) == 3, "演習9 検算 x=0")
chk(abs(sp.Integer(-2) - 1) == 3 and abs(sp.Integer(-2) + 3) == 1,
    "演習9 検算 x=-2")
chk(abs(sp.Integer(-1) - 1) == 2 and abs(sp.Integer(-1) + 3) == 2,
    "演習9 境目では等しい")
solves(abs(2 * x - 1) > 3, U(I.open(-oo, -1), I.open(2, oo)), "演習10")
chk(abs(2 * sp.Integer(0) - 1) == 1, "演習10 x=0 は満たさない")
chk(sp.Integer(0) > -1, "演習10 生徒の答えには x=0 が入る")
chk(abs(2 * sp.Integer(3) - 1) == 5 and abs(2 * sp.Integer(-2) - 1) == 5,
    "演習10 検算")

# ══════════════════════════════════════════════════════════
# 4. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> The graphs of the functions, $y = \\lvert f(x) \\rvert$ and"
        " $y = f(\\lvert x \\rvert)$, $y = \\dfrac{1}{f(x)}$, $y = f(ax+b)$,"
        " $y = [f(x)]^{2}$.", "シラバス本体を逐語で")
in_text("> Solution of modulus equations and inequalities.",
        "シラバス（方程式・不等式）を逐語で")
in_text("> Dynamic graphing packages could be used to investigate these"
        " transformations.", "Guidance を逐語で")
in_text("> Example: $\\lvert 3x\\arccos(x) \\rvert > 1$", "Example を逐語で")
not_in_text("公式集の **2.16**", "ありもしない欄を書かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 5. GDC / 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("`abs(`", "TI-Nspire の入力")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl216-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl216", "他ページの @-ref: " + _r0)
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
in_text("### 1. $y = \\lvert f(x) \\rvert$: reflecting what is "
        "below the axis（下を折り返す） {#abs-f}", "見出し 1")
in_text("### 2. $y = f(\\lvert x \\rvert)$: copying the right half "
        "to the left（右半分を左に写す） {#f-abs}", "見出し 2")
in_text("### 3. $y = \\dfrac{1}{f(x)}$: the reciprocal "
        "graph（逆数のグラフ） {#reciprocal}", "見出し 3")
in_text("### 4. $y = f(ax+b)$: horizontal transformations（横の変換） "
        "{#horizontal}", "見出し 4")
in_text("### 5. $y = [f(x)]^{2}$: squaring the function（$2$ 乗のグラフ） "
        "{#squared}", "見出し 5")
in_text("### 6. Modulus equations（絶対値を含む方程式） {#modulus-equations}", "見出し 6")
in_text("### 7. Modulus inequalities（絶対値を含む不等式） "
        "{#modulus-inequalities}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 6. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-2-16-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-2-16-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("One curve, four transformations", "図(a) の題")
in_fig("$y=f(|x|)$", "図(a) の 3 枚目")
in_fig("$y=[f(x)]^{2}$", "図(a) の 4 枚目")
in_fig("they cross where the height is $1$ or $-1$", "図(b) の要点")
in_fig("t * t - 2.0 * t - 3.0", "図(a) は §1 と同じ関数")
in_text("$1$ つの曲線から作った $4$ つの形です。", "キャプション (a)")
in_text("$f$ が $0$ のところが漸近線、$f$ が $\\pm 1$ のところが交点です。",
        "キャプション (b)")
for leak in ["-4/3", "5/3", "-5/2"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 7. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("4x+1", "演習4"), ("2x-5", "演習5"), ("x-4", "演習6"),
                    ("3x+2", "演習7"), ("x^{2}-9", "演習8"),
                    ("2x-1", "演習10")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 8. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/02-functions/aahl-2-16.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-2-15.qmd") < DRAFT.index("aahl-2-16.qmd"),
    "サイドバーの並びが 2.15 → 2.16")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aahl-2-16.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| modulus function |", "| absolute value |", "| transformation |",
          "| modulus inequality |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 9. 見張り
# ══════════════════════════════════════════════════════════
in_text("## 左側にあった零点は、消えます", "f(|x|) の見張り")
in_text("## $>$ のときに、$-k$ の向きを変え忘れる", "向きの見張り")
in_text("## $k$ が負なら、解はありません", "k < 0 の見張り")
in_text("**$\\lvert f(x) \\rvert$ と $[f(x)]^{2}$ は、どちらも「下に行かない」形ですが、"
        "別のものです。**", "2 つの取りちがえ")
in_text("**中身がもとの $x$ の役をします。**", "f(ax+b) の要点")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
