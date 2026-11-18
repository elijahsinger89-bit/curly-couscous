SINUMERIK ONE PROGRAM GENERATOR
===============================

USE
  Double-click SINUMERIK_GENERATOR.html. It runs offline in Chrome, Edge or
  Firefox: no server, no internet, no install.
  Fill the tabs, press Generate ZIP. The zip holds every NC file.
  Tab 5 (CMC) appears only while a step row has CMC ticked.
  Tab 4 previews every file before saving; "Download this file" saves one.
  Save job writes the whole form to a .json file; Load job reopens it.
  The .json file is the input store (it replaces the Excel sheets).
  Blank work offset X/Y/Z: you are asked Yes/No before anything is written.

STEP BUILDER (tab 1)
  First step, Last step, Increment, then Build steps: one row per step.
  Program names are B_[part]_[step]_[machine] from Header > Part number and
  Machine (letters, digits, _ only). The step is padded to 3 digits, 4 when
  a step is 1000 or more. Names over 24 characters (NC limit) are left
  blank and listed, with the longest machine name that would fit.
  If the table already has data you choose:
    Overwrite all    every row replaced, all names regenerated
    Keep existing    every current row untouched, missing steps added,
                     rows sorted by step number
    Cancel           nothing changes
  "Fill blank program names" uses the same pattern on blank names only.

STEP TABLE CHECKBOXES (tab 1)
  The box under Measure, Always, Brk check, Debug M1, SETPIECE and CMC turns
  that column on or off for every row. Ticked = all on, empty = all off,
  dash = mixed (a click turns all on). The per-row boxes work as before.
  Always acts only on rows with Measure on.

IMPORT B LIST (from hyperMILL)
  Import B list..., pick <document>_B_PROGRAMS.json written by the hyperMILL
  b_program_export or go_to_machine script (after posting). Format:
  B_PROGRAM_LIST_FORMAT.txt.
  It fills the step table (step, tool ID, B program name, break check,
  breakage tolerance, measure, max breaks, life, SETPIECE), and part and
  machine in the Header when they are blank. The probe program name is
  generated from the Header (B_[part]_001_[machine]): overwrite regenerates
  it, keep existing fills it only when blank. Probe step off: untouched.
  Asks first when: the list's units differ from the page (switch or
  cancel), part or machine differ from the Header (list's / page's /
  cancel), the table already has data (overwrite all / keep existing and
  add missing / cancel).
  Steps with break check on and no tolerance show in red. Compound jobs
  hyperMILL left out (more than one tool, wrong name) are listed.
  From go_to_machine also, per B program: the number of toolpaths, G41/G42
  found in the posted NC file and the R parameters it uses. Keep existing
  refreshes these three on rows with the same program name.

CMC - CUT / MEASURE / CUT (tick CMC on a step row, fill its card on tab 5)
  The step runs C_P1_CMC<step> per nest in place of its B program:
    1. first cut with first-cut wear (leaves stock);
    2. measure with the probe (measure-only cycle, no correction);
    3. final cut with the corrected wear;
    4. optional verify: in tolerance = OK; out with material left = re-cut
       (max re-cuts) or accept and log; past size = scrap.
  Features: bore, boss, slot X/Y (inside two walls), web X/Y (outside two
  walls), rectangle pocket / spigot (X and Y, correction from their mean),
  bore / boss on a circle segment (3 or 4 points, CYCLE979), single wall
  X/Y (material side), floor / face Z.
  Protection zone (CYCLE977, MC PM 5.1.7): inside features = an island in
  the middle (the probe starts above it at the approach Z and lowers
  outside it), outside features = the wall around (a channel). Use it for
  an ID or OD inside a round channel.
  Probe swivel: paste the CYCLE800(...) line of the CAM program (a block
  number and comment are dropped). Blank = the nest face. With a swivel the
  card's X / Y / Z are in that plane.
  Tool type: rotating = $TC_DP15 wear radius (floor: $TC_DP12 length 1),
  +wear leaves material. Turning = $TC_DP12 length 1 (face: $TC_DP13), you
  set what +wear does (larger / smaller) and radius or diameter. The field
  and edge can be changed on the card.
  Wear: the wear found on the edge before the CMC + the CMC wear while
  cutting; the found wear is put back after every cut. Do not edit the
  cutter wear during a CMC hold.
  Math: first-cut wear w1 = stock on the material side; expected after it
  E = nominal + stock (x2 for a diameter with radius wear); next wear =
  wear used + (nominal - measured) / (+-1 or +-2). Your example: boss
  2.000, first-cut wear .002 -> E 2.004, measured 2.0052 -> wear -.0006.
  Holds (M0, message names the R to set: 0 measure again, 1 scrap, 2 as
  the message says): measured more than the check window from expected,
  correction above the limit, probe touched while lowering (G1 MEAS=1:
  first cut missing, chip, wrong position), max re-cuts reached.
  R parameters: 50 per CMC step from the first R (default R700), kept
  through power-off: pass, nest, cutter T, sister, wear, measurement,
  result per nest. A restart resumes inside the nest; wear is always
  written as an absolute value, so a correction is never added twice.
  The generator refuses a block that covers R999 (tool_load_mda), an R the
  posted B programs use, or the last R on the control (MD28050). Check on
  the machine that nothing else (tool change, Blum, OEM cycles, FIFO from
  $MC_MM_START_FIFO) uses the range.
  Back to the cutter: TCA loads the recorded sister (to confirm on the
  machine); if it is gone or disabled, T M6 by name and that nest starts
  again from the first cut (first-cut wear leaves stock). Or T M6 always.
  Counting: L_RUN_NESTS still loads, laser-measures, break-checks and
  counts. SETPIECE(0) at the end of each CMC nest drops the probe and the
  extra cuts; the cutter is counted once. A scrap nest gets status 3 after
  the step (A_P1), so later steps skip it; nests cut counts it (it was
  machined). Log: CMC_LOG.SPF, one line per measurement and a step summary.
  C_P1_CMC_CLEAR puts back wear a stopped cut left and clears the R blocks:
  A_P1 runs it on a fresh start; run it by hand when a job is abandoned
  part-way through a CMC step, before another job uses that cutter.
  Warnings from the B list: more than one toolpath in the CMC B program
  (all are re-cut), no G41/G42 with radius wear (the wear does nothing).

WHERE THE FILES GO
  DEF/UGUD.DEF    definitions directory (_N_DEF_DIR, file _N_UGUD_DEF)
  CUS/L_*.SPF     user cycles directory (_N_CUS_DIR). Called by name.
                  Cycles need no EXTERN (NC PM 4.2.3.2). The CMC programs
                  call WKS sub-programs with parameters and declare them
                  with EXTERN, as NC PM 4.2.3.2 requires there.
  WKS/*           the job's workpiece directory, next to the CAM B_ programs.
                  A_P1.MPF is the main program.

GLOBAL VARIABLES (UGUD.DEF, all DEF NCK INT, kept through power-off)
  GV_STEP            current step (0 = fresh pallet)
  GV_NEST            current nest
  GV_NEST_STATUS[33] per nest: 0 off, 1 running, 2 no part / out of
                     tolerance, 3 CMC scrap, 100+step = tool failed at that
                     step
  GV_WO[33]          work offset frame per nest (nest n = G5(n+4))
  GV_SKIP            1 = every nest off, skip the step
  GV_BRK_COUNT       breaks this step
  GV_NESTS_CUT       nests cut this step
  GV_PROBE_CHK       1 = probe health check done this job

NCK RESET
  After any change to UGUD.DEF, activate the definitions and reset the NCK.
  Activating re-creates the variables, so their values start at 0.
  MD18120 $MN_MM_NUM_GUD_NAMES_NCK and MD18150 $MN_MM_GUD_VALUES_MEM need
  room for the 8 names.

MACHINE DATA
  MD18600 $MN_MM_FRAME_FINE_TRANS = 1
    Probing corrects the FINE part of the nest work offset (CYCLE977/978
    S_KNUM ten-thousands digit 0). Without MD18600 the cycles write the
    coarse part instead (MC PM 5.1.7 note 6), $P_UIFR[..,FI] stays 0 and
    the tolerance check never trips.
  MD28080 $MC_MM_NUM_USER_FRAMES >= nests + 5 (37 for 32 nests: G505-G536).
  MD10240 $MN_SCALING_SYSTEM_IS_METRIC must match the units chosen in the
    generator. G70/G71 convert only geometry; work offsets, feeds and the
    $MA_POS_LIMIT_PLUS retract are in the basic system (NC PM 3.8.4.5).

FRAMEWORK REVISION (comment only, nothing is checked on the control)
  The fixed files - the 10 L_ cycles, C_P1_HOME, C_P1_LOAD_WO, UGUD.DEF -
  are installed once per machine. Each carries "NEST FRAMEWORK REV 01" and
  a revision table near the top (REV 00 = the Excel/VBA package). Job
  files (A_P1, C_P1_WO, C_P1_NESTS, probe program) say "NEEDS NEST
  FRAMEWORK REV 01". If the machine shows a lower revision, install the
  fixed files from a new zip. The revision only goes up when an installed
  file changes; every job produces identical fixed files for the same
  units (metric and inch differ only in the retract clearance).

B_ PROGRAMS
  B_TEMPLATE.SPF is a CAM stub with no motion. The real cutting B_ programs
  come from CAM: one nest per call, run in G54, no T/M6, orient per face
  with CYCLE800(0,"H",...), end with the block in the template.
  The probe program is generated complete.

WHAT CHANGED FROM THE OLD PACKAGE (all from the SINUMERIK ONE manuals)
  - One-line IF is only defined for GOTOx (NC PM 4.1.5.2). IF ... SETPIECE,
    IF ... M1 and IF ... GV_NEST=1 are now IF/ENDIF blocks.
  - No jumps out of IF blocks (NC PM 4.1.7). The jump is a one-line
    conditional placed after ENDIF. Same behaviour.
  - GROUP_BEGIN is a cycle call (NC PM 4.27.1.55), so the DEFs now come
    first in A_P1.
  - STOPRE after CALL LD_PROG in L_RUN_NESTS: a reset mid-cut can no
    longer make a restart skip that nest.
  - C_P1_NESTS also sets GV_NEST=0 on a fresh start.
  - L_TOOL_LOAD ends with SETPIECE(0), so the previous step's tool is not
    counted again (SV: SETPIECE counts edges used since the last SETPIECE).
  - L_TOOL_BRK uses IF/ELSE instead of RET inside the IF.
  - Probe cycles: S_TSA = S_FA (the safe area alarm stops AUTOMATIC, MC PM
    3.10), _AMODE = 0, _DMODE = 1. The Z datum and inside features start
    S_FA + 1 mm (0.04 in) above Z nominal (MC PM 4.3.7: "somewhat greater").
  - Part existence check is a MEAS=1 touch with $AC_MEA[1]: no part sets
    status 2 with no alarm. CYCLE978 would alarm 61301 (MC PM 3.16.5).
  - Every probing section re-selects G54 D1 after a SUPA ... D0 retract.

RESTART
  Offsets and nest status are written only when GV_STEP==0. After a reset
  mid-job the next start shows RESUMING AT STEP, holds on M0, then resumes
  at that step and nest. For a new pallet set GV_STEP=0 first.
  Max breaks in a step: park and hold until reset (LOOP / M0).

FIRST RUN ON THE MACHINE (prove-out, single block, low feed override)
  1. Probe one nest. On an outside feature, watch the probe go DOWN by
     S_ID from the start height (negative S_ID lowers in G17).
  2. After probing, read $P_UIFR[5,X,FI] (nest 1). Not 0 = MD18600 works
     and the FI tolerance check is live.
  3. Force a break on the laser: BL9908_MOD must return 19.19, the nest
     goes to 100+step, the next nest gets a sister tool.
  4. Reset mid-step, restart: RESUMING AT STEP / NEST must name the nest
     that was cutting, and the job must resume there.
  5. Out-of-tolerance nest: status 2, MSG, M0; that nest is skipped later.
  6. CMC: first run on a scrap part with verify on. Check TCA brings back
     the same sister (C_P1_CMC_BACK); watch the probe lower with MEAS=1;
     read CMC_LOG.SPF; reset mid-nest and restart: no double correction.

BLUM MACROS (outside the Siemens manuals, not verified)
  BL9908_MOD must return 19.19 in its last parameter on a break and disable
  the tool. BL9902 and its ;NCG# lines in L_TOOL_MEAS are copied verbatim
  from the old package (inch values). S3750 is the laser speed in both.

TESTS (tests/, for whoever maintains the generator)
  node tests/run_fixtures.js OUT    engine on 9 fixture jobs (2 CMC), bad
                                    jobs, step builder, CMC math and R blocks
  python3 tests/nc_lint.py OUT/f*   manual rules on every generated file
  python3 tests/test_lint_cmc.py OUT/f8_cmc_milling
                                    the CMC lint rules catch broken output
  node tests/e2e.js OUT2            browser test, file://, network blocked
