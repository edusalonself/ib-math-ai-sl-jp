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
# (a) 傾きの場（slope field）と解の曲線
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.0, 3.4))


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

ax1.text(0.05, 3.55, "solution curve", fontsize=9.5, color=ACCENT)
ax1.set_xlim(-0.25, 2.75)
ax1.set_ylim(0.0, 4.0)
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

t = np.linspace(0, 1.0, 500)
A = 100.0
N = A / (1 + 9 * np.exp(-10 * t))
ax2.plot(t, N, color=ACCENT, linewidth=2.2, zorder=3)
ax2.plot([0, 1.0], [A, A], color=GREY, linewidth=1.2,
         linestyle=(0, (4, 3)), zorder=2)
ax2.plot([0, 1.0], [A / 2, A / 2], color=WARM, linewidth=1.0,
         linestyle=(0, (2, 2)), zorder=2)
ax2.text(0.72, A + 4, "the ceiling $a$", fontsize=9.5, color=GREY)
ax2.set_xlim(-0.03, 1.05)
ax2.set_ylim(-45, 122)
ax2.set_xlabel("$t$", fontsize=10, color=INK)
ax2.set_ylabel("$n$", fontsize=10, color=INK)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)


# ══════════════════════════════════════════════════════════
# (c) Euler 法を 3 回：本当の曲線と、折れ線
# ══════════════════════════════════════════════════════════
fig3, ax3 = plt.subplots(figsize=(5.4, 3.6))
_xs = np.linspace(0, 1.25, 300)
ax3.plot(_xs, 2 * np.exp(_xs) - _xs - 1, color=ACCENT, linewidth=2.0, zorder=3)
_h = 0.4
_px, _py = [0.0], [1.0]
for _k in range(3):
    _py.append(_py[-1] + _h * (_px[-1] + _py[-1]))
    _px.append(_px[-1] + _h)
ax3.plot(_px, _py, color=WARM, linewidth=1.8, zorder=4)
ax3.plot(_px, _py, "o", color=WARM, markersize=5, zorder=5)
for _k in range(4):
    ax3.text(_px[_k] + 0.03, _py[_k] - 0.28, "$(x_{%d},\\ y_{%d})$" % (_k, _k),
             fontsize=9.5, color=WARM)
# h の目盛り
for _k in range(3):
    ax3.annotate("", xy=(_px[_k + 1], 0.35), xytext=(_px[_k], 0.35),
                 arrowprops=dict(arrowstyle="<|-|>", color=GREY, linewidth=1.0))
    ax3.text((_px[_k] + _px[_k + 1]) / 2 - 0.02, 0.45, "$h$", fontsize=10,
             color=GREY)
ax3.text(0.78, 4.3, "solution", fontsize=10, color=ACCENT)
ax3.set_xlim(-0.1, 1.4)
ax3.set_ylim(0.2, 5.3)
ax3.set_xticks([])
ax3.set_yticks([])
for _sp in ("top", "right", "left"):
    ax3.spines[_sp].set_visible(False)
ax3.set_xlabel("$x$", fontsize=10, color=INK)

for _fig, _name in ((fig1, "a"), (fig2, "b"), (fig3, "c")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-18a-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-18a-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
