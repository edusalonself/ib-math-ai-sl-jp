"""AA HL 1.13（極形式・Euler 形と、積と商）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_13.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_13.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-13-idea-a.svg
      aa-hl/01-number-and-algebra/img/aahl-1-13-idea-b.svg
      aa-hl/01-number-and-algebra/img/aahl-1-13-idea-c.svg

(a) 掛け算：偏角は足し算、絶対値は掛け算。
    z1 = 2e^(iπ/3), z2 = 3e^(iπ/6), z1z2 = 6e^(iπ/2)。
(b) 足し算：平行四辺形。(3+2i) + (1+4i) = 4+6i。

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
GREEN = "#15803d"

fig1, ax1 = plt.subplots(figsize=(5.6, 4.6))
fig2, ax2 = plt.subplots(figsize=(5.6, 4.6))
fig3, ax3 = plt.subplots(figsize=(5.2, 4.6))


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
    ax.text(xhi, 0.16, "Re", ha="right", va="bottom", fontsize=10, color=INK)
    ax.text(0.16, yhi, "Im", ha="left", va="top", fontsize=10, color=INK)


def ray(ax, r, t, color, label, lw=1.8, dy=0.22):
    ax.annotate("", xy=(r * np.cos(t), r * np.sin(t)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=color, linewidth=lw))
    ax.text(r * np.cos(t) + 0.12, r * np.sin(t) + dy, label,
            ha="left", va="bottom", fontsize=10.5, color=color)


def arc(ax, rad, t0, t1, color, label, lr=None):
    _t = np.linspace(t0, t1, 200)
    ax.plot(rad * np.cos(_t), rad * np.sin(_t), color=color, linewidth=1.4,
            zorder=4)
    _m = 0.5 * (t0 + t1)
    _lr = lr if lr is not None else rad + 0.28
    ax.text(_lr * np.cos(_m), _lr * np.sin(_m), label, ha="center",
            va="center", fontsize=10.5, color=color)


# ══════════════════════════════════════════════════════════
# (a) 掛け算：角は足す、長さは掛ける
# ══════════════════════════════════════════════════════════
axes(ax1, -1.2, 5.2, -0.9, 5.0)
T1, T2, R1, R2 = 0.75, 0.35, 2.2, 1.7
ray(ax1, R2, T2, WARM, "$z_2$", dy=-0.52)
ray(ax1, R1, T1, ACCENT, "$z_1$", dy=0.10)
ax1.annotate("", xy=(R1 * R2 * np.cos(T1 + T2), R1 * R2 * np.sin(T1 + T2)),
             xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=2.4))
ax1.text(R1 * R2 * np.cos(T1 + T2) - 0.18,
         R1 * R2 * np.sin(T1 + T2) + 0.10, "$z_1z_2$", ha="right",
         va="bottom", fontsize=10.5, color=INK)
arc(ax1, 0.60, 0.0, T2, WARM, "$\\theta_2$", lr=0.86)
arc(ax1, 1.05, T2, T1 + T2, ACCENT, "$\\theta_1$", lr=1.55)
ax1.text(2.30, 4.55, "modulus $r_1r_2$", ha="left", va="center",
         fontsize=10, color=INK)
ax1.text(2.30, 4.05, "argument $\\theta_1 + \\theta_2$", ha="left",
         va="center", fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 足し算：平行四辺形
# ══════════════════════════════════════════════════════════
axes(ax2, -1.3, 6.2, -0.8, 7.8)
A = np.array([3.0, 2.0])
B = np.array([1.0, 4.0])
S = A + B
for _v, _c, _lab, _dx, _dy, _ha, _va in (
        (A, ACCENT, "$z_1$", 0.18, -0.18, "left", "top"),
        (B, WARM, "$z_2$", -0.18, 0.16, "right", "bottom"),
        (S, INK, "$z_1+z_2$", 0.20, 0.0, "left", "center")):
    ax2.annotate("", xy=tuple(_v), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=_c,
                                 linewidth=2.4 if _ha == "left" and _lab.startswith("$z_1+") else 1.8))
    ax2.text(_v[0] + _dx, _v[1] + _dy, _lab, ha=_ha, va=_va,
             fontsize=10.5, color=_c)
ax2.plot([A[0], S[0]], [A[1], S[1]], linestyle=(0, (3, 3)), linewidth=1.2,
         color=GREY, zorder=2)
ax2.plot([B[0], S[0]], [B[1], S[1]], linestyle=(0, (3, 3)), linewidth=1.2,
         color=GREY, zorder=2)


# ══════════════════════════════════════════════════════════
# (c) i をかけると 1/4 回転
# ══════════════════════════════════════════════════════════
ax3.set_xlim(-3.9, 4.3)
ax3.set_ylim(-1.1, 4.3)
ax3.set_aspect("equal")
ax3.axis("off")

ax3.annotate("", xy=(4.0, 0), xytext=(-3.6, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.0))
ax3.annotate("", xy=(0, 4.0), xytext=(0, -0.9),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.0))
ax3.text(4.05, -0.30, "Re", fontsize=10, color=GREY, ha="right")
ax3.text(0.14, 4.05, "Im", fontsize=10, color=GREY, va="top")
for _t in (-3, -2, -1, 1, 2, 3):
    ax3.plot([_t, _t], [-0.07, 0.07], color=GREY, linewidth=0.9)
    if _t > 0:
        ax3.text(_t, -0.33, "$%d$" % _t, fontsize=9, color=GREY, ha="center")
for _t in (1, 2, 3):
    ax3.plot([-0.07, 0.07], [_t, _t], color=GREY, linewidth=0.9)
    ax3.text(-0.16, _t, "$%d$" % _t, fontsize=9, color=GREY, ha="right",
             va="center")
ax3.text(-2, -0.33, "$-2$", fontsize=9, color=GREY, ha="center")

P = (3.0, 2.0)
Q = (-2.0, 3.0)
ax3.annotate("", xy=P, xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=2.0))
ax3.annotate("", xy=Q, xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=2.0))
ax3.plot([P[0]], [P[1]], "o", markersize=5, color=ACCENT, zorder=3)
ax3.plot([Q[0]], [Q[1]], "o", markersize=5, color=WARM, zorder=3)
ax3.text(P[0] + 0.18, P[1] - 0.05, "$3+2i$", fontsize=10.5, color=ACCENT,
         va="center")
ax3.text(Q[0] - 0.18, Q[1] + 0.05, "$-2+3i$", fontsize=10.5, color=WARM,
         ha="right", va="center")

_a0 = np.arctan2(P[1], P[0])
_arc = np.linspace(_a0, _a0 + np.pi / 2, 60)
_R = 2.55
ax3.plot(_R * np.cos(_arc), _R * np.sin(_arc), color=GREEN, linewidth=1.4)
ax3.annotate("", xy=(_R * np.cos(_arc[-1]), _R * np.sin(_arc[-1])),
             xytext=(_R * np.cos(_arc[-6]), _R * np.sin(_arc[-6])),
             arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.4))
_m = _a0 + np.pi / 4
ax3.text(2.95 * np.cos(_m), 2.95 * np.sin(_m), r"$\times i$", fontsize=11,
         color=GREEN, ha="center", va="center")

for _fig, _name in ((fig1, "aahl-1-13-idea-a.svg"),
                    (fig2, "aahl-1-13-idea-b.svg"),
                    (fig3, "aahl-1-13-idea-c.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
