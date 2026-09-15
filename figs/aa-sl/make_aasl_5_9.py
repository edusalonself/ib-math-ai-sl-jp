"""AA SL 5.9 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_9.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_9.py

出力: aa-sl/05-calculus/img/aasl-5-9-idea.svg

(a) v-t グラフ。displacement は符号つきの和、distance は大きさの和。
(b) s → v → a のつながり（下は微分、上は積分）。

★ 目盛りの数も式も入れません。交点は t1、t2 と呼びます（例題・演習と
   重ならないように）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * \\bigl \\bigr \\Box は読めない → ふつうの ( ) と文字を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#e8f0f9"
SHADE = "#fdf0dc"

T1, T2, TEND = 1.0, 2.6, 4.2
T = np.linspace(0, TEND, 400)
V = (T - T1) * (T - T2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.2))

# ══════════════════════════════════════════════════════════
# (a) v-t グラフ
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Reading a velocity-time graph", fontsize=11, color=INK,
              loc="left", pad=12)
ax1.plot(T, V, color=ACCENT, linewidth=2.2)
ax1.axhline(0, color=GREY, linewidth=1.0)
ax1.set_xlim(-0.25, TEND + 0.35)
ax1.set_ylim(-1.9, 4.6)
ax1.set_xticks([])
ax1.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax1.spines[_s].set_visible(False)
ax1.text(-0.2, 4.3, "$v$", fontsize=11, color=ACCENT)
ax1.text(TEND + 0.25, -0.30, "$t$", fontsize=11, color=GREY, ha="center",
         va="top")
for _tv, _tl in ((T1, "$t_{1}$"), (T2, "$t_{2}$")):
    ax1.plot([_tv, _tv], [-0.10, 0.10], color=GREY, linewidth=1.0)
    ax1.text(_tv, -0.30, _tl, fontsize=10, color=GREY, ha="center", va="top")

_m1 = T <= T1
_m2 = (T >= T1) & (T <= T2)
_m3 = T >= T2
ax1.fill_between(T[_m1], 0, V[_m1], color=FILL, edgecolor=ACCENT,
                 linewidth=0.7)
ax1.fill_between(T[_m2], 0, V[_m2], color=SHADE, edgecolor=WARM,
                 linewidth=0.7)
ax1.fill_between(T[_m3], 0, V[_m3], color=FILL, edgecolor=ACCENT,
                 linewidth=0.7)

ax1.text(0.42, 0.60, "$A_{1}$", fontsize=12, color=ACCENT, ha="center")
ax1.text(1.8, -0.55, "$A_{2}$", fontsize=12, color=WARM, ha="center")
ax1.text(3.55, 0.55, "$A_{3}$", fontsize=12, color=ACCENT, ha="center")

ax1.text(0.42, 2.55, "$v > 0$", fontsize=9.5, color=ACCENT, ha="center")
ax1.text(1.8, -1.35, "$v < 0$", fontsize=9.5, color=WARM, ha="center")
ax1.text(3.30, 3.45, "$v > 0$", fontsize=9.5, color=ACCENT, ha="center")

ax1.text(-0.25, -2.35,
         "$A_{1}$, $A_{2}$, $A_{3}$ are areas, so each one is positive",
         fontsize=9.5, color=GREY, ha="left", va="center")
ax1.text(-0.25, -3.05, "displacement $= A_{1} - A_{2} + A_{3}$", fontsize=10.5,
         color=INK, ha="left", va="center")
ax1.text(-0.25, -3.75, "distance $= A_{1} + A_{2} + A_{3}$", fontsize=10.5,
         color=WARM, ha="left", va="center")
ax1.text(-0.25, -4.45, "the particle changes direction at $t_{1}$ and $t_{2}$",
         fontsize=9.5, color=GREY, ha="left", va="center")
ax1.set_clip_on(False)

# ══════════════════════════════════════════════════════════
# (b) s → v → a
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) How $s$, $v$ and $a$ are linked", fontsize=11, color=INK,
              loc="left", pad=12)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")

BOX = dict(boxstyle="round,pad=0.42", facecolor=FILL, edgecolor=ACCENT,
           linewidth=1.3)
XS = (1.55, 5.0, 8.45)
NAMES = ("$s$", "$v$", "$a$")
SUB = ("displacement", "velocity", "acceleration")
for _x, _n, _sub in zip(XS, NAMES, SUB):
    ax2.text(_x, 6.4, _n, fontsize=15, color=ACCENT, ha="center",
             va="center", bbox=BOX)
    ax2.text(_x, 5.25, _sub, fontsize=9.5, color=GREY, ha="center",
             va="center")

for _a, _b in ((XS[0], XS[1]), (XS[1], XS[2])):
    ax2.annotate("", xy=(_b - 0.75, 6.95), xytext=(_a + 0.75, 6.95),
                 arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.4,
                                 connectionstyle="arc3,rad=-0.25"))
    ax2.annotate("", xy=(_a + 0.75, 5.85), xytext=(_b - 0.75, 5.85),
                 arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.4,
                                 connectionstyle="arc3,rad=-0.25"))

ax2.text(3.3, 8.35, "differentiate", fontsize=10, color=WARM, ha="center")
ax2.text(6.75, 8.35, "differentiate", fontsize=10, color=WARM, ha="center")
ax2.text(3.3, 4.05, "integrate", fontsize=10, color=INK, ha="center")
ax2.text(6.75, 4.05, "integrate", fontsize=10, color=INK, ha="center")

ax2.plot([0.2, 9.8], [3.1, 3.1], color=GREY, linewidth=0.9)
ax2.text(0.25, 2.35, "speed $= |v|$, so speed is never negative",
         fontsize=10.5, color=INK, va="center")
ax2.text(0.25, 1.55, "the particle is at rest when $v = 0$, not when $a = 0$",
         fontsize=10, color=WARM, va="center")
ax2.text(0.25, 0.75, "integrating needs a starting value to fix $C$",
         fontsize=9.5, color=GREY, va="center")

fig.tight_layout(w_pad=2.4, rect=(0, 0.16, 1, 1))
path = os.path.join(OUT, "aasl-5-9-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
