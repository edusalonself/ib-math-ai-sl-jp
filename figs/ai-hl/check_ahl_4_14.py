"""AHL 4.14 の本文・例題・演習の数値を独立に検算する。

   E と Var は【定義から】計算する。つまり、確率分布を実際に作って
   E(X) = Σ x P(X=x)、Var(X) = Σ (x-μ)^2 P(X=x) を数え上げ、
   そのうえで aX+b の分布を作り直して E と Var を出す。
   公式 E(aX+b)=aE(X)+b、Var(aX+b)=a^2Var(X) は【使わずに】確かめる。

   実行: python3 figs/ai-hl/check_ahl_4_14.py
"""
import math
import itertools
import numpy as np

ok, ng = 0, 0


def eq(name, got, want, tol=1e-9):
    """数値は相対誤差で比べる。"""
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


def sf(x, n=3):
    if x == 0:
        return 0.0
    d = math.floor(math.log10(abs(x)))
    return round(x, -(d - n + 1))


# ── 分布を「値と確率の対」で持ち、定義どおりに E と Var を出す ──────
def EV(dist):
    """dist = {value: prob}。(E, Var) を定義から返す。"""
    tot = sum(dist.values())
    assert abs(tot - 1) < 1e-12, f"確率の合計が {tot}"
    mu = sum(x * p for x, p in dist.items())
    var = sum((x - mu) ** 2 * p for x, p in dist.items())
    return mu, var


def transform(dist, a, b):
    """aX + b の分布を作り直す（公式を使わない）。"""
    out = {}
    for x, p in dist.items():
        out[a * x + b] = out.get(a * x + b, 0.0) + p
    return out


def combine(d1, d2, a, b):
    """独立な X, Y から aX + bY の分布を作る（同時分布を全部たどる）。"""
    out = {}
    for x, px in d1.items():
        for y, py in d2.items():
            v = a * x + b * y
            out[v] = out.get(v, 0.0) + px * py
    return out


def binomial(n, p):
    return {k: math.comb(n, k) * p ** k * (1 - p) ** (n - k)
            for k in range(n + 1)}


print("══════════ 定義から公式そのものを確かめる ══════════")
# 適当な分布を 3 つ用意して、公式が本当に成り立つかを数え上げで見る
D1 = {1: 0.2, 3: 0.5, 7: 0.3}
D2 = {0: 0.4, 2: 0.35, 5: 0.25}
D3 = binomial(6, 0.4)

for name, D in (("D1", D1), ("D2", D2), ("D3=B(6,0.4)", D3)):
    mu, var = EV(D)
    for a, b in ((3, 5), (-2, 1), (0.5, -2), (1, 0)):
        m2, v2 = EV(transform(D, a, b))
        eq(f"{name}: E({a}X+{b}) = {a}E(X)+{b}", m2, a * mu + b)
        eq(f"{name}: Var({a}X+{b}) = {a}^2 Var(X)", v2, a * a * var)

# 線形結合（独立）
m1, v1 = EV(D1)
m2_, v2_ = EV(D2)
for a, b in ((1, 1), (1, -1), (2, -3), (-1, 4)):
    mc, vc = EV(combine(D1, D2, a, b))
    eq(f"E({a}X+({b})Y) = {a}E(X)+({b})E(Y)", mc, a * m1 + b * m2_)
    eq(f"Var({a}X+({b})Y) = {a}^2Var(X)+{b}^2Var(Y)  ← 符号は必ず +",
       vc, a * a * v1 + b * b * v2_)

# 2X と X1+X2 は違う（同じ分布から）
mA, vA = EV(transform(D1, 2, 0))
mB, vB = EV(combine(D1, D1, 1, 1))
eq("2X と X1+X2 の平均は等しい", mA, mB)
eq("2X の分散は X1+X2 の 2 倍", vA, 2 * vB)
eq("Var(2X) = 4Var(X)", vA, 4 * v1)
eq("Var(X1+X2) = 2Var(X)", vB, 2 * v1)

print("══════════ 本文：SL 4.3 の表との対応 ══════════")
mu1, var1 = EV(D1)
eq("c を足すと Var は変わらない", EV(transform(D1, 1, 9))[1], var1)
eq("c を足すと E は c 増える", EV(transform(D1, 1, 9))[0], mu1 + 9)
eq("k 倍すると Var は k^2 倍", EV(transform(D1, 3, 0))[1], 9 * var1)
eq("k 倍すると sd は |k| 倍", math.sqrt(EV(transform(D1, -3, 0))[1]),
   3 * math.sqrt(var1))

print("══════════ 例題1：E(X)=12, Var(X)=9 ══════════")
EX, VX = 12.0, 9.0
eq("sd(X) = 3", math.sqrt(VX), 3.0)
eq("E(3X+5) = 41", 3 * EX + 5, 41.0)
eq("Var(3X+5) = 81", 9 * VX, 81.0)
eq("sd(3X+5) = 9", math.sqrt(9 * VX), 9.0)
eq("E(-2X+1) = -23", -2 * EX + 1, -23.0)
eq("Var(-2X+1) = 36", 4 * VX, 36.0)
eq("sd(-2X+1) = 6（負にならない）", math.sqrt(4 * VX), 6.0)
eq("sd は |a| 倍：|-2| x 3 = 6", abs(-2) * 3, 6.0)

print("══════════ 例題2：タクシー料金 F = 2.2X + 3.5 ══════════")
EXd, SDd = 6.5, 2.5
eq("Var(X) = 6.25", SDd ** 2, 6.25)
eq("E(F) = 17.80", 2.2 * EXd + 3.5, 17.80)
eq("sd(F) = 5.50", 2.2 * SDd, 5.50)
eq("Var(F) = 30.25", 2.2 ** 2 * SDd ** 2, 30.25)
eq("Var(F) = sd(F)^2", 2.2 ** 2 * SDd ** 2, (2.2 * SDd) ** 2)
# b を変えても Var は変わらない（b = 3.5 と b = 5 で比べる）
eq("b を 3.5 から 5 にしても Var は同じ",
   EV(transform({6.5 - 2.5: 0.5, 6.5 + 2.5: 0.5}, 2.2, 5.0))[1],
   EV(transform({6.5 - 2.5: 0.5, 6.5 + 2.5: 0.5}, 2.2, 3.5))[1])
eq("例題2(c) 新しい平均 = 19.30", 2.2 * EXd + 5.0, 19.30)
eq("例題2(c) 平均は 1.50 増える", (2.2 * EXd + 5.0) - (2.2 * EXd + 3.5), 1.50)
eq("例題2(c) sd は 5.50 のまま", 2.2 * SDd, 5.50)

print("══════════ 例題3：独立な X, Y の線形結合 ══════════")
EXx, VXx, EYy, VYy = 20.0, 16.0, 8.0, 9.0
eq("E(2X-3Y) = 16", 2 * EXx - 3 * EYy, 16.0)
eq("Var(2X-3Y) = 145", 4 * VXx + 9 * VYy, 145.0)
eq("  内訳 64 + 81", (4 * VXx, 9 * VYy), (64.0, 81.0))
eq("sd(2X-3Y) = 12.0 (3 s.f.)", sf(math.sqrt(145)), 12.0)
eq("sd の生の値は 12.0416", round(math.sqrt(145), 4), 12.0416)
eq("引き算でも足す（145 であって 64-81 ではない）", 4 * VXx + 9 * VYy > 0, True)
eq("E(X+Y) = 28", EXx + EYy, 28.0)
eq("E(X-Y) = 12", EXx - EYy, 12.0)
eq("Var(X+Y) = Var(X-Y) = 25", (VXx + VYy, VXx + VYy), (25.0, 25.0))

print("══════════ 例題4：2X と X1+X2（袋づめ） ══════════")
EB, SDB = 5.0, 0.2
VB = SDB ** 2
eq("Var(X) = 0.04", VB, 0.04)
eq("E(X1+X2) = 10", 2 * EB, 10.0)
eq("Var(X1+X2) = 0.08", 2 * VB, 0.08)
eq("sd(X1+X2) = 0.283 (3 s.f.)", sf(math.sqrt(2 * VB)), 0.283)
eq("E(2X) = 10（同じ）", 2 * EB, 10.0)
eq("Var(2X) = 0.16", 4 * VB, 0.16)
eq("sd(2X) = 0.4", math.sqrt(4 * VB), 0.4)
eq("Var(2X) は Var(X1+X2) の 2 倍", 4 * VB, 2 * (2 * VB))
eq("sd の比は sqrt(2)", (4 * VB) ** 0.5 / (2 * VB) ** 0.5, math.sqrt(2))
# 10 袋
eq("E(10 袋の合計) = 50", 10 * EB, 50.0)
eq("Var(10 袋の合計) = 0.4", 10 * VB, 0.4)
eq("sd(10 袋の合計) = 0.632 (3 s.f.)", sf(math.sqrt(10 * VB)), 0.632)
eq("sd は 0.2 x sqrt(10)", math.sqrt(10 * VB), 0.2 * math.sqrt(10))

print("══════════ 本文：不偏推定（8 個のデータ） ══════════")
S8 = np.array([12, 15, 11, 18, 14, 16, 13, 17], float)
n8 = len(S8)
xbar = S8.mean()
SS8 = ((S8 - xbar) ** 2).sum()
eq("n = 8", int(n8), 8)
eq("xbar = 14.5", float(xbar), 14.5)
eq("合計は 116", float(S8.sum()), 116.0)
eq("偏差の 2 乗の合計 = 42", float(SS8), 42.0)
eq("sn^2 (= sigma_x^2) = 5.25", float(SS8 / n8), 5.25)
eq("sigma_x = 2.29 (3 s.f.)", sf(math.sqrt(SS8 / n8)), 2.29)
eq("s_{n-1}^2 = 6（ちょうど）", float(SS8 / (n8 - 1)), 6.0)
eq("s_{n-1} = 2.45 (3 s.f.)", sf(math.sqrt(SS8 / (n8 - 1))), 2.45)
eq("公式集の n/(n-1) sn^2 と一致",
   float(n8 / (n8 - 1) * SS8 / n8), float(SS8 / (n8 - 1)))
eq("s_{n-1} は sigma_x より大きい",
   math.sqrt(SS8 / (n8 - 1)) > math.sqrt(SS8 / n8), True)
eq("電卓の s_x は s_{n-1} と同じもの",
   float(np.std(S8, ddof=1)), math.sqrt(SS8 / (n8 - 1)))
eq("電卓の sigma_x は sn と同じもの",
   float(np.std(S8, ddof=0)), math.sqrt(SS8 / n8))

print("══════════ 不偏であることの実験（n-1 が正しいことの確認） ══════════")
# 小さな母集団から、大きさ n の標本を【全部】取り出して平均を見る
POP = np.array([2, 4, 6, 8, 10], float)   # 母集団（5 個）
mu_pop = POP.mean()
var_pop = ((POP - mu_pop) ** 2).mean()     # 母分散
eq("母平均 mu = 6", float(mu_pop), 6.0)
eq("母分散 sigma^2 = 8", float(var_pop), 8.0)

for nsmp in (2, 3):
    smps = list(itertools.product(POP, repeat=nsmp))   # 復元抽出：全通り
    means = np.array([np.mean(s) for s in smps])
    v_n = np.array([np.var(s, ddof=0) for s in smps])
    v_n1 = np.array([np.var(s, ddof=1) for s in smps])
    eq(f"n={nsmp}: E(xbar) = mu", float(means.mean()), float(mu_pop))
    eq(f"n={nsmp}: E(sn^2) = (n-1)/n sigma^2（小さすぎる）",
       float(v_n.mean()), float((nsmp - 1) / nsmp * var_pop))
    eq(f"n={nsmp}: E(s_(n-1)^2) = sigma^2（ちょうど）",
       float(v_n1.mean()), float(var_pop))
    eq(f"n={nsmp}: sn^2 は平均して小さめに出る",
       float(v_n.mean()) < float(var_pop), True)

print("══════════ 演習1〜3 ══════════")
eq("演習1 E(2X+7) = 37", 2 * 15 + 7, 37.0)
eq("演習1 Var(2X+7) = 16", 4 * 4, 16.0)
eq("演習1 sd(2X+7) = 4", math.sqrt(16), 4.0)
eq("演習2 Var(X) = 25", 5.0 ** 2, 25.0)
eq("演習2 E(0.5X-2) = 13", 0.5 * 30 - 2, 13.0)
eq("演習2 Var(0.5X-2) = 6.25", 0.25 * 25, 6.25)
eq("演習2 sd(0.5X-2) = 2.5", math.sqrt(6.25), 2.5)
ET, SDT = 84000.0, 12000.0
eq("演習3 E(P) = 8600", 0.4 * ET - 25000, 8600.0)
eq("演習3 sd(P) = 4800", 0.4 * SDT, 4800.0)
eq("演習3 Var(P) = 23040000", 0.16 * SDT ** 2, 23040000.0)
eq("演習3(c) 固定費 28000 での平均 = 5600", 0.4 * ET - 28000, 5600.0)
eq("演習3(c) 平均は 3000 減る",
   (0.4 * ET - 25000) - (0.4 * ET - 28000), 3000.0)
eq("演習3(c) sd は 4800 のまま（b を変えても変わらない）",
   EV(transform({ET - SDT: 0.5, ET + SDT: 0.5}, 0.4, -28000))[1] ** 0.5,
   EV(transform({ET - SDT: 0.5, ET + SDT: 0.5}, 0.4, -25000))[1] ** 0.5)

print("══════════ 演習4〜6 ══════════")
eq("演習4 E(X+Y) = 16", 10 + 6, 16.0)
eq("演習4 Var(X+Y) = 8", 3 + 5, 8.0)
eq("演習4 E(X-Y) = 4", 10 - 6, 4.0)
eq("演習4 Var(X-Y) = 8（同じ）", 3 + 5, 8.0)
eq("演習4 和と差で Var が等しい（数え上げ）",
   EV(combine(D1, D2, 1, 1))[1], EV(combine(D1, D2, 1, -1))[1])
eq("演習4 sd = 2.83 (3 s.f.)", sf(math.sqrt(8)), 2.83)
# 演習6：部品 3 個
EP6, SDP6 = 4.2, 0.15
VP6 = SDP6 ** 2
eq("演習6 Var(X) = 0.0225", VP6, 0.0225)
eq("演習6 E(合計) = 12.6", 3 * EP6, 12.6)
eq("演習6 Var(合計) = 0.0675", 3 * VP6, 0.0675)
eq("演習6 sd(合計) = 0.260 (3 s.f.)", sf(math.sqrt(3 * VP6)), 0.260)
eq("演習6 E(3X) = 12.6（同じ）", 3 * EP6, 12.6)
eq("演習6 Var(3X) = 0.2025", 9 * VP6, 0.2025)
eq("演習6 sd(3X) = 0.45", math.sqrt(9 * VP6), 0.45)
eq("演習6 Var(3X) は 3 倍", 9 * VP6, 3 * (3 * VP6))

print("══════════ 演習7〜10 ══════════")
S5 = np.array([22, 25, 19, 24, 20], float)
eq("演習7 xbar = 22", float(S5.mean()), 22.0)
SS5 = ((S5 - S5.mean()) ** 2).sum()
eq("演習7 偏差の 2 乗の合計 = 26", float(SS5), 26.0)
eq("演習7 s_{n-1}^2 = 6.5", float(SS5 / 4), 6.5)
eq("演習7 s_{n-1} = 2.55 (3 s.f.)", sf(math.sqrt(SS5 / 4)), 2.55)
eq("演習7 sigma_x^2 = 5.2（これは不偏でない）", float(SS5 / 5), 5.2)
eq("演習8 sn^2 = 12.96", 3.6 ** 2, 12.96)
eq("演習8 s_{n-1}^2 = 14.4", 10 / 9 * 3.6 ** 2, 14.4)
eq("演習8 s_{n-1} = 3.79 (3 s.f.)", sf(math.sqrt(14.4)), 3.79)
# 演習9：binomial
n9, p9 = 50, 0.3
mb, vb = EV(binomial(n9, p9))
eq("演習9 E(X) = np = 15", mb, 15.0)
eq("演習9 Var(X) = np(1-p) = 10.5", vb, 10.5)
eq("演習9 E(2X+1) = 31", 2 * 15 + 1, 31.0)
eq("演習9 Var(2X+1) = 42", 4 * 10.5, 42.0)
eq("演習9 sd(2X+1) = 6.48 (3 s.f.)", sf(math.sqrt(42)), 6.48)
# 演習10
E10, V10 = 8.0, 2.0
eq("演習10 E(3X) = 24", 3 * E10, 24.0)
eq("演習10 E(X1+X2+X3) = 24（同じ）", 3 * E10, 24.0)
eq("演習10 Var(3X) = 18", 9 * V10, 18.0)
eq("演習10 Var(X1+X2+X3) = 6", 3 * V10, 6.0)
eq("演習10 sd(3X) = 4.24 (3 s.f.)", sf(math.sqrt(18)), 4.24)
eq("演習10 sd(合計) = 2.45 (3 s.f.)", sf(math.sqrt(6)), 2.45)
eq("演習10 Var(3X) は 3 倍", 9 * V10, 3 * (3 * V10))
# 数え上げでも確かめる（E(X)=8, Var(X)=2 をもつ分布を 1 つ作る）
D10 = {6: 0.25, 8: 0.5, 10: 0.25}
eq("演習10 用の分布は E=8, Var=2", EV(D10), (8.0, 2.0))
eq("演習10 数え上げ Var(3X) = 18", EV(transform(D10, 3, 0))[1], 18.0)
eq("演習10 数え上げ Var(X1+X2+X3) = 6",
   EV(combine(combine(D10, D10, 1, 1), D10, 1, 1))[1], 6.0)

print("══════════ 独立でないと Var の公式が崩れることの確認 ══════════")
# X と Y = X（完全に従属）。Var(X+Y) = Var(2X) = 4Var(X) ≠ 2Var(X)
eq("従属なら Var(X+X) = 4Var(X)、2Var(X) ではない",
   EV(transform(D1, 2, 0))[1], 4 * v1)
eq("  独立なら 2Var(X)", EV(combine(D1, D1, 1, 1))[1], 2 * v1)
eq("  2 つは一致しない", abs(4 * v1 - 2 * v1) > 1e-9, True)

print("══════════ 図の数値 ══════════")
# ahl-4-14-2x.svg で描いている分布は、本文どおり sd = 0.2 か
BV = np.array([4.6, 4.8, 5.0, 5.2, 5.4])
BPr = np.array([0.05, 0.30, 0.30, 0.30, 0.05])
eq("図の確率の合計 = 1", float(BPr.sum()), 1.0)
bmf = float((BV * BPr).sum())
bvf = float((((BV - bmf) ** 2) * BPr).sum())
eq("図の袋の平均 = 5", bmf, 5.0)
eq("図の袋の sd = 0.2（本文と一致）", math.sqrt(bvf), 0.2)
eq("図の 2X の sd = 0.4", math.sqrt(4 * bvf), 0.4)
eq("図の X1+X2 の sd = 0.283 (3 s.f.)", sf(math.sqrt(2 * bvf)), 0.283)

# ahl-4-14-transform.svg のラベル
XSf = np.array([1, 2, 3, 4, 5], float)
PSf = np.array([0.1, 0.2, 0.4, 0.2, 0.1])
muf = float((XSf * PSf).sum())
vf = float((((XSf - muf) ** 2) * PSf).sum())
eq("図 transform の平均 = 3", muf, 3.0)
eq("図 transform の sd = 1.10 (3 s.f.)", sf(math.sqrt(vf)), 1.10)
eq("図 X+3 の平均 = 6", muf + 3, 6.0)
eq("図 X+3 の sd は変わらない", math.sqrt(vf), math.sqrt(vf))
eq("図 2X の平均 = 6", 2 * muf, 6.0)
eq("図 2X の sd = 2.19 (3 s.f.)", sf(2 * math.sqrt(vf)), 2.19)

# ahl-4-14-unbiased.svg 左パネルの 2 つの平方和
smpf = np.array([53.0, 57.0, 62.0, 64.0])
eq("図 unbiased の xbar = 59", float(smpf.mean()), 59.0)
eq("図 mu = 50 から測った平方和 = 398",
   float(((smpf - 50.0) ** 2).sum()), 398.0)
eq("図 xbar から測った平方和 = 74",
   float(((smpf - smpf.mean()) ** 2).sum()), 74.0)
eq("xbar から測ったほうが小さい",
   float(((smpf - smpf.mean()) ** 2).sum())
   < float(((smpf - 50.0) ** 2).sum()), True)
# xbar が平方和を最小にすることを、総当たりで確かめる
cands = np.linspace(40, 80, 4001)
best = cands[np.argmin([((smpf - c) ** 2).sum() for c in cands])]
eq("平方和を最小にする点は xbar", round(float(best), 2), 59.0)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
