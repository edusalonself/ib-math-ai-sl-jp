"""AA HL 5.14（陰関数微分・関連する変化率・最適化）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_14.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_14.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-14-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-14-idea-b.svg

(a) 円は 1 つの関数のグラフではない。それでも各点に接線がある。
(b) 関連する変化率：はしごの問題。x と y は時刻でつながっている。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → 使わない
  * \\lvert \\rvert も読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

# ══════════════════════════════════════════════════════════
# (a) 円と接線
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.2, 3.8))
ax1.set_title("a circle is not the graph of one function, yet every point"
              " has a tangent", fontsize=9.6, color=INK, loc="left", pad=10)

th = np.linspace(0, 2 * np.pi, 600)
ax1.plot(5 * np.cos(th), 5 * np.sin(th), color=ACCENT, linewidth=2.0,
         zorder=3)
P = np.array([3.0, 4.0])
ax1.plot([0, P[0]], [0, P[1]], color=GREY, linewidth=1.3, zorder=3)
_ts = np.array([-3.2, 3.2])
ax1.plot(P[0] + _ts * 4 / 5, P[1] - _ts * 3 / 5, color=WARM, linewidth=1.8,
         zorder=4)
ax1.plot([P[0]], [P[1]], "o", color=INK, markersize=5, zorder=5)
ax1.text(P[0] + 0.18, P[1] + 0.22, "$P$", fontsize=11, color=INK)
ax1.text(1.90, 1.55, "radius", fontsize=9.5, color=GREY)
ax1.text(5.35, 2.35, "tangent", fontsize=9.5, color=WARM)
ax1.plot([-2.8, 2.8], [3.0, 3.0], color=GREY, linewidth=1.0,
         linestyle=(0, (3, 3)), zorder=2)
ax1.text(-6.9, -5.35, "one value of $x$ can give", fontsize=8.8,
         color=GREY)
ax1.text(-6.9, -5.95, "two values of $y$", fontsize=8.8, color=GREY)
ax1.plot([-4.0], [3.0], "o", color=ACCENT, markersize=4.5, zorder=5)
ax1.plot([-4.0], [-3.0], "o", color=ACCENT, markersize=4.5, zorder=5)
ax1.plot([-4.0, -4.0], [-3.0, 3.0], color=GREY, linewidth=1.0,
         linestyle=(0, (3, 3)), zorder=2)
ax1.set_xlim(-7.0, 8.4)
ax1.set_ylim(-6.6, 6.6)
ax1.set_aspect("equal")
ax1.plot([-5.8, 5.8], [0, 0], color=GREY, linewidth=0.8, zorder=0)
ax1.plot([0, 0], [-5.8, 5.8], color=GREY, linewidth=0.8, zorder=0)
ax1.set_xticks([])
ax1.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax1.spines[_s].set_visible(False)

# ══════════════════════════════════════════════════════════
# (b) 関連する変化率（はしご）
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.4, 3.6))
ax2.set_title("related rates: $x$ and $y$ are tied together by the"
              " ladder", fontsize=10.2, color=INK, loc="left", pad=10)

X0, Y0 = 3.0, 4.0
ax2.plot([0, 0], [0, 5.4], color=GREY, linewidth=2.2, zorder=2)
ax2.plot([-0.4, 5.6], [0, 0], color=GREY, linewidth=2.2, zorder=2)
ax2.plot([0, X0], [Y0, 0], color=ACCENT, linewidth=2.4, zorder=3)
ax2.plot([0, X0], [0, 0], color=INK, linewidth=1.2, zorder=4)
ax2.plot([0, 0], [0, Y0], color=INK, linewidth=1.2, zorder=4)
ax2.plot([0.32, 0.32, 0], [0, 0.32, 0.32], color=INK, linewidth=1.0,
         zorder=4)
ax2.text(X0 / 2 - 0.08, -0.52, "$x$", fontsize=11, color=INK)
ax2.text(-0.42, Y0 / 2, "$y$", fontsize=11, color=INK)
ax2.text(1.75, 2.35, "$L$", fontsize=11, color=ACCENT)
ax2.annotate("", xy=(X0 + 1.0, 0), xytext=(X0 + 0.15, 0),
             arrowprops=dict(arrowstyle="-|>", color=WARM, linewidth=1.8))
ax2.annotate("", xy=(0, Y0 - 1.0), xytext=(0, Y0 - 0.15),
             arrowprops=dict(arrowstyle="-|>", color=WARM, linewidth=1.8))
ax2.text(X0 + 0.20, 0.28, "$\\frac{dx}{dt}$", fontsize=11, color=WARM)
ax2.text(0.20, Y0 - 1.50, "$\\frac{dy}{dt}$", fontsize=11, color=WARM)
ax2.text(-0.5, -1.55, "$x^{2} + y^{2} = L^{2}$ holds at every moment,"
         " so differentiating with", fontsize=9, color=GREY)
ax2.text(-0.5, -2.05, "respect to $t$ links the two rates", fontsize=9,
         color=GREY)
ax2.set_xlim(-1.1, 6.4)
ax2.set_ylim(-2.5, 5.8)
ax2.set_aspect("equal")
ax2.set_xticks([])
ax2.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax2.spines[_s].set_visible(False)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-14-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-14-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
