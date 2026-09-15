"""AA SL 3.3 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_3.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_3.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-3-idea.svg

(a) 仰角と俯角。水平線から測る。錯角なので 2 つは等しい。
(b) 方位角。北から時計回りに、3 桁で書く。逆向きは 180 ちがう。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（角の値は θ で書く）。
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.8))

# ══════════════════════════════════════════════════════════
# (a) 仰角と俯角
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Elevation and depression", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-0.9, 9.4)
ax1.set_ylim(-1.7, 5.4)
ax1.axis("off")

P = (0.6, 0.0)      # 下の観測者
T = (7.6, 3.6)      # 上の点

# 地面
ax1.plot([-0.4, 9.0], [0, 0], color=GREY, linewidth=1.4)
# 塔
ax1.plot([T[0], T[0]], [0, T[1]], color=INK, linewidth=2.2)
# 視線
ax1.plot([P[0], T[0]], [P[1], T[1]], color=ACCENT, linewidth=2.2)
# 上の水平線（俯角を測る線）
ax1.plot([T[0] - 5.4, T[0] + 1.1], [T[1], T[1]], color=GREY, linewidth=1.2,
         linestyle=(0, (5, 4)))

th = np.arctan2(T[1] - P[1], T[0] - P[0])
t = np.linspace(0, th, 60)
ax1.plot(P[0] + 1.5 * np.cos(t), P[1] + 1.5 * np.sin(t), color=GREEN,
         linewidth=1.5)
ax1.text(P[0] + 1.68, P[1] + 0.30, "$\\theta$", fontsize=12, color=GREEN)

t2 = np.linspace(np.pi, np.pi + th, 60)
ax1.plot(T[0] + 1.5 * np.cos(t2), T[1] + 1.5 * np.sin(t2), color=WARM,
         linewidth=1.5)
ax1.text(T[0] - 2.15, T[1] - 0.62, "$\\theta$", fontsize=12, color=WARM)

ax1.plot([P[0]], [P[1]], marker="o", markersize=5.5, color=INK, zorder=3)
ax1.plot([T[0]], [T[1]], marker="o", markersize=5.5, color=INK, zorder=3)

ax1.text(0.10, 4.55, "angle of depression, measured", fontsize=10, color=WARM)
ax1.text(0.10, 4.10, "down from the horizontal", fontsize=10, color=WARM)
ax1.text(3.05, 1.15, "angle of elevation", fontsize=10, color=GREEN)
ax1.text(-0.9, -1.60,
         "the two are alternate angles between parallel horizontals, so they "
         "are equal", fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 方位角
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Bearings", fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-4.4, 4.4)
ax2.set_ylim(-3.8, 4.4)
ax2.set_aspect("equal")
ax2.axis("off")

O = (-1.4, -1.0)
# 北の線
ax2.annotate("", xy=(O[0], O[1] + 3.9), xytext=(O[0], O[1]),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.3))
ax2.text(O[0] - 0.12, O[1] + 4.05, "N", fontsize=11, color=GREY, ha="center")

bear = np.deg2rad(62.0)
L = 4.2
Q = (O[0] + L * np.sin(bear), O[1] + L * np.cos(bear))
ax2.plot([O[0], Q[0]], [O[1], Q[1]], color=ACCENT, linewidth=2.2)
ax2.plot([O[0]], [O[1]], marker="o", markersize=5.5, color=INK, zorder=3)
ax2.plot([Q[0]], [Q[1]], marker="o", markersize=5.5, color=INK, zorder=3)
ax2.text(O[0] - 0.42, O[1] - 0.36, "$P$", fontsize=12, color=INK)
ax2.text(Q[0] + 0.14, Q[1] + 0.06, "$Q$", fontsize=12, color=INK)

tt = np.linspace(np.pi / 2, np.pi / 2 - bear, 60)
ax2.plot(O[0] + 1.1 * np.cos(tt), O[1] + 1.1 * np.sin(tt), color=GREEN,
         linewidth=1.5)
ax2.text(O[0] + 0.34, O[1] + 1.26, "$\\theta$", fontsize=12, color=GREEN)

# Q での北の線と、戻りの方位角
ax2.annotate("", xy=(Q[0], Q[1] + 1.5), xytext=(Q[0], Q[1]),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(Q[0] - 0.12, Q[1] + 1.66, "N", fontsize=10, color=GREY, ha="center")
tb = np.linspace(np.pi / 2, np.pi / 2 - (bear + np.pi), 90)
ax2.plot(Q[0] + 0.78 * np.cos(tb), Q[1] + 0.78 * np.sin(tb), color=WARM,
         linewidth=1.4)
ax2.text(Q[0] + 0.30, Q[1] - 1.05, "$\\theta + 180°$", fontsize=10.5,
         color=WARM)

ax2.text(-4.3, 3.95, "measured from north, clockwise,", fontsize=10, color=INK)
ax2.text(-4.3, 3.50, "always written with three figures", fontsize=10,
         color=INK)
ax2.text(-4.4, -3.75, "the bearing back the other way differs by $180°$",
         fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-3-3-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
