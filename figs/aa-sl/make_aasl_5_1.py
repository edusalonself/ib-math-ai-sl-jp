"""AA SL 5.1 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_1.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_1.py  … 目視用の PNG も

出力: aa-sl/05-calculus/img/aasl-5-1-idea-a.svg
      aa-sl/05-calculus/img/aasl-5-1-idea-b.svg
      aa-sl/05-calculus/img/aasl-5-1-idea-c.svg

(a) chord（割線）とは何か。2 点 P、Q を結ぶ直線と、横と縦の差。
(b) 極限は「x = a のときの値」ではなく「x = a に近づくときの行き先」であること。
(c) Q を P に近づけると、割線が接線に近づくこと。

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

fig1, ax1 = plt.subplots(figsize=(5.8, 4.9))
fig2, ax2 = plt.subplots(figsize=(5.8, 4.9))
fig3, ax3 = plt.subplots(figsize=(5.8, 4.9))
# ══════════════════════════════════════════════════════════
# (a) chord とは
# ══════════════════════════════════════════════════════════
ax1.set_title("A chord joins two points on the curve", fontsize=11,
              color=INK, loc="left", pad=12)


def f(t):
    return 0.28 * t * t + 0.5


X = np.linspace(0.2, 5.0, 400)
ax1.plot(X, f(X), color=ACCENT, linewidth=1.9)
ax1.set_xlim(-0.35, 5.6)
ax1.set_ylim(-1.05, 8.4)
ax1.axis("off")
ax1.plot([0.0, 5.4], [0, 0], color=GREY, linewidth=1.0)
ax1.plot([0.0, 0.0], [0, 8.0], color=GREY, linewidth=1.0)
ax1.text(5.45, -0.05, "$x$", fontsize=10, color=GREY, va="center")
ax1.text(-0.06, 8.1, "$y$", fontsize=10, color=GREY, ha="right")

AX, BX = 1.4, 4.3
AY, BY = f(AX), f(BX)

# 割線
_mA = (BY - AY) / (BX - AX)
_t = np.array([0.7, 5.15])
ax1.plot(_t, AY + _mA * (_t - AX), color=WARM, linewidth=1.8)
ax1.text(5.15, AY + _mA * (5.15 - AX) + 0.55, "chord", fontsize=10.5,
         color=WARM, ha="right")

# 横と縦の差
ax1.plot([AX, BX], [AY, AY], color=GREY, linewidth=1.2,
         linestyle=(0, (4, 3)))
ax1.plot([BX, BX], [AY, BY], color=GREY, linewidth=1.2,
         linestyle=(0, (4, 3)))
ax1.text((AX + BX) / 2, AY - 0.45, "$b - a$", fontsize=10.5, color=GREY,
         ha="center")
ax1.text(BX + 0.12, (AY + BY) / 2, "$f(b) - f(a)$", fontsize=10.5,
         color=GREY, va="center")

# 2 点
ax1.plot([AX], [AY], "o", color=INK, markersize=6.5)
ax1.plot([BX], [BY], "o", color=INK, markersize=6.5)
ax1.text(AX - 0.16, AY + 0.30, "$P$", fontsize=11, color=INK, ha="right")
ax1.text(BX - 0.16, BY + 0.30, "$Q$", fontsize=11, color=INK, ha="right")

# x 軸の目盛り
for _x, _lab in ((AX, "$a$"), (BX, "$b$")):
    ax1.plot([_x, _x], [-0.12, 0.12], color=GREY, linewidth=1.0)
    ax1.text(_x, -0.42, _lab, fontsize=10.5, color=GREY, ha="center")

# ══════════════════════════════════════════════════════════
# (b) 極限は「近づくときの行き先」
# ══════════════════════════════════════════════════════════
ax2.set_title("A limit is where the outputs are heading", fontsize=11,
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

# ══════════════════════════════════════════════════════════
# (c) Q を P に近づけると、割線が接線に近づく
# ══════════════════════════════════════════════════════════
ax3.set_title("The chord turns into the tangent", fontsize=11,
              color=INK, loc="left", pad=12)

ax3.plot(X, f(X), color=ACCENT, linewidth=1.9)
ax3.set_xlim(-0.35, 5.6)
ax3.set_ylim(-1.05, 8.4)
ax3.axis("off")
ax3.plot([0.0, 5.4], [0, 0], color=GREY, linewidth=1.0)
ax3.plot([0.0, 0.0], [0, 8.0], color=GREY, linewidth=1.0)
ax3.text(5.45, -0.05, "$x$", fontsize=10, color=GREY, va="center")
ax3.text(-0.06, 8.1, "$y$", fontsize=10, color=GREY, ha="right")

PX = 1.4
PY = f(PX)
for _qx in (4.5, 3.4, 2.5):
    _m3 = (f(_qx) - PY) / (_qx - PX)
    _t3 = np.array([0.7, 5.1])
    ax3.plot(_t3, PY + _m3 * (_t3 - PX), color=LIGHT, linewidth=1.0)
    ax3.plot([_qx], [f(_qx)], "o", color=LIGHT, markersize=5.5)

MT = 2 * 0.28 * PX
_t3 = np.array([0.35, 4.1])
ax3.plot(_t3, PY + MT * (_t3 - PX), color=WARM, linewidth=1.8)
ax3.plot([PX], [PY], "o", color=INK, markersize=6.5)

ax3.text(PX - 0.16, PY - 0.55, "$P$", fontsize=11, color=INK, ha="right")
ax3.text(4.70, f(4.5) + 0.30, "$Q_1$", fontsize=10, color=GREY)
ax3.text(3.60, f(3.4) + 0.30, "$Q_2$", fontsize=10, color=GREY)
ax3.text(2.60, f(2.5) - 0.62, "$Q_3$", fontsize=10, color=GREY)
ax3.text(4.15, PY + MT * (4.1 - PX) - 0.05, "tangent at $P$", fontsize=9.5,
         color=WARM, va="center")

for _fig, _name in ((fig1, "aasl-5-1-idea-a.svg"),
                    (fig2, "aasl-5-1-idea-b.svg"),
                    (fig3, "aasl-5-1-idea-c.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
