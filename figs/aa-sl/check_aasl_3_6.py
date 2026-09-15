"""AA SL 3.6（三角比の恒等式）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_6.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-6.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_6.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
PI = sp.pi
TH = sp.Symbol("theta", real=True)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(u - v) == 0, msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def s2(s_, c_):
    return 2 * s_ * c_


def c2(s_, c_):
    return c_ ** 2 - s_ ** 2


# ══════════════════════════════════════════════════════════
# 0. 恒等式そのもの
# ══════════════════════════════════════════════════════════
eq(sp.cos(TH) ** 2 + sp.sin(TH) ** 2, 1, "ピタゴラスの恒等式")
eq(sp.sin(2 * TH), 2 * sp.sin(TH) * sp.cos(TH), "sin 2θ")
eq(sp.cos(2 * TH), sp.cos(TH) ** 2 - sp.sin(TH) ** 2, "cos 2θ の 1 つ目")
eq(sp.cos(2 * TH), 2 * sp.cos(TH) ** 2 - 1, "cos 2θ の 2 つ目")
eq(sp.cos(2 * TH), 1 - 2 * sp.sin(TH) ** 2, "cos 2θ の 3 つ目")
# 3 つの形は入れかえで移り合う
_c, _s = sp.symbols("c_ s_")
eq((_c ** 2 - (1 - _c ** 2)), 2 * _c ** 2 - 1, "sin² = 1 - cos² を入れる")
eq(((1 - _s ** 2) - _s ** 2), 1 - 2 * _s ** 2, "cos² = 1 - sin² を入れる")
# θ = 0 でどれも 1
for _f in [sp.cos(TH) ** 2 - sp.sin(TH) ** 2, 2 * sp.cos(TH) ** 2 - 1,
           1 - 2 * sp.sin(TH) ** 2]:
    eq(_f.subs(TH, 0), 1, "θ = 0 でどの形も 1")
# 半角の形
eq((1 - sp.cos(2 * TH)) / 2, sp.sin(TH) ** 2, "sin²θ = (1 - cos2θ)/2")
# 本文の走る例（sin = 2/3、鋭角）
_S, _C = R(2, 3), sp.sqrt(5) / 3
eq(_S ** 2 + _C ** 2, 1, "本文 単位円の上")
eq(sp.sqrt(1 - R(2, 3) ** 2), sp.sqrt(5) / 3, "本文 cos = √5/3")
eq(_S / _C, 2 * sp.sqrt(5) / 5, "本文 tan = 2√5/5")
eq(s2(_S, _C), 4 * sp.sqrt(5) / 9, "本文 sin2θ = 4√5/9")
eq(1 - 2 * _S ** 2, R(1, 9), "本文 cos2θ = 1/9")
in_text("\\cos\\theta = \\sqrt{1 - \\frac{4}{9}} = \\sqrt{\\frac{5}{9}} = "
        "\\frac{\\sqrt{5}}{3}", "本文の cos の例")
in_text("\\sin 2\\theta = 2 \\times \\frac{2}{3} \\times \\frac{\\sqrt{5}}{3} = "
        "\\frac{4\\sqrt{5}}{9}", "本文の sin2θ の例")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  sin = 3/5、鋭角
# ══════════════════════════════════════════════════════════
eq(1 - R(3, 5) ** 2, R(16, 25), "例題1(a) cos² = 16/25")
eq(sp.sqrt(R(16, 25)), R(4, 5), "例題1(a) cos = 4/5")
eq(R(3, 5) / R(4, 5), R(3, 4), "例題1(b) tan = 3/4")
eq(s2(R(3, 5), R(4, 5)), R(24, 25), "例題1(c) sin2θ = 24/25")
eq(3 ** 2 + 4 ** 2, 5 ** 2, "例題1 検算 3-4-5")
chk(R(24, 25) <= 1, "例題1(c) 検算 1 以下")
chk(R(24, 25) > R(3, 5), "例題1(c) 検算 sinθ より大きい")
chk(abs(float(sp.deg(sp.asin(R(3, 5)))) - 36.87) < 0.01, "θ ≈ 37°")
chk(abs(float(sp.deg(sp.asin(R(24, 25)))) - 73.74) < 0.01, "2θ ≈ 74°")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  cos = 3/4、鋭角
# ══════════════════════════════════════════════════════════
eq(1 - R(3, 4) ** 2, R(7, 16), "例題2(a) sin² = 7/16")
eq(sp.sqrt(R(7, 16)), sp.sqrt(7) / 4, "例題2(a) sin = √7/4")
eq(s2(sp.sqrt(7) / 4, R(3, 4)), 3 * sp.sqrt(7) / 8, "例題2(b) sin2x = 3√7/8")
eq(2 * R(3, 4) ** 2 - 1, R(1, 8), "例題2(c) cos2x = 1/8")
eq(c2(sp.sqrt(7) / 4, R(3, 4)), R(1, 8), "例題2(c) 検算 別の形")
eq(R(3, 4) ** 2 + (sp.sqrt(7) / 4) ** 2, 1, "例題2(a) 検算 2 乗の和")
chk(abs(float(3 * sp.sqrt(7) / 8) - 0.9922) < 0.001, "例題2(b) 検算 約 0.99")
chk(3 * sp.sqrt(7) / 8 < 1, "例題2(b) 検算 1 以下")
chk(R(1, 8) > 0, "例題2(d) cos2x は正")
_x2 = sp.acos(R(3, 4))
chk(0 < float(2 * _x2) < float(PI / 2), "例題2(d) 2x は鋭角")
chk(abs(float(sp.deg(_x2)) - 41.41) < 0.01, "x ≈ 41.4°")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  sin = -5/13、第 3 象限
# ══════════════════════════════════════════════════════════
eq(1 - R(5, 13) ** 2, R(144, 169), "例題3(a) cos² = 144/169")
eq(-sp.sqrt(R(144, 169)), R(-12, 13), "例題3(a) cos = -12/13")
eq(R(-5, 13) / R(-12, 13), R(5, 12), "例題3(b) tan = 5/12")
eq(s2(R(-5, 13), R(-12, 13)), R(120, 169), "例題3(c) sin2θ = 120/169")
eq(1 - 2 * R(5, 13) ** 2, R(119, 169), "例題3(d) cos2θ = 119/169")
eq(c2(R(-5, 13), R(-12, 13)), R(119, 169), "例題3(d) 検算 別の形")
eq(5 ** 2 + 12 ** 2, 13 ** 2, "例題3 検算 5-12-13")
eq(R(120, 169) ** 2 + R(119, 169) ** 2, 1, "例題3 検算 2 乗の和")
eq(120 ** 2 + 119 ** 2, 169 ** 2, "例題3 検算 14400+14161 = 28561")
chk(R(120, 169) > 0 and R(119, 169) > 0, "例題3(d) 2θ は第 1 象限")
# 第 3 象限の θ で本当にそうなるか
_t3 = PI + sp.asin(R(5, 13))
chk(float(PI) < float(_t3) < float(3 * PI / 2), "θ は第 3 象限")
eq(sp.sin(_t3), R(-5, 13), "θ の sin は -5/13")
eq(sp.simplify(sp.cos(_t3)), R(-12, 13), "θ の cos は -12/13")
eq(sp.simplify(sp.sin(2 * _t3)), R(120, 169), "sin2θ を直接")
eq(sp.simplify(sp.cos(2 * _t3)), R(119, 169), "cos2θ を直接")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  書きかえ
# ══════════════════════════════════════════════════════════
eq((1 - sp.cos(2 * TH)) / 2, sp.sin(TH) ** 2, "例題4(a)")
eq(sp.sin(PI / 8) ** 2, (2 - sp.sqrt(2)) / 4, "例題4(b) sin²(π/8)")
eq((1 - sp.cos(PI / 4)) / 2, (2 - sp.sqrt(2)) / 4, "例題4(b) 半角から")
eq(2 * (PI / 8), PI / 4, "例題4(b) 2θ = π/4")
eq(1 + sp.cos(2 * TH), 2 * sp.cos(TH) ** 2, "例題4(c) 分母")
eq(sp.simplify(sp.sin(2 * TH) / (1 + sp.cos(2 * TH)) - sp.tan(TH)), 0,
   "例題4(c) 全体")
eq(1 + sp.cos(PI), 0, "例題4(d) 分母が 0")
chk(sp.cos(PI / 2) == 0, "例題4(d) cos(π/2) = 0")
# 検算：数でためす
eq((1 - sp.cos(PI / 3)) / 2, sp.sin(PI / 6) ** 2, "例題4(a) 検算 θ = π/6")
eq((1 - R(1, 2)) / 2, R(1, 4), "例題4(a) 検算 1/4")
chk(abs(float((2 - sp.sqrt(2)) / 4) - 0.1464) < 0.001, "例題4(b) 検算 約 0.146")
chk((2 - sp.sqrt(2)) / 4 < R(1, 4), "例題4(b) 検算 1/4 より小さい")
eq(sp.sin(PI / 2) / (1 + sp.cos(PI / 2)), 1, "例題4(c) 検算 θ = π/4 で 1")
eq(sp.tan(PI / 4), 1, "例題4(c) 検算 右辺も 1")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(1 - R(4, 5) ** 2, R(9, 25), "演習1 cos² = 9/25")
eq(sp.sqrt(R(9, 25)), R(3, 5), "演習1 cos = 3/5")
eq(1 - R(8, 17) ** 2, R(225, 289), "演習2 sin² = 225/289")
eq(sp.sqrt(R(225, 289)), R(15, 17), "演習2 sin = 15/17")
eq(8 ** 2 + 15 ** 2, 17 ** 2, "演習2 検算 8-15-17")
eq(sp.sqrt(1 - R(1, 3) ** 2), 2 * sp.sqrt(2) / 3, "演習3 cos = 2√2/3")
eq(R(1, 3) / (2 * sp.sqrt(2) / 3), sp.sqrt(2) / 4, "演習3 tan = √2/4")
eq(1 / (2 * sp.sqrt(2)), sp.sqrt(2) / 4, "演習3 有理化")
eq(sp.sqrt(1 + 8), 3, "演習3 検算 斜辺 3")
eq(sp.sqrt(1 - R(7, 25) ** 2), R(24, 25), "演習4 sin = 24/25")
eq(s2(R(24, 25), R(7, 25)), R(336, 625), "演習4 sin2θ = 336/625")
eq(7 ** 2 + 24 ** 2, 25 ** 2, "演習4 検算 7-24-25")
chk(R(336, 625) < 1, "演習4 検算 1 以下")
eq(1 - 2 * R(1, 4) ** 2, R(7, 8), "演習5 cos2θ = 7/8")
eq(c2(R(1, 4), sp.sqrt(R(15, 16))), R(7, 8), "演習5 検算 別の形")
eq(1 - R(1, 4) ** 2, R(15, 16), "演習5 検算 cos² = 15/16")
# 象限によらないこと
for _sg in [1, -1]:
    eq(1 - 2 * (R(1, 4)) ** 2, 1 - 2 * (_sg * R(1, 4)) ** 2,
       "演習5 sin の符号によらない")
eq(2 * R(1, 3) ** 2 - 1, R(-7, 9), "演習6 cos2θ = -7/9")
eq(1 - 2 * (1 - R(1, 9)), R(-7, 9), "演習6 検算 sin の形")
eq(1 - R(1, 3) ** 2, R(8, 9), "演習6 検算 sin² = 8/9")
eq(sp.simplify(sp.sin(2 * TH) / (2 * sp.sin(TH)) - sp.cos(TH)), 0, "演習7")
eq(sp.sin(PI / 3) / (2 * sp.sin(PI / 6)), sp.cos(PI / 6), "演習7 検算 θ = π/6")
eq(sp.sin(PI / 3), sp.sqrt(3) / 2, "演習7 検算 sin(π/3)")
# 演習8：cos2θ は sin だけで決まるが、cos θ は決まらない
eq(sp.cos(2 * PI / 6), sp.cos(2 * (5 * PI / 6)), "演習8 同じ sin なら cos2θ も同じ")
eq(sp.sin(PI / 6), sp.sin(5 * PI / 6), "演習8 sin は同じ")
chk(sp.cos(PI / 6) != sp.cos(5 * PI / 6), "演習8 cos はちがう")
eq(1 - 2 * R(1, 2) ** 2, R(1, 2), "演習8 検算 cos2θ = 1/2")
eq(c2(sp.sin(PI / 12), sp.cos(PI / 12)), sp.cos(PI / 6), "演習9")
eq(sp.cos(PI / 6), sp.sqrt(3) / 2, "演習9 √3/2")
chk(abs(float(sp.sqrt(3) / 2) - 0.866) < 0.001, "演習9 検算 約 0.87")
eq(sp.sqrt(1 - R(15, 17) ** 2), R(8, 17), "演習10 cos = 8/17")
eq(s2(R(15, 17), R(8, 17)), R(240, 289), "演習10 sin2θ = 240/289")
eq(2 * R(15, 17), R(30, 17), "演習10 生徒の値は 30/17")
chk(R(30, 17) > 1, "演習10 生徒の値は 1 を超える")
chk(R(240, 289) < 1, "演習10 正しい値は 1 以下")
eq(15 ** 2 + 8 ** 2, 17 ** 2, "演習10 検算 8-15-17")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("\\frac{24}{25}", "例題1(c)"), ("\\frac{3}{4}$$", "例題1(b)"),
                ("\\frac{\\sqrt{7}}{4}", "例題2(a)"),
                ("\\frac{3\\sqrt{7}}{8}", "例題2(b)"),
                ("\\frac{1}{8}", "例題2(c)"),
                ("\\frac{12}{13}", "例題3(a)"), ("\\frac{5}{12}", "例題3(b)"),
                ("\\frac{120}{169}", "例題3(c)"),
                ("\\frac{119}{169}", "例題3(d)"),
                ("2 - \\sqrt{2}}{4}", "例題4(b)"),
                ("\\frac{3}{5}$$", "演習1"), ("\\frac{15}{17}", "演習2"),
                ("\\frac{\\sqrt{2}}{4}", "演習3"),
                ("\\frac{336}{625}", "演習4"), ("\\frac{7}{8}", "演習5"),
                ("\\frac{7}{9}", "演習6"), ("\\frac{240}{289}", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **3.6** の欄に `Pythagorean identity` として印刷されています。",
        "ピタゴラスの欄")
in_text("> $\\cos^2\\theta + \\sin^2\\theta = 1$", "ピタゴラスを逐語で")
in_text("> $\\sin 2\\theta = 2\\sin\\theta\\cos\\theta$", "sin2θ を逐語で")
in_text("> $\\cos 2\\theta = \\cos^2\\theta - \\sin^2\\theta = 2\\cos^2\\theta - 1 = "
        "1 - 2\\sin^2\\theta$", "cos2θ を逐語で")
chk(TEXT.count("\n> ") == 3, f"引用は公式集の 3 つ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 3, "公式集の callout は 3 つ")
not_in_text("The Pythagorean identity:", "シラバス本文は引かない")
not_in_text("Given $\\sin\\theta$, finding possible values of", "Guidance は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("これは **identity**（恒等式）です。**どんな $\\theta$ でも成り立つ**、という意味で、"
        "解くべき方程式ではありません。", "恒等式の意味")
in_text("**$\\pm$ のどちらかは、象限を見て決めます**", "符号は象限から")
in_text("与えられていないときは、**$2$ つとも書きます**。", "象限がないとき")
in_text("**$\\sin 2\\theta$ は $2\\sin\\theta$ ではありません。**", "sin は外に出せない")
in_text("$3$ つは**同じ値の書きかえ**です。", "3 つは書きかえ")
in_text("$P$ が軸の上にあるときは三角形がつぶれますが、そのときも座標が "
        "$(\\pm 1,\\ 0)$ か $(0,\\ \\pm 1)$ なので、式はそのまま成り立ちます。",
        "軸の上の場合")
in_text("- **使える角を確かめる。** 書きかえた式に $\\tan$ や分数が出てきたら、"
        "**分母が $0$ になる角がないか**を見ます。", "使えない角")
in_text("## $\\cos^{2}\\theta$ を $\\cos(\\theta^{2})$ と読む", "記法の注意")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 は電卓がないので、この確かめ方はできません。**",
        "Paper 1 では手で解くと明記")
in_text("$1$ から離れたら、どちらかの値がまちがっているか、途中で丸めすぎています。",
        "自分の値で確かめる")
in_text("**$\\theta$ そのものを入れて $\\cos^{2}\\theta+\\sin^{2}\\theta$ を計算しても、"
        "確かめにはなりません。**", "恒等式では確かめにならない")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 6,
    f"model-answer が 6: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl36-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk(TEXT.count("::: {.callout-warning}") == 7, "Common errors 6 + 本文の注意 1 で 7")
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
    _b = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _b), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl36", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _tgt in ["aasl-3-4", "aasl-3-5a", "aasl-3-5b"]:
    _TT = open(os.path.join(BASE, _tgt + ".qmd"), encoding="utf-8").read()
    for _a2 in set(re.findall(r"\]\(" + _tgt + r"\.qmd#([a-z0-9-]+)\)", TEXT)):
        chk(("{#" + _a2 + "}") in _TT, _tgt + " 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl36-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl36-which", "eq-aasl36-pyth", "eq-aasl36-move",
             "eq-aasl36-sin2", "eq-aasl36-cos2"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
for _lab in ["tbl-aasl36-which", "eq-aasl36-pyth", "eq-aasl36-move",
             "eq-aasl36-sin2", "eq-aasl36-cos2"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-3-6-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-6-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) The Pythagorean identity", "図(a) の題")
in_fig("the hypotenuse is the radius, so it is $1$", "図(a) の説明")
in_fig("$\\\\cos^{2}\\\\theta + \\\\sin^{2}\\\\theta = 1$ for every ", "図(a) の式")
in_fig("(b) Three forms of $\\\\cos 2\\\\theta$", "図(b) の題")
in_fig("the same value, written three ways", "図(b) の説明")
in_fig("put $\\\\sin^{2}\\\\theta = 1 - \\\\cos^{2}\\\\theta$", "図(b) の入れかえ 1")
in_fig("put $\\\\cos^{2}\\\\theta = 1 - \\\\sin^{2}\\\\theta$", "図(b) の入れかえ 2")
in_fig("$2\\\\cos^{2}\\\\theta - 1$", "図(b) の 2 つ目の形")
in_fig("$1 - 2\\\\sin^{2}\\\\theta$", "図(b) の 3 つ目の形")
in_text("(a) When $\\theta$ is not on an axis, the point on the unit circle at angle "
        "$\\theta$ gives a right-angled triangle with legs $|\\cos\\theta|$ and "
        "$|\\sin\\theta|$", "キャプションが (a) を説明")
in_text("(b) The three forms of $\\cos 2\\theta$ are obtained from one another",
        "キャプションが (b) を説明")
chk(set(re.findall(r"\d+", FIGSTR)) <= {"1", "2"},
    f"図の数字は 1 と 2 だけ: {set(re.findall(chr(92) + 'd+', FIGSTR))}")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-6.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-5b.qmd") < DRAFT.index("aasl-3-6.qmd"), "並びが 3.5b → 3.6")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-6.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| identity |", "| Pythagorean identity |", "| double angle |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 見分けの試し値を π/6 にした -----------------------------------------
in_text("$\\theta = \\dfrac{\\pi}{6}$ を入れて確かめる習慣をつけて", "試し値は π/6")
in_text("**$\\theta = 0$ でも、この符号のまちがいは見つかります。** 正しい $2$ つの形は"
        "どちらも $1$ を返しますが、$2\\sin^{2}\\theta - 1$ や $1 - 2\\cos^{2}\\theta$ は "
        "$-1$ を返すからです。", "θ = 0 でも符号の誤りは見つかる")
not_in_text("**$\\theta = 0$ ではどの形も $1$ を返してしまう**ので、確かめになりません。",
            "古い（誤った）θ = 0 の説明は戻っていない")
in_text("$\\theta = \\dfrac{\\pi}{6}$ を入れると、どちらも $\\dfrac{1}{2}$ になるはずです。",
        "Common errors も π/6")
eq(1 - 2 * sp.sin(PI / 6) ** 2, R(1, 2), "π/6 で 1 - 2sin² = 1/2")
eq(2 * sp.cos(PI / 6) ** 2 - 1, R(1, 2), "π/6 で 2cos² - 1 = 1/2")
eq(sp.cos(PI / 3), R(1, 2), "cos(π/3) = 1/2")
# 取りちがえた形は -1/2 を返す
eq(1 - 2 * sp.cos(PI / 6) ** 2, R(-1, 2), "取りちがえ 1 - 2cos² は -1/2")
eq(2 * sp.sin(PI / 6) ** 2 - 1, R(-1, 2), "取りちがえ 2sin² - 1 は -1/2")
# θ = 0 では見分けられない
for _f in [1 - 2 * sp.sin(TH) ** 2, 2 * sp.cos(TH) ** 2 - 1,
           1 - 2 * sp.sin(TH), 2 * sp.cos(TH) - 1]:
    chk(sp.simplify(_f.subs(TH, 0)) == 1, "θ = 0 ではまちがった形も 1 を返す")

# --- 象限が与えられるかどうかの言い方 ------------------------------------
in_text("**問題文はふつう象限や範囲を与えます**", "ふつう与える")
not_in_text("**問題文が象限や範囲を必ず与えています**", "「必ず」は消した")
in_text("ただし、$2$ 乗だけで決まる量（あとで出てくる $\\cos 2\\theta = 1 - 2\\sin^{2}\\theta$ "
        "など）は、象限がなくても $1$ つに決まります。", "2 乗だけで決まる量")

# --- 第 7 節が例題4 の答えを先に出さない --------------------------------
not_in_body("\\sin^{2}\\theta = \\frac{1 - \\cos 2\\theta}{2}", "例題4(a) の結果")
not_in_body("$\\\\cos\\\\theta = 0$ の角では使えません", "例題4(d) の理由")
not_in_text("{#eq-aasl36-half}", "使わないラベルは消した")
in_text("$\\sin^{2}\\theta$ や $\\cos^{2}\\theta$ を $\\cos 2\\theta$ の $1$ 次式に"
        "書きかえられます（例題 4）。", "例題 4 に送る")

# --- 2 倍角の出どころ ----------------------------------------------------
in_text("**$2$ 倍角の式そのものは、公式集に印刷されているところから出発します。** "
        "導き方は SL の範囲外なので、ここでは「$3$ つの形がなぜ同じものか」を見ます。",
        "2 倍角の出どころ")

# --- GDC の確かめを、意味のあるものにした --------------------------------
in_text("**自分が出した値**を電卓に入れて確かめます。", "自分の値で確かめる")
in_text("恒等式なので、どんな $\\theta$ でも $1$ が返ります。", "恒等式は常に 1")
in_text("$\\theta$ を出してから $\\sin(2\\theta)$ を直接計算し、自分の "
        "$2\\sin\\theta\\cos\\theta$ の値とくらべます。", "sin2θ の確かめ方")
in_text("正確な値を求める問題は電卓では答えが出せないので、恒等式は Paper 1 の道具です。",
        "Paper 1 の道具")
not_in_text("Paper 1 でよく出ます。", "食いちがう言い方は消した")

# --- 図のキャプションに絶対値と例外 --------------------------------------
in_text("with legs $|\\cos\\theta|$ and $|\\sin\\theta|$ and hypotenuse $1$",
        "キャプションに絶対値")
in_text("on the axes the coordinates are $(\\pm 1, 0)$ or $(0, \\pm 1)$ and the identity "
        "still holds.", "軸の上の場合もキャプションに")
for _a in [0, PI / 2, PI, 3 * PI / 2]:
    eq(sp.cos(_a) ** 2 + sp.sin(_a) ** 2, 1, f"軸の上でも成り立つ ({_a})")

# --- 解答例に代入の行を入れた --------------------------------------------
in_text("**(b)** $\\tan\\theta = \\dfrac{\\frac{3}{5}}{\\frac{4}{5}}$", "例題1(b) の代入")
in_text("**(b)** $\\sin 2x = 2\\left(\\dfrac{\\sqrt{7}}{4}\\right)\\left(\\dfrac{3}{4}\\right)$",
        "例題2(b) の代入")
in_text("**(b)** $\\tan\\theta = \\dfrac{-\\frac{5}{13}}{-\\frac{12}{13}}$", "例題3(b) の代入")
in_text("**(c)** $\\sin 2\\theta = 2\\left(-\\dfrac{5}{13}\\right)\\left(-\\dfrac{12}{13}\\right)$",
        "例題3(c) の代入")

# --- 例題2(d) の境目 -----------------------------------------------------
in_text("on the unit circle the $x$-coordinate is $0$ at $2x = \\dfrac{\\pi}{2}$ and "
        "negative for $\\dfrac{\\pi}{2} < 2x < \\pi$", "境目も書いた")
chk(sp.cos(PI / 2) == 0, "π/2 では x 座標は 0")
chk(R(1, 8) != 0, "例題2 では cos2x は 0 でない")

# --- 例題4(c) の解答例に約分の条件 ---------------------------------------
in_text("**(c)** $1 + \\cos 2\\theta = 2\\cos^{2}\\theta$, and $\\cos\\theta \\neq 0$, so",
        "例題4(c) の条件")
in_text("= \\frac{\\sin\\theta}{\\cos\\theta} = \\tan\\theta$$", "約分の途中も書いた")

# --- 演習3 を 2 つの部分にした -------------------------------------------
in_text("**(b)** [If no quadrant is given, find the possible values of "
        "$\\tan\\theta$.]{.q-en}", "演習3(b) は 2 つの値")
in_text("$$\\tan\\theta = \\pm\\frac{\\sqrt{2}}{4}$$", "演習3(b) の答え")
in_text("$\\sin\\theta$ が正なので $\\theta$ は第 $1$ 象限か第 $2$ 象限で、第 $1$ 象限なら "
        "$\\tan\\theta$ は正、第 $2$ 象限なら負です。", "演習3(b) の解説")
eq(R(1, 3) / (-2 * sp.sqrt(2) / 3), -sp.sqrt(2) / 4, "第 2 象限なら tan は -√2/4")
chk(sp.tan(PI - sp.asin(R(1, 3))) < 0, "第 2 象限で tan は負")
eq(sp.simplify(sp.tan(PI - sp.asin(R(1, 3)))), -sp.sqrt(2) / 4, "第 2 象限の値")
eq(sp.simplify(sp.tan(sp.asin(R(1, 3)))), sp.sqrt(2) / 4, "第 1 象限の値")

# --- 演習5 に大きさの検算を足した ----------------------------------------
in_text("**検算（大きさで）。** $\\sin\\theta = 0.25$ は小さいので、$\\theta$ も $2\\theta$ も "
        "$0$ に近く、$\\cos 2\\theta$ は $1$ に近いはずです。", "演習5 の大きさの検算")
chk(R(7, 8) > R(1, 2), "7/8 は 1 に近い")

# --- 演習8 に -1 < k < 1 の条件を付けた ----------------------------------
in_text("[It is given that $\\sin\\theta = k$, where $-1 < k < 1$.", "演習8 の条件")
in_text("*$\\cos 2\\theta = 1 - 2k^{2}$ uses only $k^{2}$, but $\\cos\\theta = "
        "\\pm\\sqrt{1 - k^{2}}$ is non-zero and needs the quadrant to fix the sign.*",
        "演習8 の解答例")
in_text("for $-1 < \\sin\\theta < 1$ the two signs occur for different quadrants",
        "model answer にも条件")
# k = ±1 では cos θ が 1 つに決まる（条件が要る理由）
eq(sp.cos(PI / 2), 0, "sinθ = 1 なら cosθ = 0")
chk(sp.sqrt(1 - 1) == 0, "k = 1 では ± が消える")
for _k in [R(1, 2), R(-1, 3), R(3, 5)]:
    chk(sp.sqrt(1 - _k ** 2) != 0, f"-1 < k < 1 なら cosθ は 0 でない ({_k})")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
