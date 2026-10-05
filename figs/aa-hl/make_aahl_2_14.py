"""AA HL 2.14（偶関数・奇関数・逆関数・self-inverse）の図をつくる。

    python3 figs/aa-hl/make_aahl_2_14.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_2_14.py  … 目視用の PNG も

出力: aa-hl/02-functions/img/aahl-2-14-idea-a.svg
      aa-hl/02-functions/img/aahl-2-14-idea-b.svg

(a) 偶関数は y 軸について線対称、奇関数は原点について点対称。
(b) 定義域を切ってから、y = x について折り返すと逆関数が出る。

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"


def frame(ax):
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GREY)
    ax.spines["bottom"].set_color(GREY)
    ax.set_xticks([])
    ax.set_yticks([])


# ══════════════════════════════════════════════════════════
# (a) 偶関数・奇関数の対称性
# ══════════════════════════════════════════════════════════
fig1, axes1 = plt.subplots(1, 2, figsize=(6.4, 2.9))
_t = np.linspace(-1.9, 1.9, 300)

axes1[0].plot(_t, _t ** 2 - 1.0, color=ACCENT, linewidth=1.8)
axes1[0].axvline(0.0, color=WARM, linestyle="--", linewidth=1.1)
axes1[0].plot([-1.3, 1.3], [1.3 ** 2 - 1.0] * 2, "o", color=WARM, markersize=5)
axes1[0].annotate("", xy=(1.25, 0.69), xytext=(-1.25, 0.69),
                  arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=0.9))
axes1[0].set_title("even: $f(-x) = f(x)$", fontsize=10.5, color=ACCENT, pad=6)
axes1[0].text(0.0, -2.6, "a mirror in the $y$-axis", ha="center", va="center",
              fontsize=8.5, color=GREY)
axes1[0].set_xlim(-2.2, 2.2)
axes1[0].set_ylim(-2.2, 2.6)
frame(axes1[0])

axes1[1].plot(_t, _t ** 3 * 0.5, color=ACCENT, linewidth=1.8)
axes1[1].plot([-1.5, 1.5], [-1.6875, 1.6875], "o", color=WARM, markersize=5)
axes1[1].annotate("", xy=(1.45, 1.63), xytext=(-1.45, -1.63),
                  arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=0.9,
                                  linestyle="--"))
axes1[1].plot([0.0], [0.0], "o", color=WARM, markersize=5)
axes1[1].set_title("odd: $f(-x) = -f(x)$", fontsize=10.5, color=ACCENT, pad=6)
axes1[1].text(0.0, -2.6, "a half turn about the origin", ha="center",
              va="center", fontsize=8.5, color=GREY)
axes1[1].set_xlim(-2.2, 2.2)
axes1[1].set_ylim(-2.2, 2.6)
frame(axes1[1])

# ══════════════════════════════════════════════════════════
# (b) 定義域を切って、y = x で折り返す
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.4, 4.4))
ax2.set_title("Cut the domain first, then reflect in $y=x$",
              fontsize=10.5, color=INK, loc="left", pad=10)
_u = np.linspace(-2.2, 2.6, 300)
ax2.plot(_u, _u ** 2, color=GREY, linewidth=1.2, linestyle=":")
_p = np.linspace(0.0, 2.6, 200)
ax2.plot(_p, _p ** 2, color=ACCENT, linewidth=2.0)
ax2.plot(_p ** 2, _p, color=WARM, linewidth=2.0)
_l = np.linspace(-1.0, 6.4, 100)
ax2.plot(_l, _l, color=GREY, linewidth=1.0, linestyle="--")
ax2.text(1.35, 6.0, "$y=f(x)$, $x \\geq 0$", ha="center", va="center",
         fontsize=9.5, color=ACCENT,
         bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax2.text(5.6, 1.5, "$y=f^{-1}(x)$", ha="center", va="center", fontsize=9.5,
         color=WARM, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax2.text(5.2, 5.6, "$y=x$", ha="center", va="center", fontsize=9, color=GREY)
ax2.text(-1.7, 5.2, "the dotted part\nis cut off", ha="left", va="center",
         fontsize=8.5, color=GREY)
ax2.set_xlim(-2.4, 6.8)
ax2.set_ylim(-1.2, 6.8)
frame(ax2)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-2-14-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-2-14-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
