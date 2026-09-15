"""AA SL 2.9（指数関数と対数関数）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_9.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-9.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_9.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, y = sp.symbols("x y", real=True)
E = sp.E
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


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 指数と対数の性質そのもの
# ══════════════════════════════════════════════════════════
_a = sp.Symbol("a", positive=True)
_b = sp.Symbol("b", positive=True)
# a^x は決して 0 にならない
chk(sp.solveset(sp.Eq(_a ** x, 0), x, REALS) == sp.EmptySet, "a^x = 0 に実数解はない")
for _base in [2, 3, 5, 6, 8, 9, sp.Rational(1, 2), E]:
    chk(sp.Pow(_base, 0) == 1, f"{_base}^0 = 1")
    for _v in [-5, -2, 0, 1, 3]:
        chk(sp.Pow(_base, _v) > 0, f"{_base}^{_v} > 0")
# a^0 = 1 → log_a 1 = 0
for _base in [2, 3, 5, 10, E]:
    eq(sp.log(1, _base), 0, f"log_{_base} 1 = 0")
    eq(sp.log(_base, _base), 1, f"log_{_base} {_base} = 1")
# log_a a^x = x, a^{log_a x} = x
eq(sp.simplify(sp.log(E ** x)), x, "ln e^x = x")
eq(sp.simplify(E ** sp.log(_b)), _b, "e^{ln b} = b")
# a^x = e^{x ln a}
chk(sp.simplify(E ** (x * sp.log(_a)) / _a ** x) == 1, "a^x = e^{x ln a}")
# log の中身が 0 や負なら実数でない
chk(not sp.log(-3).is_real, "ln(-3) は実数でない")
chk(not sp.log(0).is_real, "ln 0 は実数でない")
# e の値
chk(abs(float(E) - 2.718281) < 1e-5, "e = 2.718281...")
in_text("e = 2.718281\\ldots", "e の値")
# 本文の走る例
eq(sp.log(1000, 10), 3, "log_10 1000 = 3")
chk(10 ** 3 == 1000, "10^3 = 1000")
chk(sp.simplify(E ** (x * sp.log(4)) / 4 ** x) == 1, "4^x = e^{x ln 4}")
in_text("たとえば $10^{3} = 1000$ なので、$\\log_{10} 1000 = 3$ です。", "本文の走る例")
in_text("たとえば $4^{x} = e^{x \\ln 4}$ です。", "本文の底そろえの例")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  f(x) = 3^x
# ══════════════════════════════════════════════════════════
F1 = 3 ** x
eq(F1.subs(x, 0), 1, "例題1(a) f(0) = 1")
eq(sp.limit(3 ** (-x), x, sp.oo), 0, "例題1(b) x → -∞ で 0")
chk(sp.solveset(sp.Eq(F1, 0), x, REALS) == sp.EmptySet, "例題1(d) 3^x = 0 に解はない")
eq(F1.subs(x, 1), 3, "例題1 検算 f(1) = 3")
eq(F1.subs(x, -1), R(1, 3), "例題1 検算 f(-1) = 1/3")
eq(F1.subs(x, -2), R(1, 9), "例題1 検算 f(-2) = 1/9")
eq(F1.subs(x, -5), R(1, 243), "例題1 検算 f(-5) = 1/243")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  g(x) = ln x
# ══════════════════════════════════════════════════════════
chk(sp.solveset(sp.Eq(sp.log(x), 2), x, REALS) == sp.FiniteSet(E ** 2),
    "例題2(c) x = e^2")
eq(sp.log(E ** 2), 2, "例題2 検算 ln e^2 = 2")
eq(sp.log(E ** -5), -5, "例題2 検算 ln e^-5 = -5")
eq(sp.log(E ** -10), -10, "例題2 検算 ln e^-10 = -10")
chk(not sp.log(-E).is_real, "例題2(d) ln(-e) は実数でない")
chk(sp.solveset(sp.Eq(E ** y, -E), y, REALS) == sp.EmptySet,
    "e^y = -e に実数解はない")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  f(x) = e^x と h(x) = ln x
# ══════════════════════════════════════════════════════════
_p = sp.Symbol("p", positive=True)
eq(sp.simplify(E ** sp.log(_p)), _p, "例題3(a) e^{ln x} = x")
eq(sp.simplify(sp.log(E ** x)), x, "例題3 検算 ln e^x = x")
eq((E ** x).subs(x, 0), 1, "e^0 = 1 なので (0,1) を通る")
eq(sp.log(1), 0, "例題3(c) ln 1 = 0 なので (1,0)")

# ══════════════════════════════════════════════════════════
# 4. 例題 4
# ══════════════════════════════════════════════════════════
chk(sp.simplify(E ** (x * sp.log(5)) / 5 ** x) == 1, "例題4(a) 5^x = e^{x ln 5}")
chk(sp.simplify(E ** (x * sp.log(2)) / 2 ** x) == 1, "例題4(b) 2^x = e^{x ln 2}")
chk(sp.log(2) != 2, "ln 2 ≠ 2")
chk(sp.Pow(2, 1) == 2 and float(E ** 2) > 7, "x=1 で 2 と e^2 はちがう")
eq(sp.log(81, 3), 4, "例題4(c) log_3 81 = 4")
chk(3 ** 4 == 81, "3^4 = 81")
chk(3 * 3 == 9 and 9 * 3 == 27 and 27 * 3 == 81, "例題4(c) の検算のかけ算")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq((6 ** x).subs(x, -3), R(1, 216), "演習1 検算 6^-3 = 1/216")
chk(sp.solveset(sp.Eq(6 ** x, 0), x, REALS) == sp.EmptySet, "演習1 6^x = 0 に解はない")
eq(sp.limit(9 ** (-x), x, sp.oo), 0, "演習2 水平漸近線 y = 0")
eq((9 ** x).subs(x, -2), R(1, 81), "演習2 検算 9^-2 = 1/81")
eq((9 ** x).subs(x, -3), R(1, 729), "演習2 検算 9^-3 = 1/729")
chk(sp.solveset(sp.Eq(5 ** y, 0), y, REALS) == sp.EmptySet, "演習3 5^y = 0 に解はない")
eq(sp.log(E ** 7), 7, "演習4 ln e^7 = 7")
eq(sp.log(32, 2), 5, "演習5 log_2 32 = 5")
chk(2 ** 5 == 32, "2^5 = 32")
chk(sp.simplify(E ** (x * sp.log(7)) / 7 ** x) == 1, "演習6 7^x = e^{x ln 7}")
eq(sp.simplify(E ** sp.log(7)), 7, "演習6 検算 e^{ln 7} = 7")
_A = sp.Symbol("A", positive=True)
chk(sp.solveset(sp.Eq(_A ** 3, 125), _A, REALS) == sp.FiniteSet(5), "演習7 a = 5")
chk(sp.real_roots(sp.Symbol("t") ** 3 - 125) == [5], "3 乗根は 1 つだけ")
chk(5 ** 3 == 125, "演習7 検算 5^3 = 125")
eq(sp.log(1), 0, "演習9 ln 1 = 0")
chk(sp.solveset(sp.Eq(sp.log(x), 0), x, REALS) == sp.FiniteSet(1), "演習9 (1,0)")
chk(sp.solveset(sp.Eq(8 ** x, 0), x, REALS) == sp.EmptySet, "演習10 8^x = 0 に解はない")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("3^{x}", "例題1"), ("e^{2}", "例題2(c)"),
                ("5^{x} = e^{x \\ln 5}", "例題4(a)"),
                ("2^{x} = e^{x \\ln 2}", "例題4(b)"),
                ("\\log_{3} 81", "例題4(c)"),
                ("6^{x}", "演習1"), ("9^{x}", "演習2"),
                ("\\log_{5} x", "演習3"), ("\\ln e^{7}", "演習4"),
                ("\\log_{2} 32", "演習5"),
                ("7^{x}", "演習6"), ("125", "演習7"), ("8^{x}", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.5** の欄に `Exponents and logarithms` として印刷されています。",
        "1.5 の欄")
in_text("> $a^{x} = b \\Leftrightarrow \\log_{a}b = x$, where $a > 0, b > 0, a \\neq 1$",
        "公式集 1.5 を逐語で")
in_text("公式集の **1.7** の欄に、`Exponents and logarithms` の $1$ つとして印刷されています。",
        "1.7 の欄")
in_text("> $a^{x} = e^{x\\ln a}$", "公式集 1.7 を逐語で")
chk(TEXT.count("\n> ") == 2, f"引用は公式集の 2 つだけ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 2, "公式集の callout は 2 つ")
chk(TEXT.index("$$ {#eq-aasl29-equiv}") < TEXT.index("公式集の **1.5** の欄"),
    "公式集 1.5 の callout は式の直後")
chk(TEXT.index("$$ {#eq-aasl29-basee}") < TEXT.index("公式集の **1.7** の欄"),
    "公式集 1.7 の callout は式の直後")
# ★ シラバスの逐語引用は置かない
not_in_text("Exponential functions and their graphs", "シラバス本文は引かない")
not_in_text("Logarithmic functions and their graphs", "シラバス本文は引かない")
not_in_text("Link to:", "Link to の行は引かない")
not_in_text("シラバスは、", "「シラバスは」で始まる文は置かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("**底（base）$a$ は正**とします。", "a > 0 の断り")
in_text("**さらに、ここから先は $a \\neq 1$ とします。**", "a ≠ 1 を先に断る")
in_text("## $\\log$ の中身が $0$ や負のときは、値がありません", "log の中身の注意")
in_text("## $a^{x}$ は $0$ にも負にもなりません", "a^x > 0 の注意")
in_text("だから range は $y > 0$ で、**$y \\ge 0$ ではありません。**", "range は狭義")
in_text("## $\\log_{a}(x+y)$ は $\\log_{a} x + \\log_{a} y$ ではありません", "足し算は分けられない")
in_text("「値が $0$」ではなく「**値がない**」です。答案には `undefined` と書きます。",
        "undefined の書き方")

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
in_text("**`log(` を底なしで使うと、底 $10$ になります。**", "log( の既定の底")
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
chk(len(re.findall(r"^::: \{#exm-aasl29-", TEXT, re.M)) == 4, "例題が 4")
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
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl29", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
for _lab in ["fig-aasl29-idea", "tbl-aasl29-pair", "eq-aasl29-equiv",
             "eq-aasl29-undo", "eq-aasl29-basee"]:
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
SVG = os.path.join(BASE, "img", "aasl-2-9-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-9-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Exponential functions", "図(a) の題")
in_fig("$y = 2^{x}$", "図(a) の y = 2^x")
in_fig("$y = e^{x}$", "図(a) の y = e^x")
in_fig("$y = \\\\left(\\\\frac{1}{2}\\\\right)^{x}$", "図(a) の減る例")
in_fig("$(0,\\\\ 1)$", "図(a) の通る点")
in_fig("asymptote $y = 0$; the value is never $0$ or negative", "図(a) の注意")
in_fig("(b) Inverse of each other", "図(b) の題")
in_fig("$y = \\\\ln x$", "図(b) の対数")
in_fig("$(1,\\\\ 0)$", "図(b) の通る点")
in_fig("$y = x$", "図(b) の対称の線")
in_fig("each is the reflection of the other in $y = x$", "図(b) の説明")
in_text("(a) Exponential functions $y=a^x$ all pass through $(0,1)$",
        "キャプションが (a) を説明")
in_text("(b) $y=e^x$ and $y=\\ln x$ are inverse functions", "キャプションが (b) を説明")
# 図に例題・演習の答えを書いていない
for leak in ["3^", "5^", "6^", "7^", "8^", "9^", "125", "= 4", "= 5", "= 7"]:
    chk(leak not in FIGSTR, "図が答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-9.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-8.qmd") < DRAFT.index("aasl-2-9.qmd"), "並びが 2.8 → 2.9")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-9.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| exponential function |", "| logarithmic function |",
           "| natural logarithm |", "| base |", "| undefined |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════

# --- a ≠ 1 を、主張より先に置く -----------------------------------------
chk(sp.solveset(sp.Eq(1 ** x, 0), x, REALS) == sp.EmptySet, "1^x = 0 に解はない")
chk(sp.simplify(1 ** x) == 1, "1^x はいつも 1（range は 1 点）")
in_text("$a = 1$ だと $1^{x} = 1$ で、グラフは水平な直線になり、range は $y = 1$ の "
        "$1$ 点だけ、漸近線もありません。", "a = 1 の場合の説明")
not_in_text("ふつうは $a \\neq 1$ とします。", "「ふつうは」という言い方は消した")
chk(TEXT.index("**さらに、ここから先は $a \\neq 1$ とします。**")
    < TEXT.index("- **range** は $y > 0$。"), "a ≠ 1 の断りが range より前")
in_text("ここで**底 $a$ は $a > 0$、$a \\neq 1$** とします。", "対数の節にも底の条件")
in_text("$a = 1$ では $1^{y}$ がいつも $1$ なので、「$1$ を何乗したら $x$ に"
        "なるか」に答えられず、対数が決められません。", "a = 1 で対数が決まらない理由")

# --- 0 に近づく向きは a の大小による ------------------------------------
eq((R(1, 2) ** x).subs(x, -10), 1024, "(1/2)^-10 = 1024（0 に近づかない）")
in_text("$a > 1$ のときは、$x$ が大きな負の数になると **$0$ に近づくだけ**で、"
        "$0$ にはなりません。$0 < a < 1$ のときは、$x$ を大きくしていくと同じことが"
        "起こります。", "近づく向きの場合分け")
not_in_text("$x$ が大きな負の数でも、**$0$ に近づくだけ**です。",
            "向きを場合分けしない言い切りは消した")

# --- 無理数の指数と、漸近線であることの証明 -----------------------------
in_text("**ここまでで、指数が有理数のときは正だと分かりました。**", "有理数までの証明")
in_text("$x$ が $\\sqrt{2}$ のような無理数のときに $a^{x}$ をどう定めるかは、"
        "ここでは扱いません。", "無理数の指数にふれた")
in_text("**では、なぜ $y = 0$ が水平漸近線なのでしょうか。** $0$ にならないだけでは"
        "足りません。**$0$ にいくらでも近づく**ことも要ります。",
        "漸近線には「近づく」ことも要る")
not_in_text("**どこにも $0$ や負になる場面がありません。**", "網羅の宣言は消した")
not_in_text("だから $y = 0$ は**近づくだけの線**、つまり水平漸近線になります。",
            "飛躍のある一文は消した")

# --- ほどき合う 2 式の条件 ----------------------------------------------
in_text("左の式はどんな実数 $x$ でも成り立ちますが、**右の式は $x > 0$ のときだけ**です",
        "e^{ln x} = x の条件")
not_in_text("とくに $\\ln e^{x} = x$、$e^{\\ln x} = x$ です。\n", "条件なしの一文は消した")

# --- 演習8・例題1(d) の答えの先出しを外した -----------------------------
not_in_body("$a^{x} = 0$ に解がないため", "例題1(d) の理由が本文にない")
not_in_body("$x = 0$ が domain の外だから", "演習8 の理由が本文にない")
in_text("グラフは漸近線に**いくら近づいても触れません**。", "理由を書かない言い方")

# --- e が無理数であること -----------------------------------------------
in_text("$e$ は $\\pi$ と同じ **irrational number**（無理数）です。", "e は無理数")
in_text("**分数 $\\dfrac{p}{q}$ の形には書けません。**", "分数に書けない")
not_in_text("**割り切れず、循環もしません。**", "あいまいな言い方は消した")
in_text("- $f(x) = e^{x}$ の $e$ が、$2.718\\ldots$ という無理数の定数だと知っている。",
        "冒頭 callout も直した")

# --- 真数・漸近線の英語 -------------------------------------------------
in_text("真数（$\\log$ の中身）も正です。", "真数の言いかえ")
in_text("**$y = 0$ が水平漸近線**（horizontal asymptote）です。", "水平漸近線の英語")
in_text("**$x = 0$ が垂直漸近線**（vertical asymptote）です。", "垂直漸近線の英語")

# --- 電卓（キー名に頼らない）--------------------------------------------
in_text("**自分の機械で一度たしかめておいてください。**", "キーの位置は機種による")
not_in_text("`e^x` のテンプレート（`ctrl` と `e^x` のキー）", "存在しないキー名は消した")

# --- 検算：循環をやめ、設問順に並べた ------------------------------------
# 例題1
eq(sp.Integer(3) ** 1 * sp.Integer(3) ** -1, 1, "3^1 × 3^-1 = 1")
in_text("**検算（(a) について）。** **指数法則から出し直します。**", "例題1(a) の検算")
in_text("**「$0$ 乗は $1$」を覚えていなくても出せます。**", "例題1(a) の検算の締め")
_i1 = TEXT.index("**検算（(a) について）。** **指数法則から出し直します。**")
_i2 = TEXT.index("**検算（(b) について）。** **小さい $x$ で値を見ます。**")
_i3 = TEXT.index("**検算（(c) について）。** **$y \\ge 0$ としていないかを見ます。**")
chk(_i1 < _i2 < _i3, "例題1 の検算は (a) → (b) → (c) の順")
in_text("$3^{x} = 0$ を解こうとして両辺に $3^{-x}$ をかけると $1 = 0$ になり",
        "例題1(c) の検算は最後まで書く")
not_in_text("$1 = 0 \\times 3^{-x}$", "途中で止めた式は消した")
# 例題2
eq(sp.log(E ** -1), -1, "ln(1/e) = -1")
eq(sp.log(R(1, 25), 5), -2, "log_5(1/25) = -2")
_j1 = TEXT.index("**検算（(a) について）。** **$1$ より小さい正の数でも値があるかを見ます。**")
_j2 = TEXT.index("**検算（(b) について）。** **$0$ に近い値を入れます。**")
_j3 = TEXT.index("**検算（(c) について）。** **もとの式に入れ直します。**")
_j4 = TEXT.index("**検算（(d) について）。** **その生徒が出したかった値と見くらべます。**")
chk(_j1 < _j2 < _j3 < _j4, "例題2 の検算は (a) → (b) → (c) → (d) の順")
in_text("**domain は $x > 1$ でも $x \\ge 1$ でもなく、$0$ より大きければ入る**",
        "例題2(a) の検算は domain の形をしぼる")
in_text("**$-1$ が出るのは $\\dfrac{1}{e}$ のときであって、$-e$ のときではありません。**",
        "例題2(d) の検算は独立")
not_in_text("**$e^{y}$ が負になれるかを見ます。**", "model-answer の言い直しは消した")
# 例題3
_k1 = TEXT.index("**検算（(a) について）。** **逆向きの合成も見ます。**")
_k2 = TEXT.index("**検算（(b) について）。** **domain と range が入れかわっているかを見ます。**")
_k3 = TEXT.index("**検算（(c) について）。** **入れかえた点が、本当に $y = \\ln x$ 上にあるかを見ます。**")
chk(_k1 < _k2 < _k3, "例題3 の検算は (a) → (b) → (c) の順")
in_text("**(b)** **(a)** で $f(h(x)) = x$、下の検算で $h(f(x)) = x$ が確かめられます。"
        "**両方の向きでもとに戻るので**、$h$ が $f$ の逆関数です。",
        "例題3(b) は両向きで逆関数と言う")
# 演習3
in_text("**検算。** **$1$ より小さい正の数を入れてみます。** $x = \\dfrac{1}{25}$ なら",
        "演習3 の検算は代入")
not_in_text("**$5^{y}$ が $0$ 以下になれるかを見ます。**", "演習3 の言い直しは消した")

# --- command term（exact value は整数の答えには使わない）----------------
chk(TEXT.count("Find the exact value of") == 1,
    f"exact value は答えが e/ln を含む 1 問だけ: {TEXT.count('Find the exact value of')}")
in_text("[Find the exact value of $x$ for which $g(x) = 2$.]", "例題2(c) は exact value")
in_text("[Find the value of $\\log_{3} 81$.]", "例題4(c) は Find the value of")
in_text("[Find the value of $\\ln e^{7}$.]", "演習4 は Find the value of")
in_text("[Find the value of $\\log_{2} 32$.]", "演習5 は Find the value of")
in_text("[In this question, give all answers in exact form.]", "例題4 の導入文")
not_in_text("[Answer the following.]", "Answer the following は消した")
in_text("[Explain why the graph of $y = f^{-1}(x)$ is the reflection of the graph "
        "of $y = f(x)$ in the line $y = x$.]", "例題3(d) は Explain why")
not_in_text("Explain the geometric relationship", "Explain + relationship は消した")


# ══════════════════════════════════════════════════════════
# E02  演習2 — 0 < a < 1 の指数関数と対数関数
# ══════════════════════════════════════════════════════════
in_text("[On the same axes, sketch the graphs of "
        "$y = \\left(\\dfrac{1}{2}\\right)^{x}$ and "
        "$y = \\log_{\\frac{1}{2}} x$", "E02 演習2 はスケッチ")
in_text("(img/aasl-2-9-ex2.svg){#fig-aasl29-ex2 width=100%}",
        "E02 演習2 の解答図")
in_text("**底が $1$ より小さいので、どちらも減少します**", "E02 減少する")
in_text("**この $2$ つは互いに逆関数です**", "E02 逆関数")
not_in_text("Write down the equation of the horizontal asymptote of the "
            "graph of $y = 9^{x}$", "E02 旧演習2 が消えている")
_e02y = sp.Symbol("y", positive=True)
chk(sp.Rational(1, 2) ** 0 == 1, "E02 指数関数は (0, 1) を通る")
chk(sp.log(1, sp.Rational(1, 2)) == 0, "E02 対数関数は (1, 0) を通る")
chk(sp.Rational(1, 2) ** 2 == sp.Rational(1, 4), "E02 (2, 1/4) を通る")
chk(sp.log(sp.Rational(1, 4), sp.Rational(1, 2)) == 2, "E02 (1/4, 2) を通る")
chk(sp.limit(sp.Rational(1, 2) ** sp.Symbol("t"), sp.Symbol("t"), sp.oo)
    == 0, "E02 指数関数の漸近線は y = 0")
chk(sp.Rational(1, 2) ** 3 < sp.Rational(1, 2) ** 2, "E02 指数関数は減少")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
