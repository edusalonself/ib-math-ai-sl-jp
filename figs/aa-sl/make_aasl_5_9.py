"""AA SL 5.9 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_9.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_9.py

出力: aa-sl/05-calculus/img/aasl-5-9-idea-a.svg
      aa-sl/05-calculus/img/aasl-5-9-idea-b.svg

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

fig1, ax1 = plt.subplots(figsize=(6.4, 3.4))
fig2, ax2 = plt.subplots(figsize=(7.8, 3.6))
# ══════════════════════════════════════════════════════════
# (a) v-t グラフ
# ══════════════════════════════════════════════════════════
ax1.set_title("Reading a velocity-time graph", fontsize=11, color=INK,
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


# ══════════════════════════════════════════════════════════
# (b) s → v → a
# ══════════════════════════════════════════════════════════
# ★ ラベルは必ず ylim の中に置くこと（外に置くと図がずれます）。
ax2.set_title("How $s$, $v$ and $a$ are linked", fontsize=11, color=INK,
              loc="left", pad=8)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 5.3)
ax2.axis("off")

BOX = dict(boxstyle="round,pad=0.42", facecolor=FILL, edgecolor=ACCENT,
           linewidth=1.3)
XS = (1.45, 5.0, 8.55)
NAMES = ("$s$", "$v$", "$a$")
SUB = ("displacement", "velocity", "acceleration")
for _x, _n, _sub in zip(XS, NAMES, SUB):
    ax2.text(_x, 2.62, _n, fontsize=15, color=ACCENT, ha="center",
             va="center", bbox=BOX)
    ax2.text(_x, 1.88, _sub, fontsize=9.5, color=GREY, ha="center",
             va="center")

DIFF = (r"differentiate:  $\frac{ds}{dt} = v$",
        r"differentiate:  $\frac{dv}{dt} = a$")
INTEG = (r"integrate:  $s = \int v\,dt$",
         r"integrate:  $v = \int a\,dt$")
for _k, (_a, _b) in enumerate(((XS[0], XS[1]), (XS[1], XS[2]))):
    _mid = (_a + _b) / 2
    # 上：微分（左から右へ）
    ax2.annotate("", xy=(_b - 0.62, 3.30), xytext=(_a + 0.62, 3.30),
                 arrowprops=dict(arrowstyle="-|>", color=WARM, linewidth=1.5,
                                 connectionstyle="arc3,rad=-0.28"))
    ax2.text(_mid, 4.55, DIFF[_k], fontsize=10.5, color=WARM, ha="center",
             va="center")
    # 下：積分（右から左へ）
    ax2.annotate("", xy=(_a + 0.62, 1.30), xytext=(_b - 0.62, 1.30),
                 arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.5,
                                 connectionstyle="arc3,rad=-0.28"))
    ax2.text(_mid, 0.42, INTEG[_k], fontsize=10.5, color=INK, ha="center",
             va="center")

for _fig, _name in ((fig1, "aasl-5-9-idea-a.svg"), (fig2, "aasl-5-9-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
