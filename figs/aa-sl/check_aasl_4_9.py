# -*- coding: utf-8 -*-
"""AA SL 4.9 のページを検算する。

    python3 figs/aa-sl/check_aasl_4_6a.py
"""
import glob
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability", "aasl-4-9.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_9.py")

TEXT = open(QMD, encoding="utf-8").read()
FIG = open(FIGP, encoding="utf-8").read()
FIGCODE = FIG.split('"""', 2)[-1]

OK = 0
NG = 0


def chk(cond, msg=""):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(a, b, msg=""):
    chk(sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0,
        "%s :: %s != %s" % (msg, a, b))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: %s :: %s" % (msg, sub[:60]))


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: %s :: %s" % (msg, sub[:60]))


def in_fig(sub, msg=""):
    chk(sub in FIG, "図に見つからない: %s :: %s" % (msg, sub[:60]))


BODY = TEXT.split("## Worked examples")[0]


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "本文（例題より前）に残っている: %s :: %s" % (msg, sub[:60]))


DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]


def prob(space, pred):
    return F(sum(1 for s in space if pred(s)), len(space))


from statistics import NormalDist as ND

BIG = 10 ** 9


def ncdf(a, b, mu, sd):
    _d = ND(mu, sd)
    return _d.cdf(b) - _d.cdf(a)


def inv(area, mu, sd):
    return ND(mu, sd).inv_cdf(area)


def near(v, target, tol=5e-4):
    return abs(v - target) < tol


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 4.9 — The normal distribution（正規分布） {#sec-aasl-4-9}", "見出し")

for _h in ("## What you should be able to do", "## The idea", "## Why it works",
           "## Worked examples", "## Common errors",
           "## Using your GDC (TI-Nspire CX II)", "## Exercises"):
    in_text(_h, "節 " + _h)

_secs = re.findall(r"^### (\d)\. .*\{#([a-z-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)] + ["1", "2", "3"],
    "### の番号 1..7 と GDC 1..3: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["curve", "properties", "empirical", "calc",
                              "tails", "inverse", "sketch",
                              "gdc-normcdf", "gdc-invnorm", "gdc-check"],
    "アンカー: %s" % [s[1] for s in _secs])
chk(TEXT.index("## Using your GDC (TI-Nspire CX II)") > TEXT.index("## Common errors"),
    "GDC の節は Common errors の後")
chk(TEXT.index("## Using your GDC (TI-Nspire CX II)") < TEXT.index("## Exercises"),
    "GDC の節は Exercises の前")

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper 2 の注 1）")
chk(TEXT.count("{.callout-important}") == 0,
    "callout-important 0（4.9 は公式集に欄がない）")
chk(TEXT.count("**検算") >= 12, "検算 12 以上: %d" % TEXT.count("**検算"))

_d = 0
for _l in TEXT.split("\n"):
    _t = _l.strip()
    if _t.startswith(":::"):
        _d += -1 if _t[3:].strip() == "" else 1
chk(_d == 0, "::: の開閉が合う: %d" % _d)

_verbs = re.compile(r"Explain|Justify|Comment|Interpret|Identify|Describe|Suggest")
_qs = [q for q in re.findall(r"\[([^\[\]]*?)\]\{\.q-en\}", TEXT, re.S)
       if _verbs.search(q)]
chk(TEXT.count("{.model-answer}") == len(_qs),
    "model-answer %d = 問い %d" % (TEXT.count("{.model-answer}"), len(_qs)))
chk(len(_qs) == 8, "Explain 系の問いは 8: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-4-9-idea.svg){#fig-aasl49-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl49-idea (a)", "図 (a) の参照")
in_text("@fig-aasl49-idea (b)", "図 (b) の参照")

_quotes = re.findall(r"^> (.+)$", TEXT, re.M)
chk(_quotes == ["For inverse normal calculations mean and standard deviation "
                "will be given."],
    "引用は inverse normal の 1 行だけ: %s" % _quotes)
for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# 4.9 では z を使わない（4.12 の内容）
chk("$z$" not in TEXT.split("## Why it works")[1].split("## Worked examples")[0]
    or "[SL 4.12]" in TEXT, "z に触れるときは 4.12 に送る")
not_in_text("z = \\frac{x - \\mu}", "z の式は 4.12 で扱う")
not_in_text("標準化", "標準化は 4.12 で扱う")

# ══════════════════════════════════════════════════════════
# 2. 記法と性質
# ══════════════════════════════════════════════════════════
in_text("X \\sim N(\\mu,\\ \\sigma^{2})\n$$ {#eq-aasl49-not}", "N(μ, σ²)")
in_text("{#tbl-aasl49-prop}", "性質の表")
in_text("{#tbl-aasl49-emp}", "68-95-99.7 の表")
in_text("{#tbl-aasl49-gdc}", "normCdf の表")
in_text("{#tbl-aasl49-inv}", "invNorm の表")
in_text("**$P(X = a) = 0$ です。**", "1 点の確率は 0")
in_text("$N(90,\\ 49)$ なら $\\sigma^{2} = 49$、つまり $\\sigma = 7$ です。",
        "分散と標準偏差の例")
eq(sp.sqrt(49), 7, "√49 = 7")
# ★ 本文の例が、例題・演習の分布と重ならないこと
_page_pairs = [(50, 8), (170, 6), (500, 40), (72, 5), (20, 3), (100, 15),
               (250, 12), (65, 8), (500, 25), (30, 4), (12, sp.Rational("2.5")),
               (sp.Rational("4.2"), sp.Rational("0.6"))]
chk((90, 7) not in _page_pairs, "本文の例 N(90, 49) は例題・演習と重ならない")

# 68-95-99.7 が実際に成り立つこと
chk(near(ncdf(-1, 1, 0, 1), 0.6827, 5e-4), "μ±σ は約 68%")
chk(near(ncdf(-2, 2, 0, 1), 0.9545, 5e-4), "μ±2σ は約 95%")
chk(near(ncdf(-3, 3, 0, 1), 0.9973, 5e-4), "μ±3σ は約 99.7%")
chk(near(ncdf(0, BIG, 0, 1), 0.5, 1e-9), "μ より上は 0.5")
chk(near(ncdf(2, BIG, 0, 1), 0.02275, 5e-5), "μ+2σ より上は約 2.5%")
chk(near(ncdf(1, BIG, 0, 1), 0.15866, 5e-5), "μ+σ より上は約 16%")
eq((100 - 95) / sp.Integer(2), sp.Rational("2.5"), "(100-95)/2 = 2.5")

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig("K = 0.8416212335729144", "図 (b) の k")
chk(near(ncdf(-BIG, 0.8416212335729144, 0, 1), 0.8, 1e-9),
    "図 (b) の面積は 0.8")
in_fig("about $68", "図 (a) の 68%")
in_fig("about $95", "図 (a) の 95%")
in_fig("area $= 0.8$", "図 (b) の面積のラベル")
# 図に例題・演習の答えは出さない
for _v in ("0.894", "0.734", "0.628", "0.0478", "0.683", "551", "566",
           "0.0548", "0.0808", "0.954"):
    chk(_v not in FIGCODE, "図に答え %s は出さない" % _v)

# ══════════════════════════════════════════════════════════
# 4. 例題1  N(50, 8^2)
# ══════════════════════════════════════════════════════════
chk(near(ncdf(-BIG, 60, 50, 8), 0.8944), "例題1(a) 0.894")
chk(near(ncdf(45, BIG, 50, 8), 0.7340), "例題1(b) 0.734")
chk(near(ncdf(45, 60, 50, 8), 0.6284), "例題1(c) 0.628")
chk(near(ncdf(-BIG, 45, 50, 8), 0.2660), "P(X<45) = 0.266")
chk(near(0.8944 - 0.2660, 0.6284, 1e-9), "0.8944 - 0.2660 = 0.6284")
chk(near(1 - 0.7340, 0.2660, 1e-9), "1 - 0.734 = 0.266")
chk(ncdf(-BIG, 60, 50, 8) > 0.5, "60 は μ より上")
chk(ncdf(45, BIG, 50, 8) > 0.5, "45 は μ より下")
eq(sp.Rational(60 - 50, 8), sp.Rational("1.25"), "60 は μ+1.25σ")
in_text("P(X < 60) = 0.894", "例題1(a)")
in_text("P(X > 45) = 0.734", "例題1(b)")
in_text("P(45 < X < 60) = 0.628", "例題1(c)")

# ══════════════════════════════════════════════════════════
# 5. 例題2  N(170, 6^2)
# ══════════════════════════════════════════════════════════
chk(near(ncdf(180, BIG, 170, 6), 0.04779, 5e-5), "例題2(a) 0.0478")
chk(near(ncdf(164, 176, 170, 6), 0.68269, 5e-5), "例題2(b) 0.683")
chk(near(ncdf(-BIG, 180, 170, 6), 0.9522), "余事象 0.9522")
chk(near(1 - 0.9522, 0.0478, 1e-9), "1 - 0.9522 = 0.0478")
eq(170 - 6, 164, "μ-σ = 164")
eq(170 + 6, 176, "μ+σ = 176")
chk(abs((180 - 170) / 6 - 1.667) < 5e-3, "180 は μ+1.67σ")
chk(0.0250 < ncdf(180, BIG, 170, 6) < 0.1587, "2.5% と 16% の間")

# ══════════════════════════════════════════════════════════
# 6. 例題3  N(500, 40^2)
# ══════════════════════════════════════════════════════════
chk(near(inv(0.9, 500, 40), 551.262, 5e-3), "例題3(a) k = 551")
chk(near(inv(0.95, 500, 40), 565.794, 5e-3), "例題3(b) 566")
chk(near(ncdf(460, 560, 500, 40), 0.77454, 5e-5), "例題3(c) 0.775")
chk(near(ncdf(-BIG, 551.26, 500, 40), 0.9000, 5e-5), "もどすと 0.900")
chk(inv(0.95, 500, 40) > inv(0.9, 500, 40), "上位 5% の境目は上位 10% より右")
eq(1 - sp.Rational("0.05"), sp.Rational("0.95"), "1 - 0.05 = 0.95")
eq(500 - 40, 460, "μ-σ = 460")
eq(500 + 40, 540, "μ+σ = 540")
chk(540 < inv(0.9, 500, 40) < 580, "551 は 540 と 580 の間")
chk(inv(0.9, 500, 40) > 500, "面積 0.9 なら k > μ")

# ══════════════════════════════════════════════════════════
# 7. 例題4  N(72, 5^2)
# ══════════════════════════════════════════════════════════
chk(near(ncdf(80, BIG, 72, 5), 0.05480, 5e-5), "例題4(a) 0.0548")
chk(near(ncdf(-BIG, 65, 72, 5), 0.08076, 5e-5), "例題4(b) 0.0808")
chk(near(ncdf(62, 82, 72, 5), 0.95450, 5e-5), "例題4(c) 0.954")
eq(72 - 2 * 5, 62, "μ-2σ = 62")
eq(72 + 2 * 5, 82, "μ+2σ = 82")
eq(sp.Rational(80 - 72, 5), sp.Rational("1.6"), "80 は μ+1.6σ")
eq(sp.Rational(72, 5), sp.Rational("14.4"), "0 は μ から 14.4σ")
chk(ncdf(-BIG, 0, 72, 5) < 1e-40, "負になる確率はきわめて小さい")
chk(0.0250 < ncdf(80, BIG, 72, 5) < 0.1587, "0.0548 は 2.5% と 16% の間")

# ══════════════════════════════════════════════════════════
# 8. 演習の答え
# ══════════════════════════════════════════════════════════
chk(near(ncdf(-BIG, 24, 20, 3), 0.90879), "演習1 P(X<24) = 0.909")
chk(near(ncdf(17, BIG, 20, 3), 0.84134), "演習1 P(X>17) = 0.841")
eq(20 - 3, 17, "17 = μ-σ")
chk(near(ncdf(-1, BIG, 0, 1), 0.84134), "μ-σ より上は約 84%")
chk(abs((24 - 20) / 3 - 1.333) < 5e-3, "24 は μ+1.33σ")

chk(near(ncdf(130, BIG, 100, 15), 0.02275, 5e-5), "演習2 0.0228")
chk(near(ncdf(-BIG, 70, 100, 15), 0.02275, 5e-5), "演習2 対称の側も 0.0228")
chk(near(ncdf(-BIG, 130, 100, 15), 0.97725, 5e-5), "余事象 0.9772")
chk(near(1 - 0.9772, 0.0228, 1e-9), "1 - 0.9772 = 0.0228")
eq(100 + 2 * 15, 130, "130 = μ+2σ")

chk(near(inv(0.25, 250, 12), 241.906, 5e-3), "演習3 Q1 = 242")
chk(near(inv(0.75, 250, 12), 258.094, 5e-3), "演習3 Q3 = 258")
chk(near(250 - 241.9, 8.1, 1e-9) and near(258.1 - 250, 8.1, 1e-9),
    "μ からの距離が等しい")
chk(near(ncdf(241.9, 258.1, 250, 12), 0.5003, 1e-3), "四分位数の間は 0.500")
chk(inv(0.25, 250, 12) < 250 < inv(0.75, 250, 12), "Q1 < μ < Q3")

chk(near(ncdf(5, BIG, sp.Rational("4.2"), sp.Rational("0.6")), 0.09121, 5e-5)
    if False else near(ncdf(5, BIG, 4.2, 0.6), 0.09121, 5e-5), "演習4 0.0912")
chk(near(ncdf(-BIG, 5, 4.2, 0.6), 0.90879), "余事象 0.9088")
chk(near(1 - 0.9088, 0.0912, 1e-9), "1 - 0.9088 = 0.0912")
chk(abs((5 - 4.2) / 0.6 - 1.333) < 5e-3, "5 は μ+1.33σ")
eq(sp.Rational("0.6") ** 2, sp.Rational("0.36"), "分散は 0.36（入れてはいけない）")

chk(near(inv(0.1, 65, 8), 54.7476, 5e-3), "演習5 k = 54.7")
chk(near(ncdf(-BIG, 54.75, 65, 8), 0.1000, 1e-3), "もどすと 0.100")
chk(inv(0.1, 65, 8) < 65, "面積 0.1 なら k < μ")
eq(65 - 8, 57, "μ-σ = 57")
eq(65 - 2 * 8, 49, "μ-2σ = 49")
chk(49 < inv(0.1, 65, 8) < 57, "54.7 は 49 と 57 の間")

chk(near(ncdf(480, 530, 500, 25), 0.67307, 5e-5), "演習6 0.673")
chk(near(ncdf(480, 500, 500, 25), 0.2881), "左半分 0.2881")
chk(near(ncdf(500, 530, 500, 25), 0.3849), "右半分 0.3849")
chk(near(0.2881 + 0.3849, 0.6730, 1e-9), "0.2881 + 0.3849 = 0.673")
chk(ncdf(500, 530, 500, 25) > ncdf(480, 500, 500, 25), "右のほうが長い")
eq(500 - 480, 20, "左は 20")
eq(530 - 500, 30, "右は 30")

chk(near(inv(0.95, 30, 4), 36.5794, 5e-3), "演習7 k = 36.6")
chk(near(ncdf(-BIG, 36.58, 30, 4), 0.9500, 1e-3), "もどすと 0.950")
chk(near(inv(0.05, 30, 4), 23.4206, 5e-3), "0.05 を入れると 23.4")
eq(30 + 4, 34, "μ+σ = 34")
eq(30 + 2 * 4, 38, "μ+2σ = 38")
chk(34 < inv(0.95, 30, 4) < 38, "36.6 は 34 と 38 の間")

chk(near(ncdf(-BIG, 10, 12, 2.5), 0.21186, 5e-5), "演習8 0.212")
chk(near(ncdf(14, BIG, 12, 2.5), 0.21186, 5e-5), "対称の側も 0.212")
chk(near(200 * 0.212, 42.4, 1e-9), "200 × 0.212 = 42.4")
chk(abs((12 - 10) / 2.5 - 0.8) < 1e-9, "10 は μ-0.8σ")
chk(ncdf(-BIG, 10, 12, 2.5) > 0.15866, "0.212 は 16% より大きい")
eq(12 + 2, 14, "対称の点は 14")

chk(near(ncdf(10, 10, 12, 2.5), 0.0, 1e-12), "下端と上端が同じなら 0")

chk(near(ncdf(50, BIG, 30, 4), 2.8665e-7, 1e-10), "演習10 約 2.87e-7")
eq(sp.Rational(50 - 30, 4), 5, "50 は μ+5σ")
chk(ncdf(50, BIG, 30, 4) > 0, "0 ではない")
chk(ncdf(50, BIG, 30, 4) < ncdf(3, BIG, 0, 1), "5σ の外は 3σ の外より小さい")
# ══════════════════════════════════════════════════════════
# 10. ページに書いてある計算を、機械的に全部たしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|\\times|[\d.]))"
                   % (_EXPR, _EXPR))


def _tonum(t):
    t = t.strip()
    m = re.fullmatch(r"\\[dt]?frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2)))
    return sp.Rational(t)


def _value(expr):
    """+ - かけ算だけの式を、かけ算を先に計算して評価する。"""
    total = sp.Integer(0)
    sign = 1
    for _tk in re.finditer(r"([+-])|(%s)" % _TERM, expr):
        if _tk.group(1):
            sign = 1 if _tk.group(1) == "+" else -1
        else:
            prod = sp.Integer(1)
            for _f in re.finditer(_ATOM, _tk.group(2)):
                prod *= _tonum(_f.group(0))
            total += sign * prod
    return total


_nstmt = 0
for _m in _STMT.finditer(TEXT):
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 8, "ページの計算を %d 本たしかめた" % _nstmt)

# 確率の値は、すべて 0 以上 1 以下
_nprob = 0
for _m in re.finditer(r"P\([^)]*\)\s*=\s*(%s)" % _ATOM, TEXT):
    _nprob += 1
    _v = _tonum(_m.group(1))
    chk(0 <= _v <= 1, "確率が 0..1 の外: %s" % _m.group(0)[:60])
chk(_nprob >= 3, "確率の値を %d 個たしかめた" % _nprob)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- B1・M1 「すべての実数に正の確率」は誤り ---------------------------
in_text("A normal distribution gives positive probability to every interval",
        "B1 区間で言う")
not_in_text("gives a positive probability to every real value", "誤りは消した")
in_text("正規分布はどんな区間にも正の確率を与えるので、「$P(X > 50) = 0$」とは"
        "言えません。", "M1 演習10")
not_in_text("正規分布はすべての実数に正の確率を与える", "誤りは消した（演習10）")
# 1 点の確率は 0、区間の確率は正
chk(near(ncdf(50, 50, 30, 4), 0.0, 1e-15), "1 点の確率は 0")
chk(ncdf(50, BIG, 30, 4) > 0, "区間の確率は正")
chk(near(72 / 5, 14.4, 1e-9), "0 は μ から 14.4σ")
in_text("zero lies $14.4$ standard deviations below the mean", "B1 14.4σ")

# --- M2 逆正規の説明 ---------------------------------------------------
in_text("**なぜ、逆正規計算では面積を「左から」で数えるのでしょうか。**", "M2")
in_text("面積 $1$ つに対して $k$ が $1$ つだけ決まります。", "M2 一意性")
not_in_text("`normCdf` が返すのが「下端から上端までの面積」で、`invNorm` は"
            "その逆をたどるからです。", "説明になっていない文は消した")
# P(X<k) は k について単調増加
for _k in (-2, -1, 0, 1, 2):
    chk(ncdf(-BIG, _k + 0.5, 0, 1) > ncdf(-BIG, _k, 0, 1),
        "P(X<k) は k について増える: k=%s" % _k)

# --- M3 例題3(d)・演習5 の答えの先出しを消した ------------------------
not_in_text("左半分だけで面積は $0.5$ なので、それをこえるには $\\mu$ を通りすぎる",
            "答案そのものは本文から消した")
chk("面積が $0.5$ より大きければ $k > \\mu$、小さければ $k < \\mu$ です。"
    not in TEXT.split("## Worked examples")[0],
    "§6 の先出しは消した（GDC の節に検査として残すのは可）")
not_in_text("a value with more than half the area to its left must lie above "
            "the mean", "キャプションの先出しは消した")
chk("$k$ is above $\\mu$ because the area exceeds" not in FIG,
    "図の説明から理由は消した")
in_text("**この向きは、図をかけば目で確かめられます。**", "M3 言いかえ")

# --- m5 図の面積を 0.8 にした -----------------------------------------
chk(near(inv(0.75, 250, 12), 258.094, 5e-3), "演習3 の Q3 は面積 0.75")
chk(near(ncdf(-BIG, 0.8416212335729144, 0, 1), 0.8, 1e-9), "図は面積 0.8")
in_fig("0.8 にしてある", "m5 図の但し書き")

# --- m1 §2 の言い方 ---------------------------------------------------
in_text("**「より小さい」と「以下」（同じく「より大きい」と「以上」）を区別する"
        "必要がありません。**", "m1")

# --- m6 例題3(c) を非対称な区間にした ----------------------------------
in_text("P(460 < X < 560) = 0.775", "m6 例題3(c)")
not_in_text("P(460 < X < 540) = 0.683", "例題2(b) と同じ問題は消した")
in_text("左は $1\\sigma$、右は $1.5\\sigma$ です。", "m6 検算")
eq(500 - 40, 460, "460 = μ-σ")
chk(near(500 + 1.5 * 40, 560, 1e-9), "560 = μ+1.5σ")
chk(0.68269 < ncdf(460, 560, 500, 40) < 0.9545,
    "0.775 は 68% と 95% の間")

# --- M6 例題3(b) に図をかかせた ---------------------------------------
in_text("Sketch the normal curve, shade the region whose area is $0.05$",
        "M6 演習の指示")
in_text("**図：$\\mu = 500$ に縦線を入れ、右のすその細い部分を塗ります。**",
        "M6 解答に図の説明")
in_text("*sketch: curve with the right-hand tail of area $0.05$ shaded",
        "M6 解答例に図")

# --- M5 演習2 を N(100, 225) にした -----------------------------------
in_text("$X \\sim N(100,\\ 225)$. Write down the value of $\\sigma$", "M5 演習2")
in_text("\\sigma = \\sqrt{225} = 15", "M5 演習2 の解答例")
in_text("**$225$ は分散です。** GDC に入れるのは $\\sqrt{225} = 15$ です",
        "M5 演習2 の解説")
eq(sp.sqrt(225), 15, "√225 = 15")
chk(near(ncdf(130, BIG, 100, 15), 0.02275, 5e-5), "演習2 の答えは変わらない")
# 分散を入れると答えが変わる
chk(not near(ncdf(130, BIG, 100, 225), 0.02275, 5e-3),
    "σ に 225 を入れると答えが変わる")

# --- M7 演習7 を右側の面積にした --------------------------------------
in_text("Find the value of $k$ such that $P(X > k) = 0.05$.", "M7 演習7")
in_text("右の面積が $0.05$ なので、左の面積は $1 - 0.05 = 0.95$ です。",
        "M7 演習7 の解説")
in_text("*area to the left* $= 1 - 0.05 = 0.95$", "M7 演習7 の解答例")
chk(near(inv(0.95, 30, 4), 36.5794, 5e-3), "演習7 の答えは変わらない")
chk(near(ncdf(inv(0.95, 30, 4), BIG, 30, 4), 0.05, 1e-9), "右の面積は 0.05")

# --- M4・M8 演習9 を「誤りを見つける」問いにした ----------------------
in_text("A student finds $P(X < 50) = 0.798$ and then writes", "M4 演習9")
in_text("Identify the error in the student's reasoning.", "M4 Identify")
in_text("`normCdf(50, 50, 40, 12)` は $0$ になります", "M8 実行できる検算")
not_in_text("`normCdf(10, 10, μ, σ)` は $0$ になります",
            "μ, σ が与えられていない検算は消した")
in_text("$X \\sim B(20,\\ 0.5)$ なら $P(X = 10) = 0.176$", "m10 離散の例に数を入れた")
chk(near(ncdf(-BIG, 50, 40, 12), 0.79767, 5e-5), "演習9 P(X<50) = 0.798")
chk(near(ncdf(50, 50, 40, 12), 0.0, 1e-15), "演習9 P(X=50) = 0")
chk(near(float(sp.binomial(20, 10)) / 2 ** 20, 0.1762, 5e-5),
    "B(20,0.5) の P(X=10) = 0.176")
chk(abs(0.79767 + 0.0001 - 0.798) < 5e-4, "0.0001 を足しても 3 桁は変わらない")

# --- m7・m8・m9 検算の強化 --------------------------------------------
in_text("$0.84$ と $0.975$ の間のはずです ✓ $0.894$ はこの中にあります。",
        "m7 例題1 の検算")
chk(0.84134 < ncdf(-BIG, 60, 50, 8) < 0.97725, "0.894 は 84% と 97.5% の間")
in_text("$\\mu$ から右に $5$ ずれています。", "m8 演習6 の検算")
chk(ncdf(480, 530, 500, 25) < ncdf(475, 525, 500, 25),
    "ずらした区間のほうが面積が小さい")
in_text("**検算（(b) について、何 $\\sigma$ か）。** $72 - 1.4 \\times 5 = 65$",
        "m9 例題4(b) の検算")
chk(near(72 - 1.4 * 5, 65, 1e-9), "65 = μ-1.4σ")
chk(0.02275 < ncdf(-BIG, 65, 72, 5) < 0.15866, "0.0808 は 2.5% と 16% の間")
# 分散を入れると、対称性の検算は通ってしまう
chk(ncdf(-BIG, 65, 72, 25) < 0.5, "σ に 25 を入れても 0.5 未満（だから足りない）")
chk(not (0.02275 < ncdf(-BIG, 65, 72, 25) < 0.15866),
    "σ に 25 を入れると、何 σ かの検算で見つかる")

# --- m10 検算でないものを地の文にした ---------------------------------
in_text("**なお、$0$ までの距離。**", "m10 例題4")
in_text("**なお、モデルと現実。**", "m10 演習10")
not_in_text("**検算（(d) について、$0$ までの距離）。**", "検算の見出しをやめた")
not_in_text("**検算（モデルと現実）。**", "検算の見出しをやめた（2）")

# --- m11 GDC の道すじ -------------------------------------------------
in_text("`menu → Statistics → Distributions` から `normCdf` を出します。",
        "m11 normCdf")
in_text("同じ `menu → Statistics → Distributions` から `invNorm` を出します。",
        "m11 invNorm")
not_in_text("正規分布の Cdf を選びます", "検証していないメニュー名は消した")
not_in_text("正規分布の逆（inverse）を選びます", "検証していないメニュー名は消した（2）")
_body_nogdc = TEXT.replace("#gdc-normcdf", "").replace("#gdc-invnorm", "")
for _bad in ("normcdf", "normalCdf", "NormCdf", "invnorm", "solve("):
    chk(_bad not in _body_nogdc, "検証していない書き方 %s は使わない" % _bad)

# --- m12 GDC §3 の 0..1 チェック --------------------------------------
in_text("ただし、$\\mu$ と $\\sigma$ だけを入れかえたときは $0$ と $1$ の間に"
        "収まることがあります。", "m12")
chk(0 < ncdf(45, 60, 8, 50) < 1, "μ と σ を入れかえても 0..1 に入る")

# --- m13 Common errors の 6 番目 -------------------------------------
in_text("## 確率を問われて、めやすの値を答えにする", "m13")
not_in_text("## $68$–$95$–$99.7$ の値を答案に書く", "衝突する見出しは消した")
in_text("**`Interpret` のようにめやすを使えと言われたときだけ**答案に書きます",
        "m13 本文")

# --- m14 Why it works の言い方 ----------------------------------------
in_text("点は無限にあるので、合計はいくらでも大きくなってしまいます。", "m14")
not_in_text("$1$ 点ずつに正の確率を割りあてると合計が $1$ をこえてしまいます",
            "雑な言い方は消した")

# --- m15 z の形の割り算をやめた ---------------------------------------
for _bad in ("\\dfrac{5 - 4.2}{0.6}", "\\dfrac{12 - 10}{2.5}",
             "\\dfrac{50 - 30}{4}", "\\dfrac{72 - 0}{5}",
             "\\dfrac{10}{6}\\sigma", "\\dfrac{4}{3}\\sigma"):
    not_in_text(_bad, "z の形の割り算は使わない: %s" % _bad)
in_text("$170 + 1.67 \\times 6 \\approx 180$", "m15 例題2")
in_text("$72 + 1.6 \\times 5 = 80$", "m15 例題4")
in_text("$4.2 + 1.33 \\times 0.6 \\approx 5$", "m15 演習4")
in_text("$12 - 0.8 \\times 2.5 = 10$", "m15 演習8")
in_text("$30 + 5 \\times 4 = 50$", "m15 演習10")
in_text("$20 + 1.33 \\times 3 \\approx 24$", "m15 演習1")
chk(near(72 + 1.6 * 5, 80, 1e-9), "72 + 1.6×5 = 80")
chk(near(12 - 0.8 * 2.5, 10, 1e-9), "12 - 0.8×2.5 = 10")
chk(near(30 + 5 * 4, 50, 1e-9), "30 + 5×4 = 50")

# --- m16 例題1(d) の model answer -------------------------------------
in_text("*Every value with $X > 50$ also has $X > 45$", "m16")
not_in_text("The region $X > 45$ contains all of $X > 50$", "読みにくい文は消した")


# ══════════════════════════════════════════════════════════
# E09・C09  正規曲線の図と、連続分布での P(X = a) = 0
# ══════════════════════════════════════════════════════════
in_text("(img/aasl-4-9-tail.svg){#fig-aasl49-tail width=100%}",
        "E09 例題 の正規曲線")
in_text("**ちょうど $1$ つの値をとる確率は $0$ です。**", "C09 1 点の確率は 0")
in_text("だから **$P(X < a)$ と $P(X \\le a)$ は同じ値**に", "C09 等号の有無")
in_text("aasl-4-5.qmd#properties", "C09 4.5 へのリンク")
_e09z = sp.Symbol("z")
chk(sp.integrate(sp.exp(-_e09z ** 2 / 2) / sp.sqrt(2 * sp.pi),
                 (_e09z, 2, 2)) == 0, "C09 幅のない区間の面積は 0")
# 566 は 500 + z*40 で z ≈ 1.645
chk(abs(float(500 + 40 * 1.6449) - 565.8) < 0.5, "E09 5% の境目は約 566")
chk(500 < 566, "E09 右のすそは平均より右")

print()
print("OK", OK, "/ NG", NG)
