"""AI HL の行列まわりの図で共通に使う道具。
   ★ matplotlib の mathtext は pmatrix / array を扱えないので、
     行列は【線と文字で手描き】する。この関数群がその土台。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, GOLD, FILL = "#7a8592", "#b9770e", "#eaf2fb"
BOX = dict(facecolor="white", edgecolor="none", pad=1.8, alpha=0.94)

plt.rcParams.update({"font.size": 11, "text.color": INK, "svg.fonttype": "path"})


def blank(ax, xlim=(0, 1), ylim=(0, 1)):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def matrix(ax, cx, cy, rows, cw=0.62, ch=0.46, fs=13, color=INK,
           bracket=INK, lw=1.8, cell_color=None, weight="normal"):
    """(cx, cy) を中心に行列を描き、各セルの中心座標を返す。

    rows       … [["1","2"],["3","4"]] のような文字列の二次元リスト
    cell_color … {(r, c): "#..."} で個別に色を変えられる
    """
    nr, nc = len(rows), len(rows[0])
    w, h = nc * cw, nr * ch
    x0, y0 = cx - w / 2, cy - h / 2
    ear = cw * 0.20
    for sx, d in ((x0, +1), (x0 + w, -1)):
        ax.plot([sx, sx], [y0, y0 + h], color=bracket, lw=lw,
                solid_capstyle="round", zorder=5)
        for yy in (y0, y0 + h):
            ax.plot([sx, sx + d * ear], [yy, yy], color=bracket, lw=lw,
                    solid_capstyle="round", zorder=5)
    centres = {}
    for r in range(nr):
        for c in range(nc):
            X = x0 + (c + 0.5) * cw
            Y = y0 + h - (r + 0.5) * ch
            centres[(r, c)] = (X, Y)
            col = (cell_color or {}).get((r, c), color)
            ax.text(X, Y, rows[r][c], fontsize=fs, ha="center", va="center",
                    color=col, zorder=6, weight=weight)
    return centres, (x0, y0, w, h)


def label(ax, x, y, text, color=INK, fs=11.5, ha="center", va="center",
          box=True, weight="normal"):
    ax.text(x, y, text, fontsize=fs, ha=ha, va=va, color=color, zorder=10,
            weight=weight, bbox=BOX if box else None)


def arrow(ax, xy_from, xy_to, color=INK, lw=1.6, style="-|>", rad=0.0,
          scale=13):
    ax.annotate("", xy=xy_to, xytext=xy_from,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=scale,
                                connectionstyle=f"arc3,rad={rad}"),
                zorder=7)
