"""AA HL 1.15（数学的帰納法・背理法・反例）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_15.py
"""
import glob
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-15.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_15.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
n, k, r, x, y = sp.symbols("n k r x y")


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


# ══════════════════════════════════════════════════════════
# 0. 和の公式（記号のまま）と、帰納法の一歩
# ══════════════════════════════════════════════════════════
eq(sp.summation(r, (r, 1, n)), n * (n + 1) / 2, "§4 Σr")
eq(sp.summation(r ** 2, (r, 1, n)), n * (n + 1) * (2 * n + 1) / 6, "例題1 Σr^2")
eq(sp.summation(2 * r - 1, (r, 1, n)), n ** 2, "演習1 Σ(2r-1)")
eq(sp.summation(r * (r + 1), (r, 1, n)),
   n * (n + 1) * (n + 2) / 3, "演習2 Σr(r+1)")

# §4 の一歩
eq(k * (k + 1) / 2 + (k + 1), (k + 1) * (k + 2) / 2, "§4 帰納法の一歩")
eq((k + 1) * ((k + 1) + 1) / 2, (k + 1) * (k + 2) / 2, "§4 目標の形")
# 例題1 の一歩
eq(k * (k + 1) * (2 * k + 1) / 6 + (k + 1) ** 2,
   (k + 1) * (k + 2) * (2 * k + 3) / 6, "例題1 帰納法の一歩")
eq(k * (2 * k + 1) + 6 * (k + 1), 2 * k ** 2 + 7 * k + 6, "例題1 かっこの中")
eq(2 * k ** 2 + 7 * k + 6, (k + 2) * (2 * k + 3), "例題1 因数分解")
eq((k + 1) * ((k + 1) + 1) * (2 * (k + 1) + 1) / 6,
   (k + 1) * (k + 2) * (2 * k + 3) / 6, "例題1 目標の形")
# 演習1・2 の一歩
eq(k ** 2 + (2 * (k + 1) - 1), (k + 1) ** 2, "演習1 帰納法の一歩")
eq(k * (k + 1) * (k + 2) / 3 + (k + 1) * (k + 2),
   (k + 1) * (k + 2) * (k + 3) / 3, "演習2 帰納法の一歩")
eq(sp.Rational(1, 1) * k / 3 + 1, (k + 3) / 3, "演習2 くくったあと")

# ══════════════════════════════════════════════════════════
# 1. 割り切れる型
# ══════════════════════════════════════════════════════════
for a, d in [(5, 4), (7, 6), (8, 7)]:
    for m in range(1, 15):
        chk((a ** m - 1) % d == 0, "%d^%d - 1 が %d で割り切れる" % (a, m, d))
    # 一歩（文字のまま）
    mm = sp.Symbol("m")
    eq(a * (d * mm + 1) - 1, d * (a * mm + 1), "%d^n - 1 の帰納法の一歩" % a)
for m in range(1, 12):
    chk((3 ** (2 * m) - 1) % 8 == 0, "3^{2·%d} - 1 が 8 で割り切れる" % m)
_m = sp.Symbol("m")
eq(9 * (8 * _m + 1) - 1, 8 * (9 * _m + 1), "演習4 の一歩")
eq(3 ** (2 * (k + 1)), 9 * 3 ** (2 * k), "演習4 3^{2k+2} = 9·3^{2k}")
chk(5 ** 1 - 1 == 4 and 7 ** 1 - 1 == 6 and 8 ** 1 - 1 == 7
    and 3 ** 2 - 1 == 8, "base case の値")
chk(7 ** 2 - 1 == 48 and 48 == 6 * 8, "例題2 検算 n=2")
chk(7 ** 3 - 1 == 342 and 342 == 6 * 57, "例題2 検算 n=3")
chk(8 ** 2 - 1 == 63 and 63 == 7 * 9, "演習3 検算 n=2")
chk(8 ** 3 - 1 == 511 and 511 == 7 * 73, "演習3 検算 n=3")
chk(3 ** 4 - 1 == 80 and 80 == 8 * 10, "演習4 検算 n=2")
chk(3 ** 6 - 1 == 728 and 728 == 8 * 91, "演習4 検算 n=3")

# ══════════════════════════════════════════════════════════
# 2. 不等式（演習 5）
# ══════════════════════════════════════════════════════════
for m in range(1, 4):
    chk(not math.factorial(m) > 2 ** m, "n! > 2^n は n=%d で成り立たない" % m)
for m in range(4, 30):
    chk(math.factorial(m) > 2 ** m, "n! > 2^n が n=%d で成り立つ" % m)
chk(math.factorial(4) == 24 and 2 ** 4 == 16, "演習5 base case 24 > 16")
chk(math.factorial(5) == 120 and 2 ** 5 == 32, "演習5 検算 n=5")
chk(math.factorial(3) == 6 and 2 ** 3 == 8, "演習5 n=3 では 6 < 8")

# ══════════════════════════════════════════════════════════
# 3. 反例
# ══════════════════════════════════════════════════════════
_P = [m ** 2 + 41 * m + 41 for m in range(0, 5)]
chk(_P == [41, 83, 127, 173, 221], "§7 の表の値: %s" % _P)
for _v in _P[:4]:
    chk(sp.isprime(_v), "§7 %d は素数" % _v)
chk(not sp.isprime(221), "§7 221 は素数でない")
chk(221 == 13 * 17, "§7 221 = 13 × 17")
chk(min(m for m in range(0, 200) if not sp.isprime(m ** 2 + 41 * m + 41)) == 4,
    "§7 最初に素数でなくなるのは n=4")
_f = [m ** 2 + m + 1 for m in range(1, 5)]
chk(_f == [3, 7, 13, 21], "例題4 の値: %s" % _f)
for _v in _f[:3]:
    chk(sp.isprime(_v), "例題4 %d は素数" % _v)
chk(not sp.isprime(21) and 21 == 3 * 7, "例題4 21 = 3 × 7 は素数でない")
chk(min(m for m in range(1, 200) if not sp.isprime(m ** 2 + m + 1)) == 4,
    "例題4 最初の反例は n=4")
# 演習8：x^2 > x の反例
chk(not (sp.Rational(1, 2) ** 2 > sp.Rational(1, 2)), "演習8 x=1/2 が反例")
chk(sp.Rational(1, 2) ** 2 == sp.Rational(1, 4), "演習8 (1/2)^2 = 1/4")
chk(not (1 ** 2 > 1), "演習8 x=1 も反例")
chk(not (0 ** 2 > 0), "演習8 x=0 も反例")
chk(2 ** 2 > 2, "演習8 x=2 では成り立つ（だから「いつも」だけが偽）")
# 演習9：x^2 + y^2 = 10
chk(1 ** 2 + 3 ** 2 == 10 and 3 ** 2 + 1 ** 2 == 10, "演習9 (1,3) と (3,1)")
_sols = [(a, b) for a in range(1, 11) for b in range(1, 11)
         if a * a + b * b == 10]
chk(sorted(_sols) == [(1, 3), (3, 1)], "演習9 正の整数解はこの 2 組: %s" % _sols)

# ══════════════════════════════════════════════════════════
# 4. 演習 10（まちがい探し）
# ══════════════════════════════════════════════════════════
_wrong = (n ** 2 + n + 2) / 2
eq(_wrong.subs(n, k) + (k + 1), (k ** 2 + 3 * k + 4) / 2, "演習10 一歩の計算")
eq((k ** 2 + 3 * k + 4) / 2, _wrong.subs(n, k + 1), "演習10 一歩は通る")
chk(_wrong.subs(n, 1) == 2, "演習10 n=1 の右辺は 2")
chk(sp.summation(r, (r, 1, 1)) == 1, "演習10 n=1 の左辺は 1")
eq(_wrong - n * (n + 1) / 2, 1, "演習10 いつも 1 だけ大きい")
chk(_wrong.subs(n, 3) == 7 and sp.summation(r, (r, 1, 3)) == 6, "演習10 n=3 の検算")

# ══════════════════════════════════════════════════════════
# 5. 背理法
# ══════════════════════════════════════════════════════════
chk(sp.sqrt(2).is_rational is False, "√2 は有理数でない")
chk(sp.sqrt(3).is_rational is False, "√3 は有理数でない")
chk(sp.Rational(3, 4) - sp.Rational(1, 6) == sp.Rational(7, 12), "例題3 検算の差")
_p, _q, _s, _t = sp.symbols("p q s t", integer=True)
eq(_s / _t - _p / _q, (_s * _q - _p * _t) / (_t * _q), "例題3 差の通分")
for _tt in range(1, 6):
    _odd = (2 * _tt + 1) ** 2
    chk(_odd % 2 == 1, "奇数の 2 乗は奇数: (2·%d+1)^2" % _tt)
eq((2 * sp.Symbol("t") + 1) ** 2, 4 * sp.Symbol("t") ** 2 + 4 * sp.Symbol("t") + 1,
   "演習6 (2t+1)^2 の展開")
eq(4 * sp.Symbol("s") ** 2, 2 * sp.Symbol("q") ** 2 * 0 + 4 * sp.Symbol("s") ** 2,
   "演習6 p=2s の代入")
chk(sp.Rational(1, 200) < sp.Rational(1, 100), "演習7 検算 r/2 < r")
chk(sp.Rational(1, 200).is_rational, "演習7 r/2 も有理数")
# Euclid（Why it works）：N は並べたどの素数でも割り切れない
for _r in range(1, 7):
    _ps = list(sp.primerange(2, 100))[:_r]
    _N = 1
    for _pp in _ps:
        _N *= _pp
    _N += 1
    for _pp in _ps:
        chk(_N % _pp == 1, "Euclid: N を %d で割ると 1 余る（r=%d）" % (_pp, _r))

# ══════════════════════════════════════════════════════════
# 6. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Proof by mathematical induction.", "シラバス 1 行目を逐語で")
in_text("> Proof by contradiction.", "シラバス 2 行目を逐語で")
in_text("> Use of a counterexample to show that a statement is not always true.",
        "シラバス 3 行目を逐語で")
in_text("> It is not sufficient to state the counterexample alone."
        " Students must explain why their example is a counterexample.",
        "Guidance を逐語で")
in_text("> Example: Consider the set $P$ of numbers of the form"
        " $n^{2} + 41n + 41$, $n \\in \\mathbb{N}$,"
        " show that not all elements of $P$ are prime.",
        "シラバスの例（素数）を逐語で")
in_text("> Examples: Irrationality of $\\sqrt{3}$; irrationality of the cube root"
        " of $5$; Euclid's proof of an infinite number of prime numbers;"
        " if $a$ is a rational number and $b$ is an irrational number,"
        " then $a + b$ is an irrational number.",
        "シラバスの例（背理法）を逐語で")
in_text("**公式集には、この項目の欄がありません。**", "公式集にないことを書く")
not_in_text("公式集の **1.15**", "ありもしない欄を書かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 7. GDC / 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("**ただし、これは証明ではありません。**", "電卓は証明にならないと書く")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl115-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl115", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
not_in_text("aahl-1-16.qmd", "1.16 への前方リンクは張らない")
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
in_text("### 1. Three kinds of proof（証明の $3$ つの型） {#three-kinds}", "見出し 1")
in_text("### 2. Proof by mathematical induction（数学的帰納法） {#induction}", "見出し 2")
in_text("### 3. How to set out an induction proof（帰納法の書き方） "
        "{#induction-writing}", "見出し 3")
in_text("### 4. Proving a formula for a sum（和の公式を示す） {#sums}", "見出し 4")
in_text("### 5. Proving divisibility（割り切れることを示す） {#divisibility}", "見出し 5")
in_text("### 6. Proof by contradiction（背理法） {#contradiction}", "見出し 6")
in_text("### 7. Counterexamples（反例） {#counterexample}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 8. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-1-15-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-1-15-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Induction: reach the first rung, then always the next one", "図(a) の題")
in_fig("both parts are needed: neither one alone is enough", "図(a) の要点")
in_fig("Proof by contradiction", "図(b) の題")
in_fig("Arrive at something impossible", "図(b) の要点")
in_text("はしごを $1$ 段目までのぼれて、どの段からも次の段にのぼれるなら、"
        "すべての段にのぼれます。", "キャプション (a)")
in_text("否定を仮定して、正しい変形だけで進み、あり得ないことにたどり着きます。",
        "キャプション (b)")
for leak in ["221", "13 \\times 17", "\\frac{1}{4}", "3 \\times 7"]:
    chk(leak not in FIGSTR, "図が本文・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 9. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("(2r-1)", "演習1"), ("r(r+1)", "演習2"),
                    ("8^{n}-1", "演習3"), ("3^{2n}-1", "演習4"),
                    ("x^{2}+y^{2}", "演習9"),
                    ("k^{2}+k+2", "演習10")]:
    chk(leak not in _BODY, "%s の答え・問題文が本文・例題に出ている: %s" % (where, leak))
chk("n! > 2^{n}$ は $n = 1, 2, 3$ では成り立たず" in TEXT,
    "Why it works だけは演習5 に触れてよい（base case の説明）")

# ══════════════════════════════════════════════════════════
# 10. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-15.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-1-14.qmd") < DRAFT.index("aahl-1-15.qmd"),
    "サイドバーの並びが 1.14 → 1.15")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-15.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| proof by mathematical induction |", "| base case |",
          "| inductive step |", "| proof by contradiction |",
          "| divisible by |", "| irrational |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 11. 見張り
# ══════════════════════════════════════════════════════════
in_text("## $2$ つの両方が要ります", "base case と inductive step の両方が要る")
in_text("`Assume` か `Suppose` を使ってください。", "Assume の書き方")
in_text("ですから $n_{0} \\geq 2$ で、$n_{0} - 1$ も正の整数です。",
        "Why it works の最小反例")
in_text("見つからなくても、正しい証明にはならない", "反例の向き")
in_text("**base case が $n = 1$ ではありません**", "演習5 の base case")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
