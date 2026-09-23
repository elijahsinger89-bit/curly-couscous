# THE NINE ACCEPTANCE CRITERIA BOSS OWNS

**Requested by the owner 2026-09-23. Each step below is reproduced from D8 exactly as
it stands. The ACCEPT line is the one that needs writing.**

**What an acceptance criterion has to be, per D8's own rule: HOW YOU KNOW IT IS RIGHT,
OBSERVABLE AT THAT MOMENT.** Not a figure to record - the RECORD line already carries
that. **A tick or no tick, decidable by the person standing there.**

**SIX CRITERIA COVER ALL NINE STEPS.** Three of them are pairs whose second step reads
"as the first": **D8-09 with D8-10, D8-18 with D8-19, D8-49 with D8-50.** The remaining
three - **D8-25, D8-26, D8-27** - stand alone.

**D8-27 is not really yours to write and is included so the set is complete.** Its ACCEPT
line says the row has no criterion AND SAYS WHY: **running it IS the decision to accept
an uncharacterised state on purpose, once, under observation.** The owner takes that
decision; BOSS records it. **If you agree the reasoning holds, the answer is "no
criterion, and here is the sentence that says so" rather than a criterion.**

---

## D8-09

**D8-09. Run C-24 on one float position: lift that float's conductor at the panel
terminal and observe the chain.**
SOURCE: C-24. One lift.
BEFORE: tanks empty and dry, the chain complete, and the float's conductor landed.
**Write the position's name beside the tick.** How many float positions there are is
D2's roster's fact and the float requirement's, and is not stated here.
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** C-24 says to confirm the chain does what
D-154 says it does, and **the eight fail directions are D-154's and are not printed in
the C- row.** Owner: **BOSS**, `decisions.md` D-154.
RECORD: D9 group **MR-G1**, one row per float position.
COST AND WHAT IT BUYS: **no part and no instrument added.** It buys the only test of the
float fail directions that exists, because C-19 records what the Pi reports and G-01
makes all eight floats invisible to the Pi. **F-109.**

## D8-10

**D8-10. Repeat D8-09 for the next float position, and start none until the one before
it is ticked.**
SOURCE: C-24.
BEFORE: as D8-09.
ACCEPT: as D8-09. **NO ACCEPTANCE CRITERION IN THE ROW.** Owner: BOSS, D-154.
RECORD: D9 group **MR-G1**.

## D8-18

**D8-18. Run C-19 on one sense conductor: disconnect it at the gland and record what
the Pi reports.**
SOURCE: C-19. No instruments needed.
BEFORE: **at the gland, not at a terminal.** Write the conductor's CDR- id beside the
tick. How many sense conductors there are is D5's fact.
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** C-19 says to record what the Pi reports
and names no expected report. **The expectation per signal is G-22's - what a SEVERED
conductor does and what a SHORT TO ITS REALISTIC NEIGHBOUR does - and it is not in the
C- row.** Owner: **BOSS.**
RECORD: D9 group **MR-G3**, one row per sense conductor.
COST AND WHAT IT BUYS: **no instrument and no part.** It is the only thing that converts
G-22 from an intention into a fact.

## D8-19

**D8-19. Repeat D8-18 for the next sense conductor, and start none until the one before
it is ticked.**
SOURCE: C-19.
BEFORE: as D8-18.
ACCEPT: as D8-18. **NO ACCEPTANCE CRITERION IN THE ROW.** Owner: BOSS.
RECORD: D9 group **MR-G3**.

## D8-25

**D8-25. Run C-13: measure the driver standstill current, and record the EN state it was
measured in.**
SOURCE: C-13.
BEFORE: drivers wired, rail set and recorded at D8-16, **and VDD present per whatever
P-09 decides. C-13's own row says this presumes VDD exists while P-09 has not said where
it comes from, and says not to read that as settled.**
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** C-13 names no limit. Its own stated
consumer is the rail's real load, **and no document read for this checklist holds a rail
load budget for the figure to be judged against.** Owner: **BOSS to say where that
budget lives; MAIN-PANEL owns the rail.**
RECORD: D9 row **MR-07**.
WHY IT MATTERS THAT IT IS MEASURED: `parts.md` records it as never measured and
currently assumed. **T-012: an assumption in that position is correct until the data
moves, with nothing to say when it stopped.**

## D8-26

**D8-26. Run C-15: measure the temperature rise inside a sealed pump box with one motor
running and three idle at standstill current, and record the EN state of the three idle
ones.**
SOURCE: C-15.
BEFORE: boxes populated and closed, heatsinks fitted, lids on.
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** C-15 names no limit and no pass mark.
Owner: **BOSS, with PUMP-BOXES stating the rating the rise is judged against.**
RECORD: D9 row **MR-08**.
COST AND WHAT IT BUYS: **no part.** It is the only measurement that could ever relax
G-06, one pump at a time, which is a THERMAL constraint and not a control preference.
**Sequential dosing is mandatory until this figure exists.**

## D8-27

**D8-27. Run C-18: command STEP with VM removed, and observe the manual-reset
re-application transient.**
SOURCE: C-18.
BEFORE: **read C-18's blocked-on cell first.** P-09 cannot be closed from documentation,
D-070: the datasheet neither allows, forbids nor characterises the state.
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW, AND THE ROW SAYS WHY.** Running it IS
itself the decision to accept an uncharacterised state on purpose, once, under
observation. The alternative is to remove the state, which reopens D-031. Owner: **the
owner takes the decision; BOSS records it.**
RECORD: D9 row **MR-09**, which is an observation record and not a figure.
WHY IT EXISTS: **no other row exercises the one state the system enters on every fault
and every shutdown**, and leaves by a human pressing a button at a moment software does
not choose.

## D8-49

**D8-49. Run C-01 on one channel: delivered volume per revolution and per step, measured
against REAL BACK PRESSURE into the running manifold.**
SOURCE: C-01. **Write the channel token beside the tick.**
BEFORE: D8-48 ticked. The manifold running, so the back pressure is the real one.
**G-04: nothing in this system measures delivered volume, so a wrong figure here is
invisible.**
ACCEPT: **NO ACCEPTANCE CRITERION IN THE ROW.** C-01 names no tolerance. It names a
DIRECTION only: the manufacturer's per-revolution figure is specified at NO back
pressure, so the real figure is lower, in a known direction, by an amount nobody has
measured. **A measured figure at or above the no-back-pressure figure is the one thing
the row lets you call wrong.** Owner of a tolerance, if one is wanted: **BOSS.**
RECORD: D9 group **MR-G6**, one row per channel, two value cells.

## D8-50

**D8-50. Repeat D8-49 for the next channel, and start none until the one before it is
ticked.**
SOURCE: C-01.
BEFORE: as D8-49.
ACCEPT: as D8-49. **NO ACCEPTANCE CRITERION IN THE ROW.** Owner: BOSS.
RECORD: D9 group **MR-G6**.
