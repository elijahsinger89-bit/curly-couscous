# The standpipe, extracted from the 1st Edition sheets

**READ 2026-09-04 at the owner's request, from two sheets read directly rather
than through a summary:**
`main/float-standpipe-assembly-1st-edition.pdf` and
`addon/storage-standpipe-1st-edition.pdf`, one page each.

> **THE OWNER'S CAVEAT GOVERNS AND IS FROZEN AS G-40. NOTHING BELOW IS
> AUTHORITATIVE.** "Every figure in it is a candidate for T-018, assume seeded
> until traced. Every part in it may have been superseded, returned, or never
> bought. Where it disagrees with your tree, YOUR TREE WINS. Do not cite it as a
> source for anything."
>
> **D-121 adopted THE STANDPIPE AS A MOUNTING METHOD ONLY: no dimension, no
> material, no attachment detail, no count. Nothing in this file changes that.
> Everything here is a proposal to confirm or replace.**

## PART 1. The figure-free mechanism, which is the part worth having

**These are the sheets' RULES rather than their numbers. Each survives every
figure in the old set being wrong, which is the test D-121 was adopted under.**

**SP-01. THE TRIP HEIGHT IS WHERE THE WEIGHT SITS, NOT WHERE THE FLOAT SITS.**
Stated in a box of its own on the day tank sheet. An external cable weight clamps
to the float's cord; **the weight is the PIVOT and the float hangs on a tether
below it, swinging from the weight.** So the level at which a float trips is set by
where its weight is clamped, and the float body's own position is a consequence.
**Observed in the 1st Edition set, unverified. Confirm or replace.**

**SP-02. THE TETHER LENGTH SETS THE DIFFERENTIAL.** A short tether is a narrow
swing angle and a small band between make and break; a longer one is a wider band.
**So the switching band is a build dimension, not a property of the float.**
Observed, unverified. Confirm or replace.

**SP-03. THE TRIP HEIGHT IS SET BY A TIE ON THE CORD, NEVER ON THE FLOAT BODY.**
And the commissioning rule attached to it, in red on both sheets: **"Fill slowly
and confirm each float trips at its mark. ADJUST THE CABLE TIE, NEVER ADJUST THE
WIRING."** Observed, unverified. Confirm or replace.

**SP-04. MARK EVERY TRIP HEIGHT ON THE PIPE BEFORE ANYTHING GOES IN THE TANK.**
With a paint marker, against a stated datum. **The pipe carries its own scale, so
a float that has moved can be seen to have moved.** That is the answer to the
thing that made a drifted float dangerous - **nothing in this system measures a
level, so an unmarked float that slips is invisible; a marked one is not.**
Observed, unverified. Confirm or replace.

**SP-05. FIT THE BRACKET FIRST, THEN SET FLOAT HEIGHTS AGAINST THE STANDPIPE.**
An order-of-operations rule, not a dimension. Observed, unverified.

**SP-06. THE BRACKET CARRIES THE PIPE, THE FLOATS AND EVERY CORD. NOTHING HANGS
OFF A FLOAT BODY AND NOTHING RESTS ON THE TANK FLOOR.** This is the sentence D-121
already adopted, found here in its original form. **The end cap stands clear of
the floor in the day tank and above the cone apex in the cone-bottom storage
tank.**

**SP-07. CORDS RUN UP THE PIPE, TIED AT INTERVALS, AND LEAVE THROUGH A CORD GRIP
WITH A DRIP LOOP OUTSIDE THE BOX.** The drip loop is the part the current tree has
no position on. **It is the same design-to-shed principle D-047 applies to the
panel's top face, applied to a cord entry.** Observed, unverified. Confirm or
replace. **This is CBL-04's business and it arrives free with the mounting method,
which is what D-117 predicted: a cord route is a consequence of a mounting
method.**

## PART 2. Two things this corrects in what the owner transcribed

**He read these off other pages and flagged the gaps himself. The standpipe sheets
close both.**

**SPX-01. LS-8 IS NOT UNACCOUNTED FOR. It is STORAGE HIGH-HIGH.** The storage sheet
names it and gives it a role: if the fill overruns, LS-8 drops a permissive and
the fill relay with it, described as a hardware backstop **in series with the day
tank's own high-high float.**

**SPX-02. THE STORAGE LOW PUMP-DOWN FLOAT IS LS-3, AND IT IS IN THE LS SERIES.** The
owner recorded it as "a separate STORAGE LOW pump-down float, not numbered in the
LS series". The storage sheet numbers it LS-3 and describes it as the pre-existing
transfer dry-run stop, distinguished from LS-6, LS-7 and LS-8 not by being outside
the series but by **being base-set hardware while those three arrive with the
auto-fill add-on.**

**So the eight-float roster is fully accounted for on these two sheets, with no
gaps and no spares:**

| Tank | Float | Role as drawn |
|---|---|---|
| Day | LS-2 | high-high, overfill fault |
| Day | LS-5 | fill stop |
| Day | LS-1 | fill start |
| Day | LS-4 | low-low, dry-run stop |
| Storage | LS-8 | high-high |
| Storage | LS-7 | fill stop |
| Storage | LS-6 | fill start |
| Storage | LS-3 | storage low, transfer dry-run stop |

**Observed in the 1st Edition set, unverified. This is a ROSTER OF POSITIONS, not
a parts list.** D-118 struck the inherited part roster and restarted the float
pass from requirements; **what this table is good for is confirming that the
positions a design must answer for are eight, not six or ten.**

## PART 3. The electrical observations, and one of them is worth a decision

**E-01. THE CONTACT SENSE FOLLOWS THE ROLE, AND THE PATTERN IS DELIBERATE.**

| Role | Contact as drawn |
|---|---|
| High-high, fill stop, fill start | **NC** |
| **Dry-run and pump-down stops - day LS-4 and storage LS-3** | **NO** |

**Both of the floats whose job is to STOP something on low level are drawn NORMALLY
OPEN, while every fill-control float is NORMALLY CLOSED.** Observed, unverified.

**Why it matters here rather than in the old build: S-05 closed level-based
YESTERDAY, D-119, and the dry-run element is now a float.** G-22 asks what a
severed conductor does. **On an NO dry-run contact a severed conductor reads the
same as "level is fine", which is the UNSAFE direction.** On an NC one it reads as
a trip.

**BOSS states no fail direction and inherits none - that is F-017's lesson and
G-22's amendment.** What is raised is that **the old set's choice and this build's
newly-closed S-05 land on the same contact, and the choice was made in a build
whose dry-run element was not this one.** MAIN-PANEL and WATER jointly, against
G-22 and D-049.

**E-02. THE FLOATS ARE DRAWN AS SPDT, A CHANGEOVER.** Observed, unverified, and
the part may have been superseded, returned or never bought.

**If a float has a changeover contact, it carries a second leg for free.** G-27:
"a complementary pair is a fail-detect, and the construction rule is both legs at
the same potential on the same cable - then a severed conductor makes them
contradict, and any state where both agree is a broken sense path." **D-053 calls
that free wherever two legs of one changeover are already bought.**

**Nobody has considered a float as a source of a complementary pair.** G-27 was
written for relay contacts. **Raised as a question and not a proposal: a
fail-detected float is a different thing from a fail-safe one, and F-091's overflow
question exists precisely because a single float currently has no second line.**

## PART 4. Contradictions inside the old set, from these two sheets alone

**These are findings about the old set and not about this tree. They are also the
reason no height is adopted.**

1. **The day tank sheet places its high-high float ABOVE THE TOP OF THE PIPE
   CARRYING IT** - the elevation's own MAX line sits below that float's height,
   on a pipe hung clear of the floor. Either the datum silently changes for that
   float or the drawing is wrong.
2. **The datum is stated two ways in the set.** These sheets say, in red and twice,
   **heights are off the END CAP FACE, not the pipe end.** The build book's float
   sheet says all dimensions are off the TANK FLOOR. **The same numbers appear
   under both**, and the two datums differ by however far the end cap stands off
   the floor.
3. **The day tank sheet's clamp detail says "identical for all five floats" while
   its own elevation and parts table carry four.** Explained by the base-set and
   add-on split, but stated on one sheet without the qualifier.

**A number that disagrees with itself inside its own source is not a seed, it is
noise. D-120 already refuses these heights and this is the evidence for it.**

## What this file does NOT do

**It adopts nothing beyond D-121's method.** It names no part as a choice. It
states no height, no length, no diameter and no material as a fact of this build.
**Every item is a proposal to confirm or replace, and the verification is the
owner's.**
