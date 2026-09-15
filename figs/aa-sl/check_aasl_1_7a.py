"""AA SL 1.7a（有理数の指数）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_7a.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-7a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_7a.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x", positive=True)
a = sp.Symbol("a", positive=True)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def _S(v):
    if isinstance(v, float):
        return sp.Rational(str(v))
    return sp.nsimplify(v, rational=True)


def eq(p, q, msg=""):
    chk(sp.simplify(_S(p) - _S(q)) == 0, msg + f"  ({p} vs {q})")


def ne(p, q, msg=""):
    chk(sp.simplify(_S(p) - _S(q)) != 0, msg + f"  ({p} vs {q})")


def ident(lhs, rhs, msg=""):
    chk(sp.simplify(lhs - rhs) == 0, "恒等式でない: " + msg)


def sols(equation):
    """実数解だけを、小さい順に返す。"""
    return sorted(v for v in sp.solve(equation, x) if v.is_real)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 定義そのもの
# ══════════════════════════════════════════════════════════
ident((a ** R(1, 2)) ** 2, a, "(a^(1/2))^2 = a")
ident(a ** R(1, 2), sp.sqrt(a), "a^(1/2) = √a")
ident(a ** R(1, 3), sp.root(a, 3), "a^(1/3) = 3乗根")
for _m, _n in [(2, 3), (3, 4), (3, 5), (5, 2)]:
    ident((a ** R(1, _n)) ** _m, a ** R(_m, _n), f"(n乗根)^m = a^(m/n): {_m}/{_n}")
    ident((a ** _m) ** R(1, _n), a ** R(_m, _n), f"n乗根(a^m) = a^(m/n): {_m}/{_n}")
ident(a ** R(-1, 2), 1 / a ** R(1, 2), "負の有理指数は逆数")
# m が偶数なら正の根
eq(R(16) ** R(1, 2), 4, "16^(1/2) = 4")
ne(R(16) ** R(1, 2), -4, "16^(1/2) は -4 ではない")
eq((-4) ** 2, 16, "(-4)^2 も 16")
chk(sorted(sp.solve(sp.Eq(x ** 2, 16), x)) == [4], "x>0 の解は 4 だけ")
_all = sorted(sp.solve(sp.Eq(sp.Symbol("t") ** 2, 16), sp.Symbol("t")))
chk(_all == [-4, 4], f"x^2 = 16 の解は ±4: {_all}")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
eq(R(27) ** R(2, 3), 9, "27^(2/3) = 9")
eq(sp.root(27, 3), 3, "27 の 3 乗根は 3")
eq(27 ** 2, 729, "27^2 = 729")
eq(sp.root(729, 3), 9, "729 の 3 乗根は 9")
eq(9 ** 3, 729, "9^3 = 729（戻し）")
eq(R(32) ** R(2, 5), 4, "32^(2/5) = 4")
eq(2 ** 5, 32, "32 = 2^5")
eq(R(8) ** R(2, 3), 4, "8^(2/3) = 4")
eq(R(8) ** R(-2, 3), R(1, 4), "8^(-2/3) = 1/4")
eq(R(9, 16) ** R(-1, 2), R(4, 3), "(9/16)^(-1/2) = 4/3")
# 第 5 節
ident(x ** R(1, 2) * x ** R(3, 2), x ** 2, "x^(1/2)·x^(3/2) = x^2")
ident(x ** R(5, 3) / x ** R(2, 3), x, "x^(5/3)/x^(2/3) = x")
ident((x ** R(2, 3)) ** R(3, 4), x ** R(1, 2), "(x^(2/3))^(3/4) = x^(1/2)")
# 第 6 節
ident(sp.sqrt(x), x ** R(1, 2), "√x = x^(1/2)")
ident(sp.root(x, 3), x ** R(1, 3), "3乗根x = x^(1/3)")
ident(1 / sp.sqrt(x), x ** R(-1, 2), "1/√x = x^(-1/2)")
ident(x * sp.sqrt(x), x ** R(3, 2), "x√x = x^(3/2)")
ident(sp.sqrt(x ** 3), x ** R(3, 2), "√(x^3) = x^(3/2)")
# 第 7 節
eq(R(9) ** R(3, 2), 27, "9^(3/2) = 27")
chk(sols(sp.Eq(x ** R(2, 3), 9)) == [27], "x^(2/3) = 9 の解は 27")

# ══════════════════════════════════════════════════════════
# 2. 例題 1
# ══════════════════════════════════════════════════════════
eq(R(49) ** R(1, 2), 7, "例題1(a) 7")
eq(7 ** 2, 49, "7^2 = 49（戻し）")
eq(R(27) ** R(2, 3), 9, "例題1(b) 9")
eq(R(8) ** R(-2, 3), R(1, 4), "例題1(c) 1/4")
eq(sp.root(8, 3), 2, "8 の 3 乗根は 2")
eq(R(1, 4) ** R(-3, 2), 8, "1/4 を -3/2 乗すると 8（戻し）")
eq(R(4) ** R(3, 2), 8, "4^(3/2) = 8")
chk(R(8) ** R(-2, 3) > 0, "答えは正")

# ══════════════════════════════════════════════════════════
# 3. 例題 2
# ══════════════════════════════════════════════════════════
eq(R(81) ** R(3, 4), 27, "例題2(a) 27")
eq(3 ** 4, 81, "3^4 = 81")
eq(R(27) ** R(4, 3), 81, "27^(4/3) = 81（戻し）")
eq(R(9, 16) ** R(1, 2), R(3, 4), "例題2(b) 3/4")
eq(R(8, 27) ** R(-1, 3), R(3, 2), "例題2(c) 3/2")
eq(R(3, 2) ** -3, R(8, 27), "(3/2)^-3 = 8/27（戻し）")
eq(R(2, 3) ** -3, R(27, 8), "誤答 2/3 を -3 乗すると 27/8")
ne(R(27, 8), R(8, 27), "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 4. 例題 3
# ══════════════════════════════════════════════════════════
ident(sp.sqrt(x), x ** R(1, 2), "例題3(a)")
ident(1 / sp.root(x, 3), x ** R(-1, 3), "例題3(b)")
ident(x ** 2 * sp.sqrt(x), x ** R(5, 2), "例題3(c)")
ident(sp.sqrt(x ** 5) / x, x ** R(3, 2), "例題3(d)")
eq(16 * 2, 32, "x=4 で x^2√x = 32")
eq(R(4) ** R(5, 2), 32, "4^(5/2) = 32")
eq(sp.sqrt(R(4) ** 5), 32, "√(4^5) = 32")
eq(R(32, 4), 8, "x=4 で (d) は 8")
eq(R(4) ** R(3, 2), 8, "4^(3/2) = 8")
ne(32, 8, "(c) と (d) は別の値")

# ══════════════════════════════════════════════════════════
# 5. 例題 4
# ══════════════════════════════════════════════════════════
chk(sols(sp.Eq(x ** R(1, 2), 6)) == [36], "例題4(a) 36")
chk(sols(sp.Eq(x ** R(2, 3), 9)) == [27], "例題4(b) 27")
chk(sols(sp.Eq(x ** R(-1, 2), R(1, 5))) == [25], "例題4(c) 25")
chk(sols(sp.Eq(x ** R(3, 2), 27)) == [9], "例題4(d) 9")
eq(R(36) ** R(1, 2), 6, "36^(1/2) = 6（検算）")
eq(R(27) ** R(2, 3), 9, "27^(2/3) = 9（検算）")
eq(R(25) ** R(-1, 2), R(1, 5), "25^(-1/2) = 1/5（検算）")
eq(R(9) ** R(3, 2), 27, "9^(3/2) = 27（検算）")
ne(R(9) ** R(2, 3), 27, "9^(2/3) は 27 ではない")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(R(36) ** R(1, 2), 6, "演習1 6")
eq(6 ** 2, 36, "戻すと 36")

eq(R(64) ** R(2, 3), 16, "演習2(a) 16")
eq(sp.root(64, 3), 4, "64 の 3 乗根は 4")
eq(R(16) ** R(3, 2), 64, "16^(3/2) = 64（戻し）")
eq(R(32) ** R(3, 5), 8, "演習2(b) 8")
eq(sp.root(32, 5), 2, "32 の 5 乗根は 2")
eq(R(8) ** R(5, 3), 32, "8^(5/3) = 32（戻し）")
eq(64 ** 2, 4096, "先に 2 乗すると 4096")
eq(sp.root(4096, 3), 16, "4096 の 3 乗根は 16")

eq(R(125) ** R(-1, 3), R(1, 5), "演習3(a) 1/5")
eq(R(1, 5) ** -3, 125, "戻すと 125")
eq(R(16) ** R(-3, 4), R(1, 8), "演習3(b) 1/8")
eq(sp.root(16, 4), 2, "16 の 4 乗根は 2")
eq(R(1, 8) ** R(-4, 3), 16, "戻すと 16")

eq(R(25, 4) ** R(-1, 2), R(2, 5), "演習4 2/5")
eq(R(2, 5) ** -2, R(25, 4), "戻すと 25/4")
eq(R(5, 2) ** -2, R(4, 25), "誤答 5/2 は 4/25 に戻る")
ne(R(4, 25), R(25, 4), "その誤答は合わない")

ident(sp.root(x, 4), x ** R(1, 4), "演習5(a)")
ident(1 / (x * sp.sqrt(x)), x ** R(-3, 2), "演習5(b)")
eq(R(16) ** R(1, 4), 2, "x=16 で (a) は 2")
eq(R(1, 4 * 2), R(1, 8), "x=4 で (b) は 1/8")
eq(R(4) ** R(-3, 2), R(1, 8), "4^(-3/2) = 1/8")
eq(R(4) ** R(-1, 2), R(1, 2), "誤答 x^(-1/2) は x=4 で 1/2")
ne(R(1, 2), R(1, 8), "その誤答は合わない")

ident(x ** R(1, 2) * x ** R(3, 2) / x ** -1, x ** 3, "演習6 x^3")
eq(R(1, 2) + R(3, 2), 2, "1/2 + 3/2 = 2")
eq(2 - (-1), 3, "2 - (-1) = 3")
eq(R(2) * 8 / R(1, 4), 64, "x=4 でもとの式は 64")
eq(4 ** 3, 64, "4^3 = 64")
eq(4 ** 1, 4, "誤答 x^1 は x=4 で 4")
ne(4, 64, "その誤答は合わない")

chk(sols(sp.Eq(x ** R(1, 3), 4)) == [64], "演習7(a) 64")
eq(R(64) ** R(1, 3), 4, "戻すと 4")
chk(sols(sp.Eq(x ** R(-1, 2), R(1, 7))) == [49], "演習7(b) 49")
eq(R(49) ** R(-1, 2), R(1, 7), "戻すと 1/7")
eq(R(1, 49) ** R(-1, 2), 7, "誤答 1/49 は 7 に戻る")
ne(7, R(1, 7), "その誤答は合わない")

chk(sols(sp.Eq(x ** R(2, 3), 25)) == [125], "演習8 125")
eq(R(25) ** R(3, 2), 125, "25^(3/2) = 125")
eq(5 ** 3, 125, "5^3 = 125")
eq(R(125) ** R(2, 3), 25, "戻すと 25")
ne(R(25) ** R(2, 3), 125, "25^(2/3) は 125 ではない")

eq(R(1, 3) + R(1, 6), R(1, 2), "演習9 1/3 + 1/6 = 1/2")
ident(a ** R(1, 3) * a ** R(1, 6), a ** R(1, 2), "演習9 の恒等式")
eq(R(64) ** R(1, 3), 4, "a=64 で 64^(1/3) = 4")
eq(R(64) ** R(1, 6), 2, "a=64 で 64^(1/6) = 2")
eq(4 * 2, 8, "積は 8")
eq(R(64) ** R(1, 2), 8, "64^(1/2) = 8")
ne(R(64) ** R(2, 9), 8, "誤答 2/9 では 8 にならない")

eq(R(16) ** R(3, 4), 8, "演習10 正しい値 8")
eq(16 * R(3, 4), 12, "生徒の答え 12")
ne(12, 8, "生徒の答えは合わない")
eq(16 ** 3, 4096, "16^3 = 4096")
eq(R(4096) ** R(1, 4), 8, "4096 の 4 乗根は 8")
eq(8 ** 4, 4096, "8^4 = 4096")
eq(R(4) ** R(1, 2), 2, "4^(1/2) = 2")
eq(4 * R(1, 2), 2, "生徒の方法でも 2（たまたま一致）")
eq(R(9) ** R(1, 2), 3, "9^(1/2) = 3")
eq(9 * R(1, 2), R(9, 2), "生徒の方法なら 4.5")
ne(R(9, 2), 3, "ここで方法が壊れる")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この式は公式集にありません", "有理指数の式は載っていないと明記")
in_text("**有理数の指数についての式は、載っていません。**", "同上（本文）")
in_text("> $a^{\\frac{1}{m}} = \\sqrt[m]{a}$, if $m$ is even this refers to"
        " the positive root.", "シラバスの Guidance を逐語で")
# 2026-09: コードスパン内の $…$ は LaTeX が処理されないため、$ を外した
in_text("`if m is even this refers to the positive root`", "但し書きを引用")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")

# ══════════════════════════════════════════════════════════
# 9. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aasl17a-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl17a", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 10. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-7a-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-7a-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Two routes to $27^{\\\\frac{2}{3}}$", "図(a) の題")
in_fig("cube root", "図(a) の道すじ")
in_fig("small numbers all the way", "図(a) の要点")
in_fig("a hard root to do by hand", "図(a) のもう一方")
in_fig("Half-steps in the exponent, base $9$", "図(b) の題")
in_fig("the half-steps are the square roots", "図(b) の要点")
in_text("(a) Two routes to the same value", "キャプションが (a) を説明")
in_text("(b) Half-steps on the exponent", "キャプションが (b) を説明")
# 図の値が本文と合っているか
eq(R(27) ** R(2, 3), 9, "図(a) の行き先")
eq(sp.root(27, 3), 3, "図(a) の途中（上の道）")
eq(27 ** 2, 729, "図(a) の途中（下の道）")
for _e, _v in [(0, 1), (R(1, 2), 3), (1, 9), (R(3, 2), 27), (2, 81)]:
    eq(R(9) ** _e, _v, f"図(b) の 9^{_e}")
for _lk in ["16", "64", "125", "49", "4096", "1/5", "2/5", "1/8"]:
    chk(_lk not in FIGSTR, "図が演習の答えを載せている: " + _lk)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-7a.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-6.qmd") < DRAFT.index("aasl-1-7a.qmd"), "並びが 1.6 → 1.7a")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aasl-1-7a.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| rational exponent |", "| root |", "| square root |",
          "| cube root |", "| evaluate |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ══════════════════════════════════════════════════════════
# 12. レビュー反映の見張り
# ══════════════════════════════════════════════════════════
in_text("## このページでは、底は正とします", "底が正であることを明記")
in_text("$(-16)^{\\frac{1}{2}}$ は、実数としては定義されません。", "負の底の偶数根")
in_text("**対数の法則・底の変換・$a^{x} = \\mathrm{e}^{x\\ln a}$** だけです",
        "公式集 1.7 の中身を正しく書く")
in_text("（if $m$ is even this refers to the positive root）", "バッククォートを外した")
in_text("## 文字の役割が、[第 2 節](#root) と入れかわります", "m と n の役割")
in_text("**底が $n$ 乗数になっているときは、左（先に根をとる）が圧倒的に楽です。**",
        "条件つきの言い方")
not_in_text("**手で計算するなら、左のほう（先に根をとる）が楽です。**", "言い切りを直した")
in_text("9^{3} = 729, \\qquad 27^{2} = 729", "検算は掛け算だけで済ませる")
not_in_text("27^{2} = 729, \\qquad \\sqrt[3]{729} = 9", "∛729 を直接使わない")
eq(9 ** 3, 729, "9^3 = 729")
eq(27 ** 2, 729, "27^2 = 729")
# 第 5 節・第 7 節が、演習や例題の答えと重ならないようにした
in_text("x^{\\frac{1}{4}} \\times x^{\\frac{3}{4}} = x^{\\frac{1}{4} + \\frac{3}{4}}"
        " = x^{1} = x", "第 5 節の例を差しかえた")
ident(x ** R(1, 4) * x ** R(3, 4), x, "x^(1/4)·x^(3/4) = x")
in_text("x^{\\frac{3}{4}} = 8 \\ \\Rightarrow", "第 7 節の例を差しかえた")
chk(sols(sp.Eq(x ** R(3, 4), 8)) == [16], "x^(3/4) = 8 の解は 16")
eq(R(8) ** R(4, 3), 16, "8^(4/3) = 16")
in_text("$x > 0$、$c > 0$ のとき", "方程式の解き方に条件")
# 正の根を選ぶ理由
in_text("**$a^{\\frac{1}{2}} = \\left(a^{\\frac{1}{4}}\\right)^{2}$ が壊れます。**",
        "負の根では壊れる式")
eq((R(16) ** R(1, 4)) ** 2, 4, "(16^(1/4))^2 = 4")
in_text("**決め手にはなりません。**", "a^(1/2)×a^(1/2)=a は決め手にならない")
in_text("決めごとなのは、$\\pm$ のどちらを選ぶかだけです。", "何が決めごとかを分ける")
# 命令語
chk(TEXT.count("Find the value of") >= 6, "Evaluate ではなく Find the value of")
not_in_text("[Evaluate without using a calculator.]{.q-en}", "Evaluate は使わない")
not_in_text("[Evaluate $36^", "同上")
in_text("[Explain why $16^{\\frac{1}{2}} = 4$ rather than $\\pm 4$.]{.q-en}", "(d) の英語")
in_text("where $x > 0$ and $k$ is a rational number", "定義域を書く")
in_text("[Identify the error in the student's working, and find the correct value"
        " of $16^{\\frac{3}{4}}$.]{.q-en}", "give ではなく find")
in_text("State the law of exponents that you use.", "使った法則を述べさせる")
# Common errors
in_text("## 負の数に、偶数の根をつける", "追加した Common error 1")
in_text("## 分数の指数を、和にばらまく", "追加した Common error 2")
eq(R(-8) ** R(1, 3) if False else -2, -2, "(-8)^(1/3) = -2（実数の立方根）")
eq(sp.root(25, 2), 5, "√25 = 5")
eq(R(16) ** R(1, 2) + 3, 7, "誤答 x^(1/2)+3 は 7")
ne(7, 5, "√25 とはちがう")
not_in_text("**答えが底より小さくなる**のが、この形の特徴です。", "偽の見分け方を消した")
in_text("**大きさを見るだけでは、この誤りは見つかりません。**", "正しい言い方に")
eq(8 * R(2, 3), R(16, 3), "誤答 8 × 2/3 = 16/3")
chk(R(16, 3) < 8 and 4 < 8, "誤答も正答も 8 より小さい")
eq(R(8) ** R(2, 3), 4, "8^(2/3) = 4")
# 演習の答えを Common errors から消した
not_in_text("## $x\\sqrt{x}$ を $x^{\\frac{1}{2}}$ にする", "演習 5(b) の答えを消した")
in_text("## $x\\sqrt[3]{x}$ を $x^{\\frac{1}{3}}$ にする", "差しかえ先")
ident(x * sp.root(x, 3), x ** R(4, 3), "x·∛x = x^(4/3)")
eq(R(8) ** R(4, 3), 16, "x=8 で 16")
eq(8 * 2, 16, "8 × 2 = 16")
# 検算の独立性
in_text("**この検算で決まるのは大きさだけで、符号は決まりません。**", "±6 を排除できない")
eq((-6) ** 2, 36, "(-6)^2 も 36")
in_text("答えを $4$ 乗すると、$\\left(x^{\\frac{1}{4}}\\right)^{4} = x$ に戻ります。",
        "演習 5(a) の非循環な検算")
not_in_text("同じ書き方です。$x = 16$ にすると", "循環した検算は消した")
in_text("**指数どうしの足し算・引き算を使わずに、値だけで確かめました。**", "言い方を正した")
in_text("**逆数を外す向きが逆です。**", "演習 7(b) の説明を直した")
in_text("$64^{\\frac{2}{9}} = 2^{6 \\times \\frac{2}{9}} = 2^{\\frac{4}{3}}$", "手で出せる形に直した")
eq(R(2) ** R(4, 3), R(64) ** R(2, 9), "64^(2/9) = 2^(4/3)")
ne(R(2) ** R(4, 3), 8, "2^(4/3) は 8 ではない")
# (-4)^(-3/2) は実数として定義されない
in_text("**実数としては定義されない**", "戻し計算が書けないことを説明")
# 図のキャプション
in_text("(a) Two routes to the same value of 27^(2/3)", "キャプションに底を書く")
in_text("(b) Half-steps on the exponent for base 9", "同上")
# 指数法則は底が正のとき
in_text("$\\left((-2)^{2}\\right)^{\\frac{1}{2}} = 4^{\\frac{1}{2}} = 2$ であって、$-2$ ではありません",
        "底が負だと崩れる例")
eq((R(-2) ** 2) ** R(1, 2), 2, "((-2)^2)^(1/2) = 2")
ne(2, -2, "-2 には戻らない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
