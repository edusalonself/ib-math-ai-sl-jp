"""AA SL 1.7b（対数法則・底の変換・指数方程式）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_7b.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-7b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_7b.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x", real=True)
a, y, p, q = sp.symbols("a y p q", positive=True)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def lg(v, b):
    """log_b(v) を、値になるところまで簡単にする。"""
    return sp.simplify(sp.log(v, b))


def eq(u, v, msg=""):
    chk(sp.simplify(u - v) == 0, msg + f"  ({u} vs {v})")


def ne(u, v, msg=""):
    chk(sp.simplify(u - v) != 0, msg + f"  ({u} vs {v})")


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
# 0. 法則そのもの（記号で）
# ══════════════════════════════════════════════════════════
_b = sp.Symbol("b", positive=True)
eq(sp.expand_log(sp.log(x * y, a), force=True),
   sp.log(x, a) + sp.log(y, a), "積の法則")
eq(sp.expand_log(sp.log(x / y, a), force=True),
   sp.log(x, a) - sp.log(y, a), "商の法則")
_m = sp.Symbol("m", positive=True)
eq(sp.expand_log(sp.log(x ** _m, a), force=True),
   _m * sp.log(x, a), "累乗の法則")
eq(sp.simplify(sp.log(x, a) - sp.log(x, _b) / sp.log(a, _b)), 0, "底の変換")
# 打ち消し合う 2 つ
eq(sp.simplify(sp.log(a ** x, a) - x), 0, "log_a a^x = x")
eq(sp.simplify(a ** sp.log(x, a) - x), 0, "a^(log_a x) = x")
eq(sp.simplify(a ** x - sp.exp(x * sp.log(a))), 0, "a^x = e^(x ln a)")
# 和には法則がない（反例）
ne(sp.log(2, 10), sp.log(1, 10) + sp.log(1, 10), "log(1+1) ≠ log1 + log1")
eq(sp.log(1, 10) + sp.log(1, 10), 0, "log1 + log1 = 0")
ne(sp.log(2, 10), 0, "log 2 は 0 ではない")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
eq(2 ** 3 * 2 ** 2, 2 ** 5, "2^3 × 2^2 = 2^5")
eq(lg(8, 2), 3, "log_2 8 = 3")
eq(lg(4, 2), 2, "log_2 4 = 2")
eq(lg(32, 2), 5, "log_2 32 = 5")
eq(lg(8, 2) + lg(4, 2), lg(32, 2), "3 + 2 = 5")
eq(8 * 4, 32, "8 × 4 = 32")
# 第 2 節の使い分け
eq(lg(9 ** 4, 3), 8, "log_3 9^4 = 8")
eq(lg(9, 3), 2, "log_3 9 = 2")
eq(3 * lg(2, 10), lg(8, 10), "3 log 2 = log 8")
# 第 3 節
eq(lg(125, 25), R(3, 2), "log_25 125 = 3/2")
eq(lg(125, 5), 3, "log_5 125 = 3")
eq(lg(25, 5), 2, "log_5 25 = 2")
eq(R(25) ** R(3, 2), 125, "25^(3/2) = 125（戻し）")
eq(sp.simplify(sp.log(7, 4) - sp.log(7) / sp.log(4)), 0, "log_4 7 = ln7/ln4")
# a = b にすると正しい向きが見える（Common errors）
eq(sp.simplify(sp.log(x, a) / sp.log(a, a) - sp.log(x, a)), 0, "b = a なら元に戻る")
# 第 4 節
eq(lg(2 ** 7, 2), 7, "log_2 2^7 = 7")
eq(5 ** sp.log(9, 5), 9, "5^(log_5 9) = 9")
# 第 5 節
eq(2 * lg(3, 5) + lg(2, 5), lg(18, 5), "2log_5 3 + log_5 2 = log_5 18")
eq(3 ** 2 * 2, 18, "3^2 × 2 = 18")
eq(2 ** 2 * 3, 12, "12 = 2^2 × 3")
eq(sp.expand_log(sp.log(12, a), force=True),
   2 * sp.log(2, a) + sp.log(3, a), "log_a 12 = 2p + q")
# 第 6 節
chk(sols(sp.Eq(9 ** x, 27)) == [R(3, 2)], "9^x = 27 の解は 3/2")
eq(3 ** 2, 9, "9 = 3^2")
eq(3 ** 3, 27, "27 = 3^3")
# 第 7 節
eq(sols(sp.Eq(5 ** x, 12))[0], sp.log(12) / sp.log(5), "5^x = 12 の解")
eq(sp.simplify(sp.log(12) / sp.log(5) - sp.log(12, 10) / sp.log(5, 10)), 0,
   "底は 10 でも e でも同じ")
chk(1 < float(sp.log(12) / sp.log(5)) < 2, "解は 1 と 2 のあいだ")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
_M, _N = sp.symbols("M N", real=True)
eq(sp.simplify(a ** _M * a ** _N - a ** (_M + _N)), 0, "導出に使う指数法則")
eq(sp.simplify(sp.log(a ** _M, a) - _M), 0, "対数の形に戻す")

# ══════════════════════════════════════════════════════════
# 3. 例題 1
# ══════════════════════════════════════════════════════════
eq(lg(6, 10) + lg(5, 10), lg(30, 10), "例題1(a) log 30")
eq(6 * 5, 30, "6 × 5 = 30")
eq(lg(24, 2) - lg(3, 2), lg(8, 2), "例題1(b) log_2 8")
eq(lg(8, 2), 3, "= 3")
eq(R(24, 3), 8, "24/3 = 8")
chk(lg(16, 2) == 4 and lg(32, 2) == 5, "log_2 24 は 4 と 5 のあいだ")
chk(4 < float(sp.log(24, 2)) < 5, "実際に 4 台")
chk(1 < float(sp.log(3, 2)) < 2, "log_2 3 は 1 台")
eq(2 * lg(3, 5) + lg(2, 5), lg(18, 5), "例題1(c) log_5 18")
eq(lg(9, 5) + lg(2, 5), lg(18, 5), "log_5 9 + log_5 2")
ne(lg(6, 5), lg(18, 5), "誤答 log_5 6 は合わない")

# ══════════════════════════════════════════════════════════
# 4. 例題 2
# ══════════════════════════════════════════════════════════
eq(lg(40, 2) - lg(5, 2), 3, "例題2(a) 3")
eq(R(40, 5), 8, "40/5 = 8")
eq(lg(9 ** 4, 3), 8, "例題2(b) 8")
eq(4 * lg(9, 3), 8, "4 × 2 = 8")
eq(sp.Integer(9) ** 4, 3 ** 8, "9^4 = 3^8")
eq(lg(3 ** 8, 3), 8, "log_3 3^8 = 8")
eq(lg(4, 10) + lg(25, 10), 2, "例題2(c) 2")
eq(4 * 25, 100, "4 × 25 = 100")
eq(lg(100, 10), 2, "log 100 = 2")
eq(lg(125, 25), R(3, 2), "例題2(d) 3/2")
eq(R(25) ** R(3, 2), 125, "戻すと 125")
ne(R(25) ** R(2, 3), 125, "誤答 2/3 では 125 にならない")
chk(lg(125, 25) > 1, "答えは 1 より大きい")

# ══════════════════════════════════════════════════════════
# 5. 例題 3（底をそろえる）
# ══════════════════════════════════════════════════════════
chk(sols(sp.Eq(2 ** x, 32)) == [5], "例題3(a) 5")
chk(sols(sp.Eq(9 ** x, 27)) == [R(3, 2)], "例題3(b) 3/2")
chk(sols(sp.Eq(R(1, 2) ** x, 8)) == [-3], "例題3(c) -3")
chk(sols(sp.Eq(4 ** (x + 1), 8 ** x)) == [2], "例題3(d) 2")
eq(2 ** 5, 32, "検算 (a)")
eq(R(9) ** R(3, 2), 27, "検算 (b)")
eq(R(1, 2) ** -3, 8, "検算 (c)")
eq(4 ** 3, 64, "検算 (d) 左辺")
eq(8 ** 2, 64, "検算 (d) 右辺")
eq(R(1, 2) ** 3, R(1, 8), "誤答 x=3 なら 1/8")
ne(R(1, 8), 8, "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 6. 例題 4（対数をとる）
# ══════════════════════════════════════════════════════════
eq(sols(sp.Eq(5 ** x, 12))[0], sp.log(12) / sp.log(5), "例題4(a)")
chk(1 < float(sp.log(12) / sp.log(5)) < 2, "1 と 2 のあいだ")
chk(float(sp.log(5) / sp.log(12)) < 1, "上下を逆にすると 1 未満")
eq(sols(sp.Eq(2 ** (x - 1), 10))[0], 1 + sp.log(10, 2), "例題4(b)")
eq(sp.simplify(2 ** ((1 + sp.log(10, 2)) - 1)), 10, "入れ直すと 10")
eq(sp.log(2, 10) + sp.log(1, 10) * 0, sp.log(2, 10), "log 2 はそのまま")
eq(sp.log(1, 10), 0, "log 1 = 0")
ne(sp.log(2, 10), 0, "log(1+1) は 0 ではない")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(lg(7, 10) + lg(4, 10), lg(28, 10), "演習1 log 28")
eq(7 * 4, 28, "7 × 4 = 28")
ne(lg(11, 10), lg(28, 10), "誤答 log 11 は合わない")

eq(lg(45, 3) - lg(5, 3), 2, "演習2(a) 2")
eq(R(45, 5), 9, "45/5 = 9")
eq(3 ** 2, 9, "9 = 3^2")
eq(9 * 5, 45, "9 × 5 = 45（戻し）")
eq(lg(8 ** 3, 2), 9, "演習2(b) 9")
eq(3 * lg(8, 2), 9, "3 × 3 = 9")
eq(sp.Integer(8) ** 3, 2 ** 9, "8^3 = 2^9")

eq(lg(50, 10) + lg(2, 10), 2, "演習3 2")
eq(50 * 2, 100, "50 × 2 = 100")
chk(1 < float(sp.log(50, 10)) < 2, "log 50 は 1 台")
chk(0 < float(sp.log(2, 10)) < 1, "log 2 は 0 台")
eq(sp.simplify(lg(50, 10) - (2 - lg(2, 10))), 0, "log 50 = 2 - log 2")

eq(sp.expand_log(sp.log(18, a), force=True),
   sp.log(2, a) + 2 * sp.log(3, a), "演習4 p + 2q")
eq(2 * 3 ** 2, 18, "18 = 2 × 3^2")
eq(sp.simplify(sp.log(18, 3) - (sp.log(2, 3) + 2)), 0, "a=3 での検算")
ne(2 * sp.log(2, a) + sp.log(3, a), sp.log(18, a), "誤答 2p+q は合わない")
eq(4 * 3, 12, "2p+q は 12 のほう")

eq(lg(32, 8), R(5, 3), "演習5 5/3")
eq(lg(32, 2), 5, "log_2 32 = 5")
eq(lg(8, 2), 3, "log_2 8 = 3")
eq(R(8) ** R(5, 3), 32, "8^(5/3) = 32（戻し）")
chk(1 < float(sp.log(32, 8)) < 2, "答えは 1 と 2 のあいだ")
chk(float(R(3, 5)) < 1, "逆にすると 1 未満")

chk(sols(sp.Eq(3 ** x, 81)) == [4], "演習6(a) 4")
eq(3 ** 4, 81, "3^4 = 81")
chk(sols(sp.Eq(R(1, 5) ** x, 125)) == [-3], "演習6(b) -3")
eq(R(1, 5) ** -3, 125, "戻すと 125")
eq(R(1, 5) ** 3, R(1, 125), "誤答 x=3 なら 1/125")
ne(R(1, 125), 125, "その誤答は合わない")

chk(sols(sp.Eq(8 ** x, 16 ** (x - 1))) == [4], "演習7 4")
eq(8 ** 4, 4096, "8^4 = 4096")
eq(16 ** 3, 4096, "16^3 = 4096")
eq(2 ** 12, 4096, "= 2^12")
eq(4 * (4 - 1), 12, "4(x-1) は x=4 で 12")
eq(3 * 4, 12, "3x も 12")
# 4x - 1 と読みちがえた場合
chk(sp.solve(sp.Eq(3 * x, 4 * x - 1), x) == [1], "誤答なら x=1")
eq(8 ** 1, 8, "x=1 で左辺は 8")
eq(16 ** 0, 1, "x=1 で右辺は 1")
ne(8, 1, "その誤答は合わない")

eq(sols(sp.Eq(7 ** x, 30))[0], sp.log(30) / sp.log(7), "演習8")
eq(7 ** 2, 49, "7^2 = 49")
chk(1 < float(sp.log(30) / sp.log(7)) < 2, "1 と 2 のあいだ")
chk(float(sp.log(7) / sp.log(30)) < 1, "上下を逆にすると 1 未満")

eq(sp.expand_log(sp.log(x ** _m, a), force=True), _m * sp.log(x, a), "演習9")
eq(lg(4 ** 3, 2), 6, "a=2,x=4,m=3 の左辺")
eq(3 * lg(4, 2), 6, "同じく右辺")
eq(lg(4, 2) ** 3, 8, "(log_2 4)^3 は 8")
ne(8, 6, "log の外の指数とは別物")

eq(lg(8, 10) - lg(2, 10), lg(4, 10), "演習10 正しい答え log 4")
eq(R(8, 2), 4, "8/2 = 4")
ne(lg(6, 10), lg(4, 10), "生徒の log 6 は合わない")
eq(lg(8, 2) - lg(2, 2), 2, "底 2 で 3 - 1 = 2")
eq(lg(4, 2), 2, "log_2 4 = 2")
chk(2 < float(sp.log(6, 2)) < 3, "log_2 6 は 2 と 3 のあいだ")

# ══════════════════════════════════════════════════════════
# 8. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この $3$ つは公式集にあります", "対数法則は載っていると明記")
in_text("> $\\log_{a} xy = \\log_{a} x + \\log_{a} y$", "積の法則を逐語で")
in_text("> $\\log_{a} \\dfrac{x}{y} = \\log_{a} x - \\log_{a} y$", "商の法則を逐語で")
in_text("> $\\log_{a} x^{m} = m \\log_{a} x$", "累乗の法則を逐語で")
in_text("> for $a$, $x$, $y > 0$", "条件を逐語で")
in_text("> $\\log_{a} x = \\dfrac{\\log_{b} x}{\\log_{b} a}$",
        "底の変換を逐語で（公式集）")
in_text("> for $a$, $b$, $x > 0$", "条件はシラバスの Content 欄")
in_text("> $\\log_47 = \\dfrac{\\ln7}{\\ln4}$", "シラバスの例を逐語で")
in_text("> $a^{x} = \\mathrm{e}^{x \\ln a}$ ; $\\log_{a} a^{x} = x = a^{\\log_{a} x}$"
        " where $a$, $x > 0$, $a \\neq 1$", "指数・対数関数の欄を逐語で")
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
in_text("**Paper 1 では、$\\dfrac{\\ln 7}{\\ln 3}$ が答えです。**",
        "Paper 1 は正確な形で止めると明記")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aasl17b-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl17b", "他ページの @-ref: " + _r0)
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
SVG = os.path.join(BASE, "img", "aasl-1-7b-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-7b-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Multiplying below, adding above (base $2$)", "図(a) の題")
in_fig("a product becomes a sum", "図(a) の要点")
in_fig("values", "図(a) の下段ラベル")
in_fig("Change of base: pick $b$ you can do by hand", "図(b) の題")
in_fig("take $b = 5$", "図(b) の選び方")
in_text("(a) Multiplying values corresponds to adding exponents",
        "キャプションが (a) を説明")
in_text("(b) Change of base rewrites one logarithm as a ratio",
        "キャプションが (b) を説明")
eq(lg(8, 2) + lg(4, 2), lg(32, 2), "図(a) の 3 + 2 = 5")
eq(lg(125, 25), R(3, 2), "図(b) の 3/2")
eq(5 ** 3, 125, "図(b) の 125 = 5^3")
eq(5 ** 2, 25, "図(b) の 25 = 5^2")
for _lk in ["28", "45", "81", "30", "4096", "5}{3", "16"]:
    chk(_lk not in FIGSTR, "図が演習の答えを載せている: " + _lk)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-7b.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-7a.qmd") < DRAFT.index("aasl-1-7b.qmd"),
    "並びが 1.7a → 1.7b")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aasl-1-7b.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| laws of logarithms |", "| change of base |",
          "| exponential equation |", "| exact value |", "| logarithm |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ══════════════════════════════════════════════════════════
# 13. レビュー反映の見張り
# ══════════════════════════════════════════════════════════
# 条件（a ≠ 1、b ≠ 1）
in_text("これに加えて、**底は $a \\neq 1$** でなければなりません。", "対数法則に a ≠ 1")
in_text("これに加えて、**$a \\neq 1$ と $b \\neq 1$** が要ります。", "底の変換に条件")
in_text("条件は、シラバスの Content 欄のほうに書かれています。", "条件の出どころを正しく")
chk(all(sp.Integer(1) ** _t == 1 for _t in [-3, 0, 2, 7]), "1 は何乗しても 1")
# log(x+y) は「一般には」等しくない
in_text("（正確には「一般には等しくない」です。", "特別な場合がある")
in_text("一般に $\\log_{a}(x + y) \\neq \\log_{a} x + \\log_{a} y$ です", "Common errors も同様")
eq(sp.log(4, 10), sp.log(2, 10) + sp.log(2, 10), "x=y=2 ではたまたま一致")
eq(2 + 2, 2 * 2, "x + y = xy の場合")
in_text("for all positive $x$ and $y$", "問題文も「すべての」に")
# 第 4 節の言い方と条件
in_text("どちらの式も、$a > 0$、$a \\neq 1$、$x > 0$ のときに使えます。", "打ち消しの条件")
not_in_text("実際にその回数だけ掛ければ", "「回数」の言い方を直した")
# 本文が例題の答えを書いていた 4 か所
in_text("$\\log_{2} 4^{5} = 5 \\log_{2} 4 = 5 \\times 2 = 10$", "第 2 節の例を差しかえた")
eq(lg(4 ** 5, 2), 10, "log_2 4^5 = 10")
not_in_text("- **前に出す。** $\\log_{3} 9^{4}", "例題 2(b) と重ならない")
in_text("2\\log_{3} 2 + \\log_{3} 5 = \\log_{3} 2^{2} + \\log_{3} 5"
        " = \\log_{3} 4 + \\log_{3} 5 = \\log_{3} 20", "第 5 節の例を差しかえた")
eq(2 * lg(2, 3) + lg(5, 3), lg(20, 3), "2log_3 2 + log_3 5 = log_3 20")
eq(2 ** 2 * 5, 20, "4 × 5 = 20")
in_text("$$\n8^{x} = 4\n$$", "第 6 節の例を差しかえた")
chk(sols(sp.Eq(8 ** x, 4)) == [R(2, 3)], "8^x = 4 の解は 2/3")
eq(2 ** 3, 8, "8 = 2^3")
in_text("$$\n3^{x} = 7\n$$", "第 7 節の例を差しかえた")
eq(sols(sp.Eq(3 ** x, 7))[0], sp.log(7) / sp.log(3), "3^x = 7 の解")
chk(abs(float(sp.log(7) / sp.log(3)) - 1.7712437) < 1e-6, "1.7712…")
chk(1 < float(sp.log(7) / sp.log(3)) < 2, "1 と 2 のあいだ")
in_text("有効数字 $3$ 桁**で $x = 1.77$", "3 s.f. の指示")
chk(round(float(sp.log(7) / sp.log(3)), 2) == 1.77, "3 s.f. で 1.77")
in_text("方法点（M mark）", "途中式の点の呼び方")
not_in_text("`ln(12)/ln(5)`", "GDC の例も差しかえた")
# 例題 2(d) を、本文・図と別の数にした
in_text("**(d)** [$\\log_{9} 27$]{.q-en}", "例題 2(d) は log_9 27")
eq(lg(27, 9), R(3, 2), "log_9 27 = 3/2")
eq(lg(27, 3), 3, "log_3 27 = 3")
eq(lg(9, 3), 2, "log_3 9 = 2")
eq(R(9) ** R(3, 2), 27, "9^(3/2) = 27（戻し）")
chk(R(9) ** R(2, 3) < 9, "9^(2/3) は 9 より小さい")
chk(9 < 27, "だから 27 には届かない")
not_in_text("**(d)** [$\\log_{25} 125$]{.q-en}", "図と同じ数を出題しない")
# Why it works の条件
in_text("以下、$a > 0$、$a \\neq 1$、$x > 0$、$y > 0$ とします。", "導出の前提")
in_text("**$b$ は、$b > 0$、$b \\neq 1$ でありさえすれば、どれを選んでも同じ値になります。**",
        "b の条件を正しく")
in_text("$\\log_{b} a \\neq 0$、つまり **$a \\neq 1$** が要ります。", "割り算の条件")
not_in_text("どこにも $b$ の条件を使っていないからです", "矛盾した一文を消した")
# 検算の独立性
in_text("この $8$ に、引いた $\\log_{2} 3$ の中身 $3$ を掛け戻すと $8 \\times 3 = 24$",
        "例題 1(b) の非循環な検算")
in_text("**範囲を絞るだけで、値を決める検算ではありません。**", "見積もりの限界")
eq(8 * 3, 24, "8 × 3 = 24")
in_text("5^{\\log_{5} 18} = 18", "例題 1(c) の非循環な検算")
eq(5 ** sp.log(18, 5), 18, "5^(log_5 18) = 18")
in_text("**@eq-aasl17b-pow を使わない別の道すじです。**", "何を使っていないかを正しく")
not_in_text("**法則を使わない別の道すじです。**", "言い方を正した")
in_text("$\\log 28 - \\log 4 = \\log \\dfrac{28}{4} = \\log 7$", "演習 1 の非循環な検算")
eq(lg(28, 10) - lg(4, 10), lg(7, 10), "log28 - log4 = log7")
eq(R(28, 4), 7, "28/4 = 7")
eq(lg(11, 10) - lg(4, 10), lg(sp.Rational(11, 4), 10), "誤答なら log(11/4)")
ne(lg(sp.Rational(11, 4), 10), lg(7, 10), "log 7 には戻らない")
in_text("a^{p + 2q} = a^{p} \\times \\left(a^{q}\\right)^{2} = 2 \\times 3^{2} = 18",
        "演習 4 の非循環な検算")
eq(2 * 3 ** 2, 18, "2 × 3^2 = 18")
eq(2 ** 2 * 3, 12, "誤答 2p+q なら 12")
ne(12, 18, "その誤答は合わない")
in_text("**中身を掛ける道すじとは別です。**", "演習 3 の検算")
eq(2 - lg(2, 10) + lg(2, 10), 2, "log50 = 2 - log2 を使う道すじ")
# 手で出せない主張を、大小の議論に
in_text("$8^{\\frac{3}{5}} < 8^{1} = 8$ なので、$32$ には届きません。", "演習 5 の誤答の見分け方")
chk(R(8) ** R(3, 5) < 8, "8^(3/5) < 8")
chk(8 < 32, "だから 32 には届かない")
# 例題 4(b) の一歩
in_text("$2^{\\square} = 10$ は、対数の定義（[SL 1.5](aasl-1-5.qmd#log-def)）から"
        " $\\square = \\log_{2} 10$ ということです。", "定義に戻る一歩")
in_text("in the form $a + \\log_{2} b$, where $a$ and $b$ are integers", "答えの形を指定")
# @-ref を表示数式の中に置かない
not_in_text("\\qquad (\\text{@eq-aasl17b-pow})", "数式の中の @-ref を外に出した")
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
# 演習 6(c)（シラバスの型）
in_text("**(c)** [$\\left(\\dfrac{1}{3}\\right)^{x} = 9^{x+1}$]{.q-en}", "シラバスの型を出題")
chk(sols(sp.Eq(R(1, 3) ** x, 9 ** (x + 1))) == [R(-2, 3)], "解は -2/3")
eq(R(1, 3) ** R(-2, 3), R(3) ** R(2, 3), "左辺は 3^(2/3)")
eq(R(9) ** R(1, 3), R(3) ** R(2, 3), "右辺も 3^(2/3)")
eq(2 * (x + 1), 2 * x + 2, "2(x+1) = 2x+2")
chk(sp.solve(sp.Eq(-x, 2 * x + 1), x) == [R(-1, 3)], "2x+1 とした誤答は -1/3")
eq(R(1, 3) ** R(-1, 3), R(3) ** R(1, 3), "その誤答の左辺")
eq(R(9) ** R(2, 3), R(3) ** R(4, 3), "その誤答の右辺")
ne(R(3) ** R(1, 3), R(3) ** R(4, 3), "合わない")
# Common errors の追加
in_text("$\\dfrac{\\ln 7}{\\ln 3}$ を $\\ln \\dfrac{7}{3}$ にするのも、同じ誤りです。",
        "ln の分数を log の中に入れない")
in_text("**ただし $x = a$ のときは両方とも $1$ になる**", "向きの確かめ方の但し書き")
# 英語
in_text("[Find the value of $\\log_{10} 50 + \\log_{10} 2$.]{.q-en}", "演習 3 の英語")
in_text("**(c)** [$\\log_{10} 4 + \\log_{10} 25$]{.q-en}", "例題 2(c) の英語")
not_in_text("where the base is $10$", "底は式の中に書く")
in_text("The student subtracted the arguments instead of dividing them", "演習 10 の英語")
in_text("which is exactly what the first law of logarithms states", "records → states")


# まだ存在しないページへのリンクを置かない
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(not _href.startswith("../") or _href.endswith(".qmd"),
        "まだないページへのリンク: " + _href)
not_in_text("(../02-functions/)", "Topic 2 はまだ書いていない")


# ── 採点の言い方（★2026-09-07 の修正）────────────────────
in_text("方法点（M mark）を得るためにも、途中式を書いておくのが安全です。", "断定を弱めた")
not_in_text("方法点（M mark）がもらえないことがあります", "古い言い方は残っていない")
# Topic 2 へのリンクは、ページができるまで張らない
not_in_text("(../02-functions/)", "まだないページへのリンクは張らない")
in_text("**Topic 2（Functions）** の指数関数で使います", "文章で書く")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
