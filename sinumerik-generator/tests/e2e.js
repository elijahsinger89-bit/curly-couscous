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
  check(await page.$eval('[data-path="config.trunnion"]', e => e.value) === 'A', 'loaded trunnion A into the form');
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
