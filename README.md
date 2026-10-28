# skills

小板・小比賀研究室で作った Claude のスキル置き場．研究室共有Driveの skills フォルダ（https://drive.google.com/drive/folders/1OgpKVVX1C6Z8nxL49j_QQej73zNtyhje ）の中身を，フォルダの構成のまま置いている．

| フォルダ | 作成者 | 内容 |
|---|---|---|
| [koita-ai-v2](koita-ai-v2/) | 小板 隆浩 | 論文原稿の添削（paper-review）．信学技報，IEEE論文・国際会議，大会原稿，卒論・修論を，体裁から主張の強さまで決まった順で確認し，変更前／変更後の表で指摘する．卒業論文は研究室の卒業論文チェックシート（①書式〜⑧参考文献）の全項目も確認する．version 2.5.0．論文の添削にはこれを使う |
| [koita-ai-v1](koita-ai-v1/) | 片岡 悠 | 小板として話すスキル（koita-ai）．研究の原稿，スライド，計画，コード，相談ごとを，小板の目で見て返す．判断の基準（judgment.md）と話し方（voice.md）を含む |
| [paper-review-v1](paper-review-v1/) | 木村 太陽 | 論文原稿のチェック（paper-review）の初期版．SKILL.md が3つある（下の「paper-review-v1 にある3つの SKILL.md」を参照） |
| [research-slides-v1](research-slides-v1/) | 國領 あい理 | 研究発表スライドの作成（research-slides）．学会・ゼミ・卒論／修論発表のスライドを pptxgenjs で .pptx と PDF に生成する．テンプレート，指針，作例を含む |
| [master-thesis-support](master-thesis-support/) | 北村 佳資 | 修士論文の執筆支援．同志社大学大学院 理工学研究科 情報工学専攻の修士論文本文，英文Abstract，試問会レジュメの構成・執筆・推敲・LaTeX の整備・根拠付きの点検を支援する．LaTeX のテンプレートと年度別の要領を含む |
| [ieee-format-check](ieee-format-check/) | 杉田 雄一 | IEEE 形式の論文（IEEEtran の .tex／PDF）が，投稿先の規定・IEEEtran_HOWTO・IEEE の慣例に合うかを根拠付きで調べる．確認用スクリプト（check_paper.py）を含む |
| [create-poster](create-poster/) | 近藤 大輔 | 学会ポスター（A0 縦）の作成ガイド |

## 原稿の種類ごとの使い分け

論文・原稿まわりのスキルが複数あるので，原稿の種類で選ぶ．**中心は koita-ai-v2（paper-review）で，ほかは必要なときに足す．**

| 原稿 | まず使う | 必要なら足す |
|---|---|---|
| 信学技報（電子情報通信学会の研究会） | koita-ai-v2（paper-review．3-A 信学技報の規則で見る） | — |
| 情報処理学会の研究報告・シンポジウム（ComSys など） | koita-ai-v2（paper-review．共通ルールと 1-8 要旨の目安で見る） | 投稿先の執筆要項・テンプレート（いっしょに渡す） |
| IEEE の国際会議・論文誌 | koita-ai-v2（paper-review．3-B で内容と英文） | ieee-format-check（IEEEtran の体裁．投稿先の規定を調べて根拠付きで報告） |
| 卒業論文の研究計画書（様式1・2） | thesis-plan-review（tkoita/Research） | — |
| 卒業論文 | koita-ai-v2（paper-review．3-C と 3-D 卒業論文チェックシート） | — |
| 修士論文・試問会レジュメ | master-thesis-support（要領・LaTeX・レジュメ） | koita-ai-v2（paper-review．本文の添削） |
| 発表スライド・ポスター | research-slides-v1 ／ create-poster | — |

- koita-ai-v1（小板として話す）は，「小板の目で見て」と頼んだときだけ動く．研究の筋や相談ごとを見てほしいときに使う．原稿の細かい添削は paper-review に任せる．
- paper-review-v1 は入れない．name が koita-ai-v2 と同じ「paper-review」なので，両方入れるとどちらが動くか分からなくなる．

## ComSys や研究会の原稿をチェックするとき

1. **koita-ai-v2 を入れる．** Claude Code なら `claude --plugin-dir koita-ai-v2`．claude.ai なら `koita-ai-v2/skills/paper-review/` を zip にして上げる（下の「入れ方」）．
2. **原稿と投稿先の情報を渡す．** 原稿の PDF（あれば `.tex` か `.docx` も）と，投稿先の名前，執筆要項・テンプレート（ページ数，あらましの字数など）．投稿先の名前がないと「大会原稿など」として共通ルールだけで見るので，必ず書く．
3. **頼む．** 例：「ComSys 2026 の原稿です．paper-review で投稿前チェックしてください．執筆要項は添付のとおり」「信学技報（〇〇研究会）の原稿です．paper-review で添削して」
4. **出てくるもの．** 1枚の HTML のレビュー（研究のコアの図，よい点，まず直す点，変更前／変更後の指摘表（必須・推奨・任意），検討して欲しいこと，次のアクション，参考資料）．指摘の「理由」欄に，根拠の本・資料とページが書いてある．
5. **直したら，同じ頼み方でもう一度チェックする．** 「必須」がなくなったら，共著者（教員）に見せる．
6. **IEEE の国際会議なら，最後に ieee-format-check で体裁を見る．** カメラレディの前にも使う．

## 研究計画書のレビュースキル（thesis-plan-review）

卒業論文の研究計画書（様式1）と，既存研究との比較と新規性シート（様式2）をレビューするスキル．作成者は小板 隆浩．

- 研究のコアとなる技術・方法の図，題目案3つと章立て案，よくできている点，まず直してほしい点，項目ごとのコメント（変更前／変更後の表），文章のチェック，しっかり検討して欲しいこと，次のアクションを，1枚のHTMLにまとめて返す．
- 置き場所は tkoita/Research の `.claude/skills/thesis-plan-review/` で，このリポジトリには入れていない．
- 卒論本文の添削には koita-ai-v2（paper-review）を使う．

## paper-review-v1 にある3つの SKILL.md

Drive の `Paper review-v1/skills/paper-review/` にあった3つのファイルを，そのまま置いている．

| ファイル | Drive での持ち主 | 中身 |
|---|---|---|
| `SKILL.md`（20行） | 木村 太陽 | 最初の下書き．見出し（1. 共通ルール，2. どの論文かを判断，3. 信学技報の場合，3. IEEEの場合）だけで，本文はまだない．冒頭の name と description が2組あるので，このままではスキルとして正しく読み込めない |
| `SKILL.md.md`（18行） | 國領 あい理（とみられる） | 上の下書きと同じ内容の Google ドキュメント．Drive では「SKILL.md」という名前の Google ドキュメントだったので，Markdown に書き出して置いた．書き出しで冒頭の区切りや見出しの記号が崩れている |
| `SKILL (1).md`（363行） | 小板 隆浩 | 下書きを書き上げた版．koita-ai-v2 の paper-review の 2.0.0 とほぼ同じで，違いは2か所だけ（冒頭の name に引用符がない，「出力の形式」の確認順が「1-1 → 1-10」になっている（2.0.0 では「1-1 → 1-9」））．2.1.0 で足した「不必要な接続詞」の項目は入っていない |

論文の添削に使うのは koita-ai-v2 で，paper-review-v1 は経緯の記録として残している．

## 入れ方

- Claude Code：プラグインの形のもの（`.claude-plugin/` があるもの）は `claude --plugin-dir <フォルダ>` で読み込む．スキルだけ使うなら，`SKILL.md` のあるフォルダを `~/.claude/skills/` に置く．
- claude.ai：`SKILL.md` のあるフォルダを zip にして（フォルダが zip の根に来る形），Customize > Skills から上げる．

## 更新するとき

Drive の skills フォルダと，このリポジトリの両方を更新する．
