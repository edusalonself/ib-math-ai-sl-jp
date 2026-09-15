"""AA SL 3.5a（単位円による定義）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_5a.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-5a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_5a.py"), encoding="utf-8").read()
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


def pt(a):
    return (sp.cos(a), sp.sin(a))


# ══════════════════════════════════════════════════════════
# 0. 定義そのもの
# ══════════════════════════════════════════════════════════
# 軸の上の 4 点
for _a, _xy in [(0, (1, 0)), (PI / 2, (0, 1)), (PI, (-1, 0)),
                (3 * PI / 2, (0, -1))]:
    eq(sp.cos(_a), _xy[0], f"cos の値 ({_a})")
    eq(sp.sin(_a), _xy[1], f"sin の値 ({_a})")
in_text("| 点 | $(1,\\ 0)$ | $(0,\\ 1)$ | $(-1,\\ 0)$ | $(0,\\ -1)$ |",
        "軸の上の 4 点の表")
# 単位円の上にある
for _a in [0, PI / 6, PI / 2, 2 * PI / 3, PI, 5 * PI / 4, 3 * PI / 2, 2]:
    eq(sp.cos(_a) ** 2 + sp.sin(_a) ** 2, 1, f"単位円の上 ({_a})")
# tan の定義
eq(sp.tan(PI / 6), sp.sin(PI / 6) / sp.cos(PI / 6), "tan = sin/cos")
eq(sp.tan(PI / 4), 1, "tan(π/4) = 1")
eq(sp.tan(PI), 0, "tan π = 0")
chk(sp.cos(PI / 2) == 0, "cos(π/2) = 0")
chk(sp.cos(3 * PI / 2) == 0, "cos(3π/2) = 0")
chk(sp.tan(PI / 2) is sp.zoo or sp.tan(PI / 2) == sp.zoo,
    f"tan(π/2) は値をもたない: {sp.tan(PI / 2)}")
# 範囲
chk(sp.maximum(sp.cos(TH), TH) == 1 and sp.minimum(sp.cos(TH), TH) == -1,
    "-1 ≤ cos θ ≤ 1")
chk(sp.maximum(sp.sin(TH), TH) == 1 and sp.minimum(sp.sin(TH), TH) == -1,
    "-1 ≤ sin θ ≤ 1")
# 折り返しの関係
eq(sp.cos(-TH), sp.cos(TH), "cos(-θ) = cos θ")
eq(sp.sin(-TH), -sp.sin(TH), "sin(-θ) = -sin θ")
eq(sp.cos(PI - TH), -sp.cos(TH), "cos(π-θ) = -cos θ")
eq(sp.sin(PI - TH), sp.sin(TH), "sin(π-θ) = sin θ")
eq(sp.cos(PI + TH), -sp.cos(TH), "cos(π+θ) = -cos θ")
eq(sp.sin(PI + TH), -sp.sin(TH), "sin(π+θ) = -sin θ")
eq(sp.tan(-TH), -sp.tan(TH), "tan(-θ) = -tan θ")
eq(sp.tan(PI - TH), -sp.tan(TH), "tan(π-θ) = -tan θ")
eq(sp.tan(PI + TH), sp.tan(TH), "tan(π+θ) = tan θ")
eq(sp.cos(TH + 2 * PI), sp.cos(TH), "cos(θ+2π) = cos θ")
eq(sp.sin(TH + 2 * PI), sp.sin(TH), "sin(θ+2π) = sin θ")
# 象限の符号（代表の角で）
for _q, _a, _cs, _sn, _tn in [(1, PI / 6, 1, 1, 1), (2, 2 * PI / 3, -1, 1, -1),
                              (3, 5 * PI / 4, -1, -1, 1),
                              (4, 7 * PI / 4, 1, -1, -1)]:
    chk(sp.sign(sp.cos(_a)) == _cs, f"第 {_q} 象限の cos の符号")
    chk(sp.sign(sp.sin(_a)) == _sn, f"第 {_q} 象限の sin の符号")
    chk(sp.sign(sp.tan(_a)) == _tn, f"第 {_q} 象限の tan の符号")
in_text("| 第 $3$ | $\\pi < \\theta < \\dfrac{3\\pi}{2}$ | $-$ | $-$ | $+$ |",
        "第 3 象限の行")
in_text("| 第 $2$ | $\\dfrac{\\pi}{2} < \\theta < \\pi$ | $-$ | $+$ | $-$ |",
        "第 2 象限の行")
# 本文の走る例
eq(sp.tan(PI / 4), 1, "本文 tan(π/4) = 1")
in_text("だから $\\tan\\dfrac{\\pi}{4} = 1$ で、直線は $y = x$ です。", "本文の直線の例")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  軸の上の点
# ══════════════════════════════════════════════════════════
eq(sp.cos(PI), -1, "例題1(a) x 座標 -1")
eq(sp.sin(PI), 0, "例題1(a) y 座標 0")
eq(sp.cos(3 * PI / 2), 0, "例題1(b) cos = 0")
eq(sp.sin(3 * PI / 2), -1, "例題1(b) sin = -1")
_a1, _b1 = sp.symbols("a1 b1", real=True)
eq(sp.cos(TH + PI), -sp.cos(TH), "例題1(c) x 座標は -a")
eq(sp.sin(TH + PI), -sp.sin(TH), "例題1(c) y 座標は -b")
eq((-1) ** 2 + 0 ** 2, 1, "例題1(a) 検算 単位円の上")
eq(sp.cos(TH + 2 * PI), sp.cos(TH), "例題1(c) 検算 2 回で戻る")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  折り返し
# ══════════════════════════════════════════════════════════
_t2 = PI / 5  # 0 < θ < π/2 の代表
chk(sp.cos(PI - _t2) < 0 and sp.sin(PI - _t2) > 0, "例題2(a) 第 2 象限の符号")
chk(sp.cos(-_t2) > 0 and sp.sin(-_t2) < 0, "例題2(b) 第 4 象限の符号")
eq(sp.sin(PI - _t2), sp.sin(_t2), "例題2(c) sin(π-θ) = sin θ")
eq(sp.cos(-_t2), sp.cos(_t2), "例題2(c) cos(-θ) = cos θ")
eq(sp.tan(PI - _t2), -sp.tan(_t2), "例題2(d) tan(π-θ) = -tan θ")
chk(sp.tan(_t2) > 0 and sp.tan(PI - _t2) < 0, "例題2(d) 検算 符号が反対")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  直線
# ══════════════════════════════════════════════════════════
eq(R(4, 4), 1, "例題3(b) 傾き 1")
eq(sp.tan(PI / 4), 1, "例題3(b) θ = π/4")
eq(R(3, -3), -1, "例題3(c) 傾き -1")
eq(sp.tan(3 * PI / 4), -1, "例題3(c) θ = 3π/4")
eq(PI - PI / 4, 3 * PI / 4, "例題3(c) π - π/4")
chk(sp.cos(3 * PI / 4) < 0 and sp.sin(3 * PI / 4) > 0, "3π/4 は第 2 象限")
chk(4 * sp.tan(PI / 4) == 4, "例題3(b) 検算 (4, 4) を通る")
chk(sp.cos(PI / 2) == 0, "例題3(d) π/2 では傾きがない")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  周期と 3π - θ
# ══════════════════════════════════════════════════════════
eq(sp.cos(TH + 2 * PI), sp.cos(TH), "例題4(a) x 座標は変わらない")
eq(sp.sin(TH + 2 * PI), sp.sin(TH), "例題4(a) y 座標は変わらない")
eq(sp.tan(TH + PI), sp.tan(TH), "例題4(b) tan(θ+π) = tan θ")
eq(3 * PI - TH, (PI - TH) + 2 * PI, "例題4(c) 3π-θ = (π-θ)+2π")
eq(sp.tan(3 * PI - TH), -sp.tan(TH), "例題4(c) tan(3π-θ) = -tan θ")
eq(sp.sin(TH + 4 * PI), sp.sin(TH), "例題4(d) sin(θ+4π) = sin θ")
# (b) の検算：象限が対になる
for _a in [PI / 6, 2 * PI / 3]:
    chk(sp.sign(sp.tan(_a)) == sp.sign(sp.tan(_a + PI)),
        f"例題4(b) 検算 θ と θ+π で tan の符号が同じ ({_a})")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(sp.cos(3 * PI / 2), 0, "演習1 x 座標 0")
eq(sp.sin(3 * PI / 2), -1, "演習1 y 座標 -1")
eq(0 ** 2 + (-1) ** 2, 1, "演習1 検算 単位円の上")
eq(sp.tan(PI), 0, "演習2 tan π = 0")
eq(sp.sin(PI) / sp.cos(PI), 0, "演習2 検算 0/(-1)")
chk(sp.cos(2 * PI / 3) < 0 and sp.sin(2 * PI / 3) > 0 and sp.tan(2 * PI / 3) < 0,
    "演習3 第 2 象限の符号")
eq(sp.sin(-TH), -sp.sin(TH), "演習4 sin(-θ) = -sin θ")
eq(sp.cos(-TH), sp.cos(TH), "演習4 検算 cos は動かない")
eq(R(6, 6), 1, "演習5 傾き 1")
eq(sp.tan(PI / 4), 1, "演習5 θ = π/4")
eq(sp.cos(PI / 4), sp.sin(PI / 4), "演習5 検算 x 座標と y 座標が等しい")
eq(sp.cos(TH + 2 * PI), sp.cos(TH), "演習6 cos(θ+2π) = cos θ")
eq(sp.cos(2 * PI), 1, "演習6 検算 cos 2π = 1")
eq(sp.cos(0), 1, "演習6 検算 cos 0 = 1")
chk(sp.cos(PI / 2) == 0 and sp.sin(PI / 2) == 1, "演習7 (0, 1) なので分母が 0")
eq(sp.sin(2 * PI - TH), -sp.sin(TH), "演習8 sin(2π-θ) = -sin θ")
eq(2 * PI - TH, -TH + 2 * PI, "演習8 2π-θ = -θ+2π")
chk(sp.tan(3 * PI / 4) < 0 and PI / 2 < float(3 * PI / 4) < float(PI),
    "演習9 傾きが負なら第 2 象限の向き")
for _a in [PI / 6, PI / 4, PI / 3]:
    chk(sp.tan(_a) > 0, f"演習9 第 1 象限では tan > 0 ({_a})")
for _a in [2 * PI / 3, 3 * PI / 4, 5 * PI / 6]:
    chk(sp.tan(_a) < 0, f"演習9 第 2 象限では tan < 0 ({_a})")
eq(sp.tan(0), 0, "演習9 θ = 0 では tan = 0")
eq(sp.tan(PI + TH), sp.tan(TH), "演習10 正しい関係は tan(π+θ) = tan θ")
chk(sp.simplify(sp.tan(PI + PI / 6) + sp.tan(PI / 6)) != 0,
    "演習10 生徒の -tan θ は誤り")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("(-a,\\ -b)", "例題1(c)"), ("(-a,\\ b)", "例題2(a)"),
                ("(a,\\ -b)", "例題2(b)"), ("(p,\\ -q)", "演習4"),
                ("\\frac{3\\pi}{4}$$", "例題3(c)"), ("(4,\\ 4)", "例題3(b)"),
                ("(-3,\\ 3)", "例題3(c)"), ("(6,\\ 6)", "演習5"),
                ("\\tan\\pi", "演習2"), ("\\sin(2\\pi - \\theta)", "演習8"),
                ("\\sin(\\theta + 4\\pi)", "例題4(d)"),
                ("\\tan(3\\pi - \\theta)", "例題4(c)")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **3.5** の欄に `Identity for tanθ` として印刷されています。", "tan の欄")
in_text("> $\\tan\\theta = \\dfrac{\\sin\\theta}{\\cos\\theta}$", "tan を逐語で")
chk(TEXT.count("\n> ") == 1, f"引用は公式集の 1 つだけ: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 1, "公式集の callout は 1 つ")
not_in_text("Definition of cos", "シラバス本文は引かない")
not_in_text("Includes the relationship between angles in different quadrants",
            "Guidance は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("**分母が $0$ のときは定まりません。** そこは公式集には書かれていないので、"
        "自分で気をつけます。", "定まらないことは公式集にない")
# ★ 正確な値の表（3.5b で扱う）はここには置かない
chk("\\sqrt{3}}{2}" not in TEXT, "√3/2 のような正確な値は 3.5b に回す")
chk("\\sqrt{2}}{2}" not in TEXT, "√2/2 のような正確な値は 3.5b に回す")
chk("ambiguous" not in TEXT, "あいまいな場合は 3.5b で扱う")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("角は、**$x$ 軸の正の向きから測ります**。**anticlockwise**（反時計回り）が正、"
        "**clockwise**（時計回り）が負です。", "角の測り方")
in_text("方位角（[SL 3.3](aasl-3-3.qmd#bearings)）とはちがい、**北からでも時計回りでも"
        "ありません。**", "方位角とのちがい")
in_text("鋭角のところで前の定義と一致しているので、これは**広げ方として筋が通っています**。",
        "拡張の筋")
in_text("と書けます（$\\theta \\ne \\dfrac{\\pi}{2}$ のとき）。", "直線の式の但し書き")
in_text("$\\tan\\theta$ が定まる角では", "tan の関係の但し書き")
in_text("## $\\sin$ と $\\cos$ で、変わり方がちがいます", "sin と cos のちがい")
in_text("## $y = x\\tan\\theta$ の $\\theta$ を傾きと読む", "傾きと角のちがい")

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
in_text("どちらも「値がない」ことの表れです。", "電卓の返し方の意味")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
_expl = len(re.findall(r"Explain why|Identify the error, and", TEXT))
chk(TEXT.count("{.model-answer}") == 8,
    f"model-answer が 8: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl35a-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl35a", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _tgt in ["aasl-3-2", "aasl-3-3"]:
    _TT = open(os.path.join(BASE, _tgt + ".qmd"), encoding="utf-8").read()
    for _a2 in set(re.findall(r"\]\(" + _tgt + r"\.qmd#([a-z0-9-]+)\)", TEXT)):
        chk(("{#" + _a2 + "}") in _TT, _tgt + " 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl35a-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl35a-axes", "tbl-aasl35a-signs", "eq-aasl35a-def",
             "eq-aasl35a-range", "eq-aasl35a-tan", "eq-aasl35a-reflect",
             "eq-aasl35a-tanreflect", "eq-aasl35a-turn", "eq-aasl35a-line"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
for _lab in ["tbl-aasl35a-axes", "tbl-aasl35a-signs", "eq-aasl35a-def",
             "eq-aasl35a-tan", "eq-aasl35a-reflect", "eq-aasl35a-tanreflect",
             "eq-aasl35a-turn", "eq-aasl35a-line"]:
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
SVG = os.path.join(BASE, "img", "aasl-3-5a-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-5a-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) The unit circle", "図(a) の題")
in_fig("$P(\\\\cos\\\\theta,\\\\ \\\\sin\\\\theta)$", "図(a) の P の座標")
in_fig("the radius is $1$, so the coordinates of $P$ are the ", "図(a) の説明")
in_fig("(b) Signs, and reflections", "図(b) の題")
in_fig("all $> 0$", "図(b) の第 1 象限")
in_fig("$\\\\sin\\\\theta > 0$", "図(b) の第 2 象限")
in_fig("$\\\\tan\\\\theta > 0$", "図(b) の第 3 象限")
in_fig("$\\\\cos\\\\theta > 0$", "図(b) の第 4 象限")
in_fig("the four points are reflections of one another in the ", "図(b) の説明")
in_text("(a) On the unit circle the point at angle $\\theta$, measured "
        "anticlockwise from the positive $x$-axis", "キャプションが (a) を説明")
in_text("(b) The signs of the three ratios in the four quadrants",
        "キャプションが (b) を説明")
chk(set(re.findall(r"\d+", FIGSTR)) <= {"0", "1"},
    f"図の数字は 0 と 1 だけ: {set(re.findall(chr(92) + 'd+', FIGSTR))}")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-5a.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-4.qmd") < DRAFT.index("aasl-3-5a.qmd"), "並びが 3.4 → 3.5a")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-5a.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| unit circle |", "| quadrant |", "| anticlockwise |",
           "| gradient |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 直線の節に、角の範囲を付けた ----------------------------------------
in_text("$\\theta$ に $\\pi$ を足しても同じ直線になるので、**$0 \\le \\theta < \\pi$ の"
        "範囲で考えれば足ります**。", "直線は 0 ≤ θ < π で考える")
in_text("$\\cos\\theta = 0$ となる角（$\\theta = \\dfrac{\\pi}{2}$、$\\dfrac{3\\pi}{2}$、…）"
        "では、直線は $y$ 軸そのもの", "cos θ = 0 の角すべて")
not_in_text("$\\theta = \\dfrac{\\pi}{2}$ のときは、直線は $y$ 軸そのもの",
            "π/2 だけを挙げる言い方は消した")
eq(sp.tan(PI / 4 + PI), sp.tan(PI / 4), "θ に π を足しても傾きは同じ")
chk(sp.cos(3 * PI / 2) == 0, "3π/2 でも cos は 0")

# --- tan(π/4) = 1 の根拠と、3.5b への案内 --------------------------------
in_text("$\\dfrac{\\pi}{4}$ は $0$ と $\\dfrac{\\pi}{2}$ のちょうど真ん中なので、その点は "
        "$2$ つの軸から等しい位置にあり、$x$ 座標と $y$ 座標が等しくなります",
        "tan(π/4) = 1 の根拠")
in_text("**このページで使う正確な値は、軸の上の $0$ と $\\pm 1$、それに "
        "$\\tan\\dfrac{\\pi}{4} = 1$ だけです。**", "使う正確な値を宣言")
in_text("次のページ SL 3.5b でまとめます。", "3.5b への案内")
eq(sp.cos(PI / 4), sp.sin(PI / 4), "π/4 では 2 座標が等しい")

# --- 広げ方の説明を、弧の長さから ----------------------------------------
in_text("半径 $1$ の円では、角 $\\theta$ に対する弧の長さは $l = r\\theta = \\theta$ です"
        "（[SL 3.4](aasl-3-4.qmd#arc)）。", "弧の長さから")
in_text("$\\theta$ と $\\theta + 2\\pi$ のように**ちがう角が同じ点になる**ことはありますが、"
        "決めているのは「角から点へ」の向きなので、値が $2$ つになることはありません。",
        "1 対 1 でなくてよい")
not_in_text("単位円の上の点は、角を決めれば $1$ つに決まります。だから",
            "同語反復は消した")

# --- 電卓の返し方 --------------------------------------------------------
in_text("`undef`（未定義）が返ります。", "undef")
in_text("角を小数（$1.5707963$ など）で入れた場合は、けた数の大きな数が返ることも"
        "あります。", "小数で入れた場合")
in_text("電卓が `undef` や大きな数を返しても、それは値ではありません。",
        "Common errors も直した")

# --- anticlockwise / gradient を英語が先で ------------------------------
in_text("**anticlockwise**（反時計回り）", "anticlockwise を英語が先で")
in_text("**clockwise**（時計回り）", "clockwise を英語が先で")
in_text("**原点と $P$ を結ぶ直線の gradient**（傾き）", "gradient を英語が先で")

# --- 例題1(c)：θ を一般にもどした ----------------------------------------
in_text("[Now let $\\theta$ be any angle, and suppose $\\mathrm{P}$ has coordinates",
        "例題1(c) は一般の θ")
in_text("今度は $\\theta$ をどんな角でもよいものとします。", "日本語訳も直した")
# 例題1(a) の検算
in_text("**検算（(a) について）。** **折り返して見ます。**", "例題1(a) の検算")
not_in_text("**もう $1$ つの座標でも見ます。**", "弱い検算は消した")

# --- 例題3：単位円と 2 点で交わることを踏まえた -------------------------
in_text("passes through the point $(\\cos\\theta,\\ \\sin\\theta)$ of the unit circle.",
        "交点の 1 つだと書いた")
not_in_text("meets the unit circle at the point $(\\cos\\theta,\\ \\sin\\theta)$",
            "1 点で交わるという言い方は消した")
chk(sp.simplify(sp.cos(2 * PI / 3) + sp.cos(2 * PI / 3 + PI)) == 0,
    "反対側の点も同じ直線の上")
# 例題3(c) に範囲
in_text("Write down the gradient of $M$, and find the angle $\\theta$ it makes with "
        "the positive $x$-axis, where $0 \\le \\theta < \\pi$.", "例題3(c) に範囲")
chk(TEXT.count("where $0 \\le \\theta < \\pi$") >= 3, "範囲を書いた設問が 3 つ以上")

# --- 例題4：条件を、要る小問だけに ---------------------------------------
in_text("[In this question $\\theta$ is any angle.]{.q-en}", "例題4 の前置き")
in_text("for every $\\theta$ at which $\\tan\\theta$ is defined.]{.q-en}", "例題4(b) の条件")
in_text("whenever $\\tan\\theta$ is defined.]{.q-en}", "例題4(c) の条件")
not_in_text("[$\\theta$ is an angle for which $\\tan\\theta$ is defined.]{.q-en}",
            "全体にかける条件は消した")
in_text("$2\\pi$ は $1$ 周で点が同じなので、$\\cos$ も $\\sin$ も変わらず"
        "（@eq-aasl35a-turn）、その比である $\\tan$ も変わりません。", "tan の周期の根拠")

# --- 演習1：定義が広がる理由 ---------------------------------------------
in_text("[1]{.ex-no} [Explain why $\\cos\\theta$ and $\\sin\\theta$ have a value for every "
        "angle $\\theta$", "演習1 は Explain")
in_text("because each extra turn of $2\\pi$ returns to the same point", "何周しても 1 点")
not_in_text("[Write down the coordinates of the point on the unit circle at an angle "
            "of $\\dfrac{3\\pi}{2}$.]", "例題1(b) と重なる演習1 は消した")
eq(sp.cos(9 * PI / 2 - 4 * PI), sp.cos(PI / 2), "9π/2 は 2 周ぶん引くと π/2")
eq(sp.sin(9 * PI / 2), 1, "sin(9π/2) = 1")

# --- 演習2 の検算を独立させた --------------------------------------------
in_text("**検算。** **$\\pi$ を足す関係で見ます。**", "演習2 の検算")
not_in_text("原点と $(-1,\\ 0)$ を結ぶ直線は $x$ 軸そのもので、傾きは $0$ です",
            "同じ比を繰り返す検算は消した")
eq(sp.tan(PI + 0), sp.tan(0), "tan π = tan 0")

# --- 演習5：第 3 象限の点 -------------------------------------------------
in_text("[A line passes through the origin and the point $(-5,\\ -5)$.", "演習5 は (-5,-5)")
eq(R(-5, -5), 1, "演習5 傾き 1")
in_text("**$\\dfrac{5\\pi}{4}$ と答えないでください。**", "範囲の注意")
eq(sp.tan(5 * PI / 4), 1, "5π/4 でも傾きは 1")
chk(float(5 * PI / 4) >= float(PI), "5π/4 は範囲の外")
not_in_text("[A line passes through the origin and the point $(6,\\ 6)$.",
            "本文と重なる演習5 は消した")

# --- 演習7：定まらない角をすべて ----------------------------------------
in_text("write down all the angles $\\theta$ with $0 \\le \\theta < 4\\pi$ at which "
        "$\\tan\\theta$ is not defined.]{.q-en}", "演習7 は角をすべて")
in_text("$$\\theta = \\frac{\\pi}{2},\\ \\frac{3\\pi}{2},\\ \\frac{5\\pi}{2},\\ \\frac{7\\pi}{2}$$",
        "演習7 の答え")
for _k in range(4):
    _a = PI / 2 + _k * PI
    chk(sp.cos(_a) == 0, f"cos が 0: {_a}")
    chk(float(_a) < float(4 * PI), f"4π 未満: {_a}")
chk(sp.cos(PI / 2 + 4 * PI) == 0 and float(PI / 2 + 4 * PI) >= float(4 * PI),
    "次の角は 4π 以上")
in_text("**検算（角の並びについて）。** **$\\pi$ ずつ増えるか見ます。**", "演習7 の検算")

# --- 演習9：英文と場合分け ------------------------------------------------
in_text("The angle it makes with the positive $x$-axis is $\\theta$, where "
        "$0 \\le \\theta < \\pi$. Explain why $\\dfrac{\\pi}{2} < \\theta < \\pi$.]{.q-en}",
        "演習9 の英文")
not_in_text("satisfies $\\dfrac{\\pi}{2} < \\theta < \\pi$, where $0 \\le \\theta < \\pi$",
            "読みにくい英文は消した")
in_text("$\\theta = 0$・第 $1$ 象限・$\\theta = \\dfrac{\\pi}{2}$・第 $2$ 象限の $4$ つに"
        "分けます。", "4 つに分ける")
in_text("At $\\theta = 0$ the point is $(1,\\ 0)$, so $\\tan 0 = 0$.", "θ = 0 を別に扱う")
eq(sp.tan(0), 0, "tan 0 = 0")

# --- Hence write down ----------------------------------------------------
chk(TEXT.count("ence write down") == 2, f"(H/h)ence write down が 2 か所: {TEXT.count('ence write down')}")
chk(TEXT.count("Hence write $") == 0, "Hence write は使わない")

# --- できることの言い直し ------------------------------------------------
in_text("- $\\theta$ が鋭角でなくても（鈍角でも、負でも、$2\\pi$ より大きくても）、",
        "できることの 2 つ目")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
