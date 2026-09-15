# tools/ — 執筆中の検査に使う小道具

新しいチャット（新しいコンテナ）でも、そのまま使えるようにここに置いてあります。
以前は `/tmp` に置いていましたが、セッションが変わると消えてしまうためです。

## 先に入れるもの

```bash
npm install -g katex playwright
```

Chromium は `/opt/pw-browsers/chromium` に入っているので、
`playwright install` は**実行しないでください**（環境変数で解決されます）。

`require(...)` のパスが合わないときは、各ファイルの先頭の
`/home/claude/.npm-global/lib/node_modules/...` を、その環境の
`npm root -g` の出力に書き換えてください。

## 3 つの道具

### 1. mathcheck.js — KaTeX が読めるかを全式について確かめる

```bash
node tools/mathcheck.js ai-hl/03-geometry-and-trigonometry/ahl-3-13b.qmd
```

`$…$` と `$$…$$` を全部抜き出して KaTeX に通します。
**0 failed でなければ、レンダーしても数式が出ません。**

よく出るもの:

- `✓` `✗` `①` `②` に KaTeX のメトリクスがない → **数式の外に出す**
- `\lvert` `\rvert` は使えます（matplotlib では使えません。下記）

★ 2026-09: **通貨の `\$`**（`$\$2000$` のような書き方）が数式の区切りと
取りちがえられ、誤検出になっていました。いまは `mathcheck.js` と `mathwidth.js` の
両方で、先に別の文字へ置き換えてから数式を取り出しています。

### 2. mathwidth.js — 表示数式が読める幅に収まっているか

```bash
node tools/mathwidth.js ai-hl/03-geometry-and-trigonometry/ahl-3-13b.qmd
```

既定は 700 px（本文の幅）。第 2 引数で変えられます。
はみ出す式は、スマホで横スクロールになります。

### 3. svg2png.js — 図を目で見るために PNG に落とす

```bash
node tools/svg2png.js /root/book/ai-hl/.../img/xxx.svg
```

**絶対パスで渡してください。** `.svg` の隣に `.png` を書きます。
そのあと Read ツールで PNG を開いて、**実際に目で見ます。**

**確認が終わったら PNG を消してください**（リポジトリに入れません）。

```bash
rm -f ai-hl/**/img/*.png
```

## 図を作るときの、matplotlib の制限

`figs/ai-hl/make_*.py` で使っている mathtext には、次の制限があります。

- `\begin{pmatrix}` は**読めません** → `\binom{a}{b}` を使う
- `\lvert` `\rvert` も**読めません** → `|` を使う
- `\overrightarrow` `\vec` `\mathbf` `\hat` `\sqrt` `\binom` は使えます

日本語のグリフはありません。**図のラベルはすべて英語**です。
