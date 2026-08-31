"""SL 2.6 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/02-functions/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_2_6.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, FILL = "#7a8592", "#e8f1fb"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.82)


# ================= 1. the modelling cycle =================
fig, ax = plt.subplots(figsize=(8.6, 5.4))

CARDS = [
    (0.50, 0.86, "1.  Pose a real-world problem", GREY),
    (0.84, 0.52, "2.  Develop and fit\nthe model", LINE),
    (0.50, 0.16, "3.  Test and reflect\nupon the model", ACC),
    (0.16, 0.52, "4.  Use the model", GREEN),
]
W, H = 0.30, 0.16
for (cx, cy, text, col) in CARDS:
    ax.add_patch(FancyBboxPatch((cx - W / 2, cy - H / 2), W, H,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor="white", edgecolor=col, linewidth=1.8,
                                zorder=4))
    ax.annotate(text, (cx, cy), ha="center", va="center", fontsize=10.5,
                color=col, zorder=6)


def arc(p0, p1, rad, color=INK, style="-|>", lw=1.7, ls="-", z=7):
    """★ zorder は箱(4)より上にする。でないと矢の先が隠れる。"""
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle=style, color=color, linewidth=lw,
                                 linestyle=ls, mutation_scale=16, zorder=z,
                                 shrinkA=0, shrinkB=0))


# ── 外まわりの4本。始点・終点は【箱の外】に置く ──────────────
#    箱の範囲:  1) x 0.35-0.65, y 0.78-0.94    2) x 0.69-0.99, y 0.44-0.60
#               3) x 0.35-0.65, y 0.08-0.24    4) x 0.01-0.31, y 0.44-0.60
arc((0.665, 0.805), (0.795, 0.625), -0.30)   # 1 → 2
arc((0.795, 0.415), (0.665, 0.235), -0.30)   # 2 → 3
arc((0.335, 0.235), (0.205, 0.415), -0.30)   # 3 → 4
arc((0.205, 0.625), (0.335, 0.805), -0.30)   # 4 → 1

# ── reject の戻り。外まわりとぶつからないよう【内側】を通す ──
arc((0.560, 0.250), (0.680, 0.470), -0.45, color=ACC, ls="--", lw=1.5)
# ラベルは【線の上に乗せない】。輪の内側の、何もない場所に置く。
LBL = dict(facecolor="white", edgecolor="none", pad=2.2, alpha=1.0)
ax.annotate("reject:\ngo back and change it", (0.545, 0.415), fontsize=9.5,
            color=ACC, ha="right", va="center", zorder=8, bbox=LBL)

ax.annotate("accept", (0.330, 0.300), fontsize=9.5, color=GREEN,
            ha="left", va="center", zorder=8, bbox=LBL)
ax.annotate("extend the problem", (0.325, 0.715), fontsize=9.5, color=GREY,
            ha="left", va="center", zorder=8, bbox=LBL)

ax.set_xlim(0, 1.02)
ax.set_ylim(0.02, 1.0)
ax.axis("off")
ax.set_title("The modelling process", fontsize=13, pad=6)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-6-cycle.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ================= 2. good fit と bad fit =================
DX = np.array([1, 2, 3, 4, 5, 6])
DY = np.array([6.0, 8.6, 10.0, 9.7, 7.6, 4.0])

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

# bad: linear
ax = axes[0]
ax.scatter(DX, DY, s=60, color=INK, zorder=6)
xs = np.linspace(0.4, 6.6, 200)
m, cc = np.polyfit(DX, DY, 1)
ax.plot(xs, m * xs + cc, color=ACC, linewidth=2.4, zorder=5)
ax.annotate("a linear model\ndoes not follow the shape", (3.5, 12.4),
            color=ACC, fontsize=11, ha="center", zorder=8)
ax.set_xlim(0, 7); ax.set_ylim(0, 14.6)
ax.set_xticks([1, 2, 3, 4, 5, 6]); ax.set_yticks([4, 8, 12])
ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("Not appropriate", fontsize=11.5, pad=10)

# good: quadratic
ax = axes[1]
ax.scatter(DX, DY, s=60, color=INK, zorder=6)
q = np.polyfit(DX, DY, 2)
ax.plot(xs, np.polyval(q, xs), color=GREEN, linewidth=2.4, zorder=5)
ax.annotate("a quadratic model rises\nthen falls, like the data", (3.5, 12.4),
            color=GREEN, fontsize=11, ha="center", zorder=8)
ax.set_xlim(0, 7); ax.set_ylim(0, 14.6)
ax.set_xticks([1, 2, 3, 4, 5, 6]); ax.set_yticks([4, 8, 12])
ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("Appropriate", fontsize=11.5, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-6-fit.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ================= 3. interpolation と extrapolation =================
fig, ax = plt.subplots(figsize=(8.6, 4.8))
h = lambda t: 6 * t + 76
ts = np.array([2, 4, 6, 8, 10])
ax.axvspan(2, 10, color=FILL, zorder=1)

xs = np.linspace(0, 42, 200)
ax.plot(xs, h(xs), color=GREY, linestyle="--", linewidth=1.8, zorder=3)
xin = np.linspace(2, 10, 100)
ax.plot(xin, h(xin), color=LINE, linewidth=2.8, zorder=5)
ax.scatter(ts, h(ts), s=62, color=INK, zorder=7)

ax.annotate("the data covers\nonly this range", (6, 300), fontsize=10.5,
            color=LINE, ha="center", zorder=8)
ax.annotate("interpolation\n(inside the data)", (6, 200), fontsize=10.5,
            color=LINE, ha="center", zorder=8)
ax.annotate("extrapolation\n(outside the data)", (27, 130), fontsize=10.5,
            color=ACC, ha="center", zorder=8)

ax.scatter([40], [h(40)], s=70, color=ACC, zorder=7)
ax.annotate("the model says 316 cm\nat age 40", xy=(40, h(40)), xytext=(30, 355),
            fontsize=10.5, color=ACC, ha="center", zorder=8,
            arrowprops=dict(arrowstyle="->", color=ACC, linewidth=1.4))

ax.set_xlim(0, 46); ax.set_ylim(0, 420)
ax.set_xticks([2, 10, 20, 30, 40]); ax.set_yticks([100, 200, 300, 400])
ax.set_xlabel("age $t$ (years)")
ax.set_ylabel("height $h$ (cm)")
ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("The danger of extrapolation:  $h(t) = 6t + 76$", fontsize=12.5,
             pad=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-6-extrapolation.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 4. Ferris wheel（sinusoidal のあてはめ）=================
from matplotlib.patches import Circle

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6),
                         gridspec_kw={"width_ratios": [0.85, 1.25]})

# --- 左：観覧車そのもの ---
ax = axes[0]
ax.add_patch(Circle((0, 22), 20, facecolor="none", edgecolor=LINE, lw=2.2,
                    zorder=4))
ax.plot([-26, 26], [0, 0], color=INK, lw=2.0, zorder=5)          # 地面
ax.plot([0, 0], [0, 22], color=GREY, lw=1.4, ls="--", zorder=3)  # 支柱
ax.plot([0], [22], "o", color=GREY, ms=6, zorder=6)
ax.plot([0], [2], "o", color=ACC, ms=9, zorder=7)                # 座席（t=0）

ax.annotate("centre\n$22$ m", (1.6, 22), fontsize=10, color=GREY,
            ha="left", va="center", zorder=8)
ax.annotate("lowest:  $2$ m\n($t = 0$)", (1.8, 2.6), fontsize=10, color=ACC,
            ha="left", va="bottom", zorder=8)
ax.annotate("highest:  $42$ m", (0, 43.4), fontsize=10, color=LINE,
            ha="center", va="bottom", zorder=8)
ax.annotate("", xy=(-20, 22), xytext=(0, 22),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4,
                            mutation_scale=11), zorder=6)
ax.annotate("radius $20$ m", (-10, 23.4), fontsize=10, color=GREEN,
            ha="center", va="bottom", zorder=8)

ax.set_xlim(-27, 27); ax.set_ylim(-3, 50)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("the Ferris wheel", fontsize=12.5, pad=8)

# --- 右：高さと時間のグラフ ---
ax = axes[1]
tt = np.linspace(0, 240, 600)
hh = -20 * np.cos(np.radians(3 * tt)) + 22
ax.plot(tt, hh, color=LINE, lw=2.4, zorder=5)
ax.axhline(22, color=GREEN, lw=1.4, ls="--", zorder=3)
ax.annotate("principal axis  $h = 22$", (238, 23.4), fontsize=10, color=GREEN,
            ha="right", va="bottom", zorder=8)

for (tv, hv, lab) in [(0, 2, "$(0,\\ 2)$"), (20, 12, "$(20,\\ 12)$"),
                      (60, 42, "$(60,\\ 42)$")]:
    ax.scatter([tv], [hv], s=64, color=ACC, zorder=7)
    ax.annotate(lab, (tv + 5, hv + 1.5), fontsize=10.5, color=ACC, zorder=8)

ax.annotate("", xy=(120, 47), xytext=(0, 47),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.4,
                            mutation_scale=11), zorder=6)
ax.annotate("one turn:  period $= 120$ s", (60, 48.4), fontsize=10.5,
            color=GREY, ha="center", va="bottom", zorder=8)

ax.set_xlim(-8, 248); ax.set_ylim(-2, 54)
ax.set_xticks([0, 60, 120, 180, 240]); ax.set_yticks([2, 22, 42])
ax.set_xlabel("time $t$ (seconds)")
ax.set_ylabel("height $h$ (m)")
ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for sp2 in ("top", "right"):
    ax.spines[sp2].set_visible(False)
ax.set_title("$h(t) = -20\\cos(3t) + 22$", fontsize=12.5, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-6-ferris.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)


print("wrote sl-2-6-cycle.svg, sl-2-6-fit.svg, sl-2-6-extrapolation.svg,")
print("      sl-2-6-ferris.svg")
print("check ferris: h(0), h(20), h(60), h(120) =",
      [round(-20 * np.cos(np.radians(3 * v)) + 22, 6) for v in (0, 20, 60, 120)])
print("check h(2), h(10), h(40) =", h(2), h(10), h(40))
print("check data used for fit figure:", list(zip(DX, DY)))
