"""SL 3.4 の図を作る。ラベルはすべて英語。
   出力先: 03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/make_sl_3_4.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Wedge, Polygon, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, FILL = "#7a8592", "#eaf2fb"
GOLD = "#b9770e"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.88)


def clean(ax, xlim=None, ylim=None):
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def P(deg, r=1.0, c=(0.0, 0.0)):
    """中心 c、半径 r、角度 deg（度・反時計回り）の点"""
    t = np.radians(deg)
    return np.array([c[0] + r * np.cos(t), c[1] + r * np.sin(t)])


def circle(ax, c=(0, 0), r=1.0, color=LINE, lw=1.8, ls="-"):
    ax.add_patch(Circle(c, r, fill=False, edgecolor=color,
                        linewidth=lw, linestyle=ls, zorder=4))


def wedge(ax, c, r, a1, a2, fc=FILL, ec="none", alpha=1.0, z=2):
    ax.add_patch(Wedge(c, r, a1, a2, facecolor=fc, edgecolor=ec,
                       alpha=alpha, zorder=z))


def arcline(ax, c, r, a1, a2, color=ACC, lw=3.4, z=6):
    ax.add_patch(Arc(c, 2 * r, 2 * r, theta1=a1, theta2=a2,
                     color=color, linewidth=lw, zorder=z))


def dot(ax, p, color=INK, s=26, z=8):
    ax.plot([p[0]], [p[1]], "o", color=color, markersize=np.sqrt(s),
            zorder=z, clip_on=False)


# ══════════════════ 1. 円の各部の名前 ══════════════════
fig, axes = plt.subplots(1, 3, figsize=(11.6, 4.3))

# --- (1) centre / radius / diameter / chord / tangent -------------
ax = axes[0]
O = np.array([0.0, 0.0]); R = 1.0
circle(ax, O, R)

# diameter（水平）
ax.plot([-R, R], [0, 0], color=LINE, lw=2.0, zorder=5)
ax.text(0.52, -0.05, "diameter $2r$", color=LINE, ha="center", va="top",
        fontsize=10.5, bbox=BOX, zorder=9)

# radius
A = P(62, R)
ax.plot([O[0], A[0]], [O[1], A[1]], color=GREEN, lw=2.6, zorder=6)
ax.text(0.42, 0.56, "radius $r$", color=GREEN, ha="left", va="center",
        fontsize=10.5, bbox=BOX, zorder=9)

dot(ax, O)
ax.text(-0.04, -0.06, "O", ha="right", va="top", fontsize=11, zorder=9)

# chord
C1, C2 = P(250, R), P(310, R)
ax.plot([C1[0], C2[0]], [C1[1], C2[1]], color=GOLD, lw=2.2, zorder=5)
ax.text(0.14, -0.80, "chord", color=GOLD, ha="center", va="bottom",
        fontsize=10.5, bbox=BOX, zorder=9)

# tangent
T = P(146, R)
d = np.array([-np.sin(np.radians(146)), np.cos(np.radians(146))])
ax.plot([T[0] - 0.58 * d[0], T[0] + 0.58 * d[0]],
        [T[1] - 0.58 * d[1], T[1] + 0.58 * d[1]],
        color=GREY, lw=1.8, zorder=5)
ax.text(-1.02, 0.94, "tangent", color=GREY, ha="center", va="bottom",
        fontsize=10.5, bbox=BOX, zorder=9)

ax.text(0, -1.42, "circumference $= 2\\pi r$,   area $= \\pi r^{2}$",
        ha="center", va="center", fontsize=10.5, color=INK)
clean(ax, (-1.45, 1.45), (-1.75, 1.45))

# --- (2) arc / sector --------------------------------------------
ax = axes[1]
th = 72.0
wedge(ax, O, R, 24, 24 + th, fc=FILL)
circle(ax, O, R)
S1, S2 = P(24, R), P(24 + th, R)
ax.plot([O[0], S1[0]], [O[1], S1[1]], color=LINE, lw=1.8, zorder=6)
ax.plot([O[0], S2[0]], [O[1], S2[1]], color=LINE, lw=1.8, zorder=6)
arcline(ax, O, R, 24, 24 + th)
dot(ax, O)
ax.add_patch(Arc(O, 0.40, 0.40, theta1=24, theta2=24 + th,
                 color=ACC, lw=1.5, zorder=7))
ax.text(*P(60, 0.31), r"$\theta$", color=ACC, ha="center", va="center",
        fontsize=12, zorder=9)
ax.annotate("arc  (length $l$)", xy=P(60, R * 1.02), xytext=(0.10, 1.30),
            color=ACC, fontsize=10.5, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.4), zorder=9)
ax.text(*P(60, 0.68), "sector", color=LINE, ha="center", va="center",
        fontsize=11, zorder=9, bbox=BOX)
ax.text(0, -1.42, "sector = two radii + the arc between them",
        ha="center", va="center", fontsize=10.5, color=INK)
clean(ax, (-1.45, 1.45), (-1.75, 1.45))

# --- (3) segment -------------------------------------------------
ax = axes[2]
a1, a2 = 200.0, 340.0
poly = [P(a, R) for a in np.linspace(a1, a2, 90)]
ax.add_patch(Polygon(poly, closed=True, facecolor="#fdecea",
                     edgecolor="none", zorder=2))
circle(ax, O, R)
B1, B2 = P(a1, R), P(a2, R)
ax.plot([B1[0], B2[0]], [B1[1], B2[1]], color=GOLD, lw=2.2, zorder=6)
arcline(ax, O, R, a1, a2, color=ACC, lw=3.0)
dot(ax, O)
ax.text(0, -0.72, "segment", color=ACC, ha="center", va="center",
        fontsize=11, zorder=9, bbox=BOX)
ax.text(0, -0.26, "chord", color=GOLD, ha="center", va="bottom",
        fontsize=10.5, zorder=9, bbox=BOX)
ax.text(0, -1.42, "segment = the part cut off by a chord",
        ha="center", va="center", fontsize=10.5, color=INK)
clean(ax, (-1.45, 1.45), (-1.75, 1.45))

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-4-parts.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════════ 2. θ/360 は「円全体のうちどれだけか」 ══════════════════
fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.2))
cases = [(90.0, r"$90^{\circ}$", r"$\frac{90}{360}=\frac{1}{4}$"),
         (120.0, r"$120^{\circ}$", r"$\frac{120}{360}=\frac{1}{3}$"),
         (45.0, r"$45^{\circ}$", r"$\frac{45}{360}=\frac{1}{8}$")]

for ax, (th, lab, frac) in zip(axes, cases):
    wedge(ax, O, R, 0, th, fc=FILL)
    circle(ax, O, R)
    for a in (0.0, th):
        p = P(a, R)
        ax.plot([O[0], p[0]], [O[1], p[1]], color=LINE, lw=1.8, zorder=6)
    arcline(ax, O, R, 0, th)
    dot(ax, O)
    ax.add_patch(Arc(O, 0.42, 0.42, theta1=0, theta2=th,
                     color=ACC, lw=1.5, zorder=7))
    ax.text(*P(th / 2, 0.62), lab, color=ACC,
            ha="center", va="center", fontsize=11.5, zorder=9, bbox=BOX)
    ax.text(0, -1.38, frac, ha="center", va="center", fontsize=15, color=INK)
    clean(ax, (-1.35, 1.35), (-1.85, 1.35))

fig.suptitle(r"the sector is this fraction of the whole circle",
             y=0.99, fontsize=11.5, color=INK)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-4-fraction.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════════ 3. perimeter of a sector ══════════════════
fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6))
th = 100.0

# --- correct ---
ax = axes[0]
wedge(ax, O, R, 20, 20 + th, fc=FILL)
circle(ax, O, R, color=GRID, lw=1.4, ls="--")
S1, S2 = P(20, R), P(20 + th, R)
ax.plot([O[0], S1[0]], [O[1], S1[1]], color=GREEN, lw=3.2, zorder=6)
ax.plot([O[0], S2[0]], [O[1], S2[1]], color=GREEN, lw=3.2, zorder=6)
arcline(ax, O, R, 20, 20 + th)
dot(ax, O)
ax.text(*(O + S1) / 2 + np.array([0.10, -0.10]), "$r$", color=GREEN,
        fontsize=12, ha="left", va="top", zorder=9, bbox=BOX)
ax.text(*(O + S2) / 2 + np.array([-0.12, -0.06]), "$r$", color=GREEN,
        fontsize=12, ha="right", va="top", zorder=9, bbox=BOX)
ax.annotate("$l$", xy=P(70, R), xytext=(0.34, 1.42), color=ACC, fontsize=13,
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.4), zorder=9)
ax.text(0, -1.42, r"perimeter $= l + 2r$   $\checkmark$",
        ha="center", va="center", fontsize=12.5, color=GREEN)
clean(ax, (-1.45, 1.45), (-1.75, 1.80))

# --- wrong ---
ax = axes[1]
circle(ax, O, R, color=GRID, lw=1.4, ls="--")
S1, S2 = P(20, R), P(20 + th, R)
ax.plot([O[0], S1[0]], [O[1], S1[1]], color=GRID, lw=1.6, zorder=5)
ax.plot([O[0], S2[0]], [O[1], S2[1]], color=GRID, lw=1.6, zorder=5)
arcline(ax, O, R, 20, 20 + th)
dot(ax, O, color=GREY)
ax.text(0, -1.42, r"perimeter $= l$   $\times$",
        ha="center", va="center", fontsize=12.5, color=ACC)
ax.text(0, -0.58, "the two radii\nare forgotten", color=ACC, fontsize=10.5,
        ha="center", va="center", zorder=9, bbox=BOX)
clean(ax, (-1.45, 1.45), (-1.75, 1.80))

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-4-perimeter.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════════ 4. segment = sector − triangle ══════════════════
fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.3))
a1, a2 = 205.0, 335.0

def base(ax, shade):
    circle(ax, O, R, color=GRID, lw=1.4)
    B1, B2 = P(a1, R), P(a2, R)
    if shade == "sector":
        wedge(ax, O, R, a1, a2, fc=FILL)
    elif shade == "triangle":
        ax.add_patch(Polygon([O, B1, B2], closed=True,
                             facecolor="#eafaef", edgecolor="none", zorder=2))
    elif shade == "segment":
        poly = [P(a, R) for a in np.linspace(a1, a2, 90)]
        ax.add_patch(Polygon(poly, closed=True, facecolor="#fdecea",
                             edgecolor="none", zorder=2))
    for p in (B1, B2):
        ax.plot([O[0], p[0]], [O[1], p[1]], color=LINE, lw=1.7, zorder=6)
    ax.plot([B1[0], B2[0]], [B1[1], B2[1]], color=GOLD, lw=2.0, zorder=6)
    arcline(ax, O, R, a1, a2, color=ACC, lw=2.8)
    dot(ax, O)
    ax.add_patch(Arc(O, 0.40, 0.40, theta1=a1, theta2=a2,
                     color=ACC, lw=1.4, zorder=7))
    ax.text(*P(270, 0.34), r"$\theta$", color=ACC, ha="center", va="center",
            fontsize=11, zorder=9)
    clean(ax, (-1.30, 1.30), (-1.75, 1.35))

base(axes[0], "sector")
axes[0].text(0, -1.48, "sector", ha="center", va="center", fontsize=12,
             color=LINE)
axes[0].text(0, 1.16, r"$\dfrac{\theta}{360}\times\pi r^{2}$", ha="center",
             va="center", fontsize=13, color=INK)

base(axes[1], "triangle")
axes[1].text(0, -1.48, "$-$   triangle", ha="center", va="center",
             fontsize=12, color=GREEN)
axes[1].text(0, 1.16, r"$\dfrac{1}{2}r^{2}\sin\theta$", ha="center",
             va="center", fontsize=13, color=INK)

base(axes[2], "segment")
axes[2].text(0, -1.48, "$=$   segment", ha="center", va="center",
             fontsize=12, color=ACC)
axes[2].text(0, 1.16, "the answer", ha="center", va="center",
             fontsize=12, color=INK)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-4-segment.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════════ 5. windscreen wiper（扇形の差） ══════════════════
fig, ax = plt.subplots(figsize=(7.4, 5.0))
Rin, Rout = 11.0, 45.0
b1, b2 = 33.0, 148.0            # 115°

# 掃いた部分（外の扇形 − 内の扇形）
ax.add_patch(Wedge(O, Rout, b1, b2, width=Rout - Rin,
                   facecolor=FILL, edgecolor="none", zorder=2))
for r_, col in ((Rin, GREY), (Rout, ACC)):
    ax.add_patch(Arc(O, 2 * r_, 2 * r_, theta1=b1, theta2=b2,
                     color=col, lw=2.4, zorder=6))
for a in (b1, b2):
    p1, p2 = P(a, Rin), P(a, Rout)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=LINE, lw=1.8, zorder=6)

# ピボットから内側の弧までの点線（ここが 11 cm）
for a in (b1, b2):
    p = P(a, Rin)
    ax.plot([0, p[0]], [0, p[1]], color=GREY, lw=1.5, ls="--", zorder=5)
dot(ax, O)
ax.text(0, -2.4, "pivot", ha="center", va="top", fontsize=10.5, color=INK)

# 115°：ピボットのところで取る
ax.add_patch(Arc(O, 14, 14, theta1=b1, theta2=b2, color=ACC, lw=1.5, zorder=7))
ax.text(*P((b1 + b2) / 2, 4.0), r"$115^\circ$", color=ACC, ha="center",
        va="center", fontsize=11, zorder=9, bbox=BOX)

# 半径のラベル
ax.annotate("11 cm", xy=P(b1, Rin * 0.80), xytext=(28.0, 1.5), color=GREY,
            fontsize=11, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3), zorder=9)
q = P(126.0, Rout)
ax.annotate("45 cm", xy=(q[0], q[1]), xytext=(-44.0, 46.0), color=ACC,
            fontsize=11, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.3), zorder=9)

ax.text(*P(90.5, 28.0), "the part\nthat is wiped", color=LINE, fontsize=11,
        ha="center", va="center", zorder=9, bbox=BOX)

clean(ax, (-56, 60), (-9, 58))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-4-wiper.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════════ 自己チェック ══════════════════
from math import pi, sin, radians
f = lambda t: t / 360
print("E1  r=12 t=65 : l =", f(65) * 2 * pi * 12, " A =", f(65) * pi * 144,
      " P =", f(65) * 2 * pi * 12 + 24)
print("E4  segment r=10 t=80 :",
      f(80) * pi * 100 - 0.5 * 100 * sin(radians(80)))
print("E5  wiper :", f(115) * pi * (45 ** 2 - 11 ** 2))
print("figures written to", os.path.normpath(OUT))
