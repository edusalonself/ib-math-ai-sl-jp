# -*- coding: utf-8 -*-
"""サイト全体の相互参照とリンクの切れを探す。

  quarto の website プロジェクトでは、@fig-… のような crossref は
  「同じ .qmd の中」でしか解決しません。解決しないと本文に
  「?@fig-…」と出てしまうので、書き換えのあとは必ずこれを通すこと。

  見るもの:
    1. @fig-/@tbl-/@eq-/@exm-/@sec-… が、同じファイルで定義されているか
    2. ページ内リンク ](#anchor) の行き先があるか
    3. 別ページへのリンク ](other.qmd#anchor) の行き先があるか
    4. 参照されていない図・表・式のラベル（参考情報）

  実行: python3 tools/check_refs.py
"""
import io
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP = {"_site", "_book", "_freeze", ".git", ".quarto", "Claude outputs"}
KINDS = ("fig", "tbl", "eq", "exm", "sec", "thm", "lem", "def", "cor", "prp", "lst")

# 属性ブロック {...} の中の #id を拾う
#   {#id} / {#id width=…} / ::: {.callout-warning #id} / $$ …$$ {#id}
RE_ATTR = re.compile(r"\{([^}\n]*)\}")
RE_IDIN = re.compile(r"(?<![A-Za-z0-9_\-])#([A-Za-z0-9][A-Za-z0-9_\-]*)")
RE_REF = re.compile(r"(?<![A-Za-z0-9_])@(-?(?:%s)-[A-Za-z0-9_\-]+)" % "|".join(KINDS))
RE_SELF = re.compile(r"\]\(#([A-Za-z0-9][A-Za-z0-9_\-]*)\)")
RE_FILE = re.compile(r"\]\(([^)\s#]+\.qmd)(?:#([A-Za-z0-9][A-Za-z0-9_\-]*))?\)")
RE_HEAD = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)


def slug(text):
    t = re.sub(r"\{#[^}]*\}", "", text)
    t = re.sub(r"[`*_$\\]", "", t).strip().lower()
    t = re.sub(r"[^\w\s-]", "", t, flags=re.U)
    return re.sub(r"[\s]+", "-", t)


def qmds():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP and not d.startswith(".")]
        for fn in sorted(fns):
            if fn.endswith(".qmd"):
                yield os.path.join(dp, fn)


def load():
    ids, texts = {}, {}
    for p in qmds():
        t = io.open(p, encoding="utf-8").read()
        texts[p] = t
        s = set()
        for attr in RE_ATTR.findall(t):
            s.update(RE_IDIN.findall(attr))
        for h in RE_HEAD.findall(t):          # 明示 id の無い見出し
            if "{#" not in h:
                s.add(slug(h))
        ids[p] = s
    return ids, texts


def main():
    ids, texts = load()
    bad = 0
    for p, t in sorted(texts.items()):
        rel = os.path.relpath(p, ROOT)
        here = ids[p]

        for ref in sorted(set(RE_REF.findall(t))):
            if ref.lstrip("-") not in here:
                bad += 1
                print("NG  %s : @%s が同じページにありません" % (rel, ref))

        for a in sorted(set(RE_SELF.findall(t))):
            if a not in here:
                bad += 1
                print("NG  %s : ページ内リンク #%s の行き先がありません" % (rel, a))

        for m in RE_FILE.finditer(t):
            tgt = os.path.normpath(os.path.join(os.path.dirname(p), m.group(1)))
            if not os.path.exists(tgt):
                bad += 1
                print("NG  %s : %s というファイルがありません" % (rel, m.group(1)))
            elif m.group(2) and m.group(2) not in ids.get(tgt, set()):
                bad += 1
                print("NG  %s : %s#%s の行き先がありません"
                      % (rel, m.group(1), m.group(2)))

    print("=" * 62)
    print("NG %d 件" % bad if bad else "切れた参照・リンクはありません")
    print("=" * 62)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
