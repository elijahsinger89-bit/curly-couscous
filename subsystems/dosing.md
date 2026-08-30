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

## Open question routed to BOSS, not to be answered by DOSING

The owner states a flow cell sits upstream of the injection ports and that a
no-circulation fault exists. How the Pi learns the loop is moving has not been
established. BOSS has not checked this against any device and is not asserting
that nothing exists. Interface S-13 is OPEN and nothing may be built against it.

## Waiting on

| From | What |
|---|---|
| PUMP-BOXES | Head barb form and size, F-05 and F-06. Lid penetration, C-05 |
| DISPLAY-BOX | Probe cable termination and length limits, S-11 |
| WATER | Union type at F-03 and F-04, and circulation pump flow through the manifold |

## Do not

Do not decide port count, manifold diameter, tubing size or jug volume from
memory. Counts come back when the requirement is known.
