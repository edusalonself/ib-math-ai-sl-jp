"""AA SL 3.8 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_8.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_8.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-8-idea-a.svg
      aa-sl/03-geometry/img/aasl-3-8-idea-c.svg
      aa-sl/03-geometry/img/aasl-3-8-idea-d.svg
      aa-sl/03-geometry/img/aasl-3-8-idea-e.svg

(a) y = sin x と y = k。交点の数が解の数。
(c) sin は単位円の y 座標。横線 y = k との交点。
(d) cos は単位円の x 座標。縦線 x = k との交点。
(e) tan は (1,0) での接線の高さ。原点と (1,k) を結ぶ直線との交点。
    (c)(d)(e) には参照角 α の弧も入れてある。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（(a) の高さは k のまま）。
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

fig1, ax1 = plt.subplots(figsize=(5.4, 4.4))
fig3, ax3 = plt.subplots(figsize=(4.8, 4.6))
fig4, ax4 = plt.subplots(figsize=(4.8, 4.6))
fig5, ax5 = plt.subplots(figsize=(6.2, 4.6))
# ══════════════════════════════════════════════════════════
# (a) 交点の数が解の数
# ══════════════════════════════════════════════════════════
ax1.set_title("Reading the number of solutions", fontsize=11, color=INK,
              loc="left", pad=10)
x = np.linspace(0, 2 * np.pi, 700)
K = 0.62
ax1.plot(x, np.sin(x), color=ACCENT, linewidth=2.2)
ax1.axhline(K, color=WARM, linewidth=1.6, linestyle=(0, (6, 3)))
ax1.axhline(0, color=GREY, linewidth=1.0)
for _r in (np.arcsin(K), np.pi - np.arcsin(K)):
    ax1.plot([_r], [K], marker="o", markersize=6.0, color=INK, zorder=3)
    ax1.plot([_r, _r], [0, K], color=GREY, linewidth=0.9,
             linestyle=(0, (2, 3)))
ax1.set_xlim(-0.25, 2 * np.pi + 0.25)
ax1.set_ylim(-1.45, 1.95)
ax1.set_xticks([0, np.pi, 2 * np.pi])
ax1.set_xticklabels(["$0$", "$\\pi$", "$2\\pi$"], fontsize=9.5)
ax1.set_yticks([-1, 0, 1])
ax1.set_yticklabels(["$-1$", "$0$", "$1$"], fontsize=9.5)
for _sp in ("top", "right", "left", "bottom"):
    ax1.spines[_sp].set_visible(False)
ax1.tick_params(length=0, colors=GREY)
ax1.text(2 * np.pi + 0.05, K - 0.02, "$y = k$", fontsize=10.5, color=WARM)
ax1.text(0.05, 1.62, "$y = \\sin x$", fontsize=10.5, color=ACCENT)



# ══════════════════════════════════════════════════════════
# (c) 単位円に線を引いて、もう 1 つの解を読む
# ══════════════════════════════════════════════════════════
_tc = np.linspace(0, 2 * np.pi, 400)


def _circle(ax, title):
    ax.set_title(title, fontsize=11, color=INK, loc="left", pad=10)
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.55, 1.55)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot(np.cos(_tc), np.sin(_tc), color=GREY, linewidth=1.2)
    ax.annotate("", xy=(1.45, 0), xytext=(-1.45, 0),
                arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1.0))
    ax.annotate("", xy=(0, 1.40), xytext=(0, -1.40),
                arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1.0))
    ax.plot([0], [0], marker="o", markersize=4, color=INK, zorder=3)


def _arm(ax, a, col, lab, dx, dy):
    ax.plot([0, np.cos(a)], [0, np.sin(a)], color=col, linewidth=2.2)
    ax.plot([np.cos(a)], [np.sin(a)], marker="o", markersize=5.5, color=col,
            zorder=3)
    ax.text(np.cos(a) + dx, np.sin(a) + dy, lab, fontsize=11, color=col)


def _refarc(ax, a, r=0.30):
    """x 軸と半径のなす鋭角（参照角）に、小さな弧をかく。"""
    _b = 0.0 if np.cos(a) >= 0 else np.pi
    _t = np.linspace(min(a, _b), max(a, _b), 60)
    ax.plot(r * np.cos(_t), r * np.sin(_t), color=GREEN, linewidth=1.6)
    _mid = (a + _b) / 2.0
    ax.text((r + 0.18) * np.cos(_mid), (r + 0.18) * np.sin(_mid),
            r"$\alpha$", fontsize=11, color=GREEN, ha="center", va="center")


_k = 0.62

# 左：sin は y 座標
_circle(ax3, r"$\sin\theta = k$")
_al = np.arcsin(_k)
ax3.plot([-1.45, 1.45], [_k, _k], color=WARM, linewidth=1.8)
ax3.text(1.00, _k - 0.30, "$y = k$", fontsize=10.5, color=WARM)
ax3.plot([0, 0], [0, _k], color=WARM, linewidth=3.4, solid_capstyle="butt",
         zorder=4)
_arm(ax3, _al, ACCENT, r"$\alpha$", 0.06, 0.14)
_arm(ax3, np.pi - _al, ACCENT, r"$\pi-\alpha$", -0.70, 0.14)
_refarc(ax3, _al)

# 中：cos は x 座標
_circle(ax4, r"$\cos\theta = k$")
_be = np.arccos(_k)
ax4.plot([_k, _k], [-1.40, 1.40], color=WARM, linewidth=1.8)
ax4.text(_k + 0.10, 1.20, "$x = k$", fontsize=10.5, color=WARM)
ax4.plot([0, _k], [0, 0], color=WARM, linewidth=3.4, solid_capstyle="butt",
         zorder=4)
_arm(ax4, _be, ACCENT, r"$\alpha$", 0.14, 0.10)
_arm(ax4, -_be, ACCENT, r"$2\pi-\alpha$", 0.14, -0.26)
_refarc(ax4, _be)

# 右：tan は (1,0) での接線の高さ
_circle(ax5, r"$\tan\theta = k$")
ax5.set_xlim(-1.65, 2.65)
_kt = 0.80
_ga = np.arctan(_kt)
ax5.plot([-1.22, 1.22], [-1.22 * _kt, 1.22 * _kt], color=ACCENT,
         linewidth=1.1, linestyle=(0, (4, 3)), zorder=1)
ax5.plot([1, 1], [-1.40, 1.40], color=GREY, linewidth=1.2,
         linestyle=(0, (5, 3)))
ax5.text(1.08, -1.38, "tangent at $(1,0)$", fontsize=9.5, color=GREY)
ax5.plot([1, 1], [0, _kt], color=WARM, linewidth=3.4, solid_capstyle="butt",
         zorder=4)
ax5.plot([1], [_kt], marker="o", markersize=5.5, color=WARM, zorder=5)
ax5.text(1.10, _kt - 0.08, r"$(1,\,k)$", fontsize=10.5, color=WARM)
_arm(ax5, _ga, ACCENT, r"$\alpha$", -0.12, 0.20)
_arm(ax5, _ga + np.pi, ACCENT, r"$\pi+\alpha$", -0.92, -0.26)
_refarc(ax5, _ga)

for _fig, _name in ((fig1, "aasl-3-8-idea-a.svg"),
                    (fig3, "aasl-3-8-idea-c.svg"),
                    (fig4, "aasl-3-8-idea-d.svg"),
                    (fig5, "aasl-3-8-idea-e.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
