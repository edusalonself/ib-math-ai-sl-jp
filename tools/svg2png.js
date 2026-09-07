const {chromium} = require('/home/claude/.npm-global/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:1400,height:900}});
  for (const f of process.argv.slice(2)) {
    await p.goto('file://'+f);
    const el = await p.$('svg');
    await el.screenshot({path:f.replace(/\.svg$/,'.png')});
  }
  await b.close();
})();
