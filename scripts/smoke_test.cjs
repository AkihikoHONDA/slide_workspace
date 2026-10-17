// Synthetic environment test. It is NOT a design template for real slides.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const PptxGenJS = require('pptxgenjs');
async function main() {
  const out = process.argv[2];
  if (!out) throw new Error('Usage: node scripts/smoke_test.cjs OUTPUT_DIRECTORY');
  fs.mkdirSync(out, { recursive: true });
  const p = new PptxGenJS();
  p.layout = 'LAYOUT_WIDE';
  p.author = 'Environment smoke test';
  p.subject = 'Synthetic test only; not a presentation template';
  p.title = 'Slide environment smoke test';
  p.lang = 'en-US';
  p.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri', lang: 'en-US' };
  let s = p.addSlide();
  s.addText('Environment test', {x:.6, y:.4, w:12, h:.7, fontSize:32, fontFace:'Cambria'});
  s.addText('Latin text: Calibri 16 pt; 0123456789.', {x:.6, y:1.4, w:11.5, h:.5, fontSize:16, fontFace:'Calibri'});
  s.addText('日本語の表示確認：測定・解析・結論', {x:.6, y:2.3, w:11.5, h:.7, fontSize:24, fontFace:'Noto Sans CJK JP', lang:'ja-JP'});
  s.addText('Synthetic sample — not a design template', {x:.6, y:4.4, w:11.5, h:.6, fontSize:20, fontFace:'Arial'});
  s.addNotes('SMOKE_NOTE_1: Notes are stored separately from slide text.');
  s = p.addSlide();
  s.addText('Native chart test — synthetic values', {x:.6, y:.4, w:12, h:.7, fontSize:28, fontFace:'Cambria'});
  s.addChart(p.ChartType.bar, [{name:'Test', labels:['A','B','C'], values:[2,3,1]}], {
    x:.8, y:1.6, w:11.7, h:4.8, barDir:'col', showLegend:false, showValue:true,
    catAxisLabelFontSize:16, valAxisLabelFontSize:16, dataLabelFormatCode:'0',
    catAxisLabelFontFace:'Arial', valAxisLabelFontFace:'Arial', dataLabelPosition:'outEnd'
  });
  s.addNotes('SMOKE_NOTE_2: Native chart, generated using synthetic data.');
  await p.writeFile({fileName:path.join(out,'smoke.pptx')});
  console.log('Synthetic smoke.pptx generated.');
}
main().catch(e => {console.error(e.message); process.exitCode=1;});
