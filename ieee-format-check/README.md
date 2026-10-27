# ieee-format-check

IEEE形式の論文（IEEEtran の `.tex` と PDF）を、次の2つに照らしてチェックする Claude 用のスキルです。

- **規則**：投稿先の規定と、IEEEtran の説明書（IEEEtran_HOWTO）
- **慣例**：IEEE 自身の会議テンプレート、Reference Guide、数式ガイドなどに書かれた書き方

指摘には、すべて原文の引用と出典が付きます。スキルが論文のファイルを書き換えることはありません。

## 何をしてくれるか

Claude に「この論文、IEEEフォーマットに合ってる？」「カメラレディ前にチェックして」のように頼むと、次の順に進みます。

1. 投稿先（会議）の公式ページで、ページ数・締切などの規定を調べる
2. 付属のスクリプト（`scripts/check_paper.py`）で、`.tex` と PDF を機械的に調べる
3. PDF のページを画像にして、見た目を確かめる
4. 指摘を4段階に分けて報告する
   - A：規定違反
   - B：HOWTO からの逸脱
   - C：IEEE の慣例からの逸脱
   - D：参考・好み

主に調べること：著者欄の書き方、図表キャプションの位置と書き方、「Fig.」「(1)」「[3]」などの参照の書き方、略語の定義、参考文献の書式、数式の書き方、ページ数・用紙サイズ・フォントの埋め込み、テンプレート文の消し忘れ。

## 入れ方

### Claude Code で使う（おすすめ）

1. ZIP を展開すると、`ieee-format-check` フォルダが出てきます。
2. このフォルダを、次のどちらかに置きます。
   - 自分のすべてのプロジェクトで使う：`~/.claude/skills/ieee-format-check/`
   - 特定のプロジェクトだけで使う：`<プロジェクト>/.claude/skills/ieee-format-check/`
3. Claude Code を開き直すと使えます。「この論文をIEEEフォーマットでチェックして」のように頼むか、`/ieee-format-check` と入力します。

### claude.ai／Claude デスクトップアプリで使う

1. Customize > Skills を開き、「+」→「Create skill」→「Upload a skill」を選びます。
2. 受け取った ZIP をそのままアップロードします（展開しない）。
3. コード実行の設定を有効にしておく必要があります。

claude.ai では、PDF を調べる道具（poppler）やネット検索が使えないことがあり、その場合は一部のチェックが飛ばされます。全部のチェックを使うなら Claude Code をおすすめします。

## 必要なもの

| もの | 何に使うか | 入れ方 |
|---|---|---|
| python3 | 付属スクリプト（標準ライブラリだけで動きます） | Mac には最初から入っていることが多い |
| poppler（`pdfinfo`、`pdffonts`、`pdftotext`、`pdfimages`、`pdftoppm`） | PDF のページ数、用紙サイズ、フォントの埋め込み、画像化 | Mac：`brew install poppler` |
| ネット検索（WebSearch／WebFetch） | 投稿先の規定を調べる | Claude Code では標準で使えます |

道具が足りない場合も、スクリプトは止まらず、その部分を飛ばしたと報告します。

## 中身

```
ieee-format-check/
├── SKILL.md                      Claude への手順書
├── README.md                     この説明
├── scripts/check_paper.py        機械的なチェック（読むだけで、ファイルは書き換えない）
└── references/
    ├── ieeetran-rules.md         IEEEtran_HOWTO の原文抜き書き（規則）
    └── ieee-conventions.md       IEEE の各ガイドの原文抜き書き（慣例）
```

## 使う前に

- スキルは、ソフトウェアを入れるのと同じように扱ってください。入れる前に `SKILL.md` と `scripts/check_paper.py` に目を通すことをおすすめします。スクリプトは、指定した `.tex`／PDF を読んで結果を表示するだけで、ネットへの送信やファイルの書き換えはしません。
- 判断の最終責任は書き手にあります。とくに投稿先の規定は会議ごとに違うので、指摘は必ず公式の案内と照らし合わせてください。
- 参照した文書の版：IEEEtran_HOWTO（2015）、IEEE 会議テンプレート（2019）、IEEE Reference Guide（V 3.28.2025）、IEEE Editing Mathematics（V 10.27.2023）、IEEE Editorial Style Manual（2026年10月時点の公開版）。
