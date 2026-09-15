"""AA SL 1.9（二項定理）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_9.py
"""
import glob
import os
import re
import sys

import sympy as sp
from sympy import binomial as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-9.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_9.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x")
a, b = sp.symbols("a b")


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + f"  ({u} vs {v})")


def ne(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) != 0, msg + f"  ({u} vs {v})")


def coeff(expr, k):
    return sp.expand(expr).coeff(x, k)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 定理そのもの
# ══════════════════════════════════════════════════════════
for _n in range(1, 9):
    _lhs = (a + b) ** _n
    _rhs = sum(C(_n, _r) * a ** (_n - _r) * b ** _r for _r in range(_n + 1))
    eq(_lhs, _rhs, f"二項定理 n={_n}")
    # 指数の和はいつも n
    for _r in range(_n + 1):
        chk((_n - _r) + _r == _n, f"指数の和が n: n={_n}, r={_r}")
    # 左右対称
    for _r in range(_n + 1):
        chk(C(_n, _r) == C(_n, _n - _r), f"nCr = nC(n-r): n={_n}, r={_r}")
    # 行の合計は 2^n
    chk(sum(C(_n, _r) for _r in range(_n + 1)) == 2 ** _n,
        f"行の合計が 2^n: n={_n}")
    # パスカルの規則
    for _r in range(1, _n):
        chk(C(_n, _r) == C(_n - 1, _r - 1) + C(_n - 1, _r),
            f"上の 2 つの和: n={_n}, r={_r}")
# 公式そのもの
for _n, _r in [(5, 2), (7, 3), (8, 2), (6, 3), (10, 3), (4, 2)]:
    eq(C(_n, _r), sp.factorial(_n) / (sp.factorial(_r) * sp.factorial(_n - _r)),
       f"nCr の式: n={_n}, r={_r}")
eq(sp.factorial(5), 120, "5! = 120")
eq(sp.factorial(0), 1, "0! = 1")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
eq((a + b) ** 2, a ** 2 + 2 * a * b + b ** 2, "(a+b)^2")
eq((a + b) ** 3, a ** 3 + 3 * a ** 2 * b + 3 * a * b ** 2 + b ** 3, "(a+b)^3")
# パスカルの三角形の表
PASCAL = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
for _n, _row in enumerate(PASCAL):
    chk([C(_n, _r) for _r in range(_n + 1)] == _row, f"n={_n} の行: {_row}")
eq(3 + 3, 6, "3 + 3 = 6")
eq(1 + 3, 4, "1 + 3 = 4")
# 第 3 節
eq(C(5, 2), 10, "5C2 = 10")
eq(sp.Integer(120) / 12, 10, "120/12 = 10")
eq(sp.Integer(5 * 4) / 2, 10, "約分してから計算しても 10")
eq(C(10, 3), 120, "10C3 = 120")
eq(sp.Integer(10 * 9 * 8) / 6, 120, "10×9×8/6 = 120")
# 第 5 節
eq(coeff((x + 3) ** 5, 2), 270, "(x+3)^5 の x^2 の係数は 270")
eq(C(5, 3) * 27, 270, "5C3 × 27 = 270")
chk(5 - 3 == 2, "5 - r = 2 なら r = 3")
# 第 6 節
eq(C(4, 1) * (2 * x) ** 3 * (-3), -96 * x ** 3, "4C1 (2x)^3 (-3) = -96x^3")
eq((2 * x) ** 3, 8 * x ** 3, "(2x)^3 = 8x^3")
ne((2 * x) ** 3, 2 * x ** 3, "2x^3 ではない")
for _k, _v in [(1, -3), (2, 9), (3, -27), (4, 81)]:
    eq(sp.Integer(-3) ** _k, _v, f"(-3)^{_k} = {_v}")
# 第 7 節
chk([C(6, _r) for _r in range(7)] == [1, 6, 15, 20, 15, 6, 1], "6Cr の並び")
chk([_r for _r in range(7) if C(6, _r) == 20] == [3], "20 になるのは r=3 だけ")
eq(C(8, 6), C(8, 2), "8C6 = 8C2")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
eq(C(3, 2), 3, "3 つのかっこから 2 つ選ぶのは 3 通り")
eq(coeff(sp.expand((x + 1) ** 3), 1), 3, "ab^2 の係数は 3")
for _n in range(2, 7):
    for _r in range(1, _n):
        chk(C(_n, _r) == C(_n - 1, _r - 1) + C(_n - 1, _r),
            f"最後の 1 個を使うか使わないか: n={_n}, r={_r}")

# ══════════════════════════════════════════════════════════
# 3. 例題 1
# ══════════════════════════════════════════════════════════
eq((x + 2) ** 4, 16 + 32 * x + 24 * x ** 2 + 8 * x ** 3 + x ** 4, "例題1")
for _r, _c, _t in [(0, 1, 1), (1, 4, 2), (2, 6, 4), (3, 4, 8), (4, 1, 16)]:
    eq(C(4, _r), _c, f"係数 4C{_r} = {_c}")
    eq(sp.Integer(2) ** _r, _t, f"2^{_r} = {_t}")
eq(C(4, 1) * 2, 8, "8x^3 の係数")
eq(C(4, 2) * 4, 24, "24x^2 の係数")
eq(C(4, 3) * 8, 32, "32x の係数")
eq((1 + 2) ** 4, 81, "x=1 でもとの式は 81")
eq(16 + 32 + 24 + 8 + 1, 81, "x=1 で答えの式も 81")
eq((-1 + 2) ** 4, 1, "x=-1 でもとの式は 1")
eq(16 - 32 + 24 - 8 + 1, 1, "x=-1 で答えの式も 1")
eq(1 + 16, 17, "x^4 + 2^4 とした誤答は x=1 で 17")
ne(17, 81, "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 4. 例題 2
# ══════════════════════════════════════════════════════════
eq(C(7, 3), 35, "例題2(a) 35")
eq(sp.Integer(7 * 6 * 5) / 6, 35, "7×6×5/6 = 35")
eq(sp.Integer(210) / 6, 35, "210/6 = 35")
eq(C(7, 4), 35, "例題2(b) 35")
chk([C(5, _r) for _r in range(6)] == [1, 5, 10, 10, 5, 1], "n=5 の行")
chk([C(6, _r) for _r in range(7)] == [1, 6, 15, 20, 15, 6, 1], "n=6 の行")
chk([C(7, _r) for _r in range(8)] == [1, 7, 21, 35, 35, 21, 7, 1], "n=7 の行")
eq(sp.factorial(7) / sp.factorial(3), 840, "7!/3! = 840")
ne(840, 35, "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 5. 例題 3
# ══════════════════════════════════════════════════════════
eq((2 * x - 3) ** 3, 8 * x ** 3 - 36 * x ** 2 + 54 * x - 27, "例題3")
eq((2 * x) ** 2, 4 * x ** 2, "(2x)^2 = 4x^2")
eq(3 * 4 * (-3), -36, "-36x^2 の係数")
eq(3 * 2 * 9, 54, "54x の係数")
eq((2 - 3) ** 3, -1, "x=1 でもとの式は -1")
eq(8 - 36 + 54 - 27, -1, "x=1 で答えの式も -1")
eq(sp.Integer(-3) ** 3, -27, "x=0 で定数項は -27")
eq(3 * 2 * (-3), -18, "(2x)^2 を 2x^2 とした誤答の係数")
eq(8 - 18 + 54 - 27, 17, "その誤答は x=1 で 17")
ne(17, -1, "合わない")

# ══════════════════════════════════════════════════════════
# 6. 例題 4
# ══════════════════════════════════════════════════════════
eq(coeff((x + 3) ** 6, 3), 540, "例題4(a) 540")
eq(C(6, 3) * 27, 540, "6C3 × 3^3 = 540")
chk(6 - 3 == 3, "6 - r = 3 なら r = 3")
eq(coeff((2 * x - 1) ** 5, 2), -40, "例題4(b) -40")
eq(C(5, 3) * 4 * (-1), -40, "5C3 × (2)^2 × (-1)^3 = -40")
chk(5 - 3 == 2, "5 - r = 2 なら r = 3")
chk(coeff((2 * x - 1) ** 5, 2) < 0, "答えは負")
eq(sp.Integer(-1) ** 3, -1, "(-1)^3 = -1")
eq(C(6, 3), 20, "6C3 = 20")
eq(sp.Integer(6 * 5 * 4) / 6, 20, "6×5×4/6 = 20")
eq(3 + 3, 6, "指数の和は n = 6")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
chk([C(5, _r) for _r in range(6)] == [1, 5, 10, 10, 5, 1], "演習1(a)")
eq((x + 1) ** 5,
   x ** 5 + 5 * x ** 4 + 10 * x ** 3 + 10 * x ** 2 + 5 * x + 1, "演習1(b)")
eq(2 ** 5, 32, "x=1 で 2^5 = 32")
eq(1 + 5 + 10 + 10 + 5 + 1, 32, "係数の合計も 32")
chk(len([C(5, _r) for _r in range(6)]) == 6, "n=5 の行は 6 個")

eq(C(8, 2), 28, "演習2(a) 28")
eq(sp.Integer(8 * 7) / 2, 28, "8×7/2 = 28")
eq(C(8, 6), 28, "演習2(b) 28")
eq(sp.factorial(8) / sp.factorial(2), 20160, "8!/2! = 20160")
ne(20160, 28, "その誤答は合わない")

eq((x - 2) ** 4, x ** 4 - 8 * x ** 3 + 24 * x ** 2 - 32 * x + 16, "演習3")
for _k, _v in [(1, -2), (2, 4), (3, -8), (4, 16)]:
    eq(sp.Integer(-2) ** _k, _v, f"(-2)^{_k} = {_v}")
eq((1 - 2) ** 4, 1, "x=1 でもとの式は 1")
eq(1 - 8 + 24 - 32 + 16, 1, "x=1 で答えの式も 1")
eq(1 + 8 + 24 + 32 + 16, 81, "b=2 とした誤答は 81")
ne(81, 1, "合わない")

eq((3 * x + 1) ** 3, 27 * x ** 3 + 27 * x ** 2 + 9 * x + 1, "演習4")
eq((3 * x) ** 3, 27 * x ** 3, "(3x)^3 = 27x^3")
eq((3 * x) ** 2, 9 * x ** 2, "(3x)^2 = 9x^2")
eq(3 * 9, 27, "3 × 9 = 27（x^2 の係数）")
eq(4 ** 3, 64, "x=1 でもとの式は 64")
eq(27 + 27 + 9 + 1, 64, "x=1 で答えの式も 64")
eq(27 + 9 + 9 + 1, 46, "(3x)^2 を 3x^2 とした誤答は 46")
ne(46, 64, "合わない")

eq((1 + 2 * x) ** 4,
   1 + 8 * x + 24 * x ** 2 + 32 * x ** 3 + 16 * x ** 4, "演習5")
eq((2 * x) ** 2, 4 * x ** 2, "(2x)^2")
eq((2 * x) ** 4, 16 * x ** 4, "(2x)^4")
eq((1 + 2) ** 4, 81, "x=1 でもとの式は 81")
eq(1 + 8 + 24 + 32 + 16, 81, "x=1 で答えの式も 81")
eq((1 + 2 * R(-1, 2)) ** 4, 0, "x=-1/2 でもとの式は 0")
eq(1 - 4 + 6 - 4 + 1, 0, "x=-1/2 で答えの式も 0")

eq(coeff((x + 2) ** 7, 4), 280, "演習6 280")
eq(C(7, 3) * 8, 280, "7C3 × 2^3 = 280")
chk(7 - 3 == 4, "7 - r = 4 なら r = 3")
chk(4 + 3 == 7, "指数の和は 7")
eq(sp.Integer(7 * 6 * 5 * 4) / 24, 35, "7×6×5×4/24 = 35")
eq(sp.Integer(840) / 24, 35, "840/24 = 35")
eq(C(7, 4) * 16, 560, "r=4 とした誤答は 560")
eq(coeff((x + 2) ** 7, 3), 560, "それは x^3 の係数")
ne(560, 280, "x^4 の係数ではない")

eq(coeff((2 * x - 1) ** 4, 2), 24, "演習7 24")
eq(C(4, 2) * 4, 24, "4C2 × (2)^2 = 24")
eq((2 * x - 1) ** 4,
   16 * x ** 4 - 32 * x ** 3 + 24 * x ** 2 - 8 * x + 1, "演習7 の全展開")
eq((2 - 1) ** 4, 1, "x=1 でもとの式は 1")
eq(16 - 32 + 24 - 8 + 1, 1, "x=1 で展開した式も 1")
eq(C(4, 2) * 2, 12, "(2x)^2 を 2x^2 とした誤答は 12")
ne(12, 24, "合わない")

chk([C(6, _r) for _r in range(7)] == [1, 6, 15, 20, 15, 6, 1], "演習8(a)")
chk([_r for _r in range(7) if C(6, _r) == 20] == [3], "演習8(b) r=3")
eq(sum(C(6, _r) for _r in range(7)), 64, "行の合計は 64")
eq(2 ** 6, 64, "= 2^6")
chk([C(6, _r) for _r in range(7)] == [C(6, 6 - _r) for _r in range(7)],
    "左右対称")

eq(sum(C(3, _r) for _r in range(4)), 8, "演習9 n=3 で 8")
eq(2 ** 3, 8, "= 2^3")
eq(sum(C(4, _r) for _r in range(5)), 16, "n=4 で 16")
eq(2 ** 4, 16, "= 2^4")
eq((1 + 1) ** 5, 32, "a=b=1 を入れると 2^n")
for _n in range(1, 9):
    eq(sum(C(_n, _r) for _r in range(_n + 1)), 2 ** _n, f"n={_n} でも 2^n")

eq((x - 3) ** 4,
   x ** 4 - 12 * x ** 3 + 54 * x ** 2 - 108 * x + 81, "演習10 正しい展開")
eq((x + 3) ** 4,
   x ** 4 + 12 * x ** 3 + 54 * x ** 2 + 108 * x + 81, "生徒の答えは (x+3)^4")
eq((1 - 3) ** 4, 16, "x=1 でもとの式は 16")
eq(1 - 12 + 54 - 108 + 81, 16, "x=1 で正しい展開も 16")
eq(1 + 12 + 54 + 108 + 81, 256, "生徒の答えは 256")
ne(256, 16, "合わない")

# ══════════════════════════════════════════════════════════
# 8. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.9** の欄に、二項定理といっしょに印刷されています。", "公式集にある")
in_text("> $^{n}\\mathrm{C}_{r} = \\dfrac{n!}{r!(n-r)!}$", "nCr の式を逐語で")
in_text("> Binomial theorem $n \\in \\mathbb{N}$", "二項定理の見出しを逐語で")
in_text("> $(a+b)^{n} = a^{n} + {}^{n}\\mathrm{C}_{1} a^{n-1}b + \\ldots +"
        " {}^{n}\\mathrm{C}_{r} a^{n-r}b^{r} + \\ldots + b^{n}$",
        "二項定理を逐語で")
in_text("> $^{n}C_r$ should be found using **both** the formula and technology.",
        "両方で求められる（Guidance）")
in_text("> Example: Find $r$ when $^{6}C_r = 20$, using a table of values"
        " generated with technology.", "表を作る例（Guidance）")
in_text("`Counting principles may be used in the development of the theorem`",
        "数え上げの Guidance")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aasl19-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk("## 解答例（答案用紙にはこう書く）" not in TEXT, "解答例の見出しをそろえた")
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
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl19", "他ページの @-ref: " + _r0)
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
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-9-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-9-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Pascal's triangle", "図(a) の題")
in_fig("add the two entries above", "図(a) の作り方")
in_fig("$3 + 3 = 6$", "図(a) の例")
in_fig("(b) Reading a term of $(a+b)^{4}$", "図(b) の題")
in_fig("index of $a$", "図(b) のラベル")
in_fig("index of $b$", "図(b) のラベル")
in_fig("the two indices always add up to $n$", "図(b) の要点")
in_text("(a) Apart from the 1 at each end, every entry of Pascal's triangle"
        " is the sum of the two entries directly above it",
        "キャプションが (a) を説明（両端は例外）")
in_text("(b) In every term the two indices add up to n", "キャプションが (b) を説明")
# 図の値が本文と合っているか
_figrows = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
for _n, _row in enumerate(_figrows):
    chk([C(_n, _r) for _r in range(_n + 1)] == _row, f"図(a) の n={_n} の行")
for _ia, _ib in [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)]:
    chk(_ia + _ib == 4, f"図(b) の指数の和: {_ia}+{_ib}")
chk("[1, 5, 10, 10, 5, 1]" not in FIGSTR, "図に n=5 の行を書かない")
for leak in ["10", "15", "20", "28", "280", "24", "54", "108", "35"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-9.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-8.qmd") < DRAFT.index("aasl-1-9.qmd"), "並びが 1.8 → 1.9")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aasl-1-9.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| binomial theorem |", "| Pascal's triangle |", "| factorial |",
          "| combination |", "| coefficient |", "| expansion |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ══════════════════════════════════════════════════════════
# 13. レビュー反映の見張り
# ══════════════════════════════════════════════════════════
# 演習 1・8 の答えを、本文と例題から消した
# 本文・例題（Exercises より前）には出さない。演習どうしの参照はよい。
_BODY = TEXT[:TEXT.index("## Exercises")]
chk("1, 5, 10, 10, 5, 1" not in _BODY, "n=5 の行は本文・例題に出さない")
chk("1, 6, 15, 20, 15, 6, 1" not in _BODY, "n=6 の行は本文・例題に出さない")
chk("$1, 6, 15, 20, 15, 6, 1$" not in TEXT, "n=6 の行はどこにも出さない")
chk(TEXT.count("1, 5, 10, 10, 5, 1") == 1, "n=5 の行は演習 5 の参照だけ")
chk(TEXT.count("$1, \\ 5, \\ 10, \\ 10, \\ 5, \\ 1$") == 1,
    "演習 1 の解答例にだけ書いてある")
not_in_text("1, \\quad 6, \\quad 15, \\quad 20, \\quad 15, \\quad 6, \\quad 1",
            "同上（第 7 節）")
not_in_text("n=7: \\ 1, 7, 21, 35, 35, 21, 7, 1", "n=7 の行も出さない")
not_in_text("$20$ になるのは $r = 3$ のときだけです。", "演習 8(b) の答えを出さない")
in_text("$^{4}\\mathrm{C}_{r} = 6$ になるのは $r = 2$ のときだけ", "第 7 節は n=4 で説明")
not_in_text("$^{8}\\mathrm{C}_{6}$ を出すなら、$^{8}\\mathrm{C}_{2}$", "演習 2 の方法を出さない")
in_text("$^{9}\\mathrm{C}_{7}$ を出すなら、$^{9}\\mathrm{C}_{2}$", "別の例に差しかえた")
eq(C(9, 7), C(9, 2), "9C7 = 9C2")
eq(C(9, 2), 36, "9C2 = 36")
eq(C(4, 2), 6, "4C2 = 6")
chk([_r for _r in range(5) if C(4, _r) == 6] == [2], "4Cr = 6 は r=2 だけ")
# nC0 = nCn = 1 を書いた
in_text("^{n}\\mathrm{C}_{0} = \\frac{n!}{0!\\,n!} = 1", "nC0 = 1")
in_text("^{n}\\mathrm{C}_{n} = \\frac{n!}{n!\\,0!} = 1", "nCn = 1")
for _n in range(1, 8):
    eq(C(_n, 0), 1, f"{_n}C0 = 1")
    eq(C(_n, _n), 1, f"{_n}C{_n} = 1")
# IB の N は 0 を含む
in_text("**日本の学校では「自然数」に $0$ を含めないのがふつうですが、"
        "IB の $\\mathbb{N}$ は $0$ を含みます。**", "N の約束のちがい")
# (x+1)^20 を最後まで書いた
in_text("^{20}\\mathrm{C}_{2} = \\frac{20 \\times 19}{2 \\times 1} = 190",
        "冒頭の例を最後まで")
eq(C(20, 2), 190, "20C2 = 190")
eq(coeff((x + 1) ** 20, 18), 190, "(x+1)^20 の x^18 の係数は 190")
chk(20 - 2 == 18, "20 - r = 18 なら r = 2")
# 符号が交互になるのは、a と b の符号が逆のとき
in_text("**$a$ と $b$ の符号が逆のときは、符号が $1$ つおきに変わります。**", "条件つき")
not_in_text("**符号は $1$ つおきに変わります。** 展開したとき", "言い切りを直した")
in_text("**$a$ も $b$ も正のときは、すべて $+$ です。**", "Common errors も条件つき")
_pos = sp.Poly(sp.expand((3 * x + 1) ** 3), x).all_coeffs()
chk(all(c > 0 for c in _pos), "(3x+1)^3 の係数はすべて正")
_pos5 = sp.Poly(sp.expand((1 + 2 * x) ** 5), x).all_coeffs()
chk(all(c > 0 for c in _pos5), "(1+2x)^5 の係数もすべて正")
_alt = sp.Poly(sp.expand((2 * x - 3) ** 3), x).all_coeffs()
chk(all(_alt[_i] * _alt[_i + 1] < 0 for _i in range(len(_alt) - 1)),
    "(2x-3)^3 の係数は交互")
# 対称性の条件
in_text("ただし $n$ と $r$ は整数で、$0 \\leq r \\leq n$ のときの話です。", "対称性の条件")
in_text("for integers $n$ and $r$ with $0 \\leq r \\leq n$", "問題文にも条件")
# 例題 1 の検算（順序は x=1 では見つからない）
in_text("**独立なのは、左側だけです。**", "係数の合計は独立ではない")
in_text("**順序は、$x = 0$ で見ます。**", "順序の確かめ方")
_asc = [16, 32, 24, 8, 1]
chk(sum(_asc) == 81, "係数の合計は 81")
chk(sum(_asc) == sum(reversed(_asc)), "順序を逆にしても合計は同じ")
chk(sum(_asc[_i] * (-1) ** _i for _i in range(5)) == 1, "x=-1 でも 1")
chk(sum(list(reversed(_asc))[_i] * (-1) ** _i for _i in range(5)) == 1,
    "逆順でも x=-1 で 1（見つからない）")
ne(_asc[0], list(reversed(_asc))[0], "x=0 なら見分けられる")
# 例題 2 の検算
in_text("^{7}\\mathrm{C}_{4} = \\frac{7!}{4!\\,3!} = \\frac{7 \\times 6 \\times 5"
        " \\times 4}{4 \\times 3 \\times 2 \\times 1} = \\frac{840}{24} = 35",
        "別の数で同じ 35")
in_text("**$7 \\times 6 \\times 5 = 210$ で止めていたら**", "手計算で起きる誤り")
eq(sp.Integer(840) / 24, 35, "840/24 = 35")
ne(210, 35, "210 で止めたら合わない")
# x = 0 の検算が確かめているのは位置
chk(TEXT.count("値が合っているかの確認にはなりません") >= 1, "定数項の検算の限界")
chk(TEXT.count("値の確認にはなりません") >= 1, "同上（演習 3）")
# 例題 4
in_text("^{6}\\mathrm{C}_{3} = {}^{5}\\mathrm{C}_{2} + {}^{5}\\mathrm{C}_{3}"
        " = 10 + 10 = 20", "パスカルの規則で確かめる")
eq(C(5, 2) + C(5, 3), C(6, 3), "5C2 + 5C3 = 6C3")
in_text("32x^{5} - 80x^{4} + 80x^{3} - 40x^{2} + 10x - 1", "例題4(b) の全展開")
eq((2 * x - 1) ** 5,
   32 * x ** 5 - 80 * x ** 4 + 80 * x ** 3 - 40 * x ** 2 + 10 * x - 1,
   "(2x-1)^5 の展開")
eq(32 - 80 + 80 - 40 + 10 - 1, 1, "x=1 で 1")
eq((2 - 1) ** 5, 1, "もとの式も 1")
chk(TEXT.count("検算にはなりません") >= 4, "効かない検算を、効かないと書いている")
in_text("**指数の和 $3 + 3 = 6$ は、検算にはなりません。**", "指数の和は自明")
in_text("**指数の和 $4 + 3 = 7$ は、検算にはなりません。**", "同上（演習 6）")
# model-answer の英語
in_text("$^{5}\\mathrm{C}_{3} = 10$ and $2^{2} = 4$, are both positive",
        "4x^2 ではなく 2^2")
in_text("Replacing $r$ by $n-r$ in the formula gives", "代入の一歩を書く")
# 演習 2 の検算
in_text("7 + 6 + 5 + 4 + 3 + 2 + 1 = 28", "割り算を使わない道すじ")
eq(7 + 6 + 5 + 4 + 3 + 2 + 1, 28, "合計は 28")
eq(C(8, 2), 28, "8C2 = 28")
in_text("**$8 \\times 7 = 56$ で止めていたら**", "手計算で起きる誤り")
ne(56, 28, "56 では合わない")
# 演習 5 を (1+2x)^5 に
in_text("[5]{.ex-no} [Expand $(1+2x)^{5}$", "演習 5 は 5 乗")
eq((1 + 2 * x) ** 5,
   1 + 10 * x + 40 * x ** 2 + 80 * x ** 3 + 80 * x ** 4 + 32 * x ** 5, "演習5")
eq(3 ** 5, 243, "x=1 で 3^5 = 243")
eq(1 + 10 + 40 + 80 + 80 + 32, 243, "係数の合計も 243")
eq(1 - 5 + 10 - 10 + 5 - 1, 0, "x=-1/2 で 0")
eq((1 + 2 * R(-1, 2)) ** 5, 0, "もとの式も 0")
for _r, _c in [(0, 1), (1, 10), (2, 40), (3, 80), (4, 80), (5, 32)]:
    eq(C(5, _r) * 2 ** _r, _c, f"5C{_r} × 2^{_r} = {_c}")
# 演習 6 の検算（r を 1 ずつ増やす）
in_text("^{7}\\mathrm{C}_{2} = 7 \\times \\frac{6}{2} = 21, \\qquad"
        " {}^{7}\\mathrm{C}_{3} = 21 \\times \\frac{5}{3} = 35",
        "階乗を書かない道すじ")
eq(7 * R(6, 2), 21, "7 × 6/2 = 21")
eq(21 * R(5, 3), 35, "21 × 5/3 = 35")
eq(C(7, 2), 21, "7C2 = 21")
# 演習 7 の検算
in_text("**効くのは $x = 1$ の代入です。**", "効く検算を名指し")
eq(16 - 32 + 12 - 8 + 1, -11, "(2x)^2 を 2x^2 とした誤答は x=1 で -11")
ne(-11, 1, "合わない")
# 演習 8 の検算
in_text("**左右対称なのは正しい形ですが、これだけでは検算になりません。**",
        "対称性だけでは足りない")
chk([1, 6, 15, 22, 15, 6, 1] == list(reversed([1, 6, 15, 22, 15, 6, 1])),
    "まちがった行も対称でありうる")
ne(sum([1, 6, 15, 22, 15, 6, 1]), 64, "しかし合計は 64 にならない")
# 演習 4 の言い方
not_in_text("のは偶然ではありません。$1 \\times 27$", "「偶然ではない」を直した")
eq(1 * 27, 3 * 9, "1×27 と 3×9 はたまたま同じ")
# GDC
in_text("| Casio fx-CG50 | `OPTN → PROB → nCr` |", "機種を増やした")
in_text("| TI-84 | `MATH → PRB → nCr` |", "同上")
in_text("`6 nCr 3` の形で入力します", "入力の形")
# Common errors を足した
in_text("## `ascending powers` を、降べきの順で答える", "順序の Common error")
in_text("**符号も係数の一部です。**", "符号の注意")
chk(TEXT.count("::: {.callout-warning}") >= 6, "Common errors が 6 つ以上")


# ══════════════════════════════════════════════════════════
# C12  「単項式」の言い方と、符号の場合分け
# ══════════════════════════════════════════════════════════
in_text("### 6. $a$ や $b$ に係数や符号が付いているとき {#substitution}",
        "C12 第6節の見出し")
not_in_text("$a$ や $b$ が単項式でないとき", "C12 旧見出しが消えている")
in_text("$2x$ も $-3$ も、項が $1$ つだけの式（**monomial**、単項式）です。",
        "C12 monomial の説明")
in_text("**$a$ も $b$ も負なら、共通の $-1$ をくくり出します。**",
        "C12 両方負の場合")
in_text("**$n$ が偶数か奇数かで決まります。**", "C12 偶奇で決まる")
_c12x = sp.Symbol("x")
chk(sp.expand((-2 * _c12x - 3) ** 4 - (2 * _c12x + 3) ** 4) == 0,
    "C12 (-2x-3)^4 = (2x+3)^4")
chk(sp.expand((-2 * _c12x - 3) ** 3 + (2 * _c12x + 3) ** 3) == 0,
    "C12 (-2x-3)^3 = -(2x+3)^3")
chk(all(_v > 0 for _v in
        sp.Poly(sp.expand((2 * _c12x + 3) ** 4), _c12x).all_coeffs()),
    "C12 a も b も正なら係数はすべて正")
_c12s = [sp.sign(_v) for _v in
         sp.Poly(sp.expand((2 * _c12x - 3) ** 4), _c12x).all_coeffs()]
chk(_c12s == [1, -1, 1, -1, 1], "C12 符号が逆なら 1 つおきに変わる")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
