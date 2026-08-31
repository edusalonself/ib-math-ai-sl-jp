"""AHL 1.15 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-hl/01-number-and-algebra/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_1_15.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _matrix import (INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX,
                     blank, matrix, label, arrow)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight")
    plt.close(fig)


def axes(ax, xlim, ylim, xt=1, yt=1):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    for x in np.arange(np.ceil(xlim[0] / xt) * xt, xlim[1] + 1e-9, xt):
        ax.axvline(x, color=GRID, lw=0.7, zorder=0)
    for y in np.arange(np.ceil(ylim[0] / yt) * yt, ylim[1] + 1e-9, yt):
        ax.axhline(y, color=GRID, lw=0.7, zorder=0)
    ax.axhline(0, color=GREY, lw=1.2, zorder=1)
    ax.axvline(0, color=GREY, lw=1.2, zorder=1)
    ax.tick_params(labelsize=8.5, colors=GREY, length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_aspect("equal")


def vec(ax, v, color, lw=2.6, z=6):
    ax.annotate("", xy=(v[0], v[1]), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=15), zorder=z)


M = np.array([[4.0, 1.0], [2.0, 3.0]])

# ══════════════ 1. 固有ベクトルとは何か ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.8))

# 左：ふつうのベクトル（向きが変わる）
ax = axs[0]
axes(ax, (-1.2, 5.6), (-1.2, 5.6), 1, 1)
u = np.array([1.2, 0.4])
Mu = M @ u                       # [5.2, 3.6]
ax.plot([0, 5.4], [0, 5.4 * u[1] / u[0]], color=LINE, lw=1.0, ls=":",
        zorder=2)
vec(ax, u, LINE)
vec(ax, Mu, ACC)
label(ax, u[0] + 0.15, u[1] - 0.45, "$\\mathbf{u}$", color=LINE, fs=14,
      ha="left")
label(ax, Mu[0] - 0.25, Mu[1] + 0.40, "$M\\mathbf{u}$", color=ACC, fs=14,
      ha="right")
ax.set_title("an ordinary vector:  the DIRECTION changes",
             fontsize=12.5, color=ACC, pad=8)
label(ax, 2.9, -0.85, "$M\\mathbf{u}$ is off the dotted line", color=GREY,
      fs=11.5)

# 右：固有ベクトル（向きは同じ、長さだけ変わる）
ax = axs[1]
axes(ax, (-1.2, 5.6), (-1.2, 5.6), 1, 1)
v = np.array([1.0, 1.0])
Mv = M @ v                       # [5, 5]
ax.plot([-1.0, 5.4], [-1.0, 5.4], color=GREEN, lw=1.0, ls=":", zorder=2)
vec(ax, Mv, GREEN, lw=2.6)
vec(ax, v, LINE, lw=3.2, z=7)
label(ax, v[0] + 0.28, v[1] - 0.28, "$\\mathbf{v}$", color=LINE, fs=14,
      ha="left")
label(ax, Mv[0] - 0.30, Mv[1] + 0.35, "$M\\mathbf{v} = 5\\mathbf{v}$",
      color=GREEN, fs=14, ha="right")
ax.set_title("an EIGENVECTOR:  same line, $5$ times as long",
             fontsize=12.5, color=GREEN, pad=8)
label(ax, 2.9, -0.85, "the number $5$ is the EIGENVALUE", color=GOLD,
      fs=11.5)

fig.tight_layout()
save(fig, "ahl-1-15-idea.svg")


# ══════════════ 2. characteristic equation ══════════════
fig, ax = plt.subplots(figsize=(8.6, 5.2))
blank(ax, (-0.8, 10.4), (-3.95, 3.4))
ax.set_aspect("auto")

ax.text(4.8, 3.0, "$M\\mathbf{v} = \\lambda\\mathbf{v}$   with   "
                  "$\\mathbf{v} \\neq \\mathbf{0}$",
        fontsize=17, ha="center", va="center", color=INK)
arrow(ax, (4.8, 2.55), (4.8, 1.95), color=GOLD, lw=1.8)

ax.text(4.8, 1.50, "$\\det(M - \\lambda I) = 0$", fontsize=19, ha="center",
        va="center", color=ACC)
ax.text(4.8, 0.80, "NOT in the formula booklet  —  learn this one",
        fontsize=12.5, ha="center", va="center", color=GOLD)

arrow(ax, (4.8, 0.30), (4.8, -0.35), color=GREY, lw=1.6)

# 一般形
ax.text(4.8, -0.85,
        "$\\lambda^{2} - (a+d)\\,\\lambda + (ad-bc) = 0$",
        fontsize=17, ha="center", va="center", color=INK)
ax.text(2.05, -1.80, "sum of the diagonal", fontsize=11.5, ha="center",
        va="center", color=GREEN)
ax.text(7.45, -1.80, "$\\det M$", fontsize=12.5, ha="center", va="center",
        color=GREEN)
arrow(ax, (2.75, -1.62), (4.05, -1.15), color=GREEN, lw=1.2, rad=-0.22,
      scale=10)
arrow(ax, (6.95, -1.62), (6.25, -1.15), color=GREEN, lw=1.2, rad=0.22,
      scale=10)

# 具体例
ax.plot([0.2, 9.4], [-2.45, -2.45], color=GRID, lw=1.2)
matrix(ax, 1.5, -3.25, [["4", "1"], ["2", "3"]], cw=0.52, ch=0.42, fs=12)
ax.text(2.55, -3.25, "$\\Rightarrow$", fontsize=13, ha="center",
        va="center", color=GREY)
ax.text(4.55, -3.25, "$\\lambda^{2} - 7\\lambda + 10 = 0$", fontsize=14,
        ha="center", va="center", color=INK)
ax.text(6.35, -3.25, "$\\Rightarrow$", fontsize=13, ha="center",
        va="center", color=GREY)
ax.text(8.00, -3.25, "$\\lambda = 5$  or  $\\lambda = 2$", fontsize=14,
        ha="center", va="center", color=ACC)

fig.tight_layout()
save(fig, "ahl-1-15-char.svg")


# ══════════════ 3. 手順は4つ ══════════════
fig, ax = plt.subplots(figsize=(9.0, 3.0))
blank(ax, (-0.5, 12.2), (-1.35, 1.35))
ax.set_aspect("auto")

steps = [("1", "find the\nEIGENVALUES", "$\\det(M-\\lambda I)=0$", ACC),
         ("2", "find an\nEIGENVECTOR", "for each $\\lambda$", GREEN),
         ("3", "build\n$P$ and $D$", "columns $\\leftrightarrow$ diagonal",
          LINE),
         ("4", "use\n$M^{n}=PD^{n}P^{-1}$", "booklet", GOLD)]
xs = [1.1, 4.0, 6.9, 9.8]
for (n, t, sub, col), x in zip(steps, xs):
    ax.text(x, 0.92, n, fontsize=12, ha="center", va="center", color="white",
            zorder=8,
            bbox=dict(boxstyle="circle,pad=0.34", facecolor=col,
                      edgecolor="none"))
    ax.text(x, 0.12, t, fontsize=12.5, ha="center", va="center", color=INK)
    ax.text(x, -0.78, sub, fontsize=11, ha="center", va="center", color=col)
for x in xs[:-1]:
    arrow(ax, (x + 1.15, 0.12), (x + 1.75, 0.12), color=GREY, lw=1.5)

fig.tight_layout()
save(fig, "ahl-1-15-steps.svg")


# ══════════════ 4. P と D の並べ方 ══════════════
fig, ax = plt.subplots(figsize=(8.2, 4.4))
blank(ax, (-0.9, 9.5), (-2.5, 2.7))

cP, _ = matrix(ax, 1.6, 0.75, [["1", "1"], ["1", "$-2$"]], cw=0.74, ch=0.66,
               fs=15, cell_color={(0, 0): ACC, (1, 0): ACC,
                                  (0, 1): GREEN, (1, 1): GREEN})
ax.text(1.6, 1.85, "$P$", fontsize=15, ha="center", va="center", color=INK)
ax.text(1.6, -0.55, "eigenvectors as COLUMNS", fontsize=11.5, ha="center",
        va="center", color=INK)

cD, _ = matrix(ax, 5.8, 0.75, [["5", "0"], ["0", "2"]], cw=0.74, ch=0.66,
               fs=15, cell_color={(0, 0): ACC, (1, 1): GREEN})
ax.text(5.8, 1.85, "$D$", fontsize=15, ha="center", va="center", color=INK)
ax.text(5.8, -0.55, "eigenvalues on the DIAGONAL", fontsize=11.5,
        ha="center", va="center", color=INK)

arrow(ax, (cP[(0, 0)][0], 1.35), (cD[(0, 0)][0], 1.35), color=ACC, lw=1.5,
      rad=-0.22)
ax.text(3.7, 2.25, "$\\lambda = 5$  goes with the FIRST column",
        fontsize=11.5, ha="center", va="center", color=ACC)

arrow(ax, (cP[(0, 1)][0], 0.05), (cD[(1, 1)][0], 0.05), color=GREEN, lw=1.5,
      rad=0.16)
ax.text(3.7, -1.35, "$\\lambda = 2$  goes with the SECOND column",
        fontsize=11.5, ha="center", va="center", color=GREEN)

ax.text(4.0, -2.10, "swap one and not the other, and $PDP^{-1}$ "
                    "is no longer $M$",
        fontsize=12.5, ha="center", va="center", color=GOLD)
fig.tight_layout()
save(fig, "ahl-1-15-pd.svg")


# ══════════════ 5. 2つの町の人口 ══════════════
T = np.array([[0.8, 0.1], [0.2, 0.9]])
s = np.array([24000.0, 6000.0])
yrs = 26
A, B = [s[0]], [s[1]]
for _ in range(yrs):
    s = T @ s
    A.append(s[0])
    B.append(s[1])
t = np.arange(yrs + 1)

fig, ax = plt.subplots(figsize=(8.4, 4.6))
ax.set_xlim(-1.2, 27.2)
ax.set_ylim(0, 26000)
for y in range(0, 26001, 5000):
    ax.axhline(y, color=GRID, lw=0.7, zorder=0)
for x in range(0, 27, 5):
    ax.axvline(x, color=GRID, lw=0.7, zorder=0)
ax.axhline(10000, color=ACC, lw=1.2, ls="--", zorder=2)
ax.axhline(20000, color=GREEN, lw=1.2, ls="--", zorder=2)
ax.plot(t, A, "o-", color=ACC, lw=2.4, ms=4, zorder=6, label="Town A")
ax.plot(t, B, "o-", color=GREEN, lw=2.4, ms=4, zorder=6, label="Town B")
ax.tick_params(labelsize=9, colors=GREY, length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_xlabel("years", fontsize=11, color=INK)
ax.set_ylabel("population", fontsize=11, color=INK, labelpad=8)
ax.text(13.0, 24200, "whatever we start with, the split settles at "
                     "$1 : 2$", fontsize=12.5, ha="center", va="center",
        color=GOLD)
ax.text(18.0, 15000, "that ratio is the eigenvector for $\\lambda = 1$",
        fontsize=11.5, ha="center", va="center", color=INK, bbox=BOX,
        zorder=10)
ax.legend(loc="lower right", fontsize=10.5, frameon=False,
          bbox_to_anchor=(0.99, 0.06))
fig.tight_layout()
save(fig, "ahl-1-15-towns.svg")

print("figures written to", os.path.normpath(OUT))
