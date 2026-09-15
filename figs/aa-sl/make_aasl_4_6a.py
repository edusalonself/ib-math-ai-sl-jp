"""AA SL 4.6a の図をつくる。

    python3 figs/aa-sl/make_aasl_4_6a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_6a.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-6a-idea.svg

(a) Venn diagram —— 重なりを 2 回数えてしまうこと。
(b) tree diagram —— 枝に沿ってかけ、枝先を足すこと。

★ 数値は例題・演習と重ならないように選んであります。
   (a) は 50 人（例題1 は 30 人、演習1 は 40 人、演習8 は 60 人）。
   (b) は 1/3（例題4 は 3/5、演習5 は 0.3、演習9 は 0.4）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#dbe8f5"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.7))

# ══════════════════════════════════════════════════════════
# (a) Venn diagram
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) A Venn diagram splits $U$ into four parts", fontsize=11,
              color=INK, loc="left", pad=10)
ax1.set_xlim(-0.6, 6.6)
ax1.set_ylim(-2.55, 4.7)
ax1.set_aspect("equal", adjustable="datalim")
ax1.axis("off")

ax1.add_patch(plt.Rectangle((-0.35, -0.35), 6.7, 4.3, facecolor="white",
                            edgecolor=GREY, linewidth=1.1))
ax1.text(6.15, 3.62, "$U$", fontsize=11, color=GREY, ha="right", va="top")

ax1.add_patch(plt.Circle((2.35, 1.85), 1.65, facecolor=FILL, alpha=0.55,
                         edgecolor=ACCENT, linewidth=1.4))
ax1.add_patch(plt.Circle((3.85, 1.85), 1.65, facecolor=FILL, alpha=0.55,
                         edgecolor=ACCENT, linewidth=1.4))
ax1.text(1.15, 3.30, "$A$", fontsize=12, color=ACCENT)
ax1.text(4.90, 3.30, "$B$", fontsize=12, color=ACCENT)

ax1.text(1.62, 1.75, "$15$", fontsize=12, color=INK, ha="center")
ax1.text(3.10, 1.75, "$10$", fontsize=12, color=WARM, ha="center")
ax1.text(4.58, 1.75, "$12$", fontsize=12, color=INK, ha="center")
ax1.text(0.30, 0.10, "$13$", fontsize=12, color=INK)

ax1.annotate("", xy=(3.10, 1.45), xytext=(3.10, -0.72),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.2))
ax1.text(3.30, -0.80, "this part is in $A$ and in $B$", fontsize=9.5,
         color=WARM)

ax1.text(-0.55, -1.70, "$n(A) = 15 + 10 = 25$ and $n(B) = 10 + 12 = 22$",
         fontsize=9.5, color=INK)
ax1.text(-0.55, -2.20, "$25 + 22 = 47$, but only $37$ people are in $A$ or $B$: "
         "the $10$ was counted twice", fontsize=9.5, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) tree diagram
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) A tree diagram: multiply along, add at the ends",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-0.45, 6.9)
ax2.set_ylim(-2.55, 4.7)
ax2.axis("off")

ROOT = (0.15, 1.8)
L1 = {"A": (2.15, 3.05), "N": (2.15, 0.55)}
L2 = {("A", "A"): (4.30, 3.75), ("A", "N"): (4.30, 2.45),
      ("N", "A"): (4.30, 1.25), ("N", "N"): (4.30, -0.05)}

for _k, _pt in L1.items():
    ax2.plot([ROOT[0], _pt[0]], [ROOT[1], _pt[1]], color=ACCENT, linewidth=1.3)
for (_a, _b), _pt in L2.items():
    ax2.plot([L1[_a][0], _pt[0]], [L1[_a][1], _pt[1]], color=ACCENT,
             linewidth=1.3)

ax2.plot(*ROOT, "o", color=ACCENT, markersize=4)
ax2.text(0.15, 1.42, "start", fontsize=9.5, color=GREY, ha="center")

_BOX = dict(facecolor="white", edgecolor="none", pad=1.4)
for _k in ("A", "N"):
    ax2.plot(*L1[_k], "o", color=ACCENT, markersize=4)
ax2.text(L1["A"][0], L1["A"][1], "$W$", fontsize=11, color=INK,
         ha="center", va="center", bbox=_BOX)
ax2.text(L1["N"][0], L1["N"][1], "$W'$", fontsize=11, color=INK,
         ha="center", va="center", bbox=_BOX)
ax2.text(1.02, 2.62, r"$\frac{1}{3}$", fontsize=10, color=WARM, ha="center")
ax2.text(1.02, 1.00, r"$\frac{2}{3}$", fontsize=10, color=WARM, ha="center")

_lab = {("A", "A"): (r"$\frac{1}{3}$", r"$W$", r"$\frac{1}{3}\times\frac{1}{3}=\frac{1}{9}$"),
        ("A", "N"): (r"$\frac{2}{3}$", r"$W'$", r"$\frac{1}{3}\times\frac{2}{3}=\frac{2}{9}$"),
        ("N", "A"): (r"$\frac{1}{3}$", r"$W$", r"$\frac{2}{3}\times\frac{1}{3}=\frac{2}{9}$"),
        ("N", "N"): (r"$\frac{2}{3}$", r"$W'$", r"$\frac{2}{3}\times\frac{2}{3}=\frac{4}{9}$")}
for _key, _pt in L2.items():
    _p, _name, _prod = _lab[_key]
    _mx = (L1[_key[0]][0] + _pt[0]) / 2
    _my = (L1[_key[0]][1] + _pt[1]) / 2
    ax2.text(_mx, _my + 0.16, _p, fontsize=9.5, color=WARM, ha="center")
    ax2.text(_pt[0] + 0.12, _pt[1], _name, fontsize=10.5, color=INK,
             va="center")
    ax2.text(_pt[0] + 0.80, _pt[1], _prod, fontsize=9.5, color=ACCENT,
             va="center")

ax2.text(-0.45, -0.92, "the first result does not change the probabilities\n"
         "for the second, so both stages use the same numbers",
         fontsize=9.5, color=GREY, linespacing=1.5)
ax2.text(-0.45, -1.82, "the four ends add to $1$:  "
         r"$\frac{1}{9}+\frac{2}{9}+\frac{2}{9}+\frac{4}{9}=1$",
         fontsize=9.5, color=INK)
ax2.text(-0.45, -2.30, "for the event \"at least one $W$\", add the three "
         "ends that contain a $W$", fontsize=9.5, color=WARM)

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-4-6a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  venn: 15 + 10 + 12 + 13 =", 15 + 10 + 12 + 13,
      "  tree ends:", 1 / 9 + 2 / 9 + 2 / 9 + 4 / 9)

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
