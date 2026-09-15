"""AHL 2.10（log-log と semi-log）の内容を検算する。

    python3 figs/ai-hl/check_ahl_2_10.py
"""
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "02-functions", "ahl-2-10.qmd")
TEXT = open(QMD, encoding="utf-8").read()

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def near(a, b, tol=5e-4, msg=""):
    chk(abs(float(a) - float(b)) < tol, msg + f"  ({float(a)} vs {float(b)})")


def sf(v, n=3):
    return float(f"{v:.{n}g}")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


L = np.log10

# ══════════════════════════════════════════════════════════
# 1. 対数目盛りの導入
# ══════════════════════════════════════════════════════════
V = 50 * 8.0 ** np.arange(0, 6)
chk(list(V) == [50, 400, 3200, 25600, 204800, 1638400], "訪問数の列")
near(L(8), 0.903090, msg="log 8 = 0.903")
near(L(V[1]) - L(V[0]), L(8), msg="1 か月ぶんの上がり幅は log 8")
in_text("\\log(8 \\times \\text{前月}) - \\log(\\text{前月}) = \\log 8 = 0.903")
in_text("**はじめの $4$ か月が、軸の上にぺしゃんこに潰れています。**", "レビュー21c")
not_in_text("**最後の $1$ か月しか見えません。**", "レビュー21c: 図と合わない")
# ★ レビュー20: 目盛りの 2 とおり
in_text("## 軸の目盛りには、$2$ とおりの書き方があります", "レビュー20")
in_text("**縦軸に $\\log_{10} y$ と書いてあったら、そこに書かれている数は $y$ ではありません。**",
        "レビュー20")

# ══════════════════════════════════════════════════════════
# 2. 線形化の代数
# ══════════════════════════════════════════════════════════
XE = np.arange(0, 5.0)
YE = 5 * 2.0 ** XE
m, c = np.polyfit(XE, L(YE), 1)
near(m, L(2), msg="semi-log の傾きは log 2")
near(c, L(5), msg="semi-log の切片は log 5")
near(L(2), 0.30103, msg="log 2 = 0.301")
near(L(5), 0.69897, msg="log 5 = 0.699")
XP = np.array([1.0, 2, 3, 4, 5])
YP = 2 * XP ** 3
m2, c2 = np.polyfit(L(XP), L(YP), 1)
near(m2, 3, msg="log-log の傾きは 3")
near(c2, L(2), msg="log-log の切片は log 2")
in_text("- 傾き $= \\log 2 = 0.301$")
# 2026-09: 4 面図を 2 枚に分け、説明のすぐ近くへ移動
in_text("**傾きは $3$、切片は $\\log 2 = 0.301$** です。")
# ★ レビュー8: 条件
in_text("指数の関係 $y = ka^{x}$（$k > 0$、$a > 0$）の両辺の $\\log$ をとります。", "レビュー8")
in_text("累乗の関係 $y = ax^{n}$（$a > 0$、$x > 0$）の両辺の $\\log$ をとります。", "レビュー8")
in_text(": どちらが直線になるか（$x > 0$、$y > 0$、$k > 0$、$a > 0$ のとき）", "レビュー8")
x3 = np.arange(0, 8.0)
r3 = np.corrcoef(x3, L(3 + 2 ** x3))[0, 1]
near(r3, 0.98853, tol=2e-4, msg="y = 3+2^x の semi-log は r = 0.989（直線でない）")
in_text("$y = 3 + 2^{x}$ のように**定数が足されている**式は、$\\log$ を取っても直線になりません",
        "レビュー8")
# ★ レビュー19: 底をそろえる
in_text("$\\log_{10} y$ を $\\ln x$ に対してかくと、傾きは $n$ になりません。", "レビュー19")

# ══════════════════════════════════════════════════════════
# 3. 元に戻す
# ══════════════════════════════════════════════════════════
near(10 ** 0.3, 1.995262, msg="10^0.3 = 2.00")
near(10 ** 1.8, 63.09573, msg="10^1.8 = 63.1")
near(10 ** 0.25, 1.778279, msg="10^0.25 = 1.78")
near(10 ** 0.6, 3.981072, msg="10^0.6 = 3.98")
near(10 ** 1.2, 15.84893, msg="10^1.2 = 15.8")
near(10 ** 0.4, 2.511886, msg="10^0.4 = 2.51")
near(10 ** -0.5, 0.3162278, msg="10^-0.5 = 0.316")
near(10 ** 0.9, 7.943282, msg="10^0.9 = 7.94")
near(10 ** 0.85, 7.079458, msg="10^0.85 = 7.08")
near(np.e ** 3, 20.08554, msg="e^3 = 20.1")
near(np.e ** 0.25, 1.284025, msg="e^0.25 = 1.28")
near(2 ** 0.75, 1.681793, msg="2^0.75 = 1.68")
in_text("**$\\ln$ で取ったなら $e$ で戻す**", "底をそろえる")

# ══════════════════════════════════════════════════════════
# 4. Worked examples
# ══════════════════════════════════════════════════════════
# WE1
near(10 ** 3.3, 1995.2623, tol=1e-3, msg="10^3.3 = 1995.26")
chk(sf(10 ** 3.3) == 2000.0, "3 s.f. は 2000")
in_text("y = 10^{3.3} = 1995.26\\ldots = 2000 \\ (3\\ \\text{s.f.})", "レビュー3")
not_in_text("= 1995.26\\ldots = 1990", "レビュー3: 誤った丸め")
near(63.1 * 1.78 ** 6, 2007.009, tol=1e-2, msg="丸めた値では 2007")
in_text("丸めた $63.1 \\times 1.78^{6}$ で計算すると $2007$ になります。", "レビュー4")
not_in_text("で計算すると $2003$ になります", "レビュー4")
# WE2
near(10 ** (1.5 * L(16) + 0.6), 254.7886, tol=1e-3, msg="WE2 (b) = 255")
near(3.981072 * 16 ** 1.5, 254.7886, tol=1e-3, msg="別の道でも 255")
chk(16 ** 1.5 == 64, "16^1.5 = 64")
# WE3 bacteria
t = np.arange(0, 5.0)
N = np.array([120, 190, 305, 480, 770.0])
mb, cb = np.polyfit(t, L(N), 1)
near(mb, 0.20171, tol=1e-5, msg="bacteria 傾き 0.20171")
near(cb, 2.07857, tol=1e-5, msg="bacteria 切片 2.07857")
near(np.corrcoef(t, L(N))[0, 1], 0.999981, tol=1e-5, msg="bacteria r = 0.99998")
for want, got in zip([2.0792, 2.2788, 2.4843, 2.6812, 2.8865], L(N)):
    near(round(got, 4), want, tol=1e-9, msg="log N の 4 桁")
near(10 ** cb, 119.8318, tol=1e-3, msg="k = 120")
near(10 ** mb, 1.591153, tol=1e-5, msg="a = 1.59")
near(10 ** cb * (10 ** mb) ** 4, 768.09, tol=0.05, msg="t=4 の予測 768.0")
near(119.83 * 1.5911 ** 4, 767.99, tol=0.05, msg="丸めた値でも 768.0")
in_text("$119.83 \\times 1.5911^{4} = 768.0$", "レビュー21a")
not_in_text("1.5911^{4} = 768.1", "レビュー21a")
near(10 ** 2.08, 120.2264, tol=1e-3, msg="丸めた切片では 120.2")
in_text("10^{2.07857} = 119.8, \\qquad 10^{2.08} = 120.2")
# WE4 planets
d = np.array([0.387, 0.723, 1.000, 1.524, 5.203, 9.537])
T = np.array([0.241, 0.615, 1.000, 1.881, 11.86, 29.45])
mp, cp = np.polyfit(L(d), L(T), 1)
near(mp, 1.499634, tol=1e-5, msg="planets 傾き 1.49963")
near(cp, 0.00011445, tol=1e-6, msg="planets 切片 0.000114")
chk(sf(cp) == 0.000114, "切片の 3 s.f. は 0.000114")
near(np.corrcoef(L(d), L(T))[0, 1], 1.0, tol=1e-6, msg="planets r = 1.000")
near(L(19.19), 1.283075, tol=1e-5, msg="log 19.19 = 1.28307")
near(1.49963 * 1.28307 + 0.000114, 1.924244, tol=1e-5, msg="1.92424")
near(10 ** (1.49963 * 1.28307 + 0.000114), 83.993, tol=0.02, msg="T = 84.0")
near(19.19 ** 1.5, 84.0637, tol=1e-3, msg="19.19^1.5 = 84.06")
near(np.corrcoef(d, L(T))[0, 1], 0.93993, tol=1e-4, msg="planets semi-log r = 0.940")
in_text("+ 0.000114", "レビュー1: 正しい切片")
not_in_text("0.000110", "レビュー1: 誤った切片")
not_in_text("1.92434", "レビュー2: 誤った途中値")
not_in_text("1.28308", "レビュー2: 誤った log")
in_text("A semi-log graph of the same data gives only $r = 0.940$", "レビュー17")
not_in_text("rather than an exponential one.*", "レビュー17: 示していない比較")

# ══════════════════════════════════════════════════════════
# 5. Exercises
# ══════════════════════════════════════════════════════════
near(10 ** 1.6, 39.81072, tol=1e-4, msg="演習1 検算 x=1 で 39.8")
near(15.848932 * 2.511886, 39.81072, tol=1e-4, msg="演習1 式でも 39.8")
in_text("**$x = 0$ で確かめても足りません。**", "レビュー11")
not_in_text("**検算。** $x = 0$ を入れます。式では $15.8489$、もとの直線では", "レビュー11")
near(10 ** 1.5, 31.62278, tol=1e-4, msg="演習2 検算 x=10 で 31.6")
near(L(4), 0.60206, msg="演習3 傾き log 4 = 0.602")
near(L(28) - L(7), L(4), msg="演習3 検算")
near(L(0.06) - L(6), -2, msg="演習4 傾き -2")
near(10 ** 0.9 * (10 ** 0.3) ** 8, 1995.262, tol=1e-2, msg="演習5 検算")
# 演習6
x6 = np.array([1.0, 2, 4, 8])
y6 = 3 * x6 ** 2.5
near(y6[3], 543.0584, tol=1e-3, msg="演習6 y の 4 つ目は 543.06")
in_text("| $y$ | $3.00$ | $16.97$ | $96.0$ | $543.06$ |", "レビュー13")
not_in_text("$96.0$ | $543.1$ |", "レビュー13")
for want, got in zip([0.4771, 1.2297, 1.9823, 2.7348], L(y6)):
    near(round(got, 4), want, tol=1e-9, msg="演習6 log y の 4 桁")
near(np.corrcoef(L(x6), L(y6))[0, 1], 1.0, tol=1e-6, msg="演習6 log-log r = 1.000")
near(np.corrcoef(x6, L(y6))[0, 1], 0.95917, tol=1e-4, msg="演習6 semi-log r = 0.959")
near(10 ** 0.4771, 2.99985, tol=1e-3, msg="10^0.4771 = 3.00")
near(0.7526 / 0.3010, 2.50033, tol=1e-3, msg="傾き 2.5")
chk(3 * 4 ** 2.5 == 96, "検算 3*4^2.5 = 96")
in_text("increase by about $0.7526$ each time", "レビュー13")
not_in_text("is exactly a straight line ($r = 1.000$)", "レビュー13")
# 演習8, 9, 10
near(np.e ** 4, 54.59815, tol=1e-3, msg="演習8 検算 e^4 = 54.598")
near(20.0855 * 1.28403 ** 4, 54.598, tol=1e-2, msg="演習8 式でも 54.598")
near(10 ** 2.1, 125.8925, tol=1e-3, msg="演習10 検算 x=1 で 125.9")
in_text("$x = 0$ で $y = 10^{1.8} = 63.1$、$x = 1$ で $y = 10^{2.1} = 125.9$")

# ══════════════════════════════════════════════════════════
# 6. 一般化への条件（レビュー 5・6・7・12）
# ══════════════════════════════════════════════════════════
xa = np.arange(1, 11.0)
ya = xa ** 2 + 40
near(np.corrcoef(xa, L(ya))[0, 1], 0.99676, tol=1e-4, msg="y=x^2+40 semi-log r = 0.997")
near(np.corrcoef(L(xa), L(ya))[0, 1], 0.92473, tol=1e-4, msg="y=x^2+40 log-log r = 0.925")
in_text("$y = x^{2}+40$ のようなデータでは semi-log の $r = 0.997$", "レビュー5")
# ★ 2026-08: 見出しが「r で判定する」と読めないようにした
in_text("## $r$ は、どちらがより直線に近いかを比べる材料です")
not_in_text("## 判定は $r$ の値でします", "r だけで決まると読める見出し")
in_text("- **$\\lvert r \\rvert$ が $1$ に近い** … 変換したあとの点が、直線に近く並んでいる")
in_text("- **それだけでは**、元のデータが本当に exponential model や power model に従うとは**断定できません**")
in_text("- 判断には、**散布図の形、residual（残差）の並び方、文脈、変数の意味**も要ります")
in_text("- このページでは、$r$ を **semi-log と log-log のどちらがより直線に近いかを比べる補助**として使います")
in_text("**実際にはどちらのモデルでもありません。**")
not_in_text("それがこの項目の正しいやり方です。", "レビュー5")
in_text("a negative gradient would mean decay", "レビュー6")
not_in_text("A positive gradient on a semi-log graph always means growth", "レビュー6")
in_text("（縦軸が $\\log_{10} y$ のときの話です。$\\ln y$ なら $e^{m}$ で見ます。）", "レビュー6")
in_text("**まったく同じとはかぎりません。**", "レビュー7")
not_in_text("**答えの式は、どちらでやっても同じ**です。", "レビュー7")
not_in_text("曲線をいきなり当てはめると、その比較ができません。", "レビュー7")
in_text("semi-log で直線 → **一定の割合で増える、または減る**（指数）", "レビュー12")
not_in_text("semi-log で直線 → **一定の割合で増える**（指数）\n", "レビュー12")
in_text("approximately exponential", "レビュー18")
not_in_text("the points lie on a straight line, the growth is exponential", "レビュー18")

# ══════════════════════════════════════════════════════════
# 7. GDC
# ══════════════════════════════════════════════════════════
in_text("ctrl + doc → Add Lists & Spreadsheet")
in_text("menu → Statistics → Stat Calculations → Linear Regression (mx+b)")
in_text("=log(b[])")
in_text("=log(a[])")
# 2026-09: GDC の入力例は画面どおりの表示に変更
in_text(r"10^{\texttt{stat.b}}")
not_in_text("10^(stat.b)")
in_text("## `stat.m` と `stat.b` は、上書きされます", "レビュー16")
in_text("`Display Digits` の設定で決まります。", "レビュー15")
not_in_text("**表示された値をそのまま**写します。列の値は丸められていません。", "レビュー15")
in_text("**log-log では $t = 0$ が使えません。**", "レビュー9")
not_in_text("**$t = 0$ は構いません。** 困るのは、", "レビュー9")
in_text("**(a)** 電卓の $C$ 列に、まとめて出します", "レビュー16b")
not_in_text("電卓の $\\log$ キーで、$1$ つずつ出します", "レビュー16b")
for cas in ["expand(", "factor(", "solve(", "csolve("]:
    not_in_text("`" + cas, "非 CAS では使えない命令 " + cas)

# ══════════════════════════════════════════════════════════
# 8. シラバス・公式集
# ══════════════════════════════════════════════════════════
# 2026-09: 公式が無い欄なので callout ごと削除し、要点を 1 文にして The idea の前へ
not_in_text("## 公式集の AHL 2.10 の欄")
in_text("**このページに、新しい公式はありません。**", "公式が無いことは 1 文で書く")
in_text("Content 欄は $3$ 行です。")
in_text("Guidance 欄には $3$ つあります。")
in_text("Connections 欄には $4$ つ挙がっています。")
in_text("Scaling very large or small numbers using logarithms.")
in_text("In examinations, students will not be expected to draw or sketch these graphs.")
in_text("**対数目盛りのグラフを、自分で描くことは求められません。**")
in_text("**Links to websites:** Gapminder makes use of log-log graphs: www.gapminder.org")
in_text("$10^{\\log x} = x$", "レビュー14: 元に戻すには対数の定義も使う")
not_in_text("**この $2$ つがあれば、このページの中身はすべて出てきます**", "レビュー14")
not_in_text("これが $2$ 番目に多い誤りです", "レビュー22")
not_in_text("ここが試験でいちばん問われるところです", "レビュー22")
not_in_text("試験で問われるのは、**読むこと**と**式に戻すこと**です", "レビュー22")

# ══════════════════════════════════════════════════════════
# 9. 構造
# ══════════════════════════════════════════════════════════
heads = re.findall(r"(?m)^## (.+)$", TEXT)
need = ["What you should be able to do", "The idea", "Why it works",
        "Worked examples", "Common errors",
        "Using your GDC (TI-Nspire CX II)", "Exercises"]
for hh in need:
    chk(hh in heads, "見出しがない: " + hh)
chk([hh for hh in heads if hh in need] == need, "7 つの見出しの順序")
chk(len(re.findall(r"(?m)^---$", TEXT)) == 6, "--- は 6 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳は 14 個")
chk(TEXT.count("::: {.ex-sep}") == 9, ".ex-sep は 9 個")
chk(len(re.findall(r"::: \{#exm-ahl210-[\w-]+\}", TEXT)) == 4, "worked example は 4 個")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習は 1..10 の連番")
idea = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(idea == [str(i) for i in range(1, 9)] + [str(i) for i in range(1, 6)],
    "The idea 1..8 と GDC 1..5 の連番: " + str(idea))
chk(TEXT.count("::: {.model-answer}") == 6, "model-answer は 6 個（レビュー10）")
for cmd in ["State, with a reason", "Interpret what this tells you",
            "Interpret the value of the gradient", "Comment on what the value of $n$",
            "Identify the error", "Interpret the value of $a$"]:
    in_text(cmd, "command term")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "確かめ。", "そのとおり"]:
    not_in_text(w, "禁止表現")
chk(TEXT.count("**検算。**") == 12, "検算。の個数: " + str(TEXT.count("**検算。**")))
for term in ["**semi-log**（片対数）", "**log-log**（両対数）",
             "**linearize**（線形化）", "growth factor（増加倍率）"]:
    in_text(term, "英語→日本語の順")
in_text("![Why a logarithmic scale helps](img/ahl-2-10-scale.svg)")
# 2026-09: 4 面図を 2 枚に分け、説明のすぐ近くへ移動
in_text("![Exponential data comes out straight on a semi-log graph]"
        "(img/ahl-2-10-semilog.svg)")
in_text("![Power data comes out straight on a log-log graph]"
        "(img/ahl-2-10-loglog.svg)")
not_in_text("ahl-2-10-which.svg")
for svg in ["ahl-2-10-semilog.svg", "ahl-2-10-loglog.svg", "ahl-2-10-scale.svg"]:
    chk(os.path.exists(os.path.join(HERE, "..", "..", "ai-hl", "02-functions",
                                    "img", svg)), "図がある: " + svg)
anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT)) | {"common-errors", "why-it-works"}
for anc in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(anc in anchors, "内部アンカーがない: #" + anc)
for m in re.findall(r"`[^`\n]*`", TEXT):
    chk("$" not in m, "コードスパンに $ が入っている: " + m[:50])
for line in TEXT.split("\n"):
    if line.startswith("|") and "$" in line:
        inner = re.sub(r"^\||\|$", "", line)
        chk("\\lvert" in line or "|" not in inner.replace(" | ", ""),
            "表のセルの中の | :: " + line[:60])
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
in_text("[AHL 1.9](../01-number-and-algebra/ahl-1-9.qmd#three-laws)")
in_text("[SL 4.4](../../ai-sl/04-statistics-and-probability/sl-4-4.qmd#gdc-regression)")
in_text("[AHL 4.13](../04-statistics-and-probability/ahl-4-13.qmd#gdc-curve)")


# レビューで追加: GDC の節も「r で決める」と読めないようにした
in_text("### 4. $r$ で、どちらが直線に近いかを比べます {#gdc-r}")
not_in_text("### 4. $r$ で、どちらが直線かを決めます {#gdc-r}")
in_text("- $\\lvert r \\rvert$ が $1$ に近いほう … **そちらのほうが直線に近い**。"
        "モデルの断定は、散布図の形と文脈で裏づけてからです（[第4節](#which)）")
not_in_text("- $\\lvert r \\rvert$ が $1$ に近いほう … そちらの関係")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
