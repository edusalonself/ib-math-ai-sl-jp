"""AA HL 4.13（Bayes の定理）の図をつくる。

    python3 figs/aa-hl/make_aahl_4_13.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_4_13.py  … 目視用の PNG も

出力: aa-hl/04-statistics-and-probability/img/aahl-4-13-idea-a.svg
      aa-hl/04-statistics-and-probability/img/aahl-4-13-idea-b.svg

(a) 樹形図：A に着く道は 2 本。分母はその和。
(b) 面積図：P(B|A) は「A の面積のうち、左側が占める割合」。

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
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "04-statistics-and-probability",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
SHADE = "#cfe3f7"
PALE = "#f1f5f9"

# ══════════════════════════════════════════════════════════
# (a) 樹形図
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.8, 3.4))
ax1.set_title("two paths lead to $A$; their sum is the denominator",
              fontsize=10.5, color=INK, loc="left", pad=10)

ROOT = (0.2, 2.0)
B = (2.2, 3.1)
BP = (2.2, 0.9)
LEAVES = {"BA": (4.6, 3.7), "BA2": (4.6, 2.6),
          "CA": (4.6, 1.5), "CA2": (4.6, 0.3)}


def branch(p, q, col, lw=1.7, ls="-"):
    ax1.plot([p[0], q[0]], [p[1], q[1]], color=col, linewidth=lw,
             linestyle=ls, zorder=2)


branch(ROOT, B, ACCENT)
branch(ROOT, BP, GREY)
branch(B, LEAVES["BA"], ACCENT)
branch(B, LEAVES["BA2"], GREY, ls=(0, (3, 3)))
branch(BP, LEAVES["CA"], ACCENT)
branch(BP, LEAVES["CA2"], GREY, ls=(0, (3, 3)))

ax1.text(B[0] + 0.08, B[1] - 0.04, "$B$", fontsize=11, color=INK)
ax1.text(BP[0] + 0.08, BP[1] - 0.04, "$B'$", fontsize=11, color=INK)
ax1.text(1.0, 2.82, "$P(B)$", fontsize=9.5, color=ACCENT,
         bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
ax1.text(1.0, 1.20, "$P(B')$", fontsize=9.5, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
ax1.text(3.15, 3.58, "$P(A|B)$", fontsize=9.5, color=ACCENT,
         bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
ax1.text(3.25, 2.62, "$P(A'|B)$", fontsize=9.5, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
ax1.text(3.15, 1.38, "$P(A|B')$", fontsize=9.5, color=ACCENT,
         bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
ax1.text(3.25, 0.38, "$P(A'|B')$", fontsize=9.5, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=0.8))

for _k, _lab, _col in (("BA", "$A$", ACCENT), ("BA2", "$A'$", GREY),
                       ("CA", "$A$", ACCENT), ("CA2", "$A'$", GREY)):
    _p = LEAVES[_k]
    ax1.text(_p[0] + 0.10, _p[1] - 0.09, _lab, fontsize=11, color=_col)

ax1.text(5.35, 3.60, "$P(B)P(A|B)$", fontsize=9.5, color=ACCENT)
ax1.text(5.35, 1.40, "$P(B')P(A|B')$", fontsize=9.5, color=ACCENT)
ax1.text(0.0, -0.55, "the numerator is the path through $B$ only",
         fontsize=9, color=GREY)
ax1.set_xlim(-0.2, 9.4)
ax1.set_ylim(-0.9, 4.3)
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 面積図
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.4, 3.6))
ax2.set_title("$P(B|A)$ is the share of the shaded area on the left",
              fontsize=10.5, color=INK, loc="left", pad=10)

w = 0.35          # P(B)
h1 = 0.70         # P(A|B)
h2 = 0.18         # P(A|B')
ax2.add_patch(Rectangle((0, 0), 1, 1, facecolor=PALE, edgecolor=INK,
                        linewidth=1.2, zorder=1))
ax2.add_patch(Rectangle((0, 0), w, h1, facecolor=SHADE, edgecolor=INK,
                        linewidth=1.2, zorder=2))
ax2.add_patch(Rectangle((w, 0), 1 - w, h2, facecolor=SHADE, edgecolor=INK,
                        linewidth=1.2, zorder=2))
ax2.plot([w, w], [0, 1], color=INK, linewidth=1.2, zorder=3)

ax2.text(w / 2, -0.09, "$P(B)$", fontsize=10, color=INK, ha="center")
ax2.text((1 + w) / 2, -0.09, "$P(B')$", fontsize=10, color=INK, ha="center")
ax2.text(w / 2, h1 / 2, "$A$", fontsize=12, color=INK, ha="center",
         va="center")
ax2.text((1 + w) / 2, h2 / 2, "$A$", fontsize=12, color=INK, ha="center",
         va="center")
ax2.text(-0.03, h1 / 2, "$P(A|B)$", fontsize=9.5, color=INK, ha="right",
         va="center")
ax2.text(1.03, h2 / 2, "$P(A|B')$", fontsize=9.5, color=INK, va="center")
ax2.text(0.0, 1.14, "a narrow left column can still hold less shaded area"
         " than a wide right one", fontsize=9, color=GREY)
ax2.set_xlim(-0.34, 1.42)
ax2.set_ylim(-0.22, 1.30)
ax2.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-4-13-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-4-13-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
