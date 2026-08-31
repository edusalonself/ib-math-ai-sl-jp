"""SL 4.9 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_4_9.py
"""
import os
from math import exp, pi, sqrt, erf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, ACC = "#1f2328", "#dfe3e8", "#c0392b"
FILL, FILL2, FILL3 = "#f0b27a", "#a9cce3", "#a3d9a5"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})


def pdf(x, mu=0.0, s=1.0):
    return np.exp(-((x - mu) ** 2) / (2 * s * s)) / (s * sqrt(2 * pi))


def cdf(x, mu=0.0, s=1.0):
    return 0.5 * (1 + erf((x - mu) / (s * sqrt(2))))


def curve(ax, mu=0.0, s=1.0, lo=-4.0, hi=4.0):
    x = np.linspace(mu + lo * s, mu + hi * s, 800)
    ax.plot(x, pdf(x, mu, s), color=INK, linewidth=1.8, zorder=5)
    return x


def bare(ax):
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.set_yticks([])
    ax.set_ylim(0, pdf(0.0) * 1.30)


# ---------- 0. いちばんシンプルな正規分布の曲線 ----------
fig, ax = plt.subplots(figsize=(7.6, 3.9))
x = curve(ax)
ax.fill_between(x, pdf(x), color="#eaf2fb", zorder=2)
ax.axvline(0, color=ACC, linestyle="--", linewidth=1.4, zorder=6)
ax.annotate("the peak is at the mean", xy=(0, pdf(0.0) * 1.015),
            xytext=(1.55, pdf(0.0) * 1.20), ha="center", va="center",
            color=ACC, fontsize=11.5, zorder=8,
            arrowprops=dict(arrowstyle="->", color=ACC, linewidth=1.3),
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"))
ax.annotate("the curve is symmetrical about $\\mu$", (0, pdf(0.0) * 0.42),
            ha="center", va="center", color=INK, fontsize=11.5, zorder=8,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"))
ax.annotate("total area $= 1$", (0, pdf(0.0) * 0.14), ha="center", va="center",
            color="#1a5276", fontsize=12, zorder=8,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"))
ax.set_xticks([0])
ax.set_xticklabels([r"$\mu$"], fontsize=13)
bare(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-9-curve.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 1. 68 / 95 / 99.7 ----------
fig, ax = plt.subplots(figsize=(8.2, 4.2))
curve(ax)
for k, col in [(3, "#d6eadf"), (2, "#a9cce3"), (1, "#f0b27a")]:
    xs = np.linspace(-k, k, 500)
    ax.fill_between(xs, pdf(xs), color=col, zorder=4 - k + 1)
ax.axvline(0, color=ACC, linestyle="--", linewidth=1.3, zorder=6)
for k, col, h, lab in [(1, "#8a4b12", 0.86, "$68\\%$"),
                       (2, "#1a5276", 1.00, "$95\\%$"),
                       (3, "#1e6b3a", 1.14, "$99.7\\%$")]:
    y = pdf(0.0) * h
    ax.annotate("", xy=(-k, y), xytext=(k, y),
                arrowprops=dict(arrowstyle="<->", color=col, linewidth=1.3), zorder=7)
    ax.annotate(lab, (0, y), ha="center", va="center", color=col, fontsize=12, zorder=8,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none"))
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
ax.set_xticklabels([r"$\mu-3\sigma$", r"$\mu-2\sigma$", r"$\mu-\sigma$", r"$\mu$",
                    r"$\mu+\sigma$", r"$\mu+2\sigma$", r"$\mu+3\sigma$"], fontsize=10)
bare(ax)
ax.set_ylim(0, pdf(0.0) * 1.30)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-9-empirical.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 2. 3種類の面積 ----------
fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.3), sharey=True)
specs = [("$\\mathrm{P}(X < a)$", -4.0, -0.7, [(-0.7, "$a$")], FILL),
         ("$\\mathrm{P}(X > a)$", 0.6, 4.0, [(0.6, "$a$")], FILL2),
         ("$\\mathrm{P}(a < X < b)$", -1.1, 1.4, [(-1.1, "$a$"), (1.4, "$b$")], FILL3)]
for ax, (title, lo, hi, marks, col) in zip(axes, specs):
    curve(ax)
    xs = np.linspace(lo, hi, 500)
    ax.fill_between(xs, pdf(xs), color=col, zorder=3)
    for v, lab in marks:
        ax.plot([v, v], [0, pdf(v)], color=INK, linewidth=1.2, zorder=6)
    ax.set_xticks([m[0] for m in marks])
    ax.set_xticklabels([m[1] for m in marks], fontsize=12)
    ax.set_title(title, fontsize=12.5, pad=9)
    bare(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-9-areas.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 3. inverse normal ----------
K = 1.2815515655446004          # invNorm(0.90)
fig, ax = plt.subplots(figsize=(7.6, 3.8))
curve(ax)
xs = np.linspace(-4, K, 600)
ax.fill_between(xs, pdf(xs), color=FILL, zorder=3)
ax.plot([K, K], [0, pdf(K)], color=INK, linewidth=1.4, zorder=6)
ax.annotate("area $= 0.90$   (given)", (-0.2, 0.06), ha="center",
            color="#8a4b12", fontsize=12.5, zorder=7)
ax.annotate("$k = ?$", (K, -0.030), ha="center", va="top", color=ACC,
            fontsize=13, zorder=7, annotation_clip=False)
ax.annotate("", xy=(K, -0.012), xytext=(K, 0.055),
            arrowprops=dict(arrowstyle="->", color=ACC, linewidth=1.6),
            zorder=7, annotation_clip=False)
ax.set_xticks([0])
ax.set_xticklabels([r"$\mu$"], fontsize=12)
bare(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-9-inverse.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

print("wrote sl-4-9-curve.svg, sl-4-9-empirical.svg, sl-4-9-areas.svg, sl-4-9-inverse.svg")
print("check 68/95/99.7 :",
      f"{(cdf(1)-cdf(-1))*100:.2f} {(cdf(2)-cdf(-2))*100:.2f} {(cdf(3)-cdf(-3))*100:.2f}")
print("check invNorm(0.90) =", K, " cdf =", cdf(K))
