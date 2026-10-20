"""AA HL 5.17（y 軸とのあいだの面積・回転体の体積）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_17.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_17.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-17-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-17-idea-b.svg
      aa-hl/05-calculus/img/aahl-5-17-idea-c.svg
      aa-hl/05-calculus/img/aahl-5-17-idea-d.svg

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
ax2.set_xlim(-0.45, 4.6)
ax2.set_ylim(-3.1, 2.6)
ax2.plot([-0.2, 4.2], [0, 0], color=GREY, linewidth=0.9, zorder=2)
ax2.set_xticks([])
ax2.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax2.spines[_s].set_visible(False)


# ══════════════════════════════════════════════════════════
# (c) y 軸まわりの回転体：厚さ dy、半径 x の円板
# ══════════════════════════════════════════════════════════
fig3, ax3 = plt.subplots(figsize=(4.6, 4.0))

yv = np.linspace(0.0, 4.0, 300)
xv = 0.35 + 0.45 * yv
ax3.plot(xv, yv, color=ACCENT, linewidth=2.0, zorder=4)
ax3.plot(-xv, yv, color=GREY, linewidth=1.2, linestyle=(0, (4, 3)), zorder=3)
ax3.add_patch(Polygon(list(zip(xv, yv)) + list(zip(-xv[::-1], yv[::-1])),
                      closed=True, facecolor=SHADE, edgecolor="none",
                      zorder=1))
_yd, _h = 2.2, 0.22
_rx = 0.35 + 0.45 * _yd
ax3.add_patch(Rectangle((-_rx, _yd), 2 * _rx, _h, facecolor="white",
                        edgecolor=WARM, linewidth=1.5, zorder=5))
ax3.add_patch(Ellipse((0, _yd + _h), 2 * _rx, 0.30, facecolor="white",
                      edgecolor=WARM, linewidth=1.5, zorder=6))
ax3.annotate("", xy=(_rx, _yd + _h + 0.02), xytext=(0, _yd + _h + 0.02),
             zorder=8,
             arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.4))
ax3.text(_rx / 2 - 0.08, _yd + _h + 0.22, "$x$", fontsize=11, color=INK)
ax3.text(_rx + 0.12, _yd - 0.02, "$dy$", fontsize=10.5, color=WARM)
ax3.text(1.75, 2.75, "$x = g(y)$", fontsize=10.5, color=ACCENT)
ax3.plot([0, 0], [-0.3, 4.5], color=GREY, linewidth=0.9, zorder=2)
ax3.text(0.08, 4.4, "$y$", fontsize=10.5, color=GREY)
ax3.set_xlim(-2.5, 2.7)
ax3.set_ylim(-0.4, 4.7)
ax3.set_aspect("equal")
ax3.set_xticks([])
ax3.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax3.spines[_s].set_visible(False)

# ══════════════════════════════════════════════════════════
# (d) 2 曲線のあいだを回す：中が空いた円板（外側の円 − 内側の円）
# ══════════════════════════════════════════════════════════
fig4, ax4 = plt.subplots(figsize=(5.8, 3.6))

t4 = np.linspace(0.2, 3.6, 300)
fo = 1.2 + 0.35 * t4
fi = 0.25 + 0.20 * t4
ax4.plot(t4, fo, color=ACCENT, linewidth=2.0, zorder=4)
ax4.plot(t4, fi, color=WARM, linewidth=2.0, zorder=4)
ax4.plot(t4, -fo, color=GREY, linewidth=1.1, linestyle=(0, (4, 3)), zorder=3)
ax4.plot(t4, -fi, color=GREY, linewidth=1.1, linestyle=(0, (4, 3)), zorder=3)
for _sg in (1, -1):
    ax4.add_patch(Polygon(list(zip(t4, _sg * fo)) + list(zip(t4[::-1], _sg * fi[::-1])),
                          closed=True, facecolor=SHADE, edgecolor="none",
                          zorder=1))
_x4 = 2.4
_ro = 1.2 + 0.35 * _x4
_ri = 0.25 + 0.20 * _x4
ax4.add_patch(Ellipse((_x4, 0), 0.42, 2 * _ro, facecolor="#bfdbfe",
                      edgecolor=INK, linewidth=1.4, zorder=6))
ax4.add_patch(Ellipse((_x4, 0), 0.42 * _ri / _ro, 2 * _ri, facecolor="white",
                      edgecolor=INK, linewidth=1.2, zorder=7))
ax4.annotate("", xy=(_x4 + 0.03, _ro), xytext=(_x4 + 0.03, 0), zorder=9,
             arrowprops=dict(arrowstyle="-|>", color=ACCENT, linewidth=1.4))
ax4.annotate("", xy=(_x4 - 0.03, -_ri), xytext=(_x4 - 0.03, 0), zorder=9,
             arrowprops=dict(arrowstyle="-|>", color=WARM, linewidth=1.4))
ax4.text(_x4 + 0.32, _ro / 2 + 0.35, "$y_{\\mathrm{outer}}$", fontsize=11,
         color=ACCENT)
ax4.text(_x4 + 0.32, -_ri / 2 - 0.15, "$y_{\\mathrm{inner}}$", fontsize=11,
         color=WARM)
ax4.plot([-0.2, 4.2], [0, 0], color=GREY, linewidth=0.9, zorder=2)
ax4.text(4.25, -0.1, "$x$", fontsize=10.5, color=GREY)
ax4.set_xlim(-0.3, 4.6)
ax4.set_ylim(-2.7, 2.7)
ax4.set_xticks([])
ax4.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax4.spines[_s].set_visible(False)

for _fig, _name in ((fig1, "a"), (fig2, "b"), (fig3, "c"), (fig4, "d")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-17-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-17-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
