"""AA SL 2.1 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_1.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_1.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/../02-functions/img/aasl-2-1-idea.svg

(a) 傾きは rise / run。直線上のどの 2 点で測っても同じ。
(b) 平行なら傾きが等しい。垂直なら傾きは負の逆数。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（このページでは数値を一切書かない）。
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# ══════════════════════════════════════════════════════════
# (a) rise / run
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Gradient $=$ rise $\\div$ run", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-0.6, 6.4)
ax1.set_ylim(-0.9, 5.4)
ax1.axis("off")

# 軸
ax1.annotate("", xy=(6.2, 0), xytext=(-0.4, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 5.2), xytext=(0, -0.6),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(6.3, -0.28, "$x$", fontsize=10, color=GREY, ha="center")
ax1.text(-0.3, 5.25, "$y$", fontsize=10, color=GREY, va="center")

AX, AY, BX, BY = 1.2, 1.3, 4.7, 4.2
xs = np.linspace(0.15, 5.8, 50)
mm = (BY - AY) / (BX - AX)
ax1.plot(xs, AY + mm * (xs - AX), color=ACCENT, linewidth=2.0)

# rise / run の三角形
ax1.plot([AX, BX], [AY, AY], color=WARM, linewidth=1.5, linestyle=(0, (5, 3)))
ax1.plot([BX, BX], [AY, BY], color=WARM, linewidth=1.5, linestyle=(0, (5, 3)))
ax1.text((AX + BX) / 2, AY - 0.42, "run $= x_{2}-x_{1}$", ha="center",
         va="center", fontsize=10, color=WARM)
ax1.text(BX + 0.16, (AY + BY) / 2, "rise\n$= y_{2}-y_{1}$", ha="left",
         va="center", fontsize=10, color=WARM)

for px, py, lab, dy in [(AX, AY, "$A(x_{1},\\,y_{1})$", 0.30),
                        (BX, BY, "$B(x_{2},\\,y_{2})$", 0.30)]:
    ax1.plot([px], [py], marker="o", markersize=6, color=INK, zorder=3)
    ax1.text(px - 0.15, py + dy, lab, ha="right", va="bottom",
             fontsize=10, color=INK)

ax1.text(0.55, 4.55, "$m = \\dfrac{y_{2}-y_{1}}{x_{2}-x_{1}}$",
         ha="left", va="center", fontsize=13, color=ACCENT)
ax1.text(3.0, -0.78, "any two points on the line give the same $m$",
         ha="center", va="center", fontsize=9.5, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 平行と垂直
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Parallel and perpendicular", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-3.2, 3.2)
ax2.set_ylim(-3.2, 3.2)
ax2.set_aspect("equal")
ax2.axis("off")

ax2.plot([-3.0, 3.0], [0, 0], color=FAINT, linewidth=1.0)
ax2.plot([0, 0], [-3.0, 3.0], color=FAINT, linewidth=1.0)

M = 2.0
t = np.linspace(-1.35, 1.35, 40)
# 傾き m の直線（2 本、平行）
ax2.plot(t, M * t, color=ACCENT, linewidth=2.0)
ax2.plot(t, M * t + 2.0, color=ACCENT, linewidth=2.0, linestyle=(0, (6, 3)))
# 傾き -1/m の直線
s = np.linspace(-2.9, 2.9, 40)
ax2.plot(s, -s / M, color=WARM, linewidth=2.0)

ax2.text(1.45, 2.55, "gradient $m$", fontsize=10, color=ACCENT, ha="left")
ax2.text(-2.9, -2.05, "gradient $m$", fontsize=10, color=ACCENT, ha="left")
ax2.text(2.05, -1.35, "gradient $-\\dfrac{1}{m}$", fontsize=11, color=WARM,
         ha="left", va="center")

# 直角の印
d = 0.36
u = np.array([1.0, M]) / np.hypot(1.0, M) * d
v = np.array([1.0, -1.0 / M]) / np.hypot(1.0, 1.0 / M) * d
ax2.plot([u[0], u[0] + v[0], v[0]], [u[1], u[1] + v[1], v[1]],
         color=INK, linewidth=1.2)

ax2.text(0.0, -2.85, "parallel: $m_{1}=m_{2}$      "
         "perpendicular: $m_{1}m_{2}=-1$",
         ha="center", va="center", fontsize=10, color=INK)

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-2-1-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
