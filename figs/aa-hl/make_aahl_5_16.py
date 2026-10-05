"""AA HL 5.16（置換積分と部分積分）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_16.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_16.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-16-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-16-idea-b.svg

(a) 置換積分の手順（流れ図）。
(b) 部分積分の面積図：長方形 uv を 2 つに分ける。

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
from matplotlib.patches import FancyBboxPatch, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
SHADE = "#dbeafe"
SHADE2 = "#fbe3c4"

# ══════════════════════════════════════════════════════════
# (a) 置換積分の手順
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(6.0, 3.2))
ax1.set_title("integration by substitution, step by step", fontsize=10.5,
              color=INK, loc="left", pad=10)


def box(x, y, w, h, text, col, fs=9.2):
    ax1.add_patch(FancyBboxPatch((x, y), w, h,
                                 boxstyle="round,pad=0.10,rounding_size=0.12",
                                 facecolor="white", edgecolor=col,
                                 linewidth=1.4, zorder=2))
    ax1.text(x + w / 2, y + h / 2, text, fontsize=fs, color=INK,
             ha="center", va="center", zorder=3)


def down(x, y0, y1):
    ax1.annotate("", xy=(x, y1), xytext=(x, y0),
                 arrowprops=dict(arrowstyle="-|>", color=GREY, linewidth=1.3,
                                 shrinkA=2, shrinkB=2))


box(0.3, 4.2, 4.6, 0.8, "choose $u = g(x)$", ACCENT)
box(0.3, 2.8, 4.6, 0.8, "find $\\frac{du}{dx}$, so $du = g'(x)\\,dx$", ACCENT)
box(0.3, 1.4, 4.6, 0.8, "rewrite the whole integrand in $u$", ACCENT)
box(0.3, 0.0, 4.6, 0.8, "integrate, then put $x$ back", WARM)
for _y0, _y1 in ((4.2, 3.6), (2.8, 2.2), (1.4, 0.8)):
    down(2.6, _y0, _y1)

ax1.text(5.2, 3.05, "for a definite integral,", fontsize=9, color=GREY)
ax1.text(5.2, 2.60, "change the limits instead", fontsize=9, color=GREY)
ax1.text(5.2, 2.15, "of putting $x$ back", fontsize=9, color=GREY)
ax1.text(0.0, -0.95, "nothing in $x$ may be left behind: $dx$ must go too",
         fontsize=9, color=GREY)
ax1.set_xlim(-0.2, 10.4)
ax1.set_ylim(-1.4, 5.3)
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 部分積分の面積図
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.0, 3.6))
ax2.set_title("$uv$ splits into two pieces", fontsize=10.5, color=INK,
              loc="left", pad=10)

t = np.linspace(0, 1, 300)
CX = 0.6 + 3.2 * t
CY = 0.6 + 2.6 * t ** 0.55
ax2.add_patch(Polygon(list(zip(CX, CY)) + [(3.8, 0.6)], closed=True,
                      facecolor=SHADE, edgecolor="none", zorder=1))
ax2.add_patch(Polygon(list(zip(CX, CY)) + [(0.6, 3.2)], closed=True,
                      facecolor=SHADE2, edgecolor="none", zorder=1))
ax2.plot(CX, CY, color=INK, linewidth=2.0, zorder=3)
ax2.plot([0.6, 3.8, 3.8, 0.6, 0.6], [0.6, 0.6, 3.2, 3.2, 0.6],
         color=GREY, linewidth=1.2, zorder=2)
ax2.text(2.55, 1.15, "$\\int v\\,du$", fontsize=11, color=INK)
ax2.text(1.05, 2.60, "$\\int u\\,dv$", fontsize=11, color=INK)
ax2.text(2.05, 0.18, "$u$", fontsize=11, color=GREY)
ax2.text(0.22, 1.85, "$v$", fontsize=11, color=GREY)
ax2.text(0.0, -0.75, "the whole rectangle is $uv$, so"
         " $\\int u\\,dv = uv - \\int v\\,du$", fontsize=9.2, color=GREY)
ax2.set_xlim(-0.2, 4.6)
ax2.set_ylim(-1.2, 3.9)
ax2.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-16-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-16-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
