"""AA HL 2.13（有理関数のグラフ）の図をつくる。

    python3 figs/aa-hl/make_aahl_2_13.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_2_13.py  … 目視用の PNG も

出力: aa-hl/02-functions/img/aahl-2-13-idea-a.svg
      aa-hl/02-functions/img/aahl-2-13-idea-b.svg

(a) 分母が 2 次：垂直漸近線 2 本と、水平漸近線 y = 0。
(b) 分子が 2 次：垂直漸近線 1 本と、斜め漸近線。

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


def pieces(f, lo, hi, breaks, ylim):
    """漸近線で切って、つながった部分ごとに返す。"""
    edges = [lo] + list(breaks) + [hi]
    out = []
    for _a, _b in zip(edges[:-1], edges[1:]):
        _t = np.linspace(_a + 1e-3, _b - 1e-3, 600)
        _y = f(_t)
        _m = np.abs(_y) <= ylim
        out.append((_t[_m], _y[_m]))
    return out


# ══════════════════════════════════════════════════════════
# (a) 分母が 2 次
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(6.2, 4.0))
ax1.set_title("A quadratic denominator: two vertical asymptotes, and $y=0$",
              fontsize=10.5, color=INK, loc="left", pad=10)
for _xa in (-2.0, 3.0):
    ax1.axvline(_xa, color=WARM, linestyle="--", linewidth=1.1)
ax1.axhline(0.0, color=WARM, linestyle="--", linewidth=1.1)
for _t, _y in pieces(lambda t: (t + 1.0) / (t * t - t - 6.0),
                     -6.0, 7.0, (-2.0, 3.0), 3.0):
    ax1.plot(_t, _y, color=ACCENT, linewidth=1.8)
ax1.text(-2.15, 2.6, "$x=-2$", ha="right", va="center", fontsize=9.5, color=WARM)
ax1.text(3.15, -2.5, "$x=3$", ha="left", va="center", fontsize=9.5,
         color=WARM)
ax1.text(6.6, 0.35, "$y=0$", ha="right", va="bottom", fontsize=9.5, color=WARM)
ax1.text(-5.8, -2.4, "the degree on top is smaller, so $y \\to 0$ far out",
         ha="left", va="center", fontsize=9, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax1.set_xlim(-6.2, 7.2)
ax1.set_ylim(-3.0, 3.0)
frame(ax1)

# ══════════════════════════════════════════════════════════
# (b) 分子が 2 次：斜め漸近線
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(6.2, 4.2))
ax2.set_title("A quadratic on top: one vertical asymptote, and a slanted one",
              fontsize=10.5, color=INK, loc="left", pad=10)
ax2.axvline(3.0, color=WARM, linestyle="--", linewidth=1.1)
_t = np.linspace(-7.0, 12.0, 400)
ax2.plot(_t, _t + 2.0, color=WARM, linestyle="--", linewidth=1.1)
for _t2, _y2 in pieces(lambda t: (t * t - t - 2.0) / (t - 3.0),
                       -7.0, 12.0, (3.0,), 14.0):
    ax2.plot(_t2, _y2, color=ACCENT, linewidth=1.8)
ax2.text(3.15, -10.0, "$x=3$", ha="left", va="center", fontsize=9.5, color=WARM)
ax2.text(-2.0, 8.0, "$y=x+2$", ha="center", va="center", fontsize=9.5,
         color=WARM, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax2.text(-6.6, -11.5,
         "divide first: the quotient is the slanted asymptote",
         ha="left", va="center", fontsize=9, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax2.set_xlim(-7.2, 12.2)
ax2.set_ylim(-13.0, 15.0)
frame(ax2)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-2-13-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-2-13-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
