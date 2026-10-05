"""AA HL HL 4.13 — Bayes' theorem の内容を検算する。

    python3 figs/aa-hl/check_aahl_4_13.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "04-statistics-and-probability")
QMD = os.path.join(BASE, "aahl-4-13.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_4_13.py"), encoding="utf-8").read()
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



R = sp.Rational


def bayes(pr, cond):
    """分子と分母を返す。pr[i] = P(B_i)、cond[i] = P(A|B_i)。"""
    num = [pr[i] * cond[i] for i in range(len(pr))]
    return num, sum(num)


# ══════════════════════════════════════════════════════════
# 0. 記号のままの性質
# ══════════════════════════════════════════════════════════
_pb, _ab, _ac = sp.symbols("pb ab ac", positive=True)
_den = _pb * _ab + (1 - _pb) * _ac
_bayes = _pb * _ab / _den
# 条件つき確率の定義と同じ
chk(sp.simplify(_bayes - (_pb * _ab) / _den) == 0, "Bayes は分子/分母")
# 2 つの答えを足すと 1
chk(sp.simplify(_bayes + (1 - _pb) * _ac / _den - 1) == 0,
    "P(B|A) + P(B'|A) = 1")
# 独立なら P(B|A) = P(B)
chk(sp.simplify(_bayes.subs(_ac, _ab) - _pb) == 0, "独立なら P(B|A) = P(B)")
# 0 以上 1 以下
chk(sp.simplify(_den - _pb * _ab).is_nonnegative is not False,
    "分子は分母以下")
# 全確率の法則
_A, _B = sp.symbols("PA PB", positive=True)
_AB = sp.Symbol("PAB", positive=True)
chk(sp.simplify((_AB / _A) * _A - _AB) == 0, "P(B|A)·P(A) = P(A∩B)")
chk(sp.simplify((_AB / _B) - (_AB / _B)) == 0, "P(A|B) の定義")
# P(A|B) と P(B|A) が一致するのは P(A)=P(B) のとき
chk(sp.solve(sp.Eq(_AB / _A, _AB / _B), _A) == [_B],
    "2 つが一致するのは P(A) = P(B) のときだけ")
# 3 分岐でも和は 1
_p1, _p2, _p3, _c1, _c2, _c3 = sp.symbols("p1 p2 p3 c1 c2 c3", positive=True)
_d3 = _p1 * _c1 + _p2 * _c2 + _p3 * _c3
chk(sp.simplify((_p1 * _c1 + _p2 * _c2 + _p3 * _c3) / _d3 - 1) == 0,
    "3 分岐でも割合の和は 1")

# ══════════════════════════════════════════════════════════
# 1. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_n1, _t1 = bayes([R(6, 10), R(4, 10)], [R(5, 100), R(10, 100)])
chk(_n1[0] == R(3, 100) and _n1[1] == R(4, 100), "例題1 0.03 と 0.04")
chk(_t1 == R(7, 100), "例題1 分母 0.07")
chk(_n1[0] / _t1 == R(3, 7), "例題1 答え 3/7")
chk(_n1[1] / _t1 == R(4, 7), "例題1 もう片方 4/7")
chk(_n1[0] / _t1 + _n1[1] / _t1 == 1, "例題1 足して 1")
# 例題2
_n2, _t2 = bayes([R(1, 100), R(99, 100)], [R(99, 100), R(5, 100)])
chk(_n2[0] == R(99, 10000), "例題2 0.0099")
chk(_n2[1] == R(495, 10000), "例題2 0.0495")
chk(_t2 == R(594, 10000), "例題2 分母 0.0594")
chk(_n2[0] / _t2 == R(1, 6), "例題2 答え 1/6")
chk(_n2[0] * 6 == _t2, "例題2 6 倍すると分母")
# 例題3
_n3, _t3 = bayes([R(5, 10), R(3, 10), R(2, 10)],
                 [R(2, 100), R(4, 100), R(5, 100)])
chk([_n3[0], _n3[1], _n3[2]] == [R(1, 100), R(12, 1000), R(1, 100)],
    "例題3 0.010, 0.012, 0.010")
chk(_t3 == R(32, 1000), "例題3 分母 0.032")
chk(_n3[1] / _t3 == R(3, 8), "例題3 答え 3/8")
chk(_n3[0] / _t3 == R(5, 16) and _n3[2] / _t3 == R(5, 16), "例題3 残りは 5/16")
chk(sum(_n3) / _t3 == 1, "例題3 3 つ足すと 1")
chk(R(2, 100) < _t3 < R(5, 100), "例題3 分母は 2% と 5% の間")
# 例題4
_n4, _t4 = bayes([R(1, 2), R(1, 2)], [R(3, 5), R(1, 5)])
chk(_n4[0] == R(3, 10) and _n4[1] == R(1, 10), "例題4 3/10 と 1/10")
chk(_t4 == R(2, 5), "例題4 分母 2/5")
chk(_n4[0] / _t4 == R(3, 4), "例題4 答え 3/4")
chk(R(1, 5) < _t4 < R(3, 5), "例題4 分母は 1/5 と 3/5 の間")
chk(R(3, 4) > R(1, 2), "例題4 もとの見込みより上がる")

# ══════════════════════════════════════════════════════════
# 2. 演習
# ══════════════════════════════════════════════════════════
# 演習1
_q1, _s1 = bayes([R(3, 10), R(7, 10)], [R(4, 10), R(2, 10)])
chk(_q1[0] == R(12, 100) and _q1[1] == R(14, 100), "演習1 0.12 と 0.14")
chk(_s1 == R(26, 100), "演習1 分母 0.26")
chk(_q1[0] / _s1 == R(6, 13), "演習1 答え 6/13")
chk(_q1[1] / _s1 == R(7, 13), "演習1 もう片方 7/13")
# 演習2
_q2, _s2 = bayes([R(1, 4), R(3, 4)], [R(8, 10), R(1, 10)])
chk(_q2[0] == R(2, 10) and _q2[1] == R(75, 1000), "演習2 0.2 と 0.075")
chk(_s2 == R(275, 1000), "演習2 分母 0.275")
chk(_q2[0] / _s2 == R(8, 11), "演習2 答え 8/11")
chk(R(200, 275) == R(8, 11), "演習2 200/275 の約分")
chk(R(8, 11) > R(1, 4), "演習2 見込みが上がる")
# 演習3
chk(_s1 == R(26, 100), "演習3 P(A) = 0.26")
chk(R(2, 10) < _s1 < R(4, 10), "演習3 0.2 と 0.4 の間")
chk(R(3, 10) * R(4, 10) + R(7, 10) * R(2, 10) == R(26, 100),
    "演習3 重みつき平均")
# 演習4
_q4, _s4 = bayes([R(2, 10), R(5, 10), R(3, 10)],
                 [R(1, 10), R(2, 10), R(4, 10)])
chk([_q4[0], _q4[1], _q4[2]] == [R(2, 100), R(10, 100), R(12, 100)],
    "演習4 0.02, 0.10, 0.12")
chk(_s4 == R(24, 100), "演習4 分母 0.24")
chk(_q4[2] / _s4 == R(1, 2), "演習4 答え 1/2")
chk(_q4[0] / _s4 == R(1, 12) and _q4[1] / _s4 == R(5, 12), "演習4 残りは 1/12 と 5/12")
chk(sum(_q4) / _s4 == 1, "演習4 3 つ足すと 1")
chk(R(1, 2) > R(3, 10), "演習4 見込みが上がる")
# 演習5
_q5, _s5 = bayes([R(1, 10), R(9, 10)], [R(9, 10), R(2, 10)])
chk(_q5[0] == R(9, 100) and _q5[1] == R(18, 100), "演習5 0.09 と 0.18")
chk(_s5 == R(27, 100), "演習5 分母 0.27")
chk(_q5[0] / _s5 == R(1, 3), "演習5 答え 1/3")
chk(R(1, 3) > R(1, 10), "演習5 見込みが上がる")
# 演習6
_q6, _s6 = bayes([R(7, 10), R(3, 10)], [R(1, 100), R(5, 100)])
chk(_q6[0] == R(7, 1000) and _q6[1] == R(15, 1000), "演習6 0.007 と 0.015")
chk(_s6 == R(22, 1000), "演習6 分母 0.022")
chk(_q6[1] / _s6 == R(15, 22), "演習6 答え 15/22")
chk(_q6[0] / _s6 == R(7, 22), "演習6 もう片方 7/22")
chk(R(1, 100) < _s6 < R(5, 100), "演習6 分母は 1% と 5% の間")
chk(R(15, 22) > R(3, 10), "演習6 生産の割合より大きい")
# 演習7
chk(sp.simplify(_bayes.subs(_ac, _ab) - _pb) == 0, "演習7 独立なら P(B)")
chk(sp.simplify((_pb * _ab) / _ab - _pb) == 0, "演習7 定義から直接でも P(B)")
chk(R(1, 6) == R(1, 6), "演習7 さいころの例")
# 演習8
_q8, _s8 = bayes([R(1, 2), R(1, 2)], [1, R(1, 2)])
chk(_q8[0] == R(1, 2) and _q8[1] == R(1, 4), "演習8 1/2 と 1/4")
chk(_s8 == R(3, 4), "演習8 分母 3/4")
chk(_q8[0] / _s8 == R(2, 3), "演習8 答え 2/3")
chk(_q8[1] / _s8 == R(1, 3), "演習8 もう片方 1/3")
chk(R(2, 3) > R(1, 2) and R(2, 3) < 1, "演習8 上がるが 1 にはならない")
# 演習9
chk(sp.simplify(_den - (_pb * _ab + (1 - _pb) * _ac)) == 0, "演習9 分母は 2 項の和")
chk(sp.simplify(_d3 - (_p1 * _c1 + _p2 * _c2 + _p3 * _c3)) == 0,
    "演習9 3 分岐なら 3 項")
# 演習10
chk(_n2[0] / _t2 != R(99, 100), "演習10 感度と混同してはいけない")
chk(sp.solve(sp.Eq(_AB / _A, _AB / _B), _A) == [_B],
    "演習10 一致するのは P(A) = P(B) のときだけ")
_half = bayes([R(1, 2), R(1, 2)], [R(95, 100), R(5, 100)])
chk(_half[0][0] / _half[1] == R(19, 20), "演習10 病気が半数なら 0.95 に近づく")

# ══════════════════════════════════════════════════════════
# 3. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Use of Bayes' theorem for a maximum of three events.",
        "シラバスを逐語で")
in_text("> Link to: independent events (SL4.6).", "Link to を逐語で")
in_text("公式集の **4.13** の欄", "公式集の場所")
in_text("> Bayes' theorem", "公式集の見出しを逐語で")

# ══════════════════════════════════════════════════════════
# 4. 図と、答えの漏れ
# ══════════════════════════════════════════════════════════
in_fig("two paths lead to $A$", "図(a) の題")
in_fig("the numerator is the path through $B$ only", "図(a) の注")
in_fig("is the share of the shaded area on the left", "図(b) の題")
in_fig("a narrow left column can still hold less shaded area", "図(b) の注")
in_text("$A$ に着く道は $2$ 本あります。", "キャプション (a)")
in_text("は、影の面積のうち左側の割合です。", "キャプション (b)")
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("\\frac{6}{13}", "演習1"),
                    ("\\frac{15}{22}", "演習6")]:
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
chk(len(re.findall(r"^::: \{#exm-aahl413-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aahl413", "他ページの @-ref: " + _r0)
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
    _p = os.path.join(BASE, "img", "aahl-4-13-idea-%s.svg" % _n)
    chk(os.path.exists(_p), "図 (%s) がある" % _n)
    chk("](img/aahl-4-13-idea-%s.svg)" % _n in TEXT,
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
chk("aa-hl/04-statistics-and-probability/aahl-4-13.qmd" in DRAFT, "draft に登録")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aahl-4-13.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)) == len(_written),
    "✅ の数とページ数が合う")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written), "PLAN の進捗")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| conditional probability |", "| independent events |",
          "| Bayes' theorem |", "| law of total probability |"]:
    chk(t in GLO, "対訳表にある: " + t)

# ══════════════════════════════════════════════════════════
# 見張り
# ══════════════════════════════════════════════════════════
in_text("## 分母を書かずに、分子だけで答える", "割るところまで")
in_text("## 分母に $P(B')P(A \\mid B')$ を足し忘れる", "道は全部足す")
in_text("## 答えが $1$ を超えても気づかない", "範囲の検算")
in_text("**縦棒の右が「分かっていること」**です", "縦棒の右")
in_text("**新しい式ではありません。**", "定義の書き直し")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
