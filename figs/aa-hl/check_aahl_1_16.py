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
in_text("> Solutions of systems of linear equations (a maximum of three equations"
        " in three unknowns), including cases where there is a unique solution,"
        " an infinite number of solutions or no solution.",
        "シラバス本体を逐語で")
in_text("> These systems should be solved using both algebraic and technological"
        " methods, for example row reduction or matrices.",
        "Guidance（解き方）を逐語で")
in_text("> Systems which have no solution(s) are inconsistent.",
        "Guidance（inconsistent）を逐語で")
in_text("> Finding a general solution for a system with an infinite number"
        " of solutions.", "Guidance（general solution）を逐語で")
in_text("> Link to: intersection of lines and planes (AHL 3.18).",
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

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl116-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
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
_j = TEXT.index(chr(10) + "## Worked examples", _i)
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
in_fig("After row reduction, the last row decides everything", "図(a) の題")
in_fig("the last row says $0=0$", "図(a) の 0 = 0")
in_fig("Two equations in two unknowns: the same three cases", "図(b) の題")
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
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
