"""SL 3.5 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_3_5.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, FILL = "#7a8592", "#eaf2fb"
GOLD = "#b9770e"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.9)


def grid(ax, xlim, ylim, step=1, ticks=2):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    for x in np.arange(np.ceil(xlim[0]), xlim[1] + 1e-9, step):
        ax.axvline(x, color=GRID, lw=0.8, zorder=0)
    for y in np.arange(np.ceil(ylim[0]), ylim[1] + 1e-9, step):
        ax.axhline(y, color=GRID, lw=0.8, zorder=0)
    ax.axhline(0, color=GREY, lw=1.2, zorder=1)
    ax.axvline(0, color=GREY, lw=1.2, zorder=1)
    ax.set_xticks(np.arange(np.ceil(xlim[0] / ticks) * ticks, xlim[1] + 1e-9, ticks))
    ax.set_yticks(np.arange(np.ceil(ylim[0] / ticks) * ticks, ylim[1] + 1e-9, ticks))
    ax.tick_params(labelsize=8.5, colors=GREY, length=0)
    for s in ax.spines.values():
        s.set_visible(False)


def pt(ax, p, label, dx=0.25, dy=0.25, color=INK, ha="left", va="bottom", fs=11):
    ax.plot([p[0]], [p[1]], "o", color=color, ms=6, zorder=8)
    ax.text(p[0] + dx, p[1] + dy, label, color=color, ha=ha, va=va,
            fontsize=fs, zorder=9, bbox=BOX)


def rt_mark(ax, c, d1, d2, size=0.42, color=GREY):
    c = np.asarray(c, float)
    u = np.asarray(d1, float); u = u / np.linalg.norm(u) * size
    v = np.asarray(d2, float); v = v / np.linalg.norm(v) * size
    p = np.array([c + u, c + u + v, c + v])
    ax.plot(p[:, 0], p[:, 1], color=color, lw=1.2, zorder=7)


# ══════════════ 1. perpendicular bisector とは何か ══════════════
fig, ax = plt.subplots(figsize=(8.0, 5.4))
A, B = np.array([1.0, 2.0]), np.array([7.0, 6.0])
M = (A + B) / 2
mp = -3 / 2
xs = np.array([2.4, 5.6])
ys = mp * (xs - M[0]) + M[1]

grid(ax, (-0.6, 8.6), (-0.6, 9.4))
ax.plot([A[0], B[0]], [A[1], B[1]], color=GOLD, lw=2.2, zorder=5)
ax.plot(xs, ys, color=ACC, lw=2.4, zorder=6)

# 線上の3点から A, B への等距離
for t in (2.6, 5.4):
    P = np.array([t, mp * (t - M[0]) + M[1]])
    ax.plot([P[0], A[0]], [P[1], A[1]], color=GREEN, lw=1.2, ls="--", zorder=4)
    ax.plot([P[0], B[0]], [P[1], B[1]], color=GREEN, lw=1.2, ls="--", zorder=4)
    ax.plot([P[0]], [P[1]], "o", color=ACC, ms=5, zorder=8)

rt_mark(ax, M, B - A, np.array([1, mp]))
pt(ax, A, "$A$", -0.28, -0.10, ha="right", va="top")
pt(ax, B, "$B$", 0.26, 0.06)
pt(ax, M, "$M$  (midpoint)", 0.30, -0.34, color=GOLD, va="top")
ax.text(2.35, 7.6, "perpendicular\nbisector of $AB$", color=ACC, fontsize=11,
        ha="center", va="center", zorder=9, bbox=BOX)
ax.text(4.2, 0.55, "every point on this line is the same\n"
                   "distance from $A$ as it is from $B$",
        color=GREEN, fontsize=11, ha="center", va="center", zorder=9, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-5-idea.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 3つの手順 ══════════════
fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.6))

for ax in axes:
    grid(ax, (-0.6, 8.8), (-0.6, 10.6))
    ax.plot([A[0], B[0]], [A[1], B[1]], color=GOLD, lw=2.0, zorder=5)

# --- step 1: midpoint
ax = axes[0]
pt(ax, A, "$A(1,2)$", -0.28, -0.12, ha="right", va="top")
pt(ax, B, "$B(7,6)$", 0.24, 0.10)
pt(ax, M, "$(4,4)$", 0.30, -0.34, color=ACC, va="top")
ax.set_title("1.  midpoint of $AB$", fontsize=11.5, color=INK, pad=8)
ax.text(4.1, 9.5, r"$\left(\frac{1+7}{2},\ \frac{2+6}{2}\right)=(4,4)$",
        ha="center", va="center", fontsize=12, zorder=9)

# --- step 2: gradient of AB
ax = axes[1]
ax.plot([A[0], B[0], B[0]], [A[1], A[1], B[1]], color=GREEN, lw=1.6,
        ls="--", zorder=4)
pt(ax, A, "$A$", -0.28, -0.12, ha="right", va="top")
pt(ax, B, "$B$", 0.24, 0.10)
ax.text(4.0, 1.55, "run $=6$", color=GREEN, ha="center", va="center",
        fontsize=10.5, zorder=9, bbox=BOX)
ax.text(7.25, 4.0, "rise $=4$", color=GREEN, ha="left", va="center",
        fontsize=10.5, zorder=9, bbox=BOX)
ax.set_title("2.  gradient of $AB$", fontsize=11.5, color=INK, pad=8)
ax.text(4.1, 9.5, r"$m=\frac{6-2}{7-1}=\frac{4}{6}=\frac{2}{3}$",
        ha="center", va="center", fontsize=12, zorder=9)

# --- step 3: perpendicular gradient + line
ax = axes[2]
xs3 = np.array([1.6, 6.4])
ax.plot(xs3, mp * (xs3 - M[0]) + M[1], color=ACC, lw=2.4, zorder=6)
rt_mark(ax, M, B - A, np.array([1, mp]))
pt(ax, M, "$(4,4)$", 0.30, -0.34, color=ACC, va="top")
ax.set_title("3.  perpendicular gradient", fontsize=11.5, color=INK, pad=8)
ax.text(4.1, 9.5, r"$m_{\perp}=-\frac{3}{2}$,   $y=-\frac{3}{2}x+10$",
        ha="center", va="center", fontsize=12, zorder=9)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-5-steps.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. 垂直な傾き：ひっくり返して符号を変える ══════════════
fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.8))

# --- (a) gradient 2/3
ax = axes[0]
grid(ax, (-1.4, 5.4), (-3.4, 3.4))
xs = np.array([-1.0, 5.0])
ax.plot(xs, (2 / 3) * xs, color=GOLD, lw=2.4, zorder=6)
ax.plot([0, 3, 3], [0, 0, 2], color=GREEN, lw=1.8, zorder=5)
ax.text(1.5, -0.55, "run $3$", color=GREEN, ha="center", va="top",
        fontsize=11, zorder=9, bbox=BOX)
ax.text(3.25, 1.0, "rise $2$", color=GREEN, ha="left", va="center",
        fontsize=11, zorder=9, bbox=BOX)
ax.text(0.2, 2.85, r"$m=\dfrac{2}{3}$", color=GOLD, ha="left", va="center",
        fontsize=14, zorder=9, bbox=BOX)

# --- (b) perpendicular
ax = axes[1]
grid(ax, (-1.4, 5.4), (-3.4, 3.4))
ax.plot(xs, (2 / 3) * xs, color=GRID, lw=1.6, zorder=3)
ax.plot(np.array([-1.4, 2.0]), -1.5 * np.array([-1.4, 2.0]),
        color=ACC, lw=2.4, zorder=6)
ax.plot([0, 2, 2], [0, 0, -3], color=GREEN, lw=1.8, zorder=5)
ax.text(1.0, 0.30, "run $2$", color=GREEN, ha="center", va="bottom",
        fontsize=11, zorder=9, bbox=BOX)
ax.text(2.25, -1.5, "rise $-3$", color=GREEN, ha="left", va="center",
        fontsize=11, zorder=9, bbox=BOX)
ax.text(-1.2, 2.85, r"$m_{\perp}=-\dfrac{3}{2}$", color=ACC, ha="left",
        va="center", fontsize=14, zorder=9, bbox=BOX)

fig.suptitle("turn the step through $90^{\\circ}$:  run and rise swap over, "
             "and one of them changes sign",
             y=1.02, fontsize=11.5, color=INK)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-5-gradient.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 特別な場合：たて・よこ ══════════════
fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.8))

# --- (a) 縦の線分 → 横の垂直二等分線
ax = axes[0]
grid(ax, (-4.5, 8.5), (-4.5, 8.5), ticks=2)
P, Q = np.array([2.0, 7.0]), np.array([2.0, -3.0])
Mv = (P + Q) / 2
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=GOLD, lw=2.4, zorder=5)
ax.plot([-4.3, 8.3], [Mv[1], Mv[1]], color=ACC, lw=2.4, zorder=6)
rt_mark(ax, Mv, (0, 1), (1, 0), size=0.45)
pt(ax, P, "$A(2,7)$", 0.26, 0.06)
pt(ax, Q, "$B(2,-3)$", 0.26, -0.30, va="top")
pt(ax, Mv, "$(2,2)$", -0.30, 0.28, color=ACC, ha="right")
ax.text(5.6, 4.6, "$y=2$", color=ACC, ha="center", va="center",
        fontsize=14, zorder=9, bbox=BOX)
ax.set_title("$AB$ is vertical  $\\Rightarrow$  the bisector is horizontal",
             fontsize=11, color=INK, pad=8)

# --- (b) 横の線分 → 縦の垂直二等分線
ax = axes[1]
grid(ax, (-5.5, 7.5), (-5.5, 7.5), ticks=2)
R, S = np.array([-4.0, 1.0]), np.array([6.0, 1.0])
Mh = (R + S) / 2
ax.plot([R[0], S[0]], [R[1], S[1]], color=GOLD, lw=2.4, zorder=5)
ax.plot([Mh[0], Mh[0]], [-5.3, 7.3], color=ACC, lw=2.4, zorder=6)
rt_mark(ax, Mh, (1, 0), (0, 1), size=0.45)
pt(ax, R, "$C(-4,1)$", -0.32, 0.24, ha="right")
pt(ax, S, "$D(6,1)$", 0.26, 0.24)
pt(ax, Mh, "$(1,1)$", 0.30, -0.34, color=ACC, va="top")
ax.text(4.4, 5.4, "$x=1$", color=ACC, ha="center", va="center",
        fontsize=14, zorder=9, bbox=BOX)
ax.set_title("$CD$ is horizontal  $\\Rightarrow$  the bisector is vertical",
             fontsize=11, color=INK, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-5-special.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. 境界線としての使い方（SL 3.6 への橋） ══════════════
fig, ax = plt.subplots(figsize=(8.4, 5.6))
A2, B2 = np.array([2.0, 3.0]), np.array([10.0, 9.0])
M2 = (A2 + B2) / 2
mp2 = -4 / 3
XL, YL = (-0.6, 13.4), (-0.6, 14.4)
grid(ax, XL, YL, ticks=2)

xs = np.linspace(XL[0], XL[1], 200)
ys = mp2 * (xs - M2[0]) + M2[1]
ax.add_patch(Polygon(list(zip(xs, ys)) + [(XL[1], YL[0]), (XL[0], YL[0])],
                     closed=True, facecolor="#eaf2fb", edgecolor="none",
                     zorder=1))
ax.add_patch(Polygon(list(zip(xs, ys)) + [(XL[1], YL[1]), (XL[0], YL[1])],
                     closed=True, facecolor="#fdf1e6", edgecolor="none",
                     zorder=1))
ax.plot(xs, ys, color=ACC, lw=2.6, zorder=6)
ax.plot([A2[0], B2[0]], [A2[1], B2[1]], color=GREY, lw=1.4, ls="--", zorder=4)

pt(ax, A2, "$A(2,3)$", 0.28, -0.34, va="top")
pt(ax, B2, "$B(10,9)$", 0.28, 0.14)
pt(ax, M2, "$(6,6)$", 0.28, -0.34, color=ACC, va="top")
C2 = np.array([3.0, 9.0])
ax.plot([C2[0]], [C2[1]], "s", color=GREEN, ms=7, zorder=8)
ax.text(C2[0] - 0.30, C2[1] + 0.10, "house $C(3,9)$", color=GREEN,
        fontsize=10.5, ha="right", va="center", zorder=9, bbox=BOX)

ax.text(2.2, 1.0, "nearer to $A$", color=LINE, fontsize=12,
        ha="left", va="center", zorder=9, bbox=BOX)
ax.text(10.6, 13.2, "nearer to $B$", color=GOLD, fontsize=12,
        ha="center", va="center", zorder=9, bbox=BOX)
ax.text(11.6, 4.2, r"$y=-\frac{4}{3}x+14$", color=ACC, fontsize=12,
        ha="center", va="center", zorder=9, bbox=BOX)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-5-boundary.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
from math import hypot
from fractions import Fraction as F
def check(A, B, name):
    mx, my = F(int(A[0] + B[0]), 2), F(int(A[1] + B[1]), 2)
    print(f"{name}: midpoint ({mx},{my})", end="  ")
    if A[0] != B[0] and A[1] != B[1]:
        m = F(int(B[1] - A[1]), int(B[0] - A[0])); print(f"m={m}  m_perp={-1/m}")
    else:
        print("(vertical or horizontal)")
check(A, B, "fig 1/2  A(1,2) B(7,6)")
check(A2, B2, "fig 5    A(2,3) B(10,9)")
print("fig 5  C(3,9): dist to A =", round(hypot(1, 6), 3),
      " dist to B =", round(hypot(7, 0), 3), " -> nearer A")
print("figures written to", os.path.normpath(OUT))


# ══════════════════════════════════════════════════════════
#  GDC の画面 — 距離を平方根のテンプレートで 1 行入力したところ
#   （TI-Nspire CX II の計算画面をまねた図）
# ══════════════════════════════════════════════════════════
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(7.4, 1.35))
ax.set_xlim(0, 100); ax.set_ylim(0, 18); ax.axis("off")

SCR_BG, SCR_EDGE, TAB = "#f5f5f7", "#9aa0ac", "#8a8f9c"

# 画面の枠
ax.add_patch(Rectangle((0.8, 0.8), 98.4, 14.4, facecolor=SCR_BG,
                       edgecolor=SCR_EDGE, linewidth=1.1, zorder=2))
# 上のタブ帯（電卓の画面上部）
ax.add_patch(Rectangle((0.8, 15.2), 98.4, 1.9, facecolor="white",
                       edgecolor="none", zorder=2))
ax.add_patch(Rectangle((0.8, 16.4), 13.5, 0.7, facecolor=TAB,
                       edgecolor="none", zorder=3))
ax.add_patch(Rectangle((22.0, 16.4), 77.2, 0.7, facecolor=TAB,
                       edgecolor="none", zorder=3))

# 入れた式と、返ってきた答え
ax.text(4.0, 7.6, r"$\sqrt{(3-2)^{2}+(9-3)^{2}}$", fontsize=17,
        color="#3a3f46", ha="left", va="center", zorder=5)
ax.text(95.5, 7.6, "6.0827625", fontsize=16, color="#3a3f46",
        ha="right", va="center", zorder=5)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-5-gdc-distance.svg"), format="svg",
            bbox_inches="tight", transparent=True)
plt.close(fig)
print("wrote sl-3-5-gdc-distance.svg    check: sqrt(37) =", 37 ** 0.5)
