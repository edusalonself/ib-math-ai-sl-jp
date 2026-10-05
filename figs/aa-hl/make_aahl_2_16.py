"""AA HL 2.16（絶対値・逆数などのグラフの変換）の図をつくる。

    python3 figs/aa-hl/make_aahl_2_16.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_2_16.py  … 目視用の PNG も

出力: aa-hl/02-functions/img/aahl-2-16-idea-a.svg
      aa-hl/02-functions/img/aahl-2-16-idea-b.svg

(a) 4 枚並べ：y = f(x) / |f(x)| / f(|x|) / [f(x)]^2。
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
# (a) 4 つの変換
# ══════════════════════════════════════════════════════════
fig1, axes1 = plt.subplots(1, 4, figsize=(6.6, 2.2))
_t = np.linspace(-4.2, 4.2, 500)


def base(t):
    return t * t - 2.0 * t - 3.0


PANELS = [
    ("$y=f(x)$", base(_t), ACCENT),
    ("$y=|f(x)|$", np.abs(base(_t)), WARM),
    ("$y=f(|x|)$", base(np.abs(_t)), WARM),
    ("$y=[f(x)]^{2}$", base(_t) ** 2 / 4.0, WARM),
]
for _ax, (_lab, _yv, _col) in zip(axes1, PANELS):
    _ax.plot(_t, _yv, color=_col, linewidth=1.6)
    _ax.set_title(_lab, fontsize=9.5, color=_col, pad=6)
    _ax.set_xlim(-4.4, 4.4)
    _ax.set_ylim(-5.6, 9.0)
    frame(_ax)
fig1.suptitle("One curve, four transformations (the last one is scaled to fit)",
              fontsize=10.5, color=INK, x=0.02, ha="left", y=1.06)

# ══════════════════════════════════════════════════════════
# (b) 逆数のグラフ
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 4.0))
ax2.set_title("Where $f$ is zero, $1/f$ has an asymptote; where $f$ is $1$ or $-1$,"
              " they meet", fontsize=9.8, color=INK, loc="left", pad=10)
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
ax2.text(-1.3, -3.1, "they cross where the height is $1$ or $-1$",
         ha="left", va="center", fontsize=9, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax2.set_xlim(-1.6, 5.6)
ax2.set_ylim(-3.6, 3.6)
frame(ax2)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-2-16-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-2-16-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
