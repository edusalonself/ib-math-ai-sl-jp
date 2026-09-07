"""AHL 3.7（弧度法）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_7.py
"""
import os
import re
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry",
                   "ahl-3-7.qmd")
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


PI = sp.pi
D2R = lambda d: sp.nsimplify(d) * PI / 180          # noqa: E731
R2D = lambda r: r * 180 / PI                        # noqa: E731

# ══════════════════════════════════════════════════════════
# 1. radian の定義と一周
# ══════════════════════════════════════════════════════════
# 円周 2πr に半径 r は 2π 本ぶん入る
near(float(2 * sp.pi), 6.283185, msg="一周は 2π = 6.283 radians")
near(float(2 * sp.pi) - 6, 0.283185, msg="6 本ぶんのあとに 0.28 残る")
in_text("$0.28$ 個ぶんです", "図(b) の余り")
near(float(R2D(1)), 57.29578, msg="1 rad = 57.2958 度")
chk(round(float(R2D(1)), 1) == 57.3, "1 rad は 1 d.p. で 57.3 度")
# ★ レビュー5: 57.3 は近似なので = ではなく約 / \approx
in_text("$1$ radian は約 $57.3^{\\circ}$ です", "近似であることを明示")
in_text("**$1$ radian $\\approx 57.3^{\\circ}$ を覚えておくと", "レビュー5: = ではない")
not_in_text("**$1$ radian $= 57.3^{\\circ}$ を覚えておくと", "レビュー5")

# ══════════════════════════════════════════════════════════
# 2. 換算
# ══════════════════════════════════════════════════════════
near(float(PI / 180), 0.0174533, msg="度→ラジアンの係数 π/180")
near(float(180 / PI), 57.29578, msg="ラジアン→度の係数 180/π")
in_text("$\\dfrac{\\pi}{180} \\approx 0.0175$")
in_text("$\\dfrac{180}{\\pi} \\approx 57.3$")
# 向きの確認（60 度 → 1.05 / 逆にかけると 3438）
near(float(D2R(60)), 1.047198, msg="60 度 = 1.0472")
chk(round(float(D2R(60)), 2) == 1.05, "60 度は 2 d.p. で 1.05")
# ★ レビュー4: 60 * 180/π = 3437.7467… なので四捨五入は 3438
near(60 * float(180 / PI), 3437.7468, tol=5e-3, msg="60×180/π")
chk(round(60 * float(180 / PI)) == 3438, "3437 ではなく 3438")
in_text("$3438$ になったら、逆をかけています。", "レビュー4")
not_in_text("$3437$ になったら", "レビュー4")
# Common errors 側の 45 度は 2578
near(45 * float(180 / PI), 2578.3100, tol=5e-3, msg="45×180/π")
chk(round(45 * float(180 / PI)) == 2578, "45 度で逆にかけると 2578")
near(float(D2R(45)), 0.785398, msg="45 度 = 0.7854")
in_text("$45^{\\circ}$ が $0.785$ になれば正しく、$2578$ になったら逆です。")

# 変換表（4 s.f.）
TABLE = [(30, "\\dfrac{\\pi}{6}", PI / 6, "0.5236"),
         (45, "\\dfrac{\\pi}{4}", PI / 4, "0.7854"),
         (60, "\\dfrac{\\pi}{3}", PI / 3, "1.047"),
         (90, "\\dfrac{\\pi}{2}", PI / 2, "1.571"),
         (120, "\\dfrac{2\\pi}{3}", 2 * PI / 3, "2.094"),
         (180, "\\pi", PI, "3.142"),
         (270, "\\dfrac{3\\pi}{2}", 3 * PI / 2, "4.712"),
         (360, "2\\pi", 2 * PI, "6.283")]
for deg, frac, val_sym, dec in TABLE:
    val = float(D2R(deg))
    chk(f"{val:.4g}" == dec, f"{deg} 度の 4 s.f.: {val:.6f} → {dec}")
    in_text(f"| ${deg}^{{\\circ}}$ | ${frac}$ | ${dec}$ |", f"{deg} 度の行")
    # 表に書いた π の形が、本当にその角か
    chk(sp.simplify(val_sym - D2R(deg)) == 0, f"{deg} 度の π 表記")

# ══════════════════════════════════════════════════════════
# 3. 例題 1 — 換算
# ══════════════════════════════════════════════════════════
chk(sp.Rational(144, 180) == sp.Rational(4, 5), "144/180 = 4/5")
chk(sp.gcd(144, 180) == 36, "144 と 180 の最大公約数は 36")
near(float(D2R(144)), 2.5132741, msg="4π/5 = 2.5133")
chk(float(D2R(144)) < float(sp.pi), "144 度は π より小さい")
in_text("$\\dfrac{4\\pi}{5} = 2.513\\ldots$")
near(2.4 * float(180 / PI), 137.50988, tol=5e-4, msg="2.4 rad = 137.51 度")
chk(round(2.4 * float(180 / PI), 1) == 137.5, "1 d.p. で 137.5")
near(float(432 / PI), 137.50988, tol=5e-4, msg="432/π")
chk(2.4 * 180 == 432, "2.4×180 = 432")
chk(float(sp.pi / 2) < 2.4 < float(sp.pi), "2.4 は π/2 と π のあいだ")
in_text("$2.4 \\times \\frac{180}{\\pi} = 137.5^{\\circ}$")
in_text("$$\\frac{180}{\\pi} = 57.3^{\\circ}$$")

# ══════════════════════════════════════════════════════════
# 4. 例題 2 — 扇形（r = 9, θ = 1.2）
# ══════════════════════════════════════════════════════════
r, th = 9, 1.2
near(r * th, 10.8, msg="l = 9×1.2")
near(0.5 * r ** 2 * th, 48.6, msg="A = ½·81·1.2")
near(r * th + 2 * r, 28.8, msg="perimeter = 10.8 + 18")
chk(r ** 2 == 81, "9² = 81")
# 「½ を先にかける」誤りとの区別
near((0.5 * r) ** 2 * th, 24.3, msg="誤った順序では 24.3（＝正解ではない）")
chk(abs((0.5 * r) ** 2 * th - 0.5 * r ** 2 * th) > 1, "順序の誤りは検出できる差になる")
near(0.5 * 9 ** 2, 40.5, msg="½×9² = 40.5")
near((0.5 * 9) ** 2, 20.25, msg="(½×9)² = 20.25")
in_text("$\\dfrac{1}{2} \\times 9^{2}$ は $40.5$ ですが、$\\left(\\dfrac{1}{2} \\times 9\\right)^{2} = 20.25$ です。")
# 割合による検算
frac12 = th / (2 * np.pi)
near(frac12, 0.190986, msg="1.2 は一周の 19.1%")
chk(round(frac12 * 100) == 19, "約 19%")
near(2 * np.pi * 9, 56.5487, tol=5e-3, msg="円周 = 56.5")
near(np.pi * 81, 254.469, tol=5e-3, msg="円の面積 = 254.5")
near(56.5 * 0.191, 10.8, tol=0.02, msg="56.5×0.191 ≈ 10.8")
near(254.5 * 0.191, 48.6, tol=0.05, msg="254.5×0.191 ≈ 48.6")

# ══════════════════════════════════════════════════════════
# 5. 例題 3 — 逆向き（l = 15, r = 6）
# ══════════════════════════════════════════════════════════
near(15 / 6, 2.5, msg="θ = l/r = 2.5")
near(2.5 * float(180 / PI), 143.2394, tol=5e-4, msg="2.5 rad = 143.2394 度")
chk(round(2.5 * float(180 / PI), 1) == 143.2, "1 d.p. で 143.2")
near(0.5 * 36 * 2.5, 45, msg="A = ½·36·2.5 = 45")
near(0.5 * 15 * 6, 45, msg="½lr = 45（l が与えられているので別の道）")
# 度を入れてしまった場合
near(0.5 * 36 * 143.2, 2577.6, tol=1e-6, msg="度を入れると 2577.6")
near(np.pi * 36, 113.0973, tol=5e-4, msg="円全体は 113 cm²")
chk(0.5 * 36 * 143.2 > np.pi * 36, "2577.6 は円全体を超える → 誤りと分かる")
in_text("$2577.6$ という値が出ます。")
in_text("**円全体の面積は $\\pi(36) = 113$ cm² しかありません。**")

# ══════════════════════════════════════════════════════════
# 6. 例題 4 — スプリンクラー（r = 8, θ = 2.1）
# ══════════════════════════════════════════════════════════
near(0.5 * 64 * 2.1, 67.2, msg="A = 67.2 m²")
near(8 * 2.1, 16.8, msg="l = 16.8 m")
near(0.5 * 256 * 2.1, 268.8, msg="r を 2 倍にすると 268.8 m²")
near(268.8 / 67.2, 4, msg="面積は 4 倍（2 倍ではない）")
chk(16 ** 2 == 256 and 8 ** 2 == 64, "8²=64, 16²=256")
# 角を 2 倍にすると面積も 2 倍（比例）
near(0.5 * 64 * 4.2 / (0.5 * 64 * 2.1), 2, msg="θ を 2 倍にすると面積は 2 倍")
in_text("**$2$ 倍ではなく $4$ 倍**です。")
in_text("Doubling the **angle** instead would double the area, because $A$ is proportional to $\\theta$.")

# ══════════════════════════════════════════════════════════
# 7. Common errors の数値
# ══════════════════════════════════════════════════════════
near(0.5 * 36 * 50, 900, msg="50 をそのまま入れると 900")
near(float(D2R(50)), 0.8726646, msg="50 度 = 0.87266 rad")
chk(f"{float(D2R(50)):.4g}" == "0.8727", "50 度は 4 s.f. で 0.8727")
near(0.5 * 36 * float(D2R(50)), 15.70796, tol=5e-4, msg="正しい面積 15.708")
chk(sf(0.5 * 36 * float(D2R(50)), 3) == 15.7, "3 s.f. で 15.7")
chk(900 > np.pi * 36, "900 は円全体 113 を超える")
near(50 / 360 * 100, 13.888, tol=5e-3, msg="50/360 = 13.9%")
near(113 * 0.139, 15.707, tol=0.01, msg="113×0.139 ≈ 15.7")

# ══════════════════════════════════════════════════════════
# 8. 演習 1..10
# ══════════════════════════════════════════════════════════
# 1) 75 度
chk(sp.Rational(75, 180) == sp.Rational(5, 12), "75/180 = 5/12")
chk(sp.gcd(75, 180) == 15, "75 と 180 の最大公約数は 15")
near(float(D2R(75)), 1.3089969, msg="5π/12 = 1.30900")
chk(sf(float(D2R(75)), 3) == 1.31, "3 s.f. で 1.31")
chk(float(D2R(60)) < float(D2R(75)) < float(D2R(90)), "1.047 < 1.31 < 1.571")
# 2) 3.7 rad
near(3.7 * float(180 / PI), 211.99437, tol=5e-4, msg="3.7 rad = 211.994 度")
chk(round(3.7 * float(180 / PI)) == 212, "最も近い整数は 212")
chk(float(sp.pi) < 3.7 < float(3 * sp.pi / 2), "3.7 は π と 3π/2 のあいだ")
near(57.3 * 3.7, 212.01, tol=0.02, msg="57.3×3.7 ≈ 212")
# 3) r = 14, θ = 0.85
near(14 * 0.85, 11.9, msg="l = 11.9")
near(0.5 * 196 * 0.85, 83.3, msg="A = 83.3")
chk(14 ** 2 == 196, "14² = 196")
near(0.5 * 11.9 * 14, 83.3, msg="½lr = 83.3")
near(np.pi * 196, 615.752, tol=5e-3, msg="円全体 615.8")
near(83.3 / (np.pi * 196) * 100, 13.528, tol=5e-2, msg="83.3 は 13.5%")
near(0.85 / (2 * np.pi) * 100, 13.528, tol=5e-3, msg="0.85/2π = 13.5%")
# ★ レビュー3: ½lr は l = rθ の書き直しなので独立ではない
in_text("**この検算で見つかるのは $\\dfrac{1}{2}$ の落としや打ち間違い**です。", "レビュー3")
not_in_text("$83.3$ ✓ 別の道でも同じ値です。", "レビュー3")
# 4) l = 24, θ = 1.6
near(24 / 1.6, 15, msg="r = 15")
near(15 * 1.6, 24, msg="検算 15×1.6 = 24")
chk(24 > 15, "θ > 1 なので弧のほうが長い")
# 5) r = 10, A = 50
near(0.5 * 100, 50, msg="½·10² = 50")
near(50 / 50, 1, msg="θ = 1 radian")
near(0.5 * 10 * 10, 50, msg="½lr = 50")
# 6) r = 7, θ = 1.5
near(7 * 1.5, 10.5, msg="l = 10.5")
near(10.5 + 14, 24.5, msg="perimeter = 24.5")
chk(10.5 < 14, "θ < 2 なので弧は 2r より短い")
# ★ レビュー1: 周そのものを判定する検算が要る（弧だけで止めた 10.5 を落とす）
chk(24.5 > 14 and not (10.5 > 14),
    "『周は 14 より大きい』は 10.5 を落とす検算になっている")
in_text("そして**周は、その弧に $14$ を足したもの**ですから、$14$ より大きくなるはずです。$24.5 > 14$ ✓",
        "レビュー1")
in_text("弧だけで止めた $10.5$ は、この $2$ つ目で落ちます。", "レビュー1")
near(7 * 2, 14, msg="θ = 2 なら弧 = 2r")
# 7) r = 12, 40 度
chk(sp.Rational(40, 180) == sp.Rational(2, 9), "40/180 = 2/9")
near(float(D2R(40)), 0.6981317, msg="2π/9 = 0.698132")
near(0.5 * 144 * float(D2R(40)), 50.26548, tol=5e-4, msg="A = 50.265")
chk(sf(0.5 * 144 * float(D2R(40)), 3) == 50.3, "3 s.f. で 50.3")
near(0.5 * 144 * 0.698, 50.256, tol=5e-3, msg="0.698 で丸めると 50.256")
chk(sf(0.5 * 144 * 0.698, 3) == 50.3, "3 s.f. では同じ 50.3")
near(40 / 360 * np.pi * 144, 50.26548, tol=5e-4, msg="度の式でも 50.265")
near(40 / 360 * np.pi * 144 - 0.5 * 144 * float(D2R(40)), 0,
     msg="2 組の式は完全に一致する")
# 8) Explain why — r = 10, θ = 90 度
near(90 / 360 * 2 * np.pi * 10, 15.70796, tol=5e-4, msg="正しい弧 15.7")
near(10 * 90, 900, msg="rθ に度を入れると 900")
near(2 * np.pi * 10, 62.8319, tol=5e-3, msg="円周 62.8")
chk(900 > 2 * np.pi * 10, "900 は円周を超える")
in_text("**円周の $62.8$ より大きい**ので、これが弧の長さでないことは、値を見ただけで分かります。")
# 9) 振り子 r = 0.75, θ = 0.3
near(0.75 * 0.3, 0.225, msg="l = 0.225 m")
near(1.5 * 0.3, 0.45, msg="2 倍にすると 0.45 m")
near(0.225 * 100, 22.5, msg="22.5 cm")
chk(abs(1.5 * 0.3 / (0.75 * 0.3) - 2) < 1e-12, "弧は r に比例（2 倍）")
chk(abs(0.5 * 1.5 ** 2 * 0.3 / (0.5 * 0.75 ** 2 * 0.3) - 4) < 1e-12,
    "面積なら 4 倍（弧とは違う）")
# 10) Identify the error
near(0.5 * 36 * float(D2R(50)), 15.70796, tol=5e-4, msg="正しくは 15.7 cm²")
chk(sf(0.5 * 36 * float(D2R(50)), 3) == 15.7, "3 s.f. で 15.7")
near(np.pi * 6 ** 2, 113.0973, tol=5e-4, msg="円全体 113")
chk(round(np.pi * 36) == 113, "π(6)² は 113")

# ══════════════════════════════════════════════════════════
# 9. Why it works の代数
# ══════════════════════════════════════════════════════════
t, R = sp.symbols("theta r", positive=True)
chk(sp.simplify(t / (2 * sp.pi) * 2 * sp.pi * R - R * t) == 0, "l = rθ の導出")
chk(sp.simplify(t / (2 * sp.pi) * sp.pi * R ** 2 - R ** 2 * t / 2) == 0,
    "A = ½r²θ の導出")
chk(sp.simplify(R ** 2 * t / 2 - (R * t) * R / 2) == 0, "½r²θ = ½lr")
# 小さい θ での三角形近似（覚え方であって証明ではない、と本文で断っている）
chk(sp.limit((R ** 2 * sp.sin(t) / 2) / (R ** 2 * t / 2), t, 0) == 1,
    "θ→0 で扇形は三角形に近づく")
in_text("**これは覚え方であって、証明ではありません。**")

# ══════════════════════════════════════════════════════════
# 10. 逆向きの表
# ══════════════════════════════════════════════════════════
in_text("| $l$ と $r$ | $\\theta$ | $\\theta = \\dfrac{l}{r}$ |")
in_text("| $l$ と $\\theta$ | $r$ | $r = \\dfrac{l}{\\theta}$ |")
in_text("| $A$ と $r$ | $\\theta$ | $\\theta = \\dfrac{2A}{r^{2}}$ |")
in_text("| $A$ と $\\theta$ | $r$ | $r = \\sqrt{\\dfrac{2A}{\\theta}}$ |")
chk(sp.solve(sp.Eq(R ** 2 * t / 2, sp.Symbol("A", positive=True)), t)[0]
    == 2 * sp.Symbol("A", positive=True) / R ** 2, "θ = 2A/r²")

# ══════════════════════════════════════════════════════════
# 11. 公式集・シラバスの引用
# ══════════════════════════════════════════════════════════
in_text("l = r\\theta \\quad (\\text{arc length}), \\qquad A = \\frac{1}{2}r^{2}\\theta")
in_text("> where $r$ is the radius, $\\theta$ is the angle measured in radians",
        "断り書きは引用ブロックで")
in_text("いっぽう、**度とラジアンの換算は印刷されていません。**")
in_text("> The definition of a radian and conversion between degrees and radians.")
in_text("> Using radians to calculate area of sector, length of arc.")
in_text("> Radian measure may be expressed as exact multiples of $\\pi$, or decimals.")
in_text("> **Link to:** trigonometric functions (AHL 2.9).")
in_text("> On HL examination papers radian measure should be assumed unless otherwise indicated.")
in_text("Recommended teaching hours は $28$ 時間です")
in_text("> **Links to other subjects:** Diffraction patterns and circular motion (physics)")
in_text("Seki Takakazu calculating $\\pi$ to ten decimal places")
in_text("> **TOK:** Which is the better measure of an angle, degrees or radians?")

# ══════════════════════════════════════════════════════════
# 12. GDC
# ══════════════════════════════════════════════════════════
in_text("doc → Settings → Document Settings")
in_text("`Angle` を **Radian** にします。")
# ★ レビュー2: 144*π/180 は設定によらない
in_text("（かけ算と割り算だけなので、Radian か Degree かの設定には左右されません）",
        "レビュー2")
not_in_text("と打つと、Radian 設定なら", "レビュー2")
in_text("**Numeric（非 CAS）**", "CX II は記号のままでは返さない")
in_text("`ctrl` と `k` を押すとパレットが開く")
near(0.5 * 6 ** 2 * float(D2R(50)), 15.70796, tol=5e-4, msg="0.5*6^2*(50*π/180)")
in_text("$15.708$ が返ります。")
chk("solve(" not in TEXT.replace("nSolve(", ""), "CAS 専用の solve( を使っていない")

# ══════════════════════════════════════════════════════════
# 13. 構造
# ══════════════════════════════════════════════════════════
chk(sum(1 for l in TEXT.split("\n") if l.strip() == "---") == 6,
    "--- は 6 本（front matter 2 + 例題 4）")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳は 14 個")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep は 9 個")
chk(len(re.findall(r"\{#exm-", TEXT)) == 4, "worked example は 4 個")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習は 1..10 の連番")
idea = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(idea == [str(i) for i in range(1, 9)] + [str(i) for i in range(1, 6)],
    "The idea 1..8 と GDC 1..5 の連番: " + str(idea))
chk(TEXT.count("::: {.model-answer}") == 4, "model-answer は 4 個")
for h in ["## What you should be able to do", "## The idea", "## Why it works",
          "## Worked examples", "## Common errors",
          "## Using your GDC (TI-Nspire CX II)", "## Exercises"]:
    in_text(h, "固定見出し")
for cmd in ["Comment on this statement", "Explain why", "Interpret what happens",
            "Identify the error"]:
    in_text(cmd, "command term")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "確かめ。", "そのとおり"]:
    not_in_text(w, "禁止表現")
chk(TEXT.count("**検算。**") == 11, "検算。の個数: " + str(TEXT.count("**検算。**")))
for term in ["**radian**（ラジアン）", "**perimeter**", "扇形の**周**（perimeter）"]:
    pass
in_text("**radian**（ラジアン）", "英語→日本語の順")
in_text("![What a radian is, and why a full turn is $2\\pi$](img/ahl-3-7-radian.svg)")
in_text("![The two formulas, and where they come from](img/ahl-3-7-sector.svg)")
for svg in ["ahl-3-7-radian.svg", "ahl-3-7-sector.svg"]:
    chk(os.path.exists(os.path.join(HERE, "..", "..", "ai-hl",
                                    "03-geometry-and-trigonometry", "img", svg)),
        "図がある: " + svg)
anchors = set(re.findall(r"\{#([a-z0-9-]+)[\s\}]", TEXT)) | {"common-errors",
                                                             "why-it-works"}
for anc in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(anc in anchors, "内部アンカーがない: #" + anc)
refs = set(re.findall(r"@((?:eq|fig|tbl|exm)-[a-z0-9-]+)", TEXT))
for rf in refs:
    chk(rf in anchors, "crossref の先がない: @" + rf)
for a in anchors:
    if re.match(r"(eq|fig|tbl|exm)-", a):
        chk(a in refs, "使われていない crossref アンカー: " + a)
for m in re.findall(r"`[^`\n]*`", TEXT):
    chk("$" not in m, "コードスパンに $ が入っている: " + m[:50])
for line in TEXT.split("\n"):
    if line.startswith("|") and "$" in line:
        inner = re.sub(r"^\||\|$", "", line)
        chk("\\lvert" in line or "|" not in inner.replace(" | ", ""),
            "表のセルの中の | :: " + line[:60])
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
in_text("[SL 3.4](../../ai-sl/03-geometry-and-trigonometry/sl-3-4.qmd#perimeter)")
in_text("[SL 3.4](../../ai-sl/03-geometry-and-trigonometry/sl-3-4.qmd#segment-area)")
in_text("[AHL 2.9a](../02-functions/ahl-2-9a.qmd#radian)")

# 登録されているか
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-7.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-7.qmd") < DRAFT.index("ahl-3-9.qmd"),
    "サイドバーで 3.7 が 3.9 より先")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.7 — Radian measure](03-geometry-and-trigonometry/ahl-3-7.qmd)" in IDX,
    "index の一覧にある")
chk("| **AHL 3.7** | **[Radian measure](03-geometry-and-trigonometry/ahl-3-7.qmd)** ✅ |"
    in IDX, "index の表が ✅ になっている")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([r for r in _rows if "\u2705" not in r]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| radian measure |", "| arc length |", "| area of a sector |",
             "| subtend / subtended at the centre |", "| pendulum |",
             "| sprinkler |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
