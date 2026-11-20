HF5500 POST (R06f_E09_mmf) - START / END FOR THE NEST FRAMEWORK
================================================================

WHAT THIS IS
  Replacement template files for the post folder R06f_E09_mmf\files_x.
  The production macros (A_P1, L_RUN_NESTS, L_TOOL_*) call every posted
  B program once per nest (CALL LD_PROG) after C_P1_LOAD_WO has put the
  nest's work offset in G54 and the framework has loaded the tool. These
  files make the B program start and end fit that. Toolpath output is not
  changed.

INSTALL
  1. Back up the whole post folder (R06f_E09_mmf).
  2. Copy files_x from this zip over R06f_E09_mmf\files_x (same names).
  3. Postprocessor Configuration (by hand, both stay comments):
       TName_prefix   ;      ->  ; T                     (reads ; T="905080900")
       TC_command     ;M6    ->  ; M6 BY THE FRAMEWORK
  4. Post one milling and one turning B program and check them (below).
  The main (A_P1) and the other job files do not change: repost only the
  B programs.

CHANGES
  StartEnd\pgm_bgn.txt (start of every file)
    Header block like the generator's files: program, compound job,
    job list, machine, control, post date, NEEDS NEST FRAMEWORK REV 02,
    the B program rules and a revision control block. The post has no
    part-number or programmer variable: the part number is in the program
    name, BY stays XXXX.
  StartEnd\pgm_bgn_2.txt (program start)
    Removed: M01 (stopped at every nest with optional stop on), STOPRE,
    the empty IF $P_SEARCH ... ENDIF block, G500 (deselected the G54 that
    C_P1_LOAD_WO just set), G0.
      G17 G40 G60 G70 G90 G94 M40 / CYCLE800() / TRAFOOF / TRANS
    20 Nov 2026 fix: G97 is out of this block. G94 and G97 are the same
    G group on SINUMERIK (group 15, feed type): both in one block = alarm
    12060 "same G group programmed repeatedly". The block is the shop's own
    line again, without G0 and G500.
  StartEnd\pgm_end.txt (program end, RET follows from final_M)
    Removed: the X / Y move to the + limits and A=DC(0) B=DC(0) after
    every nest (the next nest swivels straight back with CYCLE800).
    Added: M5, CYCLE832(), CYCLE800(), TRAFOOF.
      G0 G53 G17 G90 Z=$MA_POS_LIMIT_PLUS[AX3]-.04 D0
      M5 / M9 / CYCLE832() / CYCLE800() / TRAFOOF
    20 Nov 2026: the G97 that was here is gone (not in the shop's post;
    the next B program's start block sets G94 again).
  Every other file in this zip
    Only the line that printed the template's own file name was removed
    ("; sP.txt", "; --- files_x\ToolChange\TC_bgn.txt ---", ...). Every
    code line and the tool / job comments are unchanged. Files that held
    nothing but that line are now empty.

CHECK AFTER POSTING
  - The header block is first, with program name, job list and date
    filled in. If the compound job line is empty there, delete that line
    from pgm_bgn.txt (those variables may only be set inside a job).
  - No "; ...txt" file-name lines, no M01, no G500, no $P_SEARCH.
  - The tool call reads ; T="..." and ; M6 BY THE FRAMEWORK.
  - The start: G17 G40 G60 G70 G90 G94 M40 (no G97).
  - The end: Z retract, M5, M9, CYCLE832(), CYCLE800(), TRAFOOF, RET (no G97).

ON THE MACHINE (first run, single block)
  - Two nests of one step: no stop between nests, the table goes straight
    from one nest to the next.
  - The table now stays at the nest's angle when the B program returns
    (before, every B program swung A and B to 0). Watch the first laser
    measure and break check (L_TOOL_MEAS / L_TOOL_BRK) with the table at
    a nest angle: the path to the laser must be clear. If it needs A / B
    at 0, that goes into L_TOOL_MEAS / L_TOOL_BRK, not back into the post.
