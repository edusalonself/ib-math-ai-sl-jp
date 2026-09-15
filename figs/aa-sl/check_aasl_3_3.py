"""AA SL 3.3（三角法の応用）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_3.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-3.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_3.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational


def D(x):
    return sp.rad(x)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(u - v) == 0, msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def cos_rule(a, b, C):
    return a ** 2 + b ** 2 - 2 * a * b * sp.cos(D(C))


def area(a, b, C):
    return R(1, 2) * a * b * sp.sin(D(C))


def back(b):
    return b + 180 if b < 180 else b - 180


# ══════════════════════════════════════════════════════════
# 0. 本文の走る例と、逆向きの方位角
# ══════════════════════════════════════════════════════════
eq(12 * sp.tan(D(60)), 12 * sp.sqrt(3), "本文 柱の高さ 12√3")
in_text("h = 12\\tan 60° = 12 \\times \\sqrt{3} = 12\\sqrt{3}", "本文の柱の例")
chk(back(210) == 30, "210° の逆は 030°")
chk(back(100) == 280, "100° の逆は 280°")
in_text("$210°$ の逆は $030°$、$100°$ の逆は $280°$ です。", "本文の逆向きの例")
for _b in range(0, 360):
    chk_b = back(_b)
    if not (0 <= chk_b < 360):
        chk(False, f"逆向きが範囲外: {_b}")
chk(True, "逆向きはいつも 0° 以上 360° 未満")
# 方位の基本
for _name, _deg in [("真北", 0), ("真東", 90), ("真南", 180), ("真西", 270)]:
    in_text(f"- {_name} → ${_deg:03d}°$", "方位の基本: " + _name)
in_text("「北から西へ $30°$」のような言い方はしません。**$330°$** と書きます。",
        "北から西へ 30° は 330°")
chk(360 - 30 == 330, "北から西へ 30° は 330°（計算）")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  塔 30 m / 60°
# ══════════════════════════════════════════════════════════
eq(30 * sp.tan(D(60)), 30 * sp.sqrt(3), "例題1(a) h = 30√3")
eq(30 / sp.cos(D(60)), 60, "例題1(b) 斜辺 60")
eq(30 * sp.sqrt(3) / sp.tan(D(30)), 90, "例題1(c) x = 90")
eq(90 - 30, 60, "例題1(c) PQ = 60")
eq(sp.sqrt(30 ** 2 + (30 * sp.sqrt(3)) ** 2), 60, "例題1 検算 ピタゴラス 60")
eq(2 * 30 * sp.sqrt(3), 60 * sp.sqrt(3), "例題1 検算 斜辺は 60√3")
eq(60 * sp.sqrt(3) * sp.cos(D(30)), 90, "例題1 検算 隣辺は 90")
chk(sp.tan(D(30)) < sp.tan(D(60)), "遠いほど仰角は小さい")
# (d) の主張：h 固定で x が増えると θ は減る
_x1, _x2, _h = 30, 90, 30 * sp.sqrt(3)
chk(sp.atan(_h / _x2) < sp.atan(_h / _x1), "例題1(d) x が大きいと θ は小さい")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  がけ 50 m
# ══════════════════════════════════════════════════════════
eq(50 / sp.tan(D(45)), 50, "例題2(a) d = 50")
eq(50 / sp.tan(D(60)), 50 * sp.sqrt(3) / 3, "例題2(b) d2 = 50√3/3")
eq(50 - 50 * sp.sqrt(3) / 3, 50 * (3 - sp.sqrt(3)) / 3, "例題2(c) 進んだ距離")
chk(float(50 * sp.sqrt(3) / 3) < 50, "近づいたので d2 < 50")
chk(abs(float(50 * sp.sqrt(3) / 3) - 28.87) < 0.02, "50√3/3 ≈ 28.9")
chk(abs(float(50 * (3 - sp.sqrt(3)) / 3) - 21.13) < 0.02, "進んだ距離 ≈ 21.1")
eq((50 * sp.sqrt(3) / 3) ** 2 + 50 ** 2, R(10000, 3), "例題2(b) 検算 2 乗の和")
eq((100 * sp.sqrt(3) / 3) ** 2, R(10000, 3), "例題2(b) 検算 斜辺の 2 乗")
eq(50 / sp.sin(D(60)), 100 * sp.sqrt(3) / 3, "例題2(b) 検算 斜辺は 100√3/3")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  方位角 060° 8 km → 150° 6 km
# ══════════════════════════════════════════════════════════
chk(back(60) == 240, "例題3(a) B から A は 240°")
eq(240 - 150, 90, "例題3(a) ABC = 90°")
eq(sp.sqrt(8 ** 2 + 6 ** 2), 10, "例題3(b) AC = 10")
eq(R(6, 10), R(3, 5), "例題3(c) sin = 3/5")
eq(R(8, 10), R(4, 5), "例題3 検算 cos = 4/5")
eq(R(3, 5) ** 2 + R(4, 5) ** 2, 1, "例題3 検算 sin^2+cos^2 = 1")
eq(150 - 60, 90, "例題3 検算 舵を切った角は 90°")
chk(90 < 180, "例題3(d) 回った角は 180° より小さい")
# (d) 座標で確かめる：A を原点、北を +y、東を +x
_A = sp.Matrix([0, 0])
_B = _A + 8 * sp.Matrix([sp.sin(D(60)), sp.cos(D(60))])
_C = _B + 6 * sp.Matrix([sp.sin(D(150)), sp.cos(D(150))])
_bearAC = sp.deg(sp.atan2(_C[0] - _A[0], _C[1] - _A[1]))
_bac = sp.asin(R(3, 5))
chk(abs(float(_bearAC) - float(60 + sp.deg(_bac))) < 1e-9,
    f"例題3(d) C の方位角 = 060° + BAC ({float(_bearAC)})")
eq(sp.simplify((_C - _A).norm()), 10, "例題3 検算 座標でも AC = 10")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  AB=6, BC=10, B=120°
# ══════════════════════════════════════════════════════════
eq(cos_rule(6, 10, 120), 196, "例題4(a) AC^2 = 196")
eq(sp.sqrt(cos_rule(6, 10, 120)), 14, "例題4(a) AC = 14")
eq(area(6, 10, 120), 15 * sp.sqrt(3), "例題4(b) 面積 15√3")
eq(R(100 + 196 - 36, 2 * 10 * 14), R(13, 14), "例題4(c) cos = 13/14")
eq(cos_rule(6, 10, 90), 136, "例題4 検算 90° なら 136")
chk(196 > 136, "鈍角のほうが長い")
eq(36 + 100 - 60, 76, "例題4 検算 符号を落とすと 76")
eq(R(1, 2) * 10 * (6 * sp.sin(D(60))), 15 * sp.sqrt(3), "例題4 検算 底辺×高さ")
eq(6 * sp.sin(D(60)), 3 * sp.sqrt(3), "例題4 検算 高さ 3√3")
eq(100 + 196 - 2 * 10 * 14 * R(13, 14), 36, "例題4 検算 辺に戻すと 36")
# (d) 直角がないこと
chk(6 ** 2 + 10 ** 2 != 14 ** 2, "例題4(d) ピタゴラスは成り立たない")
_angA = sp.acos(R(196 + 36 - 100, 2 * 14 * 6))
_angC = sp.acos(R(13, 14))
chk(float(sp.deg(_angA)) < 90 and float(sp.deg(_angC)) < 90,
    "例題4(d) 残り 2 角はどちらも鋭角")
chk(abs(float(sp.deg(_angA) + sp.deg(_angC)) - 60) < 1e-9, "残り 2 角の和は 60°")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(20 * sp.tan(D(45)), 20, "演習1 h = 20")
chk(sp.tan(D(45)) == 1, "演習1 検算 tan45 = 1")
eq(20 * sp.sqrt(2), 20 * sp.sqrt(2), "演習1 20√2 は斜辺")
eq(sp.sqrt(20 ** 2 + 20 ** 2), 20 * sp.sqrt(2), "演習1 検算 斜辺は 20√2")
eq(10 * sp.sin(D(60)), 5 * sp.sqrt(3), "演習2 h = 5√3")
eq(10 * sp.cos(D(60)), 5, "演習2 検算 床まで 5")
eq(5 ** 2 + (5 * sp.sqrt(3)) ** 2, 100, "演習2 検算 ピタゴラス 100")
eq(40 / sp.tan(D(30)), 40 * sp.sqrt(3), "演習3 d = 40√3")
eq(90 - 30, 60, "演習3 検算 縦の線からは 60°")
eq(40 * sp.tan(D(60)), 40 * sp.sqrt(3), "演習3 検算 40tan60 = 40√3")
chk(back(70) == 250, "演習4 250°")
chk(0 <= 250 < 360, "演習4 検算 範囲に入る")
chk(70 - 180 == -110, "演習4 検算 引くと範囲外")
chk(360 - 70 == 290, "演習4 290° は別の操作")
eq(12 * sp.sin(D(45)), 6 * sp.sqrt(2), "演習5 東へ 6√2")
eq(12 * sp.cos(D(45)), 6 * sp.sqrt(2), "演習5 検算 南へ 6√2")
eq((6 * sp.sqrt(2)) ** 2 * 2, 144, "演習5 検算 成分の 2 乗の和は 144")
eq(180 - 135, 45, "演習5 135° は南から東へ 45°")
eq(12 * sp.sin(D(135)), 12 * sp.sin(D(45)), "演習5 45° に直しても同じ値")
eq(cos_rule(9, 7, 60), 67, "演習6 AC^2 = 67")
chk(sp.isprime(67), "演習6 67 は素数")
chk(67 < 130, "演習6 検算 直角のときより短い")
eq(sp.sqrt(81 + 49), sp.sqrt(130), "演習6 検算 直角なら √130")
_x7 = sp.Symbol("x7", positive=True)
_sol7 = sp.solve(sp.Eq(_x7 * sp.tan(D(60)), (_x7 + 20) * sp.tan(D(30))), _x7)
chk(_sol7 == [10], f"演習7 x = 10: {_sol7}")
eq(10 * sp.tan(D(60)), 10 * sp.sqrt(3), "演習7 h = 10√3")
eq((10 + 20) * sp.tan(D(30)), 10 * sp.sqrt(3), "演習7 遠いほうの三角形でも 10√3")
eq(180 - 60, 120, "演習7 検算 ABT = 120°")
eq(180 - 30 - 120, 30, "演習7 検算 ATB = 30°")
eq(20 * sp.sin(D(30)) / sp.sin(D(30)), 20, "演習7 検算 正弦定理で BT = 20")
eq(20 * sp.sin(D(60)), 10 * sp.sqrt(3), "演習7 検算 h = 20 sin60")
eq(20 * sp.tan(D(30)), 20 * sp.sqrt(3) / 3, "演習7 20tan30 は答えではない")
chk(sp.simplify(20 * sp.tan(D(30)) - 10 * sp.sqrt(3)) != 0, "20tan30 ≠ 10√3")
eq(sp.deg(sp.atan(10 / (10 * sp.sqrt(3)))), 30, "演習8 検算 仰角は 30°")
eq(sp.deg(sp.atan(10 * sp.sqrt(3) / 10)), 60, "演習8 検算 FAB = 60°")
eq(90 - 60, 30, "演習8 検算 俯角は 90° - 60°")
chk(sp.deg(sp.atan(R(10, 10))) == 45 and 90 - 45 == 45,
    "演習8 45° では、垂直から測るまちがいと区別がつかない")
# 演習9 S は L の真北 5、B は L の真東 5
_L = sp.Matrix([0, 0])
_S = sp.Matrix([0, 5])
_Bp = sp.Matrix([5, 0])
eq(sp.deg(sp.atan2(_Bp[0] - _S[0], _Bp[1] - _S[1])), 135, "演習9 方位角 135°")
eq(180 - 45, 135, "演習9 検算 180° - 45°")
chk(sp.simplify((_Bp - _S).norm()) == 5 * sp.sqrt(2), "演習9 SB = 5√2")
chk(back(50) == 230, "演習10 正しい方位角は 230°")
chk(180 - 50 == 130, "演習10 生徒の計算は 180° - 50°")
chk(130 != 230, "演習10 生徒の値は誤り")

# ══════════════════════════════════════════════════════════
# 6. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("30\\sqrt{3}", "例題1(a)"), ("50\\sqrt{3}", "例題2(b)"),
                ("3-\\sqrt{3}", "例題2(c)"), ("15\\sqrt{3}", "例題4(b)"),
                ("13}{14}", "例題4(c)"), ("3}{5}", "例題3(c)"),
                ("10\\sqrt{3}", "演習7"), ("40\\sqrt{3}", "演習3"),
                ("5\\sqrt{3}", "演習2"), ("6\\sqrt{2}", "演習5"),
                ("\\sqrt{67}", "演習6"), ("$250°$", "演習4"),
                ("$230°$", "演習10"), ("$135°$", "演習9"),
                ("$070°$", "演習4 の設定"), ("$050°$", "演習10 の設定")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
# ★ SL 3.3 に対応する公式集の欄はない
chk("::: {.callout-important}" not in TEXT, "公式集の callout は置かない（3.3 は欄がない）")
chk(TEXT.count("\n> ") == 0, f"引用は置かない: {TEXT.count(chr(10) + '> ')}")
not_in_text("The use of trigonometry in", "シラバス本文は引かない")
not_in_text("Contexts may include use of bearings", "シラバス本文は引かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
in_text("**bearing**（方位角）は、**北から時計回りに測った角**で、"
        "**整数部分を必ず $3$ 桁**にそろえて書きます。", "方位角の定義")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("## 俯角は、垂直な線からではなく、水平線から測ります", "俯角の注意")
in_text("## 方位角は、いつも北から時計回りです", "方位角の注意")
in_text("**縮尺は合っていなくてかまいません。**", "縮尺の断り")
in_text("$2$ 本の水平線は平行なので、視線がその $2$ 本を横切るときにできる角は "
        "**alternate angles**（錯角）です。", "錯角の説明")
in_text("**$0°$ 以上 $360°$ 未満**に収まるよう、$+180°$ か $-180°$ かを選びます。",
        "± の選び方")
in_text("$\\theta < 180°$ なら $+180°$、$\\theta \\ge 180°$ なら $-180°$ とすれば",
        "Why it works の ± の選び方")
in_text("**共通の辺は、どちらの三角形から見ても同じ長さ**です。", "共通の辺")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("**角の単位は `doc → Settings → Document Settings` の `Angle` で決まります。**",
        "角の単位の設定")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 6, f"model-answer が 6: {TEXT.count('{.model-answer}')}")
chk(len(re.findall(r"^::: \{#exm-aasl33-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h_ for h_ in _h2 if h_ in _want] == _want, "5 つの見出しが所定の順")
chk([h_ for h_ in _h2 if h_ in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
chk(TEXT.count("::: {.callout-warning}") == 8, "Common errors 6 + 本文の注意 2 で 8")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
for word in ["得点になりません", "点になりません", "点を落とします",
             "認められません", "減点されます"]:
    not_in_text(word, "採点の断定は避ける")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _b = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _b), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl33", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
# 3.2 へのリンクは、向こうに実在する見出しだけ
_T32 = open(os.path.join(BASE, "aasl-3-2.qmd"), encoding="utf-8").read()
for _a2 in set(re.findall(r"\]\(aasl-3-2\.qmd#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a2 + "}") in _T32, "3.2 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl33-idea") >= 1, "図を本文から参照している")
chk("{#eq-aasl33-back}" in TEXT, "ラベルがある: eq-aasl33-back")
chk(TEXT.count("@eq-aasl33-back") >= 2, "逆向きの式を本文から参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-3-3-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-3-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Elevation and depression", "図(a) の題")
in_fig("angle of depression, measured", "図(a) の俯角")
in_fig("down from the horizontal", "図(a) の俯角（続き）")
in_fig("angle of elevation", "図(a) の仰角")
in_fig("the two are alternate angles between parallel horizontals, so they ",
       "図(a) の説明")
in_fig("(b) Bearings", "図(b) の題")
in_fig("measured from north, clockwise,", "図(b) の説明")
in_fig("always written with three figures", "図(b) の説明（続き）")
in_fig("the bearing back the other way differs by $180°$", "図(b) の逆向き")
in_text("(a) The angle of elevation is measured up from the horizontal at the "
        "lower point", "キャプションが (a) を説明")
in_text("(b) A bearing is measured clockwise from north and written with three "
        "figures", "キャプションが (b) を説明")
# 図に答えの数を書いていない（角度は θ、方位は 180° の一般則だけ）
chk(set(re.findall(r"\d+", FIGSTR)) <= {"180"}, f"図の数字は 180 だけ: {set(re.findall(chr(92) + 'd+', FIGSTR))}")

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-3.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-2.qmd") < DRAFT.index("aasl-3-3.qmd"), "並びが 3.2 → 3.3")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-3.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| angle of elevation |", "| angle of depression |",
           "| alternate angles |", "| back bearing |", "| transversal |",
           "| line of sight |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 演習5：135° の三角比をやめ、45° の直角三角形にした ------------------
in_text("*The bearing $135°$ is $45°$ east of due south.*", "演習5 の解答例は 45°")
in_text("$$12\\sin 45° = 12 \\times \\frac{\\sqrt{2}}{2}$$", "演習5 は sin45")
not_in_text("12\\sin 135°", "sin135 は使わない")
not_in_text("12\\cos 135°", "cos135 は使わない")
in_text("**南から東へ $45°$ 傾いた向き**", "135° を南からの鋭角で読む")
in_text("北から測った $135°$ をそのまま $\\sin$ に入れる形は、SL 3.5 で扱います。",
        "一般の形は 3.5 だと断る")
chk("\\sin 135" not in TEXT and "\\cos 135" not in TEXT, "鈍角の三角比は使っていない")
chk("\\sin 120" in TEXT, "sin120 は SL 3.2 で扱ったので使ってよい（面積で使う）")

# --- 成分に分けるときの角に、条件を付けた --------------------------------
in_text("**いちばん近い南北の線（北か南）から測った鋭角**です。その鋭角を $\\alpha$、"
        "進んだ距離を $d$ とすると、東西の成分は $d\\sin\\alpha$、南北の成分は "
        "$d\\cos\\alpha$ になります。", "成分の条件つきの書き方")
not_in_text("**東向きの成分は $\\sin$**、北向きの成分は $\\cos$ です。",
            "条件なしの一般則は消した")

# --- 演習7：三角形を 2 つ使う問題に差しかえた ----------------------------
in_text("$20$ m nearer the tower than $\\mathrm{A}$", "演習7 は 2 点から見上げる")
in_text("$$h = x\\tan 60° = (x+20)\\tan 30°$$", "演習7 は共通の辺でつなぐ")
in_text("正弦定理より $\\dfrac{\\mathrm{BT}}{\\sin 30°} = \\dfrac{\\mathrm{AB}}{\\sin 30°}$",
        "演習7 の検算は正弦定理")
not_in_text("From a point on level ground $60$ m from the foot of a vertical tower",
            "古い演習7 は消した")
chk(TEXT.count("正弦定理") >= 1, "正弦定理をどこかで使っている")
chk(TEXT.count("共通の辺") >= 2, "共通の辺を本文と演習で使っている")

# --- 演習8：値を書かせる形にし、検算を見分けのつく数にした ---------------
in_text("Write down the angle of elevation of the top of the cliff from the boat",
        "演習8 は値も書かせる")
in_text("がけの高さを $10$、水平距離を $10\\sqrt{3}$ とします。", "検算は 30-60-90")
not_in_text("$\\mathrm{A}$ が高さ $10$、$\\mathrm{B}$ が水平に $10$ 離れているとします。",
            "45° の検算は消した")
in_text("**$45°$ で確かめると、垂直な線から測るまちがいでも同じ数になってしまい、"
        "見分けがつきません。**", "45° では区別がつかないと書いた")

# --- 例題3(d)：回った角が 180° より小さいことを言う ----------------------
in_text("a turn of $90°$, which is less than $180°$, so $\\mathrm{C}$ lies on the "
        "clockwise side of the line $\\mathrm{AB}$", "180° より小さいと明記")
not_in_text("The second leg turns the ship clockwise, so $\\mathrm{C}$ lies clockwise of",
            "根拠のない言い方は消した")
in_text("$90°$ は $180°$ より小さいので、$\\mathrm{C}$ は直線 $\\mathrm{AB}$ の"
        "時計回り側にある。", "日本語訳も直した")

# --- 例題3(a) の検算を、独立した道すじにした -----------------------------
in_text("**検算（(a) について）。** **舵を切った角で見ます。**", "例題3(a) の検算")
not_in_text("$\\mathrm{A}$ での北と $\\mathrm{AB}$ のなす角は $60°$、$\\mathrm{B}$ での北と",
            "同じ計算の繰り返しは消した")

# --- 例題4(d)：ピタゴラスで直角を否定するには最長辺が要る -----------------
in_text("$\\mathrm{AC} = 14$ is the longest side and so the only possible hypotenuse",
        "最長辺だと明記")
not_in_text("Equivalently, $6^{2}+10^{2} = 136 \\neq 196 = 14^{2}$, so Pythagoras' "
            "relation does not hold.", "条件なしの言い方は消した")
chk(14 > 10 > 6, "AC が最長辺")

# --- 例題4 の高さを、幾何で言った ----------------------------------------
in_text("$\\mathrm{A}$ から下ろした垂線の足は線分 $\\mathrm{BC}$ の外に出ます。", "垂線の足")
not_in_text("$6\\sin 60° = 3\\sqrt{3}$ です（$180°-120° = 60°$）", "識別子だけの説明は消した")

# --- 例題1(c)・例題2(b)・演習3 の検算を、独立した道すじにした -------------
in_text("**わり算を通らない道すじでも $90$ になりました。**", "例題1(c) の検算")
in_text("**三角比を通らない道すじでも合いました。**", "例題2(b) の検算")
in_text("**別の角を使っても同じ値になりました。**", "演習3 の検算")
not_in_text("$x = 90$ なら $\\tan 30° = \\dfrac{30\\sqrt{3}}{90}", "同じ式に戻すだけの検算は消した")
not_in_text("$d_{2} = \\dfrac{50}{\\sqrt{3}}$ なら $\\dfrac{50}{d_{2}} = \\sqrt{3}",
            "同じ式に戻すだけの検算は消した")

# --- 演習9 の解答例に、方位角の一歩を入れた ------------------------------
in_text("The bearing of $\\mathrm{L}$ from $\\mathrm{S}$ is $180°$, and $\\mathrm{B}$ is "
        "east of $\\mathrm{L}$", "演習9 の解答例に方位角の根拠")
in_text("$$180° - 45° = 135°$$", "演習9 は引き算を見せる")
in_text("ちょうど南東の向き、つまり $135°$", "真南東は直した")
not_in_text("真南東", "真は北東西南だけ")

# --- 逆向きの方位角の証明 -------------------------------------------------
in_text("**どちらの点でも「北」は同じ向き**です。", "北が同じ向き")
in_text("$3$ 桁で書くのは、範囲とは別の、書き方の約束です。", "3 桁と範囲は別")
in_text("（$\\theta = 0°$ なら $180°$、$\\theta = 180°$ なら $000°$ です）", "端の場合")

# --- 英語が先の順、transversal の説明、表への案内 -------------------------
in_text("**alternate angles**（錯角）", "英語が先")
in_text("**back bearing**（逆向きの方位角）", "英語が先")
in_text("**transversal**（横断線）", "transversal を本文で説明")
in_text("[SL 3.2 の表](aasl-3-2.qmd#tbl-aasl32-exact)", "正確な値の表への案内")
in_text("**公式集には印刷されていません。**", "表は公式集にない")
chk("（alternate angles）" not in TEXT and "（back bearing）" not in TEXT,
    "日本語が先の書き方は残っていない")

# --- 例題1(c) の英文をはっきりさせた --------------------------------------
in_text("The point $\\mathrm{Q}$ lies on the straight line through $\\mathrm{P}$ and the "
        "foot of the tower", "例題1(c) の英文")
not_in_text("further from the tower on the same straight line", "あいまいな言い方は消した")

# --- 演習5 の英文 ---------------------------------------------------------
in_text("Find the exact distance the ship ends up east of its starting point.",
        "演習5 の英文")
not_in_text("Find the exact distance it has travelled due east.", "紛らわしい英文は消した")


# ══════════════════════════════════════════════════════════
# C06  方位角の「$3$ 桁」は、有効数字 $3$ 桁とは別
# ══════════════════════════════════════════════════════════
in_text("**これは「有効数字 $3$ 桁」とは別の約束です。**",
        "C06 有効数字との区別")
in_text("$71.6°$ と丸めてから **$071.6°$** と"
        "書きます。", "C06 071.6 の例")
in_text("- **方位角は整数部分を $3$ 桁**にそろえて書きます",
        "C06 答えの書き方")
in_text("**頭に $0$ を足すだけで、有効数字を $3$ 桁にする話では"
        "ありません。**", "C06 Common errors")
chk(float("%.3g" % 71.5652) == 71.6, "C06 71.5652 を 3 有効数字で 71.6")
chk("%05.1f" % 71.6 == "071.6", "C06 整数部分を 3 桁にそろえると 071.6")
chk(len("071.6".split(".")[0]) == 3, "C06 整数部分が 3 桁")
chk("%03d" % 60 == "060" and "%03d" % 45 == "045", "C06 060 と 045")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
