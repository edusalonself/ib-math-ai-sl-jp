"""SL 3.2 の図を作る。ラベルはすべて英語。
   出力先: 03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/make_sl_3_2.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc

OUT = os.path.join(os.path.dirname(__file__), "..",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, FILL = "#7a8592", "#eaf2fb"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.4, alpha=0.85)


def clean(ax, xlim=None, ylim=None):
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def rt_mark(ax, corner, d1, d2, size=0.22, color=GREY):
    c = np.array(corner, dtype=float)
    u = np.array(d1, dtype=float); u = u / np.linalg.norm(u) * size
    v = np.array(d2, dtype=float); v = v / np.linalg.norm(v) * size
    pts = np.array([c + u, c + u + v, c + v])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=1.1, zorder=7)


def angle_mark(ax, vertex, p1, p2, radius=0.55, color=ACC, lw=1.5):
    v = np.array(vertex, dtype=float)
    a1 = np.degrees(np.arctan2(p1[1] - v[1], p1[0] - v[0]))
    a2 = np.degrees(np.arctan2(p2[1] - v[1], p2[0] - v[0]))
    if a2 < a1:
        a1, a2 = a2, a1
    if a2 - a1 > 180:
        a1, a2 = a2, a1 + 360
    ax.add_patch(Arc(v, 2 * radius, 2 * radius, angle=0, theta1=a1, theta2=a2,
                     color=color, linewidth=lw, zorder=6))


# ================= 1. どの道具を使うか =================
fig, ax = plt.subplots(figsize=(9.6, 5.2))

CARDS = [
    (0.50, 0.90, 0.46, 0.13, "Is there a right angle in the triangle?", INK),
    (0.20, 0.66, 0.30, 0.11, "YES", GREEN),
    (0.78, 0.66, 0.30, 0.11, "NO", LINE),
    (0.20, 0.44, 0.34, 0.15,
     "$\\sin$, $\\cos$, $\\tan$\n(SOH-CAH-TOA)\nand Pythagoras", GREEN),
    (0.78, 0.44, 0.40, 0.15,
     "Which three things do you know?", LINE),
    (0.60, 0.15, 0.30, 0.15,
     "a matching pair\n(a side and the angle\nopposite it)", ACC),
    (0.94, 0.15, 0.30, 0.15,
     "two sides and the\nangle between them,\nor all three sides", GREY),
]
for (cx, cy, w, h, text, col) in CARDS:
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.010,rounding_size=0.018",
                                facecolor="white", edgecolor=col, linewidth=1.7,
                                zorder=4))
    ax.annotate(text, (cx, cy), ha="center", va="center", fontsize=10,
                color=col, zorder=6)


def arrow(p0, p1, color=INK, lw=1.5):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", color=color,
                                 linewidth=lw, mutation_scale=14, zorder=3))


arrow((0.40, 0.855), (0.22, 0.72), color=GREEN)
arrow((0.60, 0.855), (0.76, 0.72), color=LINE)
arrow((0.20, 0.60), (0.20, 0.525), color=GREEN)
arrow((0.78, 0.60), (0.78, 0.525), color=LINE)
arrow((0.68, 0.365), (0.60, 0.235), color=ACC)
arrow((0.88, 0.365), (0.94, 0.235), color=GREY)

ax.annotate("use the\n**sine rule**".replace("**", ""), (0.60, 0.015),
            fontsize=11.5, color=ACC, ha="center", va="center",
            fontweight="bold", zorder=6)
ax.annotate("use the\ncosine rule", (0.94, 0.015), fontsize=11.5, color=GREY,
            ha="center", va="center", fontweight="bold", zorder=6)

ax.set_xlim(0.0, 1.14)
ax.set_ylim(-0.06, 1.0)
ax.set_aspect("auto")
ax.axis("off")
ax.set_title("Which tool do I use?", fontsize=13, pad=6)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-2-choose.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 2. ラベルの付け方 =================
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))

Apt, Bpt, Cpt = np.array([0.0, 0.0]), np.array([4.0, 0.0]), np.array([4.0, 3.0])

# --- 左：見る角によって opposite / adjacent が入れかわる ---
ax = axes[0]
for (p, q) in [(Apt, Bpt), (Bpt, Cpt), (Cpt, Apt)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=1.8, zorder=4)
rt_mark(ax, Bpt, (-1, 0), (0, 1))

angle_mark(ax, Apt, Bpt, Cpt, radius=0.7, color=ACC)
ax.annotate(r"$\theta$", (0.85, 0.26), fontsize=13, color=ACC, zorder=8)
ax.annotate("adjacent", (2.0, -0.36), fontsize=11, color=GREEN, ha="center")
ax.annotate("opposite", (4.22, 1.5), fontsize=11, color=ACC, va="center")
ax.annotate("hypotenuse", (1.7, 1.6), fontsize=11, color=LINE, rotation=36.87,
            ha="center", bbox=BOX, zorder=8)
ax.annotate("looked at from $C$ instead,\nopposite and adjacent swap.\nthe hypotenuse never moves.",
            (-0.9, 3.7), fontsize=9.5, color=GREY, ha="left", va="top", zorder=8)
for pt, lab, dx, dy in [(Apt, "$A$", -0.32, -0.28), (Bpt, "$B$", 0.14, -0.34),
                        (Cpt, "$C$", 0.14, 0.10)]:
    ax.annotate(lab, (pt[0] + dx, pt[1] + dy), fontsize=12)
clean(ax, (-1.0, 6.2), (-1.1, 4.3))
ax.set_title(r"Naming the sides from the angle $\theta$", fontsize=12, pad=8)

# --- 右：大文字と小文字の約束 ---
ax = axes[1]
P, Q, R = np.array([0.0, 0.0]), np.array([5.0, 0.0]), np.array([1.6, 3.2])
for (p, q) in [(P, Q), (Q, R), (R, P)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=1.8, zorder=4)
angle_mark(ax, P, Q, R, radius=0.6, color=ACC)
angle_mark(ax, Q, R, P, radius=0.6, color=GREEN)
angle_mark(ax, R, P, Q, radius=0.6, color=LINE)
ax.annotate("$A$", (0.46, 0.34), fontsize=13, color=ACC)
ax.annotate("$B$", (4.12, 0.30), fontsize=13, color=GREEN)
ax.annotate("$C$", (1.62, 2.42), fontsize=13, color=LINE)
ax.annotate("$c$", (2.5, -0.42), fontsize=13, color=LINE, ha="center")
ax.annotate("$a$", (3.55, 1.85), fontsize=13, color=ACC)
ax.annotate("$b$", (0.55, 1.72), fontsize=13, color=GREEN)
ax.annotate("side $a$ is opposite angle $A$", (2.5, 4.0), fontsize=11,
            color=INK, ha="center")
clean(ax, (-1.0, 6.2), (-1.1, 4.6))
ax.set_title("Capital letter = angle,  small letter = the side opposite it",
             fontsize=12, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-2-labelling.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 3. 4つの場面 =================
fig, axes = plt.subplots(1, 4, figsize=(13.0, 3.8))

TRI = [np.array([0.0, 0.0]), np.array([4.4, 0.0]), np.array([1.5, 2.9])]


def draw_tri(ax, known_sides, known_angles, want, title, col):
    A, B, Cv = TRI
    for (p, q) in [(A, B), (B, Cv), (Cv, A)]:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=GREY, linewidth=1.6, zorder=3)
    mids = {"c": (A + B) / 2 + np.array([0, -0.42]),
            "a": (B + Cv) / 2 + np.array([0.30, 0.16]),
            "b": (Cv + A) / 2 + np.array([-0.42, 0.10])}
    verts = {"A": A, "B": B, "C": Cv}

    def bisector(g):
        """角 g の内側（二等分線）の向きに、ラベルを置く位置を返す。"""
        v = verts[g]
        us = []
        for k in "ABC":
            if k == g:
                continue
            d = verts[k] - v
            us.append(d / np.linalg.norm(d))
        w = us[0] + us[1]
        return v + 0.95 * w / np.linalg.norm(w) - np.array([0.13, 0.13])
    for s in known_sides:
        p, q = {"c": (A, B), "a": (B, Cv), "b": (Cv, A)}[s]
        ax.plot([p[0], q[0]], [p[1], q[1]], color=col, linewidth=3.0, zorder=5)
        ax.annotate(f"${s}$", mids[s], fontsize=13, color=col, ha="center",
                    zorder=8)
    for g in known_angles:
        v = verts[g]
        others = [verts[k] for k in "ABC" if k != g]
        angle_mark(ax, v, others[0], others[1], radius=0.55, color=col)
        ax.annotate(f"${g}$", bisector(g), fontsize=13, color=col, zorder=8)
    ax.annotate(f"find  ${want}$", (2.2, -1.25), fontsize=12, color=INK,
                ha="center", fontweight="bold")
    clean(ax, (-1.3, 5.7), (-1.9, 3.9))
    ax.set_title(title, fontsize=11, pad=8)


draw_tri(axes[0], ["a"], ["A", "B"], "b",
         "Sine rule\n(a pair, and one more angle)", ACC)
draw_tri(axes[1], ["a", "b"], ["A"], "B",
         "Sine rule\n(a pair, and one more side)", ACC)
draw_tri(axes[2], ["a", "b"], ["C"], "c",
         "Cosine rule\n(two sides, angle between)", LINE)
draw_tri(axes[3], ["a", "b", "c"], [], "C",
         "Cosine rule\n(all three sides)", LINE)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-2-rules.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 4. 三角形の面積 =================
fig, ax = plt.subplots(figsize=(7.6, 4.4))
A2, B2, C2 = np.array([0.0, 0.0]), np.array([5.2, 0.0]), np.array([1.9, 3.1])
for (p, q) in [(A2, B2), (B2, C2), (C2, A2)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=1.8, zorder=4)
ax.plot([C2[0], C2[0]], [0, C2[1]], color=ACC, linestyle="--", linewidth=1.5,
        zorder=4)
rt_mark(ax, np.array([C2[0], 0.0]), (-1, 0), (0, 1))

angle_mark(ax, A2, B2, C2, radius=0.7, color=GREEN)
ax.annotate("$C$", (0.88, 0.30), fontsize=13, color=GREEN)
ax.annotate("$a$", (0.75, 1.75), fontsize=13, color=LINE)
ax.annotate("$b$", (2.6, -0.44), fontsize=13, color=LINE, ha="center")
ax.annotate("$h = a\\sin C$", (2.02, 1.5), fontsize=12, color=ACC, ha="left")
ax.annotate("area $= \\dfrac{1}{2}ab\\sin C$", (2.6, 3.6), fontsize=14,
            color=INK, ha="center")
ax.annotate("$C$ must be the angle\nBETWEEN $a$ and $b$", (5.0, 2.0),
            fontsize=10.5, color=GREEN, ha="center")
clean(ax, (-1.0, 7.4), (-1.1, 4.4))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-2-area.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-3-2-choose.svg, sl-3-2-labelling.svg, sl-3-2-rules.svg, "
      "sl-3-2-area.svg")
print("check 3-4-5 triangle angle at A:",
      round(np.degrees(np.arctan2(3, 4)), 4))
print("check area figure h:", round(3.1, 4))
