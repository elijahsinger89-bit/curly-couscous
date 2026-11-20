#!/usr/bin/env node
/* Browser test of SINUMERIK_GENERATOR.html opened from file://, network blocked.
   Usage: node e2e.js <outDir>   (needs Playwright + Chromium) */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const here = __dirname;
const page_url = 'file://' + path.resolve(here, '..', 'SINUMERIK_GENERATOR.html');
const out = process.argv[2] || path.join(require('os').tmpdir(), 'sng_e2e');
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
const fx = n => path.join(here, 'fixtures', n + '.json');

let failures = 0;
function check(cond, msg) { if (cond) console.log('ok   ' + msg); else { failures++; console.log('FAIL ' + msg); } }

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1360, height: 900 } });
  const netAttempts = [];
  await ctx.route('**/*', route => {
    const u = route.request().url();
    if (u.startsWith('file://') || u.startsWith('blob:') || u.startsWith('data:')) return route.continue();
    netAttempts.push(u);
    return route.abort();
  });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', d => d.dismiss());   /* beforeunload etc. */
  await page.goto(page_url);
  check(await page.title() === 'SINUMERIK ONE Generator', 'page opens from file://');

  async function loadJob(name) {
    const [fc] = await Promise.all([page.waitForEvent('filechooser'), page.click('#btnLoad')]);
    await fc.setFiles(fx(name));
    await page.waitForSelector('.msg.ok');
  }
  async function generate(expectDialog, answer) {
    const dl = page.waitForEvent('download', { timeout: 5000 }).catch(() => null);
    await page.click('#btnGenerate');
    if (expectDialog) {
      await page.waitForSelector('#dlg[open]');
      await page.click('#dlg button[data-choice="' + (answer ? 'yes' : 'no') + '"]');
    }
    return dl;
  }
  function unzipCheck(zipPath, dest) {
    execFileSync('unzip', ['-t', '-q', zipPath], { stdio: 'pipe' });
    fs.mkdirSync(dest, { recursive: true });
    execFileSync('unzip', ['-o', '-q', zipPath, '-d', dest]);
  }

  /* 0. step builder on a fresh page */
  const rows = () => page.$$eval('#tab-config tbody tr', r => r.length);
  const stepVals = f => page.$$eval('[data-path$=".' + f + '"]', l => l.filter(i => /^steps\./.test(i.dataset.path)).map(i => i.value));
  await page.fill('[data-path="header.part"]', '00223344');
  await page.fill('[data-path="header.machine"]', 'HF5');
  await page.fill('[data-path="builder.last"]', '60');
  check((await page.textContent('#builderNote')).includes('B_00223344_010_HF5'), 'builder note shows the example name live');
  /* type into a structural field, then click Build straight away: the
     re-render must not swallow the click */
  await page.fill('[data-path="config.faces"]', '3');
  await page.click('[data-act="build"]');
  check(await page.$('#dlg[open]') === null, 'Build on the blank starter row asks nothing');
  check(await rows() === 6, 'Build 10-60 by 10 makes 6 rows (click right after typing still works)');
  check(JSON.stringify(await stepVals('program')) === JSON.stringify(['B_00223344_010_HF5', 'B_00223344_020_HF5', 'B_00223344_030_HF5',
    'B_00223344_040_HF5', 'B_00223344_050_HF5', 'B_00223344_060_HF5']), 'rows named B_PART_STEP_MACHINE');
  check(await page.$eval('[data-path="probeStep.program"]', e => e.value) === 'B_00223344_001_HF5', 'probe program named');
  check(await page.$eval('[data-path="config.totalNests"]', e => e.value) === '6', 'deferred re-render applied faces 3 x 2 = 6 nests');
  await page.fill('[data-path="steps.2.tool"]', 'EM_12');
  await page.dispatchEvent('[data-path="steps.2.tool"]', 'change');
  await page.fill('[data-path="builder.inc"]', '5');
  await page.fill('[data-path="builder.last"]', '50');
  await page.click('[data-act="build"]');
  await page.waitForSelector('#dlg[open]');
  const dtext = await page.textContent('#dlgBody');
  check(dtext.includes('6 rows, 6 with a tool, program or tolerance'), 'dialog says how many rows hold data: ' + dtext.slice(0, 80));
  await page.click('#dlg button[data-choice="cancel"]');
  check(await rows() === 6 && (await stepVals('tool'))[2] === 'EM_12', 'Cancel changes nothing');
  await page.click('[data-act="build"]');
  await page.waitForSelector('#dlg[open]');
  await page.keyboard.press('Escape');
  check(await rows() === 6, 'Escape = cancel');
  await page.click('[data-act="build"]');
  await page.waitForSelector('#dlg[open]');
  await page.click('#dlg button[data-choice="keep"]');
  check(JSON.stringify(await stepVals('step')) === JSON.stringify(['10', '15', '20', '25', '30', '35', '40', '45', '50', '60']),
    'Keep: missing steps added, step 60 kept, sorted');
  check((await stepVals('tool'))[4] === 'EM_12' && (await stepVals('program'))[4] === 'B_00223344_030_HF5', 'Keep: edited row 30 preserved');
  await page.click('[data-act="build"]');
  await page.waitForSelector('#dlg[open]');
  await page.click('#dlg button[data-choice="overwrite"]');
  check(await rows() === 9 && (await stepVals('tool')).every(t => t === ''), 'Overwrite: 9 fresh rows 10-50 by 5');
  await page.fill('[data-path="builder.first"]', '50');
  await page.fill('[data-path="builder.last"]', '10');
  await page.click('[data-act="build"]');
  check((await page.textContent('#msgs')).includes('must not be below'), 'builder range error is shown');
  await page.screenshot({ path: path.join(out, 'shot_builder_light.png'), clip: { x: 0, y: 0, width: 1360, height: 900 } });
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.screenshot({ path: path.join(out, 'shot_builder_dark.png'), clip: { x: 0, y: 0, width: 1360, height: 900 } });
  await page.emulateMedia({ colorScheme: 'light' });

  /* 1. load the old-package job and generate */
  await loadJob('f1_old_package');
  check((await page.textContent('#jobLabel')).includes('02215800_001'), 'job loaded (header shows part number)');
  check(await page.$eval('[data-path="config.machineType"]', e => e.value) === 'HF', 'old A/B job loads as machine type HF');
  check((await page.textContent('.kinaxes')).includes('A = trunnion (table), B = rotary'), 'machine type shows its axes');
  await page.click('[data-kin="AXES"]');
  check(await page.$eval('[data-path="config.trunnion"]', e => e.value) === 'A' && await page.$eval('[data-path="config.rotary"]', e => e.value) === 'B',
        'Axes by hand starts from the machine type axes (A / B)');
  await page.click('[data-kin="MACHINE"]');
  check(await page.$eval('[data-path="config.machineType"]', e => e.value) === 'HF', 'back to Machine type: HF again');
  let d = await generate(false);
  check(!!d, 'Generate ZIP downloads a file');
  const z1 = path.join(out, 'f1.zip');
  await d.saveAs(z1);
  check(/^02215800_001_NC_\d{4}-\d\d-\d\d\.zip$/.test(d.suggestedFilename()), 'zip name ' + d.suggestedFilename());
  unzipCheck(z1, path.join(out, 'f1'));
  check(fs.existsSync(path.join(out, 'f1', 'WKS', 'A_P1.MPF')) && fs.existsSync(path.join(out, 'f1', 'CUS', 'L_RUN_NESTS.SPF')) &&
        fs.existsSync(path.join(out, 'f1', 'DEF', 'UGUD.DEF')), 'zip passes unzip -t and holds WKS/CUS/DEF files');
  check(await page.$$eval('.flist li', l => l.length) === 19, 'output tab lists 19 files after generate');

  /* 2. preview + single-file download */
  await page.click('.flist li:has-text("L_RUN_NESTS.SPF")');
  const pre = await page.textContent('.viewer pre');
  check(pre.includes('CALL LD_PROG') && pre.includes('GETEXET(LV_TNO)'), 'preview shows L_RUN_NESTS content');
  const d1p = page.waitForEvent('download');
  await page.click('[data-act="dlone"]');
  const d1 = await d1p;
  check(d1.suggestedFilename() === 'L_RUN_NESTS.SPF', 'single-file download fallback works');

  /* 3. blank work offset: No stops, Yes generates */
  await loadJob('f4_32nests');
  d = await generate(true, false);
  check(d === null, 'blank WO: answering No downloads nothing');
  check((await page.textContent('#msgs')).includes('Generation stopped'), 'blank WO: No shows "Generation stopped"');
  const dlgText = await page.textContent('#dlgBody p');
  check(dlgText.includes('17'), 'blank WO dialog lists nest 17: ' + dlgText.trim());
  d = await generate(true, true);
  check(!!d, 'blank WO: answering Yes generates');
  if (d) { await d.saveAs(path.join(out, 'f4.zip')); unzipCheck(path.join(out, 'f4.zip'), path.join(out, 'f4')); }

  /* 4. validation errors block generation and mark fields */
  await page.click('nav.tabs button[data-tab="config"]');
  await page.fill('[data-path="steps.0.tool"]', '');
  await page.dispatchEvent('[data-path="steps.0.tool"]', 'change');
  d = await generate(false);
  check(d === null, 'validation error blocks Generate');
  check((await page.textContent('#msgs')).includes('tool name is required'), 'error message names the problem');
  check(await page.$eval('[data-path="steps.0.tool"]', e => e.classList.contains('err')), 'bad field is highlighted');
  await page.click('#msgs a');
  check(await page.evaluate(() => document.activeElement.dataset.path) === 'steps.0.tool', 'clicking the error focuses the field');

  /* 5. structure edits: faces/nests drive the WCS table, steps add/remove */
  await loadJob('f1_old_package');
  await page.fill('[data-path="config.faces"]', '3');
  await page.dispatchEvent('[data-path="config.faces"]', 'change');
  check(await page.$eval('[data-path="config.totalNests"]', e => e.value) === '6', 'faces 3 x 2 sets total nests to 6');
  check(await page.$$eval('#tab-wcs tbody tr', r => r.length) === 6, 'WCS table has 6 rows');
  const angles = await page.$$eval('#tab-wcs tbody tr td:nth-child(8) input', l => l.map(i => i.placeholder));
  check(JSON.stringify(angles) === JSON.stringify(['0.000', '0.000', '120.000', '120.000', '240.000', '240.000']), 'rotary defaults 0/120/240: ' + angles);
  const before = await page.$$eval('#tab-config tbody tr', r => r.length);
  await page.click('[data-act="add"]');
  const added = await page.$eval('[data-path="steps.' + before + '.step"]', e => e.value);
  check(added === '60', 'Add step numbers the new row 60');
  await page.click('[data-act="del"][data-i="' + before + '"]');
  check(await page.$$eval('#tab-config tbody tr', r => r.length) === before, 'remove step');
  await page.selectOption('[data-path="config.mode"]', 'SINGLE PART');
  check(await page.$$eval('#tab-wcs tbody tr', r => r.length) === 1, 'single part shows one WCS row');

  /* 6. save -> load round trip */
  await loadJob('f2_horizontal_inch');
  const sp = page.waitForEvent('download');
  await page.click('#btnSave');
  const sd = await sp;
  const saved = path.join(out, 'saved_job.json');
  await sd.saveAs(saved);
  check(sd.suggestedFilename() === 'HX4410_job.json', 'Save job names the file after the part');
  const orig = JSON.parse(fs.readFileSync(fx('f2_horizontal_inch'), 'utf8'));
  const back = JSON.parse(fs.readFileSync(saved, 'utf8'));
  const norm = await page.evaluate(o => JSON.stringify(window.SNG.normalizeJob(o)), orig);
  check(JSON.stringify(back) === norm, 'saved JSON equals the loaded job');
  check(back.builder && back.builder.first === '10' && back.builder.inc === '10', 'saved JSON carries the builder fields');
  d = await generate(false);
  await d.saveAs(path.join(out, 'f2a.zip'));
  const [fc] = await Promise.all([page.waitForEvent('filechooser'), page.click('#btnLoad')]);
  await fc.setFiles(saved);
  await page.waitForSelector('.msg.ok');
  d = await generate(false);
  await d.saveAs(path.join(out, 'f2b.zip'));
  unzipCheck(path.join(out, 'f2a.zip'), path.join(out, 'f2a'));
  unzipCheck(path.join(out, 'f2b.zip'), path.join(out, 'f2b'));
  let same = true;
  for (const f of execFileSync('find', [path.join(out, 'f2a'), '-type', 'f']).toString().trim().split('\n')) {
    const g = f.replace('/f2a/', '/f2b/');
    if (!fs.existsSync(g) || fs.readFileSync(f, 'utf8') !== fs.readFileSync(g, 'utf8')) same = false;
  }
  check(same, 'reloaded job generates identical files');

  /* 6b. Import B list on a fresh page (sample written by the hyperMILL export test) */
  {
    const p2 = await ctx.newPage();
    p2.on('pageerror', e => errors.push(String(e)));
    p2.on('dialog', d => d.dismiss());
    await p2.goto(page_url);
    const sample = path.join(here, 'fixtures', 'b_list_sample.json');
    const importIt = async () => {
      const [fc] = await Promise.all([p2.waitForEvent('filechooser'), p2.click('#btnBList')]);
      await fc.setFiles(sample);
    };
    const vals = f => p2.$$eval('[data-path$=".' + f + '"]', l => l.filter(i => /^steps\./.test(i.dataset.path)).map(i => i.value));
    await importIt();
    await p2.waitForSelector('#dlg[open]');
    check((await p2.textContent('#dlgBody')).includes('The B program list is INCH, this page is METRIC'), 'import: units differ -> asks');
    await p2.click('#dlg button[data-choice="switch"]');
    await p2.waitForSelector('.msg');
    check(await p2.$eval('[data-path="config.units"]', e => e.value) === 'INCH', 'import: page switched to INCH');
    check(await p2.$eval('[data-path="header.part"]', e => e.value) === '00948602_025' &&
          await p2.$eval('[data-path="header.machine"]', e => e.value) === 'HF5', 'import: blank header filled with part and machine');
    check(JSON.stringify(await vals('program')) === JSON.stringify(['B_00948602_025_010_HF5', 'B_00948602_025_020_HF5',
      'B_00948602_025_030_HF5', 'B_00948602_025_040_HF5']), 'import: 4 B programs in the step table');
    check(JSON.stringify(await vals('tool')) === JSON.stringify(['905083900', '475080900', '416580900', '350080900']), 'import: tool IDs');
    check(JSON.stringify(await vals('brkTol')) === JSON.stringify(['0.0040', '0.0020', '', '0.0006']), 'import: preset tolerances');
    check(await p2.$eval('[data-path="steps.2.brkTol"]', e => e.classList.contains('err')) &&
          !(await p2.$eval('[data-path="steps.0.brkTol"]', e => e.classList.contains('err'))), 'import: blank tolerances red, preset ones not');
    const m1 = await p2.textContent('#msgs');
    check(m1.includes('Imported the 4 B programs') && m1.includes('1 step has break check on and no tolerance') &&
          m1.includes('Left out in hyperMILL: B_00948602_025_111_HF5'), 'import: message with blanks and left-out compound jobs');
    check(await p2.$eval('[data-path="probeStep.program"]', e => e.value) === 'B_00948602_025_001_HF5' &&
          !(await p2.$eval('[data-path="probeStep.program"]', e => e.classList.contains('err'))), 'import: probe program name filled, not red');
    check(!m1.includes('probeStep') && !m1.includes('Probe step:'), 'import: no probe step error in the message');
    await p2.fill('[data-path="steps.0.tool"]', 'EDITED');
    await p2.dispatchEvent('[data-path="steps.0.tool"]', 'change');
    await importIt();
    await p2.waitForSelector('#dlg[open]');
    check((await p2.textContent('#dlgTitle')) === 'Step table already has data', 'import over data: asks overwrite / keep');
    await p2.click('#dlg button[data-choice="keep"]');
    await p2.waitForSelector('.msg');
    check((await vals('tool'))[0] === 'EDITED' && (await vals('step')).length === 4, 'import keep: edited row kept, nothing added');
    await importIt();
    await p2.waitForSelector('#dlg[open]');
    await p2.click('#dlg button[data-choice="overwrite"]');
    await p2.waitForSelector('.msg');
    check((await vals('tool'))[0] === '905083900', 'import overwrite: rows replaced');
    check(await p2.$eval('[data-path="probeStep.program"]', e => e.value) === 'B_00948602_025_001_HF5', 'import overwrite: probe program name kept generated');

    /* column header boxes: all on / all off, per-row boxes still work */
    const ticks = f => p2.$$eval('[data-path$=".' + f + '"]', l => l.filter(i => /^steps\./.test(i.dataset.path)).map(i => i.checked));
    const dis = f => p2.$$eval('[data-path$=".' + f + '"]', l => l.filter(i => /^steps\./.test(i.dataset.path)).map(i => i.disabled));
    const head = k => p2.$eval('[data-col="' + k + '"]', e => (e.disabled ? 'disabled ' : '') + (e.indeterminate ? 'dash' : e.checked ? 'ticked' : 'empty'));
    check(await head('meas') === 'ticked' && await head('measAlways') === 'empty', 'header boxes: Measure ticked (all on), Always empty (all off)');
    await p2.click('[data-col="meas"]');
    check(JSON.stringify(await ticks('meas')) === '[false,false,false,false]' && await head('meas') === 'empty' &&
          await head('measAlways') === 'disabled empty', 'Measure header: all off, Always header disabled');
    await p2.click('[data-col="meas"]');
    check(JSON.stringify(await ticks('meas')) === '[true,true,true,true]' && await head('meas') === 'ticked', 'Measure header: all on again');
    await p2.click('[data-path="steps.1.meas"]');
    check(JSON.stringify(await ticks('meas')) === '[true,false,true,true]' && await head('meas') === 'dash', 'one row unticked: row box works, header shows a dash');
    await p2.click('[data-col="measAlways"]');
    check(JSON.stringify(await ticks('measAlways')) === '[true,false,true,true]' && await head('measAlways') === 'ticked',
          'Always header: on for the rows with Measure on only');
    await p2.click('[data-col="meas"]');
    check(JSON.stringify(await ticks('meas')) === '[true,true,true,true]', 'dash clicked: every row on');
    await p2.click('[data-col="brk"]');
    check(JSON.stringify(await ticks('brk')) === '[false,false,false,false]' &&
          JSON.stringify(await dis('brkTol')) === '[true,true,true,true]' && JSON.stringify(await dis('maxBrk')) === '[true,true,true,true]',
          'Brk check header off: tolerance and max brk disabled on every row');
    await p2.click('[data-col="brk"]');
    await p2.click('[data-col="debug"]');
    await p2.click('[data-col="setpiece"]');
    check(JSON.stringify(await ticks('brk')) === '[true,true,true,true]' && JSON.stringify(await ticks('debug')) === '[true,true,true,true]' &&
          JSON.stringify(await ticks('setpiece')) === '[false,false,false,false]' && JSON.stringify(await dis('life')) === '[true,true,true,true]',
          'Brk check all on, Debug M1 all on, SETPIECE all off (life disabled)');
    await p2.screenshot({ path: path.join(out, 'shot_column_boxes.png'), clip: { x: 0, y: 0, width: 1360, height: 900 } });
    await p2.selectOption('[data-path="config.units"]', 'METRIC');
    await importIt();
    await p2.waitForSelector('#dlg[open]');
    await p2.click('#dlg button[data-choice="cancel"]');
    check((await p2.textContent('#msgs')).includes('Import cancelled') &&
          await p2.$eval('[data-path="config.units"]', e => e.value) === 'METRIC', 'import cancel: page unchanged');
    const [fc2] = await Promise.all([p2.waitForEvent('filechooser'), p2.click('#btnBList')]);
    await fc2.setFiles(fx('f1_old_package'));
    await p2.waitForSelector('.msg.bad');
    check((await p2.textContent('#msgs')).includes('Not a B program list'), 'import: a job file is rejected as not a B program list');
    await p2.close();
  }

  /* 6c. CMC: tab 5 only while a row has CMC, cards, defaults, validation, zip */
  {
    await loadJob('f1_old_package');
    const cmcBtn = () => page.$eval('#tabBtnCmc', b => !b.hidden);
    check(!(await cmcBtn()), 'CMC tab hidden when no row has CMC');
    check(await page.$('[data-col="cmc"]') !== null && await page.$('[data-path="steps.0.cmc"]') !== null, 'CMC column with header box in the step table');
    await page.check('[data-path="steps.0.cmc"]');
    await page.waitForFunction(() => !document.querySelector('#tabBtnCmc').hidden);
    check(await cmcBtn(), 'ticking CMC shows tab 5');
    await page.click('#tabBtnCmc');
    check(await page.$$eval('.cmccard', l => l.length) === 1, 'one CMC card for the ticked row');
    check(await page.$eval('[data-path="cmcR.first"]', e => e.placeholder) === '700', 'R block start shown (default R700)');
    await page.selectOption('[data-path="steps.0.cmcTool"]', 'TURNING');
    check(await page.$eval('[data-path="steps.0.cmcSign"]', e => e.value) === 'LARGER', 'turning bore: +wear makes the bore larger by default');
    check(await page.$('[data-path="steps.0.cmcUnit"]') !== null, 'turning card shows the radius / diameter choice');
    await page.selectOption('[data-path="steps.0.cmcFeature"]', 'RECT POCKET');
    check(await page.$('[data-path="steps.0.cmcNomY"]') !== null && await page.$('[data-path="steps.0.cmcZoneY"]') !== null, 'rectangle card asks for Y length and zone Y');
    await page.selectOption('[data-path="steps.0.cmcFeature"]', 'BORE ARC');
    check(await page.$('[data-path="steps.0.cmcIncAng"]') !== null && await page.$('[data-path="steps.0.cmcZone"]') === null, 'circle segment card: angles, no protection zone');
    await page.selectOption('[data-path="steps.0.cmcFeature"]', 'WALL Y');
    check(await page.$('[data-path="steps.0.cmcSide"]') !== null && await page.$('[data-path="steps.0.cmcY"]') === null, 'wall Y card: material side, point X only');
    d = await generate(false);
    check(d === null, 'empty CMC card blocks Generate');
    check((await page.textContent('#msgs')).includes('CMC step'), 'CMC errors listed');
    await page.click('#msgs a:has-text("nominal")');
    check(await page.evaluate(() => document.activeElement.dataset.path) === 'steps.0.cmcNom' &&
          await page.$eval('#tab-cmc', t => t.classList.contains('active')), 'clicking a CMC error opens tab 5 at the field');
    await page.click('nav.tabs button[data-tab="config"]');
    await page.uncheck('[data-path="steps.0.cmc"]');
    await page.waitForFunction(() => document.querySelector('#tabBtnCmc').hidden);
    check(!(await cmcBtn()), 'unticking the last CMC row hides tab 5');
    await page.click('[data-col="cmc"]');
    check(await page.$$eval('[data-path$=".cmc"]', l => l.every(i => i.checked)) && await cmcBtn(), 'CMC header box ticks every row');
    await page.click('#tabBtnCmc');
    await page.evaluate(() => { const j = window.SNG_UI.getJob(); j.steps.forEach(s => { s.cmc = false; }); window.SNG_UI.setJob(j); });
    check(!(await cmcBtn()) && await page.$eval('#tab-config', t => t.classList.contains('active')), 'tab 5 open when its last CMC row goes: back to tab 1');
    await loadJob('f9_cmc_turning');
    await page.click('#tabBtnCmc');
    check(await page.$$eval('.cmccard', l => l.length) === 5, 'turning CMC job: 5 cards');
    check((await page.textContent('#tab-cmc')).includes('R700-R749') && (await page.textContent('#tab-cmc')).includes('R900-R949'), 'R ranges listed per CMC step');
    await page.screenshot({ path: path.join(out, 'shot_cmc.png'), fullPage: true });
    d = await generate(false);
    check(!!d, 'CMC job generates');
    if (d) {
      const zc = path.join(out, 'cmc.zip');
      await d.saveAs(zc);
      unzipCheck(zc, path.join(out, 'cmc'));
      const w = n => fs.existsSync(path.join(out, 'cmc', 'WKS', n));
      check(w('C_P1_CMC10.SPF') && w('C_P1_CMC10_M.SPF') && w('C_P1_CMC50.SPF') && w('C_P1_CMC_BACK.SPF') && w('C_P1_CMC_LOG.SPF') && w('C_P1_CMC_CLEAR.SPF'),
            'zip holds the CMC programs');
      const lint = require('child_process').spawnSync('python3', [path.join(here, 'nc_lint.py'), path.join(out, 'cmc')], { encoding: 'utf8' });
      check(lint.status === 0, 'CMC zip passes the NC lint ' + (lint.status ? lint.stdout.slice(-400) : ''));
    }
    const sp2 = page.waitForEvent('download');
    await page.click('#btnSave');
    const sd2 = await sp2;
    const saved2 = path.join(out, 'saved_cmc.json');
    await sd2.saveAs(saved2);
    const sj = JSON.parse(fs.readFileSync(saved2, 'utf8')), fj = JSON.parse(fs.readFileSync(fx('f9_cmc_turning'), 'utf8'));
    check(sj.steps[0].cmcSwivel === fj.steps[0].cmcSwivel && sj.steps[1].cmcUnit === 'DIAMETER' && sj.cmcR.first === '700', 'CMC card saved in the job file');
  }

  /* 6d. probe swivel: tab 2 box, CMC card box, sources, decoded line, defaults, zip */
  {
    await loadJob('f10_swivel');
    await page.click('nav.tabs button[data-tab="probing"]');
    const swText = () => page.$eval('#tab-probing .swline', e => e.textContent);
    check(await page.$eval('[data-path="probing.swMode"]', e => e.value) === 'ANGLES' && await page.$('[data-path="probing.swA"]') !== null &&
          await page.$('[data-path="probing.swLine"]') === null, 'tab 2 swivel: ANGLES shows only the angles');
    check((await swText()).includes('about X -90') && (await swText()).includes('CYCLE800(0,"H",0,57,0,0,0,-90,0,0,0,0,0,1,0,1)'), 'tab 2 swivel: line and decoded text shown');
    await page.selectOption('[data-path="probing.swMode"]', 'B PROGRAM');
    const opts = await page.$$eval('[data-path="probing.swFrom"] option', l => l.map(o => o.value));
    check(JSON.stringify(opts) === JSON.stringify(['', 'B_SWIVEL_CHUCK_010']), 'B PROGRAM dropdown lists only B programs with one plane: ' + opts);
    await page.selectOption('[data-path="probing.swFrom"]', 'B_SWIVEL_CHUCK_010');
    check((await swText()).includes('about X -90') && (await swText()).includes('from B_SWIVEL_CHUCK_010'), 'B PROGRAM: the plane of that B program, decoded');
    await page.selectOption('[data-path="probing.swMode"]', 'PASTE');
    await page.fill('[data-path="probing.swLine"]', 'CYCLE800(0,"TURN_TRAFO",210,57,,,,0,0,0,,,,-1,0,102)');
    await page.dispatchEvent('[data-path="probing.swLine"]', 'change');
    check((await swText()).includes('aligns a turning tool'), 'PASTE: a turning-tool alignment is refused on the page');
    await page.selectOption('[data-path="probing.swMode"]', 'NONE');
    check(await page.$('[data-path="probing.swA"]') === null && (await swText()).includes('nest face'), 'NONE: no fields, nest face');
    await page.fill('[data-path="probing.swBlock"]', ''); await page.dispatchEvent('[data-path="probing.swBlock"]', 'change');
    await page.selectOption('[data-path="probing.swDir"]', '');
    await page.selectOption('[data-path="probing.swMode"]', 'ANGLES');
    check(await page.$eval('[data-path="probing.swBlock"]', e => e.value) === 'H' && await page.$eval('[data-path="probing.swDir"]', e => e.value) === '+1',
          'ANGLES: data block and direction prefilled from the imported plane');
    await page.click('#tabBtnCmc');
    const card0 = await page.$eval('.cmccard[data-cmc-row="0"] .swline', e => e.textContent);
    check(await page.$eval('[data-path="steps.0.cmcSwMode"]', e => e.value) === 'AUTO' && card0.includes('from B_SWIVEL_CHUCK_010'), 'CMC card: AUTO = the plane of its own B program');
    await page.screenshot({ path: path.join(out, 'shot_swivel_cmc.png'), fullPage: false });
    await page.click('nav.tabs button[data-tab="probing"]');
    await page.screenshot({ path: path.join(out, 'shot_swivel_probing.png'), fullPage: true });
    d = await generate(false);
    check(!!d, 'swivel job generates');
    if (d) {
      const zs = path.join(out, 'swivel.zip');
      await d.saveAs(zs);
      unzipCheck(zs, path.join(out, 'swivel'));
      const pr = fs.readFileSync(path.join(out, 'swivel', 'WKS', 'C_P1_PROBE.SPF'), 'utf8');
      check(pr.includes('CYCLE800(0,"H",0,57,0,0,0,-90,0,0,0,0,0,1,0,1)') && /CYCLE800\(\)\s+;swivel back/.test(pr), 'probe program: swivel, then CYCLE800() at the end');
      const lint = require('child_process').spawnSync('python3', [path.join(here, 'nc_lint.py'), path.join(out, 'swivel')], { encoding: 'utf8' });
      check(lint.status === 0, 'swivel zip passes the NC lint ' + (lint.status ? lint.stdout.slice(-400) : ''));
    }
  }

  /* 6e. 1.6.0 screens: picture and help follow the box you are in, More settings, errors under the box, strip */
  {
    await loadJob('f10_swivel');
    /* your step 570: turning bore 5.721, zone 5, probe depth Z-1, approach Z1, swivel A-90, ball 0.118 */
    await page.evaluate(() => {
      const j = window.SNG_UI.getJob();
      Object.assign(j.steps[2], { step: '570', tool: '943580900', program: 'B_00984602_025_570_HF5', cmcTool: 'TURNING', cmcFeature: 'BORE', cmcSign: 'LARGER',
        cmcUnit: 'RADIUS', cmcNom: '5.721', cmcTolP: '.001', cmcTolM: '.001', cmcStock: '.002', cmcX: '0', cmcY: '0', cmcZ: '-1', cmcAppZ: '1', cmcZone: '5',
        cmcSwMode: 'ANGLES', cmcSwA: '-90', cmcSwivel: '', cmcVerify: true, cmcOut: 'RECUT', cmcMaxTry: '1', cmcClean: 'NONE' });
      j.probing.ballDia = '.118';
      window.SNG_UI.setJob(j);
    });
    await page.click('#tabBtnCmc');
    const card = '.cmccard[data-cmc-row="2"]';
    check(await page.$eval(card + ' details.more', d => !d.open), 'More settings closed by default');
    await page.click(card + ' [data-path="steps.2.cmcZ"]');
    check((await page.textContent(card + ' .help b')) === 'Probe depth Z' && (await page.textContent(card + ' .help')).includes('Z-1'),
          'clicking Probe depth Z shows its help with the value');
    check(await page.$eval(card + ' label.f.focus', l => l.textContent.startsWith('Probe depth Z')) &&
          await page.$eval(card + ' svg', () => true) && (await page.$$eval(card + ' .pic svg .hi', l => l.length)) > 0, 'the box and its part of the picture are highlighted');
    const live = await page.textContent(card + ' dl.live');
    check(live.includes('Ø5.717') && live.includes('S_ID -2') && live.includes('X2.6793') && live.includes('fits (0.1203 clear)'),
          'live numbers: expected Ø5.717, S_ID -2, test plunge X2.6793, ball fits: ' + live.replace(/\s+/g, ' ').slice(0, 300));
    check((await page.textContent(card + ' .does')).includes('re-cut up to 1 time, then hold'), 'What the machine does: verify and re-cut');
    check((await page.textContent(card + ' .vt')).includes('swivelled about X -90'), 'swivel shown under the picture (about X -90)');
    await page.click(card + ' [data-path="steps.2.cmcZone"]');
    check((await page.textContent(card + ' .help b')) === 'Protection zone' && (await page.textContent(card + ' .help')).includes('island'), 'zone help explains the island');
    await page.screenshot({ path: path.join(out, 'shot16_cmc_light.png'), fullPage: false, clip: { x: 0, y: 0, width: 1360, height: 900 } });
    await page.$eval(card, el => el.scrollIntoView());
    await page.screenshot({ path: path.join(out, 'shot16_cmc_card.png'), fullPage: false });
    /* more settings opens on a non-default value and on an error */
    await page.evaluate(() => { const j = window.SNG_UI.getJob(); j.steps[2].cmcEdge = '0'; window.SNG_UI.setJob(j); });
    await page.click('#tabBtnCmc');
    check(await page.$eval(card + ' details.more', d => d.open), 'More settings open when a value in it is not the default');
    d = await generate(false);
    check(d === null && (await page.textContent(card + ' details.more .ferr')).includes('edge (D number) must be 1-9'), 'the error shows under the box inside More settings');
    await page.evaluate(() => { const j = window.SNG_UI.getJob(); j.steps[2].cmcEdge = '1'; j.probing.ballDia = '1.0'; window.SNG_UI.setJob(j); });
    await page.click('#tabBtnCmc');
    check((await page.textContent(card)).includes('does not fit between the protection zone') && (await page.textContent(card + ' dl.live')).includes('does NOT fit'),
          'ball 1.0 does not fit: warning on the card and in the live numbers');
    /* probing tab: strip, jumps, help scoped to its card */
    await page.click('nav.tabs button[data-tab="probing"]');
    const strip = await page.$$eval('#tab-probing .strip .step', l => l.map(b => [b.textContent, b.classList.contains('off')]));
    check(JSON.stringify(strip) === JSON.stringify([['Tool call', false], ['Swivel', false], ['Health check', true], ['Part check', true], ['Z datum', false],
          ['XY datum: BOSS', false], ['Swivel back', false]]), 'sequence strip: health and part check greyed ' + JSON.stringify(strip));
    await page.click('#tab-probing [data-path="probing.diameter"]');
    check((await page.textContent('#pr-xy .help b')) === 'Diameter' && (await page.textContent('#pr-z .help b')) !== 'Diameter', 'probing help only on the card of the box');
    await page.click('#tab-probing .strip .step:has-text("Z datum")');
    await page.waitForTimeout(400);
    check(await page.$eval('#pr-z', el => { const r = el.getBoundingClientRect(); return r.top < 200 && r.top > -10; }), 'strip jumps to the Z datum card (' + await page.$eval('#pr-z', el => Math.round(el.getBoundingClientRect().top)) + ')');
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: path.join(out, 'shot16_probing_light.png'), fullPage: true });
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.screenshot({ path: path.join(out, 'shot16_probing_dark.png'), fullPage: true });
    await page.click('#tabBtnCmc');
    await page.$eval(card, el => el.scrollIntoView());
    await page.screenshot({ path: path.join(out, 'shot16_cmc_card_dark.png'), fullPage: false });
    await page.emulateMedia({ colorScheme: 'light' });
    /* every picture of every feature draws */
    for (const f of ['BORE', 'BOSS', 'SLOT X', 'SLOT Y', 'WEB X', 'WEB Y', 'RECT POCKET', 'RECT SPIGOT', 'BORE ARC', 'BOSS ARC', 'WALL X', 'WALL Y', 'FLOOR Z']) {
      await page.evaluate(ft => { const j = window.SNG_UI.getJob(); j.steps[2].cmcFeature = ft; j.steps[2].cmcNomY = '3'; j.steps[2].cmcIncAng = '30'; window.SNG_UI.setJob(j); }, f);
      await page.click('#tabBtnCmc');
      const n = await page.$$eval(card + ' .pic svg', l => l.length);
      if (n !== 2) check(false, 'feature ' + f + ': two pictures (' + n + ')');
    }
    check(errors.length === 0, 'every feature draws without a page error');
  }

  /* 6f. 1.7.0 machine type */
  {
    await loadJob('f2_horizontal_inch');
    check(await page.$eval('[data-path="config.machineType"]', e => e.value) === 'H4_B', 'old NONE/B job loads as machine type 4-axis B');
    const opts = await page.$$eval('[data-path="config.machineType"] option', l => l.map(o => o.textContent));
    check(opts.length === 6 && opts.filter(o => o.includes('layout needed')).length === 2, 'six machine types, the two swivel heads marked layout needed');
    await page.selectOption('[data-path="config.machineType"]', 'F_V_SWIVEL');
    await page.click('#btnGenerate');
    await page.waitForSelector('#msgs .msg');
    check((await page.textContent('#msgs')).includes('layout not set up yet'), 'head machine without layout: error, nothing generated');
    await page.selectOption('[data-path="config.machineType"]', 'HF');
    check((await page.textContent('.kinaxes')).includes('A = trunnion'), 'HF selected: axes shown');
    await page.click('nav.tabs button[data-tab="wcs"]');
    check((await page.textContent('#tab-wcs thead')).includes('Trunnion A'), 'WCS table follows the machine type (Trunnion A)');
    await page.click('nav.tabs button[data-tab="config"]');
    await page.screenshot({ path: path.join(out, 'shot17_machine_light.png'), clip: { x: 0, y: 0, width: 1360, height: 560 } });
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.screenshot({ path: path.join(out, 'shot17_machine_dark.png'), clip: { x: 0, y: 0, width: 1360, height: 560 } });
    await page.emulateMedia({ colorScheme: 'light' });
    await page.click('[data-kin="AXES"]');
    await page.screenshot({ path: path.join(out, 'shot17_axes_light.png'), clip: { x: 0, y: 0, width: 1360, height: 560 } });
    await page.click('[data-kin="MACHINE"]');
    /* 1.8.0 nutating head */
    await page.selectOption('[data-path="config.machineType"]', 'F_V_NUT');
    check((await page.textContent('.kinaxes')).includes('B = nutating head'), 'vertical nutating: axes shown');
    await page.click('nav.tabs button[data-tab="wcs"]');
    const th = await page.textContent('#tab-wcs thead');
    check(th.includes('Trunnion NONE') && th.includes('Table C'), 'vertical nutating: WCS table has Table C, no trunnion');
    await page.click('nav.tabs button[data-tab="config"]');
    await page.selectOption('[data-path="config.machineType"]', 'F_H_NUT');
    await page.click('nav.tabs button[data-tab="output"]');
    await page.click('[data-act="preview"]');
    await page.waitForSelector('.flist li');
    await page.click('.flist li:has-text("B_TEMPLATE.SPF")');
    check((await page.textContent('#tab-output')).includes('G0 C-180'), 'horizontal nutating: B_TEMPLATE ends with G0 C-180');
    await page.click('nav.tabs button[data-tab="config"]');
    await page.screenshot({ path: path.join(out, 'shot18_nutating_light.png'), clip: { x: 0, y: 0, width: 1360, height: 560 } });
  }

  /* 7. screenshots for review */
  await loadJob('f1_old_package');
  await page.screenshot({ path: path.join(out, 'shot_config.png'), fullPage: true });
  await page.click('nav.tabs button[data-tab="probing"]');
  await page.screenshot({ path: path.join(out, 'shot_probing.png'), fullPage: true });
  await page.click('nav.tabs button[data-tab="wcs"]');
  await page.screenshot({ path: path.join(out, 'shot_wcs.png'), fullPage: true });
  await page.click('nav.tabs button[data-tab="output"]');
  await page.click('[data-act="preview"]');
  await page.waitForSelector('.flist li');
  await page.click('.flist li:has-text("B_XXXX_001.SPF")');
  await page.screenshot({ path: path.join(out, 'shot_output.png'), fullPage: false });

  check(netAttempts.length === 0, 'no network requests (' + netAttempts.join(', ') + ')');
  check(errors.length === 0, 'no page errors ' + errors.join(' | '));
  await browser.close();
  console.log(failures ? failures + ' FAILURE(S)' : 'ALL BROWSER CHECKS PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
