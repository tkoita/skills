#!/usr/bin/env python3
"""計画書レビュー（Markdown）を HTML に書き出す．

使い方：
  python3 render_review.py <review.md> <core.svg> <out.html> --name 武市さん [--date 2026-10-27] [--student]

- レイアウトは tkoita/Exp の配布資料（固定ナビ，用紙 .sheet，上端の色帯），
  色は tkoita/net-pages の入口ページの配色に合わせている．
- <review.md> は SKILL.md の「出力の形」の順に，「## 見出し」で節を分けて書いたもの．
  最初の「## 」より前（宛名と導入）は，表紙の用紙に入る．
- <core.svg> は研究のコアとなる技術・システム・方法の図（SVG）．表紙の次の用紙に入る．
- 「## 教員向けメモ」の節は，--student を付けると出力しない（学生に渡す版）．
- Markdown から HTML への変換には pandoc を使う．
"""
import argparse, datetime, html, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument('md'); ap.add_argument('svg'); ap.add_argument('out')
ap.add_argument('--name', required=True, help='宛名の名前（例：武市さん）')
ap.add_argument('--date', default=datetime.date.today().isoformat())
ap.add_argument('--student', action='store_true', help='教員向けメモを除く')
ap.add_argument('--figcap', default='', help='図の説明（1〜2文）')
a = ap.parse_args()

src = open(a.md, encoding='utf-8').read()
svg = open(a.svg, encoding='utf-8').read().strip()
assert svg.startswith('<svg'), 'SVG ファイルは <svg で始めること'

# 節に分ける
parts = re.split(r'(?m)^## +(.+?)\s*$', src)
intro, secs = parts[0], list(zip(parts[1::2], parts[2::2]))
if a.student:
    secs = [(t, b) for t, b in secs if not t.startswith('教員向け')]

def md2html(t):
    r = subprocess.run(['pandoc', '-f', 'gfm-autolink_bare_uris', '-t', 'html5', '--wrap=none'],
                       input=t, capture_output=True, text=True, check=True)
    h = r.stdout
    h = re.sub(r'<table>', '<div class="tw"><table>', h).replace('</table>', '</table></div>')
    # 優先度のバッジ
    for k, c in (('必須', 'must'), ('推奨', 'rec'), ('任意', 'opt')):
        h = re.sub(r'<td>(?:<strong>)?%s(?:</strong>)?</td>' % k, f'<td><span class="pri {c}">{k}</span></td>', h)
    # 「注意」「参考文献について」の段落を囲みにする
    h = re.sub(r'<p><strong>注意</strong>[：:]?(.*?)</p>', r'<div class="box amber"><b>注意</b>\1</div>', h, flags=re.S)
    h = re.sub(r'<p><strong>参考文献について</strong>[：:]?(.*?)</p>', r'<div class="box blue"><b>参考文献について</b>\1</div>', h, flags=re.S)
    # 外部リンクは新しいタブで
    h = re.sub(r'<a href="(https?://[^"]+)"', r'<a class="ulink" href="\1" target="_blank" rel="noopener"', h)
    # 素の URL をリンクにする（すでに a の中にあるものは除く）
    def autolink(seg):
        return re.sub(r'(?<![">])(https?://[^\s<）)，．]+)', r'<a class="ulink" href="\1" target="_blank" rel="noopener">\1</a>', seg)
    out = []
    for i, p in enumerate(re.split(r'(<a\b.*?</a>|<[^>]+>)', h, flags=re.S)):
        out.append(p if i % 2 else autolink(p))
    return ''.join(out)

# 節ごとの色（net-pages の配色）
def kind(t):
    for k, c in (('題目案', 'blue'), ('よくできて', 'teal'), ('まず直して', 'amber'), ('項目ごと', 'slate'),
                 ('文章', 'indigo'), ('しっかり検討', 'blue'), ('次のアクション', 'teal'), ('教員向け', 'rose'), ('参考資料', 'slate')):
        if t.startswith(k): return c
    return 'slate'
SHORT = {'題目案': '題目・章立て', 'よくできて': 'よい点', 'まず直して': 'まず直す点', '項目ごと': '項目ごと',
         '文章': '文章', 'しっかり検討': '検討して欲しいこと', '次のアクション': '次のアクション', '教員向け': '教員メモ', '参考資料': '参考資料'}
def short(t):
    for k, v in SHORT.items():
        if t.startswith(k): return v
    return t[:8]

sheets, nav = [], ['<a href="#core">研究のコア</a>']
for i, (t, b) in enumerate(secs, 1):
    sid = f's{i}'
    nav.append(f'<a href="#{sid}">{html.escape(short(t))}</a>')
    eyebrow = f'<div class="eyebrow"><span class="no">{i:02d}</span>{html.escape(short(t))}</div>'
    sheets.append(f'<section class="sheet {kind(t)}" id="{sid}">{eyebrow}<h1>{html.escape(t)}</h1>{md2html(b)}</section>')

intro_h = md2html(intro.strip())
title = f'卒業論文 研究計画書レビュー：{a.name}'
cap = f'<p class="cap">{html.escape(a.figcap)}</p>' if a.figcap else ''

CSS = r'''
:root{--paper:#ffffff;--ink:#0f172a;--soft:#334155;--line:#a7b1be;--line2:#c2cbd6;}
*{box-sizing:border-box;}html,body{margin:0;padding:0;}html{scroll-behavior:smooth;}
body{background:#dce2e9;color:var(--ink);font-family:"Hiragino Kaku Gothic ProN","Yu Gothic",YuGothic,"Meiryo",sans-serif;line-height:1.75;-webkit-font-smoothing:antialiased;padding:0 16px 80px;}
.topnav{position:sticky;top:0;z-index:60;margin:0 -16px 24px;padding:0 16px;background:rgba(220,226,233,.95);backdrop-filter:saturate(150%) blur(10px);-webkit-backdrop-filter:saturate(150%) blur(10px);border-bottom:1px solid var(--line2);}
.topnav .inner{max-width:960px;margin:0 auto;display:flex;align-items:center;gap:14px;height:54px;}
.topnav .brand{font-size:12.5px;font-weight:800;color:#1C2027;white-space:nowrap;letter-spacing:.02em;}
.topnav .brand span{display:block;font-size:10.5px;font-weight:700;color:#55606d;letter-spacing:.06em;}
.topnav .links{display:flex;gap:3px;overflow-x:auto;flex:1;scrollbar-width:none;}
.topnav .links::-webkit-scrollbar{display:none;}
.topnav .links a{font-size:12px;font-weight:700;color:#334155;text-decoration:none;padding:6px 11px;border-radius:6px;white-space:nowrap;}
.topnav .links a:hover{background:#c9d2dc;color:#0f172a;}
.sheet{scroll-margin-top:70px;max-width:960px;margin:0 auto 26px;background:var(--paper);border:1px solid var(--line);border-top:6px solid var(--accent);border-radius:6px;box-shadow:0 8px 30px rgba(20,30,45,.10);padding:40px 48px 46px;}
.sheet.blue{--accent:#1668B5;--accent-deep:#0E4A82;--accentbg:#dbeafb;--accentbd:#7fb1e0;}
.sheet.teal{--accent:#0F6B60;--accent-deep:#0b4a44;--accentbg:#e3f6f2;--accentbd:#74c8bc;}
.sheet.amber{--accent:#c99000;--accent-deep:#4f3a00;--accentbg:#fff3cc;--accentbd:#e2b52e;}
.sheet.slate{--accent:#334155;--accent-deep:#1e293b;--accentbg:#f1f4f8;--accentbd:#a9b6c6;}
.sheet.indigo{--accent:#4338ca;--accent-deep:#312e81;--accentbg:#e1e4fd;--accentbd:#9ba3ef;}
.sheet.rose{--accent:#be185d;--accent-deep:#831843;--accentbg:#fcdeec;--accentbd:#ec90bb;}
.sheet.cover{--accent:#0f766e;--accent-deep:#0E4A82;--accentbg:#dbeafb;--accentbd:#7fb1e0;}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:700;letter-spacing:.16em;color:var(--accent);}
.eyebrow .no{font-family:"SFMono-Regular",Consolas,Menlo,monospace;font-size:15px;}
h1{font-size:24px;font-weight:800;margin:6px 0 14px;line-height:1.3;}
.sheet.cover h1{font-size:28px;}
h2,h3{font-size:16px;font-weight:800;margin:26px 0 8px;display:flex;align-items:center;gap:10px;}
h2::before,h3::before{content:"";flex:0 0 4px;height:18px;background:var(--accent);border-radius:2px;}
h4{font-size:14px;margin:18px 0 6px;color:var(--accent-deep);}
p,li{font-size:14px;} li{margin:4px 0;} ul,ol{padding-left:22px;}
strong,b{font-weight:800;}
.meta{margin:4px 0 18px;display:flex;gap:22px;flex-wrap:wrap;border-top:1px solid var(--line2);border-bottom:1px solid var(--line2);padding:10px 0;font-size:12.5px;color:var(--soft);}
.meta b{color:var(--ink);}
.lead p{font-size:14.5px;color:#1e293b;}
code{font-family:"SFMono-Regular",Consolas,Menlo,monospace;background:#e8edf3;border:1px solid #b8c2ce;border-radius:4px;padding:0 4px;font-size:12.5px;}
a.ulink{color:#0E4A82;text-decoration:none;border-bottom:1px solid #5e9bd6;word-break:break-all;}
a.ulink:hover{background:#E6F1FB;}
.tw{overflow-x:auto;margin:12px 0;border:1px solid var(--line2);border-radius:8px;}
table{border-collapse:collapse;width:100%;font-size:12.6px;line-height:1.65;background:#fff;}
th{background:var(--accentbg);color:var(--accent-deep);font-weight:800;text-align:left;padding:8px 10px;border-bottom:2px solid var(--accentbd);white-space:nowrap;}
td{padding:8px 10px;border-top:1px solid #dfe4ea;vertical-align:top;}
tr:nth-child(even) td{background:#f8fafc;}
.pri{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.06em;border-radius:20px;padding:1px 10px;white-space:nowrap;}
.pri.must{color:#fff;background:#c0392b;} .pri.rec{color:#1C2027;background:#e8a317;} .pri.opt{color:#334155;background:#e2e8f0;border:1px solid #a9b6c6;}
.box{margin:14px 0;padding:13px 16px;border-radius:8px;font-size:13.4px;line-height:1.8;}
.box b:first-child{margin-right:8px;}
.box.blue{background:#d9ebfb;border:1px solid #7fb1e0;border-left:6px solid #1565c0;color:#0E4A82;}
.box.amber{background:#fff0bf;border:1px solid #e2b52e;border-left:6px solid #c99000;color:#4f3a00;}
.figure{margin:8px 0 0;padding:16px 18px 10px;background:#fff;border:1px solid var(--line2);border-radius:8px;overflow-x:auto;}
.figure svg{display:block;width:100%;height:auto;min-width:640px;}
.figure .cap{font-size:12px;color:var(--soft);margin:8px 0 0;}
.foot{max-width:960px;margin:0 auto;font-size:11.5px;color:#55606d;text-align:center;}
@media (max-width:640px){.sheet{padding:28px 18px 32px;}h1{font-size:21px;}.topnav .brand{display:none;}}
@media print{body{background:#fff;padding:0;}.topnav{display:none;}.sheet{box-shadow:none;break-inside:auto;margin-bottom:14px;}}
'''

page = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body>
<header class="topnav"><div class="inner"><div class="brand">{html.escape(a.name)}の研究計画書レビュー<span>小板・小比賀研究室 卒業論文</span></div><nav class="links">{''.join(nav)}</nav></div></header>
<section class="sheet cover" id="top"><div class="eyebrow">THESIS PLAN REVIEW</div><h1>卒業論文 研究計画書レビュー</h1>
<div class="meta"><div><b>宛先</b> {html.escape(a.name)}</div><div><b>レビュー日</b> {html.escape(a.date)}</div><div><b>対象</b> 様式1 研究計画書／様式2 既存研究との比較と新規性</div></div>
<div class="lead">{intro_h}</div></section>
<section class="sheet teal" id="core"><div class="eyebrow"><span class="no">00</span>研究のコア</div><h1>この研究のコアとなる技術・方法</h1>
<p>計画書をもとに，研究の中心となる仕組みを1枚の図にしました．計画発表のスライドや卒論の第3章の図の下書きに使ってください．</p>
<div class="figure">{svg}{cap}</div></section>
{''.join(sheets)}
<p class="foot">このレビューは，研究室の計画書レビュー用スキル（thesis-plan-review）を使って作成しました．</p>
</body></html>
'''
open(a.out, 'w', encoding='utf-8').write(page)

# タグの対応を確かめる（tkoita/Exp の取り決め）
bad = []
for t in ['section', 'div', 'p', 'table', 'tr', 'td', 'th', 'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3', 'svg', 'g']:
    o = len(re.findall(r'<%s[ >]' % t, page)); c = len(re.findall(r'</%s>' % t, page))
    if o != c: bad.append((t, o, c))
if bad:
    sys.exit(f'タグの対応が取れていない：{bad}')
print('ok', a.out, len(page))
