"""AA SL 2.10（方程式を解く：グラフと式）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_10.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-10.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_10.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, u = sp.symbols("x u", real=True)
E = sp.E
REALS = sp.S.Reals


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(v_, w_, msg=""):
    chk(sp.simplify(sp.expand(v_) - sp.expand(w_)) == 0, msg + f"  ({v_} vs {w_})")


def sols(expr, want, msg=""):
    chk(sp.solveset(sp.Eq(expr, 0), x, REALS) == want, "解: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 「解く」の意味そのもの
# ══════════════════════════════════════════════════════════
# 交点として見る／差の零点として見る（同じ集合になる）
_f, _g = x ** 2, x + 6
chk(sp.solveset(sp.Eq(_f, _g), x, REALS)
    == sp.solveset(sp.Eq(_f - _g, 0), x, REALS), "交点と差の零点は同じ集合")
chk(sp.solveset(sp.Eq(_f, _g), x, REALS) == sp.FiniteSet(-2, 3), "本文の走る例 x = 3, -2")
chk(sp.factor(x ** 2 - x - 6) == (x - 3) * (x + 2), "本文 (x-3)(x+2)")
in_text("たとえば $x^{2} = x + 6$ なら", "本文の走る例")
# 本文の 2 次方程式
chk(sp.factor(x ** 2 - x - 6) == (x - 3) * (x + 2), "本文 §2 の因数分解")
# 本文のおきかえ（解までは書かない）
chk(sp.factor(u ** 2 - 9 * u + 14) == (u - 2) * (u - 7), "本文 §3 の因数分解")
in_text("e^{2x} - 9e^{x} + 14 = 0", "本文 §3 のおきかえの例")
not_in_body("\\ln 7", "本文 §3 は解まで書かない")
# 本文の対数をとる例
eq(sp.log(20) / sp.log(3), sp.log(20, 3), "本文 §4 の値")
in_text(r"x = \frac{\ln 20}{\ln 3}", "本文 §4 の答え")
# e^x = sin x は解析的に解けない（数値解が無数にあること）
_h = sp.lambdify(x, sp.exp(x) - sp.sin(x))
_signs = [_h(v / 4.0) for v in range(-40, 5)]
_ch = sum(1 for i in range(len(_signs) - 1) if _signs[i] * _signs[i + 1] < 0)
chk(_ch >= 3, f"e^x = sin x の交点は複数ある: {_ch}")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  e^{2x} - 3e^{x} - 4 = 0
# ══════════════════════════════════════════════════════════
chk(sp.factor(u ** 2 - 3 * u - 4) == (u - 4) * (u + 1), "例題1(b) (u-4)(u+1)")
eq(sp.expand((u - 4) * (u + 1)), u ** 2 - 3 * u - 4, "例題1 検算の展開")
chk(sp.solveset(sp.Eq(u ** 2 - 3 * u - 4, 0), u, REALS) == sp.FiniteSet(-1, 4),
    "例題1(b) u = 4, -1")
sols(E ** (2 * x) - 3 * E ** x - 4, sp.FiniteSet(sp.log(4)), "例題1(c) x = ln 4")
chk(sp.solveset(sp.Eq(E ** x, -1), x, REALS) == sp.EmptySet, "e^x = -1 に解はない")
eq((E ** (2 * x)).subs(x, sp.log(4)), 16, "例題1 検算 e^{2ln4} = 16")
eq(16 - 3 * 4 - 4, 0, "例題1 検算 16-12-4 = 0")

# ══════════════════════════════════════════════════════════
# 2. 例題 2
# ══════════════════════════════════════════════════════════
chk(sp.solveset(sp.Eq(3 ** x, 81), x, REALS) == sp.FiniteSet(4), "例題2(a) x = 4")
chk(3 ** 4 == 81, "81 = 3^4")
chk(sp.solveset(sp.Eq(2 ** x, 7), x, REALS)
    == sp.FiniteSet(sp.log(7) / sp.log(2)), "例題2(b) x = ln7/ln2")
chk(2 < float(sp.log(7) / sp.log(2)) < 3, "例題2 検算 2 と 3 のあいだ")
chk(2 ** 2 == 4 and 2 ** 3 == 8 and 4 < 7 < 8, "例題2 検算のはさみこみ")
chk(sp.solveset(sp.Eq(sp.log(2 * x - 1), 0), x, REALS) == sp.FiniteSet(1),
    "例題2(c) x = 1")
eq((2 * x - 1).subs(x, 1), 1, "例題2 検算 2(1)-1 = 1")
chk(abs(float(2 ** sp.Rational(7, 2)) - 11.3137) < 1e-3, "例題2(d) 2^3.5 ≈ 11.3")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  y = x^2 と y = 4 - 3x
# ══════════════════════════════════════════════════════════
chk(sp.factor(x ** 2 + 3 * x - 4) == (x - 1) * (x + 4), "例題3(b) (x+4)(x-1)")
chk(sp.solveset(sp.Eq(x ** 2, 4 - 3 * x), x, REALS) == sp.FiniteSet(-4, 1),
    "例題3(b) x = -4, 1")
for _v, _y in [(-4, 16), (1, 1)]:
    eq((4 - 3 * x).subs(x, _v), _y, f"例題3(c) 直線 x={_v}")
    eq((x ** 2).subs(x, _v), _y, f"例題3 検算 放物線 x={_v}")
eq(sp.expand(x ** 2 - (4 - 3 * x)), x ** 2 + 3 * x - 4, "例題3 検算 差の式")
eq(3 ** 2 - 4 * 1 * (-4), 25, "例題3 検算 Δ = 25")
chk(25 > 0, "Δ > 0 なので実数解 2 つ")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  2^x = x + 3
# ══════════════════════════════════════════════════════════
_F = lambda v: sp.Integer(2) ** v
for _v, _d in [(2, -1), (3, 2)]:
    eq(_F(_v) - (_v + 3), _d, f"例題4(a) x={_v} の差")
eq(_F(-3) - (-3 + 3), R(1, 8), "例題4(b) x=-3 の差 1/8")
eq(_F(-2) - (-2 + 3), R(-3, 4), "例題4(b) x=-2 の差 -3/4")
chk(R(1, 8) > 0 > R(-3, 4), "符号が変わる")
chk(float(2 ** sp.Rational(5, 2)) > 5.5, "例題4 検算 2^2.5 > 5.5")
eq(2 ** sp.Rational(5, 2), 4 * sp.sqrt(2), "2^2.5 = 4√2")
chk(4 * float(sp.sqrt(2)) > 5.6, "4√2 > 5.6")
# 解はちょうど 2 つ
_d2 = sp.lambdify(x, 2 ** x - x - 3)
_sg = [_d2(v / 8.0) for v in range(-80, 41)]
chk(sum(1 for i in range(len(_sg) - 1) if _sg[i] * _sg[i + 1] < 0) == 2,
    "2^x = x+3 の実数解は 2 つ")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
sols(E ** x - 5, sp.FiniteSet(sp.log(5)), "演習1 x = ln 5")
eq(E ** sp.log(5), 5, "演習1 検算")
chk(sp.solveset(sp.Eq(sp.log(x), 3), x, REALS) == sp.FiniteSet(E ** 3),
    "演習2 x = e^3")
eq(sp.log(E ** 3), 3, "演習2 検算")
chk(sp.solveset(sp.Eq(4 ** x, 64), x, REALS) == sp.FiniteSet(3), "演習3 x = 3")
chk(4 ** 3 == 64, "64 = 4^3")
chk(sp.factor(u ** 2 - 6 * u + 8) == (u - 2) * (u - 4), "演習4 (u-2)(u-4)")
sols(E ** (2 * x) - 6 * E ** x + 8, sp.FiniteSet(sp.log(2), sp.log(4)),
     "演習4 x = ln2, ln4")
eq(4 - 12 + 8, 0, "演習4 検算 u=2")
eq(16 - 24 + 8, 0, "演習4 検算 u=4")
chk(sp.factor(x ** 2 - x - 2) == (x - 2) * (x + 1), "演習5 (x-2)(x+1)")
chk(sp.solveset(sp.Eq(x ** 2 - 2, x), x, REALS) == sp.FiniteSet(-1, 2), "演習5 x = 2, -1")
for _v in (2, -1):
    eq((x ** 2 - 2).subs(x, _v), _v, f"演習5 検算 x={_v}")
chk(sp.solveset(sp.Eq(sp.log(3 * x + 1), 0), x, REALS) == sp.FiniteSet(0), "演習6 x = 0")
eq((3 * x + 1).subs(x, 0), 1, "演習6 検算")
chk(sp.solveset(sp.Eq(10 ** x, 3), x, REALS) == sp.FiniteSet(sp.log(3, 10)),
    "演習7 x = log_10 3")
chk(0 < float(sp.log(3, 10)) < 1, "演習7 検算 0 と 1 のあいだ")
chk(sp.solveset(sp.Eq(E ** x, -2), x, REALS) == sp.EmptySet, "演習8 解なし")
chk(sp.solveset(sp.Eq(E ** (2 * x), E ** (x + 6)), x, REALS) == sp.FiniteSet(6),
    "演習9 x = 6")
eq(2 * 6, 6 + 6, "演習9 検算 指数が等しい")
chk(sp.factor(x ** 2 - 3 * x - 4) == (x - 4) * (x + 1), "演習10 (x-4)(x+1)")
eq(sp.expand(x * (x - 3) - 4), x ** 2 - 3 * x - 4, "演習10 まとめた式")
eq(sp.log(4) + sp.log(1), sp.log(4), "演習10 検算 x=4")
chk(not sp.log(-1).is_real, "演習10 x=-1 は ln が定義されない")
chk(4 > 3, "x = 4 は x > 3 を満たす")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("e^{2x} - 3e^{x} - 4", "例題1"), ("u^{2} - 3u - 4", "例題1"),
                (r"\ln 4", "例題1"), ("3^{x} = 81", "例題2(a)"),
                ("2^{x} = 7", "例題2(b)"), (r"\frac{\ln 7}{\ln 2}", "例題2(b)"),
                (r"\ln(2x - 1)", "例題2(c)"),
                ("4 - 3x", "例題3"), ("x^{2} + 3x - 4", "例題3"),
                # E03: 2^x = x+3 の「式」は第6節で先に紹介する。
                #      漏らしてはいけないのは「解の値」のほう。
                ("2.44", "例題4 の解"), ("-2.86", "例題4 の解"),
                ("2.44490", "例題4 の解"),
                ("e^{x} = 5", "演習1"), (r"\ln x = 3", "演習2"),
                ("4^{x} = 64", "演習3"), ("e^{2x} - 6e^{x} + 8", "演習4"),
                ("x^{2} - 2", "演習5"), (r"\ln(3x + 1)", "演習6"),
                ("10^{x} = 3", "演習7"), ("e^{x} = -2", "演習8"),
                ("e^{x + 6}", "演習9"), (r"\ln(x-3)", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk(TEXT.count("::: {.callout-important}") == 1, "公式集の callout は 1 つ")
in_text("$\\ln 3^{x} = x \\ln 3$ で使った $\\log_{a} x^{m} = m \\log_{a} x$ は、"
        "公式集の **1.7** の欄に対数の法則の $1$ つとして印刷されています",
        "公式集 1.7 の欄")
in_text("**覚えていなくても、試験中に見られます。**", "覚える必要はないと書く")
chk(TEXT.count("\n> ") == 0, f"引用は置かない: {TEXT.count(chr(10) + '> ')}")
# ★ シラバスの逐語引用は置かない
not_in_text("Solving equations, both graphically and analytically",
            "シラバス本文は引かない")
not_in_text("Use of technology to solve", "シラバス本文は引かない")
not_in_text("シラバスは、", "「シラバスは」で始まる文は置かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
# 一般規則を勝手に主張しない
# 一般規則として本文で主張しない（問題文が指定するのはよい）
not_in_body("有効数字 $3$ 桁", "3 桁という一般規則は主張しない")
in_text("答えの書き方（何桁で書くか）は、**試験用紙の冒頭の指示**に"
        "従ってください。", "桁数は試験用紙の指示に従う")
not_in_text("3 s.f.", "3 s.f. という一般規則は主張しない")
in_text("**試験用紙の冒頭の指示**", "桁数は試験用紙の指示に従う")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## $u = e^{x}$ なら、$u > 0$ でなければなりません", "u > 0 の注意")
in_text("## 変形の途中で、解が増えることがあります", "増える解の注意")
in_text("## `exact` と言われたら、小数にしないでください", "exact の注意")
in_text("**「解けない」のではなく、「習った変形では届かない」**ということです。",
        "解けないの言い方")
in_text("**SL の道具ではすぐに手が出ない**", "x^4+5x-6 の言い方（解けないとは書かない）")
not_in_text("$x^{4} + 5x - 6 = 0$ は解析的に解けません", "誤った断定を置かない")
in_text("答案には *reject*（捨てる）と理由を書いてください。", "reject の書き方")

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
in_text("**画面に出ている範囲しか見えません。**", "窓の外の解への注意")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 7, f"model-answer が 7: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl210-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl210", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
for _lab in ["fig-aasl210-idea", "eq-aasl210-eq"]:
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
SVG = os.path.join(BASE, "img", "aasl-2-10-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-10-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Two ways to see a solution", "図(a) の題")
in_fig("$y = f(x)$", "図(a) の f")
in_fig("$y = g(x)$", "図(a) の g")
in_fig("$y = f(x) - g(x)$", "図(a) の差")
in_fig("$x_{1}$", "図(a) の解 1")
in_fig("$x_{2}$", "図(a) の解 2")
in_fig("the crossings of $f$ and $g$ sit above the zeros of $f - g$", "図(a) の説明")
in_fig("(b) When no method reaches it", "図(b) の題")
in_fig("$y = e^{x}$", "図(b) の指数")
in_fig("$y = \\\\sin x$", "図(b) の sin")
in_fig("at SL, these crossings are found with technology", "図(b) の説明")
in_text("(a) The solutions of $f(x)=g(x)$ are the $x$-coordinates",
        "キャプションが (a) を説明")
in_text("(b) The equation $e^x=\\sin x$ has crossings", "キャプションが (b) を説明")
# 図に例題・演習の答えを書いていない
for leak in ["= 4", "= 6", "= 1", "\\ln", "\\log"]:
    chk(leak not in FIGSTR, "図が答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-10.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-9.qmd") < DRAFT.index("aasl-2-10.qmd"), "並びが 2.9 → 2.10")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-10.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| analytically |", "| substitution |", "| reject |",
           "| point of intersection |", "| technology |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════

# --- 第 6 節の例は、本当に手が出ないもの --------------------------------
_q = x ** 4 + 5 * x - 3
chk(sp.factor(_q) == _q, "x^4+5x-3 は有理数の範囲で因数分解できない")
chk(len(sp.real_roots(_q)) == 2, "実数解は 2 つ")
chk(all(not r.is_rational for r in sp.real_roots(_q)), "実数解は有理数でない")
in_text("$x^{4} + 5x - 3 = 0$ のように、**SL の道具ではすぐに手が出ない**",
        "手が出ない例は x^4+5x-3")
# 差しかえ前の式は、実際には解けてしまう
chk(sp.factor(x ** 4 + 5 * x - 6)
    == (x - 1) * (x + 2) * (x ** 2 - x + 3), "x^4+5x-6 は解けてしまう")
not_in_text("$x^{4} + 5x - 6", "解けてしまう式は例に使わない")

# --- 「解けない」を、この課程の変形に限定した ---------------------------
in_text("### 6. 習った変形では解けない方程式 {#no-analytic}", "第 6 節の見出し")
in_text("この方程式は、**この課程で習う式の変形では解けません。**", "限定した言い方")
not_in_text("この方程式は、**式の変形では解けません。**", "無条件の断定は消した")
in_text("- **この課程の変形では解けない方程式**があることを知り", "冒頭 callout も直した")

# --- e^x = sin x の交点は負の側だけ -------------------------------------
_d = sp.lambdify(x, sp.exp(x) - sp.sin(x))
chk(all(_d(v / 8.0) > 0 for v in range(0, 81)), "x ≥ 0 では e^x > sin x")
in_text("交点は**負の側にいくつも**あります", "交点は負の側")
in_text("（$x \\ge 0$ では $e^{x} \\ge 1$、$\\sin x \\le 1$ で、同時に $1$ には"
        "ならないので交わりません。）", "x ≥ 0 で交わらない理由")

# --- 「解が増える」と「おきかえで捨てる」を分けた ------------------------
in_text("$\\log$ を $1$ つにまとめる、両辺を $2$ 乗する、といった変形をすると",
        "解が増える変形の例")
in_text("おきかえのときは少しちがい、出てきた $u$ の値のうち**対応する $x$ が"
        "ないもの**を落とすことになります。", "おきかえは別だと書く")
not_in_text("おきかえや $2$ 乗をすると、**もとの方程式の解ではない値**",
            "混ざった言い方は消した")
in_text("**なぜ、おきかえた先で出た値を、そのまま答えにできないのでしょうか。**",
        "Why it works の問いも直した")

# --- 例題2：幹の指示・整数条件・電卓なしの確かめ -------------------------
in_text("[Solve the equations in parts (a) to (c).]", "幹の指示は (a)〜(c)")
not_in_text("[Solve each of the following equations.]", "全小問にかかる指示は消した")
in_text("where $p, q \\in \\mathbb{Z}^{+}$", "例題2(b) に整数条件")
eq(2 ** R(7, 2), 8 * sp.sqrt(2), "2^{\\frac{7}{2}} = 8√2")
chk(8 * float(sp.sqrt(2)) > 8, "8√2 > 8")
in_text("$2^{\\frac{7}{2}} = 8\\sqrt{2}$, which is more than $8$, not $7$",
        "例題2(d) は電卓なしで書ける確かめ")
not_in_text("$2^{3.5} \\approx 11.3$", "小数の確かめは消した")

# --- 例題3：ちょうど 2 つの根拠 -----------------------------------------
in_text("a line can meet a parabola at most twice, so there are exactly two "
        "points of intersection", "多くても 2 点という根拠")
in_text("直線と放物線は多くても $2$ 点でしか出会えないので、交点はちょうど $2$ つ",
        "日本語側も同じ")
not_in_text("the parabola grows faster than any line in both directions",
            "不十分な論法は消した")
eq(sp.expand((x + 4) * (x - 1)), x ** 2 + 3 * x - 4, "例題3 検算の展開")
in_text("**検算（(a)(b) について）。** **因数分解を展開して戻します。**",
        "例題3 の検算に独立した道すじ")
in_text("aasl-2-7b.qmd#intersect", "2.7b の直線と曲線の節へ")

# --- 例題4：連続であること・検算の独立・外側だけの主張 -------------------
in_text("$y = 2^{x} - x - 3$ のグラフは**切れ目のない $1$ 本の曲線**なので",
        "連続であることを書く")
in_text("*$y = 2^{x}-x-3$ is a continuous curve and the sign changes",
        "解答例にも continuous")
in_text("*The sign changes again on a continuous curve", "(b) の解答例にも continuous")
eq(2 ** R(-5, 2), 1 / (4 * sp.sqrt(2)), "2^{-\\frac{5}{2}} = 1/(4√2)")
chk(float(2 ** R(-5, 2)) < 0.18, "2^{-\\frac{5}{2}} < 0.18")
chk(4 * float(sp.sqrt(2)) > 5.6, "4√2 > 5.6")
chk(float(2 ** R(-5, 2)) - 0.5 < 0, "x=-2.5 で f-g < 0")
in_text("**検算（(b) について）。** **もう $1$ 点はさんで、範囲を狭めます。**",
        "例題4(b) の検算は独立")
not_in_text("**値そのものを見直します。**", "解答のくり返しは消した")
in_text("**検算（(c)(d) について）。** **区間の外に解がないことを確かめます。**",
        "例題4 の最後の検算は範囲を限定")
in_text("**だから解はすべて $-3 \\le x \\le 3$ の中にあり", "外側にないことだけ言う")
not_in_text("**交点が $2$ つしかないかを見ます。**", "言いすぎの見出しは消した")

# --- 演習1・2 の検算に別の道すじ ----------------------------------------
chk(1 < float(sp.log(5)) < 2, "ln 5 は 1 と 2 のあいだ")
chk(abs(float(sp.E ** 2) - 7.389) < 1e-2, "e^2 ≈ 7.4")
chk(abs(float(sp.E ** 3) - 20.09) < 1e-1, "e^3 ≈ 20")
chk(abs(float(3 * sp.E) - 8.15) < 1e-1, "3e ≈ 8.2")
in_text("**大きさでも見ます。** $e^{1}$ はおよそ $2.7$、$e^{2}$ はおよそ $7.4$ なので",
        "演習1 の大きさの見当")
in_text("**大きさでも見ます。** $e^{3}$ は $20$ くらいで、$3e$ のおよそ $8.2$ とは",
        "演習2 の大きさの見当")

# --- 演習7 の整数条件、演習10 の domain ---------------------------------
in_text("in the form $\\log_{10} k$, where $k \\in \\mathbb{Z}^{+}$", "演習7 に整数条件")
chk(sp.Intersection(sp.Interval.open(0, sp.oo), sp.Interval.open(3, sp.oo))
    == sp.Interval.open(3, sp.oo), "もとの式の domain は x > 3")
in_text("**式が意味をもつのは $x > 3$ のときだけ**です。", "効いている条件は x > 3")
in_text("**$x < 0$ の側が新しく開いた**ぶんが、余分な解です。", "増えた理由")
in_text("*The original equation needs $x > 0$ and $x - 3 > 0$, so $x > 3$.",
        "解答例にも両方の条件")
not_in_text("*The value $x = -1$ makes $\\ln x$ undefined, so it is not a solution",
            "片方の条件だけの解答例は消した")


# ══════════════════════════════════════════════════════════
# E03  第6節を既習の $2^{x} = x+3$ から始め、例題4 に (e) を足す
# ══════════════════════════════════════════════════════════
in_text("### 6. 習った変形では解けない方程式 {#no-analytic}" + chr(10) + chr(10)
        + "$$" + chr(10) + "2^{x} = x + 3" + chr(10) + "$$",
        "E03 第6節は 2^x = x+3 から")
in_text("**三角関数は [SL 3.7a](../03-geometry/aasl-3-7a.qmd) で学びます**",
        "E03 三角関数は未習と断る")
in_text("[Using technology, find both solutions of $f(x) = g(x)$, correct "
        "to three significant figures.", "E03 例題4 (e) の英語")
in_text("電卓を使って $f(x) = g(x)$ の解を $2$ つとも求め、有効数字 $3$ 桁で"
        "答えなさい。", "E03 例題4 (e) の訳")
in_text("| $2 \\le x \\le 3$ | $2.44490\\ldots$ | $2.44$ |",
        "E03 (e) 正の側の解")
in_text("| $-3 \\le x \\le -2$ | $-2.86250\\ldots$ | $-2.86$ |",
        "E03 (e) 負の側の解")
in_text("**途中で丸めないでください。**", "E03 途中で丸めない")
# 2^x = x+3 の解を実際に求め直す（区間の中に 1 つずつ）
_e03f = sp.Lambda(x, 2**x - x - 3)
_e03a = sp.nsolve(2**x - x - 3, x, 2.5)
_e03b = sp.nsolve(2**x - x - 3, x, -2.5)
chk(2 < _e03a < 3, "E03 正の解は 2 と 3 のあいだ")
chk(-3 < _e03b < -2, "E03 負の解は -3 と -2 のあいだ")
chk(float("%.3g" % float(_e03a)) == 2.44, "E03 正の解は 3 有効数字で 2.44")
chk(float("%.3g" % float(_e03b)) == -2.86, "E03 負の解は 3 有効数字で -2.86")
chk(abs(float(_e03a) - 2.44490) < 5e-5, "E03 画面に出る値 2.44490...")
chk(abs(float(_e03b) + 2.86250) < 5e-5, "E03 画面に出る値 -2.86250...")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
