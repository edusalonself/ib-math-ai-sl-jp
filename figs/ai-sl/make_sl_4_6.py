"""SL 4.6 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_4_6.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, ACC, FILL, CIRC = "#1f2328", "#c0392b", "#e8f1fb", "#3b82c4"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})


def frame(ax):
    ax.add_patch(plt.Rectangle((0.02, 0.05), 0.96, 0.86,
                               facecolor=FILL, edgecolor=INK, linewidth=1.3))
    ax.annotate("$U$", (0.06, 0.86), fontsize=12, ha="left", va="top")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")


# ---------- 1. 重なるベン図 と 排反 ----------
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4))

# 左：重なる
ax = axes[0]
frame(ax)
ax.add_patch(plt.Circle((0.38, 0.48), 0.24, facecolor="none",
                        edgecolor=CIRC, linewidth=1.8))
ax.add_patch(plt.Circle((0.62, 0.48), 0.24, facecolor="none",
                        edgecolor=CIRC, linewidth=1.8))
ax.annotate("$A$", (0.22, 0.72), fontsize=13)
ax.annotate("$B$", (0.74, 0.72), fontsize=13)
ax.annotate("only $A$", (0.28, 0.48), fontsize=9.5, ha="center", va="center")
ax.annotate("only $B$", (0.72, 0.48), fontsize=9.5, ha="center", va="center")
ax.annotate("$A \\cap B$", (0.50, 0.48), fontsize=10, ha="center", va="center",
            color=ACC)
ax.annotate("neither", (0.5, 0.13), fontsize=9.5, ha="center", va="center",
            color="#5b6472")
ax.set_title("Overlapping:  $\\mathrm{P}(A \\cap B) \\neq 0$",
             fontsize=11, pad=10)

# 右：排反
ax = axes[1]
frame(ax)
ax.add_patch(plt.Circle((0.27, 0.48), 0.18, facecolor="white",
                        edgecolor=CIRC, linewidth=1.8))
ax.add_patch(plt.Circle((0.73, 0.48), 0.18, facecolor="white",
                        edgecolor=CIRC, linewidth=1.8))
ax.annotate("$A$", (0.27, 0.48), fontsize=13, ha="center", va="center")
ax.annotate("$B$", (0.73, 0.48), fontsize=13, ha="center", va="center")
ax.annotate("no overlap", (0.5, 0.13), fontsize=9.5, ha="center", va="center",
            color=ACC)
ax.set_title("Mutually exclusive:  $\\mathrm{P}(A \\cap B) = 0$",
             fontsize=11, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-6-venn.svg"), format="svg", bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-6-venn.svg")

# ---------- 2. 樹形図（戻さない場合） ----------
fig, ax = plt.subplots(figsize=(6.6, 4.2))

X0, X1, X2 = 0.06, 0.42, 0.80
NODES = {"start": (X0, 0.50), "R": (X1, 0.74), "B": (X1, 0.26),
         "RR": (X2, 0.88), "RB": (X2, 0.62), "BR": (X2, 0.36), "BB": (X2, 0.10)}

BRANCH = [
    ("start", "R", r"$\frac{5}{8}$"),
    ("start", "B", r"$\frac{3}{8}$"),
    ("R", "RR", r"$\frac{4}{7}$"),
    ("R", "RB", r"$\frac{3}{7}$"),
    ("B", "BR", r"$\frac{5}{7}$"),
    ("B", "BB", r"$\frac{2}{7}$"),
]
for a, b, lab in BRANCH:
    (xa, ya), (xb, yb) = NODES[a], NODES[b]
    ax.plot([xa, xb], [ya, yb], "-", color=INK, linewidth=1.3, zorder=2)
    ax.annotate(lab, ((xa + xb) / 2, (ya + yb) / 2 + 0.035),
                fontsize=11, ha="center", va="bottom", color=ACC)

for key, lab in (("R", "R"), ("B", "B")):
    x, y = NODES[key]
    ax.plot(x, y, "o", color="white", markersize=20,
            markeredgecolor=INK, markeredgewidth=1.2, zorder=3)
    ax.annotate(lab, (x, y), fontsize=11, ha="center", va="center", zorder=4)

OUTC = [("RR", r"RR:  $\frac{5}{8}\times\frac{4}{7}=\frac{20}{56}$"),
        ("RB", r"RB:  $\frac{5}{8}\times\frac{3}{7}=\frac{15}{56}$"),
        ("BR", r"BR:  $\frac{3}{8}\times\frac{5}{7}=\frac{15}{56}$"),
        ("BB", r"BB:  $\frac{3}{8}\times\frac{2}{7}=\frac{6}{56}$")]
for key, lab in OUTC:
    x, y = NODES[key]
    ax.annotate(lab, (x + 0.02, y), fontsize=10.5, ha="left", va="center")

ax.annotate("1st counter", (X1, 0.99), fontsize=10, ha="center",
            va="top", color="#5b6472", style="italic")
ax.annotate("2nd counter", (X2, 0.99), fontsize=10, ha="center",
            va="top", color="#5b6472", style="italic")

ax.set_xlim(0, 1.30)
ax.set_ylim(0, 1.02)
ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-6-tree.svg"), format="svg", bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-6-tree.svg")

# ---------- 3. 具体的な人数を入れたベン図（football / tennis） ----------
fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.add_patch(plt.Rectangle((0.03, 0.06), 0.94, 0.88,
                           facecolor=FILL, edgecolor=INK, linewidth=1.3))
ax.annotate("$U$", (0.07, 0.90), fontsize=13, ha="left", va="top")
ax.annotate("$n(U) = 30$", (0.07, 0.12), fontsize=10.5, ha="left", va="center",
            color="#5b6472")

for cx in (0.38, 0.62):          # 先に白で塗る
    ax.add_patch(plt.Circle((cx, 0.54), 0.23, facecolor="white",
                            edgecolor="none", zorder=2))
for cx in (0.38, 0.62):          # そのあとに輪郭を引く
    ax.add_patch(plt.Circle((cx, 0.54), 0.23, facecolor="none",
                            edgecolor=CIRC, linewidth=1.9, zorder=3))

ax.annotate("$F$  (football)", (0.25, 0.83), fontsize=11.5, ha="center", zorder=5)
ax.annotate("$T$  (tennis)", (0.75, 0.83), fontsize=11.5, ha="center", zorder=5)

for x, num, sub, col in [(0.28, "$10$", "football only", INK),
                         (0.50, "$8$", "both", ACC),
                         (0.72, "$6$", "tennis only", INK)]:
    ax.annotate(num, (x, 0.57), fontsize=16, ha="center", va="center",
                color=col, zorder=5)
    ax.annotate(sub, (x, 0.47), fontsize=8.5, ha="center", va="center",
                color=ACC if col == ACC else "#5b6472", zorder=5)

ax.annotate("$6$", (0.88, 0.20), fontsize=16, ha="center", va="center", zorder=5)
ax.annotate("neither", (0.88, 0.13), fontsize=8.5, ha="center", va="center",
            color="#5b6472", zorder=5)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-6-venn-counts.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-6-venn-counts.svg   check 10+8+6+6 =", 10 + 8 + 6 + 6,
      "  n(F) =", 10 + 8, "  n(T) =", 8 + 6)
