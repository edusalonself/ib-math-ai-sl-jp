"""SL 5.7 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_7.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle, Ellipse

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, GOLD = "#7a8592", "#b9770e"
plt.rcParams.update({"font.size": 11, "text.color": INK, "svg.fonttype": "path"})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.93)


def blank(ax, xlim=(0, 1), ylim=(0, 1)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def axes(ax, xlim, ylim, xt=1, yt=1, xlab="$x$", ylab="$y$", ypad=12):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for x in np.arange(np.ceil(xlim[0] / xt) * xt, xlim[1] + 1e-9, xt):
        ax.axvline(x, color=GRID, lw=0.7, zorder=0)
    for y in np.arange(np.ceil(ylim[0] / yt) * yt, ylim[1] + 1e-9, yt):
        ax.axhline(y, color=GRID, lw=0.7, zorder=0)
    ax.axhline(0, color=GREY, lw=1.2, zorder=1)
    ax.axvline(0, color=GREY, lw=1.2, zorder=1)
    ax.tick_params(labelsize=8.5, colors=GREY, length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel(xlab, fontsize=11, color=INK, labelpad=1)
    ax.set_ylabel(ylab, fontsize=11, color=INK, labelpad=ypad, rotation=0)


def dim(ax, p, q, lab, off=0.0, side=1, color=INK, fs=12, rot=0):
    """p→q に寸法線と文字"""
    p, q = np.array(p, float), np.array(q, float)
    v = q - p; n = np.array([-v[1], v[0]]); n = n / np.linalg.norm(n) * off * side
    ax.annotate("", xy=q + n, xytext=p + n,
                arrowprops=dict(arrowstyle="<|-|>", color=color, lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=11))
    m = (p + q) / 2 + n * 1.9
    ax.text(m[0], m[1], lab, color=color, fontsize=fs, ha="center",
            va="center", rotation=rot, zorder=10, bbox=BOX)


# ══════════════ 1. 5つの手順 ══════════════
fig, ax = plt.subplots(figsize=(7.2, 4.2))
blank(ax, (0, 1), (0, 1))

steps = [
    ("1", "name the variable", "$x = \\ldots$", ACC),
    ("2", "write the constraint", "e.g. $60 = 2x + y$", GOLD),
    ("3", "get ONE variable", "$A(x) = \\ldots$", GREEN),
    ("4", "differentiate, solve", "$A'(x) = 0$", LINE),
    ("5", "check, then answer", "max or min?  units?", INK),
]
for i, (no, lab, eq, col) in enumerate(steps):
    y = 0.90 - i * 0.19
    ax.text(0.055, y, no, color="white", fontsize=12, ha="center", va="center",
            zorder=9, fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.34", fc=col, ec="none"))
    ax.text(0.115, y, lab, color=col, fontsize=13, ha="left", va="center")
    ax.text(0.99, y, eq, color=INK, fontsize=13.5, ha="right", va="center")
    if i < 4:
        ax.annotate("", xy=(0.055, y - 0.145), xytext=(0.055, y - 0.045),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
ax.text(0.5, 0.015, "step 2 is the one students forget",
        fontsize=12, ha="center", va="center", color=GOLD)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-7-steps.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 壁ぎわの囲い ══════════════
fig, ax = plt.subplots(figsize=(6.6, 4.0))
blank(ax, (-1.2, 11.2), (-1.9, 5.4))
ax.set_aspect("equal")

W, H = 8.0, 3.2
# wall
ax.plot([-0.6, W + 0.6], [H, H], color=INK, lw=4.0, zorder=6)
for t in np.arange(-0.6, W + 0.7, 0.42):
    ax.plot([t, t - 0.30], [H, H + 0.34], color=GREY, lw=1.3, zorder=5)
ax.text(W / 2, H + 0.72, "wall  (no fence needed here)", fontsize=12,
        ha="center", va="bottom", color=INK)

ax.add_patch(Rectangle((0, 0), W, H, facecolor=LINE, alpha=0.13, zorder=2))
for seg in ([(0, 0), (0, H)], [(W, 0), (W, H)], [(0, 0), (W, 0)]):
    ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], color=ACC,
            lw=3.0, zorder=6)

dim(ax, (-0.75, 0), (-0.75, H), "$x$", off=0.0, color=ACC, fs=13)
dim(ax, (0, -0.85), (W, -0.85), "$60-2x$", off=0.0, color=ACC, fs=13)
ax.text(W / 2, H / 2, "area $= x(60-2x)$", fontsize=13.5, ha="center",
        va="center", color=INK, zorder=10, bbox=BOX)
ax.text(10.9, 1.6, "the fence has\n$3$ sides only", fontsize=11.5,
        ha="right", va="center", color=ACC, zorder=10, bbox=BOX)
ax.text(-1.1, 4.9, "$60$ m of fencing:   $2x + (\\text{other side}) = 60$",
        fontsize=12.5, ha="left", va="center", color=GOLD)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-7-fence.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. 角を切って折る箱 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.6),
                        gridspec_kw=dict(wspace=0.05))

ax = axs[0]
blank(ax, (-1.6, 14.6), (-2.6, 15.2))
ax.set_aspect("equal")
S, c = 12.0, 2.6
ax.add_patch(Rectangle((0, 0), S, S, facecolor="none", edgecolor=INK, lw=2.0,
                       zorder=5))
for (px, py) in ((0, 0), (S - c, 0), (0, S - c), (S - c, S - c)):
    ax.add_patch(Rectangle((px, py), c, c, facecolor=ACC, alpha=0.22,
                           edgecolor=ACC, lw=1.6, zorder=4))
for t in (c, S - c):
    ax.plot([t, t], [0, S], color=GREY, lw=1.3, ls=(0, (5, 4)), zorder=3)
    ax.plot([0, S], [t, t], color=GREY, lw=1.3, ls=(0, (5, 4)), zorder=3)
dim(ax, (0, -1.3), (S, -1.3), "$12$", off=0.0, fs=12.5)
dim(ax, (0, S + 1.1), (c, S + 1.1), "$x$", off=0.0, color=ACC, fs=12.5)
dim(ax, (c, S + 1.1), (S - c, S + 1.1), "$12-2x$", off=0.0, color=GREEN,
    fs=12.5)
ax.set_title("cut a square of side $x$ from each corner", fontsize=12.5,
             color=INK, pad=10)

ax = axs[1]
blank(ax, (-1.6, 13.6), (-2.6, 15.2))
ax.set_aspect("equal")
b, hh = 7.6, 4.2
dv = np.array([2.6, 1.9])
O = np.array([1.5, 2.6])
FBL, FBR = O, O + np.array([b, 0.0])
BBR, BBL = FBR + dv, O + dv
up = np.array([0.0, hh])
TFL, TFR, TBR, TBL = FBL + up, FBR + up, BBR + up, BBL + up

ax.add_patch(Polygon([FBL, FBR, BBR, BBL], closed=True, facecolor=LINE,
                     alpha=0.16, edgecolor="none", zorder=2))
# hidden edges
for p0, p1 in ((FBL, BBL), (BBL, BBR), (BBL, TBL)):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=GREY, lw=1.4,
            ls=(0, (5, 4)), zorder=3)
# visible edges
for p0, p1 in ((FBL, FBR), (FBR, BBR), (FBL, TFL), (FBR, TFR), (BBR, TBR),
               (TFL, TFR), (TFR, TBR), (TBR, TBL), (TBL, TFL)):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=INK, lw=2.0, zorder=6)

dim(ax, (FBL[0] - 0.95, FBL[1]), (FBL[0] - 0.95, TFL[1]), "$x$", off=0.0,
    color=ACC, fs=12.5)
dim(ax, (FBL[0], FBL[1] - 1.1), (FBR[0], FBR[1] - 1.1), "$12-2x$", off=0.0,
    color=GREEN, fs=12.5)
ax.text(6.0, 13.0, "$V = x(12-2x)^{2}$", fontsize=15, ha="center",
        va="center", color=INK)
ax.set_title("fold up the sides: an open box", fontsize=12.5, color=INK,
             pad=10)

fig.savefig(os.path.join(OUT, "sl-5-7-box.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 定義域を忘れない ══════════════
fig, ax = plt.subplots(figsize=(7.4, 4.8))
axes(ax, (-0.9, 7.4), (-40, 175), 1, 40, ylab="")
xs = np.linspace(-0.6, 7.2, 500)
V = lambda t: 4 * t ** 3 - 48 * t ** 2 + 144 * t
ax.plot(xs, V(xs), color=GRID, lw=2.4, zorder=3)
xd = np.linspace(0, 6, 400)
ax.plot(xd, V(xd), color=LINE, lw=3.0, zorder=5)
ax.fill_between(xd, -40, V(xd), color=LINE, alpha=0.07, zorder=1)

ax.plot([2], [128], "o", color=ACC, ms=10, zorder=9)
ax.text(2.35, 148, "maximum  $(2,\\,128)$", color=ACC, fontsize=12.5,
        ha="left", va="center", zorder=10, bbox=BOX)
ax.plot([6], [0], "o", color=GREY, ms=8, zorder=9)
ax.text(6.15, 34, "$x=6$ also solves\n$V'(x)=0$, but the box\nwould have no base",
        color=GREY, fontsize=11, ha="right", va="center", zorder=10, bbox=BOX)

for a in (0, 6):
    ax.axvline(a, color=GOLD, lw=1.6, ls=(0, (5, 4)), zorder=2)
ax.text(3.0, -28, "the only sensible domain is  $0 < x < 6$",
        color=GOLD, fontsize=12.5, ha="center", va="center", zorder=10,
        bbox=BOX)
ax.set_xlabel("$x$  (cm cut from each corner)", fontsize=11, color=INK,
              labelpad=1)
ax.text(-0.7, 165, "$V$  (cm$^{3}$)", color=LINE, fontsize=12, ha="left",
        va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-7-domain.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. 円柱：公式集にあるのは「側面」だけ ══════════════
fig, axs = plt.subplots(1, 2, figsize=(9.8, 4.4),
                        gridspec_kw=dict(wspace=0.08))

ax = axs[0]
blank(ax, (-3.4, 3.4), (-1.4, 6.4))
ax.set_aspect("equal")
R, HH = 1.9, 3.6
ax.add_patch(Rectangle((-R, 0.6), 2 * R, HH, facecolor=LINE, alpha=0.14,
                       edgecolor="none", zorder=2))
ax.add_patch(Ellipse((0, 0.6 + HH), 2 * R, 0.95, facecolor="white",
                     edgecolor=INK, lw=1.8, zorder=5))
ax.add_patch(Ellipse((0, 0.6), 2 * R, 0.95, facecolor=GREEN, alpha=0.20,
                     edgecolor=INK, lw=1.8, zorder=3))
for sx in (-R, R):
    ax.plot([sx, sx], [0.6, 0.6 + HH], color=INK, lw=1.8, zorder=4)
ax.plot([0, R], [0.6 + HH, 0.6 + HH], color=ACC, lw=1.8, zorder=7)
ax.plot([0], [0.6 + HH], "o", color=ACC, ms=4.5, zorder=8)
ax.text(R / 2, 0.6 + HH + 0.42, "$r$", color=ACC, fontsize=13, ha="center",
        va="bottom", zorder=9)
dim(ax, (R + 0.75, 0.6), (R + 0.75, 0.6 + HH), "$h$", off=0.0, color=ACC,
    fs=12.5)
ax.text(0, -0.9, "open at the top", fontsize=12, ha="center", va="center",
        color=INK)
ax.set_title("the container", fontsize=12.5, color=INK, pad=8)

ax = axs[1]
blank(ax, (-0.6, 10.6), (-2.2, 6.6))
ax.set_aspect("equal")
ax.add_patch(Rectangle((0.4, 2.0), 5.0, 2.9, facecolor=LINE, alpha=0.14,
                       edgecolor=INK, lw=1.8, zorder=3))
ax.text(2.9, 3.45, "$2\\pi r \\times h$", fontsize=15, ha="center",
        va="center", color=INK, zorder=6)
ax.text(2.9, 5.15, "curved surface\nIN the booklet", color=GREEN,
        fontsize=11.5, ha="center", va="bottom", zorder=6)
ax.add_patch(plt.Circle((8.0, 3.45), 1.25, facecolor=GREEN, alpha=0.20,
                        edgecolor=INK, lw=1.8, zorder=3))
ax.text(8.0, 3.45, "$\\pi r^{2}$", fontsize=15, ha="center", va="center",
        color=INK, zorder=6)
ax.text(8.0, 5.15, "the base\nNOT in the booklet", color=ACC, fontsize=11.5,
        ha="center", va="bottom", zorder=6)
ax.text(4.6, 0.4, "$S = 2\\pi r h + \\pi r^{2}$", fontsize=15.5,
        ha="center", va="center", color=INK)
ax.set_title("its surface, opened out", fontsize=12.5, color=INK, pad=8)

fig.savefig(os.path.join(OUT, "sl-5-7-cylinder.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
import sympy as sp
X = sp.Symbol('x', positive=True)
for e, lab in ((X * (60 - 2 * X), "fence"), (X * (12 - 2 * X) ** 2, "box")):
    d = sp.diff(e, X)
    print(lab, "->", sp.factor(sp.expand(d)), " zeros", sp.solve(d, X))
print("V(2) =", (X * (12 - 2 * X) ** 2).subs(X, 2))
R = sp.Symbol('r', positive=True)
S = sp.pi * R ** 2 + 2000 / R
rr = sp.solve(sp.diff(S, R), R)[0]
print("cylinder r = %.4f, S = %.4f" % (float(rr), float(S.subs(R, rr))))
print("figures written to", os.path.normpath(OUT))
