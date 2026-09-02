"""AHL 4.17 の本文・例題・演習の数値を独立に検算する。

   ★ 確率は【定義から】自分で組み立てる。
     P(X = x) = e^{-m} m^x / x! を math だけで計算し、scipy と突き合わせる。
     公式集に pmf は載っていないので、本文では電卓（poissPdf / poissCdf）で
     出すが、検算では両方の実装が一致することを確かめる。
   ★ 「独立な Poisson の和は Poisson」は【仮定せず】、畳み込みで確かめる。
   ★ E(X) = m、Var(X) = m も【数え上げで】確かめる（公式を使わない）。
   ★ 最後に qmd 本文を読み、計算した値が実際に書かれているかを照合する。

   実行: python3 figs/ai-hl/check_ahl_4_17.py
"""
import math
import os
import numpy as np
from scipy import stats

ok, ng = 0, 0


def eq(name, got, want, tol=1e-9):
    global ok, ng

    def close(a, b):
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))

    if isinstance(got, (list, tuple)):
        good = (len(got) == len(want)
                and all(close(a, b) for a, b in zip(got, want)))
    elif isinstance(got, float) or isinstance(want, float):
        good = close(float(got), float(want))
    else:
        good = got == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


def approx(name, got, want, tol):
    global ok, ng
    good = abs(got - want) < tol
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}  (tol {tol})"))
    ok, ng = ok + good, ng + (not good)


def sf(x, n=3):
    if x == 0:
        return 0.0
    d = math.floor(math.log10(abs(x)))
    return round(x, -(d - n + 1))


# ── 定義から作った Poisson。scipy と必ず突き合わせる ────────────────
def ppdf(x, m):
    """P(X = x) を定義から。電卓の poissPdf(m, x) と同じもの。"""
    mine = math.exp(-m) * m ** x / math.factorial(x)
    theirs = float(stats.poisson.pmf(x, m))
    assert abs(mine - theirs) < 1e-12, f"pmf が食い違う {mine} {theirs}"
    return mine


def pcdf(a, b, m):
    """P(a <= X <= b) を、定義の和から。電卓の poissCdf(m, a, b) と同じもの。"""
    mine = sum(ppdf(k, m) for k in range(a, b + 1))
    theirs = float(stats.poisson.cdf(b, m) - (stats.poisson.cdf(a - 1, m)
                                              if a > 0 else 0.0))
    assert abs(mine - theirs) < 1e-11, f"cdf が食い違う {mine} {theirs}"
    return mine


def tail(a, m, top=160):
    """P(X >= a)。上を十分大きくとって足す。"""
    return sum(ppdf(k, m) for k in range(a, top))


print("══════════ 分布そのもの ══════════")
for m in (0.5, 1.7, 3.4, 4.3, 10.2):
    tot = sum(ppdf(k, m) for k in range(0, 160))
    approx(f"Po({m}) の確率の合計 = 1", tot, 1.0, 1e-12)
    # ★ E(X) と Var(X) を【数え上げで】出す（公式 E=Var=m を使わない）
    mu = sum(k * ppdf(k, m) for k in range(0, 160))
    var = sum((k - mu) ** 2 * ppdf(k, m) for k in range(0, 160))
    approx(f"Po({m}) の E(X) = m", mu, m, 1e-10)
    approx(f"Po({m}) の Var(X) = m", var, m, 1e-9)
eq("平均と分散が等しいのが Poisson の目印", True, True)
eq("sd は sqrt(m)", math.sqrt(6.0), 6.0 ** 0.5)

print("══════════ 独立な Poisson の和（畳み込みで確かめる） ══════════")
# ★ 定理を仮定せず、同時分布を全部たどって和の分布を作る
for m1, m2 in ((2.5, 1.8), (1.4, 2.1), (3.0, 3.0)):
    conv = {}
    for i in range(0, 120):
        for j in range(0, 120):
            conv[i + j] = conv.get(i + j, 0.0) + ppdf(i, m1) * ppdf(j, m2)
    worst = max(abs(conv.get(k, 0.0) - ppdf(k, m1 + m2)) for k in range(0, 60))
    approx(f"Po({m1}) + Po({m2}) = Po({m1 + m2})", worst, 0.0, 1e-12)
eq("和の m は m1 + m2", 2.5 + 1.8, 4.3)
eq("和の m は掛け算ではない", 2.5 * 1.8 != 4.3, True)
# ★ 差は Poisson にならない（負の値をとりうる）
d_neg = sum(ppdf(i, 2.5) * ppdf(j, 1.8)
            for i in range(0, 60) for j in range(0, 60) if i - j < 0)
eq("差は負になりうるので Poisson ではない", d_neg > 0.1, True)
approx("  P(差 < 0) は 0.3 前後", d_neg, 0.30, 0.06)

print("══════════ m は区間に比例する ══════════")
RATE = 3.4          # 1 時間あたり
for hours, want in ((1, 3.4), (3, 10.2), (0.5, 1.7), (2, 6.8)):
    eq(f"{hours} 時間なら m = {want}", RATE * hours, want)
eq("m は時間に比例する（2 倍の時間で 2 倍の m）", RATE * 2, 2 * RATE)
eq("m を変えずに時間だけ変えるのは誤り", RATE * 3 != RATE, True)

print("══════════ 例題1：Po(3.4)（1 時間あたりのメール） ══════════")
M1 = 3.4
eq("E(X) = 3.4", M1, 3.4)
eq("Var(X) = 3.4", M1, 3.4)
eq("sd = 1.84 (3 s.f.)", sf(math.sqrt(M1)), 1.84)
eq("P(X = 2) = 0.193 (3 s.f.)", sf(ppdf(2, M1)), 0.193)
eq("  生の値 0.19290", round(ppdf(2, M1), 5), 0.19290)
eq("P(X <= 2) = 0.340 (3 s.f.)", sf(pcdf(0, 2, M1)), 0.340)
eq("  生の値 0.33974", round(pcdf(0, 2, M1), 5), 0.33974)
eq("  内訳 0.0334 + 0.113 + 0.193",
   (sf(ppdf(0, M1)), sf(ppdf(1, M1)), sf(ppdf(2, M1))), (0.0334, 0.113, 0.193))
eq("P(X >= 4) = 0.442 (3 s.f.)", sf(tail(4, M1)), 0.442)
eq("  生の値 0.44164", round(tail(4, M1), 5), 0.44164)
eq("P(X >= 4) = 1 - P(X <= 3)", tail(4, M1), 1 - pcdf(0, 3, M1))
eq("  P(X <= 3) = 0.558 (3 s.f.)", sf(pcdf(0, 3, M1)), 0.558)
# よくある誤り：X >= 4 を 1 - P(X <= 4) としてしまう
eq("1 - P(X <= 4) は 0.256 で、別の値", sf(1 - pcdf(0, 4, M1)), 0.256)
eq("  正しい 0.442 とは違う", sf(1 - pcdf(0, 4, M1)) != 0.442, True)

print("══════════ 例題2：区間を変える（3 時間） ══════════")
M2 = 3.4 * 3
eq("3 時間の m = 10.2", M2, 10.2)
eq("P(X > 12) = 0.228 (3 s.f.)", sf(tail(13, M2)), 0.228)
eq("  生の値 0.22777", round(tail(13, M2), 5), 0.22777)
eq("X > 12 は X >= 13", tail(13, M2), 1 - pcdf(0, 12, M2))
eq("  X >= 12 なら別の値 0.326 (3 s.f.)", sf(tail(12, M2)), 0.326)
eq("P(X <= 8) = 0.311 (3 s.f.)", sf(pcdf(0, 8, M2)), 0.311)
eq("  生の値 0.31076", round(pcdf(0, 8, M2), 5), 0.31076)
# m を変え忘れるとどうなるか
eq("m = 3.4 のままだと P(X > 12) は 0.0000571", sf(tail(13, 3.4), 3), 5.71e-05)
eq("  正しい 0.228 とは大きく違う", tail(13, 3.4) < 0.001, True)
# 30 分なら
eq("30 分の m = 1.7", 3.4 * 0.5, 1.7)
eq("30 分で P(X = 0) = 0.183 (3 s.f.)", sf(ppdf(0, 1.7)), 0.183)
eq("  生の値 0.18268", round(ppdf(0, 1.7), 5), 0.18268)

print("══════════ 例題3：2 つの店の合計 ══════════")
MA, MB = 2.5, 1.8
MS = MA + MB
eq("合計の m = 4.3", MS, 4.3)
eq("E(合計) = 4.3", MS, 4.3)
eq("Var(合計) = 4.3", MS, 4.3)
eq("P(合計 = 5) = 0.166 (3 s.f.)", sf(ppdf(5, MS)), 0.166)
eq("  生の値 0.16622", round(ppdf(5, MS), 5), 0.16622)
eq("P(合計 <= 3) = 0.377 (3 s.f.)", sf(pcdf(0, 3, MS)), 0.377)
eq("  生の値 0.37715", round(pcdf(0, 3, MS), 5), 0.37715)
# 畳み込みでも同じ
conv5 = sum(ppdf(i, MA) * ppdf(5 - i, MB) for i in range(0, 6))
approx("  畳み込みでも P(合計 = 5) は同じ", conv5, ppdf(5, MS), 1e-12)

print("══════════ 平均と分散が近いか（Poisson が妥当かの目安） ══════════")
eq("平均 4.1・分散 4.0 は近い → Poisson は妥当", abs(4.1 - 4.0) < 0.5, True)
eq("平均 4.1・分散 1.2 は離れている → Poisson は不適", abs(4.1 - 1.2) > 0.5, True)
# binomial は分散が平均より小さい（np(1-p) < np）
n_, p_ = 20, 0.3
eq("binomial の平均 = 6", n_ * p_, 6.0)
eq("binomial の分散 = 4.2", n_ * p_ * (1 - p_), 4.2)
eq("binomial では分散 < 平均", n_ * p_ * (1 - p_) < n_ * p_, True)
eq("Poisson では分散 = 平均", 6.0, 6.0)

print("══════════ 演習1〜3 ══════════")
eq("演習1 P(X = 3) = 0.218 (3 s.f.)", sf(ppdf(3, 2.6)), 0.218)
eq("  生の値 0.21757", round(ppdf(3, 2.6), 5), 0.21757)
eq("演習1 P(X <= 1) = 0.267 (3 s.f.)", sf(pcdf(0, 1, 2.6)), 0.267)
eq("  生の値 0.26738", round(pcdf(0, 1, 2.6), 5), 0.26738)
eq("演習1 P(X >= 2) = 0.733 (3 s.f.)", sf(tail(2, 2.6)), 0.733)
eq("  P(X<=1) と P(X>=2) を足すと 1", pcdf(0, 1, 2.6) + tail(2, 2.6), 1.0)
M_20 = 5 * 20 / 60
eq("演習2 20 分の m = 5/3", M_20, 5 / 3)
eq("  小数では 1.67 (3 s.f.)", sf(M_20), 1.67)
eq("演習2 P(X = 0) = 0.189 (3 s.f.)", sf(ppdf(0, M_20)), 0.189)
eq("  生の値 0.18888", round(ppdf(0, M_20), 5), 0.18888)
eq("演習2 P(X >= 1) = 0.811 (3 s.f.)", sf(1 - ppdf(0, M_20)), 0.811)
eq("演習3 和の m = 3.5", 1.4 + 2.1, 3.5)
eq("演習3 P(X = 4) = 0.189 (3 s.f.)", sf(ppdf(4, 3.5)), 0.189)
eq("  生の値 0.18881", round(ppdf(4, 3.5), 5), 0.18881)

print("══════════ 演習6〜9 ══════════")
eq("演習6 平均 4.1・分散 4.0 → 妥当", abs(4.1 - 4.0) < 0.5, True)
eq("演習6 平均 4.1・分散 1.2 → 不適", abs(4.1 - 1.2) > 0.5, True)
eq("演習7 Po(6) の E(X) = 6", 6.0, 6.0)
eq("演習7 Po(6) の Var(X) = 6", 6.0, 6.0)
eq("演習7 sd = 2.45 (3 s.f.)", sf(math.sqrt(6)), 2.45)
eq("  生の値 2.44949", round(math.sqrt(6), 5), 2.44949)
# 演習8：AHL 4.14 との組み合わせ
eq("演習8 E(3X+2) = 14", 3 * 4 + 2, 14.0)
eq("演習8 Var(3X+2) = 36", 9 * 4, 36.0)
eq("演習8 sd(3X+2) = 6", math.sqrt(36), 6.0)
eq("  3X+2 は Poisson ではない（平均 14、分散 36 で等しくない）",
   14.0 != 36.0, True)
M9 = 12 * 4 / 24
eq("演習9 4 時間の m = 2", M9, 2.0)
eq("演習9 P(X = 2) = 0.271 (3 s.f.)", sf(ppdf(2, M9)), 0.271)
eq("  生の値 0.27067", round(ppdf(2, M9), 5), 0.27067)
eq("演習9 P(X >= 3) = 0.323 (3 s.f.)", sf(tail(3, M9)), 0.323)
eq("  生の値 0.32332", round(tail(3, M9), 5), 0.32332)

print("══════════ 本文に、その数値が実際に書かれているか ══════════")
# ★ ここまでは数値を【計算】しただけ。qmd を読んで、記述と突き合わせる。
QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "ahl-4-17.qmd")
TXT = open(QMD, encoding="utf-8").read()


def in_text(name, needle, want=True):
    global ok, ng
    good = (needle in TXT) == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else
           f"   ({'欠けている' if want else '残っている'}: {needle!r})"))
    ok, ng = ok + good, ng + (not good)


for lab, needle in [
        ("例題1 P(X=2)", "0.193"),
        ("例題1 P(X<=2)", "0.340"),
        ("例題1 P(X>=4)", "0.442"),
        ("例題2 3 時間の m", "10.2"),
        ("例題2 P(X>12)", "0.228"),
        ("例題3 合計の m", "4.3"),
        ("例題3 P(=5)", "0.166"),
        ("演習1 P(X=3)", "0.218"),
        ("演習2 P(X=0)", "0.189"),
        ("演習7 sd", "2.45"),
        ("演習9 P(X>=3)", "0.323")]:
    in_text(lab, needle)

# ★ 公式集の記述
in_text("公式集の Po(m) がある", "X \\sim \\mathrm{Po}(m)")
in_text("E(X) = m がある", "E(X) = m")
in_text("Var(X) = m がある", "\\text{Var}(X) = m")
# ★ シラバスの引用
in_text("2 条件の引用（independent）", "Events are independent")
in_text("2 条件の引用（uniform rate）",
        "Events occur at a uniform average rate")
in_text("分布の選び分けの引用", "select between the normal, the binomial and "
                                "the Poisson distributions")
in_text("Not required の引用", "Formal proof of means and variances")
# ★ Common error の数値が、計算した値と一致しているか
in_text("m を変え忘れたときの値 0.0000571", "0.0000571")
in_text("  誤った 0.0000066 が残っていない", "0.0000066", want=False)
in_text("more than / at least の差 0.326", "0.326")
# ★ 2 つの値の【比】まで検証する（本文が「〜分の1」と書いているところ）
RATIO = tail(13, M2) and (tail(13, M2) / tail(13, 3.4))
eq("  0.228 と 0.0000571 の比は約 4000", round(RATIO / 1000) * 1000, 4000)
in_text("比を 4000 分の 1 と書いている", "$4000$ 分の $1$")
in_text("  誤った 3 万分の 1 が残っていない", "$3$ 万分の $1$", want=False)
# ★ GDC のメニューは Statistics → Distributions（本の他ページと同じ）
in_text("GDC のメニューが Statistics → Distributions",
        "menu → Statistics → Distributions")
in_text("  Probability → Distributions が残っていない",
        "Probability → Distributions", want=False)
# ★ 和の規則を 3X と取り違えさせない書き方になっているか
in_text("3X は Po(10.2) にならないと書いてある", "$3X$ は $\\mathrm{Po}(10.2)$ には")
# ★ 公式集に無いものを明示しているか
in_text("覚える必要があります と書いてある", "覚える必要があります")
# ★ m の比例を「掛ける」と書いているか（割ると書いていないか）
in_text("m は区間に比例すると書いてある", "比例")
# ★ 平均 = 分散 が Poisson の目印であること
in_text("平均と分散が等しいと書いてある", "平均と分散が等しい")

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
