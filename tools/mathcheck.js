const katex = require('/home/claude/.npm-global/lib/node_modules/katex');
const fs = require('fs');
const file = process.argv[2];
let s = fs.readFileSync(file, 'utf8');
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
  try { katex.renderToString(src, { displayMode: kind === 'display', throwOnError: true, strict: false }); }
  catch (e) { bad++; console.log('★', kind, '::', src.trim().slice(0, 90), '\n   ', e.message.split('\n')[0]); }
}
console.log(`checked ${items.length} math expressions, ${bad} failed`);
