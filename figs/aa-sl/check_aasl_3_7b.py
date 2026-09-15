"""AA SL 3.7b（三角関数のグラフの変換と、実際の場面）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_7b.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-7b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_7b.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
PI = sp.pi
X = sp.Symbol("x", real=True)
T = sp.Symbol("t", real=True)


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


def amp(a):
    return abs(a)


def per(b, tan_=False):
    return (PI if tan_ else 2 * PI) / abs(b)


def maxmin(a, d):
    return d + abs(a), d - abs(a)


# ══════════════════════════════════════════════════════════
# 0. 一般の形
# ══════════════════════════════════════════════════════════
_a, _b, _c, _d = sp.symbols("a_ b_ c_ d_", real=True)
_f = _a * sp.sin(_b * (X + _c)) + _d
# period の一般則
for _bv in [1, 2, 3, R(1, 2), -2, PI / 6]:
    eq(sp.periodicity(sp.sin(_bv * X), X), 2 * PI / abs(_bv), f"period ({_bv})")
    eq(sp.periodicity(sp.tan(_bv * X), X), PI / abs(_bv), f"tan の period ({_bv})")
# amplitude と最大・最小
for _av, _dv in [(2, 1), (-3, 0), (4, -1), (8, 10), (2, 5)]:
    _hi, _lo = maxmin(_av, _dv)
    eq(sp.maximum(_av * sp.sin(X) + _dv, X), _hi, f"最大 ({_av},{_dv})")
    eq(sp.minimum(_av * sp.sin(X) + _dv, X), _lo, f"最小 ({_av},{_dv})")
    eq(R(1, 2) * (_hi + _lo), _dv, f"midline ({_av},{_dv})")
    eq(R(1, 2) * (_hi - _lo), abs(_av), f"amplitude ({_av},{_dv})")
# c のくくり出し
eq(sp.sin(2 * X + PI), sp.sin(2 * (X + PI / 2)), "sin(2x+π) = sin(2(x+π/2))")
eq(2 * (X + PI / 2), 2 * X + PI, "くくり出しの確認")
in_text("\\sin(2x + \\pi) = \\sin\\bigl(2(x + \\tfrac{\\pi}{2})\\bigr)", "本文のくくり出し")
in_text("**左へ $\\pi$ ではなく、左へ $\\dfrac{\\pi}{2}$** です。", "左へ π/2")
# 表
in_text("| $b$ | 横の伸縮 | period $= \\dfrac{2\\pi}{\\lvert b \\rvert}$ |", "表の b の行")
in_text("| $c$ | 横の平行移動 | 左へ $c$（$c<0$ なら右へ $\\lvert c \\rvert$） |",
        "表の c の行")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  f(x) = 2cos(3(x-4)) + 1
# ══════════════════════════════════════════════════════════
_f1 = 2 * sp.cos(3 * (X - 4)) + 1
eq(amp(2), 2, "例題1(a) amplitude = 2")
eq(per(3), 2 * PI / 3, "例題1(b) period = 2π/3")
eq(sp.periodicity(_f1, X), 2 * PI / 3, "例題1(b) sympy でも 2π/3")
eq(sp.maximum(_f1, X), 3, "例題1(c) 最大 3")
eq(sp.minimum(_f1, X), -1, "例題1(c) 最小 -1")
chk(3 < 4, "例題1(d) 最大は 4 より小さい")
eq(_f1.subs(X, 4), 3, "例題1(d) 検算 f(4) = 3")
eq(3 * (2 * PI / 3), 2 * PI, "例題1(b) 検算 中身は 2π 増える")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  y = 3 sin 2x
# ══════════════════════════════════════════════════════════
_f2 = 3 * sp.sin(2 * X)
eq(amp(3), 3, "例題2(b) amplitude = 3")
eq(per(2), PI, "例題2(c) period = π")
eq(sp.periodicity(_f2, X), PI, "例題2(c) sympy でも π")
eq(sp.maximum(_f2, X), 3, "例題2 最大 3")
# 零点の間隔
_z2 = [v for v in [R(k, 4) * PI for k in range(0, 9)]
       if 0 <= v <= 2 * PI and sp.simplify(_f2.subs(X, v)) == 0]
chk(_z2 == [0, PI / 2, PI, 3 * PI / 2, 2 * PI], f"例題2(d) 零点は π/2 ごと: {_z2}")
eq(_z2[1] - _z2[0], PI / 2, "例題2(d) 間隔は π/2")
eq(PI / 2, PI / 2, "例題2(d) もとの π の半分")
# 山の点
eq(_f2.subs(X, PI / 4), 3, "例題2 検算 (π/4, 3)")
eq(sp.sin(PI / 2), 1, "例題2 検算 sin(π/2) = 1")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  g(x) = tan(x - π/4)
# ══════════════════════════════════════════════════════════
_g = sp.tan(X - PI / 4)
eq(sp.periodicity(_g, X), PI, "例題3(b) period = π")
_as3 = [v for v in [R(k, 4) * PI for k in range(0, 9)]
        if 0 <= v <= 2 * PI and sp.cos(v - PI / 4) == 0]
chk(_as3 == [3 * PI / 4, 7 * PI / 4], f"例題3(c) 漸近線は 3π/4, 7π/4: {_as3}")
eq(PI / 2 + PI / 4, 3 * PI / 4, "例題3(c) 3π/4")
eq(3 * PI / 4 + PI, 7 * PI / 4, "例題3(c) 7π/4")
chk(float(11 * PI / 4) > float(2 * PI), "例題3(c) 次は範囲外")
eq(_g.subs(X, PI / 4), 0, "例題3(d) x = π/4 で 0")
eq(7 * PI / 4 - 3 * PI / 4, PI, "例題3(c) 検算 間隔は period")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  D(t) = 2 sin(πt/6) + 5
# ══════════════════════════════════════════════════════════
_D = 2 * sp.sin(PI * T / 6) + 5
eq(sp.maximum(_D, T), 7, "例題4(a) 最大 7")
eq(sp.minimum(_D, T), 3, "例題4(d) 最小 3")
eq(per(PI / 6), 12, "例題4(b) period = 12")
eq(sp.periodicity(_D, T), 12, "例題4(b) sympy でも 12")
eq(_D.subs(T, 2), sp.sqrt(3) + 5, "例題4(c) D(2) = √3 + 5")
eq(PI * 2 / 6, PI / 3, "例題4(c) 中身は π/3")
eq(sp.sin(PI / 3), sp.sqrt(3) / 2, "例題4(c) sin(π/3)")
chk(abs(float(sp.sqrt(3) + 5) - 6.73) < 0.01, "例題4(c) 検算 約 6.73")
chk(3 < float(sp.sqrt(3) + 5) < 7, "例題4(c) 検算 3 と 7 のあいだ")
eq(R(24, 12), 2, "例題4(b) 検算 1 日に 2 回")
eq(_D.subs(T, 9), 3, "例題4(d) 検算 t = 9 で 3")
eq(PI * 9 / 6, 3 * PI / 2, "例題4(d) 検算 中身は 3π/2")
eq(_D.subs(T, 3), 7, "例題4 検算 t = 3 で最大")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(amp(3), 3, "演習1 amplitude = 3")
eq(sp.maximum(3 * sp.sin(X), X), 3, "演習1 検算 最大 3")
eq(sp.minimum(3 * sp.sin(X), X), -3, "演習1 検算 最小 -3")
eq(per(4), PI / 2, "演習2 period = π/2")
eq(sp.periodicity(sp.cos(4 * X), X), PI / 2, "演習2 sympy でも π/2")
eq(4 * (PI / 2), 2 * PI, "演習2 検算 中身は 2π")
eq(sp.sin(PI / 3 - PI / 3), 0, "演習3 検算 (π/3, 0) を通る")
in_text("*A translation of $\\dfrac{\\pi}{3}$ to the right", "演習3 は右へ π/3")
_hi4, _lo4 = maxmin(1, 2)
eq(_hi4, 3, "演習4 最大 3")
eq(_lo4, 1, "演習4 最小 1")
eq(R(_hi4 + _lo4, 2), 2, "演習4 検算 midline は 2")
_f5 = 4 * sp.cos(2 * X) - 1
eq(amp(4), 4, "演習5 amplitude = 4")
eq(per(2), PI, "演習5 period = π")
eq(sp.maximum(_f5, X), 3, "演習5 最大 3")
eq(sp.minimum(_f5, X), -5, "演習5 最小 -5")
eq(R(3 + (-5), 2), -1, "演習5 検算 midline は -1")
eq(R(3 - (-5), 2), 4, "演習5 検算 amplitude は 4")
eq(sp.periodicity(2 * sp.tan(X), X), PI, "演習6 period = π")
eq(2 * sp.tan(0), 0, "演習6 検算 2tan0 = 0")
eq(2 * sp.tan(PI), 0, "演習6 検算 2tanπ = 0")
chk(sp.maximum(sp.tan(X), X) == sp.oo, "演習6 tan に最大値はない")
_h7 = 8 * sp.sin(PI * T / 5) + 10
eq(sp.maximum(_h7, T), 18, "演習7 最大 18")
eq(per(PI / 5), 10, "演習7 period = 10")
eq(sp.periodicity(_h7, T), 10, "演習7 sympy でも 10")
eq(sp.minimum(_h7, T), 2, "演習7 検算 最小 2")
eq(18 - 2, 16, "演習7 検算 直径 16")
eq(sp.maximum(-3 * sp.sin(X), X), 3, "演習8 a = -3 でも最大 3")
eq(sp.minimum(-3 * sp.sin(X), X), -3, "演習8 a = -3 でも最小 -3")
eq(R(3 - (-3), 2), 3, "演習8 amplitude は 3（-3 ではない）")
chk(-3 != 3, "演習8 a と |a| はちがう")
eq(sp.cos(X + PI / 2), -sp.sin(X), "演習9 cos(x+π/2) = -sin x")
eq(sp.sin(X + PI), -sp.sin(X), "演習9 sin(x+π) = -sin x")
eq(sp.cos(PI / 2), 0, "演習9 検算 x = 0")
eq(sp.cos(PI), -1, "演習9 検算 x = π/2")
eq(sp.periodicity(sp.sin(2 * X), X), PI, "演習10 period = π")
chk(sp.simplify(sp.sin(2 * PI) - sp.sin(0)) == 0, "演習10 検算 π 離れて一致")
chk(PI != 4 * PI, "演習10 生徒の 4π は誤り")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("2\\cos\\bigl(3(x - 4)\\bigr)", "例題1"),
                ("\\frac{2\\pi}{3}", "例題1(b)"),
                ("\\tan\\left(x - \\dfrac{\\pi}{4}\\right)", "例題3"),
                ("\\frac{3\\pi}{4}", "例題3(c)"),
                ("\\frac{\\pi t}{6}", "例題4"), ("\\sqrt{3} + 5", "例題4(c)"),
                ("\\cos 4x", "演習2"), ("\\frac{\\pi}{2}$$", "演習2"),
                ("4\\cos 2x", "演習5"), ("\\frac{\\pi t}{5}", "演習7"),
                ("2\\tan x", "演習6"), ("-\\sin x", "演習9")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
# ★ SL 3.7 に対応する公式集の欄はない
chk("::: {.callout-important}" not in TEXT, "公式集の callout は置かない（3.7 は欄がない）")
chk(TEXT.count("\n> ") == 0, f"引用は置かない: {TEXT.count(chr(10) + '> ')}")
not_in_text("Composite functions of the form", "シラバス本文は引かない")
not_in_text("Real-life contexts", "シラバス本文は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## $\\tan$ では $\\dfrac{\\pi}{\\lvert b \\rvert}$ です", "tan の period の注意")
in_text("**そのまま $\\tan$ に使わないでください。**", "tan には使わない")
in_text("**絶対値が付くのは、$a$ が負のこともあるからです。**", "絶対値の理由")
in_text("**$b$ でくくってから読みます。**", "くくってから")
in_text("$b < 0$ のときは、$x$ が増えると中身は**減ります**。中身が $2\\pi$ 減っても"
        "もとにもどるので $bp = -2\\pi$", "b が負のとき")
in_text("**時間には範囲があります。**", "時間の範囲")
in_text("**$t$ の単位**（時間・分）と **$h$ の単位**（m など）を、答えに必ず書きます",
        "単位を書く")
in_text("## $b$ が大きいと period も大きいと思う", "period の注意")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("**下限と上限を指定する**ところまでが操作です。", "下限と上限")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 8,
    f"model-answer が 8: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl37b-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl37b", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _tgt, _dir in [("aasl-3-5a", BASE), ("aasl-3-5b", BASE), ("aasl-3-7a", BASE),
                   ("aasl-2-11", os.path.join(ROOT, "aa-sl", "02-functions"))]:
    _TT = open(os.path.join(_dir, _tgt + ".qmd"), encoding="utf-8").read()
    for _a2 in set(re.findall(r"\]\((?:\.\./02-functions/)?" + _tgt
                              + r"\.qmd#([a-z0-9-]+)\)", TEXT)):
        chk(("{#" + _a2 + "}") in _TT, _tgt + " 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl37b-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl37b-four", "eq-aasl37b-form", "eq-aasl37b-amp",
             "eq-aasl37b-period", "eq-aasl37b-maxmin", "eq-aasl37b-back"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
for _lab in ["tbl-aasl37b-four", "eq-aasl37b-amp", "eq-aasl37b-period",
             "eq-aasl37b-maxmin", "eq-aasl37b-back"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-3-7b-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-7b-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) A stretch in each direction", "図(a) の題")
in_fig("the same shape, stretched in one direction and squeezed in ", "図(a) の説明")
chk("factor of $3$" not in FIG, "図に倍率は書かない")
in_fig("(b) Where $a$, $b$, $c$ and $d$ show up", "図(b) の題")
in_fig("highest value $d + |a|$, lowest value $d - |a|$", "図(b) の最大・最小")
in_fig("one period $= \\\\frac{2\\\\pi}{|b|}$", "図(b) の period")
in_fig("midline $y = d$", "図(b) の midline")
in_fig("shift by $c$", "図(b) の平行移動")
in_fig("the midline is halfway between the highest and the ", "図(b) の説明")
in_text("(a) The graphs of $y = \\sin x$ and $y = 3\\sin 2x$ have the same shape, "
        "stretched in one direction and squeezed in the other.",
        "キャプションが (a) を説明")
in_text("(b) For $y = a\\sin(b(x+c)) + d$ the number $|a|$ is the amplitude",
        "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-7b.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-7a.qmd") < DRAFT.index("aasl-3-7b.qmd"), "並びが 3.7a → 3.7b")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-7b.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| midline |", "| stretch |", "| translation |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- |a| 倍・|b| が大きいほど -------------------------------------------
in_text("上下の振れ幅は $\\lvert a \\rvert$ 倍です。", "振れ幅は |a| 倍")
not_in_text("上下の振れ幅も $a$ 倍です。", "a 倍という言い方は消した")
in_text("**$\\lvert b \\rvert$ が大きいほど period は小さくなります。**", "|b| が大きいほど")
in_text("$\\lvert b \\rvert$ が大きいほど**縮みます**", "Common errors も |b|")
in_text("$bx$ が $2\\pi$ だけ変わるのに必要な $x$ の幅が period", "だけ変わる")
# 反例：b = -1 と b = -5 では、大きいほうが period も大きい
chk(sp.periodicity(sp.sin(-1 * X), X) > sp.periodicity(sp.sin(-5 * X), X),
    "b = -1 のほうが b = -5 より period が大きい")
chk(-1 > -5, "b としては -1 のほうが大きい")
eq(sp.periodicity(sp.sin(-2 * X), X), PI, "b = -2 でも period は π")

# --- period の導出を b < 0 まで ------------------------------------------
in_text("$b > 0$ のときは、中身が $2\\pi$ 増えればもとにもどるので", "b > 0 の場合")
in_text("**どちらの場合も $\\dfrac{2\\pi}{\\lvert b \\rvert}$ にまとまります。**", "まとめ")
eq(-2 * PI / (-2), PI, "b = -2 なら p = π")

# --- 公式集にないこと、度、電卓の返す形 ----------------------------------
in_text("**この項目は公式集にありません。** amplitude と period の式は印刷されていないので、"
        "覚える必要があります。", "公式集にない")
in_text("**角が度で与えられているときは $\\dfrac{360°}{\\lvert b \\rvert}$ です**", "度のとき")
in_text("**電卓や表計算ソフトの回帰は、$a\\sin(bx+c)+d$ の形で返すことがあります。**",
        "電卓の返す形")
eq(R(360, 2), 180, "度でも b で割る")

# --- 例題2 の答えを本文から落とした --------------------------------------
not_in_body("**縦に $3$ 倍**", "縦の倍率は本文から落とした")
not_in_body("stretch factor", "stretch factor は使わない")
in_text("$2$ つのちがいの読み取りは、例題 2 でやります。", "例題 2 に送る")
chk(TEXT.count("stretch factor") == 0, "stretch factor は使わない")
chk(TEXT.count("scale factor") >= 3, f"scale factor を使う: {TEXT.count('scale factor')}")
in_text("- $y$ 方向に **scale factor $3$** の拡大（$a = 3$）", "例題2(a) の 1 つ目")
in_text("- $x$ 方向に **scale factor $\\dfrac{1}{2}$** の縮小（$b = 2$）", "例題2(a) の 2 つ目")

# --- 順番のこと ----------------------------------------------------------
in_text("ただし、**変換として述べる**ときは順番が効きます。", "順番が効く")
in_text("ここで読み取っている amplitude・period・midline は、順番によりません。",
        "読み取りは順番によらない")

# --- b と c の出し方 -----------------------------------------------------
in_text("逆に period が分かれば $\\lvert b \\rvert = \\dfrac{2\\pi}{\\text{period}}$ で $b$ が"
        "出ます", "period から b")
in_text("**ここでは $a > 0$、$b > 0$ に選びます。** そうすると、"
        "$t = t_{0}$ で最大になるのは、$\\sin$ の中身がそこで "
        "$\\dfrac{\\pi}{2}$ になるときです", "M04 c の決め方")
in_text("**$\\tan$ には amplitude も最大・最小もありません。**",
        "M04 tan に amplitude はない")
in_text("**$\\sin$・$\\cos$ の場合**：$a$ から amplitude",
        "M04 手順に sin・cos の断り")
in_text("**係数が負のときは、拡大・縮小に加えて折り返しが入ります。**",
        "M04 負の係数の折り返し")
in_text("**横の移動は「左へ $c$」**です（座標の変化は $-c$）",
        "M04 横の移動の向き")
in_text("$a \\ne 0$、$b \\ne 0$", "M04 定数でない三角関数の条件")
in_text("たとえば $-4\\sin t + 1$ は、$\\sin t = 1$ となる "
        "$t = \\dfrac{\\pi}{2}$ で**最小** $-3$", "M04 負の a の例")
# -4 sin t + 1 は t = π/2 で最小 -3、t = 3π/2 で最大 5
chk(-4 * sp.sin(sp.pi / 2) + 1 == -3, "M04 t=π/2 で -3")
chk(-4 * sp.sin(3 * sp.pi / 2) + 1 == 5, "M04 t=3π/2 で 5")
eq(2 * PI / 4, PI / 2, "period 4 なら b = π/2")

# --- 例題3 の検算を独立させた --------------------------------------------
in_text("**検算（(b) について）。** **値でためします。**", "例題3(b) の検算")
eq(sp.tan(0 - PI / 4), -1, "g(0) = -1")
eq(sp.tan(PI - PI / 4), -1, "g(π) = -1")
eq(sp.tan(PI / 2 - PI / 4), 1, "g(π/2) = 1")
not_in_text("**$2\\pi/\\lvert b \\rvert$ を使っていないか見ます。**", "規則の言い直しは消した")

# --- 例題4(b) の単位 -----------------------------------------------------
in_text("= 12 \\text{ hours}", "例題4(b) の単位")

# --- 演習1：負の a -------------------------------------------------------
in_text("[Write down the amplitude, the maximum value and the minimum value of "
        "$y = -4\\sin x + 1$.]{.q-en}", "演習1 は負の a")
eq(sp.maximum(-4 * sp.sin(X) + 1, X), 5, "演習1 最大 5")
eq(sp.minimum(-4 * sp.sin(X) + 1, X), -3, "演習1 最小 -3")
eq(R(5 - (-3), 2), 4, "演習1 amplitude 4")
in_text("**負の符号は amplitude には入りません。**", "負号は入らない")
not_in_text("[Write down the amplitude of $y = 3\\sin x$.]", "古い演習1 は消した")

# --- 演習4：くくり出し ---------------------------------------------------
in_text("[Write $y = \\sin(3x + \\pi)$ in the form $y = \\sin\\bigl(b(x+c)\\bigr)$",
        "演習4 はくくり出し")
eq(sp.sin(3 * X + PI), sp.sin(3 * (X + PI / 3)), "3x+π = 3(x+π/3)")
eq(3 * (X + PI / 3), 3 * X + PI, "展開して戻る")
in_text("*A translation of $\\dfrac{\\pi}{3}$ to the left (in the negative $x$-direction).*",
        "演習4 は左へ π/3")
not_in_text("[Write down the maximum value and the minimum value of $y = \\sin x + 2$.]",
            "古い演習4 は消した")

# --- 演習5：midline も ---------------------------------------------------
in_text("the equation of the midline, the maximum value and the minimum value of $f$",
        "演習5 に midline")
in_text("$$\\text{midline: } y = -1$$", "演習5 の midline")

# --- 演習6 の model answer -----------------------------------------------
in_text("just below each asymptote it takes arbitrarily large positive values, and just "
        "above the next one it takes arbitrarily large negative values", "両側の説明")
not_in_text("since it increases without bound near each asymptote, and multiplying by $2$",
            "片側だけの説明は消した")
eq(2 * sp.tan(PI / 4), 2, "2tan(π/4) = 2")
eq(2 * sp.tan(5 * PI / 4), 2, "2tan(5π/4) = 2")

# --- 演習7：b を出す部分 -------------------------------------------------
in_text("**(b)** [A second wheel takes $4$ minutes for one complete turn. Find the value "
        "of $b$ for that wheel.]{.q-en}", "演習7(b)")
in_text("**(b)** $\\dfrac{2\\pi}{b} = 4$", "演習7(b) の式")
eq(2 * PI / (PI / 2), 4, "b = π/2 なら period 4")
chk(PI / 2 > PI / 5, "b が大きいほうが速い")

# --- 演習10 の検算 -------------------------------------------------------
in_text("**中身に入れて確かめます。**", "演習10 の検算")
in_text("$2$ 点だけで確かめると、零点は半周期ごとに来るので見分けがつきません。",
        "零点は半周期ごと")
eq(sp.sin(2 * (X + PI)), sp.sin(2 * X), "sin(2(x+π)) = sin2x")
# 零点だけでは period を決められない（sin x の零点も π ごと）
chk(sp.periodicity(sp.sin(X), X) == 2 * PI, "sin x の period は 2π")
eq(sp.sin(PI), 0, "sin x の零点も π ごと")
eq(sp.sin(2 * PI), 0, "sin x の零点も π ごと（2）")


# ══════════════════════════════════════════════════════════
# C01c  2.11 の「$f(ax+b)$ は扱わない」との関係
# ══════════════════════════════════════════════════════════
in_text("## [SL 2.11](../02-functions/aasl-2-11.qmd#composite) の"
        "「$f(ax+b)$ は扱わない」との関係", "C01c 3.7b の折り畳み")
in_text("**矛盾ではありません。**", "C01c 矛盾ではない")
in_text("だから、この節では**先にくくる**のです。", "C01c 先にくくる")


# ══════════════════════════════════════════════════════════
# E06  演習2 — 条件からモデルを作る
# ══════════════════════════════════════════════════════════
in_text("[The depth of water in a harbour is modelled by "
        "$D(t) = a\\sin\\bigl(b(t+c)\\bigr) + d$", "E06 演習2 はモデル作り")
in_text("港の水深が $D(t) = a\\sin\\bigl(b(t+c)\\bigr) + d$ でモデル化されて"
        "います。", "E06 演習2 の訳")
in_text("$$D(t) = 3\\sin\\left(\\frac{\\pi t}{6}\\right) + 5$$", "E06 sin の答え")
in_text("$$D(t) = 3\\cos\\left(\\frac{\\pi}{6}(t-3)\\right) + 5$$",
        "E06 cos の答え")
in_text("**答えが $1$ つに決まらない**問題なので、", "E06 一意でない")
in_text("Take $a > 0$ and $b > 0$.]", "E06 a>0, b>0 を指定")
# 最大 8・最小 2・period 12・t=3 で最大 → 3 sin(πt/6) + 5
_t = sp.Symbol("t")
_D = 3 * sp.sin(PI * _t / 6) + 5
chk(sp.Rational(8 - 2, 2) == 3 and sp.Rational(8 + 2, 2) == 5,
    "E06 a = 3, d = 5")
chk(sp.simplify(2 * PI / (PI / 6) - 12) == 0, "E06 period は 12")
chk(_D.subs(_t, 3) == 8, "E06 t=3 で最大 8")
chk(_D.subs(_t, 9) == 2, "E06 t=9 で最小 2")
chk(sp.periodicity(_D, _t) == 12, "E06 sympy でも period 12")
_C = 3 * sp.cos(PI * (_t - 3) / 6) + 5
chk(sp.simplify(_D - _C) == 0, "E06 cos の形も同じ関数")
chk(_C.subs(_t, 3) == 8, "E06 cos の形も t=3 で最大")
chk(_D.subs(_t, 0) == 5 and _C.subs(_t, 0) == 5, "E06 t=0 ではどちらも 5")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
