"""AA HL 4.14a（離散確率変数の分散）の図をつくる。

    python3 figs/aa-hl/make_aahl_4_14a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_4_14a.py  … 目視用の PNG も

出力: aa-hl/04-statistics-and-probability/img/aahl-4-14a-idea-a.svg
      aa-hl/04-statistics-and-probability/img/aahl-4-14a-idea-b.svg

(a) 平均が同じでも、ちらばりはちがう。分散はそのちらばりを測る。
(b) aX + b：b はずらすだけ、a は広げる。分散は a^2 倍。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → 使わない
  * \\lvert \\rvert も読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "04-statistics-and-probability",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

# ══════════════════════════════════════════════════════════
# (a) 同じ平均、ちがうちらばり
# ══════════════════════════════════════════════════════════
fig1, axs = plt.subplots(1, 2, figsize=(6.6, 2.8), sharey=True)
fig1.suptitle("same mean, different spread", fontsize=11, color=INK,
              x=0.01, ha="left", y=1.03)

XS = [1, 2, 3, 4, 5]
TIGHT = [0.05, 0.20, 0.50, 0.20, 0.05]
WIDE = [0.30, 0.10, 0.20, 0.10, 0.30]

for _ax, _ps, _title, _col in ((axs[0], TIGHT, "small variance", ACCENT),
                               (axs[1], WIDE, "large variance", WARM)):
    _ax.bar(XS, _ps, width=0.55, color=_col, alpha=0.85, zorder=2)
    _ax.axvline(3, color=INK, linewidth=1.3, linestyle=(0, (4, 3)), zorder=3)
    _ax.text(3.08, 0.545, "mean", fontsize=9, color=INK)
    _ax.set_title(_title, fontsize=9.8, color=INK, loc="left", pad=4)
    _ax.set_xticks(XS)
    _ax.set_ylim(0, 0.62)
    _ax.set_xlabel("$x$", fontsize=10, color=INK)
    _ax.spines["top"].set_visible(False)
    _ax.spines["right"].set_visible(False)
    _ax.tick_params(labelsize=9, colors=GREY)

axs[0].set_ylabel("$P(X = x)$", fontsize=10, color=INK)
fig1.text(0.01, -0.06, "the mean alone does not say how far the values"
          " usually sit from it", fontsize=9, color=GREY)

# ══════════════════════════════════════════════════════════
# (b) aX + b
# ══════════════════════════════════════════════════════════
fig2, axs2 = plt.subplots(3, 1, figsize=(6.2, 4.0), sharex=True)
fig2.suptitle("$aX + b$: adding $b$ slides, multiplying by $a$ stretches",
              fontsize=10.5, color=INK, x=0.01, ha="left", y=1.02)

PS = [0.2, 0.5, 0.3]
ROWS = ((axs2[0], [1, 2, 3], ACCENT, "$X$", "gaps of $1$"),
        (axs2[1], [5, 6, 7], GREY, "$X + b$  (here $b = 4$)",
         "same gaps: the spread has not changed"),
        (axs2[2], [6, 8, 10], WARM, "$aX + b$  (here $a = 2$)",
         "gaps of $2$: the spread is $a$ times wider"))

for _ax, _xs, _col, _lab, _note in ROWS:
    _ax.bar(_xs, PS, width=0.32, color=_col, alpha=0.88, zorder=2)
    _ax.set_ylim(0, 0.72)
    _ax.set_yticks([0, 0.5])
    _ax.text(0.4, 0.52, _lab, fontsize=9.5, color=_col)
    _ax.text(3.4, 0.52, _note, fontsize=8.8, color=GREY)
    _ax.spines["top"].set_visible(False)
    _ax.spines["right"].set_visible(False)
    _ax.tick_params(labelsize=9, colors=GREY)

axs2[2].set_xticks([1, 2, 3, 5, 6, 7, 8, 10])
axs2[2].set_xlabel("value", fontsize=10, color=INK)
axs2[1].set_ylabel("probability", fontsize=9.5, color=INK)
fig2.text(0.01, -0.03, "so the variance is multiplied by $a^{2}$ and is not"
          " changed by $b$", fontsize=9, color=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-4-14a-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-4-14a-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
