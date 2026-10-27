// research-slides ひな形：学会での論文発表（口頭15分想定）のサンプル
// 使い方: node build_template.js [出力ファイル名.pptx]
// 中身（題目・各スライドの文言・図・数値）を差し替えて使う。ヘルパー関数とレイアウトはそのまま流用できる。
// 骨格＝メインカラー（タイトル・見出し・番号・カード）／強調＝アクセントカラーを1スライド1箇所
// 必要: npm install pptxgenjs react react-dom react-icons sharp
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const TB = require("react-icons/tb"); // Tabler の線アイコン（PowerPoint のアイコンに近い見た目）

const C = {
  // 白黒基調＋強調だけ緑
  TEXT: "3C3C3C", SUB: "7A7A7A", LINE: "D9D9D9", BG_SOFT: "F5F5F5",
  MAIN: "262626", MAIN_TINT: "EBEBEB", ACCENT: "1F8A4C", WHITE: "FFFFFF", GRAY2: "BDBDBD",
};
const FONT = "Meiryo";
const THEME = {
  name: "Research Talk",
  colors: {
    dk1: C.TEXT, lt1: C.WHITE, dk2: C.MAIN, lt2: C.BG_SOFT,
    accent1: C.MAIN, accent2: C.ACCENT, accent3: C.SUB, accent4: "595959",
    accent5: C.MAIN_TINT, accent6: C.GRAY2, hlink: C.MAIN, folHlink: C.SUB,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
pres.title = "マイクロドローンのホバリング安定化（サンプル）";
const FOOT = "國領 あい理（同志社大学）";

// ---- レイアウト ----
const titlePh = { name: "title", type: "title", x: 0.5, y: 0.3, w: 9.0, h: 0.85, fontFace: FONT, fontSize: 24, bold: true, color: C.MAIN, valign: "middle", align: "left", margin: 0 };
pres.defineSlideMaster({
  title: "TITLE", background: { color: C.WHITE },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 0.6, w: 8.6, h: 2.0, fontFace: FONT, fontSize: 32, bold: true, color: C.MAIN, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.7, y: 2.9, w: 8.6, h: 1.9, fontFace: FONT, fontSize: 18, color: C.TEXT, valign: "top", margin: 0 }, text: "" } },
  ],
});
for (const [name, bg, foot] of [["CONTENT", C.WHITE, FOOT], ["APPENDIX", C.BG_SOFT, "予備スライド"]]) {
  pres.defineSlideMaster({
    title: name, background: { color: bg },
    objects: [
      { placeholder: { options: titlePh, text: "" } },
      { text: { text: foot, options: { x: 0.5, y: 5.2, w: 2.8, h: 0.3, fontFace: FONT, fontSize: 12, color: C.SUB, margin: 0 } } },
    ],
    slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontFace: FONT, fontSize: 12, color: C.SUB, align: "right" },
  });
}

// ---- アイコン（react-icons → PNG）----
const ICON_CACHE = {};
async function preloadIcons(list) {
  for (const [name, color] of list) {
    const key = name + color;
    if (ICON_CACHE[key]) continue;
    const Comp = TB[name];
    if (!Comp) throw new Error("アイコンが見つからない: " + name);
    const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { size: 512, color: "#" + color }));
    const png = await sharp(Buffer.from(svg)).png().toBuffer();
    ICON_CACHE[key] = "image/png;base64," + png.toString("base64");
  }
}
const icon = (s, name, x, y, size, color = C.MAIN) => {
  const data = ICON_CACHE[name + color];
  if (!data) throw new Error(`preloadIcons に未登録: ${name} ${color}`);
  s.addImage({ data, x, y, w: size, h: size, altText: name });
};
// 薄い円の上にアイコン（必要なときだけ使う）
const iconBadge = (s, name, x, y, d, { bg = C.MAIN_TINT, color = C.MAIN } = {}) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
  icon(s, name, x + d * 0.22, y + d * 0.22, d * 0.56, color);
};

// ---- ヘルパー ----
const T = (s, text, o) => s.addText(text, { isTextBox: true, fontFace: FONT, color: C.TEXT, fontSize: 18, margin: 0, valign: "top", ...o });
const EM = { color: C.ACCENT, bold: true };          // 強調：1スライド1箇所だけ
const H = { color: C.MAIN, bold: true, fontSize: 20 }; // 骨格の見出し
const lines = (items, o = {}) => items.map((t, i) => {
  const [text, opt] = Array.isArray(t) ? t : [t, {}];
  return { text, options: { breakLine: i < items.length - 1, paraSpaceAfter: 10, ...o, ...opt } };
});
const bullets = (items, o = {}) => lines(items, { bullet: { indent: 16 }, paraSpaceAfter: 8, ...o });
const box = (s, o) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.08, line: { type: "none" }, ...o });
const fig = (s, label, x, y, w, h) => {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.BG_SOFT }, line: { type: "none" } });
  T(s, label, { x, y, w, h, fontSize: 14, color: C.SUB, align: "center", valign: "middle" });
};
const num = (s, n, x, y, d = 0.45) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: C.MAIN }, line: { type: "none" } });
  T(s, String(n), { x, y, w: d, h: d, color: C.WHITE, bold: true, fontSize: 18, align: "center", valign: "middle" });
};
const arrow = (s, x, y, w) => s.addShape(pres.shapes.RIGHT_ARROW, { x, y, w, h: 0.3, fill: { color: C.MAIN_TINT }, line: { type: "none" } });
const cite = (s, text) => T(s, text, { x: 0.5, y: 4.88, w: 9.0, h: 0.28, fontSize: 12, color: C.SUB });

// 章ナビ（今どこを話しているかをフッターに示す。現在の章だけメイン色）
const CHAPTERS = ["背景", "先行研究", "目的", "提案手法", "実験", "結果", "考察", "まとめ"];
const nav = (s, cur) => T(s, CHAPTERS.map((c, i) => ({ text: c + (i < CHAPTERS.length - 1 ? "　" : ""), options: c === cur ? { color: C.MAIN, bold: true } : { color: C.GRAY2 } })),
  { x: 3.4, y: 5.2, w: 5.45, h: 0.3, fontSize: 12, align: "right" });
const add = (sec, master = "CONTENT") => {
  const sl = pres.addSlide({ masterName: master, sectionTitle: sec });
  if (master === "CONTENT" && CHAPTERS.includes(sec)) nav(sl, sec);
  return sl;
};
const sec = (t) => pres.addSection({ title: t });

// アイコンカードを横に並べる（アイコン＋短いラベル）
const pointCards = (s, items, { y = 1.4, h = 2.35 } = {}) => {
  const n = items.length, gap = 0.25, w = (9.0 - gap * (n - 1)) / n;
  items.forEach((label, i) => {
    const x = 0.5 + i * (w + gap);
    box(s, { x, y, w, h, fill: { color: C.BG_SOFT } });
    num(s, i + 1, x + (w - 0.5) / 2, y + 0.35, 0.5);
    T(s, label, { x: x + 0.15, y: y + 1.1, w: w - 0.3, h: h - 1.25, align: "center", valign: "middle" });
  });
};
// 結論の1行（強調）
const takeaway = (s, text, y = 4.1) => T(s, text, { ...EM, x: 0.5, y, w: 9.0, h: 0.6, fontSize: 24, valign: "middle" });

// 日本語の字形にするための後処理（pptxgenjs は lang=en-US・中国語の文字セットで書き出すため）
async function fixJapanese(file) {
  const fs = require("fs");
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  for (const name of Object.keys(zip.files).filter(n => n.endsWith(".xml"))) {
    const x = await zip.file(name).async("string");
    const y = x.replace(/lang="en-US"/g, 'lang="ja-JP"')
      .replace(/charset="-122"/g, 'charset="-128"')
      .replace(/<a:ea typeface=""/g, `<a:ea typeface="${FONT}"`);
    if (y !== x) zip.file(name, y);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function build() {
  await preloadIcons([["TbCamera", C.MAIN], ["TbCpu", C.WHITE], ["TbAntenna", C.MAIN], ["TbDrone", C.MAIN]]);
  let s;

  // ===== 表紙 =====
  sec("タイトル");
  s = add("タイトル", "TITLE");
  s.addText("ステレオカメラを用いた\nマイクロドローンの\nホバリング安定化システム", { placeholder: "title" });
  s.addText([
    { text: "國領 あい理", options: { bold: true } },
    { text: "，[共著者]，[指導教員]", options: { breakLine: true } },
    { text: "同志社大学大学院 理工学研究科", options: { fontSize: 18, color: C.SUB, breakLine: true } },
    { text: "ネットワーク情報システム研究室", options: { fontSize: 18, color: C.SUB, breakLine: true } },
    { text: "◯◯学会 ◯◯研究会　2026年◯月◯日", options: { fontSize: 18, color: C.SUB } },
  ], { placeholder: "body" });
  T(s, "※ CLAUDE.md の作例です（数値・図・文献はダミー／[要確認] は実データに差し替え）", { x: 0.7, y: 4.95, w: 8.6, h: 0.3, fontSize: 12, color: C.SUB });
  s.addNotes("同志社大学の國領です。ステレオカメラを用いたマイクロドローンのホバリング安定化システムについて発表します。");

  // ===== 本日の流れ =====
  s = add("タイトル");
  s.addText("本日の流れ", { placeholder: "title" });
  [["背景・先行研究", "屋内飛行の課題と既存手法"], ["目的・貢献", "本研究がねらう空白"], ["提案手法", "検出・高度推定・制御"], ["実験・結果", "開ループとの比較"], ["考察・まとめ", "限界と今後の課題"]].forEach(([h, d], i) => {
    const y = 1.35 + i * 0.7;
    box(s, { x: 0.5, y, w: 9.0, h: 0.58, fill: { color: i % 2 ? C.WHITE : C.BG_SOFT } });
    num(s, i + 1, 0.7, y + 0.08, 0.42);
    T(s, h, { x: 1.35, y, w: 2.6, h: 0.58, bold: true, color: C.MAIN, valign: "middle" });
    T(s, d, { x: 4.0, y, w: 5.3, h: 0.58, valign: "middle" });
  });
  s.addNotes("本日の流れです。背景と先行研究、目的、提案手法、実験と結果、考察とまとめの順にお話しします。");

  // ===== 背景 =====
  sec("背景");
  s = add("背景");
  s.addText("屋内ではGNSS（衛星測位）が使えず、高度が分からない", { placeholder: "title" });
  pointCards(s, ["屋内点検・倉庫での\n活用が期待", "衛星の電波が\n屋内に届かない", "気圧センサは\n空調で乱れる"]);
  takeaway(s, "→ 屋内では、高度の基準が得にくい");
  s.addNotes("ドローンは屋内点検や倉庫などでの活用が期待されています。しかし屋内ではGNSSの電波が届かず、気圧センサも空調などの影響を受けるため、高度の基準を得るのが難しいという課題があります。");

  s = add("背景");
  s.addText("マイクロドローンには、センサを追加する余裕がない", { placeholder: "title" });
  pointCards(s, ["搭載できる\n重量が小さい", "バッテリー・電力に\n余裕がない", "機体側の\n計算資源も限られる"]);
  takeaway(s, "→ センサを足すほど、飛行時間が減る");
  s.addNotes("一方、マイクロドローンは機体が小さく、搭載重量、電力、計算資源のいずれにも余裕がありません。センサを追加すると重くなり、飛行時間が短くなります。");

  // ===== 先行研究 =====
  sec("先行研究");
  const sideText = (s, head, pts, em) => {
    T(s, head, { ...H, x: 5.0, y: 1.4, w: 4.5, h: 0.5, valign: "middle" });
    T(s, bullets(pts), { x: 5.0, y: 2.05, w: 4.5, h: 1.3 });
    T(s, em, { ...EM, x: 5.0, y: 3.6, w: 4.5, h: 0.9, fontSize: 24, valign: "middle" });
  };
  s = add("先行研究");
  s.addText("外部カメラ計測は高精度だが、設置が大がかり", { placeholder: "title" });
  fig(s, "[図：先行研究 [1] の\nシステム構成図を引用]", 0.5, 1.35, 4.1, 3.35);
  sideText(s, "先行研究 A：外部計測", ["複数のカメラで機体を追跡 [1]", "制御研究で広く利用 [2]"], "高価で、専用の部屋が必要");
  cite(s, "[1] [要記入] 著者, 会議・論文誌名, 年　[2] [要記入] 著者, 会議・論文誌名, 年");
  s.addNotes("1つ目の系統は、モーションキャプチャなど外部のカメラで機体を計測する方法です。精度は高く、制御の研究で広く使われていますが、高価で、専用の部屋とカメラの較正が必要です。");

  s = add("先行研究");
  s.addText("機体搭載センサは、マイクロ機には負担が大きい", { placeholder: "title" });
  fig(s, "[図：先行研究 [3] の\n機体・センサ構成を引用]", 0.5, 1.35, 4.1, 3.35);
  sideText(s, "先行研究 B：機体搭載", ["カメラ＋IMUで位置推定 [3]", "ToFセンサで高度を計測 [4]"], "重量・電力の負担が増える");
  cite(s, "[3] [要記入] 著者, 会議・論文誌名, 年　[4] [要記入] 著者, 会議・論文誌名, 年");
  s.addNotes("2つ目の系統は、機体にカメラや距離センサを載せる方法です。外部設備なしで完結しますが、マイクロドローンでは重量・電力・計算の負担が大きくなります。");

  s = add("先行研究");
  s.addText("「安価」かつ「機体に足さない」方法はまだない", { placeholder: "title" });
  const lab = (t) => [t, { color: C.SUB, fontSize: 14, paraSpaceAfter: 1 }];
  [["外部計測", "高い", "マーカー", false],
   ["機体搭載", "中〜低", "センサ・計算機", false],
   ["本研究", "低い", "色バンドのみ", true]].forEach(([h, cost, add_, hl], i) => {
    const x = 0.5 + i * 3.07;
    box(s, { x, y: 1.35, w: 2.86, h: 3.4, fill: { color: hl ? C.MAIN_TINT : C.BG_SOFT } });
    T(s, h, { ...(hl ? { ...EM, fontSize: 22 } : H), x: x + 0.25, y: 1.6, w: 2.4, h: 0.6, valign: "middle" });
    if (!hl) T(s, i === 0 ? "[1][2]" : "[3][4]", { x: x + 0.25, y: 4.3, w: 2.4, h: 0.3, fontSize: 14, color: C.SUB });
    T(s, lines([lab("コスト"), [cost, { paraSpaceAfter: 14 }], lab("機体への追加"), add_]), { x: x + 0.25, y: 2.55, w: 2.45, h: 2.0, fontSize: 20 });
  });
  s.addNotes("2つの系統を、コストと機体への追加で比べると、安価で、かつ機体に何も足さない方法はまだありません。本研究はここをねらいます。");

  // ===== 目的・貢献 =====
  sec("目的");
  s = add("目的");
  s.addText("本研究の目的と貢献", { placeholder: "title" });
  box(s, { x: 0.5, y: 1.3, w: 9.0, h: 1.3, fill: { color: C.MAIN_TINT } });
  T(s, lines([["目的", { ...H, fontSize: 18, paraSpaceAfter: 4 }], ["地上カメラで高度を測り、ホバリングを安定させる", { ...EM, fontSize: 24 }]]), { x: 0.8, y: 1.45, w: 8.4, h: 1.1 });
  ["ステレオ＋色検出で\n高度を推定", "Raspberry Pi 5で\n閉ループ制御", "実機で\n評価"].forEach((t, i) => {
    const x = 0.5 + i * 3.07;
    box(s, { x, y: 2.85, w: 2.86, h: 1.9, fill: { color: C.BG_SOFT } });
    num(s, i + 1, x + 0.25, 3.1, 0.45);
    T(s, "貢献", { ...H, fontSize: 18, x: x + 0.85, y: 3.1, w: 1.6, h: 0.45, valign: "middle" });
    T(s, t, { x: x + 0.25, y: 3.95, w: 2.4, h: 0.75 });
  });
  s.addNotes("本研究の目的は、地上のステレオカメラで高度を測り、ホバリングを安定させることです。貢献は3点で、ステレオカメラと色ブロブ検出による高度推定、Raspberry Pi 5で完結する閉ループ制御、実機での評価です。");

  // ===== 手法：システム構成 =====
  sec("提案手法");
  s = add("提案手法");
  s.addText("計測・推定・制御はすべて地上側で行う", { placeholder: "title" });
  [["TbCamera", "ステレオ\nカメラ", "左右画像"], ["TbCpu", "Raspberry\nPi 5", "検出・推定\n・制御"], ["TbAntenna", "ELRS\n送信機", "2.4GHzで送信"], ["TbDrone", "ドローン", "Pavo Pico"]].forEach(([ic, h, d], i) => {
    const x = 0.5 + i * 2.33, hl = i === 1;
    box(s, { x, y: 1.35, w: 2.05, h: 2.9, fill: { color: hl ? C.ACCENT : C.BG_SOFT } });
    icon(s, ic, x + 0.6, 1.55, 0.85, hl ? C.WHITE : C.MAIN);
    T(s, h, { x: x + 0.1, y: 2.5, w: 1.85, h: 0.8, bold: true, color: hl ? C.WHITE : C.MAIN, align: "center", valign: "middle" });
    T(s, d, { x: x + 0.05, y: 3.35, w: 1.95, h: 0.7, color: hl ? C.WHITE : C.SUB, align: "center" });
    if (i < 3) arrow(s, x + 2.07, 2.65, 0.24);
  });
  T(s, "機体の高度はカメラで再び観測される（閉ループ）", { x: 0.5, y: 4.45, w: 9.0, h: 0.4, color: C.SUB, align: "center" });
  s.addNotes("システム構成です。ステレオカメラの画像をRaspberry Pi 5で処理して高度を推定し、PIDでスロットル値を計算して、ELRS送信機から機体へ送ります。処理はすべて地上側で行います。");

  // ===== 手法：検出 =====
  s = add("提案手法");
  s.addText("機体の色バンドを、左右の画像で検出する", { placeholder: "title" });
  ["左カメラ", "右カメラ"].forEach((lb, i) => {
    const x = 0.5 + i * 2.45, bx = i === 0 ? 1.25 : 0.85;
    box(s, { x, y: 1.35, w: 2.25, h: 2.0, fill: { color: C.BG_SOFT } });
    s.addShape(pres.shapes.RECTANGLE, { x: x + bx - 0.4, y: 2.2, w: 0.8, h: 0.26, fill: { color: C.MAIN_TINT }, line: { color: C.MAIN, width: 1 } });
    s.addShape(pres.shapes.OVAL, { x: x + bx - 0.09, y: 2.24, w: 0.18, h: 0.18, fill: { color: C.ACCENT }, line: { type: "none" } });
    T(s, lb, { x, y: 3.45, w: 2.25, h: 0.35, bold: true, color: C.MAIN, align: "center" });
  });
  T(s, "● 色バンドの重心", { x: 0.5, y: 3.95, w: 4.7, h: 0.35, fontSize: 14, color: C.SUB });
  [["HSV色空間に変換"], ["色の範囲で領域を抽出"], ["最大領域の重心を計算"]].forEach(([h], i) => {
    const y = 1.5 + i * 0.85;
    num(s, i + 1, 5.6, y, 0.42);
    T(s, h, { x: 6.2, y, w: 3.3, h: 0.42, valign: "middle" });
  });
  s.addNotes("機体の側面に色のバンドを付け、左右それぞれの画像で検出します。HSV色空間に変換してしきい値で色領域を取り出し、ノイズを除去したあと、最大の領域の重心を画像モーメントから求めます。");

  // ===== 手法：高度推定 =====
  s = add("提案手法");
  s.addText("左右の重心のずれ（視差）から距離を求める", { placeholder: "title" });
  [["ステレオ較正・平行化"], ["視差 d = u_L − u_R"], ["距離 Z を機体高度へ換算"]].forEach(([h], i) => {
    const y = 1.5 + i * 0.85;
    num(s, i + 1, 0.5, y, 0.42);
    T(s, h, { x: 1.1, y, w: 4.2, h: 0.42, valign: "middle" });
  });
  box(s, { x: 5.6, y: 1.35, w: 3.9, h: 3.0, fill: { color: C.BG_SOFT } });
  T(s, "三角測量", { ...H, fontSize: 18, x: 5.9, y: 1.5, w: 3.3, h: 0.4 });
  T(s, "Z = f・B / d", { ...EM, x: 5.9, y: 1.95, w: 3.3, h: 0.8, fontSize: 32, valign: "middle" });
  T(s, lines(["f：焦点距離", "B：カメラ間の距離"], { paraSpaceAfter: 6 }), { x: 5.9, y: 2.95, w: 3.4, h: 1.2 });
  s.addNotes("事前にステレオ較正と平行化を行い、左右の画像の行をそろえておきます。左右の重心のx座標の差を視差dとし、三角測量の式 Z = fB/d で距離を求め、カメラの設置条件から機体の高度に換算します。遠いほど視差が小さくなり、誤差が大きくなる点に注意が必要です。");

  // ===== 手法：制御 =====
  s = add("提案手法");
  s.addText("スロットルだけをPIDで調整し、目標高度を保つ", { placeholder: "title" });
  [["目標高度 r", 0.5], ["PID制御器", 2.75], ["ドローン", 5.0], ["ステレオ計測", 7.25]].forEach(([h, x], i) => {
    const hl = i === 1;
    box(s, { x, y: 1.5, w: 2.0, h: 0.85, fill: { color: hl ? C.ACCENT : C.BG_SOFT } });
    T(s, h, { x, y: 1.5, w: 2.0, h: 0.85, bold: true, align: "center", valign: "middle", color: hl ? C.WHITE : C.MAIN });
    if (i < 3) arrow(s, x + 2.02, 1.77, 0.21);
  });
  s.addShape(pres.shapes.LINE, { x: 8.25, y: 2.35, w: 0, h: 0.5, line: { color: C.MAIN, width: 2 } });
  s.addShape(pres.shapes.LINE, { x: 3.75, y: 2.85, w: 4.5, h: 0, line: { color: C.MAIN, width: 2 } });
  s.addShape(pres.shapes.LINE, { x: 3.75, y: 2.35, w: 0, h: 0.5, line: { color: C.MAIN, width: 2, endArrowType: "triangle" }, flipV: true });
  T(s, "計測した高度 y を戻す", { x: 4.2, y: 2.92, w: 3.6, h: 0.32, fontSize: 14, color: C.SUB, align: "center" });
  box(s, { x: 0.5, y: 3.55, w: 9.0, h: 1.0, fill: { color: C.BG_SOFT } });
  T(s, "u = Kp・e + Ki・∫e dt + Kd・de/dt　（e = r − y）", { x: 0.8, y: 3.55, w: 8.4, h: 1.0, valign: "middle" });
  s.addNotes("制御はスロットルのみのPIDです。目標高度と計測高度の差 e からスロットルの補正量 u を計算します。姿勢の安定化は機体のフライトコントローラに任せ、本システムは高度だけを外側のループで制御します。");

  // ===== 実験条件 =====
  sec("実験");
  s = add("実験");
  s.addText("屋内で目標高度を与え、ホバリング中の高度を記録した", { placeholder: "title" });
  const rows = [["項目", "条件"], ["機体", "BetaFPV Pavo Pico"], ["目標高度", "[要確認] m"], ["試行回数", "各条件 [要確認] 回"], ["比較条件", "開ループ（スロットル固定）"], ["評価指標", "RMSE・最大偏差・整定時間"]];
  const HLINE = [{ type: "none" }, { type: "none" }, { type: "solid", pt: 0.75, color: C.LINE }, { type: "none" }];
  s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: c, options: {
    bold: i === 0 || j === 0, color: i === 0 ? C.WHITE : (j === 0 ? C.MAIN : C.TEXT),
    fill: { color: i === 0 ? C.MAIN : C.WHITE }, ...(i === 5 && j === 1 ? EM : {}) } }))),
    { x: 0.5, y: 1.35, w: 5.4, colW: [1.4, 4.0], rowH: 0.52, fontFace: FONT, fontSize: 18, border: HLINE, valign: "middle", margin: [0, 0.1, 0, 0.1] });
  fig(s, "[図：実験環境の写真\n（カメラと機体の配置）]", 6.2, 1.35, 3.3, 3.2);
  s.addNotes("実験条件です。屋内で目標高度を与えてホバリングさせ、そのときの高度を記録しました。比較として、スロットルを固定した開ループ条件も測定しました。評価指標はRMSE、最大偏差、整定時間の3つです。");

  // ===== 結果：数値 =====
  sec("結果");
  s = add("結果");
  s.addText("閉ループ制御で、高度誤差（RMSE）が小さくなった", { placeholder: "title" });
  const res = [["指標", "開ループ", "閉ループ（提案）"], ["RMSE [m]", "[要確認]", "[要確認]"], ["最大偏差 [m]", "[要確認]", "[要確認]"], ["整定時間 [s]", "—", "[要確認]"]];
  s.addTable(res.map((r, i) => r.map((c, j) => ({ text: c, options: {
    bold: i === 0 || j === 0, align: j === 0 ? "left" : "center", color: i === 0 ? C.WHITE : (j === 0 ? C.MAIN : C.TEXT),
    fill: { color: i === 0 ? C.MAIN : (j === 2 ? C.MAIN_TINT : C.WHITE) }, ...(i === 1 && j === 2 ? { ...EM, fontSize: 22 } : {}) } }))),
    { x: 0.5, y: 1.4, w: 9.0, colW: [3.0, 3.0, 3.0], rowH: 0.62, fontFace: FONT, fontSize: 18, border: HLINE, valign: "middle", margin: [0, 0.15, 0, 0.15] });
  T(s, "値は [要確認] 回の試行の平均 ± 標準偏差", { x: 0.5, y: 4.15, w: 9.0, h: 0.4, color: C.SUB });
  s.addNotes("結果の数値です。閉ループ制御により、開ループと比べてRMSEが小さくなりました。値は複数回の試行の平均と標準偏差です。開ループは整定しないため整定時間は定義していません。（数値は実データに差し替え）");

  // ===== 結果：グラフ =====
  s = add("結果");
  s.addText("提案手法では、数秒で目標高度付近に収まる", { placeholder: "title" });
  const t = Array.from({ length: 21 }, (_, i) => i * 1.5);
  const labels = t.map(x => (x % 6 === 0 ? x.toFixed(0) : ""));
  s.addChart(pres.charts.LINE, [
    { name: "目標高度", labels, values: t.map(() => 0.5) },
    { name: "開ループ（比較）", labels, values: t.map((x, i) => +(0.5 + 0.18 * Math.sin(i * 0.6) + 0.006 * i).toFixed(3)) },
    { name: "閉ループ（提案）", labels, values: t.map((x, i) => +(0.5 + 0.25 * Math.exp(-i * 0.45) * Math.cos(i * 0.9)).toFixed(3)) },
  ], {
    x: 0.5, y: 1.3, w: 5.9, h: 3.75, chartColors: [C.MAIN, C.GRAY2, C.ACCENT], lineSize: 2, lineDataSymbol: "none",
    showLegend: true, legendPos: "b", legendFontSize: 14, legendFontFace: "+mn-lt", legendColor: C.TEXT,
    catAxisTitle: "時間 [s]", showCatAxisTitle: true, valAxisTitle: "高度 [m]", showValAxisTitle: true,
    catAxisTitleFontSize: 14, valAxisTitleFontSize: 14, catAxisTitleColor: C.SUB, valAxisTitleColor: C.SUB,
    catAxisLabelFontSize: 14, valAxisLabelFontSize: 14, catAxisLabelColor: C.SUB, valAxisLabelColor: C.SUB,
    catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisTitleFontFace: "+mn-lt", valAxisTitleFontFace: "+mn-lt",
    valAxisMinVal: 0.2, valAxisMaxVal: 0.8, valAxisMajorUnit: 0.1, valAxisLabelFormatCode: "0.0",
    valGridLine: { color: C.LINE, size: 0.5 }, catGridLine: { style: "none" },
  });
  box(s, { x: 6.6, y: 1.35, w: 2.9, h: 2.4, fill: { color: C.BG_SOFT } });
  T(s, "読み取れること", { ...H, fontSize: 18, x: 6.85, y: 1.5, w: 2.5, h: 0.4 });
  T(s, bullets(["提案：数秒で収束", "比較：変動が続く"]), { x: 6.85, y: 2.05, w: 2.55, h: 1.5 });
  T(s, "※ダミーデータ", { x: 6.6, y: 4.5, w: 2.5, h: 0.3, fontSize: 12, color: C.SUB });
  s.addNotes("時間ごとの高度の変化です。オレンジの提案手法は、はじめに少し行き過ぎたあと、数秒で目標高度付近に収まります。開ループでは高度がゆっくり変動し続けます。※このグラフはダミーデータです。");

  // ===== 考察 =====
  sec("考察");
  s = add("考察");
  s.addText("高度の安定化は実現したが、計測範囲に制約が残る", { placeholder: "title" });
  [["できたこと", ["追加センサなしで高度を推定", "地上側だけで閉ループ制御"], C.MAIN_TINT, null],
   ["限界", ["カメラの視野内でのみ有効", "照明変化で検出が不安定に", "水平方向は未制御"], C.BG_SOFT, 0]].forEach(([h, pts, fill, emIdx], i) => {
    const x = 0.5 + i * 4.6;
    box(s, { x, y: 1.35, w: 4.4, h: 3.4, fill: { color: fill } });
    T(s, h, { ...H, x: x + 0.3, y: 1.55, w: 3.8, h: 0.5, valign: "middle" });
    T(s, bullets(pts.map((p, k) => (k === emIdx ? [p, EM] : p))), { x: x + 0.3, y: 2.3, w: 3.85, h: 2.3 });
  });
  s.addNotes("考察です。追加センサなしで、地上側だけで閉ループ制御が動作することを確認できました。一方で最も大きな制約は、カメラの視野内でしか使えないことです。ほかに照明変化と、水平方向が未制御であることが課題です。");

  // ===== まとめ =====
  sec("まとめ");
  s = add("まとめ");
  s.addText("まとめと今後の課題", { placeholder: "title" });
  box(s, { x: 0.5, y: 1.3, w: 9.0, h: 1.0, fill: { color: C.MAIN_TINT } });
  T(s, "地上ステレオカメラだけで、ホバリングを安定化", { ...EM, fontSize: 24, x: 0.8, y: 1.3, w: 8.4, h: 1.0, valign: "middle" });
  [["まとめ", ["色バンド＋視差で高度を推定", "開ループより誤差が減少"]], ["今後の課題", ["水平方向（x, y）への拡張", "照明変化に強い検出"]]].forEach(([h, pts], i) => {
    const x = 0.5 + i * 4.7;
    T(s, h, { ...H, x, y: 2.6, w: 4.2, h: 0.45, valign: "middle" });
    T(s, bullets(pts), { x, y: 3.25, w: 4.3, h: 1.4 });
  });
  s.addNotes("まとめです。地上のステレオカメラだけで、マイクロドローンのホバリングを安定させるシステムを提案し、実機で開ループより誤差が小さくなることを確認しました。今後は水平方向への拡張と、照明変化への対策に取り組みます。ご清聴ありがとうございました。");

  // ===== 参考文献 =====
  sec("参考文献");
  s = add("参考文献");
  s.addText("参考文献", { placeholder: "title" });
  [1, 2, 3, 4].forEach((n, i) => {
    const y = 1.4 + i * 0.75;
    T(s, `[${n}]`, { x: 0.5, y, w: 0.6, h: 0.5, fontSize: 16, bold: true, color: C.MAIN });
    T(s, "[要記入] 著者, “論文タイトル,” 会議・論文誌名, 巻, 号, ページ, 年.", { x: 1.15, y, w: 8.35, h: 0.5, fontSize: 16 });
  });
  s.addNotes("参考文献。実在・書誌情報を確認した文献のみを載せる。");

  // ===== 予備 =====
  sec("予備スライド");
  [["Q. なぜArUcoマーカーではなく色ブロブ検出か", ["[要記入] 比較実験で分かった一番の理由", "[要記入] 機体サイズとマーカーの大きさの関係", "[要記入] 処理負荷・フレームレートへの影響"]],
   ["Q. 画像処理の遅延は制御に影響しないか", ["[要記入] 画像取得〜指令送信までの遅延（実測値）", "[要記入] 制御周期との関係", "[要記入] 遅延を減らす工夫"]]].forEach(([q, a]) => {
    s = add("予備スライド", "APPENDIX");
    s.addText(q, { placeholder: "title" });
    box(s, { x: 0.5, y: 1.35, w: 9.0, h: 3.45, fill: { color: C.WHITE } });
    T(s, "回答", { ...H, x: 0.8, y: 1.55, w: 3, h: 0.45 });
    T(s, bullets(a.map((x, k) => (k === 0 ? [x, EM] : x))), { x: 0.8, y: 2.15, w: 8.4, h: 2.5 });
    s.addNotes("想定質問への回答用。本編では使わない。");
  });

  const out = process.argv[2] || "sample_uav_talk.pptx";
  await pres.writeFile({ fileName: out });
  await fixJapanese(out);
  console.log("wrote", out);
}

build();
