"""AHL 4.18b（各分布での検定）の数値をぜんぶ検算する。
   実行: python3 figs/ai-hl/check_ahl_4_18b.py

   方針:
     (1) z と t の統計量は【定義の式から】組み立てる
     (2) p-value は scipy と、独立な実装（誤差関数・確率の和）で突き合わせる
     (3) matched pairs は「差をとって 1 標本」と ttest_rel の両方で出して一致を見る
     (4) 相関の t は r から作った式と linregress の両方で出す
     (5) 最後に .qmd を読んで、本文にその数値が書かれているかを確かめる
"""
import math
import os

import numpy as np
from scipy import stats

ok = ng = 0


def eq(name, got, want, note=""):
    global ok, ng
    good = got == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}") +
          (("   " + note) if note else ""))
    ok, ng = ok + good, ng + (not good)


def approx(name, got, want, tol=5e-7):
    global ok, ng
    good = abs(got - want) <= tol
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got!r}  want {want!r}"))
    ok, ng = ok + good, ng + (not good)


def sf(x, n=3):
    if x == 0:
        return 0.0
    d = math.floor(math.log10(abs(x)))
    return round(x, -(d - n + 1))


def ncdf(z):
    mine = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    theirs = float(stats.norm.cdf(z))
    assert abs(mine - theirs) < 1e-13, f"ncdf が食い違う {mine} {theirs}"
    return mine


def bpdf(k, n, p):
    mine = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    theirs = float(stats.binom.pmf(k, n, p))
    assert abs(mine - theirs) < 1e-13
    return mine


def ppdf(k, m):
    mine = math.exp(-m) * m ** k / math.factorial(k)
    theirs = float(stats.poisson.pmf(k, m))
    assert abs(mine - theirs) < 1e-13
    return mine


def btail_up(k, n, p):
    return sum(bpdf(j, n, p) for j in range(k, n + 1))


def btail_lo(k, n, p):
    return sum(bpdf(j, n, p) for j in range(0, k + 1))


def ptail_up(k, m, top=160):
    return sum(ppdf(j, m) for j in range(k, top))


def ptail_lo(k, m):
    return sum(ppdf(j, m) for j in range(0, k + 1))


def zstat(xbar, mu0, sigma, n):
    """定義の式そのまま。"""
    return (xbar - mu0) / (sigma / math.sqrt(n))


def tstat(data, mu0):
    """定義の式そのまま。s は不偏推定（ddof=1）。"""
    a = np.asarray(data, dtype=float)
    n = a.size
    xbar = a.mean()
    s = a.std(ddof=1)
    return (xbar - mu0) / (s / math.sqrt(n)), xbar, s, n - 1


print("══════════ 例題1：z Test（両側） ══════════")
Z1 = zstat(25.15, 25.0, 0.4, 40)
approx("standard error = 0.0632…", round(0.4 / math.sqrt(40), 6), 0.063246)
approx("z = 2.37 (3 s.f.)", sf(Z1), 2.37)
approx("  生の値 2.37171", round(Z1, 5), 2.37171)
P1 = 2 * (1 - ncdf(Z1))
approx("両側 p = 0.0177 (3 s.f.)", sf(P1), 0.0177)
approx("  生の値 0.017706", round(P1, 6), 0.017706)
# ★ scipy と独立に一致するか
approx("  scipy と一致", round(P1, 12),
       round(2 * float(1 - stats.norm.cdf(Z1)), 12))
eq("  0.0177 < 0.05 なので棄却", P1 < 0.05, True)
# ★ 片側にしてしまったときの値（Common error）
approx("  片側にすると半分の 0.00885", sf(P1 / 2, 3), 0.00885)
approx("  生の値 0.008853", round(P1 / 2, 6), 0.008853)

print("══════════ 例題2：t Test（片側・上側） ══════════")
D2 = [0.28, 0.31, 0.24, 0.33, 0.29, 0.27, 0.35, 0.26]
T2, XB2, S2, DF2 = tstat(D2, 0.25)
eq("データは 8 個", len(D2), 8)
eq("自由度 = 7", DF2, 7)
approx("xbar = 0.291 (3 s.f.)", sf(XB2), 0.291)
approx("  生の値 0.29125", round(XB2, 5), 0.29125)
approx("s = 0.0368 (3 s.f.)", sf(S2), 0.0368)
approx("  生の値 0.036815", round(S2, 6), 0.036815)
approx("t = 3.17 (3 s.f.)", sf(T2), 3.17)
approx("  生の値 3.16914", round(T2, 5), 3.16914)
P2 = float(1 - stats.t.cdf(T2, DF2))
approx("片側 p = 0.00786 (3 s.f.)", sf(P2), 0.00786)
approx("  生の値 0.0078633", round(P2, 7), 0.0078633)
# ★ scipy の ttest_1samp と突き合わせる（独立な実装）
R2 = stats.ttest_1samp(D2, 0.25, alternative="greater")
approx("  ttest_1samp と t が一致", round(float(R2.statistic), 10),
       round(T2, 10))
approx("  ttest_1samp と p が一致", round(float(R2.pvalue), 12),
       round(P2, 12))
eq("  棄却する", P2 < 0.05, True)
eq("  xbar は mu0 より大きい（H1 の向きと合う）", XB2 > 0.25, True)

print("══════════ 例題3：matched pairs（差は全部 負） ══════════")
BEF = [62, 58, 71, 55, 66, 60, 69, 57]
AFT = [59, 57, 66, 54, 61, 58, 64, 56]
DIFF = [a - b for a, b in zip(AFT, BEF)]
eq("差は [-3, -1, -5, -1, -5, -2, -5, -1]", DIFF,
   [-3, -1, -5, -1, -5, -2, -5, -1])
eq("  8 つとも負", all(d < 0 for d in DIFF), True)
T3, DB3, S3, DF3 = tstat(DIFF, 0.0)
eq("自由度 = 7", DF3, 7)
approx("dbar = -2.875", round(DB3, 6), -2.875)
approx("t = -4.31 (3 s.f.)", sf(T3), -4.31)
approx("  生の値 -4.31370", round(T3, 5), -4.31370)
P3 = float(1 - stats.t.cdf(T3, DF3))
approx("片側（上側）p = 0.998 (3 s.f.)", sf(P3), 0.998)
approx("  生の値 0.99825", round(P3, 5), 0.99825)
# ★ 「差をとって 1 標本」と ttest_rel が同じ答えになるか
R3 = stats.ttest_rel(AFT, BEF, alternative="greater")
approx("  ttest_rel と t が一致", round(float(R3.statistic), 10),
       round(T3, 10))
approx("  ttest_rel と p が一致", round(float(R3.pvalue), 12),
       round(P3, 12))
eq("  0.998 > 0.05 なので棄却しない", P3 > 0.05, True)
eq("  p が 0.5 より大きいのは、データが H1 と逆を向いている合図",
   P3 > 0.5 and DB3 < 0, True)

print("══════════ 例題4：binomial（上側） ══════════")
approx("p-value P(X >= 10 | B(20, 0.3)) = 0.0480",
       sf(btail_up(10, 20, 0.3), 3), 0.0480)
approx("  生の値 0.047962", round(btail_up(10, 20, 0.3), 6), 0.047962)
eq("  0.0480 < 0.05 なので棄却", btail_up(10, 20, 0.3) < 0.05, True)
# ★ 1 つずらしたときの値（Common error）
approx("  誤って P(X >= 11) にすると 0.0171",
       sf(btail_up(11, 20, 0.3), 3), 0.0171)
approx("  生の値 0.017145", round(btail_up(11, 20, 0.3), 6), 0.017145)
approx("  抜けるのは P(X = 10) = 0.0308", sf(bpdf(10, 20, 0.3), 3), 0.0308)
approx("  足すと元に戻る",
       round(btail_up(11, 20, 0.3) + bpdf(10, 20, 0.3), 12),
       round(btail_up(10, 20, 0.3), 12))
# ★ AHL 4.18a の critical region と一致するか
CRIT4 = [k for k in range(21) if btail_up(k, 20, 0.3) <= 0.05][0]
eq("  5% の critical region は X >= 10", CRIT4, 10)
approx("  P(X >= 9) = 0.113", sf(btail_up(9, 20, 0.3), 3), 0.113)
eq("  観測値 10 は critical region の中", 10 >= CRIT4, True)

print("══════════ 例題5：Poisson（上側） ══════════")
approx("p-value P(X >= 15 | Po(8)) = 0.0173", sf(ptail_up(15, 8.0), 3),
       0.0173)
approx("  生の値 0.017257", round(ptail_up(15, 8.0), 6), 0.017257)
eq("  棄却する", ptail_up(15, 8.0) < 0.05, True)
eq("  観測 15 は H0 の平均 8 より多い", 15 > 8, True)
# ★ Upper Bound を小さくとる誤り
approx("  Upper Bound を 20 にすると抜ける分がある",
       round(ptail_up(15, 8.0) - sum(ppdf(j, 8.0) for j in range(15, 21)), 8),
       round(sum(ppdf(j, 8.0) for j in range(21, 160)), 8))
eq("  その抜ける分は 0 ではない",
   sum(ppdf(j, 8.0) for j in range(21, 160)) > 0, True)

print("══════════ 例題6：rho = 0 の検定 ══════════")
X6 = [4, 7, 3, 9, 6, 5, 8, 4, 10, 7]
Y6 = [22, 26, 19, 31, 23, 27, 25, 20, 30, 24]
N6 = len(X6)
R6 = float(np.corrcoef(X6, Y6)[0, 1])
T6 = R6 * math.sqrt((N6 - 2) / (1 - R6 ** 2))
P6 = 2 * float(1 - stats.t.cdf(abs(T6), N6 - 2))
eq("データは 10 組", N6, 10)
eq("自由度 = n - 2 = 8", N6 - 2, 8)
approx("r = 0.864 (3 s.f.)", sf(R6), 0.864)
approx("  生の値 0.863684", round(R6, 6), 0.863684)
approx("t = 4.85 (3 s.f.)", sf(T6), 4.85)
approx("  生の値 4.84662", round(T6, 5), 4.84662)
approx("両側 p = 0.00128 (3 s.f.)", sf(P6), 0.00128)
approx("  生の値 0.0012772", round(P6, 7), 0.0012772)
# ★ linregress と突き合わせる（独立な実装）
LR6 = stats.linregress(X6, Y6)
approx("  linregress と r が一致", round(float(LR6.rvalue), 12),
       round(R6, 12))
approx("  linregress と p が一致", round(float(LR6.pvalue), 12),
       round(P6, 12))
eq("  0.00128 < 0.01 なので 1% でも棄却", P6 < 0.01, True)

print("══════════ 演習2：z Test（片側・上側） ══════════")
SE_E2 = 15 / math.sqrt(50)
approx("standard error = 2.12 (3 s.f.)", sf(SE_E2), 2.12)
Z_E2 = zstat(184.2, 180.0, 15.0, 50)
approx("z = 1.98 (3 s.f.)", sf(Z_E2), 1.98)
approx("  生の値 1.97990", round(Z_E2, 5), 1.97990)
P_E2 = 1 - ncdf(Z_E2)
approx("片側 p = 0.0239 (3 s.f.)", sf(P_E2), 0.0239)
approx("  生の値 0.023857", round(P_E2, 6), 0.023857)
eq("  棄却する", P_E2 < 0.05, True)
approx("  両側にすると 0.0477", sf(2 * P_E2, 3), 0.0477)
eq("  両側でも 0.05 は下回るので、この問題では結論は変わらない",
   2 * P_E2 < 0.05, True)

print("══════════ 演習3：t Test（両側） ══════════")
D_E3 = [512, 505, 498, 517, 509, 503, 515, 508, 511, 502]
T_E3, XB_E3, S_E3, DF_E3 = tstat(D_E3, 505.0)
eq("データは 10 個", len(D_E3), 10)
eq("自由度 = 9", DF_E3, 9)
approx("xbar = 508", round(XB_E3, 9), 508.0)
approx("s = 6.02 (3 s.f.)", sf(S_E3), 6.02)
approx("  生の値 6.018490", round(S_E3, 6), 6.018490)
approx("t = 1.58 (3 s.f.)", sf(T_E3), 1.58)
approx("  生の値 1.57628", round(T_E3, 5), 1.57628)
P_E3 = 2 * float(1 - stats.t.cdf(abs(T_E3), DF_E3))
approx("両側 p = 0.149 (3 s.f.)", sf(P_E3), 0.149)
approx("  生の値 0.149415", round(P_E3, 6), 0.149415)
eq("  0.149 > 0.05 なので棄却しない", P_E3 > 0.05, True)
approx("  ttest_1samp と一致",
       round(float(stats.ttest_1samp(D_E3, 505.0).pvalue), 12),
       round(P_E3, 12))

print("══════════ 演習4：matched pairs（差は全部 正） ══════════")
BEF4 = [24, 31, 28, 35, 22, 30, 27]
AFT4 = [27, 33, 29, 38, 26, 31, 30]
DIFF4 = [a - b for a, b in zip(AFT4, BEF4)]
eq("差は [3, 2, 1, 3, 4, 1, 3]", DIFF4, [3, 2, 1, 3, 4, 1, 3])
eq("  7 つとも正", all(d > 0 for d in DIFF4), True)
T4, DB4, S4, DF4 = tstat(DIFF4, 0.0)
eq("自由度 = 6", DF4, 6)
approx("dbar = 2.43 (3 s.f.)", sf(DB4), 2.43)
approx("  生の値 2.428571", round(DB4, 6), 2.428571)
approx("s_d = 1.13 (3 s.f.)", sf(S4), 1.13)
approx("  生の値 1.133893", round(S4, 6), 1.133893)
approx("t = 5.67 (3 s.f.)", sf(T4), 5.67)
approx("  生の値 5.66667", round(T4, 5), 5.66667)
P4 = float(1 - stats.t.cdf(T4, DF4))
approx("片側 p = 0.000650 (3 s.f.)", sf(P4), 0.000650)
approx("  生の値 0.00064952", round(P4, 8), 0.00064952)
eq("  1% でも棄却", P4 < 0.01, True)
approx("  ttest_rel と一致",
       round(float(stats.ttest_rel(AFT4, BEF4,
                                   alternative="greater").pvalue), 12),
       round(P4, 12))

print("══════════ 演習5〜6：離散 ══════════")
approx("演習5 P(X >= 10 | B(40, 0.15)) = 0.0672",
       sf(btail_up(10, 40, 0.15), 3), 0.0672)
approx("  生の値 0.067220", round(btail_up(10, 40, 0.15), 6), 0.067220)
eq("  0.0672 > 0.05 なので棄却しない", btail_up(10, 40, 0.15) > 0.05, True)
approx("  ★ 誤って P(X >= 11) にすると 0.0299",
       sf(btail_up(11, 40, 0.15), 3), 0.0299)
eq("  ★ それだと結論が逆になる", btail_up(11, 40, 0.15) < 0.05, True)
approx("  H0 のもとでの平均 = 6", 40 * 0.15, 6.0)

approx("演習6 P(X <= 1 | Po(3.5)) = 0.136", sf(ptail_lo(1, 3.5), 3), 0.136)
approx("  生の値 0.135888", round(ptail_lo(1, 3.5), 6), 0.135888)
eq("  0.136 > 0.05 なので棄却しない", ptail_lo(1, 3.5) > 0.05, True)
approx("  X = 0 でも 0.0302 で、やっと 0.05 を下回る",
       sf(ptail_lo(0, 3.5), 3), 0.0302)
eq("  その 0.0302 は 0.05 未満", ptail_lo(0, 3.5) < 0.05, True)
approx("  1 週間ぶんなら m = 24.5", 3.5 * 7, 24.5)

print("══════════ 演習7：rho（n = 8） ══════════")
X7 = [1, 2, 3, 4, 5, 6, 7, 8]
Y7 = [12, 15, 13, 18, 16, 20, 17, 22]
N7 = len(X7)
R7 = float(np.corrcoef(X7, Y7)[0, 1])
T7 = R7 * math.sqrt((N7 - 2) / (1 - R7 ** 2))
P7 = 2 * float(1 - stats.t.cdf(abs(T7), N7 - 2))
eq("自由度 = n - 2 = 6", N7 - 2, 6)
approx("r = 0.855 (3 s.f.)", sf(R7), 0.855)
approx("  生の値 0.854624", round(R7, 6), 0.854624)
approx("t = 4.03 (3 s.f.)", sf(T7), 4.03)
approx("  生の値 4.03159", round(T7, 5), 4.03159)
approx("両側 p = 0.00687 (3 s.f.)", sf(P7), 0.00687)
approx("  生の値 0.0068680", round(P7, 7), 0.0068680)
eq("  棄却する", P7 < 0.05, True)
approx("  linregress と一致",
       round(float(stats.linregress(X7, Y7).pvalue), 12), round(P7, 12))

print("══════════ 演習8：x_obs を含める ══════════")
approx("正しい P(X >= 12 | B(30, 0.25)) = 0.0507",
       sf(btail_up(12, 30, 0.25), 3), 0.0507)
approx("  生の値 0.050658", round(btail_up(12, 30, 0.25), 6), 0.050658)
approx("誤った P(X > 12) = 0.0216", sf(btail_up(13, 30, 0.25), 3), 0.0216)
approx("  生の値 0.021594", round(btail_up(13, 30, 0.25), 6), 0.021594)
approx("抜けた 1 本 P(X = 12) = 0.0291", sf(bpdf(12, 30, 0.25), 3), 0.0291)
approx("  足すと戻る 0.0216 + 0.0291 = 0.0507",
       round(btail_up(13, 30, 0.25) + bpdf(12, 30, 0.25), 12),
       round(btail_up(12, 30, 0.25), 12))
eq("★ 正しい値では棄却しない", btail_up(12, 30, 0.25) > 0.05, True)
eq("★ 誤った値では棄却してしまう", btail_up(13, 30, 0.25) < 0.05, True)
# ★ AHL 4.18a 演習4 の critical region と一致するか
CRIT8 = [k for k in range(31) if btail_up(k, 30, 0.25) <= 0.05][0]
eq("  4.18a 演習4 の critical region は X >= 13", CRIT8, 13)
eq("  観測値 12 は critical region の外", 12 >= CRIT8, False)

print("══════════ 演習9：区間を合わせる ══════════")
approx("4 時間ぶんの m = 10", 2.5 * 4, 10.0)
approx("P(X >= 18 | Po(10)) = 0.0143", sf(ptail_up(18, 10.0), 3), 0.0143)
approx("  生の値 0.014278", round(ptail_up(18, 10.0), 6), 0.014278)
eq("  棄却する", ptail_up(18, 10.0) < 0.05, True)
WRONG9 = ptail_up(18, 2.5)
approx("★ m = 2.5 のままだと 2.15e-10", sf(WRONG9, 3), 2.15e-10)
eq("  それは 1e-6 より小さい（合わせ忘れの合図）", WRONG9 < 1e-6, True)

print("══════════ 本文に、その数値が実際に書かれているか ══════════")
QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "ahl-4-18b.qmd")
TXT = open(QMD, encoding="utf-8").read()


def in_text(name, needle, want=True):
    global ok, ng
    good = (needle in TXT) == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else
           f"   ({'欠けている' if want else '残っている'}: {needle!r})"))
    ok, ng = ok + good, ng + (not good)


for lab, needle in [
        ("例題1 z", "2.37"), ("例題1 p", "0.0177"),
        ("例題1 片側にした値", "0.00885"),
        ("例題2 t", "3.17"), ("例題2 p", "0.00786"), ("例題2 s", "0.0368"),
        ("例題3 t", "-4.31"), ("例題3 p", "0.998"),
        ("例題4 p", "0.0480"), ("例題4 誤り", "0.0171"),
        ("例題5 p", "0.0173"),
        ("例題6 r", "0.864"), ("例題6 p", "0.00128"),
        ("演習2 z", "1.98"), ("演習2 p", "0.0239"),
        ("演習3 t", "1.58"), ("演習3 p", "0.149"),
        ("演習4 t", "5.67"), ("演習4 p", "0.000650"),
        ("演習5 p", "0.0672"), ("演習5 誤り", "0.0299"),
        ("演習6 p", "0.136"), ("演習6 X=0 の値", "0.0302"),
        ("演習7 r", "0.855"), ("演習7 p", "0.00687"),
        ("演習8 正しい値", "0.0507"), ("演習8 誤り", "0.0216"),
        ("演習8 抜けた 1 本", "0.0291"),
        ("演習9 m", "2.5 \\times 4 = 10"), ("演習9 p", "0.0143")]:
    in_text(lab, needle)

# ★ シラバスの引用
in_text("sigma 既知は normal という引用",
        "Use of the normal distribution when $\\sigma$ is known")
in_text("regardless of sample size の引用", "regardless of sample size")
in_text("matched pairs の引用",
        "The case of matched pairs is to be treated as an example of a "
        "single sample technique")
in_text("binomial で割合という引用",
        "Test for proportion using binomial distribution")
in_text("Poisson で平均という引用",
        "Test for population mean using Poisson distribution")
in_text("片側のみという引用",
        "Poisson and binomial tests will be **one-tailed only**")
in_text("rho = 0 の引用",
        "population product moment correlation coefficient")
in_text("データは与えられるという引用", "In examinations the data will be given")
# ★ GDC（ユーザーの実機画面で確認したもの）
in_text("メニューは Statistics → Stat Tests", "menu → Statistics → Stat Tests")
in_text("  Probability → が残っていない", "Probability → Distributions",
        want=False)
in_text("Linear Reg t Test がある", "Linear Reg t Test")
in_text("1-Prop z Test への注意がある", "1-Prop z Test")
in_text("Paired t Test は無いと書いてある", "`Paired t Test` はありません")
# ★ 教える上での要点
in_text("x_obs を含めると書いてある", "含めます")
in_text("sigma で決めると書いてある", "$\\sigma$ で")
# ★ 参考資料で確認した、追加すべき内容が入っているか
in_text("paired は【差】が正規分布と書いてある",
        "the differences are normally distributed")
in_text("  母集団の正規性は不要と書いてある", "もとの $2$ つの母集団が正規分布かどうかは、問われません")
in_text("個数が同じ＝ペアではない、と書いてある", "個数が同じでも、ペアでないことがあります")
in_text("2-Sample z Test に触れている", "2-Sample z Test")
in_text("rho の片側（positive / negative）に触れている",
        "positive linear correlation")
in_text("r の critical value を与えられる形式に触れている", "$0.632$")
in_text("  |r| は両側限定と書いてある", "絶対値を使うのは、両側のときだけ")
in_text("  片側の比べ方の表がある", "{#tbl-ahl418b-rcrit}")
in_text("  この例は両側だと書いてある", "@exm-ahl418b-rho は**両側**なので")
# ★ 母平均の検定は「正規母集団」が前提
in_text("正規母集団が前提だと書いてある",
        "第2節と第3節は、「母集団が正規分布」が前提です")
in_text("  シラバスの normal distribution を引いている",
        "`Test for population mean for normal distribution`")
in_text("  選び分け表に正規母集団と書いてある", "**正規母集団**の母平均")
in_text("sample variance の変換式がある", "s_{n-1}^2 = \\frac{n}{n-1}")


# ★ code span の中に数式や markdown が入っていないか（レンダリングが壊れる）
import re as _re
_bad = [m for m in _re.findall(r"`[^`\n]+`", TXT)
        if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", _bad, [])
# ★ 開き fence の直前が空行か（空行が無いと div にならず、literal で出る）
_L = TXT.split("\n")
_nb = [i + 1 for i, l in enumerate(_L)
       if _re.match(r"^:{3,} *\{", l) and i > 0
       and _L[i - 1].strip() != "" and not _L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", _nb, [])

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
