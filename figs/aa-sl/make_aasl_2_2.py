"""AA SL 2.2 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_2.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_2.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-2-vlt.svg
      aa-sl/02-functions/img/aasl-2-2-hlt.svg
      aa-sl/02-functions/img/aasl-2-2-idea-a.svg
      aa-sl/02-functions/img/aasl-2-2-idea-b.svg

(vlt) vertical line test。左は関数、右は円（関数でない）。
(hlt) horizontal line test。左は one-to-one、右は y = x^2。
(a) domain は x 軸に、range は y 軸に落とした範囲。
(b) 逆関数のグラフは、y = x について対称。

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
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FAINT = "#e5e7eb"

fig0, (ax0L, ax0R) = plt.subplots(1, 2, figsize=(6.8, 3.1))
figH, (axHL, axHR) = plt.subplots(1, 2, figsize=(6.8, 3.1))
fig1, ax1 = plt.subplots(figsize=(5.3, 4.4))
fig2, ax2 = plt.subplots(figsize=(5.3, 4.4))
# ══════════════════════════════════════════════════════════
# (vlt) vertical line test
# ══════════════════════════════════════════════════════════
for _ax in (ax0L, ax0R):
    _ax.set_xlim(-1.75, 1.75)
    _ax.set_ylim(-1.75, 1.75)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _ax.plot([-1.6, 1.6], [0, 0], color=FAINT, linewidth=1.0)
    _ax.plot([0, 0], [-1.6, 1.6], color=FAINT, linewidth=1.0)

# 左：関数（縦線と 1 か所で交わる）
ax0L.set_title("a function", fontsize=11, color=INK, loc="left", pad=8)
XL = np.linspace(-1.45, 1.45, 300)
YL = 1.35 * XL ** 3 - 1.15 * XL
ax0L.plot(XL, YL, color=ACCENT, linewidth=2.0)
VL = 0.95
ax0L.plot([VL, VL], [-1.6, 1.6], color=WARM, linewidth=1.3,
          linestyle=(0, (5, 3)))
_y = 1.35 * VL ** 3 - 1.15 * VL
ax0L.plot([VL], [_y], marker="o", markersize=6, color=WARM)
ax0L.text(VL + 0.12, -1.42, "one point", fontsize=10, color=WARM,
          ha="left", va="center")

# 右：円（縦線と 2 か所で交わる）
ax0R.set_title("not a function", fontsize=11, color=INK, loc="left", pad=8)
TH = np.linspace(0, 2 * np.pi, 400)
ax0R.plot(np.cos(TH), np.sin(TH), color=ACCENT, linewidth=2.0)
VR = 0.55
ax0R.plot([VR, VR], [-1.6, 1.6], color=WARM, linewidth=1.3,
          linestyle=(0, (5, 3)))
_h = np.sqrt(1 - VR ** 2)
ax0R.plot([VR, VR], [_h, -_h], marker="o", markersize=6, color=WARM,
          linestyle="none")
ax0R.text(VR + 0.12, -1.42, "two points", fontsize=10, color=WARM,
          ha="left", va="center")
ax0R.text(-1.60, 1.18, "$x^{2}+y^{2}=1$", fontsize=10, color=ACCENT,
          ha="left", va="center")


# ══════════════════════════════════════════════════════════
# (hlt) horizontal line test
# ══════════════════════════════════════════════════════════
for _ax in (axHL, axHR):
    _ax.set_xlim(-3.4, 3.4)
    _ax.set_ylim(-3.4, 5.2)
    _ax.axis("off")
    _ax.plot([-3.1, 3.1], [0, 0], color=FAINT, linewidth=1.0)
    _ax.plot([0, 0], [-3.1, 4.9], color=FAINT, linewidth=1.0)

# 左：y = 4x - 7 は one-to-one
axHL.set_title("one-to-one", fontsize=11, color=INK, loc="left", pad=8)
XH = np.linspace(1.0, 3.0, 50)
axHL.plot(XH, 4 * XH - 7, color=ACCENT, linewidth=2.0)
HL = 2.0
axHL.plot([-3.1, 3.1], [HL, HL], color=WARM, linewidth=1.3,
          linestyle=(0, (5, 3)))
axHL.plot([(HL + 7) / 4], [HL], marker="o", markersize=6, color=WARM)
axHL.text(-3.1, 3.9, "$y = 4x - 7$", fontsize=10, color=ACCENT,
          ha="left", va="center")
axHL.text(-3.1, 2.45, "one point", fontsize=10, color=WARM,
          ha="left", va="center")

# 右：y = x^2 は one-to-one でない
axHR.set_title("not one-to-one", fontsize=11, color=INK, loc="left", pad=8)
XQ = np.linspace(-2.2, 2.2, 300)
axHR.plot(XQ, XQ ** 2, color=ACCENT, linewidth=2.0)
HR = 2.6
axHR.plot([-3.1, 3.1], [HR, HR], color=WARM, linewidth=1.3,
          linestyle=(0, (5, 3)))
axHR.plot([-np.sqrt(HR), np.sqrt(HR)], [HR, HR], marker="o", markersize=6,
          color=WARM, linestyle="none")
axHR.text(-3.1, 4.7, "$y = x^{2}$", fontsize=10, color=ACCENT,
          ha="left", va="center")
axHR.text(0.15, 3.35, "two points", fontsize=10, color=WARM,
          ha="left", va="center")

# ══════════════════════════════════════════════════════════
# (a) domain と range
# ══════════════════════════════════════════════════════════
ax1.set_title("Domain on the $x$-axis, range on the $y$-axis",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(-4.6, 3.6)
ax1.set_ylim(-1.3, 3.2)
ax1.axis("off")

ax1.annotate("", xy=(3.4, 0), xytext=(-4.4, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 3.0), xytext=(0, -1.0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(3.5, -0.3, "$x$", fontsize=10, color=GREY, ha="center")
ax1.text(-0.28, 3.05, "$y$", fontsize=10, color=GREY, va="center")
ax1.text(2.0, -0.34, "$2$", fontsize=10, color=INK, ha="center")

xs = np.linspace(-4.0, 2.0, 200)
ax1.plot(xs, np.sqrt(2 - xs), color=ACCENT, linewidth=2.2)
ax1.plot([2.0], [0.0], marker="o", markersize=6, color=ACCENT, zorder=3)
ax1.text(-3.4, 2.65, "$y = \\sqrt{2-x}$", fontsize=12, color=ACCENT)

# domain（x 軸の太い部分）
ax1.plot([-4.2, 2.0], [-0.22, -0.22], color=WARM, linewidth=4.0,
         solid_capstyle="butt")
ax1.annotate("", xy=(-4.4, -0.22), xytext=(-4.0, -0.22),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.6))
ax1.text(-1.1, -0.72, "domain: $x \\leq 2$", fontsize=11, color=WARM,
         ha="center")

# range（y 軸の太い部分）
ax1.plot([-0.2, -0.2], [0.0, 2.9], color=WARM, linewidth=4.0,
         solid_capstyle="butt")
ax1.annotate("", xy=(-0.2, 3.05), xytext=(-0.2, 2.7),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.6))
ax1.text(-0.52, 1.15, "range:\n$y \\geq 0$", fontsize=11, color=WARM,
         ha="right", va="center")

ax1.plot([-4.2, 2.0], [0, 0], color=FAINT, linewidth=0.0)
ax1.text(-0.5, -1.22, "shadow on each axis", fontsize=9.5, color=INK,
         ha="center")

# ══════════════════════════════════════════════════════════
# (b) y = x について対称
# ══════════════════════════════════════════════════════════
ax2.set_title("The inverse is the reflection in $y = x$",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-0.5, 3.4)
ax2.set_ylim(-0.5, 3.4)
ax2.set_aspect("equal")
ax2.axis("off")

ax2.annotate("", xy=(3.3, 0), xytext=(-0.35, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 3.3), xytext=(0, -0.35),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(3.4, -0.28, "$x$", fontsize=10, color=GREY, ha="center")
ax2.text(-0.26, 3.35, "$y$", fontsize=10, color=GREY, va="center")

t = np.linspace(0, 1.72, 120)
ax2.plot(t, t ** 2, color=ACCENT, linewidth=2.2)
ax2.plot(t ** 2, t, color=WARM, linewidth=2.2)
d = np.linspace(-0.2, 3.15, 20)
ax2.plot(d, d, color=INK, linewidth=1.1, linestyle=(0, (5, 4)))

ax2.text(1.0, 2.75, "$y = f(x)$", fontsize=11, color=ACCENT)
ax2.text(2.9, 1.62, "$y = f^{-1}(x)$", fontsize=11, color=WARM,
         ha="center")
ax2.text(2.55, 2.85, "$y = x$", fontsize=10.5, color=INK)

# 対応する 2 点
A, B = 1.4, 1.96
ax2.plot([A], [B], marker="o", markersize=6, color=ACCENT, zorder=3)
ax2.plot([B], [A], marker="o", markersize=6, color=WARM, zorder=3)
ax2.plot([A, B], [B, A], color=GREY, linewidth=1.0, linestyle=(0, (3, 3)))
ax2.text(A - 0.12, B + 0.14, "$(a,\\,b)$", fontsize=10, color=ACCENT,
         ha="right")
ax2.text(B + 0.06, A - 0.34, "$(b,\\,a)$", fontsize=10, color=WARM,
         ha="left", va="top")


for _fig, _name in ((fig0, "aasl-2-2-vlt.svg"),
                    (fig1, "aasl-2-2-idea-a.svg"),
                    (figH, "aasl-2-2-hlt.svg"),
                    (fig2, "aasl-2-2-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
