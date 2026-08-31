"""SL 5.4 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_4.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

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


def right_angle(ax, p, u, v, s=0.30, color=INK):
    """p を頂点に、方向 u と v ではさむ直角記号"""
    u = np.array(u, float); u = u / np.linalg.norm(u)
    v = np.array(v, float); v = v / np.linalg.norm(v)
    p = np.array(p, float)
    pts = [p + s * u, p + s * u + s * v, p + s * v]
    ax.plot([q[0] for q in pts], [q[1] for q in pts],
            color=color, lw=1.3, zorder=9)


# ══════════════ 1. 接線と法線 ══════════════
fig, ax = plt.subplots(figsize=(7.0, 7.4))
axes(ax, (-0.3, 5.7), (-0.6, 6.4), 1, 1)
ax.set_aspect("equal")

xs = np.linspace(-0.1, 5.3, 400)
ax.plot(xs, xs ** 2 - 4 * xs + 5, color=LINE, lw=2.6, zorder=5)
ax.text(0.92, 3.45, "$y=f(x)$", color=LINE, fontsize=12.5, ha="left",
        va="center", zorder=10, bbox=BOX)

# tangent y = 2x - 4
t = np.array([2.25, 4.75])
ax.plot(t, 2 * t - 4, color=ACC, lw=2.4, zorder=6)
ax.text(4.62, 5.55, "tangent", color=ACC, fontsize=12.5, ha="right",
        va="center", zorder=10, bbox=BOX)

# normal y = -0.5x + 3.5
n = np.array([1.25, 5.05])
ax.plot(n, -0.5 * n + 3.5, color=GREEN, lw=2.4, zorder=6)
ax.text(4.30, 1.62, "normal", color=GREEN, fontsize=12.5, ha="left",
        va="center", zorder=10, bbox=BOX)

right_angle(ax, (3, 2), (1, 2), (2, -1), s=0.34)
ax.plot([2.62, 2.95], [2.72, 2.12], color=GREY, lw=1.0, zorder=10)
ax.plot([3], [2], "o", color=INK, ms=8, zorder=11)
ax.text(2.55, 2.86, "$P(3,\\,2)$", fontsize=12.5, ha="center", va="bottom",
        zorder=12, bbox=BOX)

ax.text(0.55, 5.9, "the tangent touches the curve at $P$\n"
                   "the normal is perpendicular to it",
        fontsize=11.5, ha="left", va="center", color=INK, zorder=10, bbox=BOX)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-4-idea.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 3つの手順 ══════════════
fig, ax = plt.subplots(figsize=(8.6, 2.9))
blank(ax, ylim=(0.06, 0.94))

steps = [
    (0.115, "1", "differentiate", r"$f'(x)$", ACC, 0.035),
    (0.430, "2", "put $x=a$ in", r"$m_{\mathrm{tangent}}=f'(a)$", GREEN, 0.112),
    (0.815, "3", "use", r"$y-y_{1}=m(x-x_{1})$", LINE, 0.118),
]
for i, (px, no, lab, eq, col, half) in enumerate(steps):
    ax.text(px - 0.085, 0.73, no, color="white", fontsize=12, ha="center",
            va="center", zorder=9, fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.34", fc=col, ec="none"))
    ax.text(px - 0.052, 0.73, lab, color=col, fontsize=12.5, ha="left",
            va="center")
    ax.text(px, 0.42, eq, color=INK, fontsize=19, ha="center", va="center")
    if i:
        px0, half0 = steps[i-1][0], steps[i-1][5]
        ax.annotate("", xy=(px - half - 0.035, 0.44),
                    xytext=(px0 + half0 + 0.035, 0.44),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.8))
ax.text(0.50, 0.14, "for the normal, only step 3 changes:   use   "
                    r"$m_{\mathrm{normal}}=-\dfrac{1}{m_{\mathrm{tangent}}}$",
        fontsize=12.5, ha="center", va="center", color=GOLD)
ax.set_xlim(0.0, 1.0)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-4-steps.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. y 座標は自分で作る ══════════════
fig, ax = plt.subplots(figsize=(7.4, 5.6))
axes(ax, (-0.3, 5.4), (-0.6, 6.4), 1, 1)
xs = np.linspace(-0.1, 5.1, 400)
ax.plot(xs, xs ** 2 - 6 * xs + 11, color=LINE, lw=2.6, zorder=5)

ax.plot([4, 4], [0, 3], ls=(0, (5, 4)), color=ACC, lw=1.6, zorder=4)
ax.plot([0, 4], [3, 3], ls=(0, (5, 4)), color=ACC, lw=1.6, zorder=4)
ax.plot([4], [3], "o", color=INK, ms=8, zorder=9)
ax.plot([4], [0], "o", color=ACC, ms=6, zorder=9)

ax.text(4.0, -0.32, "$x=4$  (given)", color=ACC, fontsize=11.5, ha="center",
        va="top", zorder=10, bbox=BOX)
ax.text(-0.16, 3.0, r"$f(4)=3$", color=ACC, fontsize=12, ha="right",
        va="center", zorder=10, bbox=BOX)
ax.text(4.28, 3.35, "$(4,\\,3)$", fontsize=12.5, ha="left", va="bottom",
        zorder=10, bbox=BOX)
ax.text(2.85, 5.6, "the question gives only $x=4$\n"
                   r"put it into $f$ to get the $y$-coordinate",
        fontsize=11.5, ha="center", va="center", color=INK, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-4-point.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 傾きの三角形は 90 度まわしただけ ══════════════
fig, ax = plt.subplots(figsize=(7.6, 6.0))
blank(ax, (-3.5, 2.7), (-3.0, 3.5))
ax.set_aspect("equal")

# tangent through the origin, gradient 2
ax.plot([-1.35, 1.55], [-2.7, 3.1], color=ACC, lw=2.4, zorder=5)
# normal through the origin, gradient -1/2
ax.plot([-3.2, 1.5], [1.6, -0.75], color=GREEN, lw=2.4, zorder=5)

# tangent slope triangle: right 1, up 2
ax.plot([0, 1, 1], [0, 0, 2], color=ACC, lw=1.6, ls=(0, (4, 3)), zorder=6)
ax.text(0.5, -0.22, "right $1$", color=ACC, fontsize=11.5, ha="center",
        va="top", zorder=10, bbox=BOX)
ax.text(1.14, 1.0, "up $2$", color=ACC, fontsize=11.5, ha="left",
        va="center", zorder=10, bbox=BOX)
ax.text(1.42, 3.30, r"$m_{\mathrm{tangent}}=2$", color=ACC, fontsize=13, ha="left",
        va="center", zorder=10, bbox=BOX)

# normal slope triangle: up 1, left 2
ax.plot([0, 0, -2], [0, 1, 1], color=GREEN, lw=1.6, ls=(0, (4, 3)), zorder=6)
ax.text(0.16, 0.55, "up $1$", color=GREEN, fontsize=11.5, ha="left",
        va="center", zorder=10, bbox=BOX)
ax.text(-1.0, 1.20, "left $2$", color=GREEN, fontsize=11.5, ha="center",
        va="bottom", zorder=10, bbox=BOX)
ax.text(-3.95, 1.80, r"$m_{\mathrm{normal}}=-\dfrac{1}{2}$", color=GREEN, fontsize=13,
        ha="left", va="center", zorder=10, bbox=BOX)

right_angle(ax, (0, 0), (1, 2), (-2, 1), s=0.34)
ax.plot([0], [0], "o", color=INK, ms=8, zorder=11)

ax.text(-3.4, -1.15, "the same triangle,\nturned through $90^\\circ$",
        fontsize=12, ha="left", va="center", color=INK, zorder=10, bbox=BOX)
ax.text(-3.4, -2.2, r"$m_{\mathrm{tangent}}\times m_{\mathrm{normal}}"
                    r"=2\times\left(-\frac{1}{2}\right)=-1$", fontsize=13,
        ha="left", va="center", color=INK, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-4-normal.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. 特別な場合：f'(a)=0 ══════════════
fig, ax = plt.subplots(figsize=(7.6, 5.8))
axes(ax, (-2.5, 2.5), (-3.6, 3.6), 1, 1)
xs = np.linspace(-2.3, 2.3, 400)
ax.plot(xs, xs ** 3 - 3 * xs, color=LINE, lw=2.6, zorder=5)

for a, y in ((-1, 2), (1, -2)):
    ax.plot([a - 1.0, a + 1.0], [y, y], color=ACC, lw=2.4, zorder=6)
    ax.plot([a, a], [-3.45, 3.45], color=GREEN, lw=2.0,
            ls=(0, (6, 4)), zorder=4)
    ax.plot([a], [y], "o", color=INK, ms=8, zorder=11)
    right_angle(ax, (a, y), (1 if a < 0 else -1, 0), (0, 1 if a < 0 else -1),
                s=0.24)

ax.text(-1.0, 2.62, "tangent  $y=2$", color=ACC, fontsize=11.5, ha="center",
        va="bottom", zorder=10, bbox=BOX)
ax.text(1.0, -2.62, "tangent  $y=-2$", color=ACC, fontsize=11.5, ha="center",
        va="top", zorder=10, bbox=BOX)
ax.text(-1.12, -1.5, "normal\n$x=-1$", color=GREEN, fontsize=11.5, ha="right",
        va="center", zorder=10, bbox=BOX)
ax.text(1.12, 1.5, "normal\n$x=1$", color=GREEN, fontsize=11.5, ha="left",
        va="center", zorder=10, bbox=BOX)
ax.text(-2.4, 3.25, r"at both points $f'(a)=0$", fontsize=12.5, ha="left",
        va="center", color=INK, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-4-special.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
import sympy as sp
X = sp.Symbol('x')
for f, a in [(X**2 - 4*X + 5, 3), (X**3 - 3*X, 1), (X**3 - 3*X, -1)]:
    fp = sp.diff(f, X)
    print(f"f={f} a={a}: f(a)={f.subs(X, a)}  f'(a)={fp.subs(X, a)}")
print("figures written to", os.path.normpath(OUT))
