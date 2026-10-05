"""AA SL 3.7a の図をつくる。

    python3 figs/aa-sl/make_aasl_3_7a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_7a.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-7a-idea-a.svg
      aa-sl/03-geometry/img/aasl-3-7a-idea-b.svg

(a) y = sin x と y = cos x。同じ形が π/2 ずれている。
(b) y = tan x。周期は π で、漸近線がある。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
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
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig1, ax1 = plt.subplots(figsize=(5.4, 4.4))
fig2, ax2 = plt.subplots(figsize=(5.4, 4.4))
PIL = ["$-2\\pi$", "$-\\pi$", "$0$", "$\\pi$", "$2\\pi$"]

# ══════════════════════════════════════════════════════════
# (a) sin と cos
# ══════════════════════════════════════════════════════════
ax1.set_title("$y = \\sin x$ and $y = \\cos x$", fontsize=11, color=INK,
              loc="left", pad=10)
x = np.linspace(-2 * np.pi, 2 * np.pi, 800)
ax1.plot(x, np.sin(x), color=ACCENT, linewidth=2.2, label="$y = \\sin x$")
ax1.plot(x, np.cos(x), color=WARM, linewidth=2.0, linestyle=(0, (6, 3)),
         label="$y = \\cos x$")
ax1.axhline(0, color=GREY, linewidth=1.0)
ax1.axvline(0, color=GREY, linewidth=1.0)
ax1.axhline(1, color=GREEN, linewidth=0.9, linestyle=(0, (2, 3)))
ax1.axhline(-1, color=GREEN, linewidth=0.9, linestyle=(0, (2, 3)))
ax1.set_xlim(-2 * np.pi - 0.4, 2 * np.pi + 0.4)
ax1.set_ylim(-1.40, 2.05)
ax1.set_xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi])
ax1.set_xticklabels(PIL, fontsize=9.5)
ax1.set_yticks([-1, 0, 1])
ax1.set_yticklabels(["$-1$", "$0$", "$1$"], fontsize=9.5)
for _sp in ("top", "right", "left", "bottom"):
    ax1.spines[_sp].set_visible(False)
ax1.tick_params(length=0, colors=GREY)
ax1.legend(loc="upper center", ncol=2, frameon=False, fontsize=10,
           bbox_to_anchor=(0.5, 1.03))

# ══════════════════════════════════════════════════════════
# (b) tan
# ══════════════════════════════════════════════════════════
ax2.set_title("$y = \\tan x$", fontsize=11, color=INK, loc="left", pad=10)
for k in (-2, -1, 0, 1):
    lo = (k + 0.5) * np.pi + 0.02
    hi = (k + 1.5) * np.pi - 0.02
    xs = np.linspace(lo, hi, 400)
    ax2.plot(xs, np.tan(xs), color=ACCENT, linewidth=2.2)
for k in (-2, -1, 0, 1):
    ax2.axvline((k + 0.5) * np.pi, color=WARM, linewidth=1.1,
                linestyle=(0, (5, 4)))
ax2.axhline(0, color=GREY, linewidth=1.0)
ax2.axvline(0, color=GREY, linewidth=1.0)
ax2.set_xlim(-1.7 * np.pi, 1.7 * np.pi)
ax2.set_ylim(-6.0, 6.8)
ax2.set_xticks([-np.pi, 0, np.pi])
ax2.set_xticklabels(["$-\\pi$", "$0$", "$\\pi$"], fontsize=9.5)
ax2.set_yticks([-3, 0, 3])
ax2.set_yticklabels(["$-3$", "$0$", "$3$"], fontsize=9.5)
for _sp in ("top", "right", "left", "bottom"):
    ax2.spines[_sp].set_visible(False)
ax2.tick_params(length=0, colors=GREY)
ax2.text(np.pi / 2 + 0.14, 5.2, "asymptote", fontsize=9.5, color=WARM)
ax2.text(-1.7 * np.pi, 5.9, "repeats every $\\pi$", fontsize=10, color=INK)

for _fig, _name in ((fig1, "aasl-3-7a-idea-a.svg"), (fig2, "aasl-3-7a-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
