"""AA HL 3.10（加法定理と 2 倍角）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_10.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_10.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-10-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-10-idea-b.svg

(a) sin(A+B) の図による説明：長方形の中に直角三角形を 2 つ入れる。
(b) 加法定理に B = A を入れると 2 倍角が出る、という流れ図。

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
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "03-geometry-and-trigonometry",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

# ══════════════════════════════════════════════════════════
# (a) sin(A+B) の図
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.0, 4.6))
ax1.set_title("A picture behind $\\sin(A+B)$", fontsize=10.5, color=INK,
              loc="left", pad=10)
A = np.radians(30.0)
B = np.radians(38.0)
# O を原点、OP = 1 とする。角 AOP = A+B。
O = np.array([0.0, 0.0])
P = np.array([np.cos(A + B), np.sin(A + B)])
# Q は OP を角 A の辺に下ろした足
Q = np.array([np.cos(A), np.sin(A)]) * np.cos(B)
F = np.array([P[0], 0.0])           # P から x 軸へ
G = np.array([Q[0], 0.0])           # Q から x 軸へ
H = np.array([P[0], Q[1]])          # P から OQ の高さへ

for _a, _b, _c, _w in ((O, P, ACCENT, 1.8), (O, Q, ACCENT, 1.8),
                       (Q, P, ACCENT, 1.8), (P, F, GREY, 1.2),
                       (Q, G, GREY, 1.2), (P, H, GREY, 1.2)):
    ax1.plot([_a[0], _b[0]], [_a[1], _b[1]], color=_c, linewidth=_w)
ax1.plot([0.0, 1.15], [0.0, 0.0], color=GREY, linewidth=1.2)
ax1.plot([H[0], Q[0]], [H[1], Q[1]], color=GREY, linewidth=1.2,
         linestyle=":")
ax1.text(P[0] + 0.02, P[1] + 0.03, "$P$", fontsize=10, color=INK)
ax1.text(Q[0] + 0.03, Q[1] + 0.02, "$Q$", fontsize=10, color=INK)
ax1.text(-0.07, -0.02, "$O$", fontsize=10, color=INK)
ax1.text(0.22, 0.045, "$A$", fontsize=10, color=WARM)
ax1.text(0.44, 0.30, "$B$", fontsize=10, color=WARM)
ax1.text(0.15, 0.52, "$OP = 1$", ha="right", fontsize=9.5,
         color=ACCENT)
ax1.text(0.44, 0.96, "the height of $P$ is $\\sin(A+B)$",
         fontsize=9, color=GREY)
ax1.text(-0.02, -0.14, "it splits into two pieces, one from each triangle",
         fontsize=9, color=GREY)
ax1.set_xlim(-0.14, 1.24)
ax1.set_ylim(-0.24, 1.08)
ax1.set_aspect("equal")
ax1.set_xticks([])
ax1.set_yticks([])
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 加法定理 → 2 倍角
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(6.2, 3.2))
ax2.set_title("Put $B = A$ and the double angle identities drop out",
              fontsize=10.5, color=INK, loc="left", pad=10)
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.0)
ax2.axis("off")

ROWS = [
    (0.80, "$\\sin(A+B) = \\sin A\\cos B + \\cos A\\sin B$",
     "$\\sin 2A = 2\\sin A\\cos A$", ACCENT),
    (0.50, "$\\cos(A+B) = \\cos A\\cos B - \\sin A\\sin B$",
     "$\\cos 2A = \\cos^{2}A - \\sin^{2}A$", WARM),
    (0.20, "$\\tan(A+B) = \\dfrac{\\tan A + \\tan B}{1 - \\tan A\\tan B}$",
     "$\\tan 2A = \\dfrac{2\\tan A}{1 - \\tan^{2}A}$", GREY),
]
for _y, _left, _right, _col in ROWS:
    ax2.add_patch(FancyBboxPatch((0.01, _y - 0.10), 0.47, 0.20,
                                 boxstyle="round,pad=0.012", linewidth=1.1,
                                 edgecolor=_col, facecolor="none"))
    ax2.text(0.245, _y, _left, ha="center", va="center", fontsize=9.5,
             color=_col)
    ax2.annotate("", xy=(0.60, _y), xytext=(0.50, _y),
                 arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.0))
    ax2.text(0.80, _y, _right, ha="center", va="center", fontsize=9.5,
             color=_col)
ax2.text(0.55, 0.95, "$B = A$", ha="center", va="center", fontsize=9,
         color=INK)
ax2.text(0.01, 0.02, "the booklet prints the left column; the right one you derive",
         ha="left", va="center", fontsize=9, color=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-10-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-10-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
