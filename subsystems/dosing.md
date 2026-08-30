# DOSING

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

The PVC dosing manifold as a physical assembly: the vertical probe section, the
probe wet fittings, the flow cell, every injection port, and the manifold body
between the two unions. The entire wet path from the manifold back to the pump
heads and on to the jugs: dose delivery tubing, head suction tubing, the
nutrient jugs, jug placement, and how a jug is changed without spilling or
losing prime.

Ends at the manifold unions F-03 and F-04, and at the pump head barbs F-05 and
F-06.

## Out of scope

The pump heads themselves and everything inside the pump boxes, including the
lid penetrations. That is PUMP-BOXES. The EZO circuits and carriers are
DISPLAY-BOX. Cable runs are INTERCONNECT. The day tank and the return drop are
WATER.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| G-10 | Probes sit first in line in a vertical section, ahead of every injection point, so a bubble cannot corrupt a reading |
| G-04 | No flow meters on the dosing lines. Nothing measures what a head actually delivered |
| G-05 | No level sensors on the jugs. Remaining volume is arithmetic |
| D-006 | DOSING owns manifold to head to jug as one path. PUMP-BOXES stops at the barb |

## Settled

- Manifold is PVC and the owner has the PVC.
- Injection is downstream of all three probes.
- The loop returns to the day tank by an open drop, WATER's side.

## Open, owned by DOSING

- Probe wet fitting requirement for each EZO probe, per the probe body. Return
  a requirement and a search term, not a part number.
- Injection port arrangement: how a port is made in PVC, and whether ports need
  a check to stop backflow into a dose line when its head is idle. Report the
  requirement, do not pick a part.
- Tubing selection for delivery and suction, against the head barb PUMP-BOXES
  returns and against nutrient chemical compatibility.
- Jug placement: height relative to the head, so a head is not asked to lift
  more than it can and so a jug change is possible without a tool.
- Whether a dose line can siphon when the head is idle, given jug height.
- Manifold orientation and mounting on the dosing wall, M-02, jointly with
  PUMP-BOXES.

## Settled 2026-08-30: the flow cell is a fitting, not an instrument

There is no flow signal into the Pi. The flow cell is a PVC body that holds the
probes in the moving stream. No output, no contact, no wire. Decision D-007,
interface S-13. Do not build a sensor pocket, a tapping or a wire route for it.

## Open design question routed to DOSING, answer only, change nothing

Read findings.md F-001 first. The only verification that exists is EC rising
during a dose, which confirms the manifold flowed but not which of the eight
heads delivered, and does nothing at rest or for pH up, pH down and fulvic.

Answer three things for your path, manifold to head to jug:
- what would it take to confirm a per-channel dose actually moved
- what it would cost
- where it would land physically

ANSWERED 2026-08-30. Nineteen options are in
subsystems/dosing-verification-options.md, ranked by cost, each with a
requirement, a search term, the numbers it needs, its physical landing and its
crossings. O-19, a flow meter per channel, is written down honestly costed and
neither softened nor advocated. Nothing is decided and nothing was changed.

Two things came out of that answer and are now BOSS-held:
- findings.md F-002, a jug reconnected to the wrong channel, which no
  flow-measuring option catches.
- interface-table.md S-16, the pH probe appearing to cover two of the three
  channels F-001 calls EC-invisible. That extends FROZEN row S-15, so it is the
  owner's decision.

DOSING did not declare itself finished and BOSS has not declared it finished.

## Owner rulings on that answer, 2026-08-30

| Ruling | Effect on DOSING |
|---|---|
| D-011 | pH attributes pH up and pH down. S-16 frozen with two constraints |
| D-013 | Fulvic stays unattributed. Do not solve it |
| D-014 | O-19, a flow meter per channel, is off the table. Do not bring it back unless something changes |
| D-015 | F-002 outranks the option list. O-09 and O-11 come back as their own proposal, separate from the nineteen |
| D-012, F-004 | Every tank-read check is delayed by an unmeasured interval. DOSING and CONTROL-SOFTWARE answer the settling time between them |

## Both tasks answered 2026-08-30, neither finished

1. F-002 proposal: subsystems/dosing-f002-proposal.md. Blocked from being built
   on F-06, which is OPEN, and on DOSING's own open items: tubing selection, jug
   placement, the siphon question.
2. Wet side of F-004: subsystems/dosing-f004-wet-side.md. Blocked on WATER
   returning circulation flow at F-03, DISPLAY-BOX returning probe response, and
   DOSING's own manifold volumes.

Four things DOSING found and did not fix, now BOSS-held: interface S-19 and
findings F-006, the channel token nobody owned; commissioning C-09, the
end-to-end trace; commissioning C-08 restated as an in-situ measurement, found
independently of CONTROL-SOFTWARE; and the C-02 ordering circularity, now fixed
in commissioning.md.

Two owner decisions the proposal forces and DOSING refused to make: whether jugs
are dedicated per channel for life or interchangeable vessels, and whether the
jug change procedure is defined so the break point IS the keyed joint. Without
the second, the key is decorative.

## Waiting on

| From | What |
|---|---|
| PUMP-BOXES | Head barb form and size, F-05 and F-06. Lid penetration, C-05 |
| DISPLAY-BOX | Probe cable termination and length limits, S-11 |
| WATER | Union type at F-03 and F-04, and circulation pump flow through the manifold |

## Do not

Do not decide port count, manifold diameter, tubing size or jug volume from
memory. Counts come back when the requirement is known.
