"""SL 4.2 の図を作る。ラベルはすべて英語（日本語フォントに依存しないため）。
   出力先: ai-sl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_4_2.py
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


def finish(fig, ax, name):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), format="svg", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


LO = [0, 10, 20, 30, 40, 50]
FREQ = [6, 14, 24, 20, 12, 4]
CUM = [6, 20, 44, 64, 76, 80]

# ---------- 1. histogram ----------
fig, ax = plt.subplots(figsize=(6.2, 3.6))
ax.bar([x + 5 for x in LO], FREQ, width=10, color=BAR, edgecolor=INK, linewidth=1.1)
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Frequency")
ax.set_xticks(range(0, 70, 10))
ax.set_yticks(range(0, 30, 5))
ax.set_ylim(0, 27)
ax.yaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
finish(fig, ax, "sl-4-2-histogram.svg")

# ---------- 2. cumulative frequency graph ----------
def monotone_cubic(xs, ys, n=400):
    """単調を保つ 3 次補間（Fritsch-Carlson）。累積度数は減らないので、
       曲線が途中で下がったり行きすぎたりしないこの方式を使う。"""
    xs, ys = list(map(float, xs)), list(map(float, ys))
    k = len(xs)
    h = [xs[i + 1] - xs[i] for i in range(k - 1)]
    d = [(ys[i + 1] - ys[i]) / h[i] for i in range(k - 1)]
    m = [d[0]] + [0.0] * (k - 2) + [d[-1]]
    for i in range(1, k - 1):
        if d[i - 1] * d[i] <= 0:
            m[i] = 0.0
        else:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    out_x, out_y = [], []
    for i in range(k - 1):
        for j in range(n // (k - 1) + 1):
            t = j / (n // (k - 1))
            x = xs[i] + t * h[i]
            t2, t3 = t * t, t * t * t
            y = ((2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * h[i] * m[i]
                 + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * h[i] * m[i + 1])
            out_x.append(x)
            out_y.append(y)
    return out_x, out_y


fig, ax = plt.subplots(figsize=(6.4, 4.4))
xs = [0] + [x + 10 for x in LO]
ys = [0] + CUM
cx, cy = monotone_cubic(xs, ys)
ax.plot(cx, cy, "-", color="#0b5fff", linewidth=1.8, zorder=3)
ax.plot(xs, ys, "o", color="#0b5fff", markersize=5, zorder=4)

for target, label, x, dx in ((20, "$Q_1$", 20.0, 1.2), (40, "median", 28.3, 1.2),
                             (60, "$Q_3$", 37.6, 1.2)):
    ax.plot([0, x], [target, target], "--", color=ACC, linewidth=1.1, zorder=2)
    ax.plot([x, x], [0, target], "--", color=ACC, linewidth=1.1, zorder=2)
    ax.annotate(label, (x + dx, target - 4.5), color=ACC, fontsize=10,
                ha="left", va="top")

ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Cumulative frequency")
ax.set_xticks(range(0, 70, 10))
ax.set_yticks(range(0, 90, 10))
ax.set_xlim(0, 62)
ax.set_ylim(0, 84)
ax.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
finish(fig, ax, "sl-4-2-cumfreq.svg")

# ---------- 3. box plot with an outlier ----------
fig, ax = plt.subplots(figsize=(6.2, 2.5))
mn, q1, md, q3, mx, out = 22, 27, 32, 38, 40, 62
y = 0
ax.add_patch(plt.Rectangle((q1, y - 0.22), q3 - q1, 0.44,
                           facecolor=BAR, edgecolor=INK, linewidth=1.2))
ax.plot([md, md], [y - 0.22, y + 0.22], color=INK, linewidth=2.2)
for a, b in ((mn, q1), (q3, mx)):
    ax.plot([a, b], [y, y], color=INK, linewidth=1.2)
for v in (mn, mx):
    ax.plot([v, v], [y - 0.13, y + 0.13], color=INK, linewidth=1.2)
ax.plot([out], [y], marker="x", color=ACC, markersize=10, markeredgewidth=2.2)
ax.annotate("outlier", (out, y + 0.2), color=ACC, ha="center", va="bottom", fontsize=10)

for v, lab in ((mn, "22"), (q1, "27"), (md, "32"), (q3, "38"), (mx, "40"), (out, "62")):
    ax.annotate(lab, (v, y - 0.32), ha="center", va="top", fontsize=9.5,
                color=ACC if v == out else INK)

ax.set_xlim(18, 66)
ax.set_ylim(-0.62, 0.55)
ax.set_yticks([])
ax.set_xlabel("Number of items sold")
ax.spines["left"].set_visible(False)
ax.xaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
finish(fig, ax, "sl-4-2-boxplot.svg")

# ---------- 4. two box plots to compare ----------
fig, ax = plt.subplots(figsize=(6.2, 3.0))
data = [("Class A", 30, 45, 55, 65, 80, 1.0), ("Class B", 40, 50, 70, 78, 85, 0.0)]
for name, mn, q1, md, q3, mx, y in data:
    ax.add_patch(plt.Rectangle((q1, y - 0.2), q3 - q1, 0.4,
                               facecolor=BAR, edgecolor=INK, linewidth=1.2))
    ax.plot([md, md], [y - 0.2, y + 0.2], color=INK, linewidth=2.2)
    for a, b in ((mn, q1), (q3, mx)):
        ax.plot([a, b], [y, y], color=INK, linewidth=1.2)
    for v in (mn, mx):
        ax.plot([v, v], [y - 0.12, y + 0.12], color=INK, linewidth=1.2)

ax.set_yticks([0.0, 1.0])
ax.set_yticklabels(["Class B", "Class A"])
ax.set_xlim(25, 92)
ax.set_ylim(-0.55, 1.55)
ax.set_xlabel("Test score")
ax.set_xticks(range(30, 100, 10))
ax.spines["left"].set_visible(False)
ax.xaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
finish(fig, ax, "sl-4-2-compare.svg")
