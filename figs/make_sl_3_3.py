"""SL 3.3 の図を作る。ラベルはすべて英語。
   出力先: 03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/make_sl_3_3.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, FILL = "#7a8592", "#eaf2fb"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.88)


def clean(ax, xlim=None, ylim=None, equal=True):
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal")
    ax.axis("off")


def ang_arc(ax, v, p1, p2, radius=1.0, color=ACC, lw=1.6):
    v = np.asarray(v, dtype=float)
    a1 = np.degrees(np.arctan2(p1[1] - v[1], p1[0] - v[0]))
    a2 = np.degrees(np.arctan2(p2[1] - v[1], p2[0] - v[0]))
    if a2 < a1:
        a1, a2 = a2, a1
    if a2 - a1 > 180:
        a1, a2 = a2, a1 + 360
    ax.add_patch(Arc(v, 2 * radius, 2 * radius, theta1=a1, theta2=a2,
                     color=color, linewidth=lw, zorder=6))


def rt_mark(ax, corner, d1, d2, size=0.5, color=GREY):
    c = np.asarray(corner, dtype=float)
    u = np.asarray(d1, float); u = u / np.linalg.norm(u) * size
    v = np.asarray(d2, float); v = v / np.linalg.norm(v) * size
    pts = np.array([c + u, c + u + v, c + v])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=1.1, zorder=7)


# ================= 1. elevation と depression =================
fig, ax = plt.subplots(figsize=(9.4, 4.8))

Gnd, Top = np.array([0.0, 0.0]), np.array([0.0, 4.0])
Boat = np.array([9.0, 0.0])

# 崖と地面
ax.plot([Gnd[0], Top[0]], [Gnd[1], Top[1]], color=INK, linewidth=2.2, zorder=5)
ax.plot([-1.2, 11.5], [0, 0], color=INK, linewidth=1.6, zorder=4)
# 見通し線
ax.plot([Top[0], Boat[0]], [Top[1], Boat[1]], color=ACC, linewidth=2.0, zorder=5)
# 上の水平線（点線）
ax.plot([Top[0], 7.2], [Top[1], Top[1]], color=GREY, linestyle="--",
        linewidth=1.5, zorder=4)

ang_arc(ax, Top, (7.2, 4.0), Boat, radius=2.4, color=ACC)
ax.annotate("angle of\ndepression", (2.9, 3.35), fontsize=10.5, color=ACC,
            ha="left", va="top", bbox=BOX, zorder=9)

ang_arc(ax, Boat, (-1.2, 0.0), Top, radius=2.0, color=GREEN)
ax.annotate("angle of\nelevation", (6.1, 0.30), fontsize=10.5, color=GREEN,
            ha="right", va="bottom", bbox=BOX, zorder=9)

rt_mark(ax, Gnd, (1, 0), (0, 1), size=0.45)
ax.scatter([Top[0]], [Top[1]], s=52, color=INK, zorder=8)
ax.scatter([Boat[0]], [Boat[1]], s=52, color=INK, zorder=8)
ax.annotate("$T$", Top + np.array([-0.45, 0.15]), fontsize=12)
ax.annotate("$B$", Boat + np.array([0.18, -0.42]), fontsize=12)

ax.annotate("the two horizontals are parallel,\nso these two angles are EQUAL",
            (10.9, 2.55), fontsize=10.5, color=INK, ha="right", va="center",
            bbox=BOX, zorder=9)
ax.annotate("both are measured\nfrom the HORIZONTAL", (5.0, -0.95),
            fontsize=10.5, color=GREY, ha="center", zorder=9)

clean(ax, (-1.6, 11.9), (-1.9, 5.0))
ax.set_title("Angle of elevation and angle of depression", fontsize=12.5, pad=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-3-elevation.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 2. bearing の基本 =================
fig, ax = plt.subplots(figsize=(7.0, 6.4))

R = 3.0
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(R * np.cos(th), R * np.sin(th), color=GRID, linewidth=1.4, zorder=2)
for a, lab in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
    v = np.array([np.sin(np.radians(a)), np.cos(np.radians(a))])
    ax.plot([0, R * v[0]], [0, R * v[1]], color=GREY, linewidth=1.1,
            linestyle=":", zorder=2)
    ax.annotate(lab, (R + 0.42) * v, fontsize=13, color=GREY, ha="center",
                va="center")

ax.plot([0, 0], [0, R + 0.05], color=INK, linewidth=1.8, zorder=4)

for a, col in [(60, ACC), (145, GREEN), (250, LINE), (310, GREY)]:
    v = np.array([np.sin(np.radians(a)), np.cos(np.radians(a))])
    ax.add_patch(FancyArrowPatch((0, 0), (R * 0.92 * v[0], R * 0.92 * v[1]),
                                 arrowstyle="-|>", color=col, linewidth=1.9,
                                 mutation_scale=15, zorder=5))
    ax.annotate(f"${a:03d}^\\circ$", (R * 1.14 * v[0], R * 1.14 * v[1]),
                fontsize=12, color=col, ha="center", va="center", zorder=8)

ax.add_patch(Arc((0, 0), 2 * 1.15, 2 * 1.15, theta1=30, theta2=90,
                 color=ACC, linewidth=1.6, zorder=6))
ax.annotate("measured\nCLOCKWISE\nfrom North", (0.30, 1.95), fontsize=10,
            color=ACC, ha="left", va="center", bbox=BOX, zorder=9)

ax.annotate("always THREE figures:  $060^\\circ$, not $60^\\circ$",
            (0, -4.15), fontsize=11.5, color=INK, ha="center")
clean(ax, (-4.6, 4.6), (-4.7, 4.3))
ax.set_title("Three-figure bearings", fontsize=12.5, pad=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-3-bearing.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 3. 2区間の航路と、Q での角 =================
fig, ax = plt.subplots(figsize=(8.6, 5.6))


def go(bear, dist, frm=(0.0, 0.0)):
    return (frm[0] + dist * np.sin(np.radians(bear)),
            frm[1] + dist * np.cos(np.radians(bear)))


P = (0.0, 0.0)
Q = go(70, 12, P)
Rr = go(160, 9, Q)

for pt in (P, Q):
    ax.plot([pt[0], pt[0]], [pt[1], pt[1] + 5.2], color=GREY, linestyle="--",
            linewidth=1.4, zorder=3)
    ax.annotate("N", (pt[0], pt[1] + 5.6), fontsize=11, color=GREY,
                ha="center", va="center")

ax.plot([P[0], Q[0]], [P[1], Q[1]], color=LINE, linewidth=2.4, zorder=5)
ax.plot([Q[0], Rr[0]], [Q[1], Rr[1]], color=GREEN, linewidth=2.4, zorder=5)
ax.plot([P[0], Rr[0]], [P[1], Rr[1]], color=ACC, linewidth=2.0,
        linestyle=":", zorder=4)

ang_arc(ax, P, (P[0], P[1] + 5), Q, radius=2.6, color=LINE)
ax.annotate("$070^\\circ$", (1.05, 2.95), fontsize=11.5, color=LINE, zorder=9)
ang_arc(ax, Q, (Q[0], Q[1] + 5), Rr, radius=2.6, color=GREEN)
ax.annotate("$160^\\circ$", (Q[0] + 1.35, Q[1] + 2.15), fontsize=11.5,
            color=GREEN, zorder=9)
ang_arc(ax, Q, P, Rr, radius=1.5, color=ACC)
ax.annotate("$P\\hat{Q}R$", (Q[0] - 2.55, Q[1] - 2.05), fontsize=12, color=ACC,
            bbox=BOX, zorder=9)

for pt, lab, off in [(P, "$P$", (-0.7, -0.5)), (Q, "$Q$", (0.35, 0.30)),
                     (Rr, "$R$", (0.35, -0.55))]:
    ax.scatter([pt[0]], [pt[1]], s=56, color=INK, zorder=8)
    ax.annotate(lab, (pt[0] + off[0], pt[1] + off[1]), fontsize=13)

ax.annotate("$12$ km", ((P[0] + Q[0]) / 2 - 1.5, (P[1] + Q[1]) / 2 + 0.35),
            fontsize=11, color=LINE, bbox=BOX, zorder=9)
ax.annotate("$9$ km", ((Q[0] + Rr[0]) / 2 + 0.55, (Q[1] + Rr[1]) / 2 + 0.45),
            fontsize=11, color=GREEN, bbox=BOX, zorder=9)

ax.annotate("the two North lines are parallel,\n"
            "so the angle at $Q$ can be found\n"
            "from the two bearings",
            (-4.8, 11.8), fontsize=10.5, color=INK, ha="left", va="top",
            bbox=BOX, zorder=9)

clean(ax, (-5.0, 18.0), (-6.6, 12.4))
ax.set_title("A journey given by bearings", fontsize=12.5, pad=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-3-journey.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 4. 文章から図をつくる =================
fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.6))

ax = axes[0]
ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.annotate("From a point $A$, the angle of\n"
            "elevation of the top of a tower\n"
            "is $32^\\circ$.\n\n"
            "From a point $C$, which is $40$ m\n"
            "nearer the tower on the same\n"
            "straight line, the angle of\n"
            "elevation is $47^\\circ$.",
            (0.06, 0.90), fontsize=12, ha="left", va="top", color=INK)
ax.set_title("the words", fontsize=11.5, pad=8)
ax.add_patch(FancyArrowPatch((0.86, 0.50), (1.06, 0.50), arrowstyle="-|>",
                             color=GREY, linewidth=2.0, mutation_scale=18,
                             clip_on=False))

ax = axes[1]
Ap, Cp, Bp = np.array([0.0, 0.0]), np.array([5.6, 0.0]), np.array([9.0, 0.0])
Tp = np.array([9.0, 5.6])
ax.plot([-0.8, 10.4], [0, 0], color=INK, linewidth=1.6, zorder=4)
ax.plot([Bp[0], Tp[0]], [Bp[1], Tp[1]], color=INK, linewidth=2.2, zorder=5)
ax.plot([Ap[0], Tp[0]], [Ap[1], Tp[1]], color=ACC, linewidth=1.9, zorder=5)
ax.plot([Cp[0], Tp[0]], [Cp[1], Tp[1]], color=GREEN, linewidth=1.9, zorder=5)
rt_mark(ax, Bp, (-1, 0), (0, 1), size=0.42)

ang_arc(ax, Ap, Bp, Tp, radius=1.9, color=ACC)
ax.annotate("$32^\\circ$", (1.95, 0.55), fontsize=11, color=ACC, zorder=9)
ang_arc(ax, Cp, Bp, Tp, radius=1.25, color=GREEN)
ax.annotate("$47^\\circ$", (6.35, 0.42), fontsize=11, color=GREEN,
            bbox=BOX, zorder=9)

ax.annotate("", xy=(Cp[0], -0.95), xytext=(Ap[0], -0.95),
            arrowprops=dict(arrowstyle="<->", color=GREY, linewidth=1.4))
ax.annotate("$40$ m", (2.8, -1.65), fontsize=11, color=GREY, ha="center")
ax.annotate("$h$", (9.35, 2.7), fontsize=13, color=INK)

for pt, lab, off in [(Ap, "$A$", (-0.15, -0.75)), (Cp, "$C$", (-0.15, -0.75)),
                     (Bp, "$B$", (0.22, -0.75)), (Tp, "$T$", (0.25, 0.12))]:
    ax.scatter([pt[0]], [pt[1]], s=48, color=INK, zorder=8)
    ax.annotate(lab, (pt[0] + off[0], pt[1] + off[1]), fontsize=12)

clean(ax, (-1.6, 11.4), (-2.6, 6.6))
ax.set_title("the labelled diagram", fontsize=11.5, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-3-words.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-3-3-elevation.svg, sl-3-3-bearing.svg, sl-3-3-journey.svg, "
      "sl-3-3-words.svg")
print("check journey: |PQ| =", round(float(np.hypot(*Q)), 4),
      " |QR| =", round(float(np.hypot(Rr[0]-Q[0], Rr[1]-Q[1])), 4),
      " |PR| =", round(float(np.hypot(*Rr)), 4))
