"""AA SL 3.7a の演習 3 の解答図（y = tan x, 0 ≤ x ≤ 2π）。

    python3 figs/aa-sl/make_aasl_3_7a_ex3.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_7a_ex3.py

出力: aa-sl/03-geometry/img/aasl-3-7a-ex3.svg

★ これは演習 3 の「解答例」の図です。生徒が自分のスケッチと見くらべます。
   指定区間 0 ≤ x ≤ 2π では、漸近線 π/2 と 3π/2 で切れて
   **3 つの部分**になります（左端と右端は枝の一部、まん中が全体の枝）。
   零点は 0、π、2π の 3 つです。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * \\bigl \\bigr \\Box は読めない → ふつうの ( ) と文字を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

YMAX = 4.2
A1, A2 = np.pi / 2, 3 * np.pi / 2
EPS = 0.035

fig, ax = plt.subplots(figsize=(8.4, 4.6))

# 3 つの部分（指定区間で切れる）
PIECES = ((0.0, A1), (A1, A2), (A2, 2 * np.pi))
for _lo, _hi in PIECES:
    _t = np.linspace(_lo + EPS, _hi - EPS, 600)
    _y = np.tan(_t)
    _m = np.abs(_y) <= YMAX
    ax.plot(_t[_m], _y[_m], color=ACCENT, linewidth=2.2)

# 漸近線（破線）
for _a in (A1, A2):
    ax.plot([_a, _a], [-YMAX, YMAX], color=GREY, linewidth=1.2,
            linestyle=(0, (5, 4)))

ax.axhline(0, color=GREY, linewidth=1.0)

# 零点
for _z in (0.0, np.pi, 2 * np.pi):
    ax.plot([_z], [0.0], marker="o", markersize=5.5, color=WARM, zorder=5)

ax.set_xlim(-0.35, 2 * np.pi + 0.35)
ax.set_ylim(-YMAX - 0.35, YMAX + 2.1)
ax.set_xticks([0, A1, np.pi, A2, 2 * np.pi])
ax.set_xticklabels(["$0$", "$\\dfrac{\\pi}{2}$", "$\\pi$",
                    "$\\dfrac{3\\pi}{2}$", "$2\\pi$"], fontsize=11)
ax.set_yticks([])
for _s in ("top", "right", "left"):
    ax.spines[_s].set_visible(False)
ax.spines["bottom"].set_visible(False)

ax.text(2 * np.pi + 0.2, 2.6, "$y = \\tan x$", fontsize=12, color=ACCENT,
        ha="right")
ax.text(0.05, -YMAX - 0.05, "zeros at $0$, $\\pi$ and $2\\pi$", fontsize=10,
        color=WARM, ha="left", va="center")
ax.text(0.05, YMAX + 1.95,
        "three pieces on $0 \\leq x \\leq 2\\pi$: the middle one is a whole "
        "branch,\nthe two outer ones are halves of a branch. period $= \\pi$",
        fontsize=10, color=INK, ha="left", va="top")

fig.tight_layout()
path = os.path.join(OUT, "aasl-3-7a-ex3.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
