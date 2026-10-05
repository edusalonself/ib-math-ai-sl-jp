"""AA HL 5.17（y 軸とのあいだの面積・回転体の体積）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_17.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_17.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-17-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-17-idea-b.svg

(a) y 軸とのあいだの面積：よこ長の細い長方形を積む。
(b) 回転体：厚さ dx、半径 y の円板を積む。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → 使わない
  * \\lvert \\rvert も読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
SHADE = "#dbeafe"

# ══════════════════════════════════════════════════════════
# (a) y 軸とのあいだの面積
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.0, 3.8))
ax1.set_title("area between a curve and the $y$-axis: horizontal strips",
              fontsize=10.2, color=INK, loc="left", pad=10)

yy = np.linspace(0, 4.0, 300)
xx = np.sqrt(yy)
ax1.fill_betweenx(yy, 0, xx, color=SHADE, zorder=1)
ax1.plot(xx, yy, color=ACCENT, linewidth=2.0, zorder=3)
_y0, _dy = 2.3, 0.34
ax1.add_patch(Rectangle((0, _y0), float(np.sqrt(_y0)), _dy,
                        facecolor="none", edgecolor=WARM, linewidth=1.6,
                        zorder=4))
ax1.annotate("", xy=(float(np.sqrt(_y0)), _y0 - 0.30), xytext=(0, _y0 - 0.30),
             arrowprops=dict(arrowstyle="<|-|>", color=GREY, linewidth=1.1))
ax1.text(float(np.sqrt(_y0)) / 2 - 0.06, _y0 - 0.66, "$x$", fontsize=11,
         color=GREY)
ax1.text(float(np.sqrt(_y0)) + 0.14, _y0 + 0.06, "$dy$", fontsize=10.5,
         color=WARM)
ax1.text(0.45, 3.30, "$x = g(y)$", fontsize=10.5, color=ACCENT)
ax1.text(-0.42, 4.05, "$b$", fontsize=10.5, color=INK)
ax1.text(-0.42, -0.12, "$a$", fontsize=10.5, color=INK)
ax1.plot([-0.08, 0.08], [4.0, 4.0], color=INK, linewidth=1.2, zorder=4)
ax1.text(-0.35, -1.25, "each strip has area $x\\,dy$, so"
         " $A = \\int_{a}^{b} x\\,dy$", fontsize=9.5, color=GREY)
ax1.set_xlim(-0.75, 3.0)
ax1.set_ylim(-1.7, 4.7)
ax1.plot([-0.3, 2.6], [0, 0], color=GREY, linewidth=0.9, zorder=0)
ax1.plot([0, 0], [-0.4, 4.4], color=GREY, linewidth=0.9, zorder=0)
ax1.set_xticks([])
ax1.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax1.spines[_s].set_visible(False)

# ══════════════════════════════════════════════════════════
# (b) 回転体
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 3.4))
ax2.set_title("rotating about the $x$-axis: a stack of circular discs",
              fontsize=10.2, color=INK, loc="left", pad=10)

t = np.linspace(0.15, 3.6, 300)
f = 0.55 + 0.42 * t
ax2.plot(t, f, color=ACCENT, linewidth=2.0, zorder=4)
ax2.plot(t, -f, color=GREY, linewidth=1.2, linestyle=(0, (4, 3)), zorder=3)
ax2.add_patch(Polygon(list(zip(t, f)) + list(zip(t[::-1], -f[::-1])),
                      closed=True, facecolor=SHADE, edgecolor="none",
                      zorder=1))
_xd, _w = 2.3, 0.22
_r = 0.55 + 0.42 * _xd
ax2.add_patch(Rectangle((_xd, -_r), _w, 2 * _r, facecolor="white",
                        edgecolor=WARM, linewidth=1.5, zorder=5))
ax2.add_patch(Ellipse((_xd + _w, 0), 0.30, 2 * _r, facecolor="white",
                      edgecolor=WARM, linewidth=1.5, zorder=6))
ax2.annotate("", xy=(_xd + _w + 0.02, _r), xytext=(_xd + _w + 0.02, 0),
             zorder=8,
             arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.4))
ax2.text(_xd + _w + 0.14, _r / 2, "$y$", fontsize=11, color=INK)
ax2.text(_xd - 0.02, -_r - 0.44, "$dx$", fontsize=10.5, color=WARM)
ax2.text(0.35, 2.05, "$y = f(x)$", fontsize=10.5, color=ACCENT)
ax2.text(-0.25, -2.55, "each disc has volume $\\pi y^{2}\\,dx$, so"
         " $V = \\int_{a}^{b} \\pi y^{2}\\,dx$", fontsize=9.5, color=GREY)
ax2.set_xlim(-0.45, 4.6)
ax2.set_ylim(-3.1, 2.6)
ax2.plot([-0.2, 4.2], [0, 0], color=GREY, linewidth=0.9, zorder=2)
ax2.set_xticks([])
ax2.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax2.spines[_s].set_visible(False)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-17-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-17-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
