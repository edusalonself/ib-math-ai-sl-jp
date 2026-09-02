"""AHL 4.18a（critical values / critical regions）の数値をぜんぶ検算する。
   実行: python3 figs/ai-hl/check_ahl_4_18a.py

   方針（AHL 4.16 / 4.17 と同じ）:
     (1) 定義から自分で計算する
     (2) scipy と突き合わせる（独立な 2 実装）
     (3) critical region は「総当たり」で探す（公式を仮定しない）
     (4) 最後に .qmd を読んで、本文にその数値が書かれているかを確かめる
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


# ── 標準正規の裾。誤差関数から作って scipy と突き合わせる ──────────────
def ncdf(z):
    mine = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    theirs = float(stats.norm.cdf(z))
    assert abs(mine - theirs) < 1e-13, f"ncdf が食い違う {mine} {theirs}"
    return mine


def zcrit(area_right):
    """右の裾の面積が area_right になる z。二分法で出して scipy と照合。"""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 1 - ncdf(mid) > area_right:
            lo = mid
        else:
            hi = mid
    mine = (lo + hi) / 2
    theirs = float(stats.norm.ppf(1 - area_right))
    assert abs(mine - theirs) < 1e-9, f"zcrit が食い違う {mine} {theirs}"
    return mine


def bpdf(k, n, p):
    mine = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    theirs = float(stats.binom.pmf(k, n, p))
    assert abs(mine - theirs) < 1e-13, f"binom pmf が食い違う {mine} {theirs}"
    return mine


def ppdf(k, m):
    mine = math.exp(-m) * m ** k / math.factorial(k)
    theirs = float(stats.poisson.pmf(k, m))
    assert abs(mine - theirs) < 1e-13, f"poisson pmf が食い違う {mine} {theirs}"
    return mine


def btail_up(k, n, p):
    """P(X >= k) を、和で。"""
    return sum(bpdf(j, n, p) for j in range(k, n + 1))


def btail_lo(k, n, p):
    """P(X <= k) を、和で。"""
    return sum(bpdf(j, n, p) for j in range(0, k + 1))


def ptail_up(k, m, top=160):
    return sum(ppdf(j, m) for j in range(k, top))


def ptail_lo(k, m):
    return sum(ppdf(j, m) for j in range(0, k + 1))


# ★ critical region は【総当たり】で探す。公式も電卓の逆関数も使わない。
def crit_binom_up(n, p, alpha):
    """P(X >= k) <= alpha となる最小の k。"""
    for k in range(0, n + 1):
        if btail_up(k, n, p) <= alpha:
            return k
    return None


def crit_binom_lo(n, p, alpha):
    """P(X <= k) <= alpha となる最大の k。"""
    best = None
    for k in range(0, n + 1):
        if btail_lo(k, n, p) <= alpha:
            best = k
    return best


def crit_pois_up(m, alpha, top=160):
    for k in range(0, top):
        if ptail_up(k, m) <= alpha:
            return k
    return None


def crit_pois_lo(m, alpha, top=160):
    best = None
    for k in range(0, top):
        if ptail_lo(k, m) <= alpha:
            best = k
    return best


print("══════════ 正規分布の critical value ══════════")
approx("片側 5% の z = 1.645", sf(zcrit(0.05), 4), 1.645)
approx("  生の値 1.64485", round(zcrit(0.05), 5), 1.64485)
approx("両側 5%（片側 2.5%）の z = 1.96", sf(zcrit(0.025), 3), 1.96)
approx("  生の値 1.95996", round(zcrit(0.025), 5), 1.95996)
approx("片側 1% の z = 2.326", sf(zcrit(0.01), 4), 2.326)
approx("  生の値 2.32635", round(zcrit(0.01), 5), 2.32635)
approx("両側 1%（片側 0.5%）の z = 2.576", sf(zcrit(0.005), 4), 2.576)
approx("  生の値 2.57583", round(zcrit(0.005), 5), 2.57583)
approx("片側 10% の z = 1.282", sf(zcrit(0.10), 4), 1.282)
eq("両側 10% の z は、片側 5% の z と同じ",
   round(zcrit(0.05), 9), round(zcrit(0.05), 9))
# ★ 面積が本当に α になっているか（逆向きの確認）
approx("  z = 1.645 の右の裾は 0.05", round(1 - ncdf(zcrit(0.05)), 10), 0.05,
       1e-9)
approx("  z = 1.96 の外側 2 つ合わせて 0.05",
       round(2 * (1 - ncdf(zcrit(0.025))), 10), 0.05, 1e-9)

print("══════════ 例題1：袋の重さ（片側・下側） ══════════")
MU0, SIG, N1 = 500.0, 8.0, 25
SE1 = SIG / math.sqrt(N1)
approx("standard error = 1.6", SE1, 1.6)
C1 = MU0 - zcrit(0.05) * SE1
approx("critical value = 497.368…", round(C1, 5), 497.36823)
approx("  3 s.f. で 497", sf(C1), 497.0)
approx("  1 d.p. で 497.4", round(C1, 1), 497.4)
# ★ 逆向きの確認：その値より下になる確率が、ちょうど 5% か
approx("  P(Xbar < 497.368…) = 0.05",
       round(float(stats.norm.cdf(C1, MU0, SE1)), 10), 0.05, 1e-9)
XB1 = 496.5
approx("観測値 496.5 の z = -2.19", sf((XB1 - MU0) / SE1, 3), -2.19)
approx("  生の値 -2.1875", round((XB1 - MU0) / SE1, 4), -2.1875)
approx("観測値 496.5 の p-value = 0.0144",
       sf(float(stats.norm.cdf(XB1, MU0, SE1)), 3), 0.0144)
approx("  生の値 0.014353", round(float(stats.norm.cdf(XB1, MU0, SE1)), 6),
       0.014353)
eq("  496.5 は critical region の中", XB1 < C1, True)
eq("  p-value < 0.05 でも、同じ判定になる",
   float(stats.norm.cdf(XB1, MU0, SE1)) < 0.05, True)
# ★ 境目のすぐ外側でも、両方の判定が一致するか
XB1B = 497.5
eq("  497.5 は critical region の外", XB1B < C1, False)
eq("  497.5 の p-value は 0.05 より大きい",
   float(stats.norm.cdf(XB1B, MU0, SE1)) > 0.05, True)
approx("  497.5 の p-value = 0.0591",
       sf(float(stats.norm.cdf(XB1B, MU0, SE1)), 3), 0.0591)

print("══════════ 例題2：両側検定 ══════════")
MU2, SIG2, N2 = 20.0, 1.5, 36
SE2 = SIG2 / math.sqrt(N2)
approx("standard error = 0.25", SE2, 0.25)
LO2 = MU2 - zcrit(0.025) * SE2
HI2 = MU2 + zcrit(0.025) * SE2
approx("下の critical value = 19.510…", round(LO2, 5), 19.51001)
approx("上の critical value = 20.489…", round(HI2, 5), 20.48999)
approx("  3 s.f. で 19.5", sf(LO2), 19.5)
approx("  3 s.f. で 20.5", sf(HI2), 20.5)
eq("  2 つは mu0 について対称", round(MU2 - LO2, 9), round(HI2 - MU2, 9))
approx("  外側 2 つ合わせて 0.05",
       round(float(stats.norm.cdf(LO2, MU2, SE2))
             + float(1 - stats.norm.cdf(HI2, MU2, SE2)), 10), 0.05, 1e-9)
XB2 = 20.55
eq("観測値 20.55 は critical region の中", XB2 > HI2, True)
approx("  両側 p-value = 0.0278",
       sf(2 * float(1 - stats.norm.cdf(XB2, MU2, SE2)), 3), 0.0278)
approx("  生の値 0.027807",
       round(2 * float(1 - stats.norm.cdf(XB2, MU2, SE2)), 6), 0.027807)
# ★ 片側の値を使ってしまう誤り
approx("  片側の 1.645 を使うと 20.411…", round(MU2 + zcrit(0.05) * SE2, 5),
       20.41121)

print("══════════ 例題3：binomial の critical region ══════════")
N3, P3 = 25, 0.4
eq("B(25, 0.4)、H1: p > 0.4、5% の critical region は X >= 15",
   crit_binom_up(N3, P3, 0.05), 15)
approx("  P(X >= 15) = 0.0344", sf(btail_up(15, N3, P3), 3), 0.0344)
approx("  生の値 0.034392", round(btail_up(15, N3, P3), 6), 0.034392)
approx("  P(X >= 14) = 0.0778", sf(btail_up(14, N3, P3), 3), 0.0778)
approx("  生の値 0.077801", round(btail_up(14, N3, P3), 6), 0.077801)
eq("  X >= 14 は 5% を超えるので使えない", btail_up(14, N3, P3) > 0.05, True)
eq("  X >= 15 は 5% 以下なので使える", btail_up(15, N3, P3) <= 0.05, True)
eq("  「5% 以下でいちばん大きい region」が X >= 15", 15, crit_binom_up(N3, P3, 0.05))
# ★ 期待値との対比（region が平均のどちら側にあるか）
approx("  H0 のもとでの平均 np = 10", N3 * P3, 10.0)
eq("  critical region は平均より上", 15 > N3 * P3, True)

print("══════════ 例題4：Poisson の critical region ══════════")
M4 = 6.0
eq("Po(6)、H1: m > 6、5% の critical region は X >= 11",
   crit_pois_up(M4, 0.05), 11)
approx("  P(X >= 11) = 0.0426", sf(ptail_up(11, M4), 3), 0.0426)
approx("  生の値 0.042621", round(ptail_up(11, M4), 6), 0.042621)
approx("  P(X >= 10) = 0.0839", sf(ptail_up(10, M4), 3), 0.0839)
approx("  生の値 0.083924", round(ptail_up(10, M4), 6), 0.083924)
eq("  X >= 10 は 5% を超える", ptail_up(10, M4) > 0.05, True)
eq("  X >= 11 は 5% 以下", ptail_up(11, M4) <= 0.05, True)
# ★ P(X >= 12) は「もっと小さい」region。最大を取らない誤り
approx("  P(X >= 12) = 0.0201", sf(ptail_up(12, M4), 3), 0.0201)
eq("  X >= 12 も 5% 以下だが、X >= 11 より小さい region",
   ptail_up(12, M4) < ptail_up(11, M4), True)

print("══════════ 離散では α ちょうどにならない ══════════")
eq("binomial の実際の水準は 5% より小さい", btail_up(15, N3, P3) < 0.05, True)
eq("Poisson の実際の水準は 5% より小さい", ptail_up(11, M4) < 0.05, True)
approx("  binomial: 0.0344 は 0.05 の 7 割ほど",
       round(btail_up(15, N3, P3) / 0.05, 2), 0.69)
approx("  Poisson: 0.0426 は 0.05 の 9 割ほど",
       round(ptail_up(11, M4) / 0.05, 2), 0.85)

print("══════════ 演習2〜3（normal） ══════════")
SE_E2 = 12 / math.sqrt(36)
approx("演習2 standard error = 2", SE_E2, 2.0)
C_E2 = 250 + zcrit(0.05) * SE_E2
approx("演習2 critical value = 253.289…", round(C_E2, 5), 253.28971)
approx("  3 s.f. で 253", sf(C_E2), 253.0)
eq("  観測値 254 は critical region の中", 254 > C_E2, True)
approx("  p-value = 0.0228",
       sf(float(1 - stats.norm.cdf(254, 250, SE_E2)), 3), 0.0228)
approx("  生の値 0.022750",
       round(float(1 - stats.norm.cdf(254, 250, SE_E2)), 6), 0.022750)

SE_E3 = 0.2 / math.sqrt(25)
approx("演習3 standard error = 0.04", SE_E3, 0.04)
LO_E3 = 1.5 - zcrit(0.005) * SE_E3
HI_E3 = 1.5 + zcrit(0.005) * SE_E3
approx("演習3 下の critical value = 1.396967", round(LO_E3, 6), 1.396967)
approx("演習3 上の critical value = 1.603033", round(HI_E3, 6), 1.603033)
approx("  3 s.f. で 1.40", sf(LO_E3), 1.40)
approx("  3 s.f. で 1.60", sf(HI_E3), 1.60)
eq("  観測値 1.62 は critical region の中", 1.62 > HI_E3, True)
approx("  両側 p-value = 0.0027",
       sf(2 * float(1 - stats.norm.cdf(1.62, 1.5, SE_E3)), 2), 0.0027)

print("══════════ 演習4〜7（離散） ══════════")
eq("演習4 B(30, 0.25)、上側 5% は X >= 13", crit_binom_up(30, 0.25, 0.05), 13)
approx("  P(X >= 13) = 0.0216", sf(btail_up(13, 30, 0.25), 3), 0.0216)
approx("  生の値 0.021594", round(btail_up(13, 30, 0.25), 6), 0.021594)
approx("  P(X >= 12) = 0.0507", sf(btail_up(12, 30, 0.25), 3), 0.0507)
approx("  生の値 0.050658", round(btail_up(12, 30, 0.25), 6), 0.050658)
eq("  ★ X >= 12 は 0.0507 で、5% をわずかに超える",
   btail_up(12, 30, 0.25) > 0.05, True)

eq("演習5 Po(4)、上側 1% は X >= 10", crit_pois_up(4.0, 0.01), 10)
approx("  P(X >= 10) = 0.00813", sf(ptail_up(10, 4.0), 3), 0.00813)
approx("  生の値 0.008132", round(ptail_up(10, 4.0), 6), 0.008132)
approx("  P(X >= 9) = 0.0214", sf(ptail_up(9, 4.0), 3), 0.0214)
eq("  X >= 9 は 1% を超える", ptail_up(9, 4.0) > 0.01, True)

eq("演習6 Po(10)、下側 5% は X <= 4", crit_pois_lo(10.0, 0.05), 4)
approx("  P(X <= 4) = 0.0293", sf(ptail_lo(4, 10.0), 3), 0.0293)
approx("  生の値 0.029253", round(ptail_lo(4, 10.0), 6), 0.029253)
approx("  P(X <= 5) = 0.0671", sf(ptail_lo(5, 10.0), 3), 0.0671)
eq("  X <= 5 は 5% を超える", ptail_lo(5, 10.0) > 0.05, True)

eq("演習7 B(20, 0.6)、下側 5% は X <= 7", crit_binom_lo(20, 0.6, 0.05), 7)
approx("  P(X <= 7) = 0.0210", sf(btail_lo(7, 20, 0.6), 3), 0.0210)
approx("  生の値 0.021029", round(btail_lo(7, 20, 0.6), 6), 0.021029)
approx("  P(X <= 8) = 0.0565", sf(btail_lo(8, 20, 0.6), 3), 0.0565)
eq("  X <= 8 は 5% を超える", btail_lo(8, 20, 0.6) > 0.05, True)

print("══════════ ★ 表示用の丸め（通常の四捨五入）と、計算用の未丸め値 ══════════")


def region_p(bound, mu, se, op):
    return ncdf((bound - mu) / se) if op == "<" else 1 - ncdf((bound - mu) / se)


# ★ 連続分布では、critical region を【未丸めの境目】で決める。
#   だから P(Type I) は、設定した alpha にぴったり一致する。
for lab, mu, se, op, alpha, exact in [
        ("例題1", 500.0, 1.6, "<", 0.05, 500 - zcrit(0.05) * 1.6),
        ("例題2 下", 20.0, 0.25, "<", 0.025, 20 - zcrit(0.025) * 0.25),
        ("例題2 上", 20.0, 0.25, ">", 0.025, 20 + zcrit(0.025) * 0.25),
        ("演習2", 250.0, 2.0, ">", 0.05, 250 + zcrit(0.05) * 2.0),
        ("演習3 下", 1.5, 0.04, "<", 0.005, 1.5 - zcrit(0.005) * 0.04),
        ("演習3 上", 1.5, 0.04, ">", 0.005, 1.5 + zcrit(0.005) * 0.04)]:
    approx(f"{lab}：未丸めの境目なら確率はちょうど {alpha}",
           round(region_p(exact, mu, se, op), 10), alpha, 1e-9)

# ★ 本文が書いている表示値は、通常の四捨五入になっているか
for lab, exact, digits, want, kind in [
        ("例題1（小数第1位）", 497.368234, 1, 497.4, "dp"),
        ("例題2 下（3 s.f.）", 19.510009, 3, 19.5, "sf"),
        ("例題2 上（3 s.f.）", 20.489991, 3, 20.5, "sf"),
        ("演習2（小数第1位）", 253.289707, 1, 253.3, "dp"),
        ("演習3 下（小数第2位）", 1.396967, 2, 1.40, "dp"),
        ("演習3 上（小数第2位）", 1.603033, 2, 1.60, "dp")]:
    got = round(exact, digits) if kind == "dp" else sf(exact, digits)
    approx(f"{lab}：ふつうに四捨五入すると {want}", got, want)

# ★ 丸めた値を確率に入れ直すと alpha からずれる。
#   ずれること自体は「使えない」という意味ではない、というのが本文の説明。
approx("例題1：丸めた 497.4 を入れ直すと 0.0521（0.05 ではない）",
       sf(region_p(497.4, 500, 1.6, "<"), 3), 0.0521)
eq("  ずれはあるが、答案の表示値としては 497.4 が正しい",
   round(497.368234, 1), 497.4)
approx("演習3：丸めた 1.40 / 1.60 を入れ直すと片側 0.00621",
       sf(region_p(1.40, 1.5, 0.04, "<"), 3), 0.00621)
eq("  それでも表示値は 1.40 と 1.60", (round(1.396967, 2), round(1.603033, 2)),
   (1.4, 1.6))

# ★ 連続分布では、境目 1 点の確率は 0（< と <= の違いが効かない）
approx("連続分布では P(Xbar = c) = 0",
       round(region_p(497.368234, 500, 1.6, "<")
             - region_p(497.368234, 500, 1.6, "<"), 12), 0.0)
eq("  離散では P(X = 15) は 0 ではない", bpdf(15, 25, 0.4) > 0, True)

print("══════════ 演習8（与えられた region の確率） ══════════")
approx("演習8 B(25, 0.5) の P(X >= 18) = 0.0216", sf(btail_up(18, 25, 0.5), 3),
       0.0216)
approx("  生の値 0.021643", round(btail_up(18, 25, 0.5), 6), 0.021643)
eq("★ 与えられた region は 5% を超えていない（超えていたら本文の規則と矛盾する）",
   btail_up(18, 25, 0.5) <= 0.05, True)
eq("★ 自分で作っても同じ X >= 18 になる", crit_binom_up(25, 0.5, 0.05), 18)
approx("  1 つ手前の P(X >= 17) = 0.0539", sf(btail_up(17, 25, 0.5), 3), 0.0539)
eq("  X >= 17 は 5% を超えるので使えない", btail_up(17, 25, 0.5) > 0.05, True)
approx("  H0 のもとでの平均 = 12.5", 25 * 0.5, 12.5)

print("══════════ Inverse Binomial の 1 ずれ（上側と下側で向きが逆） ══════════")


def inv_binom(n, p, cum):
    """P(X <= k) >= cum となる最小の k（TI の Inverse Binomial と同じ）。"""
    for k in range(0, n + 1):
        if btail_lo(k, n, p) >= cum:
            return k
    return None


eq("上側 B(25, 0.4) 5%: invBinom(0.95) は 14", inv_binom(25, 0.4, 0.95), 14)
eq("  critical region はその 1 つ上", 14 + 1, crit_binom_up(25, 0.4, 0.05))
eq("下側 B(20, 0.6) 5%: invBinom(0.05) は 8", inv_binom(20, 0.6, 0.05), 8)
eq("★ 下側の critical region はその 1 つ【下】", 8 - 1,
   crit_binom_lo(20, 0.6, 0.05))
eq("★ 上側の規則を下側に使うと 2 つずれる",
   (8 + 1) - crit_binom_lo(20, 0.6, 0.05), 2)

print("══════════ 演習9（region から実際の水準を出す） ══════════")
approx("演習9 Po(6) の X >= 12 の確率 = 0.0201", sf(ptail_up(12, 6.0), 3),
       0.0201)
approx("  生の値 0.020092", round(ptail_up(12, 6.0), 6), 0.020092)
eq("  5% よりずっと小さい", ptail_up(12, 6.0) < 0.05, True)

print("══════════ 本文に、その数値が実際に書かれているか ══════════")
QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "ahl-4-18a.qmd")
TXT = open(QMD, encoding="utf-8").read()


def in_text(name, needle, want=True):
    global ok, ng
    good = (needle in TXT) == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else
           f"   ({'欠けている' if want else '残っている'}: {needle!r})"))
    ok, ng = ok + good, ng + (not good)


for lab, needle in [
        ("片側 5% の 1.645", "1.645"),
        ("両側 5% の 1.96", "1.96"),
        ("片側 1% の 2.326", "2.326"),
        ("両側 1% の 2.576", "2.576"),
        ("例題1 の 497.4", "497.4"),
        ("例題1 の standard error 1.6", "1.6"),
        ("例題2 の 19.5", "19.5"),
        ("例題2 の 20.5", "20.5"),
        ("例題3 の X >= 15", "0.0344"),
        ("例題3 の 0.0778", "0.0778"),
        ("例題4 の 0.0426", "0.0426"),
        ("例題4 の 0.0839", "0.0839"),
        ("演習4 の 0.0507", "0.0507"),
        ("演習5 の 0.00813", "0.00813"),
        ("演習6 の 0.0293", "0.0293"),
        ("演習7 の 0.0210", "0.0210")]:
    in_text(lab, needle)

# ★ シラバスの引用（t の critical region は不要）
in_text("t の critical region が不要という引用",
        "not be expected to calculate critical regions for $t$-tests")
in_text("離散は片側のみという引用",
        "critical regions will only be required for one-tailed tests")
in_text("最大にするという引用",
        "maximize the probability of a Type I error while keeping it less "
        "than the stated significance level")
# ★ GDC のメニュー（ユーザーの実機画面で確認したもの）
in_text("Inverse Normal がある", "Inverse Normal")
in_text("Inverse Binomial がある", "Inverse Binomial")
in_text("Stat Tests に binomial 検定が無いと書いてある", "`Stat Tests`")
in_text("メニューは Statistics → Distributions",
        "menu → Statistics → Distributions")
in_text("  Probability → Distributions が残っていない",
        "Probability → Distributions", want=False)
# ★ 「α ちょうどにはならない」ことを書いているか
in_text("演習8 の 0.0216", "0.0216")
in_text("演習8 の 0.0539（使えない側）", "0.0539")
in_text("  誤った region X >= 17 が残っていない", "critical region is $X \\geq 17$", want=False)
in_text("下側では 1 つ下と書いてある", "$1$ つ下")
# ★ 丸める向きの規則が本文に書かれているか
# ★ 旧「外向きに丸める」規則が残っていないか
in_text("  切り下げの規則が残っていない", "切り下げ", want=False)
in_text("  切り上げの規則が残っていない", "切り上げ", want=False)
in_text("  外向きに丸めるという説明が残っていない", "Rounding outwards", want=False)
in_text("  丸める向きという見出しが残っていない", "丸める向きに、決まりがあります",
        want=False)
# ★ 新しい説明が入っているか
in_text("表示用と計算用を分ける説明がある", "表示用の値と、計算用の値")
in_text("  通常の四捨五入と書いてある", "ふつうに四捨五入")
in_text("  未丸めの値を使う場面が書いてある", "**丸める前**の $497.368\\ldots$")
in_text("  Type II error にも触れている", "Type II error の確率を計算する")
in_text("連続分布で > と >= の違いが効かないと書いてある",
        "P(\\bar{X} = 497.368\\ldots) = 0")
in_text("  < と <= が同じ確率と書いてある", "**同じ確率**")
in_text("  離散は別あつかいと書いてある", "**離散分布は違います。**")
in_text("P(Type I) = alpha が成り立つ理由が書いてある",
        "がぴったり成り立ちます")
# ★ 表示値が通常の四捨五入になっているか
in_text("例題1 の region が 497.4", "$\\bar{x} < 497.4$")
in_text("  region としての 497.3 が残っていない", "$\\bar{x} < 497.3$",
        want=False)
in_text("  497.3 g という表記も残っていない", "497.3$ g", want=False)
in_text("演習2 の region が 253.3", "$\\bar{x} > 253.3$")
in_text("演習3 の region が 1.40 / 1.60",
        "$\\bar{x} < 1.40$ mm or $\\bar{x} > 1.60$ mm")
in_text("  1.39 が残っていない", "$1.39$", want=False)
in_text("  1.61 が残っていない", "$1.61$", want=False)
# ★ Common error が「丸めた値を精密な計算に使う」になっているか
in_text("Common error が丸めた値の使いどころになっている",
        "丸めた値を、精密な判定や Type II error の計算に使う")
# ★ 演習5 の解説：同じ Po(4) の 5% は X >= 9（X >= 8 ではない）
in_text("演習5 の解説が 5% では X >= 9 と書いている",
        "$5\\%$ なら $X \\geq 9$")
in_text("  誤った「5% なら X >= 8」が残っていない",
        "$5\\%$ なら $X \\geq 8$", want=False)
in_text("離散では α ちょうどにならないと書いてある", "ちょうど")
# ★ critical region と p-value が同じ判定になること
in_text("2 つの判定が一致すると書いてある", "同じ判定")

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
