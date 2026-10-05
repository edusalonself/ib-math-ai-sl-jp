"""AA HL HL 5.16 — Integration by substitution and by parts の内容を検算する。

    python3 figs/aa-hl/check_aahl_5_16.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "05-calculus")
QMD = os.path.join(BASE, "aahl-5-16.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_5_16.py"), encoding="utf-8").read()
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
_u = sp.Symbol("u", positive=True)
R = sp.Rational


def d(f):
    return sp.simplify(sp.diff(f, _x))


def back(F, f):
    """F を微分すると f にもどるか。"""
    return sp.simplify(sp.diff(F, _x) - f) == 0


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_f = sp.Function("f")
_g = sp.Function("g")
# 連鎖律を逆に読む
chk(sp.simplify(sp.diff(_f(_g(_x)), _x)
                - sp.Derivative(_f(_g(_x)), _g(_x)) * sp.diff(_g(_x), _x))
    == 0, "連鎖律の形")
# 部分積分は積の微分から
_uu = sp.Function("uu")(_x)
_vv = sp.Function("vv")(_x)
chk(sp.simplify(sp.diff(_uu * _vv, _x)
                - (_uu * sp.diff(_vv, _x) + _vv * sp.diff(_uu, _x))) == 0,
    "積の微分公式")
# 置換の一般形
chk(back((_x ** 2 + 1) ** 6 / 6, 2 * _x * (_x ** 2 + 1) ** 5),
    "置換の形が成り立つ")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(back((_x ** 2 + 1) ** 6 / 6, 2 * _x * (_x ** 2 + 1) ** 5),
    "例題1 微分でもどる")
chk(sp.integrate(_u ** 5, _u) == _u ** 6 / 6, "例題1 u の積分")
# 例題2
_ans2 = R(2, 5) * (_x + 1) ** R(5, 2) - R(2, 3) * (_x + 1) ** R(3, 2)
chk(sp.simplify(sp.diff(_ans2, _x) - _x * sp.sqrt(_x + 1)) == 0,
    "例題2 微分でもどる")
chk(sp.expand((_u - 1) * sp.sqrt(_u))
    == _u ** R(3, 2) - sp.sqrt(_u), "例題2 展開")
chk(sp.integrate(_u ** R(3, 2) - _u ** R(1, 2), _u)
    == R(2, 5) * _u ** R(5, 2) - R(2, 3) * _u ** R(3, 2), "例題2 u の積分")
# 例題3
chk(back(-_x * sp.cos(_x) + sp.sin(_x), _x * sp.sin(_x)),
    "例題3 微分でもどる")
chk(sp.integrate(sp.sin(_x), _x) == -sp.cos(_x), "例題3 v = -cos x")
chk(sp.simplify(sp.integrate(_x * sp.sin(_x), _x)
                - (-_x * sp.cos(_x) + sp.sin(_x))) == 0, "例題3 答えが一致")
# 例題4
_ans4 = sp.exp(_x) * (_x ** 2 - 2 * _x + 2)
chk(back(_ans4, _x ** 2 * sp.exp(_x)), "例題4 微分でもどる")
chk(sp.simplify(sp.integrate(_x ** 2 * sp.exp(_x), _x) - _ans4) == 0,
    "例題4 答えが一致")
chk(sp.simplify(sp.integrate(2 * _x * sp.exp(_x), _x)
                - (2 * _x * sp.exp(_x) - 2 * sp.exp(_x))) == 0,
    "例題4 2 回目の積分")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
chk(back((_x ** 3 + 2) ** 5 / 5, 3 * _x ** 2 * (_x ** 3 + 2) ** 4), "演習1")
chk(back(sp.sin(_x) ** 4 / 4, sp.sin(_x) ** 3 * sp.cos(_x)), "演習2")
chk(sp.sin(sp.pi / 2) ** 4 / 4 == R(1, 4), "演習2 x=π/2 で 1/4")
chk(back(sp.exp(_x ** 2) / 2, _x * sp.exp(_x ** 2)), "演習3")
chk(back(sp.log(_x ** 2 + 1) / 2, _x / (_x ** 2 + 1)), "演習4")
chk(back(_x * sp.log(_x) - _x, sp.log(_x)), "演習5")
chk((_x * sp.log(_x) - _x).subs(_x, 1) == -1, "演習5 x=1 で -1")
chk(back(_x * sp.sin(_x) + sp.cos(_x), _x * sp.cos(_x)), "演習6")
chk(sp.integrate(_x * sp.exp(_x), (_x, 0, 1)) == 1, "演習7 定積分は 1")
chk(sp.simplify((sp.exp(_x) * (_x - 1)).subs(_x, 1)
                - (sp.exp(_x) * (_x - 1)).subs(_x, 0) - 1) == 0,
    "演習7 不定積分からも 1")
_I = sp.exp(_x) * (sp.sin(_x) - sp.cos(_x)) / 2
chk(back(_I, sp.exp(_x) * sp.sin(_x)), "演習8 微分でもどる")
chk(sp.simplify(sp.integrate(sp.exp(_x) * sp.sin(_x), _x) - _I) == 0,
    "演習8 答えが一致")
chk(sp.simplify(sp.integrate(sp.exp(_x) * sp.cos(_x), _x)
                - sp.exp(_x) * (sp.sin(_x) + sp.cos(_x)) / 2) == 0,
    "演習8 cos のほうも同じ形")
# 演習9
chk(sp.simplify(sp.integrate(_x ** 2 * sp.cos(_x) / 2, _x)
                - (_x ** 2 * sp.sin(_x) / 2 + _x * sp.cos(_x)
                   - sp.sin(_x))) == 0, "演習9 悪い選び方は次数が上がる")
# 演習10
chk(sp.simplify(sp.diff(_x * sp.exp(_x) + sp.exp(_x), _x)
                - (_x * sp.exp(_x) + 2 * sp.exp(_x))) == 0,
    "演習10 生徒の答えを微分すると xe^x + 2e^x")
chk(back(_x * sp.exp(_x) - sp.exp(_x), _x * sp.exp(_x)), "演習10 正しい答え")
chk(sp.simplify((_x * sp.exp(_x) + sp.exp(_x))
                - (_x * sp.exp(_x) - sp.exp(_x)) - 2 * sp.exp(_x)) == 0,
    "演習10 差は 2e^x で定数でない")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Integration by substitution.", "シラバス 1 行目を逐語で")
in_text("> On examination papers, substitutions will be provided if the"
        " integral is not of the form $\\int kg'(x) f (g(x))\\mathrm{d}x$.",
        "置換が与えられることを逐語で")
in_text("> Link to: integration by substitution (SL5.10).",
        "SL5.10 への Link を逐語で")
in_text("> Integration by parts.", "部分積分を逐語で")
in_text("> Repeated integration by parts.", "くり返しを逐語で")
in_text("> Examples: $\\int x\\sin x\\,\\mathrm{d}x$,"
        " $\\int \\ln x\\,\\mathrm{d}x$,"
        " $\\int \\arcsin x\\,\\mathrm{d}x$", "例を逐語で")
in_text("> Examples: $\\int x^{2}e^{x}\\mathrm{d}x$ and"
        " $\\int e^{x}\\sin x\\,\\mathrm{d}x$.", "くり返しの例を逐語で")
in_text("公式集の **5.16** の欄", "公式集の場所")
in_text("> Integration by parts", "公式集の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("integration by substitution, step by step", "図(a) の題")
in_fig("nothing in $x$ may be left behind", "図(a) の注")
in_fig("splits into two pieces", "図(b) の題")
in_fig("the whole rectangle is $uv$", "図(b) の注")
in_text("手順は $4$ つです。", "キャプション (a)")
in_text("が $2$ つに分かれます。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("\\sin^{4}x", "演習2"), ("\\sin x-\\cos x", "演習8")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl516-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl516", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-5-16-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-5-16-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/05-calculus/aahl-5-16.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(05-calculus/aahl-5-16.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| substitution |", "| integration by parts |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## $\\mathrm{d}x$ を置きかえない", "dx も置きかえる")
in_text("## 部分積分のマイナスを落とす", "符号")
in_text("## $u$ の選び方をまちがえる", "選び方")
in_text("## $\\ln x$ と $\\arcsin x$ は、積分できないほうです", "u に置く")
in_text("**$x$ が $1$ つでも残っていたら、まだ終わっていません。**", "x を残さない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
