"""AA SL 3.7b の図をつくる。

    python3 figs/aa-sl/make_aasl_3_7b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_7b.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-7b-idea-a.svg
      aa-sl/03-geometry/img/aasl-3-7b-idea-b.svg
      aa-sl/03-geometry/img/aasl-3-7b-idea-c.svg
      aa-sl/03-geometry/img/aasl-3-7b-idea-d.svg

(a) y = sin x と y = 3 sin 2x。縦に 3 倍、横に 1/2 倍。
(b) y = a sin(b(x+c)) + d の 4 つの数が、グラフのどこに出るか。
(c) 数の入った例。h = 4 sin(pi/6 (t-3)) + 6 の潮の高さ。
(d) 第 6 節で読み取った例 y = 3 sin(2x - pi/2) + 4。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（(b) は文字のまま）。
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

fig1, ax1 = plt.subplots(figsize=(5.4, 4.6))
fig2, ax2 = plt.subplots(figsize=(5.4, 4.6))
fig3, ax3 = plt.subplots(figsize=(6.4, 4.3))
fig4, ax4 = plt.subplots(figsize=(6.2, 4.2))
# ══════════════════════════════════════════════════════════
# (a) 縦に伸ばし、横に縮める
# ══════════════════════════════════════════════════════════
ax1.set_title("A stretch in each direction", fontsize=11, color=INK,
              loc="left", pad=10)
x = np.linspace(0, 2 * np.pi, 600)
ax1.plot(x, np.sin(x), color=GREY, linewidth=1.8, linestyle=(0, (6, 3)),
         label="$y = \\sin x$")
ax1.plot(x, 3 * np.sin(2 * x), color=ACCENT, linewidth=2.2,
         label="$y = 3\\sin 2x$")
ax1.axhline(0, color=GREY, linewidth=1.0)
ax1.set_xlim(-0.3, 2 * np.pi + 0.3)
ax1.set_ylim(-4.0, 5.6)
ax1.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax1.set_xticklabels(["$0$", "$\\frac{\\pi}{2}$", "$\\pi$", "$\\frac{3\\pi}{2}$",
                     "$2\\pi$"], fontsize=9.5)
ax1.set_yticks([-3, -1, 0, 1, 3])
ax1.set_yticklabels(["$-3$", "$-1$", "$0$", "$1$", "$3$"], fontsize=9.5)
for _sp in ("top", "right", "left", "bottom"):
    ax1.spines[_sp].set_visible(False)
ax1.tick_params(length=0, colors=GREY)
ax1.legend(loc="upper right", frameon=False, fontsize=10)

# ══════════════════════════════════════════════════════════
# (b) 4 つの数がどこに出るか
# ══════════════════════════════════════════════════════════
ax2.set_title("Where $a$, $b$, $c$ and $d$ show up", fontsize=11, color=INK,
              loc="left", pad=10)
A, D, SH = 2.0, 3.0, 0.7
xx = np.linspace(-0.6, 7.2, 700)
yy = A * np.sin(xx - SH) + D
ax2.plot(xx, yy, color=ACCENT, linewidth=2.2)
ax2.axhline(D, color=GREEN, linewidth=1.2, linestyle=(0, (5, 4)))
ax2.set_xlim(-0.9, 8.9)
ax2.set_ylim(-0.4, 6.7)
ax2.set_xticks([])
ax2.set_yticks([])
for _sp in ("top", "right", "left", "bottom"):
    ax2.spines[_sp].set_visible(False)

_top = SH + np.pi / 2
_bot = SH + 3 * np.pi / 2
ax2.annotate("", xy=(_top, D + A), xytext=(_top, D),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.3))
ax2.text(_top + 0.14, D + A / 2 - 0.12, "$|a|$", fontsize=11, color=WARM)
ax2.annotate("", xy=(SH + 2 * np.pi, 0.30), xytext=(SH, 0.30),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.3))
ax2.text((2 * SH + 2 * np.pi) / 2 - 0.62, 0.62,
         "one period $= \\frac{2\\pi}{|b|}$", fontsize=10, color=WARM)
ax2.text(7.30, D + 0.30, "midline $y = d$", fontsize=10, color=GREEN)
ax2.annotate("", xy=(SH, D), xytext=(0, D),
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.3))
ax2.text(-0.85, D + 0.34, "shift by $c$", fontsize=10, color=INK)
ax2.plot([SH], [D], marker="o", markersize=5.0, color=INK, zorder=3)


# ══════════════════════════════════════════════════════════
# (c) 数の入った例：潮の高さ
# ══════════════════════════════════════════════════════════
ax3.set_title(r"$h = 4\sin\left(\frac{\pi}{6}(t-3)\right) + 6$",
              fontsize=12, color=INK, loc="left", pad=12)
_t3 = np.linspace(0, 24, 600)
_h3 = 4 * np.sin(np.pi / 6 * (_t3 - 3)) + 6
ax3.plot(_t3, _h3, color=ACCENT, linewidth=2.4)
ax3.axhline(6, color=GREEN, linewidth=1.4, linestyle=(0, (5, 3)))
ax3.set_xlim(-1.2, 27.5)
ax3.set_ylim(-0.6, 12.2)
ax3.set_xticks([0, 6, 12, 18, 24])
ax3.set_yticks([2, 6, 10])
ax3.tick_params(length=0, colors=GREY)
for _sp in ("top", "right", "left"):
    ax3.spines[_sp].set_visible(False)
ax3.spines["bottom"].set_color(GREY)

for _tp in (6, 18):
    ax3.plot([_tp], [10], marker="o", markersize=5.5, color=ACCENT, zorder=3)
    ax3.text(_tp, 10.5, "$(%d,\\ 10)$" % _tp, fontsize=10, color=ACCENT,
             ha="center")
for _tp in (0, 12, 24):
    ax3.plot([_tp], [2], marker="o", markersize=5.5, color=WARM, zorder=3)
ax3.text(12, 1.0, "$(12,\\ 2)$", fontsize=10, color=WARM, ha="center")

ax3.annotate("", xy=(3.0, 10), xytext=(3.0, 6),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.3))
ax3.text(3.35, 7.8, "$4$", fontsize=11, color=WARM)
ax3.annotate("", xy=(18, 11.5), xytext=(6, 11.5),
             arrowprops=dict(arrowstyle="<->", color=INK, linewidth=1.3))
ax3.text(12, 11.7, "$12$ h", fontsize=10.5, color=INK, ha="center")
ax3.text(24.9, 6.35, "$h = 6$", fontsize=10.5, color=GREEN, va="bottom")
ax3.text(26.6, -0.35, "$t$ (h)", fontsize=10.5, color=GREY, ha="right")
ax3.text(-1.1, 11.9, "$h$ (m)", fontsize=10.5, color=GREY, va="top")


# ══════════════════════════════════════════════════════════
# (d) 第 6 節で読み取った例
# ══════════════════════════════════════════════════════════
ax4.set_title(r"$y = 3\sin\left(2x - \frac{\pi}{2}\right) + 4$",
              fontsize=12, color=INK, loc="left", pad=12)
_x4 = np.linspace(0, 2 * np.pi, 700)
_y4 = 3 * np.sin(2 * _x4 - np.pi / 2) + 4
ax4.plot(_x4, _y4, color=ACCENT, linewidth=2.4)
ax4.plot([-0.35, 2 * np.pi], [4, 4], color=GREEN, linewidth=1.4,
         linestyle=(0, (5, 3)))
ax4.set_xlim(-0.35, 2 * np.pi + 1.95)
ax4.set_ylim(-0.05, 9.2)
ax4.set_xticks([0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax4.set_xticklabels(["$0$", "$\\frac{\\pi}{4}$", "$\\frac{\\pi}{2}$",
                     "$\\pi$", "$\\frac{3\\pi}{2}$", "$2\\pi$"], fontsize=9.5)
ax4.set_yticks([1, 4, 7])
ax4.set_yticklabels(["$1$", "$4$", "$7$"], fontsize=9.5)
ax4.tick_params(length=0, colors=GREY)
for _sp in ("top", "right", "left"):
    ax4.spines[_sp].set_visible(False)
ax4.spines["bottom"].set_color(GREY)

ax4.plot([np.pi / 2], [7], marker="o", markersize=5.5, color=ACCENT, zorder=3)
ax4.text(np.pi / 2 + 0.12, 7.25, "maximum $7$", fontsize=10, color=ACCENT)
ax4.plot([np.pi], [1], marker="o", markersize=5.5, color=WARM, zorder=3)
ax4.text(np.pi + 0.16, 0.55, "minimum $1$", fontsize=10, color=WARM)
ax4.plot([np.pi / 4], [4], marker="o", markersize=5.0, color=INK, zorder=3)

ax4.annotate("", xy=(np.pi / 2, 7), xytext=(np.pi / 2, 4),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.3))
ax4.text(np.pi / 2 + 0.16, 5.3, "$3$", fontsize=11, color=WARM,
         ha="left")
ax4.annotate("", xy=(5 * np.pi / 4, 8.6), xytext=(np.pi / 4, 8.6),
             arrowprops=dict(arrowstyle="<->", color=INK, linewidth=1.3))
ax4.text(3 * np.pi / 4, 8.8, "period $= \\pi$", fontsize=10.5, color=INK,
         ha="center")
ax4.text(2 * np.pi + 0.18, 4.0, "midline $y = 4$", fontsize=10.5,
         color=GREEN, va="center")

for _fig, _name in ((fig1, "aasl-3-7b-idea-a.svg"),
                    (fig2, "aasl-3-7b-idea-b.svg"),
                    (fig3, "aasl-3-7b-idea-c.svg"),
                    (fig4, "aasl-3-7b-idea-d.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
