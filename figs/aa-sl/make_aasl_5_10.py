"""AA SL 5.10 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_10.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_10.py

      aa-sl/05-calculus/img/aasl-5-10-linear.svg

(linear) ax + b との合成。微分すると a がかかるので、積分では a で割る。

★ 具体的な数値や答えは入れません。ラベルはすべて英語です。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * \\bigl \\bigr \\Box は読めない → ふつうの ( ) と文字を使う
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

figL, axL = plt.subplots(figsize=(6.6, 2.7))
# ══════════════════════════════════════════════════════════
# (linear) ax + b との合成
# ══════════════════════════════════════════════════════════
axL.set_title("Integrating $f'(ax + b)$", fontsize=11, color=INK,
              loc="left", pad=10)
axL.set_xlim(0, 10)
axL.set_ylim(0.15, 3.65)
axL.axis("off")

BOX = dict(boxstyle="round,pad=0.42", facecolor=FILL, edgecolor=ACCENT,
           linewidth=1.3)
axL.text(2.3, 1.9, "$f(ax + b)$", fontsize=14, color=ACCENT, ha="center",
         va="center", bbox=BOX)
axL.text(7.7, 1.9, "$a\\,f'(ax + b)$", fontsize=14, color=ACCENT,
         ha="center", va="center", bbox=BOX)

axL.annotate("", xy=(6.15, 2.42), xytext=(3.85, 2.42),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.4,
                             connectionstyle="arc3,rad=-0.30"))
axL.text(5.0, 3.32, "differentiate:  $\\times a$", fontsize=11.5,
         color=WARM, ha="center", va="center")

axL.annotate("", xy=(3.85, 1.38), xytext=(6.15, 1.38),
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.4,
                             connectionstyle="arc3,rad=-0.30"))
axL.text(5.0, 0.48, "integrate:  $\\times \\frac{1}{a}$", fontsize=11.5,
         color=INK, ha="center", va="center")

for _fig, _name in ((figL, "aasl-5-10-linear.svg"),):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
