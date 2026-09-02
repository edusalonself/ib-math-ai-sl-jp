"""AHL 4.13 の本文・例題・演習の数値を独立に検算する。
   回帰係数は【正規方程式を自分で組み立てて】出し、numpy の polyfit と
   突き合わせる。R^2 も 1 - SSres/SStot と、線形のときは r^2 の両方で確かめる。
   実行: python3 figs/ai-hl/check_ahl_4_13.py
"""
import math
import numpy as np

ok, ng = 0, 0


def eq(name, got, want, tol=1e-9):
    """数値は相対誤差で比べる。3 s.f. に丸めた値どうしなので、
       相対 1e-9 でぴったり一致するはず。"""
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


def polyfit_normal(x, y, deg):
    """正規方程式 (X^T X) c = X^T y を自分で解く。polyfit に頼らない。"""
    X = np.vstack([np.asarray(x, float) ** k for k in range(deg, -1, -1)]).T
    return np.linalg.solve(X.T @ X, X.T @ np.asarray(y, float))


def stats(y, yhat):
    y = np.asarray(y, float)
    yhat = np.asarray(yhat, float)
    ssr = float(((y - yhat) ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    return 1 - ssr / sst, ssr, sst


print("══════════ 例題1：residual と SS_res を手で出す ══════════")
X1 = np.array([1, 2, 3, 4, 5], float)
Y1 = np.array([4, 4, 8, 9, 10], float)
MODEL = 2 * X1 + 1
eq("モデルの値は 3,5,7,9,11", list(MODEL), [3, 5, 7, 9, 11])
res = Y1 - MODEL
eq("residual は 1,-1,1,0,-1", list(res), [1, -1, 1, 0, -1])
eq("residual の合計は 0（この例では）", float(res.sum()), 0.0)
eq("SS_res = 4", float((res ** 2).sum()), 4.0)
eq("ybar = 7", float(Y1.mean()), 7.0)
eq("SS_tot = 32", float(((Y1 - Y1.mean()) ** 2).sum()), 32.0)
R1, ssr1, sst1 = stats(Y1, MODEL)
eq("R^2 = 1 - 4/32 = 0.875", R1, 0.875)

# 最小二乗の直線
c1 = polyfit_normal(X1, Y1, 1)
eq("最小二乗の直線 y = 1.7x + 1.9", [float(c1[0]), float(c1[1])], [1.7, 1.9])
eq("polyfit と一致", [float(v) for v in np.polyfit(X1, Y1, 1)],
   [float(c1[0]), float(c1[1])])
R1b, ssr1b, _ = stats(Y1, np.polyval(c1, X1))
eq("その SS_res = 3.1", ssr1b, 3.1)
eq("3.1 < 4（最小二乗のほうが小さい）", ssr1b < 4.0, True)
eq("その R^2 = 0.903 (3 s.f.)", sf(R1b), 0.903)
r1 = float(np.corrcoef(X1, Y1)[0, 1])
eq("r = 0.950 (3 s.f.)", sf(r1), 0.950)
eq("r^2 = R^2（線形モデル）", r1 * r1, R1b, 1e-12)
eq("r^2 = 0.903 (3 s.f.)", sf(r1 * r1), 0.903)

print("══════════ 例題2：quadratic（価格と利益） ══════════")
X2 = np.array([2, 4, 6, 8, 10, 12], float)
P2 = np.array([78, 150, 199, 191, 160, 72], float)
c2 = polyfit_normal(X2, P2, 2)
eq("a = -5.00 (3 s.f.)", sf(float(c2[0])), -5.00)
eq("b = 69.9 (3 s.f.)", sf(float(c2[1])), 69.9)
eq("c = -44.2 (3 s.f.)", sf(float(c2[2])), -44.2)
eq("polyfit と一致", [float(v) for v in np.polyfit(X2, P2, 2)],
   [float(v) for v in c2])
R2q, ssr2, sst2 = stats(P2, np.polyval(c2, X2))
eq("R^2 = 0.993 (3 s.f.)", sf(R2q), 0.993)
eq("SS_res = 99.1 (3 s.f.)", sf(ssr2), 99.1)
vx = -float(c2[1]) / (2 * float(c2[0]))
eq("頂点の x = 6.99 (3 s.f.)", sf(vx), 6.99)
eq("そのときの P = 200 (3 s.f.)", sf(float(np.polyval(c2, vx))), 200.0)
eq("P(5) = 180 (3 s.f.)", sf(float(np.polyval(c2, 5))), 180.0)
# 直線を当てはめると意味がない
c2l = polyfit_normal(X2, P2, 1)
R2l, _, _ = stats(P2, np.polyval(c2l, X2))
eq("直線の R^2 は 0.0000608 (3 s.f.)", sf(R2l), 0.0000608)
eq("直線の R^2 はほとんど 0", R2l < 0.001, True)

print("══════════ 例題3：linear と exponential を比べる（車の価値） ══════════")
T = np.array([0, 1, 2, 3, 4, 5], float)
V = np.array([24400, 20000, 15700, 12700, 10800, 8200], float)
cL = polyfit_normal(T, V, 1)
eq("linear の傾き -3190 (3 s.f.)", sf(float(cL[0])), -3190.0)
eq("linear の切片 23300 (3 s.f.)", sf(float(cL[1])), 23300.0)
RL, ssrL, sstL = stats(V, np.polyval(cL, T))
eq("linear R^2 = 0.975 (3 s.f.)", sf(RL), 0.975)
eq("linear SS_res = 4560000 (3 s.f.)", sf(ssrL), 4560000.0)
rL = float(np.corrcoef(T, V)[0, 1])
eq("linear r = -0.987 (3 s.f.)", sf(rL), -0.987)
eq("r^2 = R^2", rL * rL, RL, 1e-12)

# exponential：log を取って直線に直す（多くの電卓と同じやり方）
be, ae = np.polyfit(T, np.log(V), 1)
A, B = float(np.exp(ae)), float(np.exp(be))
eq("exp の a = 24500 (3 s.f.)", sf(A), 24500.0)
eq("exp の b = 0.807 (3 s.f.)", sf(B), 0.807)
RE, ssrE, _ = stats(V, A * B ** T)
eq("exp R^2 = 0.998 (3 s.f.)", sf(RE), 0.998)
eq("exp SS_res = 359000 (3 s.f.)", sf(ssrE), 359000.0)
eq("exp のほうが SS_res が小さい", ssrE < ssrL, True)
eq("exp のほうが R^2 が大きい", RE > RL, True)

eq("linear の t=8 は -2240 (3 s.f.)", sf(float(np.polyval(cL, 8))), -2240.0)
eq("linear の t=8 は負（車の価値としてありえない）",
   float(np.polyval(cL, 8)) < 0, True)
eq("exp の t=8 は 4400 (3 s.f.)", sf(A * B ** 8), 4400.0)
eq("exp はいつも正", all(A * B ** tt > 0 for tt in range(0, 30)), True)

print("══════════ 例題3(d)：R^2 が大きいほうがよいとはかぎらない ══════════")
cC = polyfit_normal(T, V, 3)
RC, ssrC, _ = stats(V, np.polyval(cC, T))
eq("cubic R^2 = 0.998 (3 s.f.)", sf(RC), 0.998)
eq("cubic R^2 の生の値 (5 s.f.)", sf(RC, 5), 0.99824)
eq("exp R^2 の生の値 (5 s.f.)", sf(RE, 5), 0.99803)
eq("cubic の R^2 のほうが大きい", RC > RE, True)

# 本文 §8 理由2 の表は quadratic と cubic を並べる（どちらも多項式なので、
# 電卓が log を取るかどうかの違いに左右されない）。
cQ = polyfit_normal(T, V, 2)
RQ, ssrQ, _ = stats(V, np.polyval(cQ, T))
eq("§8表 quadratic R^2 (5 s.f.)", sf(RQ, 5), 0.99759)
eq("§8表 quadratic の t=10 は 9100 (3 s.f.)",
   sf(float(np.polyval(cQ, 10))), 9100.0)
eq("§8表 quadratic の t=10 は正", float(np.polyval(cQ, 10)) > 0, True)
eq("cubic > quadratic だが、cubic の外挿は負",
   (RC > RQ) and (float(np.polyval(cC, 10)) < 0)
   and (float(np.polyval(cQ, 10)) > 0), True)
eq("その差は 0.001 未満", (RC - RQ) < 0.001, True)
eq("cubic SS_res = 322000 (3 s.f.)", sf(ssrC), 322000.0)
eq("cubic の t=10 は -7260 (3 s.f.)", sf(float(np.polyval(cC, 10))), -7260.0)
eq("cubic の t=10 は負", float(np.polyval(cC, 10)) < 0, True)
eq("exp の t=10 は 2860 (3 s.f.)", sf(A * B ** 10), 2860.0)
eq("R^2 が大きいほうが、外では役に立たない", (RC > RE) and
   (float(np.polyval(cC, 10)) < 0) and (A * B ** 10 > 0), True)
eq("cubic は係数 4 個、exp は 2 個", (4, 2), (4, 2))

print("══════════ 例題4：sinusoidal（日照時間） ══════════")
M = np.arange(1, 13, dtype=float)
D = np.array([9.1, 10.2, 11.9, 13.7, 15.2, 15.9, 15.4, 14.0,
              12.2, 10.5, 9.3, 8.8])
eq("データは 12 個", len(D), 12)
eq("最大は 15.9、最小は 8.8", (float(D.max()), float(D.min())), (15.9, 8.8))
eq("振幅の目安 (max-min)/2 = 3.55", (float(D.max()) - float(D.min())) / 2, 3.55)
eq("中心の目安 (max+min)/2 = 12.35", (float(D.max()) + float(D.min())) / 2,
   12.35)
# 電卓の SinReg にあたる非線形当てはめ
from scipy.optimize import curve_fit
f = lambda x, a, b, c, d: a * np.sin(b * x + c) + d
pars, _ = curve_fit(f, M, D, p0=[3.5, 2 * math.pi / 12, -1.8, 12.3],
                    maxfev=40000)
a, b, c, d = [float(v) for v in pars]
eq("a = 3.47 (3 s.f.)", sf(a), 3.47)
eq("b = 0.547 (3 s.f.)", sf(b), 0.547)
eq("c = -1.76 (3 s.f.)", sf(c), -1.76)
eq("d = 12.3 (3 s.f.)", sf(d), 12.3)
RS, ssrS, sstS = stats(D, f(M, *pars))
eq("R^2 = 0.999 (3 s.f.)", sf(RS), 0.999)
eq("SS_res = 0.0396 (3 s.f.)", sf(ssrS), 0.0396)
per = 2 * math.pi / b
eq("周期 = 11.5 (3 s.f.)", sf(per), 11.5)
eq("周期は 12 に近い", abs(per - 12) < 1, True)
eq("a は (max-min)/2 に近い", abs(a - 3.55) < 0.15, True)
eq("d は (max+min)/2 に近い", abs(d - 12.35) < 0.1, True)
eq("m=14 の予測は 11.0 (3 s.f.)", sf(float(f(14, *pars))), 11.0)

print("══════════ 演習：power model（振り子） ══════════")
L = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2], float)
TP = np.array([0.90, 1.27, 1.55, 1.80, 2.01, 2.20], float)
bp, ap = np.polyfit(np.log(L), np.log(TP), 1)
Ap, Bp = float(np.exp(ap)), float(bp)
eq("power の a = 2.01 (3 s.f.)", sf(Ap), 2.01)
eq("power の n = 0.499 (3 s.f.)", sf(Bp), 0.499)
RP, ssrP, _ = stats(TP, Ap * L ** Bp)
eq("R^2 = 1.00 (3 s.f.)", sf(RP), 1.00)
eq("R^2 の生の値 (5 s.f.)", sf(RP, 5), 0.99995)
eq("n はほぼ 0.5（平方根）", abs(Bp - 0.5) < 0.01, True)
eq("L = 1.5 の予測は 2.46 (3 s.f.)", sf(Ap * 1.5 ** Bp), 2.46)

print("══════════ 演習：R^2 と r の関係 ══════════")
for r in (0.9, -0.9, 0.6, -0.6, 0.0):
    eq(f"r = {r} なら r^2 = {round(r*r,2)}", round(r * r, 10),
       round(r * r, 10))
eq("R^2 = 0.81 から r = ±0.9", round(math.sqrt(0.81), 10), 0.9)
eq("R^2 からは r の符号が決まらない", True, True)
eq("R^2 は 0 以上 1 以下", (0 <= 0.975 <= 1), True)

print("══════════ 演習2：与えられたモデル yhat = 3x - 2 ══════════")
X2e = np.array([1, 2, 3, 4], float)
Y2e = np.array([2, 5, 8, 12], float)
yh2 = 3 * X2e - 2
res2 = Y2e - yh2
eq("演習2 residual", [float(v) for v in res2], [1.0, 1.0, 1.0, 2.0])
eq("演習2 SS_res = 7", float((res2 ** 2).sum()), 7.0)
eq("演習2 ybar = 6.75", float(Y2e.mean()), 6.75)
sst2 = float(((Y2e - Y2e.mean()) ** 2).sum())
eq("演習2 SS_tot = 54.75", sst2, 54.75)
eq("演習2 の 2 乗の内訳", [round(float(v), 4) for v in (Y2e - Y2e.mean()) ** 2],
   [22.5625, 3.0625, 1.5625, 27.5625])
eq("演習2 R^2 = 0.872 (3 s.f.)", sf(1 - 7 / sst2), 0.872)

print("══════════ 演習5：次数を上げても R^2 は下がらない ══════════")
eq("0.968 <= 0.971（表の値）", 0.968 <= 0.971, True)
eq("『必ず増える』ではなく『減らない』",
   "cannot decrease", "cannot decrease")
# 反例：点が完全に直線上にあれば linear/quadratic/cubic とも R^2 = 1
Xc = np.array([1, 2, 3, 4, 5], float)
Yc = 2 * Xc + 1
r2s = [stats(Yc, np.polyval(polyfit_normal(Xc, Yc, d), Xc))[0]
       for d in (1, 2, 3)]
eq("直線上のデータでは 3 つとも R^2 = 1（増えない反例）",
   [round(v, 9) for v in r2s], [1.0, 1.0, 1.0])

print("══════════ 演習6：バクテリア（exponential） ══════════")
T6 = np.arange(0, 6, dtype=float)
N6 = np.array([50, 79, 126, 199, 318, 501], float)
c6 = np.polyfit(T6, np.log(N6), 1)
A6, B6 = math.exp(c6[1]), math.exp(c6[0])
eq("演習6 a = 49.9 (3 s.f.)", sf(A6), 49.9)
eq("演習6 b = 1.59 (3 s.f.)", sf(B6), 1.59)
R6, _, _ = stats(N6, A6 * B6 ** T6)
eq("演習6 R^2 = 1.00 (3 s.f.)", sf(R6), 1.0)
eq("演習6 R^2 は 0.9999 より上", R6 > 0.9999, True)
eq("演習6 毎時およそ 59% 増（1.59 倍）", round((B6 - 1) * 100), 59)

print("══════════ 演習10：冷めるコーヒー（exponential） ══════════")
T10 = np.array([0, 5, 10, 15, 20, 25], float)
TH = np.array([85, 67, 54, 45, 38, 33], float)
c10 = np.polyfit(T10, np.log(TH), 1)
A10, B10 = math.exp(c10[1]), math.exp(c10[0])
eq("演習10 a = 81.6 (3 s.f.)", sf(A10), 81.6)
eq("演習10 b = 0.963 (3 s.f.)", sf(B10), 0.963)
R10, _, _ = stats(TH, A10 * B10 ** T10)
eq("演習10 R^2 = 0.990 (3 s.f.)", sf(R10), 0.990)
eq("演習10 t=60 の予測は 8.45 (3 s.f.)", sf(A10 * B10 ** 60), 8.45)
eq("演習10 の予測は室温 20 度を下回る（ありえない）",
   A10 * B10 ** 60 < 20, True)

print("══════════ 本文の追加主張 ══════════")
# Degree モードで SinReg を走らせたときの b と 2pi/b
from scipy.optimize import curve_fit as _cf
Md = np.arange(1, 13, dtype=float)
Dd = np.array([9.1, 10.2, 11.9, 13.7, 15.2, 15.9, 15.4, 14.0,
               12.2, 10.5, 9.3, 8.8])
pd_, _ = _cf(lambda m, a, b, c, d: a * np.sin(np.radians(b * m + c)) + d,
             Md, Dd, p0=[3.5, 30.0, -100.0, 12.3], maxfev=200000)
eq("Degree モードの b は 31.4 前後", round(float(pd_[1]), 1), 31.4)
eq("そのとき 2pi/b は 0.2 (1 s.f.)", sf(2 * math.pi / float(pd_[1]), 1), 0.2)
eq("Degree での正しい周期 360/b は 11.5 (3 s.f.)",
   sf(360 / float(pd_[1])), 11.5)

# quadratic は t = 7 あたりで底を打って上を向く
Tq = np.array([0, 1, 2, 3, 4, 5], float)
Vq = np.array([24400, 20000, 15700, 12700, 10800, 8200], float)
cQ2 = polyfit_normal(Tq, Vq, 2)
vertq = -cQ2[1] / (2 * cQ2[0])
eq("quadratic の頂点は t = 7.30 (3 s.f.)", sf(float(vertq)), 7.30)
eq("quadratic は t=7 のあと上を向く",
   float(np.polyval(cQ2, 8)) > float(np.polyval(cQ2, 7)), True)

# exponential / power の R^2 を log スケールで計算すると値が変わる
be_, ae_ = np.polyfit(Tq, np.log(Vq), 1)
lv = np.log(Vq); pv = np.polyval([be_, ae_], Tq)
r2trans = 1 - ((lv - pv) ** 2).sum() / ((lv - lv.mean()) ** 2).sum()
eq("車の exp：log スケールの R^2 は 0.997 (3 s.f.)", sf(r2trans), 0.997)
eq("どちらの出し方でも linear の 0.975 より大きい", r2trans > 0.975, True)

Tc = np.array([0, 5, 10, 15, 20, 25], float)
Hc = np.array([85, 67, 54, 45, 38, 33], float)
cc_ = np.polyfit(Tc, np.log(Hc), 1)
lh = np.log(Hc); ph = np.polyval(cc_, Tc)
eq("コーヒー：log スケールの R^2 は 0.991 (3 s.f.)",
   sf(1 - ((lh - ph) ** 2).sum() / ((lh - lh.mean()) ** 2).sum()), 0.991)

# 演習3
eq("演習3 R^2 = (-0.84)^2 = 0.706 (3 s.f.)", sf(0.84 ** 2), 0.706)
eq("演習3 の生の値は 0.7056", round(0.84 ** 2, 4), 0.7056)

# 例題3 の丸め注意：3 s.f. の係数で代入すると 3 桁目が変わる
cLr = polyfit_normal(Tq, Vq, 1)
eq("丸めた係数だと -2220、丸めないと -2240",
   (sf(-3190 * 8 + 23300), sf(float(np.polyval(cLr, 8)))),
   (-2220.0, -2240.0))

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
