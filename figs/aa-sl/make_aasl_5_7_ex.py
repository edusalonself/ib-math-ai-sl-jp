"""AA SL 5.7 の例題 4 の図をつくる（A・B・C の 3 つのグラフ）。

    python3 figs/aa-sl/make_aasl_5_7_ex.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_7_ex.py

出力: aa-sl/05-calculus/img/aasl-5-7-ex.svg

もとの関数は f(x) = x^3/3 - x。並び順は P = f'、Q = f''、R = f。
★ どれがどれかは図に書きません（それが問題だからです）。

matplotlib の mathtext の制限は make_aasl_5_7.py の docstring を見てください。

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

X = np.linspace(-2.2, 2.2, 400)
CURVES = (("P", X ** 2 - 1, ACCENT, (-1.9, 4.2), True),
          ("Q", 2 * X, WARM, (-5.0, 5.0), False),
          ("R", X ** 3 / 3 - X, INK, (-1.9, 1.9), True))

fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.6))

for _ax, (_name, _y, _c, _lim, _dash) in zip(axes, CURVES):
    _ax.plot(X, _y, color=_c, linewidth=2.0)
    _ax.axhline(0, color=GREY, linewidth=0.9)
    _ax.axvline(0, color=GREY, linewidth=0.9)
    _ax.set_xlim(-2.3, 2.3)
    _ax.set_ylim(*_lim)
    _ax.set_xticks([-1, 1])
    _ax.set_yticks([])
    for _s in ("top", "right", "left", "bottom"):
        _ax.spines[_s].set_visible(False)
    _ax.tick_params(axis="x", colors=GREY, labelsize=9, length=0)
    _ax.set_title("Graph " + _name, fontsize=11.5, color=_c, loc="left",
                  pad=10)
    _ax.set_xlabel("$x$", fontsize=10, color=GREY, labelpad=2)
    if _dash:
        for _v in (-1, 1):
            _ax.axvline(_v, color=GREY, linewidth=0.7, linestyle=(0, (3, 3)),
                        alpha=0.7)

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-5-7-ex.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
