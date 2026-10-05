"""AA HL 1.10a（counting principles）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_10a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_10a.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-10a-idea-a.svg
      aa-hl/01-number-and-algebra/img/aahl-1-10a-idea-b.svg

(a) かけ算の原理。4 枚の shirt と 3 本の trousers の組み合わせが
    4 x 3 = 12 通りであることを、格子で見せる。
(b) 選んでから並べる。8C3 の 1 つの選び方が、3! 通りに並ぶ。
    だから 8P3 = 8C3 x 3!。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

fig1, ax1 = plt.subplots(figsize=(5.5, 4.0))
fig2, ax2 = plt.subplots(figsize=(6.2, 2.9))

# ══════════════════════════════════════════════════════════
# (a) かけ算の原理：4 x 3 の格子
# ══════════════════════════════════════════════════════════
ax1.set_title("One shirt and one pair of trousers", fontsize=11,
              color=INK, loc="left", pad=10)
ax1.set_xlim(-1.35, 3.35)
ax1.set_ylim(-1.30, 4.15)
ax1.axis("off")

N_SHIRT, N_TROUSER = 4, 3

for _i in range(N_SHIRT):
    ax1.text(-0.45, _i, "shirt %d" % (_i + 1), ha="right", va="center",
             fontsize=9.5, color=ACCENT)
for _j in range(N_TROUSER):
    ax1.text(_j, 3.60, "trousers %d" % (_j + 1), ha="center", va="bottom",
             fontsize=9.5, color=WARM, rotation=0)

for _i in range(N_SHIRT):
    for _j in range(N_TROUSER):
        ax1.plot([_j], [_i], marker="o", markersize=9,
                 color=GREY, zorder=3)
for _i in range(N_SHIRT):
    ax1.plot([-0.05, N_TROUSER - 0.95], [_i, _i], color="#e9eef4",
             linewidth=2.0, zorder=1)
for _j in range(N_TROUSER):
    ax1.plot([_j, _j], [-0.05, N_SHIRT - 0.95], color="#f6ede1",
             linewidth=2.0, zorder=1)

ax1.text(1.0, -0.72, "$4 \\times 3 = 12$ outfits", ha="center",
         va="center", fontsize=12, color=INK)
ax1.text(1.0, -1.18, "one dot for each outfit", ha="center",
         va="center", fontsize=10, color=GREY)

# ══════════════════════════════════════════════════════════
# (b) 選んでから並べる
# ══════════════════════════════════════════════════════════
ax2.set_title("Choosing 3 people out of 8, then putting them in order",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.0)
ax2.axis("off")

ax2.text(0.135, 0.74, "$\\{A,\\ B,\\ C\\}$", ha="center", va="center",
         fontsize=13, color=ACCENT)
ax2.text(0.135, 0.55, "one selection", ha="center", va="center",
         fontsize=9.5, color=GREY)
ax2.text(0.135, 0.26, "$^{8}\\mathrm{C}_{3} = 56$", ha="center",
         va="center", fontsize=12, color=ACCENT)
ax2.text(0.135, 0.10, "selections", ha="center", va="center",
         fontsize=9.5, color=GREY)

ax2.annotate("", xy=(0.40, 0.74), xytext=(0.255, 0.74),
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.3))
ax2.text(0.328, 0.845, "$\\times\\ 3! = 6$", ha="center", va="center",
         fontsize=11, color=INK)

ORDERS = ["$ABC$", "$ACB$", "$BAC$", "$BCA$", "$CAB$", "$CBA$"]
for _k, _s in enumerate(ORDERS):
    _cx = 0.46 + 0.09 * _k
    ax2.text(_cx, 0.74, _s, ha="center", va="center", fontsize=11,
             color=WARM)
ax2.text(0.70, 0.55, "the $3!$ orders of that one selection",
         ha="center", va="center", fontsize=9.5, color=GREY)
ax2.text(0.70, 0.26, "$^{8}\\mathrm{P}_{3} = 336$", ha="center",
         va="center", fontsize=12, color=WARM)
ax2.text(0.70, 0.10, "arrangements", ha="center", va="center",
         fontsize=9.5, color=GREY)

for _fig, _name in ((fig1, "aahl-1-10a-idea-a.svg"),
                    (fig2, "aahl-1-10a-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
