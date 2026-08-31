"""SL 3.2 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_3_2.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl",
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


# ================================================================
#  以下、あとから足した図
#    5. 大文字と小文字の約束（§3 の見出し直下）
#    6. cosine rule（§5 の見出し直下）
#    7-12. 例題1〜6 の図
# ================================================================

def tri(A_deg, b, c):
    """A を原点、AB を x 軸にとった三角形の頂点 (A, B, C) を返す。"""
    A = np.array([0.0, 0.0])
    B = np.array([float(c), 0.0])
    C = np.array([b * np.cos(np.radians(A_deg)), b * np.sin(np.radians(A_deg))])
    return A, B, C


def side_label(ax, p, q, text, color=INK, off=0.09, fs=13, inside=None,
               weight=None):
    """辺 pq の中点の、三角形の外側にラベルを置く。"""
    p, q = np.array(p, float), np.array(q, float)
    m = (p + q) / 2.0
    d = q - p
    n = np.array([-d[1], d[0]])
    n = n / np.linalg.norm(n)
    if inside is not None:                       # 内側を向いていたら反転
        if np.dot(np.array(inside, float) - m, n) > 0:
            n = -n
    L = np.linalg.norm(d)
    ha = "center"
    if abs(n[0]) > 0.35:                         # 斜めの辺は、線と反対側へ寄せる
        ha = "left" if n[0] > 0 else "right"
    ax.annotate(text, m + n * off * L, color=color, fontsize=fs,
                ha=ha, va="center", zorder=9, fontweight=weight)


def ang_label(ax, v, p, q, text, color=ACC, r=None, fs=13, rad=0.55, mark=True,
              tmul=1.75):
    """頂点 v の角に弧とラベルを描く。"""
    v, p, q = np.array(v, float), np.array(p, float), np.array(q, float)
    scale = max(np.linalg.norm(p - v), np.linalg.norm(q - v))
    R = rad if r is None else r
    if mark:
        angle_mark(ax, v, p, q, radius=R, color=color)
    u = (p - v) / np.linalg.norm(p - v) + (q - v) / np.linalg.norm(q - v)
    u = u / np.linalg.norm(u)
    ax.annotate(text, v + u * R * tmul, color=color, fontsize=fs,
                ha="center", va="center", zorder=9)


def outline(ax, pts, color=INK, lw=2.0, z=5):
    P = np.array(pts + [pts[0]], float)
    ax.plot(P[:, 0], P[:, 1], color=color, linewidth=lw, zorder=z)


def vlabels(ax, pts, names, offs, fs=13):
    for p, n, o in zip(pts, names, offs):
        ax.annotate(n, p, textcoords="offset points", xytext=o, fontsize=fs,
                    color=INK, ha="center", va="center")


# ================= 5. 大文字と小文字の約束 =================
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

A, B, C = tri(52, 5.4, 7.0)

# --- 左：A-a, B-b, C-c を色で対応させる ---
ax = axes[0]
outline(ax, [A, B, C], color=INK, lw=2.0)
side_label(ax, B, C, "$a$", color=ACC, inside=A, off=0.10)
side_label(ax, C, A, "$b$", color=GREEN, inside=B, off=0.10)
side_label(ax, A, B, "$c$", color=LINE, inside=C, off=0.085)
ang_label(ax, A, B, C, "$A$", color=ACC, r=0.85)
ang_label(ax, B, C, A, "$B$", color=GREEN, r=0.85)
ang_label(ax, C, A, B, "$C$", color=LINE, r=0.85)
vlabels(ax, [A, B, C], ["$A$", "$B$", "$C$"],
        [(-16, -12), (16, -12), (0, 16)])
ax.annotate("same colour = a pair\n(an angle and the side opposite it)",
            (3.5, -2.30), fontsize=10.5, ha="center", color=INK)
clean(ax, (-1.9, 8.9), (-3.3, 6.4))
ax.set_title("Capital = angle,  small = the side opposite it",
             fontsize=12, pad=8)

# --- 右：PQR で出されたら、自分で書き込む ---
ax = axes[1]
outline(ax, [A, B, C], color=INK, lw=2.0)
vlabels(ax, [A, B, C], ["$P$", "$Q$", "$R$"],
        [(-16, -12), (16, -12), (0, 16)])
side_label(ax, B, C, "$p$", color=ACC, inside=A, off=0.10)
side_label(ax, C, A, "$q$", color=GREEN, inside=B, off=0.10)
side_label(ax, A, B, "$r$", color=LINE, inside=C, off=0.085)
ax.annotate("the question gives you only $P$, $Q$, $R$ —\n"
            "write $p$, $q$, $r$ on your own diagram first",
            (3.5, -2.30), fontsize=10.5, ha="center", color=ACC)
clean(ax, (-1.9, 8.9), (-3.3, 6.4))
ax.set_title("Same rule with any letters", fontsize=12, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-2-notation.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)


# ================= 6. cosine rule =================
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))

A, B, C = tri(43.7735, 10.0, 8.2885)          # a=7, b=10, C=55

# --- 左：2辺とあいだの角 → 残りの辺 ---
ax = axes[0]
ax.plot([C[0], B[0]], [C[1], B[1]], color=LINE, linewidth=2.6, zorder=5)
ax.plot([C[0], A[0]], [C[1], A[1]], color=LINE, linewidth=2.6, zorder=5)
ax.plot([A[0], B[0]], [A[1], B[1]], color=ACC, linewidth=2.4, linestyle="--",
        zorder=5)
side_label(ax, B, C, "$a$", color=LINE, inside=A, off=0.11)
side_label(ax, C, A, "$b$", color=LINE, inside=B, off=0.11)
side_label(ax, A, B, "$c = ?$", color=ACC, inside=C, off=0.10)
ang_label(ax, C, A, B, "$C$", color=LINE, r=1.05)
vlabels(ax, [A, B, C], ["$A$", "$B$", "$C$"],
        [(-16, -12), (16, -12), (0, 18)])
ax.annotate(r"$c^{2} = a^{2} + b^{2} - 2ab\cos C$", (4.1, -2.35), fontsize=13,
            ha="center", color=INK)
clean(ax, (-2.2, 10.4), (-3.4, 9.0))
ax.set_title("Two sides and the angle between them", fontsize=12, pad=8,
             color=LINE)

# --- 右：3辺 → 角 ---
ax = axes[1]
outline(ax, [A, B, C], color=LINE, lw=2.6)
side_label(ax, B, C, "$a$", color=LINE, inside=A, off=0.11)
side_label(ax, C, A, "$b$", color=LINE, inside=B, off=0.11)
side_label(ax, A, B, "$c$", color=LINE, inside=C, off=0.10)
ang_label(ax, C, A, B, "$C = ?$", color=ACC, r=1.05, tmul=2.7)
vlabels(ax, [A, B, C], ["$A$", "$B$", "$C$"],
        [(-16, -12), (16, -12), (0, 18)])
ax.annotate(r"$\cos C = \dfrac{a^{2} + b^{2} - c^{2}}{2ab}$", (4.1, -2.45),
            fontsize=13, ha="center", color=INK)
clean(ax, (-2.2, 10.4), (-3.4, 9.0))
ax.set_title("All three sides", fontsize=12, pad=8, color=LINE)

fig.text(0.5, 0.015,
         "in both pictures  $C$  is between  $a$  and  $b$,  "
         "and  $c$  is the side opposite  $C$",
         ha="center", fontsize=11.5, color=ACC)
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig(os.path.join(OUT, "sl-3-2-cosine.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)


# ================= 7-12. 例題の図 =================
def we_fig(name, draw, figsize=(5.4, 3.9)):
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    fig.tight_layout()
    # 例題の図は callout の中に置くので、背景を透明にして地の色になじませる
    fig.savefig(os.path.join(OUT, name), format="svg", bbox_inches="tight",
                transparent=True)
    plt.close(fig)


# --- 例題1：はしご（直角三角形） ---
def _we1(ax):
    F = np.array([0.0, 0.0])            # はしごの足
    W = np.array([1.5, 0.0])            # 壁の根もと
    T = np.array([1.5, 3.9230])         # はしごの先
    ax.plot([-0.9, 2.6], [0, 0], color=GREY, linewidth=1.6, zorder=3)
    for x in np.arange(-0.75, 2.6, 0.30):
        ax.plot([x, x - 0.18], [0, -0.20], color=GREY, linewidth=0.9, zorder=3)
    ax.plot([W[0], 1.5], [0, 4.5], color=GREY, linewidth=2.6, zorder=3)
    ax.plot([F[0], T[0]], [F[1], T[1]], color=ACC, linewidth=2.8, zorder=6)
    ax.plot([F[0], W[0]], [0, 0], color=GREEN, linewidth=2.8, zorder=6)
    ax.plot([W[0], T[0]], [W[1], T[1]], color=LINE, linewidth=2.8, zorder=6)
    rt_mark(ax, W, (-1, 0), (0, 1), size=0.24)
    ang_label(ax, F, W, T, r"$\theta = ?$", color=ACC, r=0.55, tmul=2.4, fs=12)
    ax.annotate("ladder  4.2 m", (0.45, 2.25), color=ACC, fontsize=12,
                rotation=69.1, ha="center", va="center", bbox=BOX, zorder=9)
    ax.annotate("1.5 m", (0.75, -0.42), color=GREEN, fontsize=12, ha="center")
    ax.annotate("$?$ m", (1.72, 2.0), color=LINE, fontsize=13, ha="left",
                va="center")
    ax.annotate("wall", (1.72, 4.25), color=GREY, fontsize=10.5, ha="left")
    clean(ax, (-1.1, 3.4), (-0.9, 4.9))
    ax.set_title("The wall is vertical, so the right angle is at the foot "
                 "of the wall", fontsize=10.5, pad=8)


we_fig("sl-3-2-we1.svg", _we1, figsize=(5.6, 4.3))


def _plain(A_deg, b, c, sides, angles, verts=("$A$", "$B$", "$C$"),
           title="", note=None, pad=None):
    """三角形を1つ描く関数を返す。sides/angles は (text, color) の3つ組。"""
    def draw(ax):
        A, B, C = tri(A_deg, b, c)
        outline(ax, [A, B, C], color=INK, lw=2.0)
        for ((p0, p1, inside), (txt, col, off)) in zip(
                [(B, C, A), (C, A, B), (A, B, C)], sides):
            if txt:
                side_label(ax, p0, p1, txt, color=col, inside=inside,
                           off=off, fs=12.5)
        for (v, p, q, spec) in [(A, B, C, angles[0]), (B, C, A, angles[1]),
                                (C, A, B, angles[2])]:
            if spec and spec[0]:
                txt, col, r, tm = spec
                ang_label(ax, v, p, q, txt, color=col, r=r, tmul=tm, fs=12.5)
        vlabels(ax, [A, B, C], list(verts),
                [(-15, -12), (15, -12), (0, 16)], fs=12.5)
        if note:
            ax.annotate(note[0], note[1], fontsize=10.5, ha="center",
                        color=note[2])
        xs = [A[0], B[0], C[0]]; ys = [A[1], B[1], C[1]]
        mx, my = max(xs) - min(xs), max(ys) - min(ys)
        if pad is None:                       # 上下左右の余白を同じ割合にする
            # 底辺のラベルは横幅を基準に置かれるので、下は mx も見て決める
            px = 0.17 * mx
            py_top = max(0.17 * my, 0.10 * mx)
            py_bot = max(0.17 * my, 0.17 * mx)
            clean(ax, (min(xs) - px, max(xs) + px),
                  (min(ys) - py_bot, max(ys) + py_top))
        else:
            clean(ax, (min(xs) - 0.22 * mx, max(xs) + 0.22 * mx),
                  (pad[0], pad[1]))
        ax.set_title(title, fontsize=11, pad=8)
    return draw


# --- 例題2：A=42, B=63, a=8 → b ---
we_fig("sl-3-2-we2.svg", _plain(
    42, 10.6527, 11.5484,
    [("$a = 8$ cm", ACC, 0.07), ("$b = ?$", LINE, 0.07), (None, INK, 0.10)],
    [(r"$42^{\circ}$", ACC, 1.5, 1.7), (r"$63^{\circ}$", LINE, 1.5, 1.7),
     (r"$C = ?$", GREEN, 1.4, 2.0)],
    title="A pair:  $a$ with $42^{\\circ}$"), figsize=(5.6, 4.0))

# --- 例題3：B=105, b=14, c=9 → C ---
we_fig("sl-3-2-we3.svg", _plain(
    36.6143, 14.0, 9.0,
    [(None, INK, 0.10), ("$b = 14$ cm", ACC, 0.07), ("$c = 9$ cm", LINE, 0.11)],
    [(None, INK, 1, 1), (r"$105^{\circ}$", ACC, 1.6, 1.35),
     (r"$C = ?$", LINE, 1.5, 2.15)],
    title="A pair:  $b$ with $105^{\\circ}$"), figsize=(5.6, 4.2))

# --- 例題4：a=7, b=10, C=55 → c ---
we_fig("sl-3-2-we4.svg", _plain(
    43.7735, 10.0, 8.2885,
    [("$a = 7$ cm", LINE, 0.07), ("$b = 10$ cm", LINE, 0.07),
     ("$c = ?$", ACC, 0.11)],
    [(None, INK, 1, 1), (None, INK, 1, 1),
     (r"$55^{\circ}$", ACC, 1.4, 1.8)],
    title="Two sides, and the angle between them"), figsize=(5.6, 4.0))

# --- 例題5：5, 7, 9 → 最大角 ---
we_fig("sl-3-2-we5.svg", _plain(
    33.5573, 7.0, 9.0,
    [("$a = 5$ cm", LINE, 0.09), ("$b = 7$ cm", LINE, 0.08),
     ("$c = 9$ cm  (longest)", ACC, 0.11)],
    [(None, INK, 1, 1), (None, INK, 1, 1),
     (r"$C = ?$", ACC, 1.2, 1.75)],
    title="The largest angle is opposite the longest side"),
    figsize=(5.8, 3.8))

# --- 例題6：土地 40, 55, 68 ---
we_fig("sl-3-2-we6.svg", _plain(
    42.8249, 55.0, 54.5594,
    [("40 m", LINE, 0.07), ("55 m", LINE, 0.07),
     (r"$\mathrm{third\ side} = ?$", ACC, 0.11)],
    [(None, INK, 1, 1), (None, INK, 1, 1),
     (r"$68^{\circ}$", ACC, 7.5, 1.8)],
    verts=("", "", ""),
    title="Two sides, and the angle between them"), figsize=(5.6, 4.0))

print("wrote sl-3-2-notation.svg, sl-3-2-cosine.svg, sl-3-2-we1..we6.svg")
