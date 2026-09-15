"""AA SL 5.10b の図をつくる。

    python3 figs/aa-sl/make_aasl_5_10b.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_10b.py

出力: aa-sl/05-calculus/img/aasl-5-10b-idea.svg

(a) 見分ける形。k g'(x) f(g(x)) の、どこが「中身」でどこが「中身の導関数」か。
(b) 置換積分の流れ。u を置く → du に直す → u で積分 → x にもどす。

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.2))

# ══════════════════════════════════════════════════════════
# (a) 形を見分ける
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Spotting the pattern", fontsize=11, color=INK,
              loc="left", pad=12)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

ax1.text(5.0, 7.5, "$\\int k\\,g'(x)\\,f(g(x))\\,dx$", fontsize=17,
         color=ACCENT, ha="center", va="center")

ax1.annotate("", xy=(3.95, 6.85), xytext=(2.4, 5.75),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.4))
ax1.annotate("", xy=(6.05, 6.85), xytext=(7.6, 5.75),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.4))
ax1.text(2.2, 5.3, "the derivative\nof the inside", fontsize=10.5,
         color=WARM, ha="center", va="center")
ax1.text(7.8, 5.3, "the inside,\n$u = g(x)$", fontsize=10.5,
         color=WARM, ha="center", va="center")

ax1.plot([0.2, 9.8], [4.2, 4.2], color=GREY, linewidth=0.9)
ax1.text(0.25, 3.5, "$k$ is a constant, so it can be adjusted",
         fontsize=10.5, color=INK, va="center")
ax1.text(0.25, 2.7, "the extra factor must be $g'(x)$, not just any function",
         fontsize=10.5, color=WARM, va="center")
ax1.text(0.25, 1.9, "with no such factor, this method does not apply",
         fontsize=10.5, color=INK, va="center")
ax1.text(0.25, 1.1, "$g(x) = ax + b$ is the special case of SL 5.10a",
         fontsize=9.5, color=GREY, va="center")

# ══════════════════════════════════════════════════════════
# (b) 置換積分の流れ
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Integration by substitution", fontsize=11, color=INK,
              loc="left", pad=12)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")

BOX = dict(boxstyle="round,pad=0.40", facecolor=FILL, edgecolor=ACCENT,
           linewidth=1.3)
SBOX = dict(boxstyle="round,pad=0.40", facecolor=SHADE, edgecolor=WARM,
            linewidth=1.3)

YS = (8.6, 6.5, 4.4, 2.3)
TXT = ("$\\int k\\,g'(x)\\,f(g(x))\\,dx$",
       "$u = g(x), \\quad du = g'(x)\\,dx$",
       "$k\\int f(u)\\,du$",
       "answer in $u$, add $+C$, then put $g(x)$ back")
for _i, (_y, _t) in enumerate(zip(YS, TXT)):
    ax2.text(5.0, _y, _t, fontsize=12.5, color=ACCENT if _i != 1 else WARM,
             ha="center", va="center", bbox=BOX if _i != 1 else SBOX)

for _y0, _y1 in ((YS[0], YS[1]), (YS[1], YS[2]), (YS[2], YS[3])):
    ax2.annotate("", xy=(5.0, _y1 + 0.62), xytext=(5.0, _y0 - 0.62),
                 arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.4))

ax2.plot([0.2, 9.8], [1.25, 1.25], color=GREY, linewidth=0.9)
ax2.text(0.25, 0.55, "every $x$ must disappear before integrating in $u$",
         fontsize=10.5, color=WARM, va="center")

fig.tight_layout(w_pad=2.4, rect=(0, 0.16, 1, 1))
path = os.path.join(OUT, "aasl-5-10b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
