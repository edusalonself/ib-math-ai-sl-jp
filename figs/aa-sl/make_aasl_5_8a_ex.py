"""AA SL 5.8a の第 6 節の図（$f''(a) = 0$ だけでは足りない）。

    python3 figs/aa-sl/make_aasl_5_8a_ex.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_8a_ex.py

出力: aa-sl/05-calculus/img/aasl-5-8a-ex.svg

左: y = x^4。原点で f'' = 0 だが、f'' は符号を変えない（シラバスが名指しした例）。
右: y = x^3。原点で f'' = 0 で、f'' が符号を変える。

matplotlib の mathtext の制限は make_aasl_5_8a.py の docstring を見てください。

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

X = np.linspace(-1.35, 1.35, 400)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.2))

PANELS = ((ax1, X ** 4, WARM, "$y = x^{4}$", (-0.9, 3.4),
           "$f''$ does not change sign", "not a point of inflexion"),
          (ax2, X ** 3, ACCENT, "$y = x^{3}$", (-2.6, 2.6),
           "$f''$ changes sign", "a point of inflexion"))

for _ax, _y, _c, _t, _lim, _s1, _s2 in PANELS:
    _ax.plot(X, _y, color=_c, linewidth=2.2)
    _ax.axhline(0, color=GREY, linewidth=0.9)
    _ax.axvline(0, color=GREY, linewidth=0.9)
    _ax.plot([0], [0], "o", color=INK, markersize=6, zorder=5)
    _ax.set_xlim(-1.45, 1.45)
    _ax.set_ylim(*_lim)
    _ax.set_xticks([])
    _ax.set_yticks([])
    for _s in ("top", "right", "left", "bottom"):
        _ax.spines[_s].set_visible(False)
    _ax.set_title(_t, fontsize=12, color=_c, loc="left", pad=12)
    _ax.annotate("$(0,\\,0)$", xy=(0, 0), xytext=(9, -15),
                 textcoords="offset points", fontsize=9.5, color=GREY)
    _ax.text(0.5, -0.10, "$f''(0) = 0$", transform=_ax.transAxes,
             fontsize=10.5, color=INK, ha="center", va="top")
    _ax.text(0.5, -0.22, _s1, transform=_ax.transAxes, fontsize=10,
             color=_c, ha="center", va="top")
    _ax.text(0.5, -0.34, _s2, transform=_ax.transAxes, fontsize=10,
             color=INK, ha="center", va="top")

fig.tight_layout(w_pad=3.0, rect=(0, 0.10, 1, 1))
path = os.path.join(OUT, "aasl-5-8a-ex.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
