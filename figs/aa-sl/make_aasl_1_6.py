"""AA SL 1.6 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_6.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_6.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-6-idea.svg

(a) 試験で安全な書き方は、片側だけを下りていく。LHS から出発して RHS に着く。
    示したい式から出発する道は、線を引いて消してある。
(b) 方程式は数直線の 1 点でだけ成り立ち、恒等式はどこでも成り立つ。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
RED = "#b91c1c"

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(9.8, 4.2), gridspec_kw={"width_ratios": [1.15, 1.0]}
)

# ══════════════════════════════════════════════════════════
# (a) LHS から RHS へ、片側だけを下りる
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The safe layout: down one side only",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0.0, 1.0)
ax1.axis("off")

STEPS = [(0.86, "LHS $= (x+2)^{2} - 4x$", "start here"),
         (0.62, "$= x^{2} + 4x + 4 - 4x$", "expand"),
         (0.38, "$= x^{2} + 4$", "collect"),
         (0.14, "$=$ RHS", "arrive here")]

for y, expr, note in STEPS:
    ax1.text(0.30, y, expr, ha="left", va="center", fontsize=12.5, color=INK)
    ax1.text(0.26, y, "", ha="right", va="center")
    ax1.text(0.97, y, note, ha="right", va="center", fontsize=9,
             color=WARM if note.endswith("here") else GREY)

for i in range(len(STEPS) - 1):
    ax1.annotate("", xy=(0.24, STEPS[i + 1][0] + 0.05),
                 xytext=(0.24, STEPS[i][0] - 0.05),
                 arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.5))

ax1.annotate("", xy=(0.10, 0.86), xytext=(0.10, 0.14),
             arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.4,
                             linestyle=(0, (4, 3))))
ax1.plot([0.045, 0.155], [0.44, 0.56], color=RED, linewidth=2.0)
ax1.plot([0.045, 0.155], [0.56, 0.44], color=RED, linewidth=2.0)
ax1.text(0.10, 0.03, "avoid starting\nfrom the answer", ha="center", va="bottom",
         fontsize=8.5, color=RED)

# ══════════════════════════════════════════════════════════
# (b) 方程式は 1 点、恒等式はどこでも
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Where the statement is true",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-4.6, 5.4)
ax2.set_ylim(-1.5, 2.3)
ax2.axis("off")

XS = np.linspace(-4.0, 5.0, 200)

# 上：恒等式
ax2.plot([-4.0, 5.0], [1.5, 1.5], color=ACCENT, linewidth=5.0,
         solid_capstyle="butt", alpha=0.85)
ax2.text(-4.0, 2.0, "identity  $(x+1)^{2} \\equiv x^{2}+2x+1$",
         ha="left", va="center", fontsize=10.5, color=INK)
ax2.text(5.25, 1.5, "true\neverywhere", ha="left", va="center",
         fontsize=9, color=ACCENT)

# 下：方程式
ax2.plot([-4.0, 5.0], [0.0, 0.0], color=GREY, linewidth=1.4)
for t in range(-4, 6):
    ax2.plot([t, t], [-0.10, 0.10], color=GREY, linewidth=0.9)
    if t % 2 == 0:
        ax2.text(t, -0.32, str(t), ha="center", va="center",
                 fontsize=8.5, color=GREY)
ax2.plot([3], [0.0], marker="o", markersize=9, color=WARM, zorder=3)
ax2.text(-4.0, 0.75, "equation  $2x+1 = 7$",
         ha="left", va="center", fontsize=10.5, color=INK)
ax2.text(5.25, 0.0, "true at\none value", ha="left", va="center",
         fontsize=9, color=WARM)
ax2.text(3.0, -0.85, "$x = 3$", ha="center", va="center",
         fontsize=10, color=WARM)

ax2.text(0.5, -1.35, "$x$", ha="center", va="center", fontsize=10, color=GREY)

fig.tight_layout(w_pad=2.6)
path = os.path.join(OUT, "aasl-1-6-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
