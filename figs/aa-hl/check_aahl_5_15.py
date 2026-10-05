"""AA HL HL 5.15 — Further derivatives and their integrals の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_15.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-15.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_15.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0


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



_x = sp.Symbol("x")
_a = sp.Symbol("a", positive=True)
R = sp.Rational


def d(f):
    return sp.simplify(sp.diff(f, _x))


def same(u, v):
    """記号で閉じないときは、数値でも確かめる。"""
    _df = sp.simplify(u - v)
    if _df == 0:
        return True
    for _t in (sp.Rational(3, 10), sp.Rational(7, 10), sp.Rational(11, 10),
               sp.Rational(2, 1), sp.Rational(29, 10)):
        _val = complex(_df.subs({_x: _t, _a: 2}).evalf())
        if abs(_val) > 1e-9:
            return False
    return True


# ══════════════════════════════════════════════════════════
# 0. 公式集の導関数（記号のまま）
# ══════════════════════════════════════════════════════════
chk(same(d(sp.tan(_x)), sp.sec(_x) ** 2), "tan の導関数は sec²")
chk(same(d(sp.sec(_x)), sp.sec(_x) * sp.tan(_x)), "sec の導関数")
chk(same(d(sp.csc(_x)), -sp.csc(_x) * sp.cot(_x)), "cosec の導関数")
chk(same(d(sp.cot(_x)), -sp.csc(_x) ** 2), "cot の導関数")
chk(same(d(_a ** _x), _a ** _x * sp.log(_a)), "a^x の導関数")
chk(same(d(sp.log(_x) / sp.log(_a)), 1 / (_x * sp.log(_a))),
    "log_a x の導関数")
chk(same(d(sp.asin(_x)), 1 / sp.sqrt(1 - _x ** 2)), "arcsin の導関数")
chk(same(d(sp.acos(_x)), -1 / sp.sqrt(1 - _x ** 2)), "arccos の導関数")
chk(same(d(sp.atan(_x)), 1 / (1 + _x ** 2)), "arctan の導関数")
# 商の微分から tan
chk(sp.simplify((sp.cos(_x) * sp.cos(_x) - sp.sin(_x) * (-sp.sin(_x)))
                / sp.cos(_x) ** 2 - 1 / sp.cos(_x) ** 2) == 0,
    "商の微分の分子は 1")
# a^x = e^{x ln a}
chk(sp.simplify(sp.exp(_x * sp.log(_a)).rewrite(sp.Pow) - _a ** _x) == 0,
    "a^x = e^{x ln a}")
chk(sp.log(sp.E) == 1, "ln e = 1")
# arcsin と arccos の和は π/2
chk(sp.simplify(sp.asin(R(1, 2)) + sp.acos(R(1, 2)) - sp.pi / 2) == 0,
    "arcsin + arccos = π/2（x=1/2）")
chk(sp.simplify(sp.asin(0) + sp.acos(0) - sp.pi / 2) == 0,
    "arcsin + arccos = π/2（x=0）")
chk(same(d(sp.asin(_x)) + d(sp.acos(_x)), 0), "2 つの導関数の和は 0")
# 公式集の不定積分
chk(same(d(_a ** _x / sp.log(_a)), _a ** _x), "∫a^x dx の検算")
chk(same(d(sp.atan(_x / _a) / _a), 1 / (_a ** 2 + _x ** 2)),
    "∫1/(a²+x²) dx の検算")
chk(same(d(sp.asin(_x / _a)), 1 / sp.sqrt(_a ** 2 - _x ** 2)),
    "∫1/√(a²-x²) dx の検算")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(same(d(sp.tan(3 * _x)), 3 * sp.sec(3 * _x) ** 2), "例題1(a) 3sec²3x")
chk(same(d(_x * sp.sec(_x)),
         sp.sec(_x) + _x * sp.sec(_x) * sp.tan(_x)), "例題1(b)")
chk(same(d(sp.atan(2 * _x)), 2 / (1 + 4 * _x ** 2)), "例題1(c)")
chk(d(sp.tan(3 * _x)).subs(_x, 0) == 3, "例題1(a) x=0 で 3")
chk(d(sp.atan(2 * _x)).subs(_x, 0) == 2, "例題1(c) x=0 で 2")
# 例題2
chk(same(d(3 ** _x), 3 ** _x * sp.log(3)), "例題2 3^x")
chk(same(d(sp.log(_x) / sp.log(2)), 1 / (_x * sp.log(2))), "例題2 log₂x")
chk(sp.log(3) > 0 and sp.log(2) > 0, "例題2 どちらも正")
# 例題3
chk(same(d(sp.tan(2 * _x + 5) / 2), 1 / sp.cos(2 * _x + 5) ** 2),
    "例題3(a) 微分でもどる")
chk(sp.expand((_x + 1) ** 2 + 4) == _x ** 2 + 2 * _x + 5, "例題3(b) 平方完成")
chk(same(d(sp.atan((_x + 1) / 2) / 2), 1 / (_x ** 2 + 2 * _x + 5)),
    "例題3(b) 微分でもどる")
# 例題4
chk(sp.factor(_x ** 2 + 3 * _x + 2) == (_x + 1) * (_x + 2),
    "例題4 因数分解")
chk(sp.simplify(sp.apart(1 / (_x ** 2 + 3 * _x + 2))
                - (1 / (_x + 1) - 1 / (_x + 2))) == 0, "例題4 部分分数")
chk(same(d(sp.log(_x + 1) - sp.log(_x + 2)), 1 / (_x ** 2 + 3 * _x + 2)),
    "例題4 微分でもどる")
chk(sp.simplify((1 / (_x + 1) - 1 / (_x + 2)).subs(_x, 0) - R(1, 2)) == 0,
    "例題4 x=0 で 1/2")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(same(d(sp.tan(4 * _x)), 4 * sp.sec(4 * _x) ** 2), "演習1 4sec²4x")
chk(d(sp.tan(4 * _x)).subs(_x, 0) == 4, "演習1 x=0 で 4")
chk(same(d(sp.asin(3 * _x)), 3 / sp.sqrt(1 - 9 * _x ** 2)), "演習2")
chk(sp.solve(sp.Eq(1 - 9 * _x ** 2, 0), _x) == [-R(1, 3), R(1, 3)],
    "演習2 定義域の端は ±1/3")
chk(same(d(2 ** _x), 2 ** _x * sp.log(2)), "演習3")
chk(sp.N(sp.log(2), 3) < 1, "演習3 ln2 < 1")
chk(same(d(sp.log(_x) / sp.log(5)), 1 / (_x * sp.log(5))), "演習4")
chk(sp.N(1 / sp.log(5), 3) < 1, "演習4 1/ln5 < 1")
chk(same(d(sp.atan(_x / 3) / 3), 1 / (9 + _x ** 2)), "演習5")
chk(same(d(sp.asin(_x / 2)), 1 / sp.sqrt(4 - _x ** 2)), "演習6")
chk(same(d(5 ** _x / sp.log(5)), 5 ** _x), "演習7")
chk(sp.expand((_x + 2) ** 2 + 9) == _x ** 2 + 4 * _x + 13, "演習8 平方完成")
chk(4 ** 2 - 4 * 1 * 13 == -36, "演習8 判別式は -36")
chk(same(d(sp.atan((_x + 2) / 3) / 3), 1 / (_x ** 2 + 4 * _x + 13)),
    "演習8 微分でもどる")
chk(same(d(sp.asin(_x)) + d(sp.acos(_x)), 0), "演習9 和の導関数は 0")
chk(sp.simplify(sp.asin(R(1, 2)) + sp.acos(R(1, 2)) - sp.pi / 2) == 0,
    "演習9 恒等式")
chk(same(d(sp.log(1 + _x ** 2)), 2 * _x / (1 + _x ** 2)),
    "演習10 生徒の答えを微分すると 2x/(1+x²)")
chk(same(d(sp.atan(_x)), 1 / (1 + _x ** 2)), "演習10 正しい答え")
chk(sp.simplify(2 * _x / (1 + _x ** 2) - 1 / (1 + _x ** 2)) != 0,
    "演習10 2 つはちがう")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Derivatives of tanx, secx, cosecx, cotx, ax, loga x, arcsinx,"
        " arccosx, arctanx.", "シラバスの導関数を逐語で")
in_text("> Indefinite integrals of the derivatives of any of the above"
        " functions.", "不定積分を逐語で")
in_text("> Indefinite integral interpreted as a family of curves.",
        "曲線の族を逐語で")
in_text("> The composites of any of these with a linear function.",
        "1 次式との合成を逐語で")
in_text("> Use of partial fractions to rearrange the integrand.",
        "部分分数を逐語で")
in_text("> Link to: partial fractions (AHL1.11)", "1.11 への Link を逐語で")
in_text("公式集の **5.15** の欄", "公式集の場所")
in_text("> Standard derivatives", "公式集の見出しを逐語で")
in_text("> Standard integrals", "公式集の不定積分の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig(", and the triangle", "図(a) の題")
in_fig("1-x^{2}}$, and", "図(a) の注")
in_fig("an indefinite integral is a family of curves", "図(b) の題")
in_fig("at the same $x$ the curves are parallel", "図(b) の注")
in_text("三角形から $\\cos y$ が読めます。", "キャプション (a)")
in_text("がちがうだけで、傾きは同じです。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("9x^{2}", "演習2"), ("x+2}{3}", "演習8")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 構成
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "cSolve"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl515-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl515", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    chk(os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(QMD), _href.split("#")[0]))),
        "リンク先のページがない: " + _href)
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

# ══════════════════════════════════════════════════════════
# 図
# ══════════════════════════════════════════════════════════
for _n in ("a", "b"):
    _p = os.path.join(BASE, "img", "aahl-5-15-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-15-idea-%s.svg)" % _n in TEXT,
        "本文が図 (%s) を貼っている" % _n)
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")

# ══════════════════════════════════════════════════════════
# 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/05-calculus/aahl-5-15.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-15.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| partial fractions |", "| indefinite integral |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## `co` の付く関数の符号を落とす", "co はマイナス")
in_text("## $a^{x}$ を $xa^{x-1}$ と微分する", "指数に x")
in_text("## 平方完成をせずに $\\arctan$ の形に当てはめる", "平方完成が先")
in_text("## $+C$ を書かない", "+C を忘れない")
in_text("**判別式を見る**と早いです。", "判別式で分ける")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
