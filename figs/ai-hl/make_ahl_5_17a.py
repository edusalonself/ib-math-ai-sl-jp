"""AHL 5.17a（異なる 2 つの実固有値の phase portrait）の図を作る。ラベルは英語。
   ★ 4 枚組は 2 行 2 列（AHL 5.15 / 5.16 と同じ理由）。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_17a.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)
R = 4.0
XR = YR = (-R, R)
TICKS = [-4, -2, 0, 2, 4]


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def frame(ax):
    ax.set_xlim(*XR)
    ax.set_ylim(*YR)
    ax.set_aspect("equal")
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color=GREY, lw=1.0, alpha=0.6, zorder=1)
    ax.axvline(0, color=GREY, lw=1.0, alpha=0.6, zorder=1)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)
    ax.set_xticks(TICKS)
    ax.set_yticks(TICKS)
    ax.set_xlabel("$x$", fontsize=12)
    ax.set_ylabel("$y$", fontsize=12)


def traj(ax, M, p0, col=LINE, lw=2.2, tmax=6.0, n=4000, zorder=5,
         arrow_at=0.45, both=True):
    """dX/dt = M X を RK4 で前後にたどる（図を描くためだけのもの）。"""
    M = np.array(M, dtype=float)

    def march(sign):
        h = sign * tmax / n
        X = np.array(p0, dtype=float)
        pts = [X.copy()]
        for _ in range(n):
            k1 = M @ X
            k2 = M @ (X + h * k1 / 2)
            k3 = M @ (X + h * k2 / 2)
            k4 = M @ (X + h * k3)
            X = X + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            if np.max(np.abs(X)) > 3 * R:
                break
            pts.append(X.copy())
        return np.array(pts)

    # ★ node の図では前向きだけを描く。前後をつなぐと、原点の反対側から
    #   来たように見えて、軌道どうしが交わっているように読めてしまう。
    fwd = march(+1)
    P = np.vstack([march(-1)[::-1], fwd[1:]]) if both else fwd
    ax.plot(P[:, 0], P[:, 1], color=col, lw=lw, zorder=zorder)
    # 進む向きの矢印を 1 本
    i = int(len(P) * arrow_at)
    if 0 < i < len(P) - 3:
        ax.annotate("", xy=P[i + 3], xytext=P[i],
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=lw + 0.3),
                    zorder=zorder + 1)
    return P


def eigline(ax, v, col, lab=None, lw=2.6, outward=True, labxy=None):
    """eigenvector 方向の直線と、その上を進む向きの矢印。"""
    v = np.array(v, dtype=float)
    v = v / np.linalg.norm(v)
    s = np.linspace(-1.35 * R, 1.35 * R, 2)
    ax.plot(s * v[0], s * v[1], color=col, lw=lw, zorder=4)
    for sgn in (+1, -1):
        a, b = (1.6, 2.7) if outward else (2.7, 1.6)
        ax.annotate("", xy=sgn * b * v, xytext=sgn * a * v,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4),
                    zorder=6)
    if lab:
        p = labxy if labxy is not None else 3.15 * v
        ax.text(p[0], p[1], lab, fontsize=11.5, color=col, ha="center",
                va="center", bbox=BOX, zorder=8)


# 3 つの行列（すべて固有ベクトルが (1,1) と (1,-1)）
M_OUT = [[3, 2], [2, 3]]        # lambda = 5, 1   両方正
M_IN = [[-3, 2], [2, -3]]       # lambda = -1, -5 両方負
M_SAD = [[1, 2], [2, 1]]        # lambda = 3, -1  異符号
V1 = (1, 1)
V2 = (1, -1)


# ═════════════ 1a. eigenvector の方向 ═════════════
fig, ax = plt.subplots(figsize=(5.8, 5.4))
frame(ax)
eigline(ax, V1, ACC, "$\\lambda_1 = 5$\n$\\mathbf{p}_1 = \\binom{1}{1}$",
        outward=True, labxy=(2.55, 3.35))
eigline(ax, V2, GREEN, "$\\lambda_2 = 1$\n$\\mathbf{p}_2 = \\binom{1}{-1}$",
        outward=True, labxy=(2.75, -3.35))
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("along an eigenvector the path is a\nSTRAIGHT line through the origin",
             fontsize=12.5, color=INK, pad=10)
fig.text(0.5, -0.03,
         "Both $\\lambda > 0$, so both arrows point AWAY from the origin.",
         fontsize=11, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-17a-eigen.svg")


# ═════════════ 1b. node の 2 つ（1×2） ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.0, 5.4))

# (a) 両方正
ax = axs[0]
frame(ax)
eigline(ax, V1, ACC, outward=True, lw=2.0)
eigline(ax, V2, GREEN, outward=True, lw=2.0)
for p in [(0.60, -0.50), (0.50, -0.60), (-0.60, 0.50), (-0.50, 0.60),
          (0.55, 0.05), (-0.55, -0.05)]:
    traj(ax, M_OUT, p, col=LINE, lw=2.0, tmax=3.0, both=False)
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("(a)  $\\lambda = 5,\\ 1$  (both POSITIVE)\nall paths move AWAY from the origin",
             fontsize=12.5, color=LINE, pad=10)

# (b) 両方負
ax = axs[1]
frame(ax)
eigline(ax, V1, ACC, outward=False, lw=2.0)
eigline(ax, V2, GREEN, outward=False, lw=2.0)
for p in [(3.7, 1.0), (-3.7, -1.0), (1.0, 3.7), (-1.0, -3.7),
          (3.6, -2.2), (-3.6, 2.2)]:
    traj(ax, M_IN, p, col=LINE, lw=2.0, tmax=5.0, both=False)
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("(b)  $\\lambda = -1,\\ -5$  (both NEGATIVE)\nall paths move TOWARDS the origin",
             fontsize=12.5, color=LINE, pad=10)

fig.text(0.5, -0.07,
         "The two eigenvector directions are the SKELETON of the picture.\n"
         "A positive $\\lambda$ pushes outwards along its own direction,\n"
         "a negative $\\lambda$ pulls inwards along its own direction.",
         fontsize=12.5, ha="center", va="top", color=INK,
         linespacing=1.5)
fig.tight_layout()
save(fig, "ahl-5-17a-nodes.svg")


# ═════════════ 1c. saddle ═════════════
fig, ax = plt.subplots(figsize=(5.8, 5.4))
frame(ax)
eigline(ax, V1, ACC, "$\\lambda = 3$\nOUT", outward=True, lw=2.2,
        labxy=(2.6, 3.4))
eigline(ax, V2, GREEN, "$\\lambda = -1$\nIN", outward=False, lw=2.2,
        labxy=(2.8, -3.4))
for p in [(1.4, -1.15), (-1.4, 1.15), (1.15, -1.4), (-1.15, 1.4),
          (2.6, -3.4), (-2.6, 3.4)]:
    traj(ax, M_SAD, p, col=LINE, lw=2.0, tmax=3.2, both=False)
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("$\\lambda = 3,\\ -1$  (OPPOSITE signs)\nthe origin is a SADDLE POINT",
             fontsize=12.5, color=GOLD, pad=10)

fig.tight_layout()
save(fig, "ahl-5-17a-saddle.svg")


# ═════════════ 2. 長い目で見るとどうなるか（1×2） ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.0, 5.4))

ax = axs[0]
frame(ax)
eigline(ax, V1, ACC, "$\\lambda = 5$", outward=True, lw=2.2,
        labxy=(3.0, 3.45))
eigline(ax, V2, GREEN, "$\\lambda = 1$", outward=True, lw=2.2,
        labxy=(3.1, -3.45))
# ★ 出発点は原点のすぐ近くにとる。離れた点から始めると、λ=5 の向きに
#    そろう前に窓の外へ出てしまい、「そろう」ところが見えない。
for p, c in (((0.60, -0.50), LINE), ((0.50, -0.60), GOLD),
             ((-0.60, 0.50), LINE), ((-0.50, 0.60), GOLD)):
    traj(ax, M_OUT, p, col=c, lw=2.2, tmax=3.0, both=False)
ax.plot([0], [0], "o", color=INK, ms=8, zorder=9)
ax.set_title("paths set off near the $\\lambda = 1$ direction,\nthen BEND towards the $\\lambda = 5$ direction",
             fontsize=12.5, color=ACC, pad=10)

ax = axs[1]
frame(ax)
eigline(ax, V1, ACC, "$\\lambda = 3$", outward=True, lw=2.2,
        labxy=(3.0, 3.45))
eigline(ax, V2, GREEN, "$\\lambda = -1$", outward=False, lw=2.2,
        labxy=(3.1, -3.45))
# ★ (1.4, -1.15) は直線 y = -x の【上】、(-1.4, 1.15) は【下】。
#    色と説明が入れかわらないよう、対応をここで固定する。
traj(ax, M_SAD, (1.4, -1.15), col=LINE, lw=2.4, tmax=3.2, both=False)
traj(ax, M_SAD, (-1.4, 1.15), col=GOLD, lw=2.4, tmax=3.2, both=False)
ax.text(-3.85, 3.8, "start just ABOVE the $\\lambda = -1$ line\n"
                    "$\\rightarrow$ leaves TOP RIGHT",
        fontsize=10.5, color=LINE, bbox=BOX, zorder=9, va="top", ha="left")
ax.text(-3.85, -2.3, "start just BELOW it\n$\\rightarrow$ leaves BOTTOM LEFT",
        fontsize=10.5, color=GOLD, bbox=BOX, zorder=9, va="top", ha="left")
ax.plot([0], [0], "o", color=INK, ms=8, zorder=9)
ax.set_title("at a saddle, which SIDE you start on\ndecides where you end up",
             fontsize=12.5, color=GOLD, pad=10)

fig.text(0.5, -0.13,
         "The term with the biggest $\\lambda$ grows fastest, so it takes over\n"
         "whenever its coefficient is not zero: the further out you go,\n"
         "the closer the path gets to that direction.\n"
         "At a saddle, the $\\lambda < 0$ line is the dividing line — paths that\n"
         "are not on it eventually leave along the $\\lambda > 0$ line.",
         fontsize=12.5, ha="center", va="top", color=INK,
         linespacing=1.5)
fig.tight_layout()
save(fig, "ahl-5-17a-longrun.svg")

print("figures written to", os.path.normpath(OUT))
