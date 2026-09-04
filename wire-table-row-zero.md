# One wire table row, filled in for a real conductor

**Written 2026-09-04 at the owner's request. Not the table. ONE ROW, to find out
whether the schema survives contact with a real conductor before 200 of them exist.**

It did not survive intact. **Two defects fell out of filling in a single row and
both are namespace defects, which is the class that is cheap now and unfixable
after the generated set exists.** They are at the bottom.

## The schema

Twelve columns. **Each one is here because a specific frozen row or rule needs it,
and that is stated - a column nobody can name a reason for is a column that gets
filled in with a guess.**

| # | Column | What it is for | Who owns the value |
|---|---|---|---|
| 1 | **Conductor ID** | The one identity. Unique across the build | BOSS assigns the namespace, INTERCONNECT assigns within it |
| 2 | **Cable** | Which CBL- run it travels in | INTERCONNECT |
| 3 | **From: device** | Named as the tree names it, never invented | The subsystem owning that end |
| 4 | **From: terminal** | Position or silk, **never a name that is not printed on the part**, per F-051 | The subsystem owning that end |
| 5 | **To: device** | As above | The subsystem owning that end |
| 6 | **To: terminal** | As above | The subsystem owning that end |
| 7 | **Function** | What it carries, in words | The interface row |
| 8 | **Class** | 120 VAC / 24 V control / SELV signal / EGC. **Drives segregation and insulation rating** | Derived from the interface row, not chosen |
| 9 | **Design current, and WHICH EVENT** | **Not "current". The event.** A contact is sized on make and break, not on holding | The subsystem owning the load |
| 10 | **Interface row** | The F-, P-, S-, CBL- or M- row this conductor realises. **A conductor with no interface row does not exist** | BOSS |
| 11 | **Fail behaviour** | What a severed conductor does, per G-22. **Never inherited, per F-017** | The subsystem that established it, or OPEN |
| 12 | **Status** | BUILDABLE, or BLOCKED ON *(named row)* | BOSS |

Deliberately **not** columns: length, gauge, core count, colour, part number. **Those
are outputs of a cut rule and a lookup, not facts about a conductor, and putting them
here is what makes a wire table disagree with a cable schedule.** Length comes from
D-090's rule - wall run plus 3 ft - applied at cut time, not stored twice.

## The row

The fill solenoid's coil hot leg. **Chosen because it is the newest fully-specified
device in the build, so if any row fills in cleanly it should be this one.**

| Column | Value |
|---|---|
| Conductor ID | **CDR-001** |
| Cable | **CBL-04** *(WATER field devices to INTERCONNECT field runs)* |
| From: device | **MAIN-PANEL: the fill relay pole that switches the solenoid** |
| From: terminal | **OPEN.** No terminal namespace exists yet. **This is defect 2 below** |
| To: device | **The fill solenoid, ASCO 8210G095AC120/60** |
| To: terminal | **OPEN.** Coil lead identification not established. Per F-051 it is named by what is printed on the part, and nobody has looked |
| Function | Switched 120 VAC to the fill solenoid coil |
| Class | **120 VAC.** Not SELV. **Segregation applies against every signal run sharing the wall** |
| Design current, and which event | **0.58 A INRUSH, at make and break. NOT the 0.21 A holding figure.** parts.md, D-136 |
| Interface row | **OPEN - and this is defect 1 below.** The solenoid's power feed has no P- row. F-01 and F-02 are its FLUID rows; its electrical crossing was never created |
| Fail behaviour | **Severed conductor: the coil de-energises and the valve SPRING-RETURNS CLOSED.** D-114 and G-39. **This is the one cell that filled in with certainty**, because the fail state was chosen before the part was |
| Status | **BLOCKED ON: no P- row for the solenoid feed; no terminal namespace; coil lead identification not looked up** |

## What filling in one row cost, and what it found

**Twelve cells. Four filled with certainty, three filled from the interface table,
five OPEN - and two of the five are defects rather than pending work.**

### DEFECT 1. The solenoid has fluid rows and no power row.

**F-01 and F-02 carry the water. Nothing carries the electricity.** The valve was a
"solenoid" in the tree for weeks as a thing that opens, and **the conductor that
opens it never got a crossing.**

It is invisible until you try to write the conductor down, because **every other
view of the system describes the valve by what it does to water.** The wire table
is the first artifact that asks who energises it.

**BOSS does not create the row from here** - it needs both ends named by the
subsystems that own them, and MAIN-PANEL's ladder pass is running now and will hit
the same gap from the other side. **Recorded and routed, not invented.**

### DEFECT 2. There is no terminal namespace, and the ID namespace is already ambiguous.

**Columns 4 and 6 have nowhere to point.** A terminal schedule needs an identity
scheme before it has rows, and INTERCONNECT is deciding the schedule's shape right
now, so the moment to settle it is this one.

**And worse, in what already exists: F- MEANS TWO THINGS.**

| Prefix | Used for | Example |
|---|---|---|
| F-nn | **Fluid interface rows** | **F-09**, the day tank outlet, the scope boundary |
| F-nnn | **Findings** | **F-090**, the struck float roster |

**They are distinguished by ZERO PADDING ALONE. F-09 and F-090 are one keystroke
apart and mean unrelated things**, one of them being the frozen edge of the whole
project's scope.

**This is F-026 exactly - the collision AUDIT caught between the interface table's
old C-nn cable rows and commissioning's C-nn rows, which was fixed by renaming
cables to CBL-.** It was fixed in one place and the same defect was left standing in
another. **Nobody noticed because no document had ever had to cite both kinds of F-
in the same table. A wire table does: column 10 cites interface rows, and every
other file cites findings.**

**CDR- is used above as the conductor prefix precisely to avoid guessing into this.
W- is already taken informally by C-12's W-1 witness.**

## What this row proves about the schema

**The schema survives. The tree does not, quite.**

Nine of the twelve columns are answerable in principle today and three are blocked
on things that are one decision each. **No column turned out to be unfillable in
principle, and none turned out to be unnecessary** - which is the useful result,
because it means the shape can be committed to before the rows exist.

**The cost of finding this was one row. The cost of finding it at row 140 would have
been 140 rows.** That is the whole argument for the owner's instruction.
