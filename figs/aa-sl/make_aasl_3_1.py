"""AA SL 3.1 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_1.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_1.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-1-idea-a.svg
      aa-sl/03-geometry/img/aasl-3-1-idea-b.svg
      aa-sl/03-geometry/img/aasl-3-1-idea-c.svg

(a) 空間の対角線は、ピタゴラスの定理を 2 回使って出す。
(b) 直線と平面のなす角は、その直線と「影」のなす角。
(c) 円錐の母線 l は、半径 r と高さ h の直角三角形の斜辺。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（辺の長さは a, b, c で書く）。
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

# 斜投影：(x, y, z) -> 平面座標
KX, KY = 0.46, 0.44


def pr(x, y, z):
    return (x + KX * y, z + KY * y)


fig1, ax1 = plt.subplots(figsize=(5.3, 4.6))
fig2, ax2 = plt.subplots(figsize=(5.3, 4.6))
fig3, ax3 = plt.subplots(figsize=(4.9, 4.6))
# ══════════════════════════════════════════════════════════
# (a) 直方体の対角線
# ══════════════════════════════════════════════════════════
ax1.set_title("Pythagoras twice", fontsize=11, color=INK, loc="left",
              pad=10)
ax1.set_xlim(-0.9, 6.6)
ax1.set_ylim(-0.75, 5.2)
ax1.set_aspect("equal")
ax1.axis("off")

A, B, C, D = 0.0, 4.2, 3.2, 3.0          # 幅 a、奥行き b、高さ c
P000 = pr(0, 0, 0)
P100 = pr(B, 0, 0)
P110 = pr(B, C, 0)
P010 = pr(0, C, 0)
P001 = pr(0, 0, D)
P101 = pr(B, 0, D)
P111 = pr(B, C, D)
P011 = pr(0, C, D)

# 見える辺
for u, v in [(P000, P100), (P100, P101), (P000, P001), (P001, P101),
             (P100, P110), (P110, P111), (P101, P111), (P001, P011),
             (P011, P111)]:
    ax1.plot([u[0], v[0]], [u[1], v[1]], color=INK, linewidth=1.5)
# 隠れる辺
for u, v in [(P000, P010), (P010, P110), (P010, P011)]:
    ax1.plot([u[0], v[0]], [u[1], v[1]], color=GREY, linewidth=1.0,
             linestyle=(0, (3, 3)))

# 底面の対角線（1 回目のピタゴラス）
ax1.plot([P000[0], P110[0]], [P000[1], P110[1]], color=WARM, linewidth=2.2)
# 空間の対角線（2 回目）
ax1.plot([P000[0], P111[0]], [P000[1], P111[1]], color=ACCENT, linewidth=2.4)

ax1.text((P000[0] + P100[0]) / 2, P000[1] - 0.42, "$a$", fontsize=11,
         color=INK, ha="center")
ax1.text((P100[0] + P110[0]) / 2 + 0.26, (P100[1] + P110[1]) / 2 - 0.30,
         "$b$", fontsize=11, color=INK, ha="left", va="center")
ax1.text(P111[0] + 0.18, (P110[1] + P111[1]) / 2, "$c$", fontsize=11,
         color=INK)
ax1.text(2.30, 0.90, "$\\sqrt{a^{2}+b^{2}}$", fontsize=11, color=WARM)
ax1.text(2.40, 2.76, "$\\sqrt{a^{2}+b^{2}+c^{2}}$", fontsize=11,
         color=ACCENT, ha="right", va="center")

# ══════════════════════════════════════════════════════════
# (b) 直線と平面のなす角
# ══════════════════════════════════════════════════════════
ax2.set_title("A line and a plane", fontsize=11, color=INK, loc="left",
              pad=10)
ax2.set_xlim(-0.9, 6.6)
ax2.set_ylim(-0.75, 5.2)
ax2.set_aspect("equal")
ax2.axis("off")

# 平面（平行四辺形）
Q = [pr(0, 0, 0), pr(5.0, 0, 0), pr(5.0, 3.0, 0), pr(0, 3.0, 0)]
ax2.add_patch(plt.Polygon(Q, closed=True, facecolor="#eef2f6",
                          edgecolor=GREY, linewidth=1.2))

FOOT = pr(0.9, 0.8, 0)          # 直線が平面と出会う点
SHAD = pr(4.3, 2.2, 0)          # 影の先
TOPP = pr(4.3, 2.2, 2.9)        # 直線の先

ax2.plot([FOOT[0], TOPP[0]], [FOOT[1], TOPP[1]], color=ACCENT, linewidth=2.4)
ax2.plot([FOOT[0], SHAD[0]], [FOOT[1], SHAD[1]], color=WARM, linewidth=2.2)
ax2.plot([SHAD[0], TOPP[0]], [SHAD[1], TOPP[1]], color=GREY, linewidth=1.2,
         linestyle=(0, (3, 3)))

# 直角の印
sq = 0.24
ax2.plot([SHAD[0] - sq, SHAD[0] - sq, SHAD[0]],
         [SHAD[1], SHAD[1] + sq, SHAD[1] + sq], color=GREY, linewidth=1.0)

# なす角の弧
v1 = np.array(SHAD) - np.array(FOOT)
v2 = np.array(TOPP) - np.array(FOOT)
a1 = np.arctan2(v1[1], v1[0])
a2 = np.arctan2(v2[1], v2[0])
th = np.linspace(a1, a2, 60)
rr = 0.95
ax2.plot(FOOT[0] + rr * np.cos(th), FOOT[1] + rr * np.sin(th), color=GREEN,
         linewidth=1.4)
ax2.text(FOOT[0] + 1.22, FOOT[1] + 0.34, "$\\theta$", fontsize=12,
         color=GREEN)

ax2.plot([FOOT[0]], [FOOT[1]], marker="o", markersize=5, color=INK, zorder=3)
ax2.text(1.85, 2.75, "the line", fontsize=10, color=ACCENT)
ax2.text(2.60, 0.32, "its shadow on the plane", fontsize=10, color=WARM)

# ══════════════════════════════════════════════════════════
# (c) 円錐の母線
# ══════════════════════════════════════════════════════════
ax3.set_title("Slant height of a cone", fontsize=11, color=INK, loc="left",
              pad=10)
ax3.set_xlim(-3.4, 3.4)
ax3.set_ylim(-1.75, 4.6)
ax3.set_aspect("equal")
ax3.axis("off")

RR, BB, HH = 2.4, 0.62, 3.6          # 底面の半径、楕円の縦半径、高さ
APX = (0.0, HH)
tt = np.linspace(0.0, np.pi, 160)

# r, h, l の直角三角形をうすく塗る
ax3.add_patch(plt.Polygon([(0.0, 0.0), (RR, 0.0), APX], closed=True,
                          facecolor="#eef2f6", edgecolor="none", zorder=0))
# 底面の楕円（手前は実線、奥は点線）
ax3.plot(RR * np.cos(tt), -BB * np.sin(tt), color=INK, linewidth=1.5)
ax3.plot(RR * np.cos(tt), BB * np.sin(tt), color=GREY, linewidth=1.0,
         linestyle=(0, (3, 3)))
# 母線（右）と、ふつうの側面（左）
ax3.plot([APX[0], RR], [APX[1], 0.0], color=ACCENT, linewidth=2.6)
ax3.plot([APX[0], -RR], [APX[1], 0.0], color=INK, linewidth=1.5)
# 高さ
ax3.plot([0.0, 0.0], [0.0, HH], color=WARM, linewidth=2.2,
         linestyle=(0, (5, 3)))
# 半径
ax3.plot([0.0, RR], [0.0, 0.0], color=GREEN, linewidth=2.4)
# 中心の直角
sq3 = 0.28
ax3.plot([sq3, sq3, 0.0], [0.0, sq3, sq3], color=GREY, linewidth=1.0)

ax3.plot([APX[0]], [APX[1]], marker="o", markersize=5, color=INK, zorder=3)
ax3.text(0.16, HH + 0.10, "apex", fontsize=9.5, color=INK)
ax3.text(1.50, 2.05, "$l$", fontsize=13, color=ACCENT)
ax3.text(-0.50, 1.80, "$h$", fontsize=13, color=WARM)
ax3.text(1.16, 0.16, "$r$", fontsize=13, color=GREEN)   # 半径の真上へ
ax3.text(-3.3, -1.42, "$l^{2} = r^{2} + h^{2}$", fontsize=10.5, color=INK,
         va="bottom")

for _fig, _name in ((fig1, "aasl-3-1-idea-a.svg"),
                    (fig2, "aasl-3-1-idea-b.svg"),
                    (fig3, "aasl-3-1-idea-c.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
