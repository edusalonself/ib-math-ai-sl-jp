"""AA SL 3.5b の図をつくる。

    python3 figs/aa-sl/make_aasl_3_5b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_5b.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-5b-idea.svg

(a) 正確な値のもとになる 2 つの三角形。
(b) あいまいな場合。C を中心とする半径 a の円が、半直線と 2 回交わる。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.9))

# ══════════════════════════════════════════════════════════
# (a) 2 つの三角形
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The two special triangles", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-0.35, 5.6)
ax1.set_ylim(-1.15, 2.75)
ax1.set_aspect("equal")
ax1.axis("off")


def rt(ax, x0, y0, col, d=0.17):
    """直角の印を (x0, y0) の角に置く（直角は左下）。"""
    ax.plot([x0 + d, x0 + d, x0], [y0, y0 + d, y0 + d], color=col,
            linewidth=1.0)


# 45-45-90
ax1.plot([0, 1.6, 0, 0], [0, 0, 1.6, 0], color=ACCENT, linewidth=2.0)
rt(ax1, 0, 0, GREY)
ax1.text(0.72, -0.36, "$1$", fontsize=11, color=INK)
ax1.text(-0.30, 0.72, "$1$", fontsize=11, color=INK)
ax1.text(0.86, 0.86, "$\\sqrt{2}$", fontsize=11, color=INK)
ax1.text(1.05, 0.13, "$\\frac{\\pi}{4}$", fontsize=11, color=GREEN)
ax1.text(0.09, 1.20, "$\\frac{\\pi}{4}$", fontsize=11, color=GREEN)

# 30-60-90
bx = 3.1
ax1.plot([bx, bx + 1.75, bx, bx], [0, 0, 1.01, 0], color=ACCENT, linewidth=2.0)
rt(ax1, bx, 0, GREY)
ax1.text(bx + 0.80, -0.36, "$\\sqrt{3}$", fontsize=11, color=INK)
ax1.text(bx - 0.30, 0.44, "$1$", fontsize=11, color=INK)
ax1.text(bx + 0.94, 0.60, "$2$", fontsize=11, color=INK)
ax1.text(bx + 1.16, 0.11, "$\\frac{\\pi}{6}$", fontsize=11, color=GREEN)
ax1.text(bx + 0.09, 0.66, "$\\frac{\\pi}{3}$", fontsize=11, color=GREEN)

ax1.text(-0.35, 2.50, "half a square, and half an equilateral triangle",
         fontsize=10, color=INK)
ax1.text(-0.35, -1.10, "every exact value comes from reading a ratio off one "
         "of these", fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) あいまいな場合
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) The ambiguous case", fontsize=11, color=INK, loc="left",
              pad=10)
ax2.set_xlim(-0.7, 7.6)
ax2.set_ylim(-1.15, 4.75)
ax2.set_aspect("equal")
ax2.axis("off")

A = np.array([0.0, 0.0])
ang = np.deg2rad(30.0)
b = 5.0                      # AC = b（角 A の一方の辺）
C = A + b * np.array([np.cos(ang), np.sin(ang)])
a = 3.0                      # CB = a（A の向かいの辺）
dx = np.sqrt(a ** 2 - C[1] ** 2)
B1 = np.array([C[0] - dx, 0.0])
B2 = np.array([C[0] + dx, 0.0])

ax2.annotate("", xy=(7.1, 0), xytext=(A[0], A[1]),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
ax2.plot([A[0], C[0]], [A[1], C[1]], color=ACCENT, linewidth=2.2)

tt = np.linspace(0, 2 * np.pi, 300)
ax2.plot(C[0] + a * np.cos(tt), C[1] + a * np.sin(tt), color=GREY,
         linewidth=1.0, linestyle=(0, (4, 4)))
ax2.plot([C[0], B1[0]], [C[1], B1[1]], color=WARM, linewidth=2.0)
ax2.plot([C[0], B2[0]], [C[1], B2[1]], color=WARM, linewidth=2.0)

ax2.plot([C[0], C[0]], [0, C[1]], color=GREEN, linewidth=1.4,
         linestyle=(0, (3, 3)))

for _p, _lab, _dx, _dy in [(A, "$A$", -0.34, -0.30), (C, "$C$", 0.10, 0.14),
                           (B1, "$B_{1}$", -0.16, -0.52),
                           (B2, "$B_{2}$", -0.16, -0.52)]:
    ax2.plot([_p[0]], [_p[1]], marker="o", markersize=5.2, color=INK, zorder=3)
    ax2.text(_p[0] + _dx, _p[1] + _dy, _lab, fontsize=11, color=INK)

ta = np.linspace(0, ang, 60)
ax2.plot(A[0] + 0.85 * np.cos(ta), A[1] + 0.85 * np.sin(ta), color=INK,
         linewidth=1.2)
ax2.text(0.95, 0.16, "$A$", fontsize=11, color=INK)

ax2.text(2.0, 1.62, "$b$", fontsize=11, color=ACCENT)
ax2.text(3.55, 1.62, "$a$", fontsize=11, color=WARM)
ax2.text(5.20, 1.62, "$a$", fontsize=11, color=WARM)
ax2.text(C[0] + 0.10, 1.00, "$b\\sin A$", fontsize=10, color=GREEN)

ax2.text(-0.7, 4.45, "two sides and an angle that is not between them",
         fontsize=10, color=INK)
ax2.text(-0.7, -1.10, "the circle of radius $a$ centred at $C$ can meet the "
         "ray twice, once, or not at all", fontsize=9.5, color=INK,
         va="bottom")

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-3-5b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
