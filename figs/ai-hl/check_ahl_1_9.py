"""AHL 1.9 の本文・例題・演習の数値を独立に検算する。
   log の法則そのものを使わずに、【定義にもどって】確かめるのが方針。
   たとえば log10(xy) = log10 x + log10 y は、両辺を 10 の指数にして
   xy と一致するかで見る。
   実行: python3 figs/ai-hl/check_ahl_1_9.py
"""
import math

ok, ng = 0, 0
TOL = 5e-10


def eq(name, got, want, tol=TOL):
    global ok, ng
    if isinstance(got, float) or isinstance(want, float):
        good = abs(got - want) < tol
    else:
        good = got == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


def sf(x, n=3):
    """有効数字 n 桁に丸める。"""
    if x == 0:
        return 0.0
    from decimal import Decimal
    d = math.floor(math.log10(abs(x)))
    return round(x, -(d - n + 1))


print("══════════ 3 つの法則を、定義にもどって確かめる ══════════")
# 積 → 和
for x, y in ((4, 25), (2, 3), (7, 11), (0.5, 8)):
    eq(f"log({x}·{y}) = log{x} + log{y}",
       math.log10(x * y), math.log10(x) + math.log10(y))
# 商 → 差
for x, y in ((100, 4), (3, 7), (1, 2)):
    eq(f"log({x}/{y}) = log{x} - log{y}",
       math.log10(x / y), math.log10(x) - math.log10(y))
# 累乗 → 前へ
for x, m in ((2, 5), (3, -2), (7, 0.5), (10, 3)):
    eq(f"log({x}^{m}) = {m}·log{x}",
       math.log10(x ** m), m * math.log10(x))
# ln でも同じ
eq("ln(6) = ln2 + ln3", math.log(6), math.log(2) + math.log(3))
eq("ln(2^10) = 10 ln2", math.log(2 ** 10), 10 * math.log(2))

print("══════════ よくある誤り（成り立たないこと） ══════════")
eq("log(3+4) ≠ log3 + log4",
   abs(math.log10(7) - (math.log10(3) + math.log10(4))) > 0.2, True)
eq("log(2·3) ≠ log2 · log3",
   abs(math.log10(6) - math.log10(2) * math.log10(3)) > 0.1, True)
eq("log(100/4) ≠ log100 / log4",
   abs(math.log10(25) - math.log10(100) / math.log10(4)) > 0.1, True)
eq("(log 1000)^2 ≠ 2 log 1000",
   abs(math.log10(1000) ** 2 - 2 * math.log10(1000)) > 0.1, True)

print("══════════ The idea の数値 ══════════")
eq("log 2 = 0.301 (3 s.f.)", sf(math.log10(2)), 0.301)
eq("log 3 = 0.477 (3 s.f.)", sf(math.log10(3)), 0.477)
eq("log 6 = 0.778 (3 s.f.)", sf(math.log10(6)), 0.778)
eq("0.301 + 0.477 = 0.778", round(0.301 + 0.477, 3), 0.778)
eq("log 500 = 2.70 (3 s.f.)", sf(math.log10(500)), 2.70)
eq("log 5 + log 100 = log 500",
   math.log10(5) + math.log10(100), math.log10(500))

print("══════════ 例題1：値を1つにまとめる ══════════")
# (a) log 8 + log 125
eq("(a) log8 + log125 = log1000 = 3",
   math.log10(8) + math.log10(125), 3.0)
eq("(a) 8 × 125 = 1000", 8 * 125, 1000)
# (b) log 200 - log 2
eq("(b) log200 - log2 = log100 = 2",
   math.log10(200) - math.log10(2), 2.0)
eq("(b) 200 / 2 = 100", 200 // 2, 100)
# (c) 3 log 2 + log 125
eq("(c) 3log2 = log8", 3 * math.log10(2), math.log10(8))
eq("(c) 3log2 + log125 = 3", 3 * math.log10(2) + math.log10(125), 3.0)

print("══════════ 例題2：1つの log にまとめる ══════════")
# 2 ln x + ln y = ln(x^2 y)
x, y = 3.0, 5.0
eq("2 ln x + ln y = ln(x^2 y)",
   2 * math.log(x) + math.log(y), math.log(x ** 2 * y))
eq("x^2 y = 45", x ** 2 * y, 45.0)
# ln x - 3 ln y = ln(x / y^3)
eq("ln x - 3 ln y = ln(x/y^3)",
   math.log(x) - 3 * math.log(y), math.log(x / y ** 3))
eq("x / y^3 = 0.024", x / y ** 3, 0.024)

print("══════════ 例題3：指数方程式を解く ══════════")
# 3(1.4)^t = 20
t = math.log10(20 / 3) / math.log10(1.4)
eq("3(1.4)^t = 20 → t = 5.638 (4 s.f.)", sf(t, 4), 5.638)
eq("t = 5.64 (3 s.f.)", sf(t), 5.64)
eq("検算 3(1.4)^t = 20", 3 * 1.4 ** t, 20.0, 1e-9)
eq("log(20/3) = log20 - log3",
   math.log10(20 / 3), math.log10(20) - math.log10(3))
# ln でも同じ答え
eq("ln で解いても同じ", math.log(20 / 3) / math.log(1.4), t, 1e-9)

print("══════════ 例題4：半減期 ══════════")
# 200 e^{-0.03t} = 50
t2 = math.log(50 / 200) / (-0.03)
eq("200 e^(-0.03t) = 50 → t = 46.21 (4 s.f.)", sf(t2, 4), 46.21)
eq("t = 46.2 (3 s.f.)", sf(t2), 46.2)
eq("検算 200 e^(-0.03t) = 50", 200 * math.exp(-0.03 * t2), 50.0, 1e-9)
eq("ln(1/4) = -ln 4", math.log(0.25), -math.log(4))
eq("ln 4 = 2 ln 2", math.log(4), 2 * math.log(2))
# 半減期そのもの
half = math.log(2) / 0.03
eq("半減期 = ln2/0.03 = 23.104...", sf(half, 5), 23.105)
eq("半減期 = 23.1 (3 s.f.)", sf(half), 23.1)

print("══════════ 例題5：桁数（AHL 2.10 への橋） ══════════")
# 2^100 の桁数
d = math.floor(100 * math.log10(2)) + 1
eq("100 log 2 = 30.10 (4 s.f.)", sf(100 * math.log10(2), 4), 30.10)
eq("2^100 は 31 桁", d, 31)
eq("2^100 の実際の桁数", len(str(2 ** 100)), 31)
eq("2^100 = 1.2676...×10^30",
   sf(2 ** 100 / 10 ** 30, 5), 1.2677)

print("══════════ Common errors で使う値 ══════════")
eq("log(3+4)=log7=0.845", sf(math.log10(7)), 0.845)
eq("log3+log4=log12=1.079", sf(math.log10(3) + math.log10(4), 4), 1.079)
eq("この 2 つは違う",
   abs(math.log10(7) - math.log10(12)) > 0.2, True)

print("══════════ 演習 ══════════")
# 1 まとめる
eq("1(a) log4 + log25 = 2", math.log10(4) + math.log10(25), 2.0)
eq("1(b) log60 - log6 = 1", math.log10(60) - math.log10(6), 1.0)
eq("1(c) 2log5 + log4 = 2", 2 * math.log10(5) + math.log10(4), 2.0)
eq("1(c) 5^2 × 4 = 100", 5 ** 2 * 4, 100)
# 2 1 つの log に
eq("2(a) 3ln a + ln b = ln(a^3 b)",
   3 * math.log(2.0) + math.log(7.0), math.log(2.0 ** 3 * 7.0))
eq("2(b) ln p - 2 ln q = ln(p/q^2)",
   math.log(9.0) - 2 * math.log(3.0), math.log(9.0 / 3.0 ** 2))
eq("2(b) 9/9 = 1 なので ln = 0", math.log(9.0 / 3.0 ** 2), 0.0)
# 3 指数方程式
t3 = math.log10(500 / 80) / math.log10(1.06)
eq("3 80(1.06)^n = 500 → n = 31.45 (4 s.f.)", sf(t3, 4), 31.45)
eq("3 n = 31.5 (3 s.f.)", sf(t3), 31.5)
eq("3 検算", 80 * 1.06 ** t3, 500.0, 1e-9)
eq("3 整数なら 32 年目", math.ceil(t3), 32)
eq("3 80(1.06)^31 < 500", 80 * 1.06 ** 31 < 500, True)
eq("3 80(1.06)^32 > 500", 80 * 1.06 ** 32 > 500, True)
# 4 e の方程式
t4 = math.log(0.1) / (-0.25)
eq("4 e^(-0.25t) = 0.1 → t = 9.2103...", sf(t4, 5), 9.2103)
eq("4 t = 9.21 (3 s.f.)", sf(t4), 9.21)
eq("4 検算", math.exp(-0.25 * t4), 0.1, 1e-12)
# 5 展開する
eq("5 log(x^3 y) = 3log x + log y",
   math.log10(2.0 ** 3 * 5.0), 3 * math.log10(2.0) + math.log10(5.0))
eq("5 log(x/y^2) = log x - 2 log y",
   math.log10(2.0 / 5.0 ** 2), math.log10(2.0) - 2 * math.log10(5.0))
# 6 値を求める（log 2 = p, log 3 = q）
p, q = math.log10(2), math.log10(3)
eq("6(a) log6 = p + q", math.log10(6), p + q)
eq("6(b) log 1.5 = q - p", math.log10(1.5), q - p)
eq("6(c) log 12 = 2p + q", math.log10(12), 2 * p + q)
eq("6(d) log 5 = 1 - p", math.log10(5), 1 - p)
# 7 なぜ成り立たないか
eq("7 log(10+10) = log20 = 1.301", sf(math.log10(20), 4), 1.301)
eq("7 log10 + log10 = 2", math.log10(10) + math.log10(10), 2.0)
eq("7 1.301 ≠ 2", abs(math.log10(20) - 2) > 0.5, True)
# 8 桁数
d8 = math.floor(50 * math.log10(3)) + 1
eq("8 50 log 3 = 23.856 (5 s.f.)", sf(50 * math.log10(3), 5), 23.856)
eq("8 3^50 は 24 桁", d8, 24)
eq("8 実際の桁数", len(str(3 ** 50)), 24)
# 9 文脈（薬）
t9 = math.log(0.2) / math.log(0.85)
eq("9 (0.85)^t = 0.2 → t = 9.9031 (5 s.f.)", sf(t9, 5), 9.9031)
eq("9 t = 9.90 (3 s.f.)", sf(t9), 9.90)
eq("9 検算", 0.85 ** t9, 0.2, 1e-12)
eq("9 10 時間目で初めて 20% 未満", 0.85 ** 10 < 0.2, True)
eq("9 9 時間では まだ 20% 以上", 0.85 ** 9 > 0.2, True)
# 10 log-log への橋
eq("10 log(2x^3) = log2 + 3log x",
   math.log10(2 * 4.0 ** 3), math.log10(2) + 3 * math.log10(4.0))
eq("10 傾き 3、切片 log2 = 0.301",
   sf(math.log10(2)), 0.301)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
