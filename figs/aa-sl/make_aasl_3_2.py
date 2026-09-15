"""AA SL 3.2 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_2.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_2.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-2-idea.svg

(a) 辺と角の名前のつけ方。a は A の向かい、b は B の向かい、c は C の向かい。
(b) どちらの定理を使うか。向かい合う組がそろえば正弦定理、はさむ角なら余弦定理。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（数値は入れない）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.6))


def arc(ax, V, U, W, r, color, lw=1.4):
    """頂点 V での角に弧をかく。"""
    a1 = np.arctan2(U[1] - V[1], U[0] - V[0])
    a2 = np.arctan2(W[1] - V[1], W[0] - V[0])
    if a2 < a1:
        a1, a2 = a2, a1
    if a2 - a1 > np.pi:
        a1, a2 = a2, a1 + 2 * np.pi
    t = np.linspace(a1, a2, 60)
    ax.plot(V[0] + r * np.cos(t), V[1] + r * np.sin(t), color=color,
            linewidth=lw)
    m = 0.5 * (a1 + a2)
    return (V[0] + 1.55 * r * np.cos(m), V[1] + 1.55 * r * np.sin(m))


# ══════════════════════════════════════════════════════════
# (a) 名前のつけ方
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Naming sides and angles", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-1.0, 7.2)
ax1.set_ylim(-1.6, 5.0)
ax1.set_aspect("equal")
ax1.axis("off")

PA = (0.0, 0.0)
PB = (6.0, 0.0)
PC = (4.1, 3.7)
tri = plt.Polygon([PA, PB, PC], closed=True, facecolor="#eef2f6",
                  edgecolor=INK, linewidth=2.0)
ax1.add_patch(tri)

ax1.text(PA[0] - 0.42, PA[1] - 0.30, "$A$", fontsize=12, color=INK)
ax1.text(PB[0] + 0.18, PB[1] - 0.30, "$B$", fontsize=12, color=INK)
ax1.text(PC[0] + 0.12, PC[1] + 0.18, "$C$", fontsize=12, color=INK)

# 辺の名前（向かいの頂点の小文字）
ax1.plot([PB[0], PC[0]], [PB[1], PC[1]], color=ACCENT, linewidth=3.0)
ax1.text(5.42, 1.85, "$a$", fontsize=12, color=ACCENT)
ax1.plot([PA[0], PC[0]], [PA[1], PC[1]], color=WARM, linewidth=3.0)
ax1.text(1.72, 1.92, "$b$", fontsize=12, color=WARM)
ax1.plot([PA[0], PB[0]], [PA[1], PB[1]], color=GREEN, linewidth=3.0)
ax1.text(2.95, -0.62, "$c$", fontsize=12, color=GREEN)

for V, U, W, col in [(PA, PB, PC, GREEN), (PB, PC, PA, WARM),
                     (PC, PA, PB, ACCENT)]:
    arc(ax1, V, U, W, 0.62, GREY, 1.2)

ax1.annotate("", xy=(5.15, 1.85), xytext=(2.05, 3.35),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=0.9,
                             linestyle=(0, (3, 3))))
ax1.text(0.35, 3.45, "$a$ faces $A$", fontsize=10, color=INK)
ax1.text(-1.0, -1.5, "each small letter names the side opposite that capital",
         fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) どちらの定理か
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Which rule?", fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-0.6, 9.4)
ax2.set_ylim(-1.6, 5.0)
ax2.set_aspect("equal")
ax2.axis("off")

# 左：正弦定理（向かい合う組）
QA = (0.0, 0.0)
QB = (3.5, 0.0)
QC = (2.5, 2.6)
ax2.add_patch(plt.Polygon([QA, QB, QC], closed=True, facecolor="#eef2f6",
                          edgecolor=GREY, linewidth=1.4))
ax2.plot([QB[0], QC[0]], [QB[1], QC[1]], color=ACCENT, linewidth=3.0)
p = arc(ax2, QA, QB, QC, 0.48, ACCENT, 1.6)
ax2.text(p[0] - 0.05, p[1] - 0.12, "$A$", fontsize=11, color=ACCENT)
ax2.text(3.18, 1.30, "$a$", fontsize=11, color=ACCENT)
ax2.text(0.05, 3.30, "a side and the angle", fontsize=10, color=INK)
ax2.text(0.05, 2.85, "facing it: sine rule", fontsize=10, color=INK)

# 右：余弦定理（はさむ角）
RA = (5.4, 0.0)
RB = (9.0, 0.0)
RC = (7.9, 2.6)
ax2.add_patch(plt.Polygon([RA, RB, RC], closed=True, facecolor="#eef2f6",
                          edgecolor=GREY, linewidth=1.4))
ax2.plot([RA[0], RB[0]], [RA[1], RB[1]], color=WARM, linewidth=3.0)
ax2.plot([RB[0], RC[0]], [RB[1], RC[1]], color=WARM, linewidth=3.0)
q = arc(ax2, RB, RA, RC, 0.48, WARM, 1.6)
ax2.text(q[0] - 0.10, q[1] - 0.12, "$B$", fontsize=11, color=WARM)
ax2.text(5.45, 3.30, "two sides and the", fontsize=10, color=INK)
ax2.text(5.45, 2.85, "angle between them:", fontsize=10, color=INK)
ax2.text(5.45, 2.40, "cosine rule", fontsize=10, color=INK)

ax2.text(-0.6, -1.5, "look for a matching pair first; if there is none, use the "
         "included angle", fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-3-2-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
