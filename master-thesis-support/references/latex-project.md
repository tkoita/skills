# LaTeX・Overleaf

## 既存原稿

既存のdocumentclass、latexmkrc、sty、bibを先に読む。本文・レジュメでコンパイラは同一とは限らない。日本語本文の標準同梱例はuplatex/upbibtex/dvipdfmx、レジュメはplatex/pbibtex/dvipdfmx。英語や既存LuaLaTeX等を一律に置き換えない。環境に対応するビルド手段を使う。

main.texのinput/include先とローカルstyも対象にする。依存関係を追い、文献キー・図・ファイルの実在を確認する。mainだけの更新日時ではPDFの鮮度は分からない。再ビルドできなければ整合性は未確認。

## 同梱の開始用テンプレート

- [本文](../assets/templates/thesis/main.tex)
- [レジュメ](../assets/templates/resume/main.tex)

ユーザーが新規作成を依頼した場合、該当フォルダを新しい出力先にコピーして使う。同梱assetや原資料をユーザー原稿として直接上書きしない。既存プロジェクトへ一括上書きしない。

配布された研究室テンプレートから、本文のref.bib欠落を解消し、他人のサンプル引用・業績・例図を外した。章本文、題目、本人情報は「要記入」を含む開始用の状態。これらはユーザーの根拠資料で埋める。図が必要ならプロジェクト内へ追加する。研究業績は本人の実績が提供された場合だけ有効にする。

レジュメのLetter設定は元の仕様として保持。現行の用紙指定は未確認。日付・年度は古い値を外してある。本文の固定所属・指導教員も利用時に確認する。原本の共通要領が求める製本の写真・白紙等は自動挿入しない。

同梱テンプレートは作成時に静的点検済みだが、TeXツールチェーンのない環境で作成しておりコンパイル・PDF表示は未検証。使用時にビルドして未定義引用、欠字、はみ出し、目次・ページ番号を確認する。Overleafでは同梱のlatexmkrcが使われる設定を確認し、実際のログによりエンジンを確認する。

## 読み取り専用の補助検査

Python 3標準ライブラリで実行する（パスは実際のスキル配置先に置き換える）。

```text
python3 /path/to/master-thesis-support/scripts/inspect_project.py --root /path/to/project --main main.tex
python3 /path/to/master-thesis-support/scripts/inspect_project.py --root /path/to/project --main main.tex --pdf main.pdf
```

標準出力のJSONにはfacts、candidates、uncheckedが分かれて出る。原稿は変更せず、TeXやプロジェクト内スクリプトを実行しない。PDF測定だけは任意のpypdfが必要。未導入・読取失敗ならuncheckedへ記録する。

対応は静的なinput/include、ローカルsty、bibliography/addbibresource、一般的なlabel/ref/cite、includegraphics。TeXの完全なパーサではない。条件分岐、動的マクロ、verbatim、特殊な引用マクロ、graphicspath等は制約があり、候補を手動確認する。ルート外の参照は追跡せず未検査とする。TeX配布のパッケージ実在はビルドで確認する。

最終確認では主ファイルからビルドし、文献・相互参照の再実行が収束したことと生成PDFを確認する。確認不能なら、TeX原稿のみ完成したことと未検証項目を伝える。
