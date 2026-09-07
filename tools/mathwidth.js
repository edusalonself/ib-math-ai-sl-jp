const katex = require('/home/claude/.npm-global/lib/node_modules/katex');
const fs = require('fs'), path = require('path');
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const KDIR = '/home/claude/.npm-global/lib/node_modules/katex/dist';

(async () => {
  const file = process.argv[2];
  const width = parseInt(process.argv[3] || '700', 10);
  let s = fs.readFileSync(file, 'utf8').replace(/```[\s\S]*?```/g, '');
  const disp = [];
  s.replace(/\$\$([\s\S]*?)\$\$/g, (m, g) => { disp.push(g); return ''; });
  const html = ['<meta charset="utf-8"><link rel="stylesheet" href="katex.min.css">',
    `<style>body{margin:0;font-size:16px} .box{width:${width}px;overflow:auto;border:0;margin:4px 0}</style>`];
  disp.forEach((d, i) => {
    let r;
    try { r = katex.renderToString(d, { displayMode: true, throwOnError: false, strict: false }); }
    catch (e) { r = '<span>ERR</span>'; }
    html.push(`<div class="box" data-i="${i}">${r}</div>`);
  });
  fs.writeFileSync(path.join(KDIR, '_probe.html'), html.join('\n'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: width + 60, height: 900 } });
  await p.goto('file://' + path.join(KDIR, '_probe.html'));
  await p.waitForTimeout(600);
  const over = await p.evaluate(() => [...document.querySelectorAll('.box')]
    .map(e => ({ i: +e.dataset.i, sw: e.scrollWidth, cw: e.clientWidth }))
    .filter(o => o.sw > o.cw + 2));
  console.log(`display equations: ${disp.length}, wider than ${width}px: ${over.length}`);
  for (const o of over) console.log(`  #${o.i} (${o.sw}px) :: ${disp[o.i].trim().slice(0, 120)}`);
  await b.close();
  fs.unlinkSync(path.join(KDIR, '_probe.html'));
})();
