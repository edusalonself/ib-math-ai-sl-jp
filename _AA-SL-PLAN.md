# AA SL — ページ一覧（執筆計画）

シラバス `5. (Subject guide) mathematics-analysis-and-approaches-guide-en ... copy 2.pdf`
（74 ページ、first assessment 2021）の Content / Guidance 欄から起こしました。
公式集は `2.Math AA SL formula booklet(New) copy.pdf`（10 ページ、SL の欄のみ）を使います。

- **シラバス項目：51**（SL 1.1–1.9 / 2.1–2.11 / 3.1–3.8 / 4.1–4.12 / 5.1–5.11）
- **ページ数：60**（うち 9 項目を a / b に分割）
- ファイル名の接頭辞は `aasl-`。AI SL の `sl-1-1.qmd` とアンカーが衝突しないようにします
  （見出しは `{#sec-aasl-1-1}`、参照は `@eq-aasl11-...`、図は `figs/aa-sl/make_aasl_1_1.py`）。

## 決まっていること

### ページの形（AI 版から変えました。詳しくは `_AA-START-HERE.md` 第 3 節）

生徒が**上から読んで、そのまま理解できる**ことを最優先にします。

```
# SL X.Y — English title（日本語）

::: {.callout-note} ## What you should be able to do :::   ← 読む前の地図

## The idea          ← 公式が出た直後に「公式集にあります／ありません」を差し込む
                        電卓が要る場面に、その場で折りたたみの callout を差し込む
## Why it works
## Worked examples
## Common errors
[## Using your GDC]  ← 統計など、操作が長い項目だけ
## Exercises

::: {.callout-note collapse="true"} ## 参考：この項目のシラバス（原文） :::   ← 末尾
```

- **冒頭に公式集の表を置きません。** 何の話か分からない段階で式を見せないためです。
- **シラバスの英語の引用は末尾に折りたたみます。** ただし `Not required:` は本文にも書きます。
- **GDC の独立した節は原則なし。** 電卓は Paper 1 で使えないので、本筋ではなく補助です。
  見出しは「**Paper 2 では、電卓でこう出せます**」で始め、`collapse="true"` を付けます。
- **例外**：シラバスが `must be found using technology` と書いている統計の項目
  （SL 4.3・4.4・4.8・4.9・4.12）では、Exercises の前に `## Using your GDC` を置きます。

### そのほか

- **AI SL と共通の 26 項目**（SL 1.1–1.5, 2.1–2.4, 3.1–3.3, 4.1–4.9, 5.1–5.5）も、
  ページは新しく書く。流用するのは数学の説明の骨格だけ。
- `glossary-aa.qmd` を新しく作る（AI 版とは分ける）。
- サイドバーは `_quarto-draft.yml` に `aa-sl` として登録する。公開用の `_quarto.yml` は触らない。

---

## 進捗（2026-09-08 現在）

**AA SL は 全 60 ページが完成しました（Topic 1 から Topic 5 まで）。**

### 2026-09-09 の変更指示（35 項目）— 完了

1.9 と Topic 2〜4 について、M01〜M13（数学・答えの誤り）・C01〜C12（前提と表現）・
E01〜E10（演習と図）の 35 項目をすべて実装しました。
何をどう直したかは `_AA-SL-変更指示-完了報告.md` にまとめてあります。

- 演習の差し替え・小問追加は 10 か所（各ページ 10 問は維持）
- 解答用の図を 13 点追加（`figs/aa-sl/make_aasl_*_ex*.py` など）
- 検算は削除せず、修正後の内容に対応する形へ置きかえたうえで、
  数値・性質・構造を sympy で確かめる検算を追加
- checker 36 ページ NG 0 ／ mathcheck 0 failed ／ 変更 27 ページの
  `quarto render --profile draft` 成功 ／ リンク切れ・未解決参照 0
- 公開・デプロイは行っていません
次は AA HL です。

| Topic | ページ | 状態 |
|:--|--:|:--|
| Topic 1 — Number and algebra | 10 | ✅ 完成（検証ずみ） |
| Topic 2 — Functions | 12 | ✅ 完成（検証ずみ） |
| Topic 3 — Geometry and trigonometry | 10 | ✅ 完成（検証ずみ） |
| Topic 4 — Statistics and probability | 13 | ✅ 完成（検証ずみ） |
| Topic 5 — Calculus | 15 | ✅ 完成（検証ずみ） |

検証結果（全 60 ページ、2026-09-08）。

- `figs/aa-sl/check_aasl_*.py` … 合計 **42,433 項目 / NG 0**
  - Topic 1（10 ページ）… 10,049 項目
  - Topic 2（12 ページ）… 11,397 項目
  - Topic 3（10 ページ）… 9,905 項目
  - Topic 4（13 ページ）… 7,578 項目
  - Topic 5（15 ページ）… 3,499 項目
- `tools/mathcheck.js` … 全ページ 0 failed（Topic 5 は 8,248 式）
- `tools/mathwidth.js` … 700px を超える表示数式 0
- `quarto render --profile draft` … 全ページでエラー・警告なし
  （※ 1 ページずつのレンダーです。公開前に、全体を通したレンダーを一度かけてください）
- リンク検査 … AA SL 全 60 ページで、未解決の相互参照 0・壊れたリンク 0
  （このとき見つかった `aasl-2-8`・`aasl-2-9` から `aasl-2-5.qmd#inverse` への
  リンク切れ 8 か所を `#find-inverse` に、`aasl-2-4.qmd#intercepts` を `#zeros` に直しました）

**各ページは opus のレビューを 1 回通し、指摘をすべて反映してあります。**
何を直したかは、各ページの `check_aasl_*.py` の末尾
「査読で直したところ」の節に、文字列の釘として残してあります。

Topic 3 でレビューが見つけた主なもの（すべて修正ずみ）。

- SL 3.4 … 「$\theta > \pi$ でも弦が扇形を $2$ つに分ける」は偽（優弧の扇形では弦が外側）
- SL 3.5b … 図の SSA の配置が本文の代数（$a$, $b$, $\hat{A}$）と別物だった
- SL 3.7a … 「グラフをかく」が第 1 の目標なのに、かかせる問いが $1$ つもなかった
- SL 3.8 … §6 と Why it works が例題 4 の答えをそのまま出していた／
  $b(x+c)$ の形を目標に挙げながら、例題にも演習にも出ていなかった

---

## Topic 1 — Number and algebra（9 項目 → 10 ページ）

| 項目 | ページの見出し | ファイル |
|:--|:--|:--|
| SL 1.1 | Numbers in standard form（指数表記・標準形） | `aasl-1-1.qmd` |
| SL 1.2 | Arithmetic sequences and series（等差数列と等差級数） | `aasl-1-2.qmd` |
| SL 1.3 | Geometric sequences and series（等比数列と等比級数） | `aasl-1-3.qmd` |
| SL 1.4 | Financial applications of geometric sequences（複利・減価償却・実質価値） | `aasl-1-4.qmd` |
| SL 1.5 | Laws of exponents and introduction to logarithms（整数の指数法則と対数の導入） | `aasl-1-5.qmd` |
| SL 1.6 | Simple deductive proof（簡単な演繹的証明 — LHS から RHS へ） | `aasl-1-6.qmd` |
| **SL 1.7a** | Laws of exponents with rational exponents（有理数の指数） | `aasl-1-7a.qmd` |
| **SL 1.7b** | Laws of logarithms, change of base and exponential equations（対数法則・底の変換・指数方程式） | `aasl-1-7b.qmd` |
| SL 1.8 | The sum of an infinite convergent geometric series（無限等比級数の和） | `aasl-1-8.qmd` |
| SL 1.9 | The binomial theorem（二項定理） | `aasl-1-9.qmd` |

**1.7 を分ける理由。** Content 欄に「rational exponents」「laws of logarithms」「change of base」
「solving exponential equations」の 4 つが並んでいます。Paper 1 が電卓なしなので、
$16^{3/4}$ の手計算と、対数法則の変形は、それぞれ例題 4 本ぶんの中身があります。

---

## Topic 2 — Functions（11 項目 → 12 ページ）

| 項目 | ページの見出し | ファイル |
|:--|:--|:--|
| SL 2.1 | Different forms of the equation of a straight line（直線の方程式） | `aasl-2-1.qmd` |
| SL 2.2 | Functions, domain, range and inverse functions（関数・定義域・値域・逆関数） | `aasl-2-2.qmd` |
| SL 2.3 | The graph of a function（グラフをかく — draw と sketch） | `aasl-2-3.qmd` |
| SL 2.4 | Key features of graphs（グラフの重要な特徴） | `aasl-2-4.qmd` |
| SL 2.5 | Composite functions and inverse functions（合成関数と逆関数） | `aasl-2-5.qmd` |
| SL 2.6 | The quadratic function and its three forms（2 次関数の 3 つの形） | `aasl-2-6.qmd` |
| **SL 2.7a** | Solving quadratic equations and inequalities（2 次方程式・2 次不等式を解く） | `aasl-2-7a.qmd` |
| **SL 2.7b** | The discriminant and the nature of the roots（判別式と解の種類） | `aasl-2-7b.qmd` |
| SL 2.8 | The reciprocal and rational functions（反比例と 1 次分数関数・漸近線） | `aasl-2-8.qmd` |
| SL 2.9 | Exponential and logarithmic functions（指数関数と対数関数） | `aasl-2-9.qmd` |
| SL 2.10 | Solving equations graphically and analytically（方程式を解く — グラフと式） | `aasl-2-10.qmd` |
| SL 2.11 | Transformations of graphs（グラフの平行移動・対称移動・拡大縮小） | `aasl-2-11.qmd` |

**2.7 を分ける理由。** 手で解く技法（factorization / completing the square / quadratic formula /
不等式）だけで 1 ページぶんあり、そのうえ Guidance 欄に $3kx^2+2x+k=0$ の $k$ を求める
判別式の設問例が別に挙がっています。

**2.11 は 1 ページのまま**にします（Not required at SL: $f(ax+b)$ の形の変換）。
書いてみて長すぎるようなら、そのときに分割をご報告します。

---

## Topic 3 — Geometry and trigonometry（8 項目 → 10 ページ）

| 項目 | ページの見出し | ファイル |
|:--|:--|:--|
| SL 3.1 | Three-dimensional geometry（空間図形 — 距離・体積・表面積・角） | `aasl-3-1.qmd` |
| SL 3.2 | Right-angled trigonometry, the sine and cosine rules（三角比と正弦定理・余弦定理） | `aasl-3-2.qmd` |
| SL 3.3 | Applications of trigonometry（三角法の応用 — 仰角・俯角・方位角） | `aasl-3-3.qmd` |
| SL 3.4 | Radian measure, arc length and sector area（弧度法・弧の長さ・扇形の面積） | `aasl-3-4.qmd` |
| **SL 3.5a** | The unit circle definitions of sine, cosine and tangent（単位円による定義と象限） | `aasl-3-5a.qmd` |
| **SL 3.5b** | Exact values and the ambiguous case of the sine rule（三角比の正確な値と正弦定理のあいまいな場合） | `aasl-3-5b.qmd` |
| SL 3.6 | Trigonometric identities（三角関数の相互関係と 2 倍角の公式） | `aasl-3-6.qmd` |
| **SL 3.7a** | The circular functions and their graphs（三角関数のグラフ） | `aasl-3-7a.qmd` |
| **SL 3.7b** | Transformations of trigonometric graphs and real-life models（$a\sin(b(x+c))+d$ と現実の場面） | `aasl-3-7b.qmd` |
| SL 3.8 | Solving trigonometric equations（三角方程式を解く） | `aasl-3-8.qmd` |

**3.5 を分ける理由。** 単位円の定義・象限ごとの符号・$\tan\theta = \dfrac{\sin\theta}{\cos\theta}$ と、
$0, \frac{\pi}{6}, \frac{\pi}{4}, \frac{\pi}{3}, \frac{\pi}{2}$ とその倍数の正確な値、さらに
「Extension of the sine rule to the ambiguous case」が同じ項目に入っています。
正確な値は Paper 1 の土台なので、独立したページにします。

**3.7 を分ける理由。** グラフそのもの（amplitude・周期）と、$a\sin(b(x+c))+d$ の変換・
現実の場面（潮位、観覧車）を 1 ページに収めると、図が多くなりすぎます。

**Topic 3 は 10 ページとも完成し、検証ずみです（2026-09-08）。**
公式集の引用は SL 3.2（正弦定理・余弦定理・面積）、SL 3.4（$l = r\theta$、$A = \frac{1}{2}r^{2}\theta$）、
SL 3.5（$\tan\theta = \frac{\sin\theta}{\cos\theta}$）、SL 3.6（Pythagoras と $2$ 倍角）だけです。
SL 3.3・SL 3.7・SL 3.8 には公式集の項目がないので、`callout-important` を置いていません。
正確な値の表も公式集には印刷されないので、SL 3.5b で「覚える」と明記しています。

---

## Topic 4 — Statistics and probability（12 項目 → 13 ページ）

| 項目 | ページの見出し | ファイル |
|:--|:--|:--|
| SL 4.1 | Sampling, bias and outliers（標本の取り方・かたより・外れ値） | `aasl-4-1.qmd` |
| SL 4.2 | Presentation of data（度数分布・ヒストグラム・累積度数・箱ひげ図） | `aasl-4-2.qmd` |
| SL 4.3 | Measures of central tendency and dispersion（代表値と散らばり） | `aasl-4-3.qmd` |
| SL 4.4 | Correlation and linear regression（相関と回帰 — Pearson の相関係数） | `aasl-4-4.qmd` |
| SL 4.5 | Introduction to probability（確率の基礎） | `aasl-4-5.qmd` |
| **SL 4.6a** | Combined events: Venn diagrams, tree diagrams and tables（事象の組み合わせ） | `aasl-4-6a.qmd` |
| **SL 4.6b** | Conditional probability and independence（条件付き確率と独立） | `aasl-4-6b.qmd` |
| SL 4.7 | Discrete random variables and expected value（離散確率変数と期待値） | `aasl-4-7.qmd` |
| SL 4.8 | The binomial distribution（二項分布） | `aasl-4-8.qmd` |
| SL 4.9 | The normal distribution（正規分布） | `aasl-4-9.qmd` |
| SL 4.10 | The regression line of x on y（x を y で表す回帰直線） | `aasl-4-10.qmd` |
| SL 4.11 | Formal conditional probability and independence（条件付き確率の定義と独立性の判定） | `aasl-4-11.qmd` |
| SL 4.12 | Standardization of normal variables（z 値と、平均・標準偏差が未知の場合） | `aasl-4-12.qmd` |

**4.6 を分ける理由。** Content 欄に、Venn 図・樹形図・表、combined events、mutually exclusive、
conditional probability、with / without replacement、independent events が並んでいます。
図の数がいちばん多くなる項目です。

**Topic 4 は 13 ページとも完成し、検証ずみです（2026-09-08）。**

レビューが見つけた主なもの（すべて修正ずみ）。

- SL 4.7 … 「$E(X) = 0$ なら合計が $0$ の近くにとどまる」は偽（近づくのは $1$ 回あたりの平均だけ）
- SL 4.9 … 「正規分布はすべての実数に正の確率を与える」が $P(X = a) = 0$ と矛盾していた
- SL 4.10 … 「$c \le 1/a$」は傾きが負のとき偽（$|c| \le 1/|a|$）。同じページの演習 1 が反例だった
- SL 4.11 … $3$ つの独立の言いかえを、$0 < P(B) < 1$ の条件なしに同値だと書いていた
- SL 4.12 … 「$z$ を $3$ 桁に丸めると答えの $3$ 桁目がずれる」が、挙げた数では成り立っていなかった

**Topic 4 は、GDC の節を置く例外**です。シラバスが
「binomial probabilities should be found using available technology」（SL 4.8）、
「Probabilities and values of the variable must be found using technology」（SL 4.9・4.12）と
明記しているので、SL 4.3・4.4・4.8・4.9・4.12 では Exercises の前に
`## Using your GDC (TI-Nspire CX II)` の節を置きます。長い手順が本文で分断されないためです。
その節の冒頭にも「これは Paper 2 でだけ使えます」を置きます。

Topic 5 でレビューが見つけた主なもの（すべて修正ずみ）。

- SL 5.9 … 「$a = 0$ は、速度がその瞬間いちばん大きい（小さい）ことを表す」は偽
- SL 5.10a … Why it works で「$\cos x$ を積分すると $-\sin x$」と、微分と積分が
  入れかわっていた／「$b$ は答えに影響しません」は偽（$b$ は答えの中身に残る）
- SL 5.10b … 例題 4 の「$u = \cos x$ では解けない」は偽
  （$\sin^{2}x = 1 - \cos^{2}x$ を使えば解ける）。演習 6 の検算も同じ理由で偽だった
- SL 5.11a … $\int_a^b g'(x)\,dx = g(b) - g(a)$ に「区間全体で定義されている」条件が
  抜けていた（$\int_{-1}^{1} x^{-2}dx$ に角かっこを当てると正の関数の積分が負になる）
- SL 5.11b … 「$2$ つの交点が上端と下端です」は偽（$y = x^{3}$ と $y = x$ など交点 $3$ つ）／
  「$2$ つとも負でも差は正です」は理由になっていない

Topic 5 で使った規約（Topic 1 から 4 と共通のものに加えて）。

- **GDC の節は置きません。** 電卓の話は、たたむ `callout-note` に $1$ つだけ入れます。
- 公式集の `callout-important` を置けるのは **5.3・5.5・5.6a・5.6b・5.9・5.10a・
  5.11a・5.11b** のページだけです（5.11a は 5.11 の欄が面積の式だけなので $0$ 個）。
- シラバスの逐語引用は SL 5.1・5.5・5.9・5.11 の $4$ 項目・$5$ 文だけです。
- ページをまたぐ Quarto の相互参照（`@eq-…`）は使いません。リンクで送ります。

---

## Topic 5 — Calculus（11 項目 → 15 ページ）

| 項目 | ページの見出し | ファイル |
|:--|:--|:--|
| SL 5.1 | Introduction to limits and the derivative（極限と導関数の考え方） | `aasl-5-1.qmd` |
| SL 5.2 | Increasing and decreasing functions（増加・減少と導関数の符号） | `aasl-5-2.qmd` |
| SL 5.3 | Differentiating $ax^n$（べき乗の微分） | `aasl-5-3.qmd` |
| SL 5.4 | Tangents and normals（接線と法線） | `aasl-5-4.qmd` |
| SL 5.5 | Introduction to integration（原始関数・積分定数・面積） | `aasl-5-5.qmd` |
| **SL 5.6a** | Derivatives of standard functions and the chain rule（$\sin x$・$\cos x$・$e^x$・$\ln x$ の微分と連鎖律） | `aasl-5-6a.qmd` |
| **SL 5.6b** | The product and quotient rules（積の微分法と商の微分法） | `aasl-5-6b.qmd` |
| SL 5.7 | The second derivative（第 2 次導関数と $f$・$f'$・$f''$ のグラフ） | `aasl-5-7.qmd` |
| **SL 5.8a** | Maximum and minimum points, concavity and points of inflexion（極大・極小・凹凸・変曲点） | `aasl-5-8a.qmd` |
| **SL 5.8b** | Optimization（最適化問題） | `aasl-5-8b.qmd` |
| SL 5.9 | Kinematics（変位・速度・加速度・道のり） | `aasl-5-9.qmd` |
| **SL 5.10a** | Indefinite integrals of standard functions（標準的な不定積分と $ax+b$ の合成） | `aasl-5-10a.qmd` |
| **SL 5.10b** | Integration by inspection and by substitution（逆連鎖律と置換積分） | `aasl-5-10b.qmd` |
| **SL 5.11a** | Definite integrals（定積分 — $\int_a^b g'(x)\,dx = g(b)-g(a)$） | `aasl-5-11a.qmd` |
| **SL 5.11b** | Areas below the axis and areas between curves（符号のある面積と 2 曲線ではさまれた面積） | `aasl-5-11b.qmd` |

**分ける理由。**

- **5.6** — 標準的な導関数 5 つと連鎖律で 1 ページ、積と商の公式でもう 1 ページ。
  AA の Paper 1 は、この 2 つをどちらも手で使わせます。
- **5.8** — Content 欄に、極値の判定・optimization・変曲点（$f''(x)=0$ だけでは足りないこと）が
  並んでいます。optimization は文章題なので、例題が長くなります。
- **5.10** — 標準的な不定積分と、$\int k\,g'(x)f(g(x))\,dx$ の形の置換は、別の技法です。
- **5.11** — 定積分の計算そのものと、$f(x)$ が負になる面積・2 曲線の間の面積は、
  つまずくところが違います。Guidance 欄も「without the use of technology」と明記しています。

---

## 書く順番

シラバス番号順（Topic 1 → 5）。1 ページ書くごとに、`_AA-START-HERE.md` 第 6 節の検証を回します。

## 積み残し

- **AA HL の公式集（AHL の欄が入った PDF）** — AA SL には要りませんが、HL に入る前に必要です。
