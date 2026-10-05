"""AA SL 5.2 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_2.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_2.py  … 目視用の PNG も

出力: aa-sl/05-calculus/img/aasl-5-2-updown.svg
      aa-sl/05-calculus/img/aasl-5-2-idea-a.svg
      aa-sl/05-calculus/img/aasl-5-2-idea-b.svg
      aa-sl/05-calculus/img/aasl-5-2-stat.svg

(updown) 第 1 節用。増加している部分は赤、減少している部分は青。
(a) y = f(x)。減っているところは青、増えているところは赤。停留点も。
(b) y = f'(x)。(a) と x をそろえた別の図にする。
(stat) 第 3 節用。sign diagram と曲線の形を、3 つの場合で並べる。
    f' が x 軸より上 ⇔ f は上がる、下 ⇔ f は下がる、
    x 軸に触れるだけ（符号が変わらない）⇔ f は水平になるが向きは変わらない。

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
UP = "#d8e6f4"
DOWN = "#f6ddc4"
RED = "#c0392b"
BLUE = "#1f5fa8"
REDF = "#f7dedb"
BLUEF = "#dce7f5"

# f'(x) = -(x+2)(x-1)^2 * k をやめ、符号が変わる点と触れるだけの点を
# 1 つずつ持つ形にする: f'(x) = (x + 2)(x - 1)^2 / 6
A, B = -2.0, 1.0


def fp(t):
    return ((t + 2.0) * (t - 1.0) ** 2) / 6.0


def f(t):
    """fp の原始関数（手で積分した多項式）。
    fp = (x+2)(x-1)^2/6 = (x^3 - 3x + 2)/6  なので
    f  = (x^4/4 - 3x^2/2 + 2x)/6 + c
    """
    return (t ** 4 / 4.0 - 1.5 * t ** 2 + 2.0 * t) / 6.0 + 1.6


# ══════════════════════════════════════════════════════════
# (updown) 第 1 節：増加している部分は赤、減少している部分は青
# ══════════════════════════════════════════════════════════
figU, axU = plt.subplots(figsize=(7.4, 4.3))


def fu(t):
    """増加 → 減少 → 増加 となる形。fu = t^3/3 - t"""
    return t ** 3 / 3.0 - t


TU = np.linspace(-2.05, 2.05, 600)
axU.set_title("Reading the graph from left to right", fontsize=11,
              color=INK, loc="left", pad=12)
axU.set_xlim(-2.45, 2.65)
axU.set_ylim(-1.75, 1.95)
axU.axis("off")
axU.plot([-2.35, 2.35], [0, 0], color=GREY, linewidth=1.0)
axU.plot([0, 0], [-1.60, 1.70], color=GREY, linewidth=1.0)
axU.text(2.42, -0.02, "$x$", fontsize=10, color=GREY, va="center")
axU.text(-0.07, 1.78, "$y$", fontsize=10, color=GREY, ha="right")

for _lo, _hi, _col in ((-2.05, -1.0, RED), (-1.0, 1.0, BLUE),
                       (1.0, 2.05, RED)):
    _t = np.linspace(_lo, _hi, 300)
    axU.plot(_t, fu(_t), color=_col, linewidth=2.6)

for _x in (-1.0, 1.0):
    axU.plot([_x], [fu(_x)], "o", color=INK, markersize=6.0, zorder=4)
    axU.plot([_x, _x], [0, fu(_x)], color=GREY, linewidth=1.0,
             linestyle=(0, (3, 3)))

axU.text(-1.62, fu(-1.62) + 0.20, "increasing", fontsize=11, color=RED,
         ha="center")
axU.text(0.0, -0.34, "decreasing", fontsize=11, color=BLUE, ha="center")
axU.text(1.42, fu(1.42) - 0.42, "increasing", fontsize=11, color=RED,
         ha="center", va="top")

axU.annotate("", xy=(2.05, -1.48), xytext=(-2.05, -1.48),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
axU.text(0.0, -1.68, "$x$ increasing", fontsize=9.5, color=GREY,
         ha="center", va="top")

figU.tight_layout()
_pU = os.path.join(OUT, "aasl-5-2-updown.svg")
figU.savefig(_pU, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(_pU))
if os.environ.get("FIG_PNG"):
    _qU = _pU[:-4] + ".png"
    figU.savefig(_qU, format="png", dpi=150, bbox_inches="tight",
                 facecolor="white")
    print("wrote", os.path.normpath(_qU))

figA, ax1 = plt.subplots(figsize=(9.2, 5.0))
figB, ax2 = plt.subplots(figsize=(9.2, 4.2))
T = np.linspace(-3.1, 2.6, 500)

# ══════════════════════════════════════════════════════════
# (a) y = f(x)
# ══════════════════════════════════════════════════════════
ax1.set_title("$y = f(x)$", fontsize=12, color=INK, loc="left", pad=10)
ax1.set_xlim(-3.45, 3.25)
ax1.set_ylim(-0.75, 4.10)
ax1.axis("off")
ax1.plot([-3.3, 3.10], [0, 0], color=GREY, linewidth=1.1)
ax1.text(3.16, 0.0, "$x$", fontsize=11, color=GREY, va="center")

_dn = T[T <= A]
_up = T[T >= A]
ax1.plot(_dn, f(_dn), color=BLUE, linewidth=2.8)
ax1.plot(_up, f(_up), color=RED, linewidth=2.8)

for _x in (A, B):
    ax1.plot([_x, _x], [0, f(_x)], color=GREY, linewidth=0.9,
             linestyle=(0, (3, 3)))
    _t = np.array([_x - 0.78, _x + 0.78])
    ax1.plot(_t, [f(_x)] * 2, color=WARM, linewidth=1.8)
    ax1.plot([_x], [f(_x)], "o", color=INK, markersize=7, zorder=5)

ax1.text(A, -0.16, "$p$", fontsize=12, color=INK, ha="center", va="top")
ax1.text(B, -0.16, "$q$", fontsize=12, color=INK, ha="center", va="top")
ax1.text(-2.55, 3.55, "decreasing", fontsize=12, color=BLUE, ha="center")
ax1.text(-0.30, 3.55, "increasing", fontsize=12, color=RED, ha="center")
ax1.text(2.05, 3.55, "increasing", fontsize=12, color=RED, ha="center")
ax1.text(A, f(A) + 0.30, "stationary point", fontsize=10, color=WARM,
         ha="center")
ax1.text(B + 0.88, f(B) + 0.02, "stationary point", fontsize=10, color=WARM,
         ha="left", va="center")

figA.tight_layout()
_pA = os.path.join(OUT, "aasl-5-2-idea-a.svg")
figA.savefig(_pA, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(_pA))
if os.environ.get("FIG_PNG"):
    figA.savefig(_pA[:-4] + ".png", format="png", dpi=150,
                 bbox_inches="tight", facecolor="white")

# ══════════════════════════════════════════════════════════
# (b) y = f'(x)
# ══════════════════════════════════════════════════════════
ax2.set_title("$y = f'(x)$", fontsize=12, color=INK, loc="left", pad=10)
ax2.set_xlim(-3.45, 3.25)
ax2.set_ylim(-1.75, 2.05)
ax2.axis("off")

ax2.fill_between(T, 0, fp(T), where=(fp(T) > 0), color=REDF)
ax2.fill_between(T, 0, fp(T), where=(fp(T) < 0), color=BLUEF)
ax2.plot(T, fp(T), color=INK, linewidth=2.4)

# x 軸は太くして、目立たせる
ax2.plot([-3.3, 3.10], [0, 0], color=INK, linewidth=2.0, zorder=4)
ax2.text(3.16, 0.0, "$x$", fontsize=11, color=INK, va="center")

for _x in (A, B):
    ax2.plot([_x, _x], [-1.30, 0], color=GREY, linewidth=0.9,
             linestyle=(0, (3, 3)))
    ax2.plot([_x], [0], "o", color=INK, markersize=7, zorder=5)
    ax2.text(_x, -1.38, "$p$" if _x == A else "$q$", fontsize=12, color=INK,
             ha="center", va="top")

ax2.text(-2.55, -0.55, "$f'(x) < 0$", fontsize=12, color=BLUE, ha="center")
ax2.text(-0.30, 0.95, "$f'(x) > 0$", fontsize=12, color=RED, ha="center")
ax2.text(2.10, 0.55, "$f'(x) > 0$", fontsize=12, color=RED, ha="center")

figB.tight_layout()
_pB = os.path.join(OUT, "aasl-5-2-idea-b.svg")
figB.savefig(_pB, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(_pB))
if os.environ.get("FIG_PNG"):
    figB.savefig(_pB[:-4] + ".png", format="png", dpi=150,
                 bbox_inches="tight", facecolor="white")


# ══════════════════════════════════════════════════════════
# (stat) 停留点：sign diagram と曲線の形
# ══════════════════════════════════════════════════════════
figS, axS = plt.subplots(figsize=(10.2, 6.4))
axS.set_xlim(0, 14)
axS.set_ylim(0, 9.4)
axS.axis("off")

# 罫線
axS.plot([0.1, 13.9], [8.7, 8.7], color=INK, linewidth=1.1)
for _y in (5.85, 3.0):
    axS.plot([0.1, 13.9], [_y, _y], color=GREY, linewidth=0.7)
for _x in (5.9, 10.2):
    axS.plot([_x, _x], [0.1, 8.7], color=GREY, linewidth=0.7)

# 見出し
axS.text(0.30, 8.95, "sign diagram of $f'(x)$", fontsize=11.5, color=INK,
         style="italic", va="bottom")
axS.text(6.15, 8.95, "shape near $x = a$", fontsize=11.5, color=INK,
         style="italic", va="bottom")
axS.text(10.45, 8.95, "$x = a$ is", fontsize=11.5, color=INK,
         style="italic", va="bottom")


def _sign(cx, cy, left, right, w=1.5):
    """数直線を 1 本かき、a の左右に符号を書く。"""
    axS.annotate("", xy=(cx + w, cy), xytext=(cx - w, cy),
                 arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.2))
    axS.plot([cx, cx], [cy - 0.16, cy + 0.16], color=INK, linewidth=1.3)
    for _dx, _s in ((-w * 0.52, left), (w * 0.52, right)):
        axS.text(cx + _dx, cy + 0.24, _s, fontsize=16,
                 color=RED if _s == "$+$" else BLUE, ha="center", va="bottom")
    axS.text(cx, cy - 0.26, "$a$", fontsize=11.5, color=INK, ha="center",
             va="top")
    axS.text(cx + w + 0.12, cy, "$x$", fontsize=11, color=INK, ha="left",
             va="center")


def _shape(cx, cy, kind, s=0.80):
    """曲線の形。上がっている向きは赤、下がっている向きは青。"""
    _t = np.linspace(-1, 1, 201)
    if kind == "max":
        _y, _cols, _py = -_t ** 2 + 1.0, (RED, BLUE), 1.0
    elif kind == "min":
        _y, _cols, _py = _t ** 2 - 1.0, (BLUE, RED), -1.0
    elif kind == "up":
        _y, _cols, _py = _t ** 3, (RED, RED), 0.0
    else:
        _y, _cols, _py = -_t ** 3, (BLUE, BLUE), 0.0
    _lo, _hi = cy + s * _y.min(), cy + s * _y.max()
    axS.plot([cx, cx], [_lo - 0.26, _hi + 0.20], color=GREY,
             linewidth=0.9, linestyle=(0, (3, 3)))
    _h = len(_t) // 2 + 1
    axS.plot(cx + s * _t[:_h], cy + s * _y[:_h], color=_cols[0], linewidth=2.6)
    axS.plot(cx + s * _t[_h - 1:], cy + s * _y[_h - 1:], color=_cols[1],
             linewidth=2.6)
    axS.plot([cx], [cy + s * _py], "o", color=INK, markersize=6.5, zorder=5)
    axS.text(cx, _lo - 0.34, "$x = a$", fontsize=10, color=GREY,
             ha="center", va="top")


# 1 行目
_sign(3.0, 7.35, "$+$", "$-$")
_shape(8.05, 7.08, "max")
axS.text(10.45, 7.28, "a local maximum", fontsize=12, color=INK, va="center")

# 2 行目
_sign(3.0, 4.50, "$-$", "$+$")
_shape(8.05, 5.04, "min")
axS.text(10.45, 4.43, "a local minimum", fontsize=12, color=INK, va="center")

# 3 行目（符号が変わらない：2 とおり）
_sign(1.95, 1.62, "$+$", "$+$", w=0.98)
_sign(4.40, 1.62, "$-$", "$-$", w=0.98)
_shape(7.20, 1.76, "up", s=0.62)
_shape(9.15, 1.76, "down", s=0.62)
axS.text(10.45, 1.62, "neither of these", fontsize=12, color=INK, va="center")

figS.tight_layout()
_pS = os.path.join(OUT, "aasl-5-2-stat.svg")
figS.savefig(_pS, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(_pS))
if os.environ.get("FIG_PNG"):
    figS.savefig(_pS[:-4] + ".png", format="png", dpi=150,
                 bbox_inches="tight", facecolor="white")
