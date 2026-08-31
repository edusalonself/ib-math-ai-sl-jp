"""AHL 1.14 / 1.15 の例題・演習の数値を独立に検算する。
   図を作るコードとは【別に】書いて、答えが一致するかを見る。
   実行: python3 figs/ai-hl/check_ahl_1_14_15.py
"""
import sympy as sp

ok, ng = 0, 0


def eq(name, got, want):
    global ok, ng
    g = sp.nsimplify(got) if not isinstance(got, sp.MatrixBase) else got
    w = sp.nsimplify(want) if not isinstance(want, sp.MatrixBase) else want
    good = sp.simplify(g - w) == 0 if not isinstance(g, sp.MatrixBase) \
        else sp.simplify(g - w) == sp.zeros(*g.shape)
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


M = sp.Matrix
print("══════════ AHL 1.14 ══════════")

# --- The idea ---
A = M([[1, 2], [3, 4]]); B = M([[5, 6], [7, 8]])
eq("AB", A * B, M([[19, 22], [43, 50]]))
eq("BA", B * A, M([[23, 34], [31, 46]]))

# --- 例題1: 2A - B ---
A1 = M([[2, 0, -1], [3, 1, 4]]); B1 = M([[1, 5, 2], [0, -2, 3]])
eq("E1 2A-B", 2 * A1 - B1, M([[3, -5, -4], [6, 4, 5]]))

# --- 例題3: 売上 × 単価 ---
S = M([[12, 8, 5], [10, 14, 6]]); P = M([[4], [7], [10]])
eq("E3 revenue", S * P, M([[154], [198]]))

# --- 例題4: det, inverse, Ax=b ---
A4 = M([[3, 1], [5, 2]])
eq("E4 det", A4.det(), 1)
eq("E4 inverse", A4.inv(), M([[2, -1], [-5, 3]]))
eq("E4 AA^-1", A4 * A4.inv(), sp.eye(2))
eq("E4 x", A4.inv() * M([[11], [19]]), M([[3], [2]]))

# --- 例題5: 暗号 CODE ---
COD = A4
eq("E5 [3,15]->", COD * M([[3], [15]]), M([[24], [45]]))
eq("E5 [4,5]->", COD * M([[4], [5]]), M([[17], [30]]))
eq("E5 decode 1", COD.inv() * M([[24], [45]]), M([[3], [15]]))
eq("E5 decode 2", COD.inv() * M([[17], [30]]), M([[4], [5]]))

# --- 演習 ---
Ax = M([[2, -1], [4, 3]]); Bx = M([[1, 5], [0, 2]])
eq("Ex1 A+B", Ax + Bx, M([[3, 4], [4, 5]]))
eq("Ex1 3A", 3 * Ax, M([[6, -3], [12, 9]]))
eq("Ex1 A-B", Ax - Bx, M([[1, -6], [4, 1]]))

A3 = M([[3, 2], [1, 4]]); B3 = M([[2, 0], [5, 1]])
eq("Ex3 AB", A3 * B3, M([[16, 2], [22, 4]]))
eq("Ex3 BA", B3 * A3, M([[6, 4], [16, 14]]))

A5 = M([[5, 3], [3, 2]])
eq("Ex4 det", A5.det(), 1)
eq("Ex4 inv", A5.inv(), M([[2, -3], [-3, 5]]))
eq("Ex5 singular det", M([[6, 4], [3, 2]]).det(), 0)

A6 = M([[2, 5], [1, 3]])
eq("Ex6 det", A6.det(), 1)
eq("Ex6 inv", A6.inv(), M([[3, -5], [-1, 2]]))
eq("Ex6 x", A6.inv() * M([[16], [9]]), M([[3], [2]]))

S7 = M([[10, 6, 4], [8, 9, 5]])
eq("Ex7 revenue", S7 * M([[3], [2], [5]]), M([[62], [67]]))

A8 = M([[2, 3, 1], [1, 2, 3], [3, 1, 2]])
eq("Ex8 det", A8.det(), 18)
eq("Ex8 prices", A8.inv() * M([[64], [61], [73]]), M([[15], [8], [10]]))

eq("Ex9 HI->", COD * M([[8], [9]]), M([[33], [58]]))
eq("Ex9 DE->", COD * M([[4], [5]]), M([[17], [30]]))
eq("Ex9 decode HI", COD.inv() * M([[33], [58]]), M([[8], [9]]))

A10 = M([[2, 1], [3, 4]])
eq("Ex10 AI", A10 * sp.eye(2), A10)
eq("Ex10 A^2", A10 ** 2, M([[7, 6], [18, 19]]))

Sw = M([[0, 1], [1, 0]]); A11 = M([[1, 2], [3, 4]])
eq("Ex11 AB", A11 * Sw, M([[2, 1], [4, 3]]))
eq("Ex11 BA", Sw * A11, M([[3, 4], [1, 2]]))


print("\n══════════ AHL 1.15 ══════════")
lam = sp.Symbol('lambda')


def char_poly(Mx):
    return sp.expand((Mx - lam * sp.eye(2)).det())


def eigen(Mx):
    """固有値（小さい順ではなく sympy の順）と固有ベクトルを返す"""
    return sp.Matrix(Mx).eigenvects()


Mw = M([[4, 1], [2, 3]])
eq("E1 char poly", char_poly(Mw), sp.expand(lam ** 2 - 7 * lam + 10))
eq("E1 lambdas", sp.Matrix(sorted(Mw.eigenvals().keys())), M([[2], [5]]))

# 固有ベクトル（比で確認：定数倍は自由）
for l, v in [(5, M([[1], [1]])), (2, M([[1], [-2]]))]:
    eq(f"E2 M v = {l} v  (v={list(v)})", Mw * v, l * v)

Pm = M([[1, 1], [1, -2]]); Dm = sp.diag(5, 2)
eq("E3 P D P^-1", Pm * Dm * Pm.inv(), Mw)
eq("E3 P^-1", Pm.inv(), sp.Rational(1, 3) * M([[2, 1], [1, -1]]))
eq("E4 M^3 formula", Pm * Dm ** 3 * Pm.inv(), Mw ** 3)
eq("E4 M^3 value", Mw ** 3, M([[86, 39], [78, 47]]))
eq("E4 M^4 value", Mw ** 4, M([[422, 203], [406, 219]]))

# 例題5：2つの町
T = M([[sp.Rational(4, 5), sp.Rational(1, 10)],
       [sp.Rational(1, 5), sp.Rational(9, 10)]])
eq("E5 char poly", char_poly(T),
   sp.expand(lam ** 2 - sp.Rational(17, 10) * lam + sp.Rational(7, 10)))
eq("E5 lambdas", sp.Matrix(sorted(T.eigenvals().keys())),
   M([[sp.Rational(7, 10)], [1]]))
eq("E5 lambda=1 vector", T * M([[1], [2]]), M([[1], [2]]))
eq("E5 s1", T * M([[24000], [6000]]), M([[19800], [10200]]))
eq("E5 long run", M([[30000 * sp.Rational(1, 3)], [30000 * sp.Rational(2, 3)]]),
   M([[10000], [20000]]))

# --- 演習 ---
M1 = M([[5, 2], [2, 2]])
eq("Ex1 char", char_poly(M1), sp.expand(lam ** 2 - 7 * lam + 6))
eq("Ex1 lambdas", sp.Matrix(sorted(M1.eigenvals().keys())), M([[1], [6]]))
eq("Ex2 v(6)", M1 * M([[2], [1]]), 6 * M([[2], [1]]))
eq("Ex2 v(1)", M1 * M([[1], [-2]]), 1 * M([[1], [-2]]))

M3 = M([[3, 1], [0, 2]])
eq("Ex3 char", char_poly(M3), sp.expand(lam ** 2 - 5 * lam + 6))
eq("Ex3 v(3)", M3 * M([[1], [0]]), 3 * M([[1], [0]]))
eq("Ex3 v(2)", M3 * M([[1], [-1]]), 2 * M([[1], [-1]]))

M4 = M([[1, 2], [2, 1]])
eq("Ex4 char", char_poly(M4), sp.expand(lam ** 2 - 2 * lam - 3))
eq("Ex4 v(3)", M4 * M([[1], [1]]), 3 * M([[1], [1]]))
eq("Ex4 v(-1)", M4 * M([[1], [-1]]), -1 * M([[1], [-1]]))
P4 = M([[1, 1], [1, -1]]); D4 = sp.diag(3, -1)
eq("Ex5 P D^3 P^-1", P4 * D4 ** 3 * P4.inv(), M4 ** 3)
eq("Ex5 M^3", M4 ** 3, M([[13, 14], [14, 13]]))

M6 = M([[2, 4], [1, 2]])
eq("Ex6 det", M6.det(), 0)
eq("Ex6 char", char_poly(M6), sp.expand(lam ** 2 - 4 * lam))

T7 = M([[sp.Rational(7, 10), sp.Rational(2, 10)],
        [sp.Rational(3, 10), sp.Rational(8, 10)]])
eq("Ex7 char", char_poly(T7),
   sp.expand(lam ** 2 - sp.Rational(3, 2) * lam + sp.Rational(1, 2)))
eq("Ex7 v(1)", T7 * M([[2], [3]]), M([[2], [3]]))
eq("Ex7 long run", M([[5000 * sp.Rational(2, 5)], [5000 * sp.Rational(3, 5)]]),
   M([[2000], [3000]]))

P8 = M([[1, 1], [1, -1]]); D8 = sp.diag(3, 1)
eq("Ex8 M", P8 * D8 * P8.inv(), M([[2, 1], [1, 2]]))

eq("Ex9 M^5 formula", Pm * Dm ** 5 * Pm.inv(), Mw ** 5)
eq("Ex9 M^5", Mw ** 5, M([[2094, 1031], [2062, 1063]]))

T10 = M([[sp.Rational(9, 10), sp.Rational(15, 100)],
         [sp.Rational(1, 10), sp.Rational(85, 100)]])
eq("Ex10 char", char_poly(T10),
   sp.expand(lam ** 2 - sp.Rational(7, 4) * lam + sp.Rational(3, 4)))
eq("Ex10 v(1)", T10 * M([[3], [2]]), M([[3], [2]]))
eq("Ex10 long run",
   M([[40000 * sp.Rational(3, 5)], [40000 * sp.Rational(2, 5)]]),
   M([[24000], [16000]]))

print(f"\n合計  OK {ok}   NG {ng}")
raise SystemExit(1 if ng else 0)
