"""AA SL 2.1（直線の方程式）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_1.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-1.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_2_1.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, y, k = sp.symbols("x y k")


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


def grad(p, q):
    """公式集の gradient formula から。"""
    return R(q[1] - p[1], q[0] - p[0])


def on(line, p, msg=""):
    """点 p が直線 line（= 0 の形）の上にあるか。"""
    chk(sp.simplify(line.subs({x: p[0], y: p[1]})) == 0,
        "点が直線上にない: " + msg + f" {p}")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの
# ══════════════════════════════════════════════════════════
_m, _c, _x1, _y1 = sp.symbols("m c x1 y1")
# 3 つの形が同じ直線を表す
eq(sp.solve(sp.Eq(y - _y1, _m * (x - _x1)), y)[0],
   _m * x + (_y1 - _m * _x1), "point-gradient → gradient-intercept")
_a, _b, _d = sp.symbols("a b d", nonzero=True)
eq(sp.solve(_a * x + _b * y + _d, y)[0], (-_a * x - _d) / _b,
   "general → gradient-intercept")
# 傾きは、順番を入れかえても同じ
for _p, _q in [((1, 5), (4, 14)), ((-2, 7), (4, -5)), ((1, 2), (5, -6)),
               ((3, 8), (7, 2))]:
    eq(grad(_p, _q), grad(_q, _p), f"順番を入れかえても同じ: {_p},{_q}")
# 上下がずれると符号が逆になる
eq(R(5 - 14, 4 - 1), -3, "上下がずれた値は -3")
ne(R(5 - 14, 4 - 1), grad((1, 5), (4, 14)), "正しい値とはちがう")
# 垂直の条件
for _m1 in [2, R(-2, 3), 1, 3, R(1, 2)]:
    eq(_m1 * (-1 / R(_m1)), -1, f"m×(-1/m) = -1: m={_m1}")
eq(R(-2, 3) * R(3, 2), -1, "-2/3 と 3/2 は垂直")
ne(R(-2, 3) * R(2, 3), -1, "逆数だけでは垂直にならない")
ne(R(-2, 3) * R(-3, 2), -1, "符号だけでは垂直にならない")
# 90 度回すと、傾きが負の逆数になる（Why it works）
for _m1 in [2, 3, R(1, 2), R(-2, 3)]:
    _v = (1, _m1)
    _w = (-_m1, 1)          # 反時計回りに 90 度
    eq(R(_w[1], 1) / R(_w[0], 1), -1 / R(_m1), f"回した向きの傾き: m={_m1}")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
eq(grad((1, 5), (4, 14)), 3, "第 2 節の例は 3")
# 第 4 節の変形
_L4 = x + 2 * y + 4
on(_L4, (2, -3), "第 4 節の直線")
eq(sp.solve(_L4, y)[0], -R(1, 2) * x - 2, "第 4 節の gradient-intercept form")
eq(sp.solve(_L4.subs(x, 0), y)[0], -2, "第 5 節の y 切片")
eq(sp.solve(_L4.subs(y, 0), x)[0], -4, "第 5 節の x 切片")
# 第 6 節の表
for _m1, _m2 in [(2, R(-1, 2)), (R(-2, 3), R(3, 2)), (1, -1)]:
    eq(_m1 * _m2, -1, f"表の組: {_m1}, {_m2}")
# 第 7 節
eq(R(45, 900), R(1, 20), "45/900 = 1/20")
eq(R(1, 20), R("0.05"), "1/20 = 0.05")
eq(R("0.05") * 100, 5, "5%")

# ══════════════════════════════════════════════════════════
# 2. 例題 1
# ══════════════════════════════════════════════════════════
eq(grad((1, 5), (4, 14)), 3, "例題1(a) 3")
eq(R(9, 3), 3, "9/3 = 3")
_L1 = 3 * x - y + 2
eq(sp.solve(_L1, y)[0], 3 * x + 2, "例題1(b) y = 3x+2")
on(_L1, (1, 5), "例題1 の A")
on(_L1, (4, 14), "例題1 の B")
eq((3 * x + 2).subs(x, 4), 14, "B を入れると 14")
eq(sp.solve(_L1.subs(y, 0), x)[0], R(-2, 3), "例題1(d) x 切片")
eq((3 * x + 2).subs(x, R(-2, 3)), 0, "戻すと y = 0")
eq((-3 * x + 2).subs(x, 4), -10, "符号をまちがえた誤答は -10")
ne(-10, 14, "その誤答は B と合わない")

# ══════════════════════════════════════════════════════════
# 3. 例題 2
# ══════════════════════════════════════════════════════════
_L2 = 3 * x + 2 * y - 10
on(_L2, (4, -1), "例題2 の点")
eq(sp.solve(_L2, y)[0], -R(3, 2) * x + 5, "例題2 の傾きは -3/2")
eq(sp.solve(_L2.subs(x, 0), y)[0], 5, "例題2(c) y 切片 5")
eq(-3 * (4 - 4) + 12 - 12, 0, "2y+2 = -3(x-4) の途中")
eq(2 * (-1) + 2, 0, "点を入れると 2y+2 = 0")
# 例題 2 は、本文（第 4・5 節）と同じ数値を使っていない
_body = TEXT[:TEXT.index("## Worked examples")]
chk("(4, -1)" not in _body and "(4,-1)" not in _body, "例題2 の点は本文に出てこない")
chk("3x + 2y - 10" not in _body, "例題2 の答えは本文に出てこない")
# 符号をまちがえた式は、点を通らない
_bad2 = y + 1 + R(3, 2) * (x + 4)
ne(_bad2.subs({x: 4, y: -1}), 0, "符号をまちがえた式は (4,-1) を通らない")
eq(-R(3, 2) * (4 + 4), -12, "符号をまちがえた右辺は -12")

# ══════════════════════════════════════════════════════════
# 4. 例題 3
# ══════════════════════════════════════════════════════════
_L3 = 2 * x + 3 * y - 12
eq(sp.solve(_L3, y)[0], -R(2, 3) * x + 4, "例題3(a) 傾き -2/3")
_par = 2 * x + 3 * y - 9
on(_par, (3, 1), "例題3(b) の点")
eq(sp.solve(_par, y)[0], -R(2, 3) * x + 3, "平行なので傾きも -2/3")
_perp = 3 * x - 2 * y - 7
on(_perp, (3, 1), "例題3(c) の点")
eq(sp.solve(_perp, y)[0], R(3, 2) * x - R(7, 2), "垂直の傾きは 3/2")
eq(R(-2, 3) * R(3, 2), -1, "積は -1")
eq(R(-2, 3) * R(2, 3), R(-4, 9), "符号を変えない誤答は -4/9")
ne(R(-4, 9), -1, "その誤答は垂直にならない")
# (d) 平行な 2 直線は交わらない（連立すると矛盾する）
chk(sp.solve([_par, _L3], [x, y]) == [], "2x+3y-9=0 と 2x+3y-12=0 は交点なし")
eq(sp.expand(_L3 - _par), -3, "2 式の差は定数 -3（= 9 - 12）")
ne(-9, -12, "9 = 12 にはならない")
eq(sp.solve(_par, y)[0] - sp.solve(_L3, y)[0], -1, "y 切片だけが違う")

# ══════════════════════════════════════════════════════════
# 5. 例題 4
# ══════════════════════════════════════════════════════════
eq(R(84, 1200), R(7, 100), "例題4(a) 7/100")
eq(R(7, 100), R("0.07"), "= 0.07")
eq(R("0.07") * 100, 7, "例題4(b) 7%")
eq(R("0.02") * 350, 7, "例題4(c) 7 m")
eq(R(7, 350), R("0.02"), "戻すと 0.02")
eq(R(84, 12), 7, "水平 100 m あたり 7 m")
eq(R(1200, 100), 12, "1200 は 100 の 12 倍")
eq(350 / R("0.02"), 17500, "掛けるところを割った誤答")
eq(R(17500, 1000), R("17.5"), "17500 m は 17.5 km")
chk(17500 > 1000, "その誤答は大きすぎる")
# 例題 4 は、第 7 節と同じ数値を使っていない
chk("84" not in _body and "1200" not in _body, "例題4 の数値は本文に出てこない")
# 道に沿った距離は、水平距離より長い（斜辺のほうが長い）
_along = sp.sqrt(sp.Integer(100) ** 2 + 5 ** 2)
chk(_along > 100, "斜辺は水平の辺より長い")
not_in_text("100.1", "電卓が要る数値は書かない")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(grad((-2, 7), (4, -5)), -2, "演習1 -2")
eq(R(-12, 6), -2, "-12/6 = -2")
eq(grad((4, -5), (-2, 7)), -2, "順番を変えても -2")
chk(grad((-2, 7), (4, -5)) < 0, "x が増えて y が減るので負")

eq((4 * x - 5).subs(x, 2), 3, "演習2 は (2,3) を通る")
eq(4 * 2 - 8, 0, "y-3 = 4x-8 の途中")
eq((4 * x + 3).subs(x, 2), 11, "c に y 座標を入れた誤答は 11")
ne(11, 3, "その誤答は合わない")

_e3 = 3 * x - 4 * y - 8
on(_e3, (0, -2), "演習3 の y 切片")
on(_e3, (4, 1), "演習3 のもう 1 点")
eq((R(3, 4) * x - 2).subs(x, 4), 1, "もとの式でも (4,1)")
eq(sp.solve(_e3, y)[0], R(3, 4) * x - 2, "もとの式に戻る")

_e4 = 5 * x - 2 * y - 20
eq(sp.solve(_e4.subs(y, 0), x)[0], 4, "演習4 x 切片 4")
eq(sp.solve(_e4.subs(x, 0), y)[0], -10, "演習4 y 切片 -10")
on(_e4, (4, 0), "演習4 (4,0)")
on(_e4, (0, -10), "演習4 (0,-10)")
eq(sp.solve(_e4, y)[0], R(5, 2) * x - 10, "傾きは正、y 切片は負")

eq(grad((1, 2), (5, -6)), -2, "演習5 傾き -2")
eq(R(-8, 4), -2, "-8/4 = -2")
_e5 = 2 * x + y - 4
on(_e5, (1, 2), "演習5 の 1 点目")
on(_e5, (5, -6), "演習5 の 2 点目")
eq(sp.solve(_e5, y)[0], -2 * x + 4, "y = -2x+4")

eq(sp.solve(3 * x - y + 5, y)[0], 3 * x + 5, "演習6 L の傾きは 3")
eq((3 * x - 5).subs(x, 2), 1, "演習6(a) は (2,1) を通る")
_e6 = x + 3 * y - 5
on(_e6, (2, 1), "演習6(b) は (2,1) を通る")
eq(sp.solve(_e6, y)[0], -R(1, 3) * x + R(5, 3), "傾きは -1/3")
eq(3 * R(-1, 3), -1, "積は -1")
eq(3 * (-3), -9, "符号だけ変えた誤答の積")
ne(-9, -1, "その誤答は垂直にならない")

eq(R("0.6") / R("7.5"), R(2, 25), "演習7 2/25")
eq(R(2, 25), R("0.08"), "= 0.08")
eq(R("0.08") * 100, 8, "演習7(b) 8%")
eq(R("0.08") * R("7.5"), R("0.6"), "戻すと 0.6")
eq(R("7.5") / R("0.6"), R(25, 2), "上下を逆にした誤答は 12.5")
chk(R(25, 2) * 100 > 1000, "その誤答は 1000% を超える")

chk(sp.solve(sp.Eq(R(1, 6) * (1 - k), -R(1, 2)), k) == [4], "演習8 k = 4")
eq(grad((0, 4), (6, 1)), -R(1, 2), "k=4 で傾きが -1/2")
eq(grad((0, -2), (6, 1)), R(1, 2), "k=-2 とした誤答は +1/2")
ne(R(1, 2), -R(1, 2), "符号が逆になる")
chk(4 > 1, "傾きが負なので k > 1")

# 演習 9（縦向きの直線）
chk((3 - 3) == 0, "(3,1) と (3,8) では分母が 0")
eq(8 - 1, 7, "分子は 7")
chk(sp.zoo == sp.Integer(7) / 0, "7/0 は数ではない")

eq(grad((3, 8), (7, 2)), -R(3, 2), "演習10 正しい傾き -3/2")
eq(R(7 - 3, 2 - 8), -R(2, 3), "生徒の答えは -2/3")
ne(-R(2, 3), -R(3, 2), "合わない")
eq((8 - R(3, 2) * (7 - 3)), 2, "正しい傾きなら B を通る")
eq((8 - R(2, 3) * (7 - 3)), R(16, 3), "生徒の傾きだと 16/3")
ne(R(16, 3), 2, "B とは合わない")
chk(-R(2, 3) < 0 and -R(3, 2) < 0, "どちらも負なので符号では見分けられない")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **2.1** の欄に `Gradient formula` として印刷", "公式集にある")
in_text("> $m = \\dfrac{y_{2}-y_{1}}{x_{2}-x_{1}}$", "gradient formula を逐語で")
in_text("公式集の **2.1** の欄に `Equations of a straight line` として、まとめて印刷",
        "3 つの形も公式集にある")
in_text("> $y = mx + c$ ; $ax + by + d = 0$ ; $y - y_{1} = m\\left(x - x_{1}\\right)$",
        "3 つの形を逐語で")
in_text("> $y = mx + c$ (gradient-intercept form).", "Guidance の名前")
in_text("> $ax + by + d = 0$ (general form).", "同上")
in_text("> $y - y_1 = m(x - x_1)$ (point-gradient form).", "同上")
in_text("## この $2$ つは公式集にありません", "平行・垂直は載っていない")
in_text("> Parallel lines $m_1 = m_2$.", "シラバスの Content を逐語で")
in_text("> Perpendicular lines $m_1 \\times m_2 = -1$.", "同上")
in_text("> Calculate gradients of inclines such as mountain roads, bridges, etc.",
        "勾配の Guidance を逐語で")
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
chk(len(re.findall(r"^::: \{#exm-aasl21-", TEXT, re.M)) == 4, "例題が 4")
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
for word in ["得点になりません", "点になりません", "点を落とします"]:
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
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl21", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 10. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-1-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-1-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Gradient $=$ rise $\\\\div$ run", "図(a) の題")
in_fig("run $= x_{2}-x_{1}$", "図(a) の run")
in_fig("rise\\n$= y_{2}-y_{1}$", "図(a) の rise")
in_fig("any two points on the line give the same $m$", "図(a) の要点")
in_fig("(b) Parallel and perpendicular", "図(b) の題")
in_fig("gradient $m$", "図(b) のラベル")
in_fig("gradient $-\\\\dfrac{1}{m}$", "図(b) の負の逆数")
in_text("(a) The gradient is the rise divided by the run", "キャプションが (a) を説明")
in_text("(b) Parallel lines have equal gradients", "キャプションが (b) を説明")
# 図が使っている傾きは、実際に垂直
eq(2 * (-R(1, 2)), -1, "図(b) の 2 本は垂直")
# 図に数値の答えを書いていない
for leak in ["-2", "4x", "3x - 4y", "(4, 0)", "(0, -10)", "2x + y",
             "3x - 5", "x + 3y", "0.08", "8\\%", "= 4", "-3/2", "5\\%"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-1.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-9.qmd") < DRAFT.index("aasl-2-1.qmd"), "並びが 1.9 → 2.1")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-1.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| gradient |", "| intercept |", "| parallel |", "| perpendicular |",
          "| incline |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ══════════════════════════════════════════════════════════
# 12. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════
# 所見 1 — 誤答検証の計算を直した
in_text("$A(1,5)$ から $y - 5 = -3(x-1)$、つまり $y = -3x + 8$ になります。", "誤答の式")
eq((-3 * x + 8).subs(x, 1), 5, "誤答の式も A は通る")
eq((-3 * x + 8).subs(x, 4), -4, "誤答の式では x=4 で -4")
ne(-4, 14, "B とは合わない")
not_in_text("$y = -3(4)+2 = -10$", "成り立たない式は残っていない")
# 所見 2 — 上下の順の説明が式と合っている
in_text("上を $A$ から（$5-14$）、下を $B$ から（$4-1$）取っているので、符号が逆になります。",
        "説明と式が合っている")
not_in_text("**上を $B$ から、下を $A$ から**取ることです", "逆の説明は残っていない")
# 所見 5 — 演習 1 の検算が誤りを捕まえられる
in_text("**上下をそろえて入れかえるだけでは、検算になりません。**", "循環的な検算を直した")
not_in_text("**上下をそろえて入れかえれば、値は変わりません。**", "古い検算は残っていない")
eq(-2 * (-2) + 3, 7, "y = -2x+3 は (-2,7) を通る")
eq(-2 * 4 + 3, -5, "(4,-5) も通る")
chk(R(7 - (-5), 4 - (-2)) == 2, "上下をまぜた誤答は +2")
chk(R(-5 - 7, -2 - 4) == 2, "入れかえても同じ誤答 +2 が出る")
# 所見 8 — m1 ≠ 0 の条件
in_text("**$m_{1} \\neq 0$ のとき**、$m_{1}m_{2} = -1$ は $m_{2} = -\\dfrac{1}{m_{1}}$ と書き直せます。",
        "条件つきで書いた")
in_text("$m_{1} = 0$（横向きの直線）のときは、下の警告を見てください。", "同上")
# 所見 9 — 90 度回転の説明
in_text("横だった辺が縦になり、縦だった辺が横になります。", "回転の説明を足した")
in_text("（$m < 0$ のときは「左へ $m$」が実際には右向きになりますが、座標の書き方は同じ $(-m, 1)$ です。）",
        "m < 0 の但し書き")
# 所見 10 — 演習 6 の検算
in_text("**自分で書いた $-\\dfrac{1}{3}$ ではなく、答えの式から傾きを取り直すのが要です。**",
        "循環的な検算を直した")
eq(sp.solve(_e6, y)[0], -R(1, 3) * x + R(5, 3), "答えの式から取り直した傾き")
# 所見 11 — 図を本文で受けている
chk(TEXT.count("@fig-aasl21-idea") >= 2, f"図を本文で受けている: {TEXT.count('@fig-aasl21-idea')}")
# 所見 12 — 演習 2 の検算
in_text("$x = 3$ とすると $y = 12 - 5 = 7$", "独立した確認になっている")
eq((4 * x - 5).subs(x, 3), 7, "x=3 で y=7")
not_in_text("$y = mx+c$ の $m$ が $4$ です ✓", "読み返すだけの検算は残っていない")
# 所見 13 — 平行の条件
in_text("定数項まで同じ比なら、同じ直線になります", "同一直線の場合を書いた")
# 所見 15 — 演習 10
in_text("**この誤りは、符号だけを見ても気づけない**", "言い方を正した")
not_in_text("値が近いと見つけにくい", "不正確な言い方は残っていない")
# 所見 18 — 演習 7 の見当
in_text("$7.5$ の $10\\%$ は $0.75$ で、実際の上がり $0.6$ より大きい。", "独立した見当")
eq(R("7.5") * R("0.1"), R("0.75"), "7.5 の 10% は 0.75")
chk(R("0.6") < R("0.75"), "0.6 < 0.75 なので 10% より小さい")
# 所見 19 — 「いつも」を外した
not_in_text("いつも point-gradient form から", "断定は残っていない")
# 所見 14 — command term
not_in_text("[Write the equation", "裸の Write は使っていない")
chk(TEXT.count("Write down the equation") == 1, "Write down は代入だけの設問に 1 つ")
# 所見 6 — 演習 9 と重ならない
not_in_text("cannot be used to check that a horizontal line and a vertical line",
            "例題 3(d) は差し替えた")
chk(TEXT.count("A vertical line has") == 1, "縦向きの直線の英文は演習 9 だけ")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
