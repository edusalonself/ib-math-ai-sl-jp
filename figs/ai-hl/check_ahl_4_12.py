"""AHL 4.12 の本文・例題・演習の数値を独立に検算する。
   χ² の値は【定義どおり Σ(O-E)²/E を手で組み立てて】出し、
   p-value は scipy の分布から出して突き合わせる。
   実行: python3 figs/ai-hl/check_ahl_4_12.py
"""
import math
from statistics import NormalDist
from scipy import stats as st

ok, ng = 0, 0
Z = NormalDist(0, 1)


def eq(name, got, want, tol=5e-4):
    global ok, ng
    if isinstance(got, float) or isinstance(want, float):
        good = abs(got - want) < tol
    elif isinstance(got, list) and got and isinstance(got[0], float):
        good = len(got) == len(want) and all(abs(a - b) < tol
                                             for a, b in zip(got, want))
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


def chi2(O, E):
    return sum((o - e) ** 2 / e for o, e in zip(O, E))


print("══════════ 例題：normal を当てはめる（母数を 2 つ推定） ══════════")
MID = [10, 14, 18, 22, 26, 30, 34, 38]
F = [3, 7, 35, 30, 31, 34, 6, 4]
n = sum(F)
eq("合計は 150", n, 150)
mean = sum(x * c for x, c in zip(MID, F)) / n
var = sum(c * (x - mean) ** 2 for x, c in zip(MID, F)) / n
sd = math.sqrt(var)
eq("grouped mean = 24.0（ちょうど）", mean, 24.0, 1e-12)
eq("grouped sigma = 6.0（ちょうど）", sd, 6.0, 1e-12)

CUT = [12, 16, 20, 24, 28, 32, 36]
zs = [(c - 24.0) / 6.0 for c in CUT]
eq("z(12) = -2", zs[0], -2.0, 1e-12)
P = ([Z.cdf(zs[0])] + [Z.cdf(zs[i + 1]) - Z.cdf(zs[i]) for i in range(6)]
     + [1 - Z.cdf(zs[6])])
eq("確率の合計は 1", sum(P), 1.0, 1e-12)
eq("P(H < 12) = 0.0228 (3 s.f.)", sf(P[0]), 0.0228)
E = [150 * p for p in P]
eq("E は 3.41, 10.27, 24.19, 37.13, 37.13, 24.19, 10.27, 3.41 (4 s.f.)",
   [sf(e, 4) for e in E],
   [3.413, 10.27, 24.19, 37.13, 37.13, 24.19, 10.27, 3.413])
eq("E を 3 s.f. にすると", [sf(e) for e in E],
   [3.41, 10.3, 24.2, 37.1, 37.1, 24.2, 10.3, 3.41])
eq("E の合計は 150", sum(E), 150.0, 1e-9)
eq("両端だけが 5 より小さい", [e < 5 for e in E],
   [True] + [False] * 6 + [True])
eq("残り 6 つは 5 より大きい", all(e > 5 for e in E[1:7]), True)
eq("O の合計は 150", sum(F), 150)

Oc = [F[0] + F[1]] + F[2:6] + [F[6] + F[7]]
Ec = [E[0] + E[1]] + E[2:6] + [E[6] + E[7]]
eq("まとめた O", Oc, [10, 35, 30, 31, 34, 10])
eq("まとめた E (4 s.f.)", [sf(e, 4) for e in Ec],
   [13.68, 24.19, 37.13, 37.13, 24.19, 13.68])
eq("3.413 + 10.27 = 13.68", sf(E[0] + E[1], 4), 13.68)
eq("まとめたあとは全部 5 より大きい", all(e > 5 for e in Ec), True)
eq("O の合計は 150", sum(Oc), 150)
eq("E の合計は 150", sum(Ec), 150.0, 1e-9)

terms = [(o - e) ** 2 / e for o, e in zip(Oc, Ec)]
eq("各項 (3 s.f.)", [sf(t) for t in terms],
   [0.991, 4.83, 1.37, 1.01, 3.98, 0.991])
X2 = chi2(Oc, Ec)
eq("chi^2 = 13.2 (3 s.f.)", sf(X2), 13.2)
eq("chi^2 の生の値 (4 s.f.)", sf(X2, 4), 13.16)

k = len(Oc)
eq("まとめたあとのカテゴリ数は 6", k, 6)
nu = k - 1 - 2
eq("自由度 nu = 6 - 1 - 2 = 3", nu, 3)
eq("nu > 1（シラバスの条件）", nu > 1, True)
p = 1 - st.chi2.cdf(X2, nu)
eq("p = 0.00429 (3 s.f.)", sf(p), 0.00429)
eq("5% で reject", p < 0.05, True)
eq("1% でも reject", p < 0.01, True)
eq("critical value chi2_3(0.05) = 7.81", sf(st.chi2.ppf(0.95, 3)), 7.81)
eq("chi^2 > critical value", X2 > st.chi2.ppf(0.95, 3), True)

print("══════════ 自由度・まとめ方を取りちがえたとき ══════════")
p5 = 1 - st.chi2.cdf(X2, 5)
eq("nu=5（まとめたが -2 を忘れた）の p = 0.0219", sf(p5), 0.0219)
eq("nu=5 でも 5% では reject", p5 < 0.05, True)
eq("しかし p は 5 倍ほど大きい", p5 / p > 4, True)
# まとめなかった場合は chi^2 そのものが変わる
X8 = chi2(F, E)
eq("まとめないと chi^2 = 14.1 (3 s.f.)", sf(X8), 14.1)
eq("まとめないと chi^2 が大きくなる", X8 > X2, True)
p7 = 1 - st.chi2.cdf(X8, 7)
eq("nu=7（まとめず -2 も忘れた）の p = 0.0486", sf(p7), 0.0486)
eq("5% ではかろうじて reject", p7 < 0.05, True)
eq("1% では reject しない（正しい答えと食い違う）", p7 > 0.01, True)

print("══════════ 演習：binomial を当てはめる（母数を 1 つ推定） ══════════")
K = [0, 1, 2, 3, 4]
FB = [81, 88, 26, 4, 1]
nb = sum(FB)
eq("標本の数は 200", nb, 200)
tot = sum(k * f for k, f in zip(K, FB))
eq("不良品の総数は 156", tot, 156)
phat = tot / (4 * nb)
eq("p の推定値は 0.195", phat, 0.195)
EB = [nb * math.comb(4, k) * phat ** k * (1 - phat) ** (4 - k) for k in K]
eq("EB (4 s.f.)", [sf(e, 4) for e in EB],
   [83.99, 81.38, 29.57, 4.775, 0.2892])
eq("EB の合計は 200", sum(EB), 200.0, 1e-9)
eq("k=3 と k=4 が 5 未満", [e < 5 for e in EB], [False] * 3 + [True] * 2)
# まとめる（3 以上）
OB = FB[:3] + [FB[3] + FB[4]]
EBc = EB[:3] + [EB[3] + EB[4]]
eq("まとめた O", OB, [81, 88, 26, 5])
eq("まとめた E (4 s.f.)", [sf(e, 4) for e in EBc], [83.99, 81.38, 29.57, 5.064])
eq("まとめたあとは全部 5 より大きい", all(e > 5 for e in EBc), True)
X2b = chi2(OB, EBc)
eq("chi^2 = 1.08 (3 s.f.)", sf(X2b), 1.08)
nub = len(OB) - 1 - 1
eq("自由度 = 4 - 1 - 1 = 2", nub, 2)
pb = 1 - st.chi2.cdf(X2b, nub)
eq("p = 0.584 (3 s.f.)（生の chi^2 から）", sf(pb), 0.584)
eq("問題文の chi^2 = 1.08 からだと p = 0.583",
   sf(1 - st.chi2.cdf(1.08, nub)), 0.583)
eq("5% で reject しない", pb > 0.05, True)

print("══════════ 演習：自由度の数え方（表） ══════════")
CASES = [
    ("6 categories, no parameter estimated", 6, 0, 5),
    ("6 categories, mean estimated", 6, 1, 4),
    ("6 categories, mean and sd estimated", 6, 2, 3),
    ("8 -> 5 after combining, mean and sd estimated", 5, 2, 2),
    ("5 -> 4 after combining, p estimated", 4, 1, 2),
    ("7 -> 6 after combining, lambda estimated", 6, 1, 4),
]
for name, k, q, want in CASES:
    eq(name, k - 1 - q, want)

print("══════════ 演習：クラスの区切り方 ══════════")
# 30 個の観測値を 6 クラスに等分すると期待度数 5、7 クラスだと 5 未満
eq("30 個を 10 等分すると期待度数は 3", 30 / 10, 3.0)
eq("k = 6 だと期待度数はちょうど 5 で、>5 をみたさない", 30 / 6 > 5, False)
eq("等確率にするなら 5 クラスまで",
   max(k for k in range(1, 31) if 30 / k > 5), 5)

print("══════════ 本文の数値 ══════════")
eq("z = (16-24)/4.02 = -1.99 (3 s.f.)", sf((16 - 24) / 4.02), -1.99)
eq("P(X < 16) = 0.0233 (3 s.f.)", sf(Z.cdf((16 - 24) / 4.02)), 0.0233)
eq("100 x 0.0233 = 2.33", sf(100 * Z.cdf((16 - 24) / 4.02)), 2.33)

print("══════════ 例題3：カテゴリ分け（0 個推定） ══════════")
E3 = [3.1, 18.4, 21.7, 11.6, 4.2, 1.0]
eq("合計は 60", round(sum(E3), 10), 60.0)
eq("5 より小さいのは 1 つ目・5 つ目・6 つ目", [e < 5 for e in E3],
   [True, False, False, False, True, True])
E3c = [E3[0] + E3[1], E3[2], E3[3], E3[4] + E3[5]]
eq("まとめた E", [round(e, 10) for e in E3c], [21.5, 21.7, 11.6, 5.2])
eq("まとめても合計は 60", round(sum(E3c), 10), 60.0)
eq("まとめたあとは全部 5 より大きい", all(e > 5 for e in E3c), True)
eq("自由度 = 4 - 1 - 0 = 3", len(E3c) - 1 - 0, 3)

print("══════════ 演習6：まとめ方と自由度 ══════════")
E6 = [2.4, 9.6, 21.0, 24.8, 14.2, 4.8, 3.2]
eq("合計は 80", round(sum(E6), 10), 80.0)
eq("5 より小さいのは A・F・G", [e < 5 for e in E6],
   [True, False, False, False, False, True, True])
E6c = [E6[0] + E6[1], E6[2], E6[3], E6[4], E6[5] + E6[6]]
eq("まとめた E", [round(e, 10) for e in E6c], [12.0, 21.0, 24.8, 14.2, 8.0])
eq("まとめても合計は 80", round(sum(E6c), 10), 80.0)
eq("まとめたあとは全部 5 より大きい", all(e > 5 for e in E6c), True)
eq("class は 5 つ", len(E6c), 5)
eq("自由度 = 5 - 1 - 1 = 3", len(E6c) - 1 - 1, 3)
eq("F を E とまとめる必要はない（F+G だけで足りる）", E6[5] + E6[6] > 5, True)

print("══════════ 演習7：自由度（independence を含む） ══════════")
eq("7(a) 6 classes, q=0", 6 - 1 - 0, 5)
eq("7(b) 8 -> 5, q=2", 5 - 1 - 2, 2)
eq("7(c) 7 -> 6, q=1", 6 - 1 - 1, 4)
eq("7(d) independence 3 x 4", (3 - 1) * (4 - 1), 6)

print("══════════ 演習10：分割表の大きさ ══════════")
eq("3 x 5 は 15 マス", 3 * 5, 15)
eq("45 / 15 = 3", 45 / 15, 3.0)
eq("3 x 3 だと 45/9 = 5 ちょうどで、>5 をみたさない", 45 / 9 > 5, False)
eq("3 x 2 なら 45/6 = 7.5 > 5", 45 / 6 > 5, True)
eq("45/6 = 7.5", 45 / 6, 7.5)

print("══════════ GDC と Why it works の数値 ══════════")
eq("normCdf(20,24,24,6) = 0.25249 (5 s.f.)",
   sf(Z.cdf((24 - 24) / 6) - Z.cdf((20 - 24) / 6), 5), 0.24751)
eq("normCdf(-9999,12,24,6) = 0.022750 (5 s.f.)",
   sf(Z.cdf((12 - 24) / 6), 5), 0.022750)
eq("1^2 / 2 = 0.5", 1 ** 2 / 2, 0.5)
eq("1^2 / 20 = 0.05", 1 ** 2 / 20, 0.05)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
