"""AA HL 5.18a（1 階微分方程式：Euler 法と変数分離）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_18a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_18a.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-18a-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-18a-idea-b.svg

(a) Euler 法：傾きの場の上を、短い直線でつないでいく。
(b) ロジスティック曲線：S 字で、上限に近づく。

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
# (a) Euler 法
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.8, 3.6))
ax1.set_title("Euler's method follows the slope field in straight steps",
              fontsize=10.2, color=INK, loc="left", pad=10)


def slope(x, y):
    return 0.6 * (x + y)


for _gx in np.arange(0.0, 2.51, 0.5):
    for _gy in np.arange(0.4, 3.21, 0.45):
        _m = slope(_gx, _gy)
        _d = 0.18 / np.sqrt(1 + _m ** 2)
        ax1.plot([_gx - _d, _gx + _d], [_gy - _d * _m, _gy + _d * _m],
                 color=GREY, linewidth=0.9, zorder=1)

# 本当の解（数値積分）
_xs = np.linspace(0, 3.0, 400)
_ys = [1.0]
for i in range(1, len(_xs)):
    _hh = _xs[i] - _xs[i - 1]
    _k1 = slope(_xs[i - 1], _ys[-1])
    _k2 = slope(_xs[i - 1] + _hh, _ys[-1] + _hh * _k1)
    _ys.append(_ys[-1] + _hh * (_k1 + _k2) / 2)
_keep = [i for i in range(len(_xs)) if _ys[i] <= 3.9]
ax1.plot(_xs[_keep], [_ys[i] for i in _keep], color=ACCENT,
         linewidth=2.0, zorder=3)

# Euler（h を大きめにして、ずれを見せる）
_h = 0.6
_ex, _ey = [0.0], [1.0]
while _ey[-1] < 3.4:
    _ey.append(_ey[-1] + _h * slope(_ex[-1], _ey[-1]))
    _ex.append(_ex[-1] + _h)
ax1.plot(_ex, _ey, color=WARM, linewidth=1.8, marker="o", markersize=4.5,
         zorder=4)

ax1.text(0.05, 3.55, "true solution", fontsize=9.5, color=ACCENT)
ax1.text(1.95, 1.05, "Euler steps", fontsize=9.5, color=WARM)
ax1.text(-0.12, -0.72, "each step uses the gradient at the point it starts"
         " from, so error builds up", fontsize=9, color=GREY)
ax1.set_xlim(-0.25, 3.1)
ax1.set_ylim(-1.05, 4.2)
ax1.set_xticks([0, 1, 2])
ax1.set_yticks([])
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.tick_params(labelsize=9, colors=GREY)

# ══════════════════════════════════════════════════════════
# (b) ロジスティック曲線
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.6, 3.2))
ax2.set_title("the logistic curve: fast in the middle, flat at both ends",
              fontsize=10.2, color=INK, loc="left", pad=10)

t = np.linspace(0, 1.0, 500)
A = 100.0
N = A / (1 + 9 * np.exp(-10 * t))
ax2.plot(t, N, color=ACCENT, linewidth=2.2, zorder=3)
ax2.plot([0, 1.0], [A, A], color=GREY, linewidth=1.2,
         linestyle=(0, (4, 3)), zorder=2)
ax2.plot([0, 1.0], [A / 2, A / 2], color=WARM, linewidth=1.0,
         linestyle=(0, (2, 2)), zorder=2)
ax2.text(0.72, A + 4, "the ceiling $a$", fontsize=9.5, color=GREY)
ax2.text(0.60, A / 2 + 4, "steepest at half the ceiling", fontsize=9.2,
         color=WARM)
ax2.text(-0.02, -34, "growth slows as $n$ approaches $a$, because the"
         " factor $a-n$ shrinks", fontsize=9, color=GREY)
ax2.set_xlim(-0.03, 1.05)
ax2.set_ylim(-45, 122)
ax2.set_xlabel("$t$", fontsize=10, color=INK)
ax2.set_ylabel("$n$", fontsize=10, color=INK)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-18a-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-18a-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
