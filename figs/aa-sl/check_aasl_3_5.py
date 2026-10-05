"""AA SL 3.5（単位円・正確な値・あいまいな場合。3.5a と 3.5b を結合）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_5.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-5.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_5.py"), encoding="utf-8").read()
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
not_in_text("| 点 | $(1,\\ 0)$ | $(0,\\ 1)$ | $(-1,\\ 0)$ | $(0,\\ -1)$ |",
            "4 点の表は図にした（2026-10-01）")
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
chk(TEXT.count("\n> ") == 1, f"引用は公式集の 1 つ（単位円）: {TEXT.count(chr(10) + '> ')}")
chk(TEXT.count("::: {.callout-important}") == 1, "公式集の callout は 1 つ")
not_in_text("Definition of cos", "シラバス本文は引かない")
not_in_text("Includes the relationship between angles in different quadrants",
            "Guidance は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("**分母が $0$ のときは定まりません。** そこは公式集には書かれていないので、"
        "自分で気をつけます。", "定まらないことは公式集にない")
# ★ 正確な値の表（3.5b で扱う）はここには置かない
in_text("\\dfrac{\\sqrt{3}}{2}", "正確な値 √3/2 がこのページにある")
in_text("\\dfrac{\\sqrt{2}}{2}", "正確な値 √2/2 がこのページにある")
in_text("**ambiguous case**（あいまいな場合）", "あいまいな場合もこのページ")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("角は、**$x$ 軸の正の向きから測ります**。**anticlockwise**（反時計回り）が正、"
        "**clockwise**（時計回り）が負です。", "角の測り方")
in_text("**bearings**（方位角）（[SL 3.3](aasl-3-3.qmd#bearings)）とはちがい、**北からでも時計回りでも"
        "ありません。**", "方位角とのちがい")
in_text("鋭角のところで前の定義と一致しているので、これは**広げ方として筋が通っています**。",
        "拡張の筋")
in_text("$\\tan\\theta$ が定まる角では", "tan の関係の但し書き")
in_text("## $\\sin$ と $\\cos$ で、変わり方がちがいます", "sin と cos のちがい")
# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips
        if not h_.startswith("解説") and h_ != "クリックすると開きます"]
chk(len(_gdc) == 2, f"GDC の折りたたみは 2 つ: {_gdc}")
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
chk(TEXT.count("{.model-answer}") == 9,
    f"model-answer が 9: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl35-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk(TEXT.count("::: {.callout-warning}") == 12,
    f"Common errors 10 + 本文の注意 2 で 12: {TEXT.count(chr(58)*3 + chr(32) + chr(123) + chr(46) + chr(99))}")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h_ for h_ in _h2 if h_ in _want] == _want, "5 つの見出しが所定の順")
chk([h_ for h_ in _h2 if h_ in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 7)), f"The idea が 1..6 で連番: {_idea}")
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
    chk(_r0 == "aasl35", "他ページの @-ref: " + _r0)
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
chk(TEXT.count("@fig-aasl35-idea") >= 1, "図を本文から参照している")
for _lab in ["tbl-aasl35-signs", "eq-aasl35-def",
             "eq-aasl35-range", "eq-aasl35-tan", "eq-aasl35-reflect",
             "eq-aasl35-tanreflect", "eq-aasl35-turn"]:
    chk(("{#" + _lab + "}") in TEXT, "ラベルがある: " + _lab)
for _lab in ["tbl-aasl35-signs", "eq-aasl35-def",
             "eq-aasl35-tan", "eq-aasl35-reflect", "eq-aasl35-tanreflect",
             "eq-aasl35-turn"]:
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
for _n in "abcde":
    _svg = os.path.join(BASE, "img", "aasl-3-5-idea-%s.svg" % _n)
    chk(os.path.exists(_svg), "図 (%s) がある" % _n)
    chk(not os.path.exists(_svg[:-4] + ".png"),
        "図 (%s) の PNG は消してある" % _n)
    chk(("](img/aasl-3-5-idea-%s.svg)" % _n) in TEXT,
        "本文が図 (%s) を貼っている" % _n)
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("The unit circle", "図(a) の題")
in_fig("$P(\\\\cos\\\\theta,\\\\ \\\\sin\\\\theta)$", "図(a) の P の座標")
in_fig("Signs, and reflections", "図(b) の題")
in_fig("all $> 0$", "図(b) の第 1 象限")
in_fig("$\\\\sin\\\\theta > 0$", "図(b) の第 2 象限")
in_fig("$\\\\tan\\\\theta > 0$", "図(b) の第 3 象限")
in_fig("$\\\\cos\\\\theta > 0$", "図(b) の第 4 象限")
# (d) の 2 つの三角形には 1・2・3・4・6 が出る（辺の比と角の分母）
chk(set(re.findall(r"\d+", FIGSTR)) <= {"0", "1", "2", "3", "4", "6"},
    f"図の数字は、辺の比と角の分母だけ: {set(re.findall(chr(92) + 'd+', FIGSTR))}")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
# 2026-10-05：AA SL は公開側（_quarto.yml）に移した
DRAFT = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-5.qmd" in DRAFT, "_quarto.yml に登録")
chk(DRAFT.index("aasl-3-4.qmd") < DRAFT.index("aasl-3-5.qmd"), "並びが 3.4 → 3.5a")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("- aa-sl/**/*.qmd" in PUB, "公開用の render に AA SL")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-5.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"\*\*全 (\d+) ページを公開しています\*\*", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「全 N ページ」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| unit circle |", "| quadrant |", "| anticlockwise |",
           "| gradient |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 直線の節に、角の範囲を付けた ----------------------------------------
not_in_text("$\\theta = \\dfrac{\\pi}{2}$ のときは、直線は $y$ 軸そのもの",
            "π/2 だけを挙げる言い方は消した")
eq(sp.tan(PI / 4 + PI), sp.tan(PI / 4), "θ に π を足しても傾きは同じ")
chk(sp.cos(3 * PI / 2) == 0, "3π/2 でも cos は 0")

# --- tan(π/4) = 1 の根拠と、3.5b への案内 --------------------------------
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
# --- 例題1(c)：θ を一般にもどした ----------------------------------------
in_text("[Now let $\\theta$ be any angle, and suppose $\\mathrm{P}$ has coordinates",
        "例題1(c) は一般の θ")
in_text("今度は $\\theta$ をどんな角でもよいものとします。", "日本語訳も直した")
# 例題1(a) の検算
in_text("**検算（(a) について）。** **折り返して見ます。**", "例題1(a) の検算")
not_in_text("**もう $1$ つの座標でも見ます。**", "弱い検算は消した")

# --- 例題3：単位円と 2 点で交わることを踏まえた -------------------------
not_in_text("meets the unit circle at the point $(\\cos\\theta,\\ \\sin\\theta)$",
            "1 点で交わるという言い方は消した")
chk(sp.simplify(sp.cos(2 * PI / 3) + sp.cos(2 * PI / 3 + PI)) == 0,
    "反対側の点も同じ直線の上")
# 例題3(c) に範囲
# --- 例題4：条件を、要る小問だけに ---------------------------------------
in_text("[In this question $\\theta$ is any angle.]{.q-en}", "例題4 の前置き")
in_text("for every $\\theta$ at which $\\tan\\theta$ is defined.]{.q-en}", "例題4(b) の条件")
in_text("whenever $\\tan\\theta$ is defined.]{.q-en}", "例題4(c) の条件")
not_in_text("[$\\theta$ is an angle for which $\\tan\\theta$ is defined.]{.q-en}",
            "全体にかける条件は消した")
in_text("$2\\pi$ は $1$ 周で点が同じなので、$\\cos$ も $\\sin$ も変わらず"
        "（@eq-aasl35-turn）、その比である $\\tan$ も変わりません。", "tan の周期の根拠")

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
eq(R(-5, -5), 1, "演習5 傾き 1")
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
not_in_text("satisfies $\\dfrac{\\pi}{2} < \\theta < \\pi$, where $0 \\le \\theta < \\pi$",
            "読みにくい英文は消した")
eq(sp.tan(0), 0, "tan 0 = 0")

# --- Hence write down ----------------------------------------------------
chk(TEXT.count("Hence write $") == 0, "Hence write は使わない")

# --- できることの言い直し ------------------------------------------------
in_text("- $\\theta$ が鋭角でなくても（鈍角でも、負でも、$2\\pi$ より大きくても）、",
        "できることの 2 つ目")

# ══════════════════════════════════════════════════════════
# 20. 2026-09-22：3.5a と 3.5b を結合した分
# ══════════════════════════════════════════════════════════
# --- 節の見出し ---------------------------------------------------------
in_text("### 1. unit circle（単位円） {#unit-circle}", "§1 の見出し")
in_text("### 2. $\\cos\\theta$、$\\sin\\theta$、$\\tan\\theta$ の定義 {#definitions}",
        "§2 の見出し")
in_text("### 3. quadrants and signs（象限と符号） {#quadrants}", "§3 の見出し")
in_text("### 4. the two special triangles（2 つの特別な三角形） {#special}",
        "§4 の見出し")
in_text("### 5. reference angle（参照角）と、折り返しでできる関係 {#reference}",
        "§5 の見出し")
in_text("### 6. 負の角・$2\\pi$ を超える角（periodicity） {#periodic}", "§6 の見出し")
not_in_text("### 7. the ambiguous case", "§7 は例題 4 の中へ移した")
not_in_text("{#ambiguous}", "#ambiguous は無い")
in_text("**この問題は、$2$ 辺と、そのあいだにない角**", "例題 4 が説明している")
in_text("これを **ambiguous case**（あいまいな場合）といいます。", "例題 4 で用語を出す")
_idea5 = [int(m) for m in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea5 == list(range(1, 7)), f"The idea が 1..6 で連番: {_idea5}")
for _a in ("{#tan}", "{#relations}", "{#line}", "{#triangles}", "{#table}",
           "{#reduce}", "{#howmany}", "{#writing}"):
    not_in_text(_a, "吸収したアンカーは残っていない: " + _a)
_OLDA, _OLDB = "aasl-3-5" + "a", "aasl-3-5" + "b"
not_in_text(_OLDA, "3.5a への参照は残っていない")
not_in_text(_OLDB, "3.5b への参照は残っていない")
not_in_text("[SL 3.5" + "a]", "SL 3.5a という呼び方は残っていない")
not_in_text("[SL 3.5" + "b]", "SL 3.5b という呼び方は残っていない")

# --- §2 に tan を吸収した -----------------------------------------------
in_text("**$\\tan\\theta$ は、unit circle のなかの直角三角形で、"
        "$\\dfrac{\\text{opposite}}{\\text{adjacent}}$ を使います。**", "§2 の tan の導入")
in_text("opposite $= \\sin\\theta$、adjacent $= \\cos\\theta$ なので、次のようになります。", "opposite・adjacent の言いかえ")
not_in_text("$2$ つの座標の割り算で決めます", "前の言い方は消した")
not_in_text("$2$ つの座標の比として定めます", "同上")
in_text("**そこでは $\\tan\\theta$ は定まりません（英語では `undefined`）。**",
        "undefined を併記した")
not_in_text("**原点と $P$ を結ぶ直線の gradient**（傾き）でもあります。",
            "gradient の段落は消したまま")

# --- §3 の表は 5 列（図の列は無い）---------------------------------------
in_text("| 象限 | $\\theta$ の範囲 | $\\cos\\theta$ | $\\sin\\theta$ | $\\tan\\theta$ |",
        "象限の表は 5 列")
chk("| 図 |" not in TEXT, "どの表にも「図」の列は無い")
_sig = [l for l in TEXT.split("\n") if l.startswith("| 第 $")]
chk(len(_sig) == 4, f"象限の表は 4 行: {len(_sig)}")

def _sgn(t):
    return "$+$" if t > 0 else "$-$"

for _q, _th in ((1, PI / 4), (2, 3 * PI / 4), (3, 5 * PI / 4), (4, 7 * PI / 4)):
    _cells = [x.strip() for x in _sig[_q - 1].split("|")[1:-1]]
    chk(_cells[2] == _sgn(sp.cos(_th)), f"第 {_q} 象限の cos の符号")
    chk(_cells[3] == _sgn(sp.sin(_th)), f"第 {_q} 象限の sin の符号")
    chk(_cells[4] == _sgn(sp.tan(_th)), f"第 {_q} 象限の tan の符号")

# --- §4 特別な三角形と、正確な値の表 -------------------------------------
in_text("**`exact values`（特別な三角比の値）は、この $2$ つの三角形から"
        "読み取ったものです。**", "§4 に exact values の小見出し")
in_text(": $0$ から $\\dfrac{\\pi}{2}$ までの正確な値 {#tbl-aasl35-exact}",
        "正確な値の表")
for _th, _s5, _c5, _t5 in ((PI / 6, R(1, 2), sp.sqrt(3) / 2, sp.sqrt(3) / 3),
                           (PI / 4, sp.sqrt(2) / 2, sp.sqrt(2) / 2, sp.Integer(1)),
                           (PI / 3, sp.sqrt(3) / 2, R(1, 2), sp.sqrt(3))):
    eq(sp.sin(_th), _s5, "表の sin")
    eq(sp.cos(_th), _c5, "表の cos")
    eq(sp.tan(_th), _t5, "表の tan")
chk(sp.simplify(sp.sqrt(1 ** 2 + 1 ** 2) - sp.sqrt(2)) == 0, "1,1 の斜辺は √2")
chk(sp.simplify(sp.sqrt(2 ** 2 - 1 ** 2) - sp.sqrt(3)) == 0, "2,1 の残りは √3")
in_fig("The two special triangles", "図 (d) の題")

# --- §5 参照角（新しい図と、4 手順）--------------------------------------
in_text("@fig-aasl35-idea-c を見てください。", "図 (c) を参照している")
in_fig("Reference angles", "図 (c) の題")
for _p in ("all $+$", "sin+", "tan+", "cos+"):
    in_fig(_p, "図 (c) の " + _p)
chk("BASE = (0.0, np.pi, np.pi, 2 * np.pi)" in FIGCODE,
    "図 (c) はいちばん近い x 軸に弧をかいている")
in_text("3. **もとの角がどの象限にあるかを見る。**", "手順 3：象限")
in_text("4. **その象限の符号を付ける**（[第 3 節](#quadrants)）。", "手順 4：符号")
in_text("**参照角は、折り返しと同じことを言っています。**", "折り返しとのつながり")
in_text(": 参照角の出し方 {#tbl-aasl35-ref}", "参照角の表")
for _th in (PI / 6, 5 * PI / 6, 7 * PI / 6, 11 * PI / 6):
    _ref = sp.Min(sp.Abs(_th), sp.Abs(PI - _th), sp.Abs(_th - PI),
                  sp.Abs(2 * PI - _th))
    eq(_ref, PI / 6, "参照角は π/6")
    eq(sp.Abs(sp.sin(_th)), sp.sin(PI / 6), "大きさは参照角の sin")
    eq(sp.Abs(sp.cos(_th)), sp.cos(PI / 6), "大きさは参照角の cos")
eq(sp.sin(5 * PI / 6), R(1, 2), "本文の例 sin(5π/6)")
eq(sp.cos(5 * PI / 6), -sp.sqrt(3) / 2, "本文の例 cos(5π/6)")

# --- §6 負の角・2π を超える角 -------------------------------------------
in_text("**大きい角や負の角の正確な値も、これで出せます。**", "§6 の書き出し")
in_text("そのあとは [第 5 節](#reference)と同じ $4$ 手順です。", "§6 から §5 へ")
in_text("$\\dfrac{9\\pi}{4} - 2\\pi = \\dfrac{\\pi}{4}$",
        "本文の例 9π/4")
in_text("$\\dfrac{17\\pi}{4} - 4\\pi = \\dfrac{\\pi}{4}$",
        "本文の例 17π/4")
not_in_text("$\\dfrac{7\\pi}{4}$", "前の例（−π/4）は消した")
eq(9 * PI / 4 - 2 * PI, PI / 4, "9π/4 − 2π = π/4")
eq(17 * PI / 4 - 4 * PI, PI / 4, "17π/4 − 4π = π/4")
for _th6 in (PI / 4, 9 * PI / 4, 17 * PI / 4):
    eq(sp.sin(_th6), sp.sqrt(2) / 2, "本文の例 sin")
    eq(sp.cos(_th6), sp.sqrt(2) / 2, "本文の例 cos")

# --- §7 あいまいな場合 ---------------------------------------------------
in_text(": $\\hat{A}$ が鋭角のとき {#tbl-aasl35-count}", "個数の表は例題 4 の中")
in_text("**答案では、こう書きます。**", "答案の書き方は例題 4 の中")
in_text("\\frac{a}{\\sin A} = \\frac{b}{\\sin B}", "正弦定理")
in_text("$\\sin(\\pi - B) = \\sin B$", "sin(π−B) = sin B")
eq(sp.sin(PI - TH), sp.sin(TH), "sin(π−θ) = sin θ")
in_text(": $\\hat{A}$ が鋭角のとき {#tbl-aasl35-count}", "個数の表")
in_fig("The ambiguous case", "図 (e) の題")
# 個数の判定を、実際の三角形で確かめる
for _a5, _b5, _A5, _num in ((4, 4 * sp.sqrt(2), PI / 6, 2),
                            (4, 9, PI / 6, 0),
                            (8, 8, PI / 6, 1)):
    _sinB = _b5 * sp.sin(_A5) / _a5
    if _sinB > 1:
        chk(_num == 0, "sin B > 1 なら三角形なし")
    elif sp.simplify(_sinB - 1) == 0:
        chk(_num == 1, "sin B = 1 なら 1 つ")
    elif _a5 >= _b5:
        chk(_num == 1, "a ≥ b なら 1 つ")
    else:
        chk(_num == 2, "b sin A < a < b なら 2 つ")

# --- 演習の出どころ -----------------------------------------------------
for _q in ("Explain why $\\cos\\theta$ and $\\sin\\theta$ have a value for every",
           "Explain why $\\tan\\theta$ is not defined when",
           "The angle $\\theta$ lies in the second quadrant",
           "Write down the exact value of $\\cos\\dfrac{\\pi}{3}$",
           "Find the exact value of $\\tan\\dfrac{5\\pi}{4}$",
           "Find the exact value of $\\sin\\dfrac{13\\pi}{6}$",
           "Show that there are two possible triangles",
           "Find the number of possible triangles"):
    in_text(_q, "演習にある: " + _q[:32])
eq(sp.tan(5 * PI / 4), 1, "演習 5 tan(5π/4) = 1")
eq(sp.sin(13 * PI / 6), R(1, 2), "演習 7 sin(13π/6) = 1/2")
eq(sp.cos(2 * PI / 3), -R(1, 2), "演習 4 cos(2π/3) = −1/2")

# --- 図には説明の文を書かない（方針 第 21 節）----------------------------
for _sent in ("the radius is $1$, so the coordinates of $P$ are the",
              "the four points are reflections of one another in the",
              "half a square, and half an equilateral triangle",
              "every exact value comes from reading a ratio off one",
              "two sides and an angle that is not between them",
              "the circle of radius $a$ centred at $C$ can meet the"):
    chk(_sent not in FIGSTR, "図に説明の文を書いていない: " + _sent[:32])

# --- 登録と、古いファイル -------------------------------------------------
chk(_OLDA + ".qmd" not in DRAFT and _OLDB + ".qmd" not in DRAFT,
    "3.5a・3.5b はもう登録されていない")
for _old in (_OLDA + ".qmd", _OLDB + ".qmd"):
    chk(not os.path.exists(os.path.join(BASE, _old)), _old + " は消した")
for _old in ("make_aasl_3_5" + "a.py", "make_aasl_3_5" + "b.py",
             "check_aasl_3_5" + "a.py", "check_aasl_3_5" + "b.py"):
    chk(not os.path.exists(os.path.join(HERE, _old)), _old + " は消した")

# --- 対訳表 -------------------------------------------------------------
GLO5 = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| unit circle |", "| quadrant |", "| reference angle |",
           "| ambiguous case |"]:
    chk(_t in GLO5, "対訳表にある: " + _t)



# ══════════════════════════════════════════════════════════
# 2026-09-29：図のキャプションは 1 行に収める（方針 第 23 節）
# ══════════════════════════════════════════════════════════
for _cm in re.finditer(r"^!\[(.*?)\]\(img/", TEXT, re.M):
    chk(0 < len(_cm.group(1)) <= 75,
        "図のキャプションは 75 字以内（%d 字）: %s"
        % (len(_cm.group(1)), _cm.group(1)[:50]))



# ══════════════════════════════════════════════════════════
# 2026-10-01：軸の上の 4 点は図に、参照角には α という名前を
# ══════════════════════════════════════════════════════════
not_in_text("{#tbl-aasl35-axes}", "4 点の表は消した")
in_text("![The four points where the unit circle meets the axes]"
        "(img/aasl-3-5-axes.svg){#fig-aasl35-axes width=100%}", "新しい図")
in_text("@fig-aasl35-axes に、その $4$ 点の $\\cos$ と $\\sin$ を書き入れて"
        "あります。", "図への参照")
chk(os.path.exists(os.path.join(BASE, "img", "aasl-3-5-axes.svg")),
    "SVG がある: aasl-3-5-axes.svg")
_F2 = FIG.replace("\\\\", "\\")
for _s in ("$\\cos 0 = 1$", "$\\sin 0 = 0$", "$\\cos\\frac{\\pi}{2} = 0$",
           "$\\sin\\frac{\\pi}{2} = 1$", "$\\cos\\pi = -1$", "$\\sin\\pi = 0$",
           "$\\cos\\frac{3\\pi}{2} = 0$", "$\\sin\\frac{3\\pi}{2} = -1$"):
    chk(_s in _F2, "図に書いてある: " + _s)
# 参照角 α
in_text("1. **reference angle**（参照角）$\\alpha$ を出す", "手順 1 に α")
in_text("2. **$\\alpha$ の $\\sin$・$\\cos$・$\\tan$ を、@tbl-aasl35-exact から"
        "読む。**", "手順 2 に α")
in_text("| 参照角 $\\alpha$ | $\\theta$ | $\\pi - \\theta$ | $\\theta - \\pi$ | "
        "$2\\pi - \\theta$ |", "表 4 に α")
in_text("参照角は $\\alpha = \\pi - \\dfrac{5\\pi}{6} = \\dfrac{\\pi}{6}$ です。",
        "例の参照角 α")
in_text("**よって、$\\sin\\alpha$ と $\\cos\\alpha$ の値を使います。**",
        "α を使う")
in_text("\\sin\\frac{5\\pi}{6} = \\sin\\alpha = \\frac{1}{2}, \\qquad "
        "\\cos\\frac{5\\pi}{6} = -\\cos\\alpha = -\\frac{\\sqrt{3}}{2}",
        "例の式も α で")


in_fig('figX, axX = plt.subplots(figsize=(5.6, 3.9))', "図は縦を詰めた")
in_fig('axX.set_xlim(-2.6, 2.6)', "横の範囲")
in_fig('axX.set_ylim(-1.85, 1.75)', "縦の範囲")
in_fig('axX.text(1.42, 0.06,', "右のラベルは軸の先より外・少し上")
in_fig('axX.text(-1.42, 0.06,', "左のラベルも同じ")
chk('axX.annotate("", xy=(1.35, 0), xytext=(-1.35, 0),' in FIG,
    "横軸はラベルに届かない長さ")
chk(1.35 < 1.42, "横軸の先より外にラベルがある")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
