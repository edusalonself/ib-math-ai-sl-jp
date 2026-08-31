"""SL 5.1 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_1.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from math import exp

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY = "#7a8592"
GOLD = "#b9770e"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.9)


def axes(ax, xlim, ylim, xt=1, yt=1, xlab="$x$", ylab="$y$"):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for x in np.arange(np.ceil(xlim[0] / xt) * xt, xlim[1] + 1e-9, xt):
        ax.axvline(x, color=GRID, lw=0.7, zorder=0)
    for y in np.arange(np.ceil(ylim[0] / yt) * yt, ylim[1] + 1e-9, yt):
        ax.axhline(y, color=GRID, lw=0.7, zorder=0)
    ax.axhline(0, color=GREY, lw=1.2, zorder=1)
    ax.axvline(0, color=GREY, lw=1.2, zorder=1)
    ax.tick_params(labelsize=8.5, colors=GREY, length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel(xlab, fontsize=11, color=INK, labelpad=1)
    ax.set_ylabel(ylab, fontsize=11, color=INK, labelpad=12, rotation=0)


# ══════════════ 1. 極限：値が近づいていく ══════════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6),
                        gridspec_kw={"width_ratios": [1.15, 1]})

# --- (a) 表のイメージ
ax = axs[0]
ax.axis("off")
rows = [("$2.9$", "$5.9$"), ("$2.99$", "$5.99$"), ("$2.999$", "$5.999$"),
        ("$3$", "undefined"), ("$3.001$", "$6.001$"), ("$3.01$", "$6.01$"),
        ("$3.1$", "$6.1$")]
ax.text(0.30, 0.94, "$x$", ha="center", va="center", fontsize=12, weight="bold")
ax.text(0.72, 0.94, "$f(x)$", ha="center", va="center", fontsize=12, weight="bold")
ax.plot([0.10, 0.92], [0.885, 0.885], color=GREY, lw=1.2)
for i, (a, b) in enumerate(rows):
    y = 0.80 - i * 0.115
    col = ACC if b == "undefined" else INK
    ax.text(0.30, y, a, ha="center", va="center", fontsize=12, color=col)
    ax.text(0.72, y, b, ha="center", va="center", fontsize=12, color=col)
    if b == "undefined":
        ax.plot([0.10, 0.92], [y + 0.058, y + 0.058], color=ACC, lw=0.9, ls="--")
        ax.plot([0.10, 0.92], [y - 0.058, y - 0.058], color=ACC, lw=0.9, ls="--")
ax.annotate("", xy=(0.05, 0.53), xytext=(0.05, 0.84),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
ax.annotate("", xy=(0.05, 0.38), xytext=(0.05, 0.07),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
ax.set_title(r"$f(x)=\dfrac{x^{2}-9}{x-3}$", fontsize=12.5, color=INK, pad=10)
ax.set_xlim(0, 1); ax.set_ylim(-0.06, 1.02)

# --- (b) グラフ
ax = axs[1]
axes(ax, (-0.4, 6.4), (-0.4, 9.4), 1, 1)
xs = np.linspace(-0.4, 6.4, 400)
ax.plot(xs, xs + 3, color=LINE, lw=2.4, zorder=5)
ax.plot([3], [6], "o", color="white", markeredgecolor=ACC,
        markeredgewidth=2.2, ms=9, zorder=9)
ax.plot([3, 3], [0, 6], color=ACC, lw=1.1, ls="--", zorder=4)
ax.plot([0, 3], [6, 6], color=ACC, lw=1.1, ls="--", zorder=4)
ax.annotate("", xy=(2.75, 5.75), xytext=(1.6, 4.6),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
ax.annotate("", xy=(3.25, 6.25), xytext=(4.4, 7.4),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
ax.text(3.35, 5.15, "there is a hole\nat $x=3$", color=ACC, fontsize=10.5,
        ha="left", va="center", zorder=10, bbox=BOX)
ax.text(0.85, 8.3, r"$\lim_{x\to 3}\ f(x)=6$", color=INK, fontsize=13,
        ha="left", va="center", zorder=10, bbox=BOX)
ax.set_title("the graph gets close to $6$ from both sides",
             fontsize=11.5, color=INK, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-1-limit.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 弦から接線へ ══════════════
fig, ax = plt.subplots(figsize=(8.4, 5.8))
axes(ax, (-0.3, 3.6), (-0.6, 10.4), 0.5, 2)
xs = np.linspace(-0.3, 3.4, 400)
ax.plot(xs, xs ** 2, color=LINE, lw=2.4, zorder=5)
P = (2.0, 4.0)

cols = ["#e59866", "#d98880", GOLD, "#7d6608"]
labs = ["chord:  gradient $5$",
        "chord:  gradient $4.5$",
        "chord:  gradient $4.1$",
        "chord:  gradient $4.01$"]
# 弦の端の点に、座標をそのまま書き入れる（表と見くらべやすくするため）
QLBL = {1.0: (0.10, -0.62, "left", "top", "$(3,\\,9)$"),
        0.5: (0.12, -0.55, "left", "top", "$(2.5,\\,6.25)$"),
        0.1: (0.14, -0.42, "left", "top", "$(2.1,\\,4.41)$")}
for (h, c, lb) in zip([1.0, 0.5, 0.1, 0.01], cols, labs):
    Q = (2 + h, (2 + h) ** 2)
    m = (Q[1] - P[1]) / h
    t = np.array([1.35, 3.45])
    ax.plot(t, m * (t - P[0]) + P[1], color=c, lw=1.5, ls="--", zorder=6,
            label=lb)
    ax.plot([Q[0]], [Q[1]], "o", color=c, ms=6, zorder=8)
    if h in QLBL:
        dx, dy, ha, va, txt = QLBL[h]
        ax.text(Q[0] + dx, Q[1] + dy, txt, color=c, fontsize=10.5, ha=ha,
                va=va, zorder=11, bbox=BOX)
# 4つめの点は P に重なってしまうので、引き出し線で示す
ax.annotate("$(2.01,\\,4.0401)$", xy=(2.01, 4.0401), xytext=(1.20, 6.35),
            color="#7d6608", fontsize=10.5, ha="center", va="center",
            zorder=11, bbox=BOX,
            arrowprops=dict(arrowstyle="->", color="#7d6608", lw=1.2))

ax.plot(np.array([1.15, 3.45]), 4 * (np.array([1.15, 3.45]) - 2) + 4,
        color=ACC, lw=2.6, zorder=7, label="tangent at $P$:  $4$")
ax.plot([P[0]], [P[1]], "o", color=INK, ms=8, zorder=9)
ax.text(1.86, 3.55, "$P(2,4)$", ha="right", va="top", fontsize=11.5,
        zorder=10, bbox=BOX)
leg = ax.legend(loc="upper left", fontsize=10, frameon=True, framealpha=0.95,
                edgecolor="none", borderpad=0.7, labelspacing=0.6)
leg.set_zorder(12)
ax.text(3.45, 1.0, "as the second point slides towards $P$,\n"
                   "the chord turns into the tangent",
        color=GREEN, fontsize=11, ha="right", va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-1-chords.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. 傾きの関数（gradient function）══════════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.8))

ax = axs[0]
axes(ax, (-2.6, 2.6), (-0.6, 6.4), 1, 1)
xs = np.linspace(-2.5, 2.5, 400)
ax.plot(xs, xs ** 2, color=LINE, lw=2.4, zorder=5)
for a in (-2, -1, 0, 1, 2):
    m = 2 * a
    t = np.array([a - 0.65, a + 0.65])
    ax.plot(t, m * (t - a) + a ** 2, color=ACC, lw=1.9, zorder=6)
    ax.plot([a], [a ** 2], "o", color=INK, ms=5.5, zorder=8)
    if a == 0:
        ax.text(0.45, 0.30, "$0$", color=ACC, fontsize=10.5,
                ha="left", va="bottom", zorder=10, bbox=BOX)
    else:
        ax.text(a, a ** 2 - 0.55, f"${m}$", color=ACC, fontsize=10.5,
                ha="center", va="top", zorder=10, bbox=BOX)
ax.set_title("the gradient at each point of  $y=x^{2}$",
             fontsize=11.5, color=INK, pad=10)

ax = axs[1]
axes(ax, (-2.6, 2.6), (-4.6, 4.6), 1, 2, ylab="gradient")
ax.plot(np.linspace(-2.5, 2.5, 200), 2 * np.linspace(-2.5, 2.5, 200),
        color=ACC, lw=2.4, zorder=5)
for a in (-2, -1, 0, 1, 2):
    ax.plot([a], [2 * a], "o", color=ACC, ms=7, zorder=8)
ax.text(-2.35, 3.4, "plot the gradients\nagainst $x$", color=GREEN,
        fontsize=11, ha="left", va="center", zorder=10, bbox=BOX)
ax.set_title("those gradients form a new function",
             fontsize=11.5, color=INK, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-1-gradient-fn.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 変化率の見積もり（コーヒー）══════════════
fig, ax = plt.subplots(figsize=(8.4, 5.6))
axes(ax, (-0.6, 10.8), (18, 86), 2, 10, xlab="$t$ (minutes)",
     ylab="$T$ ($^\\circ$C)")
ts = np.linspace(0, 10.6, 400)
Tf = lambda t: 20 + 60 * np.exp(-0.15 * t)
ax.plot(ts, Tf(ts), color=LINE, lw=2.4, zorder=5)
for t in (0, 2, 4, 6, 8, 10):
    ax.plot([t], [Tf(t)], "o", color=INK, ms=5.5, zorder=8)

# 弦 (2, 64.4) → (6, 44.4)
ax.plot([2, 6], [64.4, 44.4], color=GREEN, lw=2.6, zorder=7)
ax.plot([2, 6], [64.4, 64.4], color=GREEN, lw=1.1, ls="--", zorder=6)
ax.plot([6, 6], [64.4, 44.4], color=GREEN, lw=1.1, ls="--", zorder=6)
ax.text(4.0, 67.5, "$4$ minutes", color=GREEN, fontsize=10.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(6.35, 54.4, r"$-20\,^{\circ}$C", color=GREEN, fontsize=10.5,
        ha="left", va="center", zorder=10, bbox=BOX)

# t=4 での接線
m = -9 * exp(-0.6)
tt = np.array([1.8, 6.6])
ax.plot(tt, m * (tt - 4) + Tf(4), color=ACC, lw=2.2, ls="--", zorder=7)
ax.plot([4], [Tf(4)], "o", color=ACC, ms=8, zorder=9)
ax.text(0.4, 32.0, r"chord:  $\dfrac{-20}{4}=-5\ ^{\circ}$C per minute",
        color=GREEN, fontsize=11.5, ha="left", va="center", zorder=10, bbox=BOX)
ax.text(0.4, 25.0, "the chord gradient estimates\nthe tangent gradient at $t=4$",
        color=ACC, fontsize=10.5, ha="left", va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-1-rate.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. 傾きの符号 ══════════════
fig, ax = plt.subplots(figsize=(8.4, 5.2))
# ★ 山と谷が x = -2, 2 ちょうどに来る形にしてある。
#    表から読み取る設問なので、目盛りの上でぴったり読めることが大事。
f = lambda x: 0.25 * x ** 3 - 3.0 * x + 1.0
axes(ax, (-4.4, 4.4), (-4.6, 6.6), 1, 1)
xs = np.linspace(-4.15, 4.15, 400)
ax.plot(xs, f(xs), color=LINE, lw=2.6, zorder=5)
SP = 2.0                               # f'(x) = 0.75x^2 - 3 = 0
for a in (-SP, SP):
    t = np.array([a - 1.05, a + 1.05])
    ax.plot(t, np.full_like(t, f(a)), color=ACC, lw=2.2, zorder=6)
    ax.plot([a], [f(a)], "o", color=ACC, ms=7.5, zorder=9)
for a, col in ((-3.4, GREEN), (0.0, GOLD), (3.4, GREEN)):
    m = 0.75 * a ** 2 - 3.0
    t = np.array([a - 0.6, a + 0.6])
    ax.plot(t, m * (t - a) + f(a), color=col, lw=2.0, zorder=6)
    ax.plot([a], [f(a)], "o", color=col, ms=6, zorder=8)
ax.text(-4.15, 3.4, "$f'(x)>0$", color=GREEN, fontsize=11.5, ha="left",
        va="center", zorder=10, bbox=BOX)
ax.text(0.85, 2.6, "$f'(x)<0$", color=GOLD, fontsize=11.5, ha="left",
        va="center", zorder=10, bbox=BOX)
ax.text(2.55, 4.9, "$f'(x)>0$", color=GREEN, fontsize=11.5, ha="left",
        va="center", zorder=10, bbox=BOX)
ax.text(-SP, f(-SP) + 0.50, "$f'(x)=0$  at  $x=-2$", color=ACC, fontsize=11,
        ha="center", va="bottom", zorder=10, bbox=BOX)
ax.text(SP, f(SP) - 0.50, "$f'(x)=0$  at  $x=2$", color=ACC, fontsize=11,
        ha="center", va="top", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-1-sign.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
print("limit table (x^2-9)/(x-3):",
      [round((x * x - 9) / (x - 3), 4) for x in (2.9, 2.99, 3.001, 3.01, 3.1)])
print("chord gradients at (2,4):",
      [round(((2 + h) ** 2 - 4) / h, 4) for h in (1, 0.5, 0.1, 0.01)])
print("coffee table:", {t: round(20 + 60 * exp(-0.15 * t), 1)
                        for t in (0, 2, 4, 6, 8, 10)})
print("coffee chord estimate at t=4:", (44.4 - 64.4) / 4,
      "  true:", round(-9 * exp(-0.6), 4))
print("figures written to", os.path.normpath(OUT))


# ══════════════════════════════════════════════════════════
#  例題の「問題文のところに出す」グラフ
#   本文の図は答えが書き込んであるので、問題用には
#   注釈のない素のグラフを別に作る。
#   例題の枠の中に置くので、背景は透明にする。
# ══════════════════════════════════════════════════════════
def q_fig(name, draw, figsize=(6.4, 4.2)):
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


# --- 例題1：y = (x^2-9)/(x-3)、x = 3 に穴 ---
def _q1(ax):
    axes(ax, (-0.4, 6.4), (-0.4, 9.4), 1, 1)
    xs = np.linspace(-0.4, 6.4, 400)
    ax.plot(xs, xs + 3, color=LINE, lw=2.4, zorder=5)
    ax.plot([3], [6], "o", color="white", markeredgecolor=ACC,
            markeredgewidth=2.2, ms=9, zorder=9)
    ax.set_title(r"$y = f(x)$", fontsize=12, color=INK, pad=10)


q_fig("sl-5-1-q1.svg", _q1, (5.6, 4.0))


# --- 例題2：y = x^2 と、P・2つの Q ---
def _q2(ax):
    axes(ax, (-0.3, 3.6), (-0.6, 10.4), 0.5, 2)
    xs = np.linspace(-0.3, 3.4, 400)
    ax.plot(xs, xs ** 2, color=LINE, lw=2.4, zorder=5)
    P = (2.0, 4.0)
    for Q in [(3.0, 9.0), (2.1, 4.41)]:
        ax.plot([P[0], Q[0]], [P[1], Q[1]], color=GREY, lw=1.3, ls="--",
                zorder=6)
        ax.plot([Q[0]], [Q[1]], "o", color=ACC, ms=7, zorder=8)
    ax.plot([P[0]], [P[1]], "o", color=INK, ms=8, zorder=9)
    ax.text(1.80, 3.30, "$P(2,4)$", ha="right", va="top", fontsize=11.5,
            zorder=10)
    ax.text(3.08, 8.75, "$Q(3,\\,9)$", ha="left", va="center", color=ACC,
            fontsize=11.5, zorder=10)
    ax.annotate("$Q(2.1,\\,4.41)$", xy=(2.1, 4.41), xytext=(1.05, 6.4),
                color=ACC, fontsize=11.5, ha="center", va="center", zorder=10,
                arrowprops=dict(arrowstyle="->", color=ACC, lw=1.2))
    ax.set_title(r"$y = x^{2}$", fontsize=12, color=INK, pad=10)


q_fig("sl-5-1-q2.svg", _q2, (6.0, 4.4))


# --- 例題4：関数のグラフ（注釈なし） ---
def _q4(ax):
    f = lambda x: 0.25 * x ** 3 - 3.0 * x + 1.0
    axes(ax, (-4.4, 4.4), (-4.6, 6.6), 1, 1)
    xs = np.linspace(-4.15, 4.15, 400)
    ax.plot(xs, f(xs), color=LINE, lw=2.6, zorder=5)
    ax.set_title(r"$y = f(x)$", fontsize=12, color=INK, pad=10)


q_fig("sl-5-1-q4.svg", _q4, (6.4, 4.6))

print("wrote sl-5-1-q1.svg, sl-5-1-q2.svg, sl-5-1-q4.svg")


# ══════════════════════════════════════════════════════════
#  GDC の画面 — ctrl + T でグラフと表の2分割にしたところ
#   表は「はじめから埋まっている」ことと、x = 3 が undef に
#   なることを見せるための図。
# ══════════════════════════════════════════════════════════
from matplotlib.patches import Rectangle

fig, ax = plt.subplots(figsize=(9.2, 3.6))
ax.set_xlim(0, 124); ax.set_ylim(0, 53); ax.axis("off")

SCR_BG, SCR_EDGE, HDR = "#ffffff", "#9aa0ac", "#eef0f3"

# 画面ぜんたいの枠
ax.add_patch(Rectangle((1, 1), 98, 44, facecolor=SCR_BG, edgecolor=SCR_EDGE,
                       linewidth=1.3, zorder=2))
ax.plot([53, 53], [1, 45], color=SCR_EDGE, lw=1.3, zorder=3)   # 2分割の線

# ── 左：グラフ ─────────────────────────────────────────
gx0, gy0, gw, gh = 5.0, 5.0, 44.0, 35.0
cx, cy = gx0 + gw * 0.44, gy0 + gh * 0.44
ax.plot([gx0 + 2, gx0 + gw - 2], [cy, cy], color=GREY, lw=1.0, zorder=4)
ax.plot([cx, cx], [gy0 + 2, gy0 + gh - 2], color=GREY, lw=1.0, zorder=4)
M = 0.95                                   # 画面の中に収まる傾き
ylo, yhi = gy0 + 3.0, gy0 + gh - 3.0       # 線を枠の中で切る
t = np.array([cx + (ylo - cy) / M, cx + (yhi - cy) / M])
ax.plot(t, cy + (t - cx) * M, color="#c4009b", lw=2.2, zorder=6)
ax.text(gx0 + gw - 1.0, gy0 + 1.5, r"$f1(x)=\dfrac{x^{2}-9}{x-3}$",
        color="#c4009b", fontsize=10.5, ha="right", va="bottom", zorder=7)

# ── 右：表 ─────────────────────────────────────────────
tx0, tw = 56.0, 40.0
rows = [("$0.$", "$3.$"), ("$1.$", "$4.$"), ("$2.$", "$5.$"),
        ("$3.$", "undef"), ("$4.$", "$7.$")]
rh, top = 5.6, 38.0
ax.add_patch(Rectangle((tx0, top), tw, 5.0, facecolor=HDR, edgecolor=SCR_EDGE,
                       linewidth=0.9, zorder=4))
ax.text(tx0 + tw * 0.25, top + 2.5, "$x$", fontsize=11.5, ha="center",
        va="center", zorder=6)
ax.text(tx0 + tw * 0.72, top + 2.5, "$f1(x)$", fontsize=11.5, ha="center",
        va="center", color="#c4009b", zorder=6)
for i, (a, b) in enumerate(rows):
    y = top - (i + 1) * rh
    hit = (b == "undef")
    ax.add_patch(Rectangle((tx0, y), tw, rh,
                           facecolor="#fdecea" if hit else "white",
                           edgecolor=SCR_EDGE, linewidth=0.7, zorder=4))
    ax.text(tx0 + tw * 0.25, y + rh / 2, a, fontsize=11, ha="center",
            va="center", zorder=6)
    ax.text(tx0 + tw * 0.72, y + rh / 2, b, fontsize=11, ha="center",
            va="center", color=ACC if hit else INK,
            fontweight="bold" if hit else None, zorder=6)
    if hit:
        ax.add_patch(Rectangle((tx0, y), tw, rh, facecolor="none",
                               edgecolor=ACC, linewidth=2.0, zorder=7))
        yhit = y + rh / 2

ax.annotate("$f(3)$ does not exist", xy=(99.8, yhit), xytext=(102.5, yhit),
            color=ACC, fontsize=11, ha="left", va="center", zorder=9,
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.4))
ax.text(50, 49.0, "the table comes out already filled in", fontsize=11,
        color=INK, ha="center", va="center", zorder=9)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-1-gdc-table.svg"), bbox_inches="tight",
            transparent=True)
plt.close(fig)
print("wrote sl-5-1-gdc-table.svg")
