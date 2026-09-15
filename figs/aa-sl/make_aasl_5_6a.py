"""AA SL 5.6a の図をつくる。

    python3 figs/aa-sl/make_aasl_5_6a.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_6a.py

出力: aa-sl/05-calculus/img/aasl-5-6a-idea.svg

(a) 合成関数を「2 段の機械」として見る。連鎖律は 2 つの傾きのかけ算。
(b) 外側と内側の見分け方（かっこの中が内側）。

★ 数値の答えは入れません（例題・演習と重ならないように）。

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 5.0))

# ══════════════════════════════════════════════════════════
# (a) 2 段の機械
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) A composite function is two steps", fontsize=11, color=INK,
              loc="left", pad=12)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

BOXI = dict(boxstyle="round,pad=0.45", facecolor=SHADE, edgecolor=WARM,
            linewidth=1.3)
BOXO = dict(boxstyle="round,pad=0.45", facecolor=FILL, edgecolor=ACCENT,
            linewidth=1.3)

ax1.text(1.15, 8.3, "$x$", fontsize=13, color=INK, ha="center", va="center")
ax1.text(4.1, 8.3, "$u = g(x)$", fontsize=12.5, color=WARM, ha="center",
         va="center", bbox=BOXI)
ax1.text(8.05, 8.3, "$y = f(u)$", fontsize=12.5, color=ACCENT, ha="center",
         va="center", bbox=BOXO)

ax1.annotate("", xy=(2.85, 8.3), xytext=(1.7, 8.3),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.5))
ax1.annotate("", xy=(6.75, 8.3), xytext=(5.45, 8.3),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.5))

ax1.text(2.28, 9.05, "inside", fontsize=9.5, color=WARM, ha="center")
ax1.text(6.10, 9.05, "outside", fontsize=9.5, color=ACCENT, ha="center")

ax1.text(4.1, 6.7, r"$\frac{du}{dx} = g'(x)$", fontsize=12, color=WARM,
         ha="center", va="center")
ax1.text(8.05, 6.7, r"$\frac{dy}{du} = f'(u)$", fontsize=12, color=ACCENT,
         ha="center", va="center")

ax1.text(0.15, 4.6, "the two rates multiply:", fontsize=10.5, color=INK)
ax1.text(0.6, 3.2, r"$\frac{dy}{dx} = \frac{dy}{du} \times \frac{du}{dx}$",
         fontsize=17, color=ACCENT)
ax1.text(0.15, 1.35, "differentiate the outside, leaving the inside alone,",
         fontsize=10, color=INK)
ax1.text(0.15, 0.55, "then multiply by the derivative of the inside",
         fontsize=10, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) 外側と内側の見分け方
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Which part is the inside?", fontsize=11, color=INK,
              loc="left", pad=12)
ax2.set_xlim(-0.2, 10.2)
ax2.set_ylim(-0.3, 10)
ax2.axis("off")

ax2.text(0.9, 9.7, "outside", fontsize=10, color=GREY, ha="center")
ax2.text(6.2, 9.7, "inside", fontsize=10, color=GREY, ha="left")

ROWS = ((8.55, r"$(\,u\,)^{n}$", "raise to a power"),
        (6.75, r"$e^{\,u}$", "exponential"),
        (4.95, r"$\sin(\,u\,)$", "sine"),
        (3.15, r"$\ln(\,u\,)$", "natural log"))
for _y, _sym, _name in ROWS:
    ax2.text(0.9, _y, _sym, fontsize=15, color=ACCENT, ha="center",
             va="center")
    ax2.text(2.35, _y, _name, fontsize=10.5, color=ACCENT, ha="left",
             va="center")
    ax2.text(6.2, _y, "$u$ is the inside", fontsize=10.5, color=WARM,
             ha="left", va="center")

ax2.plot([-0.1, 10.5], [2.15, 2.15], color=GREY, linewidth=0.9)
ax2.text(-0.1, 1.35, "the inside is whatever $u$ stands for",
         fontsize=10.5, color=INK)
ax2.text(-0.1, 0.55, "if the inside is just $x$, its derivative is $1$ and "
         "nothing changes", fontsize=9.5, color=GREY)

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-5-6a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
