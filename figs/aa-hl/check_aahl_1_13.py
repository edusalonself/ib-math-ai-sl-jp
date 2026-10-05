"""AA HL 1.13（極形式・Euler 形、積と商）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_13.py
"""
import glob
import os
import re
import sys

import sympy as sp
from sympy import I, pi
from sympy import Rational as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-13.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_13.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
th, th1, th2 = sp.symbols("theta theta_1 theta_2", real=True)
r1, r2 = sp.symbols("r_1 r_2", positive=True)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + "  (%s vs %s)" % (u, v))


def ne(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) != 0, msg + "  (%s vs %s)" % (u, v))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def cart(r, t):
    return sp.simplify(sp.expand(r * (sp.cos(t) + I * sp.sin(t))))


# ══════════════════════════════════════════════════════════
# 0. 記号のままの恒等式
# ══════════════════════════════════════════════════════════
eq(sp.expand(sp.cos(th) + I * sp.sin(th)), sp.exp(I * th).rewrite(sp.cos),
   "cosθ + i sinθ = e^{iθ}")
# 積：長さは掛け算、角は足し算
_lhs = (r1 * (sp.cos(th1) + I * sp.sin(th1))) * (r2 * (sp.cos(th2) + I * sp.sin(th2)))
_rhs = r1 * r2 * (sp.cos(th1 + th2) + I * sp.sin(th1 + th2))
chk(sp.simplify(sp.expand(_lhs) - sp.expand(_rhs)) == 0, "積の公式（記号のまま）")
# 商
_lq = (r1 * (sp.cos(th1) + I * sp.sin(th1))) / (r2 * (sp.cos(th2) + I * sp.sin(th2)))
_rq = (r1 / r2) * (sp.cos(th1 - th2) + I * sp.sin(th1 - th2))
chk(sp.simplify(_lq - _rq) == 0, "商の公式（記号のまま）")
# 加法定理が効いている
eq(sp.expand(sp.cos(th1) * sp.cos(th2) - sp.sin(th1) * sp.sin(th2)),
   sp.expand(sp.cos(th1 + th2)), "実部は cos(θ1+θ2)")
eq(sp.expand(sp.sin(th1) * sp.cos(th2) + sp.cos(th1) * sp.sin(th2)),
   sp.expand(sp.sin(th1 + th2)), "虚部は sin(θ1+θ2)")
# |z1z2| = |z1||z2|
for _a in [1 + I, 3 - 2 * I, -4 * I, -1 - I]:
    for _b in [2 + I, -3 + I, 5, I]:
        eq(sp.Abs(sp.expand(_a * _b)), sp.Abs(_a) * sp.Abs(_b),
           "|z1z2| = |z1||z2|: %s, %s" % (_a, _b))
# cosθ - i sinθ = cos(-θ) + i sin(-θ)
eq(sp.cos(th) - I * sp.sin(th), sp.cos(-th) + I * sp.sin(-th), "符号の直し方")
# -r e^{iθ} = r e^{i(θ+π)}
eq(sp.expand(-2 * (sp.cos(pi / 3) + I * sp.sin(pi / 3))),
   cart(2, pi / 3 + pi), "-2e^{iπ/3} = 2e^{i(π/3+π)}")
eq(cart(2, pi / 3 + pi), cart(2, -2 * pi / 3), "= 2e^{-i2π/3}")
eq(sp.exp(I * pi), -1, "e^{iπ} = -1")
eq(sp.exp(I * pi) + 1, 0, "Euler の等式")
eq(sp.exp(I * pi / 2), I, "i = e^{iπ/2}")

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
eq(cart(2, pi / 3), 1 + sp.sqrt(3) * I, "§1 2(cos π/3 + i sin π/3)")
eq(sp.cos(pi / 3), R(1, 2), "cos π/3 = 1/2")
eq(sp.sin(pi / 3), sp.sqrt(3) / 2, "sin π/3 = √3/2")
eq(sp.Abs(4 * I), 4, "§3 |4i| = 4")
eq(sp.arg(4 * I), pi / 2, "§3 arg(4i) = π/2")
eq(cart(4, pi / 2), 4 * I, "§3 戻すと 4i")
eq(sp.expand(cart(2, pi / 3) * cart(3, pi / 6)), 6 * I, "§4 積は 6i")
eq(cart(6, pi / 2), 6 * I, "§4 6e^{iπ/2} = 6i")
eq(pi / 3 + pi / 6, pi / 2, "§4 角の和")
eq(2 * 3, 6, "§4 長さの積")
eq(3 * pi / 4 + 3 * pi / 4, 3 * pi / 2, "§4 範囲を出る例")
eq(3 * pi / 2 - 2 * pi, -pi / 2, "§4 2π を引いて主値に")
eq(sp.simplify(cart(2, pi / 3) / cart(3, pi / 6)), cart(R(2, 3), pi / 6),
   "§5 商は (2/3)e^{iπ/6}")
eq(pi / 3 - pi / 6, pi / 6, "§5 角の差")
eq(sp.expand(I * (3 + 2 * I)), -2 + 3 * I, "§6 i(3+2i) = -2+3i")
eq(sp.Abs(3 + 2 * I), sp.Abs(-2 + 3 * I), "§6 長さは変わらない")
chk(abs(float(sp.arg(-2 + 3 * I) - sp.arg(3 + 2 * I)) - float(pi / 2)) < 1e-12,
    "§6 角が π/2 増える")
eq((3 + 2 * I) + (1 + 4 * I), 4 + 6 * I, "§7 和")

# ══════════════════════════════════════════════════════════
# 2. 例題 1〜4
# ══════════════════════════════════════════════════════════
eq(sp.Abs(1 - I), sp.sqrt(2), "例題1 r = √2")
eq(sp.arg(1 - I), -pi / 4, "例題1 θ = -π/4")
eq(cart(sp.sqrt(2), -pi / 4), 1 - I, "例題1 検算：戻る")
eq(sp.expand((1 - I) * (1 + I)), 2, "例題1 zz* = 2")
ne(cart(sp.sqrt(2), pi / 4), 1 - I, "θ = π/4 なら 1+i になってしまう")
eq(cart(sp.sqrt(2), pi / 4), 1 + I, "その誤答は 1+i")

eq(cart(6, 5 * pi / 6), -3 * sp.sqrt(3) + 3 * I, "例題2")
eq(sp.cos(5 * pi / 6), -sp.sqrt(3) / 2, "cos 5π/6")
eq(sp.sin(5 * pi / 6), R(1, 2), "sin 5π/6")
eq(sp.Abs(-3 * sp.sqrt(3) + 3 * I), 6, "例題2 検算：|z| = 6")
eq(sp.simplify(3 / (-3 * sp.sqrt(3))), -1 / sp.sqrt(3), "例題2 検算：b/a")
eq(sp.simplify(sp.tan(5 * pi / 6)), -1 / sp.sqrt(3), "tan 5π/6 = -1/√3")
eq(27 + 9, 36, "例題2 27+9 = 36")

eq(pi / 4 + pi / 12, pi / 3, "例題3(a) 角の和")
eq(pi / 4 - pi / 12, pi / 6, "例題3(b) 角の差")
eq(sp.expand(cart(4, pi / 4) * cart(2, pi / 12)), cart(8, pi / 3), "例題3(a)")
eq(sp.simplify(cart(4, pi / 4) / cart(2, pi / 12)), cart(2, pi / 6), "例題3(b)")
eq(cart(8, pi / 3), 4 + 4 * sp.sqrt(3) * I, "例題3 検算：a+bi")
eq(sp.Abs(4 + 4 * sp.sqrt(3) * I), 8, "例題3 検算：|z| = 8")
eq(16 + 48, 64, "16+48 = 64")
eq(sp.simplify(cart(8, pi / 3) / cart(2, pi / 6)), cart(4, pi / 6),
   "例題3 検算：(a)÷(b)")
eq(sp.expand(cart(2, pi / 12) ** 2), cart(4, pi / 6), "例題3 検算：= z2^2")
ne(pi / 8, pi / 3, "通分を忘れた誤答は合わない")

eq(pi / 6 + pi / 2, 2 * pi / 3, "例題4(a) 角の和")
eq(cart(3, 2 * pi / 3), R(-3, 2) + 3 * sp.sqrt(3) * I / 2, "例題4(b)")
eq(sp.expand(I * cart(3, pi / 6)), cart(3, 2 * pi / 3), "例題4 検算：iz")
eq(cart(3, pi / 6), 3 * sp.sqrt(3) / 2 + R(3, 2) * I, "例題4 z の a+bi")
eq(sp.Abs(cart(3, 2 * pi / 3)), 3, "例題4 検算：|w| = 3")
eq(R(9, 4) + R(27, 4), 9, "9/4 + 27/4 = 9")

# ══════════════════════════════════════════════════════════
# 3. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(sp.Abs(3 + 3 * I), 3 * sp.sqrt(2), "演習1 r")
eq(sp.arg(3 + 3 * I), pi / 4, "演習1 θ")
eq(cart(3 * sp.sqrt(2), pi / 4), 3 + 3 * I, "演習1 検算")
eq(sp.sqrt(18), 3 * sp.sqrt(2), "√18 = 3√2")

eq(sp.Abs(-5 * I), 5, "演習2 r")
eq(sp.arg(-5 * I), -pi / 2, "演習2 θ")
eq(cart(5, -pi / 2), -5 * I, "演習2 検算")
chk(not (-pi < 3 * pi / 2 <= pi), "3π/2 は範囲の外")

eq(cart(4, pi / 3), 2 + 2 * sp.sqrt(3) * I, "演習3")
eq(sp.Abs(2 + 2 * sp.sqrt(3) * I), 4, "演習3 検算")
eq(4 + 12, 16, "4+12 = 16")
eq(cart(4, pi / 6), 2 * sp.sqrt(3) + 2 * I, "演習3 誤答（cos と sin の取りちがえ）")
eq(sp.Abs(2 * sp.sqrt(3) + 2 * I), 4, "その誤答も絶対値は 4")

eq(cart(2, 3 * pi / 4), -sp.sqrt(2) + sp.sqrt(2) * I, "演習4")
eq(sp.simplify(2 / sp.sqrt(2)), sp.sqrt(2), "2/√2 = √2")
eq(sp.Abs(-sp.sqrt(2) + sp.sqrt(2) * I), 2, "演習4 検算")

eq(5 * pi / 12 + pi / 4, 2 * pi / 3, "演習5(a) 角の和")
eq(5 * pi / 12 - pi / 4, pi / 6, "演習5(b) 角の差")
eq(sp.expand(cart(6, 5 * pi / 12) * cart(2, pi / 4)), cart(12, 2 * pi / 3),
   "演習5(a)")
eq(sp.simplify(cart(6, 5 * pi / 12) / cart(2, pi / 4)), cart(3, pi / 6),
   "演習5(b)")
eq(sp.simplify(cart(12, 2 * pi / 3) / cart(3, pi / 6)), cart(4, pi / 2),
   "演習5 検算：(a)÷(b)")
eq(sp.expand(cart(2, pi / 4) ** 2), cart(4, pi / 2), "演習5 検算：= z2^2")

_q6 = sp.expand((1 + I) * (sp.sqrt(3) + I))
eq(sp.Abs(_q6), 2 * sp.sqrt(2), "演習6 |z|")
eq(sp.simplify(sp.arg(_q6) - 5 * pi / 12), 0, "演習6 arg z = 5π/12")
eq(pi / 4 + pi / 6, 5 * pi / 12, "演習6 角の和")
eq(sp.Abs(1 + I) * sp.Abs(sp.sqrt(3) + I), 2 * sp.sqrt(2), "演習6 検算：積")
eq(sp.expand(_q6), (sp.sqrt(3) - 1) + (sp.sqrt(3) + 1) * I, "演習6 展開")
eq(sp.expand((sp.sqrt(3) - 1) ** 2 + (sp.sqrt(3) + 1) ** 2), 8, "演習6 |z|^2 = 8")
eq(sp.simplify((sp.sqrt(3) + 1) / (sp.sqrt(3) - 1)), 2 + sp.sqrt(3), "演習6 b/a")
eq(sp.simplify(sp.tan(5 * pi / 12)), 2 + sp.sqrt(3), "tan 5π/12 = 2+√3")

eq(2 * pi / 3 - pi / 6, pi / 2, "演習7 角の差")
eq(sp.simplify(cart(8, 2 * pi / 3) / cart(4, pi / 6)), 2 * I, "演習7")
eq(cart(2, pi / 2), 2 * I, "演習7 2e^{iπ/2} = 2i")
eq(sp.expand(cart(2, pi / 2) * cart(4, pi / 6)), cart(8, 2 * pi / 3),
   "演習7 検算：戻す")
eq(cart(2, -pi / 2), -2 * I, "演習7 向きを逆にした誤答は -2i")

eq(sp.expand((3 + 2 * I) * (1 - I)), 5 - I, "演習8 例：積は 5-i")
eq(sp.Abs(5 - I), sp.sqrt(26), "演習8 例：|5-i| = √26")
eq(sp.sqrt(13) * sp.sqrt(2), sp.sqrt(26), "√13 × √2 = √26")

eq(pi / 3 - pi / 2, -pi / 6, "演習9 時計回りは引き算")
eq(cart(5, -pi / 6), 5 * sp.sqrt(3) / 2 - R(5, 2) * I, "演習9")
eq(sp.Abs(cart(5, -pi / 6)), 5, "演習9 検算：長さは変わらない")
eq(R(75, 4) + R(25, 4), 25, "75/4 + 25/4 = 25")
eq(pi / 3 + pi / 2, 5 * pi / 6, "演習9 向きを逆にした誤答の角")

eq(pi / 4 + pi / 4, pi / 2, "演習10 正しい角")
eq(sp.expand(cart(5, pi / 4) * cart(2, pi / 4)), 10 * I, "演習10 正しい答え")
eq(cart(10, pi / 2), 10 * I, "演習10 10e^{iπ/2} = 10i")
ne(pi ** 2 / 16, pi / 2, "生徒の角はちがう")
eq(5 * 2, 10, "演習10 絶対値は合っている")
eq(sp.expand((1 + I) ** 2), 2 * I, "演習10 検算：(1+i)^2 = 2i")
eq(sp.simplify(R(10, 2) * (1 + I) ** 2), 10 * I, "演習10 検算：a+bi で 10i")

# ══════════════════════════════════════════════════════════
# 4. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.13** の欄に、$3$ つの形が $1$ 行に並べて印刷されています。",
        "公式集にある")
in_text("> Modulus-argument (polar) and exponential (Euler) form", "見出しを逐語で")
in_text("> $z = r(\\cos\\theta + i\\sin\\theta) = re^{i\\theta}"
        " = r\\,\\mathrm{cis}\\,\\theta$", "公式集の式を逐語で")
in_text("> The ability to convert between Cartesian, modulus-argument (polar)"
        " and Euler form is expected.", "Guidance を逐語で")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
# cis は 1 度だけ紹介する（_AA-HL-PLAN.md 決まったこと 2）
# cis は The idea の中（紹介と公式集の引用）だけに置く
_after_idea = TEXT[TEXT.index(chr(10) + "## Why it works" + chr(10)):]
chk("\\mathrm{cis}" not in _after_idea,
    "cis は The idea より後には出さない")
chk(TEXT.count("\\mathrm{cis}") <= 4,
    "cis の登場は最小限: %d" % TEXT.count("\\mathrm{cis}"))
in_text("## $r\\,\\mathrm{cis}\\,\\theta$ という短い書き方もあります", "cis の紹介")
in_text("**この本では $r(\\cos\\theta + i\\sin\\theta)$ と $re^{i\\theta}$ を使います。**",
        "主に使う形を決めてある")

# ══════════════════════════════════════════════════════════
# 5. GDC / 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB"]:
    not_in_text(_m, "他機種: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl113-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)] == list(range(1, 8)),
    "The idea が 1..7 で連番")
chk(TEXT.count("**検算") >= 12, "検算が十分ある: %d" % TEXT.count("**検算"))
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
_ce = TEXT[TEXT.index("\n## Common errors"):TEXT.index("\n## Exercises")]
chk(_ce.count("::: {.callout-warning}") == 6, "Common errors が 6 つ")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    chk(not re.search(r"[ぁ-んァ-ン一-龥]",
                      _blk.replace("**試験ではこう書く**", "")),
        "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aahl113", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
chk(len(re.findall(r"\]\(aahl-1-12\.qmd", TEXT)) >= 4, "HL 1.12 へのリンク")
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head, "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は 1 つだけ")
not_in_text("**この節ですること：", "節の頭の 1 文は置かない")
not_in_text("\\vec{", "ベクトルの記号は太字")
chk(len(re.findall(r"^::: ", TEXT, re.M)) == len(re.findall(r"^:::$", TEXT, re.M)),
    "::: の開閉が一致")
for _h in re.findall(r"^#{1,4} .+$", TEXT, re.M):
    chk(not re.search(r"\$\s*—", _h), "見出しで数式の直後に —: " + _h)
for _line in TEXT.splitlines():
    if _line.startswith("|") and _line.endswith("|") and not re.fullmatch(r"[|:\- ]+", _line):
        for _cell in _line[1:-1].split(" | "):
            chk("|" not in _cell or "\\lvert" in _cell or "\\rvert" in _cell,
                "表のセルの中の裸の | :: " + _line[:60])
_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_j = TEXT.index(chr(10) + "## Worked examples", _i)
_wiw = TEXT[_i:_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
# ★ The idea の見出しは「英語（日本語）」の形（_AA-HL-PLAN.md の「決まったこと」5）
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)
in_text("### 1. Modulus–argument form（極形式） {#polar}", "見出し 1")
in_text("### 2. Euler form（Euler 形） {#euler}", "見出し 2")
in_text("### 3. Converting between the forms（形のあいだを行き来する） {#convert}", "見出し 3")
in_text("### 4. Multiplication: multiply the moduli, add the "
        "arguments（掛け算：長さはかけ算、角は足し算） {#product}", "見出し 4")
in_text("### 5. Division: divide the moduli, subtract the "
        "arguments（割り算：長さは割り算、角は引き算） {#quotient}", "見出し 5")
in_text("### 6. Rotation and enlargement（図形的な意味：回転と拡大） {#geometry}", "見出し 6")
in_text("### 7. Addition is done in Cartesian form（足し算は $a+bi$ の形で） "
        "{#sums}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 6. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-1-13-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-1-13-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Multiplying: the arguments add, the moduli multiply", "図(a) の題")
in_fig("modulus $r_1r_2$", "図(a) の長さ")
in_fig("Adding follows the parallelogram rule", "図(b) の題")
in_fig("the real parts add and", "図(b) の要点")
in_text("$2$ つを掛けると、長さはかけ算、角は足し算になります。", "キャプション (a)")
in_text("$2$ つの矢印を $2$ 辺とする平行四辺形の対角線が、和になります。", "キャプション (b)")
chk("A = np.array([3.0, 2.0])" in FIG and "B = np.array([1.0, 4.0])" in FIG,
    "図(b) の 2 数は本文と同じ")
for leak in ["8e^{i", "12e", "10i", "2\\sqrt{2}", "5\\pi/12", "-32", "6i"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 7. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("3\\sqrt{2}\\,e^{i\\pi/4}", "演習1"), ("5e^{-i\\pi/2}", "演習2"),
                    ("2 + 2\\sqrt{3}", "演習3"), ("12e^{i2\\pi/3}", "演習5"),
                    ("5\\pi}{12}", "演習6"), ("10e^{i\\pi/2}", "演習10")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 8. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-13.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-1-12.qmd") < DRAFT.index("aahl-1-13.qmd")
    < DRAFT.index("aahl-1-14.qmd"), "サイドバーの並びが 1.12 → 1.13 → 1.14")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-13.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| polar form |", "| Euler form |", "| cis |", "| modulus |",
          "| argument |", "| principal argument |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 9. 見張り
# ══════════════════════════════════════════════════════════
in_text("## 偏角の和が、範囲から出ることがあります", "主値の注意")
in_text("**$2\\pi$ を足し引きしても、指す点は変わりません。**", "2π の扱い")
in_text("## $r$ を負の数のまま答える", "r は 0 以上")
in_text("**なぜ $e$ が出てくるのか**", "Euler 形の理由は Why it works へ")
in_text("**それは AHL 5.19 で扱います。**", "級数は 5.19 へ送る")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
