# INTERCONNECT

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

Every cable between the four enclosures and out to the field. Wall layout and
enclosure positions relative to each other. Cable routing, separation of line
voltage from signal, cable and gland selection, connector scheme, strain relief,
and labelling at both ends of every conductor. Where the E-stop and manual reset
land on the wall so an operator can reach them.

Ends at each enclosure's gland. What is inside the gland belongs to that
enclosure.

## Out of scope

The inside of any enclosure. What any signal means. Which device a chain
contains.

## YOU CONSUME THE CHANNEL TOKEN. Read channel-token.md.

Added 2026-08-30 after AUDIT found that this file contained no mention of the token
at all, so INTERCONNECT did not know it was a consumer. Findings F-036.

CONTROL-SOFTWARE declares what channel N is, S-19 and D-021. **You are handed the
eight tokens, CH1 to CH8, to be applied as the conductor identity at BOTH ends of
every core carrying a per-channel signal.**

**You must not invent:** a per-cable restart if the eight are split across more than
one cable; a renumbering to match a connector's pin order or a core's position in a
bundle; or a channel token for a spare core. **A spare is a spare. There is no ninth
channel.**

**Where your own conductor-labelling scheme applies a code, the channel token
appears IN ADDITION, and the two are never merged or abbreviated into each other.**

Your "Out of scope: what any signal means" line does not exempt you from this.
Applying an identity is not interpreting a meaning.

One question the declaration puts to you and nobody else, and BOSS has flagged that
it may not be yours alone: **whether a monotone ascending run of CH1 to CH8, read
from the operator's standing position, is achievable across the wall you
arbitrate.** If it is not, that is reported to CONTROL-SOFTWARE as a defect in the
declaration and **is never solved locally by reversing a row.**

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| Physical shape | Four enclosures: main panel, two pump boxes on the dosing wall, one display box. Cables run between them on a wall |
| G-13 | The E-stop is a hardwired device an operator must reach. Its position is a safety matter, not a tidiness matter |

## Settled

- Four enclosures, wall mounted.
- Pump boxes are on the dosing wall with the manifold.
- Room is 62 to 65 F, under 60 percent humidity, not wet, but water moves tank
  to tank so a spill path exists.

## Open, owned by INTERCONNECT

- Wall layout: where each enclosure sits, and the arbitration of M-02 between
  DOSING's manifold and PUMP-BOXES.
- Cable schedule: one row per cable, both ends named, matched against the
  interface table so no crossing is missing a cable and no cable serves a
  crossing that does not exist.
- Separation of the 120 V pump and chiller runs from step and direction and from
  probe cables.
- Probe cable runs, S-11, against whatever length limit the EZO circuits impose.
  Get that limit from DISPLAY-BOX, do not assume one.
- Gland positions with each enclosure owner.
- Labelling scheme, applied at both ends. A conductor labelled at one end only
  is worse than one labelled at neither, because it looks done.
- Routing above any spill path, and drip loops where a cable enters a box from
  above.

## Waiting on

| From | What |
|---|---|
| All four enclosure owners | Gland positions and entry sides, CBL-01 to CBL-04 |
| MAIN-PANEL | Which runs are line voltage |
| DISPLAY-BOX | Probe cable length limit and step and direction cable requirements |
| WATER | Field device positions: floats, solenoid, leak sensors, pump cords |

## Do not

Do not state a cable part number, a gauge, a conductor count or a gland size
from memory. Return the requirement and a search term. Do not pick a wall
position that puts a cable where a jug is changed or a tank is filled without
saying so.

## THREE THINGS YOU WERE BLOCKED ON ARE SETTLED. 2026-09-04.

**Your first pass is accepted, D-142. Zero buildable of twenty is rule 9 working,
not pessimism, and BOSS is not asking you to soften it.**

**1. THE NAMESPACE, D-145 and G-43.** The reserved list is at the top of
interface-table.md. **You were right that CBL- names a CROSSING and cannot serve as
a cable identity** - that is why wire-table column 2 had no valid values.

| New prefix | For |
|---|---|
| **RUN-nnn** | One physical cable run. Yours |
| **TRM-** | One terminal. **The prefix is reserved; THE SHAPE IS YOURS to propose**, and only the prefix was BOSS's to settle |
| CDR-nnn | One conductor. The wire table's |

**And fluid interface rows are renamed F-nn to FL-nn**, 72 references in one pass,
so F- now means only a finding. **Re-read any FL- row you cited before you write
against it.**

**2. THE GLAND DEADLOCK IS BROKEN, D-146, AND YOUR REFUSAL TO BREAK IT WAS RIGHT.**
Recorded as such: **an allocation of decision rights is an interface decision, and a
subsystem taking one unilaterally is how a boundary stops meaning anything.**

**THE ENCLOSURE OWNER DECIDES WHICH FACE AND IN WHAT ORDER. YOU DECIDE WHERE ON THAT
FACE AND THE SPACING.** Neither waits. **If an enclosure owner tells you it cannot
state a face without knowing the run, report that as a finding rather than
absorbing it** - it would mean that box's contents are being decided by its cabling.

**3. THE FLOOR DRAIN IS A TRACK, 6 IN WIDE, AND THE OVERFLOW MAY ENTER ANYWHERE**,
D-147. **A free entry point, not a fixed one.**

**Two of your findings are with their owners and neither is yours to solve: F-100,
the float cord being a part property rather than a cut length, is now in the float
requirement WATER is writing. F-099, parts.md's two cable-run tables with
contradictory allowance rules, is with the owner - BOSS does not edit parts.md.**

**What BOSS wants next from you, and only this: the cable schedule and terminal
schedule SHAPES you returned, now expressed with the real prefixes, and RUN-nnn
assigned to the 17 runs you enumerated.** Blocked rows stay blocked and keep saying
what blocks them. **A schedule of blocked rows with real IDs is a document; a
schedule waiting for everything to close is not.**

Write in ONE pass at the end. State no length, gauge, core count or part number.
