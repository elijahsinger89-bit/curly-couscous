#!/usr/bin/env node
/* Runs the generator engine (extracted from the HTML) headless on every
   fixture, writes the NC files and the zip, and checks the validator on
   broken jobs. Usage: node run_fixtures.js <outDir> */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const here = __dirname;
const html = fs.readFileSync(path.join(here, '..', 'SINUMERIK_GENERATOR.html'), 'utf8');
const m = html.match(/<script id="engine">([\s\S]*?)<\/script>/);
if (!m) throw new Error('engine script not found');
const ctx = {};
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const S = ctx.SNG;

const out = process.argv[2] || path.join(require('os').tmpdir(), 'sng_out');
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });

let failures = 0;
function fail(msg) { failures++; console.log('FAIL ' + msg); }

const fixtures = fs.readdirSync(path.join(here, 'fixtures')).filter(f => f.endsWith('.json')).sort();
const expectBlank = { f4_32nests: [17] };
for (const f of fixtures) {
  const id = f.replace(/\.json$/, '');
  const job = S.normalizeJob(JSON.parse(fs.readFileSync(path.join(here, 'fixtures', f), 'utf8')));
  const v = S.validate(job);
  if (v.errors.length) { fail(id + ' validation: ' + JSON.stringify(v.errors)); continue; }
  const eb = JSON.stringify(expectBlank[id] || []);
  if (JSON.stringify(v.blankNests) !== eb) fail(id + ' blank nests ' + JSON.stringify(v.blankNests) + ' expected ' + eb);
  const g = S.generate(job, { date: '2026-11-12' });
  const dir = path.join(out, id);
  for (const file of g.files) {
    const p = path.join(dir, file.path);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, file.text);
  }
  fs.writeFileSync(path.join(out, id + '.zip'), Buffer.from(S.makeZip(g.files, new Date(2026, 10, 12, 9, 30, 0))));
  fs.writeFileSync(path.join(out, id + '.manifest.json'), JSON.stringify(g.files.map(x => x.path)));
  console.log('ok   ' + id + ': ' + g.files.length + ' files');
}

/* ---- validator must reject broken jobs ---- */
const base = () => S.normalizeJob(JSON.parse(fs.readFileSync(path.join(here, 'fixtures', 'f1_old_package.json'), 'utf8')));
const negatives = [
  ['tombstone without rotary', j => { j.config.rotary = 'NONE'; }, 'config.rotary'],
  ['trunnion equals rotary', j => { j.config.trunnion = 'B'; }, 'config.trunnion'],
  ['total above faces x nests', j => { j.config.totalNests = '9'; }, 'config.totalNests'],
  ['total above 32', j => { j.config.faces = '8'; j.config.nestsPerFace = '5'; j.config.totalNests = '40'; }, 'config.totalNests'],
  ['duplicate step', j => { j.steps[1].step = '10'; }, 'steps.1.step'],
  ['step before probe', j => { j.probeStep.step = '20'; }, 'steps.0.step'],
  ['program name starts with digit', j => { j.steps[0].program = '1ABC'; }, 'steps.0.program'],
  ['program name 25 chars', j => { j.steps[0].program = 'B_ABCDEFGHIJKLMNOPQRSTUVW'; }, 'steps.0.program'],
  ['tool with quote', j => { j.steps[0].tool = 'FACE"MILL'; }, 'steps.0.tool'],
  ['tool 26 chars', j => { j.steps[0].tool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; }, 'steps.0.tool'],
  ['brk on without tolerance', j => { j.steps[0].brkTol = ''; }, 'steps.0.brkTol'],
  ['max breaks 0', j => { j.steps[0].maxBrk = '0'; }, 'steps.0.maxBrk'],
  ['life 0 with setpiece', j => { j.steps[0].life = '0'; }, 'steps.0.life'],
  ['wcs comma decimal', j => { j.wcs[2].x = '12,5'; }, 'wcs.2.x'],
  ['rotary angle text', j => { j.wcs[2].rotary = 'abc'; }, 'wcs.2.rotary'],
  ['bore at XY point without alt Z', j => { j.probing.xyMethod = 'BORE'; }, 'probing.zAlt'],
  ['xy tol >= search', j => { j.probing.xyTol = '5'; }, 'probing.xyTol'],
  ['z tol >= search', j => { j.probing.zTol = '6'; }, 'probing.zTol'],
  ['travel too short', j => { j.probing.maxTravel = '5'; }, 'probing.maxTravel'],
  ['probe depth above start', j => { j.probing.probeZ = '30'; }, 'probing.probeZ'],
  ['nothing to probe', j => { j.probing.partCheck = false; j.probing.skipZ = true; j.probing.xyMethod = 'NONE'; }, 'probing.xyMethod'],
  ['health target above start', j => { j.probing.health = true; j.probing.hX = '0'; j.probing.hY = '0'; j.probing.hStartZ = '1'; j.probing.hTargetZ = '2'; }, 'probing.hTargetZ'],
  ['probe-on M code junk', j => { j.probing.probeOnM = 'PROBE ON'; }, 'probing.probeOnM'],
  ['approach clr <= search (Z default)', j => { j.probing.approachClr = '4'; }, 'probing.approachClr'],
  ['alt Z too low', j => { j.probing.zAlt = true; j.probing.zX = '0'; j.probing.zY = '0'; j.probing.zZ = '3'; }, 'probing.zZ'],
  ['rib width missing', j => { j.probing.widthY = ''; }, 'probing.widthY'],
  ['faces not integer', j => { j.config.faces = '4.5'; }, 'config.faces'],
  ['cutting program equals probe program', j => { j.steps[0].program = 'B_XXXX_001'; }, 'steps.0.program'],
];
for (const [label, mut, wantPath] of negatives) {
  const j = base();
  mut(j);
  const v = S.validate(j);
  if (!v.errors.some(e => e.path === wantPath)) fail('validator missed "' + label + '" (want ' + wantPath + ', got ' + JSON.stringify(v.errors) + ')');
  else console.log('ok   rejects: ' + label);
}

/* ---- number formatting ---- */
const fmt = [[S.fix(-0.0001, 3), '0.000'], [S.fix(1.0005, 3), '1.001'], [S.fix(-2.5, 3), '-2.500'], [S.fix(12.34565, 4), '12.3457'],
  [S.compact(0.04, 4), '0.04'], [S.compact(1, 4), '1'], [S.fix(-1e-17, 3), '0.000']];
for (const [got, want] of fmt) if (got !== want) fail('format ' + got + ' != ' + want); else console.log('ok   format ' + want);

/* ---- JSON round trip ---- */
const j1 = base();
const j2 = S.normalizeJob(JSON.parse(JSON.stringify(j1)));
if (JSON.stringify(j1) !== JSON.stringify(j2)) fail('normalizeJob round trip changed the job');
else console.log('ok   job JSON round trip');

console.log(failures ? failures + ' FAILURE(S)' : 'ALL HARNESS CHECKS PASSED');
process.exit(failures ? 1 : 0);
