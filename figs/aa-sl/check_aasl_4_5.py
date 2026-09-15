"""AA SL 4.5（確率の基礎）の内容を検算する。

    python3 figs/aa-sl/check_aasl_4_5.py
"""
import glob
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability")
QMD = os.path.join(BASE, "aasl-4-5.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_4_5.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.nsimplify(u) - sp.nsimplify(v)) == 0,
        msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 道具 —— 標本空間を作って数える
# ══════════════════════════════════════════════════════════
DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]


def prob(space, pred):
    return F(sum(1 for s in space if pred(s)), len(space))


chk(len(DICE) == 36, "さいころ 2 個の標本空間は 36")
chk(prob(DICE, lambda s: True) == 1, "道具: 全体の確率は 1")
chk(prob(DICE, lambda s: False) == 0, "道具: 空事象は 0")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
in_text("{#eq-aasl45-prob}", "P(A) のラベル")
in_text("{#eq-aasl45-comp}", "余事象のラベル")
in_text("{#eq-aasl45-relfreq}", "相対度数のラベル")
in_text("{#eq-aasl45-expected}", "期待される回数のラベル")
in_text("{#tbl-aasl45-words}", "ことばの表")
chk(TEXT.count("@eq-aasl45-prob") >= 3, "P(A) を参照している")
chk(TEXT.count("@eq-aasl45-comp") >= 3, "余事象を参照している")
chk(TEXT.count("@eq-aasl45-expected") >= 3, "期待される回数を参照している")
in_text("P(A) = \\frac{n(A)}{n(U)}", "P(A) の式")
in_text("P(A) + P(A') = 1", "余事象の式")
in_text("(\\text{expected number}) = n \\times p", "期待される回数の式")
in_text("- $0 \\le P(A) \\le 1$", "確率の範囲")
in_text("**この式は公式集にありません。** ただ、割り算をするだけです。",
        "相対度数は公式集にない")
in_text("**この式は、公式集の 4.5 の欄にはありません。**", "期待される回数は 4.5 にない")
in_text("$E(X) = np$ として、**4.8 の欄**に出てきます", "4.8 にある")
# シラバスの例（128 人、0.1、12.8）
eq(128 * sp.Rational("0.1"), sp.Rational("12.8"), "シラバスの例: 128×0.1 = 12.8")
in_text("「$128$ 人のクラスで欠席の確率が $0.1$ なら、期待される欠席者は $12.8$ 人」です。",
        "128 人の例")
not_in_text("というのが、シラバスの挙げている例です", "出典は付けない")
# 表のマス目
eq(6 * 6, 36, "6×6 = 36")
in_text("コイン $1$ 枚とさいころ $1$ 個なら $2 \\times 6 = 12$ マスです。", "12 マス")
in_text("$(1, 4)$ と $(4, 1)$ は**別の結果**です。", "順番を区別する")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
in_text("\\frac{n(A)}{n(U)} + \\frac{n(A')}{n(U)} = 1", "余事象の導出")
in_text("だから $n(A) + n(A') = n(U)$ です。", "個数の関係")
in_text("ずれの大きさそのものは、回数が増えると**大きくなります**。", "ずれ自体は増える")
_nA, _nU = sp.symbols("n_A n_U", positive=True)
eq(_nA / _nU + (_nU - _nA) / _nU, 1, "P(A) + P(A') = 1（記号のまま）")
# 1 つあたり 1/n(U) を n(A) 回足す
eq(sp.Rational(1, 36) * 6, F(6, 36), "1/36 を 6 回足すと 6/36")

# ══════════════════════════════════════════════════════════
# 3. 例題 1  袋の玉
# ══════════════════════════════════════════════════════════
BAG = ["r"] * 5 + ["b"] * 3 + ["g"] * 4
chk(len(BAG) == 12, "例題1 の n(U) は 12")
eq(5 + 3 + 4, 12, "5+3+4 = 12")
eq(prob(BAG, lambda c: c == "r"), F(5, 12), "例題1(b)")
eq(prob(BAG, lambda c: c != "b"), F(3, 4), "例題1(c)")
eq(1 - F(3, 12), F(9, 12), "1 - 3/12 = 9/12")
eq(F(9, 12), F(3, 4), "9/12 = 3/4")
eq(F(5, 12) + F(3, 12) + F(4, 12), 1, "3 色の確率の合計は 1")
chk(F(5, 12) < 1, "5/12 < 1")
chk(5 + 4 == 9, "青でない玉は 9 個")
in_text("P(\\text{red}) = \\frac{5}{12}", "例題1(b) の答え")
in_text("P(\\text{not blue}) = 1 - \\frac{3}{12} = \\frac{9}{12} = \\frac{3}{4}",
        "例題1(c) の答え")

# ══════════════════════════════════════════════════════════
# 4. 例題 2  さいころ 2 個
# ══════════════════════════════════════════════════════════
eq(prob(DICE, lambda s: s[0] % 2 == 0 and s[1] % 2 == 0), F(1, 4), "例題2(b)")
eq(F(9, 36), F(1, 4), "9/36 = 1/4")
eq(3 * 3, 9, "3×3 = 9")
eq(prob(DICE, lambda s: sum(s) == 5), F(1, 9), "例題2(c)")
chk(sorted(s for s in DICE if sum(s) == 5) == [(1, 4), (2, 3), (3, 2), (4, 1)],
    "和が 5 になる組")
eq(F(4, 36), F(1, 9), "4/36 = 1/9")
eq(prob(DICE, lambda s: sum(s) != 5), F(8, 9), "例題2(d)")
eq(F(1, 9) + F(8, 9), 1, "足すと 1")
# 別の道すじ：1 個ずつ
eq(F(3, 6) * F(3, 6), F(1, 4), "1/2 × 1/2 = 1/4")
eq(F(3, 6), F(1, 2), "3/6 = 1/2")
# 順番を区別しないと 2 通りになる
chk(len({tuple(sorted(s)) for s in DICE if sum(s) == 5}) == 2,
    "区別しないと 2 通りになる")
in_text("(1,4), \\quad (2,3), \\quad (3,2), \\quad (4,1)", "例題2(c) の書き出し")
in_text("和が $2$ で $1$ 通り、$3$ で $2$、$4$ で $3$、$5$ で $4$、$6$ で $5$、$7$ で $6$ 通り", "和ごとの通り数")

# ══════════════════════════════════════════════════════════
# 5. 例題 3  期待される欠席者
# ══════════════════════════════════════════════════════════
eq(640 * sp.Rational("0.045"), sp.Rational("28.8"), "例題3(a)")
eq(F(41, 640), sp.Rational("0.0640625"), "41/640")
chk(abs(float(F(41, 640)) - 0.0641) < 5e-5, "3 桁で 0.0641")
eq(sp.Rational("28.8") * 200, 5760, "例題3(d)")
eq(640 * 200, 128000, "640×200 = 128000")
eq(128000 * sp.Rational("0.045"), 5760, "別の道すじでも 5760")
chk(F(41, 640) > sp.Rational("0.045"), "その日は期待より多い")
chk(41 > sp.Rational("28.8"), "41 > 28.8")
chk(abs(float(640 / 22) - 29) < 1, "640÷22 は約 29")
in_text("640 \\times 0.045 = 28.8", "例題3(a) の計算")
in_text("\\frac{41}{640} = 0.0640625 = 0.0641 \\ (3 \\text{ s.f.})", "例題3(b)")
in_text("$640 \\times 200 = 128\\,000$ 回の「生徒・日」があり、"
        "$128\\,000 \\times 0.045 = 5760$", "例題3(d) の検算")

# ══════════════════════════════════════════════════════════
# 6. 例題 4  コイン
# ══════════════════════════════════════════════════════════
eq(F(116, 200), sp.Rational("0.58"), "例題4(a)")
eq(200 * sp.Rational("0.5"), 100, "例題4(c)")
eq(116 - 100, 16, "16 回多い")
eq(F(16, 200), sp.Rational("0.08"), "16/200 = 0.08")
eq(sp.Rational("0.58") - sp.Rational("0.5"), sp.Rational("0.08"), "差も 0.08")
eq(200 * sp.Rational("0.5") * 2, 200, "表と裏の期待値の合計は 200")
chk(sp.Rational("0.58") <= 1, "相対度数は 1 以下")
in_text("\\frac{116}{200} = 0.58", "例題4(a) の計算")
in_text("裏は $200 - 116 = 84$ 回で、$\\dfrac{84}{200} = 0.42$ です", "例題4(d) の検算")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1  素数
DIE = list(range(1, 7))
_primes = [k for k in DIE if k > 1 and all(k % d for d in range(2, k))]
chk(_primes == [2, 3, 5], f"さいころの素数: {_primes}")
eq(F(len(_primes), 6), F(1, 2), "演習1 の答え")
chk(1 not in _primes, "1 は素数ではない")
chk(sorted(set(DIE) - set(_primes)) == [1, 4, 6], "素数でないのは 1,4,6")
in_text("*primes on a die:* $2, 3, 5$", "演習1 の素数")
in_text("$$P = \\frac{3}{6} = \\frac{1}{2}$$", "演習1 の答え")
# 2  白と黒
eq(7 + 5, 12, "演習2 の n(U)")
eq(F(7, 12) + F(5, 12), 1, "演習2 の合計")
eq(1 - F(7, 12), F(5, 12), "余事象でも 5/12")
chk(sp.gcd(7, 12) == 1, "7/12 は約分できない")
in_text("P(\\text{white}) = \\frac{7}{12}, \\qquad P(\\text{not white}) = "
        "\\frac{5}{12}", "演習2 の答え")
# 3  コイン 2 枚
COINS = [(a, b) for a in "HT" for b in "HT"]
chk(len(COINS) == 4, "演習3 の n(U) は 4")
eq(prob(COINS, lambda s: s.count("H") == 1), F(1, 2), "演習3 の答え")
eq(F(2, 4), F(1, 2), "2/4 = 1/2")
chk([sum(1 for s in COINS if s.count("H") == k) for k in range(3)] == [1, 2, 1],
    "0 枚 1 通り、1 枚 2 通り、2 枚 1 通り")
eq(1 + 2 + 1, 4, "合計 4")
in_text("| **first coin $H$** | $HH$ | $HT$ |", "演習3 の表")
in_text("| **first coin $T$** | $TH$ | $TT$ |", "演習3 の表 2 行目")
in_text("も「起こりうる結果をすべて集めたもの」ではあります。**", "3 通りも標本空間ではある")
# 4  余事象と期待される回数
eq(1 - sp.Rational("0.35"), sp.Rational("0.65"), "演習4 の P(A')")
eq(400 * sp.Rational("0.35"), 140, "演習4 の期待される回数")
eq(400 * sp.Rational("0.65"), 260, "A' の側は 260")
eq(140 + 260, 400, "合計は 400")
chk(abs(400 / 3 - 133) < 1, "400 の 1/3 は約 133")
chk(sp.Rational("0.35") > F(1, 3), "0.35 は 1/3 より大きい")
in_text("$$P(A') = 1 - 0.35 = 0.65$$", "演習4 の答え")
in_text("$400 \\times 0.65 = 260$ で、$140 + 260 = 400$", "演習4 の検算")
# 5  スピナー
SP = list(range(1, 9))
_m3 = [k for k in SP if k % 3 == 0]
chk(_m3 == [3, 6], f"1..8 の 3 の倍数: {_m3}")
eq(F(2, 8), F(1, 4), "演習5 の答え")
chk(9 not in SP, "9 はスピナーにない")
in_text("*multiples of $3$:* $3, 6$", "演習5 の倍数")
in_text("$$P = \\frac{2}{8} = \\frac{1}{4}$$", "演習5 の答え")
# 6  種
eq(300 * sp.Rational("0.82"), 246, "演習6 の答え")
eq(300 * sp.Rational("0.18"), 54, "発芽しない側")
eq(246 + 54, 300, "合計は 300")
eq(300 * F(4, 5), 240, "300 の 4/5 は 240")
chk(sp.Rational("0.82") > F(4, 5), "0.82 > 4/5")
in_text("$$300 \\times 0.82 = 246$$", "演習6 の答え")
# 7  さいころ 60 回
eq(60 * F(1, 6), 10, "演習7 の期待される回数")
eq(14 - 10, 4, "差は 4")
chk(abs(float(F(14, 60)) - 0.233) < 5e-4, "14/60 は約 0.233")
chk(abs(float(F(1, 6)) - 0.167) < 5e-4, "1/6 は約 0.167")
in_text("$6$ 以外は $60 - 14 = 46$ 回で、期待される回数は $60 \\times \\dfrac{5}{6} = 50$ 回", "演習7 の検算")
in_text("$\\dfrac{14}{60} \\approx 0.233$ で、$\\dfrac{1}{6} \\approx 0.167$",
        "演習7 の相対度数")
eq(60 - 14, 46, "6 以外は 46 回")
eq(60 * F(5, 6), 50, "期待は 50 回")
eq(50 - 46, 4, "ずれは 4 回")
# 8  バス
eq(10 * sp.Rational("0.2"), 2, "演習8 の期待される回数")
eq(8 * sp.Rational("0.2"), sp.Rational("1.6"), "8 回なら 1.6")
chk(sp.Rational("1.6") != sp.floor(sp.Rational("1.6")), "1.6 は整数でない")
in_text("$$10 \\times 0.2 = 2$$", "演習8 の計算")
in_text("遅れる回数は $0, 1, 2, \\ldots, 10$ の $11$ 通りありえます", "演習8 の検算")
# 9  P(A) <= 1
in_text("n(A) \\le n(U)", "個数の関係")
# 10  画びょう
eq(F(31, 50), sp.Rational("0.62"), "演習10 の相対度数")
in_text("$\\dfrac{31}{50}$", "演習10 の値")

# ══════════════════════════════════════════════════════════
# 8. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _leak, _m in [
        ("\\frac{5}{12}", "例題1(b)"),
        ("\\frac{3}{4}", "例題1(c)"),
        ("和が $5$", "例題2(c)"),
        ("$6 \\times 6 = 36$", "例題2(a)"),
        ("ちょうど $100$ 回", "例題4(c)"),
        ("28.8", "例題3(a)"),
        ("0.0641", "例題3(b)"),
        ("5760", "例題3(d)"),
        ("0.58", "例題4(a)"),
        ("246", "演習6"),
        ("\\frac{2}{8}", "演習5"),
]:
    not_in_body(_leak, _m)
# 本文の 6/36 は図の説明に合わせたもので、例題・演習では和が 5（4/36）を使う
chk("\\dfrac{4}{36}" in BODY, "本文の例は 4/36（約分の例）")
chk(prob(DICE, lambda s: sum(s) == 7) == F(1, 6), "和が 7 なら 6/36")
chk(prob(DICE, lambda s: sum(s) == 5) == F(1, 9), "和が 5 なら 4/36")

# ══════════════════════════════════════════════════════════
# 9. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk(TEXT.count("callout-important") == 2, "公式集の callout は 2 つ")
in_text("$P(A) = \\dfrac{n(A)}{n(U)}$ は、公式集の **4.5** の欄にあります。",
        "P(A) は公式集の 4.5")
in_text("$P(A) + P(A') = 1$ は、公式集の **4.5** の欄にあります。",
        "余事象も公式集の 4.5")
_quotes = [l for l in TEXT.splitlines() if l.startswith("> ")]
chk(len(_quotes) == 0, f"シラバスの逐語の引用はない: {_quotes}")
not_in_text("Sample spaces can be represented in many ways", "Guidance は貼らない")
not_in_text("expected number of absent students is 12.8", "Guidance は逐語で貼らない")

# ══════════════════════════════════════════════════════════
# 10. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("**覚えるのは、この式が使える条件のほうです。**", "使える条件")
in_text("**「必ずその回数だけ起こる」ではありません。**", "保証ではない")
in_text("**$1$ より大きい確率や、負の確率が出たら、計算がまちがっています。**",
        "範囲の確かめ")

# ══════════════════════════════════════════════════════════
# 11. GDC —— このページには置かない
# ══════════════════════════════════════════════════════════
chk("## Using your GDC" not in TEXT, "4.5 には GDC の節を置かない")
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 0, f"GDC の折りたたみも置かない: {_gdc}")
in_text("## この項目に電卓は要りません", "電卓が要らないことを書く")
in_text("確率の計算は、Paper 1 でも Paper 2 でも**手でできます**。", "手でできる")
not_in_text("solve(", "CAS 前提の solve( は書いていない")
not_in_text("binomPdf", "この項目では使わない")

# ══════════════════════════════════════════════════════════
# 12. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 7,
    f"model-answer が 7: {TEXT.count('{.model-answer}')}")
_asks = len(re.findall(r"\[(?:[^\]]*?)(?:Explain|Justify|Comment|Interpret|Identify"
                       r"|Describe|Suggest)(?:[^\]]*?)\]\{\.q-en\}", TEXT))
chk(_asks == 7, f"説明を求める問いが 7: {_asks}")
chk(len(re.findall(r"^::: \{#exm-aasl45-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk(TEXT.count("::: {.callout-warning}") == 7, "Common errors 6 + 本文 1 で 7")
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
    _bb = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _bb), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl45", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "形の合わないリンク: " + _href)
chk(TEXT.count("@fig-aasl45-idea") >= 2, "図を本文から 2 か所以上参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-4-5-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-4-5-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) The sample space as a table", "図(a) の題")
in_fig("the number of cells is $n(U)$", "図(a) の n(U)")
chk("6 \\\\times 6 = 36" not in FIG, "図に 36 は書かない")
in_fig("shaded event: the two numbers add to $7$", "図(a) の事象の名前")
in_fig("\\\\frac{6}{36} = \\\\frac{1}{6}", "図(a) は約分してある")
in_fig("$(2,5)$ and $(5,2)$ are both shaded, and are counted ", "図(a) の注意")
in_fig("(b) Relative frequency as trials are added", "図(b) の題")
in_fig("theoretical probability", "図(b) の理論値")
in_fig("wide swings at the start", "図(b) のはじめ")
in_fig("narrow later", "図(b) のあと")
in_fig("the relative frequency settles towards the theoretical ", "図(b) の説明")
# 図の色を付けた事象は「和が 7」で、例題・演習の「和が 5」とちがう
chk("a + b == 7" in FIGCODE, "図は和が 7 を色づけしている")
chk("a + b == 5" not in FIGCODE, "図は和が 5 ではない")
chk(len([s for s in DICE if sum(s) == 7]) == 6, "和が 7 は 6 マス")
# 図の (2,5) と (5,2) が、本当に色を付けたマスであること
chk((2, 5) in [s for s in DICE if sum(s) == 7], "(2,5) は和が 7")
chk((5, 2) in [s for s in DICE if sum(s) == 7], "(5,2) は和が 7")
chk((1, 4) not in [s for s in DICE if sum(s) == 7], "(1,4) は色を付けていない")
# 図の p が、例題・演習で使った確率とちがう
_m = re.search(r"^P = ([0-9.]+)$", FIGCODE, re.M)
chk(_m is not None, "図の p が読める")
for _v in ["0.045", "0.5", "0.35", "0.82", "0.2"]:
    chk(abs(float(_m.group(1)) - float(_v)) > 1e-9,
        "図の p が本文の値と重なる: " + _v)
in_text("(a) When two things happen one after the other, the sample space can be set "
        "out as a table", "キャプションが (a) を説明")
in_text("(b) The relative frequency of an event moves up and down",
        "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 14. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/04-statistics-and-probability/aasl-4-5.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-4-4.qmd") < DRAFT.index("aasl-4-5.qmd"), "並びが 4.4 → 4.5")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aasl-4-5.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| trial |", "| outcome |", "| sample space |", "| event |",
           "| complementary events |", "| relative frequency |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- §3 が equally likely の議論で一般の性質を出していた ----------------
in_text("**equally likely のときは** $n(A)$ が $0$ 以上 $n(U)$ 以下で", "equally likely のとき")
in_text("同様に確からしくないときも、**どの結果の確率も $0$ 以上で、全部を足すと $1$**",
        "そうでないときの理由")
not_in_text("$n(A)$ は $0$ 以上 $n(U)$ 以下なので、次のことが自動的に成り立ちます。",
            "古い言い方は消した")
# ゆがんださいころでは n(A)/n(U) が確率にならない例
_biased = {1: F(1, 2), 2: F(1, 10), 3: F(1, 10), 4: F(1, 10), 5: F(1, 10),
           6: F(1, 10)}
chk(sum(_biased.values()) == 1, "ゆがんださいころでも確率の合計は 1")
chk(_biased[6] != F(1, 6), "6 の確率は 1/6 ではない")
chk(all(0 <= v <= 1 for v in _biased.values()), "それでも 0 以上 1 以下")
chk(sum(v for k, v in _biased.items() if k % 2 == 0) <= 1, "事象の確率も 1 以下")

# --- §5・§6 が例題の答えを出していた -----------------------------------
in_text("コイン $1$ 枚とさいころ $1$ 個なら $2 \\times 6 = 12$ マスです。", "§5 の例")
not_in_body("6 \\times 6 = 36", "例題2(a) の答えは本文に出さない")
in_text("公平なコインを $60$ 回投げても、表がちょうど $30$ 回になる", "§6 の例")
not_in_body("$200$ 回投げても", "例題4 の場面は本文に出さない")
eq(2 * 6, 12, "2×6 = 12")
eq(60 * F(1, 2), 30, "60 の半分は 30")

# --- 期待される回数の式は 4.8 の欄にある ---------------------------------
in_text("**この式は、公式集の 4.5 の欄にはありません。**", "4.5 にはない")
in_text("二項分布の平均 $E(X) = np$ として、**4.8 の欄**に出てきます。", "4.8 にある")
not_in_text("です。**この式は公式集にありません。**\\n\\n**整数にならない",
            "誤った言い方は消した")

# --- シラバスの例に出典を付けない ----------------------------------------
not_in_text("シラバスの挙げている例", "出典は付けない")

# --- Why it works —— 足せるという規則を名指しした ------------------------
in_text("**重ならない結果の確率は、足せます。**", "足せるという規則")
in_text("ここで使っているのは、[第 3 節](#properties)の", "第 3 節を参照")

# --- Why it works —— ずれの大きさは増える -------------------------------
in_text("ずれの大きさそのものは、回数が増えると**大きくなります**。", "ずれは増える")
in_text("**ずれの増え方が回数の増え方よりずっとゆっくり**", "増え方がゆっくり")
not_in_text("同じだけのずれが**分母に薄められて**いきます", "誤った言い方は消した")
# 実際に、ずれの典型的な大きさは sqrt(n p (1-p)) で増える
for _n in (10, 100, 1000):
    _sdv = sp.sqrt(_n * sp.Rational(1, 2) * sp.Rational(1, 2))
    chk(float(_sdv) > 0, f"n={_n} のずれの目安")
chk(float(sp.sqrt(1000 * F(1, 4))) > float(sp.sqrt(10 * F(1, 4))),
    "n が大きいほど、回数のずれは大きい")
chk(float(sp.sqrt(1000 * F(1, 4))) / 1000 < float(sp.sqrt(10 * F(1, 4))) / 10,
    "それでも、割ったあとは小さくなる")

# --- 図のキャプションに事象の名前を入れた --------------------------------
in_text("the shaded event here is that the two numbers add to seven.",
        "キャプションに事象の名前")

# --- 例題2 の検算 3 つ ---------------------------------------------------
in_text("**$1$ 個目を固定して数えます。**", "例題2(a) の検算")
in_text("**偶数でない場合も数えます。** どちらも奇数が $3 \\times 3 = 9$ 通り",
        "例題2(b) の検算")
not_in_text("$\\dfrac{1}{2} \\times \\dfrac{1}{2} = \\dfrac{1}{4}$ ✓ 数えた答えと一致します",
            "独立性を使う検算は消した")
in_text("**和ごとの通り数を数えます。**", "例題2(c) の検算")
not_in_text("**$(1,4)$ と $(4,1)$ を両方数えたか見ます。**", "答えを渡す検算は消した")
# 和ごとの通り数
_bysum = {k: sum(1 for s in DICE if sum(s) == k) for k in range(2, 13)}
chk([_bysum[k] for k in range(2, 8)] == [1, 2, 3, 4, 5, 6], f"和 2..7: {_bysum}")
chk(sum(_bysum[k] for k in range(2, 8)) == 21, "和 7 までで 21 通り")
chk(sum(_bysum[k] for k in range(8, 13)) == 15, "和 8 以上で 15 通り")
chk(21 + 15 == 36, "合計 36")
# 偶奇の数え方
chk(sum(1 for s in DICE if s[0] % 2 and s[1] % 2) == 9, "どちらも奇数が 9")
chk(sum(1 for s in DICE if (s[0] % 2) != (s[1] % 2)) == 18, "片方だけ偶数が 18")
chk(9 + 18 + 9 == 36, "9 + 18 + 9 = 36")

# --- 例題4(d) —— 「公平なら 100 にならない」は偽 -------------------------
in_text("A fair coin need not give exactly $100$ heads", "need not に直した")
not_in_text("a fair coin does not give exactly $100$ heads", "断定は消した")
in_text("However $16$ is a large difference for $200$ flips, so this result does give "
        "some reason to doubt that the coin is fair.", "疑う理由にはなる")
not_in_text("One experiment of this size cannot show that the coin is not fair",
            "言いすぎは消した")
# 公平なコインでちょうど 100 回になる確率は 0 ではない
_p100 = sp.binomial(200, 100) / sp.Integer(2) ** 200
chk(float(_p100) > 0.05, f"ちょうど 100 になる確率は約 {float(_p100):.4f}")
chk(float(_p100) < 0.07, "それでも 7% より小さい")
# 116 は 2 標準偏差より外
chk(abs(116 - 100) / float(sp.sqrt(200 * F(1, 4))) > 2,
    "116 は 2 標準偏差より外（だから「疑う理由」）")
# 演習7 の 14/60 は 2 標準偏差の内側（だから「言えない」）
chk(abs(14 - 10) / float(sp.sqrt(60 * F(1, 6) * F(5, 6))) < 2,
    "14 は 2 標準偏差の内側")

# --- 例題4(d) の検算を、裏の側にした -------------------------------------
in_text("**裏の相対度数を出します。** 裏は $200 - 116 = 84$ 回", "裏で見る検算")
eq(200 - 116, 84, "裏は 84 回")
eq(F(84, 200), sp.Rational("0.42"), "84/200 = 0.42")
eq(sp.Rational("0.58") + sp.Rational("0.42"), 1, "0.58 + 0.42 = 1")
eq(abs(84 - 100), 16, "裏のずれも 16")

# --- 演習1 の検算が、1 を素数と数えても通っていた ------------------------
in_text("**$1$ つずつ判定します。** $1$ は約数が $1$ つだけなので素数では",
        "演習1 の検算")
not_in_text("**素数でないほうを数えます。** $1, 4, 6$ の $3$ つです", "通ってしまう検算は消した")
# 1 を素数と数えても、古い検算は通ってしまうことを確かめる
chk(len([1, 2, 3, 5]) + len([4, 6]) == 6, "誤った分け方でも合計は 6（だから検算にならない）")

# --- 演習3 —— 表で書き出させ、標本空間の説明を直した ---------------------
in_text("Set out the sample space as a table", "演習3 は表")
in_text("| **first coin $H$** | $HH$ | $HT$ |", "演習3 の表")
in_text("も「起こりうる結果をすべて集めたもの」ではあります。**", "3 通りも標本空間")
in_text("$1$ 枚が $2$ 通り、$0$ 枚と $2$ 枚が $1$ 通りずつ", "確からしさがちがう理由")
not_in_text("**$3$ 通り（$0$ 枚・$1$ 枚・$2$ 枚）としないでください。**",
            "定義と食いちがう言い方は消した")
# 目標に対応する問い（表）ができたこと
chk("as a table" in TEXT, "表で書き出させる問いがある")

# --- 演習5 の検算が、9 を入れる誤りを通していた --------------------------
in_text("**$3$ の倍数でない数を数えます。** $1, 2, 4, 5, 7, 8$ の $6$ 個です",
        "演習5 の検算")
not_in_text("$8$ 個なら $2$ 個か $3$ 個です", "通ってしまう検算は消した")
chk(len([k for k in range(1, 9) if k % 3]) == 6, "3 の倍数でないのは 6 個")
chk(2 + 6 == 8, "2 + 6 = 8")

# --- 演習7・8 の検算 -----------------------------------------------------
in_text("**$6$ 以外の側でも見ます。**", "演習7 の検算")
in_text("**起こりうる回数を数えます。** 遅れる回数は $0, 1, 2, \\ldots, 10$ の "
        "$11$ 通り", "演習8 の検算")
chk(len(range(0, 11)) == 11, "0 から 10 で 11 通り")

# --- 演習10 —— 「同様に確からしくない」を断定していた ---------------------
in_text("**同様に確からしいと言える理由があるか探します。**", "演習10 の検算")
in_text("A drawing pin has no symmetry that makes the two outcomes equally likely",
        "対称性がない、という言い方")
not_in_text("the two outcomes are not equally likely, so the probability cannot be "
            "found by counting; it can only be estimated, and a larger",
            "断定は消した")
not_in_text("画びょうは、上向きと横向きが**同様に確からしくありません**", "断定は消した（検算）")

# --- 演習9 —— equally likely でない場合も足した --------------------------
in_text("When they are not, the same conclusion follows because the probabilities of "
        "all the outcomes are non-negative and add to $1$.", "演習9 の一般の場合")

# --- 図の系列を、理論値の近くで終わるものに変えた ------------------------
in_fig("np.random.default_rng(22)", "系列の種を変えた")
chk("20260908" not in FIGCODE, "古い種は消した")


# ══════════════════════════════════════════════════════════
# C09  $P(A)=0$ =「起こらない」は、結果が有限個の場面に限る
# ══════════════════════════════════════════════════════════
in_text("- **結果が有限個の場面では**、$P(A) = 0$ は「起こらない」",
        "C09 有限個への限定")
in_text("## 連続な量では、$P(A) = 0$ でも「起こらない」とは限りません",
        "C09 折り畳みの見出し")
in_text("aasl-4-9.qmd#calc", "C09 4.9 へのリンク")
in_text("**「確率 $0$」と「起こらない」が同じなのは、有限個の場面に限った"
        "話**です。", "C09 まとめ")
# 連続分布では 1 点の確率が 0
_c09 = sp.Symbol("t")
chk(sp.integrate(sp.exp(-_c09 ** 2 / 2) / sp.sqrt(2 * sp.pi),
                 (_c09, 1, 1)) == 0, "C09 1 点の区間の面積は 0")
chk(sp.integrate(sp.Rational(1, 1), (_c09, 0, 1)) == 1,
    "C09 区間全体の面積は 1")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
