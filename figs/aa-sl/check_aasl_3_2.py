"""AA SL 3.2（三角比・正弦定理・余弦定理）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_2.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-2.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_2.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational


def D(x):
    return sp.rad(x)


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


def cos_rule(a, b, C):
    return a ** 2 + b ** 2 - 2 * a * b * sp.cos(D(C))


def area(a, b, C):
    return R(1, 2) * a * b * sp.sin(D(C))


# ══════════════════════════════════════════════════════════
# 0. 正確な値の表と、定理そのもの
# ══════════════════════════════════════════════════════════
for _d, _s, _c, _t in [(30, R(1, 2), sp.sqrt(3) / 2, sp.sqrt(3) / 3),
                       (45, sp.sqrt(2) / 2, sp.sqrt(2) / 2, sp.Integer(1)),
                       (60, sp.sqrt(3) / 2, R(1, 2), sp.sqrt(3))]:
    eq(sp.sin(D(_d)), _s, f"sin {_d}°")
    eq(sp.cos(D(_d)), _c, f"cos {_d}°")
    eq(sp.tan(D(_d)), _t, f"tan {_d}°")
eq(sp.sin(D(120)), sp.sqrt(3) / 2, "sin 120°")
eq(sp.cos(D(120)), R(-1, 2), "cos 120°")
eq(sp.sin(D(90)), 1, "sin 90°")
eq(sp.cos(D(90)), 0, "cos 90°")
in_text("| $\\sin\\theta$ | $\\dfrac{1}{2}$ | $\\dfrac{\\sqrt{2}}{2}$ | "
        "$\\dfrac{\\sqrt{3}}{2}$ |", "表の sin の行")
in_text("| $\\cos\\theta$ | $\\dfrac{\\sqrt{3}}{2}$ | $\\dfrac{\\sqrt{2}}{2}$ | "
        "$\\dfrac{1}{2}$ |", "表の cos の行")
in_text("| $\\tan\\theta$ | $\\dfrac{\\sqrt{3}}{3}$ | $1$ | $\\sqrt{3}$ |",
        "表の tan の行")
# 余弦定理は C = 90° でピタゴラス
_a, _b = sp.symbols("a b", positive=True)
eq(cos_rule(_a, _b, 90), _a ** 2 + _b ** 2, "C = 90° でピタゴラス")
# 余弦定理の 2 つの形が同値
_c = sp.Symbol("c", positive=True)
_C = sp.Symbol("Cang")
eq(sp.solve(sp.Eq(_c ** 2, _a ** 2 + _b ** 2 - 2 * _a * _b * _C), _C)[0],
   (_a ** 2 + _b ** 2 - _c ** 2) / (2 * _a * _b), "余弦定理の 2 つの形")
# 本文の走る例
eq(4 * sp.sin(D(30)) / sp.sin(D(45)), 2 * sp.sqrt(2), "本文 正弦定理 a = 2√2")
eq(cos_rule(3, 5, 60), 19, "本文 余弦定理 c^2 = 19")
eq(area(4, 6, 30), 6, "本文 面積 6")
in_text("a = \\frac{4 \\times \\frac{1}{2}}{\\frac{\\sqrt{2}}{2}} = "
        "\\frac{2}{\\frac{\\sqrt{2}}{2}} = \\frac{4}{\\sqrt{2}} = 2\\sqrt{2}",
        "本文の正弦定理の例")
in_text("c^{2} = 9 + 25 - 2(3)(5)\\left(\\frac{1}{2}\\right) = 34 - 15 = 19",
        "本文の余弦定理の例")
in_text("$A = \\dfrac{1}{2}(4)(6)\\left(\\dfrac{1}{2}\\right) = 6$", "本文の面積の例")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  直角三角形 8, 15, 17
# ══════════════════════════════════════════════════════════
eq(sp.sqrt(8 ** 2 + 15 ** 2), 17, "例題1(a) AC = 17")
eq(R(15, 17), R(15, 17), "例題1(b) sinA = 15/17")
eq(R(8, 15), R(8, 15), "例題1(c) tanC = 8/15")
eq(R(15, 17) ** 2 + R(8, 17) ** 2, 1, "例題1 検算 sin^2+cos^2 = 1")
eq((17 - 15) * (17 + 15), 64, "例題1 検算 2 乗の差 = 64")
eq(R(15, 8) * R(8, 15), 1, "例題1 検算 tanA と tanC は逆数")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  A=30°, B=45°, a=8
# ══════════════════════════════════════════════════════════
eq(180 - 30 - 45, 105, "例題2(a) C = 105°")
eq(8 * sp.sin(D(45)) / sp.sin(D(30)), 8 * sp.sqrt(2), "例題2(b) b = 8√2")
chk(sp.sin(D(45)) > sp.sin(D(30)), "sin 45° > sin 30°")
chk(8 * sp.sqrt(2) > 8, "b > a")
chk(abs(float(8 * sp.sqrt(2)) - 11.31) < 0.01, "8√2 ≈ 11.3")
# c は最長
_cc = 8 * sp.sin(D(105)) / sp.sin(D(30))
chk(float(_cc) > float(8 * sp.sqrt(2)), "c が最長")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  a=5, b=8, C=60°
# ══════════════════════════════════════════════════════════
eq(cos_rule(5, 8, 60), 49, "例題3(a) c^2 = 49")
eq(sp.sqrt(cos_rule(5, 8, 60)), 7, "例題3(a) c = 7")
eq(area(5, 8, 60), 10 * sp.sqrt(3), "例題3(b) 面積 10√3")
eq(R(64 + 49 - 25, 2 * 8 * 7), R(11, 14), "例題3(c) cosA = 11/14")
chk(5 < 7 < 8, "c は a と b の間")
eq(R(1, 2) * 5 * (8 * sp.sin(D(60))), 10 * sp.sqrt(3), "例題3 検算 底辺×高さ")
eq(sp.sqrt(196 - 121) / 14, 5 * sp.sqrt(3) / 14, "例題3 検算 sinA = 5√3/14")
eq(5 / (5 * sp.sqrt(3) / 14), 14 / sp.sqrt(3), "例題3 検算 a/sinA")
eq(7 / sp.sin(D(60)), 14 / sp.sqrt(3), "例題3 検算 c/sinC")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  AB=7, BC=3, B=120°
# ══════════════════════════════════════════════════════════
eq(cos_rule(7, 3, 120), 79, "例題4(a) AC^2 = 79")
eq(area(7, 3, 120), 21 * sp.sqrt(3) / 4, "例題4(b) 面積 21√3/4")
eq(cos_rule(7, 3, 90), 58, "例題4 検算 90° なら 58")
chk(79 > 58, "鈍角のほうが長い")
eq(49 + 9 - 21, 37, "例題4 検算 符号を落とすと 37")
eq(R(1, 2) * 3 * (7 * sp.sin(D(60))), 21 * sp.sqrt(3) / 4, "例題4 検算 底辺×高さ")
eq(R(1, 2) * 7 * sp.sqrt(79) * sp.sin(D(120)), 7 * sp.sqrt(237) / 4,
   "例題4(c) 生徒の式は 7√237/4")
chk(float(sp.sqrt(237)) > 15, "√237 > 15")
chk(float(7 * sp.sqrt(237) / 4) > 26, "生徒の値は 26 より大きい")
chk(abs(float(21 * sp.sqrt(3) / 4) - 9.09) < 0.02, "正しい面積 ≈ 9.1")
chk(180 - 120 == 60, "残り 2 角の和は 60°")
chk(sp.sqrt(79) > 7 and sp.sqrt(79) > 3, "AC が最長")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(sp.sqrt(13 ** 2 - 5 ** 2), 12, "演習1 x = 12")
eq((13 - 5) * (13 + 5), 144, "演習1 検算 2 乗の差")
eq(R(12, 9), R(4, 3), "演習2 tanP = 4/3")
eq(R(9, 12) * R(12, 9), 1, "演習2 検算 逆数")
eq(6 * sp.sin(D(90)) / sp.sin(D(30)), 12, "演習3 b = 12")
eq(6 / sp.sin(D(30)), 12, "演習3 検算 直角三角形でも 12")
eq(cos_rule(4, 6, 60), 28, "演習4 a^2 = 28")
eq(sp.sqrt(28), 2 * sp.sqrt(7), "演習4 a = 2√7")
eq(cos_rule(4, 6, 90), 52, "演習4 検算 90° なら 52")
chk(28 < 52, "60° は 90° より短い")
eq(area(6, 10, 30), 15, "演習5 面積 15")
eq(R(1, 2) * 10 * (6 * sp.sin(D(30))), 15, "演習5 検算 底辺×高さ")
eq(R(49 + 64 - 169, 2 * 7 * 8), R(-1, 2), "演習6 cosC = -1/2")
eq(cos_rule(7, 8, 120), 169, "演習6 検算 辺に戻すと 169")
eq(10 * sp.sin(D(60)) / sp.sin(D(45)), 5 * sp.sqrt(6), "演習7 c = 5√6")
chk(float(5 * sp.sqrt(6)) > 10, "演習7 c > b")
chk(abs(float(5 * sp.sqrt(6)) - 12.25) < 0.01, "5√6 ≈ 12.2")
eq(R(1, 2) * 4 * 7, 14, "演習8 最大の面積は 14")
eq(R(1, 2) * 4 * 7 * sp.sin(D(90)), 14, "演習8 C = 90° で 14")
chk(sp.sin(D(90)) == 1, "sin 90° = 1 が最大")
eq(R(25 + 49 - 81, 2 * 5 * 7), R(-1, 10), "演習9 cos = -1/10")
eq(25 + 49 - 2 * 5 * 7 * R(-1, 10), 81, "演習9 検算 辺に戻すと 81")
eq(R(1, 2) * 6 * 8 * sp.sin(D(30)), 12, "演習10 生徒の値は 12")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("15}{17}", "例題1(b)"), ("8}{15}", "例題1(c)"),
                ("105", "例題2(a)"), ("8\\sqrt{2}", "例題2(b)"),
                ("10\\sqrt{3}", "例題3(b)"), ("11}{14}", "例題3(c)"),
                ("\\sqrt{79}", "例題4(a)"), ("21\\sqrt{3}", "例題4(b)"),
                ("13^{2}-5^{2}", "演習1"), ("4}{3}", "演習2"),
                ("2\\sqrt{7}", "演習4"), ("5\\sqrt{6}", "演習7"),
                ("-\\frac{1}{10}", "演習9"), ("\\dfrac{1}{10}", "演習9")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **3.2** の欄に `Sine rule` として印刷されています。", "正弦定理の欄")
in_text("> $\\dfrac{a}{\\sin A} = \\dfrac{b}{\\sin B} = \\dfrac{c}{\\sin C}$",
        "正弦定理を逐語で")
in_text("公式集の **3.2** の欄に `Cosine rule` として印刷されています。", "余弦定理の欄")
in_text("> $c^2 = a^2 + b^2 - 2ab\\cos C$ ; $\\cos C = \\dfrac{a^2+b^2-c^2}{2ab}$",
        "余弦定理を逐語で")
in_text("公式集の **3.2** の欄に `Area of a triangle` として印刷されています。",
        "面積の欄")
in_text("> $A = \\dfrac{1}{2}ab\\sin C$", "面積を逐語で")
# ★ 答案の書き方を縛る Guidance の一文だけを引く
in_text("> In all areas of this topic, students should be encouraged to sketch "
        "well-labelled diagrams to support their solutions.", "答案の書き方の一文")
chk(TEXT.count("\n> ") == 4, f"引用は公式集 3 つ + Guidance 1 つ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 3, "公式集の callout は 3 つ")
not_in_text("Use of sine, cosine and tangent ratios to find", "シラバス本文は引かない")
not_in_text("This section does not include the ambiguous case", "シラバス本文は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("**なお、SL 3.2 では ambiguous case（あいまいな場合）は扱いません。**",
        "ambiguous case は範囲外だと書く")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("**この $3$ つは、直角三角形でしか使えません。**", "SOH-CAH-TOA の前提")
in_text("## $\\sin^{-1}x$ と $(\\sin x)^{-1}$ はちがいます", "逆関数の記号の注意")
in_text("## 正弦定理は、辺と「その向かいの角」を組にします", "組の注意")
in_text("## $\\cos$ が負になることがあります", "鈍角の注意")
in_text("## 面積の式で、はさむ角でない角を使う", "はさむ角の注意")
in_text("$\\hat{A}$ が鈍角だと $H$ は $A$ の外側に出ます。このとき直角三角形 $ACH$ の "
        "$A$ のところの角は $180° - \\hat{A}$ なので", "余弦定理の導出で鈍角にふれた")

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
in_text("**途中の値を丸めないでください。**", "丸めへの注意")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 8, f"model-answer が 8: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl32-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl32", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl32-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl32-exact", "tbl-aasl32-which", "eq-aasl32-soh",
             "eq-aasl32-inv", "eq-aasl32-sine", "eq-aasl32-cos",
             "eq-aasl32-cosang", "eq-aasl32-area"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
for _lab in ["eq-aasl32-soh", "eq-aasl32-sine", "eq-aasl32-cos",
             "eq-aasl32-cosang", "eq-aasl32-area"]:
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
SVG = os.path.join(BASE, "img", "aasl-3-2-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-2-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Naming sides and angles", "図(a) の題")
in_fig("$a$ faces $A$", "図(a) の対応")
in_fig("each small letter names the side opposite that capital", "図(a) の説明")
in_fig("(b) Which rule?", "図(b) の題")
in_fig("a side and the angle", "図(b) の正弦定理")
in_fig("facing it: sine rule", "図(b) の正弦定理（続き）")
in_fig("two sides and the", "図(b) の余弦定理")
in_fig("angle between them:", "図(b) の余弦定理（続き）")
in_fig("cosine rule", "図(b) の余弦定理（名前）")
in_fig("look for a matching pair first; if there is none, use the ", "図(b) の説明")
in_text("(a) In triangle $ABC$ each small letter names the side opposite",
        "キャプションが (a) を説明")
in_text("(b) If a side and the angle facing it are both known, use the sine rule",
        "キャプションが (b) を説明")
chk(not re.search(r"\d", FIGSTR), "図のラベルに数字がない")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-2.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-1.qmd") < DRAFT.index("aasl-3-2.qmd"), "並びが 3.1 → 3.2")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-2.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| hypotenuse |", "| opposite |", "| adjacent |", "| sine rule |",
           "| cosine rule |", "| included angle |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 演習8 の答えが Why it works にあったので差しかえた ------------------
in_text("[8]{.ex-no} [In triangle $ABC$, $a = 4$ cm and $b = 7$ cm, and the "
        "angle $\\hat{C}$ can vary.", "演習8 は面積の最大")
not_in_text("[Explain why the cosine rule becomes Pythagoras' theorem",
            "答えが本文にあった演習8 は消した")
in_text("*Area $= \\dfrac{1}{2}(4)(7)\\sin \\hat{C} = 14\\sin \\hat{C}$", "演習8 の解答例")
in_text("**変わるのは $\\sin \\hat{C}$ だけ**です。", "変わるのは sin だけ")

# --- 正弦定理の証明に、鈍角の但し書き -----------------------------------
eq(sp.sin(D(180) - D(50)), sp.sin(D(50)), "sin(180-θ) = sin θ")
eq(sp.cos(D(180) - D(50)), -sp.cos(D(50)), "cos(180-θ) = -cos θ")
in_text("$\\hat{A}$ が鈍角だと $H$ は $A$ の外側に出て、直角三角形 $ACH$ の $A$ の"
        "ところの角は $\\hat{A}$ ではなく $180° - \\hat{A}$ になります。",
        "正弦定理の証明の鈍角")
in_text("$\\sin(180° - \\hat{A}) = \\sin \\hat{A}$（SL 3.5 で扱います）",
        "sin(180-A) = sin A")

# --- 面積の証明をていねいにした -----------------------------------------
in_text("その足を $K$ とすると、直角三角形 $ACK$ の斜辺は $b$（$= CA$）で、$C$ の"
        "ところの角は $\\hat{C}$ ですから、$h = b\\sin C$ です。", "面積の証明の三角形")
in_text("（$\\hat{C}$ が鈍角のときは $K$ が $BC$ の外に出て", "面積の証明の鈍角")
not_in_text("その垂線を含む直角三角形で、$\\hat{C}$ から見れば高さは",
            "あいまいな言い方は消した")

# --- 余弦定理の鈍角の但し書きをていねいにした ---------------------------
in_text("$AH = b\\cos(180° - A) = -b\\cos A$（$\\cos A < 0$ なので、これは正の長さです）",
        "AH の符号")
in_text("$\\hat{B}$ が鈍角で $H$ が $B$ の外側に出るときは $HB$ の長さが "
        "$b\\cos A - c$ になりますが、$2$ 乗するので結果は変わりません。",
        "B が鈍角のとき")

# --- 例題2(c) の一般化を落とした ----------------------------------------
in_text("Here $\\hat{A} = 30°$ and $\\hat{B} = 45°$ are both acute, and the "
        "sine function is increasing between $0°$ and $90°$", "鋭角だと明記")
not_in_text("In any triangle, the longer side faces the larger angle.*",
            "解答例からは一般命題を落とした")
in_text("鈍角がある三角形では $0°$ から $90°$ の増加だけでは説明できません。",
        "一般の場合の注意（日本語）")

# --- 例題2(b) の検算を正弦定理に戻す形にした ----------------------------
eq(8 / sp.sin(D(30)), 16, "a/sinA = 16")
eq(8 * sp.sqrt(2) / sp.sin(D(45)), 16, "b/sinB = 16")
in_text("**検算（(b) について）。** **正弦定理に戻して、両辺の値を出します。**",
        "例題2(b) の検算")
not_in_text("**有理化して大きさを見ます。**", "大小だけの検算は消した")

# --- 例題3(a) の検算に根拠を書いた --------------------------------------
in_text("$\\hat{A}+\\hat{B} = 180°-60° = 120°$ なので、$\\hat{A}$ と $\\hat{B}$ の"
        "一方は $60°$ より小さく、他方は $60°$ より大きくなります。", "大小の根拠")
in_text("$a = 5 < b = 8$ だから $\\hat{A} < \\hat{B}$ で、$\\hat{A} < 60° < \\hat{B}$ です。",
        "辺の大小から角の大小")

# --- 例題3(b) の検算を、別の 2 辺とはさむ角にした ------------------------
eq(R(1, 2) * 8 * 7 * (5 * sp.sqrt(3) / 14), 10 * sp.sqrt(3),
   "1/2 bc sinA = 10√3")
eq(sp.sqrt(1 - R(11, 14) ** 2), 5 * sp.sqrt(3) / 14, "sinA = 5√3/14")
in_text("**検算（(b) について）。** **別の $2$ 辺と、そのはさむ角で出し直します。**",
        "例題3(b) の検算は別の組")
not_in_text("**底辺と高さで出し直します。** $\\hat{C}$ から見て、$a = 5$ を底辺",
            "同じ積の並べかえは消した")

# --- 正確な値の表に 90° を足し、公式集にないと書いた ---------------------
in_text("直角については $\\sin 90° = 1$、$\\cos 90° = 0$ を使います。", "90° の値")
in_text("**この表は公式集にはありません。** Paper 1 は電卓なしなので、覚える必要があります。",
        "表は公式集にない")

# --- シラバスは「奨励」------------------------------------------------
in_text("シラバスは、この項目について次のように述べています。", "述べています")
in_text("シラバスが、ラベルを付けた図をかくよう勧めています", "勧めています")
not_in_text("シラバスは、この項目について次のように求めています。", "「求めています」は消した")
not_in_text("ラベルを付けた図をかくよう求めています", "「求めています」は消した")

# --- command term（exact の言い方）と設問の英語 -------------------------
chk(TEXT.count("giving an exact answer") == 0,
    f"giving an exact answer は使わない: {TEXT.count('giving an exact answer')}")
chk(TEXT.count("Find the exact value of") == 5,
    f"Find the exact value of が 5 か所: {TEXT.count('Find the exact value of')}")
chk(TEXT.count("giving your answer in exact form") == 2,
    f"giving your answer in exact form が 2 か所: {TEXT.count('giving your answer in exact form')}")
in_text("[A triangular flower bed $ABC$ has $AB = 7$ m", "花壇（面積に見合う場面）")
not_in_text("A triangular field $ABC$", "field は消した")
chk(abs(float(21 * sp.sqrt(3) / 4) - 9.09) < 0.02, "面積は約 9.1 m^2")

# --- 電卓（機種に依存しない書き方）--------------------------------------
in_text("ハンドヘルドでは `trig` キーでパレットが開きますが、`sin(` のように直接"
        "打ち込んでもかまいません。", "機種に依存しない書き方")


# ══════════════════════════════════════════════════════════
# E05  演習6 — cos C から角まで、そして GDC で一般の角
# ══════════════════════════════════════════════════════════
in_text("Find the exact value of $\\cos \\hat{C}$, and hence find $\\hat{C}$.]",
        "E05 演習6(a) は角まで")
in_text("[In a second triangle, $a = 7$ cm, $b = 8$ cm and $c = 11$ cm. Use "
        "your calculator to find $\\hat{C}$, correct to three significant "
        "figures. State the angle setting the calculator must be in.]",
        "E05 演習6(b) は GDC")
in_text("$$\\hat{C} = 120°$$", "E05 演習6(a) の答え")
in_text("**角度の設定を `Degree` にしてください。**", "E05 角度モードの指示")
in_text("**途中で丸めず、最後に有効数字 $3$ 桁**にします。", "E05 丸めの指示")
# a=7, b=8, c=13 → cosC = -1/2 → 120°;  c=11 → -1/14 → 94.1°
chk(sp.Rational(49 + 64 - 169, 112) == sp.Rational(-1, 2), "E05 cosC = -1/2")
chk(sp.deg(sp.acos(sp.Rational(-1, 2))) == 120, "E05 C = 120°")
chk(sp.Rational(49 + 64 - 121, 112) == sp.Rational(-1, 14), "E05 cosC = -1/14")
_e05c = sp.deg(sp.acos(sp.Rational(-1, 14)))
chk(abs(float(_e05c) - 94.0965) < 1e-3, "E05 C = 94.0965...°")
chk(float("%.3g" % float(_e05c)) == 94.1, "E05 3 有効数字で 94.1")
chk(float(_e05c) > 90, "E05 cos が負なら鈍角")
chk(float(_e05c) < 120, "E05 c を短くすると角も小さい")
chk(7 + 8 > 11 and 7 + 11 > 8 and 8 + 11 > 7, "E05 3 辺は三角形をつくる")
# ラジアン設定のままだと別の数になる
chk(abs(float(sp.acos(sp.Rational(-1, 14))) - 1.6423) < 1e-3,
    "E05 ラジアンなら 1.64")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
