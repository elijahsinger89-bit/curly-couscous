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
| All four enclosure owners | Gland positions and entry sides, C-01 to C-04 |
| MAIN-PANEL | Which runs are line voltage |
| DISPLAY-BOX | Probe cable length limit and step and direction cable requirements |
| WATER | Field device positions: floats, solenoid, leak sensors, pump cords |

## Do not

Do not state a cable part number, a gauge, a conductor count or a gland size
from memory. Return the requirement and a search term. Do not pick a wall
position that puts a cable where a jug is changed or a tank is filled without
saying so.
