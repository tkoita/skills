# skills

小板・小比賀研究室で作った Claude のスキル置き場．研究室共有Driveの skills フォルダ（https://drive.google.com/drive/folders/1OgpKVVX1C6Z8nxL49j_QQej73zNtyhje ）と同じ構成で置いている．

| フォルダ | 作成者 | 内容 |
|---|---|---|
| [paper-review](paper-review/) | 小板 隆浩 | 論文原稿の添削（paper-review）．信学技報，情報処理学会の研究報告・シンポジウム（ComSys など），IEEE論文・国際会議，大会原稿，卒論・修論を，体裁から主張の強さまで決まった順で確認し，変更前／変更後の表で指摘する．卒業論文は研究室の卒業論文チェックシート（①書式〜⑧参考文献）の全項目も確認する．version 2.7.0．論文の添削にはこれを使う．以前のフォルダ名は koita-ai-v2 |
| [thesis-plan-review](thesis-plan-review/) | 小板 隆浩 | 卒業論文の研究計画書（様式1）と，既存研究との比較と新規性シート（様式2）のレビュー．本体は tkoita/Research の `.claude/skills/thesis-plan-review/` で，ここにはその写しを置いている（下の「研究計画書のレビュースキル」） |
| [koita-persona](koita-persona/) | 片岡 悠 | 小板として話すスキル（koita-ai）．研究の原稿，スライド，計画，コード，相談ごとを，小板の目で見て返す．判断の基準（judgment.md）と話し方（voice.md）を含む．以前のフォルダ名は koita-ai-v1（スキルの名前は koita-ai のまま） |
| [research-slides-v1](research-slides-v1/) | 國領 あい理 | 研究発表スライドの作成（research-slides）．学会・ゼミ・卒論／修論発表のスライドを pptxgenjs で .pptx と PDF に生成する．テンプレート，指針，作例を含む |
| [make-research-slides](make-research-slides/) | Drive の持ち主は rinbear98@gmail.com | 研究発表スライドの作成（research-slides）．Drive の make-research-slides フォルダ（2026-10-30）をそのまま置いた．中身は research-slides-v1 と同じで，SKILL.md の冒頭（name と description）が正しい形になっている．スキルの name が research-slides-v1 と同じ research-slides なので，両方は入れない |
| [master-thesis-support](master-thesis-support/) | 北村 佳資 | 修士論文の執筆支援．同志社大学大学院 理工学研究科 情報工学専攻の修士論文本文，英文Abstract，試問会レジュメの構成・執筆・推敲・LaTeX の整備・根拠付きの点検を支援する．LaTeX のテンプレートと年度別の要領を含む |
| [ieee-format-check](ieee-format-check/) | 杉田 雄一 | IEEE 形式の論文（IEEEtran の .tex／PDF）が，投稿先の規定・IEEEtran_HOWTO・IEEE の慣例に合うかを根拠付きで調べる．確認用スクリプト（check_paper.py）を含む |
| [create-poster](create-poster/) | 近藤 大輔 | 学会ポスター（A0 縦）の作成ガイド |
| [archive](archive/) | — | 使わなくなったスキルの記録．入れない（下の「archive」） |

## 原稿の種類ごとの使い分け

論文・原稿まわりのスキルが複数あるので，原稿の種類で選ぶ．**中心は paper-review で，ほかは必要なときに足す．**

| 原稿 | まず使う | 必要なら足す |
|---|---|---|
| 信学技報（電子情報通信学会の研究会） | paper-review（3-A 信学技報の規則で見る） | — |
| 情報処理学会の研究報告・シンポジウム（ComSys など） | paper-review（3-E 情報処理学会の規則で見る） | 投稿先の発表募集（CFP）・執筆要項（いっしょに渡す） |
| IEEE の国際会議・論文誌 | paper-review（3-B で内容と英文） | ieee-format-check（IEEEtran の体裁．投稿先の規定を調べて根拠付きで報告） |
| 卒業論文の研究計画書（様式1・2） | thesis-plan-review | — |
| 卒業論文 | paper-review（3-C と 3-D 卒業論文チェックシート） | — |
| 修士論文・試問会レジュメ | master-thesis-support（要領・LaTeX・レジュメ） | paper-review（本文の添削） |
| 発表スライド・ポスター | research-slides-v1 ／ create-poster | — |

- koita-persona（小板として話す）は，「小板の目で見て」と頼んだときだけ動く．研究の筋や相談ごとを見てほしいときに使う．原稿の細かい添削は paper-review に任せる．
- archive の中のものは入れない．archive/paper-review-v1 はスキルの name が paper-review と同じなので，両方入れるとどちらが動くか分からなくなる．

## ComSys や研究会の原稿をチェックするとき

1. **paper-review を入れる．** Claude Code なら `claude --plugin-dir paper-review`．claude.ai なら `paper-review/skills/paper-review/` を zip にして上げる（下の「入れ方」）．
2. **原稿と投稿先の情報を渡す．** 原稿の PDF（あれば `.tex` か `.docx` も）と，投稿先の名前（例：ComSys 2026 ポスター・デモ発表，OS研究会 2026年2月研究発表会），発表募集（CFP）のURLか執筆要項．投稿先の名前がないと「大会原稿など」として共通ルールだけで見るので，必ず書く．
3. **頼む．** 例：「ComSys 2026 のポスター原稿です．paper-review で投稿前チェックしてください．CFP は https://sigos.ipsj.or.jp/event/comsys2026/ 」「信学技報（〇〇研究会）の原稿です．paper-review で添削して」
4. **出てくるもの．** 1枚の HTML のレビュー（研究のコアの図，よい点，まず直す点，変更前／変更後の指摘表（必須・推奨・任意），検討して欲しいこと，次のアクション，参考資料）．指摘の「理由」欄に，根拠の本・資料とページが書いてある．
5. **直したら，同じ頼み方でもう一度チェックする．** 「必須」がなくなったら，共著者（教員）に見せる．
6. **出す前に，PDF のフォントの埋め込みを確かめる．** 情報処理学会の投稿システムは，埋め込まれていないと警告を出す．
7. **IEEE の国際会議なら，最後に ieee-format-check で体裁を見る．** カメラレディの前にも使う．

## 研究計画書のレビュースキル（thesis-plan-review）

卒業論文の研究計画書（様式1）と，既存研究との比較と新規性シート（様式2）をレビューするスキル．作成者は小板 隆浩．

- 研究のコアとなる技術・方法の図，題目案3つと章立て案，よくできている点，まず直してほしい点，項目ごとのコメント（変更前／変更後の表），文章のチェック，しっかり検討して欲しいこと，次のアクションを，1枚のHTMLにまとめて返す．
- 本体は tkoita/Research の `.claude/skills/thesis-plan-review/`（tkoita/Research で Claude Code を起動すると読み込まれる）．このリポジトリの `thesis-plan-review/` はその写しで，ほかの場所で使うときや claude.ai に上げるときに使う．
- 直すときは本体（tkoita/Research）を直し，ここと Drive にコピーし直す．
- 卒論本文の添削には paper-review を使う．

## archive

使わなくなったスキルを，経緯の記録として残している．入れない．Drive では持ち主が別の人なので archive フォルダに移せず，skills フォルダの直下に「archive-paper-review-v1（使わない）」という名前で置いている．

### archive/paper-review-v1 にある3つの SKILL.md

Drive の `Paper review-v1/skills/paper-review/` にあった3つのファイルを，そのまま置いている．作成者は木村 太陽．

| ファイル | Drive での持ち主 | 中身 |
|---|---|---|
| `SKILL.md`（20行） | 木村 太陽 | 最初の下書き．見出し（1. 共通ルール，2. どの論文かを判断，3. 信学技報の場合，3. IEEEの場合）だけで，本文はまだない．冒頭の name と description が2組あるので，このままではスキルとして正しく読み込めない |
| `SKILL.md.md`（18行） | 國領 あい理（とみられる） | 上の下書きと同じ内容の Google ドキュメント．Drive では「SKILL.md」という名前の Google ドキュメントだったので，Markdown に書き出して置いた．書き出しで冒頭の区切りや見出しの記号が崩れている |
| `SKILL (1).md`（363行） | 小板 隆浩 | 下書きを書き上げた版．paper-review の 2.0.0 とほぼ同じで，違いは2か所だけ（冒頭の name に引用符がない，「出力の形式」の確認順が「1-1 → 1-10」になっている（2.0.0 では「1-1 → 1-9」））．2.1.0 で足した「不必要な接続詞」の項目は入っていない |

## 入れ方

- Claude Code：プラグインの形のもの（`.claude-plugin/` があるもの）は `claude --plugin-dir <フォルダ>` で読み込む．スキルだけ使うなら，`SKILL.md` のあるフォルダを `~/.claude/skills/` に置く．
- claude.ai：`SKILL.md` のあるフォルダを zip にして（フォルダが zip の根に来る形），Customize > Skills から上げる．

## 更新するとき

1. このリポジトリを直して push する．プラグインの形のものは `.claude-plugin/plugin.json` の version を上げる．
2. Drive の skills フォルダの同じファイルを差し替える．
3. **claude.ai に上げている人は，上げ直す．** claude.ai に上げたスキルは，このリポジトリや Drive を直しても変わらない．`SKILL.md` のあるフォルダを zip にし直して，Customize > Skills で同じ名前のスキルを上げ直す．
4. Claude Code で `~/.claude/skills/` にコピーして使っている人も，コピーし直す（`--plugin-dir` でこのリポジトリのフォルダを直接指しているなら，`git pull` だけでよい）．
5. 変えたことを Slack の #10-nislab-saas で知らせる．
