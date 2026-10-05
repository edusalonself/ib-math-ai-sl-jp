"""AA SL 3.5 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_5.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_5.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-5-idea-a.svg
      aa-sl/03-geometry/img/aasl-3-5-axes.svg
      aa-sl/03-geometry/img/aasl-3-5-idea-b.svg
      aa-sl/03-geometry/img/aasl-3-5-idea-c.svg
      aa-sl/03-geometry/img/aasl-3-5-idea-d.svg
      aa-sl/03-geometry/img/aasl-3-5-idea-e.svg

(a) 単位円の定義。P の座標が (cos θ, sin θ)。
(axes) 軸の上の 4 点。cos と sin の値を書き入れる。
(b) 4 つの象限の符号と、折り返しでできる 3 つの点。
(c) 参照角。x 軸とのあいだの鋭角 α と、4 つの象限で正になる比。
(d) 正確な値のもとになる 2 つの三角形。
(e) あいまいな場合。C を中心とする半径 a の円が、半直線と 2 回交わる。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（角は θ、参照角は α で書く）。
★ 図の中に定義や規則を文で書かないこと（_方針変更-2026-09-15.md 第 21 節）。
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

fig1, ax1 = plt.subplots(figsize=(5.3, 5.1))
fig2, ax2 = plt.subplots(figsize=(5.3, 5.1))
figX, axX = plt.subplots(figsize=(5.6, 3.9))
t = np.linspace(0, 2 * np.pi, 400)

# ══════════════════════════════════════════════════════════
# (a) 単位円の定義
# ══════════════════════════════════════════════════════════
ax1.set_title("The unit circle", fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(-1.55, 1.95)
ax1.set_ylim(-1.18, 1.75)
ax1.set_aspect("equal")
ax1.axis("off")

ax1.annotate("", xy=(1.55, 0), xytext=(-1.35, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 1.45), xytext=(0, -1.35),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(1.60, -0.16, "$x$", fontsize=11, color=GREY)
ax1.text(0.08, 1.46, "$y$", fontsize=11, color=GREY)

ax1.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.2)

th = 1.05
Px, Py = np.cos(th), np.sin(th)
ax1.plot([0, Px], [0, Py], color=ACCENT, linewidth=2.2)
ax1.plot([Px, Px], [0, Py], color=WARM, linewidth=1.8, linestyle=(0, (5, 3)))
ax1.plot([0, Px], [0, 0], color=GREEN, linewidth=2.6, solid_capstyle="butt")
ax1.plot([Px], [Py], marker="o", markersize=5.5, color=INK, zorder=3)

ta = np.linspace(0, th, 60)
ax1.plot(0.27 * np.cos(ta), 0.27 * np.sin(ta), color=INK, linewidth=1.3)
ax1.text(0.31, 0.11, "$\\theta$", fontsize=12, color=INK)

ax1.text(Px + 0.07, Py + 0.07, "$P(\\cos\\theta,\\ \\sin\\theta)$", fontsize=11,
         color=INK)
ax1.text(Px * 0.42 - 0.06, -0.27, "$\\cos\\theta$", fontsize=10.5, color=GREEN)
ax1.text(Px + 0.10, Py * 0.45, "$\\sin\\theta$", fontsize=10.5, color=WARM)
ax1.text(1.06, -0.20, "$1$", fontsize=10.5, color=GREY)
ax1.plot([1], [0], marker="o", markersize=4, color=GREY, zorder=3)


# ══════════════════════════════════════════════════════════
# (axes) 軸の上の 4 点
# ══════════════════════════════════════════════════════════
axX.set_title("The four points on the axes", fontsize=11, color=INK,
              loc="left", pad=10)
axX.set_xlim(-2.6, 2.6)
axX.set_ylim(-1.85, 1.75)
axX.set_aspect("equal")
axX.axis("off")

axX.annotate("", xy=(1.35, 0), xytext=(-1.35, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
axX.annotate("", xy=(0, 1.5), xytext=(0, -1.5),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
axX.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.2)

for _x, _y in ((1, 0), (0, 1), (-1, 0), (0, -1)):
    axX.plot([_x], [_y], marker="o", markersize=6, color=ACCENT, zorder=3)

axX.text(1.42, 0.06, "$\\cos 0 = 1$\n$\\sin 0 = 0$", fontsize=10.5,
         color=ACCENT, ha="left", va="bottom")
axX.text(0.14, 1.20, "$\\cos\\frac{\\pi}{2} = 0$"
         "\n$\\sin\\frac{\\pi}{2} = 1$", fontsize=10.5, color=ACCENT,
         ha="left", va="bottom")
axX.text(-1.42, 0.06, "$\\cos\\pi = -1$\n$\\sin\\pi = 0$",
         fontsize=10.5, color=ACCENT, ha="right", va="bottom")
axX.text(0.14, -1.20, "$\\cos\\frac{3\\pi}{2} = 0$"
         "\n$\\sin\\frac{3\\pi}{2} = -1$", fontsize=10.5, color=ACCENT,
         ha="left", va="top")

# ══════════════════════════════════════════════════════════
# (b) 象限の符号と、折り返し
# ══════════════════════════════════════════════════════════
ax2.set_title("Signs, and reflections", fontsize=11, color=INK, loc="left",
              pad=10)
ax2.set_xlim(-1.75, 1.75)
ax2.set_ylim(-1.18, 1.75)
ax2.set_aspect("equal")
ax2.axis("off")

ax2.annotate("", xy=(1.5, 0), xytext=(-1.5, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 1.45), xytext=(0, -1.35),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.0)

ax2.text(0.46, 0.14, "all $> 0$", fontsize=9.5, color=GREEN)
ax2.text(-1.16, 0.14, "$\\sin\\theta > 0$", fontsize=9.5, color=GREEN)
ax2.text(-1.16, -0.34, "$\\tan\\theta > 0$", fontsize=9.5, color=GREEN)
ax2.text(0.46, -0.34, "$\\cos\\theta > 0$", fontsize=9.5, color=GREEN)

for _x, _y, _lab, _col, _ha in [
        (np.cos(th), np.sin(th), "$\\theta$", ACCENT, "left"),
        (-np.cos(th), np.sin(th), "$\\pi-\\theta$", WARM, "right"),
        (-np.cos(th), -np.sin(th), "$\\pi+\\theta$", WARM, "right"),
        (np.cos(th), -np.sin(th), "$-\\theta$", WARM, "left")]:
    ax2.plot([0, _x], [0, _y], color=_col, linewidth=1.6)
    ax2.plot([_x], [_y], marker="o", markersize=4.8, color=_col, zorder=3)
    ax2.text(_x * 1.14 + (0.06 if _x > 0 else -0.06), _y * 1.14 - 0.06, _lab,
             fontsize=11, color=_col, ha=_ha)

# ══════════════════════════════════════════════════════════
# (c) 参照角
# ══════════════════════════════════════════════════════════
fig3, ax3 = plt.subplots(figsize=(5.6, 5.4))
ax3.set_title("Reference angles", fontsize=11, color=INK, loc="left", pad=10)
ax3.set_xlim(-1.75, 1.75)
ax3.set_ylim(-1.62, 1.62)
ax3.set_aspect("equal")
ax3.axis("off")

ax3.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.2)
ax3.annotate("", xy=(1.60, 0), xytext=(-1.60, 0),
             arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1.0))
ax3.annotate("", xy=(0, 1.45), xytext=(0, -1.45),
             arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1.0))

AL = np.deg2rad(38.0)                     # 参照角 α
ANGS = (AL, np.pi - AL, np.pi + AL, 2 * np.pi - AL)
BASE = (0.0, np.pi, np.pi, 2 * np.pi)     # いちばん近い x 軸
LABS = (r"$\alpha$", r"$\pi-\alpha$", r"$\pi+\alpha$", r"$2\pi-\alpha$")
LPOS = ((1.18, 0.86), (-1.72, 0.86), (-1.72, -0.98), (1.18, -0.98))
POSI = ("all $+$", "$\\sin+$", "$\\tan+$", "$\\cos+$")
PANG = np.deg2rad((66.0, 114.0, 246.0, 294.0))

for _a, _b, _lab, _lp, _pos, _pa in zip(ANGS, BASE, LABS, LPOS, POSI, PANG):
    _x, _y = np.cos(_a), np.sin(_a)
    ax3.plot([0, _x], [0, _y], color=ACCENT, linewidth=2.2)
    ax3.plot([_x], [_y], marker="o", markersize=5, color=ACCENT, zorder=3)
    # x 軸とのあいだの鋭角（参照角）に弧をかく
    _th = np.linspace(min(_a, _b), max(_a, _b), 60)
    ax3.plot(0.34 * np.cos(_th), 0.34 * np.sin(_th), color=WARM, linewidth=1.8)
    _m = 0.5 * (_a + _b)
    ax3.text(0.52 * np.cos(_m), 0.52 * np.sin(_m), r"$\alpha$", fontsize=11,
             color=WARM, ha="center", va="center")
    ax3.text(_lp[0], _lp[1], _lab, fontsize=11, color=ACCENT)
    ax3.text(0.84 * np.cos(_pa), 0.84 * np.sin(_pa), _pos, fontsize=10.5,
             color=GREEN, ha="center", va="center")

ax3.plot([0], [0], marker="o", markersize=4.5, color=INK, zorder=3)


fig4, ax4 = plt.subplots(figsize=(5.3, 4.9))
fig5, ax5 = plt.subplots(figsize=(5.3, 4.9))
# ══════════════════════════════════════════════════════════
# (a) 2 つの三角形
# ══════════════════════════════════════════════════════════
ax4.set_title("The two special triangles", fontsize=11, color=INK,
              loc="left", pad=10)
ax4.set_xlim(-0.35, 5.6)
ax4.set_ylim(-0.62, 1.85)
ax4.set_aspect("equal")
ax4.axis("off")


def rt(ax, x0, y0, col, d=0.17):
    """直角の印を (x0, y0) の角に置く（直角は左下）。"""
    ax.plot([x0 + d, x0 + d, x0], [y0, y0 + d, y0 + d], color=col,
            linewidth=1.0)


# 45-45-90
ax4.plot([0, 1.6, 0, 0], [0, 0, 1.6, 0], color=ACCENT, linewidth=2.0)
rt(ax4, 0, 0, GREY)
ax4.text(0.72, -0.36, "$1$", fontsize=11, color=INK)
ax4.text(-0.30, 0.72, "$1$", fontsize=11, color=INK)
ax4.text(0.86, 0.86, "$\\sqrt{2}$", fontsize=11, color=INK)
ax4.text(1.05, 0.13, "$\\frac{\\pi}{4}$", fontsize=11, color=GREEN)
ax4.text(0.09, 1.20, "$\\frac{\\pi}{4}$", fontsize=11, color=GREEN)

# 30-60-90
bx = 3.1
ax4.plot([bx, bx + 1.75, bx, bx], [0, 0, 1.01, 0], color=ACCENT, linewidth=2.0)
rt(ax4, bx, 0, GREY)
ax4.text(bx + 0.80, -0.36, "$\\sqrt{3}$", fontsize=11, color=INK)
ax4.text(bx - 0.30, 0.44, "$1$", fontsize=11, color=INK)
ax4.text(bx + 0.94, 0.60, "$2$", fontsize=11, color=INK)
ax4.text(bx + 1.16, 0.11, "$\\frac{\\pi}{6}$", fontsize=11, color=GREEN)
ax4.text(bx + 0.09, 0.66, "$\\frac{\\pi}{3}$", fontsize=11, color=GREEN)


# ══════════════════════════════════════════════════════════
# (b) あいまいな場合
# ══════════════════════════════════════════════════════════
ax5.set_title("The ambiguous case", fontsize=11, color=INK, loc="left",
              pad=10)
ax5.set_xlim(-0.7, 7.6)
ax5.set_ylim(-0.95, 4.75)
ax5.set_aspect("equal")
ax5.axis("off")

A = np.array([0.0, 0.0])
ang = np.deg2rad(30.0)
b = 5.0                      # AC = b（角 A の一方の辺）
C = A + b * np.array([np.cos(ang), np.sin(ang)])
a = 3.0                      # CB = a（A の向かいの辺）
dx = np.sqrt(a ** 2 - C[1] ** 2)
B1 = np.array([C[0] - dx, 0.0])
B2 = np.array([C[0] + dx, 0.0])

ax5.annotate("", xy=(7.1, 0), xytext=(A[0], A[1]),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
ax5.plot([A[0], C[0]], [A[1], C[1]], color=ACCENT, linewidth=2.2)

tt = np.linspace(0, 2 * np.pi, 300)
ax5.plot(C[0] + a * np.cos(tt), C[1] + a * np.sin(tt), color=GREY,
         linewidth=1.0, linestyle=(0, (4, 4)))
ax5.plot([C[0], B1[0]], [C[1], B1[1]], color=WARM, linewidth=2.0)
ax5.plot([C[0], B2[0]], [C[1], B2[1]], color=WARM, linewidth=2.0)

ax5.plot([C[0], C[0]], [0, C[1]], color=GREEN, linewidth=1.4,
         linestyle=(0, (3, 3)))

for _p, _lab, _dx, _dy in [(A, "$A$", -0.34, -0.30), (C, "$C$", 0.10, 0.14),
                           (B1, "$B_{1}$", -0.16, -0.52),
                           (B2, "$B_{2}$", -0.16, -0.52)]:
    ax5.plot([_p[0]], [_p[1]], marker="o", markersize=5.2, color=INK, zorder=3)
    ax5.text(_p[0] + _dx, _p[1] + _dy, _lab, fontsize=11, color=INK)

ta = np.linspace(0, ang, 60)
ax5.plot(A[0] + 0.85 * np.cos(ta), A[1] + 0.85 * np.sin(ta), color=INK,
         linewidth=1.2)
ax5.text(0.95, 0.16, "$A$", fontsize=11, color=INK)

ax5.text(2.0, 1.62, "$b$", fontsize=11, color=ACCENT)
ax5.text(3.55, 1.62, "$a$", fontsize=11, color=WARM)
ax5.text(5.20, 1.62, "$a$", fontsize=11, color=WARM)
ax5.text(C[0] + 0.10, 1.00, "$b\\sin A$", fontsize=10, color=GREEN)

for _fig, _name in ((fig1, "aasl-3-5-idea-a.svg"),
                    (figX, "aasl-3-5-axes.svg"),
                    (fig2, "aasl-3-5-idea-b.svg"),
                    (fig3, "aasl-3-5-idea-c.svg"),
                    (fig4, "aasl-3-5-idea-d.svg"),
                    (fig5, "aasl-3-5-idea-e.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
