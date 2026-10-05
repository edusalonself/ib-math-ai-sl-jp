"""AA SL 3.3 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_3.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_3.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-3-idea-a.svg
      aa-sl/03-geometry/img/aasl-3-3-idea-b.svg
      aa-sl/03-geometry/img/aasl-3-3-idea-c.svg

(a) 仰角と俯角。水平線から測る。錯角なので 2 つは等しい。
(b) 方位角。北から時計回りに、3 桁で書く。逆向きは 180 ちがう。
(c) 塔を 2 か所から見上げる。高さ h が共通の辺。

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

fig1, ax1 = plt.subplots(figsize=(5.3, 4.8))
fig2, ax2 = plt.subplots(figsize=(5.3, 4.8))
fig3, ax3 = plt.subplots(figsize=(6.4, 4.0))
# ══════════════════════════════════════════════════════════
# (a) 仰角と俯角
# ══════════════════════════════════════════════════════════
ax1.set_title("Elevation and depression", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-0.9, 9.4)
ax1.set_ylim(-1.05, 5.4)
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

# ══════════════════════════════════════════════════════════
# (b) 方位角
# ══════════════════════════════════════════════════════════
ax2.set_title("Bearings", fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-4.4, 4.4)
ax2.set_ylim(-3.15, 3.55)
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


# ══════════════════════════════════════════════════════════
# (c) 塔を 2 か所から見上げる（共通の辺は h）
# ══════════════════════════════════════════════════════════
ax3.set_title("Two triangles, one shared side", fontsize=11, color=INK,
              loc="left", pad=10)
ax3.set_xlim(-1.0, 9.8)
ax3.set_ylim(-1.35, 5.9)
ax3.set_aspect("equal")
ax3.axis("off")

# 実際の比のとおりに置く（B で 45 度、A で 30 度になる）
XA, XB, XF = 0.0, 3.55, 8.40
HT = 4.85
TOP = (XF, HT)

# 地面
ax3.plot([-0.5, 9.3], [0.0, 0.0], color=GREY, linewidth=1.2)
# 塔
ax3.plot([XF, XF], [0.0, HT], color=WARM, linewidth=3.2)
# 見通し線
ax3.plot([XA, TOP[0]], [0.0, TOP[1]], color=ACCENT, linewidth=2.0)
ax3.plot([XB, TOP[0]], [0.0, TOP[1]], color=GREEN, linewidth=2.0)

# 足もとの直角
sq = 0.30
ax3.plot([XF - sq, XF - sq, XF], [0.0, sq, sq], color=GREY, linewidth=1.0)

# 角の弧
for _x, _r in ((XA, 1.25), (XB, 1.05)):
    _th = np.linspace(0.0, np.arctan2(HT, XF - _x), 60)
    ax3.plot(_x + _r * np.cos(_th), _r * np.sin(_th), color=INK,
             linewidth=1.2)

ax3.plot([XA, XB], [0.0, 0.0], marker="o", markersize=5, color=INK,
         linestyle="none", zorder=3)
ax3.text(XA - 0.42, -0.34, "$A$", fontsize=12, color=INK)
ax3.text(XB - 0.14, -0.78, "$B$", fontsize=12, color=INK)
ax3.text(1.34, 0.26, "$30°$", fontsize=11, color=INK)
ax3.text(4.34, 0.30, "$45°$", fontsize=11, color=INK)
ax3.text(1.55, -0.78, "$40$ m", fontsize=11, color=INK, ha="center")
ax3.text(5.95, -0.78, "$x$ m", fontsize=11, color=INK, ha="center")
ax3.text(XF + 0.20, HT / 2 - 0.18, "$h$", fontsize=13, color=WARM)

for _fig, _name in ((fig1, "aasl-3-3-idea-a.svg"),
                    (fig2, "aasl-3-3-idea-b.svg"),
                    (fig3, "aasl-3-3-idea-c.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
