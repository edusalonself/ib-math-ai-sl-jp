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

次の画面に出てくる URL（`https://github.com/○○○/ib-math-ai-sl-jp.git`）を控えてください。
`○○○` があなたの GitHub ユーザー名です。

### A-2. Positron のターミナルで、手元のフォルダをつなぐ

**手元の git リポジトリは、すでに作って最初のコミットまで済ませてあります。**
（47ファイル。IBO の PDF は除外済み。）ですから、つなぐ作業だけです。

Positron でこのフォルダを開き、**ターミナル**（Terminal タブ）で1行ずつ実行します。

```bash
git remote add origin https://github.com/○○○/ib-math-ai-sl-jp.git
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
https://○○○.github.io/ib-math-ai-sl-jp/
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

---

## D-2. 下書きを手元だけで見る

**まだ公開したくないページ**は `_quarto-draft.yml` に書いてあります。

```bash
quarto preview --profile draft     # ← 下書きも見える
quarto preview                     # ← 公開されるものだけ
```

`--profile draft` を付けると、サイドバーの一番下に
**「下書き（まだ公開していません）」**という区分が出て、その中に入ります。

**`quarto publish gh-pages` には profile を付けません。** ですから
**下書きが誤って公開されることはありません。**

公開する段になったら、

1. `_quarto-draft.yml` からその行を消す
2. `_quarto.yml` の該当行のコメント（`# `）を外す
3. `index.qmd` の「いまは執筆中です」の項目数を直す

の3つをやります。

---

### 新しい項目を公開するときに忘れやすいこと

`_quarto.yml` の該当行が **コメントアウトされたまま**だと、書いてもサイドバーに出ません。

```yaml
        # - file: 02-functions/sl-2-1.qmd
        #   text: "SL 2.1 — Equations of a straight line"
```

先頭の `# ` を2行とも外してください。
その Topic 全体がコメントアウトされている場合は、`- part:` の行も戻します。

`index.qmd` の「いまは執筆中です」の項目数も、あわせて直します。

---

## E. あとで：math.selfsg.com にする

URL を `○○○.github.io/...` から `math.selfsg.com` に変えられます。無料です。

1. GitHub の `リポジトリ → Settings → Pages → Custom domain` に `math.selfsg.com` と入れて `Save`
2. Wix の管理画面で **ドメイン → ドメインのアクション → DNSレコードを管理**
3. **CNAME（エイリアス）** に1件追加
   - ホスト名 … `math`
   - 値 … `○○○.github.io`
4. 保存（反映に最大48時間）
5. GitHub Pages の画面に戻り、**Enforce HTTPS** にチェック
6. Wix のメニューのリンク先を、新しい URL に差し替える

**注意**：この方法が使えるのは、selfsg.com のDNSを Wix 側で管理している場合です。
「ネームサーバー方式」ではなく「ポインティング方式」で他社から接続していると、CNAME を足せません。

---

## 公開してはいけないもの

`.gitignore` で次のものを除外しています。**この設定は消さないでください。**

- **`*.pdf`** … IBO のシラバスと公式集。**再配布は著作権に触れます。**
- `_book/`、`.quarto/` … 生成物（`quarto publish` が別ルートで送ります）
- `*プレビュー.html`、`*_preview.zip` … 手元の確認用
- `.DS_Store`

除外できているかは、コミット前にこれで確認できます。

```bash
git status --short
```

`.pdf` が一覧に出てきたら、**コミットしないでください。**
