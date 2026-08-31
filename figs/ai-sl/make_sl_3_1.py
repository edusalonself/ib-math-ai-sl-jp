"""SL 3.1 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_3_1.py

   立体は「斜投影」で描く。 x -> (1, 0)、 y(奥行き) -> (0.46, 0.34)、 z -> (0, 1)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl",
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


# ================= 4. 円錐の slant height（見出しの下に置く図） =================
def ell(ax, cx, cy, rx, ry, color=INK, lw=1.6, ls="-", z=4, part="full"):
    """part: full / front(手前=下半分) / back(奥=上半分)"""
    if part == "full":
        t = np.linspace(0, 2 * np.pi, 300)
    elif part == "front":
        t = np.linspace(np.pi, 2 * np.pi, 200)
    else:
        t = np.linspace(0, np.pi, 200)
    ax.plot(cx + rx * np.cos(t), cy + ry * np.sin(t), color=color,
            linewidth=lw, linestyle=ls, zorder=z)


fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

# --- 左：円錐の中の r, h, l ---
ax = axes[0]
r, hh, ry = 1.8, 3.4, 0.50
ell(ax, 0, 0, r, ry, color=GREY, lw=1.3, ls="--", z=3, part="back")
ell(ax, 0, 0, r, ry, color=LINE, lw=1.8, z=5, part="front")
ax.plot([-r, 0, r], [0, hh, 0], color=LINE, linewidth=1.9, zorder=5)
ax.plot([0, 0], [0, hh], color=GREY, linestyle="--", linewidth=1.5, zorder=6)
ax.plot([0, r], [0, 0], color=GREEN, linewidth=2.6, zorder=7)
ax.plot([0, r], [hh, 0], color=ACC, linewidth=2.8, zorder=7)
ax.plot([0.001, 0.30, 0.30], [0.30, 0.30, 0.001], color=GREY, linewidth=1.1,
        zorder=8)
ax.annotate("$r$", (r / 2, -0.40), color=GREEN, fontsize=14, ha="center")
ax.annotate("$h$", (-0.30, hh / 2), color=GREY, fontsize=14, ha="right")
ax.annotate("$l$", (r / 2 + 0.26, hh / 2 + 0.10), color=ACC, fontsize=14)
ax.annotate("slant height\n(apex to the rim)", (r + 0.75, hh / 2 - 0.30),
            color=ACC, fontsize=10, ha="left", va="center")
ax.annotate(r"$A = \pi r l$   uses $l$,  never $h$", (0, -1.55), color=ACC,
            fontsize=12, ha="center")
ax.set_xlim(-4.0, 4.6); ax.set_ylim(-2.3, 4.4)
clean(ax)
ax.set_title("The three lengths in a cone", fontsize=12, pad=8)

# --- 右：取り出した直角三角形（5, 12, 13） ---
ax = axes[1]
ax.plot([0, 3.0], [0, 0], color=GREEN, linewidth=2.8, zorder=6)
ax.plot([0, 0], [0, 3.6], color=GREY, linewidth=2.4, zorder=6)
ax.plot([0, 3.0], [3.6, 0], color=ACC, linewidth=2.8, zorder=6)
ax.plot([0.001, 0.28, 0.28], [0.28, 0.28, 0.001], color=GREY, linewidth=1.1,
        zorder=7)
ax.annotate("$r = 5$", (1.5, -0.36), color=GREEN, fontsize=13, ha="center")
ax.annotate("$h = 12$", (-0.22, 1.8), color=GREY, fontsize=13, ha="right",
            va="center")
ax.annotate("$l = 13$", (1.85, 2.05), color=ACC, fontsize=13)
ax.annotate(r"$l = \sqrt{r^{2} + h^{2}} = \sqrt{5^{2} + 12^{2}}"
            r" = \sqrt{169} = 13$", (1.5, -1.35), fontsize=12.5, ha="center",
            color=INK)
ax.set_xlim(-2.8, 5.8); ax.set_ylim(-2.3, 4.4)
clean(ax)
ax.set_title("Pull the triangle out flat, then use Pythagoras",
             fontsize=12, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-1-slant.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)


# ================= 5. hemisphere（見出しの下に置く図） =================
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))
R, RY = 1.35, 0.42


def dome(ax, cx, cy, face=None, edge=GREEN, lw=1.9, z=5, rim=None,
         rim_ls="-", rim_lw=1.7):
    """flat side down のドーム。silhouette は上の弧＋手前の弧。"""
    t1 = np.linspace(0, np.pi, 220)
    t2 = np.linspace(np.pi, 2 * np.pi, 220)
    xs = np.concatenate([cx + R * np.cos(t1), cx + R * np.cos(t2)])
    ys = np.concatenate([cy + R * np.sin(t1), cy + RY * np.sin(t2)])
    if face:
        ax.fill(xs, ys, color=face, zorder=2, linewidth=0)
    ax.plot(cx + R * np.cos(t1), cy + R * np.sin(t1), color=edge,
            linewidth=lw, zorder=z)
    ax.plot(cx + R * np.cos(t2), cy + RY * np.sin(t2), color=edge,
            linewidth=lw, zorder=z)
    if rim:
        ell(ax, cx, cy, R, RY, color=rim, lw=rim_lw, ls=rim_ls, z=z + 1,
            part="back")


# --- 左：体積は半分でよい ---
ax = axes[0]
t = np.linspace(0, 2 * np.pi, 300)
ax.plot(-2.3 + R * np.cos(t), 1.6 + R * np.sin(t), color=LINE, linewidth=1.8,
        zorder=5)
ell(ax, -2.3, 1.6, R, RY, color=GREY, lw=1.2, ls="--", z=4)
ax.annotate("sphere", (-2.3, -0.55), fontsize=10.5, ha="center", color=LINE)
ax.annotate(r"$\dfrac{4}{3}\pi r^{3}$", (-2.3, 3.55), fontsize=14,
            ha="center", color=LINE)

ax.annotate("", xy=(0.55, 1.6), xytext=(-0.45, 1.6),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
ax.annotate(r"$\times \dfrac{1}{2}$", (0.05, 1.85), fontsize=13, ha="center",
            color=INK)

dome(ax, 2.6, 1.0, face=FILL)
ell(ax, 2.6, 1.0, R, RY, color=GREY, lw=1.2, ls="--", z=6, part="back")
ax.annotate("hemisphere", (2.6, -0.55), fontsize=10.5, ha="center", color=GREEN)
ax.annotate(r"$\dfrac{2}{3}\pi r^{3}$", (2.6, 3.55), fontsize=14, ha="center",
            color=GREEN)
ax.set_xlim(-4.6, 4.9); ax.set_ylim(-1.6, 4.8)
clean(ax)
ax.set_title("Volume:  halving the sphere is correct", fontsize=12, pad=8,
             color=GREEN)

# --- 右：表面積は半分では足りない（曲面 ＋ 切り口の円） ---
ax = axes[1]
dome(ax, -2.3, 1.0, face="#cfe4f7")
ell(ax, -2.3, 1.0, R, RY, color=GREY, lw=1.2, ls="--", z=6, part="back")
ax.annotate("curved surface", (-2.3, -0.55), fontsize=10.5, ha="center",
            color=LINE)
ax.annotate(r"$2\pi r^{2}$", (-2.3, 3.55), fontsize=14, ha="center",
            color=LINE)

ax.annotate("$+$", (0.05, 1.35), fontsize=17, ha="center", color=INK)

th = np.linspace(0, 2 * np.pi, 300)
ax.fill(2.6 + R * np.cos(th), 1.2 + RY * np.sin(th), color="#f6d3cd", zorder=3)
ell(ax, 2.6, 1.2, R, RY, color=ACC, lw=2.2, z=5)
ax.annotate("the flat circle", (2.6, -0.55), fontsize=10.5, ha="center",
            color=ACC)
ax.annotate(r"$\pi r^{2}$", (2.6, 3.55), fontsize=14, ha="center", color=ACC)

ax.annotate(r"$\mathrm{total} = 2\pi r^{2} + \pi r^{2} = 3\pi r^{2}$", (0.15, -1.25),
            fontsize=13, ha="center", color=ACC)
ax.set_xlim(-4.6, 4.9); ax.set_ylim(-1.6, 4.8)
clean(ax)
ax.set_title("Surface area:  half is NOT enough", fontsize=12, pad=8, color=ACC)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-1-hemisphere.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)


# ================= 6. 組み合わせた立体（円柱＋半球） =================
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8))
cr, ch, cry = 1.3, 3.1, 0.40


def cyl_hemi(ax, cx=0.0, base=0.0):
    """底面 base、半径 cr、高さ ch の円柱の上に半径 cr の半球。"""
    top = base + ch
    ell(ax, cx, base, cr, cry, color=GREY, lw=1.2, ls="--", z=3, part="back")
    ell(ax, cx, base, cr, cry, color=LINE, lw=1.8, z=5, part="front")
    ax.plot([cx - cr, cx - cr], [base, top], color=LINE, linewidth=1.8, zorder=5)
    ax.plot([cx + cr, cx + cr], [base, top], color=LINE, linewidth=1.8, zorder=5)
    th = np.linspace(0, np.pi, 220)
    ax.plot(cx + cr * np.cos(th), top + cr * np.sin(th), color=GREEN,
            linewidth=1.9, zorder=5)
    return top


# --- 左：どこがどの立体か ---
ax = axes[0]
top = cyl_hemi(ax)
ell(ax, 0, top, cr, cry, color=GREY, lw=1.3, ls="--", z=6)
ax.plot([0, cr], [0, 0], color=INK, linewidth=2.2, zorder=7)
ax.annotate("$r = 3$", (0.65, 0.74), color=INK, fontsize=12, ha="center",
            va="center", zorder=9)
ax.annotate("", xy=(-cr - 0.55, 0), xytext=(-cr - 0.55, top),
            arrowprops=dict(arrowstyle="<|-|>", color=GREY, lw=1.4))
ax.annotate("$h = 10$", (-cr - 0.72, top / 2), color=GREY, fontsize=12,
            ha="right", va="center")
ax.annotate("hemisphere", (cr + 0.55, top + cr * 0.55), color=GREEN,
            fontsize=11, ha="left", va="center")
ax.annotate("cylinder", (cr + 0.55, top / 2), color=LINE, fontsize=11,
            ha="left", va="center")
ax.annotate(r"$V = \pi(3)^{2}(10) + \dfrac{2}{3}\pi(3)^{3}"
            r" = 90\pi + 18\pi = 108\pi$", (0.1, -1.35), fontsize=12,
            ha="center", color=INK)
ax.set_xlim(-4.3, 4.6); ax.set_ylim(-2.1, 5.6)
clean(ax)
ax.set_title("Volume:  just add the two parts", fontsize=12, pad=8)

# --- 右：表面積で数える面・数えない面 ---
ax = axes[1]
top = cyl_hemi(ax)
ell(ax, 0, top, cr, cry, color=ACC, lw=1.5, ls="--", z=6)
# くっついた円（数えない）
ax.annotate("the join is inside:\nnot counted", (cr + 0.60, top + 0.10),
            color=ACC, fontsize=10, ha="left", va="center")
ax.annotate("", xy=(0.35, top - 0.10), xytext=(cr + 0.50, top + 0.10),
            arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.5), zorder=9)
ax.annotate(r"$2\pi r^{2} = 18\pi$", (-cr - 0.45, top + cr * 0.75),
            color=GREEN, fontsize=11.5, ha="right", va="center")
ax.annotate(r"$2\pi r h = 60\pi$", (-cr - 0.45, top / 2 + 0.2), color=LINE,
            fontsize=11.5, ha="right", va="center")
ax.annotate(r"$\pi r^{2} = 9\pi$", (-cr - 0.45, -0.55), color=LINE,
            fontsize=11.5, ha="right", va="center")
ax.annotate("", xy=(-0.35, -cry * 0.55), xytext=(-cr - 0.40, -0.50),
            arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.4), zorder=9)
ax.annotate(r"$A = 60\pi + 9\pi + 18\pi = 87\pi$", (0.1, -1.35), fontsize=12,
            ha="center", color=INK)
ax.set_xlim(-4.6, 4.3); ax.set_ylim(-2.1, 5.6)
clean(ax)
ax.set_title("Surface area:  only the faces you can see", fontsize=12, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-1-combined.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-3-1-slant.svg, sl-3-1-hemisphere.svg, sl-3-1-combined.svg")
print("combined V:", 90 + 18, "pi ;  A:", 60 + 9 + 18, "pi")
