"""AA HL 1.15（帰納法・背理法・反例）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_15.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_15.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-15-idea-a.svg
      aa-hl/01-number-and-algebra/img/aahl-1-15-idea-b.svg

(a) 帰納法：はしご。1 段目に乗れること（base case）と、
    どの段からでも次の段へ行けること（inductive step）。
(b) 背理法：逆を仮定して、正しく進み、あり得ないところに着く。

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
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

fig1, ax1 = plt.subplots(figsize=(5.8, 3.8))
fig2, ax2 = plt.subplots(figsize=(5.8, 4.2))

# ══════════════════════════════════════════════════════════
# (a) 帰納法：はしご
# ══════════════════════════════════════════════════════════
ax1.set_title("Induction: reach the first rung, then always the next one",
              fontsize=10.5, color=INK, loc="left", pad=10)
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0.0, 1.0)
ax1.axis("off")

RUNGS = [(0.14, "$n=1$"), (0.30, "$n=2$"), (0.46, "$n=3$"), (0.62, "$n=4$")]
for _x, _lab in RUNGS:
    ax1.plot([_x - 0.05, _x + 0.05], [0.30, 0.30], color=INK, linewidth=3.0,
             solid_capstyle="round", zorder=3)
    ax1.text(_x, 0.21, _lab, ha="center", va="top", fontsize=10, color=INK)
ax1.text(0.80, 0.30, "$\\cdots$", ha="center", va="center", fontsize=14,
         color=GREY)
ax1.plot([0.09, 0.86], [0.30, 0.30], color="#e9eef4", linewidth=2.0, zorder=1)

ax1.annotate("", xy=(0.14, 0.36), xytext=(0.14, 0.58),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.8))
ax1.text(0.14, 0.62, "base case:\nthe statement is\ntrue for $n=1$",
         ha="center", va="bottom", fontsize=9.5, color=ACCENT)

for _i in range(3):
    _a = RUNGS[_i][0] + 0.055
    _b = RUNGS[_i + 1][0] - 0.055
    ax1.annotate("", xy=(_b, 0.40), xytext=(_a, 0.40),
                 arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.5,
                                 connectionstyle="arc3,rad=-0.45"))
ax1.text(0.66, 0.72, "inductive step:\nif it is true for $n=k$,\n"
                     "it is true for $n=k+1$",
         ha="center", va="bottom", fontsize=9.5, color=WARM)
ax1.text(0.50, 0.08, "both parts are needed: neither one alone is enough",
         ha="center", va="center", fontsize=9.5, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 背理法の流れ
# ══════════════════════════════════════════════════════════
ax2.set_title("Proof by contradiction", fontsize=10.5, color=INK,
              loc="left", pad=10)
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.0)
ax2.axis("off")

BOXES = [(0.86, "Assume the statement is FALSE", ACCENT),
         (0.62, "Work forwards, using only\nvalid steps", INK),
         (0.38, "Arrive at something impossible", WARM),
         (0.14, "So the assumption was wrong:\nthe statement is TRUE", ACCENT)]
for _y, _txt, _c in BOXES:
    ax2.add_patch(FancyBboxPatch((0.14, _y - 0.075), 0.72, 0.15,
                                 boxstyle="round,pad=0.012",
                                 linewidth=1.3, edgecolor=_c,
                                 facecolor="none", zorder=2))
    ax2.text(0.50, _y, _txt, ha="center", va="center", fontsize=10, color=_c)
for _i in range(3):
    ax2.annotate("", xy=(0.50, BOXES[_i + 1][0] + 0.080),
                 xytext=(0.50, BOXES[_i][0] - 0.080),
                 arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.4))

for _fig, _name in ((fig1, "aahl-1-15-idea-a.svg"),
                    (fig2, "aahl-1-15-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
