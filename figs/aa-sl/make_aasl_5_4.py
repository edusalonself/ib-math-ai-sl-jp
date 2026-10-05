"""AA SL 5.4 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_4.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_4.py

出力: aa-sl/05-calculus/img/aasl-5-4-idea-a.svg

(a) 曲線上の点 P での接線と法線。直角の印と、傾きの関係。

★ 数値は入れません。文字だけです（例題・演習と重ならないように）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#e8f0f9"
SHADE = "#fdf0dc"

fig1, ax1 = plt.subplots(figsize=(5.8, 5.2))
# ══════════════════════════════════════════════════════════
# (a) 接線と法線
# ══════════════════════════════════════════════════════════
ax1.set_title("The tangent and the normal at $P$", fontsize=11, color=INK,
              loc="left", pad=12)


def f(t):
    return 0.16 * t * t + 0.6


PX = 2.6
PY = f(PX)
M = 2 * 0.16 * PX

T = np.linspace(0.15, 5.0, 400)
ax1.plot(T, f(T), color=ACCENT, linewidth=2.0)
ax1.set_xlim(-0.45, 5.7)
ax1.set_ylim(-1.25, 4.90)
# ★ 直角を直角に見せるため、縦横の目もりの幅をそろえる。
ax1.set_aspect("equal", adjustable="box")
ax1.axis("off")
ax1.plot([0.0, 5.5], [0, 0], color=GREY, linewidth=1.0)
ax1.plot([0.0, 0.0], [0, 4.65], color=GREY, linewidth=1.0)
ax1.text(5.58, -0.05, "$x$", fontsize=10, color=GREY, va="center")
ax1.text(-0.08, 4.75, "$y$", fontsize=10, color=GREY, ha="right")

_t = np.array([1.05, 4.55])
ax1.plot(_t, PY + M * (_t - PX), color=WARM, linewidth=1.8)
_s = np.array([1.35, 3.85])
ax1.plot(_s, PY - (1.0 / M) * (_s - PX), color=ACCENT, linewidth=1.8,
         linestyle=(0, (5, 3)))
ax1.plot([PX], [PY], "o", color=INK, markersize=7, zorder=4)

# 直角の印（縦横の目もりがそろっているので、正方形に見える）
_u = np.array([1.0, M]) / np.hypot(1.0, M) * 0.32
_v = np.array([1.0, -1.0 / M]) / np.hypot(1.0, 1.0 / M) * 0.32
_c = np.array([PX, PY])
ax1.plot([(_c + _u)[0], (_c + _u + _v)[0], (_c + _v)[0]],
         [(_c + _u)[1], (_c + _u + _v)[1], (_c + _v)[1]],
         color=GREY, linewidth=1.1)

ax1.text(PX - 0.16, PY + 0.24, "$P$", fontsize=12, color=INK, ha="right")
ax1.text(4.64, PY + M * (4.55 - PX), "tangent", fontsize=10, color=WARM,
         va="center")
ax1.text(1.24, PY - (1.0 / M) * (1.35 - PX), "normal", fontsize=10,
         color=ACCENT, va="center", ha="right")

ax1.text(0.0, -0.62, "gradient of tangent $= m$", fontsize=10, color=WARM)
ax1.text(0.0, -1.06, r"gradient of normal $= -\frac{1}{m}$   (when $m \neq 0$)",
         fontsize=10, color=ACCENT)

for _fig, _name in ((fig1, "aasl-5-4-idea-a.svg"),):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
