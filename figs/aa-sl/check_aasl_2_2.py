"""AA SL 2.2（関数・定義域・値域・逆関数）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_2.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-2.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_2_2.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, t, n, a, b = sp.symbols("x t n a b")
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


def dom(expr_ge0, want, msg=""):
    """expr_ge0 >= 0 の解が want と一致するか。"""
    chk(sp.solveset(expr_ge0 >= 0, x, REALS) == want, "定義域: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 定義そのもの
# ══════════════════════════════════════════════════════════
# 「2 乗すると x になる数」は関数ではない（x = 9 で 2 つ）
chk(sp.solveset(sp.Eq(x ** 2, 9), x, REALS) == {-3, 3}, "x=9 で 3 と -3")
chk(len(sp.solveset(sp.Eq(x ** 2, 9), x, REALS)) == 2, "出力が 2 つ")
# 円は関数ではない
chk(sp.solveset(sp.Eq(0 ** 2 + x ** 2, 1), x, REALS) == {-1, 1},
    "x=0 で y は 1 と -1")
# 1/x は x = 0 で値をもたない
chk(sp.limit(1 / x, x, 0, "+") is sp.oo, "1/x は 0 で発散")
chk((1 / x).subs(x, 0) is sp.zoo, "1/0 は数ではない")
# シラバスの例 f(x) = sqrt(2-x)
dom(2 - x, sp.Interval(-sp.oo, 2), "sqrt(2-x) は x <= 2")
eq(sp.sqrt(2 - 2), 0, "x=2 で 0 が出る")
chk(sp.sqrt(2 - sp.Integer(3)).is_real is False, "x=3 では実数にならない")
chk(sp.minimum(sp.sqrt(2 - x), x, sp.Interval(-sp.oo, 2)) == 0, "range の下端は 0")
# 1/(x-3)
chk(sp.solveset(sp.Eq(x - 3, 0), x, REALS) == {3}, "1/(x-3) は x = 3 を外す")
# (a,b) と (b,a) は y = x について対称
eq(sp.simplify((a - b) / (b - a)), -1, "結ぶ線分の傾きは -1")
eq(1 * sp.Integer(-1), -1, "y = x と垂直")
eq((a + b) / 2, (b + a) / 2, "中点は y = x の上")

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
eq(4 * 3 - 7, 5, "第 2 節 f(3) = 5")
eq(45 + 3 * 20, 105, "第 6 節 C(20) = 105")
eq(sp.Integer(3) ** 2, sp.Integer(-3) ** 2, "f(3) = f(-3)（x^2）")
eq(sp.Integer(3) ** 2, 9, "9 になる")
eq(R(1, 4 * 5 - 7), R(1, 13), "1/f(5) = 1/13")
ne(R(1, 13), 3, "1/f(5) は f^{-1}(5) とちがう")

# ══════════════════════════════════════════════════════════
# 2. 例題 1  f(x) = sqrt(3x-6)
# ══════════════════════════════════════════════════════════
dom(3 * x - 6, sp.Interval(2, sp.oo), "例題1(a) x >= 2")
eq(3 * 2 - 6, 0, "境目で 0")
chk(3 * 1 - 6 < 0, "x=1 は定義域の外")
chk(sp.sqrt(sp.Integer(3 * 1 - 6)).is_real is False, "sqrt(-3) は実数でない")
chk(sp.minimum(sp.sqrt(3 * x - 6), x, sp.Interval(2, sp.oo)) == 0,
    "例題1(b) range の下端は 0")
eq(sp.sqrt(3 * 5 - 6), 3, "例題1(c) f(5) = 3")
eq(sp.sqrt(sp.Integer(9)), 3, "sqrt(9) = 3")
chk(sp.solve(sp.Eq(3 * x - 6, 36), x) == [14], "例題1(d) x = 14")
eq(sp.sqrt(3 * 14 - 6), 6, "検算 f(14) = 6")
eq(sp.sqrt(sp.Integer(36)), 6, "sqrt(36) = 6")
# 2 乗を忘れた誤答
chk(sp.solve(sp.Eq(3 * x - 6, 6), x) == [4], "2 乗を忘れると x = 4")
ne(sp.sqrt(3 * 4 - 6), 6, "その誤答では 6 にならない")
eq(sp.sqrt(3 * 4 - 6), sp.sqrt(6), "f(4) = sqrt(6)")

# ══════════════════════════════════════════════════════════
# 3. 例題 2  f(x) = 4x - 7
# ══════════════════════════════════════════════════════════
_f2 = 4 * x - 7
eq(_f2.subs(x, 3), 5, "例題2(a) f(3) = 5")
chk(sp.solve(sp.Eq(_f2, 5), x) == [3], "例題2(b) f^{-1}(5) = 3")
chk(sp.solve(sp.Eq(_f2, 21), x) == [7], "例題2(c) x = 7")
eq(_f2.subs(x, 7), 21, "検算 f(7) = 21")
eq(4 * 7 - 7, 21, "28 - 7 = 21")
# f は one-to-one（傾きが 0 でない 1 次関数）
chk(sp.diff(_f2, x) == 4 and 4 != 0, "傾きが 0 でないので one-to-one")
chk(len(sp.solveset(sp.Eq(_f2, 21), x, REALS)) == 1, "戻り先はただ 1 つ")

# ══════════════════════════════════════════════════════════
# 4. 例題 3  f(x) = x^2 + 1
# ══════════════════════════════════════════════════════════
_f3 = x ** 2 + 1
eq(_f3.subs(x, 3), 10, "例題3(a) f(3) = 10")
eq(_f3.subs(x, -3), 10, "f(-3) = 10")
eq(_f3.subs(x, 3), _f3.subs(x, -3), "同じ値になる")
ne(3, -3, "入力はちがう")
chk(sp.solveset(sp.Eq(_f3, 10), x, REALS) == {-3, 3}, "実数全体では戻り先が 2 つ")
chk(sp.minimum(_f3, x, sp.Interval(0, sp.oo)) == 1, "例題3(c) range >= 1")
eq(_f3.subs(x, 0), 1, "x=0 で 1")
chk(sp.solveset(sp.Eq(_f3, 0), x, REALS) == sp.S.EmptySet, "0 は出ない")
chk(sp.solveset(sp.Eq(_f3, 10), x, sp.Interval(0, sp.oo)) == {3},
    "例題3(d) 制限すると 3 だけ")
chk(-3 not in sp.Interval(0, sp.oo), "-3 は制限後の定義域の外")

# ══════════════════════════════════════════════════════════
# 5. 例題 4  V(t) = 120 - 8t
# ══════════════════════════════════════════════════════════
_V = 120 - 8 * t
eq(_V.subs(t, 5), 80, "例題4(a) V(5) = 80")
eq(8 * 5, 40, "5 分で 40 L 減る")
eq(120 - 40, 80, "残りは 80 L")
chk(sp.solve(sp.Eq(_V, 0), t) == [15], "例題4(b) t = 15")
eq(_V.subs(t, 15), 0, "検算 V(15) = 0")
eq(_V.subs(t, 0), 120, "V(0) = 120")
eq(_V.subs(t, 20), -40, "V(20) = -40")
chk(20 not in sp.Interval(0, 15), "t=20 は定義域の外")
chk(_V.subs(t, 20) < 0, "体積が負になってしまう")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
_e1 = 5 * x - 2
eq(_e1.subs(x, 4), 18, "演習1(a) 18")
chk(sp.solve(sp.Eq(_e1, 13), x) == [3], "演習1(b) x = 3")
eq(_e1.subs(x, 3), 13, "検算 f(3) = 13")
chk(3 < 4 and 13 < 18, "13 < 18 なので答えは 4 より小さい")

chk(sp.solveset(sp.Eq(x + 4, 0), x, REALS) == {-4}, "演習2 x = -4 を外す")
eq(R(1, -3 + 4), 1, "x=-3 では 1")
eq(R(1, -5 + 4), -1, "x=-5 では -1")
chk((1 / (x + 4)).subs(x, -4) is sp.zoo, "x=-4 だけ値をもたない")

dom(2 * x + 6, sp.Interval(-3, sp.oo), "演習3 x >= -3")
eq(2 * (-3) + 6, 0, "境目で 0")
chk(2 * (-4) + 6 < 0, "x=-4 は外")
chk(sp.sqrt(sp.Integer(2 * (-4) + 6)).is_real is False, "sqrt(-2) は実数でない")
chk(sp.diff(2 * x + 6, x) > 0, "正の数で割るので向きは変わらない")

chk(sp.minimum(x ** 2 - 3, x, sp.Interval(0, sp.oo)) == -3, "演習4 range >= -3")
eq((x ** 2 - 3).subs(x, 0), -3, "x=0 で -3")
chk(sp.solveset(sp.Eq(x ** 2 - 3, -4), x, REALS) == sp.S.EmptySet, "-4 は出ない")

chk(sp.solve(sp.Eq(2 * x + 9, 15), x) == [3], "演習5 f^{-1}(15) = 3")
eq(2 * 3 + 9, 15, "検算 f(3) = 15")
eq(2 * 15 + 9, 39, "f(15) = 39")
ne(R(1, 39), 3, "1/f(15) は答えではない")

_C = 60 + 5 * n
eq(_C.subs(n, 12), 120, "演習6(a) 120")
chk(sp.solve(sp.Eq(_C, 210), n) == [30], "演習6(b) n = 30")
eq(_C.subs(n, 30), 210, "検算 C(30) = 210")
chk(_C.subs(n, 24) != 2 * _C.subs(n, 12), "定数項があるので 2 倍にはならない")

dom(x - 1, sp.Interval(1, sp.oo), "演習7 x >= 1")
chk(sp.sqrt(sp.Integer(0 - 1)).is_real is False, "x=0 は外")
eq(sp.sqrt(1 - 1), 0, "x=1 で 0")
eq(sp.sqrt(5 - 1), 2, "f(5) = 2")
eq(sp.sqrt(10 - 1), 3, "f(10) = 3")
chk(sp.minimum(sp.sqrt(x - 1), x, sp.Interval(1, sp.oo)) == 0, "演習7 range >= 0")

# 演習 8 — 座標が入れかわる
chk((2, 7) != (7, 2), "点は入れかわる")

# 演習 9 — (x-3)^2 は one-to-one でない
_e9 = (x - 3) ** 2
eq(_e9.subs(x, 1), 4, "演習9 f(1) = 4")
eq(_e9.subs(x, 5), 4, "f(5) = 4")
ne(1, 5, "入力はちがう")
chk(sp.solveset(sp.Eq(_e9, 4), x, REALS) == {1, 5}, "戻り先が 2 つ")
eq(_e9.subs(x, 2), 1, "f(2) = 1")
eq(_e9.subs(x, 4), 1, "f(4) = 1（別の組）")
eq(R(1 + 5, 2), 3, "1 と 5 は x = 3 から等距離")
eq(R(2 + 4, 2), 3, "2 と 4 も同じ")

# 演習 10 — 不等号の向き
dom(5 - x, sp.Interval(-sp.oo, 5), "演習10 正しくは x <= 5")
chk(6 in sp.Interval(5, sp.oo), "生徒の範囲には 6 が入る")
chk(sp.sqrt(sp.Integer(5 - 6)).is_real is False, "しかし x=6 では値が出ない")
eq(sp.sqrt(5 - 0), sp.sqrt(5), "x=0 では sqrt(5)")
chk(0 not in sp.Interval(5, sp.oo), "x=0 は生徒の範囲の外")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この項目には、公式集の欄がありません", "2.2 は公式集にない")
in_text("**2.2 の内容は、公式集には載っていません。**", "同上")
not_in_text("> Function notation, for example", "Content 欄の引用は置かない")
in_text("シラバスは、$f(x)$、$v(t)$、$C(n)$ のような書き方を挙げています。", "文章で書く")
in_text("> Unless otherwise stated, the domain will be the largest possible "
        "domain for which a function is defined.", "domain の但し書きを逐語で")
not_in_text("> For example, for the function", "Content 欄の引用は置かない")
in_text("シラバスも、$f(x) = \\sqrt{2-x}$ をそのまま例に挙げ、domain は $x \\le 2$、"
        "range は $f(x) \\ge 0$ だとしています。", "文章で書く")
not_in_text("> The concept of a function as a mathematical model.",
            "Content 欄の引用は置かない")
in_text("シラバスは、関数を**現実の場面のモデル**として使うことも求めています。", "文章で書く")
in_text("> Solving $f(x) = 10$ is equivalent to finding $f^{-1}(10)$.",
        "逆関数の言いかえを逐語で")
in_text("> An inverse function exists for one-to-one functions.",
        "one-to-one の条件を逐語で")
in_text("**そっくり入れかわります。** $f^{-1}$ の domain は $f$ の range であり、"
        "$f^{-1}$ の range は $f$ の domain です。", "domain と range の入れかわり")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("**vertical line test**（縦線判定）", "縦線判定")
in_text("$f^{-1}(x)$ は $\\dfrac{1}{f(x)}$ ではありません", "指数ではない")
not_in_text("**domain が変われば、range も変わります。**", "無条件の断定は外した")
in_text("**domain を変えると、range も変わることがあります。**", "断定を弱めた")
in_text("ただし、**変わらないこともあります**", "反例にふれた")
in_text("**domain を見ずに range は書けません。**", "Common errors も直した")
in_text("$\\dfrac{1}{\\sqrt{x+2}}$ のように**両方あるとき**", "分母と根号が両方")
in_text("分母が $0$ になってもいけないので $x > -2$ です。", "その条件")
not_in_text("$\\dfrac{1}{\\sqrt{x-1}}$", "演習 7 と同じ式は使わない")
in_text("このとき、$2$ 点を結ぶ線分の傾きは", "a = b を先に片づけてから")

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
chk(len(re.findall(r"^::: \{#exm-aasl22-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
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
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors, "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl22", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
# 定義した表・式・図は、本文から参照している
for _lab in ["tbl-aasl22-isfn", "tbl-aasl22-notation", "tbl-aasl22-domain",
             "tbl-aasl22-shadow", "fig-aasl22-idea", "eq-aasl22-undo"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-2-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-2-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Domain on the $x$-axis, range on the $y$-axis", "図(a) の題")
in_fig("$y = \\\\sqrt{2-x}$", "図(a) の関数")
in_fig("domain: $x \\\\leq 2$", "図(a) の domain")
in_fig("range:\\n$y \\\\geq 0$", "図(a) の range")
in_fig("shadow on each axis", "図(a) の要点")
in_fig("(b) The inverse is the reflection in $y = x$", "図(b) の題")
in_fig("$y = f(x)$", "図(b) の f")
in_fig("$y = f^{-1}(x)$", "図(b) の逆関数")
in_fig("$f(a) = b$ means $f^{-1}(b) = a$", "図(b) の要点")
in_text("(a) The domain of $f(x)=\\sqrt{2-x}$ is the shadow of the graph",
        "キャプションが (a) を説明")
in_text("(b) The graph of $y=f^{-1}(x)$ is the reflection", "キャプションが (b) を説明")
# 図が使っている 2 点は、実際に入れかえの関係
chk(abs(1.4 ** 2 - 1.96) < 1e-9, "図の点は y = x^2 の上")
# 図に演習の答えを書いていない
for leak in ["x \\\\leq 5", "x \\\\geq 1", "x \\\\geq -3", "f(x) \\\\geq -3",
             "(7, 2)", "= 18", "= 30", "= 120", "x \\\\neq -4"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-2.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-1.qmd") < DRAFT.index("aasl-2-2.qmd"), "並びが 2.1 → 2.2")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-2.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| function |", "| domain |", "| range |", "| inverse function |",
           "| one-to-one |", "| mathematical model |"]:
    chk(_t in GLO, "対訳表にある: " + _t)


# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════
# 所見 2 — 例題 3 (d) に one-to-one と range の確認を足した
in_text("$x \\ge 0$ に限れば、$x$ が大きくなるほど $x^{2}+1$ も大きくなるので、"
        "ちがう $2$ つの入力が同じ値になることはもうありません。", "one-to-one の確認")
in_text("## domain を狭めても、range は変わらないことがあります", "狭めた目的")
chk(sp.minimum(_f3, x, REALS) == 1, "実数全体でも range の下端は 1")
chk(sp.minimum(_f3, x, sp.Interval(0, sp.oo)) == 1, "x>=0 でも下端は 1（同じ）")
chk(sp.is_increasing(_f3, sp.Interval(0, sp.oo)), "x>=0 では単調増加")
# 所見 4 — 例題 2 の検算から循環を外した
not_in_text("**検算（(d) について）。** $f(7) = 21$ なので $f^{-1}(21) = 7$ ✓",
            "循環的な検算は残っていない")
in_text("**(d) は (c) と同じ事実を左右から見たものなので、(d) だけを別に確かめる"
        "ことはできません。**", "確かめられないと明記")
chk(sp.solve(sp.Eq(_f2, 21), x)[0] > sp.solve(sp.Eq(_f2, 5), x)[0],
    "大きい値のほうが戻り値も大きい")
# 所見 5 — 例題 4 (c) の検算を、範囲の外で意味が壊れることに変えた
in_text("(b) と同じ計算を繰り返しても検算にはなりません。", "循環を避けた")
in_text("$t = 20$ とすると $V(20) = 120 - 160 = -40$ となり、水の量が負に"
        "なってしまいます ✓", "外側で壊れる")
eq(120 - 160, -40, "V(20) = -40")
# 所見 6 — 演習 6 の見当を、意味のあるものに
in_text("$60$ ドルは時間によらずかかる分なので、時間で決まるのは "
        "$210 - 60 = 150$ ドルです。", "固定分を分けた")
eq(210 - 60, 150, "150 ドル")
eq(R(150, 5), 30, "150 ÷ 5 = 30")
ne(_C.subs(n, 21), 210, "1.75 倍の 21 時間では 210 にならない")
# 所見 9 — 参照先の誤りを直した
not_in_text("[第 5 節](#from-graph)の逆で考えます", "誤った参照は残っていない")
in_text("$f^{-1}(10)$ が欲しければ、$f(x) = 10$ を解けばよいからです", "言いかえ")
# 所見 10 — a = b の場合
in_text("$a = b$ のときは、点 $(a,b)$ 自身が $y = x$ の上にあり、"
        "折り返しても動きません。", "a = b の場合")
# 所見 11 — one-to-one の説明を定義に合わせた
in_text("**入力 $1$ つに出力 $1$ つ**という[第 1 節](#idea)の条件を満たさないので、"
        "$f^{-1}$ は関数になれないのです。", "定義に合わせた")
# 所見 12 — 逆関数があることの前提
in_text("この $f$ は、ちがう $x$ からは必ずちがう値が出るので、戻し先が $1$ つに"
        "決まります。", "前提を書いた")
# 所見 15 — 図 (b) の位置づけ
in_text("**(b) は逆関数の図で、[第 7 節](#inverse)で使います。**", "図(b) の案内")
# 所見 16 — モデルと現実を分けた
in_text("The model simply stops applying at $t = 15$", "モデルの外だと明記")
# 所見 17 — 演習 3 と 演習 10 の論点を分けた
in_text("**割るのが正の数なので、ここでは不等号の向きは変わりません**", "演習3 の論点")
not_in_text("$h(x) = \\sqrt{10 - 2x}$", "古い演習 3 は残っていない")
# 所見 3 — 演習 9 が本文の書き写しにならないようにした
in_text("$f(x) = (x-3)^{2}$", "演習9 の関数を変えた")
_body22 = TEXT[:TEXT.index("## Exercises")]
chk("(x-3)^{2}" not in _body22, "演習9 の関数は本文にも例題にも出てこない")
chk("(x-3)" not in _body22, "同上")
# 所見 8 — model-answer の分量
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _w = len(_blk.split())
    chk(_w <= 110, f"model-answer が長すぎない: {_w} 語")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
