"""SL 4.5 の図を作る。ラベルはすべて英語。
   出力先: 04-statistics-and-probability/img/*.svg
   再生成: python3 figs/make_sl_4_5.py
   ★ 乱数は seed を固定しているので、何度実行しても同じ図になります。
"""
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, FILL = "#1f2328", "#dfe3e8", "#3b82c4", "#c0392b", "#dbeafe"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})

# ---------- 1. 相対度数が理論値に近づく ----------
random.seed(20260826)
N = 500
heads = 0
xs, ys = [], []
for i in range(1, N + 1):
    heads += random.random() < 0.5
    xs.append(i)
    ys.append(heads / i)

fig, ax = plt.subplots(figsize=(6.6, 3.6))
ax.axhline(0.5, color=ACC, linewidth=1.4, linestyle="--", zorder=2)
ax.annotate("theoretical probability = 0.5", (N * 0.98, 0.515), color=ACC,
            ha="right", va="bottom", fontsize=10)
ax.plot(xs, ys, "-", color=LINE, linewidth=1.4, zorder=3)

ax.set_xlabel("Number of tosses")
ax.set_ylabel("Relative frequency\nof heads")
ax.set_xlim(0, N)
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(True, color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-5-relfreq.svg"), format="svg", bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-5-relfreq.svg  (最後の値 =", round(ys[-1], 4), ")")

# ---------- 2. 余事象 ----------
fig, ax = plt.subplots(figsize=(5.0, 3.0))

# 標本空間 U
ax.add_patch(plt.Rectangle((0.05, 0.08), 0.90, 0.84,
                           facecolor=FILL, edgecolor=INK, linewidth=1.4))
ax.annotate("$U$", (0.09, 0.85), fontsize=13, ha="left", va="top")

# 事象 A
ax.add_patch(plt.Circle((0.32, 0.5), 0.21,
                        facecolor="white", edgecolor=INK, linewidth=1.4))
ax.annotate("$A$", (0.32, 0.5), fontsize=14, ha="center", va="center")

ax.annotate("$A'$", (0.72, 0.56), fontsize=14, ha="center", va="center",
            color="#14507f")
ax.annotate("(not $A$)", (0.72, 0.42), fontsize=11, ha="center", va="center",
            color="#14507f")
ax.annotate(r"$\mathrm{P}(A) + \mathrm{P}(A') = 1$", (0.5, -0.02),
            fontsize=12, ha="center", va="top", color=ACC)

ax.set_xlim(0, 1)
ax.set_ylim(-0.18, 1)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-5-complement.svg"), format="svg", bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-5-complement.svg")
