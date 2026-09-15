"""AA SL 2.11 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_11.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_11.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-11-idea.svg

(a) 平行移動と対称移動。もとの山を、上へ・右へ・x 軸で折り返す。
(b) 拡大。縦に p 倍、横に 1/q 倍。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（動かす量は a, b, p, q で書く）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"
PLUM = "#7e22ce"


def bump(t):
    """もとの関数 y = f(x)：原点あたりの、左右非対称な山。"""
    return 2.0 * np.exp(-(t ** 2) / 1.6) + 0.55 * t * np.exp(-(t ** 2) / 3.0)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.8))

# ══════════════════════════════════════════════════════════
# (a) 平行移動と対称移動
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Translations and reflections", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-4.4, 6.4)
ax1.set_ylim(-3.6, 5.4)
ax1.axis("off")

ax1.annotate("", xy=(6.1, 0), xytext=(-4.1, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 5.1), xytext=(0, -3.3),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(6.2, -0.45, "$x$", fontsize=11, color=GREY, ha="center")
ax1.text(-0.45, 5.2, "$y$", fontsize=11, color=GREY, va="center")

t = np.linspace(-4.0, 6.0, 500)
ax1.plot(t, bump(t), color=INK, linewidth=2.4)
ax1.plot(t, bump(t) + 2.0, color=ACCENT, linewidth=1.9, linestyle=(0, (6, 3)))
ax1.plot(t, bump(t - 3.0), color=GREEN, linewidth=1.9, linestyle=(0, (6, 3)))
ax1.plot(t, -bump(t), color=WARM, linewidth=1.9, linestyle=(0, (2, 2)))

ax1.text(-4.3, 2.1, "$y = f(x)$", fontsize=10.5, color=INK)
ax1.text(-4.3, 4.4, "$y = f(x) + b$", fontsize=10.5, color=ACCENT)
ax1.text(3.15, 2.6, "$y = f(x - a)$", fontsize=10.5, color=GREEN)
ax1.text(-4.3, -2.4, "$y = -f(x)$", fontsize=10.5, color=WARM)

ax1.annotate("", xy=(0.0, 4.05), xytext=(0.0, 2.05),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.1))
ax1.text(0.16, 3.0, "$b$", fontsize=10.5, color=ACCENT)
ax1.annotate("", xy=(3.0, 1.05), xytext=(0.0, 1.05),
             arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.1))
ax1.text(1.35, 1.25, "$a$", fontsize=10.5, color=GREEN)

ax1.text(-4.3, -3.5, "up by $b$; right by $a$; flipped in the $x$-axis",
         fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 拡大
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Stretches", fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-4.4, 4.8)
ax2.set_ylim(-1.6, 5.8)
ax2.axis("off")

ax2.annotate("", xy=(4.5, 0), xytext=(-4.1, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 5.5), xytext=(0, -1.3),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(4.6, -0.4, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.42, 5.6, "$y$", fontsize=11, color=GREY, va="center")

v = np.linspace(-4.0, 4.4, 500)
ax2.plot(v, bump(v), color=INK, linewidth=2.4)
ax2.plot(v, 2.0 * bump(v), color=PLUM, linewidth=1.9, linestyle=(0, (6, 3)))
ax2.plot(v, bump(2.0 * v), color=WARM, linewidth=1.9, linestyle=(0, (2, 2)))

ax2.text(1.55, 1.55, "$y = f(x)$", fontsize=10.5, color=INK)
ax2.text(1.15, 4.5, "$y = p\\,f(x)$", fontsize=10.5, color=PLUM)
ax2.text(-4.3, 2.6, "$y = f(qx)$", fontsize=10.5, color=WARM)
ax2.annotate("", xy=(0.62, 1.05), xytext=(-2.5, 2.5),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))

ax2.text(-4.3, -1.55, "vertical by $p$; horizontal by $\\frac{1}{q}$",
         fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-2-11-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
