# AUDIT run 2: the channel token declaration against its four consumers

Returned 2026-08-30. AUDIT read the declaration, the four consumer files, the
interface table, decisions and traps, and nothing else. Questions only. It reports
FINISHED on the ground it was given and NOT finished on anything needing
findings.md, commissioning.md, agents.md, parts.md or the control-software files.

## What it could not check, named as findings about the picture

**Z5 is load-bearing and undefined in anything AUDIT was given.** The whole Position
axis is "read from Z5", and the only other appearance in its eight files is DOSING's
O-04. **Nothing says where Z5 is or who owns it. The strongest claim in the
declaration cannot be checked from its own consumers' files.**

"Exhaustive for the chain in F-006" is exhaustive against a document it does not
have. And "DOSING's carrier requirements" are restated in the declaration but live
in the F-002 proposal, not in dosing.md.

## Tier A, where a wrong answer costs a rebuild or a permanent silent crossing

**A1.** Does the Position axis leave PUMP-BOXES' box division any freedom beyond
which box stands first and confirming a contiguous split? **The heads are
panel-mount through sealed lids, so if PUMP-BOXES returns a division the axis
forbids, is the correction a re-drilled lid?**

**A2. Who was handed the lid penetration?** It is one of the eleven carriers.
PUMP-BOXES gets "driver, head and box", DOSING gets "tube, jug station and jug
body". **Is the lid penetration in either row? CBL-05 is exactly that two-owner
seam. T-002's shape: one hop of eleven that both consumers' rows end before
reaching.**

**A3. Does the pump tube carry a token, and is a tube change a channel change?** The
declaration says a tube that is ever moved must be re-tokened, "which is a channel
change, not a maintenance action". **The change table has rows for a moved head, a
replaced driver, a retired product and a retired channel. Is there a row for a
replaced pump tube? Does a routine 1000-hour consumable swap trigger OUT OF SERVICE
and C-09 on all eight?**

**A4.** Is the carrier list exhaustive against a cable schedule that does not exist
yet? **If DIAG and INDEX are ever wired they are per-channel cores the INTERCONNECT
row already obliges to be tokened, but the exhaustive list does not name them.**
T-012: derived from the schedule, or asserted ahead of it?

**A5.** Is the monotone-run question addressed to the party that can answer it? The
row of heads is PUMP-BOXES', the row of stations is DOSING's, the wall is M-02 which
INTERCONNECT only arbitrates, **and INTERCONNECT is deliberately not invoked. Is it
one question or three?**

**A6. Does INTERCONNECT know it consumes this declaration at all?** Its file
contained no occurrence of token, CH1, channel, S-19, D-021 or Z5, and its Out of
scope says "what any signal means". **Is applying a channel identity inside or
outside that line?** *FIXED by BOSS: the declaration is now written into
interconnect.md and display-box.md, with the note that applying an identity is not
interpreting a meaning. Findings F-036.*

**A7. Can a channel actually be taken OUT OF SERVICE?** The change procedure says
software refuses to command it. **G-21 and D-032 say software has no per-driver
disable, permanently, and a severed DIR runs a head on an enabled driver. Does OUT
OF SERVICE mean anything beyond software declining to issue steps, and is the
declaration relying on an inhibit that will never exist?** *OPEN and sharp.*

**A8.** Does the colour axis collide with T-011, two conductors in one jacket cannot
share a colour? **Is the colour axis meant to reach the cable core at all, or only
the wall-visible wet-path carriers?**

## Tier B

**B9.** display-box.md contained no occurrence of token or CH and spoke only of
"eight drivers". **Is that a vocabulary for eight tokens or a driver-indexed
picture, and will the sixteen sweep rows be keyed by token or by output number?
That is where T-013 bites.** *Partly fixed with A6.*

**B10.** The declaration says none of the consumers is waiting; display-box.md says
it waits on CONTROL-SOFTWARE for which signals it needs. **Same request answered, or
two different things?**

**B11. Where does the one record per token live?** The declaration requires exactly
one record holding pin, core, box and product. **The pin is in display-box.md, the
core in INTERCONNECT's schedule, the box in pump-boxes.md, the product in DOSING's.
If four attributes are written into four files, what is the one record, and does
reconciling four files by hand become the thing forbidden item 1 calls a table in
any medium? The change procedure says the change is made in ONE place first. Which
file is that?**

**B12.** Is C-09 free and hardware-free, or does it need doses? D-022 calls it free
and needing no hardware; the declaration asks the owner whether its trace doses may
go into a live tank. **Is C-09 one check or two? T-017's shape: an element placed
first in a chain that may need the chain built to produce it.**

**B13.** The declaration counts the C-09 script and the UI trace mode as complete
and consumable today. **S-14 says no Pi application source is in reach and is still
open. Are a script and a UI mode being counted as complete in an application nobody
has located? T-004.**

**B14.** Is the PUMP-BOXES box division open or closed? Its bullet sits under a
"now closed" heading while saying "coordinate with INTERCONNECT, do not decide
alone", and INTERCONNECT is not invoked.

**B15.** Should the driver-replacement conditional still be conditional? MS1 and MS2
are PUMP-BOXES' to set. **Should the row read that a driver replacement ALWAYS voids
C-01?**

**B16.** Do the eight injection ports have to ascend from Z5 too? The declaration
tokens both ends of the delivery line but names heads, stations, tube ends and UI
lists in the ordering rule, not ports.

**B17.** Can DOSING token a tube before the product on that token is known? Five of
eight products are unnamed and tubing selection is open on per-product
compatibility. **And the colour carrier's "union chemical duty" cannot be a union
over products nobody has named.**

**B18.** Is the S-16 non-adjacency rule a constraint on the OWNER's product-to-token
assignment, and does the owner's row say so plainly enough that they know they are
the one constrained?

## Tier C

**C19.** The CBL rename left one reference behind: dosing.md's waiting-on row said
"Lid penetration, C-05" with C-0n now meaning commissioning everywhere else.
*FIXED.* And **F-06 the fluid crossing and F-006 the finding are one character
apart and both concern the jug and tube path.**

**C20.** Are "mapping" and "binding" the same word to all five parties? **Will a
consumer see its own required attribute table and think it has been told not to
write it?**

**C21. Is a jug an attribute?** The declaration says every attribute is replaceable
without the channel changing, **but G-17 dedicates the jug for life and G-18 fixes
the tube to the channel. Are jug and tube attributes in the same sense as a pin and
a core, or a third category: bound-for-life attributes that cannot be replaced
independently? The attribute-versus-identity line is drawn in a different place at
the wet end than at the electrical end.**

**C22.** Does DOSING own "the fixed station" as a named artifact? Its file does not
use the word. **Are eight fixed, ordered, tokened stations something DOSING knows it
owes?**

## Where the five genuinely agree, stated plainly and not manufactured

- **DOSING and the declaration agree on the definitional end**, word for word in
  substance. **Of the four consumers, DOSING is the only one whose file recorded the
  consumption.**
- The carrier count reconciles: eleven carriers, eleven hops.
- **Both-ends labelling agrees, and INTERCONNECT reached it independently** in its
  own words: a conductor labelled at one end only is worse than one labelled at
  neither, because it looks done.
- The out-of-service stop agrees with G-16, and the declaration says so.
- G-17 and G-18 are consumed correctly.
