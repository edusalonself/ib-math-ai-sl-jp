"""AI HL の graph theory（AHL 3.14 / 3.15 / 3.16）の図で共通に使う道具。
   ラベルはすべて英語。日本語のグリフは matplotlib に無いので使わない。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, GOLD, FILL = "#7a8592", "#b9770e", "#eaf2fb"
BOX = dict(facecolor="white", edgecolor="none", pad=1.8, alpha=0.94)

plt.rcParams.update({"font.size": 11, "text.color": INK, "svg.fonttype": "path"})

R = 0.30          # 頂点の丸の半径


def board(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def node(ax, p, name, color=LINE, fc="white", fs=12, r=R, z=10, tc=None):
    ax.add_patch(Circle(p, r, fc=fc, ec=color, lw=2.0, zorder=z))
    ax.text(p[0], p[1], name, fontsize=fs, ha="center", va="center",
            color=tc or color, zorder=z + 1, weight="bold")


def _trim(p, q, r=R):
    """円の縁で線を止めるための端点。"""
    p, q = np.array(p, float), np.array(q, float)
    d = q - p
    L = np.hypot(*d)
    if L < 1e-9:
        return p, q
    u = d / L
    return p + u * r, q - u * r


def edge(ax, p, q, color=GREY, lw=2.0, z=3, ls="-", r=R, rad=0.0):
    a, b = _trim(p, q, r)
    if abs(rad) < 1e-9:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, ls=ls,
                zorder=z, solid_capstyle="round")
    else:
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-", lw=lw, color=color,
                                     zorder=z,
                                     connectionstyle=f"arc3,rad={rad}"))


def arc_edge(ax, p, q, color=GREY, lw=2.0, z=3, r=R, rad=0.25, arrow=True):
    """有向辺。arrow=False なら曲がった無向辺。"""
    a, b = _trim(p, q, r)
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>" if arrow else "-",
                                 mutation_scale=15, lw=lw, color=color,
                                 zorder=z,
                                 connectionstyle=f"arc3,rad={rad}"))


def loop(ax, p, color=GREY, lw=2.0, z=3, r=R, size=0.42, angle=90):
    """自己ループ。"""
    th = np.radians(angle)
    c = (p[0] + size * np.cos(th), p[1] + size * np.sin(th))
    ax.add_patch(Circle(c, size, fc="none", ec=color, lw=lw, zorder=z))


def wlabel(ax, p, q, text, color=GOLD, fs=11, off=0.0, dy=0.0, box=True,
           t=0.5):
    """辺の上にラベル（重みなど）。t=0.5 で中点、0 に寄せると p 側。"""
    mx, my = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
    dx, dyy = q[0] - p[0], q[1] - p[1]
    L = np.hypot(dx, dyy) or 1.0
    nx, ny = -dyy / L, dx / L
    ax.text(mx + nx * off, my + ny * off + dy, text, fontsize=fs, ha="center",
            va="center", color=color, zorder=12,
            bbox=BOX if box else None)


def note(ax, x, y, text, color=INK, fs=11.5, ha="center", va="center",
         box=True, weight="normal"):
    ax.text(x, y, text, fontsize=fs, ha=ha, va=va, color=color, zorder=13,
            weight=weight, bbox=BOX if box else None)


def ring(n, cx=0.0, cy=0.0, rad=1.6, start=90):
    """n 個の頂点を円周上に並べた座標を返す。"""
    out = []
    for i in range(n):
        th = np.radians(start + 360 * i / n)
        out.append((cx + rad * np.cos(th), cy + rad * np.sin(th)))
    return out
