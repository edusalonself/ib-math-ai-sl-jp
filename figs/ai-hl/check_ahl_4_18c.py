"""AHL 4.18c（Type I / Type II error）の数値をぜんぶ検算する。
   実行: python3 figs/ai-hl/check_ahl_4_18c.py

   方針:
     (1) alpha は【H0 の分布】、beta は【本当の値の分布】で別々に計算する
     (2) 「beta != 1 - alpha」を、すべての例で明示的に確かめる
     (3) critical region は総当たりで探す（公式を仮定しない）
     (4) alpha を下げると beta が上がることを、単調性として確かめる
     (5) 最後に .qmd を読んで、本文にその数値が書かれているかを確かめる
"""
import math
import os

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


def ncdf(x, mu=0.0, sd=1.0):
    mine = 0.5 * (1 + math.erf((x - mu) / (sd * math.sqrt(2))))
    theirs = float(stats.norm.cdf(x, mu, sd))
    assert abs(mine - theirs) < 1e-13, f"ncdf が食い違う {mine} {theirs}"
    return mine


def zcrit(area_right):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 1 - ncdf(mid) > area_right:
            lo = mid
        else:
            hi = mid
    mine = (lo + hi) / 2
    assert abs(mine - float(stats.norm.ppf(1 - area_right))) < 1e-9
    return mine


def bpdf(k, n, p):
    mine = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    assert abs(mine - float(stats.binom.pmf(k, n, p))) < 1e-13
    return mine


def ppdf(k, m):
    mine = math.exp(-m) * m ** k / math.factorial(k)
    assert abs(mine - float(stats.poisson.pmf(k, m))) < 1e-13
    return mine


def btail_up(k, n, p):
    return sum(bpdf(j, n, p) for j in range(k, n + 1))


def btail_lo(k, n, p):
    return sum(bpdf(j, n, p) for j in range(0, k + 1))


def ptail_up(k, m, top=160):
    return sum(ppdf(j, m) for j in range(k, top))


def ptail_lo(k, m):
    return sum(ppdf(j, m) for j in range(0, k + 1))


def crit_binom_up(n, p, alpha):
    for k in range(0, n + 1):
        if btail_up(k, n, p) <= alpha:
            return k
    return None


def crit_pois_up(m, alpha, top=160):
    for k in range(0, top):
        if ptail_up(k, m) <= alpha:
            return k
    return None


# ★ 2 つの誤りを、必ず【別々の分布から】出す関数にしておく
def errors_binom(n, p0, p_true, k):
    """critical region X >= k のときの (alpha, beta)。"""
    alpha = btail_up(k, n, p0)          # H0 の分布、region の中
    beta = btail_lo(k - 1, n, p_true)   # 本当の値の分布、region の外
    return alpha, beta


def errors_pois(m0, m_true, k):
    alpha = ptail_up(k, m0)
    beta = ptail_lo(k - 1, m_true)
    return alpha, beta


def errors_normal_upper(mu0, mu_true, se, level):
    crit = mu0 + zcrit(level) * se
    alpha = 1 - ncdf(crit, mu0, se)
    beta = ncdf(crit, mu_true, se)
    return crit, alpha, beta


print("══════════ 例題1：binomial（コイン） ══════════")
eq("B(20, 0.5)、5% の critical region は X >= 15",
   crit_binom_up(20, 0.5, 0.05), 15)
approx("  P(X >= 14) = 0.0577", sf(btail_up(14, 20, 0.5), 3), 0.0577)
approx("  生の値 0.057659", round(btail_up(14, 20, 0.5), 6), 0.057659)
eq("  X >= 14 は 5% を超える", btail_up(14, 20, 0.5) > 0.05, True)
A1, B1 = errors_binom(20, 0.5, 0.8, 15)
approx("P(Type I) = 0.0207", sf(A1, 3), 0.0207)
approx("  生の値 0.020695", round(A1, 6), 0.020695)
eq("  ★ 0.05 ではない（離散だから）", abs(A1 - 0.05) > 1e-3, True)
approx("P(Type II | p = 0.8) = 0.196", sf(B1, 3), 0.196)
approx("  生の値 0.195792", round(B1, 6), 0.195792)
eq("★ alpha + beta は 1 にならない", abs(A1 + B1 - 1.0) > 0.5, True)
approx("  足すと 0.216（丸めた値どうしなら 0.217）", sf(A1 + B1, 3), 0.216)
# ★ beta は「本当の値の分布」で出したか（H0 の分布で出すと別の値になる）
approx("  もし p = 0.5 のまま出したら 0.979（誤り）",
       sf(btail_lo(14, 20, 0.5), 3), 0.979)
eq("  それは正しい beta とは違う", abs(btail_lo(14, 20, 0.5) - B1) > 0.5, True)

print("══════════ 例題2：Poisson（交差点の事故） ══════════")
eq("Po(3)、5% の critical region は X >= 7", crit_pois_up(3.0, 0.05), 7)
approx("  P(X >= 6) = 0.0839", sf(ptail_up(6, 3.0), 3), 0.0839)
approx("  生の値 0.083918", round(ptail_up(6, 3.0), 6), 0.083918)
A2, B2 = errors_pois(3.0, 5.0, 7)
approx("P(Type I) = 0.0335", sf(A2, 3), 0.0335)
approx("  生の値 0.033509", round(A2, 6), 0.033509)
approx("P(Type II | m = 5) = 0.762", sf(B2, 3), 0.762)
approx("  生の値 0.762183", round(B2, 6), 0.762183)
eq("★ beta が大きい（1 か月では見分けにくい）", B2 > 0.7, True)
eq("  alpha + beta は 1 にならない", abs(A2 + B2 - 1.0) > 0.1, True)
# ★ 3 か月ぶんにすると beta は小さくなるはず
K3 = crit_pois_up(9.0, 0.05)
_, B2B = errors_pois(9.0, 15.0, K3)
eq("  3 か月ぶん（Po(9) vs Po(15)）なら beta は小さくなる", B2B < B2, True)

print("══════════ 例題3：normal（砂糖の袋） ══════════")
SE3 = 15 / math.sqrt(25)
approx("standard error = 3", SE3, 3.0)
C3, A3, B3 = errors_normal_upper(100.0, 106.0, SE3, 0.05)
approx("critical value = 104.9 (3 s.f.)", sf(C3, 4), 104.9)
approx("  生の値 104.93456", round(C3, 5), 104.93456)
approx("P(Type I) = 0.05（連続なのでちょうど）", round(A3, 10), 0.05, 1e-9)
approx("P(Type II | mu = 106) = 0.361", sf(B3, 3), 0.361)
approx("  生の値 0.361240", round(B3, 6), 0.361240)
eq("★ beta != 1 - alpha", abs(B3 - (1 - A3)) > 0.5, True)
approx("  1 - alpha は 0.95", round(1 - A3, 10), 0.95, 1e-9)
approx("  power = 1 - beta = 0.639", sf(1 - B3, 3), 0.639)
# (d) 1% にすると
C3B, A3B, B3B = errors_normal_upper(100.0, 106.0, SE3, 0.01)
approx("1% の critical value = 107 (3 s.f.)", sf(C3B, 3), 107.0)
approx("  生の値 106.97904", round(C3B, 5), 106.97904)
approx("1% での P(Type II) = 0.628", sf(B3B, 3), 0.628)
approx("  生の値 0.627919", round(B3B, 6), 0.627919)
eq("★ alpha を下げたら beta は上がった", B3B > B3, True)
# ★ 10% も足して、単調性を確かめる
C3C, A3C, B3C = errors_normal_upper(100.0, 106.0, SE3, 0.10)
approx("10% の critical value = 103.8 (3 s.f.)", sf(C3C, 4), 103.8)
approx("10% での P(Type II) = 0.236", sf(B3C, 3), 0.236)
eq("★ 10% < 5% < 1% の順で beta は単調に増える",
   B3C < B3 < B3B, True)
# ★ GDC の注意（se ではなく sigma を入れる誤り）
approx("  sigma = 15 を入れてしまうと 0.472",
       sf(ncdf(C3, 106.0, 15.0), 3), 0.472)
# ★ Why it works の 2 つの値
approx("  mu = 101 なら beta = 0.905", sf(ncdf(C3, 101.0, SE3), 3), 0.905)
approx("  mu = 110 なら beta = 0.0457", sf(ncdf(C3, 110.0, SE3), 3), 0.0457)
eq("  H0 から遠いほど beta は小さい",
   ncdf(C3, 110.0, SE3) < ncdf(C3, 101.0, SE3), True)

print("══════════ 演習1：binomial ══════════")
A_E1, B_E1 = errors_binom(25, 0.4, 0.6, 15)
approx("P(Type I) = 0.0344", sf(A_E1, 3), 0.0344)
approx("  生の値 0.034392", round(A_E1, 6), 0.034392)
approx("P(Type II | p = 0.6) = 0.414", sf(B_E1, 3), 0.414)
approx("  生の値 0.414225", round(B_E1, 6), 0.414225)
approx("  足すと 0.449（丸めた値どうしなら 0.448）", sf(A_E1 + B_E1, 3), 0.449)
eq("  1 にはならない", abs(A_E1 + B_E1 - 1.0) > 0.4, True)
eq("  4.18a 例題3 と同じ critical region", crit_binom_up(25, 0.4, 0.05), 15)

print("══════════ 演習2：Poisson ══════════")
A_E2, B_E2 = errors_pois(6.0, 10.0, 11)
approx("P(Type I) = 0.0426", sf(A_E2, 3), 0.0426)
approx("  生の値 0.042621", round(A_E2, 6), 0.042621)
approx("P(Type II | m = 10) = 0.583", sf(B_E2, 3), 0.583)
approx("  生の値 0.583040", round(B_E2, 6), 0.583040)
eq("  4.18a 例題4 と同じ critical region", crit_pois_up(6.0, 0.05), 11)
eq("  Upper Bound は 10（region の下端 11 から 1 引いた数）", 11 - 1, 10)

print("══════════ 演習3：normal ══════════")
SE_E3 = 6 / math.sqrt(36)
approx("standard error = 1", SE_E3, 1.0)
C_E3, A_E3, B_E3 = errors_normal_upper(50.0, 52.0, SE_E3, 0.05)
approx("critical value = 51.6 (3 s.f.)", sf(C_E3, 3), 51.6)
approx("  生の値 51.64485", round(C_E3, 5), 51.64485)
approx("P(Type I) = 0.05", round(A_E3, 10), 0.05, 1e-9)
approx("P(Type II | mu = 52) = 0.361", sf(B_E3, 3), 0.361)
# ★ 丸めた critical value を使うと、どうずれるか
approx("  丸めた 51.6 で計算すると 0.345", sf(ncdf(51.6, 52.0, SE_E3), 3),
       0.345)
eq("★ 丸めると 2 桁目からずれる",
   abs(ncdf(51.6, 52.0, SE_E3) - B_E3) > 0.01, True)
# ★ 例題3 と beta が一致する理由（標準誤差 2 個ぶんで同じ）
approx("  例題3 と同じ beta（どちらも se 2 個ぶん離れている）",
       round(B_E3, 9), round(B3, 9))
approx("  例題3：(106 - 100) / 3 = 2", (106 - 100) / SE3, 2.0)
approx("  演習3：(52 - 50) / 1 = 2", (52 - 50) / SE_E3, 2.0)

print("══════════ 演習6：trade-off ══════════")
SE_E6 = 10 / math.sqrt(25)
approx("standard error = 2", SE_E6, 2.0)
C6A, _, B6A = errors_normal_upper(200.0, 205.0, SE_E6, 0.05)
C6B, _, B6B = errors_normal_upper(200.0, 205.0, SE_E6, 0.01)
approx("5% の critical value = 203.3 (3 s.f.)", sf(C6A, 4), 203.3)
approx("  生の値 203.28971", round(C6A, 5), 203.28971)
approx("5% での beta = 0.196", sf(B6A, 3), 0.196)
approx("  生の値 0.196235", round(B6A, 6), 0.196235)
approx("1% の critical value = 204.7 (3 s.f.)", sf(C6B, 4), 204.7)
approx("  生の値 204.65270", round(C6B, 5), 204.65270)
approx("1% での beta = 0.431", sf(B6B, 3), 0.431)
approx("  生の値 0.431069", round(B6B, 6), 0.431069)
eq("★ beta は 2 倍以上に増える", B6B > 2 * B6A, True)

print("══════════ 演習7：本当の値が遠いほど beta は小さい ══════════")
eq("Po(4)、critical region X >= 9 のときの alpha", crit_pois_up(4.0, 0.05), 9)
BS = []
for m, want in ((6.0, 0.847), (8.0, 0.593), (10.0, 0.333)):
    _, bb = errors_pois(4.0, m, 9)
    approx(f"P(Type II | m = {m:g}) = {want}", sf(bb, 3), want)
    BS.append(bb)
approx("  m = 6 の生の値 0.847237", round(BS[0], 6), 0.847237)
approx("  m = 8 の生の値 0.592547", round(BS[1], 6), 0.592547)
approx("  m = 10 の生の値 0.332820", round(BS[2], 6), 0.332820)
eq("★ 単調に減っている", BS[0] > BS[1] > BS[2], True)
eq("  Upper Bound は 3 回とも 8", 9 - 1, 8)

print("══════════ 演習8：離散の alpha は 0.05 にならない ══════════")
eq("B(30, 0.25)、5% の critical region は X >= 13",
   crit_binom_up(30, 0.25, 0.05), 13)
approx("  P(X >= 12) = 0.0507", sf(btail_up(12, 30, 0.25), 3), 0.0507)
approx("  生の値 0.050658", round(btail_up(12, 30, 0.25), 6), 0.050658)
eq("  ★ 0.05 をわずかに超える", btail_up(12, 30, 0.25) > 0.05, True)
A_E8, B_E8 = errors_binom(30, 0.25, 0.5, 13)
approx("P(Type I) = 0.0216", sf(A_E8, 3), 0.0216)
approx("  生の値 0.021594", round(A_E8, 6), 0.021594)
eq("  0.05 の半分以下", A_E8 < 0.025, True)
approx("P(Type II | p = 0.5) = 0.181", sf(B_E8, 3), 0.181)
approx("  生の値 0.180797", round(B_E8, 6), 0.180797)
approx("  H0 の平均 = 7.5", 30 * 0.25, 7.5)
approx("  本当の値の平均 = 15", 30 * 0.5, 15.0)
eq("  15 は critical region（X >= 13）の中なので beta は小さめ",
   15 >= 13 and B_E8 < 0.25, True)

print("══════════ 演習10：下側の検定 ══════════")
SE_E10 = 2 / math.sqrt(16)
approx("standard error = 0.5", SE_E10, 0.5)
C_E10 = 25 - zcrit(0.05) * SE_E10
approx("critical value = 24.2 (3 s.f.)", sf(C_E10, 3), 24.2)
approx("  生の値 24.17757", round(C_E10, 5), 24.17757)
approx("  P(Xbar < crit | mu = 25) = 0.05",
       round(ncdf(C_E10, 25.0, SE_E10), 10), 0.05, 1e-9)
# ★ 下側なので、region の外は「上」
B_E10 = 1 - ncdf(C_E10, 23.5, SE_E10)
approx("P(Type II | mu = 23.5) = 0.0877", sf(B_E10, 3), 0.0877)
approx("  生の値 0.087685", round(B_E10, 6), 0.087685)
eq("★ 向きを取り違えると 0.912 になる",
   sf(ncdf(C_E10, 23.5, SE_E10), 3), 0.912)
eq("  本当の平均 23.5 は critical region の中", 23.5 < C_E10, True)

print("══════════ 標本を大きくすると両方減る ══════════")
for n_big in (36, 64, 100):
    se = 2 / math.sqrt(n_big)
    c = 25 - zcrit(0.05) * se
    bb = 1 - ncdf(c, 23.5, se)
    print(f"    n = {n_big}: se = {se:.4f}, beta = {bb:.6f}")
BETAS = []
for n_big in (16, 36, 64, 100):
    se = 2 / math.sqrt(n_big)
    c = 25 - zcrit(0.05) * se
    BETAS.append(1 - ncdf(c, 23.5, se))
eq("★ n を増やすと（alpha は 0.05 のまま）beta は単調に減る",
   all(BETAS[i] > BETAS[i + 1] for i in range(len(BETAS) - 1)), True)

print("══════════ 本文に、その数値が実際に書かれているか ══════════")
QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "ahl-4-18c.qmd")
TXT = open(QMD, encoding="utf-8").read()


def in_text(name, needle, want=True):
    global ok, ng
    good = (needle in TXT) == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else
           f"   ({'欠けている' if want else '残っている'}: {needle!r})"))
    ok, ng = ok + good, ng + (not good)


for lab, needle in [
        ("例題1 alpha", "0.0207"), ("例題1 beta", "0.196"),
        ("例題1 P(X>=14)", "0.0577"),
        ("例題2 alpha", "0.0335"), ("例題2 beta", "0.762"),
        ("例題2 P(X>=6)", "0.0839"),
        ("例題3 crit", "104.9"), ("例題3 beta", "0.361"),
        ("例題3 1% crit", "107.0"), ("例題3 1% beta", "0.628"),
        ("trade-off 10%", "103.8"), ("trade-off 10% beta", "0.236"),
        ("演習1 alpha", "0.0344"), ("演習1 beta", "0.414"),
        ("演習2 alpha", "0.0426"), ("演習2 beta", "0.583"),
        ("演習3 crit", "51.6"),
        ("演習6 5% crit", "203.3"), ("演習6 5% beta", "0.196"),
        ("演習6 1% crit", "204.7"), ("演習6 1% beta", "0.431"),
        ("演習7 m=6", "0.847"), ("演習7 m=8", "0.593"),
        ("演習7 m=10", "0.333"),
        ("演習8 P(X>=12)", "0.0507"), ("演習8 alpha", "0.0216"),
        ("演習8 beta", "0.181"),
        ("演習10 crit", "24.2"), ("演習10 beta", "0.0877"),
        ("power の値", "0.639"),
        ("Why it works の 0.905", "0.905"),
        ("Why it works の 0.0457", "0.0457"),
        ("GDC の誤りの値 0.472", "0.472"),
        ("演習3 の丸め誤差 0.345", "0.345")]:
    in_text(lab, needle)

# ★ シラバスの引用
in_text("適用範囲の引用",
        "Applied to normal with known variance, Poisson and binomial "
        "distributions")
in_text("離散は片側のみの引用",
        "critical regions will only be required for one-tailed tests")
# ★ 教える上での要点
in_text("beta != 1 - alpha を書いている", "$\\beta = 1 - \\alpha$ では、ありません")
in_text("本当の値が要ると書いている", "具体的な値")
in_text("離散では alpha ちょうどにならないと書いている",
        "$\\alpha$ ちょうどにはなりません")
in_text("alpha を下げると beta が上がると書いている",
        "$\\alpha$ を小さくすると、$\\beta$ は大きくなります")
in_text("標本を大きくすれば両方減ると書いている", "標本を大きくすること")
# ★ GDC（ユーザーの実機画面で確認したもの）
in_text("  Probability → Distributions が残っていない",
        "Probability → Distributions", want=False)
in_text("Normal Cdf を使うと書いてある", "Normal Cdf")

# ★ 確率の中に書いた境目が、丸める前の値になっているか
#   （丸めた値を書くと、その値では答えが出ない — 前回これを見落とした）
for lab, bound, mu, se, want in [
        ("例題3 (c)", 104.9346, 106.0, 3.0, 0.361),
        ("例題3 (d)", 106.9790, 106.0, 3.0, 0.628),
        ("演習3 (c)", 51.6449, 52.0, 1.0, 0.361),
        ("演習6 (a)", 203.2897, 205.0, 2.0, 0.196),
        ("演習6 (b)", 204.6527, 205.0, 2.0, 0.431)]:
    approx(f"{lab} 本文の境目 {bound} で計算すると {want}",
           sf(ncdf(bound, mu, se), 3), want)
    in_text(f"  本文に {bound} と書いてある", str(bound))
approx("演習10 本文の境目 24.1776 で計算すると 0.0877",
       sf(1 - ncdf(24.1776, 23.5, 0.5), 3), 0.0877)
in_text("  本文に 24.1776 と書いてある", "24.1776")
# ★ 丸めた値を確率の中に書いていないか
for bad in ("P(\\bar{X} < 104.9)", "P(\\bar{X} < 104.9 \\mid",
            "P(\\bar{X} < 107.0)", "P(\\bar{X} < 107.0 \\mid",
            "P(\\bar{X} < 51.6)", "P(\\bar{X} < 203.3 \\mid",
            "P(\\bar{X} < 204.7 \\mid", "P(\\bar{X} > 24.2)"):
    in_text(f"  丸めた境目 {bad} が残っていない", bad, want=False)
# ★ 演習10(d)：n を増やしても alpha は 0.05 のまま、という事実と本文が合っているか
in_text("演習10(d) が「同じ有意水準なら beta が下がる」と書いている",
        "At the same significance level the probability of a Type II error "
        "becomes much smaller")
in_text("  誤った「有意水準を変えずに両方下がる」が残っていない",
        "without changing the significance level", want=False)
in_text("§7 が「中心は動きません」と書いている", "中心は動きませんが")
# ★ stated / actual significance level の区別
in_text("2 つの significance level を区別している",
        "stated significance level")
in_text("  actual significance level もある", "actual significance level")
in_text("  連続分布では一致すると書いてある",
        "P(\\text{Type I}) = \\alpha \\quad (\\text{連続分布})")
in_text("  離散分布では alpha 以下と書いてある",
        "P(\\text{Type I}) \\leq \\alpha \\quad (\\text{離散分布})")
in_text("できるようになること が一般化しすぎていない",
        "連続分布では設定した $\\alpha$ に等しく、離散分布では一般に $\\alpha$ 以下")
in_text("  表が P(Type I) = alpha と決めつけていない",
        "| $P(\\text{Type I}) = \\alpha$ | **$H_0$ の値**で作った分布", want=False)
# ★ 4.18a と同じく、正規分布では未丸めの境目を使う
in_text("未丸めの境目を使うと書いてある", "丸める前の値を使ってください")
# ★ 検定のあとに起こりえる誤り（参考資料で確認した出題型）
in_text("検定後にどちらが起こりえたか、の節がある", "{#after}")
in_text("  reject したら Type I と書いてある",
        "$H_0$ を **reject した** | **Type I**")
in_text("  reject しなかったら Type II と書いてある",
        "$H_0$ を **reject しなかった** | **Type II**")
in_text("false positive / false negative がある", "false positive")
in_text("  false negative もある", "false negative")
in_text("演習4 に (d) がある", "which type of error could have occurred")

# ★ code span の中に数式や markdown が入っていないか
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
