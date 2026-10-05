# AA HL — ページ一覧（執筆計画）

シラバス `5. (Subject guide) mathematics-analysis-and-approaches-guide-en ... copy 2.pdf`
（first assessment 2021）の **AHL** の Content / Guidance 欄から起こしました。
公式集は AA HL 用のものを使います（SL の欄も含まれます）。

- **シラバス項目：32**（AHL 1.10–1.16 / 2.12–2.16 / 3.9–3.18 / 4.13–4.14 / 5.12–5.19）
- **ページ数：35（案）**　**原則 1 項目 1 ページ**です（2026-09-19、Early の指示で
  49 ページ案から改めました）。分けるのは次の $3$ 項目だけです。
    - **AHL 1.10** … 数え上げと二項定理の拡張は、中身が別ものです（a は執筆済み）
    - **AHL 4.14** … 離散の分散と、連続確率変数・確率密度関数
    - **AHL 5.18** … Euler 法・変数分離と、同次形・積分因子
  分け方は**書きながら決め直してよい**ものです。下の表の「分割」欄が案です。
- **AA HL は AA SL を完全に含みます。** SL 項目のページは `aa-sl/` にあるので、
  ここでは **AHL の項目だけ**を書きます（AI HL と同じ作り方です）。

## 名前の付け方

| もの | 形 | 例 |
|:--|:--|:--|
| ファイル | `aa-hl/<topic>/aahl-X-Y.qmd` | `aa-hl/01-number-and-algebra/aahl-1-10a.qmd` |
| 題名のアンカー | `{#sec-aahl-X-Y}` | `{#sec-aahl-1-10a}` |
| 式・図・表 | `eq-aahlXY-...` / `fig-aahlXY-...` / `tbl-aahlXY-...` | `@eq-aahl110a-ncr` |
| 図のスクリプト | `figs/aa-hl/make_aahl_X_Y.py` | `figs/aa-hl/make_aahl_1_10a.py` |
| チェッカー | `figs/aa-hl/check_aahl_X_Y.py` | `figs/aa-hl/check_aahl_1_10a.py` |
| 図の出力 | `aa-hl/<topic>/img/aahl-X-Y-idea-a.svg` | |

- `figs/aa-hl/` は**まだありません。** 最初のページを書くときに作ります。
- 用語集は **`glossary-aa.qmd` を AA SL と共用**します（同じコースの上下なので）。
  AHL だけの語（複素数・ベクトルなど）は、この表に足していきます。
- `_quarto-draft.yml` には **`aa-hl` が登録済み**です（サイドバーの項目だけ足します）。
- 公開用の `_quarto.yml` は触りません。AA は SL・HL とも下書き側です。

## ページの形

**AA SL とまったく同じ**です。`_AA-START-HERE.md` 第 3 節と
`_方針変更-2026-09-15.md`（第 1〜18 節）に従ってください。食い違うときは後者が優先です。

```
# HL X.Y — English title（日本語）

::: {.callout-note} ## What you should be able to do :::

## The idea            ### 1.〜 7. 程度（各見出しに {#anchor} を手書き）
## Why it works        ::: {.callout-tip collapse="true"} ## クリックすると開きます
## Worked examples     例題 4
## Common errors
[## Using your GDC (TI-Nspire CX II)]   ← 操作が長い項目だけ
## Exercises           演習 10
```

**AA SL と同じ不変量**：例題 4／演習 10／`{.ex-sep}` 9／`<details class="jp-trans">` 14／
`## 解答例` 14／行頭 `---` 6／`**検算` 12 以上／`:::` の開閉が一致。

---

## 進捗

**35 / 35 ページ。**
`aa-hl/index.qmd` は、AHL 1.10a を書いたときに本物の一覧へ差しかえました。

凡例：`—` 未着手／`書` 執筆中／`✅` 完成（チェッカー NG 0・`check_refs.py` 通過）

### Topic 1 — Number and algebra（7 項目 → 8 ページ）

| 項目 | 分割 | 内容 | 状態 |
|:--|:--|:--|:--|
| AHL 1.10 | a | Counting principles（順列・組合せ）。`Not required:` 同じものを含む順列、円順列 | ✅ |
| AHL 1.10 | b | 二項定理の拡張（$n \in \mathbb{Q}$、分数・負の指数）。`Not required:` 二項定理の証明 | ✅ |
| AHL 1.11 | — | Partial fractions（部分分数分解）。分母は相異なる 1 次式 2 つまで | ✅ |
| AHL 1.12 | — | 複素数：$i$、$a+bi$、実部・虚部・共役・絶対値・偏角、複素平面 | ✅ |
| AHL 1.13 | — | 極形式 $r(\cos\theta + i\sin\theta) = r\,\mathrm{cis}\,\theta$、Euler 形 $re^{i\theta}$、相互変換、積と商とその図形的な意味 | ✅ |
| AHL 1.14 | — | 共役な複素数解、De Moivre の定理（有理数乗まで）、$n$ 乗根 | ✅ |
| AHL 1.15 | — | 数学的帰納法、背理法、反例（反例は「なぜ反例か」まで書かせる） | ✅ |
| AHL 1.16 | — | 連立 1 次方程式（3 元まで）。解が 1 つ／無数／なし。row reduction | ✅ |

### Topic 2 — Functions（5 項目 → 5 ページ）

| 項目 | 分割 | 内容 | 状態 |
|:--|:--|:--|:--|
| AHL 2.12 | — | 多項式関数とそのグラフ、zeros・roots・factors、因数定理と剰余定理、解の和と積 | ✅ |
| AHL 2.13 | — | $f(x) = \dfrac{ax+b}{cx^{2}+dx+e}$ と $f(x) = \dfrac{ax^{2}+bx+c}{dx+e}$ のグラフ（斜め漸近線を含む） | ✅ |
| AHL 2.14 | — | 偶関数・奇関数、周期関数、domain を制限した逆関数、self-inverse | ✅ |
| AHL 2.15 | — | $g(x) \ge f(x)$ を、グラフでも式でも解く（3 次まで） | ✅ |
| AHL 2.16 | — | $y=\lvert f(x)\rvert$・$y=f(\lvert x\rvert)$・$y=\dfrac{1}{f(x)}$・$y=f(ax+b)$・$y=[f(x)]^{2}$ のグラフと、絶対値を含む方程式・不等式 | ✅ |

### Topic 3 — Geometry and trigonometry（10 項目 → 10 ページ）

| 項目 | 分割 | 内容 | 状態 |
|:--|:--|:--|:--|
| AHL 3.9 | — | $\sec\theta$・$\csc\theta$・$\cot\theta$、$1+\tan^{2}\theta=\sec^{2}\theta$、$1+\cot^{2}\theta=\csc^{2}\theta$、$\arcsin x$・$\arccos x$・$\arctan x$ の domain・range・グラフ | ✅ |
| AHL 3.10 | — | 加法定理、$\tan$ の 2 倍角（2 倍角を加法定理から導く） | ✅ |
| AHL 3.11 | — | $\sin(\pi-\theta)$ などの関係と、グラフの対称性 | ✅ |
| AHL 3.12 | — | ベクトルの考え、位置ベクトル・変位ベクトル、基底 $\mathbf{i},\mathbf{j},\mathbf{k}$、成分、和・差・スカラー倍・平行、大きさ、単位ベクトル、2 点間の距離、ベクトルによる図形の証明 | ✅ |
| AHL 3.13 | — | 内積、なす角、垂直・平行の判定 | ✅ |
| AHL 3.14 | — | 直線のベクトル方程式 $\mathbf{r} = \mathbf{a} + \lambda\mathbf{b}$、媒介変数表示 | ✅ |
| AHL 3.15 | — | 一致・平行・交わる・ねじれの位置、交点 | ✅ |
| AHL 3.16 | — | 外積、平行四辺形・三角形の面積 | ✅ |
| AHL 3.17 | — | 平面のベクトル方程式、$\mathbf{r}\cdot\mathbf{n} = \mathbf{a}\cdot\mathbf{n}$、$ax+by+cz=d$ | ✅ |
| AHL 3.18 | — | 直線と平面、2 平面・3 平面の交わりと、なす角（AHL 1.16 とつなぐ） | ✅ |

### Topic 4 — Statistics and probability（2 項目 → 3 ページ）

| 項目 | 分割 | 内容 | 状態 |
|:--|:--|:--|:--|
| AHL 4.13 | — | Bayes の定理（3 事象まで） | ✅ |
| AHL 4.14 | a | 離散確率変数の分散、$\mathrm{Var}(X) = E(X^{2}) - [E(X)]^{2}$、$E(aX+b)$・$\mathrm{Var}(aX+b)$、公平なゲーム | ✅ |
| AHL 4.14 | b | 連続確率変数と確率密度関数、$\int_{-\infty}^{\infty} f(x)\,dx = 1$、区分的な関数、最頻値・中央値・平均・分散 | ✅ |

### Topic 5 — Calculus（8 項目 → 9 ページ）

| 項目 | 分割 | 内容 | 状態 |
|:--|:--|:--|:--|
| AHL 5.12 | — | 連続性と微分可能性（非形式的）、極限、**第一原理による微分** | ✅ |
| AHL 5.13 | — | $\frac{0}{0}$・$\frac{\infty}{\infty}$ の極限、l'Hôpital の定理 | ✅ |
| AHL 5.14 | — | 陰関数微分、関連する変化率、最適化（端点が答えになる場合を含む） | ✅ |
| AHL 5.15 | — | $\tan x$・$\sec x$・$\csc x$・$\cot x$・$a^{x}$・$\log_{a}x$・逆三角関数の導関数と、その不定積分、1 次式との合成、部分分数で積分しやすくする | ✅ |
| AHL 5.16 | — | 置換積分（$\int kg'(x)f(g(x))\,dx$ でない形は置換が与えられる）と部分積分（繰り返す場合を含む） | ✅ |
| AHL 5.17 | — | $y$ 軸とのあいだの面積、回転体の体積（$x$ 軸まわり・$y$ 軸まわり） | ✅ |
| AHL 5.18 | a | 1 階微分方程式、Euler 法（$x_{n+1} = x_{n} + h$）、変数分離形（ロジスティック方程式。AHL 1.11 とつなぐ） | ✅ |
| AHL 5.18 | b | 同次形 $\dfrac{dy}{dx} = f\!\left(\dfrac{y}{x}\right)$ を $y = vx$ で解く。積分因子による $y' + P(x)y = Q(x)$ | ✅ |
| AHL 5.19 | — | Maclaurin 展開（$e^{x}$、$\sin x$、$\cos x$、$\arctan x$、$\ln(1+x)$、$(1+x)^{p}$）と、置換・積・積分・微分・微分方程式から他の級数を作る | ✅ |

---

## 書く順番（案）

**Topic 1 → 2 → 3 → 4 → 5** の順です。理由は $2$ つあります。

- **AHL 1.15（証明）を先に置く**と、そのあとの項目で `Prove by induction` を使えます。
  De Moivre（AHL 1.14）が帰納法を要求するので、1.14 の前に 1.15 を書く手もあります。
- **ベクトル（3.12〜3.18）はひとまとまり**です。途中で別の Topic に移らないほうが、
  記号の決め方（太字か矢印か、$\mathbf{i},\mathbf{j},\mathbf{k}$ の扱い）がぶれません。

## 決まったこと（2026-09-19、Early の判断）

### 1. ベクトルの記号は $\mathbf{v}$（太字）

本文・図・答案例のすべてで **$\mathbf{v}$（太字）**を使います。$\vec{v}$ は使いません。

- 基底は $\mathbf{i}$、$\mathbf{j}$、$\mathbf{k}$。
- 位置ベクトルは $\mathbf{a}$、$\mathbf{r}$ のように小文字の太字。
- **$2$ 点を結ぶベクトルだけは $\overrightarrow{AB}$** と書きます（IB の問題文がこの形なので）。
  初出で「$\overrightarrow{AB} = \mathbf{b} - \mathbf{a}$」と橋を渡しておきます。
- **手書きでは太字が書けない**ことに、最初のページで触れてください。答案では
  $\underline{v}$ か $\vec{v}$ でよい、と一言添えます。
- チェッカーに `not_in_text("\\vec{")` を入れて、混ざらないようにします。

### 2. $\mathrm{cis}$ は紹介する（主には使わない）

$r\,\mathrm{cis}\,\theta$ は**紹介します。** シラバスに載っており、公式集にも出てくる書き方なので、
見て分からないと困るためです。ただし**本文で主に使うのは
$r(\cos\theta + i\sin\theta)$ と $re^{i\theta}$** とし、$\mathrm{cis}$ は AHL 1.13a の初出で
「同じものの短い書き方」として $1$ 度出すにとどめます。

- **書く前に、AA HL の公式集で実際の表記を確かめてください**（第 11 節：裏の取れないことは書かない）。
- 例題・演習の答えは $r(\cos\theta + i\sin\theta)$ か $re^{i\theta}$ で書きます。

### 3. `Using your GDC` の独立した節は置かない

**AA HL では $1$ ページも置きません。** 電卓が要る場面は、**その場で本文に折りたたみを差し込む**
形にします（AA SL の Topic 1〜3 と同じ）。

```
::: {.callout-tip collapse="true"}
## Paper 2 では、電卓でこう出せます
（TI-Nspire CX II の手順。第 18 節のとおり、他機種は書かない）

**Paper 1 では使えません。** …
:::
```

AHL 1.16（連立方程式）・4.14（連続確率変数）・5.18（Euler 法）も、この形でよいと判断しました。

### 4. AA SL へのリンクは張る。ただし逐語では引かない

**関連する SL 項目には、そのつどリンクを張ります。** AA HL は AA SL を含むので、
「どこで習ったか」が分かることが生徒の助けになります。

ただし **AA SL は今もレビュー中で本文が変わります。** ですから、

- リンクは **ページ＋アンカーまで**にとどめる（`../../aa-sl/05-calculus/aasl-5-10.qmd#steps` など）。
- **SL 側の文言を逐語で引き写さない。** 引き写すと、SL を直したときに食い違います。
- 節番号で呼ばない（「SL 5.10b の第 3 節」ではなく「[SL 5.10b](…#steps)」）。
  節番号は繰り上がることがあります（実際、レビューで 1.6 と 2.5 の節番号が変わりました）。
- チェッカーには **リンク先のファイルが実在するか**の見張りを入れます。

```python
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    if not _href.startswith("../"):
        continue
    _p = os.path.join(os.path.dirname(QMD), _href.split("#")[0])
    chk(os.path.exists(_p), "リンク先のページがある: " + _href)
```

アンカー切れは `python3 tools/check_refs.py` が全体で見ます。

### 5. The idea の見出しは「英語（日本語）」の形（2026-09-20、Early の指示）

`### N.` の見出しは、**英語を先に書き、そのあとに丸かっこで日本語**を添えます。

```
### 4. Quadratic inequalities（$2$ 次の不等式）
### 6. Proof by contradiction（背理法）
### 1. $y = \lvert f(x) \rvert$: reflecting what is below the axis（下を折り返す）
```

- **日本語（英語）の順ではありません。** ページの `#` 見出しと同じ並びにそろえます。
- 数式で始まる見出しは、**数式 → コロン → 英語 → （日本語）** の順にします。
- 英語の側に日本語を混ぜない。日本語はかっこの中だけです。
- **Topic 1・Topic 2 の 91 見出しは、2026-09-20 にこの形へ直しました。**
- チェッカーには、次の見張りを必ず入れます。

```python
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)
```

`##` の $5$ つの見出し（The idea など）と、callout の `##` 見出しは、
**いままでどおり**です。変えたのは `### N.` だけです。

---

## 書く前に確かめること（各ページ）

1. 公式集（AA HL 版）に、その式の欄があるか。あれば「公式集にあります」、
   なければ「ありません」と本文に書く（第 14 節の前置きとセットで）。
2. シラバスの `Not required:` があれば、本文にも書く。
3. AA SL のどのページにつながるか（第 4 節の書き方でリンク）。
