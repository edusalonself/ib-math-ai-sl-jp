"""AA HL 1.12（複素数：Cartesian form）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_12.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_12.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-12-idea-a.svg
      aa-hl/01-number-and-algebra/img/aahl-1-12-idea-b.svg

(a) complex plane（Argand diagram）に 4 つの複素数を置く。
    z1 = 3+2i と z4 = 3-2i は実軸について対称（conjugate）。
(b) z = -1 + i√3 の modulus r と argument θ。
    θ は正の実軸から測る。第 2 象限なので θ = 2π/3。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
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
OUT = os.path.join(HERE, "..", "..", "aa-hl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

fig1, ax1 = plt.subplots(figsize=(5.4, 4.4))
fig2, ax2 = plt.subplots(figsize=(5.4, 4.4))


def axes(ax, xlo, xhi, ylo, yhi):
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    ax.axhline(0.0, color=INK, linewidth=1.1, zorder=1)
    ax.axvline(0.0, color=INK, linewidth=1.1, zorder=1)
    ax.set_aspect("equal")
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(xhi, 0.18, "Re", ha="right", va="bottom", fontsize=10, color=INK)
    ax.text(0.18, yhi, "Im", ha="left", va="top", fontsize=10, color=INK)


# ══════════════════════════════════════════════════════════
# (a) Argand diagram に 4 点
# ══════════════════════════════════════════════════════════
ax1.set_title("Four complex numbers on the complex plane",
              fontsize=11, color=INK, loc="left", pad=10)
axes(ax1, -3.6, 4.4, -3.2, 3.2)
for _k in range(-3, 5):
    if _k:
        ax1.plot([_k], [0], marker="|", markersize=5, color=GREY, zorder=2)
for _k in range(-3, 4):
    if _k:
        ax1.plot([0], [_k], marker="_", markersize=5, color=GREY, zorder=2)

PTS = [(3, 2, "$z_1 = 3+2i$", ACCENT, "left", "bottom"),
       (-2, 1, "$z_2 = -2+i$", INK, "right", "bottom"),
       (-1, -2, "$z_3 = -1-2i$", INK, "right", "top"),
       (3, -2, "$z_4 = 3-2i$", ACCENT, "left", "top")]
for _a, _b, _lab, _c, _ha, _va in PTS:
    ax1.plot([_a], [_b], marker="o", markersize=7, color=_c, zorder=4)
    ax1.text(_a + (0.18 if _ha == "left" else -0.18), _b + (0.16 if _va == "bottom" else -0.16),
             _lab, ha=_ha, va=_va, fontsize=10.5, color=_c)
ax1.plot([3, 3], [2, -2], linestyle=(0, (3, 3)), linewidth=1.2,
         color=ACCENT, zorder=3)
ax1.text(2.72, 1.05, "mirror images\nin the real axis", ha="right",
         va="center", fontsize=9.5, color=ACCENT)

# ══════════════════════════════════════════════════════════
# (b) modulus と argument
# ══════════════════════════════════════════════════════════
ax2.set_title("Modulus and argument of $z = -1 + i\\sqrt{3}$",
              fontsize=11, color=INK, loc="left", pad=10)
axes(ax2, -2.8, 2.8, -1.4, 2.6)
ZX, ZY = -1.0, np.sqrt(3.0)
ax2.plot([0, ZX], [0, ZY], color=ACCENT, linewidth=2.0, zorder=4)
ax2.plot([ZX], [ZY], marker="o", markersize=7, color=ACCENT, zorder=5)
ax2.text(ZX - 0.12, ZY + 0.12, "$z = -1 + i\\sqrt{3}$", ha="right",
         va="bottom", fontsize=10.5, color=ACCENT)
ax2.plot([ZX, ZX], [0, ZY], linestyle=(0, (3, 3)), linewidth=1.1,
         color=GREY, zorder=3)
ax2.plot([0, ZX], [0, 0], linestyle=(0, (3, 3)), linewidth=1.1,
         color=GREY, zorder=3)
ax2.text(-0.5, -0.18, "$-1$", ha="center", va="top", fontsize=10, color=GREY)
ax2.text(ZX - 0.12, ZY / 2, "$\\sqrt{3}$", ha="right", va="center",
         fontsize=10, color=GREY)
ax2.text(-0.16, 1.06, "$r = 2$", ha="left", va="center",
         fontsize=11, color=ACCENT)
_th = np.linspace(0.0, 2.0 * np.pi / 3.0, 200)
ax2.plot(0.62 * np.cos(_th), 0.62 * np.sin(_th), color=WARM,
         linewidth=1.5, zorder=4)
ax2.text(0.92 * np.cos(1.05), 0.92 * np.sin(1.05), "$\\theta$",
         ha="center", va="center", fontsize=12, color=WARM)
ax2.text(1.25, 1.55, "$\\theta = \\frac{2\\pi}{3}$, measured from\nthe positive real axis",
         ha="left", va="center", fontsize=9.5, color=WARM)

for _fig, _name in ((fig1, "aahl-1-12-idea-a.svg"),
                    (fig2, "aahl-1-12-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
