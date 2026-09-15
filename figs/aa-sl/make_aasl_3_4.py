"""AA SL 3.4 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_4.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_4.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-4-idea.svg

(a) ラジアンの定義。半径と同じ長さの弧に対する中心角が 1 ラジアン。
(b) 扇形。弧の長さと面積。弦を引くと弓形が見える。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（角は θ、半径は r で書く）。
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.9))

# ══════════════════════════════════════════════════════════
# (a) ラジアンの定義
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) One radian", fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(-1.55, 1.75)
ax1.set_ylim(-1.45, 1.85)
ax1.set_aspect("equal")
ax1.axis("off")

t = np.linspace(0, 2 * np.pi, 400)
ax1.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.2)

one = 1.0  # 1 radian
ta = np.linspace(0, one, 120)
ax1.plot(np.cos(ta), np.sin(ta), color=ACCENT, linewidth=3.4,
         solid_capstyle="round")

ax1.plot([0, 1], [0, 0], color=INK, linewidth=1.8)
ax1.plot([0, np.cos(one)], [0, np.sin(one)], color=INK, linewidth=1.8)
ax1.plot([0], [0], marker="o", markersize=4.5, color=INK, zorder=3)

tb = np.linspace(0, one, 60)
ax1.plot(0.28 * np.cos(tb), 0.28 * np.sin(tb), color=GREEN, linewidth=1.4)
ax1.text(0.33, 0.12, "$1$", fontsize=12, color=GREEN)

ax1.text(0.46, -0.20, "$r$", fontsize=12, color=INK)
ax1.text(0.16, 0.52, "$r$", fontsize=12, color=INK)
ax1.text(1.02, 0.62, "arc of length $r$", fontsize=10, color=ACCENT)

ax1.text(-1.55, 1.62, "the angle at the centre cut off by an arc",
         fontsize=10, color=INK)
ax1.text(-1.55, 1.34, "as long as the radius is one radian",
         fontsize=10, color=INK)
ax1.text(-1.55, -1.40, "a whole turn is $2\\pi$ radians", fontsize=9.5,
         color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 扇形と弓形
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Sector and segment", fontsize=11, color=INK, loc="left",
              pad=10)
ax2.set_xlim(-1.6, 2.05)
ax2.set_ylim(-1.45, 1.85)
ax2.set_aspect("equal")
ax2.axis("off")

ax2.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.0, linestyle=(0, (4, 4)))

th = 1.9
ts = np.linspace(0, th, 200)
ax2.fill(np.concatenate([[0], np.cos(ts), [0]]),
         np.concatenate([[0], np.sin(ts), [0]]),
         color=ACCENT, alpha=0.13, linewidth=0)
ax2.plot(np.cos(ts), np.sin(ts), color=ACCENT, linewidth=3.0,
         solid_capstyle="round")
ax2.plot([0, 1], [0, 0], color=INK, linewidth=1.8)
ax2.plot([0, np.cos(th)], [0, np.sin(th)], color=INK, linewidth=1.8)
ax2.plot([0], [0], marker="o", markersize=4.5, color=INK, zorder=3)

# 弓形（弦と弧のあいだ）
ax2.fill(np.concatenate([np.cos(ts), [1]]),
         np.concatenate([np.sin(ts), [0]]),
         color=WARM, alpha=0.16, linewidth=0)
# 弦（弓形の境）
ax2.plot([1, np.cos(th)], [0, np.sin(th)], color=WARM, linewidth=1.7,
         linestyle=(0, (5, 3)))

tc = np.linspace(0, th, 60)
ax2.plot(0.26 * np.cos(tc), 0.26 * np.sin(tc), color=GREEN, linewidth=1.4)
ax2.text(0.13, 0.34, "$\\theta$", fontsize=12, color=GREEN)

ax2.text(0.47, -0.21, "$r$", fontsize=12, color=INK)
ax2.text(1.05, 0.98, "arc $l = r\\theta$", fontsize=10.5, color=ACCENT)
ax2.text(1.05, 0.62, "sector $A = \\frac{1}{2}r^{2}\\theta$", fontsize=10.5,
         color=ACCENT)
ax2.text(0.16, 0.70, "segment", fontsize=10, color=WARM)

ax2.text(-1.6, 1.62, "the chord cuts the sector into a triangle",
         fontsize=10, color=INK)
ax2.text(-1.6, 1.34, "and a segment", fontsize=10, color=INK)
ax2.text(-1.6, -1.40, "both formulas need $\\theta$ in radians",
         fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-3-4-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
