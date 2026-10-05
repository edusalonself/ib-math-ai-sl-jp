"""AA HL 4.14b（連続確率変数と確率密度関数）の図をつくる。

    python3 figs/aa-hl/make_aahl_4_14b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_4_14b.py  … 目視用の PNG も

出力: aa-hl/04-statistics-and-probability/img/aahl-4-14b-idea-a.svg
      aa-hl/04-statistics-and-probability/img/aahl-4-14b-idea-b.svg

(a) 確率は面積。全体の面積は 1。
(b) 最頻値は山の頂上、中央値は面積を半分に分ける値。

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
OUT = os.path.join(HERE, "..", "..", "aa-hl", "04-statistics-and-probability",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
SHADE = "#cfe3f7"
SHADE2 = "#fbe3c4"


def dens(t):
    """山が左寄りの、なめらかな密度（面積は目で見て 1 くらい）。"""
    return 1.9 * t * np.exp(-1.6 * t)


# ══════════════════════════════════════════════════════════
# (a) 確率は面積
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.8, 3.0))
ax1.set_title("for a continuous variable, probability is area under the"
              " curve", fontsize=10.2, color=INK, loc="left", pad=10)

T = np.linspace(0, 4.4, 600)
Y = dens(T)
ax1.plot(T, Y, color=ACCENT, linewidth=2.0, zorder=3)
_a, _b = 1.1, 2.3
_m = (T >= _a) & (T <= _b)
ax1.fill_between(T[_m], 0, Y[_m], color=SHADE, zorder=2)
ax1.plot([_a, _a], [0, dens(_a)], color=GREY, linewidth=1.0,
         linestyle=(0, (3, 3)), zorder=3)
ax1.plot([_b, _b], [0, dens(_b)], color=GREY, linewidth=1.0,
         linestyle=(0, (3, 3)), zorder=3)
ax1.text(_a - 0.06, -0.035, "$a$", fontsize=10.5, color=INK)
ax1.text(_b - 0.05, -0.035, "$b$", fontsize=10.5, color=INK)
ax1.text(1.28, 0.10, "$P(a \\leq X \\leq b)$", fontsize=10, color=INK)
ax1.text(3.0, 0.24, "total area $= 1$", fontsize=10, color=GREY)
ax1.text(1.45, 0.40, "$y = f(x)$", fontsize=11, color=ACCENT)
ax1.set_xlim(-0.15, 4.5)
ax1.set_ylim(-0.08, 0.50)
ax1.set_xlabel("$x$", fontsize=10, color=INK)
ax1.set_yticks([])
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.tick_params(labelsize=9, colors=GREY)

# ══════════════════════════════════════════════════════════
# (b) 最頻値と中央値
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 3.2))
ax2.set_title("the mode is the peak; the median splits the area in half",
              fontsize=10.2, color=INK, loc="left", pad=10)

ax2.plot(T, Y, color=INK, linewidth=2.0, zorder=4)
MODE = 1.0 / 1.6
TOT = np.trapezoid(Y, T)
_cum = np.cumsum(Y) * (T[1] - T[0])
MED = float(T[np.searchsorted(_cum, TOT / 2)])
_left = T <= MED
_right = T >= MED
ax2.fill_between(T[_left], 0, Y[_left], color=SHADE, zorder=2)
ax2.fill_between(T[_right], 0, Y[_right], color=SHADE2, zorder=2)
ax2.plot([MED, MED], [0, dens(MED)], color=INK, linewidth=1.4, zorder=5)
ax2.plot([MODE, MODE], [0, dens(MODE)], color=WARM, linewidth=1.4,
         linestyle=(0, (4, 3)), zorder=5)
ax2.plot([MODE], [dens(MODE)], "o", color=WARM, markersize=5, zorder=6)

ax2.text(MODE - 0.52, dens(MODE) + 0.025, "mode", fontsize=10, color=WARM)
ax2.text(MED + 0.06, dens(MED) + 0.045, "median", fontsize=10, color=INK)
ax2.text(0.38, 0.055, "area $0.5$", fontsize=9.5, color=INK,
         bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
ax2.text(MED + 0.45, 0.055, "area $0.5$", fontsize=9.5, color=INK)
ax2.text(0.02, -0.105, "they are different unless the curve is symmetric",
         fontsize=9, color=GREY)
ax2.set_xlim(-0.15, 4.5)
ax2.set_ylim(-0.14, 0.52)
ax2.set_xlabel("$x$", fontsize=10, color=INK)
ax2.set_yticks([])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.tick_params(labelsize=9, colors=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-4-14b-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-4-14b-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
