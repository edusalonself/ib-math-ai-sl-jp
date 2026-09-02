# 公開の手順（GitHub Pages）

このサイトは **GitHub Pages** で無料公開しています。
更新は最後の【D. 2回目以降】だけ読めば足ります。

---

## 前提

- Mac に **Quarto** と **git** が入っていること（Positron に付いています）
- GitHub の無料アカウント … <https://github.com/signup>

---

## A. 最初の1回だけ：GitHub にリポジトリを作る

### A-1. GitHub の画面で新しいリポジトリを作る

<https://github.com/new> を開いて、

| 項目 | 入れるもの |
|---|---|
| Repository name | `ib-math-ai-sl-jp` |
| 公開設定 | **Public**（Private だと無料では Pages が使えません） |
| Add a README file | **チェックしない** |
| .gitignore / license | **どちらも None** |

`Create repository` を押します。

次の画面に出てくる URL は `https://github.com/edusalonself/ib-math-ai-sl-jp.git` になります。

### A-2. Positron のターミナルで、手元のフォルダをつなぐ

**手元の git リポジトリは、すでに作って最初のコミットまで済ませてあります。**
（47ファイル。IBO の PDF は除外済み。）ですから、つなぐ作業だけです。

Positron でこのフォルダを開き、**ターミナル**（Terminal タブ）で1行ずつ実行します。

```bash
git remote add origin https://github.com/edusalonself/ib-math-ai-sl-jp.git
git branch -M main
git push -u origin main
```

初回はユーザー名とパスワードを聞かれます。
**パスワード欄には、GitHub のログインパスワードではなく [Personal Access Token](https://github.com/settings/tokens) を貼ります**（`repo` にチェックを入れて作成）。

---

## B. 最初の1回だけ：サイトを公開する

ターミナルで、

```bash
quarto publish gh-pages
```

`Publish site? (Y/n)` と聞かれたら `Y` を押します。
レンダリングが走り、`gh-pages` というブランチに公開用ファイルが送られます。

終わると URL が表示されます。

```
https://edusalonself.github.io/ib-math-ai-sl-jp/
```

**この URL が本のアドレスです。**

### B-1. 表示されなかったとき

数分待っても 404 なら、GitHub の

`リポジトリ → Settings → Pages`

で、`Source` が **Deploy from a branch**、`Branch` が **gh-pages / (root)** になっているか確認してください。
違っていたら直して `Save` を押します。反映まで1〜2分かかります。

---

## C. 最初の1回だけ：Wix からリンクする

Wix エディタで、

1. 左メニューの **メニューとページ** を開く
2. **+ メニュー項目を追加** → **リンク**
3. **ウェブアドレス** を選び、B で出た URL を貼る
4. **新しいタブで開く** にチェック
5. 名前を「IB数学 AI SL 解説（無料）」などにする
6. **公開** を押す

Services の「IBDP数学」のページに、同じリンクのボタンを置いてもよいです。

---

## D. 2回目以降：更新のしかた

ページを書き足したら、ターミナルで **この2つだけ**です。

```bash
git add -A
git commit -m "SL 2.1 を追加"
git push

quarto publish gh-pages
```

上の3行が「原稿の保存」、最後の1行が「サイトへの反映」です。
`git push` を忘れても サイトは更新されますが、**原稿のバックアップが残らない**ので、両方やってください。

### 書きかけのコースも GitHub には上がります（2026年9月に確認）

`git add -A` は、**AI HL の書きかけページも GitHub に送ります。**

- **サイトには出ません。** `_quarto.yml` の `render` に入っていないので、HTML すら作られません。
- ただし **リポジトリは Public** なので、GitHub 上では `.qmd` のソースが誰でも読めます。

**これでよい、と決めました。** 書きかけが人目に触れるより、**原稿が GitHub にバックアップされているほうが安全**だからです。

もし将来、書きかけを隠したくなったら、`git add -A` のかわりに公開分だけを指定します。

```bash
git add ai-sl glossary-ai.qmd index.qmd _quarto.yml styles.scss PUBLISH.md .gitignore
```

---

## D-2. 下書きを手元だけで見る

**まだ書きかけのコース**（AI HL / AA SL / AA HL）は `_quarto-draft.yml` に書いてあります。

```bash
quarto preview --profile draft     # ← 書きかけのコースも見える
quarto preview                     # ← 公開するものだけ
```

`--profile draft` を付けると、ナビバーに **AI HL / AA SL / AA HL** と
**「AI と AA、どちらを取るか」** が増え、それぞれのサイドバーが見られます。

**`quarto publish gh-pages` には profile を付けません。** ですから
**書きかけのコースが誤って公開されることはありません。**

そのコースを公開する段になったら、`_quarto-draft.yml` から
navbar の項目と sidebar のかたまりを切り取って、`_quarto.yml` の
該当箇所に貼ります。

---

### AI SL について（2026年8月に変わりました）

**AI SL の39項目は、もう `_quarto.yml` に入っています。**
以前は Topic 2〜5 を `_quarto-draft.yml` に隠していましたが、
全項目を無料公開する方針に決めたので、その仕組みは畳みました。

ただし **公開はまだしていません。** 上の `quarto publish gh-pages` を
実行するまで、オンラインに出ているのは Topic 1 の8項目だけです。
手元でビルドしたものと、公開されているものは、いまは違います。

---

### 新しい項目を足すときに忘れやすいこと

`_quarto.yml` の sidebar に行を足さないと、ファイルを書いてもサイドバーに出ません。
**パスの先頭にコース名が付く**ことに注意してください。

```yaml
            - file: ai-sl/02-functions/sl-2-1.qmd
              text: "SL 2.1 — Equations of a straight line"
```

図を作る Python も、コースごとに分けてあります。

```bash
python3 figs/ai-sl/make_sl_5_8.py     # → ai-sl/05-calculus/img/*.svg
```

---

## E. あとで：math.selfsg.com にする

URL を `edusalonself.github.io/...` から `math.selfsg.com` に変えられます。無料です。

1. GitHub の `リポジトリ → Settings → Pages → Custom domain` に `math.selfsg.com` と入れて `Save`
2. Wix の管理画面で **ドメイン → ドメインのアクション → DNSレコードを管理**
3. **CNAME（エイリアス）** に1件追加
   - ホスト名 … `math`
   - 値 … `edusalonself.github.io`
4. 保存（反映に最大48時間）
5. GitHub Pages の画面に戻り、**Enforce HTTPS** にチェック
6. Wix のメニューのリンク先を、新しい URL に差し替える

**注意**：この方法が使えるのは、selfsg.com のDNSを Wix 側で管理している場合です。
「ネームサーバー方式」ではなく「ポインティング方式」で他社から接続していると、CNAME を足せません。

---

## 公開してはいけないもの

`.gitignore` で次のものを除外しています。**この設定は消さないでください。**

- **`*.pdf`** … IBO のシラバスと公式集。**再配布は著作権に触れます。**
- `_site/`、`.quarto/` … 生成物（`quarto publish` が別ルートで送ります）
- `*プレビュー.html`、`*_preview.zip` … 手元の確認用
- `.DS_Store`

除外できているかは、コミット前にこれで確認できます。

```bash
git status --short
```

`.pdf` が一覧に出てきたら、**コミットしないでください。**
