"""AA SL 3.1（空間図形）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_1.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-1.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_1.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
PI = sp.pi
r_, h_, l_, a_, b_, c_ = sp.symbols("r h l a b c", positive=True)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def dist(P, Q):
    return sp.sqrt(sum((p - q) ** 2 for p, q in zip(P, Q)))


def mid(P, Q):
    return tuple(sp.Rational(1, 2) * (p + q) for p, q in zip(P, Q))


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの
# ══════════════════════════════════════════════════════════
x1, y1, z1, x2, y2, z2 = sp.symbols("x1 y1 z1 x2 y2 z2", real=True)
# 距離：引く順を変えても同じ
eq(dist((x1, y1, z1), (x2, y2, z2)) ** 2,
   dist((x2, y2, z2), (x1, y1, z1)) ** 2, "距離は引く順によらない")
eq((x1 - x2) ** 2, (x2 - x1) ** 2, "(a-b)^2 = (b-a)^2")
# 中点：両端までの距離が等しい
_A = (x1, y1, z1)
_B = (x2, y2, z2)
_M = mid(_A, _B)
eq(dist(_A, _M) ** 2, dist(_M, _B) ** 2, "中点は両端から等距離")
eq(2 * dist(_A, _M) ** 2 * 2, dist(_A, _B) ** 2, "中点までは全体の半分")
# 母線
eq(sp.sqrt(r_ ** 2 + h_ ** 2) ** 2, r_ ** 2 + h_ ** 2, "l^2 = r^2+h^2")
chk(sp.simplify(sp.sqrt(r_ ** 2 + h_ ** 2) - h_) != 0, "l ≠ h")
# 半球
eq(R(1, 2) * R(4, 3) * PI * r_ ** 3, R(2, 3) * PI * r_ ** 3, "半球の体積")
eq(R(1, 2) * 4 * PI * r_ ** 2, 2 * PI * r_ ** 2, "半球の曲面")
eq(2 * PI * r_ ** 2 + PI * r_ ** 2, 3 * PI * r_ ** 2, "単独の半球の表面積")
# ピタゴラス 2 回
eq(sp.sqrt(sp.sqrt(a_ ** 2 + b_ ** 2) ** 2 + c_ ** 2) ** 2,
   a_ ** 2 + b_ ** 2 + c_ ** 2, "ピタゴラス 2 回")
# 立方体：空間の対角線 > 面の対角線
eq(sp.sqrt(2 * a_ ** 2), a_ * sp.sqrt(2), "面の対角線 a√2")
eq(sp.sqrt(3 * a_ ** 2), a_ * sp.sqrt(3), "空間の対角線 a√3")
chk(sp.sqrt(3) > sp.sqrt(2), "√3 > √2")

# 本文の走る例
eq(dist((1, 2, 3), (3, 5, 9)), 7, "本文 距離 7")
chk(mid((1, 2, 3), (3, 5, 9)) == (2, R(7, 2), 6), "本文 中点")
in_text("d = \\sqrt{2^{2}+3^{2}+6^{2}} = \\sqrt{4+9+36} = \\sqrt{49} = 7",
        "本文の距離の例")
in_text("中点は $\\left(2, \\dfrac{7}{2}, 6\\right)$ です。", "本文の中点の例")
# 本文の円錐 r=4, h=3
eq(sp.sqrt(16 + 9), 5, "本文 l = 5")
eq(R(1, 3) * PI * 16 * 3, 16 * PI, "本文 V = 16π")
eq(PI * 4 * 5, 20 * PI, "本文 側面 20π")
eq(20 * PI + 16 * PI, 36 * PI, "本文 表面積 36π")
in_text("$r = 4$、$h = 3$ の円錐なら $l = 5$", "本文の円錐")
# 本文の直方体 12 × 9 × 8
eq(sp.sqrt(144 + 81), 15, "本文 底面の対角線 15")
eq(sp.sqrt(15 ** 2 + 8 ** 2), 17, "本文 空間の対角線 17")
in_text("底面の対角線は $\\sqrt{144+81} = 15$", "本文の底面の対角線")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  A(1,2,2), B(5,5,14)
# ══════════════════════════════════════════════════════════
A1, B1 = (1, 2, 2), (5, 5, 14)
eq(dist(A1, B1), 13, "例題1(a) AB = 13")
eq(4 ** 2 + 3 ** 2 + 12 ** 2, 169, "16+9+144 = 169")
chk(mid(A1, B1) == (3, R(7, 2), 8), "例題1(b) 中点")
C1 = tuple(2 * b - a for a, b in zip(A1, B1))
chk(C1 == (9, 8, 26), "例題1(c) C = (9,8,26)")
chk(mid(A1, C1) == B1, "例題1(c) 検算 mid(A,C) = B")
chk(tuple(m - a for m, a in zip(mid(A1, B1), A1)) == (2, R(3, 2), 6),
    "例題1 検算 M-A")
chk(tuple(b - m for m, b in zip(mid(A1, B1), B1)) == (2, R(3, 2), 6),
    "例題1 検算 B-M")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  円錐 r=5, h=12
# ══════════════════════════════════════════════════════════
eq(R(1, 3) * PI * 25 * 12, 100 * PI, "例題2(a) V = 100π")
eq(sp.sqrt(25 + 144), 13, "例題2(b) l = 13")
eq(5 ** 2 + 12 ** 2, 169, "5-12-13")
eq(PI * 5 * 13 + PI * 25, 90 * PI, "例題2(c) A = 90π")
eq(PI * 5 * 13, 65 * PI, "例題2 側面 65π")
eq(PI * 25 * 12, 300 * PI, "例題2 検算 同じ円柱は 300π")
eq(R(1, 3) * 300 * PI, 100 * PI, "例題2 検算 その 1/3")
chk(90 * PI > 65 * PI, "total は curved より大きい")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  半球 r=3 + 円柱 r=3, h=8
# ══════════════════════════════════════════════════════════
eq(PI * 9 * 8, 72 * PI, "例題3(a) 円柱 72π")
eq(R(2, 3) * PI * 27, 18 * PI, "例題3(b) 半球 18π")
eq(72 * PI + 18 * PI, 90 * PI, "例題3(b) 合計 90π")
eq(R(4, 3) * PI * 27, 36 * PI, "例題3 検算 球なら 36π")
eq(R(1, 2) * 36 * PI, 18 * PI, "例題3 検算 その半分")
eq(2 * PI * 3 * 8, 48 * PI, "例題3(c) 円柱の側面 48π")
eq(2 * PI * 9, 18 * PI, "例題3(c) 半球の曲面 18π")
eq(PI * 9, 9 * PI, "例題3(c) 底の円 9π")
eq(48 * PI + 18 * PI + 9 * PI, 75 * PI, "例題3(c) 合計 75π")
eq(75 * PI + 9 * PI, 84 * PI, "例題3(d) 誤ると 84π")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  直方体 4, 3, 12
# ══════════════════════════════════════════════════════════
eq(sp.sqrt(16 + 9), 5, "例題4(a) AC = 5")
eq(sp.sqrt(25 + 144), 13, "例題4(b) AG = 13")
eq(sp.sqrt(16 + 9 + 144), 13, "例題4 検算 3 辺から直接でも 13")
eq(R(5, 13), R(5, 13), "例題4(c) cosθ = 5/13")
eq(R(5, 13) ** 2 + R(12, 13) ** 2, 1, "例題4 検算 sin^2+cos^2 = 1")
eq(R(12, 5), R(12, 5), "例題4 検算 tanθ = 12/5")
eq(25 + 144, 169, "例題4 検算 169")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(dist((1, 0, 2), (3, 4, 8)) ** 2, 56, "演習1 d^2 = 56")
eq(sp.sqrt(56), 2 * sp.sqrt(14), "演習1 √56 = 2√14")
chk(mid((2, -1, 5), (6, 3, -1)) == (4, 1, 2), "演習2 中点 (4,1,2)")
eq(R(4, 3) * PI * 216, 288 * PI, "演習3 V = 288π")
chk(6 ** 3 == 216, "6^3 = 216")
chk(sp.solveset(sp.Eq(4 * PI * r_ ** 2, 100 * PI), r_,
                sp.Interval.open(0, sp.oo)) == sp.FiniteSet(5), "演習4 r = 5")
eq(4 * PI * 25, 100 * PI, "演習4 検算")
eq(R(1, 3) * 36 * 4, 48, "演習5 V = 48")
chk(6 ** 2 == 36, "底面積 36")
eq(36 * 4, 144, "演習5 検算 直方体は 144")
eq(sp.sqrt(17 ** 2 - 8 ** 2), 15, "演習6 h = 15")
eq(8 ** 2 + 15 ** 2, 289, "演習6 検算 289")
eq(2 * PI * 9 + PI * 9, 27 * PI, "演習7 A = 27π")
eq(4 * PI * 9, 36 * PI, "演習7 検算 球なら 36π")
eq(sp.sqrt(4 + 9 + 36), 7, "演習9 d = 7")
eq(sp.sqrt(4 + 9), sp.sqrt(13), "演習9 検算 面の対角線 √13")
eq(sp.sqrt(13 + 36), 7, "演習9 検算 2 段でも 7")
eq(PI * 3 * 5, 15 * PI, "演習10 側面 15π")
eq(PI * 3 * 5 + PI * 9, 24 * PI, "演習10 正しくは 24π")
chk(15 * PI > 9 * PI, "演習10 検算 側面 > 底面")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("(1, 2, 2)", "例題1"), ("(5, 5, 14)", "例題1"),
                ("13", "例題1(a)"), ("100\\pi", "例題2(a)"),
                ("90\\pi", "例題2(c)"), ("75\\pi", "例題3(c)"),
                ("\\frac{5}{13}", "例題4(c)"), ("\\dfrac{5}{13}", "例題4(c)"),
                ("2\\sqrt{14}", "演習1"), ("(4, \\ 1, \\ 2)", "演習2"),
                ("288\\pi", "演習3"), ("27\\pi", "演習7"),
                ("24\\pi", "演習10"), ("a\\sqrt{3}", "演習8")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **3.1** の欄に `Distance between two points` として印刷されています。",
        "3.1 距離の欄")
in_text("> $d = \\sqrt{(x_1-x_2)^2 + (y_1-y_2)^2 + (z_1-z_2)^2}$", "距離を逐語で")
in_text("公式集の **3.1** の欄に `Coordinates of the midpoint of a line segment` "
        "として印刷されています。", "3.1 中点の欄")
in_text("> $\\left(\\dfrac{x_1+x_2}{2}, \\dfrac{y_1+y_2}{2}, \\dfrac{z_1+z_2}{2}\\right)$",
        "中点を逐語で")
chk(TEXT.count("\n> ") == 2, f"引用は公式集の 2 つだけ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 3, "公式集の callout は 3 つ")
chk(TEXT.index("$$ {#eq-aasl31-dist}") < TEXT.index("公式集の **3.1** の欄に `Distance"),
    "距離の callout は式の直後")
chk(TEXT.index("$$ {#eq-aasl31-mid}") < TEXT.index("公式集の **3.1** の欄に `Coordinates"),
    "中点の callout は式の直後")
# 公式集にないものを、あると書かない
in_text("**半球（hemisphere）の式は、印刷されていません。**", "半球は公式集にない")
not_in_text("Volume of a hemisphere |", "半球を表に入れていない")
for _row in ["| Volume of a right-pyramid |", "| Volume of a right cone |",
             "| Area of the curved surface of a cone |",
             "| Volume of a sphere |", "| Surface area of a sphere |"]:
    in_text(_row, "公式集の表の行: " + _row)
# ★ シラバスの逐語引用は置かない
not_in_text("In SL examinations, only right-angled trigonometry questions",
            "シラバスの逐語引用は置かない")
not_in_text("Volume and surface area of three-dimensional solids",
            "シラバス本文は引かない")
not_in_text("シラバスは、答案", "答案の書き方の引用はこのページにはない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("SL の試験で立体を題材に問われる三角比は、**直角三角形のもの**に限られます。",
        "3D は直角三角形の三角比だけ（要約で書く）")
in_text("**立体の中の三角形がぜんぶ直角三角形だ、という意味ではありません。**",
        "直角でない三角形もあると断る")
in_text("**垂線を $1$ 本下ろして直角三角形に分ける**", "垂線で分ける手")
not_in_text("シラバスは、SL の試験で立体について", "シラバスに帰属させない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## `surface area` は、ふつう底面も入ります", "total と curved の注意")
in_text("## くっついている面は、表面積に入れません", "組み合わせの注意")
in_text("## 「影」は、真下に下ろした先です", "影の注意")
in_text("ただし、**平らな円の面**を足すかどうかは、その半球がどう置かれているかで決まります。",
        "半球は置かれ方による")
in_text("$0°$ から $180°$ の間では **$\\cos$ が小さいほど角は大きい**ので、",
        "cos の単調性")

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
in_text("**角の単位に気をつけてください。**", "角の単位への注意")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 6, f"model-answer が 6: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl31-", TEXT, re.M)) == 4, "例題が 4")
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
    _b = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _b), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl31", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl31-idea") >= 1, "図を本文から参照している")
chk(TEXT.count("@tbl-aasl31-booklet") >= 1, "表を本文から参照している")
for _lab in ["eq-aasl31-dist", "eq-aasl31-mid", "eq-aasl31-slant",
             "eq-aasl31-hemi"]:
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
SVG = os.path.join(BASE, "img", "aasl-3-1-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-1-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Pythagoras twice", "図(a) の題")
in_fig("$\\\\sqrt{a^{2}+b^{2}}$", "図(a) の底面の対角線")
in_fig("$\\\\sqrt{a^{2}+b^{2}+c^{2}}$", "図(a) の空間の対角線")
in_fig("the base diagonal first, then straight up", "図(a) の説明")
in_fig("(b) A line and a plane", "図(b) の題")
in_fig("the line", "図(b) の直線")
in_fig("its shadow on the plane", "図(b) の影")
in_fig("$\\\\theta$", "図(b) の角")
in_fig("$\\\\theta$ is the angle with the shadow, and it is the smallest one",
       "図(b) の説明")
in_text("(a) The space diagonal of a cuboid is found with Pythagoras' theorem "
        "used twice", "キャプションが (a) を説明")
in_text("(b) The angle between a line and a plane is the angle between the line "
        "and its shadow", "キャプションが (b) を説明")
# 図に具体的な数を書いていない
chk(not re.search(r"\d", FIGSTR.replace("a^{2}", "").replace("b^{2}", "")
                  .replace("c^{2}", "")), "図のラベルに数字がない")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-1.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-11.qmd") < DRAFT.index("aasl-3-1.qmd"), "並びが 2.11 → 3.1")
chk('- section: "Topic 3 — Geometry and trigonometry"' in DRAFT,
    "Topic 3 の section がある")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-1.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| cuboid |", "| cone |", "| sphere |", "| hemisphere |",
           "| slant height |", "| surface area |", "| midpoint |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 例題1(d)・演習9 の答えを本文に先出ししない ------------------------
in_text("なぜそう言えるのかは、[例題 1](#exm-aasl31-distance) の (d) で考えます。",
        "引く順の理由は例題に送る")
not_in_body("$2$ 乗するので、符号が消えるからです", "例題1(d) の理由が本文にない")
not_in_body("\\sqrt{1^{2}+4^{2}+8^{2}}", "演習9 の式が本文にない")
in_text("[9]{.ex-no} [A cuboid has edges of length $1$ cm, $4$ cm and $8$ cm.",
        "演習9 は 1, 4, 8")
eq(sp.sqrt(1 + 16 + 64), 9, "演習9 d = 9")
eq(sp.sqrt(1 + 16), sp.sqrt(17), "演習9 面の対角線 √17")
eq(sp.sqrt(17 + 64), 9, "演習9 2 段でも 9")
not_in_text("edges of length $2$ cm, $3$ cm and $6$ cm", "本文と重なる演習9 は消した")

# --- 半球の場合分け -----------------------------------------------------
in_text("**単独の半球**（中身のつまった `solid hemisphere`。伏せて置いた形）",
        "solid hemisphere と明記")
in_text("**半径のちがう立体の上にのった半球** → かくれるのは**重なっているところだけ**です。",
        "半径がちがう場合")
eq(PI * sp.Symbol("R", positive=True) ** 2 - PI * r_ ** 2,
   PI * (sp.Symbol("R", positive=True) ** 2 - r_ ** 2), "ドーナツ形の面積")
not_in_text("（お椀を伏せた形）", "中空に読める言い方は消した")

# --- 「影との角が最小」の証明（条件つき）--------------------------------
in_text("ここでは、**直線が平面に垂直ではない**としておきます", "垂直な場合を除く")
in_text("**$\\mathrm{OP}$ とその直線のなす角は、その直線上のどこに点をとっても同じ**",
        "R の取り方の一般性")
in_text("\\cos \\angle \\mathrm{POQ} = \\frac{\\mathrm{OP}^{2}+\\mathrm{OQ}^{2}-"
        "\\mathrm{PQ}^{2}}{2\\,\\mathrm{OP}\\cdot\\mathrm{OQ}}", "余弦定理で書く")
# 余弦定理そのもの
_op, _oq, _pq = sp.symbols("OP OQ PQ", positive=True)
eq((_op ** 2 + _oq ** 2 - _pq ** 2) / (2 * _op * _oq),
   sp.cos(sp.acos((_op ** 2 + _oq ** 2 - _pq ** 2) / (2 * _op * _oq))),
   "余弦定理の形")
chk(sp.cos(sp.rad(60)) > sp.cos(sp.rad(120)), "cos が小さいほど角は大きい")
in_text("そうしてできた角は、その直線と平面上の直線とのなす角のうち、"
        "**いちばん小さいもの**です", "最小だと正しく書く")
not_in_text("その直線と平面上のどの直線とのなす角よりも**小さく**なります",
            "影自身を含む言い方は消した")

# --- 2 点と直方体を結ぶ一歩 ---------------------------------------------
in_text("辺が座標軸に平行な直方体をかきます。その辺の長さは $a = |x_{1}-x_{2}|$",
        "2 点から直方体へ")

# --- 中点が平均である理由 -----------------------------------------------
in_text("**同じ向きに、同じだけ、$2$ 回動く**ので、$\\mathrm{M}$ は $\\mathrm{A}$ と "
        "$\\mathrm{B}$ を結ぶ線分の上にあります。", "中点の理由（線分の上）")
in_text("**線分の上にあって両端から等距離**、これが中点です。", "中点の定義に戻す")
not_in_text("**一定の割合で**変わります", "言いかえだけの説明は消した")

# --- 検算を独立した道すじにした ------------------------------------------
# 例題1(a)
eq(sp.sqrt(4 ** 2 + 3 ** 2), 5, "例題1 検算 2 段の 1 段目")
eq(sp.sqrt(5 ** 2 + 12 ** 2), 13, "例題1 検算 2 段の 2 段目")
in_text("**検算（(a) について）。** **$2$ 段に分けて出し直します。**", "例題1(a) の検算")
not_in_text("差を $\\mathrm{A}-\\mathrm{B}$ でとると $-4$、$-3$、$-12$",
            "(d) と重なる検算は消した")
# 例題2(b)
eq((13 - 12) * (13 + 12), 25, "例題2 検算 (l-h)(l+h) = 25")
eq(13 ** 2 - 12 ** 2, 5 ** 2, "l^2 - h^2 = r^2")
in_text("**検算（(b) について）。** **$2$ 乗の差で見ます。**", "例題2(b) の検算は差の積")
not_in_text("**$5$-$12$-$13$ の組かどうかを見ます。**", "同じ足し算のくり返しは消した")
# 例題2(c)
eq(PI * 5 * (13 + 5), 90 * PI, "πr(l+r) = 90π")
in_text("**$\\pi r$ でくくって出し直します。** $A = \\pi r(l+r)", "例題2(c) の検算")
# 例題3(a)
chk(float(72 * PI) < 288, "72π < 288")
chk(abs(float(72 * PI) - 226.19) < 0.1, "72π ≈ 226")
chk(abs(288 * float(PI / 4) - float(72 * PI)) < 1e-6, "288 × π/4 = 72π")
in_text("**検算（(a) について）。** **直方体で上から押さえます。**", "例題3(a) の検算")
not_in_text("**数を分けて計算し直します。** $\\pi(9)(8)", "同じ計算のくり返しは消した")
# 例題3(c)
eq(48 * PI + 9 * PI + 9 * PI, 66 * PI, "ふたのある円柱は 66π")
eq(66 * PI - 9 * PI + 18 * PI, 75 * PI, "置きかえても 75π")
in_text("**ふたのある円柱と見くらべます。**", "例題3(c) の検算は別の組み立て")
not_in_text("**上下から $1$ 回ずつ数え直します。**", "見る向きの言い方は消した")
# 例題3 の検算の順
_i1 = TEXT.index("**検算（(a) について）。** **直方体で上から押さえます。**")
_i2 = TEXT.index("**検算（(b) について）。** **半球を球と見くらべます。**")
_i3 = TEXT.index("**検算（(c) について）。** **ふたのある円柱と見くらべます。**")
chk(_i1 < _i2 < _i3, "例題3 の検算は (a) → (b) → (c) の順")
# 例題4(c)(d)
eq(R(12, 5), R(12, 5), "tanθ = 12/5")
chk(sp.simplify(sp.sqrt(5 ** 2 + 12 ** 2)) == 13, "5:12:13 の三角形")
eq(R(4, 13), R(4, 13), "cos GAB = 4/13")
chk(R(4, 13) < R(5, 13), "4/13 < 5/13")
eq(4 ** 2 + (3 ** 2 + 12 ** 2), 13 ** 2, "三角形 ABG は B が直角")
in_text("**$\\mathrm{AG}$ を使わない道すじで出し直します。**", "例題4(c) の検算は独立")
in_text("**検算（(d) について）。** **$\\mathrm{G}\\hat{\\mathrm{A}}\\mathrm{B}$ も"
        "直角三角形で出せます。**", "例題4(d) の検算")
not_in_text("**サインとタンジェントでも見ます。**", "必ず成り立つ検算は消した")
in_text("$\\cos \\mathrm{G}\\hat{\\mathrm{A}}\\mathrm{B} = \\dfrac{4}{13} < \\dfrac{5}{13}$.*",
        "例題4(d) の解答例に根拠")
# 演習1
eq((2 * sp.sqrt(14)) ** 2, 56, "(2√14)^2 = 56")
in_text("**検算。** **$2$ 乗して戻します。** $\\left(2\\sqrt{14}\\right)^{2}",
        "演習1 の検算は 2 乗して戻す")
not_in_text("**順番を入れかえます。**", "符号だけの検算は消した")

# --- 命令語（command term）と設問の英語 ---------------------------------
in_text("**(a)** [Find the volume of the cylinder, giving your answer in terms of $\\pi$.]",
        "例題3(a) は Find")
not_in_text("[Write down the volume of the cylinder", "計算の要る Write down は消した")
in_text("giving your answer in the form $a\\sqrt{b}$, where $a, b \\in \\mathbb{Z}^{+}$",
        "演習1 は形を指定")
not_in_text("giving an exact answer.]", "あいまいな言い方は消した")

# --- 電卓（角の単位は問題文に合わせる）----------------------------------
in_text("**問題文の角が度で与えられていれば `Degree`、ラジアンで与えられていれば "
        "`Radian`** に合わせます。", "単位は問題文に合わせる")
not_in_text("**立体の問題はふつう度**なので、`Degree` にしておきます。",
            "一般則のような助言は消した")
in_text("`trig` キーで開くパレットから選びます", "trig はパレット")


# ══════════════════════════════════════════════════════════
# C03  「影との角がいちばん小さい」証明は、余弦定理（3.2）を使う
# ══════════════════════════════════════════════════════════
in_text("## なぜ「影」との角がいちばん小さいのか（余弦定理を使います）",
        "C03 折り畳みの見出し")
in_text("余弦定理は [SL 3.2](aasl-3-2.qmd) で学ぶので、**3.2 のあとで"
        "読んでください。**", "C03 3.2 への案内")
in_text('::: {.callout-note collapse="true"}', "C03 折り畳みになっている")
# 余弦定理: OP=5, OQ=OR=4, PQ=3, PR=6 で、PR が長いほど角は大きい
_c03 = [(5, 4, 3), (5, 4, 6)]
_cos = [sp.Rational(_a ** 2 + _b ** 2 - _c ** 2, 2 * _a * _b)
        for _a, _b, _c in _c03]
chk(_cos[1] < _cos[0], "C03 PR が長いほど cos は小さい")
chk(sp.acos(_cos[1]) > sp.acos(_cos[0]), "C03 cos が小さいほど角は大きい")
chk(3 ** 2 + 27 == 6 ** 2, "C03 PR^2 = PQ^2 + QR^2")


# ══════════════════════════════════════════════════════════
# E05  演習5 — 斜高から表面積、側稜と底面のなす角
# ══════════════════════════════════════════════════════════
in_text("[Show that the slant height of a triangular face is $5$ cm, and "
        "hence find the total surface area of the pyramid.]",
        "E05 演習5 の斜高")
in_text("[Find the angle between a slant edge of the pyramid and the base,",
        "E05 演習5 の なす角")
in_text("側面の三角形の斜高（slant height）が $5$ cm であることを示し、",
        "E05 演習5 の訳（斜高）")
in_text("角錐の側稜（slant edge）と底面のなす角を、", "E05 演習5 の訳（なす角）")
in_text("$$A = 36 + 4\\left(\\frac{1}{2}\\right)(6)(5) = 36 + 60 = 96 \\text{ cm}^{2}$$",
        "E05 演習5 の表面積")
in_text("**$3$ と $3\\sqrt{2}$ を取りちがえないでください。**",
        "E05 中点までと頂点までの区別")
# 底面 6 の正四角錐、高さ 4
chk(sp.sqrt(4**2 + 3**2) == 5, "E05 斜高は 5")
chk(36 + 4 * sp.Rational(1, 2) * 6 * 5 == 96, "E05 表面積は 96")
chk(sp.Rational(1, 3) * 36 * 4 == 48, "E05 体積は 48")
chk(sp.simplify(sp.sqrt(6**2 + 6**2) / 2 - 3 * sp.sqrt(2)) == 0,
    "E05 中心から頂点までは 3√2")
_e05t = sp.deg(sp.atan(4 / (3 * sp.sqrt(2))))
chk(abs(float(_e05t) - 43.3138) < 1e-3, "E05 側稜と底面のなす角は 43.3°")
chk(float("%.3g" % float(_e05t)) == 43.3, "E05 3 有効数字で 43.3")
_e05a = sp.deg(sp.atan(sp.Rational(4, 3)))
chk(float(_e05t) < float(_e05a), "E05 側稜の角は面の傾きより小さい")
chk(abs(float(_e05a) - 53.1301) < 1e-3, "E05 面の傾きは 53.1°")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
