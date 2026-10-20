"""AA HL 1.16（連立 1 次方程式）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_16.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-16.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_16.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x, y, z, k, lam = sp.symbols("x y z k lambda")


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + "  (%s vs %s)" % (u, v))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def not_in_fig(sub, msg=""):
    chk(sub not in FIG, "図に文章が残っている: " + msg + " :: " + sub[:70])


def unique(eqs, want, msg):
    """解がただ 1 つで、その値が want であること。"""
    sol = sp.solve(eqs, (x, y, z), dict=True)
    chk(len(sol) == 1 and all(v in sol[0] for v in (x, y, z))
        and (sol[0][x], sol[0][y], sol[0][z]) == want,
        "%s: 解が (%s) になる（得た解 %s）" % (msg, want, sol))


def none(eqs, msg):
    chk(sp.solve(eqs, (x, y, z), dict=True) == [], msg + ": 解なし")


def family(eqs, gen, msg):
    """gen(lam) が、すべての lam で 3 式を満たすこと（かつ解が 1 つでないこと）。"""
    sol = sp.solve(eqs, (x, y, z), dict=True)
    chk(len(sol) == 1 and z not in sol[0], msg + ": 解が 1 つに決まらない（%s）" % sol)
    for _lv in (-2, 0, sp.Rational(1, 2), 1, 3, 7):
        _p = [sp.nsimplify(c) for c in gen(_lv)]
        for _i, _e in enumerate(eqs):
            chk(sp.simplify(_e.subs({x: _p[0], y: _p[1], z: _p[2]})) == 0,
                "%s: λ=%s が式 %d を満たす" % (msg, _lv, _i + 1))


# ══════════════════════════════════════════════════════════
# 1. The idea の連立方程式
# ══════════════════════════════════════════════════════════
unique([x + y + z - 6, 2 * x - y + z - 3, x + 2 * y - z - 2], (1, 2, 3), "§3")
# §3 の途中の行
eq((2 * x - y + z - 3) - 2 * (x + y + z - 6), -3 * y - z + 9, "§3 R2-2R1")
eq((x + 2 * y - z - 2) - (x + y + z - 6), y - 2 * z + 4, "§3 R3-R1")
chk(sp.solve([3 * y + z - 9, y - 2 * z + 4], (y, z), dict=True)[0] == {y: 2, z: 3},
    "§3 2 文字の連立")
eq(3 * (2 * z - 4) + z - 9, 7 * z - 21, "§3 代入したあと")

_INF = [x + y + z - 6, x + 2 * y + 3 * z - 14, 2 * x + 3 * y + 4 * z - 20]
family(_INF, lambda L: (-2 + L, 8 - 2 * L, L), "§4")
eq((x + 2 * y + 3 * z - 14) - (x + y + z - 6), y + 2 * z - 8, "§4 R2-R1")
eq((2 * x + 3 * y + 4 * z - 20) - 2 * (x + y + z - 6), y + 2 * z - 8, "§4 R3-2R1")
eq(6 - (8 - 2 * lam) - lam, -2 + lam, "§4 x の式")
chk(all(sp.simplify(_e.subs({x: -2, y: 8, z: 0})) == 0 for _e in _INF),
    "§4 λ=0 は (-2, 8, 0)")
chk(all(sp.simplify(_e.subs({x: 1, y: 2, z: 3})) == 0 for _e in _INF),
    "§4 λ=3 は (1, 2, 3)")
none([x + y + z - 6, x + 2 * y + 3 * z - 14, 2 * x + 3 * y + 4 * z - 21], "§5")
eq((2 * x + 3 * y + 4 * z - 21) - 2 * (x + y + z - 6), y + 2 * z - 9, "§5 R3-2R1")
eq((y + 2 * z - 9) - (y + 2 * z - 8), -1, "§5 R3-R2 が 0 = 1")

# ══════════════════════════════════════════════════════════
# 2. 例題
# ══════════════════════════════════════════════════════════
unique([x + y + z - 4, 2 * x - y + 3 * z - 14, 3 * x + 2 * y - z - 1],
       (2, -1, 3), "例題1")
eq((2 * x - y + 3 * z - 14) - 2 * (x + y + z - 4), -3 * y + z - 6, "例題1 R2-2R1")
eq((3 * x + 2 * y - z - 1) - 3 * (x + y + z - 4), -y - 4 * z + 11, "例題1 R3-3R1")
eq(y + 4 * (6 + 3 * y) - 11, 13 * y + 13, "例題1 代入")

_E2 = [x + 2 * y - z - 3, 2 * x + 5 * y + z - 10, 3 * x + 7 * y - 13]
family(_E2, lambda L: (-5 + 7 * L, 4 - 3 * L, L), "例題2")
eq((2 * x + 5 * y + z - 10) - 2 * (x + 2 * y - z - 3), y + 3 * z - 4, "例題2 R2-2R1")
eq((3 * x + 7 * y - 13) - 3 * (x + 2 * y - z - 3), y + 3 * z - 4, "例題2 R3-3R1")
eq(3 - 2 * (4 - 3 * lam) + lam, -5 + 7 * lam, "例題2 x の式")
none([x + 2 * y - z - 3, 2 * x + 5 * y + z - 10, 3 * x + 7 * y - 14], "例題3")
eq((3 * x + 7 * y - 14) - 3 * (x + 2 * y - z - 3), y + 3 * z - 5, "例題3 R3-3R1")
chk(all(sp.simplify(_e.subs({x: 2, y: 1, z: 1})) == 0 for _e in _E2),
    "例題2 λ=1 は (2, 1, 1)")
chk(sp.simplify((3 * x + 7 * y - 14).subs({x: 2, y: 1, z: 1})) == -1,
    "例題3 の 3 行目だけが合わない")

_E4 = [x + 2 * y + 3 * z - 4, 2 * x + 5 * y + 4 * z - 7, 3 * x + 7 * y + k * z - 11]
eq((2 * x + 5 * y + 4 * z - 7) - 2 * (x + 2 * y + 3 * z - 4), y - 2 * z + 1,
   "例題4 R2-2R1")
eq((3 * x + 7 * y + k * z - 11) - 3 * (x + 2 * y + 3 * z - 4),
   y + (k - 9) * z + 1, "例題4 R3-3R1")
eq((y + (k - 9) * z + 1) - (y - 2 * z + 1), (k - 7) * z, "例題4 R3-R2")
for _kv in (-3, 0, 1, 5, 6, 8, 12):
    _s = sp.solve([_e.subs(k, _kv) for _e in _E4], (x, y, z), dict=True)
    chk(len(_s) == 1 and _s[0] == {x: 6, y: -1, z: 0},
        "例題4 k=%s なら (6, -1, 0)" % _kv)
family([_e.subs(k, 7) for _e in _E4], lambda L: (6 - 7 * L, 2 * L - 1, L), "例題4 k=7")
eq(4 - 2 * (2 * lam - 1) - 3 * lam, 6 - 7 * lam, "例題4 x の式")
chk(all(sp.simplify(_e.subs({k: 7, x: -1, y: 1, z: 1})) == 0 for _e in _E4),
    "例題4 検算 λ=1 は (-1, 1, 1)")

# ══════════════════════════════════════════════════════════
# 3. 演習
# ══════════════════════════════════════════════════════════
unique([x + y + z - 5, 2 * x - y + z - 7, x + 2 * y - z + 1], (2, 0, 3), "演習1")
unique([x + y + z - 6, 2 * x + y - z - 1, x - y + 2 * z - 5], (1, 2, 3), "演習2")
family([x + y + z - 4, 2 * x + 3 * y + z - 9, 3 * x + 5 * y + z - 14],
       lambda L: (3 - 2 * L, 1 + L, L), "演習3")
eq((3 * x + 5 * y + z - 14) - 3 * (x + y + z - 4), 2 * y - 2 * z - 2, "演習3 R3-3R1")
eq((2 * y - 2 * z - 2) - 2 * (y - z - 1), 0, "演習3 R3-2R2 が 0 = 0")
none([x + 2 * y + z - 3, 2 * x + 3 * y - z - 5, 3 * x + 5 * y - 9], "演習4")
eq((2 * x + 3 * y - z - 5) - 2 * (x + 2 * y + z - 3), -y - 3 * z + 1, "演習4 R2-2R1")
eq((3 * x + 5 * y - 9) - 3 * (x + 2 * y + z - 3), -y - 3 * z, "演習4 R3-3R1")
eq((x + 2 * y + z - 3) + (2 * x + 3 * y - z - 5), 3 * x + 5 * y - 8, "演習4 足すと 8")

_E5 = [x + y + z - 2, 2 * x + 3 * y + z - 5, x + k * y + 3 * z - 4]
eq((2 * x + 3 * y + z - 5) - 2 * (x + y + z - 2), y - z - 1, "演習5 R2-2R1")
eq((x + k * y + 3 * z - 4) - (x + y + z - 2), (k - 1) * y + 2 * z - 2, "演習5 R3-R1")
eq(((k - 1) * y + 2 * z - 2) - (k - 1) * (y - z - 1), (k + 1) * z - (3 - k),
   "演習5 R3-(k-1)R2")
none([_e.subs(k, -1) for _e in _E5], "演習5 k=-1")
for _kv in (-3, 0, 1, 2, 5):
    chk(len(sp.solve([_e.subs(k, _kv) for _e in _E5], (x, y, z), dict=True)) == 1
        and z in sp.solve([_e.subs(k, _kv) for _e in _E5],
                          (x, y, z), dict=True)[0],
        "演習5 k=%s なら解が 1 つ" % _kv)
chk(sp.solve([_e.subs(k, 1) for _e in _E5], (x, y, z), dict=True)[0]
    == {x: -1, y: 2, z: 1}, "演習5 検算 k=1 は (-1, 2, 1)")
family([x + y + z - 2, 2 * x + 3 * y + z - 5, x - y + 3 * z],
       lambda L: (1 - 2 * L, 1 + L, L), "演習6")
eq((x - y + 3 * z) - (x + y + z - 2), -2 * y + 2 * z + 2, "演習6 R3-R1")
_E7 = [x + y + z - 6, 2 * x + y - z - 3]
for _lv in (-1, 0, 2, 3, sp.Rational(5, 2)):
    for _i, _e in enumerate(_E7):
        chk(sp.simplify(_e.subs({x: 2 * _lv - 3, y: 9 - 3 * _lv, z: _lv})) == 0,
            "演習7 λ=%s が式 %d を満たす" % (_lv, _i + 1))
eq((2 * x + y - z - 3) - 2 * (x + y + z - 6), -y - 3 * z + 9, "演習7 R2-2R1")
eq(6 - (9 - 3 * lam) - lam, -3 + 2 * lam, "演習7 x の式")
none([x + y + z - 1, x + y + z - 2, 0 * x], "演習8 検算の 2 式は解なし")
unique([x + y + z - 12, 2 * x + 3 * y + z - 22, x + 2 * y + 3 * z - 28],
       (2, 4, 6), "演習9")
eq((2 * x + 3 * y + z - 22) - 2 * (x + y + z - 12), y - z + 2, "演習9 R2-2R1")
eq((x + 2 * y + 3 * z - 28) - (x + y + z - 12), y + 2 * z - 16, "演習9 R3-R1")
eq((y + 2 * z - 16) - (y - z + 2), 3 * z - 18, "演習9 R3-R2")
chk(2 + 4 + 6 == 12 and 2 * 2 + 3 * 4 + 6 == 22 and 2 + 2 * 4 + 3 * 6 == 28,
    "演習9 の 3 つの条件")

# ══════════════════════════════════════════════════════════
# 4. 操作が解を変えないこと（Why it works）
# ══════════════════════════════════════════════════════════
_A = [x + y + z - 6, 2 * x - y + z - 3, x + 2 * y - z - 2]
_c = sp.Symbol("c")
for _cv in (-3, -1, 2, 5):
    _B = [_A[0], _A[1] + _cv * _A[0], _A[2]]
    chk(sp.solve(_B, (x, y, z), dict=True) == sp.solve(_A, (x, y, z), dict=True),
        "R2 -> R2 + %s R1 で解が変わらない" % _cv)
    _C = [_A[0], _cv * _A[1], _A[2]]
    chk(sp.solve(_C, (x, y, z), dict=True) == sp.solve(_A, (x, y, z), dict=True),
        "R2 -> %s R2 で解が変わらない（0 でない）" % _cv)
_D = [_A[0], 0 * _A[1], _A[2]]
chk(sp.solve(_D, (x, y, z), dict=True) != sp.solve(_A, (x, y, z), dict=True),
    "0 倍すると解が変わる")

# ══════════════════════════════════════════════════════════
# 5. シラバス（逐語）
# ══════════════════════════════════════════════════════════
not_in_text("> Solutions of systems of linear equations (a maximum of three equations"
        " in three unknowns), including cases where there is a unique solution,"
        " an infinite number of solutions or no solution.",
        "シラバス本体を逐語で")
not_in_text("> These systems should be solved using both algebraic and technological"
        " methods, for example row reduction or matrices.",
        "Guidance（解き方）を逐語で")
not_in_text("> Systems which have no solution(s) are inconsistent.",
        "Guidance（inconsistent）を逐語で")
not_in_text("> Finding a general solution for a system with an infinite number"
        " of solutions.", "Guidance（general solution）を逐語で")
not_in_text("> Link to: intersection of lines and planes (AHL 3.18).",
        "Link to を逐語で")
in_text("## 公式集には、この項目の欄がありません", "公式集にないことを書く")
not_in_text("公式集の **1.16**", "ありもしない欄を書かない")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 6. GDC / 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("`Solve System of Linear Equations`", "TI-Nspire のメニュー名")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 2, "--- は 2 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl116-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Common errors",
         "Exercises"]
not_in_text("## Worked examples", "例題は各節の説明のすぐ後に置く")
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)] == list(range(1, 8)),
    "The idea が 1..7 で連番")
chk(TEXT.count("**検算") >= 12, "検算が十分ある: %d" % TEXT.count("**検算"))
not_in_text("**確かめ", "検算は「検算」で統一")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
_ce = TEXT[TEXT.index("\n## Common errors"):TEXT.index("\n## Exercises")]
chk(_ce.count("::: {.callout-warning}") == 6, "Common errors が 6 つ")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
chk(all("@eq-" not in TEXT.split("$$")[i] for i in range(1, len(TEXT.split("$$")), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    chk(not re.search(r"[ぁ-んァ-ン一-龥]",
                      _blk.replace("**試験ではこう書く**", "")),
        "model-answer に日本語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors", "exercises"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aahl116", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
not_in_text("aahl-3-18.qmd", "3.18 への前方リンクは張らない")
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head, "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は 1 つだけ")
not_in_text("**この節ですること：", "節の頭の 1 文は置かない")
not_in_text("\\vec{", "ベクトルの記号は太字")
chk(len(re.findall(r"^::: ", TEXT, re.M)) == len(re.findall(r"^:::$", TEXT, re.M)),
    "::: の開閉が一致")
for _h in re.findall(r"^#{1,4} .+$", TEXT, re.M):
    chk(not re.search(r"\$\s*—", _h), "見出しで数式の直後に —: " + _h)
_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_j = TEXT.index(chr(10) + "## Common errors", _i)
_wiw = TEXT[_i:_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
# ★ The idea の見出しは「英語（日本語）」の形（_AA-HL-PLAN.md の「決まったこと」5）
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)
in_text("### 1. Systems of linear equations and their solutions（連立 "
        "$1$ 次方程式とその解） {#idea}", "見出し 1")
in_text("### 2. Row reduction: the three operations（row "
        "reduction：$3$ つの操作） {#operations}", "見出し 2")
in_text("### 3. A unique solution（解が $1$ つに決まる場合） {#unique}", "見出し 3")
in_text("### 4. Infinitely many solutions: the general "
        "solution（解が無数にある場合） {#infinite}", "見出し 4")
in_text("### 5. No solution: inconsistent systems（解がない場合） "
        "{#inconsistent}", "見出し 5")
in_text("### 6. Telling the three cases apart（$3$ つの場合の見分け方） "
        "{#classify}", "見出し 6")
in_text("### 7. A picture in two variables（$2$ 変数の図で見る） {#picture}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 7. 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-1-16-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-1-16-idea-%s.svg)" % _n in TEXT, "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
not_in_fig("After row reduction, the last row decides everything", "図(a) の題")
in_fig("the last row says $0=0$", "図(a) の 0 = 0")
not_in_fig("Two equations in two unknowns: the same three cases", "図(b) の題")
in_fig("the two lines coincide", "図(b) の重なる場合")
in_text("row reduction のあと、いちばん下の行だけを見ます。", "キャプション (a)")
in_text("$2$ 変数でも、$3$ つの場合は同じように起こります。", "キャプション (b)")
for leak in ["(2, 4, 6)", "6 - 7", "lambda"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 8. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("3-2\\lambda", "演習3"), ("1-2\\lambda", "演習6"),
                    ("-3+2\\lambda", "演習7"), ("2$ 個、", "演習9")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 9. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-16.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-1-15.qmd") < DRAFT.index("aahl-1-16.qmd"),
    "サイドバーの並びが 1.15 → 1.16")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-16.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| system of linear equations |", "| general solution |",
          "| inconsistent |", "| row reduction |", "| augmented matrix |",
          "| back substitution |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")

# ══════════════════════════════════════════════════════════
# 10. 見張り
# ══════════════════════════════════════════════════════════
in_text("## $0$ 倍はできません", "0 倍は禁じてある")
in_text("**縦線の左が係数、右が定数**です。", "augmented matrix の読み方")
in_text("**$0 = 0$ と $0 = b$ を取りちがえないでください。**", "2 つの区別")
in_text("なお、この本では行列そのものは扱いません。", "行列は扱わないと明記")
in_text("**平面としての見方は、Topic 3 で扱います。**", "3.18 は先の話")

print()

# ══════════════════════════════════════════════════════════
# 2026-10-13 の手直し（表 1 を数字の例に）
# ══════════════════════════════════════════════════════════
in_text("| $2$ つの式を入れかえる | $R_{1} \\leftrightarrow R_{2}$ | "
        "$\\begin{aligned} 2x - y + z &= 3 \\\\ x + y + z &= 6 \\\\ "
        "x + 2y - z &= 2 \\end{aligned}$ |", "表 1 の 1 行目")
in_text("| $1$ つの式を $0$ でない数倍する | $R_{2} \\to 3R_{2}$ | "
        "$\\begin{aligned} x + y + z &= 6 \\\\ 6x - 3y + 3z &= 9 \\\\ "
        "x + 2y - z &= 2 \\end{aligned}$ |", "表 1 の 2 行目")
in_text("| $1$ つの式に、別の式の何倍かを足す | $R_{2} \\to R_{2} - 2R_{1}$ | "
        "$\\begin{aligned} x + y + z &= 6 \\\\ -3y - z &= -9 \\\\ "
        "x + 2y - z &= 2 \\end{aligned}$ |", "表 1 の 3 行目")
# 例の列は式だけ（日本語を混ぜない）
for _row in re.findall(r"^\| \$\d\$ つの式[^\n]*$", TEXT, re.M):
    _cell = _row.split("|")[3]
    chk(not re.search(r"[ぁ-んァ-ヴ一-龥]", _cell), "表 1 の例に日本語: " + _cell[:40])
not_in_text("| $1$ 行目と $2$ 行目を交換 |", "前の抽象的な例は消した")
in_text("$2x-y+z=3$ を $0$ 倍すると $0 = 0$ になり", "0 倍の例も数字で")
not_in_text("$R_{2} \\to 0 \\times R_{2}$ とすると", "前の書き方は消した")
# 表 1 の数値が @eq-aahl116-system と合っていること
_x16, _y16, _z16 = sp.symbols("x y z")
_r1 = _x16 + _y16 + _z16 - 6
_r2 = 2 * _x16 - _y16 + _z16 - 3
_r3 = _x16 + 2 * _y16 - _z16 - 2
chk(sp.expand(3 * _r2 - (6 * _x16 - 3 * _y16 + 3 * _z16 - 9)) == 0,
    "3R2 は 6x-3y+3z=9")
chk(sp.expand(_r2 - 2 * _r1 - (-3 * _y16 - _z16 + 9)) == 0,
    "R2-2R1 は -3y-z=-9")
chk(sp.solve([_r1, _r2, _r3], [_x16, _y16, _z16]) == {_x16: 1, _y16: 2, _z16: 3},
    "もとの連立の解は (1, 2, 3)")


# code span の中に数式を入れない（$ がそのまま表示されてしまう）
for _cs in re.findall(r"`([^`\n]+)`", TEXT):
    chk("$" not in _cs, "code span の中に数式: " + _cs[:50])
in_text("*Let $x$, $y$, $z$ be ...* の $1$ 行です。", "文字の宣言は italic")


# ══════════════════════════════════════════════════════════
# 2026-10-13 の手直し（§3〜§5 を 3 つの式セットで書く）
# ══════════════════════════════════════════════════════════
in_text("**$3$ つの式は、いつもセットで書き直します。**", "セットで書く方針")
in_text("R_{2} \\to R_{2} - 2R_{1}, \\qquad R_{3} \\to R_{3} - R_{1}", "§3 の操作")
in_text("x + y + z &= 6 \\\\\n-3y - z &= -9 \\\\\ny - 2z &= -4", "§3 の 1 回目")
in_text("x + y + z &= 6 \\\\\n3y + z &= 9 \\\\\ny - 2z &= -4", "§3 の 2 回目")
in_text("R_{2} \\to -R_{2}", "§3 の -1 倍")
_idea16 = TEXT[TEXT.index("## The idea"):TEXT.index("## Why it works")]
chk(": \\qquad" not in _idea16, "The idea に 1 本だけ書く形は残っていない")
chk("$2$ 行目は、両辺に $-1$ を掛けておきます。" in _idea16, "§3 の -1 倍の説明")
in_text("x + y + z &= 6 \\\\\ny + 2z &= 8 \\\\\ny + 2z &= 8", "§4 の 1 回目")
in_text("x + y + z &= 6 \\\\\ny + 2z &= 8 \\\\\n0 &= 0", "§4 の 2 回目")
in_text("x + y + z &= 6 \\\\\ny + 2z &= 8 \\\\\ny + 2z &= 9", "§5 の 1 回目")
in_text("x + y + z &= 6 \\\\\ny + 2z &= 8 \\\\\n0 &= 1", "§5 の 2 回目")
# 書き直した 3 つの式が、もとの連立と同じ解をもつこと
_x6, _y6, _z6 = sp.symbols("x y z")
_sys3 = [_x6 + _y6 + _z6 - 6, 2 * _x6 - _y6 + _z6 - 3, _x6 + 2 * _y6 - _z6 - 2]
_step1 = [_x6 + _y6 + _z6 - 6, -3 * _y6 - _z6 + 9, _y6 - 2 * _z6 + 4]
_step2 = [_x6 + _y6 + _z6 - 6, 3 * _y6 + _z6 - 9, _y6 - 2 * _z6 + 4]
for _nm, _sy in (("§3 の 1 回目", _step1), ("§3 の 2 回目", _step2)):
    chk(sp.solve(_sy, [_x6, _y6, _z6]) == {_x6: 1, _y6: 2, _z6: 3},
        _nm + " の解も (1, 2, 3)")
_inf = [_x6 + _y6 + _z6 - 6, _x6 + 2 * _y6 + 3 * _z6 - 14,
        2 * _x6 + 3 * _y6 + 4 * _z6 - 20]
chk(sp.expand(_inf[1] - _inf[0] - (_y6 + 2 * _z6 - 8)) == 0, "§4 R2-R1")
chk(sp.expand(_inf[2] - 2 * _inf[0] - (_y6 + 2 * _z6 - 8)) == 0, "§4 R3-2R1")
_bad = 2 * _x6 + 3 * _y6 + 4 * _z6 - 21
chk(sp.expand(_bad - 2 * _inf[0] - (_y6 + 2 * _z6 - 9)) == 0, "§5 R3-2R1 は y+2z=9")


# ══════════════════════════════════════════════════════════
# 2026-10-13 の手直し（例題・演習も 3 つの式セットで書く）
# ══════════════════════════════════════════════════════════
_X, _Y, _Z, _K = sp.symbols("x y z k")


def _aug(rows):
    """[左辺 - 右辺] の並びを拡大係数行列にして、既約行階段形で返す。"""
    M = []
    for _e in rows:
        _p = sp.Poly(sp.expand(_e), _X, _Y, _Z)
        M.append([_p.coeff_monomial(_X), _p.coeff_monomial(_Y),
                  _p.coeff_monomial(_Z), -_p.coeff_monomial(1)])
    return sp.Matrix(M).rref()[0]


def same_system(orig, shown, msg):
    chk(_aug(orig) == _aug(shown), "同じ連立になっていない: " + msg)


# 例題 1
_o1 = [_X + _Y + _Z - 4, 2 * _X - _Y + 3 * _Z - 14, 3 * _X + 2 * _Y - _Z - 1]
same_system(_o1, [_X + _Y + _Z - 4, -3 * _Y + _Z - 6, -_Y - 4 * _Z + 11],
            "例題1 の 1 回目")
same_system(_o1, [_X + _Y + _Z - 4, -3 * _Y + _Z - 6, _Y + 4 * _Z - 11],
            "例題1 の 2 回目")
chk(sp.solve(_o1, [_X, _Y, _Z]) == {_X: 2, _Y: -1, _Z: 3}, "例題1 の解")
# 例題 2（解は無数）
_o2 = [_X + 2 * _Y - _Z - 3, 2 * _X + 5 * _Y + _Z - 10, 3 * _X + 7 * _Y - 13]
same_system(_o2, [_X + 2 * _Y - _Z - 3, _Y + 3 * _Z - 4, _Y + 3 * _Z - 4],
            "例題2 の 1 回目")
same_system(_o2, [_X + 2 * _Y - _Z - 3, _Y + 3 * _Z - 4, sp.Integer(0)],
            "例題2 の 2 回目（0 = 0）")
# 例題 3（解なし）: 3 行目の右辺だけ 14
_o3 = [_X + 2 * _Y - _Z - 3, 2 * _X + 5 * _Y + _Z - 10, 3 * _X + 7 * _Y - 14]
chk(sp.solve(_o3, [_X, _Y, _Z]) == [], "例題3 に解はない")
chk(sp.expand((3 * _X + 7 * _Y - 14) - 3 * (_X + 2 * _Y - _Z - 3)
              - (_Y + 3 * _Z - 5)) == 0, "例題3 R3-3R1 は y+3z=5")
# 例題 4（k 入り）
for _kv in (0, 1, 5, 8, 9):
    _o4 = [_X + 2 * _Y + 3 * _Z - 4, 2 * _X + 5 * _Y + 4 * _Z - 7,
           3 * _X + 7 * _Y + _kv * _Z - 11]
    _s4 = [_X + 2 * _Y + 3 * _Z - 4, _Y - 2 * _Z + 1,
           (_kv - 7) * _Z]
    same_system(_o4, _s4, "例題4（k = %d）" % _kv)
# 演習 1〜7, 9
_ex = [
    ("演習1", [_X + _Y + _Z - 5, 2 * _X - _Y + _Z - 7, _X + 2 * _Y - _Z + 1],
     [_X + _Y + _Z - 5, 3 * _Y + _Z - 3, _Y - 2 * _Z + 6]),
    ("演習2", [_X + _Y + _Z - 6, 2 * _X + _Y - _Z - 1, _X - _Y + 2 * _Z - 5],
     [_X + _Y + _Z - 6, _Y + 3 * _Z - 11, -2 * _Y + _Z + 1]),
    ("演習3a", [_X + _Y + _Z - 4, 2 * _X + 3 * _Y + _Z - 9,
                3 * _X + 5 * _Y + _Z - 14],
     [_X + _Y + _Z - 4, _Y - _Z - 1, 2 * _Y - 2 * _Z - 2]),
    ("演習3b", [_X + _Y + _Z - 4, 2 * _X + 3 * _Y + _Z - 9,
                3 * _X + 5 * _Y + _Z - 14],
     [_X + _Y + _Z - 4, _Y - _Z - 1, sp.Integer(0)]),
    ("演習4", [_X + 2 * _Y + _Z - 3, 2 * _X + 3 * _Y - _Z - 5,
               3 * _X + 5 * _Y - 9],
     [_X + 2 * _Y + _Z - 3, -_Y - 3 * _Z + 1, -_Y - 3 * _Z]),
    ("演習6a", [_X + _Y + _Z - 2, 2 * _X + 3 * _Y + _Z - 5,
                _X - _Y + 3 * _Z],
     [_X + _Y + _Z - 2, _Y - _Z - 1, -2 * _Y + 2 * _Z + 2]),
    ("演習6b", [_X + _Y + _Z - 2, 2 * _X + 3 * _Y + _Z - 5,
                _X - _Y + 3 * _Z],
     [_X + _Y + _Z - 2, _Y - _Z - 1, sp.Integer(0)]),
    ("演習7", [_X + _Y + _Z - 6, 2 * _X + _Y - _Z - 3],
     [_X + _Y + _Z - 6, _Y + 3 * _Z - 9]),
    ("演習9a", [_X + _Y + _Z - 12, 2 * _X + 3 * _Y + _Z - 22,
                _X + 2 * _Y + 3 * _Z - 28],
     [_X + _Y + _Z - 12, _Y - _Z + 2, _Y + 2 * _Z - 16]),
    ("演習9b", [_X + _Y + _Z - 12, 2 * _X + 3 * _Y + _Z - 22,
                _X + 2 * _Y + 3 * _Z - 28],
     [_X + _Y + _Z - 12, _Y - _Z + 2, 3 * _Z - 18]),
]
for _nm, _o, _sh in _ex:
    same_system(_o, _sh, _nm)
# 演習 5（k 入り）
for _kv in (-1, 0, 1, 3):
    _o5 = [_X + _Y + _Z - 2, 2 * _X + 3 * _Y + _Z - 5, _X + _kv * _Y + 3 * _Z - 4]
    _s5 = [_X + _Y + _Z - 2, _Y - _Z - 1, (_kv + 1) * _Z - (3 - _kv)]
    same_system(_o5, _s5, "演習5（k = %d）" % _kv)
# 1 本だけ書く形は、ページのどこにも残っていない
not_in_text(": \\qquad", "1 本だけ書く形は残っていない（本文）")
not_in_text(": \\quad", "1 本だけ書く形は残っていない（解答例）")
chk(TEXT.count("\\begin{aligned}") >= 30,
    "3 式セットの表示が十分ある: %d" % TEXT.count("\\begin{aligned}"))

not_in_text("シラバスは、次のように書いています。", "決まり文句は使わない")

print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
