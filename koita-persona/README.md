# koita-ai

小板として話すスキル。
研究の原稿、スライド、計画、相談ごとを、小板の目で見て返す。

中身は `skills/koita-ai/` にある。フォルダ名は koita-persona（以前は koita-ai-v1）で、スキルの名前は koita-ai のまま。

- `SKILL.md`：役割、返すまでの順番、書き方。
- `judgment.md`：見る順番と、型ごとの問い、なぜ止まるか、通る条件。根拠は本人の言葉。
- `voice.md`：口調と、指摘の形。

## 入れ方

### Claude Code

このフォルダごと手元に置き、起動時に指定する。

```
claude --plugin-dir /path/to/koita-persona
```

スキルだけ使うなら、`skills/koita-ai/` を `~/.claude/skills/` に置く（`~/.claude/skills/koita-ai/SKILL.md` になる形）。

### claude.ai（Web、デスクトップ）

`skills/koita-ai/` フォルダを zip にする（フォルダが zip の根に来る形）。
Customize > Skills で「+」、「Create skill」、「Upload a skill」の順に進んで上げ、一覧でオンにする。
Settings > Capabilities でコード実行を有効にしておく。

### Codex（CLI、IDE、ChatGPT デスクトップ）

`skills/koita-ai/` フォルダを `~/.agents/skills/` に置く。

### ChatGPT（Web）

Project を作り、三つの md をファイルとして添付し、「指示」に次を書く。

```
あなたは小板。添付の SKILL.md を最初に読み、judgment.md と voice.md を参照して、その指示に従って一人称で返す。
```

## 使い方

原稿や相談ごとをそのまま貼って、「小板として見て」と頼む。
