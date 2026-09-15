"""AA SL 2.5（合成関数と逆関数）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_5.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-5.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_5.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x")
xp = sp.Symbol("xp", nonnegative=True)
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


def comp(outer, inner):
    """(outer ∘ inner)(x) を作る。"""
    return sp.simplify(outer.subs(x, inner))


def inv_ok(f, fi, msg="", dom=None):
    """f(f^{-1}(x)) = x と f^{-1}(f(x)) = x を確かめる。"""
    v = xp if dom == "nonneg" else x
    chk(sp.simplify(f.subs(x, fi).subs(x, v) - v) == 0, "f(f^-1) = x: " + msg)
    chk(sp.simplify(fi.subs(x, f).subs(x, v) - v) == 0, "f^-1(f) = x: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. The idea
# ══════════════════════════════════════════════════════════
# 第 2 節の例（f = x/2, g = x+6）
eq(comp(x / 2, x + 6), (x + 6) / 2, "本文 f∘g = (x+6)/2")
eq(comp(x + 6, x / 2), x / 2 + 6, "本文 g∘f = x/2 + 6")
ne((x + 6) / 2, x / 2 + 6, "2 つは別の式")
eq(((x + 6) / 2).subs(x, 2), 4, "x=2 で 4")
eq((x / 2 + 6).subs(x, 2), 7, "x=2 で 7")
ne(4, 7, "値もちがう")
# 例題 1 の関数（本文には出てこない）
_f, _g = 2 * x + 1, x ** 2
eq(comp(_f, _g), 2 * x ** 2 + 1, "f∘g = 2x^2+1")
eq(comp(_g, _f), 4 * x ** 2 + 4 * x + 1, "g∘f = 4x^2+4x+1")
chk("2x^{2}+1" not in BODY and "2x^{2} + 1" not in BODY,
    "例題 1 の答えは本文に出てこない")
# 第 3 節の例（f = √x, g = 2x-6）
eq(comp(sp.sqrt(x), 2 * x - 6), sp.sqrt(2 * x - 6), "√(2x-6)")
chk(sp.solveset(2 * x - 6 >= 0, x, REALS) == sp.Interval(3, sp.oo),
    "domain は x >= 3")
chk("\\sqrt{x-9}" not in BODY, "演習 7 の答えは本文に出てこない")
# 第 5 節の例
_f5, _fi5 = 3 * x - 4, (x + 4) / 3
inv_ok(_f5, _fi5, "3x-4")
# 第 6 節 / 第 7 節の例
_fr = sp.sqrt(x - 1)
chk(sp.minimum(_fr, x, sp.Interval(1, sp.oo)) == 0, "√(x-1) の range は 0 以上")
# 第 6 節の callout は √(x+2)（例題 3 と重ならない）
chk(sp.minimum(sp.sqrt(x + 2), x, sp.Interval(-2, sp.oo)) == 0, "√(x+2) の range")
eq(sp.simplify((xp ** 2 - 2) + 2 - xp ** 2), 0, "逆の式は x^2 - 2")
eq(sp.simplify(sp.sqrt((xp ** 2 - 2) + 2) - xp), 0, "x >= 0 で往復する")
chk("x^{2}+1" not in BODY, "例題 3 の答えは本文に出てこない")
chk("\\sqrt{x-1}$（domain $x \\ge 1$、range" not in BODY,
    "例題 3 を本文で解いていない")
eq(sp.simplify(sp.sqrt((xp ** 2 + 1) - 1) - xp), 0, "x >= 0 なら √(x^2) = x")
chk(sp.sqrt(sp.Integer(-2) ** 2) == 2, "x = -2 では 2 が返る（戻らない）")
ne(2, -2, "だから制限が要る")
# Why it works の例
eq(2 * 3 + 1, 7, "2 倍してから 1 足すと 7")
eq((3 + 1) * 2, 8, "1 足してから 2 倍すると 8")
ne(7, 8, "順番で変わる")

# ══════════════════════════════════════════════════════════
# 1. 例題 1
# ══════════════════════════════════════════════════════════
eq(_g.subs(x, 3), 9, "例題1(a) g(3) = 9")
eq(_f.subs(x, 9), 19, "f(9) = 19")
eq(comp(_f, _g).subs(x, 3), 19, "合成の式でも 19")
chk(sp.solveset(sp.Eq(comp(_f, _g), comp(_g, _f)), x, REALS) == {0, -2},
    "例題1(d) x = 0, -2")
eq(sp.expand(comp(_g, _f) - comp(_f, _g)), 2 * x ** 2 + 4 * x, "差の式")
chk(sp.factor(2 * x ** 2 + 4 * x) == 2 * x * (x + 2), "因数分解")
for _v in (0, -2):
    eq(comp(_f, _g).subs(x, _v), comp(_g, _f).subs(x, _v), f"x={_v} で一致")
eq(comp(_f, _g).subs(x, 0), 1, "x=0 では 1")
eq(comp(_f, _g).subs(x, -2), 9, "x=-2 では 9")
ne(comp(_f, _g).subs(x, 1), comp(_g, _f).subs(x, 1), "x=1 では一致しない")

# ══════════════════════════════════════════════════════════
# 2. 例題 2
# ══════════════════════════════════════════════════════════
eq(_fi5.subs(x, 11), 5, "例題2(c) f^-1(11) = 5")
eq(_f5.subs(x, 5), 11, "検算 f(5) = 11")
eq(sp.simplify(_f5.subs(x, _fi5)), x, "f(f^-1(x)) = x")
eq(sp.simplify(_fi5.subs(x, _f5)), x, "f^-1(f(x)) = x")
chk(sp.diff(_f5, x) == 3 and 3 != 0, "傾きが 0 でないので one-to-one")
chk(sp.is_increasing(_f5, REALS), "単調増加")

# ══════════════════════════════════════════════════════════
# 3. 例題 3
# ══════════════════════════════════════════════════════════
_fi3 = x ** 2 + 1
eq(sp.simplify(_fr.subs(x, _fi3.subs(x, xp))), xp, "x >= 0 で f(f^-1(x)) = x")
eq(sp.simplify(_fi3.subs(x, _fr)), x, "f^-1(f(x)) = x")
eq(_fr.subs(x, 5), 2, "f(5) = 2")
eq(_fi3.subs(x, 2), 5, "f^-1(2) = 5（往復した）")
eq(_fi3.subs(x, -2), 5, "x=-2 も 5 に移る")
ne(2, -2, "だから x^2+1 は実数全体では one-to-one でない")
chk(sp.solveset(sp.Eq(_fi3, 5), x, REALS) == {2, -2}, "戻り先が 2 つになる")

# ══════════════════════════════════════════════════════════
# 4. 例題 4
# ══════════════════════════════════════════════════════════
_f4, _g4 = 1 / x, x - 3
eq(comp(_f4, _g4), 1 / (x - 3), "例題4(a)")
chk(sp.solveset(sp.Eq(x - 3, 0), x, REALS) == {3}, "例題4(b) x ≠ 3")
eq(sp.simplify(comp(_g4, _f4) - (1 / x - 3)), 0, "例題4(c)")
eq(comp(_f4, _g4).subs(x, 0), -R(1, 3), "x=0 でも値が出る")
eq(comp(_f4, _g4).subs(x, 4), 1, "x=4 で 1")
eq(comp(_f4, _g4).subs(x, 2), -1, "x=2 で -1")
chk(comp(_f4, _g4).subs(x, 3) is sp.zoo, "x=3 では値をもたない")
eq(sp.simplify(comp(_g4, _f4).subs(x, 2)), -R(5, 2), "(g∘f)(2) = -5/2")
ne(-1, -R(5, 2), "2 つの合成はちがう")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
_e1f, _e1g = x + 4, 3 * x
eq(_e1g.subs(x, 2), 6, "演習1 g(2) = 6")
eq(_e1f.subs(x, 6), 10, "f(6) = 10")
eq(comp(_e1f, _e1g), 3 * x + 4, "演習2(a)")
eq(comp(_e1g, _e1f), 3 * x + 12, "演習2(b)")
eq(comp(_e1f, _e1g).subs(x, 2), 10, "合成の式でも 10")
eq(comp(_e1g, _e1f).subs(x, 2), 18, "(g∘f)(2) = 18")
ne(10, 18, "取りちがえると値がちがう")
eq(comp(_e1f, _e1g).subs(x, 1), 7, "x=1 で 7")
eq(comp(_e1g, _e1f).subs(x, 1), 15, "x=1 で 15")

inv_ok(5 * x - 2, (x + 2) / 5, "演習3")
eq(sp.simplify((5 * x - 2).subs(x, (x - 2) / 5)), x - 4, "符号を誤ると x-4")
ne(x - 4, x, "x にならない")

inv_ok(x / 4 + 3, 4 * x - 12, "演習4")
eq(sp.expand(4 * (x - 3)), 4 * x - 12, "4(x-3) = 4x-12")
ne(sp.simplify((x / 4 + 3).subs(x, 4 * x - 3)), x, "4x-3 では x にならない")

chk(sp.solve(sp.Eq(2 * x + 7, 3), x) == [-2], "演習5 f^-1(3) = -2")
eq((2 * x + 7).subs(x, -2), 3, "検算 f(-2) = 3")
eq(((x - 7) / 2).subs(x, 3), -2, "式からも -2")
inv_ok(2 * x + 7, (x - 7) / 2, "演習5 の式")

eq(comp(x ** 2, x + 5), (x + 5) ** 2, "演習6(a)")
chk(sp.solveset(x + 5 >= 0, x, REALS) == sp.Interval(-5, sp.oo), "演習6(b)")
eq((x + 5).subs(x, -6), -1, "x=-6 では g(x) = -1")
chk(-1 < 0, "f の domain に入らない")
eq((x + 5).subs(x, -5), 0, "x=-5 では 0（入る）")
eq((x + 5).subs(x, -1), 4, "x=-1 でも入る")

eq(comp(sp.sqrt(x), x - 9), sp.sqrt(x - 9), "演習7")
chk(sp.solveset(x - 9 >= 0, x, REALS) == sp.Interval(9, sp.oo), "演習7 domain")
chk(sp.sqrt(sp.Integer(8 - 9)).is_real is False, "x=8 では実数でない")
eq(sp.sqrt(sp.Integer(13 - 9)), 2, "x=13 で 2")
chk(sp.solveset(x >= 0, x, REALS) == sp.Interval(0, sp.oo), "g∘f の domain は x >= 0")

_e8, _e8i = 2 / (x - 1), 2 / x + 1
inv_ok(_e8, _e8i, "演習8")
eq(sp.simplify(_e8.subs(x, 3)), 1, "f(3) = 1")
eq(sp.simplify(_e8i.subs(x, 1)), 3, "f^-1(1) = 3（往復した）")

eq(comp(2 * x, x + 1), 2 * x + 2, "演習9 f∘g")
eq(comp(x + 1, 2 * x), 2 * x + 1, "演習9 g∘f")
ne(2 * x + 2, 2 * x + 1, "ちがう")
eq(comp(2 * x, x + 1).subs(x, 3), 8, "x=3 で 8")
eq(comp(x + 1, 2 * x).subs(x, 3), 7, "x=3 で 7")

eq(comp(x ** 2, x + 3), (x + 3) ** 2, "演習10 正しい式")
eq(sp.expand((x + 3) ** 2), x ** 2 + 6 * x + 9, "展開")
eq(sp.expand((x + 3) ** 2 - (x ** 2 + 3)), 6 * x + 6, "差は 6x+6")
chk(sp.solveset(sp.Eq(6 * x + 6, 0), x, REALS) == {-1}, "一致するのは x=-1 だけ")
eq(((x + 3) ** 2).subs(x, -1), 4, "x=-1 では両方 4")
eq((x ** 2 + 3).subs(x, -1), 4, "同上")
eq(((x + 3) ** 2).subs(x, 1), 16, "x=1 では 16")
eq((x ** 2 + 3).subs(x, 1), 4, "誤った式では 4")
ne(16, 4, "合わない")
eq(comp(x + 3, x ** 2), x ** 2 + 3, "生徒の式は g∘f")

# ══════════════════════════════════════════════════════════
# 6. 演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("3x + 4", "演習2"), ("3x + 12", "演習2"),
                ("\\frac{x+2}{5}", "演習3"), ("4x - 12", "演習4"),
                ("(x+5)^{2}", "演習6"), ("\\sqrt{x-9}", "演習7"),
                ("\\frac{2}{x}+1", "演習8"), ("(x+3)^{2}", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この項目には、公式集の欄がありません", "2.5 は公式集にない")
in_text("> $(f \\circ g)(x) = f(g(x))$.", "Guidance を逐語で")
in_text("> $(f \\circ f^{-1})(x) = (f^{-1} \\circ f)(x) = x$.", "同上")
chk(TEXT.count("\n> ") == 2, f"引用は 2 つだけ: {TEXT.count(chr(10) + '> ')}")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("**$\\circ$ は「かける」ではありません。**", "記号の注意")
in_text("正しくは、**$g(x)$ が $f$ の domain に入る条件**を、$x$ の条件に書き直します。",
        "合成の domain の決め方")
not_in_text("**できあがった式を見て決める**のがいちばん確実です。", "誤った指示は残っていない")
in_text("**できあがった式だけを見て決めてはいけません。**", "言い方を正した")
in_text("## $f \\circ g$ と $g \\circ f$ は、ふつうちがいます", "「ふつう」と書いた")
in_text("**ただし、いつもちがうわけではありません。**", "断定を避けた")
in_text("## 外側の関数だけを見て決めないでください", "合成の domain")
in_text("## $x$ は、それぞれの domain の中の値です", "恒等関数になる範囲")
in_text("入れかえを $1$ 回だけ**行うことに気をつけてください。", "入れかえは 1 回")
in_text("**$\\sqrt{x^{2}} = x$ と書けるのは $x \\ge 0$ のときだけ**です。", "条件つき")

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
chk(TEXT.count("{.model-answer}") == 5, "model-answer が 5")
chk(len(re.findall(r"^::: \{#exm-aasl25-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl25", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
for _lab in ["tbl-aasl25-steps", "tbl-aasl25-swap", "fig-aasl25-idea",
             "eq-aasl25-comp", "eq-aasl25-identity", "eq-aasl25-undo"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-5-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-5-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) $(f \\\\circ g)(x) = f(g(x))$: $g$ acts first", "図(a) の題")
in_fig("$g(x)$", "図(a) の途中")
in_fig("$f(g(x))$", "図(a) の出口")
in_fig("the inner function is written next to $x$, ", "図(a) の要点")
in_fig("(b) $(f^{-1} \\\\circ f)(x) = x$: the inverse undoes $f$", "図(b) の題")
in_fig("$x$ again", "図(b) の出口")
in_text("(a) In $(f \\circ g)(x) = f(g(x))$ the inner function $g$ acts first",
        "キャプションが (a) を説明")
in_text("(b) Passing $x$ through $f$ and then through $f^{-1}$",
        "キャプションが (b) を説明")
# 図に具体的な式を書いていない
chk(not re.search(r"\d\s*x", FIGSTR), "図に具体的な式を書いていない")
for leak in ["3x + 4", "4x - 12", "x+5", "x-9", "x+3"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-5.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-4.qmd") < DRAFT.index("aasl-2-5.qmd"), "並びが 2.4 → 2.5")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-5.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| composite function |", "| identity function |",
           "| inner function |", "| restrict |"]:
    chk(_t in GLO, "対訳表にある: " + _t)


# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════
# 所見 1 — 演習 6 が「できあがった式で決める」の反例になっていた
eq(comp(x ** 2, x + 5), (x + 5) ** 2, "演習6 の式")
chk(sp.solveset(x + 5 >= 0, x, REALS) == sp.Interval(-5, sp.oo),
    "正しい domain は x >= -5")
ne(sp.Interval(-5, sp.oo).inf, -sp.oo, "式だけ見ると実数全体になってしまう")
in_text("できあがった式の分母や根号を見るだけで済むのは、$f$ の domain が"
        "その式の条件とたまたま一致するときだけです。", "限界を書いた")
# 所見 2 — 例題 2 の誤答の説明を直した
not_in_text("それは $f^{-1}$ ではなく $f$ そのものを $3$ で割った式です。",
            "誤った説明は残っていない")
in_text("**合成して確かめること自体は、有効な検算です。** 候補が誤っていれば、"
        "合成しても $x$ にはもどりません。", "合成は有効な検算だと明記")
not_in_text("この計算は $f^{-1}$ が正しくても誤っていても $x$ になってしまうので、"
            "検算にはなりません。", "古い（誤った）循環の説明は戻っていない")
eq(sp.simplify((_fi5).subs(x, _f5)), x, "f^-1(f(x)) はつねに x")
# 所見 3 — 例題 1(d) の検算を f と g に通す形に
in_text("**(b)(c) の式ではなく、$f$ と $g$ に順に通して**確かめます。", "循環を避けた")
eq(_g.subs(x, 0), 0, "g(0) = 0")
eq(_f.subs(x, 0), 1, "f(0) = 1")
eq(_g.subs(x, 1), 1, "g(1) = 1")
eq(_g.subs(x, -2), 4, "g(-2) = 4")
eq(_f.subs(x, 4), 9, "f(4) = 9")
eq(_f.subs(x, -2), -3, "f(-2) = -3")
eq(_g.subs(x, -3), 9, "g(-3) = 9")
# 所見 4 — 例題 3(c) の検算を制限の外側で
in_text("**制限の外側で、往復が壊れることを見ます。**", "制限を検証している")
eq((x ** 2 + 1).subs(x, -1), 2, "x=-1 を入れると 2")
eq(sp.sqrt(sp.Integer(2) - 1), 1, "f(2) = 1")
ne(1, -1, "-1 には戻らない")
eq((x ** 2 + 1).subs(x, 0), 1, "f^-1(0) = 1")
eq(sp.sqrt(sp.Integer(1) - 1), 0, "f(1) = 0（往復する）")
# 所見 5 — 例題 4 の検算
in_text("**合成の式を自分で評価し直すだけでは、(a) の誤りは見つかりません。**", "限界を明記")
eq((x - 3).subs(x, 5), 2, "g(5) = 2")
eq(R(1, 2), sp.simplify((1 / (x - 3)).subs(x, 5)), "合成の式でも 1/2")
in_text("**$g(x)$ が $f$ の domain に入るかを、境目の前後で見ます。**", "domain の検算")
eq((x - 3).subs(x, 4), 1, "g(4) = 1")
eq((x - 3).subs(x, 2), -1, "g(2) = -1")
eq((x - 3).subs(x, 3), 0, "g(3) = 0")
# 所見 6 — 演習 1 の解説が演習 2 の答えを漏らしていた
_exs = TEXT[TEXT.index("## Exercises"):]
_ex1 = _exs[:_exs.index("[2]{.ex-no}")]
chk("3x + 4" not in _ex1, "演習1 の解説に演習2 の答えがない")
chk("3x + 12" not in _ex1 and "18" not in _ex1, "同上")
in_text("**それぞれの機械が何をするかに戻ります。**", "式を作らない検算")
# 所見 7 — Why it works と Common errors の例を演習 9 と分けた
in_text("「$3$ 倍する」と「$2$ を足す」で考えてみてください。", "本文の例を変えた")
eq(3 * 4 + 2, 14, "3 倍してから 2 足すと 14")
eq((4 + 2) * 3, 18, "2 足してから 3 倍すると 18")
ne(14, 18, "順番で変わる")
chk("2x+2" not in BODY, "演習 9 の答えは本文に出てこない")
in_text("$f(x) = 3x$、$g(x) = x+2$ なら、$(f \\circ g)(x) = 3x+6$", "Common errors も変えた")
eq(comp(3 * x, x + 2), 3 * x + 6, "3(x+2) = 3x+6")
eq(sp.expand(3 * x * (x + 2)), 3 * x ** 2 + 6 * x, "かけ算はちがう")
# 所見 8 — 同値に条件を書いた
in_text("$f$ が one-to-one なら、$f$ が出した $y$ から、もとの $x$ がただ $1$ つに"
        "決まります。", "one-to-one の条件")
in_text("つまり、$x$ が $f$ の domain に、$y$ が $f$ の range にあるとき", "範囲の条件")
# 所見 9 — 第 7 節を一般論にとどめた
in_text("実際の例は、例題 $3$ で見ます。", "例題に譲った")
in_text("たとえば $f(x) = \\sqrt{x+2}$（domain $x \\ge -2$）の逆関数の式は $x^{2}-2$",
        "第 6 節の例も変えた")
# 所見 10 — 演習 9 の解説
in_text("この $f$、$g$ では $2x+2 = 2x+1$ に解がないので、どの $x$ でも一致しません。",
        "例が主張を支えている")
chk(sp.solveset(sp.Eq(2 * x + 2, 2 * x + 1), x, REALS) == sp.S.EmptySet,
    "実際に解がない")
# 所見 11 — GDC の断定を弱めた
in_text("**いくつかの値で試して、いつも入れた数がそのまま返ってくるかを見てください。**",
        "1 点では証明にならない")
not_in_text("**$7$ が返ってくれば、逆関数として正しく働いています。**", "断定は残っていない")
# 所見 12 — 検算の限界
in_text("**ただし、この検算では domain の書き忘れは見つかりません。**", "限界を書いた")
# 所見 13 — 図 (b) の向き
in_text("図には描いていませんが、順を入れかえて $f^{-1}$ → $f$ としても同じです。", "両向き")
# 所見 14 — 2 乗の条件
in_text("$x^{2} = y-1$ から $x = \\sqrt{y-1}$ に戻れるのは $x \\ge 0$ のときだけで",
        "2 乗の条件を正しく述べた")
not_in_text("**ここで $x \\ge 0$ が効きます**", "古い言い方は残っていない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
