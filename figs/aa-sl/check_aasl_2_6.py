"""AA SL 2.6（2 次関数の 3 つの形）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_6.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-6.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_6.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x")
a, b, c, p, q, h, k = sp.symbols("a b c p q h k")
REALS = sp.S.Reals


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


def roots(expr, want, msg=""):
    chk(sp.solveset(sp.Eq(expr, 0), x, REALS) == want, "零点: " + msg)


def axis(expr, want, msg=""):
    """公式集の軸の式で確かめる。"""
    _p = sp.Poly(sp.expand(expr), x).all_coeffs()
    _a, _b = _p[0], _p[1]
    eq(-_b / (2 * _a), want, "軸: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの
# ══════════════════════════════════════════════════════════
# 平方完成で vertex form になる（a ≠ 0）
_a = sp.Symbol("a", nonzero=True)
eq(_a * (x + b / (2 * _a)) ** 2 - b ** 2 / (4 * _a) + c,
   _a * x ** 2 + b * x + c, "平方完成 → standard form")
eq(x ** 2 + (b / _a) * x, (x + b / (2 * _a)) ** 2 - b ** 2 / (4 * _a ** 2),
   "かっこの中の平方完成")
# factorised form を展開すると b = -a(p+q)
eq(sp.expand(_a * (x - p) * (x - q)),
   _a * x ** 2 - _a * (p + q) * x + _a * p * q, "展開")
eq(-(-_a * (p + q)) / (2 * _a), (p + q) / 2, "2 つの軸の言い方が一致する")
# vertex form から頂点
eq((a * (x - h) ** 2 + k).subs(x, h), k, "x = h で値は k")
# a が同じでも x 切片は同じ
for _aa in (1, 3, -R(1, 2)):
    chk(sp.solveset(sp.Eq(_aa * (x - 2) * (x - 6), 0), x, REALS) == {2, 6},
        f"a = {_aa} でも x 切片は同じ")
ne((1) * (0 - 2) * (0 - 6), (3) * (0 - 2) * (0 - 6), "しかし y 切片はちがう")

# ══════════════════════════════════════════════════════════
# 1. The idea の例
# ══════════════════════════════════════════════════════════
eq(sp.expand((x + 5) ** 2 - 22), x ** 2 + 10 * x + 3, "第 5 節の平方完成")
eq(sp.expand(3 * (x + 2) ** 2 - 7), 3 * x ** 2 + 12 * x + 5, "a ≠ 1 の平方完成")
eq(3 * (-4) + 5, -7, "-12 + 5 = -7")
eq(((x + 6) ** 2 - 1).subs(x, -6), -1, "第 4 節の例の頂点")
axis(x ** 2 + 10 * x + 3, -5, "第 5 節の例の軸")

# ══════════════════════════════════════════════════════════
# 2. 例題 1  f(x) = x^2 + 8x + 11
# ══════════════════════════════════════════════════════════
_f1 = x ** 2 + 8 * x + 11
eq(_f1.subs(x, 0), 11, "例題1(a) y 切片 11")
axis(_f1, -4, "例題1(b)")
eq(sp.expand((x + 4) ** 2 - 5), _f1, "例題1(c) 平方完成")
eq(_f1.subs(x, -4), -5, "頂点の y は -5")
chk(sp.minimum(_f1, x, REALS) == -5, "例題1(d) 最小は -5")
eq(_f1.subs(x, -3), -4, "検算 f(-3) = -4")
eq(_f1.subs(x, -5), -4, "検算 f(-5) = -4（左右対称）")
chk(_f1.subs(x, -3) > -5, "頂点より大きい")
eq(_f1.subs(x, 4), 59, "符号を落とした誤答の位置では 59")
chk(59 > -5, "頂点ではない")

# ══════════════════════════════════════════════════════════
# 3. 例題 2  f(x) = 2x^2 + 4x - 6
# ══════════════════════════════════════════════════════════
_f2 = 2 * x ** 2 + 4 * x - 6
eq(sp.expand(2 * (x + 3) * (x - 1)), _f2, "例題2(a) 因数分解")
roots(_f2, {-3, 1}, "例題2(b)")
eq(R(-3 + 1, 2), -1, "例題2(c) まん中")
axis(_f2, -1, "例題2(c) 公式でも")
eq(_f2.subs(x, -1), -8, "例題2(d) 頂点の y")
eq(2 * (-1 + 3) * (-1 - 1), -8, "因数分解した形でも -8")
chk(sp.minimum(_f2, x, REALS) == -8, "実際に最小")
eq(_f2.subs(x, 0), -6, "y 切片は -6")
eq(((x + 3) * (x - 1)).subs(x, 0), -3, "a を忘れると y 切片が -3")
ne(-3, -6, "合わない")
eq(((x + 3) * (x - 1)).subs(x, -1), -4, "a を忘れると頂点も -4")

# ══════════════════════════════════════════════════════════
# 4. 例題 3  頂点 (1,4)、(3,16) を通る
# ══════════════════════════════════════════════════════════
_f3 = 3 * (x - 1) ** 2 + 4
eq(_f3.subs(x, 3), 16, "例題3(a) (3,16) を通る")
eq(_f3.subs(x, 1), 4, "頂点を通る")
chk(sp.solve(sp.Eq(a * (3 - 1) ** 2 + 4, 16), a) == [3], "a = 3")
eq(sp.expand(_f3), 3 * x ** 2 - 6 * x + 7, "例題3(b) standard form")
eq(_f3.subs(x, 0), 7, "例題3(c) y 切片 7")
eq((3 * x ** 2 - 6 * x + 7).subs(x, 0), 7, "standard form でも 7")
axis(3 * x ** 2 - 6 * x + 7, 1, "軸は x = 1")
chk(sp.minimum(_f3, x, REALS) == 4, "最小値は 4")
chk(sp.solveset(sp.Eq(_f3, 0), x, REALS) == sp.S.EmptySet, "例題3(d) x 切片なし")
chk(4 > 0, "最小値が正")
eq((3 * x ** 2 - 6 * x + 7).subs(x, 3), 16, "standard form でも (3,16)")

# ══════════════════════════════════════════════════════════
# 5. 例題 4  f(x) = -x^2 - 4x + 5
# ══════════════════════════════════════════════════════════
_f4 = -x ** 2 - 4 * x + 5
eq(sp.expand(-(x + 5) * (x - 1)), _f4, "例題4(a) 因数分解")
roots(_f4, {-5, 1}, "例題4(b)")
eq(R(-5 + 1, 2), -2, "例題4(c) まん中")
axis(_f4, -2, "例題4(c) 公式でも")
eq(_f4.subs(x, -2), 9, "頂点の y は 9")
chk(sp.maximum(_f4, x, REALS) == 9, "実際に最大")
eq(_f4.subs(x, -1), 8, "検算 f(-1) = 8")
eq(_f4.subs(x, -3), 8, "検算 f(-3) = 8")
chk(8 < 9, "頂点より小さい")
eq(_f4.subs(x, 10), -135, "例題4(d) f(10) = -135")
chk(sp.limit(_f4, x, sp.oo) is -sp.oo, "いくらでも小さくなる")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
_e1 = x ** 2 - 4 * x - 5
eq(_e1.subs(x, 0), -5, "演習1(a)")
axis(_e1, 2, "演習1(b)")
eq(_e1.subs(x, 1), -8, "検算 f(1) = -8")
eq(_e1.subs(x, 3), -8, "検算 f(3) = -8")
eq(_e1.subs(x, -1), 0, "符号を落とした位置では 0")
eq(_e1.subs(x, -3), 16, "その反対側は 16")
ne(0, 16, "左右が合わない")

eq(sp.expand((x + 3) ** 2 - 7), x ** 2 + 6 * x + 2, "演習2")
eq((x ** 2 + 6 * x + 2).subs(x, -3), -7, "頂点でも -7")
chk(sp.minimum(x ** 2 + 6 * x + 2, x, REALS) == -7, "最小は -7")

eq(sp.expand((x - 5) * (x + 3)), x ** 2 - 2 * x - 15, "演習3(a)")
roots(x ** 2 - 2 * x - 15, {5, -3}, "演習3(b)")
eq((-5) * 3, -15, "かけて -15")
eq(-5 + 3, -2, "足して -2")
eq(((x - 5) * (x + 3)).subs(x, 0), -15, "y 切片も一致")

_e4 = 2 * (x - 3) ** 2 - 8
eq(_e4.subs(x, 3), -8, "演習4(a) 頂点")
eq(sp.expand(_e4), 2 * x ** 2 - 12 * x + 10, "演習4(b)")
axis(2 * x ** 2 - 12 * x + 10, 3, "軸は x = 3")
eq(_e4.subs(x, 0), 10, "y 切片 10")
eq(2 * 9 - 8, 10, "2(9) - 8 = 10")

_e5 = 2 * (x + 1) * (x - 5)
roots(_e5, {-1, 5}, "演習5 x 切片")
eq(_e5.subs(x, 0), -10, "演習5 (0,-10) を通る")
chk(sp.solve(sp.Eq(a * (0 + 1) * (0 - 5), -10), a) == [2], "a = 2")
eq(((x + 1) * (x - 5)).subs(x, 0), -5, "a を忘れると -5")
ne(-5, -10, "合わない")

_e6 = 2 * (x + 2) ** 2 + 1
eq(_e6.subs(x, -2), 1, "演習6 頂点")
eq(_e6.subs(x, 0), 9, "演習6 (0,9) を通る")
chk(sp.solve(sp.Eq(a * (0 + 2) ** 2 + 1, 9), a) == [2], "a = 2")
eq((2 * (x - 2) ** 2 + 1).subs(x, 0), 9, "h の符号を誤ってもここは合う")
eq((2 * (x - 2) ** 2 + 1).subs(x, 2), 1, "しかし頂点が (2,1) になる")
ne(2, -2, "頂点がちがう")

_e7 = -2 * x ** 2 + 8 * x - 3
axis(_e7, 2, "演習7(a)")
eq(_e7.subs(x, 2), 5, "演習7(b) 最大値 5")
chk(sp.maximum(_e7, x, REALS) == 5, "実際に最大")
eq(_e7.subs(x, 1), 3, "検算 f(1) = 3")
eq(_e7.subs(x, 3), 3, "検算 f(3) = 3")
chk(3 < 5, "頂点より小さい")

chk(sp.solveset(sp.Eq(3 * x ** 2 + 5, 0), x, REALS) == sp.S.EmptySet, "演習8")
chk(sp.minimum(3 * x ** 2 + 5, x, REALS) == 5, "最小は 5")
eq((3 * x ** 2 + 5).subs(x, 0), 5, "x=0 で 5")
chk(sp.solveset(sp.Eq(3 * x ** 2 + 5, 4), x, REALS) == sp.S.EmptySet, "4 も出ない")

_e9 = (x - 7) ** 2 + 2
eq(_e9.subs(x, 7), 2, "演習9(a) 頂点")
eq(_e9.subs(x, 6), 3, "検算 f(6) = 3")
eq(_e9.subs(x, 8), 3, "検算 f(8) = 3")
chk(3 > 2, "頂点より大きい → 最小点")
eq(_e9.subs(x, -7), 198, "(-7,2) は誤り")
ne(198, 2, "合わない")

_e10 = (x + 3) ** 2 - 4
eq(_e10.subs(x, -3), -4, "演習10 正しい頂点")
eq(_e10.subs(x, 3), 32, "x=3 では 32")
ne(32, -4, "生徒の答えは合わない")
eq(_e10.subs(x, -4), -3, "検算 f(-4) = -3")
eq(_e10.subs(x, -2), -3, "検算 f(-2) = -3")
chk(sp.minimum(_e10, x, REALS) == -4, "最小は -4")

# ══════════════════════════════════════════════════════════
# 7. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("x^{2}+8x+11", "例題1"), ("(x+4)^{2}", "例題1"),
                ("2x^{2} + 4x - 6", "例題2"), ("(x+3)(x-1)", "例題2"),
                ("3(x-1)^{2}", "例題3"), ("(x+5)(x-1)", "例題4"),
                ("x^{2} - 4x - 5", "演習1"), ("x^{2} + 6x + 2", "演習2"),
                ("(x-5)(x+3)", "演習3"), ("2(x-3)^{2}", "演習4"),
                ("(x+1)(x-5)", "演習5"), ("(x+2)^{2} + 1", "演習6"),
                ("-2x^{2}", "演習7"), ("3x^{2} + 5", "演習8"),
                ("(x-7)^{2}", "演習9"), ("(x+3)^{2} - 4", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 8. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この式は公式集にあります", "軸の式は公式集にある")
in_text("公式集の **2.6** の欄に `Axis of symmetry of the graph of a quadratic "
        "function` として印刷されています。", "欄の名前")
in_text("> $f(x) = ax^{2} + bx + c \\Rightarrow$ axis of symmetry is "
        "$x = -\\dfrac{b}{2a}$", "公式集を逐語で")
chk(TEXT.count("\n> ") == 1, f"引用は 1 つだけ: {TEXT.count(chr(10) + '> ')}")
in_text("**覚える必要はありません。**", "公式集にあるものは覚えると書かない")
chk(TEXT.index("$$ {#eq-aasl26-axis}") < TEXT.index("## この式は公式集にあります"),
    "公式集の callout は式の直後")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 9. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## $a \\neq 0$ です", "a ≠ 0 の条件")
in_text("**この計算は $a \\neq 0$ でなければできません。**", "Why it works でも")
in_text("## $x$ 切片だけでは、式は決まりません", "a が決まらない")
in_text("## $h$ の符号に気をつけてください", "h の符号")
in_text("**vertex form $a(x-h)^{2}+k$ で見れば、$a$ は開き方だけを決め、", "a の役割")
in_text("定義域が閉区間に制限されていれば、$f$ は端点のどちらかで最小値をとる",
        "定義域にふれた")

# ══════════════════════════════════════════════════════════
# 10. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")

# ══════════════════════════════════════════════════════════
# 11. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aasl26-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h_ for h_ in _h2 if h_ in _want] == _want, "5 つの見出しが所定の順")
chk([h_ for h_ in _h2 if h_ in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
for word in ["得点になりません", "点になりません", "点を落とします",
             "認められません", "減点されます"]:
    not_in_text(word, "採点の断定は避ける")
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
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl26", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
for _lab in ["tbl-aasl26-forms", "tbl-aasl26-convert", "tbl-aasl26-a",
             "tbl-aasl26-build", "fig-aasl26-idea", "eq-aasl26-standard",
             "eq-aasl26-axis", "eq-aasl26-factorised", "eq-aasl26-mid",
             "eq-aasl26-vertex"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 12. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-6-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-6-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Each form shows a different feature", "図(a) の題")
in_fig("$a(x-p)(x-q)$", "図(a) factorised form")
in_fig("$ax^{2}+bx+c$", "図(a) standard form")
in_fig("$a(x-h)^{2}+k$", "図(a) vertex form")
in_fig("axis of\\nsymmetry", "図(a) の軸")
in_fig("(b) The sign and size of $a$", "図(b) の題")
in_fig("large $a > 0$:\\nnarrow", "図(b) 細い")
in_fig("small $a > 0$:\\nwide", "図(b) 広い")
in_fig("$a < 0$:\\nopens downwards", "図(b) 上に凸")
in_fig("$a$ cannot be $0$: the graph would be a straight line", "a ≠ 0")
in_text("(a) The same parabola written in three ways", "キャプションが (a) を説明")
in_text("(b) The sign of $a$ decides which way the parabola opens",
        "キャプションが (b) を説明")
# 図に数値の座標を書いていない
chk(not re.search(r"\(\s*-?\d", FIGSTR), "図に数値の座標を書いていない")
for leak in ["= -8", "= 9", "(0, 11)", "x = -4", "x = 2"]:
    chk(leak not in FIGSTR, "図が答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 13. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-6.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-5.qmd") < DRAFT.index("aasl-2-6.qmd"), "並びが 2.5 → 2.6")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-6.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| quadratic function |", "| completing the square |",
           "| standard form |", "| factorised form |", "| vertex form |"]:
    chk(_t in GLO, "対訳表にある: " + _t)


# ══════════════════════════════════════════════════════════
# 14. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════
# 所見 1 — factorised form に書けない放物線がある
in_text("ただし、**factorised form に書けるのは $x$ 切片をもつ放物線だけ**です",
        "無条件の断定を外した")
not_in_text("同じ $1$ つの放物線を、**$3$ とおりに書けます。**", "古い書き方は残っていない")
in_text("**すべての $2$ 次関数が、この形に書けるわけではありません。**", "第 3 節でも明記")
in_text("$p$ と $q$ が同じ数のときは、$x$ 切片は $1$ つだけで", "p = q の場合")
in_text("（$x$ 切片をもつときだけ）", "表にも条件")
# 同じページに反例がある
chk(sp.solveset(sp.Eq(3 * (x - 1) ** 2 + 4, 0), x, REALS) == sp.S.EmptySet,
    "例題 3 は x 切片をもたない")
chk(sp.solveset(sp.Eq(3 * x ** 2 + 5, 0), x, REALS) == sp.S.EmptySet,
    "演習 8 も x 切片をもたない")
# 所見 2 — 例題 3(a) の検算が a によらず通っていた
in_text("**$a$ を決めたのは「$(3,16)$ を通る」という条件だけなので、それとは別の点で"
        "確かめます。**", "循環を避けた")
eq(_f3.subs(x, -1), 16, "対称な点 x=-1 でも 16")
eq(R(3 + (-1), 2), 1, "3 と -1 のまん中が軸")
# a を誤ると、この検算は通らない
eq((5 * (x - 1) ** 2 + 4).subs(x, -1), 24, "a=5 なら f(-1) = 24")
ne(24, 16, "誤った a では合わない")
# しかし軸の検算は a によらず通ってしまう
for _av in (3, 5, -2):
    _pp = sp.Poly(sp.expand(_av * (x - 1) ** 2 + 4), x).all_coeffs()
    eq(-_pp[1] / (2 * _pp[0]), 1, f"a={_av} でも軸は 1（だから検算にならない）")
in_text("(b) は (a) を展開したものなので、$a$ がどんな値でも軸は $1$ になってしまう",
        "なぜ検算にならないかを書いた")
# 所見 3 — 演習 4 の検算の順序
in_text("**定数項の誤りは、ここでしか見つかりません。**", "y 切片が効く")
eq(sp.expand(2 * (x - 3) ** 2 - 8).subs(x, 0), 10, "y 切片は 10")
# 定数項を誤っても軸は変わらない
_bad4 = 2 * x ** 2 - 12 * x + 1
_pp = sp.Poly(_bad4, x).all_coeffs()
eq(-_pp[1] / (2 * _pp[0]), 3, "定数項を誤っても軸は 3 のまま")
ne(_bad4.subs(x, 0), 10, "しかし y 切片はちがう")
# 所見 4 — 例題 3(b) の検算に使う点
in_text("**$a$ を決めるのに使っていない $x$ を選んで、$2$ つの形に入れます。**", "別の点で")
eq(_f3.subs(x, 2), 7, "vertex form で x=2 は 7")
eq((3 * x ** 2 - 6 * x + 7).subs(x, 2), 7, "standard form でも 7")
# 所見 5 — 図の参照
not_in_text("**どれも同じ $x$ 切片**をもちます（@fig-aasl26-idea の (b)）。",
            "誤った図の参照は残っていない")
in_text("ちがうのは開き方だけです（$a$ が形に効くようすは @fig-aasl26-idea の (b)）",
        "正しい参照")
# 所見 6 — Why it works の平方完成
in_text("なので、$\\dfrac{b^{2}}{4a^{2}}$ が余分です。引いておきます。", "展開を見せた")
in_text("**公式の前のマイナスは、ここから来ています。**", "符号の由来")
eq((x + b / (2 * _a)) ** 2, x ** 2 + (b / _a) * x + b ** 2 / (4 * _a ** 2),
   "展開が正しい")
# 所見 7 — a の役割に条件
in_text("**「$a$ は開き方だけ」と言えるのは、頂点をそろえて比べたときです。**", "条件つき")
_pp2 = sp.Poly(2 * x ** 2 + 8 * x + 11, x).all_coeffs()
eq(-_pp2[1] / (2 * _pp2[0]), -2, "a を変えると軸も動く")
ne(-2, -4, "もとの軸とちがう")
# 所見 8 — 例題 4(d) の模範解答
in_text("The conclusion is right but the reason given is not.", "理由づけの誤りを指摘")
in_text("on a closed interval a function can have both", "閉区間なら両方ある")
not_in_text("The reasoning should mention the domain", "講評の文体は残っていない")
# 所見 9 — 用語の英日併記
in_text("standard form（一般形）", "訳を付けた")
in_text("factorised form（因数分解した形）", "同上")
in_text("vertex form（頂点形）", "同上")
in_text("**completing the square（平方完成）**をする", "英語が先")
# 所見 10 — 「軸上にある点（頂点）」
chk(TEXT.count("**軸上にある点（頂点）**") == 3, "3 か所とも直した")
not_in_text("軸の上の点がいちばん", "紛らわしい言い方は残っていない")
# 所見 13 — 表の行
in_text("| factorised form ↔ vertex form | **いったん standard form を経由する** |",
        "行を足した")
in_text("Paper 1 ではあまり問われません", "3 点の場合の但し書き")
# 所見 14 — CAS
# 2026-09: 生徒は全員 TI-Nspire CX II なので、CAS／非CAS の区別には触れない
in_text("`Factor`（因数分解）や `Complete the Square`（平方完成）はありません",
        "電卓に因数分解・平方完成はない")
not_in_text("CAS")
# 所見 15 — 細い・広いの基準
in_text("$y = x^{2}$ を目安にすると、$\\lvert a \\rvert > 1$ なら細く、"
        "$0 < \\lvert a \\rvert < 1$ なら広くなります。", "基準を書いた")
# 所見 16 — 符号の書き方をそろえた
chk(TEXT.count("-\\dfrac{(-12)}{2(2)}") == 1, "かっこを付けて書いた")
eq(-sp.Rational(-12, 4), 3, "= 3")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
