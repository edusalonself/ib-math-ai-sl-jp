"""AA SL 1.5（指数法則と対数の導入）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_5.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-5.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_5.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
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


def _S(x):
    if isinstance(x, float):
        return sp.Rational(str(x))
    return sp.nsimplify(x, rational=True)


def eq(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) == 0, msg + f"  ({a} vs {b})")


def ne(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) != 0, msg + f"  ({a} vs {b})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 指数法則そのもの（記号で）
# ══════════════════════════════════════════════════════════
_a, _b, _m, _n = sp.symbols("a b m n", positive=True)
eq(sp.simplify(_a ** _m * _a ** _n - _a ** (_m + _n)), 0, "積の法則")
eq(sp.simplify(_a ** _m / _a ** _n - _a ** (_m - _n)), 0, "商の法則")
eq(sp.simplify((_a ** _m) ** _n - _a ** (_m * _n)), 0, "累乗の累乗")
eq(sp.simplify((_a * _b) ** _n - _a ** _n * _b ** _n), 0, "積の累乗")
eq(sp.simplify((_a / _b) ** _n - _a ** _n / _b ** _n), 0, "商の累乗")
# a^0 = 1、a^(-n) = 1/a^n は商の法則から出る
eq(_a ** 0, 1, "a^0 = 1")
eq(sp.simplify(_a ** (-_n) - 1 / _a ** _n), 0, "a^(-n) = 1/a^n")
# 底がちがえば法則は使えない（第 1 節の反例）
eq(2 ** 3 * 5 ** 4, 5000, "2^3 × 5^4 = 5000")
eq(10 ** 7, 10000000, "10^7 = 10000000")
ne(5000, 10 ** 7, "5000 と 10^7 はちがう")
# 対数の定義（第 5 節）
for _base, _val in [(2, 8), (3, 81), (10, sp.Rational(1, 100)), (5, 1)]:
    _x = sp.log(_val, _base)
    eq(sp.simplify(sp.Rational(_base) ** _x - _val), 0,
       f"a^x = b と x = log_a b が同じ: a={_base}, b={_val}")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
eq(2 ** 3, 8, "2^3 = 8")
eq(2 ** 3 * 2 ** 4, 2 ** 7, "2^3 × 2^4 = 2^7")
eq(2 ** 7, 128, "2^7 = 128")
eq(sp.Rational(2 ** 5, 2 ** 3), 4, "2^5 / 2^3 = 4")
eq(2 ** 2, 4, "2^2 = 4")
# はしご（第 3 節の表と図）
_ladder = [(3, 8), (2, 4), (1, 2), (0, 1), (-1, sp.Rational(1, 2)),
           (-2, sp.Rational(1, 4))]
for _e, _v in _ladder:
    eq(sp.Rational(2) ** _e, _v, f"2^{_e} = {_v}")
for i in range(len(_ladder) - 1):
    eq(_ladder[i][1] / 2, _ladder[i + 1][1], "1 段下りると半分")
eq(sp.Rational(8, 8), 1, "2^3/2^3 = 1 なので 2^0 = 1")
eq(sp.Rational(8, 32), sp.Rational(1, 4), "2^3/2^5 = 1/4 なので 2^-2 = 1/4")
# 第 4 節
eq((2 * 4) ** 4, 2 ** 4 * 4 ** 4, "(2x)^4 = 2^4 x^4 の形")
eq(2 ** 4, 16, "2^4 = 16")
_x = sp.symbols("x", positive=True)
eq(sp.simplify(2 * _x ** (-3) - 2 / _x ** 3), 0, "2x^-3 = 2/x^3")
eq(sp.simplify((2 * _x) ** (-3) - 1 / (8 * _x ** 3)), 0, "(2x)^-3 = 1/(8x^3)")
eq((2 * sp.Integer(1)) ** (-3), sp.Rational(1, 8), "x=1 で (2x)^-3 = 1/8")
eq(2 * sp.Integer(1) ** (-3), 2, "x=1 で 2x^-3 = 2")
ne(2, sp.Rational(1, 8), "この 2 つは別の値")
# 第 5 節の表
eq(3 ** 4, 81, "3^4 = 81")
eq(sp.Rational(10) ** -2, sp.Rational("0.01"), "10^-2 = 0.01")
eq(5 ** 0, 1, "5^0 = 1")
eq(sp.log(8, 2), 3, "log_2 8 = 3")
# 第 6 節
eq(sp.log(1, 5), 0, "log_a 1 = 0")
eq(sp.log(7, 7), 1, "log_a a = 1")
chk(abs(float(sp.E) - 2.718281828) < 1e-8, "e = 2.718…")
chk(float(sp.E) > 2 and float(sp.E) < 3, "e は 2 と 3 のあいだ")
# 第 7 節
eq(sp.log(32, 2), 5, "log_2 32 = 5")
eq(sp.log(sp.Rational(1, 9), 3), -2, "log_3 (1/9) = -2")

# ══════════════════════════════════════════════════════════
# 2. 例題 1（指数法則）
# ══════════════════════════════════════════════════════════
eq(3 ** 5 * sp.Rational(3) ** -8, sp.Rational(3) ** -3, "例題1(a) 3^-3")
eq(sp.Rational(3 ** 5, 3 ** 8), sp.Rational(3) ** -3, "分数でも 3^-3")
eq(sp.Rational(7 ** 6, 7 ** 2), 7 ** 4, "例題1(b) 7^4")
eq((sp.Rational(4) ** -2) ** 3, sp.Rational(4) ** -6, "例題1(c) 4^-6")
eq(sp.Rational(2) ** 5 * sp.Rational(2) ** -3 / sp.Rational(2) ** -4,
   2 ** 6, "例題1(d) 2^6")
eq(2 ** 6, 64, "2^6 = 64")
eq(32 * sp.Rational(1, 8), 4, "32 × 1/8 = 4")
eq(4 / sp.Rational(1, 16), 64, "4 ÷ 1/16 = 64")
eq(sp.Rational(2) ** -2, sp.Rational(1, 4), "誤答 2^-2 = 1/4")
ne(sp.Rational(1, 4), 64, "その誤答は 64 と合わない")

# ══════════════════════════════════════════════════════════
# 3. 例題 2（係数と文字）
# ══════════════════════════════════════════════════════════
eq(sp.simplify((5 * _x) ** 3 - 125 * _x ** 3), 0, "例題2(a) 125x^3")
eq(5 ** 3, 125, "5^3 = 125")
eq(sp.simplify(6 * _x ** -2 - 6 / _x ** 2), 0, "例題2(b) 6/x^2")
_A, _B = sp.symbols("A B", positive=True)
_lhs = 15 * _A ** 4 * _B ** -2 / (3 * _A ** -1 * _B)
eq(sp.simplify(_lhs - 5 * _A ** 5 / _B ** 3), 0, "例題2(c) 5a^5/b^3")
eq(_lhs.subs({_A: 1, _B: 2}), sp.Rational(5, 8), "a=1,b=2 で 5/8")
eq((5 * sp.Integer(1) ** 5) / sp.Integer(2) ** 3, sp.Rational(5, 8),
   "答えの式でも 5/8")
eq(sp.simplify((6 * _x) ** -2 - 1 / (36 * _x ** 2)), 0, "(6x)^-2 = 1/(36x^2)")
eq(6 * sp.Integer(1) ** -2, 6, "x=1 で 6x^-2 = 6")
eq((6 * sp.Integer(1)) ** -2, sp.Rational(1, 36), "x=1 で (6x)^-2 = 1/36")
ne(6, sp.Rational(1, 36), "この 2 つは別の値")

# ══════════════════════════════════════════════════════════
# 4. 例題 3（指数と対数の書きかえ）
# ══════════════════════════════════════════════════════════
eq(2 ** 6, 64, "例題3(a) 2^6 = 64")
eq(sp.log(64, 2), 6, "log_2 64 = 6")
eq(3 ** 5, 243, "例題3(b) 3^5 = 243")
eq(sp.log(243, 3), 5, "log_3 243 = 5")
eq(5 ** 4, 625, "例題3(c) 5^4 = 625")
eq(sp.log(625, 5), 4, "log_5 625 = 4")
eq(25 ** 2, 625, "25^2 = 625（別の道すじ）")
eq(2 ** 5, 32, "32 = 2^5")
eq(sp.log(sp.Rational(1, 32), 2), -5, "例題3(d) log_2 (1/32) = -5")
chk(sp.Rational(1, 32) < 1, "1/32 は 1 より小さい")
chk(sp.log(sp.Rational(1, 32), 2) < 0, "だから対数は負")
ne(5, -5, "5 と -5 はちがう")

# ══════════════════════════════════════════════════════════
# 5. 例題 4（底 10 と e）
# ══════════════════════════════════════════════════════════
eq(10 ** 5, 100000, "例題4(a) 10^5 = 100000")
eq(sp.log(100000, 10), 5, "log 100000 = 5")
eq(sp.log(sp.E ** 7, sp.E), 7, "例題4(b) ln e^7 = 7")
eq(sp.Rational(10) ** -3, sp.Rational("0.001"), "例題4(c) 10^-3 = 0.001")
eq(sp.log(sp.Rational("0.001"), 10), -3, "log 0.001 = -3")
for _e, _v in [(-1, "0.1"), (-2, "0.01"), (-3, "0.001")]:
    eq(sp.Rational(10) ** _e, sp.Rational(_v), f"10^{_e} = {_v}")
# (d) 4^x は負にならない
for _t in [-3, -1, 0, 1, 3]:
    chk(sp.Rational(4) ** _t > 0, f"4^{_t} > 0")
eq(sp.Rational(4) ** -1, sp.Rational(1, 4), "4^-1 = 1/4")
eq(4 ** 0, 1, "4^0 = 1")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(3 ** 7 * sp.Rational(3) ** -5, 9, "演習1 = 9")
eq(sp.Rational(3 ** 7, 3 ** 5), 9, "分数でも 9")
eq(3 ** 2, 9, "3^2 = 9")
chk(sp.Rational(3) ** -35 < 1, "誤答 3^-35 は 1 より小さい")
ne(sp.Rational(3) ** -35, 9, "その誤答は 9 と合わない")

eq(sp.Rational(5 ** 4, 5 ** 7), sp.Rational(5) ** -3, "演習2(a) 5^-3")
eq(5 ** 4, 625, "5^4 = 625")
eq(5 ** 7, 78125, "5^7 = 78125")
eq(sp.Rational(625, 78125), sp.Rational(1, 125), "625/78125 = 1/125")
eq(sp.Rational(5) ** -3, sp.Rational(1, 125), "5^-3 = 1/125")
eq((sp.Rational(2) ** -3) ** -2, 2 ** 6, "演習2(b) 2^6")
eq((sp.Rational(1, 8)) ** -2, 64, "(1/8)^-2 = 64")
eq(sp.Rational(2) ** -6, sp.Rational(1, 64), "誤答 2^-6 = 1/64")
ne(sp.Rational(1, 64), 64, "その誤答は 64 と合わない")

eq(sp.simplify(7 * _x ** -4 - 7 / _x ** 4), 0, "演習3(a) 7/x^4")
eq(sp.simplify((3 * _x) ** -2 - 1 / (9 * _x ** 2)), 0, "演習3(b) 1/(9x^2)")
eq(3 ** 2, 9, "3^2 = 9（分母に出る）")
eq(7 * sp.Integer(1) ** -4, 7, "x=1 で (a) は 7")
eq((3 * sp.Integer(1)) ** -2, sp.Rational(1, 9), "x=1 で (b) は 1/9")

_ex4 = 20 * _A ** 6 * _B ** -1 / (5 * _A ** 2 * _B ** -3)
eq(sp.simplify(_ex4 - 4 * _A ** 4 * _B ** 2), 0, "演習4 4a^4b^2")
eq(_ex4.subs({_A: 1, _B: 2}), 16, "a=1,b=2 で 16")
eq(4 * sp.Integer(1) ** 4 * sp.Integer(2) ** 2, 16, "答えの式でも 16")
eq(20 * sp.Integer(1) * sp.Rational(1, 2), 10, "分子は 10")
eq(5 * sp.Integer(1) * sp.Rational(1, 8), sp.Rational(5, 8), "分母は 5/8")
eq(10 / sp.Rational(5, 8), 16, "10 ÷ 5/8 = 16")
eq(4 * sp.Rational(1, 16), sp.Rational(1, 4), "誤答 b^-4 なら 1/4")
ne(sp.Rational(1, 4), 16, "その誤答は 16 と合わない")

eq(4 ** 3, 64, "演習5(a) 4^3 = 64")
eq(sp.log(64, 4), 3, "log_4 64 = 3")
eq(6 ** 2, 36, "演習5(b) 6^2 = 36")
eq(sp.log(36, 6), 2, "log_6 36 = 2")
ne(64 ** 3, 4, "log_64 4 = 3 は成り立たない")

eq(7 ** 2, 49, "演習6(a) 7^2 = 49")
eq(sp.log(49, 7), 2, "log_7 49 = 2")
eq(2 ** 4, 16, "16 = 2^4")
eq(sp.log(sp.Rational(1, 16), 2), -4, "演習6(b) log_2 (1/16) = -4")
eq(sp.Rational(10) ** -4, sp.Rational("0.0001"), "10^-4 = 0.0001")
eq(sp.log(sp.Rational("0.0001"), 10), -4, "演習6(c) log 0.0001 = -4")
for _v in [sp.Rational(1, 16), sp.Rational("0.0001")]:
    chk(_v < 1, f"{_v} は 1 より小さい")

eq(10 ** 6, 1000000, "演習7(a) 10^6 = 1000000")
eq(sp.log(1000000, 10), 6, "log 1000000 = 6")
eq(sp.simplify(sp.E ** -5 - 1 / sp.E ** 5), 0, "演習7(b) e^-5 = 1/e^5")
chk(sp.E ** 5 > 1, "e^5 は 1 より大きい")
chk(sp.E ** -5 < 1, "e^-5 は 1 より小さい")

eq(sp.log(10000, 10), 4, "演習8(a) M = 4")
eq(100 * 10000, 10 ** 6, "100 × 10000 = 10^6")
eq(sp.log(1000000, 10), 6, "演習8(b) M = 6")
eq(6 - 4, 2, "演習8(c) 増加は 2")
eq(sp.log(100, 10), 2, "100 倍は log で 2 の増加")
ne(400, 6, "誤答 400 は 6 ではない")

for _base in [2, 3, 7, 10]:
    eq(sp.Rational(_base) ** 0, 1, f"{_base}^0 = 1")
    eq(sp.log(1, _base), 0, f"log_{_base} 1 = 0")
chk(all(sp.Integer(1) ** _t == 1 for _t in [-2, 0, 3, 5]),
    "底 1 は使えない（1^x はいつも 1）")

eq(sp.Rational(3 ** 8, 3 ** 2), 3 ** 6, "演習10 正しい答え 3^6")
eq(3 ** 6, 729, "3^6 = 729")
eq(3 ** 4, 81, "生徒の答え 3^4 = 81")
ne(81, 729, "生徒の答えは合わない")
eq(sp.Rational(2 ** 4, 2 ** 2), 4, "2^4/2^2 = 4")
eq(2 ** 2, 4, "たまたま 2^(4÷2) と一致する")
eq(sp.Rational(2 ** 5, 2 ** 2), 8, "2^5/2^2 = 8")
eq(2 ** 3, 8, "= 2^3")
ne(sp.Rational(2) ** sp.Rational(5, 2), 8, "2^2.5 は 8 ではない")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.5** の欄に `Exponents and logarithms` として印刷",
        "公式集にある")
in_text("> $a^{x} = b \\iff x = \\log_{a} b$, where $a > 0$, $b > 0$, $a \\neq 1$",
        "公式集の条件を逐語で")
in_text("> Awareness that $a^x = b$ is equivalent to $\\log_ab = x$, "
        "that $b > 0$, and $\\log_e x = \\ln x$.", "シラバスの Guidance を逐語で")
in_text("> Numerical evaluation of logarithms using technology.",
        "電卓の Guidance")
in_text("## この $5$ つは、公式集にありません", "指数法則は載っていないと明記")
in_text("**指数法則そのものは、どこにも載っていません。**", "同上（本文）")
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
chk(len(re.findall(r"^::: \{#exm-aasl15-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(m) for m in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
# \$（通貨の $）は数式の区切りではないので、先に伏せる（tools/README.md）
_MASKED = TEXT.replace("\\$", "")
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
    chk(_r0 == "aasl15", "他ページの @-ref: " + _r0)
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
SVG = os.path.join(BASE, "img", "aasl-1-5-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-5-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Each step down divides by", "図(a) の題")
in_fig("forced,\\nnot chosen", "図(a) の要点")
in_fig("One fact, written two ways", "図(b) の題")
in_fig("a logarithm is the exponent you are looking for", "図(b) の要点")
for _lab in ["base", "exponent", "value"]:
    in_fig('"' + _lab + '"', "図(b) のラベル " + _lab)
in_text("(a) Going down the ladder, each step divides by 2",
        "キャプションが (a) を説明")
in_text("(b) The same statement written two ways",
        "キャプションが (b) を説明")
# 図の値が本文と合っているか
for _e, _v in _ladder:
    eq(sp.Rational(2) ** _e, _v, f"図(a) の {_e} 段目")
eq(sp.log(8, 2), 3, "図(b) の log_2 8 = 3")
for leak in ["49", "36", "64", "125", "243", "625", "729", "0.0001",
             "78125", "1000000"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-5.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-4.qmd") < DRAFT.index("aasl-1-5.qmd"), "並びが 1.4 → 1.5")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aasl-1-5.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_m = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_m is not None and int(_m.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| exponent |", "| base |", "| laws of exponents |",
          "| logarithm |", "| natural logarithm ($\\ln$) |",
          "| simplify |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ══════════════════════════════════════════════════════════
# 12. レビュー反映の見張り
# ══════════════════════════════════════════════════════════
in_text("## 指数を足せるのは、底がそろっているときだけです", "積の累乗は底がちがってよい")
not_in_text("指数法則が使えるのは、**底（下の数）が同じとき**だけだと覚えて",
            "言い過ぎの一文は消した")
in_text("$$\na^{0} = 1, \\qquad a^{-n} = \\frac{1}{a^{n}} \\qquad (a \\neq 0)\n$$",
        "a ≠ 0 を両方にかける")
in_text("$\\dfrac{a^{m}}{a^{n}} = a^{m-n}$（$a \\neq 0$）", "商の法則に条件")
in_text("$\\left(\\dfrac{a}{b}\\right)^{n} = \\dfrac{a^{n}}{b^{n}}$（$b \\neq 0$）",
        "商の累乗に条件")
not_in_text("$\\log_{4} 64$ が分からなければ", "演習 5(a) の答えを本文から消した")
in_text("$\\log_{9} 81$ が分からなければ", "別の例に差しかえた")
eq(sp.log(81, 9), 2, "log_9 81 = 2")
eq(9 ** 2, 81, "9^2 = 81")
in_text("$8 \\to 4 \\to 2 \\to 1 \\to \\dfrac{1}{2} \\to \\dfrac{1}{4}$", "はしごを表の左端から")
in_text("$\\log_{a} b$ が**整数になるのは、$b$ が $a$ の整数乗のとき**です。", "「きれいな値」を直した")
not_in_text("$\\log_{8} 2$ は別の数（$\\dfrac{1}{3}$）です。", "1.7 の内容を先取りしない")
not_in_text("値がありません", "undefined の言い方にそろえた")
in_text("は、定義されません", "同上")
in_text("*undefined* または *not defined* と書き", "答案の書き方")
not_in_text("*no value*", "no value は使わない")
in_text("giving each answer as a single power", "複数形をそろえた")
in_text("[Hence find the increase in magnitude from P to Q.]{.q-en}", "State ではなく Hence find")
not_in_text("[State the increase in magnitude", "State は使えない")
in_text("in the form $ax^{n}$", "かっこを外す指示を IB の書き方に")
in_text("are not equivalent", "同上")
in_text("[Solve the equation $10^{x} = 0.001$.]{.q-en}", "Solve the equation")
in_text("an earthquake of amplitude $A$", "tremor → earthquake")
in_text("**logarithm**（対数）", "英語が先、日本語が括弧")
in_text("も、決め方は $1$ 通りしかありません。**", "「勝手に決めた約束ではない」を直した")
in_text("[SL 1.7a](aasl-1-7a.qmd)", "整数でない指数は 1.7a に送る")
# 0 と 1 を代入に使わない
in_text("## $0$ と $1$ は、代入して確かめる値に向きません", "代入値の注意")
_A2, _B2 = sp.symbols("A2 B2", positive=True)
_e2 = 15 * _A2 ** 4 * _B2 ** -2 / (3 * _A2 ** -1 * _B2)
eq(_e2.subs({_A2: 2, _B2: 3}), sp.Rational(160, 27), "a=2,b=3 で 160/27")
eq(5 * sp.Integer(2) ** 5 / sp.Integer(3) ** 3, sp.Rational(160, 27), "答えの式でも 160/27")
eq(5 * sp.Integer(2) ** 3 / sp.Integer(3) ** 3, sp.Rational(40, 27), "a の指数を 3 とした誤答")
ne(sp.Rational(40, 27), sp.Rational(160, 27), "その誤答は見分けられる")
eq(_e2.subs({_A2: 1, _B2: 2}), sp.Rational(5, 8), "a=1 では")
eq(5 * sp.Integer(1) ** 3 / sp.Integer(2) ** 3, sp.Rational(5, 8), "誤答も同じ値になってしまう")
_e4 = 20 * _A2 ** 6 * _B2 ** -1 / (5 * _A2 ** 2 * _B2 ** -3)
eq(_e4.subs({_A2: 3, _B2: 2}), 1296, "a=3,b=2 で 1296")
eq(4 * sp.Integer(3) ** 4 * sp.Integer(2) ** 2, 1296, "答えの式でも 1296")
eq(4 * sp.Integer(3) ** 4 * sp.Rational(1, 16), sp.Rational(81, 4), "b^-4 の誤答")
ne(sp.Rational(81, 4), 1296, "その誤答は見分けられる")
eq(7 * sp.Rational(2) ** -4, sp.Rational(7, 16), "x=2 で 7x^-4")
eq(sp.Rational(1, 7 * 2 ** 4), sp.Rational(1, 112), "1/(7x^4) の誤答")
ne(sp.Rational(1, 112), sp.Rational(7, 16), "その誤答は見分けられる")
eq((3 * sp.Integer(2)) ** -2, sp.Rational(1, 36), "x=2 で (3x)^-2")
eq((7 * sp.Integer(2)) ** -4, sp.Rational(1, 14 ** 4), "(7x)^-4 は x=2 で 1/14^4")
# 演習 2 の検算
eq(sp.Rational(1, 8) ** -2, 64, "(1/8)^-2 = 64")
in_text("上に $5$ が $4$ 個、下に $7$ 個です", "書き出して消す検算")
not_in_text("$\\dfrac{625}{78\\,125}$", "重い割り算は使わない")
# 演習 7(a) の検算
in_text("$10^{3} = 1000$ で、$1000 \\times 1000 = 1\\,000\\,000$", "0 を数え直さない検算")
eq(1000 * 1000, 10 ** 6, "1000 × 1000 = 10^6")
eq(10 ** 7, 10000000, "x=7 なら桁が 1 つ多い")
# 演習 9 の検算が循環していた
not_in_text("いくつかの底で確かめます。$2^{0} = 1$", "a^0 = 1 を使う検算は消した")
in_text("**示したい $a^{0} = 1$ を仮定せずに出しているのが要です。**", "非循環の検算")
eq(sp.Rational(8, 8), 1, "8/8 = 1")
eq(sp.Rational(1000, 1000), 1, "1000/1000 = 1")
# 追加した Common errors
in_text("## 負の指数で割るとき、マイナスを $1$ つ落とす", "6 つめの Common error")
eq(sp.Rational(2 ** 2, 1) / sp.Rational(2) ** -4, 64, "2^2 / 2^-4 = 64")
eq(sp.Rational(2) ** -2, sp.Rational(1, 4), "2 - 4 とした誤答")
chk(TEXT.count("::: {.callout-warning}") >= 9, "callout-warning が十分ある")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
