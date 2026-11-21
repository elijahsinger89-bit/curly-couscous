const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, LevelFormat, Footer, PageNumber, BorderStyle, PageBreak
} = require('docx');

const FONT = 'Arial', MONO = 'Courier New';
const W = 10080;                       /* text width, US Letter with 1.1" margins */
const LINE = { style: BorderStyle.SINGLE, size: 4, color: '9AA4AE' };
const BORDERS = { top: LINE, bottom: LINE, left: LINE, right: LINE };

function runs(text, o) {
  /* **bold** inside a string */
  return String(text).split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(s =>
    s.startsWith('**') ? new TextRun({ text: s.slice(2, -2), bold: true, font: FONT, size: 20, ...(o || {}) })
                       : new TextRun({ text: s, font: FONT, size: 20, ...(o || {}) }));
}
const p = (t, o) => new Paragraph({ children: runs(t), spacing: { after: 80 }, ...(o || {}) });
const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t })] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t })] });
let listNo = 0;
const steps = (items, keep) => { const ref = keep || ('num' + (listNo++)); if (!keep) NUMS.push(ref); steps.last = ref;
  return items.map(t => new Paragraph({ numbering: { reference: ref, level: 0 }, children: runs(t), spacing: { after: 60 } })); };
const bullets = items => items.map(t => new Paragraph({ numbering: { reference: 'bullet', level: 0 }, children: runs(t), spacing: { after: 60 } }));
const code = lines => lines.map((l, i) => new Paragraph({
  children: [new TextRun({ text: l, font: MONO, size: 19 })],
  shading: { type: ShadingType.CLEAR, fill: 'EEF1F4', color: 'auto' },
  spacing: { after: 0, before: i === 0 ? 60 : 0 }, indent: { left: 360 }
})).concat([new Paragraph({ spacing: { after: 80 }, children: [] })]);
const note = t => new Paragraph({ children: runs(t), spacing: { after: 100 },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: 'C0392B', space: 8 } }, indent: { left: 120 } });

function table(widths, head, rows) {
  const cell = (t, i, hd) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA }, borders: BORDERS,
    shading: hd ? { type: ShadingType.CLEAR, fill: '1F3A4D', color: 'auto' } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: String(t).split('\n').map(line => new Paragraph({ spacing: { after: 0 },
      children: hd ? [new TextRun({ text: line, bold: true, color: 'FFFFFF', font: FONT, size: 19 })]
                   : runs(line, { size: 19 }) }))
  });
  return [new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: head.map((t, i) => cell(t, i, true)) })]
      .concat(rows.map(r => new TableRow({ cantSplit: true, children: r.map((t, i) => cell(t, i, false)) })))
  }), new Paragraph({ spacing: { after: 120 }, children: [] })];
}

const NUMS = [];
const body = [];
const add = (...xs) => xs.forEach(x => Array.isArray(x) ? body.push(...x) : body.push(x));

/* ---------------- title ---------------- */
add(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun('Nest Framework Operator Instructions')] }),
  p('SINUMERIK ONE. Jobs made with SINUMERIK_GENERATOR, framework REV 02. Keep this at the machine.'),
  p('Inch jobs shown. Step and nest numbers in the examples are examples: use your job’s.'));

/* ---------------- 1 how it runs ---------------- */
add(h1('1. How the job runs'),
  bullets([
    '**A_P1** is the main program. Always start the job with A_P1.',
    'Step 1 is the **probe program**. It checks each part and sets its offset.',
    'Every cutting step: load the tool → laser measure (if set) → cut nest 1, 2, 3 … → laser break check after each nest (if set) → next step.',
    'Nest n uses work offset **G5(n+4)**: nest 1 = G505, nest 2 = G506, nest 8 = G512. Before each nest the program copies that offset into **G54**. The cutting programs run in G54.',
    'The machine remembers the step and nest it is on (GV_STEP, GV_NEST) through reset and power-off. A restart picks up where it stopped.',
    'A nest that goes bad (no part, out of tolerance, broken tool, CMC scrap) is switched off. The rest of the job skips it. The other nests keep running.'
  ]));

/* ---------------- 2 variables ---------------- */
add(h1('2. Variables'),
  p('Where: **Parameter → User variable → Global GUD** (name of the softkey can differ by machine). Type over the value. Or set it in **MDA**, for example GV_STEP=60, then cycle start.'),
  table([2300, 3500, 4280], ['Variable', 'What it is', 'Values'], [
    ['**GV_STEP**', 'Step the job is on', '0 = new pallet: starts from the top, rewrites offsets, all nests on.\nAny other number = step to resume at.'],
    ['**GV_NEST**', 'Nest the job is on', '1 to the number of nests. 0 = not started.'],
    ['**GV_NEST_STATUS[n]**', 'State of nest n', 'See the table below.'],
    ['GV_WO[n]', 'Work offset number of nest n', 'Set by the program. Do not change.'],
    ['GV_SKIP', '1 = every nest is off, step is skipped', 'Set by the program at every step. Do not change.'],
    ['GV_BRK_COUNT', 'Broken tools in this step', 'Set by the program.'],
    ['GV_NESTS_CUT', 'Nests cut in this step', 'Set by the program.'],
    ['GV_PROBE_CHK', '1 = probe health check done this job', 'Set by the program.']
  ]),
  h2('Nest status: GV_NEST_STATUS[n]'),
  table([1500, 3900, 4680], ['Value', 'Meaning', 'What the job does with the nest'], [
    ['**0**', 'Off (set by operator)', 'Skipped.'],
    ['**1**', 'Good / running', 'Cut.'],
    ['**2**', 'No part, or out of tolerance at probing', 'Skipped for the rest of the job.'],
    ['**3**', 'CMC scrap', 'Skipped for the rest of the job.'],
    ['**1xx**', 'Tool failed at step xx\n110 = step 10, 160 = step 60', 'Skipped from then on.']
  ]));

/* ---------------- 3 new pallet ---------------- */
add(h1('3. Start a new pallet'),
  steps([
    'Last job finished (CYCLE COMPLETE)? GV_STEP is already 0. Last job stopped part-way? Set **GV_STEP=0** in MDA.',
    'Load the parts. Empty nest: leave it empty. The probe finds no part and switches that nest off.',
    'Select **A_P1**. Cycle start.'
  ]),
  p('At a new pallet the program writes all work offsets and switches every nest on, then probes.'));

/* ---------------- 4 restart same pallet ---------------- */
add(h1('4. Restart after a reset, alarm or power-off (same pallet)'),
  steps([
    'Fix the problem.',
    'Select **A_P1**. Cycle start from the top.',
    'Screen shows **RESUMING AT STEP x NEST y** and stops. Check it is the step and nest that was cutting.',
    'Cycle start. It goes back into that step at that nest.'
  ]),
  bullets(['That nest is cut again from the start of its program (air cut where it was already cut).',
    'Nests that were switched off stay off.']),
  note('**Do not set GV_STEP=0 for the same pallet.** That starts the pallet over: re-probe, all nests back on, every step again.'));

/* ---------------- 5 restart at a step ---------------- */
add(h1('5. Restart at a chosen step'),
  p('Use this to redo a step and everything after it on some nests. Example: a tool broke at step 60, the job ran to the end, the bad nest shows 160.'),
  steps([
    'Replace the broken tool. It was locked by the break check: unlock it in the tool list. A new tool is laser-measured before it cuts (if Measure is set for the step).',
    'Inspect the nest(s) that failed. They were cut with the broken tool.',
    'In MDA, set the step, nest 1, and every nest: **1** = redo, **0** = leave alone:'
  ]),
  code(['GV_STEP=60', 'GV_NEST=1', 'GV_NEST_STATUS[1]=1    ;REDO', 'GV_NEST_STATUS[2]=0    ;LEAVE ALONE',
    '...one line for every nest in the job...', 'GV_NEST_STATUS[8]=0', 'M30']),
  steps(['Cycle start the MDA lines.', 'Select **A_P1**. Cycle start. Screen shows **RESUMING AT STEP 60 NEST 1**.', 'Cycle start.'], steps.last),
  bullets([
    'Nests set to 1 run step 60 and every step after it. Nests set to 0 are skipped.',
    'Offsets are kept. The probe step does not run.',
    'GV_STEP must be a step number in this job (else UNKNOWN GV_STEP VALUE).',
    'Leave GV_SKIP alone. The program sets it.',
    'At the end, nests set to 0 show **INACTIVE (OPERATOR)**. That is normal.'
  ]));

/* ---------------- 6 messages ---------------- */
add(h1('6. Messages and stops'),
  table([3300, 3100, 3680], ['Message', 'What happened', 'What to do'], [
    ['STEP x / y - tool', 'Step running.', 'Nothing.'],
    ['RESUMING AT STEP x NEST y - FOR A NEW PALLET SET GV_STEP=0 THEN RESTART', 'Restart of a job that was not finished. Stopped.',
      'Right step and nest: cycle start.\nNew pallet: reset, GV_STEP=0, start A_P1.'],
    ['NEST n - NO PART', 'Probe found no part. Nest off (2). No stop.', 'Nothing. To cut it: load the part, start the pallet over (GV_STEP=0) before any cutting step ran.'],
    ['NEST n SURFACE Z OUT OF TOL: v\n(also BORE / BOSS / RIB X or Y)', 'Part is further off than the tolerance. Nest off (2). Stopped.',
      'Check: part seated, chips, right part, right fixture.\nCycle start = go on without this nest.\nTo cut it: fix it, reset, GV_STEP=0, start over (before any cutting step).'],
    ['PROBE HEALTH CHECK FAILED - PROBE DID NOT TRIGGER', 'Probe did not signal. Holds.', 'Check probe is on, battery, stylus, receiver. Reset. Restart.'],
    ['BROKEN: tool NEST n STEP s', 'Break check: tool broken or short. Nest off (100+s). Tool locked. No stop.',
      'Job goes on: next nest gets a sister tool. After the job: replace the tool, inspect nest n.'],
    ['MAX BREAKAGE: x AT STEP s - CHECK SETUP', 'Too many breaks in one step. Machine parks and holds.',
      'Check setup, tools, material. Replace tools. Reset. Restart (section 4). Failed nests stay off; set them to 1 only if they can be cut again.'],
    ['Control alarm at tool change (no tool / tool disabled)', 'Every sister of that tool is used up or locked.', 'Load a new tool or sister. Reset. Restart (section 4).'],
    ['UNKNOWN GV_STEP VALUE: x', 'GV_STEP holds a step that is not in this job. Holds.', 'Reset. Set GV_STEP=0 (new pallet) or a step in this job.'],
    ['UNKNOWN GV_NEST VALUE: x', 'GV_NEST is out of range. Holds.', 'Reset. Set GV_NEST=1. Restart.'],
    ['NEST n = INACTIVE (OPERATOR)\nNEST n = NO PART OR OUT OF TOLERANCE (PROBE)\nNEST n = CMC SCRAP (SEE CMC_LOG)\nNEST n = TOOL FAILURE AT STEP s',
      'End-of-job report. One stop for each nest that is not good.', 'Write it down for QC. Cycle start through each.'],
    ['CYCLE COMPLETE - g OF n GOOD - t SEC', 'Done. GV_STEP set to 0.', 'Unload. Next pallet: section 3.'],
    ['LOG WRITE ERROR / CMC LOG WRITE ERROR', 'Log file not written. Job goes on.', 'Tell the programmer.'],
    ['Heller 700749: measurement result invalid because override unequal to 100%', 'Probe or tool measure ran below 100% feed override.', 'Run probing and measuring at **100% feed override**. Single block is fine.']
  ]));

/* ---------------- 7 CMC ---------------- */
add(h1('7. CMC holds (cut / measure / cut)'),
  p('Only in jobs with CMC steps. The step cuts the feature with stock left, probes it, corrects the cutter wear, then makes the final cut. Info messages: **CMC STEP s NEST n: FIRST CUT** and **FINAL CUT, CMC WEAR w**.'),
  p('At a hold the message names an R parameter. Set it on **Parameter → User variable → R variables** (no reset), then cycle start.'),
  table([3700, 2500, 3880], ['Message (end)', 'Cause', 'Set the R to'], [
    ['MEASURED m EXPECTED e - SET Rxxx 0=MEASURE AGAIN 1=SCRAP 2=CUT', 'Measured too far from expected, or the correction is too big.',
      '**0** measure again (clean probe and feature first)\n**1** scrap: nest off (3)\n**2** cut with the correction shown'],
    ['PROBE TOUCHED WHILE LOWERING - FIRST CUT MISSING? - SET Rxxx 0=MEASURE AGAIN 1=SCRAP 2=CUT AGAIN', 'Probe hit something on the way in: chip, first cut missing, wrong position.',
      'Look first.\n**0** measure again\n**1** scrap\n**2** cut again'],
    ['MEASURED m NOMINAL x - SET Rxxx 0=MEASURE AGAIN 1=SCRAP 2=ACCEPT', 'Final size out of tolerance, or max re-cuts reached.',
      '**0** measure again\n**1** scrap\n**2** accept as is (logged OUT)'],
    ['CLEAN THE PROBE AND THE FEATURE, THEN CYCLE START', 'Cleaning stop before measuring.', 'Clean. Cycle start.']
  ]),
  bullets([
    '**Do not change the cutter wear during a CMC hold.** The program handles it.',
    'A restart goes back into the nest where it stopped. The correction is never added twice.',
    'Job abandoned in the middle of a CMC step: run **C_P1_CMC_CLEAR** before another job uses that cutter. (A new pallet runs it by itself.)',
    'Every measurement is written to **CMC_LOG.SPF**.'
  ]));

/* ---------------- 8 tools ---------------- */
add(h1('8. Tools'),
  bullets([
    'Tool name on the control = tool ID from CAM. Sisters have the same name: sister 1, 2, …',
    '**Tool load program** <DOCUMENT>_TOOL_LOAD.MPF: open in MDA, cycle start. It creates the tools and sisters that are missing. Tools already on the control are left as they are. Safe to run twice.',
    '**Tool life** is counted in pieces. When a tool runs out, the next nest loads a sister.',
    '**Laser measure** before cutting: every nest, or only a tool not measured yet (set per step in the job).',
    '**Break check** on the laser after each nest. A broken tool is locked; its nest goes to 1xx; the next nest gets a sister.',
    '**Turning tools:** lengths come from the presetter (Zoller), entered in the tool list.'
  ]));

/* ---------------- 9 options ---------------- */
add(h1('9. Optional stop and single nest'),
  bullets([
    '**Optional stop (M1):** steps marked Debug in the job stop after every nest when Optional stop is on. Turn Optional stop off for production.',
    'Cutting programs have no M1 of their own.',
    'To run one nest only: switch the others off (status 0) and restart at the step (section 5).'
  ]));

/* ---------------- 10 files ---------------- */
add(h1('10. Files on the control'),
  table([3300, 6780], ['File', 'What it is'], [
    ['**A_P1.MPF**', 'Main program. Start here.'],
    ['C_P1_WO, C_P1_NESTS, C_P1_PROBE, C_P1_HOME, C_P1_LOAD_WO', 'Job setup: offsets, nest list, probe call, home position, offset copy. Do not edit.'],
    ['B_part_001_machine', 'Probe program (step 1).'],
    ['B_part_step_machine', 'Cutting program of each step (from CAM). One nest per call.'],
    ['C_P1_CMC…', 'CMC programs (only in CMC jobs).'],
    ['L_… (user cycles)', 'Framework cycles. Same on every job. Do not edit.'],
    ['UGUD.DEF', 'The GV_ variables. Do not edit.'],
    ['CYCLE_LOG.SPF', 'One line per step: date, time, tool, nests cut, breaks.'],
    ['CMC_LOG.SPF', 'One line per CMC measurement.']
  ]));

/* ---------------- 11 first run ---------------- */
add(h1('11. First run of a new job'),
  steps([
    'Framework on the control matches the job: A_P1 says NEEDS NEST FRAMEWORK REV 02; the L_ files say REV 02.',
    'Tools loaded (tool load program) and measured.',
    'Single block, low rapid override. Probing and tool measuring at 100% feed override.',
    'Watch the first probe on nest 1, the first cut of each step, the first laser measure and break check.',
    'Reset in the middle of a step once and restart: RESUMING AT STEP / NEST must show the nest that was cutting.'
  ]));

/* ---------------- build ---------------- */
const numbering = { config: [{ reference: 'bullet', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] }]
  .concat(NUMS.map(ref => ({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 300 } } } }] }))) };

const doc = new Document({
  creator: 'Nest framework', title: 'Nest Framework Operator Instructions',
  styles: {
    default: { document: { run: { font: FONT, size: 20 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 36, bold: true, color: '1F3A4D' },
        paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 26, bold: true, color: '1F3A4D' },
        paragraph: { spacing: { before: 280, after: 100 }, keepNext: true, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '1F3A4D', space: 2 } } } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 22, bold: true, color: '1F3A4D' },
        paragraph: { spacing: { before: 160, after: 80 }, keepNext: true, outlineLevel: 1 } }
    ]
  },
  numbering,
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: 'Nest Framework Operator Instructions - REV 02 - page ', font: FONT, size: 16, color: '666666' }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '666666' })] })] }) },
    children: body
  }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[2], b); console.log('wrote', process.argv[2]); });
