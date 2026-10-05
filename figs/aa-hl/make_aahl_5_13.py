"""AA HL 5.13（不定形と l'Hôpital の定理）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_13.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_13.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-13-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-13-idea-b.svg

(a) 同じ点で 0 になる 2 曲線は、その近くでは接線とほぼ同じ。
    だから比は、傾きの比に近づく。
(b) sin x / x は x = 0 に穴があり、値は 1 に近づく。

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
# (a) 0 になる点の近くでは、接線とほぼ同じ
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.8, 3.4))
ax1.set_title("near a common zero, each curve looks like its tangent",
              fontsize=10.5, color=INK, loc="left", pad=10)

t = np.linspace(-1.35, 1.0, 500)
F = 1.6 * t + 0.8 * t ** 2
G = 0.8 * t - 0.5 * t ** 3
ax1.plot(t, F, color=ACCENT, linewidth=2.0, zorder=3)
ax1.plot(t, G, color=WARM, linewidth=2.0, zorder=3)
_ts = np.linspace(-0.85, 0.85, 2)
ax1.plot(_ts, 1.6 * _ts, color=ACCENT, linewidth=1.2,
         linestyle=(0, (4, 3)), zorder=2)
ax1.plot(_ts, 0.8 * _ts, color=WARM, linewidth=1.2,
         linestyle=(0, (4, 3)), zorder=2)
ax1.plot([0], [0], "o", color=INK, markersize=5, zorder=5)
ax1.text(0.06, -0.38, "$a$", fontsize=10.5, color=INK)
ax1.text(1.06, 2.32, "$y = f(x)$", fontsize=10, color=ACCENT)
ax1.text(1.06, 0.22, "$y = g(x)$", fontsize=10, color=WARM)
ax1.text(-1.45, -2.05, "both are $0$ at $x = a$, so the quotient is"
         " $\\frac{0}{0}$ there", fontsize=9, color=GREY)
ax1.text(-1.45, -2.50, "but the ratio of the tangents is"
         " $\\frac{f'(a)}{g'(a)}$", fontsize=9, color=GREY)
ax1.set_xlim(-1.6, 2.4)
ax1.set_ylim(-2.9, 2.6)
ax1.plot([-1.45, 1.10], [0, 0], color=GREY, linewidth=0.8, zorder=0)
ax1.plot([0, 0], [-1.35, 2.45], color=GREY, linewidth=0.8, zorder=0)
ax1.set_xticks([])
ax1.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax1.spines[_s].set_visible(False)

# ══════════════════════════════════════════════════════════
# (b) sin x / x
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 3.0))
ax2.set_title("$y = \\frac{\\sin x}{x}$ has a hole at $x = 0$, and the"
              " values approach $1$", fontsize=10.2, color=INK, loc="left",
              pad=10)

u = np.linspace(-11, 11, 1400)
u = u[np.abs(u) > 1e-6]
ax2.plot(u, np.sin(u) / u, color=ACCENT, linewidth=2.0, zorder=3)
ax2.plot([0], [1], "o", color="white", markeredgecolor=ACCENT,
         markeredgewidth=1.6, markersize=6.5, zorder=5)
ax2.plot([-11, 11], [1, 1], color=GREY, linewidth=1.0,
         linestyle=(0, (4, 3)), zorder=2)
ax2.text(4.4, 1.10, "the values approach $1$", fontsize=9.5, color=GREY)
ax2.set_xlim(-11.5, 11.5)
ax2.set_ylim(-0.45, 1.45)
ax2.set_xticks([-3 * np.pi, -2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi,
                3 * np.pi])
ax2.set_xticklabels(["$-3\\pi$", "$-2\\pi$", "$-\\pi$", "$0$", "$\\pi$",
                     "$2\\pi$", "$3\\pi$"])
ax2.set_yticks([0, 1])
ax2.axhline(0, color=GREY, linewidth=0.8, zorder=0)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.tick_params(labelsize=9, colors=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-13-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-13-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
