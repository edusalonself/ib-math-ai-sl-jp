"""AA SL 3.4（弧度法・弧の長さ・扇形の面積）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_4.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-4.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_4.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
PI = sp.pi


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


def arc(r, t):
    return r * t


def sector(r, t):
    return R(1, 2) * r ** 2 * t


def segment(r, t):
    return sector(r, t) - R(1, 2) * r ** 2 * sp.sin(t)


def to_rad(d):
    return sp.rad(d)


def to_deg(t):
    return sp.deg(t)


# ══════════════════════════════════════════════════════════
# 0. 定義と変換、公式そのもの
# ══════════════════════════════════════════════════════════
eq(to_rad(180), PI, "180° = π radian")
eq(to_rad(360), 2 * PI, "360° = 2π radian")
eq(to_deg(1), 180 / PI, "1 radian = 180/π 度")
chk(abs(float(to_deg(1)) - 57.2958) < 1e-3, "1 radian ≈ 57.3°")
# 表の値
for _d, _r in [(30, PI / 6), (45, PI / 4), (60, PI / 3), (90, PI / 2),
               (120, 2 * PI / 3), (180, PI), (270, 3 * PI / 2), (360, 2 * PI)]:
    eq(to_rad(_d), _r, f"{_d}° の radian")
in_text("| radian | $\\dfrac{\\pi}{6}$ | $\\dfrac{\\pi}{4}$ | $\\dfrac{\\pi}{3}$ | "
        "$\\dfrac{\\pi}{2}$ | $\\dfrac{2\\pi}{3}$ | $\\pi$ | $\\dfrac{3\\pi}{2}$ | "
        "$2\\pi$ |", "表の radian の行")
in_text("| 度 | $30°$ | $45°$ | $60°$ | $90°$ | $120°$ | $180°$ | $270°$ | $360°$ |",
        "表の度の行")
# 公式の同値性
_r, _t = sp.symbols("r theta", positive=True)
eq(sector(_r, _t), R(1, 2) * _r * arc(_r, _t), "A = ½ l r")
eq(_t / (2 * PI) * 2 * PI * _r, arc(_r, _t), "割合から l = rθ")
eq(_t / (2 * PI) * PI * _r ** 2, sector(_r, _t), "割合から A = ½r²θ")
eq(_t / 360 * 2 * PI * _r, PI * _r * _t / 180, "度で測ると πrθ/180")
chk(sp.solve(sp.Eq(arc(_r, _t), PI * _r * _t / 180), _t) == [],
    "度の式と radian の式は θ > 0 では一致しない")
# 本文の走る例
eq(to_rad(210), 7 * PI / 6, "本文 210° = 7π/6")
eq(to_deg(4 * PI / 9), 80, "本文 4π/9 = 80°")
eq(arc(4, PI / 6), 2 * PI / 3, "本文 弧 2π/3")
eq(sector(4, PI / 6), 4 * PI / 3, "本文 面積 4π/3")
in_text("l = 4 \\times \\frac{\\pi}{6} = \\frac{2\\pi}{3}", "本文の弧の例")
in_text("A = \\frac{1}{2} \\times 16 \\times \\frac{\\pi}{6} = \\frac{4\\pi}{3}",
        "本文の面積の例")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  変換
# ══════════════════════════════════════════════════════════
eq(to_rad(135), 3 * PI / 4, "例題1(a) 135° = 3π/4")
eq(to_deg(5 * PI / 6), 150, "例題1(b) 5π/6 = 150°")
eq(to_deg(2), 360 / PI, "例題1(c) 2 radian = 360/π 度")
eq(3 * PI / 4, PI - PI / 4, "例題1(a) 検算 π - π/4")
eq(to_rad(150), 5 * PI / 6, "例題1(b) 検算 逆向き")
chk(abs(float(360 / PI) - 114.59) < 0.01, "例題1(c) 検算 約 114.6°")
chk(float(to_deg(2)) < 180, "2 radian は 180° より小さい")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  r = 6, θ = π/3
# ══════════════════════════════════════════════════════════
eq(arc(6, PI / 3), 2 * PI, "例題2(a) 弧 2π")
eq(sector(6, PI / 3), 6 * PI, "例題2(b) 面積 6π")
eq(2 * 6 + arc(6, PI / 3), 12 + 2 * PI, "例題2(c) 周 12 + 2π")
eq(sector(12, PI / 3), 4 * sector(6, PI / 3), "例題2(d) 半径 2 倍で面積 4 倍")
eq((PI / 3) / (2 * PI), R(1, 6), "例題2 検算 円の 1/6")
eq(2 * PI * 6 / 6, 2 * PI, "例題2(a) 検算 円周の 1/6")
eq(PI * 36 / 6, 6 * PI, "例題2(b) 検算 円の面積の 1/6")
eq(R(1, 2) * (2 * PI) * 6, 6 * PI, "例題2(b) 検算 ½lr")
chk(float(2 * PI) > 6, "例題2(c) 検算 弧は弦 6 より長い")
eq(to_deg(PI / 3), 60, "π/3 = 60° なので弦は正三角形の辺")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  r = 4, l = 10
# ══════════════════════════════════════════════════════════
_th3 = sp.solve(sp.Eq(arc(4, _t), 10), _t)
chk(_th3 == [R(5, 2)], f"例題3(a) θ = 2.5: {_th3}")
eq(sector(4, R(5, 2)), 20, "例題3(b) 面積 20")
eq(to_deg(R(5, 2)), 450 / PI, "例題3(c) 450/π 度")
eq(R(1, 2) * 10 * 4, 20, "例題3(b) 検算 ½lr")
chk(float(PI / 2) < 2.5 < float(PI), "例題3(a) 検算 π/2 < 2.5 < π")
chk(abs(float(2 * PI * 4 / 4) - 6.28) < 0.01, "四分円の弧は約 6.3")
chk(abs(float(2 * PI * 4 / 2) - 12.57) < 0.01, "半円の弧は約 12.6")
chk(abs(float(450 / PI) - 143.2) < 0.1, "例題3(c) 検算 約 143°")
chk(90 < float(450 / PI) < 180, "143° は 90° と 180° のあいだ")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  r = 8, θ = 2π/3
# ══════════════════════════════════════════════════════════
eq(arc(8, 2 * PI / 3), 16 * PI / 3, "例題4(a) 弧 16π/3")
eq(sector(8, 2 * PI / 3), 64 * PI / 3, "例題4(b) 扇形 64π/3")
eq(R(1, 2) * 64 * sp.sin(2 * PI / 3), 16 * sp.sqrt(3), "例題4(c) 三角形 16√3")
eq(segment(8, 2 * PI / 3), 64 * PI / 3 - 16 * sp.sqrt(3), "例題4(c) 弓形")
eq(sp.sin(2 * PI / 3), sp.sqrt(3) / 2, "sin(2π/3) = √3/2")
eq(to_deg(2 * PI / 3), 120, "2π/3 = 120°")
eq((2 * PI / 3) / (2 * PI), R(1, 3), "例題4 検算 円の 1/3")
eq(2 * PI * 8 / 3, 16 * PI / 3, "例題4(a) 検算 円周の 1/3")
eq(PI * 64 / 3, 64 * PI / 3, "例題4(b) 検算 円の面積の 1/3")
chk(float(segment(8, 2 * PI / 3)) > 0, "例題4(c) 検算 弓形は正")
chk(float(segment(8, 2 * PI / 3)) < float(sector(8, 2 * PI / 3)),
    "例題4(c) 検算 弓形は扇形より小さい")
chk(abs(float(64 * PI / 3) - 67.02) < 0.02, "扇形は約 67")
chk(abs(float(16 * sp.sqrt(3)) - 27.71) < 0.02, "三角形は約 27.7")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(to_rad(100), 5 * PI / 9, "演習1 5π/9")
chk(float(PI / 2) < float(5 * PI / 9) < float(PI), "演習1 検算 π/2 と π のあいだ")
eq(to_rad(90), R(45, 10) * PI / 9, "演習1 検算 90° = 4.5π/9")
eq(to_deg(5 * PI / 4), 225, "演習2 225°")
eq(5 * PI / 4, PI + PI / 4, "演習2 検算 π + π/4")
eq(180 + 45, 225, "演習2 検算 180 + 45")
eq(arc(5, R(12, 10)), 6, "演習3 弧 6")
chk(abs(float(2 * PI * 5) - 31.42) < 0.01, "演習3 検算 円周は約 31.4")
chk(abs(float(R(12, 10) / (2 * PI)) - 0.191) < 0.001, "演習3 検算 割合は約 0.19")
eq(sector(10, PI / 5), 10 * PI, "演習4 面積 10π")
eq((PI / 5) / (2 * PI), R(1, 10), "演習4 検算 円の 1/10")
eq(PI * 100 / 10, 10 * PI, "演習4 検算 円の面積の 1/10")
_th5 = sp.solve(sp.Eq(arc(8, _t), 12), _t)
chk(_th5 == [R(3, 2)], f"演習5 θ = 1.5: {_th5}")
chk(float(R(3, 2)) < float(PI / 2), "演習5 検算 1.5 < π/2")
chk(abs(float(2 * PI * 8 / 4) - 12.57) < 0.01, "演習5 検算 四分円の弧は約 12.6")
_th6 = sp.solve(sp.Eq(sector(4, _t), 24), _t)
chk(_th6 == [3], f"演習6 θ = 3: {_th6}")
eq(R(1, 2) * arc(4, 3) * 4, 24, "演習6 検算 ½lr で 24")
eq(arc(4, 3), 12, "演習6 検算 弧は 12")
chk(3 < float(PI), "演習6 検算 3 < π なので半円より小さい")
eq(2 * 6 + arc(6, PI / 2), 12 + 3 * PI, "演習7 周 12 + 3π")
eq(arc(6, PI / 2), 3 * PI, "演習7 弧 3π")
eq(2 * PI * 6 / 4, 3 * PI, "演習7 検算 円周の 1/4")
chk(float(180 / PI) < 60, "演習8 1 radian < 60°")
chk(float(PI) > 3, "演習8 π > 3")
eq(R(180, 3), 60, "演習8 180/3 = 60")
chk(float(PI / 3) > 1, "演習8 π/3 > 1")
eq(segment(4, PI / 2), 4 * PI - 8, "演習9 弓形 4π - 8")
eq(sector(4, PI / 2), 4 * PI, "演習9 扇形 4π")
eq(R(1, 2) * 16 * sp.sin(PI / 2), 8, "演習9 三角形 8")
eq(R(1, 2) * 4 * 4, 8, "演習9 検算 直角三角形として 8")
chk(sp.sin(PI / 2) == 1, "sin(π/2) = 1")
chk(float(4 * PI - 8) > 0, "演習9 検算 弓形は正")
eq(to_rad(40), 2 * PI / 9, "演習10 40° = 2π/9")
eq(arc(9, to_rad(40)), 2 * PI, "演習10 弧 2π")
eq(R(40, 360), R(1, 9), "演習10 検算 円の 1/9")
eq(2 * PI * 9 / 9, 2 * PI, "演習10 検算 円周の 1/9")
chk(9 * 40 == 360, "演習10 生徒の計算は 360")
chk(360 > float(2 * PI * 9), "演習10 検算 360 は円周より長い")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("3\\pi}{4}", "例題1(a)"), ("150°", "例題1(b)"),
                ("360}{\\pi}", "例題1(c)"), ("6\\pi$", "例題2(b)"),
                ("12 + 2\\pi", "例題2(c)"), ("450}{\\pi}", "例題3(c)"),
                ("16\\pi}{3}", "例題4(a)"), ("64\\pi}{3}", "例題4(b)"),
                ("16\\sqrt{3}", "例題4(c)"), ("5\\pi}{9}", "演習1"),
                ("225°", "演習2"), ("10\\pi$", "演習4"),
                ("12 + 3\\pi", "演習7"), ("4\\pi - 8", "演習9"),
                ("2\\pi}{9}", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **3.4** の欄に `Length of an arc` として印刷されています。", "弧の欄")
in_text("> $l = r\\theta$, where $r$ is the radius, $\\theta$ is the angle measured "
        "in radians", "弧を逐語で")
in_text("公式集の **3.4** の欄に `Area of a sector` として印刷されています。", "扇形の欄")
in_text("> $A = \\dfrac{1}{2}r^2\\theta$, where $r$ is the radius, $\\theta$ is the "
        "angle measured in radians", "扇形を逐語で")
# ★ 答案の書き方を縛る一文だけを引く
in_text("> On examination papers, radian measure should be assumed unless otherwise "
        "indicated.", "radian を仮定する一文")
chk(TEXT.count("\n> ") == 3, f"引用は公式集 2 つ + 冒頭の一文 1 つ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 2, "公式集の callout は 2 つ")
not_in_text("The circle: radian measure of angles", "シラバス本文は引かない")
not_in_text("Radian measure may be expressed as exact multiples", "Guidance は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("**この表は公式集にはありません。**", "変換表は公式集にない")
in_text("**この式は公式集にはありません。**", "弓形の式は公式集にない")
in_text("**$\\pi$ を使った正確な形でも、小数でもかまいません。**", "答えの形")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("**半径 $r$ の円で、長さ $r$ の弧を切り取る中心角**が、**$1$ radian** です。",
        "radian の定義")
in_text("円はどれも相似なので、**弧の長さと半径の比は、円の大きさによりません。**",
        "radian は円の大きさによらない")
in_text("**この約分が起きるのは、$\\theta$ を radian で測っているからです。**",
        "radian を使う理由")
in_text("**radian には単位記号を付けません。**", "単位記号")
in_text("**この分け方ができるのは $0 < \\theta < \\pi$ のときです。**",
        "弓形の式の適用範囲")
in_text("## 度のまま $l = r\\theta$ に入れる", "度のままの注意")
in_text("## $\\frac{1}{2}r^{2}\\theta$ で $r$ を $2$ 乗し忘れる", "2 乗の注意")
in_text("## 扇形の周を、弧の長さだけにする", "周の注意")

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
in_text("**`3.14` と打ち込まないでください。**", "π のキーを使う")
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
chk(len(re.findall(r"^::: \{#exm-aasl34-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl34", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
_T32 = open(os.path.join(BASE, "aasl-3-2.qmd"), encoding="utf-8").read()
for _a2 in set(re.findall(r"\]\(aasl-3-2\.qmd#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a2 + "}") in _T32, "3.2 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl34-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl34-common", "eq-aasl34-turn", "eq-aasl34-half",
             "eq-aasl34-convert", "eq-aasl34-arc", "eq-aasl34-sector",
             "eq-aasl34-half-lr", "eq-aasl34-segment"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
for _lab in ["tbl-aasl34-common", "eq-aasl34-turn", "eq-aasl34-convert",
             "eq-aasl34-arc", "eq-aasl34-sector", "eq-aasl34-half-lr",
             "eq-aasl34-segment"]:
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
SVG = os.path.join(BASE, "img", "aasl-3-4-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-4-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) One radian", "図(a) の題")
in_fig("the angle at the centre cut off by an arc", "図(a) の説明")
in_fig("as long as the radius is one radian", "図(a) の説明（続き）")
in_fig("arc of length $r$", "図(a) のラベル")
in_fig("a whole turn is $2\\\\pi$ radians", "図(a) の一周")
in_fig("(b) Sector and segment", "図(b) の題")
in_fig("arc $l = r\\\\theta$", "図(b) の弧")
in_fig("sector $A = \\\\frac{1}{2}r^{2}\\\\theta$", "図(b) の面積")
in_fig("segment", "図(b) の弓形")
in_fig("the chord cuts the sector into a triangle", "図(b) の説明")
in_fig("both formulas need $\\\\theta$ in radians", "図(b) の但し書き")
in_text("(a) In a circle of radius $r$, an arc of length $r$ cuts off an angle of "
        "one radian at the centre", "キャプションが (a) を説明")
in_text("(b) For a sector of radius $r$ and angle $\\theta$ in radians",
        "キャプションが (b) を説明")
chk(set(re.findall(r"\d+", FIGSTR)) <= {"1", "2"},
    f"図の数字は 1 と 2 だけ: {set(re.findall(chr(92) + 'd+', FIGSTR))}")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-4.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-3.qmd") < DRAFT.index("aasl-3-4.qmd"), "並びが 3.3 → 3.4")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-4.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| radian |", "| arc |", "| sector |", "| segment |", "| chord |",
           "| perimeter |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- θ > π のとき、弦は扇形を 2 つに分けない -----------------------------
chk(float(sp.sin(3 * PI / 2)) < 0, "π < θ < 2π では sin θ が負")
eq(segment(1, 3 * PI / 2), R(3, 4) * PI + R(1, 2), "θ = 3π/2 の式の値")
eq(sector(1, 3 * PI / 2) + R(1, 2) * 1 ** 2 * sp.sin(PI / 2),
   R(3, 4) * PI + R(1, 2), "θ = 3π/2 では扇形 + 三角形")
# 弦の中点が、優弧側の扇形の外にあること（r = 1, θ = 3π/2）
_mx, _my = (sp.cos(0) + sp.cos(3 * PI / 2)) / 2, (sp.sin(0) + sp.sin(3 * PI / 2)) / 2
chk(_mx > 0 and _my < 0, f"弦の中点は第 4 象限: ({_mx}, {_my})")
chk(not (0 <= float(sp.atan2(_my, _mx)) <= float(3 * PI / 2)),
    "弦の中点は θ = 0 から 3π/2 の扇形の外")
in_text("$\\theta$ が $\\pi$ より大きいときは、弦は扇形の**外**を通るので、"
        "扇形は三角形と弓形には分かれません。", "θ > π では分かれない")
in_text("大きいほうの弓形がほしいときは、**円全体から小さいほうの弓形を引きます。**",
        "大きいほうの弓形の出しかた")
in_text("$\\theta = \\pi$ なら三角形がつぶれて、弓形はちょうど半円になります。",
        "θ = π のとき")
not_in_text("$\\theta$ が $\\pi$ より大きいときも、弦は扇形を $2$ つに分ける",
            "まちがった但し書きは消した")

# --- radian が円の大きさによらないこと -----------------------------------
in_text("だから、どの円で測っても同じ角になります。", "どの円でも同じ")
not_in_text("半径が変わっても、この定義は変わりません。", "同語反復は消した")

# --- 例題1(d) を θ > 0 で言う --------------------------------------------
in_text("For a sector we have $r > 0$ and $\\theta > 0$", "r > 0, θ > 0 と書いた")
not_in_text("The two agree only if $\\theta = 0$", "退化した場合に頼る言い方は消した")

# --- command term を Find にそろえた -------------------------------------
chk(TEXT.count("[Write ") == 0, f"Write で始まる設問はない: {TEXT.count('[Write ')}")
chk(TEXT.count("Find the size, in radians,") == 2, "radians を Find で 2 か所")
chk(TEXT.count("Find the size, in degrees,") == 3, "degrees を Find で 3 か所")
chk(TEXT.count("in terms of $\\pi$") == 2, "in terms of π が 2 か所")

# --- 扇形の周を本文で教えた ----------------------------------------------
in_text("扇形の **perimeter**（周の長さ）は、**弧 $1$ 本と半径 $2$ 本**を足したものです。",
        "周を本文で教える")
in_text("$$\n\\text{perimeter} = 2r + l = 2r + r\\theta\n$$ {#eq-aasl34-perimeter}",
        "周の式にラベル")
chk("{#eq-aasl34-perimeter}" in TEXT, "eq-aasl34-perimeter がある")
in_text("- 扇形の **perimeter**（周の長さ）が $2r + l$ であることを使える。",
        "できることに周を足した")
eq(2 * 6 + arc(6, PI / 3), 12 + 2 * PI, "周の式は例題2(c) と合う")
eq(2 * 6 + arc(6, PI / 2), 12 + 3 * PI, "周の式は演習7 と合う")

# --- sector / arc / perimeter を英語が先で出した -------------------------
in_text("**sector**（扇形）", "sector を英語が先で")
in_text("**arc**（弧）", "arc を英語が先で")
in_text("**perimeter**（周の長さ）", "perimeter を英語が先で")

# --- 例題3(d) を、半径を出す形にした -------------------------------------
in_text("Explain why its radius must be $\\dfrac{2A}{l}$", "例題3(d) は半径")
in_text("so $l > 0$ and we may divide by $l$: $r = \\dfrac{2A}{l}$.*", "l で割ってよい")
not_in_text("Explain why the area of any sector is equal to $\\dfrac{1}{2}lr$",
            "本文に答えのある設問は消した")
_A, _l = sp.symbols("A_ l_", positive=True)
eq(sp.solve(sp.Eq(_A, R(1, 2) * _l * sp.Symbol("r_", positive=True)),
            sp.Symbol("r_", positive=True))[0], 2 * _A / _l, "r = 2A/l")

# --- 演習6 を、半径を求める形にした --------------------------------------
in_text("[6]{.ex-no} [A sector of a circle has angle $3$ radians and area $24$ cm$^{2}$. "
        "Find the radius of the sector.", "演習6 は半径")
_r6 = sp.solve(sp.Eq(sector(sp.Symbol("r6", positive=True), 3), 24),
               sp.Symbol("r6", positive=True))
chk(_r6 == [4], f"演習6 r = 4: {_r6}")
eq(R(3, 2) * 16, 24, "演習6 3r²/2 = 24")
in_text("$r$ は長さなので、$r^{2} = 16$ から取るのは**正のほうだけ**です。", "正の根だけ")
not_in_text("A sector of a circle has radius $4$ cm and area $24$ cm$^{2}$",
            "古い演習6 は消した")

# --- 検算を、独立した道すじ・手計算でできる形にした -----------------------
in_text("**四分円とくらべます。** $\\theta = \\dfrac{\\pi}{2} \\approx 1.57$ のとき、"
        "弧は円周 $10\\pi \\approx 31.4$ の $\\dfrac{1}{4}$ で約 $7.9$ です。", "演習3 の検算")
not_in_text("\\dfrac{1.2}{2\\pi} \\approx \\dfrac{1.2}{6.28}", "電卓が要る検算は消した")
chk(abs(float(2 * PI * 5 / 4) - 7.854) < 0.01, "四分円の弧は約 7.9")
in_text("**弧だけなら $9.4$ にしかなりません。**", "演習7 の検算は周そのもの")
eq(sp.sqrt(6 ** 2 + 6 ** 2), 6 * sp.sqrt(2), "演習7 検算 弦は 6√2")
chk(abs(float(6 * sp.sqrt(2)) - 8.49) < 0.01, "6√2 ≈ 8.5")
chk(float(12 + 3 * PI) > 12 + float(6 * sp.sqrt(2)), "周は 12 + 弦 より大きい")
in_text("だから周は $12 + 6 = 18$ より大きく", "例題2(c) の検算は周そのもの")
chk(abs(float(12 + 2 * PI) - 18.28) < 0.01, "12 + 2π ≈ 18.3")
in_text("**$1$ radian $= \\dfrac{180}{\\pi} \\approx 57.3°$ で見ます。**",
        "57.3° の出どころを書いた")
chk(TEXT.count("$1$ radian が約 $57°$") == 0, "根拠のない 57° は消した")

# --- 演習8 の解答例に結論を書いた ----------------------------------------
in_text("so $1$ radian $< 60°$.*", "演習8 の結論")

# --- どちらの弓形かを書いた ----------------------------------------------
chk(TEXT.count("smaller segment") == 2, f"smaller segment が 2 か所: {TEXT.count('smaller segment')}")
in_text("**小さいほうの**弓形の面積", "例題4(c) の日本語訳")
not_in_text("[Find the exact area of the segment cut off by the chord",
            "どちらか分からない言い方は消した")
# 例題4：小さいほうが正しく小さいこと
chk(float(segment(8, 2 * PI / 3)) < float(PI * 64 - segment(8, 2 * PI / 3)),
    "例題4(c) は小さいほうの弓形")
chk(float(segment(4, PI / 2)) < float(PI * 16 - segment(4, PI / 2)),
    "演習9 も小さいほうの弓形")

# --- 演習9 の英文を、例題4 と同じ形にした --------------------------------
in_text("[A circle has centre $\\mathrm{O}$ and radius $4$ cm. The points $\\mathrm{A}$ "
        "and $\\mathrm{B}$ lie on the circle", "演習9 の英文")
not_in_text("A chord joins two points on the circle for which the angle at the centre",
            "読みにくい英文は消した")

# --- 正確な値の出どころ --------------------------------------------------
in_text("（[SL 3.2 の正確な値](aasl-3-2.qmd#ratios)）", "正確な値は 3.2 の第 1 節")
chk(TEXT.count("aasl-3-2.qmd#area") == 1, "面積の式へのリンクは 1 か所だけ")

# --- 見分けかたを断定にしない --------------------------------------------
in_text("かけ算の向きを取りちがえた可能性が高いので、もう一度見てください。", "断定を避けた")
not_in_text("$3$ くらいの数が出たら、かけ算の向きが逆です。", "断定は消した")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
