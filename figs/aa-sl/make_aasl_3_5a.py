"""AA SL 3.5a の図をつくる。

    python3 figs/aa-sl/make_aasl_3_5a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_5a.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-5a-idea.svg

(a) 単位円の定義。P の座標が (cos θ, sin θ)。
(b) 4 つの象限の符号と、折り返しでできる 3 つの点。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（角は θ で書く）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 5.1))

t = np.linspace(0, 2 * np.pi, 400)

# ══════════════════════════════════════════════════════════
# (a) 単位円の定義
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The unit circle", fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(-1.55, 1.95)
ax1.set_ylim(-1.45, 1.75)
ax1.set_aspect("equal")
ax1.axis("off")

ax1.annotate("", xy=(1.55, 0), xytext=(-1.35, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 1.45), xytext=(0, -1.35),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(1.60, -0.16, "$x$", fontsize=11, color=GREY)
ax1.text(0.08, 1.46, "$y$", fontsize=11, color=GREY)

ax1.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.2)

th = 1.05
Px, Py = np.cos(th), np.sin(th)
ax1.plot([0, Px], [0, Py], color=ACCENT, linewidth=2.2)
ax1.plot([Px, Px], [0, Py], color=WARM, linewidth=1.8, linestyle=(0, (5, 3)))
ax1.plot([0, Px], [0, 0], color=GREEN, linewidth=2.6, solid_capstyle="butt")
ax1.plot([Px], [Py], marker="o", markersize=5.5, color=INK, zorder=3)

ta = np.linspace(0, th, 60)
ax1.plot(0.27 * np.cos(ta), 0.27 * np.sin(ta), color=INK, linewidth=1.3)
ax1.text(0.31, 0.11, "$\\theta$", fontsize=12, color=INK)

ax1.text(Px + 0.07, Py + 0.07, "$P(\\cos\\theta,\\ \\sin\\theta)$", fontsize=11,
         color=INK)
ax1.text(Px * 0.42 - 0.06, -0.27, "$\\cos\\theta$", fontsize=10.5, color=GREEN)
ax1.text(Px + 0.10, Py * 0.45, "$\\sin\\theta$", fontsize=10.5, color=WARM)
ax1.text(1.06, -0.20, "$1$", fontsize=10.5, color=GREY)
ax1.plot([1], [0], marker="o", markersize=4, color=GREY, zorder=3)

ax1.text(-1.55, -1.38, "the radius is $1$, so the coordinates of $P$ are the "
         "cosine and the sine", fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 象限の符号と、折り返し
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Signs, and reflections", fontsize=11, color=INK, loc="left",
              pad=10)
ax2.set_xlim(-1.75, 1.75)
ax2.set_ylim(-1.45, 1.75)
ax2.set_aspect("equal")
ax2.axis("off")

ax2.annotate("", xy=(1.5, 0), xytext=(-1.5, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 1.45), xytext=(0, -1.35),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.0)

ax2.text(0.46, 0.14, "all $> 0$", fontsize=9.5, color=GREEN)
ax2.text(-1.16, 0.14, "$\\sin\\theta > 0$", fontsize=9.5, color=GREEN)
ax2.text(-1.16, -0.34, "$\\tan\\theta > 0$", fontsize=9.5, color=GREEN)
ax2.text(0.46, -0.34, "$\\cos\\theta > 0$", fontsize=9.5, color=GREEN)

for _x, _y, _lab, _col, _ha in [
        (np.cos(th), np.sin(th), "$\\theta$", ACCENT, "left"),
        (-np.cos(th), np.sin(th), "$\\pi-\\theta$", WARM, "right"),
        (-np.cos(th), -np.sin(th), "$\\pi+\\theta$", WARM, "right"),
        (np.cos(th), -np.sin(th), "$-\\theta$", WARM, "left")]:
    ax2.plot([0, _x], [0, _y], color=_col, linewidth=1.6)
    ax2.plot([_x], [_y], marker="o", markersize=4.8, color=_col, zorder=3)
    ax2.text(_x * 1.14 + (0.06 if _x > 0 else -0.06), _y * 1.14 - 0.06, _lab,
             fontsize=11, color=_col, ha=_ha)

ax2.text(-1.75, -1.38, "the four points are reflections of one another in the "
         "axes", fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-3-5a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
