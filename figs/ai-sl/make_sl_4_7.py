"""SL 4.7 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_4_7.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, BAR, ACC = "#1f2328", "#dfe3e8", "#9dc3ea", "#c0392b"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})

# ---------- E(X) は「つりあいの位置」 ----------
X = [1, 2, 3, 4]
P = [0.2, 0.3, 0.4, 0.1]
EX = sum(x * p for x, p in zip(X, P))          # = 2.4

fig, ax = plt.subplots(figsize=(6.4, 3.8))

ax.bar(X, P, width=0.45, color=BAR, edgecolor=INK, linewidth=1.2, zorder=3)
for x, p in zip(X, P):
    ax.annotate(f"{p}", (x, p + 0.012), ha="center", va="bottom", fontsize=10)

# つりあいの位置（支点）
ax.plot([EX, EX], [0, 0.50], "--", color=ACC, linewidth=1.4, zorder=2)
ax.plot([EX], [-0.024], marker="^", color=ACC, markersize=14,
        clip_on=False, zorder=5)
ax.annotate(f"$\\mathrm{{E}}(X) = {EX}$   (balance point)", (EX, 0.535),
            color=ACC, ha="center", va="bottom", fontsize=12,
            annotation_clip=False)

ax.set_xlabel("$x$")
ax.set_ylabel("$\\mathrm{P}(X = x)$")
ax.set_xticks(X)
ax.set_xlim(0.4, 4.8)
ax.set_ylim(0, 0.52)
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.yaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-7-balance.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-7-balance.svg   E(X) =", EX)
