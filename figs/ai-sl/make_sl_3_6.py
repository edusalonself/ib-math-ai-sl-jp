"""SL 3.6 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_3_6.py

   Voronoi のセルは、半平面の交わりとして自前で切り出している
   （scipy に頼らないので、地図の枠でちょうど閉じた多角形になる）。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY = "#7a8592"
GOLD = "#b9770e"
CELLC = ["#e8f1fb", "#fdf1e6", "#eafaef", "#fdecea", "#f2edfa", "#fffbe6"]
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.9)

# ── 舞台設定 ───────────────────────────────────────────────
NAMES = ["A", "B", "C", "D", "E"]
SITES = {"A": (1, 12), "B": (7, 12), "C": (12, 7), "D": (2, 7), "E": (12, 1)}
LO, HI = 0.0, 13.0
VERTS = {(4, 10): "ABD", (7, 7): "BCD", (7, 4): "CDE"}


def clip(poly, a, b, c):
    """半平面 a*x + b*y <= c で多角形を切る（Sutherland-Hodgman）"""
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        dp = a * P[0] + b * P[1] - c
        dq = a * Q[0] + b * Q[1] - c
        if dp <= 1e-12:
            out.append(P)
        if (dp < -1e-12 < dq) or (dq < -1e-12 < dp):
            t = dp / (dp - dq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out


def cell(site, sites, lo=LO, hi=HI):
    """site の Voronoi セルを、地図の枠内の多角形として返す"""
    poly = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
    sx, sy = site
    for t in sites:
        if t == site:
            continue
        tx, ty = t
        # |p-s|^2 <= |p-t|^2  ⇔  2(tx-sx)x + 2(ty-sy)y <= tx^2+ty^2-sx^2-sy^2
        a = 2 * (tx - sx); b = 2 * (ty - sy)
        c = tx * tx + ty * ty - sx * sx - sy * sy
        poly = clip(poly, a, b, c)
        if not poly:
            break
    return poly


def frame(ax, lo=LO, hi=HI, ticks=2, pad=0.7):
    ax.set_xlim(lo - pad, hi + pad); ax.set_ylim(lo - pad, hi + pad)
    ax.set_aspect("equal")
    for v in np.arange(lo, hi + 1e-9, 1):
        ax.axvline(v, color=GRID, lw=0.7, zorder=0)
        ax.axhline(v, color=GRID, lw=0.7, zorder=0)
    ax.add_patch(Polygon([(lo, lo), (hi, lo), (hi, hi), (lo, hi)], closed=True,
                         fill=False, edgecolor=GREY, lw=1.4, zorder=7))
    ax.set_xticks(np.arange(lo, hi + 1e-9, ticks))
    ax.set_yticks(np.arange(lo, hi + 1e-9, ticks))
    ax.tick_params(labelsize=8.5, colors=GREY, length=0)
    for s in ax.spines.values():
        s.set_visible(False)


def draw_map(ax, sites=None, fill=True, labels=True, lw=1.9, alpha=1.0):
    sites = sites or SITES
    pts = list(sites.values())
    for i, (nm, p) in enumerate(sites.items()):
        poly = cell(p, pts)
        if fill and len(poly) >= 3:
            ax.add_patch(Polygon(poly, closed=True, facecolor=CELLC[i % len(CELLC)],
                                 edgecolor="none", alpha=alpha, zorder=1))
        if len(poly) >= 3:
            ax.add_patch(Polygon(poly, closed=True, fill=False,
                                 edgecolor=LINE, lw=lw, zorder=5))
    for nm, p in sites.items():
        ax.plot([p[0]], [p[1]], "o", color=INK, ms=7, zorder=9)
        if labels:
            ax.text(p[0] + 0.30, p[1] + 0.28, f"${nm}$", fontsize=12.5,
                    ha="left", va="bottom", zorder=10, bbox=BOX)


# ══════════════ 1. 用語（site / cell / edge / vertex）══════════════
fig, ax = plt.subplots(figsize=(8.6, 7.4))
frame(ax)
draw_map(ax)
for v in VERTS:
    ax.plot([v[0]], [v[1]], "o", color=ACC, ms=8, zorder=9)
    ax.text(v[0] - 0.30, v[1] - 0.32, f"$({v[0]},{v[1]})$", color=ACC,
            fontsize=10.5, ha="right", va="top", zorder=10, bbox=BOX)

ax.annotate("site", xy=SITES["D"], xytext=(4.6, 5.4), fontsize=11.5, color=INK,
            ha="center", va="center", bbox=BOX, zorder=11,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.3))
ax.annotate("edge", xy=(7, 5.6), xytext=(10.0, 5.9), fontsize=11.5, color=LINE,
            ha="center", va="center", bbox=BOX, zorder=11,
            arrowprops=dict(arrowstyle="->", color=LINE, lw=1.3))
ax.annotate("vertex", xy=(7, 7), xytext=(4.3, 8.5), fontsize=11.5, color=ACC,
            ha="center", va="center", bbox=BOX, zorder=11,
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.3))
ax.text(2.2, 3.2, "cell of $D$", fontsize=11.5, color=INK, ha="center",
        va="center", zorder=11, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-6-parts.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. edge は垂直二等分線、vertex は3点から等距離 ══════════════
fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.0))

# --- (a) edge = 垂直二等分線の一部
ax = axes[0]
frame(ax)
draw_map(ax, fill=True, lw=1.5, alpha=0.55)
xs = np.array([LO, HI])
ax.plot(xs, xs, color=ACC, lw=1.6, ls="--", zorder=6)      # y = x（B|C の全体）
ax.plot([7, 13], [7, 13], color=ACC, lw=3.2, zorder=7)      # 実際の edge
B, C = SITES["B"], SITES["C"]
ax.plot([B[0], C[0]], [B[1], C[1]], color=GOLD, lw=1.6, ls=":", zorder=6)
ax.plot([9.5], [9.5], "o", color=GOLD, ms=6, zorder=9)
ax.text(9.9, 9.1, "midpoint", color=GOLD, fontsize=10, ha="left", va="top",
        zorder=10, bbox=BOX)
ax.text(2.6, 1.2, "$y = x$  is the perpendicular\nbisector of $BC$",
        color=ACC, fontsize=11, ha="center", va="center", zorder=10, bbox=BOX)
ax.set_title("an edge is part of a perpendicular bisector",
             fontsize=11.5, color=INK, pad=8)

# --- (b) vertex は3つの site から等距離
ax = axes[1]
frame(ax)
draw_map(ax, fill=True, lw=1.5, alpha=0.55)
V = (7, 7)
ax.add_patch(Circle(V, 5.0, fill=False, edgecolor=ACC, lw=1.8, ls="--", zorder=6))
for nm in "BCD":
    P = SITES[nm]
    ax.plot([V[0], P[0]], [V[1], P[1]], color=ACC, lw=1.5, zorder=7)
ax.plot([V[0]], [V[1]], "o", color=ACC, ms=8, zorder=9)
ax.text(V[0] - 0.35, V[1] - 0.40, "$(7,7)$", color=ACC, fontsize=11,
        ha="right", va="top", zorder=10, bbox=BOX)
ax.text(4.9, 9.6, "$5$", color=ACC, fontsize=11, ha="center", va="center",
        zorder=10, bbox=BOX)
ax.text(9.6, 7.35, "$5$", color=ACC, fontsize=11, ha="center", va="center",
        zorder=10, bbox=BOX)
ax.text(4.4, 6.6, "$5$", color=ACC, fontsize=11, ha="center", va="center",
        zorder=10, bbox=BOX)
ax.text(6.6, 1.3, "the vertex is the same distance\nfrom $B$, $C$ and $D$",
        color=ACC, fontsize=11, ha="center", va="center", zorder=10, bbox=BOX)
ax.set_title("a vertex is equidistant from three sites",
             fontsize=11.5, color=INK, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-6-edge.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. 一番近い site をさがす ══════════════
fig, ax = plt.subplots(figsize=(8.6, 7.4))
frame(ax)
draw_map(ax, alpha=0.75)
Fm = (10, 3)
ax.plot([Fm[0]], [Fm[1]], "s", color=GREEN, ms=9, zorder=9)
ax.text(Fm[0] - 0.35, Fm[1] + 0.30, "farm $(10,3)$", color=GREEN, fontsize=11,
        ha="right", va="bottom", zorder=10, bbox=BOX)
for nm, col, lwd in (("E", GREEN, 2.4), ("C", GREY, 1.3), ("D", GREY, 1.3)):
    P = SITES[nm]
    ax.plot([Fm[0], P[0]], [Fm[1], P[1]], color=col, lw=lwd, ls="--", zorder=7)
ax.text(10.7, 1.9, r"$\sqrt{8}=2.83$", color=GREEN, fontsize=11, ha="right",
        va="center", zorder=10, bbox=BOX)
ax.text(10.5, 5.6, r"$\sqrt{20}=4.47$", color=GREY, fontsize=10.5, ha="right",
        va="center", zorder=10, bbox=BOX)
ax.text(5.4, 5.2, r"$\sqrt{80}=8.94$", color=GREY, fontsize=10.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(6.4, 1.0, "the farm is in the cell of $E$, so $E$ is nearest",
        color=GREEN, fontsize=11, ha="center", va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-6-nearest.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. site を1つ足す ══════════════
fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.0))
NEW = (9, 10)

ax = axes[0]
frame(ax)
draw_map(ax, alpha=0.75)
ax.plot([NEW[0]], [NEW[1]], "s", color=ACC, ms=9, zorder=9)
ax.text(NEW[0] - 0.32, NEW[1] + 0.28, "$F$", color=ACC, fontsize=12.5,
        ha="right", va="bottom", zorder=10, bbox=BOX)
ax.set_title("before:  $F$ lies inside the cell of $B$",
             fontsize=11.5, color=INK, pad=8)

ax = axes[1]
frame(ax)
S2 = dict(SITES); S2["F"] = NEW
draw_map(ax, sites=S2, alpha=0.75)
polyF = cell(NEW, list(S2.values()))
ax.add_patch(Polygon(polyF, closed=True, facecolor="#fdecea", edgecolor=ACC,
                     lw=2.6, zorder=6))
ax.plot([NEW[0]], [NEW[1]], "s", color=ACC, ms=9, zorder=9)
ax.text(6.4, 1.0, "$F$ takes the nearby part of the\ncells around it",
        color=ACC, fontsize=11, ha="center", va="center", zorder=11, bbox=BOX)
ax.set_title("after:  a new cell appears around $F$",
             fontsize=11.5, color=INK, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-6-addsite.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. toxic waste dump ══════════════
fig, ax = plt.subplots(figsize=(8.6, 7.4))
frame(ax)
draw_map(ax, alpha=0.55, lw=1.5)
from math import hypot, sqrt
info = []
for v in VERTS:
    r = min(hypot(v[0] - p[0], v[1] - p[1]) for p in SITES.values())
    info.append((v, r))
best = max(info, key=lambda t: t[1])
for v, r in info:
    col = ACC if v == best[0] else GREY
    ax.add_patch(Circle(v, r, fill=False, edgecolor=col, lw=2.0 if col == ACC else 1.3,
                        ls="--", zorder=6))
    ax.plot([v[0]], [v[1]], "o", color=col, ms=8 if col == ACC else 6, zorder=9)
lbl = {(4, 10): (-0.4, -0.45, "right", "top", r"$\sqrt{13}=3.61$"),
       (7, 7): (0.45, 0.35, "left", "bottom", r"$5$"),
       (7, 4): (-0.45, -0.45, "right", "top", r"$\sqrt{34}=5.83$")}
for v, r in info:
    dx, dy, ha, va, t = lbl[v]
    col = ACC if v == best[0] else GREY
    ax.text(v[0] + dx, v[1] + dy, t, color=col, fontsize=11, ha=ha, va=va,
            zorder=11, bbox=BOX)
ax.text(3.4, 1.4, "the largest circle wins:\nthe dump goes at $(7,4)$",
        color=ACC, fontsize=11.5, ha="center", va="center", zorder=11, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-6-toxic.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
from math import hypot, sqrt
print("vertices and the distance to the nearest site:")
for v in VERTS:
    ds = sorted((hypot(v[0] - p[0], v[1] - p[1]), n) for n, p in SITES.items())
    print(f"  {v}: nearest {ds[0][1]} at {ds[0][0]:.4f}  (r^2 = {round(ds[0][0]**2)})")
print("cell of C, clipped to the map:", [tuple(round(x, 6) for x in q)
                                         for q in cell(SITES["C"], list(SITES.values()))])
pC = cell(SITES["C"], list(SITES.values()))
area = abs(sum(pC[i][0] * pC[(i + 1) % len(pC)][1] - pC[(i + 1) % len(pC)][0] * pC[i][1]
               for i in range(len(pC)))) / 2
print("area of cell C:", round(area, 6))
print("figures written to", os.path.normpath(OUT))


# ══════════════════════════════════════════════════════════
#  6. nearest neighbour interpolation の具体例
#  7. 例題1〜5 の図（解説の中に置くので背景は透明）
# ══════════════════════════════════════════════════════════
RAIN = {"A": 82, "B": 75, "C": 64, "D": 71, "E": 58}


def we_fig(name, draw, figsize=(6.4, 5.6)):
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


def rain_labels(ax, sites=None):
    sites = sites or SITES
    for nm, p in sites.items():
        if nm in RAIN:
            ax.text(p[0] + 0.30, p[1] - 0.30, f"${RAIN[nm]}$ mm", fontsize=10,
                    color=GOLD, ha="left", va="top", zorder=10, bbox=BOX)


def link(ax, p, q, txt, color=ACC, dx=0.0, dy=0.0, fs=10.5):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=1.8, ls="--", zorder=8)
    ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, txt, color=color,
            fontsize=fs, ha="center", va="center", zorder=11, bbox=BOX)


# ── 6. interpolation の具体例（P は B の cell の中）──────────
def _interp(ax):
    frame(ax)
    draw_map(ax, alpha=0.55, lw=1.6)
    rain_labels(ax)
    P = (8, 10)
    ax.plot([P[0]], [P[1]], "*", color=ACC, ms=17, zorder=10)
    ax.text(P[0] + 0.35, P[1] - 0.15, "$P$", color=ACC, fontsize=12.5,
            ha="left", va="center", zorder=11, bbox=BOX)
    ax.text(6.5, 4.6, "$P$ is inside the cell of $B$,\n"
                      "so the rainfall at $P$ is taken to be $75$ mm",
            color=ACC, fontsize=11, ha="center", va="center", zorder=11,
            bbox=BOX)
    ax.set_title("Nearest neighbour interpolation", fontsize=12, pad=8)


we_fig("sl-3-6-interp.svg", _interp, (6.6, 5.8))


# ── 例題1：vertex $(7,7)$ は B, C, D から等距離 ──────────────
def _w1(ax):
    frame(ax)
    draw_map(ax, alpha=0.45, lw=1.5)
    V = (7, 7)
    ax.add_patch(Circle(V, 5, fill=False, edgecolor=ACC, lw=1.6, ls="--",
                        zorder=6))
    for nm in ("B", "C", "D"):
        link(ax, V, SITES[nm], "$5$", color=ACC)
    ax.plot([V[0]], [V[1]], "o", color=ACC, ms=9, zorder=10)
    ax.text(V[0] + 0.35, V[1] - 0.35, "$V(7,7)$", color=ACC, fontsize=12,
            ha="left", va="top", zorder=11, bbox=BOX)
    ax.text(3.2, 2.4, "three cells meet at $V$", color=ACC, fontsize=11.5,
            ha="center", va="center", zorder=11, bbox=BOX)
    ax.set_title("$V$ is the same distance from $B$, $C$ and $D$",
                 fontsize=12, pad=8)


we_fig("sl-3-6-we1.svg", _w1)


# ── 例題2：2本の edge と、その交点 ───────────────────────────
def _w2(ax):
    frame(ax)
    draw_map(ax, alpha=0.35, lw=1.2)
    ax.plot([LO, HI], [LO, HI], color=ACC, lw=2.6, zorder=8)      # y = x
    ax.plot([1.0, HI], [13.0, 1.0], color=GREEN, lw=2.6, zorder=8)  # y = -x+14
    ax.text(12.4, 10.7, "$y = x$", color=ACC, fontsize=12, ha="center",
            va="center", zorder=11, bbox=BOX)
    ax.text(2.7, 10.2, "$y = -x + 14$", color=GREEN, fontsize=12, ha="center",
            va="center", zorder=11, bbox=BOX)
    ax.text(10.2, 8.3, "edge of $B$ and $C$", color=ACC, fontsize=10,
            ha="center", va="center", zorder=11, bbox=BOX)
    ax.text(3.6, 8.5, "edge of $B$ and $D$", color=GREEN, fontsize=10,
            ha="center", va="center", zorder=11, bbox=BOX)
    ax.plot([7], [7], "o", color=INK, ms=9, zorder=10)
    ax.text(7.4, 6.6, "$(7,7)$", color=INK, fontsize=12, ha="left", va="top",
            zorder=11, bbox=BOX)
    ax.text(6.6, 2.6, "the two edges cross at the vertex", color=INK,
            fontsize=11, ha="center", va="center", zorder=11, bbox=BOX)
    ax.set_title("Two perpendicular bisectors, and where they meet",
                 fontsize=12, pad=8)


we_fig("sl-3-6-we2.svg", _w2)


# ── 例題3：農場 $(10,3)$ と、C・D・E までの距離 ────────────────
def _w3(ax):
    frame(ax)
    draw_map(ax, alpha=0.55, lw=1.6)
    rain_labels(ax)
    F = (10, 3)
    link(ax, F, SITES["C"], r"$\sqrt{20}=4.47$", color=GREY, dx=-1.55, dy=0.55)
    link(ax, F, SITES["D"], r"$\sqrt{80}=8.94$", color=GREY, dx=-0.4, dy=0.95)
    link(ax, F, SITES["E"], r"$\sqrt{8}=2.83$", color=ACC, dx=-1.85, dy=-0.35)
    ax.plot([F[0]], [F[1]], "*", color=ACC, ms=17, zorder=10)
    ax.text(F[0] + 0.35, F[1] + 0.45, "farm $(10,3)$", color=ACC, fontsize=11,
            ha="left", va="bottom", zorder=11, bbox=BOX)
    ax.text(3.6, 1.6, "the farm is inside\nthe cell of $E$", color=ACC,
            fontsize=11, ha="center", va="center", zorder=11, bbox=BOX)
    ax.set_title("Which village is nearest to the farm?", fontsize=12, pad=8)


we_fig("sl-3-6-we3.svg", _w3, (6.6, 5.8))


# ── 例題4：F を足したあとの、B と F の edge ────────────────────
def _w4(ax):
    frame(ax)
    S2 = dict(SITES); S2["F"] = (9, 10)
    draw_map(ax, sites=S2, alpha=0.45, lw=1.4)
    # 直線 y = x + 3 は薄い点線で、そのうち実際に edge になっている
    # 部分（B と F からの距離が等しい辺）だけを太い実線にする
    ax.plot([LO, 10.0], [3.0, 13.0], color=ACC, lw=1.3, ls=":", zorder=7)
    polyF = cell((9, 10), list(S2.values()))
    Bp, Fp = SITES["B"], (9, 10)

    def eqd(q):
        return abs(hypot(q[0] - Bp[0], q[1] - Bp[1])
                   - hypot(q[0] - Fp[0], q[1] - Fp[1])) < 1e-7
    for i in range(len(polyF)):
        P0, P1 = polyF[i], polyF[(i + 1) % len(polyF)]
        if eqd(P0) and eqd(P1):
            ax.plot([P0[0], P1[0]], [P0[1], P1[1]], color=ACC, lw=3.2,
                    zorder=9)
    ax.text(2.6, 6.6, "$y = x + 3$", color=ACC, fontsize=12, ha="center",
            va="center", zorder=11, bbox=BOX)
    ax.text(5.0, 10.4, "the edge of $B$ and $F$", color=ACC, fontsize=10,
            ha="center", va="center", zorder=11, bbox=BOX)
    ax.plot([8], [11], "o", color=ACC, ms=8, zorder=10)
    ax.text(7.6, 11.35, "midpoint $(8,11)$", color=ACC, fontsize=10,
            ha="right", va="bottom", zorder=11, bbox=BOX)
    ax.plot([SITES["B"][0], 9], [SITES["B"][1], 10], color=GREY, lw=1.5,
            ls="--", zorder=7)
    ax.plot([9], [10], "s", color=ACC, ms=9, zorder=10)
    ax.text(9.35, 9.75, "$F(9,10)$", color=ACC, fontsize=12, ha="left",
            va="top", zorder=11, bbox=BOX)
    ax.text(4.0, 2.2, "the edge is the perpendicular\n"
                      "bisector of $BF$",
            color=ACC, fontsize=11, ha="center", va="center", zorder=11,
            bbox=BOX)
    ax.set_title("After the new village $F$ is added", fontsize=12, pad=8)


we_fig("sl-3-6-we4.svg", _w4)


# ── 例題5：3つの vertex を比べる ──────────────────────────────
def _w5(ax):
    frame(ax)
    draw_map(ax, alpha=0.40, lw=1.3)
    info = [((4, 10), 13 ** 0.5, "from $A$, $B$, $D$", r"$\sqrt{13}=3.61$"),
            ((7, 7), 5.0, "from $B$, $C$, $D$", r"$5$"),
            ((7, 4), 34 ** 0.5, "from $C$, $D$, $E$", r"$\sqrt{34}=5.83$")]
    best = max(info, key=lambda t: t[1])[0]
    for v, r, who, txt in info:
        col = ACC if v == best else GREY
        ax.add_patch(Circle(v, r, fill=False, edgecolor=col, ls="--",
                            lw=2.2 if v == best else 1.2, zorder=6))
        ax.plot([v[0]], [v[1]], "o", color=col, ms=9 if v == best else 6,
                zorder=10)
    ax.text(3.4, 10.5, r"$\sqrt{13}=3.61$" + "\nfrom $A$, $B$, $D$", color=GREY,
            fontsize=10, ha="right", va="center", zorder=11, bbox=BOX)
    ax.text(7.5, 7.9, "$5$\nfrom $B$, $C$, $D$", color=GREY, fontsize=10,
            ha="left", va="center", zorder=11, bbox=BOX)
    ax.text(6.3, 3.2, r"$\sqrt{34}=5.83$" + "\nfrom $C$, $D$, $E$", color=ACC,
            fontsize=10.5, ha="right", va="center", zorder=11, bbox=BOX)
    ax.set_title("The biggest circle wins:  the dump goes at $(7,4)$",
                 fontsize=12, pad=8, color=ACC)


we_fig("sl-3-6-we5.svg", _w5)

print("wrote sl-3-6-interp.svg, sl-3-6-we1..we5.svg")
print("check P(8,10):", sorted((round(hypot(8 - p[0], 10 - p[1]), 3), n)
                               for n, p in SITES.items())[:2])


# ══════════════ 8. Exercises の前に置く、素の地図 ══════════════
fig, ax = plt.subplots(figsize=(7.2, 6.4))
frame(ax)
draw_map(ax, alpha=0.55, lw=1.7, labels=False)

SLBL = {"A": (0.36, 0.34, "left", "bottom"),
        "B": (0.36, 0.34, "left", "bottom"),
        "C": (-0.36, 0.34, "right", "bottom"),
        "D": (0.36, 0.34, "left", "bottom"),
        "E": (-0.36, 0.34, "right", "bottom")}
for nm, p in SITES.items():
    dx, dy, ha, va = SLBL[nm]
    ax.text(p[0] + dx, p[1] + dy, f"${nm}({p[0]},{p[1]})$", fontsize=11.5,
            color=INK, ha=ha, va=va, zorder=11, bbox=BOX)

VLBL = {(4, 10): (-0.36, 0.30, "right", "bottom"),
        (7, 7): (0.40, -0.34, "left", "top"),
        (7, 4): (-0.40, -0.34, "right", "top")}
for v in VERTS:
    dx, dy, ha, va = VLBL[v]
    ax.plot([v[0]], [v[1]], "o", color=ACC, ms=8, zorder=9)
    ax.text(v[0] + dx, v[1] + dy, f"$({v[0]},{v[1]})$", color=ACC,
            fontsize=10.5, ha=ha, va=va, zorder=11, bbox=BOX)

ax.text(3.6, 2.2, "villages: black\nvertices: red", fontsize=10.5, color=GREY,
        ha="center", va="center", zorder=11, bbox=BOX)
ax.set_title("The map used in these exercises   ($1$ square $= 1$ km)",
             fontsize=12, pad=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-3-6-map.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote sl-3-6-map.svg")
