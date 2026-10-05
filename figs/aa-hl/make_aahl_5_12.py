"""AA HL 5.12（連続性・微分可能性・第一原理）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_12.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_12.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-12-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-12-idea-b.svg

(a) つながっていない／穴がある／角がある、の 3 通り。
(b) 割線から接線へ：h を 0 に近づける。

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
# (a) つながっていない・穴・角
# ══════════════════════════════════════════════════════════
fig1, axs = plt.subplots(1, 3, figsize=(7.4, 2.6))
fig1.suptitle("three ways a graph can fail to be smooth", fontsize=11,
              color=INK, x=0.01, ha="left", y=1.03)

# 1. とび（jump）
ax = axs[0]
t1 = np.linspace(-1.6, 0, 200)
t2 = np.linspace(0, 1.6, 200)
ax.plot(t1, 0.6 * t1 + 0.4, color=ACCENT, linewidth=2.0)
ax.plot(t2, 0.6 * t2 - 0.9, color=ACCENT, linewidth=2.0)
ax.plot([0], [0.4], "o", color=ACCENT, markersize=5.5)
ax.plot([0], [-0.9], "o", color="white", markeredgecolor=ACCENT,
        markeredgewidth=1.5, markersize=5.5)
ax.set_title("a jump", fontsize=9.8, color=INK, loc="left", pad=4)
ax.text(-1.55, -2.1, "not continuous: the two sides", fontsize=8.4,
        color=GREY)
ax.text(-1.55, -2.45, "do not meet", fontsize=8.4, color=GREY)

# 2. 穴（hole）
ax = axs[1]
t = np.linspace(-1.6, 1.6, 400)
ax.plot(t, 0.7 * t, color=ACCENT, linewidth=2.0)
ax.plot([0.6], [0.42], "o", color="white", markeredgecolor=ACCENT,
        markeredgewidth=1.5, markersize=5.5)
ax.set_title("a hole", fontsize=9.8, color=INK, loc="left", pad=4)
ax.text(-1.55, -2.1, "not continuous: one value", fontsize=8.4, color=GREY)
ax.text(-1.55, -2.45, "is missing", fontsize=8.4, color=GREY)

# 3. 角（corner）
ax = axs[2]
ax.plot(t, np.abs(t) - 0.3, color=ACCENT, linewidth=2.0)
ax.plot([0], [-0.3], "o", color=ACCENT, markersize=5.5)
ax.set_title("a corner", fontsize=9.8, color=INK, loc="left", pad=4)
ax.text(-1.55, -2.1, "continuous, but the gradient", fontsize=8.4,
        color=GREY)
ax.text(-1.55, -2.45, "jumps from $-1$ to $+1$", fontsize=8.4, color=GREY)

for _ax in axs:
    _ax.set_xlim(-1.75, 1.75)
    _ax.set_ylim(-2.7, 1.6)
    _ax.plot([-1.72, 1.72], [0, 0], color=GREY, linewidth=0.8, zorder=0)
    _ax.plot([0, 0], [-1.45, 1.55], color=GREY, linewidth=0.8, zorder=0)
    _ax.set_xticks([])
    _ax.set_yticks([])
    for _s in ("top", "right", "bottom", "left"):
        _ax.spines[_s].set_visible(False)

# ══════════════════════════════════════════════════════════
# (b) 割線から接線へ
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 3.6))
ax2.set_title("the gradient of the chord, as $h$ shrinks to $0$",
              fontsize=10.5, color=INK, loc="left", pad=10)

t = np.linspace(-0.25, 2.5, 500)
ax2.plot(t, t ** 2, color=ACCENT, linewidth=2.0, zorder=3)
X0, H = 0.8, 1.3
P = (X0, X0 ** 2)
Q = (X0 + H, (X0 + H) ** 2)
_m = (Q[1] - P[1]) / (Q[0] - P[0])
_xs = np.array([X0 - 0.5, X0 + H + 0.45])
ax2.plot(_xs, P[1] + _m * (_xs - X0), color=WARM, linewidth=1.6, zorder=4)
_mt = 2 * X0
_xt = np.array([X0 - 0.55, X0 + 0.80])
ax2.plot(_xt, P[1] + _mt * (_xt - X0), color=GREY, linewidth=1.4,
         linestyle=(0, (4, 3)), zorder=4)
ax2.plot([P[0], Q[0]], [P[1], P[1]], color=GREY, linewidth=1.0,
         linestyle=(0, (2, 2)), zorder=2)
ax2.plot([Q[0], Q[0]], [P[1], Q[1]], color=GREY, linewidth=1.0,
         linestyle=(0, (2, 2)), zorder=2)
for _p, _lab, _dx, _dy in ((P, "$P$", -0.26, -0.10), (Q, "$Q$", 0.10, 0.02)):
    ax2.plot([_p[0]], [_p[1]], "o", color=INK, markersize=5, zorder=6)
    ax2.text(_p[0] + _dx, _p[1] + _dy, _lab, fontsize=10.5, color=INK)
ax2.text((P[0] + Q[0]) / 2 - 0.05, P[1] - 0.45, "$h$", fontsize=11,
         color=GREY)
ax2.text(Q[0] + 0.08, (P[1] + Q[1]) / 2, "$f(x+h) - f(x)$", fontsize=9.5,
         color=GREY)
ax2.text(0.05, 3.9, "chord", fontsize=10, color=WARM)
ax2.text(X0 + 0.84, P[1] + _mt * 0.80 - 0.10, "tangent", fontsize=10,
         color=GREY)
ax2.text(-0.35, -1.45, "the chord turns into the tangent as $Q$ slides"
         " back to $P$", fontsize=9, color=GREY)
ax2.set_xlim(-0.45, 3.3)
ax2.set_ylim(-1.8, 5.2)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.axhline(0, color=GREY, linewidth=0.8, zorder=0)
for _s in ("top", "right", "bottom", "left"):
    ax2.spines[_s].set_visible(False)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-12-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-12-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
