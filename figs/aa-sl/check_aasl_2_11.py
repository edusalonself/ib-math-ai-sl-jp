"""AA SL 2.11（グラフの移動と拡大）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_11.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-11.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_11.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x, s_, t_ = sp.symbols("x s t", real=True)
a_, b_, p_, q_ = sp.symbols("a b p q", real=True)
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
# 0. 変換の規則そのもの（一般の f で確かめる）
# ══════════════════════════════════════════════════════════
_F = sp.Function("F")
# 点 (s, t) が y = F(x) 上 ⇔ t = F(s)
# 平行移動 y = F(x) + b は (s, t) → (s, t+b)
eq((_F(x) + b_).subs(x, s_) - (_F(s_) + b_), 0, "F(x)+b は (s, t+b)")
# y = F(x-a) は (s, t) → (s+a, t)
eq((_F(x - a_)).subs(x, s_ + a_) - _F(s_), 0, "F(x-a) は (s+a, t)")
# y = -F(x) は (s, t) → (s, -t)
eq((-_F(x)).subs(x, s_) + _F(s_), 0, "-F(x) は (s, -t)")
# y = F(-x) は (s, t) → (-s, t)
eq((_F(-x)).subs(x, -s_) - _F(s_), 0, "F(-x) は (-s, t)")
# y = p F(x) は (s, t) → (s, pt)
eq((p_ * _F(x)).subs(x, s_) - p_ * _F(s_), 0, "pF(x) は (s, pt)")
# y = F(qx) は (s, t) → (s/q, t)
eq((_F(q_ * x)).subs(x, s_ / q_) - _F(s_), 0, "F(qx) は (s/q, t)")
# 順番で変わる（縦どうし）
chk(sp.expand(3 * _F(x) + 1) != sp.expand(3 * (_F(x) + 1)),
    "縦どうしは順番で変わる")
eq(3 * (_F(x) + 1), 3 * _F(x) + 3, "上へ 1 のあと 3 倍は 3F(x)+3")
in_text("y = 3f(x) + 1", "本文 §5 の順その 1")
in_text(r"y = 3\big(f(x) + 1\big) = 3f(x) + 3", "本文 §5 の順その 2")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  f(x) = x^2
# ══════════════════════════════════════════════════════════
eq(((x - 4) ** 2 + 3), sp.expand(x ** 2 - 8 * x + 19), "例題1(c) の式")
chk(sp.Poly((x - 4) ** 2 + 3, x).all_coeffs() == [1, -8, 19], "展開の係数")
# 頂点 (4, 3)
eq(((x - 4) ** 2 + 3).subs(x, 4), 3, "例題1(c) 頂点の y は 3")
chk(sp.minimum((x - 4) ** 2 + 3, x, REALS) == 3, "最小値は 3")
chk(sp.solveset(sp.Eq(sp.diff((x - 4) ** 2 + 3, x), 0), x, REALS)
    == sp.FiniteSet(4), "最小になる x は 4")
# 検算に使う点
eq((x ** 2).subs(x, 2) + 3, 7, "例題1 検算 (2, 7)")
chk(sp.solveset(sp.Eq((x - 4) ** 2, 4), x, REALS) == sp.FiniteSet(2, 6),
    "例題1 検算 x = 2, 6")
chk(sp.solveset(sp.Eq(x ** 2, 4), x, REALS) == sp.FiniteSet(-2, 2),
    "例題1 検算 もとは x = ±2")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  f(x) = x^2 - 4x
# ══════════════════════════════════════════════════════════
_f2 = x ** 2 - 4 * x
chk(sp.factor(_f2) == x * (x - 4), "例題2(a) x(x-4)")
sols(_f2, sp.FiniteSet(0, 4), "例題2(a) 0 と 4")
sols(-_f2, sp.FiniteSet(0, 4), "例題2(b) 変わらない")
eq(_f2.subs(x, -x), x ** 2 + 4 * x, "例題2(c) f(-x) = x^2+4x")
chk(sp.factor(x ** 2 + 4 * x) == x * (x + 4), "例題2(c) x(x+4)")
sols(x ** 2 + 4 * x, sp.FiniteSet(-4, 0), "例題2(c) 0 と -4")
eq(_f2.subs(x, 0), 0, "例題2 検算 f(0) = 0")
eq(_f2.subs(x, 4), 0, "例題2 検算 f(4) = 0")
eq(sp.expand(-_f2), -x ** 2 + 4 * x, "例題2 検算 -f(x)")
chk(sp.factor(-_f2) == -x * (x - 4), "例題2 検算 -x(x-4)")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  f(x) = x^2 - 9
# ══════════════════════════════════════════════════════════
_f3 = x ** 2 - 9
chk(sp.factor(_f3) == (x - 3) * (x + 3), "例題3(a) (x-3)(x+3)")
sols(_f3, sp.FiniteSet(-3, 3), "例題3(a) x = ±3")
eq(_f3.subs(x, 2 * x), 4 * x ** 2 - 9, "例題3(b) f(2x) = 4x^2-9")
sols(4 * x ** 2 - 9, sp.FiniteSet(R(-3, 2), R(3, 2)), "例題3(b) x = ±3/2")
eq(3 * _f3.subs(x, 0), -27, "例題3(c) y 切片 -27")
eq(_f3.subs(x, 0), -9, "例題3 検算 もとの y 切片 -9")
eq(R(3, 1) / 2, R(3, 2), "例題3 検算 s/q = 3/2")
eq(_f3.subs(x, 3), 0, "例題3 検算 f(3) = 0")
eq(_f3.subs(x, -3), 0, "例題3 検算 f(-3) = 0")
# scale factor 2 なら ±6 のはず（誤答の帰結）
sols((sp.Rational(1, 2) * x) ** 2 - 9, sp.FiniteSet(-6, 6),
     "scale factor 2 なら ±6")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  縦の合成
# ══════════════════════════════════════════════════════════
eq(2 * 4 - 5, 3, "例題4(b) 2(4)-5 = 3")
eq(2 * (4 - 5), -2, "例題4(d) 2(4-5) = -2")
chk(3 != -2, "順番で結果がちがう")
eq(2 * (_F(x) - 5), 2 * _F(x) - 10, "例題4(c) 2f(x)-10")
eq(2 * 1 - 5, -3, "例題4 検算 (0,1) → (0,-3)")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(10 - 6, 4, "演習1 検算 (1, 4)")
chk(sp.solveset(sp.Eq(x + 2, 5), x, REALS) == sp.FiniteSet(3), "演習2 検算 x = 3")
eq((x - 3) ** 2 - 1, sp.expand(x ** 2 - 6 * x + 8), "演習3 の式")
eq(((x - 3) ** 2 - 1).subs(x, 3), -1, "演習3 頂点の y は -1")
chk(sp.minimum((x - 3) ** 2 - 1, x, REALS) == -1, "演習3 最小値 -1")
eq(-5, -(5), "演習4 検算 (2, -5)")
eq((-(-2)), 2, "演習5 検算 f(-(-2)) = f(2)")
eq(4 * 3, 12, "演習6 検算 (1, 12)")
chk(sp.solveset(sp.Eq(3 * x, 6), x, REALS) == sp.FiniteSet(2), "演習7 検算 x = 2")
eq(2 + 5, 7, "演習8 y = 7")
eq(_f2.subs(x, 0), 0, "演習9 検算 f(0) = 0")
eq((x ** 2 + 4 * x).subs(x, 0), 0, "演習9 検算 f(-x) も 0")
eq(R(1, 2) * 6, 3, "演習10 検算 (1, 3)")
chk(R(1, 2) != 2, "1/2 は 2 ではない")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("f(x - 4)", "例題1(b)"), ("(4, \\ 3)", "例題1(c)"),
                ("f(x-4) + 3", "例題1(c)"),
                ("x^{2} - 4x", "例題2"), ("x^{2} - 9", "例題3"),
                ("f(2x)", "例題3"), ("4x^{2} - 9", "例題3(b)"),
                ("(0, \\ -27)", "例題3(c)"),
                ("2f(x) - 5", "例題4"), ("2f(x) - 10", "例題4(c)"),
                ("f(x) - 6", "演習1"), ("f(x + 2)", "演習2"),
                ("(x-3)^{2} - 1", "演習3"), ("4f(x)", "演習6"),
                ("f(3x)", "演習7"), ("f(x) + 5", "演習8"),
                ("\\dfrac{1}{2}f(x)", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk("::: {.callout-important}" not in TEXT,
    "2.11 は公式集に何もないので、公式集の callout は置かない")
not_in_text("公式集の **2.11**", "公式集に 2.11 の欄はない")
chk(TEXT.count("\n> ") == 0, f"引用は置かない: {TEXT.count(chr(10) + '> ')}")
# ★ Not required の行だけは、内容として書いてよい
in_text("シラバスの 2.11 には `Not required:` として、**$f(ax+b)$ の形の"
        "変換**が挙がっています。", "Not required の行")
not_in_text("Translations: $y = f(x)+b$", "シラバス本文は引かない")
not_in_text("Composite transformations", "シラバス本文は引かない")
not_in_text("シラバスは、", "「シラバスは」で始まる文は置かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## $f(x-a)$ は「右へ」です。符号に見えるものと逆です", "中はさかさま")
in_text("## `scale factor` は「何倍か」です。$q$ そのものではありません",
        "scale factor の注意")
in_text("## $f(ax+b)$ の形は、この項目では扱いません", "範囲外の注意")
in_text("**ちがう向き**（縦と横）なら、どちらが先でも同じ結果です。", "縦と横は独立")
in_text("効くのは、**平行移動（足す）と、拡大・対称移動（かける）が、同じ向きで"
        "混ざるとき**です。", "順番が効く条件")
in_text("「縦に $3$ 倍」と「$x$ 軸で折り返す」は、どちらが先でも $y = -3f(x)$ です。",
        "かける操作どうしは可換")
not_in_text("**同じ向きどうし**（縦と縦、横と横）は順番が効きます。",
            "成り立たない一般化は消した")
in_text("**別々の座標をさわっているので、ぶつかりません。**", "縦と横が独立な理由")
in_text("**表を覚える必要はありません。**", "表は覚えなくてよい")

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
# --- 演習6（E04）：順番で結果が変わることを自分で確かめる --------------
in_text("[The graph of $y = f(x)$ passes through the point $(1, 4)$.]",
        "E04 演習6 の英語")
in_text("$y = f(x)$ のグラフは点 $(1, 4)$ を通ります。", "E04 演習6 の訳")
in_text("$$y = 3f(x) + 2, \\qquad (1, \\ 14)$$", "E04 (a) の答え")
in_text("$$y = 3\\bigl(f(x) + 2\\bigr) = 3f(x) + 6, \\qquad (1, \\ 18)$$",
        "E04 (b) の答え")
not_in_text("$y = f(x)$ のグラフを $y = 4f(x)$ のグラフに移す変換",
            "E04 旧演習6 が消えている")
# 3*4+2 = 14 と 3*(4+2) = 18 は別の値
chk(3 * 4 + 2 == 14, "E04 拡大してから平行移動")
chk(3 * (4 + 2) == 18, "E04 平行移動してから拡大")
chk(3 * 4 + 2 != 3 * (4 + 2), "E04 順番で結果が変わる")
chk(3 * 0 + 2 == 2 and 3 * (0 + 2) == 6, "E04 y 切片もちがう")
chk(len(re.findall(r"^::: \{#exm-aasl211-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl211", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
for _lab in ["fig-aasl211-idea", "tbl-aasl211-move", "eq-aasl211-up",
             "eq-aasl211-right", "eq-aasl211-refx", "eq-aasl211-refy",
             "eq-aasl211-vstretch", "eq-aasl211-hstretch"]:
    chk(TEXT.count("@" + _lab) >= 0, "ラベルの綴り: " + _lab)
chk(TEXT.count("@fig-aasl211-idea") >= 1, "図を本文から参照している")
chk(TEXT.count("@tbl-aasl211-move") >= 1, "表を本文から参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")
# ベクトルの書き方
chk(TEXT.count("\\begin{pmatrix}") == TEXT.count("\\end{pmatrix}"),
    "pmatrix の開閉が合う")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-11-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-11-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Translations and reflections", "図(a) の題")
in_fig("$y = f(x) + b$", "図(a) の上へ")
in_fig("$y = f(x - a)$", "図(a) の右へ")
in_fig("$y = -f(x)$", "図(a) の折り返し")
in_fig("up by $b$; right by $a$; flipped in the $x$-axis", "図(a) の説明")
in_fig("(b) Stretches", "図(b) の題")
in_fig("$y = p\\\\,f(x)$", "図(b) の縦")
in_fig("$y = f(qx)$", "図(b) の横")
in_fig("vertical by $p$; horizontal by $\\\\frac{1}{q}$", "図(b) の説明")
in_text("(a) $y=f(x)+b$ moves the graph up by $b$", "キャプションが (a) を説明")
in_text("(b) $y=p f(x)$ stretches it vertically", "キャプションが (b) を説明")
# 図に例題・演習の答えを書いていない（動かす量は文字だけ）
for leak in ["= 3", "= 4", "= 2", "= 5", "= 6"]:
    chk(leak not in FIGSTR, "図が具体的な量を載せている: " + leak)
chk(not re.search(r"\d", FIGSTR.replace("\\frac{1}{q}", "")),
    "図のラベルに数字がない（1/q だけは可）")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-11.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-10.qmd") < DRAFT.index("aasl-2-11.qmd"), "並びが 2.10 → 2.11")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-11.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| transformation |", "| translation |", "| reflection |",
           "| stretch |", "| scale factor |", "| image |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════

# --- 順番が効くのは「足す」と「かける」が同じ向きでぶつかるときだけ ------
_G = sp.Function("G")
# かける操作どうしは可換
eq(-(3 * _G(x)), 3 * (-_G(x)), "縦の 3 倍と x 軸の折り返しは可換")
eq(2 * (3 * _G(x)), 3 * (2 * _G(x)), "縦の拡大どうしは可換")
# 平行移動どうしも可換
eq((_G(x) + 2) + 5, (_G(x) + 5) + 2, "縦の平行移動どうしは可換")
# 足す × かける は可換でない
chk(sp.expand(3 * _G(x) + 1) != sp.expand(3 * (_G(x) + 1)),
    "縦の拡大と縦の平行移動は可換でない")
# 横の折り返しと横の拡大は可換
eq(_G(-(2 * x)), _G(2 * (-x)), "y 軸の折り返しと横の拡大は可換")
# 縦と横は可換
eq(2 * _G(3 * x), (lambda h: 2 * h)(_G(3 * x)), "縦と横は可換（同じ式）")
in_text("まとめると、**「足す」と「かける」が同じ向きでぶつかるときだけ、"
        "順番を気にすれば十分**です。", "順番のまとめ")
in_text("順番が問題になるのは**縦どうし**の組み合わせだけです。", "SL では縦どうしだけ")
in_text("縦の**拡大（または対称移動）**と縦の**平行移動**は、順番で結果が変わります",
        "Common errors 側も直した")
not_in_text("縦の変換どうしは、順番で結果が変わります", "言いすぎの一文は消した")

# --- p, q の符号の前提 --------------------------------------------------
in_text("ここでは **$p > 0$、$q > 0$** とします。", "p, q は正")
in_text("たとえば $y = -3f(x)$ は「$x$ 軸についての対称移動」と"
        "「scale factor $3$ の縦の拡大」の $2$ つです。", "負のときの書き方")

# --- 「外は縦・中は横」の限界 -------------------------------------------
in_text("ただし、この $2$ 行で分かるのは**向きだけ**です。", "向きだけだと断る")
in_text("この読み方が使えるのは、中が**ちょうど $x-a$ か $qx$ の形**のときだけです。",
        "使える形の限定")
in_text("$y = f(2x-6)$ を「中が $-6$ だから右へ $6$」と読むことはできません",
        "f(2x-6) の例")
eq(2 * x - 6, 2 * (x - 3), "2x-6 = 2(x-3)")

# --- 漸近線も動く理由（平面全体の点の移動）------------------------------
in_text("**変換は、平面のすべての点に同じことをします。**", "平面全体の点")
in_text("**グラフが触れていない漸近線も**、同じ規則で動きます。", "漸近線も動く")
not_in_text("**移動は、グラフ上のすべての点に同じことをします。**",
            "グラフ上の点だけ、という言い方は消した")
in_text("### 6. 特徴のある点や線は、どう動くか {#features}", "第 6 節の見出し")

# --- 「1 点で確かめる」の参照先 -----------------------------------------
not_in_text("$1$ 点で確かめる**のが確実です（[第 7 節](#answers)）",
            "確かめ方を第 7 節に送っていない")
not_in_text("その場で出せます（[第 7 節](#answers)）", "確かめ方を第 7 節に送っていない")
chk(TEXT.count("（[第 7 節](#answers)）") == 2,
    "第 7 節への参照は「名前・量・向き」の 2 か所だけ")
in_text("$1$ つの点でやってみれば、その場で出せます（[Why it works](#why-it-works)）。",
        "第 6 節の参照先")
in_text("（その確かめ方も [Why it works](#why-it-works) にあります）。",
        "第 2 節の参照先")

# --- 順番の理由から、無関係なリンクを外した ------------------------------
in_text("あとからかけると、**先に足した $1$ まで一緒に $3$ 倍されてしまう**からです。",
        "順番の理由")
not_in_text("**かけ算と足し算の順番を入れかえられない**からです", "無関係なリンクは消した")

# --- 電卓のメニュー名 ---------------------------------------------------
in_text("`menu → Actions → Insert Slider`", "Insert Slider（単数）")
in_text("**変数名を $a$ に変えて**から", "変数名を変える手順")
not_in_text("Add Sliders", "存在しないメニュー名は消した")

# --- 設問の英語 ---------------------------------------------------------
in_text("[Explain why the graph of $y = f(x-4)$ is a translation of the graph "
        "of $y = f(x)$ to the right and not to the left.]", "例題1(d) の英語")
in_text("followed by a translation by the vector", "例題4 は by the vector")
in_text("Write down the coordinates of the image of this point", "演習5 は image")
not_in_text("the corresponding point on the graph of $y = f(-x)$",
            "corresponding point は消した")
not_in_text("*A point is on $y = f(x-4)$ when $y = f(x-4)$",
            "同語反復の解答例は消した")
in_text("*A point $(x, y)$ lies on $y = f(x-4)$ when the value fed into $f$ is $x-4$.",
        "例題1(d) の解答例（直したもの）")

# --- 検算を独立した道すじにした ------------------------------------------
# 例題1(c)
in_text("**検算（(c) について）。** **式を書き下して、vertex form として読みます。**",
        "例題1(c) の検算の見出し")
not_in_text("**式を展開して、頂点の式でも読みます。**", "中身と合わない見出しは消した")
# 例題2(c)
eq((x ** 2 - 4 * x).subs(x, 4), 0, "例題2 検算 f(4) = 0")
in_text("**展開した式を使わず、もとの $f$ に入れ直します。**", "例題2(c) の検算は代入")
not_in_text("もとのグラフ上の点 $(4, 0)$ は、$y$ 軸で折り返すと $(-4, 0)$ に移ります",
            "表の言い直しは消した")
# 例題3(c)
eq(3 * (x ** 2 - 9), 3 * x ** 2 - 27, "3f(x) = 3x^2-27")
sols(3 * x ** 2 - 27, sp.FiniteSet(-3, 3), "3f(x) の x 切片は ±3")
in_text("**変換後の式を書き下して読みます。** $y = 3f(x) = 3\\big(x^{2}-9\\big) = 3x^{2}-27$",
        "例題3(c) の検算は式を書き下す")
in_text("**縦の拡大では $x$ 切片が動かない**", "ついでに分かること")
not_in_text("**もとの $y$ 切片から出し直します。**", "同じかけ算のくり返しは消した")
# 例題4：検算の順と、逆にたどる検算
_m1 = TEXT.index("**検算（(a) について）。** **点で追います。**")
_m2 = TEXT.index("**検算（(b) について）。** **像から、逆にたどって戻します。**")
_m3 = TEXT.index("**検算（(c) について）。** **同じ点で、逆の順に追います。**")
chk(_m1 < _m2 < _m3, "例題4 の検算は (a) → (b) → (c) の順")
eq((3 + 5) / 2, 4, "逆にたどると 4 に戻る")
not_in_text("もし $(0, 1)$ がもとのグラフ上にあれば", "必ず成り立つ検算は消した")
# 演習9
_f9 = x ** 2 - 4 * x + 3
eq(_f9.subs(x, 0), 3, "演習9 検算 f(0) = 3")
eq(sp.expand(_f9.subs(x, -x)), x ** 2 + 4 * x + 3, "演習9 検算 f(-x)")
eq(sp.expand(_f9.subs(x, -x)).subs(x, 0), 3, "演習9 検算 f(-0) = 3")
sols(_f9, sp.FiniteSet(1, 3), "演習9 もとの x 切片 1, 3")
sols(sp.expand(_f9.subs(x, -x)), sp.FiniteSet(-3, -1), "演習9 折り返し後 -1, -3")
in_text("**$y$ 切片が $0$ でない例で見ます。**", "演習9 の検算は退化していない例")
not_in_text("$f(x) = x^{2}-4x$ なら $f(0) = 0$、$f(-x) = x^{2}+4x$ でこれも",
            "y 切片が 0 の例は消した")


# ══════════════════════════════════════════════════════════
# C01  $f(ax+b)$ が「SL 全体で出ない」と読めた表現を、2.11 の範囲に限る
# ══════════════════════════════════════════════════════════
in_text("**これは 2.11 の範囲の話で、SL 全体で出ないという意味では"
        "ありません。**", "C01 範囲の限定")
in_text("../03-geometry/aasl-3-7b.qmd#shift-c", "C01 3.7b へのリンク")
in_text("**ちがいは、かっこが $b(x+c)$ の形にくくってあることです。**",
        "C01 くくってあるかどうか")
not_in_text("SL では横どうしが混ざる形（下の callout）が出ない",
            "C01 旧まとめが消えている")
not_in_text("つまり、横向きの平行移動と横向きの拡大を**同時に**含む形は"
            "出ません。", "C01 旧 callout が消えている")
# 3.7 の形は、確かに横の拡大と横の平行移動を同時に含む
_c01x, _c01b, _c01c = sp.symbols("x b c")
chk(sp.simplify(sp.sin(_c01b * (_c01x + _c01c))
                - sp.sin(_c01b * _c01x + _c01b * _c01c)) == 0,
    "C01 b(x+c) は bx+bc と同じ")
chk(sp.simplify(sp.sin(2 * (sp.Symbol("x") + sp.pi / 2))
                - sp.sin(2 * sp.Symbol("x") + sp.pi)) == 0,
    "C01 sin(2x+pi) は sin(2(x+pi/2))")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
