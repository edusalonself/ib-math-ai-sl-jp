"""AA SL 1.8（無限等比級数の和）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_8.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-8.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_8.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x", real=True)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def _S(v):
    if isinstance(v, float):
        return sp.Rational(str(v))
    return sp.nsimplify(v, rational=True)


def eq(u, v, msg=""):
    chk(sp.simplify(_S(u) - _S(v)) == 0, msg + f"  ({u} vs {v})")


def ne(u, v, msg=""):
    chk(sp.simplify(_S(u) - _S(v)) != 0, msg + f"  ({u} vs {v})")


def Sinf(u1, r):
    """公式集の式から。"""
    return _S(u1) / (1 - _S(r))


def Sn(u1, r, n):
    """公式集の有限和の式から。"""
    return _S(u1) * (1 - _S(r) ** n) / (1 - _S(r))


def partial(u1, r, k):
    """1 項ずつ足した列（公式を使わない道すじ）。"""
    out, term, tot = [], _S(u1), 0
    for _ in range(k):
        tot += term
        out.append(tot)
        term *= _S(r)
    return out


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの
# ══════════════════════════════════════════════════════════
_u, _r, _n = sp.symbols("u r n", positive=True)
# 有限和の式から、r^n → 0 で無限和の式が出る
eq(sp.limit(_u * (1 - R(1, 2) ** _n) / (1 - R(1, 2)), _n, sp.oo),
   _u / (1 - R(1, 2)), "r=1/2 なら S_n → u/(1-r)")
for _rr in [R(1, 3), R(-1, 2), R(3, 4), R(-3, 4), R(1, 10)]:
    chk(abs(_rr) < 1, f"|{_rr}| < 1")
    # |r^n| = |r|^n → 0 なので、S_n の行き先は u/(1-r)
    chk(sp.limit(abs(_rr) ** _n, _n, sp.oo) == 0, f"|{_rr}|^n → 0")
    _tail = _u * abs(_rr) ** 60 / abs(1 - _rr)
    chk(abs(float(_tail.subs(_u, 1))) < 1e-6,
        f"r={_rr} では 60 項で誤差が消える")
# |r| >= 1 では発散する
for _rr in [2, 3, -2]:
    chk(sp.limit(abs(_rr) ** _n, _n, sp.oo) is sp.oo, f"|{_rr}|^n → ∞")
chk(sp.limit(2 ** _n - 1, _n, sp.oo) is sp.oo, "r=2 の S_n は発散")
# 部分和と公式が一致する
for _u0, _r0 in [(15, R(1, 3)), (8, R(-1, 2)), (24, R(1, 4)), (20, R(2, 5)),
                 (18, R(1, 3)), (5, R(-3, 4)), (8, R(1, 2)), (12, R(1, 2))]:
    _p = partial(_u0, _r0, 120)[-1]
    chk(abs(float(_p - Sinf(_u0, _r0))) < 1e-9,
        f"120 項の和が S∞ に近い: u1={_u0}, r={_r0}")
    eq(Sn(_u0, _r0, 3), partial(_u0, _r0, 3)[-1],
       f"S_3 と 1 項ずつが一致: u1={_u0}, r={_r0}")
# 絶対値
eq(abs(sp.Integer(3)), 3, "|3| = 3")
eq(abs(sp.Integer(-3)), 3, "|-3| = 3")
eq(abs(R(-1, 2)), R(1, 2), "|-1/2| = 1/2")
chk(abs(R(-3)) > 1, "r=-3 は |r|<1 をみたさない")
chk(R(-3) < 1, "しかし r<1 はみたす")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
_half = partial(R(1, 2), R(1, 2), 4)
chk(_half == [R(1, 2), R(3, 4), R(7, 8), R(15, 16)], f"部分和の表: {_half}")
for _v in _half:
    chk(_v < 1, "どれも 1 を超えない")
eq(Sinf(R(1, 2), R(1, 2)), 1, "S∞ = 1")
# 第 4 節の発散する 3 つ
chk(partial(3, 2, 4) == [3, 9, 21, 45], "r=2 の部分和は増える")
chk(partial(3, 1, 4) == [3, 6, 9, 12], "r=1 の部分和も増える")
chk(partial(3, -1, 4) == [3, 0, 3, 0], "r=-1 の部分和は行き来する")
# 第 5 節の表
for _n0, _v in [(1, "0.5"), (2, "0.25"), (3, "0.125")]:
    eq(R(1, 2) ** _n0, R(_v), f"(1/2)^{_n0} = {_v}")
chk(abs(float(R(1, 2) ** 10) - 0.000976562) < 1e-8, "(1/2)^10 = 0.000976…")
# 第 6 節
eq(Sinf(10, R(3, 4)), 40, "u1=10, r=3/4 で 40")
eq(18 * (1 - R(2, 3)), 6, "S∞=18, r=2/3 で u1=6")
# 第 7 節
eq(Sinf(R(4, 10), R(1, 10)), R(4, 9), "0.4… = 4/9")
chk(abs(float(R(4, 9)) - 0.444444) < 1e-5, "4/9 = 0.4444…")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
_alt = partial(8, R(-1, 2), 6)
chk([float(v) for v in _alt] == [8.0, 4.0, 6.0, 5.0, 5.5, 5.25],
    f"r=-1/2 の部分和: {[float(v) for v in _alt]}")
eq(Sinf(8, R(-1, 2)), R(16, 3), "S∞ = 16/3")
chk(abs(float(R(16, 3)) - 5.333333) < 1e-5, "16/3 = 5.333…")
chk(min(_alt) < R(16, 3) < max(_alt), "部分和は S∞ をはさむ")

# ══════════════════════════════════════════════════════════
# 3. 例題 1
# ══════════════════════════════════════════════════════════
eq(Sinf(15, R(1, 3)), R(45, 2), "例題1(a) 45/2")
eq(1 - R(1, 3), R(2, 3), "分母は 2/3")
eq(Sinf(8, R(-1, 2)), R(16, 3), "例題1(b) 16/3")
eq(1 - R(-1, 2), R(3, 2), "分母は 3/2")
eq(R(6, 24), R(1, 4), "例題1(c) r = 1/4")
eq(R(3, 2) / 6, R(1, 4), "3 項目でも r = 1/4")
eq(Sinf(24, R(1, 4)), 32, "例題1(c) 32")
eq(24 + 6 + R(3, 2), R(63, 2), "3 項の和は 31.5")
chk(R(63, 2) < 32, "S∞ より小さい")
eq(R(63, 2) + R(3, 8), R(255, 8), "4 項でも 31.875")
chk(R(255, 8) < 32, "まだ超えない")
eq(R(10, 5), 2, "例題1(d) r = 2")
chk(abs(sp.Integer(2)) >= 1, "|r| >= 1 なので和はない")
eq(R(24, 6), 4, "r を逆にとった誤答は 4")
chk(abs(sp.Integer(4)) > 1, "その誤答なら「和はない」になってしまう")

# ══════════════════════════════════════════════════════════
# 4. 例題 2
# ══════════════════════════════════════════════════════════
chk(sp.solve(sp.Eq(10 / (1 - x), 40), x) == [R(3, 4)], "例題2(a) r = 3/4")
eq(R(10, 40), R(1, 4), "1 - r = 1/4")
eq(Sinf(10, R(3, 4)), 40, "戻すと 40")
eq(18 * (1 - R(2, 3)), 6, "例題2(b) u1 = 6")
eq(Sinf(6, R(2, 3)), 18, "戻すと 18")
eq(R(6) / R(1, 2), 12, "例題2(c) u1 = 12")
eq(Sinf(12, R(1, 2)), 24, "例題2(c) 24")
_p2 = partial(12, R(1, 2), 5)
chk([float(v) for v in _p2] == [12.0, 18.0, 21.0, 22.5, 23.25],
    f"1 項ずつ足すと: {[float(v) for v in _p2]}")
eq(Sinf(6, R(1, 2)), 12, "u2 を u1 と取りちがえた誤答は 12")
chk(12 + 6 + 3 > 12, "書き出した和がすぐ 12 を超える")

# ══════════════════════════════════════════════════════════
# 5. 例題 3（循環小数）
# ══════════════════════════════════════════════════════════
eq(Sinf(R(4, 10), R(1, 10)), R(4, 9), "例題3(a) 4/9")
eq(Sinf(R(12, 100), R(1, 100)), R(4, 33), "例題3(b) 4/33")
eq(R(12, 99), R(4, 33), "12/99 = 4/33")
eq(Sinf(R(9, 10), R(1, 10)), 1, "例題3(c) 1")
chk(abs(float(R(4, 33)) - 0.121212) < 1e-5, "4/33 = 0.1212…")
eq(Sinf(R(12, 100), R(1, 10)), R(2, 15), "r を 1/10 とした誤答は 2/15")
chk(abs(float(R(2, 15)) - 0.133333) < 1e-5, "2/15 = 0.1333…")
ne(R(2, 15), R(4, 33), "その誤答は合わない")

# ══════════════════════════════════════════════════════════
# 6. 例題 4
# ══════════════════════════════════════════════════════════
eq(Sinf(1, R(2, 5)), R(5, 3), "例題4(c) 5/3")
_p4 = partial(1, R(2, 5), 4)
chk([float(v) for v in _p4] == [1.0, 1.4, 1.56, 1.624],
    f"1 項ずつ足すと: {[float(v) for v in _p4]}")
chk(abs(float(R(5, 3)) - 1.666666) < 1e-5, "5/3 = 1.6666…")
chk(partial(1, -1, 4) == [1, 0, 1, 0], "x=-1 の部分和は 1 と 0 を行き来")
eq(sp.Rational(1) / (1 - R(-1)), R(1, 2), "x=-1 を入れると 1/2 が出てしまう")
eq(1 / (1 + R(2, 5)), R(5, 7), "1/(1+x) とした誤答は 5/7")
chk(R(5, 7) < 1, "1 項目の 1 より小さくなってしまう")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(Sinf(20, R(2, 5)), R(100, 3), "演習1 100/3")
eq(1 - R(2, 5), R(3, 5), "分母は 3/5")
_e1 = partial(20, R(2, 5), 4)
chk([float(v) for v in _e1] == [20.0, 28.0, 31.2, 32.48], f"部分和: {_e1}")
chk(abs(float(R(100, 3)) - 33.33333) < 1e-4, "100/3 = 33.33…")
eq(R(20) / R(2, 5), 50, "分母を r とした誤答は 50")
ne(50, R(100, 3), "その誤答は合わない")

eq(R(6, 18), R(1, 3), "演習2 r = 1/3")
eq(R(2, 6), R(1, 3), "3 項目でも 1/3")
eq(Sinf(18, R(1, 3)), 27, "演習2 27")
eq(18 + 6 + 2, 26, "3 項の和は 26")
chk(26 < 27, "S∞ より小さい")
eq(26 + R(2, 3), R(80, 3), "4 項でも 26.666…")
chk(R(80, 3) < 27, "まだ超えない")

eq(Sinf(5, R(-3, 4)), R(20, 7), "演習3 20/7")
eq(1 - R(-3, 4), R(7, 4), "分母は 7/4")
_e3 = partial(5, R(-3, 4), 3)
chk([float(v) for v in _e3] == [5.0, 1.25, 4.0625], f"部分和: {_e3}")
chk(abs(float(R(20, 7)) - 2.857142) < 1e-5, "20/7 = 2.857…")
eq(R(5) / R(1, 4), 20, "分母を 1/4 とした誤答は 20")
chk(20 > 5, "1 項目より大きくなりすぎる")

chk(sp.solve(sp.Eq(12 / (1 - x), 30), x) == [R(3, 5)], "演習4 r = 3/5")
eq(R(12, 30), R(2, 5), "1 - r = 2/5")
eq(Sinf(12, R(3, 5)), 30, "戻すと 30")
chk(abs(R(3, 5)) < 1, "|r| < 1 をみたす")

eq(45 * (1 - R(1, 3)), 30, "演習5 u1 = 30")
eq(Sinf(30, R(1, 3)), 45, "戻すと 45")
chk(30 < 45, "u1 は S∞ より小さい")
eq(R(45) / R(2, 3), R(135, 2), "掛けるところを割った誤答")
chk(R(135, 2) > 45, "その誤答は見当と合わない")

eq(R(2, 4), R(1, 2), "演習6 r = 1/2")
eq(R(4) / R(1, 2), 8, "u1 = 8")
eq(Sinf(8, R(1, 2)), 16, "演習6 16")
_e6 = partial(8, R(1, 2), 5)
chk([float(v) for v in _e6] == [8.0, 12.0, 14.0, 15.0, 15.5], f"部分和: {_e6}")
eq(Sinf(4, R(1, 2)), 8, "u1 を 4 のままにした誤答は 8")
eq(8 + 4 + 2, 14, "しかし 3 項で 14")
chk(14 > 8, "すでに超えている")

eq(Sinf(R(5, 10), R(1, 10)), R(5, 9), "演習7(a) 5/9")
chk(abs(float(R(5, 9)) - 0.555555) < 1e-5, "5/9 = 0.5555…")
eq(Sinf(R(18, 100), R(1, 100)), R(2, 11), "演習7(b) 2/11")
eq(R(18, 99), R(2, 11), "18/99 = 2/11")
chk(abs(float(R(2, 11)) - 0.181818) < 1e-5, "2/11 = 0.1818…")
eq(Sinf(R(18, 100), R(1, 10)), R(1, 5), "r を 1/10 とした誤答は 1/5")
ne(R(1, 5), R(2, 11), "その誤答は合わない")

eq(Sinf(8, R(3, 4)), 32, "演習8(b) 32")
eq(1 - R(3, 4), R(1, 4), "分母は 1/4")
_e8 = partial(8, R(3, 4), 4)
chk([float(v) for v in _e8] == [8.0, 14.0, 18.5, 21.875], f"部分和: {_e8}")
chk(partial(8, R(3, 4), 10)[-1] < 32, "10 項でも 32 に届かない")
chk(abs(R(-5)) > 1, "k=-5 は |k|<1 をみたさない")
chk(R(-5) < 1, "しかし k<1 はみたす")

eq(Sn(1, R(1, 2), 1), 1, "演習9 S_1 = 1")
eq(Sn(1, R(1, 2), 2), R(3, 2), "S_2 = 1.5")
eq(Sn(1, R(1, 2), 3), R(7, 4), "S_3 = 1.75")
eq(Sinf(1, R(1, 2)), 2, "S∞ = 2")
for _k in [1, 2, 3, 4]:
    eq(Sn(1, 2, _k), 2 ** _k - 1, f"r=2 なら S_{_k} = 2^{_k} - 1")
chk([Sn(1, 2, _k) for _k in [1, 2, 3, 4]] == [1, 3, 7, 15], "1,3,7,15")

eq(R(12, 4), 3, "演習10 r = 3")
eq(Sinf(4, 3), -2, "公式に入れると -2 が出る")
chk(Sinf(4, 3) < 0, "しかし答えが負")
_e10 = partial(4, 3, 4)
chk(_e10 == [4, 16, 52, 160], f"部分和は増え続ける: {_e10}")
for _v in _e10:
    chk(_v > 0, "項も部分和もすべて正")
chk(abs(sp.Integer(3)) > 1, "|r| > 1 なので公式は使えない")

# ══════════════════════════════════════════════════════════
# 8. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.8** の欄に `The sum of an infinite geometric sequence`"
        " として印刷", "公式集にある")
in_text("> $S_{\\infty} = \\dfrac{u_{1}}{1-r}$, $\\left|r\\right| < 1$",
        "公式集の条件を逐語で")
in_text("S_{n} = \\frac{u_{1}(r^{n} - 1)}{r - 1}"
        " = \\frac{u_{1}(1 - r^{n})}{1 - r}, \\qquad r \\neq 1",
        "有限和の式（公式集の 2 つの形と r ≠ 1）")
in_text("**modulus**（絶対値）", "modulus notation")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**これは確かめであって、答案ではありません。**", "電卓は答案にならない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aasl18-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
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
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl18", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-8-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-1-8-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("Filling a bar of length $1$", "図(a) の題")
in_fig("the pieces never overflow", "図(a) の要点")
in_fig("each new piece is half of what is left", "図(a) の説明")
in_fig("The terms of $r^{\\\\,n}$", "図(b) の題")
in_fig("dies away to $0$", "図(b) の |r|<1")
in_fig("off the top", "図(b) の |r|>1")
in_text("(a) Each new piece is half of what is left", "キャプションが (a) を説明")
in_text("(b) When the ratio is less than 1 in size", "キャプションが (b) を説明")
# 図の値が本文と合っているか
_edges, _x = [0], R(0)
for _k in range(1, 8):
    _x += R(1, 2) ** _k
    _edges.append(_x)
for _v in _edges:
    chk(_v < 1, "棒からはみ出さない")
eq(_edges[3], R(7, 8), "3 つめの区切りは 7/8")
for _k in range(6):
    eq(R(1, 2) ** _k, sp.Rational(1, 2 ** _k), f"(0.5)^{_k}")
    eq(sp.Integer(2) ** _k, 2 ** _k, f"2^{_k}")
chk(2 ** 3 > 4, "r=2 は 3 段目で上端を超える")
for leak in ["100", "= 27", "= 30", "20}{7", "5}{9", "2}{11", "= 32", "= 16"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-8.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-1-7b.qmd") < DRAFT.index("aasl-1-8.qmd"), "並びが 1.7b → 1.8")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aasl-1-8.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| convergent |", "| divergent |", "| sum to infinity |",
          "| modulus |"]:
    chk(t in GLO, "対訳表にある: " + t)


# ══════════════════════════════════════════════════════════
# 13. レビュー反映の見張り
# ══════════════════════════════════════════════════════════
in_text("**「項が小さくなること」だけでは足りません。**", "項が減るだけでは収束しない")
in_text("## 「近づく」を、ここでは証明していません", "極限の議論は SL 外")
in_text("$r \\neq 1$ という条件も、公式集に書かれています。", "1.3 の条件")
in_text("$r = 1$ のときは、そもそも @eq-aasl18-sn が使えません（分母が $0$）。",
        "r=1 では有限和の式も使えない")
# 第 6 節・第 7 節を、例題と別の数にした
in_text("$S_{\\infty} = 24$、$u_{1} = 16$ なら", "第 6 節の r の例")
chk(sp.solve(sp.Eq(16 / (1 - x), 24), x) == [R(1, 3)], "16/(1-r)=24 なら r=1/3")
eq(R(16, 24), R(2, 3), "1 - r = 2/3")
in_text("$S_{\\infty} = 21$、$r = \\dfrac{3}{7}$ なら", "第 6 節の u1 の例")
eq(21 * (1 - R(3, 7)), 12, "21 × 4/7 = 12")
eq(Sinf(12, R(3, 7)), 21, "戻すと 21")
not_in_text("**$r$ を求める。** $S_{\\infty} = 40$", "例題 2 と重ならない")
in_text("$0.\\overline{7} = 0.7777\\ldots$ は、**無限等比級数の和として書けます。**",
        "第 7 節の例を差しかえた")
eq(Sinf(R(7, 10), R(1, 10)), R(7, 9), "0.7… = 7/9")
chk(abs(float(R(7, 9)) - 0.777777) < 1e-5, "7/9 = 0.7777…")
not_in_text("**$0.\\overline{4} = \\dfrac{4}{9}$ です。**", "例題 3(a) と重ならない")
# Why it works の例を差しかえた
in_text("$r = -\\dfrac{1}{3}$、$u_{1} = 9$ で確かめてみます。", "Why it works の例")
_alt3 = partial(9, R(-1, 3), 5)
chk(_alt3 == [9, 6, 7, R(20, 3), R(61, 9)], f"部分和: {_alt3}")
eq(Sinf(9, R(-1, 3)), R(27, 4), "S∞ = 27/4")
eq(R(27, 4), sp.Rational("6.75"), "27/4 = 6.75")
chk(6 < R(27, 4) < 7, "6 と 7 のあいだ")
chk(R(20, 3) < R(27, 4) < R(61, 9), "20/3 と 61/9 のあいだ")
in_text("**$r$ が負のとき、$S_{\\infty}$ は連続する $2$ つの部分和のあいだにあります。**",
        "はさみうちを明示")
not_in_text("$r = -\\dfrac{1}{2}$、$u_{1} = 8$ で確かめてみます。", "例題 1(b) と重ならない")
# 「残りをまとめて足す」検算（S∞ = S_n + 次の項/(1-r)）
def tail(u1, r, k):
    """k 項で切ったときの、残りの和。"""
    return Sinf(_S(u1) * _S(r) ** k, r)
for _u0, _r0, _k in [(24, R(1, 4), 3), (20, R(2, 5), 4), (18, R(1, 3), 3),
                     (8, R(3, 4), 4)]:
    eq(partial(_u0, _r0, _k)[-1] + tail(_u0, _r0, _k), Sinf(_u0, _r0),
       f"部分和 + 残り = S∞: u1={_u0}, r={_r0}, k={_k}")
eq(tail(24, R(1, 4), 3), R(1, 2), "例題1(c) の残りは 1/2")
eq(R(63, 2) + R(1, 2), 32, "31.5 + 0.5 = 32")
eq(tail(20, R(2, 5), 4), R(64, 75), "演習1 の残りは 64/75")
eq(R(812, 25), R(2436, 75), "32.48 = 2436/75")
eq(R(2436, 75) + R(64, 75), R(100, 3), "合わせて 100/3")
eq(tail(18, R(1, 3), 3), 1, "演習2 の残りは 1")
eq(tail(8, R(3, 4), 4), R(81, 8), "演習8 の残りは 81/8")
eq(8 + 6 + R(9, 2) + R(27, 8), R(175, 8), "4 項の和は 175/8")
eq(R(175, 8) + R(81, 8), 32, "合わせて 32")
eq(8 * R(3, 4) ** 4, R(81, 32), "5 項目は 81/32")
in_text("**途中で切って、残りを足し直す別の道すじです。**", "この検算の言い方")
chk(TEXT.count("残りをまとめて足します") >= 3, "3 か所以上で使っている")
# 部分和では見つからない誤りは、問題文と照合する
in_text("**この誤りは、部分和では見つかりません。**", "検算の限界を明記")
chk(TEXT.count("**この誤りは、部分和では見つかりません。**") == 2, "2 か所")
_wrong6 = partial(4, R(1, 2), 6)
chk(all(v < 8 for v in _wrong6), "誤答の部分和は 8 を超えない")
_wrong2c = partial(6, R(1, 2), 6)
chk(all(v < 12 for v in _wrong2c), "誤答の部分和は 12 を超えない")
eq(4 * R(1, 2), 2, "u1=4 なら u2=2")
ne(2, 4, "問題文の u2=4 と合わない")
# u1 < S∞ は r > 0 のときだけ
in_text("**$r$ が負のときは、この見当は使えません。**", "見当の条件")
chk(Sinf(5, R(-3, 4)) < 5, "r<0 では u1 > S∞ になりうる")
chk(Sinf(9, R(-1, 3)) < 9, "同上")
# |r| >= 1 は計算ミスとはかぎらない
in_text("**$|r| \\geq 1$ が出たら、まず計算を見直してください。**", "言い方を直した")
chk(sp.solve(sp.Eq(12 / (1 - x), 6), x) == [-1], "u1=12, S∞=6 なら r=-1")
# r = -1 の Common error
in_text("## 「項が大きくならないから収束する」と思い込む", "追加した Common error")
chk(TEXT.count("::: {.callout-warning}") >= 6, "Common errors が 6 つ以上")
# はさみうちで誤答を除く
in_text("$1.25 < S_{\\infty} < 4.0625$", "演習3 のはさみうち")
chk(not (R(5, 4) < 20 < sp.Rational("4.0625")), "誤答 20 ははさみうちの外")
chk(R(5, 4) < R(20, 7) < sp.Rational("4.0625"), "正答ははさみうちの中")
# 0.9… = 1
in_text("**$0.\\overline{9}$ は「$1$ に限りなく近い別の数」ではなく、$1$ そのものです。**",
        "0.9… の意味")
# 場合分け
in_text("**$r = -1$ だけは、ふるまいがちがいます。**", "r=-1 を別に書く")
in_text("alternate between $u_{1}$ and $0$", "行き来する 2 つの値を書く")
# 英語と見出し
in_text("[Identify the error in the student's work, and state the correct"
        " conclusion.]{.q-en}", "演習10 の英語")
in_text("*$r = 2$, so $|r| = 2 > 1$ and the condition $|r| < 1$ fails.",
        "例題1(d) の解答例")
chk("## 解答例（答案用紙にはこう書く）" not in TEXT, "解答例の見出しをそろえた")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
in_text("得点にならない可能性があります", "採点の断定を弱めた")
not_in_text("得点になりません", "断定は残っていない")
in_text("この条件の確認が採点対象になることがあります", "同上")
# GDC
in_text("本体に一般項（$0.\\overline{7}$ なら $7 \\times 10^{-n}$）を入れます。",
        "一般項を入れることを書く")
in_text("**$|r|$ が $1$ に近いほど、収束はゆっくり**です。", "収束の速さ")


# ── |r| > 1 の発散理由（★2026-09-07 の修正）──────────────
# r < -1 でも通る説明に直した
in_text("**$|r| > 1$ のとき**（以下、$u_{1} \\neq 0$ とします）。", "u1 ≠ 0 の但し書き")
not_in_text("大きな数を足し続けるのですから、和が $1$ つの値に落ち着くはずがありません。",
            "r < -1 に合わない言い方は消した")
in_text("項の大きさ $|u_{1}| \\, |r|^{\\,n-1}$ は毎回 $|r|$ 倍になる", "項の絶対値で述べる")
in_text("部分和に次の項を足したときの**変わり方**が $0$ に近づかない", "変化量で述べる")
in_text("- **$r > 1$** なら、同じ向きにどんどん大きくなります", "r > 1 の場合")
in_text("- **$r < -1$** なら、正と負を行き来しながら、**振れ幅が大きくなります。**",
        "r < -1 の場合")
in_text("$3 - 6 + 12 - 24 + \\cdots$ の部分和は", "r = -2 の例")
in_text("3, \\quad -3, \\quad 9, \\quad -15, \\quad 33", "その部分和")
# 実際に計算して確かめる
_neg = partial(3, -2, 5)
chk(_neg == [3, -3, 9, -15, 33], f"3-6+12-24+48 の部分和: {_neg}")
chk(abs(_neg[4]) > abs(_neg[2]) > abs(_neg[0]), "振れ幅が大きくなる")
chk(any(v > 0 for v in _neg) and any(v < 0 for v in _neg), "正負を行き来する")
for _k in range(1, 8):
    chk(abs(3 * sp.Integer(-2) ** _k) > abs(3 * sp.Integer(-2) ** (_k - 1)),
        f"項の絶対値が増える: k={_k}")
chk(sp.limit(abs(sp.Integer(-2)) ** sp.Symbol("m", positive=True),
             sp.Symbol("m", positive=True), sp.oo) is sp.oo, "|-2|^n → ∞")
# r = 1、r = -1 の説明は残っている
in_text("**$r = 1$ のとき。**", "r = 1 の場合は残す")
in_text("**$r = -1$ のとき。**", "r = -1 の場合も残す")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
