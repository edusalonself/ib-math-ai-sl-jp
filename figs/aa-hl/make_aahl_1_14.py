"""AA HL 1.14（共役な解・De Moivre の定理・n 乗根）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_14.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_14.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-14-idea-a.svg
      aa-hl/01-number-and-algebra/img/aahl-1-14-idea-b.svg

(a) De Moivre：累乗するたびに、角が θ ずつ増え、長さが r 倍になる。
    r = 1.25, θ = π/6 で z から z^5 まで。
(b) n 乗根：半径が同じ円の上に、2π/n おきに n 個並ぶ。
    z^3 = 8 の 3 つの解（半径 2 の円、120 度おき）。

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

fig1, ax1 = plt.subplots(figsize=(5.4, 4.6))
fig2, ax2 = plt.subplots(figsize=(5.0, 4.8))


def axes(ax, xlo, xhi, ylo, yhi):
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    ax.axhline(0.0, color=INK, linewidth=1.0, zorder=1)
    ax.axvline(0.0, color=INK, linewidth=1.0, zorder=1)
    ax.set_aspect("equal")
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(xhi, 0.14, "Re", ha="right", va="bottom", fontsize=10, color=INK)
    ax.text(0.14, yhi, "Im", ha="left", va="top", fontsize=10, color=INK)


# ══════════════════════════════════════════════════════════
# (a) 累乗：角が増え、長さが伸びる
# ══════════════════════════════════════════════════════════
ax1.set_title("Each power turns by $\\theta$ and stretches by $r$",
              fontsize=10.5, color=INK, loc="left", pad=10)
axes(ax1, -3.5, 3.6, -0.8, 3.2)
RR, TH = 1.25, np.pi / 6.0
_t = np.linspace(0.0, 5.2 * TH, 400)
ax1.plot(RR ** (_t / TH) * np.cos(_t), RR ** (_t / TH) * np.sin(_t),
         color=GREY, linewidth=1.0, linestyle=(0, (2, 3)), zorder=2)
for _k in range(1, 6):
    _r, _a = RR ** _k, _k * TH
    ax1.plot([_r * np.cos(_a)], [_r * np.sin(_a)], marker="o", markersize=6,
             color=ACCENT if _k == 1 else INK, zorder=4)
    _lab = "$z$" if _k == 1 else "$z^{%d}$" % _k
    ax1.text(_r * np.cos(_a) + 0.10, _r * np.sin(_a) + 0.12, _lab,
             ha="left", va="bottom", fontsize=10, color=ACCENT if _k == 1 else INK)
ax1.annotate("", xy=(RR * np.cos(TH), RR * np.sin(TH)), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.6))
_ta = np.linspace(0.0, TH, 100)
ax1.plot(0.55 * np.cos(_ta), 0.55 * np.sin(_ta), color=WARM, linewidth=1.3)
ax1.text(0.78 * np.cos(TH / 2), 0.78 * np.sin(TH / 2), "$\\theta$",
         ha="center", va="center", fontsize=11, color=WARM)
ax1.text(-3.35, 2.75, "the argument becomes $n\\theta$\n"
                     "and the modulus becomes $r^{n}$",
         ha="left", va="center", fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) n 乗根：円の上に等しい間隔で
# ══════════════════════════════════════════════════════════
ax2.set_title("The cube roots of a number, on one circle",
              fontsize=10.5, color=INK, loc="left", pad=10)
axes(ax2, -3.2, 3.6, -3.0, 3.4)
_c = np.linspace(0.0, 2.0 * np.pi, 400)
ax2.plot(2.0 * np.cos(_c), 2.0 * np.sin(_c), color=GREY, linewidth=1.0,
         linestyle=(0, (3, 3)), zorder=2)
ROOTS = [(0.0, "$w_{1}$", "left", "bottom"),
         (2.0 * np.pi / 3.0, "$w_{2}$", "right", "bottom"),
         (-2.0 * np.pi / 3.0, "$w_{3}$", "right", "top")]
_pts = []
for _a, _lab, _ha, _va in ROOTS:
    _x, _y = 2.0 * np.cos(_a), 2.0 * np.sin(_a)
    _pts.append((_x, _y))
    ax2.plot([0, _x], [0, _y], color=ACCENT, linewidth=1.4, zorder=3)
    ax2.plot([_x], [_y], marker="o", markersize=7, color=ACCENT, zorder=4)
    ax2.text(_x + (0.16 if _ha == "left" else -0.16),
             _y + (0.16 if _va == "bottom" else -0.16), _lab,
             ha=_ha, va=_va, fontsize=11, color=ACCENT)
_pts.append(_pts[0])
ax2.plot([p[0] for p in _pts], [p[1] for p in _pts], color=WARM,
         linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
_ga = np.linspace(0.0, 2.0 * np.pi / 3.0, 120)
ax2.plot(0.62 * np.cos(_ga), 0.62 * np.sin(_ga), color=WARM, linewidth=1.3,
         zorder=4)
ax2.text(0.36 * np.cos(np.pi / 3.0), 0.36 * np.sin(np.pi / 3.0),
         "$\\frac{2\\pi}{3}$", ha="center", va="center", fontsize=11,
         color=WARM)
ax2.text(-3.05, -2.6, "same modulus, arguments $\\frac{2\\pi}{3}$ apart",
         ha="left", va="center", fontsize=10, color=INK)

for _fig, _name in ((fig1, "aahl-1-14-idea-a.svg"),
                    (fig2, "aahl-1-14-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
