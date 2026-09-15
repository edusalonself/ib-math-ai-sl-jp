"""AA SL 5.1 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_1.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_1.py  … 目視用の PNG も

出力: aa-sl/05-calculus/img/aasl-5-1-idea.svg

(a) 割線が接線に近づいていくこと（Q が P に近づく）。
(b) 極限は「x = a のときの値」ではなく「x = a に近づくときの行き先」であること。

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
LIGHT = "#9db8d4"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.9))

# ══════════════════════════════════════════════════════════
# (a) 割線 → 接線
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The chord turns into the tangent", fontsize=11,
              color=INK, loc="left", pad=12)


def f(t):
    return 0.28 * t * t + 0.5


X = np.linspace(0.2, 5.0, 400)
ax1.plot(X, f(X), color=ACCENT, linewidth=1.9)
ax1.set_xlim(-0.35, 5.6)
ax1.set_ylim(-1.85, 8.4)
ax1.axis("off")
ax1.plot([0.0, 5.4], [0, 0], color=GREY, linewidth=1.0)
ax1.plot([0.0, 0.0], [0, 8.0], color=GREY, linewidth=1.0)
ax1.text(5.45, -0.05, "$x$", fontsize=10, color=GREY, va="center")
ax1.text(-0.06, 8.1, "$y$", fontsize=10, color=GREY, ha="right")

PX = 1.4
PY = f(PX)
for _qx, _c in ((4.5, LIGHT), (3.4, LIGHT), (2.5, LIGHT)):
    _m = (f(_qx) - PY) / (_qx - PX)
    _t = np.array([0.7, 5.1])
    ax1.plot(_t, PY + _m * (_t - PX), color=_c, linewidth=1.0)
    ax1.plot([_qx], [f(_qx)], "o", color=_c, markersize=5.5)

MT = 2 * 0.28 * PX
_t = np.array([0.35, 4.1])
ax1.plot(_t, PY + MT * (_t - PX), color=WARM, linewidth=1.8)
ax1.plot([PX], [PY], "o", color=INK, markersize=6.5)

ax1.text(PX - 0.16, PY - 0.55, "$P$", fontsize=11, color=INK, ha="right")
ax1.text(4.70, f(4.5) + 0.30, "$Q_1$", fontsize=10, color=GREY)
ax1.text(3.60, f(3.4) + 0.30, "$Q_2$", fontsize=10, color=GREY)
ax1.text(2.60, f(2.5) - 0.62, "$Q_3$", fontsize=10, color=GREY)
ax1.text(4.15, PY + MT * (4.1 - PX) - 0.05, "tangent at $P$", fontsize=9.5,
         color=WARM, va="center")

ax1.text(0.0, -0.85, "as $Q$ slides towards $P$, the chord gradients settle",
         fontsize=9.5, color=INK)
ax1.text(0.0, -1.45, "the value they settle on is the gradient at $P$",
         fontsize=9.5, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) 極限は「近づくときの行き先」
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) A limit is where the outputs are heading", fontsize=11,
              color=INK, loc="left", pad=12)

A = 2.6
L = 3.2


def g(t):
    return L + 0.55 * (t - A) - 0.11 * (t - A) ** 3


XL = np.linspace(0.55, A - 0.012, 200)
XR = np.linspace(A + 0.012, 4.9, 200)
ax2.plot(XL, g(XL), color=ACCENT, linewidth=1.9)
ax2.plot(XR, g(XR), color=ACCENT, linewidth=1.9)
ax2.set_xlim(-0.35, 5.6)
ax2.set_ylim(-1.85, 8.4)
ax2.axis("off")
ax2.plot([0.0, 5.4], [0, 0], color=GREY, linewidth=1.0)
ax2.plot([0.0, 0.0], [0, 8.0], color=GREY, linewidth=1.0)
ax2.text(5.45, -0.05, "$x$", fontsize=10, color=GREY, va="center")
ax2.text(-0.06, 8.1, "$y$", fontsize=10, color=GREY, ha="right")

ax2.plot([A, A], [0, L], color=GREY, linewidth=0.9, linestyle=(0, (3, 3)))
ax2.plot([0, A], [L, L], color=GREY, linewidth=0.9, linestyle=(0, (3, 3)))
ax2.plot([A], [L], "o", markerfacecolor="white", markeredgecolor=ACCENT,
         markeredgewidth=1.6, markersize=8)
ax2.text(A, -0.10, "$a$", fontsize=11, color=INK, ha="center", va="top")
ax2.text(-0.14, L, "$L$", fontsize=11, color=INK, ha="right", va="center")

ax2.annotate("", xy=(A - 0.22, 0.42), xytext=(A - 1.35, 0.42),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.2))
ax2.annotate("", xy=(A + 0.22, 0.42), xytext=(A + 1.35, 0.42),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.2))

ax2.text(4.95, g(4.6) + 0.5, "$y = f(x)$", fontsize=10, color=ACCENT,
         ha="right")
ax2.text(0.0, -0.85, "from the left and from the right, the outputs head "
         "for $L$", fontsize=9.5, color=INK)
ax2.text(0.0, -1.45, "the open circle says $f(a)$ itself need not exist",
         fontsize=9.5, color=WARM)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-5-1-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  tangent gradient at P =", MT)

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
