"""SL 4.4 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_4_4.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, DOT, ACC, MUTE = "#1f2328", "#dfe3e8", "#3b82c4", "#c0392b", "#8b93a0"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})

# ---------- 1. 相関の4つの型 ----------
XS = [1, 2, 3, 4, 5, 6, 7, 8]
PANELS = [
    ("Strong positive", "$r = 0.95$", XS, [7, 22, 27, 32, 40, 37, 50, 47]),
    ("Weak positive", "$r = 0.61$", XS, [28, 21, 38, 31, 48, 52, 32, 43]),
    ("Strong negative", "$r = -0.95$", XS, [47, 34, 29, 32, 22, 22, 17, 4]),
    ("Little or no linear correlation", "$r = 0.00$", XS,
     [23, 46, 33, 42, 16, 28, 15, 51]),
]

fig, axes = plt.subplots(2, 2, figsize=(6.8, 5.0))
for ax, (title, rlab, xs, ys) in zip(axes.ravel(), PANELS):
    ax.plot(xs, ys, "o", color=DOT, markersize=6,
            markeredgecolor="white", markeredgewidth=0.8)
    ax.set_title(f"{title}   {rlab}", fontsize=10.5, pad=6)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 56)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-4-types.svg"), format="svg", bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-4-types.svg")

# ---------- 2. 回帰直線・平均点・外挿 ----------
X = [1, 2, 3, 4, 5, 6, 7, 8]
Y = [34, 38, 50, 48, 62, 58, 78, 72]
A, B = 6, 28          # y = 6x + 28
MX, MY = 4.5, 55      # 平均点

fig, ax = plt.subplots(figsize=(6.8, 4.4))

# データの外側（外挿の領域）
ax.axvspan(8, 15, color="#f4f6f8", zorder=0)
ax.annotate("beyond the data\n(extrapolation)", (11.5, 12), color=MUTE,
            ha="center", va="bottom", fontsize=9.5)

# 100点の上限
ax.axhline(100, color=ACC, linewidth=1.1, linestyle=":", zorder=1)
ax.annotate("maximum possible score = 100", (0.3, 101.5), color=ACC,
            ha="left", va="bottom", fontsize=9.5)

# 回帰直線：データの範囲は実線、その外は破線
ax.plot([0, 8], [B, A * 8 + B], "-", color=INK, linewidth=1.6, zorder=3)
ax.plot([8, 15], [A * 8 + B, A * 15 + B], "--", color=MUTE, linewidth=1.4, zorder=3)

ax.plot(X, Y, "o", color=DOT, markersize=7,
        markeredgecolor="white", markeredgewidth=0.9, zorder=4)

# 平均点
ax.plot(MX, MY, "D", color=ACC, markersize=9,
        markeredgecolor="white", markeredgewidth=1.0, zorder=5)
ax.annotate(r"mean point $(\bar{x},\ \bar{y}) = (4.5,\ 55)$", (MX + 0.4, MY - 12),
            color=ACC, ha="left", va="center", fontsize=10)

ax.annotate(r"$y = 6x + 28$", (7.6, A * 7.6 + B + 5), color=INK,
            ha="right", va="bottom", fontsize=11)

ax.set_xlabel("Hours studied, $x$")
ax.set_ylabel("Test score, $y$")
ax.set_xlim(0, 15)
ax.set_ylim(0, 135)
ax.set_xticks(range(0, 16, 2))
ax.set_yticks(range(0, 140, 20))
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(True, color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-4-regression.svg"), format="svg", bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-4-regression.svg")

# ---------- 3. r は直線の関係しか測れない ----------
CX = [1, 2, 3, 4, 5, 6, 7, 8]
CY = [12, 18, 24, 48, 48, 24, 18, 12]

fig, ax = plt.subplots(figsize=(5.2, 3.4))
ax.plot(CX, CY, "o", color=DOT, markersize=8,
        markeredgecolor="white", markeredgewidth=0.9)
ax.set_title(r"$r = 0.00$,  but $x$ and $y$ are clearly related",
             fontsize=10.5, pad=8, color=ACC)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_xlim(0, 9)
ax.set_ylim(0, 56)
ax.set_xticks(range(1, 9))
ax.set_yticks([])
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(True, color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-4-nonlinear.svg"), format="svg", bbox_inches="tight")
plt.close(fig)
print("wrote sl-4-4-nonlinear.svg")
