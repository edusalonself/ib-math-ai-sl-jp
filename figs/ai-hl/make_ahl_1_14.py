"""AHL 1.14 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-hl/01-number-and-algebra/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_1_14.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib.pyplot as plt
from _matrix import (INK, LINE, ACC, GREEN, GREY, GOLD, FILL, BOX,
                     blank, matrix, label, arrow)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight")
    plt.close(fig)


# ══════════════ 1. order（行×列）と element ══════════════
fig, ax = plt.subplots(figsize=(7.6, 4.2))
blank(ax, (-1.0, 9.2), (-1.9, 3.4))

rows = [["1", "2", "3"], ["4", "5", "6"]]
c, (x0, y0, w, h) = matrix(ax, 3.0, 1.0, rows, cw=0.86, ch=0.72, fs=15)

# 行を強調
ax.plot([x0 - 0.12, x0 + w + 0.12], [c[(0, 0)][1], c[(0, 0)][1]],
        color=ACC, lw=2.4, alpha=0.35, zorder=3)
label(ax, x0 + w + 0.45, c[(0, 0)][1], "row 1", color=ACC, ha="left")

# 列を強調
ax.plot([c[(0, 1)][0], c[(0, 1)][0]], [y0 - 0.10, y0 + h + 0.10],
        color=GREEN, lw=2.4, alpha=0.35, zorder=3)
label(ax, c[(0, 1)][0], y0 + h + 0.40, "column 2", color=GREEN)

# element
ax.plot(*c[(1, 2)], "o", ms=22, mfc="none", mec=GOLD, mew=2.0, zorder=8)
arrow(ax, (7.05, -0.80), (c[(1, 2)][0] + 0.06, c[(1, 2)][1] - 0.36),
      color=GOLD, rad=0.24)
label(ax, 7.35, -0.95, "element in row 2, column 3", color=GOLD, ha="left")

label(ax, 3.0, 2.85, "this matrix has order  $2 \\times 3$", fs=14)
label(ax, 3.0, -1.55, "ORDER is always  rows $\\times$ columns  —  in that order",
      color=GOLD, fs=12.5)
fig.tight_layout()
save(fig, "ahl-1-14-order.svg")


# ══════════════ 2. かけ算：内側がそろうこと ══════════════
fig, axs = plt.subplots(2, 1, figsize=(8.0, 5.6),
                        gridspec_kw={"height_ratios": [0.80, 1.30]})

# --- 上：次数の合わせ方 ---
ax = axs[0]
blank(ax, (-0.4, 10.4), (-1.25, 2.30))
ax.set_aspect("auto")
for x, t in ((1.4, "$2 \\times 3$"), (4.2, "$3 \\times 2$")):
    ax.text(x, 0.9, t, fontsize=20, ha="center", va="center", color=INK)
ax.text(2.8, 0.9, "$\\times$", fontsize=17, ha="center", va="center",
        color=GREY)

ax.annotate("", xy=(3.55, 1.45), xytext=(2.15, 1.45),
            arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=1.8,
                            connectionstyle="arc3,rad=-0.55",
                            mutation_scale=12))
ax.text(2.85, 2.02, "these MUST be equal", fontsize=12.5, ha="center",
        va="center", color=GREEN)

ax.annotate("", xy=(4.85, 0.15), xytext=(0.75, 0.15),
            arrowprops=dict(arrowstyle="<|-|>", color=ACC, lw=1.8,
                            connectionstyle="arc3,rad=0.30",
                            mutation_scale=12))
ax.text(2.8, -0.85, "the OUTER two give the answer's order", fontsize=12.5,
        ha="center", va="center", color=ACC)

ax.text(6.15, 0.9, "$\\Rightarrow$", fontsize=18, ha="center", va="center",
        color=GREY)
ax.text(7.6, 0.9, "$2 \\times 2$", fontsize=20, ha="center", va="center",
        color=ACC)

# --- 下：行×列 ---
ax = axs[1]
blank(ax, (-0.6, 11.0), (-0.75, 2.80))

A = [["1", "2"], ["3", "4"]]
B = [["5", "6"], ["7", "8"]]
cA, (ax0, ay0, aw, ah) = matrix(ax, 1.3, 1.0, A, cw=0.66, ch=0.62, fs=14,
                                cell_color={(0, 0): ACC, (0, 1): ACC})
ax.text(2.35, 1.0, "$\\times$", fontsize=14, ha="center", va="center",
        color=GREY)
cB, (bx0, by0, bw, bh) = matrix(ax, 3.4, 1.0, B, cw=0.66, ch=0.62, fs=14,
                                cell_color={(0, 0): GREEN, (1, 0): GREEN})
ax.text(4.45, 1.0, "$=$", fontsize=14, ha="center", va="center", color=GREY)
cC, _ = matrix(ax, 5.9, 1.0, [["19", "22"], ["43", "50"]], cw=0.84, ch=0.62,
               fs=14, cell_color={(0, 0): GOLD})

ax.plot([ax0 - 0.10, ax0 + aw + 0.10], [cA[(0, 0)][1], cA[(0, 0)][1]],
        color=ACC, lw=2.4, alpha=0.30, zorder=3)
ax.plot([cB[(0, 0)][0], cB[(0, 0)][0]], [by0 - 0.10, by0 + bh + 0.10],
        color=GREEN, lw=2.4, alpha=0.30, zorder=3)
ax.plot(*cC[(0, 0)], "o", ms=24, mfc="none", mec=GOLD, mew=1.8, zorder=8)

ax.text(8.9, 1.55, "row 1 of the first", fontsize=12, ha="center",
        va="center", color=ACC)
ax.text(8.9, 1.10, "$\\times$  column 1 of the second", fontsize=12,
        ha="center", va="center", color=GREEN)
ax.text(8.9, 0.55, "$1(5) + 2(7) = 19$", fontsize=13, ha="center",
        va="center", color=GOLD)

ax.text(5.2, 2.35, "go ACROSS the row, DOWN the column, "
                   "multiply and add", fontsize=12.5, ha="center",
        va="center", color=GOLD)
fig.tight_layout()
save(fig, "ahl-1-14-multiply.svg")


# ══════════════ 3. AB と BA は違う ══════════════
fig, ax = plt.subplots(figsize=(8.6, 3.5))
blank(ax, (-0.6, 11.95), (-1.35, 2.55))

A = [["1", "2"], ["3", "4"]]
B = [["5", "6"], ["7", "8"]]

matrix(ax, 0.9, 0.9, A, cw=0.60, ch=0.58, fs=13)
matrix(ax, 2.3, 0.9, B, cw=0.60, ch=0.58, fs=13)
ax.text(3.25, 0.9, "$=$", fontsize=14, ha="center", va="center", color=GREY)
matrix(ax, 4.35, 0.9, [["19", "22"], ["43", "50"]], cw=0.78, ch=0.58, fs=13,
       color=ACC, bracket=ACC)
ax.text(1.6, 2.05, "$AB$", fontsize=15, ha="center", va="center", color=INK)

ax.text(5.75, 0.9, "$\\neq$", fontsize=22, ha="center", va="center",
        color=GOLD)

matrix(ax, 7.1, 0.9, B, cw=0.60, ch=0.58, fs=13)
matrix(ax, 8.5, 0.9, A, cw=0.60, ch=0.58, fs=13)
ax.text(9.45, 0.9, "$=$", fontsize=14, ha="center", va="center", color=GREY)
matrix(ax, 10.55, 0.9, [["23", "34"], ["31", "46"]], cw=0.78, ch=0.58, fs=13,
       color=GREEN, bracket=GREEN)
ax.text(7.8, 2.05, "$BA$", fontsize=15, ha="center", va="center", color=INK)

ax.text(5.6, -1.00, "with numbers  $3 \\times 5 = 5 \\times 3$,  "
                    "but with matrices the ORDER matters",
        fontsize=12.5, ha="center", va="center", color=GOLD)
fig.tight_layout()
save(fig, "ahl-1-14-noncomm.svg")


# ══════════════ 4. 2×2 の逆行列の作り方 ══════════════
fig, ax = plt.subplots(figsize=(8.4, 4.2))
blank(ax, (-0.7, 9.9), (-2.35, 2.30))

# 左：もとの行列（a,d を赤、b,c を緑）
matrix(ax, 1.0, 0.85, [["$a$", "$b$"], ["$c$", "$d$"]],
       cw=0.74, ch=0.68, fs=16,
       cell_color={(0, 0): ACC, (1, 1): ACC, (0, 1): GREEN, (1, 0): GREEN})
ax.text(1.0, 1.85, "$A$", fontsize=15, ha="center", va="center", color=INK)

arrow(ax, (2.15, 0.85), (3.15, 0.85), color=GREY, lw=1.8)

# 右：入れ替えたあと
matrix(ax, 4.35, 0.85, [["$d$", "$-b$"], ["$-c$", "$a$"]],
       cw=0.90, ch=0.68, fs=16,
       cell_color={(0, 0): ACC, (1, 1): ACC, (0, 1): GREEN, (1, 0): GREEN})

ax.text(5.75, 0.85, "$\\div$", fontsize=18, ha="center", va="center",
        color=GOLD)
ax.text(7.75, 0.85, "$\\det A = ad-bc$", fontsize=15, ha="center",
        va="center", color=GOLD)
ax.text(4.35, 1.85, "$A^{-1}$", fontsize=15, ha="center", va="center",
        color=INK)

# 説明は矢印を交差させず、下に2行だけ
ax.text(2.65, -0.55, "$a$ and $d$  swap places", fontsize=12.5,
        ha="center", va="center", color=ACC)
ax.text(2.65, -1.10, "$b$ and $c$  change sign, stay put", fontsize=12.5,
        ha="center", va="center", color=GREEN)

ax.text(4.6, -1.85, "if  $\\det A = 0$  there is NO inverse  "
                    "(the matrix is SINGULAR)",
        fontsize=12.5, ha="center", va="center", color=GOLD)
fig.tight_layout()
save(fig, "ahl-1-14-inverse.svg")


# ══════════════ 5. Ax = b を解く ══════════════
fig, ax = plt.subplots(figsize=(8.2, 4.5))
blank(ax, (-0.6, 10.0), (-3.05, 3.35))
ax.set_aspect("auto")

ax.text(0.2, 2.6, "$3x + y = 11$", fontsize=14, ha="left", va="center")
ax.text(0.2, 1.9, "$5x + 2y = 19$", fontsize=14, ha="left", va="center")
arrow(ax, (2.7, 2.25), (3.7, 2.25), color=GREY)

cA, _ = matrix(ax, 4.5, 2.25, [["3", "1"], ["5", "2"]], cw=0.56, ch=0.50,
               fs=13, color=ACC, bracket=ACC)
cx, _ = matrix(ax, 5.5, 2.25, [["$x$"], ["$y$"]], cw=0.52, ch=0.50, fs=13)
ax.text(6.15, 2.25, "$=$", fontsize=13, ha="center", va="center", color=GREY)
cb, _ = matrix(ax, 6.9, 2.25, [["11"], ["19"]], cw=0.70, ch=0.50, fs=13,
               color=GREEN, bracket=GREEN)
ax.text(4.5, 3.05, "$A$", fontsize=13, ha="center", color=ACC)
ax.text(5.5, 3.05, "$\\mathbf{x}$", fontsize=13, ha="center", color=INK)
ax.text(6.9, 3.05, "$\\mathbf{b}$", fontsize=13, ha="center", color=GREEN)

ax.text(4.7, 1.05, "$A\\mathbf{x} = \\mathbf{b}$", fontsize=18, ha="center",
        va="center", color=INK)
arrow(ax, (4.7, 0.60), (4.7, -0.15), color=GOLD, lw=1.8)
ax.text(5.05, 0.22, "multiply both sides by $A^{-1}$ ON THE LEFT",
        fontsize=12, ha="left", va="center", color=GOLD)

ax.text(4.7, -0.70, "$\\mathbf{x} = A^{-1}\\mathbf{b}$", fontsize=18,
        ha="center", va="center", color=ACC)

ax.text(4.7, -1.85, "$A^{-1}$ must go on the LEFT of $\\mathbf{b}$  —  "
                    "$\\mathbf{b}A^{-1}$ is not even defined",
        fontsize=12.5, ha="center", va="center", color=GOLD)
ax.text(4.7, -2.60, "this works only when $\\det A \\neq 0$",
        fontsize=12, ha="center", va="center", color=GREY)
fig.tight_layout()
save(fig, "ahl-1-14-solve.svg")


# ══════════════ GDC の画面：inverse と determinant ══════════════
#  実機（TI-Nspire CX II、非CAS）の表示をそのまま図にしたもの。
fig, ax = plt.subplots(figsize=(8.6, 4.6))
blank(ax, (0, 8.6), (0, 4.6))
ax.set_aspect("auto")

SCREEN = "#f7f8f9"
ax.add_patch(plt.Rectangle((0.12, 0.12), 8.36, 4.36, fc="white",
                           ec="#c8cdd3", lw=1.6, zorder=1))
for y0, y1, fc in ((3.06, 4.48, SCREEN), (1.02, 3.06, "white"),
                   (0.12, 1.02, SCREEN)):
    ax.add_patch(plt.Rectangle((0.12, y0), 8.36, y1 - y0, fc=fc,
                               ec="#e4e7ea", lw=1.0, zorder=2))

# 1 行目：行列を打って a に保存
matrix(ax, 1.05, 3.77, [["1", "2"], ["3", "4"]], cw=0.44, ch=0.42, fs=13)
ax.text(1.62, 3.77, r"$\rightarrow a$", fontsize=14, ha="left", va="center",
        color=INK, zorder=6)
matrix(ax, 7.55, 3.77, [["1", "2"], ["3", "4"]], cw=0.44, ch=0.42, fs=13)

# 2 行目：逆行列
ax.text(0.45, 2.04, "$a^{-1}$", fontsize=15, ha="left", va="center",
        color=INK, zorder=6)
matrix(ax, 7.45, 2.04, [["$-2$", "$1$"],
                        [r"$\dfrac{3}{2}$", r"$-\dfrac{1}{2}$"]],
       cw=0.62, ch=0.72, fs=13)

# 3 行目：determinant
ax.text(0.45, 0.57, r"$\det(a)$", fontsize=15, ha="left", va="center",
        color=INK, zorder=6)
ax.text(8.05, 0.57, "$-2$", fontsize=15, ha="right", va="center", color=INK,
        zorder=6)
fig.tight_layout()
save(fig, "ahl-1-14-gdc.svg")

print("figures written to", os.path.normpath(OUT))
