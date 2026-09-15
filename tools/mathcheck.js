const katex = require('/home/claude/.npm-global/lib/node_modules/katex');
const fs = require('fs');
const file = process.argv[2];
let s = fs.readFileSync(file, 'utf8');
// ★ 通貨の \$ は「エスケープされたドル」なので、数式の区切りと
//    取りちがえないように、いったん別の文字に置き換えます。
//    ($\$2000$ のような書き方が、以前ここで誤検出になっていました。)
s = s.replace(/\\\$/g, '\uE000');
// remove code fences
s = s.replace(/```[\s\S]*?```/g, '');
const items = [];
// display math $$ ... $$
s.replace(/\$\$([\s\S]*?)\$\$/g, (m, g) => { items.push(['display', g]); return ''; });
let t = s.replace(/\$\$[\s\S]*?\$\$/g, '');
// inline $...$
t.replace(/(?<!\$)\$([^$\n]+)\$(?!\$)/g, (m, g) => { items.push(['inline', g]); return ''; });
let bad = 0;
for (const [kind, src] of items) {
  try { katex.renderToString(src.replace(/\uE000/g, '\\$'), { displayMode: kind === 'display', throwOnError: true, strict: false }); }
  catch (e) { bad++; console.log('★', kind, '::', src.trim().slice(0, 90), '\n   ', e.message.split('\n')[0]); }
}
console.log(`checked ${items.length} math expressions, ${bad} failed`);
