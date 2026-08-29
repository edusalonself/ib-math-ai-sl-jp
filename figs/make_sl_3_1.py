"""SL 3.1 の図を作る。ラベルはすべて英語。
   出力先: 03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/make_sl_3_1.py

   立体は「斜投影」で描く。 x -> (1, 0)、 y(奥行き) -> (0.46, 0.34)、 z -> (0, 1)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, FILL = "#7a8592", "#eaf2fb"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.4, alpha=0.85)

EX, EY, EZ = np.array([1.0, 0.0]), np.array([0.46, 0.34]), np.array([0.0, 1.0])


def P(x, y, z):
    """3次元の点を、紙の上の (X, Y) に変換する。"""
    v = x * EX + y * EY + z * EZ
    return float(v[0]), float(v[1])


def seg(ax, a, b, color=INK, lw=1.6, ls="-", z=4):
    (x0, y0), (x1, y1) = P(*a), P(*b)
    ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, linestyle=ls, zorder=z)


def right_angle(ax, corner, d1, d2, size=0.34, color=GREY):
    """corner から d1, d2 方向に小さな直角記号を描く。"""
    c = np.array(P(*corner))
    u = np.array(P(*(np.array(corner) + np.array(d1)))) - c
    v = np.array(P(*(np.array(corner) + np.array(d2)))) - c
    u = u / np.linalg.norm(u) * size
    v = v / np.linalg.norm(v) * size
    pts = np.array([c + u, c + u + v, c + v])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=1.1, zorder=6)


def clean(ax):
    ax.set_aspect("equal")
    ax.axis("off")


# ================= 1. 3次元の座標と距離 =================
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))

# --- 左：座標軸と点 ---
ax = axes[0]
seg(ax, (0, 0, 0), (5.4, 0, 0), color=GREY, lw=1.4)
seg(ax, (0, 0, 0), (0, 4.6, 0), color=GREY, lw=1.4)
seg(ax, (0, 0, 0), (0, 0, 4.6), color=GREY, lw=1.4)
for (pt, lab) in [((5.7, 0, 0), "$x$"), ((0, 4.9, 0), "$y$"), ((0, 0, 4.9), "$z$")]:
    ax.annotate(lab, P(*pt), fontsize=13, color=GREY, ha="center", va="center")

A = (4, 3, 3)
for a, b in [((0, 0, 0), (4, 0, 0)), ((4, 0, 0), (4, 3, 0)),
             ((0, 0, 0), (0, 3, 0)), ((0, 3, 0), (4, 3, 0))]:
    seg(ax, a, b, color=LINE, lw=1.3, ls=":")
seg(ax, (4, 3, 0), A, color=LINE, lw=1.3, ls=":")
ax.scatter(*P(*A), s=70, color=ACC, edgecolor=INK, linewidth=0.9, zorder=8)
ax.annotate("$A(4,\\ 3,\\ 3)$", P(*A), textcoords="offset points", xytext=(10, 6),
            fontsize=12, color=ACC, zorder=9)
ax.annotate("go 4 along $x$,\nthen 3 along $y$,\nthen 3 up $z$",
            (0.35, 4.15), fontsize=10, color=LINE, ha="left", zorder=9)
ax.set_xlim(-1.3, 8.0); ax.set_ylim(-1.5, 5.2)
clean(ax)
ax.set_title("A point in three dimensions", fontsize=12, pad=8)

# --- 右：距離は Pythagoras を2回 ---
ax = axes[1]
B = (5, 3.4, 2.8)
for a, b in [((0, 0, 0), (5, 0, 0)), ((5, 0, 0), (5, 3.4, 0)),
             ((0, 0, 0), (0, 3.4, 0)), ((0, 3.4, 0), (5, 3.4, 0)),
             ((5, 3.4, 0), B), ((0, 0, 0), (0, 0, 2.8)),
             ((0, 0, 2.8), (5, 0, 2.8)), ((5, 0, 2.8), B),
             ((0, 0, 2.8), (0, 3.4, 2.8)), ((0, 3.4, 2.8), B)]:
    seg(ax, a, b, color=GREY, lw=1.1, ls=":")
seg(ax, (0, 0, 0), (5, 3.4, 0), color=GREEN, lw=2.4)
seg(ax, (0, 0, 0), B, color=ACC, lw=2.6)
seg(ax, (5, 3.4, 0), B, color=LINE, lw=2.2)

right_angle(ax, (5, 3.4, 0), (-1, 0, 0), (0, 0, 1))
ax.annotate("first Pythagoras\n(on the base)", P(2.5, 1.7, 0),
            textcoords="offset points", xytext=(-2, -30), fontsize=10,
            color=GREEN, ha="center", bbox=BOX, zorder=9)
ax.annotate("second\nPythagoras", P(2.5, 1.7, 1.5), textcoords="offset points",
            xytext=(-30, 12), fontsize=10, color=ACC, ha="center",
            bbox=BOX, zorder=9)
ax.scatter(*P(0, 0, 0), s=56, color=INK, zorder=8)
ax.scatter(*P(*B), s=56, color=INK, zorder=8)
ax.set_xlim(-0.9, 8.0); ax.set_ylim(-1.5, 5.2)
clean(ax)
ax.set_title("The 3D distance is Pythagoras twice", fontsize=12, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-1-space.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ================= 2. 立体と、どの文字がどれか =================
fig, axes = plt.subplots(1, 3, figsize=(11.6, 4.2))


def ellipse(ax, cx, cy, rx, ry, color=INK, lw=1.6, ls="-", z=4, top=True,
            bottom=True):
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(cx + rx * np.cos(t), cy + ry * np.sin(t), color=color,
            linewidth=lw, linestyle=ls, zorder=z)


# --- cone ---
ax = axes[0]
r, hh = 1.6, 3.2
ellipse(ax, 0, 0, r, 0.45, color=LINE)
ax.plot([-r, 0, r], [0, hh, 0], color=LINE, linewidth=1.8, zorder=5)
ax.plot([0, 0], [0, hh], color=GREY, linestyle="--", linewidth=1.3, zorder=4)
ax.plot([0, r], [0, 0], color=GREEN, linewidth=2.2, zorder=6)
ax.plot([0, r], [hh, 0], color=ACC, linewidth=2.2, zorder=6)
ax.plot([0.001, 0.28, 0.28], [0.28, 0.28, 0.001], color=GREY, linewidth=1.0,
        zorder=6)
ax.annotate("$r$", (r / 2, -0.34), color=GREEN, fontsize=13, ha="center")
ax.annotate("$h$", (-0.26, hh / 2), color=GREY, fontsize=13, ha="center")
ax.annotate("$l$", (r / 2 + 0.24, hh / 2 + 0.08), color=ACC, fontsize=13)
ax.annotate("slant height", (r / 2 + 0.5, hh / 2 - 0.42), color=ACC, fontsize=9.5)
ax.set_xlim(-2.6, 3.2); ax.set_ylim(-2.0, 4.2)
clean(ax)
ax.set_title("Cone:  $l = \\sqrt{r^{2} + h^{2}}$", fontsize=11.5, pad=8)

# --- sphere / hemisphere ---
ax = axes[1]
t = np.linspace(0, 2 * np.pi, 200)
ax.plot(-1.55 + 1.15 * np.cos(t), 1.6 + 1.15 * np.sin(t), color=LINE,
        linewidth=1.8, zorder=5)
ellipse(ax, -1.55, 1.6, 1.15, 0.36, color=GREY, lw=1.1, ls="--", z=4)
ax.plot([-1.55, -0.40], [1.6, 1.6], color=GREEN, linewidth=2.2, zorder=6)
ax.annotate("$r$", (-0.95, 1.76), color=GREEN, fontsize=13)
ax.annotate("sphere", (-1.55, -0.05), fontsize=10.5, ha="center", color=LINE)

th = np.linspace(0, np.pi, 200)
ax.plot(1.75 + 1.15 * np.cos(th), 0.9 + 1.15 * np.sin(th), color=GREEN,
        linewidth=1.8, zorder=5)
ellipse(ax, 1.75, 0.9, 1.15, 0.34, color=GREEN, lw=1.6, z=5)
ax.plot([1.75, 2.90], [0.9, 0.9], color=ACC, linewidth=2.2, zorder=6)
ax.annotate("$r$", (2.30, 1.06), color=ACC, fontsize=13)
ax.annotate("hemisphere", (1.75, -0.05), fontsize=10.5, ha="center", color=GREEN)
ax.annotate("the flat circle\ncounts too", (1.75, -0.95), fontsize=9.5,
            ha="center", color=ACC)
ax.set_xlim(-3.1, 3.6); ax.set_ylim(-2.0, 4.2)
clean(ax)
ax.set_title("Sphere and hemisphere", fontsize=11.5, pad=8)

# --- right pyramid ---
ax = axes[2]
b = 1.5
base = [(-b, -b, 0), (b, -b, 0), (b, b, 0), (-b, b, 0)]
apex = (0, 0, 3.2)
for i in range(4):
    seg(ax, base[i], base[(i + 1) % 4], color=LINE, lw=1.6)
for v in base:
    seg(ax, v, apex, color=LINE, lw=1.6)
seg(ax, (0, 0, 0), apex, color=GREY, lw=1.3, ls="--")
seg(ax, (0, -b, 0), apex, color=ACC, lw=2.2, z=6)
seg(ax, (0, 0, 0), (0, -b, 0), color=GREEN, lw=2.2, z=6)
right_angle(ax, (0, 0, 0), (0, -1, 0), (0, 0, 1))
ax.annotate("$h$", P(0, 0, 2.3), textcoords="offset points", xytext=(6, 0),
            color=GREY, fontsize=13, bbox=BOX, zorder=9)
ax.annotate("slant height", P(0, -b, 1.05), textcoords="offset points",
            xytext=(-10, -4), color=ACC, fontsize=10, ha="right",
            bbox=BOX, zorder=9)
ax.annotate("base area $A$", P(0, 0, 0), textcoords="offset points",
            xytext=(0, -34), color=LINE, fontsize=10.5, ha="center",
            bbox=BOX, zorder=9)
ax.set_xlim(-2.6, 3.1); ax.set_ylim(-2.0, 4.2)
clean(ax)
ax.set_title("Right pyramid:  $V = \\dfrac{1}{3}Ah$", fontsize=11.5, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-1-solids.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 3. 直方体の中の角度 =================
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))

L, W, Hh = 4.0, 2.6, 2.4
V = {"A": (0, 0, 0), "B": (L, 0, 0), "C": (L, W, 0), "D": (0, W, 0),
     "E": (0, 0, Hh), "F": (L, 0, Hh), "G": (L, W, Hh), "H": (0, W, Hh)}

ax = axes[0]
for a, b in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
             ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"),
             ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H")]:
    seg(ax, V[a], V[b], color=GREY, lw=1.4)
seg(ax, V["A"], V["C"], color=GREEN, lw=2.4, z=6)
seg(ax, V["A"], V["G"], color=ACC, lw=2.6, z=6)
seg(ax, V["C"], V["G"], color=LINE, lw=2.2, z=6)
right_angle(ax, V["C"], (-1, 0, 0), (0, 0, 1))

for k in ("A", "C", "G"):
    ax.scatter(*P(*V[k]), s=48, color=INK, zorder=8)
for k, dx, dy in [("A", -14, -10), ("C", 10, -10), ("G", 10, 6)]:
    ax.annotate(k, P(*V[k]), textcoords="offset points", xytext=(dx, dy),
                fontsize=12, color=INK)
ax.annotate("base diagonal", P(2.0, 1.3, 0), textcoords="offset points",
            xytext=(0, -26), color=GREEN, fontsize=10, ha="center", bbox=BOX,
            zorder=9)
ax.annotate("space diagonal", P(2.0, 1.3, 1.2), textcoords="offset points",
            xytext=(-34, 16), color=ACC, fontsize=10, ha="center", bbox=BOX,
            zorder=9)
ax.annotate(r"$\theta$", P(0.75, 0.5, 0.12), fontsize=13, color=ACC, zorder=9)
clean(ax)
ax.set_title("The angle between $AG$ and the base", fontsize=12, pad=8)

# --- 右：取り出した直角三角形 ---
ax = axes[1]
ax.plot([0, 4.2, 4.2, 0], [0, 0, 2.4, 0], color=INK, linewidth=1.8, zorder=5)
ax.plot([0, 4.2], [0, 0], color=GREEN, linewidth=2.6, zorder=6)
ax.plot([4.2, 4.2], [0, 2.4], color=LINE, linewidth=2.4, zorder=6)
ax.plot([0, 4.2], [0, 2.4], color=ACC, linewidth=2.6, zorder=6)
ax.plot([3.9, 3.9, 4.2], [0, 0.3, 0.3], color=GREY, linewidth=1.1, zorder=6)
ax.annotate("$AC$  (base diagonal)", (2.1, -0.34), color=GREEN, fontsize=11,
            ha="center")
ax.annotate("$CG$\n(height)", (4.42, 1.2), color=LINE, fontsize=11, va="center")
ax.annotate("$AG$", (1.9, 1.34), color=ACC, fontsize=11)
ax.annotate(r"$\theta$", (0.52, 0.12), fontsize=13, color=ACC)
ax.annotate("$A$", (-0.22, -0.05), fontsize=12)
ax.annotate("$C$", (4.24, -0.34), fontsize=12)
ax.annotate("$G$", (4.24, 2.42), fontsize=12)
ax.annotate(r"$\tan\theta = \dfrac{CG}{AC}$", (1.5, 2.0), fontsize=13, color=ACC)
ax.set_xlim(-0.9, 6.4); ax.set_ylim(-1.0, 3.3)
clean(ax)
ax.set_title("Redraw it flat, then use right-angled trigonometry",
             fontsize=12, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-1-angle.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-3-1-space.svg, sl-3-1-solids.svg, sl-3-1-angle.svg")
print("check cone 5-12-13:", (5 ** 2 + 12 ** 2) ** 0.5)
print("check cuboid 8-6-5: base", (8 ** 2 + 6 ** 2) ** 0.5,
      " space", (8 ** 2 + 6 ** 2 + 5 ** 2) ** 0.5)
