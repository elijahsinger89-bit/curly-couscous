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

const fixtures = fs.readdirSync(path.join(here, 'fixtures')).filter(f => /^f\d.*\.json$/.test(f)).sort();
const expectBlank = { f4_32nests: [17] };
const gens = [];
for (const f of fixtures) {
  const id = f.replace(/\.json$/, '');
  const job = S.normalizeJob(JSON.parse(fs.readFileSync(path.join(here, 'fixtures', f), 'utf8')));
  const v = S.validate(job);
  if (v.errors.length) { fail(id + ' validation: ' + JSON.stringify(v.errors)); continue; }
  const eb = JSON.stringify(expectBlank[id] || []);
  if (JSON.stringify(v.blankNests) !== eb) fail(id + ' blank nests ' + JSON.stringify(v.blankNests) + ' expected ' + eb);
  const g = S.generate(job, { date: '2026-11-12' });
  gens.push({ id, units: job.config.units, files: g.files });
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

/* ---- framework revision (comment only) ---- */
const crypto = require('crypto');
const isFixed = p => /^CUS\/L_|^WKS\/C_P1_(HOME|LOAD_WO)\.SPF$|^DEF\/UGUD\.DEF$/.test(p);
const isJob = p => /^WKS\//.test(p) && !isFixed(p) && p !== 'WKS/B_TEMPLATE.SPF';
const ref = {};          /* units -> {path: text} from the first fixture of those units */
let fixedOk = true, jobOk = true, sameOk = true;
for (const g of gens) {
  const fixed = g.files.filter(f => isFixed(f.path));
  if (fixed.length !== 13) { fail(g.id + ': expected 13 fixed files, got ' + fixed.length); }
  for (const f of fixed) {
    if (!f.text.includes('; FRAMEWORK    : SINUMERIK ONE NEST FRAMEWORK REV ' + S.FW_REV + '\n')) { fixedOk = false; fail(g.id + ' ' + f.path + ' lacks REV ' + S.FW_REV); }
    if (/^PROC /.test(f.text) === false && /^L_(RUN_NESTS|TOOL|SKIP|PAL|STEP_LOG|DATA)/.test(f.path.slice(4))) { fixedOk = false; fail(g.id + ' ' + f.path + ' PROC is not line 1'); }
    if (/GENERATED|2026-11-12  ES|SINUMERIK_GENERATOR/.test(f.text)) { fixedOk = false; fail(g.id + ' ' + f.path + ' carries a generation stamp'); }
    ref[g.units] = ref[g.units] || {};
    if (!(f.path in ref[g.units])) ref[g.units][f.path] = f.text;
    else if (ref[g.units][f.path] !== f.text) { sameOk = false; fail(g.id + ' ' + f.path + ' differs from another ' + g.units + ' job'); }
  }
  for (const f of g.files.filter(x => isJob(x.path))) {
    if (!f.text.includes('; FRAMEWORK    : NEEDS NEST FRAMEWORK REV ' + S.FW_REV + '\n')) { jobOk = false; fail(g.id + ' ' + f.path + ' lacks NEEDS REV'); }
  }
}
if (fixedOk) console.log('ok   every fixed file carries REV ' + S.FW_REV + ' and no generation stamp');
if (jobOk) console.log('ok   every job file says NEEDS NEST FRAMEWORK REV ' + S.FW_REV);
if (sameOk) console.log('ok   fixed files byte-identical across jobs (' + Object.keys(ref).join(', ') + ')');
/* hash guard: fixed-file content may only change together with FW_REV */
const hashFile = path.join(here, 'framework_rev' + S.FW_REV + '.sha256');
const hashLines = [];
for (const u of Object.keys(ref).sort()) for (const p of Object.keys(ref[u]).sort())
  hashLines.push(crypto.createHash('sha256').update(ref[u][p]).digest('hex') + '  ' + u + '/' + p);
if (process.argv.includes('--write-hashes')) {
  fs.writeFileSync(hashFile, hashLines.join('\n') + '\n');
  console.log('wrote ' + hashFile);
} else if (!fs.existsSync(hashFile)) {
  fail('no ' + path.basename(hashFile) + ': new framework revision? run with --write-hashes once');
} else {
  const want = fs.readFileSync(hashFile, 'utf8').trim().split('\n');
  const diff = hashLines.filter(l => !want.includes(l)).map(l => l.split('  ')[1]);
  if (diff.length || want.length !== hashLines.length)
    fail('framework changed without a revision bump (' + diff.join(', ') + '): bump FW_REV, add an FW_HISTORY row, run --write-hashes');
  else console.log('ok   fixed files match ' + path.basename(hashFile) + ' (' + hashLines.length + ' hashes)');
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

/* ---- step builder (first / last / increment) ---- */
function bjob(over, hdr) {
  const j = S.defaultJob();
  j.header.part = '00223344'; j.header.machine = 'HF5';
  Object.assign(j.header, hdr || {});
  Object.assign(j.builder, over || {});
  return j;
}
function eq(got, want, label) {
  const g = JSON.stringify(got), w = JSON.stringify(want);
  if (g !== w) fail(label + ': got ' + g + ' want ' + w); else console.log('ok   ' + label);
}
let r = S.buildSteps(bjob({ first: '10', last: '60', inc: '10' }), 'overwrite');
eq(r.error, '', 'builder 10-60/10: no error');
eq(r.steps.map(s => s.step), ['10', '20', '30', '40', '50', '60'], 'builder 10-60/10: six rows');
eq(r.steps.map(s => s.program), ['B_00223344_010_HF5', 'B_00223344_020_HF5', 'B_00223344_030_HF5',
  'B_00223344_040_HF5', 'B_00223344_050_HF5', 'B_00223344_060_HF5'], 'builder names B_PART_STEP_MACHINE');
eq(r.probeProgram, 'B_00223344_001_HF5', 'builder names the probe program');
eq([r.steps[0].meas, r.steps[0].measAlways, r.steps[0].brk, r.steps[0].maxBrk, r.steps[0].life, r.steps[0].setpiece],
  [true, false, true, '2', '1', true], 'builder rows get the default flags');
{
  const j = bjob({ first: '10', last: '40', inc: '10' });
  const keep30 = Object.assign(S.blankStep(30), { tool: 'EM_12', program: 'MY_CAM_PROG', brkTol: '0.2', life: '5', debug: true });
  const keep35 = Object.assign(S.blankStep(35), { tool: 'DR_6' });
  j.steps = [keep35, keep30];
  j.probeStep.program = 'B_CUSTOM_PROBE';
  const k = S.buildSteps(j, 'keep');
  eq(k.steps.map(s => s.step), ['10', '20', '30', '35', '40'], 'keep: missing steps added, rows sorted, 35 kept');
  eq(k.steps[2], keep30, 'keep: existing row 30 untouched');
  eq(k.steps[3], keep35, 'keep: row 35 outside the range untouched (blank name stays blank)');
  eq(k.probeProgram, 'B_CUSTOM_PROBE', 'keep: existing probe name kept');
  eq(k.added, 3, 'keep: three rows added');
  eq(j.steps.length, 2, 'keep: the job itself is not mutated');
  const o = S.buildSteps(j, 'overwrite');
  eq(o.steps.map(s => [s.step, s.tool, s.program]), [['10', '', 'B_00223344_010_HF5'], ['20', '', 'B_00223344_020_HF5'],
    ['30', '', 'B_00223344_030_HF5'], ['40', '', 'B_00223344_040_HF5']], 'overwrite: every row fresh');
  eq(o.probeProgram, 'B_00223344_001_HF5', 'overwrite: probe name regenerated');
  eq(S.hasStepData(j), true, 'hasStepData true with a tool');
  eq(S.hasStepData(S.defaultJob()), false, 'hasStepData false on the starter row');
}
const bad = [
  ['last below first', { first: '50', last: '10', inc: '10' }, null, 'must not be below'],
  ['increment 0', { first: '10', last: '50', inc: '0' }, null, 'Increment'],
  ['not whole', { first: '10', last: '5x', inc: '10' }, null, 'whole numbers'],
  ['first <= probe step', { first: '1', last: '50', inc: '10' }, null, 'after the probe step'],
  ['more than 100 rows', { first: '10', last: '2000', inc: '10' }, null, 'max 100'],
  ['machine with a space', { first: '10', last: '50', inc: '10' }, { machine: 'HF 5' }, 'Machine'],
  ['no part number', { first: '10', last: '50', inc: '10' }, { part: '' }, 'part number'],
];
for (const [label, b, h, want] of bad) {
  const e = S.buildSteps(bjob(b, h), 'overwrite').error;
  if (!e.includes(want)) fail('builder should reject ' + label + ' (got "' + e + '")'); else console.log('ok   builder rejects ' + label);
}
r = S.buildSteps(bjob({ first: '990', last: '1010', inc: '10' }), 'overwrite');
eq(r.steps.map(s => s.program), ['B_00223344_0990_HF5', 'B_00223344_1000_HF5', 'B_00223344_1010_HF5'], 'step >= 1000 pads to 4 digits');
eq(r.probeProgram, 'B_00223344_0001_HF5', 'probe name uses the same width');
r = S.buildSteps(bjob({ first: '10', last: '30', inc: '10' }, { part: '02215800_001', machine: 'HAAS_EC500' }), 'overwrite');
eq(r.unnamed, [1, 10, 20, 30], 'names over 24 chars are left blank and listed');
eq(r.steps.map(s => s.program), ['', '', ''], 'no over-long name is written');
eq(r.maxMachine, 5, 'max machine length reported (24 - B_02215800_001_010_)');
r = S.buildSteps(bjob({ first: '10', last: '20', inc: '10' }, { machine: '' }), 'overwrite');
eq(r.steps.map(s => s.program), ['B_00223344_010', 'B_00223344_020'], 'blank machine gives B_PART_STEP');
{
  const j = bjob();
  j.steps = [Object.assign(S.blankStep(10), { program: 'KEEP_ME' }), S.blankStep(20)];
  j.probeStep.program = '';
  const f = S.fillNames(j);
  eq([f.probeProgram, f.steps[0].program, f.steps[1].program, f.filled], ['B_00223344_001_HF5', 'KEEP_ME', 'B_00223344_020_HF5', 2],
    'fill names touches only blank names');
}
{
  let threw = false;
  try { S.generate(S.defaultJob()); } catch (e) { threw = /not valid/.test(e.message); }
  eq(threw, true, 'generate() refuses an invalid job (no WKS/.SPF)');
}
{
  const old = JSON.parse(fs.readFileSync(path.join(here, 'fixtures', 'f1_old_package.json'), 'utf8'));
  delete old.builder;
  eq(S.normalizeJob(old).builder, { first: '10', last: '', inc: '10' }, 'v1.0 job without builder loads with defaults');
}

/* ---- B program list import (sample written by hypermill-scripts/tests/test_b_program_export.py) ---- */
{
  const sample = JSON.parse(fs.readFileSync(path.join(here, 'fixtures', 'b_list_sample.json'), 'utf8'));
  const rd = S.readBList(sample);
  eq(rd.error, '', 'B list sample reads');
  eq(rd.list.steps.map(s => [s.step, s.program, s.tool, s.brkTol]), [['10', 'B_00948602_025_010_HF5', '905083900', '0.0040'],
    ['20', 'B_00948602_025_020_HF5', '475080900', '0.0020'], ['30', 'B_00948602_025_030_HF5', '416580900', ''],
    ['40', 'B_00948602_025_040_HF5', '350080900', '']], 'B list rows: step, program, tool, preset tolerance');
  eq([rd.list.part, rd.list.machine, rd.list.units, rd.list.refused.length], ['00948602_025', 'HF5', 'INCH', 2], 'B list header and refused');
  eq(rd.list.steps.every(s => s.brk && s.meas && !s.measAlways && s.maxBrk === '2' && s.life === '1' && s.setpiece), true,
    'B list presets map onto the row fields');
  for (const [label, mut, want] of [
    ['no format tag', d => { delete d.format; }, 'format tag'],
    ['version 2', d => { d.version = 2; }, 'version 2'],
    ['bad units', d => { d.units = 'MM'; }, 'INCH or METRIC'],
    ['no steps', d => { d.steps = []; }, 'no steps'],
    ['step not whole', d => { d.steps[1].step = '20a'; }, 'entry 2'],
  ]) {
    const d = JSON.parse(JSON.stringify(sample)); mut(d);
    const e = S.readBList(d).error;
    if (!e.includes(want)) fail('B list should reject ' + label + ': got "' + e + '"'); else console.log('ok   B list rejects ' + label);
  }
  const j = S.normalizeJob(JSON.parse(fs.readFileSync(path.join(here, 'fixtures', 'f2_horizontal_inch.json'), 'utf8')));
  const ov = S.applyBList(j, rd.list, 'overwrite');
  eq(ov.steps.map(s => s.step), ['10', '20', '30', '40'], 'overwrite: the list replaces the table');
  const kp = S.applyBList(j, rd.list, 'keep');
  eq([kp.steps.map(s => s.step), kp.added, kp.steps[0].tool], [['10', '20', '30', '40'], 1, 'FM_3IN'], 'keep: existing 10-30 untouched, 40 added');
  j.steps = ov.steps; j.header.part = rd.list.part; j.header.machine = rd.list.machine; j.config.units = rd.list.units;
  j.probeStep.program = 'B_00948602_025_001_HF5';
  const v1 = S.validate(j);
  eq(v1.errors.map(e => e.path).filter(p => /brkTol/.test(p)), ['steps.2.brkTol', 'steps.3.brkTol'], 'only the blank imported tolerances fail validation');
  j.steps[2].brkTol = '0.0005'; j.steps[3].brkTol = '0.0005';
  const v2 = S.validate(j);
  eq(v2.errors, [], 'tolerances filled: imported job validates');
  const g = S.generate(j, { date: '2026-11-13' });
  const dir = path.join(out, 'b_list_import');
  for (const file of g.files) { const p = path.join(dir, file.path); fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, file.text); }
  const a = g.files.find(f => f.path === 'WKS/A_P1.MPF').text;
  eq(a.includes('L_RUN_NESTS("905083900",0.0040,4,"B_00948602_025_010_HF5",1,0,1,2,0,1,1)'), true, 'A_P1 calls L_RUN_NESTS with the imported tool and program');
}

/* ---- JSON round trip ---- */
const j1 = base();
const j2 = S.normalizeJob(JSON.parse(JSON.stringify(j1)));
if (JSON.stringify(j1) !== JSON.stringify(j2)) fail('normalizeJob round trip changed the job');
else console.log('ok   job JSON round trip');

console.log(failures ? failures + ' FAILURE(S)' : 'ALL HARNESS CHECKS PASSED');
process.exit(failures ? 1 : 0);
