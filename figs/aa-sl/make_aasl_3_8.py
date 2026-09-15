"""AA SL 3.8 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_8.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_8.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-8-idea.svg

(a) y = sin x と y = k。交点の数が解の数。
(b) 中身が 2x のとき、x の区間を 2 倍にしてから解く。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（(a) の高さは k のまま）。
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.4))

# ══════════════════════════════════════════════════════════
# (a) 交点の数が解の数
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Reading the number of solutions", fontsize=11, color=INK,
              loc="left", pad=10)
x = np.linspace(0, 2 * np.pi, 700)
K = 0.62
ax1.plot(x, np.sin(x), color=ACCENT, linewidth=2.2)
ax1.axhline(K, color=WARM, linewidth=1.6, linestyle=(0, (6, 3)))
ax1.axhline(0, color=GREY, linewidth=1.0)
for _r in (np.arcsin(K), np.pi - np.arcsin(K)):
    ax1.plot([_r], [K], marker="o", markersize=6.0, color=INK, zorder=3)
    ax1.plot([_r, _r], [0, K], color=GREY, linewidth=0.9,
             linestyle=(0, (2, 3)))
ax1.set_xlim(-0.25, 2 * np.pi + 0.25)
ax1.set_ylim(-1.7, 1.95)
ax1.set_xticks([0, np.pi, 2 * np.pi])
ax1.set_xticklabels(["$0$", "$\\pi$", "$2\\pi$"], fontsize=9.5)
ax1.set_yticks([-1, 0, 1])
ax1.set_yticklabels(["$-1$", "$0$", "$1$"], fontsize=9.5)
for _sp in ("top", "right", "left", "bottom"):
    ax1.spines[_sp].set_visible(False)
ax1.tick_params(length=0, colors=GREY)
ax1.text(2 * np.pi + 0.05, K - 0.02, "$y = k$", fontsize=10.5, color=WARM)
ax1.text(0.05, 1.62, "$y = \\sin x$", fontsize=10.5, color=ACCENT)
ax1.text(-0.25, -1.65, "the line meets the curve twice, so there are two "
         "solutions here", fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 中身が変わっているとき
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) When the inside is $2x$", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-0.6, 13.6)
ax2.set_ylim(-1.2, 3.0)
ax2.axis("off")

ax2.annotate("", xy=(6.9, 2.15), xytext=(0.2, 2.15),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.6))
ax2.plot([0.2, 6.9], [2.15, 2.15], color=ACCENT, linewidth=0)
ax2.text(0.05, 2.42, "$x$ runs from $0$ to $\\pi$", fontsize=10, color=ACCENT)
for _p, _lab in [(0.2, "$0$"), (6.9, "$\\pi$")]:
    ax2.plot([_p], [2.15], marker="|", markersize=11, color=ACCENT)
    ax2.text(_p - 0.12, 1.80, _lab, fontsize=9.5, color=ACCENT)

ax2.annotate("", xy=(13.2, 0.55), xytext=(0.2, 0.55),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.6))
ax2.text(0.05, 0.88, "so $2x$ runs from $0$ to $2\\pi$", fontsize=10,
         color=WARM)
for _p, _lab in [(0.2, "$0$"), (6.7, "$\\pi$"), (13.2, "$2\\pi$")]:
    ax2.plot([_p], [0.55], marker="|", markersize=11, color=WARM)
    ax2.text(_p - 0.12, 0.18, _lab, fontsize=9.5, color=WARM)

ax2.annotate("", xy=(13.2, 0.95), xytext=(6.9, 1.80),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(8.6, 1.52, "double it", fontsize=9.5, color=GREY)

ax2.text(-0.6, -1.15, "solve on the longer line first, then halve every answer",
         fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-3-8-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
