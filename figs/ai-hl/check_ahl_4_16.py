"""AHL 4.16 の本文・例題・演習の数値を独立に検算する。

   ★ AI では z 値への変換をしない（SL 4.9 のシラバス）。電卓の
     zInterval / tInterval にそのまま入れる形で書く。この検算でも、
     区間は「中心 ± (臨界値) x (標準誤差)」として直接組み立てる。
   ★ 臨界値は scipy と、自作の二分法（累積確率から逆に解く）の
     両方で出して突き合わせる。片方だけを信じない。
   ★ 「95% の信頼区間」の意味は、モンテカルロで確かめる。
     標本を何度もとって区間を作り、mu を含む割合が 0.95 に近いことを見る。

   実行: python3 figs/ai-hl/check_ahl_4_16.py
"""
import math
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


# ── 臨界値を、二分法でも出して scipy と突き合わせる ────────────────
def bisect_quantile(cdf, p, lo=-40.0, hi=40.0):
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def zstar(conf):
    p = 0.5 + conf / 2
    a = float(stats.norm.ppf(p))
    b = bisect_quantile(lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2))), p)
    assert abs(a - b) < 1e-9, f"z* が食い違う {a} {b}"
    return a


def tstar(conf, df):
    p = 0.5 + conf / 2
    a = float(stats.t.ppf(p, df))
    b = bisect_quantile(lambda x: float(stats.t.cdf(x, df)), p)
    assert abs(a - b) < 1e-8, f"t* が食い違う {a} {b}"
    return a


def interval(xbar, s, n, conf, sigma_known):
    """中心 ± 臨界値 x 標準誤差。電卓の zInterval / tInterval と同じもの。"""
    se = s / math.sqrt(n)
    q = zstar(conf) if sigma_known else tstar(conf, n - 1)
    return xbar - q * se, xbar + q * se, q, se


print("══════════ 臨界値そのもの ══════════")
eq("z* (90%) = 1.645 (4 s.f.)", sf(zstar(0.90), 4), 1.645)
eq("z* (95%) = 1.960 (4 s.f.)", sf(zstar(0.95), 4), 1.960)
eq("z* (99%) = 2.576 (4 s.f.)", sf(zstar(0.99), 4), 2.576)
eq("信頼水準を上げると z* も大きくなる",
   zstar(0.90) < zstar(0.95) < zstar(0.99), True)
# t* は df によって変わり、df が大きいと z* に近づく
eq("t*(95%, df=7) = 2.365 (4 s.f.)", sf(tstar(0.95, 7), 4), 2.365)
eq("t*(95%, df=11) = 2.201 (4 s.f.)", sf(tstar(0.95, 11), 4), 2.201)
eq("t*(95%, df=19) = 2.093 (4 s.f.)", sf(tstar(0.95, 19), 4), 2.093)
eq("t*(90%, df=19) = 1.729 (4 s.f.)", sf(tstar(0.90, 19), 4), 1.729)
eq("t* はいつも z* より大きい",
   all(tstar(0.95, df) > zstar(0.95) for df in (2, 5, 10, 30, 100, 1000)), True)
eq("df が大きいほど t* は z* に近づく",
   tstar(0.95, 5) > tstar(0.95, 30) > tstar(0.95, 200) > zstar(0.95), True)
approx("df = 1000 でも t* はまだ z* より上",
       tstar(0.95, 1000), zstar(0.95), 0.01)

print("══════════ 例題1：sigma 既知（チョコレート） ══════════")
SIG1, N1, XB1 = 2.5, 20, 48.6
lo, hi, q, se = interval(XB1, SIG1, N1, 0.95, True)
eq("標準誤差 = 2.5/sqrt(20) = 0.559 (3 s.f.)", sf(se), 0.559)
eq("  生の値 0.55902", round(se, 5), 0.55902)
eq("z* = 1.96 (3 s.f.)", sf(q), 1.96)
eq("誤差の幅 = 1.10 (3 s.f.)", sf(q * se), 1.10)
eq("下端 = 47.5 (3 s.f.)", sf(lo), 47.5)
eq("上端 = 49.7 (3 s.f.)", sf(hi), 49.7)
eq("  生の値 47.5043", round(lo, 4), 47.5043)
eq("  生の値 49.6957", round(hi, 4), 49.6957)
eq("中心は xbar", (lo + hi) / 2, XB1)
eq("幅 = 2 x 誤差の幅", hi - lo, 2 * q * se)
eq("幅 = 2.19 (3 s.f.)", sf(hi - lo), 2.19)
# t を誤って使ったら別の値になる
lo_t, hi_t, qt, _ = interval(XB1, SIG1, N1, 0.95, False)
eq("t を誤って使うと t* = 2.09 (3 s.f.)", sf(qt), 2.09)
eq("  区間も広くなる", (hi_t - lo_t) > (hi - lo), True)
eq("  そのとき下端 47.4 (3 s.f.)", sf(lo_t), 47.4)

print("══════════ 例題2：sigma 未知、データが与えられる ══════════")
D2 = np.array([12.1, 11.8, 12.4, 12.0, 11.6, 12.3, 12.1, 11.7])
n2 = len(D2)
xb2 = float(D2.mean())
s2 = float(np.std(D2, ddof=1))
eq("n = 8", int(n2), 8)
eq("合計 = 96.0", float(D2.sum()), 96.0)
eq("xbar = 12.0（ちょうど）", xb2, 12.0)
eq("偏差の2乗の合計 = 0.56", float(((D2 - xb2) ** 2).sum()), 0.56)
eq("s_{n-1}^2 = 0.56/7 = 0.08", float(((D2 - xb2) ** 2).sum() / 7), 0.08)
eq("s_{n-1} = 0.283 (3 s.f.)", sf(s2), 0.283)
eq("  生の値 0.28284", round(s2, 5), 0.28284)
eq("電卓の sigma_x（n で割る）は 0.265 (3 s.f.)",
   sf(float(np.std(D2, ddof=0))), 0.265)
eq("s_x のほうが大きい", s2 > float(np.std(D2, ddof=0)), True)
lo2, hi2, q2, se2 = interval(xb2, s2, n2, 0.95, False)
eq("df = 7", n2 - 1, 7)
eq("t* = 2.36 (3 s.f.)", sf(q2), 2.36)
eq("標準誤差 = 0.1（ちょうど）", se2, 0.1)
eq("誤差の幅 = 0.236 (3 s.f.)", sf(q2 * se2), 0.236)
eq("下端 = 11.8 (3 s.f.)", sf(lo2), 11.8)
eq("上端 = 12.2 (3 s.f.)", sf(hi2), 12.2)
eq("  生の値 11.7635", round(lo2, 4), 11.7635)
eq("  生の値 12.2365", round(hi2, 4), 12.2365)
# sigma_x を誤って使うと別の値
lo2w, hi2w, _, _ = interval(xb2, float(np.std(D2, ddof=0)), n2, 0.95, False)
eq("sigma_x を使うと下端 11.8 だが生の値が違う",
   round(lo2w, 4) != round(lo2, 4), True)
eq("  そのときの生の値 11.7788", round(lo2w, 4), 11.7788)

print("══════════ 例題3：sigma 未知、統計量だけが与えられる ══════════")
N3, XB3, S3 = 20, 68.4, 5.2
lo3, hi3, q3, se3 = interval(XB3, S3, N3, 0.90, False)
eq("df = 19", N3 - 1, 19)
eq("t* = 1.73 (3 s.f.)", sf(q3), 1.73)
eq("  生の値 1.72913", round(q3, 5), 1.72913)
eq("標準誤差 = 1.16 (3 s.f.)", sf(se3), 1.16)
eq("  生の値 1.16276", round(se3, 5), 1.16276)
eq("誤差の幅 = 2.01 (3 s.f.)", sf(q3 * se3), 2.01)
eq("下端 = 66.4 (3 s.f.)", sf(lo3), 66.4)
eq("上端 = 70.4 (3 s.f.)", sf(hi3), 70.4)
eq("  生の値 66.3894", round(lo3, 4), 66.3894)
eq("  生の値 70.4106", round(hi3, 4), 70.4106)

print("══════════ 例題3(c)：信頼水準を上げると幅が広がる ══════════")
widths = {}
for c in (0.90, 0.95, 0.99):
    a, b, _, _ = interval(XB3, S3, N3, c, False)
    widths[c] = b - a
eq("90% の幅 = 4.02 (3 s.f.)", sf(widths[0.90]), 4.02)
eq("95% の幅 = 4.87 (3 s.f.)", sf(widths[0.95]), 4.87)
eq("99% の幅 = 6.65 (3 s.f.)", sf(widths[0.99]), 6.65)
eq("信頼水準が上がると幅も広がる",
   widths[0.90] < widths[0.95] < widths[0.99], True)
a95, b95, _, _ = interval(XB3, S3, N3, 0.95, False)
eq("95% 区間は (66.0, 70.8) (3 s.f.)", (sf(a95), sf(b95)), (66.0, 70.8))
eq("  生の値 65.9663", round(a95, 4), 65.9663)
eq("  生の値 70.8337", round(b95, 4), 70.8337)

print("══════════ 本文：n を増やすと幅が狭くなる ══════════")
# 同じ xbar, s で n だけ変える（幅は 1/sqrt(n) では【ない】。t* も動く）
prev = None
for n in (5, 10, 20, 50, 100):
    a, b, q, se = interval(68.4, 5.2, n, 0.95, False)
    w = b - a
    if prev is not None:
        eq(f"n={n}: 幅が n={prev[0]} より狭い", w < prev[1], True)
    prev = (n, w)
a10, b10, q10, se10 = interval(68.4, 5.2, 10, 0.95, False)
a40, b40, q40, se40 = interval(68.4, 5.2, 40, 0.95, False)
eq("n=10 の幅 = 7.44 (3 s.f.)", sf(b10 - a10), 7.44)
eq("n=40 の幅 = 3.33 (3 s.f.)", sf(b40 - a40), 3.33)
eq("n を 4 倍にしても、幅はちょうど半分にはならない",
   abs((b40 - a40) - (b10 - a10) / 2) > 0.01, True)
eq("  標準誤差だけならちょうど半分", se40, se10 / 2)
eq("  t* が小さくなるぶん、幅はもう少し縮む",
   (b40 - a40) < (b10 - a10) / 2, True)

print("══════════ 「95% の信頼区間」の意味（モンテカルロ） ══════════")
rng = np.random.default_rng(416)
MU, SIG, NS, TRIALS = 50.0, 8.0, 12, 200_000
d = rng.normal(MU, SIG, size=(TRIALS, NS))
xb = d.mean(axis=1)
sd = d.std(axis=1, ddof=1)
for conf in (0.90, 0.95, 0.99):
    t = tstar(conf, NS - 1)
    lo_ = xb - t * sd / math.sqrt(NS)
    hi_ = xb + t * sd / math.sqrt(NS)
    hit = float(((lo_ <= MU) & (MU <= hi_)).mean())
    approx(f"t 区間が mu を含む割合 = {conf}", hit, conf, 0.004)
# sigma を知っているときは z 区間
for conf in (0.90, 0.95):
    z = zstar(conf)
    lo_ = xb - z * SIG / math.sqrt(NS)
    hi_ = xb + z * SIG / math.sqrt(NS)
    hit = float(((lo_ <= MU) & (MU <= hi_)).mean())
    approx(f"z 区間（sigma 既知）が mu を含む割合 = {conf}", hit, conf, 0.004)
# ★ sigma を知らないのに z を使うと、95% に届かない
z = zstar(0.95)
lo_ = xb - z * sd / math.sqrt(NS)
hi_ = xb + z * sd / math.sqrt(NS)
bad = float(((lo_ <= MU) & (MU <= hi_)).mean())
approx("sigma 未知なのに z を使うと 0.95 に届かない", bad, 0.9276, 0.005)
eq("  実際 0.95 より小さい", bad < 0.95, True)

print("══════════ 演習1〜3 ══════════")
lo, hi, q, se = interval(82.0, 6.0, 36, 0.95, True)
eq("演習1 標準誤差 = 1（ちょうど）", se, 1.0)
eq("演習1 z* = 1.96 (3 s.f.)", sf(q), 1.96)
eq("演習1 下端 = 80.0 (3 s.f.)", sf(lo), 80.0)
eq("演習1 上端 = 84.0 (3 s.f.)", sf(hi), 84.0)
eq("  生の値 80.0400", round(lo, 4), 80.04)
eq("  生の値 83.9600", round(hi, 4), 83.96)
lo, hi, q, se = interval(45.2, 3.8, 12, 0.95, False)
eq("演習2 t* は df=11 のもの（df=12 とは違う）",
   sf(tstar(0.95, 11), 4) != sf(tstar(0.95, 12), 4), True)
eq("演習2 t* = 2.20 (3 s.f.)", sf(q), 2.20)
eq("演習2 標準誤差 = 1.10 (3 s.f.)", sf(se), 1.10)
eq("演習2 下端 = 42.8 (3 s.f.)", sf(lo), 42.8)
eq("演習2 上端 = 47.6 (3 s.f.)", sf(hi), 47.6)
eq("  生の値 42.7856", round(lo, 4), 42.7856)
eq("  生の値 47.6144", round(hi, 4), 47.6144)
D3 = np.array([203, 198, 207, 201, 199, 204, 202, 196, 205, 200], float)
n3_, xb3_, s3_ = len(D3), float(D3.mean()), float(np.std(D3, ddof=1))
eq("演習3 n = 10", n3_, 10)
eq("演習3 合計 = 2015", float(D3.sum()), 2015.0)
eq("演習3 xbar = 201.5", xb3_, 201.5)
eq("演習3 s_{n-1} = 3.37 (3 s.f.)", sf(s3_), 3.37)
eq("  生の値 3.37474", round(s3_, 5), 3.37474)
lo, hi, q, se = interval(xb3_, s3_, n3_, 0.99, False)
eq("演習3 df = 9", n3_ - 1, 9)
eq("演習3 t* = 3.25 (3 s.f.)", sf(q), 3.25)
eq("演習3 下端 = 198 (3 s.f.)", sf(lo), 198.0)
eq("演習3 上端 = 205 (3 s.f.)", sf(hi), 205.0)
eq("  生の値 198.0318", round(lo, 4), 198.0318)
eq("  生の値 204.9682", round(hi, 4), 204.9682)

print("══════════ 演習5〜9 ══════════")
# 演習5：n を変えたときの幅（sigma 既知）
# 本文は幅だけを問うので、中心は何でもよい（ここでは 0 とする）
w = {}
for n in (16, 64):
    a, b, _, _ = interval(0.0, 9.0, n, 0.95, True)
    w[n] = b - a
eq("演習5 n=16 の幅 = 8.82 (3 s.f.)", sf(w[16]), 8.82)
eq("演習5 n=64 の幅 = 4.41 (3 s.f.)", sf(w[64]), 4.41)
eq("演習5 sigma 既知なら n が 4 倍で幅はちょうど半分", w[64], w[16] / 2)
eq("演習5 標準誤差は 2.25 -> 1.125", (9 / math.sqrt(16), 9 / math.sqrt(64)),
   (2.25, 1.125))
eq("演習5 sqrt(n) は 2 倍になる（n が 4 倍だから）",
   math.sqrt(64) / math.sqrt(16), 2.0)
# 演習7：区間から中心と誤差の幅を読む
LO7, HI7 = 23.4, 26.6
eq("演習6 xbar は中点 = 25.0", (LO7 + HI7) / 2, 25.0)
eq("演習6 誤差の幅 = 1.6", (HI7 - LO7) / 2, 1.6)
eq("演習6 幅 = 3.2", HI7 - LO7, 3.2)
# 演習7：主張が区間の外か中か
eq("演習7 主張 27 は区間 (23.4, 26.6) の外", not (LO7 <= 27 <= HI7), True)
eq("演習7 主張 24 は区間の中", LO7 <= 24 <= HI7, True)
# 演習8：2 つの区間が【重ならない】場合（例題4 と対になる）
A_LO, A_HI = 51.0, 54.0
B_LO, B_HI = 56.0, 59.0
eq("演習8 A の中心 = 52.5", (A_LO + A_HI) / 2, 52.5)
eq("演習8 B の中心 = 57.5", (B_LO + B_HI) / 2, 57.5)
eq("演習8 2 つの区間は重ならない", A_HI < B_LO, True)
eq("演習8 すき間は 54.0 から 56.0", (A_HI, B_LO), (54.0, 56.0))
eq("演習8 例題4 とは逆の結論になる",
   (A_HI < B_LO) and (55.8 > 54.1), True)
# 演習9：90% と 99%（この節の下にもう一度出てくる）
for c, want in ((0.90, 1.645), (0.99, 2.576)):
    eq(f"演習9 z*({c}) = {want}", sf(zstar(c), 4), want)
a90, b90, _, _ = interval(500.0, 15.0, 25, 0.90, True)
a99, b99, _, _ = interval(500.0, 15.0, 25, 0.99, True)
eq("演習9（別数値）90% = (495.1, 504.9) (4 s.f.)",
   (sf(a90, 4), sf(b90, 4)), (495.1, 504.9))
eq("演習9（別数値）99% = (492.3, 507.7) (4 s.f.)",
   (sf(a99, 4), sf(b99, 4)), (492.3, 507.7))
eq("演習9（別数値）99% のほうが広い", (b99 - a99) > (b90 - a90), True)
eq("演習9（別数値）90% の幅 = 9.87 (3 s.f.)", sf(b90 - a90), 9.87)
eq("演習9（別数値）99% の幅 = 15.5 (3 s.f.)", sf(b99 - a99), 15.5)

print("══════════ 第5節の臨界値の表 ══════════")
eq("表 z: 1.645 / 1.960 / 2.576",
   tuple(sf(zstar(c), 4) for c in (0.90, 0.95, 0.99)), (1.645, 1.960, 2.576))
eq("表 n=8 (df=7): 1.895 / 2.365 / 3.499",
   tuple(sf(tstar(c, 7), 4) for c in (0.90, 0.95, 0.99)), (1.895, 2.365, 3.499))
eq("表 n=20 (df=19): 1.729 / 2.093 / 2.861",
   tuple(sf(tstar(c, 19), 4) for c in (0.90, 0.95, 0.99)), (1.729, 2.093, 2.861))
eq("各行で t* > z*",
   all(tstar(c, df) > zstar(c) for c in (0.90, 0.95, 0.99) for df in (7, 19)),
   True)
eq("n=20 のほうが z* に近い",
   all(tstar(c, 19) < tstar(c, 7) for c in (0.90, 0.95, 0.99)), True)

print("══════════ 例題3(b)：99% ══════════")
a99e, b99e, q99e, _ = interval(68.4, 5.2, 20, 0.99, False)
eq("例題3(b) t* = 2.861 (4 s.f.)", sf(q99e, 4), 2.861)
eq("例題3(b) 区間 (65.1, 71.7) (3 s.f.)", (sf(a99e), sf(b99e)), (65.1, 71.7))
eq("  生の値 65.0734", round(a99e, 4), 65.0734)
eq("  生の値 71.7266", round(b99e, 4), 71.7266)

print("══════════ 例題4：2 つの区間の中心 ══════════")
eq("例題4 xbarA = 53.5（本文の演習8 と同じ数値）", (51.2 + 55.8) / 2, 53.5)
eq("例題4 xbarB = 56.5", (54.1 + 58.9) / 2, 56.5)
eq("例題4 B のほうが大きい", (54.1 + 58.9) / 2 > (51.2 + 55.8) / 2, True)
eq("例題4 区間は重なる（A の上端 > B の下端）", 55.8 > 54.1, True)
eq("例題4 重なりは max(下端) から min(上端)",
   (max(51.2, 54.1), min(55.8, 58.9)), (54.1, 55.8))
eq("例題4 mu = 55 は両方の区間に入る",
   (51.2 <= 55 <= 55.8) and (54.1 <= 55 <= 58.9), True)

print("══════════ 演習9 ══════════")
a9, b9, _, se9 = interval(500.0, 15.0, 25, 0.90, True)
c9, d9, _, _ = interval(500.0, 15.0, 25, 0.99, True)
eq("演習9 標準誤差 = 3（ちょうど）", se9, 3.0)
eq("演習9 90% = (495, 505) (3 s.f.)", (sf(a9), sf(b9)), (495.0, 505.0))
eq("  生の値 495.0654", round(a9, 4), 495.0654)
eq("  生の値 504.9346", round(b9, 4), 504.9346)
eq("演習9 99% = (492, 508) (3 s.f.)", (sf(c9), sf(d9)), (492.0, 508.0))
eq("  生の値 492.2725", round(c9, 4), 492.2725)
eq("  生の値 507.7275", round(d9, 4), 507.7275)
eq("演習9 幅 9.87 と 15.5 (3 s.f.)",
   (sf(b9 - a9), sf(d9 - c9)), (9.87, 15.5))

print("══════════ 演習10：区間と個々の値の散らばりの違い ══════════")
# 区間の半幅は s/sqrt(n) 由来、個々の値は s。比は sqrt(n)。
for n in (9, 25, 100):
    # s / (s/sqrt(n)) = sqrt(n) を、実際の s から出して確かめる
    s_ = 4.7
    eq(f"n={n}: s は標準誤差の sqrt({n}) 倍",
       s_ / (s_ / math.sqrt(n)), math.sqrt(n))
eq("n=25 なら sqrt(n) = 5 倍", math.sqrt(25), 5.0)
# 実際に、95% 区間の中に母集団の何割が入るかを見る
rng2 = np.random.default_rng(99)
mu0, sig0, n0 = 50.0, 8.0, 25
smp = rng2.normal(mu0, sig0, n0)
xb0, s0 = float(smp.mean()), float(np.std(smp, ddof=1))
t0 = tstar(0.95, n0 - 1)
lo0 = xb0 - t0 * s0 / math.sqrt(n0)
hi0 = xb0 + t0 * s0 / math.sqrt(n0)
frac = float(stats.norm.cdf(hi0, mu0, sig0) - stats.norm.cdf(lo0, mu0, sig0))
eq("95% 区間に母集団の 95% は入らない", frac < 0.5, True)
approx("  実際は 3 割ほど", frac, 0.30, 0.15)

print("══════════ 本文に、その数値が実際に書かれているか ══════════")
# ★ ここまでは数値を【計算】しただけ。qmd を読んで、本文の記述と突き合わせる。
import os
QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "ahl-4-16.qmd")
TXT = open(QMD, encoding="utf-8").read()


def in_text(name, needle, want=True):
    global ok, ng
    good = (needle in TXT) == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   ({'欠けている' if want else '残っている'}: {needle!r})"))
    ok, ng = ok + good, ng + (not good)


# 例題の答えが本文にあるか
for lab, needle in [
        ("例題1 の区間", "47.5 < \\mu < 49.7"),
        ("例題2 の区間", "11.8 < \\mu < 12.2"),
        ("例題3(a) の区間", "66.4 < \\mu < 70.4"),
        ("例題3(b) の区間", "65.1 < \\mu < 71.7"),
        ("演習1 の区間", "80.0 < \\mu < 84.0"),
        ("演習2 の区間", "42.8 < \\mu < 47.6"),
        ("演習3 の区間", "198 < \\mu < 205"),
        ("演習9 の 90% 区間", "495 < \\mu < 505"),
        ("演習9 の 99% 区間", "492 < \\mu < 508")]:
    in_text(lab, needle)

# ★ 重なりの範囲。例題4 の overlap は 54.1〜55.8 でなければならない。
eq("例題4 の overlap は 54.1 から 55.8",
   (max(51.2, 54.1), min(55.8, 58.9)), (54.1, 55.8))
in_text("例題4 の model answer が正しい overlap を書いている",
        "overlap between $54.1$ and $55.8$ hundred hours")
in_text("  誤った overlap（58.9）が残っていない",
        "overlap between $54.1$ and $58.9$", want=False)

# ★ n を 4 倍にすると sqrt(n) は 2 倍。「divides」と書いていないか。
in_text("演習5 の英文が multiplies になっている",
        "Multiplying $n$ by $4$ multiplies $\\sqrt{n}$ by $2$")
in_text("  誤った divides が残っていない",
        "divides $\\sqrt{n}$ by $2$", want=False)

# ★ シラバスの前提（normal population）が本文にあるか
in_text("Content 欄の引用がある",
        "Confidence intervals for the mean of **a normal population**.")
in_text("regardless of sample size の引用がある", "regardless of sample size.")
in_text("interpret ... in context の引用がある",
        "interpret the meaning of their results in context.")
in_text("TOK の overlap の引用がある",
        "can mean very little if there is a large overlap")

# ★ 臨界値の表の数値が本文にあるか
for v in ("1.645", "1.960", "2.576", "1.895", "2.365", "3.499",
          "1.729", "2.093", "2.861"):
    in_text(f"臨界値の表に {v} がある", "$" + v + "$")



# ══════════════════════════════════════════════════════════════
#  改稿（読む順の整理）で入れた表現が、あとで戻っていないか
# ══════════════════════════════════════════════════════════════
import re as _re

# 1. 冒頭の導入と、読む順の提示
in_text("冒頭に導入がある",
        "標本平均 $\\bar{x}$ は、標本を取り直すたびに少しずつ変わります。")
in_text("読む順が示されている", "1. なぜ $1$ つの推定値だけでは足りないのか（[第1節](#idea)）")
_i_intro = TXT.index("標本を取り直すたびに")
_i_wysb = TXT.index("## What you should be able to do")
eq("導入は What you should be able to do より前", _i_intro < _i_wysb, True)

# 2. AHL 4.15 との関係 ／ X-bar と x-bar の区別
in_text("4.15 で学んだことが書かれている",
        "**$\\mu$ が分かっているとき、標本平均 $\\bar{X}$ がどのように変動するか**")
in_text("このページで新しく学ぶことが書かれている",
        "**このページで新しく学ぶのは、その反対向きの読み方です。**")
in_text("Xbar と xbar の違いが書かれている",
        "$\\bar{X}$ は標本を取る前の「変化する標本平均」を表し、"
        "$\\bar{x}$ は実際の標本から得られた $1$ つの数値を表します")
in_text("「逆向きに使います」という説明だけの見出しは残っていない",
        "## AHL 4.15 の $\\bar{X}$ を、逆向きに使います", want=False)

# 3. 公式集の説明を短くした
in_text("専用の公式が無いことを短く書いている",
        "AHL 4.16 専用の新しい公式はありません")
in_text("手で計算する式も要りません、は残っていない",
        "**そして、手で計算する式も要りません。**", want=False)

# 4. 点推定と区間推定の対比、margin of error
in_text("point estimate の対比", "- **point estimate**（点推定値）… $\\mu$ を $1$ つの数 $\\bar{x}$ で推定する")
in_text("interval estimate の対比", "- **interval estimate**（区間推定）… $\\mu$ が入りそうな**範囲**で推定する")
in_text("margin of error の定義", "**margin of error**（誤差の幅）は、点推定値の左右にとる幅のことです")
in_text("中心と margin of error の計算",
        "\\text{中心} = \\frac{47.5 + 49.7}{2} = 48.6, \\qquad "
        "\\text{margin of error} = 49.7 - 48.6 = 1.1")
eq("中心の計算が正しい", (47.5 + 49.7) / 2, 48.6)
eq("margin of error の計算が正しい", 49.7 - 48.6, 1.1, tol=1e-9)
in_text("2 つの書き方が同じ区間だと書いてある", "$48.6 \\pm 1.1$ と**同じ区間**です")

# 5. 95% の意味を段階化
in_text("直感的な言い方が先にある",
        "長期的には約 $95\\%$ の区間が真の母平均 $\\mu$ を含む")
for _s in ("1. **横線 $1$ 本が、$1$ 回の標本から作った信頼区間**です",
           "3. **オレンジ色の縦線**が、動かない真の母平均 $\\mu = 50$ です",
           "4. **青い区間は $\\mu$ を含み、赤い区間は含んでいません**",
           "5. $100$ 本すべてが含むのではなく、**長期的に約 $95\\%$ が含みます**"):
    in_text("図の読み方 " + _s[:12], _s)
in_text("ちょうど 95 回ではない、という注意",
        "## 「$100$ 回やれば、ちょうど $95$ 回成功する」ではありません")

# 6. 確率 95% の注意
in_text("計算後は mu も区間も動かない",
        "**区間を計算した後は、$\\mu$ は動かず、区間もすでに決まっています。**")
in_text("日本語の言いかえがある",
        "チョコレートバーの母平均質量は $47.5$ g から $49.7$ g のあいだにあると、"
        "$95\\%$ の信頼度で推定できる")

# 7. 記号の意味は、その記号が出てくる式の直後に置く
_i_lead = TXT.index("分からない population mean（母平均）$\\mu$ を、手元の sample mean（標本平均）$\\bar{x}$ から推定する範囲")
_i_ci = TXT.index("{#eq-ahl416-ci}")
eq("何をする区間かの一文が基本形より前", _i_lead < _i_ci, True)
in_text("基本形", "\\bar{x} \\ \\pm \\ (\\text{critical value}) \\times (\\text{standard error})")
in_text("sigma 既知の式", "\\bar{x} \\ \\pm \\ z^{*} \\frac{\\sigma}{\\sqrt{n}}")
in_text("sigma 未知の式", "\\bar{x} \\ \\pm \\ t^{*} \\frac{s}{\\sqrt{n}}")
# 基本形の直後の 3 つ
_i_z = TXT.index("{#eq-ahl416-z}")
_i_t = TXT.index("{#eq-ahl416-t}")
for _s in ("- $\\bar{x}$ … 区間の中心となる **sample mean**（標本平均）",
           "- **critical value**（臨界値）… **confidence level**（信頼水準）に合わせて、standard error **何個分**",
           "- **standard error**（標準誤差）… sample mean が標本ごとに、どれくらいばらつくか"):
    in_text("基本形の直後に " + _s[2:22], _s)
    eq("  それが基本形と sigma 既知の式のあいだにある",
       _i_ci < TXT.index(_s) < _i_z, True)
# sigma 既知の式の直後
for _s in ("- $\\sigma$ … **population standard deviation**（母標準偏差）",
           "- $n$ … **sample size**（標本の大きさ）",
           "- $z^{*}$ … normal distribution から決まる critical value"):
    in_text("z の式の直後に " + _s[2:20], _s)
    eq("  それが z の式と t の式のあいだにある", _i_z < TXT.index(_s) < _i_t, True)
in_text("95% の z* の値", "$95\\%$ confidence interval では、$z^{*} = 1.96$ です。")
# sigma 未知の式の直後
for _s in ("- $s$ … **sample standard deviation**（標本標準偏差）",
           "- $\\dfrac{s}{\\sqrt{n}}$ … $\\sigma$ を $s$ で置きかえて**推定した** standard error",
           "- $t^{*}$ … **$t$-distribution** から決まる critical value"):
    in_text("t の式の直後に " + _s[2:20], _s)
    eq("  それが t の式より後ろにある", _i_t < TXT.index(_s), True)
# 記号の意味を一覧にまとめる書き方は残っていない
in_text("記号を一覧でまとめる書き方は残っていない", "記号は、それぞれ次のものです。", want=False)
# z と t の使い分けの理由
in_text("z を使う理由", "$\\sigma$ が分かっている場合は、standard error を**正確に**求められます")
in_text("t を使う理由", "推定による不確かさが加わるので、そのぶんを見こんで、裾が少し広い $t$-distribution を使います")
in_text("t* は df で決まる",
        "$t^{*}$ は、confidence level と **degrees of freedom**（自由度）$\\text{df} = n - 1$ によって決まります")
# 判断ルールの箱は 1 か所だけ
in_text("判断ルールの箱",
        "\\boxed{\\ \\sigma \\ \\text{が既知} \\ \\Rightarrow \\ z \\qquad \\sigma \\ \\text{が未知} \\ \\Rightarrow \\ t\\ }")
eq("判断ルールの箱は 1 つだけ", TXT.count("\\boxed{\\ \\sigma"), 1)
in_text("第5節に重複する箱が無い", "{#eq-ahl416-rule-z}", want=False)
in_text("第5節に重複する箱が無い（t）", "{#eq-ahl416-rule-t}", want=False)
in_text("第5節は第3節の箱を参照している",
        "判断のしかたは @eq-ahl416-rule のとおりで、$\\sigma$ が既知なら `z Interval`、未知なら `t Interval` です")
in_text("第5節は問題文の読み取りに絞っている",
        "ここで見るのは、**問題文からその $\\sigma$ を読み取る**ところです。")
# GDC で計算するが、形を知っていると確かめられる
in_text("手計算は要らない", "**この式を手で計算する必要はありません。** 電卓が区間の両端を返します。")
in_text("形を知ると GDC の選択と入力を確かめられる",
        "**式の形を知っていると、電卓の選び方と入力を確かめられます。**")

# 8. 正規性の前提
in_text("基本的に normal と仮定する、という書き方",
        "基本的に**母集団が normally distributed（正規分布にしたがう）と仮定します。**")
in_text("このページの問題は normal population が前提",
        "**このページの問題は、すべてこの前提でできています。**")
in_text("CLT で扱えることがある、という書き方",
        "標本平均を近似的に正規分布として扱えることがあります")
in_text("正規性が明記されていない場合の注意",
        "問題文に正規性が明記されていないのに、小さい標本でこの方法を使った場合は、"
        "その仮定を答案に書くよう求められることがあります")

# 9. sigma の確認を最初の判断に
in_text("第5節の見出し", "### 5. 計算の前に、$\\sigma$ が分かっているか確認する {#which}")
for _s in ("**$n$ の大小だけで $z$ と $t$ を選ばないでください。**",
           "**$\\sigma$ が分かったことにはなりません。**",
           "「標本が大きければ、未知の $\\sigma$ を既知としてよい」という意味では**ありません。**",
           "**$\\sigma$ が未知なら、標本が大きくても $t$-interval** を選びます"):
    in_text("第5節の注意に " + _s[:16], _s)
eq("第5節の表は 1 つに統合されている", TXT.count("{#tbl-ahl416-spot}"), 0)
in_text("統合した表の見出し行",
        "| 問題文の表現 | 分かっているもの | 使う分布 | GDC |")
in_text("it is known from experience は表の下の補足",
        "`it is known from experience that the standard deviation is 2.5` のような書き方もあります")

# 10. t 分布は理由 → 特徴の順
_i_why = TXT.index("$s$ で standard error を**推定する**ぶん不確かさが増えます")
_i_feat = TXT.index("**$1$ つ目。$t$-distribution は normal distribution より裾が広い")
eq("理由が特徴より前", _i_why < _i_feat, True)
in_text("第6節は第3節の理由を繰り返さない",
        "この推定にも不確かさがあります。そのぶんを埋め合わせるために", want=False)
in_text("第6節は第3節を参照する", "[第3節](#z-vs-t)で見たとおり")
in_text("2 つ目の特徴の言い方",
        "**$2$ つ目。$n$ が大きくなると $s$ による推定が安定するので、"
        "$t$-distribution は normal distribution に近づきます。**")
in_text("df の理由", "**標本平均を決めてしまうと、$n$ 個の偏差のうち自由に決められるのは $n - 1$ 個になる**")
in_text("n=8 のときの df", "たとえば $n = 8$ なら、$\\text{df} = 8 - 1 = 7$ です")
eq("n=8 の df", 8 - 1, 7)

# 11. 幅の比較は「ほかの条件が同じなら」
in_text("他の条件が同じ、という前置き",
        "**以下は、表に書かれている要素以外の条件が同じ場合の比較です。**")
for _s in ("- **confidence level を上げる** → より多くの場合に $\\mu$ を含みたい → "
           "critical value が大きくなる → 区間が広くなる",
           "- **$n$ を増やす** → standard error",
           "- **データのばらつきが大きくなる** → $s$ または $\\sigma$ が大きくなる"):
    in_text("因果のつながりに " + _s[:20], _s)
in_text("4 倍で半分は条件つき",
        "**幅がちょうど半分になるのは、critical value と standard deviation が同じままのとき**です")
in_text("99% の説明が割合の言葉になっている",
        "**confidence level を高くすると、同じ方法をくり返したときに $\\mu$ を含む割合は高くなります。"
        "その代わり、推定できる範囲は広くなり、精度は低くなります。**")

# 12. 答案テンプレート
in_text("空欄付きのテンプレート",
        "*We are [confidence level]% confident that the population mean [quantity] "
        "lies between [lower bound] and [upper bound] [unit].*")
for _s in ("- **confidence level** … $90$、$95$、$99$ など",
           "- **population mean quantity** … **何の母平均か**",
           "- **lower and upper bounds** … GDC で得た区間の下限・上限",
           "- **unit** … g、hours、mg per litre など"):
    in_text("テンプレートの対応に " + _s[:18], _s)
in_text("不十分な答案の例",
        "*We are $95\\%$ confident that $\\mu$ is between $47.5$ and $49.7$.*")
in_text("不十分な理由 1", "- $\\mu$ が**何の平均か**が分からない")
in_text("不十分な理由 2", "- **単位**がない")
in_text("population mean と書く指示", "**`the population mean`** と書いておけば確実です")

# 13. 第9節の見出し
in_text("第9節の見出し", "### 9. 区間が重なっているときに言えること {#compare}")
in_text("9.2 と読める見出しは残っていない", "### 9. $2$ つの区間が重なるとき", want=False)

# 14. 重なりから言えること／言えないこと
in_text("等しいことの証明ではない",
        "**$2$ つの母平均が等しいことの証明ではありません。**")
in_text("この 2 つの区間だけを根拠に断定できない",
        "**この $2$ つの区間だけを根拠として**、「一方の母平均がもう一方より大きい」と"
        "**断定することはできません。**")
in_text("正式な検討には別の方法が要る",
        "$2$ 標本の $t$ 検定のような、別の推測統計の方法が必要になります")
eq("do not provide sufficient evidence の言い方",
   TXT.count("do not provide sufficient evidence"), 3)

# 15. Worked examples の共通手順
for _s in ("1. **Parameter** … 求める母平均 $\\mu$ が**何の平均か**と、その**単位**を確かめる",
           "2. **Conditions** … 母集団が normally distributed であることを確かめる",
           "3. **Method** … $\\sigma$ が既知なら $z$-interval、未知なら $t$-interval",
           "4. **Interpret** … 区間を、**文脈と単位を含む文**で答える"):
    in_text("4 段階に " + _s[:16], _s)
eq("Method の 1 行が各例題にある", TXT.count("*Method: $\\sigma$ is"), 11)
in_text("例題1 の margin of error の対応",
        "\\text{standard error} = \\frac{2.5}{\\sqrt{20}} = 0.559, \\qquad "
        "\\text{margin of error} = 1.96 \\times 0.559 = 1.10")
in_text("例題2 の margin of error の対応", "12.0 \\pm 2.365 \\times 0.100 = 12.0 \\pm 0.237")

# 16. 例題2 の丸め方と 3 段階
in_text("例題2 の丸め方",
        "電卓が返すのは $(11.7635,\\ 12.2365)$ です。**$3$ 桁**に丸めると、"
        "次のようになります（この問題では小数第1位までです）。")
in_text("例題2 (c) の 3 段階 1",
        "1. 得られた $95\\%$ confidence interval は $11.8 < \\mu < 12.2$ mg per litre")
in_text("例題2 (c) の 3 段階 2", "2. 主張された $12.5$ mg per litre は、上限 $12.2$ より**大きい**")
in_text("例題2 (c) の 3 段階 3", "3. したがって、この標本はその主張を**支持しない**")
in_text("not consistent with this sample は落とした",
        "is not consistent with this sample", want=False)

# 17. confidence と precision の使い分け
in_text("higher confidence の説明", "- **higher confidence** … confidence level が高い")
in_text("more precise の説明", "- **more precise** … 区間が狭い")
in_text("99% は higher confidence だが more precise ではない",
        "$99\\%$ 区間は higher confidence ですが、more precise ではありません")

# 18. Common errors の並び
_ce = TXT[TXT.index("## Common errors"):TXT.index("## Using your GDC")]
eq("Common errors は 10 項目", _ce.count("::: {.callout-warning}"), 10)
_order = [t for t in _re.findall(r"^## (.+)$", _ce, _re.M) if t != "Common errors"]
eq("Common errors の並び", _order == [
    "$\\sigma$ と $s$ を読みちがえる",
    "$n$ の大きさで $z$ と $t$ を選ぶ",
    "`df` を確かめない",
    "`C Level` に $95$ と入れる",
    "「$\\mu$ がこの区間に入る確率は $95\\%$」と書く",
    "母平均ではなく、$1$ つ $1$ つの値の区間だと解釈する",
    "文脈の言葉と単位を書かない",
    "区間が重なっているのに、「こちらが大きい」と結論する",
    "confidence level を上げれば、よい答えになると思う",
    "区間を、$1$ つの数で答える",
], True)
eq("各項目に「誤り」がある", _ce.count("**誤り**"), 10)
eq("各項目に「正しい判断」がある", _ce.count("**正しい判断**"), 10)

# 19. GDC の前の判断フローと 3 列の表
in_text("GDC 前の判断フロー", "## 電卓を開く前に、$2$ つ決めます")
in_text("Data か Stats かのフロー", "**生データ（数値の列）が与えられていますか。**")
in_text("z Interval の表が 3 列", "| 欄 | 意味 | 入力例（例題1） |")
in_text("t Interval Stats の表が 3 列", "| 欄 | 意味 | 入力例（例題3） |")
in_text("df の説明が GDC にもある",
        "これは **degrees of freedom**（自由度）で、$1$ 標本の $t$-interval では $n - 1$ です")

# 20. セルフチェック
in_text("セルフチェックの見出し", "### Exercises の前に — セルフチェック {#selfcheck}")
in_text("セルフチェック 1", "## 1. $\\sigma$ が与えられているとき、$z$ と $t$ のどちらを使いますか")
in_text("セルフチェック 2", "## 2. $95\\%$ confidence interval は「$\\mu$ が $95\\%$ の確率で入る」という意味ですか")
in_text("セルフチェック 3", "## 3. $n$ を大きくすると、区間の幅はどうなりますか")
_i_self = TXT.index("### Exercises の前に — セルフチェック")
_i_ex = TXT.index("## Exercises")
eq("セルフチェックは Exercises の直前", _i_self < _i_ex, True)

# 22. 要点のまとめと、次への一文
in_text("要点のまとめ", "## このページの要点")
in_text("次のページへの一文",
        "[AHL 4.18b](ahl-4-18b.qmd) の hypothesis testing（仮説検定）です")

# ── 表記の統一 ────────────────────────────────────────
for _t in ("**confidence interval**（信頼区間）", "**point estimate**（点推定値）",
           "**margin of error**（誤差の幅）", "**standard error**（標準誤差）",
           "**critical value**（臨界値）", "**confidence level**（信頼水準）",
           "**population standard deviation**（母標準偏差）",
           "**sample standard deviation**（標本標準偏差）",
           "**degrees of freedom**（自由度）", "**population mean**（母平均）"):
    in_text("用語の併記 " + _t[2:20], _t)
in_text("「臨界値」の単独使用が残っていない", "臨界値は", want=False)
in_text("「信頼水準」の単独使用が残っていない", "| 信頼水準 |", want=False)

# ── 構造の不変条件 ──────────────────────────────────────
_bad = [m for m in _re.findall(r"`[^`\n]+`", TXT) if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", _bad, [])
_L = TXT.split("\n")
_nb = [i + 1 for i, l in enumerate(_L)
       if _re.match(r"^:{3,} *\{", l) and i > 0
       and _L[i - 1].strip() != "" and not _L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", _nb, [])
eq("演習は 10 問", TXT.count("]{.ex-no}"), 10)
eq("区切りは 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 つ", TXT.count("::: {.exercise-block}"), 1)
_chapters = [l[3:] for i, l in enumerate(_L)
             if l.startswith("## ") and not (i and _L[i - 1].lstrip().startswith(":::"))]
eq("章見出しは _TEMPLATE の順どおり", _chapters == [
    "The idea", "Why it works", "Worked examples", "Common errors",
    "Using your GDC (TI-Nspire CX II)", "Exercises"], True)
_anchors = set(_re.findall(r"\{#([A-Za-z0-9\-]+)\}", TXT))
_links = set(_re.findall(r"\]\(#([A-Za-z0-9\-]+)\)", TXT))
eq("ページ内リンクの行き先がすべてある", sorted(_links - _anchors), [])
for _w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"):
    in_text("禁止語 " + _w + " が無い", _w, want=False)




# ══════════════════════════════════════════════════════════════
#  レビューで直した点（元に戻っていないか）
# ══════════════════════════════════════════════════════════════
in_text("重ならなくても等しさは否定されない",
        "**$\\mu_A = \\mu_B$ があり得ないと証明された**わけではありません")
in_text("「可能性は残りません」は残っていない",
        "$\\mu_A = \\mu_B$ という可能性は残りません", want=False)
in_text("plausible value の言い方は残っていない",
        "Every plausible value of $\\mu_A$", want=False)
in_text("区間の外の値が不可能ではない",
        "**区間の外の値が不可能だと証明されたわけではない**")
in_text("sigma/sqrt(n) は standard deviation そのもの",
        "$\\dfrac{\\sigma}{\\sqrt{n}}$ … sample mean の standard error"
        "（[AHL 4.15](ahl-4-15.qmd#narrower) で出てきた $\\bar{X}$ の standard deviation そのものです）")
in_text("s/sqrt(n) は推定した standard error",
        "$\\sigma$ を $s$ で置きかえて**推定した** standard error")
in_text("population とだけ書いてある、という誤ったルールは残っていない",
        "`population` と書いてあるときだけ $\\sigma$ です", want=False)
in_text("sample variance の注意がある", "## `sample variance` が与えられたときは、そのまま入れられません")
eq("s_(n-1)^2 = n/(n-1) s_n^2 の変換が書いてある",
   "s_{n-1}^{2} = \\dfrac{n}{n-1}s_n^{2}" in TXT, True)
in_text("演習9 の生の値", "生の値は $(495.07,\\ 504.93)$ と $(492.27,\\ 507.73)$ です。")
approx("演習9 90% 区間の下端", 500 - float(stats.norm.ppf(0.95)) * 3, 495.0654, 5e-4)
approx("演習9 90% 区間の上端", 500 + float(stats.norm.ppf(0.95)) * 3, 504.9346, 5e-4)
in_text("誤って丸めた値は残っていない", "(495.06,\\ 504.94)", want=False)
in_text("幅の比較に confidence level の条件がある",
        "**同じ confidence level で比べたとき**、狭いほどはっきりしたことが言えています")
eq("model answer に population mean が入っている",
   TXT.count("the population mean mass of a chocolate bar"), 5)
in_text("小数第1位に丸める、という独自ルールは残っていない",
        "区間も**小数第1位に丸めて**答えます", want=False)
in_text("z Interval にも Data / Stats がある",
        "**`Data Input Method` は、`z Interval` と同じく `Data` と `Stats` の $2$ 通り**です")
in_text("2 標本の比較は SL 4.11 へ",
        "[SL 4.11](../../ai-sl/04-statistics-and-probability/sl-4-11.qmd) の $2$ 標本の $t$ 検定")
in_text("電球は 100 時間単位", "in hundreds of hours")
in_text("日本語を display math に置いていない",
        "54.1 \\ \\text{から} \\ 55.8 \\ \\text{までが重なりです}", want=False)
in_text("シラバスの引用元を書いている", "シラバスの Guidance 欄が、はっきり指定しています")
in_text("例題1 に Parameter がある", "**Parameter.** 求めるのは、チョコレート $1$ 枚の**母平均の質量**")
eq("Parameter の行が 3 つある", TXT.count("**Parameter.**"), 3)
eq("Conditions の行が 3 つある", TXT.count("**Conditions.**"), 3)
in_text("WYSBATD が英語優先", "**$\\sigma$ が分かっているときは normal distribution、"
        "分からないときは $t$-distribution（$t$ 分布）**を使う")
in_text("問題文から crossref を外した",
        "Compare your answer with @exm-ahl416-overlap", want=False)
in_text("model answer から crossref を外した",
        "In @exm-ahl416-overlap the intervals overlapped", want=False)
in_text("critical value の表に df がある",
        "$t$ の critical value（$n = 8$、$\\text{df} = 7$）")

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
