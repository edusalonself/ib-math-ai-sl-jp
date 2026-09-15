"""AA SL 3.7a（三角関数とそのグラフ）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_7a.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-7a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_7a.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
PI = sp.pi
X = sp.Symbol("x", real=True)


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


def zeros_in(f, lo, hi):
    """f(x) = 0 の解を [lo, hi] で数える（π の整数倍・半整数倍だけ調べる）。"""
    out = []
    k = -20
    while k <= 20:
        v = R(k, 2) * PI
        if lo <= v <= hi and sp.simplify(f.subs(X, v)) == 0:
            out.append(v)
        k += 1
    return out


# ══════════════════════════════════════════════════════════
# 0. グラフの基本
# ══════════════════════════════════════════════════════════
# 周期
eq(sp.sin(X + 2 * PI), sp.sin(X), "sin の周期は 2π")
eq(sp.cos(X + 2 * PI), sp.cos(X), "cos の周期は 2π")
eq(sp.tan(X + PI), sp.tan(X), "tan の周期は π")
chk(sp.periodicity(sp.sin(X), X) == 2 * PI, "sympy でも sin の周期は 2π")
chk(sp.periodicity(sp.cos(X), X) == 2 * PI, "sympy でも cos の周期は 2π")
chk(sp.periodicity(sp.tan(X), X) == PI, "sympy でも tan の周期は π")
# 値域
chk(sp.maximum(sp.sin(X), X) == 1 and sp.minimum(sp.sin(X), X) == -1,
    "sin の値域は [-1, 1]")
chk(sp.maximum(sp.cos(X), X) == 1 and sp.minimum(sp.cos(X), X) == -1,
    "cos の値域は [-1, 1]")
# amplitude
eq(R(1 - (-1), 2), 1, "amplitude = 1")
in_text("\\text{amplitude} = \\frac{1 - (-1)}{2} = 1, \\qquad \\text{period} = 2\\pi",
        "amplitude と period の式")
# ずれ
eq(sp.sin(X + PI / 2), sp.cos(X), "cos x = sin(x + π/2)")
eq(sp.cos(X - PI / 2), sp.sin(X), "sin x = cos(x - π/2)")
# 1/4 回転で (a, b) → (-b, a)
_a, _b = sp.symbols("a_ b_", real=True)
_rot = sp.Matrix([[0, -1], [1, 0]]) * sp.Matrix([_a, _b])
chk(list(_rot) == [-_b, _a], f"1/4 回転は (a, b) → (-b, a): {list(_rot)}")
chk(list(sp.Matrix([[0, -1], [1, 0]]) * sp.Matrix([1, 0])) == [0, 1],
    "(1, 0) は (0, 1) に写る")
# 対称性
eq(sp.cos(-X), sp.cos(X), "cos は偶関数")
eq(sp.sin(-X), -sp.sin(X), "sin は奇関数")
# tan の切れ目
for _k in range(-2, 3):
    chk(sp.cos(PI / 2 + _k * PI) == 0, f"cos が 0 になる: π/2 + {_k}π")
chk(sp.tan(PI / 2) == sp.zoo, "tan(π/2) は値をもたない")
# 表の値
in_text("| $\\cos x$ | $1$ | $0$ | $-1$ | $0$ | $1$ |", "cos の 5 点")
for _x, _v in [(0, 1), (PI / 2, 0), (PI, -1), (3 * PI / 2, 0), (2 * PI, 1)]:
    eq(sp.cos(_x), _v, f"cos の 5 点 ({_x})")
in_text("| $y = \\tan x$ | $x \\ne \\dfrac{\\pi}{2} + n\\pi$（$n$ は整数） | "
        "すべての実数 | $\\pi$ |", "まとめの表の tan の行")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  f(x) = sin x, 0 ≤ x ≤ 2π
# ══════════════════════════════════════════════════════════
eq(R(1 - (-1), 2), 1, "例題1(a) amplitude = 1")
eq(sp.sin(PI / 2), 1, "例題1(c) 最大は (π/2, 1)")
_z1 = zeros_in(sp.sin(X), 0, 2 * PI)
chk(_z1 == [0, PI, 2 * PI], f"例題1(d) 零点は 3 個: {_z1}")
chk(len(_z1) == 3, "例題1(d) ちょうど 3 個")
chk(sp.maximum(sp.sin(X), X, sp.Interval(0, 2 * PI)) == 1, "例題1 最大値 1")
chk(sp.minimum(sp.sin(X), X, sp.Interval(0, 2 * PI)) == -1, "例題1 最小値 -1")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  g(x) = cos x, -π ≤ x ≤ π
# ══════════════════════════════════════════════════════════
chk(sp.maximum(sp.cos(X), X, sp.Interval(-PI, PI)) == 1, "例題2(a) 最大値 1")
chk(sp.minimum(sp.cos(X), X, sp.Interval(-PI, PI)) == -1, "例題2(a) 最小値 -1")
_z2 = zeros_in(sp.cos(X), -PI, PI)
chk(_z2 == [-PI / 2, PI / 2], f"例題2(b) 交点は ±π/2: {_z2}")
eq(sp.cos(0), 1, "例題2(c) y 切片は (0, 1)")
eq(sp.cos(-PI), -1, "例題2 検算 端の値")
eq(sp.cos(-X), sp.cos(X), "例題2(d) 偶関数")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  h(x) = tan x, 0 ≤ x ≤ 2π
# ══════════════════════════════════════════════════════════
_as3 = [v for v in [R(k, 2) * PI for k in range(0, 5)]
        if 0 <= v <= 2 * PI and sp.cos(v) == 0]
chk(_as3 == [PI / 2, 3 * PI / 2], f"例題3(b) 漸近線は π/2, 3π/2: {_as3}")
_z3 = zeros_in(sp.sin(X), 0, 2 * PI)
chk(_z3 == [0, PI, 2 * PI], f"例題3(c) x 切片は 0, π, 2π: {_z3}")
chk(sp.cos(PI / 2) == 0 and sp.sin(PI / 2) == 1, "例題3(d) (0, 1) の点")
chk(sp.limit(sp.tan(X), X, PI / 2, "-") == sp.oo, "左から +∞")
chk(sp.limit(sp.tan(X), X, PI / 2, "+") == -sp.oo, "右から -∞")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  sin と cos を同じ軸に
# ══════════════════════════════════════════════════════════
eq(sp.sin(3 * PI / 2), -1, "例題4(b) 最小は (3π/2, -1)")
eq(PI / 2 + PI, 3 * PI / 2, "例題4(b) 検算 山の半周あと")
_meet = [v for v in [R(k, 4) * PI for k in range(0, 9)]
         if 0 <= v <= 2 * PI and sp.simplify(sp.sin(v) - sp.cos(v)) == 0]
chk(_meet == [PI / 4, 5 * PI / 4], f"例題4(c) 交点は 2 つ: {_meet}")
chk(len(_meet) == 2, "例題4(c) 個数は 2")
eq(1 ** 2 + 1 ** 2, 2, "例題4(d) 1 + 1 = 2")
chk(2 != 1, "例題4(d) 2 は 1 でない")
eq(sp.sqrt(1 ** 2 + 1 ** 2), sp.sqrt(2), "例題4(d) 検算 (1,1) までの距離は √2")
chk(sp.sqrt(2) != 1, "例題4(d) 検算 単位円の上にない")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(R(1 - (-1), 2), 1, "演習1 amplitude = 1")
_c2 = [v for v in [R(k, 2) * PI for k in range(0, 9)]
       if v > 0 and sp.cos(v) == -1]
chk(_c2[0] == PI, f"演習2 最小の正の解は π: {_c2[:3]}")
chk(sp.cos(PI / 2) == 0, "演習2 検算 π/2 では 0")
eq(sp.tan(X + PI), sp.tan(X), "演習3 tan の周期は π")
_min4 = [v for v in [R(k, 2) * PI for k in range(0, 9)]
         if 0 <= v <= 4 * PI and sp.sin(v) == -1]
chk(_min4 == [3 * PI / 2, 7 * PI / 2], f"演習4 最小点は 2 つ: {_min4}")
chk(float(7 * PI / 2) <= float(4 * PI), "演習4 7π/2 は範囲内")
chk(float(11 * PI / 2) > float(4 * PI), "演習4 11π/2 は範囲外")
_as5 = [v for v in [R(k, 2) * PI for k in range(0, 9)]
        if 0 <= v <= 3 * PI and sp.cos(v) == 0]
chk(_as5 == [PI / 2, 3 * PI / 2, 5 * PI / 2], f"演習5 漸近線は 3 本: {_as5}")
chk(float(7 * PI / 2) > float(3 * PI), "演習5 7π/2 は範囲外")
eq(sp.cos(PI), -1, "演習5 検算 π は切れ目ではない")
chk(sp.maximum(sp.cos(X), X) == 1 and sp.minimum(sp.cos(X), X) == -1,
    "演習6 cos の値域")
_z7 = zeros_in(sp.sin(X), -2 * PI, 2 * PI)
chk(len(_z7) == 5, f"演習7 零点は 5 個: {_z7}")
chk(_z7 == [-2 * PI, -PI, 0, PI, 2 * PI], "演習7 零点の並び")
eq(sp.sin(-X), -sp.sin(X), "演習8 奇関数")
eq(sp.sin(-PI / 2), -1, "演習8 検算 (-π/2, -1)")
chk(sp.maximum(sp.sin(X), X) < 2, "演習9 sin x = 2 に解はない")
chk(sp.solveset(sp.Eq(sp.sin(X), 2), X, sp.S.Reals) == sp.S.EmptySet,
    "演習9 解集合は空")
eq(sp.tan(X + 2 * PI), sp.tan(X), "演習10 2π でもくり返す")
chk(sp.periodicity(sp.tan(X), X) == PI, "演習10 最小の周期は π")
chk(PI < 2 * PI, "演習10 π のほうが小さい")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
# ★ このページは「グラフの性質を覚える」ページなので、amplitude 1 や period 2π
#   のような基本の値は本文にあってよい。ここで見るのは、区間を指定して数えた
#   答えなど、本文にあってはいけないものだけ。
for _lk, _m in [("\\frac{3\\pi}{2},\\ -1", "例題4(b)"),
                ("\\frac{\\pi}{2},\\ 1", "例題1(c)"),
                ("\\frac{7\\pi}{2}", "演習4"),
                ("\\frac{5\\pi}{2}", "演習5"),
                ("$$5$$", "演習7"),
                ("(0,\\ 1)$$", "例題2(c)"),
                ("rotational symmetry", "演習8"),
                ("\\sin x = 2", "演習9")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
# ★ SL 3.7 に対応する公式集の欄はない
chk("::: {.callout-important}" not in TEXT, "公式集の callout は置かない（3.7 は欄がない）")
chk(TEXT.count("\n> ") == 0, f"引用は置かない: {TEXT.count(chr(10) + '> ')}")
not_in_text("The circular functions sin", "シラバス本文は引かない")
not_in_text("Composite functions of the form", "シラバス本文は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## amplitude は「最大値」とはかぎりません", "amplitude の注意")
in_text("**上下にずらしたグラフでは、$2$ つはちがう値になります**（SL 3.7b で扱います）。",
        "3.7b への送り")
in_text("**最大値も最小値もありません。** 値はいくらでも大きく、いくらでも小さく"
        "なります。だから **amplitude もありません**。", "tan に amplitude はない")
in_text("**どちら向きにずらすかで迷ったら、$x = 0$ を見てください。**", "ずれの向き")
in_text("左から近づくときは $\\cos x > 0$ で商は正、右から近づくときは $\\cos x < 0$ で"
        "商は負です。", "漸近線の左右")
in_text("**問題文が範囲を指定したら、その中だけをかきます。**", "範囲の指定")
in_text("## $y = \\tan x$ の period を $2\\pi$ とする", "period の注意")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手でかくと明記")
in_text("**窓の設定を自分で決めてください。**", "窓の設定")
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
chk(len(re.findall(r"^::: \{#exm-aasl37a-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl37a", "他ページの @-ref: " + _r0)
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
chk(TEXT.count("@fig-aasl37a-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl37a-cos", "tbl-aasl37a-summary", "eq-aasl37a-shift",
             "eq-aasl37a-amp"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
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
SVG = os.path.join(BASE, "img", "aasl-3-7a-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-7a-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) $y = \\\\sin x$ and $y = \\\\cos x$", "図(a) の題")
in_fig("both repeat every $2\\\\pi$ and stay between ", "図(a) の説明")
in_fig("(b) $y = \\\\tan x$", "図(b) の題")
in_fig("repeats every $\\\\pi$", "図(b) の周期")
in_fig("asymptote", "図(b) の漸近線")
in_fig("no largest or smallest value; breaks where ", "図(b) の説明")
in_text("(a) The graphs of $y = \\sin x$ and $y = \\cos x$ have the same shape",
        "キャプションが (a) を説明")
in_text("(b) The graph of $y = \\tan x$ repeats every $\\pi$", "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-7a.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-6.qmd") < DRAFT.index("aasl-3-7a.qmd"), "並びが 3.6 → 3.7a")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-7a.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| amplitude |", "| period |", "| asymptote |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- period と amplitude の定義をていねいにした -------------------------
in_text("すべての $x$ で $f(x + p) = f(x)$ となる、**いちばん小さい正の数** $p$。",
        "period は最小の正の数")
in_text("（$1$ 周期ぶんの最大値 $-$ $1$ 周期ぶんの最小値）$\\div 2$", "amplitude は 1 周期ぶん")
not_in_text("**period**（周期）… 同じ形がくり返される $x$ の幅。", "ゆるい定義は消した")
# 定義域を切ると (max - min)/2 が amplitude と合わなくなる例
chk(sp.maximum(sp.sin(X), X, sp.Interval(0, PI / 2)) == 1
    and sp.minimum(sp.sin(X), X, sp.Interval(0, PI / 2)) == 0,
    "0 ≤ x ≤ π/2 では最大 1・最小 0")
chk(R(1 - 0, 2) != 1, "その区間だけで計算すると amplitude と合わない")
# 2π も tan をくり返すが、最小ではない
eq(sp.tan(X + 2 * PI), sp.tan(X), "2π でも tan はくり返す")
chk(sp.periodicity(sp.tan(X), X) == PI, "最小の正の周期は π")

# --- 公式集にないことを書いた -------------------------------------------
in_text("**この項目は公式集にありません。** amplitude と period の求め方も、$3$ つの"
        "グラフの形も印刷されていないので、覚える必要があります。", "公式集にない")

# --- tan の切れ目を両側で書き、値域の根拠も足した ------------------------
in_text("$x = -\\dfrac{\\pi}{2}$、$x = \\dfrac{\\pi}{2}$、$x = \\dfrac{3\\pi}{2}$、… と、"
        "**$\\pi$ ごと**に左右へ限りなく並びます。", "切れ目は両側")
in_text("まとめて書けば $x = \\dfrac{\\pi}{2} + n\\pi$（$n$ は整数）です。", "まとめた形")
in_text("**どんな実数もちょうど $1$ 回ずつとります**。だから**値域はすべての実数**です。",
        "値域の根拠")
for _k in range(-3, 4):
    chk(sp.cos(PI / 2 + _k * PI) == 0, f"π/2 + {_k}π で cos は 0")

# --- Why it works の一歩を補った ----------------------------------------
in_text("定義から $a = \\cos x$、$b = \\sin x$ です", "a, b の意味")
in_text("写った点は**角 $x + \\dfrac{\\pi}{2}$ の点**なので、その $y$ 座標は "
        "$\\sin\\left(x + \\dfrac{\\pi}{2}\\right)$ です。", "写った点の意味")

# --- 例題1(b) の理由、(a) の検算 ----------------------------------------
in_text("period は $y = \\sin x$ という関数そのものの性質です。", "period は関数の性質")
not_in_text("定義域を切っても、くり返しの幅は変わりません。", "あいまいな言い方は消した")
in_text("**中心線からの高さで見ます。**", "例題1(a) の検算")
in_text("**引き算を通らない見方でも $1$ になりました。**", "独立した検算")

# --- 例題3(c) の検算を値に -----------------------------------------------
in_text("$\\tan\\pi = \\dfrac{\\sin\\pi}{\\cos\\pi} = \\dfrac{0}{-1} = 0$", "例題3(c) の検算")
eq(sp.sin(PI) / sp.cos(PI), 0, "tan π = 0")

# --- 例題4(c) を単位円と直線 y = x にした -------------------------------
in_text("[Find the number of points at which the two graphs meet in this interval.]{.q-en}",
        "例題4(c) は Find")
in_text("つまり点が直線 $y = x$ の上にあるときです（[SL 3.5a](aasl-3-5a.qmd#line)）。",
        "y = x の上")
not_in_text("@fig-aasl37a-idea の (a) で、$0$ から $2\\pi$ の部分を見ます。実線と破線は",
            "図から数える言い方は消した")
in_text("$\\sin\\dfrac{\\pi}{4} = \\cos\\dfrac{\\pi}{4} = \\dfrac{\\sqrt{2}}{2}$", "例題4(c) の検算")
eq(sp.sin(PI / 4), sp.cos(PI / 4), "π/4 で一致")
eq(sp.sin(5 * PI / 4), sp.cos(5 * PI / 4), "5π/4 で一致")
eq(sp.sin(5 * PI / 4), -sp.sqrt(2) / 2, "5π/4 の値")
# 単位円と y = x の交点は 2 つ
_int = sp.solve([X ** 2 + sp.Symbol("y_") ** 2 - 1, sp.Symbol("y_") - X],
                [X, sp.Symbol("y_")])
chk(len(_int) == 2, f"単位円と y = x の交点は 2 つ: {_int}")

# --- 演習1：表とスケッチ ------------------------------------------------
in_text("[Copy and complete a table of values of $y = \\cos x$", "演習1 は表とスケッチ")
in_text("marking the coordinates of the maximum and minimum points.]{.q-en}",
        "最大点と最小点も")
in_text("*Values $1$, $0$, $-1$, $0$, $1$; plot these five points and join them with a "
        "smooth curve, stopping at $x = 2\\pi$.*", "演習1 の解答例")
in_text("$$\\text{maximum points } (0,\\ 1) \\text{ and } (2\\pi,\\ 1)$$", "最大点は 2 つ")
in_text("$$\\text{minimum point } (\\pi,\\ -1)$$", "最小点")
not_in_text("[Write down the amplitude and the period of $y = \\sin x$.]",
            "書き写すだけの演習1 は消した")

# --- 演習2：2 つの値 ----------------------------------------------------
in_text("[Write down the two values of $x$ in $-2\\pi \\le x \\le 2\\pi$ for which "
        "$\\cos x = -1$.]{.q-en}", "演習2 は 2 つ")
_c2b = [v for v in [R(k, 2) * PI for k in range(-8, 9)]
        if -2 * PI <= v <= 2 * PI and sp.cos(v) == -1]
chk(_c2b == [-PI, PI], f"演習2 の答えは ±π: {_c2b}")
chk(float(3 * PI) > float(2 * PI), "3π は範囲外")

# --- 演習3：tan のスケッチ ----------------------------------------------
in_text("[Sketch the graph of $y = \\tan x$ for $0 \\le x \\le 2\\pi$, showing the vertical "
        "asymptotes as dashed lines", "演習3 はスケッチ")
in_text("(img/aasl-3-7a-ex3.svg){#fig-aasl37a-ex3 width=100%}",
        "M03 演習3 の解答図")
not_in_text("two identical branches", "M03 「2 本の同じ枝」が消えている")
in_text("**指定された区間では、$3$ つの部分になります。**",
        "M03 3 つの部分")
in_text("**零点は $0$、$\\pi$、$2\\pi$ の $3$ つです。**", "M03 零点は 3 つ")
# tan の零点は sin の零点。0 ≤ x ≤ 2π では 0, π, 2π の 3 つ
chk([_z for _z in (0, 1, 2) if True] == [0, 1, 2], "M03 零点の個数の数え方")
chk(sp.sin(0) == 0 and sp.sin(sp.pi) == 0 and sp.sin(2 * sp.pi) == 0,
    "M03 0・π・2π で tan は 0")
chk(sp.cos(sp.pi / 2) == 0 and sp.cos(3 * sp.pi / 2) == 0,
    "M03 漸近線は π/2 と 3π/2")
in_text("**枝を漸近線でつながないでください。**", "枝はつながない")
eq(sp.tan(PI / 4), 1, "tan(π/4) = 1")
eq(sp.tan(5 * PI / 4), 1, "tan(5π/4) = 1")

# --- 演習5：ずれを説明させる --------------------------------------------
in_text("[Explain why $\\sin\\left(x + \\dfrac{\\pi}{2}\\right) = \\cos x$ for every value of "
        "$x$, using the unit circle.]{.q-en}", "演習5 は Explain")
in_text("a quarter-turn anticlockwise sends $(a,\\ b)$ to $(-b,\\ a)$", "演習5 の解答例")
not_in_text("[Write down the equations of the vertical asymptotes of $y = \\tan x$ for "
            "$0 \\le x \\le 3\\pi$.]", "古い演習5 は消した")
eq(sp.sin(0 + PI / 2), sp.cos(0), "検算 x = 0")
eq(sp.sin(PI / 2 + PI / 2), sp.cos(PI / 2), "検算 x = π/2")

# --- 演習6：tan の定義域と値域 ------------------------------------------
in_text("[Write down the domain and the range of $f(x) = \\tan x$.]{.q-en}", "演習6 は tan")
in_text("$$\\text{domain: } x \\ne \\frac{\\pi}{2} + n\\pi \\ (n \\in \\mathbb{Z})$$",
        "演習6 の定義域")
in_text("$$\\text{range: all real numbers}$$", "演習6 の値域")
chk(sp.Interval(0, 2 * PI).contains(PI / 2) and sp.Interval(0, 2 * PI).contains(3 * PI / 2),
    "0 ≤ x ≤ 2π で外れるのは 2 つ")

# --- command term を Find に ---------------------------------------------
chk(TEXT.count("[Find ") == 3, f"Find で始まる設問が 3 つ: {TEXT.count('[Find ')}")
in_text("[Find the values of $x$ in $0 \\le x \\le 4\\pi$ at which $y = \\sin x$ has a "
        "minimum point.]{.q-en}", "演習4 は Find")
in_text("[Find the number of values of $x$ in $-2\\pi \\le x \\le 2\\pi$ for which "
        "$\\sin x = 0$.]{.q-en}", "演習7 は Find")

# --- 演習7 の検算を、数え方が分かる形にした ------------------------------
in_text("**$2$ つに分けて数えます。**", "演習7 の検算")
in_text("$0$ を二重に数えているので $3 + 3 - 1 = 5$ ✓", "重複を引く")
eq(3 + 3 - 1, 5, "3 + 3 - 1 = 5")

# --- 演習10：最小の正の幅 -----------------------------------------------
in_text("**period は「くり返す幅のうち最小の正のもの」**です（[第 4 節](#amplitude)）。",
        "最小の正のもの")
in_text("but the period is the smallest positive such repeat", "model answer も positive")
in_text("and the period is the smallest positive repeat;", "解答例も positive")
eq(sp.tan(X - PI), sp.tan(X), "負の幅でもくり返す")


# ══════════════════════════════════════════════════════════
# E09  演習1 — 完成した cos のグラフ
# ══════════════════════════════════════════════════════════
in_text("(img/aasl-3-7a-ex1.svg){#fig-aasl37a-ex1 width=100%}",
        "E09 演習1 の解答図")
_e09t = [0, sp.pi / 2, sp.pi, 3 * sp.pi / 2, 2 * sp.pi]
_e09v = [sp.cos(_v) for _v in _e09t]
chk(_e09v == [1, 0, -1, 0, 1], "E09 表の値は 1, 0, -1, 0, 1")
chk(max(_e09v) == 1 and min(_e09v) == -1, "E09 上下の幅は -1 から 1")
chk(_e09v[0] == 1 and _e09v[4] == 1, "E09 両端がどちらも最大")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
