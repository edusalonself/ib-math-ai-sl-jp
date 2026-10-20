"""AA HL 2.16（絶対値・逆数などのグラフの変換）の図をつくる。

    python3 figs/aa-hl/make_aahl_2_16.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_2_16.py  … 目視用の PNG も

出力: aa-hl/02-functions/img/aahl-2-16-abs.svg / -fabs.svg / -sq.svg
      aa-hl/02-functions/img/aahl-2-16-idea-b.svg

(a) |f(x)|、f(|x|)、[f(x)]^2 を 1 枚ずつ（もとの f を点線で重ねる）。各節に 1 枚ずつ置く。
(b) y = f(x) と y = 1/f(x)：0 が漸近線に、±1 が交点になる。

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
OUT = os.path.join(HERE, "..", "..", "aa-hl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"


def frame(ax):
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GREY)
    ax.spines["bottom"].set_color(GREY)
    ax.set_xticks([])
    ax.set_yticks([])


# ══════════════════════════════════════════════════════════
# (a) 3 つの変換を、1 枚ずつ（もとの f は点線で重ねる）
# ══════════════════════════════════════════════════════════
def base(t):
    return t * t - 2.0 * t - 3.0


def one_panel(title, lab, t, yv, ylim):
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    ax.plot(t, base(t), color=ACCENT, linewidth=1.2, linestyle=(0, (4, 3)))
    ax.plot(t, yv, color=WARM, linewidth=1.9)
    ax.set_xlim(t[0] - 0.2, t[-1] + 0.2)
    ax.set_ylim(*ylim)
    frame(ax)
    ax.text(0.98, 0.97, lab, transform=ax.transAxes, ha="right", va="top",
            fontsize=9.5, color=WARM)
    ax.text(0.98, 0.87, "dashed: $y=f(x)$", transform=ax.transAxes,
            ha="right", va="top", fontsize=9, color=ACCENT)
    return fig


_t = np.linspace(-4.2, 4.2, 600)
fig_abs = one_panel("The part below the axis is reflected upwards",
                    "$y=|f(x)|$", _t, np.abs(base(_t)), (-5.6, 9.0))
fig_fabs = one_panel("The right half is copied to the left",
                     "$y=f(|x|)$", _t, base(np.abs(_t)), (-5.6, 9.0))
_s = np.linspace(-1.7, 3.7, 600)
fig_sq = one_panel("Squaring: never negative, smooth at the zeros",
                   "$y=[f(x)]^{2}$", _s, base(_s) ** 2, (-5.6, 22.0))

# ══════════════════════════════════════════════════════════
# (b) 逆数のグラフ
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 4.0))
_u = np.linspace(-1.4, 5.4, 500)
ax2.plot(_u, _u - 2.0, color=ACCENT, linewidth=1.8)
for _lo, _hi in ((-1.4, 1.98), (2.02, 5.4)):
    _s = np.linspace(_lo, _hi, 400)
    _y = 1.0 / (_s - 2.0)
    _m = np.abs(_y) <= 3.4
    ax2.plot(_s[_m], _y[_m], color=WARM, linewidth=1.8)
ax2.axvline(2.0, color=GREY, linestyle="--", linewidth=1.0)
for _px in (1.0, 3.0):
    ax2.plot([_px], [_px - 2.0], "o", color=INK, markersize=5)
ax2.text(2.1, -3.1, "$x=2$", ha="left", va="center", fontsize=9.5, color=GREY)
ax2.text(5.2, 3.0, "$y=f(x)$", ha="right", va="center", fontsize=9.5,
         color=ACCENT)
ax2.text(4.9, 1.35, "$y=1/f(x)$", ha="right", va="center", fontsize=9.5,
         color=WARM)
ax2.set_xlim(-1.6, 5.6)
ax2.set_ylim(-3.6, 3.6)
frame(ax2)

for _fig, _name in ((fig_abs, "abs"), (fig_fabs, "fabs"), (fig_sq, "sq"),
                     (fig2, "idea-b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-2-16-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-2-16-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
