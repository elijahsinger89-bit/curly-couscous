HF5500 POST (R06f_E09_mmf) - COMMENT CHANGES FOR THE NEST FRAMEWORK
===================================================================

RULE
  Only comments are changed. Every code line is exactly as the post
  writers made it (checked line by line against the original files_x).

INSTALL
  1. Back up the whole post folder (R06f_E09_mmf).
  2. Copy files_x from this zip over R06f_E09_mmf\files_x (same names).
  3. Postprocessor Configuration (optional, both are comments already):
       TName_prefix   ;      ->  ; T                     (reads ; T="905080900")
       TC_command     ;M6    ->  ; M6 BY THE FRAMEWORK
  4. Repost the B programs.

CHANGES (comments only)
  StartEnd\pgm_bgn.txt
    Header comment block like the generator's files: program, compound
    job, job list, machine, control, post date, NEEDS NEST FRAMEWORK
    REV 02, the B program rules, a revision control block.
  StartEnd\pgm_bgn_2.txt
    One comment line added on top: "; --- B PROGRAM START (NEST
    FRAMEWORK, CALLED PER NEST) ---". Code unchanged:
      G0 G17 G40 G60 G70 G90 G94 G500 M40 / CYCLE800() / TRAFOOF / TRANS /
      M01 / STOPRE / IF $P_SEARCH==TRUE ... ENDIF
  StartEnd\pgm_end.txt
    The two file-name comment lines replaced by "; --- B PROGRAM END:
    BACK TO L_RUN_NESTS ---". Code unchanged:
      Z retract with M9 / X Y to the + limits / A=DC(0) B=DC(0)
  Every other file
    Only the comment line that printed the template's own file name was
    removed ("; sP.txt", "; --- files_x\ToolChange\TC_bgn.txt ---", ...).
    Files that held nothing but that line are now empty.

HISTORY
  19 Nov 2026: the first version also changed code (start: G0, G500, M01,
  STOPRE and the block-search stub removed, G97 added; end: M5, G97,
  CYCLE832(), CYCLE800(), TRAFOOF added, X/Y/A/B move removed). G94 and
  G97 in one block gave alarm 12060 on the machine (20 Nov). All code
  changes are taken back: the post writers' code stands.
