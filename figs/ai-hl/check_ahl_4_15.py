"""AHL 4.15 の本文・例題・演習の数値を独立に検算する。

   ★ AI では z 値を使わない（SL 4.9 のシラバス）。だからこの検算でも、
     答えは電卓の normCdf(a, b, mu, sigma) と同じ形で出す。
   ★ 正規分布の確率は、math.erf から作った関数と scipy の両方で出して
     突き合わせる（片方だけを信じない）。
   ★ 和・差・標本平均の分布は、【モンテカルロでも】確かめる。
     公式 N(mu1+mu2, s1^2+s2^2) を仮定せずに、実際に足して分布を見る。

   実行: python3 figs/ai-hl/check_ahl_4_15.py
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
    """モンテカルロ用：絶対誤差 tol まで許す。"""
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


def Phi(x):
    """標準正規の累積分布を erf から作る（scipy に頼らない）。"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normcdf(a, b, mu, sd):
    """電卓の normCdf(a, b, mu, sd) と同じもの。両方の実装で一致を見る。"""
    lo = -math.inf if a is None else a
    hi = math.inf if b is None else b
    mine = ((1.0 if hi == math.inf else Phi((hi - mu) / sd))
            - (0.0 if lo == -math.inf else Phi((lo - mu) / sd)))
    theirs = float(stats.norm.cdf(hi, mu, sd) - stats.norm.cdf(lo, mu, sd))
    assert abs(mine - theirs) < 1e-12, f"erf と scipy が食い違う: {mine} {theirs}"
    return mine


def invnorm(p, mu, sd):
    return float(stats.norm.ppf(p, mu, sd))


rng = np.random.default_rng(20260901)
N = 4_000_000


print("══════════ 独立な normal の和・差が normal になることの確認 ══════════")
# 公式を仮定せず、実際に乱数を足して、平均・分散・正規性を見る
a = rng.normal(30.0, 4.0, N)
b = rng.normal(27.0, 3.0, N)
approx("和の平均 = 30 + 27 = 57", float((a + b).mean()), 57.0, 0.02)
approx("和の分散 = 16 + 9 = 25", float((a + b).var()), 25.0, 0.05)
approx("差の平均 = 30 - 27 = 3", float((a - b).mean()), 3.0, 0.02)
approx("差の分散も 25（引かない）", float((a - b).var()), 25.0, 0.05)
# 正規性：いくつかの点で、経験累積と正規累積が一致するか
for q in (-2.0, -1.0, 0.0, 1.0, 2.0):
    x = 3.0 + q * 5.0
    approx(f"差の分布は N(3, 5^2)：P(D < {x:.0f}) が一致",
           float((a - b < x).mean()), normcdf(None, x, 3.0, 5.0), 0.002)

print("══════════ 標本平均 Xbar ~ N(mu, sigma^2/n) の確認 ══════════")
for n in (4, 9, 25):
    d = rng.normal(1000.0, 12.0, size=(400_000, n))
    xb = d.mean(axis=1)
    approx(f"n={n}: Xbar の平均 = 1000", float(xb.mean()), 1000.0, 0.05)
    approx(f"n={n}: Xbar の分散 = 144/{n}", float(xb.var()), 144.0 / n, 0.15)
    approx(f"n={n}: Xbar の sd = 12/sqrt({n})",
           float(xb.std()), 12.0 / math.sqrt(n), 0.03)
eq("n=9 のとき sd = 4（ちょうど）", 12.0 / math.sqrt(9), 4.0)
eq("n=16 のとき sd = 1.25", 5.0 / math.sqrt(16), 1.25)
eq("n=25 のとき sd = 4", 20.0 / math.sqrt(25), 4.0)
eq("sd は sigma/sqrt(n)、sigma/n ではない",
   12.0 / math.sqrt(9) != 12.0 / 9, True)

print("══════════ 例題1：主菜 + 副菜の合計 ══════════")
MM, SM, MS_, SS2 = 250.0, 8.0, 180.0, 6.0
eq("Var(M) = 64", SM ** 2, 64.0)
eq("Var(S) = 36", SS2 ** 2, 36.0)
eq("合計の平均 = 430", MM + MS_, 430.0)
eq("合計の分散 = 64 + 36 = 100", SM ** 2 + SS2 ** 2, 100.0)
eq("合計の sd = 10（ちょうど）", math.sqrt(100.0), 10.0)
eq("sd を足す誤りなら 14 になる", SM + SS2, 14.0)
eq("正しい 10 とは違う", math.sqrt(100.0) != SM + SS2, True)
pA = normcdf(445, None, 430.0, 10.0)
eq("P(T > 445) = 0.0668 (3 s.f.)", sf(pA), 0.0668)
eq("  生の値 0.066807", round(pA, 6), 0.066807)
pB = normcdf(420, 445, 430.0, 10.0)
eq("P(420 < T < 445) = 0.775 (3 s.f.)", sf(pB), 0.775)
eq("  生の値 0.77454", round(pB, 5), 0.77454)
approx("  モンテカルロ（和）",
       float((rng.normal(250, 8, N) + rng.normal(180, 6, N) > 445).mean()),
       pA, 0.001)
_t = rng.normal(250, 8, N) + rng.normal(180, 6, N)   # 同じ標本で両条件を見る
approx("  モンテカルロ（区間）",
       float(((_t > 420) & (_t < 445)).mean()), pB, 0.002)

print("══════════ 本文：2 杯の合計と 2X の違い（4.14 との橋渡し） ══════════")
MU1, SD1 = 250.0, 8.0
eq("2 杯の和の分散 = 128", 2 * SD1 ** 2, 128.0)
eq("和の sd = 11.3 (3 s.f.)", sf(math.sqrt(128)), 11.3)
eq("和の sd の生の値 = 11.3137", round(math.sqrt(128), 4), 11.3137)
p1 = normcdf(510, None, 500.0, math.sqrt(128))
eq("P(和 > 510) = 0.188 (3 s.f.)", sf(p1), 0.188)
eq("  生の値 0.18838", round(p1, 5), 0.18838)
eq("2X の分散は 256 で、和の 128 とは違う", 4 * SD1 ** 2, 256.0)
p1b = normcdf(510, None, 500.0, 16.0)
eq("2X なら P(>510) = 0.266 (3 s.f.)", sf(p1b), 0.266)
eq("  生の値 0.26599", round(p1b, 5), 0.26599)
eq("2X のほうが確率が大きい", p1b > p1, True)

print("══════════ 例題2：電池 A と B の差 ══════════")
MA, SA, MB, SB = 30.0, 4.0, 27.0, 3.0
eq("D = A - B の平均 = 3", MA - MB, 3.0)
eq("D の分散 = 16 + 9 = 25", SA ** 2 + SB ** 2, 25.0)
eq("D の sd = 5（ちょうど）", math.sqrt(25.0), 5.0)
p2 = normcdf(0, None, 3.0, 5.0)
eq("P(A > B) = P(D > 0) = 0.726 (3 s.f.)", sf(p2), 0.726)
eq("  生の値 0.72575", round(p2, 5), 0.72575)
p2b = normcdf(5, None, 3.0, 5.0)
eq("P(D > 5) = 0.345 (3 s.f.)", sf(p2b), 0.345)
eq("  生の値 0.34458", round(p2b, 5), 0.34458)
approx("P(A>B) モンテカルロ",
       float((rng.normal(30, 4, N) > rng.normal(27, 3, N)).mean()), p2, 0.001)
eq("分散を引くと 7 になり、これは誤り", SA ** 2 - SB ** 2, 7.0)
eq("sd を足すと 7 になり、これも誤り", SA + SB, 7.0)
eq("正しい sd は 5 で、7 ではない", math.sqrt(25.0) != 7.0, True)

print("══════════ 例題3：砂糖 9 袋の標本平均 ══════════")
MS, SS_, NS = 1000.0, 12.0, 9
eq("Xbar の平均 = 1000", MS, 1000.0)
eq("Xbar の分散 = 144/9 = 16", SS_ ** 2 / NS, 16.0)
eq("Xbar の sd = 4", math.sqrt(SS_ ** 2 / NS), 4.0)
p3 = normcdf(None, 995, 1000.0, 4.0)
eq("P(Xbar < 995) = 0.106 (3 s.f.)", sf(p3), 0.106)
eq("  生の値 0.10565", round(p3, 5), 0.10565)
p3b = normcdf(None, 995, 1000.0, 12.0)
eq("1 袋なら P(X < 995) = 0.338 (3 s.f.)", sf(p3b), 0.338)
eq("  生の値 0.33846", round(p3b, 5), 0.33846)
eq("標本平均のほうが起こりにくい", p3 < p3b, True)
approx("P(Xbar<995) モンテカルロ",
       float((rng.normal(1000, 12, size=(600_000, 9)).mean(axis=1)
              < 995).mean()), p3, 0.002)

print("══════════ 例題4：CLT（もとが normal でない） ══════════")
MC, SC, NC = 4.2, 2.5, 40
eq("Xbar の平均 = 4.2", MC, 4.2)
eq("Xbar の分散 = 6.25/40 = 0.15625", SC ** 2 / NC, 0.15625)
eq("Xbar の sd = 0.395 (3 s.f.)", sf(math.sqrt(SC ** 2 / NC)), 0.395)
eq("  生の値 0.39528", round(math.sqrt(SC ** 2 / NC), 5), 0.39528)
p4 = normcdf(4.5, None, MC, math.sqrt(SC ** 2 / NC))
eq("P(Xbar > 4.5) = 0.224 (3 s.f.)", sf(p4), 0.224)
eq("  生の値 0.22394", round(p4, 5), 0.22394)
# 合計で考えても同じ
eq("合計の平均 = 168", NC * MC, 168.0)
eq("合計の分散 = 250", NC * SC ** 2, 250.0)
eq("合計の sd = 15.8 (3 s.f.)", sf(math.sqrt(250)), 15.8)
p4b = normcdf(180, None, 168.0, math.sqrt(250))
eq("P(合計 > 180) は P(Xbar > 4.5) と同じ", p4b, p4)
eq("  180 = 40 x 4.5", NC * 4.5, 180.0)
eq("n = 40 > 30 なので CLT が使える", NC > 30, True)
# CLT が実際に効いていることを、歪んだ分布で確かめる
skew = rng.exponential(1.0, size=(200_000, NC))   # 平均 1、sd 1 の指数分布
sb = skew.mean(axis=1)
# 指数分布は右に歪んでいるので、中央のずれは n=40 でもまだ残る。
# 「完全に正規になる」のではなく「正規に近づく」ことを確かめる。
approx("指数分布 n=40：+1sd の位置がほぼ正規どおり",
       float((sb < 1.0 + 1.0 / math.sqrt(NC)).mean()), Phi(1.0), 0.02)
approx("指数分布 n=40：-1sd の位置がほぼ正規どおり",
       float((sb < 1.0 - 1.0 / math.sqrt(NC)).mean()), Phi(-1.0), 0.02)
sb2 = rng.exponential(1.0, size=(200_000, 4)).mean(axis=1)
eq("n=4 より n=40 のほうが正規に近い",
   abs(float((sb < 1.0 + 1 / math.sqrt(40)).mean()) - Phi(1.0))
   < abs(float((sb2 < 1.0 + 1 / 2.0).mean()) - Phi(1.0)), True)

print("══════════ CLT：n が大きいほど正規に近づく ══════════")
for n, tol in ((2, 0.10), (10, 0.05), (30, 0.03), (100, 0.02)):
    s = rng.exponential(1.0, size=(200_000, n)).mean(axis=1)
    d = abs(float((s < 1.0 + 1.0 / math.sqrt(n)).mean()) - Phi(1.0))
    approx(f"n={n}: 正規からのずれが {tol} 未満", d, 0.0, tol)

print("══════════ 演習1〜3 ══════════")
MX, SX, MY, SY = 50.0, 5.0, 30.0, 12.0
eq("演習1 X+Y の平均 = 80", MX + MY, 80.0)
eq("演習1 X+Y の分散 = 25+144 = 169", SX ** 2 + SY ** 2, 169.0)
eq("演習1 X+Y の sd = 13", math.sqrt(169.0), 13.0)
eq("演習1 X-Y の平均 = 20", MX - MY, 20.0)
eq("演習1 X-Y の分散も 169", SX ** 2 + SY ** 2, 169.0)
p5 = normcdf(95, None, 80.0, 13.0)
eq("演習2 P(X+Y > 95) = 0.124 (3 s.f.)", sf(p5), 0.124)
eq("  生の値 0.12428", round(p5, 5), 0.12428)
eq("演習3 Xbar の分散 = 25/16", 5.0 ** 2 / 16, 1.5625)
eq("演習3 Xbar の sd = 1.25", math.sqrt(1.5625), 1.25)
p6 = normcdf(21.5, None, 20.0, 1.25)
eq("演習3 P(Xbar > 21.5) = 0.115 (3 s.f.)", sf(p6), 0.115)
eq("  生の値 0.11507", round(p6, 5), 0.11507)

print("══════════ 演習4〜6 ══════════")
MBx, SBx, MCn, SCn = 0.4, 0.05, 2.5, 0.2
eq("演習4 合計の平均 = 2.9", MBx + MCn, 2.9)
eq("演習4 合計の分散 = 0.0025+0.04 = 0.0425", SBx ** 2 + SCn ** 2, 0.0425)
eq("演習4 合計の sd = 0.206 (3 s.f.)", sf(math.sqrt(0.0425)), 0.206)
eq("  生の値 0.20616", round(math.sqrt(0.0425), 5), 0.20616)
p7 = normcdf(3.0, None, 2.9, math.sqrt(0.0425))
eq("演習4 P(合計 > 3) = 0.314 (3 s.f.)", sf(p7), 0.314)
eq("  生の値 0.31381", round(p7, 5), 0.31381)
eq("演習5 Xbar の sd は sigma/sqrt(n)", 12.0 / math.sqrt(9), 4.0)
MC6, SC6, NC6 = 8.4, 3.6, 50
eq("演習6 Xbar の分散 = 12.96/50 = 0.2592", SC6 ** 2 / NC6, 0.2592)
eq("演習6 Xbar の sd = 0.509 (3 s.f.)", sf(math.sqrt(0.2592)), 0.509)
eq("  生の値 0.50912", round(math.sqrt(0.2592), 5), 0.50912)
p8 = normcdf(None, 8.0, MC6, math.sqrt(0.2592))
eq("演習6 P(Xbar < 8) = 0.216 (3 s.f.)", sf(p8), 0.216)
eq("  生の値 0.21603", round(p8, 5), 0.21603)
eq("演習6 n = 50 > 30", NC6 > 30, True)

print("══════════ 演習8〜10 ══════════")
M8, S8v = 10.0, 2.0
eq("演習8 3X の平均 = 30", 3 * M8, 30.0)
eq("演習8 3X の分散 = 36", 9 * S8v ** 2, 36.0)
eq("演習8 3X の sd = 6", math.sqrt(36.0), 6.0)
eq("演習8 和の平均 = 30（同じ）", 3 * M8, 30.0)
eq("演習8 和の分散 = 12", 3 * S8v ** 2, 12.0)
eq("演習8 和の sd = 3.46 (3 s.f.)", sf(math.sqrt(12)), 3.46)
p9 = normcdf(36, None, 30.0, 6.0)
p9b = normcdf(36, None, 30.0, math.sqrt(12))
eq("演習8 P(3X > 36) = 0.159 (3 s.f.)", sf(p9), 0.159)
eq("  生の値 0.15866", round(p9, 5), 0.15866)
eq("演習8 P(和 > 36) = 0.0416 (3 s.f.)", sf(p9b), 0.0416)
eq("  生の値 0.041632", round(p9b, 6), 0.041632)
eq("演習8 3X のほうが起こりやすい", p9 > p9b, True)
# 演習9：invNorm
eq("演習9 Xbar の分散 = 400/25 = 16", 20.0 ** 2 / 25, 16.0)
eq("演習9 Xbar の sd = 4", math.sqrt(16.0), 4.0)
k = invnorm(0.95, 500.0, 4.0)
eq("演習9 k = 507 (3 s.f.)", sf(k), 507.0)
eq("  生の値 506.58", round(k, 2), 506.58)
eq("演習9 検算：P(Xbar > k) = 0.05",
   round(normcdf(k, None, 500.0, 4.0), 10), 0.05)
# 演習10：エレベーター
M10, S10, N10, LIM = 72.0, 10.0, 8, 620.0
eq("演習10 合計の平均 = 576", N10 * M10, 576.0)
eq("演習10 合計の分散 = 800", N10 * S10 ** 2, 800.0)
eq("演習10 合計の sd = 28.3 (3 s.f.)", sf(math.sqrt(800)), 28.3)
eq("  生の値 28.284", round(math.sqrt(800), 3), 28.284)
p10 = normcdf(LIM, None, 576.0, math.sqrt(800))
eq("演習10 P(合計 > 620) = 0.0599 (3 s.f.)", sf(p10), 0.0599)
eq("  生の値 0.059897", round(p10, 6), 0.059897)
approx("演習10 モンテカルロ",
       float((rng.normal(72, 10, size=(600_000, 8)).sum(axis=1)
              > 620).mean()), p10, 0.002)
eq("演習10 8X としたら分散 6400 で誤り", 64 * S10 ** 2, 6400.0)
eq("演習10 その場合 sd = 80", math.sqrt(6400.0), 80.0)

print("══════════ よくある誤りが、実際に別の値になることの確認 ══════════")
eq("sd を足す誤り：4+3=7 と、正しい 5 は違う", 4.0 + 3.0 != 5.0, True)
eq("Xbar の sd を sigma/n とする誤り：12/9 と 12/3 は違う",
   12.0 / 9 != 12.0 / 3, True)
eq("normCdf に分散を入れる誤り：128 と 11.3137 は違う",
   128.0 != math.sqrt(128.0), True)
wrong = normcdf(510, None, 500.0, 128.0)
eq("  分散を入れると P = 0.469 になってしまう", sf(wrong), 0.469)
eq("  正しい 0.188 とは大きく違う", abs(wrong - p1) > 0.2, True)

print("══════════ Common errors に書いた「誤った答え」も検算する ══════════")
# 例題1で sigma のかわりに分散 100 を入れてしまった場合
wrong1 = normcdf(445, None, 430.0, 100.0)
eq("分散 100 を入れると 0.440 (3 s.f.)", sf(wrong1), 0.440)
eq("  正しい 0.0668 とは大きく違う", abs(wrong1 - pA) > 0.3, True)
# 演習2で分散 169 を入れてしまった場合
wrong2 = normcdf(95, None, 80.0, 169.0)
eq("分散 169 を入れると 0.465 (3 s.f.)", sf(wrong2), 0.465)
eq("  正しい 0.124 とは大きく違う", abs(wrong2 - p5) > 0.3, True)
# 演習9で 0.05 をそのまま入れてしまった場合
eq("invNorm(0.05, 500, 4) = 493 (3 s.f.)", sf(invnorm(0.05, 500.0, 4.0)), 493.0)
eq("  それは平均 500 より下", invnorm(0.05, 500.0, 4.0) < 500.0, True)
# 演習3の「1 つの観測値なら」の注意
eq("演習3 1 つの X なら P(X > 21.5) = 0.382 (3 s.f.)",
   sf(normcdf(21.5, None, 20.0, 5.0)), 0.382)
# 演習10 の誤った 8X との sd 比
eq("演習10 誤った sd 80 は正しい 28.3 の 2.83 倍",
   round(80.0 / math.sqrt(800), 2), 2.83)
eq("  「3 倍近く」であって「ちょうど 3 倍」ではない",
   abs(80.0 / math.sqrt(800) - 3.0) > 0.1, True)
# 演習4：箱のばらつきは中身の 1/16
eq("演習4 分散の比は 0.04 / 0.0025 = 16", 0.04 / 0.0025, 16.0)
eq("演習4 箱を無視しても sd は 0.200",
   round(math.sqrt(0.04), 3), 0.200)
eq("演習4 箱を入れると 0.206", sf(math.sqrt(0.0425)), 0.206)
# 例題2/3 の検算コメント
eq("例題2 E(D) = 3 > 0 なので P(D>0) > 0.5", p2 > 0.5, True)
eq("例題3 sd が 12 -> 4 に減ると確率も減る", p3 < p3b, True)
# GDC 第4節の例
eq("invNorm(0.90, 60, 2.5) = 63.2 (3 s.f.)",
   sf(invnorm(0.90, 60.0, 2.5)), 63.2)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
