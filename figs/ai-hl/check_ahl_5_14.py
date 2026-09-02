"""AHL 5.14（微分方程式を立てる・変数分離）の数値をぜんぶ検算する。
   実行: python3 figs/ai-hl/check_ahl_5_14.py

   方針:
     (1) 解いた式を【sympy で微分して】もとの微分方程式に戻るか確かめる
         ——これが微分方程式の唯一まともな検算なので、全例題・全演習でやる
     (2) 数値は、閉じた式と数値計算の 2 通りで出して突き合わせる
     (3) 条件（初期値・2 点め）を、解の式に代入して満たすか確かめる
     (4) 最後に .qmd を読んで、本文にその数値が書かれているかを確かめる
"""
import math
import os

import sympy as sp

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


t = sp.symbols("t", positive=True)


def verify_ode(name, sol, rhs, var=t):
    """★ 解 sol を微分して、右辺 rhs（sol を代入したもの）と一致するか。"""
    global ok, ng
    lhs = sp.simplify(sp.diff(sol, var))
    want = sp.simplify(rhs)
    good = sp.simplify(lhs - want) == 0
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   d/dt = {lhs}   but rhs = {want}"))
    ok, ng = ok + good, ng + (not good)


print("══════════ 例題2：藻 dG/dt = k√G ══════════")
G = (t + 2) ** 2
verify_ode("G = (t+2)^2 は dG/dt = 2√G を満たす", G, 2 * sp.sqrt(G))
eq("G(0) = 4", int(G.subs(t, 0)), 4)
eq("G(2) = 16", int(G.subs(t, 2)), 16)
eq("G(5) = 49", int(G.subs(t, 5)), 49)
# ★ 定数の決まり方を、式から追う
eq("2√G = kt + C で、t=0, G=4 から C = 4", 2 * sp.sqrt(4), 4)
eq("t=2, G=16 から 2(4) = 2k + 4、つまり k = 2",
   sp.solve(sp.Eq(2 * 4, 2 * sp.Symbol("k") + 4), sp.Symbol("k")), [2])
# ★ 1/√G の積分は ln ではない（Common error）
GG = sp.Symbol("G", positive=True)
eq("∫G^(-1/2)dG = 2√G", sp.simplify(sp.integrate(GG ** sp.Rational(-1, 2), GG)
                                    - 2 * sp.sqrt(GG)), 0)
eq("  それは ln ではない",
   sp.simplify(sp.integrate(GG ** sp.Rational(-1, 2), GG) - sp.log(GG)) != 0,
   True)

print("══════════ 例題3：dP/dt = kP（指数） ══════════")
K3 = sp.Rational(15, 100)
P = 500 * sp.exp(K3 * t)
verify_ode("P = 500e^{0.15t} は dP/dt = 0.15P を満たす", P, K3 * P)
eq("P(0) = 500", int(P.subs(t, 0)), 500)
approx("P(10) = 2240.84…", round(float(P.subs(t, 10)), 5), 2240.84454)
approx("  3 s.f. で 2240", sf(float(P.subs(t, 10)), 4), 2241.0)
eq("  整数に丸めると 2241（切り捨てではない）",
   round(float(P.subs(t, 10))), 2241)
DOUBLE = math.log(2) / 0.15
approx("倍になる時間 = ln2 / 0.15 = 4.62", sf(DOUBLE), 4.62)
approx("  生の値 4.620981", round(DOUBLE, 6), 4.620981)
approx("  その時刻の P は 1000", round(float(P.subs(t, DOUBLE)), 6), 1000.0,
       1e-5)
# ★ 倍になる時間は A によらない
for A0 in (500, 5000, 12345):
    d = math.log(2) / 0.15
    approx(f"  A = {A0} でも倍になる時間は同じ",
           round(math.log(2 * A0 / A0) / 0.15, 9), round(d, 9))

print("══════════ 例題4：コーヒーの冷却 ══════════")
K4 = sp.log(sp.Rational(3, 2)) / 5
TH = 20 + 60 * sp.exp(-K4 * t)
verify_ode("θ = 20 + 60e^{-kt} は dθ/dt = -k(θ-20) を満たす", TH,
           -K4 * (TH - 20))
eq("θ(0) = 80", int(TH.subs(t, 0)), 80)
approx("θ(5) = 60", round(float(TH.subs(t, 5)), 9), 60.0)
approx("k = (1/5)ln(3/2) = 0.0811", sf(float(K4)), 0.0811)
approx("  生の値 0.08109302", round(float(K4), 8), 0.08109302)
approx("θ(15) = 37.8", sf(float(TH.subs(t, 15))), 37.8)
approx("  生の値 37.777778", round(float(TH.subs(t, 15)), 6), 37.777778)
# ★ 「差が (2/3)^3 倍」という検算が本当に合うか
approx("検算：20 + 60(2/3)^3 と一致",
       round(float(20 + 60 * sp.Rational(2, 3) ** 3), 9),
       round(float(TH.subs(t, 15)), 9))
eq("  (2/3)^3 = 8/27", sp.Rational(2, 3) ** 3, sp.Rational(8, 27))
# ★ 室温に近づく（0 ではない）
approx("t が大きいと θ → 20", round(float(TH.subs(t, 500)), 6), 20.0, 1e-5)
eq("  0 には近づかない", float(TH.subs(t, 500)) > 19.9, True)

print("══════════ 演習1：式を立てるだけ ══════════")
eq("(c) the square of F は F^2（√F ではない）", "F^2", "F^2")
DD = sp.Symbol("D", positive=True)
eq("(d) D > 5 なら -k(D-5) < 0（減る）",
   bool(sp.simplify((-(DD - 5)).subs(DD, 10)) < 0), True)

print("══════════ 演習2：dP/dt = 0.08P ══════════")
P2 = 2000 * sp.exp(sp.Rational(8, 100) * t)
verify_ode("P = 2000e^{0.08t} は dP/dt = 0.08P を満たす", P2,
           sp.Rational(8, 100) * P2)
eq("P(0) = 2000", int(P2.subs(t, 0)), 2000)
approx("P(10) = 4451.08…", round(float(P2.subs(t, 10)), 5), 4451.08186)
approx("  3 s.f. で 4450", sf(float(P2.subs(t, 10))), 4450.0)
D2 = math.log(2) / 0.08
approx("倍になる時間 = 8.66", sf(D2), 8.66)
approx("  生の値 8.664340", round(D2, 6), 8.664340)
approx("  その時刻の P は 4000", round(float(P2.subs(t, D2)), 5), 4000.0,
       1e-4)

print("══════════ 演習3：水そう dV/dt = -k√V ══════════")
V = (20 - t) ** 2
verify_ode("V = (20-t)^2 は dV/dt = -2√V を満たす（0 < t < 20）", V,
           -2 * (20 - t))
eq("V(0) = 400", int(V.subs(t, 0)), 400)
eq("V(10) = 100", int(V.subs(t, 10)), 100)
eq("V(20) = 0（空になる）", int(V.subs(t, 20)), 0)
eq("C = 2√400 = 40", 2 * int(sp.sqrt(400)), 40)
eq("t=10 から 2(10) = -10k + 40、k = 2",
   sp.solve(sp.Eq(2 * 10, -10 * sp.Symbol("k") + 40), sp.Symbol("k")), [2])
# ★ モデルが使える範囲（t > 20 では増えてしまう）
eq("★ t = 25 だと V = 25 になり、水が増えてしまう", int(V.subs(t, 25)), 25)
eq("  だからモデルは 0 <= t <= 20 でのみ妥当", 20, 20)
# ★ -2√V の √ は |20-t|。t<20 の範囲でのみ 20-t
eq("  t < 20 では √V = 20 - t", int(sp.sqrt(V.subs(t, 5))), 15)

print("══════════ 演習5：金属棒の冷却（室温 18） ══════════")
K5 = sp.log(sp.Rational(3, 2)) / 4
TH5 = 18 + 72 * sp.exp(-K5 * t)
verify_ode("θ = 18 + 72e^{-kt} は dθ/dt = -k(θ-18) を満たす", TH5,
           -K5 * (TH5 - 18))
eq("θ(0) = 90", int(TH5.subs(t, 0)), 90)
approx("θ(4) = 66", round(float(TH5.subs(t, 4)), 9), 66.0)
approx("k = (1/4)ln(3/2) = 0.101", sf(float(K5)), 0.101)
approx("  生の値 0.10136628", round(float(K5), 8), 0.10136628)
approx("θ(10) = 44.1", sf(float(TH5.subs(t, 10))), 44.1)
approx("  生の値 44.127891", round(float(TH5.subs(t, 10)), 6), 44.127891)
# ★ 丸めた k を使うとどうずれるか（本文の注意）
approx("★ k を 0.101 に丸めると 44.2 になる",
       sf(18 + 72 * math.exp(-0.101 * 10)), 44.2)
eq("  3 桁目がずれる",
   sf(18 + 72 * math.exp(-0.101 * 10)) != sf(float(TH5.subs(t, 10))), True)
approx("検算：18 + 72(2/3)^2.5 と一致",
       round(18 + 72 * (2 / 3) ** 2.5, 6),
       round(float(TH5.subs(t, 10)), 6))

print("══════════ 演習6：半減期 ══════════")
K6 = sp.log(2) / 8
M = 50 * sp.exp(-K6 * t)
verify_ode("m = 50e^{-kt} は dm/dt = -km を満たす", M, -K6 * M)
eq("m(0) = 50", int(M.subs(t, 0)), 50)
approx("m(8) = 25（半減期）", round(float(M.subs(t, 8)), 9), 25.0)
approx("k = ln2/8 = 0.0866", sf(float(K6)), 0.0866)
approx("  生の値 0.08664340", round(float(K6), 8), 0.08664340)
approx("m(20) = 8.84", sf(float(M.subs(t, 20))), 8.84)
approx("  生の値 8.838835", round(float(M.subs(t, 20)), 6), 8.838835)
approx("  50 × 2^(-2.5) と一致", round(50 * 2 ** -2.5, 9),
       round(float(M.subs(t, 20)), 9))
# ★ 半減期は最初の量によらない
for A0 in (50, 500, 7):
    approx(f"  A = {A0} でも半減期は 8", round(math.log(2) / float(K6), 9),
           8.0)

print("══════════ 演習7：うわさ ══════════")
K7 = sp.log(4) / 3
N = 40 * sp.exp(K7 * t)
verify_ode("N = 40e^{kt} は dN/dt = kN を満たす", N, K7 * N)
eq("N(0) = 40", int(N.subs(t, 0)), 40)
approx("N(3) = 160", round(float(N.subs(t, 3)), 9), 160.0)
approx("k = ln4/3 = 0.462", sf(float(K7)), 0.462)
approx("  生の値 0.4620981", round(float(K7), 7), 0.4620981)
approx("N(5) = 403.17…", round(float(N.subs(t, 5)), 5), 403.17474)
eq("  人数は 403", int(float(N.subs(t, 5))), 403)
approx("  40 × 4^(5/3) と一致", round(40 * 4 ** (5 / 3), 9),
       round(float(N.subs(t, 5)), 9))
eq("検算：6 日なら 16 倍の 640", int(round(float(N.subs(t, 6)))), 640)
eq("  403 は 160 と 640 のあいだ", 160 < float(N.subs(t, 5)) < 640, True)

print("══════════ 演習8：指数法則の誤り ══════════")
x = sp.symbols("x")
GOOD = sp.Symbol("A") * sp.exp(3 * x)
BAD = sp.exp(3 * x) + sp.exp(sp.Symbol("C"))
eq("正しい y = Ae^{3x} は dy/dx = 3y を満たす",
   sp.simplify(sp.diff(GOOD, x) - 3 * GOOD) == 0, True)
eq("★ 誤った y = e^{3x} + e^C は満たさない",
   sp.simplify(sp.diff(BAD, x) - 3 * BAD) == 0, False)
eq("  差は 3e^C",
   sp.simplify(3 * BAD - sp.diff(BAD, x) - 3 * sp.exp(sp.Symbol("C"))), 0)
eq("e^{a+b} = e^a · e^b（積）",
   sp.simplify(sp.exp(sp.Symbol("a") + sp.Symbol("b"))
               - sp.exp(sp.Symbol("a")) * sp.exp(sp.Symbol("b"))), 0)

print("══════════ 演習9：単位と k ══════════")
K9 = math.log(2.5) / 6
approx("k = ln(2.5)/6 = 0.153", sf(K9), 0.153)
approx("  生の値 0.1527151", round(K9, 7), 0.1527151)
approx("  30e^{-6k} = 12", round(30 * math.exp(-6 * K9), 9), 12.0)
approx("  -ln(0.4)/6 と同じ", round(-math.log(0.4) / 6, 12), round(K9, 12))
eq("  12/30 = 0.4", 12 / 30, 0.4)

print("══════════ 演習10：町の人口 ══════════")
K10 = sp.log(sp.Rational(3, 2)) / 6
P10 = 8000 * sp.exp(K10 * t)
verify_ode("P = 8000e^{kt} は dP/dt = kP を満たす", P10, K10 * P10)
eq("P(0) = 8000", int(P10.subs(t, 0)), 8000)
approx("P(6) = 12000", round(float(P10.subs(t, 6)), 9), 12000.0)
approx("k = ln(1.5)/6 = 0.0676", sf(float(K10)), 0.0676)
approx("  生の値 0.06757752", round(float(K10), 8), 0.06757752)
approx("P(15) = 22045.4…", round(float(P10.subs(t, 15)), 4), 22045.4077)
approx("  8000 × 1.5^2.5 と一致", round(8000 * 1.5 ** 2.5, 6),
       round(float(P10.subs(t, 15)), 6))
approx("  およそ 22000", sf(float(P10.subs(t, 15)), 2), 22000.0)
T10 = math.log(2.5) / float(K10)
approx("20000 に達するのは t = 13.6", sf(T10), 13.6)
approx("  生の値 13.559106", round(T10, 6), 13.559106)
approx("  その時刻の P は 20000", round(float(P10.subs(t, T10)), 4), 20000.0,
       1e-3)
# ★ 年に直す：t = 13.56 は 2034 年の途中
eq("★ 年は 2020 + t で決まる（(b) と同じ約束）", 2020 + 15, 2035)
eq("★ 2020 + 13.559… は 2033 年の途中", int(2020 + T10), 2033)
eq("  2034 ではない", int(2020 + T10) == 2034, False)
# ★ 年ごとの値も見ておく（もし「20000 を初めて超える年」なら 2034 になる）
approx("  P(13) = 19258", round(float(P10.subs(t, 13))), 19258.0)
approx("  P(14) = 20605", round(float(P10.subs(t, 14))), 20605.0)
eq("検算：12 年で 2.25 倍の 18000", int(round(float(P10.subs(t, 12)))), 18000)
eq("  18 年で 3.375 倍の 27000", int(round(float(P10.subs(t, 18)))), 27000)

print("══════════ ★ 解答例の【式】と【答え】が一致するか ══════════")
# 前回はここが抜けていて、丸めた k で書いた式と、丸めない k で出した答えが
# 同じ解答例に並んでいた。式に書いた定数で計算し直して確かめる。
approx("演習5：丸めた k=0.101 で計算すると 44.2（44.1 ではない）",
       sf(18 + 72 * math.exp(-0.101 * 10)), 44.2)
approx("  丸めない k なら 44.1", sf(float(TH5.subs(t, 10))), 44.1)
approx("演習10：丸めた k=0.0676 で計算すると 22100（22000 ではない）",
       sf(8000 * math.exp(0.0676 * 15), 3), 22100.0)
approx("  丸めない k なら 22045 → 22000", sf(float(P10.subs(t, 15)), 2),
       22000.0)
in_text_pending = True

print("══════════ 本文に、その数値が実際に書かれているか ══════════")
QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-14.qmd")
TXT = open(QMD, encoding="utf-8").read()


def in_text(name, needle, want=True):
    global ok, ng
    good = (needle in TXT) == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else
           f"   ({'欠けている' if want else '残っている'}: {needle!r})"))
    ok, ng = ok + good, ng + (not good)


for lab, needle in [
        ("例題2 G(5)", "= 49"),
        ("例題2 の解", "G = (t+2)^2"),
        ("例題3 P(10)", "2240"),
        ("例題3 倍になる時間", "4.62"),
        ("例題4 k", "0.0811"),
        ("例題4 θ(15)", "37.8"),
        ("例題4 の 8/27", "\\frac{8}{27}"),
        ("演習2 P(10)", "4450"),
        ("演習2 倍になる時間", "8.66"),
        ("演習3 の解", "V = (20 - t)^2"),
        ("演習3 空になる時刻", "t = 20"),
        ("演習5 k", "0.101"),
        ("演習5 θ(10)", "44.1"),
        ("  丸めた k の値 44.2", "$44.2$"),
        ("演習6 k", "0.0866"),
        ("演習6 m(20)", "8.84"),
        ("演習7 k", "0.462"),
        ("演習7 N(5)", "403"),
        ("演習9 k", "0.153"),
        ("演習10 k", "0.0676"),
        ("演習10 P(15)", "22\\,045"),
        ("演習10 t", "13.6"),

        ("演習10 の年", "2033")]:
    in_text(lab, needle)

# ★ シラバスの引用
in_text("Content 1 行目の引用",
        "Setting up a model/differential equation from a context")
in_text("Content 2 行目の引用", "Solving by separation of variables")
in_text("藻の例の引用",
        "The growth of an algae $G$, at time $t$, is proportional to "
        "$\\sqrt{G}$")
in_text("指数モデルの例の引用",
        "An exponential model as a solution of $\\dfrac{dy}{dx} = ky$")
in_text("general solution の語の引用", '**"general solution"**')
# ★ 公式集に 5.14 が無いこと
in_text("5.13 の次が 5.16 と書いてある", "**5.13 の次が 5.16**")
in_text("覚える必要があると書いてある", "覚える必要があります")
# ★ 教える上での要点
in_text("「差に比例」はカッコと書いてある", "カッコで囲みます")
in_text("減るときはマイナスと書いてある", "マイナス")
in_text("解を微分して確かめると書いてある", "微分すれば確かめられます")
in_text("deSolve は非 CAS に無いと書いてある", "`deSolve` はありません")
in_text("y = Ae^{kx} がある", "y = Ae^{kx}")
# ★ GDC のメニュー
in_text("メニューは Numerical Derivative at a Point",
        "menu → 4: Calculus → 1: Numerical Derivative at a Point")
in_text("  CAS 用の Calculus → Derivative が残っていない",
        "menu → Calculus → Derivative", want=False)
# ★ 本の他ページ（SL 5.3 / _TEMPLATE）を真として突き合わせる
for src in ("../../ai-sl/05-calculus/sl-5-3.qmd", "../../_TEMPLATE.qmd"):
    _p = os.path.join(os.path.dirname(__file__), src)
    _t = open(_p, encoding="utf-8").read()
    eq(f"  {os.path.basename(src)} も同じメニューを書いている",
       "Calculus → 1: Numerical Derivative at a Point" in _t, True)
# ★ 公式集の欄の帰属（x^n は 5.5、1/x と e^x が 5.11）
in_text("x^n は 5.5 の欄と書いてある", "べき乗のほうは **5.5** の欄です")
in_text("1/x と e^x は 5.11 と書いてある", "**5.11 の Standard integrals** の欄")
in_text("  誤った「使う積分は 5.11 の欄」が残っていない",
        "使う積分のほうは、公式集の **5.11** の欄にあります", want=False)
# ★ A は符号こみの任意定数（A = e^C と書いていない）
in_text("A は任意の定数と書いてある", "$A$ は任意の定数")
in_text("演習10 の誤った 2034 年が残っていない", "**$2034$ 年**", want=False)
in_text("  A = e^C という決めつけが解答例に残っていない",
        "where } A = e^{C}", want=False)
# ★ code span の中に数式や markdown が入っていないか
import re as _re
_bad = [m for m in _re.findall(r"`[^`\n]+`", TXT)
        if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", _bad, [])
# ★ 開き fence の直前が空行か
_L = TXT.split("\n")
_nb = [i + 1 for i, l in enumerate(_L)
       if _re.match(r"^:{3,} *\{", l) and i > 0
       and _L[i - 1].strip() != "" and not _L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", _nb, [])

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
