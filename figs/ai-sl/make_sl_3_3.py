"""SL 3.3 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_3_3.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl",
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


def bearing_arc(ax, pt, bearing, radius, color=ACC, lw=1.6):
    """North から時計回りに bearing 度ぶんの弧。180 度を超えても正しく回る。"""
    ax.add_patch(Arc(pt, 2 * radius, 2 * radius,
                     theta1=90.0 - bearing, theta2=90.0,
                     color=color, linewidth=lw, zorder=6))


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


# ================================================================
#  例題1〜5 の図（解説の中に置く。背景は透明にして callout になじませる）
# ================================================================
def we_fig(name, draw, figsize):
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), format="svg", bbox_inches="tight",
                transparent=True)
    plt.close(fig)


def ground(ax, x0, x1, y=0.0, tick=None, color=GREY):
    """水平な地面を、斜線つきで描く。"""
    ax.plot([x0, x1], [y, y], color=color, linewidth=1.6, zorder=3)
    t = (x1 - x0) / 26 if tick is None else tick
    for x in np.arange(x0 + t, x1, t * 1.5):
        ax.plot([x, x - t * 0.6], [y, y - t * 0.7], color=color,
                linewidth=0.9, zorder=3)


def north(ax, pt, length, label="N", color=GREY):
    ax.plot([pt[0], pt[0]], [pt[1], pt[1] + length], color=color,
            linestyle="--", linewidth=1.4, zorder=3)
    ax.annotate(label, (pt[0], pt[1] + length * 1.10), fontsize=11,
                color=color, ha="center", va="center")


def go(bear, dist, frm=(0.0, 0.0)):
    return (frm[0] + dist * np.sin(np.radians(bear)),
            frm[1] + dist * np.cos(np.radians(bear)))


# --- 例題1：塔と仰角 38 度 ---
def _w1(ax):
    A = np.array([0.0, 0.0])
    B = np.array([45.0, 0.0])
    T = np.array([45.0, 35.1579])
    ground(ax, -6, 56)
    ax.plot([B[0], T[0]], [B[1], T[1]], color=LINE, linewidth=2.8, zorder=6)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=GREEN, linewidth=2.8, zorder=6)
    ax.plot([A[0], T[0]], [A[1], T[1]], color=ACC, linewidth=2.4, zorder=5)
    rt_mark(ax, B, (-1, 0), (0, 1), size=2.6)
    ang_arc(ax, A, B, T, radius=9.5, color=ACC)
    ax.annotate(r"$38^{\circ}$", (11.4, 3.4), fontsize=12.5, color=ACC,
                zorder=9)
    ax.annotate("$45$ m", (22.5, -3.6), fontsize=12.5, color=GREEN,
                ha="center")
    ax.annotate("height $= ?$", (47.5, 17.5), fontsize=12.5, color=LINE,
                ha="left", va="center")
    ax.annotate("distance $= ?$", (20.0, 12.5), fontsize=12.5, color=ACC,
                ha="center", rotation=38, va="center")
    ax.scatter([A[0]], [A[1]], s=46, color=INK, zorder=8)
    clean(ax, (-12, 74), (-11, 44))
    ax.set_title("Angle of elevation from a point on the ground",
                 fontsize=11.5, pad=8)


we_fig("sl-3-3-we1.svg", _w1, (5.8, 3.9))


# --- 例題2：崖と船（50 m 近づく） ---
def _cliff(ax, boat_x, ang, ang_txt, ang_color, dist_txt, dist_color,
           title):
    T = np.array([0.0, 80.0])
    F = np.array([0.0, 0.0])
    B = np.array([boat_x, 0.0])
    ground(ax, -18, 215, tick=9)
    ax.plot([F[0], T[0]], [F[1], T[1]], color=LINE, linewidth=3.0, zorder=6)
    ax.plot([T[0], 205], [T[1], T[1]], color=GREY, linestyle="--",
            linewidth=1.4, zorder=4)
    ax.annotate("horizontal", (208, 80), fontsize=10, color=GREY,
                ha="left", va="center")
    ax.plot([T[0], B[0]], [T[1], B[1]], color=ang_color, linewidth=2.4,
            zorder=5)
    ang_arc(ax, T, (60, 80), B, radius=46, color=ang_color)
    th = np.radians(ang * 0.40)          # 弧の内側、水平線寄りに置く
    ax.annotate(ang_txt, (62 * np.cos(th), 80 - 62 * np.sin(th)),
                fontsize=13, color=ang_color, ha="center", va="center",
                zorder=9)
    rt_mark(ax, F, (1, 0), (0, 1), size=7)
    ax.annotate("$80$ m", (-6, 42), fontsize=12.5, color=LINE, ha="right",
                va="center")
    ax.annotate("", xy=(B[0], -20), xytext=(0, -20),
                arrowprops=dict(arrowstyle="<|-|>", color=dist_color, lw=1.4))
    ax.annotate(dist_txt, (B[0] / 2, -32), fontsize=12, color=dist_color,
                ha="center")
    ax.scatter([B[0]], [B[1]], s=52, color=INK, zorder=8)
    ax.annotate("boat", (B[0], 11), fontsize=11, color=INK, ha="center")
    clean(ax, (-40, 250), (-52, 100))
    ax.set_title(title, fontsize=11.5, pad=8)


fig, axes = plt.subplots(1, 2, figsize=(8.2, 2.64))
_cliff(axes[0], 179.6829, 24, r"$24^{\circ}$", ACC, "$d = ?$", ACC,
       "First position")
_cliff(axes[1], 129.6829, 31.67, r"$\theta = ?$", GREEN,
       r"$179.6\ldots - 50 = 129.6\ldots$ m", GREEN,
       "After moving $50$ m closer")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-3-we2.svg"), format="svg",
            bbox_inches="tight", transparent=True)
plt.close(fig)


# --- 例題3：P → Q → R の航路 ---
def _w3(ax):
    P = (0.0, 0.0)
    Q = go(70, 12, P)
    R = go(160, 9, Q)
    north(ax, P, 6.0)
    north(ax, Q, 6.0)
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=LINE, linewidth=2.6, zorder=5)
    ax.plot([Q[0], R[0]], [Q[1], R[1]], color=GREEN, linewidth=2.6, zorder=5)
    ax.plot([P[0], R[0]], [P[1], R[1]], color=ACC, linewidth=2.2,
            linestyle="--", zorder=5)
    ang_arc(ax, P, (P[0], P[1] + 5), Q, radius=3.0, color=LINE)
    ax.annotate(r"$070^{\circ}$", (1.15, 3.75), fontsize=11.5, color=LINE,
                zorder=9)
    ang_arc(ax, Q, (Q[0], Q[1] + 5), R, radius=3.0, color=GREEN)
    ax.annotate(r"$160^{\circ}$", (Q[0] + 1.6, Q[1] + 2.5), fontsize=11.5,
                color=GREEN, zorder=9)
    rt_mark(ax, Q, (P[0] - Q[0], P[1] - Q[1]), (R[0] - Q[0], R[1] - Q[1]),
            size=1.0)
    ax.annotate(r"$P\hat{Q}R = 90^{\circ}$", (15.4, 1.1),
                fontsize=11.5, color=INK, ha="left", zorder=9)
    ax.annotate("", xy=(11.7, 3.2), xytext=(15.2, 1.4),
                arrowprops=dict(arrowstyle="-", color=GREY, lw=1.1), zorder=7)
    ang_arc(ax, P, Q, R, radius=5.4, color=ACC)
    ax.annotate(r"$Q\hat{P}R = ?$", (6.2, 0.10), fontsize=11.5, color=ACC,
                ha="center", zorder=9)
    ax.annotate("$12$ km", (5.4, 2.75), fontsize=11.5, color=LINE,
                ha="center", rotation=20, zorder=9)
    ax.annotate("$9$ km", (Q[0] + 1.5, (Q[1] + R[1]) / 2), fontsize=11.5,
                color=GREEN, ha="left", zorder=9)
    ax.annotate("$PR = ?$", (8.6, -4.5), fontsize=11.5, color=ACC,
                ha="center", rotation=-17, zorder=9)
    for pt, lab, off in [(P, "$P$", (-1.1, -0.6)), (Q, "$Q$", (0.55, 0.55)),
                         (R, "$R$", (0.7, -0.6))]:
        ax.scatter([pt[0]], [pt[1]], s=52, color=INK, zorder=8)
        ax.annotate(lab, (pt[0] + off[0], pt[1] + off[1]), fontsize=13)
    clean(ax, (-4.5, 25.5), (-9.0, 12.5))
    ax.set_title("The two North lines are parallel", fontsize=11.5, pad=8)


we_fig("sl-3-3-we3.svg", _w3, (6.0, 4.4))


# --- 例題4：町 B から見た A と C ---
B4 = (0.0, 0.0)
A4 = go(48, 25, B4)
C4 = go(130, 18, B4)


def _w4_left(ax):
    north(ax, B4, 15.0)
    ax.plot([B4[0], A4[0]], [B4[1], A4[1]], color=LINE, linewidth=2.6, zorder=5)
    ax.plot([B4[0], C4[0]], [B4[1], C4[1]], color=GREEN, linewidth=2.6,
            zorder=5)
    ax.plot([A4[0], C4[0]], [A4[1], C4[1]], color=ACC, linewidth=2.2,
            linestyle="--", zorder=5)
    ang_arc(ax, B4, (B4[0], B4[1] + 10), A4, radius=8.0, color=LINE)
    ax.annotate(r"$048^{\circ}$", (2.0, 9.6), fontsize=11.5, color=LINE,
                ha="left", zorder=9)
    ang_arc(ax, B4, (B4[0], B4[1] + 10), C4, radius=12.5, color=GREEN)
    ax.annotate(r"$130^{\circ}$", (11.2, 5.6), fontsize=11.5, color=GREEN,
                ha="left", zorder=9)
    ang_arc(ax, B4, A4, C4, radius=4.6, color=ACC)
    ax.annotate(r"$A\hat{B}C = ?$", (5.6, -0.9), fontsize=11.5, color=ACC,
                ha="left", zorder=9)
    ax.annotate("$25$ km", (6.4, 12.4), fontsize=11.5, color=LINE,
                ha="center", rotation=42, zorder=9)
    ax.annotate("$18$ km", (4.2, -8.4), fontsize=11.5, color=GREEN,
                ha="center", rotation=-40, zorder=9)
    ax.annotate("$AC = ?$", (19.6, 3.0), fontsize=11.5, color=ACC,
                ha="left", zorder=9)
    for pt, lab, off in [(B4, "$B$", (-2.2, -1.6)), (A4, "$A$", (-2.4, 1.4)),
                         (C4, "$C$", (1.9, -1.6))]:
        ax.scatter([pt[0]], [pt[1]], s=52, color=INK, zorder=8)
        ax.annotate(lab, (pt[0] + off[0], pt[1] + off[1]), fontsize=13)
    clean(ax, (-10.0, 32.0), (-18.0, 26.0))
    ax.set_title("(a), (b):  both bearings are measured from $B$",
                 fontsize=11, pad=8)


def _w4_right(ax):
    north(ax, A4, 13.0)
    ax.plot([A4[0], B4[0]], [A4[1], B4[1]], color=LINE, linewidth=2.6, zorder=5)
    ax.plot([A4[0], C4[0]], [A4[1], C4[1]], color=ACC, linewidth=2.4, zorder=5)
    ax.plot([B4[0], C4[0]], [B4[1], C4[1]], color=GREY, linewidth=1.6,
            linestyle=":", zorder=4)
    bearing_arc(ax, A4, 228.0, 6.0, color=LINE)
    ax.annotate(r"$228^{\circ}$", (A4[0] + 8.2, A4[1] + 2.4), fontsize=11.5,
                color=LINE, ha="center", zorder=9)
    ang_arc(ax, A4, B4, C4, radius=11.0, color=ACC)
    ax.annotate(r"$B\hat{A}C = ?$", (A4[0] - 10.4, A4[1] - 12.6), fontsize=11.5,
                color=ACC, ha="center", zorder=9)
    ax.annotate("$AC = 28.7$ km", (A4[0] + 3.4, A4[1] - 15.0), fontsize=11,
                color=ACC, ha="left", rotation=-80, va="center", zorder=9)
    ax.annotate(r"bearing of $C$ from $A$ $= 228^{\circ} - B\hat{A}C$",
                (10.5, -16.6), fontsize=11, color=ACC, ha="center", zorder=9)
    for pt, lab, off in [(B4, "$B$", (-2.2, -1.6)), (A4, "$A$", (-2.6, 1.8)),
                         (C4, "$C$", (1.9, -1.6))]:
        ax.scatter([pt[0]], [pt[1]], s=52, color=INK, zorder=8)
        ax.annotate(lab, (pt[0] + off[0], pt[1] + off[1]), fontsize=13)
    clean(ax, (-12.0, 34.0), (-21.0, 34.0))
    ax.set_title("(c):  now the bearing is measured from $A$",
                 fontsize=11, pad=8)


fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.55))
_w4_left(axes[0])
_w4_right(axes[1])
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-3-we4.svg"), format="svg",
            bbox_inches="tight", transparent=True)
plt.close(fig)


# --- 例題5：2点から見上げる塔 ---
def _w5(ax):
    A = np.array([0.0, 0.0])
    C = np.array([40.0, 0.0])
    Bf = np.array([95.8543, 0.0])
    T = np.array([95.8543, 59.8964])
    ground(ax, -8, 112, tick=6)
    ax.plot([Bf[0], T[0]], [Bf[1], T[1]], color=LINE, linewidth=2.8, zorder=6)
    ax.plot([A[0], T[0]], [A[1], T[1]], color=GREY, linewidth=2.0, zorder=5)
    ax.plot([C[0], T[0]], [C[1], T[1]], color=ACC, linewidth=2.4, zorder=6)
    ax.plot([A[0], Bf[0]], [A[1], Bf[1]], color=INK, linewidth=2.0, zorder=5)
    rt_mark(ax, Bf, (-1, 0), (0, 1), size=4.4)
    ang_arc(ax, A, C, T, radius=17.0, color=GREY)
    ax.annotate(r"$32^{\circ}$", (18.6, 5.4), fontsize=12, color=GREY,
                zorder=9)
    ang_arc(ax, C, Bf, T, radius=11.0, color=ACC)
    ax.annotate(r"$47^{\circ}$", (51.5, 5.6), fontsize=12, color=ACC, zorder=9)
    ang_arc(ax, C, A, T, radius=17.0, color=GREEN)
    ax.annotate(r"$180^{\circ}-47^{\circ}$", (26.5, 27.5), fontsize=11,
                color=GREEN, ha="center", zorder=9)
    ang_arc(ax, T, A, C, radius=15.0, color=INK)
    ax.annotate(r"$A\hat{T}C = ?$", (74.0, 55.5), fontsize=11.5,
                color=INK, ha="center", zorder=9)
    ax.annotate("", xy=(A[0], -9.5), xytext=(C[0], -9.5),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.4))
    ax.annotate("$40$ m", (20.0, -16.5), fontsize=11.5, color=INK,
                ha="center")
    ax.annotate("$TC = ?$", (80.0, 20.0), fontsize=11.5, color=ACC,
                ha="center", rotation=47, zorder=9)
    ax.annotate("height $= ?$", (99.0, 30.0), fontsize=11.5, color=LINE,
                ha="left", va="center")
    for pt, lab, off in [(A, "$A$", (-4.5, -4.5)), (C, "$C$", (0.5, -6.0)),
                         (Bf, "$B$", (3.5, -5.5)), (T, "$T$", (0.5, 5.5))]:
        ax.scatter([pt[0]], [pt[1]], s=46, color=INK, zorder=8)
        ax.annotate(lab, (pt[0] + off[0], pt[1] + off[1]), fontsize=13)
    clean(ax, (-16, 132), (-26, 76))
    ax.set_title(r"$47^{\circ}$ is not an angle of triangle $ATC$",
                 fontsize=11.5, pad=8)


we_fig("sl-3-3-we5.svg", _w5, (6.4, 3.9))

print("wrote sl-3-3-we1..we5.svg")
