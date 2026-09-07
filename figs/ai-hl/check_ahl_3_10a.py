"""AHL 3.10a（ベクトルの基本）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_10a.py
"""
import os
import re
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry",
                   "ahl-3-10a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_ahl_3_10a.py"), encoding="utf-8").read()

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def vec(*a):
    return sp.Matrix(list(a))


def same(u, v, msg=""):
    chk(sp.simplify(u - v) == sp.zeros(*u.shape), msg + f"  ({list(u)} vs {list(v)})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 1. 成分・和・差・スカラー倍の基本規則
# ══════════════════════════════════════════════════════════
# 図 1(a): A(-3,-1) → B(1,2) の成分は「右に4、上に3」
A_pt, B_pt = vec(-3, -1), vec(1, 2)
same(B_pt - A_pt, vec(4, 3), "図1(a) AB の成分")
in_text("$A$ から $B$ へは、**右に $4$、上に $3$** 進みます", "図1(a) の読み取りと本文が一致")
chk("$4$ across" in FIG or "4$ across" in FIG or "\\binom{4}{3}" in FIG,
    "図1(a) のラベルが 4 across / 3 up")
chk("SAME vector $\\\\binom{4}{3}$" in FIG, "図1(b) の見出しが (4,3) になっている（(a) と同じベクトル）")
chk("binom{3}{2}" not in FIG, "図1(b) が別のベクトル (3,2) を出していない")
# 図1(b) の4本は、すべて (4,3)
starts = re.search(r"STARTS = \[(.*?)\]\n", FIG, re.S).group(1)
pairs = re.findall(r"\(([-\d.]+), ([-\d.]+)\)", starts)
chk(len(pairs) == 4, "図1(b) の矢印は 4 本")
chk("sx + 4, sy + 3" in FIG, "図1(b) の 4 本はすべて (4,3) だけ進む")

# 図 2: a=(3,1), b=(1,3)
a, b = vec(3, 1), vec(1, 3)
same(a + b, vec(4, 4), "図2(a) a+b")
same(a + b, b + a, "足し算の交換法則")
same(a - b, vec(2, -2), "a-b")
same(b - a, vec(-2, 2), "b-a")
same(b - a, -(a - b), "b-a = -(a-b)")
in_text("\\mathbf{a}-\\mathbf{b} = \\begin{pmatrix} 2 \\\\ -2 \\end{pmatrix}, \\qquad "
        "\\mathbf{b}-\\mathbf{a} = \\begin{pmatrix} -2 \\\\ 2 \\end{pmatrix}",
        "引き算の順序の例")
# 図2(b): a-b は b の先から a の先へ。図でも B→A に描いている
chk("arrow(ax, B, A, color=ACC" in FIG, "図2(b) の a-b は B から A へ")
# b-a は重ならないよう平行にずらして描く（重ねると「同じ矢印」に見える）
chk("OFF" in FIG and "arrow(ax, A + OFF, B + OFF" in FIG,
    "図2(b) の b-a は少しずらして描いている")
chk("drawn slightly to the side" in FIG, "ずらしたことを図に明記している")

# 図 3: k = 1, 2, 0.5, -1.5 倍
v = vec(2, 1)
for k, tip in [(1, (2, 1)), (2, (4, 2)), (sp.Rational(1, 2), (1, sp.Rational(1, 2))),
               (sp.Rational(-3, 2), (-3, sp.Rational(-3, 2)))]:
    same(k * v, vec(*tip), f"図3 の {k} 倍")
chk("(1.0, \"$\\\\mathbf{a}$\"" in FIG, "図3 の 1 行目は k=1")
# 図の注記は k=0 を除いてある（k=0 では平行が言えない）
chk("\\\\neq \\\\mathbf{0}$ and $k \\\\neq 0" in FIG,
    "図3 の注記に a≠0 と k≠0 の両方が入っている")
not_in_text("(for $\\mathbf{a} \\neq \\mathbf{0}$)", "図の注記の古い形")

# ══════════════════════════════════════════════════════════
# 2. 例題の数値
# ══════════════════════════════════════════════════════════
# 例題 1: a=(3,-1), b=(2,5)
a1, b1 = vec(3, -1), vec(2, 5)
same(a1 + b1, vec(5, 4), "例題1(a)")
same(a1 - b1, vec(1, -6), "例題1(b)")
same(2 * a1 - 3 * b1, vec(0, -17), "例題1(c)")
# 検算（b-a が a-b の符号違い）が、片方の符号ミスを捕まえるか
wrong = vec(3 - 2, -1 + 5)          # 引き算を足してしまった答え (1,4)
chk(sp.simplify(b1 - a1 + wrong) != sp.zeros(2, 1), "例題1 の検算は符号ミスを捕まえる")
chk(sp.simplify(b1 - a1 + (a1 - b1)) == sp.zeros(2, 1), "正しい答えなら検算は通る")

# 例題 2: p = 4i - j, q = -2i + 3j
p, q = vec(4, -1), vec(-2, 3)
same(p + q, vec(2, 2), "例題2(a)")
same(3 * p - 2 * q, vec(16, -9), "例題2(b)")
same(-q, vec(2, -3), "例題2(c) -q")
# 検算は (b) を対象にしている（(a) を i,j で足し直すのは同じ計算で circular）
in_text("いちばん危ないのは (b) なので、そこを逆から見ます", "例題2 の検算は (b) を見る")
not_in_text("(a) は $\\mathbf{i}$ と $\\mathbf{j}$ のまま足しても確かめられます",
            "同じ計算をなぞるだけの検算")
# その検算が 12-(-4) を 8 と誤った答えを捕まえるか
wrong_b = vec(8, -9)
chk(sp.simplify((wrong_b + 2 * q) - 3 * p) != sp.zeros(2, 1),
    "例題2 の検算は 12-(-4)=8 の誤りを捕まえる")
chk(sp.simplify((3 * p - 2 * q + 2 * q) - 3 * p) == sp.zeros(2, 1),
    "正しい答えなら検算は通る")

# 例題 3: (6,-4) と (-9,6) は平行、k = -2/3
a3, b3 = vec(6, -4), vec(-9, 6)
k3 = sp.Rational(-2, 3)
same(k3 * b3, a3, "例題3 の k")
chk(sp.Rational(6, -9) == k3 and sp.Rational(-4, 6) == k3, "例題3 の比が一致")
# 平行でない例 (6,-4) と (-9,5)
chk(sp.Rational(6, -9) != sp.Rational(-4, 5), "比が食い違えば平行でない")
# 「成分の符号が全部逆」→「逆向き」は、平行が前提。反例が本文にある
c1, c2 = vec(1, -1), vec(-1, 5)
chk(sp.simplify(c1[0] * c2[1] - c1[1] * c2[0]) != 0,
    "反例 (1,-1) と (-1,5) は平行ですらない")
chk(c1[0] * c2[0] < 0 and c1[1] * c2[1] < 0, "しかし成分の符号は全部逆")
in_text("は符号が全部逆ですが、平行ですらありません", "その反例を本文に書いている")
not_in_text("**両方の成分で符号が逆**なので、正反対の向き", "根拠の足りない古い検算")

# 例題 4: ドローン 3 本の行程
legs = [vec(300, 400), vec(-100, 250), vec(150, -500)]
res = legs[0] + legs[1] + legs[2]
same(res, vec(350, 150), "例題4(a) resultant")
same(-res, vec(-350, -150), "例題4(b) 戻る変位")
# 検算は「順序を変えて足し直す」。(a)+(b)=0 は circular なので使わない
same(legs[1] + legs[2], vec(50, -250), "例題4 の検算の途中")
same(legs[1] + legs[2] + legs[0], res, "順序を変えても同じ")
in_text("(a) を、足す順を変えて出し直します", "例題4 の検算が独立している")
in_text("(b) は (a) の符号を変えただけなので、(a) が間違っていても $\\mathbf{0}$ になります",
        "circular な検算を否定している")
# circular であることの確認
wrong_res = vec(350, 1150)
same(wrong_res + (-wrong_res), vec(0, 0), "誤答でも (a)+(b)=0 は成り立ってしまう")

# ══════════════════════════════════════════════════════════
# 3. 演習の数値
# ══════════════════════════════════════════════════════════
# 1: a=(5,2), b=(-1,4)
e1a, e1b = vec(5, 2), vec(-1, 4)
same(e1a + e1b, vec(4, 6), "演習1 a+b")
same(e1a - e1b, vec(6, -2), "演習1 a-b")
same((e1a + e1b) + (e1a - e1b), 2 * e1a, "演習1 の検算の等式")
chk(sp.simplify((vec(4, 6) + vec(6, 0)) - 2 * e1a) != sp.zeros(2, 1),
    "演習1 の検算は片方の誤りを捕まえる")

# 2: u = 3i+7j, v = 2i-5j
u, vv = vec(3, 7), vec(2, -5)
same(u + vv, vec(5, 2), "演習2 u+v")
same(4 * u - vv, vec(10, 33), "演習2 4u-v")
chk(28 - (-5) == 33, "演習2 の山場 28-(-5)")
same((4 * u - vv) + vv, 4 * u, "演習2 の検算の等式")
# 23 と誤った答えを捕まえるか
chk(23 - 5 != 28, "演習2 の検算は 23 の誤りを捕まえる")
in_text("$28-(-5)$ を $23$ としていたら、$23-5 = 18$ になって $28$ に戻りません",
        "演習2 の検算が誤りを名指ししている")
not_in_text("列ベクトルでやり直します。$4\\begin{pmatrix} 3 \\\\ 7 \\end{pmatrix}",
            "同じ計算を書き直すだけの古い検算")

# 3: a = (2,-3)
e3 = vec(2, -3)
same(5 * e3, vec(10, -15), "演習3 5a")
same(-2 * e3, vec(-4, 6), "演習3 -2a")
chk(sp.Rational(10, 2) == 5 and sp.Rational(-15, -3) == 5, "演習3 の比の検算")
# 成分を1つしか掛けない誤り (10,-3) は比が食い違う
chk(sp.Rational(10, 2) != sp.Rational(-3, -3), "演習3 の検算は掛け忘れを捕まえる")

# 4: 3 次元 a=(1,-2,4), b=(3,0,-1)
e4a, e4b = vec(1, -2, 4), vec(3, 0, -1)
same(e4a + e4b, vec(4, -2, 3), "演習4 a+b")
same(2 * e4a - e4b, vec(-1, -4, 9), "演習4 2a-b")
chk(8 - (-1) == 9, "演習4 の山場 8-(-1)")
same((2 * e4a - e4b) + e4b, 2 * e4a, "演習4 の検算の等式")
# 3 つ目を 7 と誤った答えを捕まえるか
wrong4 = vec(-1, -4, 7)
chk(sp.simplify((wrong4 + e4b) - 2 * e4a) != sp.zeros(3, 1),
    "演習4 の検算は 3 つ目の誤りを捕まえる")
chk((wrong4 + e4b)[1] == (2 * e4a)[1],
    "古い検算（2 つ目の成分を見る）ではこの誤りを捕まえられない")
in_text("危ないのは $3$ つ目なので", "演習4 の検算が正しい成分を見ている")
not_in_text("$\\mathbf{b}$ の $2$ つ目の成分は $0$ なので、$\\mathbf{a}+\\mathbf{b}$ と",
            "0 の成分を見る古い検算")

# 5: (4,-6) と (-10,15), k = -2/5
e5a, e5b = vec(4, -6), vec(-10, 15)
k5 = sp.Rational(-2, 5)
same(k5 * e5b, e5a, "演習5 の k")

# 6: (t,6) が (2,-3) と平行 → t = -4
t = sp.Symbol("t")
sol = sp.solve(sp.Eq(t * (-3) - 6 * 2, 0), t)
chk(sol == [-4], "演習6 t = -4")
same(vec(-4, 6), -2 * vec(2, -3), "演習6 の k = -2")
chk(sp.Rational(4, 2) != sp.Rational(6, -3), "t=4 なら比が食い違う（検算が効く）")

# 7: a=(3,-5) のとき a+b=0 → b=(-3,5)
e7a = vec(3, -5)
same(-e7a, vec(-3, 5), "演習7 b")
same(e7a + (-e7a), vec(0, 0), "演習7 の検算")
chk(sp.simplify((e7a + vec(-3, -5)) - sp.zeros(2, 1)) != sp.zeros(2, 1),
    "演習7 の検算は符号ミスを捕まえる")

# 9: (420,-160) + (-90,530)
e9 = vec(420, -160) + vec(-90, 530)
same(e9, vec(330, 370), "演習9 resultant")
same(e9 - vec(420, -160), vec(-90, 530), "演習9 の検算（逆算）")
# 南北の符号を取りちがえた誤答を捕まえるか
wrong9 = vec(330, -690)
chk(sp.simplify((wrong9 - vec(420, -160)) - vec(-90, 530)) != sp.zeros(2, 1),
    "演習9 の検算は符号ミスを捕まえる")
in_text("答えから $1$ 本目を引くと、$2$ 本目に戻るはずです", "演習9 の検算が逆算になっている")
not_in_text("東西と南北を別々に足し直します", "同じ足し算を繰り返すだけの古い検算")

# 10: 3a、a=(2,-5) → (6,-15)。生徒の誤答は (6,-5)
e10 = vec(2, -5)
same(3 * e10, vec(6, -15), "演習10 正しい 3a")
chk(sp.Rational(6, 2) == 3 and sp.Rational(-15, -5) == 3, "正答の比はそろう")
chk(sp.Rational(6, 2) != sp.Rational(-5, -5), "誤答 (6,-5) の比はそろわない")

# ══════════════════════════════════════════════════════════
# 4. 条件の付け方（平行・零ベクトル・スカラー倍）
# ══════════════════════════════════════════════════════════
in_text("**ここから、平行の判定が出ます。$\\mathbf{a} \\neq \\mathbf{0}$、"
        "$\\mathbf{b} \\neq \\mathbf{0}$ のとき**、次が成り立ちます。",
        "平行の同値式に a≠0, b≠0 が付いている")
not_in_text("**ここから、平行の判定が出ます。**\n\n$$", "条件のない古い導入")
in_text("**向きは $k$ の符号で決まります（$k \\neq 0$ のとき）。**",
        "k=0 を除いてある")
in_text("| $k = 1$ | $\\mathbf{a}$ と同じ | 変わらない |", "表に k=1 の行がある")
in_text("| $k = 0$ | 向きがなくなる | $0$ になる", "k=0 の行の「長さ」は数の 0")
not_in_text("| $k = 0$ | 向きがなくなる | $\\mathbf{0}$ になる",
            "長さの欄にベクトルを書いた古い行")
in_text("## 平行の判定は、$0$ の成分がなければ「比が同じか」で見ます",
        "見出しに条件が付いている")
not_in_text("## 平行の判定は「成分の比が同じか」で見ます", "無条件の古い見出し")
in_text("**平行の判定も同じ**です。$3$ つの比がそろえば平行——ただし $0$ の成分があるときは",
        "3 次元でも 0 成分の但し書きがある")
not_in_text("**平行の判定も同じで、$3$ つの比がそろえば平行**です。", "無条件の古い断定")
# 表の行が k>1, k=1, 0<k<1, k<0, k=0 の 5 行
tbl = TEXT.split(": $k\\mathbf{a}$ の見え方")[0].split("| $k$ | 向き | 長さ |")[1]
chk(len([l for l in tbl.split("\n") if l.startswith("| $")]) == 5,
    "スカラー倍の表は 5 行")

# 零ベクトルは向きを持たない、と書いてある
in_text("**長さが $0$ なので、向きがありません。**", "零ベクトルに向きがない")
in_text("**「$\\mathbf{0}$ はすべてのベクトルと平行」とする流儀もありますが、"
        "AI HL でそこを問われることはありません。**", "k=0 の扱いを明示")

# ══════════════════════════════════════════════════════════
# 5. base vectors の次元（2 次元の式に 3 成分の i, j を使わない）
# ══════════════════════════════════════════════════════════
in_text("$2$ 次元では、$2$ つです。", "2 次元の基本ベクトルを先に出す")
in_text("\\mathbf{i} = \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix}, \\qquad "
        "\\mathbf{j} = \\begin{pmatrix} 0 \\\\ 1 \\end{pmatrix}\n$$ {#eq-ahl310a-base}",
        "2 次元版が eq-ahl310a-base")
in_text("$$ {#eq-ahl310a-base3}", "3 次元版は別の式番号")
# 4i+3j は 2 次元の基本ベクトルで (4,3) になる
same(4 * vec(1, 0) + 3 * vec(0, 1), vec(4, 3), "2 次元の i, j で (4,3)")
# 約束していないことを約束しない
in_text("初めて出す**例**には $\\mathbf{i}$、$\\mathbf{j}$、$\\mathbf{k}$ の形も並べます",
        "「式」ではなく「例」と書いている")
not_in_text("初めて出す式には $\\mathbf{i}$、$\\mathbf{j}$、$\\mathbf{k}$ の形も並べます",
            "守れていない古い約束")

# ══════════════════════════════════════════════════════════
# 6. シラバス・公式集の記述
# ══════════════════════════════════════════════════════════
in_text("AHL 3.10 の Content 欄は $7$ 行あります。このページはそのうち $5$ 行を扱います。",
        "Content 7 行のうち 5 行")
for row in ["> Concept of a vector and a scalar.",
            "> Representation of vectors using directed line segments.",
            "> Unit vectors; base vectors $\\mathbf{i}$, $\\mathbf{j}$, $\\mathbf{k}$.",
            "> The zero vector $\\mathbf{0}$, the vector $-\\mathbf{v}$."]:
    in_text(row, "Content の逐語引用")
in_text("The resultant as the sum of two or more vectors.", "Guidance の逐語引用")
in_text("AHL Topic 3 全体の Recommended teaching hours は $28$ 時間です。",
        "28 時間")
in_text("**$1$ 行だけです。**", "公式集 AHL 3.10 は 1 行")
in_text("**このページで扱うこと——成分の書き方、和と差、スカラー倍——は、公式集にありません。**",
        "公式集にないものを明示")
in_text("**ベクトルは $1$ 度も出てきません。**", "AI SL にベクトルがないこと")
# 公式集にある式を「覚えろ」と言っていない
chk("暗記" not in TEXT or "暗記は問われません" in TEXT, "暗記を求めていない")

# ══════════════════════════════════════════════════════════
# 7. 用語の順序・言い回し・採点についての断定
# ══════════════════════════════════════════════════════════
in_text("| speed（速さ）$60$ km/h | velocity（速度）「東へ $60$ km/h」 |",
        "表でも英語→日本語の順")
in_text("| 質量 $3$ kg | force（力）「下向きに $30$ N」 |", "force も英語が先")
not_in_text("| 速さ（speed）$60$ km/h", "日本語が先の古い書き方")
in_text("採点者に、スカラーの計算をしているように読まれかねません。", "採点についての断定を避ける")
not_in_text("採点者は、ベクトルとスカラーを取りちがえた答案として読みます。",
            "根拠のない採点の断定")
in_text("（演習 $4$、演習 $10$）", "3 次元の注意が演習 4 も指している")
not_in_text("**書き写すときに $1$ つ落とさない**でください（演習 $10$）。",
            "2 次元の演習だけを指した古い参照")
in_text("各問題に、折りたたみが $3$ つ付いています。", "数字は $ $ の中")

# ══════════════════════════════════════════════════════════
# 8. GDC（TI-Nspire CX II、非 CAS）
# ══════════════════════════════════════════════════════════
for claim in ["[3;-1]", "`ctrl`", "`var`", "menu → Actions → Clear a-z"]:
    in_text(claim, "GDC の記述")
for cas_only in ["unitV(", "norm(", "solve("]:
    chk(cas_only not in TEXT, "非 CAS で確認できていない関数を使っていない: " + cas_only)
in_text("`sto` というキーはありません", "存在しない sto キーがないことを書いている")
chk(len(re.findall(r"`sto`", TEXT)) == 1, "sto は「無い」と書く 1 か所だけ")

# ══════════════════════════════════════════════════════════
# 9. 体裁の不変量
# ══════════════════════════════════════════════════════════
chk(len(re.findall(r"(?m)^---\s*$", TEXT)) == 6, "--- は front matter 2 + 例題 4")
chk(TEXT.count('<details class="jp-trans"') == 14, "日本語訳の折りたたみが 14")
chk(TEXT.count(".ex-sep") == 9, "演習の区切りが 9")
chk(TEXT.count("model-answer") == 6, "model-answer が 6")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) ==
    [str(i) for i in range(1, 11)], "演習の番号が 1..10")
chk(len(re.findall(r"(?m)^::: \{#exm-ahl310a-", TEXT)) +
    len(re.findall(r"(?m)^:::: \{#exm-ahl310a-", TEXT)) == 4, "例題が 4 つ")
ideas = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(ideas == [str(i) for i in range(1, 10)] + [str(i) for i in range(1, 6)],
    "The idea 1..9 と GDC 1..5 の連番: " + ",".join(ideas))
heads = re.findall(r"(?m)^## (.*)", TEXT)
order = [h for h in heads if h in ("What you should be able to do", "The idea",
                                   "Why it works", "Worked examples",
                                   "Common errors",
                                   "Using your GDC (TI-Nspire CX II)",
                                   "Exercises")]
chk(order == ["What you should be able to do", "The idea", "Why it works",
              "Worked examples", "Common errors",
              "Using your GDC (TI-Nspire CX II)", "Exercises"],
    "7 つの見出しの順序")
chk(TEXT.count("**検算。**") == 13, "検算が 13 か所: %d" % TEXT.count("**検算。**"))
chk("確かめます。" not in TEXT, "「確かめます。」を使っていない")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前", "そのとおり"]:
    chk(w not in TEXT, "禁止語を使っていない: " + w)
# コードスパンの中に数式を入れない
for m in re.finditer(r"`[^`\n]*`", TEXT):
    chk("$" not in m.group(0), "コードスパンの中の数式 :: " + m.group(0)[:60])
# 表のセルの中の |
for line in TEXT.split("\n"):
    if line.startswith("|") and "$" in line:
        for mm in re.finditer(r"\$[^$]*\$", line):
            chk("|" not in mm.group(0), "表のセルの数式の中の | :: " + line[:60])
chk(TEXT.count("\\left") == TEXT.count("\\right"), "\\left と \\right の対応")
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
# 参照先がすべて定義されている / 定義したものはすべて使われている
defined = set(re.findall(r"\{#([a-zA-Z0-9\-]+)[ }]", TEXT))
atrefs = set(re.findall(r"@((?:eq|fig|tbl|exm)-[a-zA-Z0-9\-]+)", TEXT))
links = set(re.findall(r"\]\(#([a-zA-Z0-9\-]+)\)", TEXT))
chk(not (atrefs - defined), "未定義の @ 参照: %s" % sorted(atrefs - defined))
chk(not (links - defined - {"why-it-works"}),
    "未定義のリンク先: %s" % sorted(links - defined - {"why-it-works"}))
unused = sorted(d for d in defined
                if d.split("-")[0] in ("eq", "fig", "tbl", "exm")
                and d not in atrefs and d not in links)
chk(not unused, "使われていない番号: %s" % unused)
# 図が 3 枚あり、ファイルが存在する
IMG = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry", "img")
for name in ["ahl-3-10a-components.svg", "ahl-3-10a-addsub.svg",
             "ahl-3-10a-scalar.svg"]:
    chk(os.path.exists(os.path.join(IMG, name)), "図がある: " + name)
    chk("img/" + name in TEXT, "図を本文で使っている: " + name)

# ══════════════════════════════════════════════════════════
# 10. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-10a.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-9.qmd") < DRAFT.index("ahl-3-10a.qmd")
    < DRAFT.index("ahl-3-14.qmd"), "サイドバーの並びが 3.9 → 3.10a → 3.14")
PUB = open(os.path.join(HERE, "..", "..", "_quarto.yml"), encoding="utf-8").read()
chk("ahl-3-10a" not in PUB, "公開用の _quarto.yml は SL だけのまま")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.10a — Vectors: the basics](03-geometry-and-trigonometry/ahl-3-10a.qmd)"
    in IDX, "index の一覧にある")
chk("| **AHL 3.10** | **[Vectors: the basics]"
    "(03-geometry-and-trigonometry/ahl-3-10a.qmd)** ／ "
    "**[Magnitude, position and unit vectors]"
    "(03-geometry-and-trigonometry/ahl-3-10b.qmd)** ✅ |" in IDX,
    "index の表が、前半・後半そろって ✅ になっている")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([r for r in _rows if "\u2705" not in r]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| vector |", "| directed line segment |", "| component（ベクトルの） |",
             "| column representation |", "| base vectors |", "| zero vector |",
             "| scalar multiple |", "| parallel（ベクトルが） |", "| resultant |",
             "| speed |", "| velocity |", "| force |", "| in the form |"]:
    chk(term in GLO, "対訳表にある: " + term)
chk("行列に掛けるとき（AHL 3.9）も、ベクトルに掛けるとき（AHL 3.10）も" in GLO,
    "scalar の行が行列だけの説明になっていない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
