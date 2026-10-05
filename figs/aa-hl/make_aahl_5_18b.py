"""AA HL 5.18b（同次形と積分因子）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_18b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_18b.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-18b-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-18b-idea-b.svg

(a) どの方法を使うかの流れ図。
(b) 1 次の微分方程式の解の族：C がちがっても、同じ曲線に近づく。

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
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

# ══════════════════════════════════════════════════════════
# (a) どの方法を使うか
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(6.4, 3.4))
ax1.set_title("which method for a first order equation?", fontsize=10.5,
              color=INK, loc="left", pad=10)


def box(x, y, w, h, text, col, fs=9.0):
    ax1.add_patch(FancyBboxPatch((x, y), w, h,
                                 boxstyle="round,pad=0.10,rounding_size=0.12",
                                 facecolor="white", edgecolor=col,
                                 linewidth=1.4, zorder=2))
    ax1.text(x + w / 2, y + h / 2, text, fontsize=fs, color=INK,
             ha="center", va="center", zorder=3)


def link(p, q, label="", dx=0.0, dy=0.14):
    ax1.annotate("", xy=q, xytext=p,
                 arrowprops=dict(arrowstyle="-|>", color=GREY, linewidth=1.3,
                                 shrinkA=2, shrinkB=2))
    if label:
        ax1.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, label,
                 fontsize=8.6, color=GREY, ha="center",
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.0))


box(0.2, 4.3, 3.2, 0.8, "is it $g(x)\\,h(y)$?", ACCENT, fs=9.4)
box(0.2, 2.5, 3.2, 0.8, "is it $f\\!\\left(\\frac{y}{x}\\right)$?", ACCENT,
    fs=9.4)
box(0.2, 0.7, 3.2, 0.8, "is it $y' + P(x)y = Q(x)$?", ACCENT, fs=9.0)
box(4.6, 4.3, 3.6, 0.8, "separate the variables", WARM, fs=9.4)
box(4.6, 2.5, 3.6, 0.8, "substitute $y = vx$", WARM, fs=9.4)
box(4.6, 0.7, 3.6, 0.8, "use the integrating factor", WARM, fs=9.4)

for _y in (4.7, 2.9, 1.1):
    link((3.5, _y), (4.5, _y), "yes", dy=0.16)
link((1.8, 4.3), (1.8, 3.4), "no", dx=0.30, dy=0.0)
link((1.8, 2.5), (1.8, 1.6), "no", dx=0.30, dy=0.0)

ax1.text(0.0, -0.35, "check them in this order: the first test that passes"
         " gives the method", fontsize=9, color=GREY)
ax1.set_xlim(-0.2, 8.8)
ax1.set_ylim(-0.8, 5.5)
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 解の族
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.4, 3.2))
ax2.set_title("solutions of a linear equation: different $C$, same"
              " long-run behaviour", fontsize=9.8, color=INK, loc="left",
              pad=10)

t = np.linspace(0, 4.0, 400)
for _c, _col in ((-1.0, GREY), (0.0, ACCENT), (2.0, WARM), (4.0, GREY)):
    ax2.plot(t, t - 1 + _c * np.exp(-t), color=_col, linewidth=1.7, zorder=3)
ax2.plot(t, t - 1, color=INK, linewidth=1.3, linestyle=(0, (4, 3)), zorder=4)
ax2.text(3.15, 3.40, "$y = x-1$", fontsize=9.5, color=INK)
ax2.text(0.06, 3.45, "each curve is $y = x-1+Ce^{-x}$", fontsize=9,
         color=GREY)
ax2.text(0.06, -2.65, "the term with $C$ dies away, so all solutions"
         " approach the same line", fontsize=9, color=GREY)
ax2.set_xlim(-0.15, 4.5)
ax2.set_ylim(-3.15, 4.0)
ax2.set_xlabel("$x$", fontsize=10, color=INK)
ax2.set_xticks([0, 1, 2, 3, 4])
ax2.set_yticks([])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.tick_params(labelsize=9, colors=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-18b-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-18b-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
