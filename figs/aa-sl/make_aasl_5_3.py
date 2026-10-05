"""AA SL 5.3 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_3.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_3.py

出力: aa-sl/05-calculus/img/aasl-5-3-idea-a.svg

(a) べき乗の微分の規則を、2 つの動きに分けて見せる。
    枠は中身に合わせて低くしてある（上下に空白を作らない）。

★ 数値は入れません。文字だけです（例題・演習と重ならないように）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

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

fig1, ax1 = plt.subplots(figsize=(6.4, 1.8))
# ══════════════════════════════════════════════════════════
# (a) べき乗の微分の 2 つの動き
# ══════════════════════════════════════════════════════════
ax1.set_title("Two things happen to the power", fontsize=11, color=INK,
              loc="left", pad=6)
ax1.set_xlim(0, 10)
ax1.set_ylim(6.9, 9.0)
ax1.axis("off")

ax1.text(2.4, 7.6, r"$x^{n}$", fontsize=20, color=ACCENT, ha="center",
         va="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=FILL,
                   edgecolor=ACCENT, linewidth=1.3))
ax1.text(7.6, 7.6, r"$n\,x^{\,n-1}$", fontsize=20, color=ACCENT, ha="center",
         va="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=FILL,
                   edgecolor=ACCENT, linewidth=1.3))
ax1.annotate("", xy=(6.2, 7.6), xytext=(3.8, 7.6),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.6))
ax1.text(5.0, 8.5, "differentiate", fontsize=9.5, color=GREY, ha="center")


for _fig, _name in ((fig1, "aasl-5-3-idea-a.svg"),):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
