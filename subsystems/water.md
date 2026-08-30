# WATER

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

Tap connection. Fill solenoid as a device, its placement and its plumbing.
100 gal cone bottom storage tank. All float switches in the system: which
floats, what type, pilot duty rating needed, and exactly where each one sits in
each tank. Anbull transfer pump and its plumbing. 40 gal day tank. Both
hi-flow submersibles as devices and their placement. All day tank penetrations
and hangers. The JBJ Arctica DBE-200 chiller and the whole chiller loop
plumbing. The manifold return drop back to the day tank. Physical placement of
the leak detection sensors and of the dry run sense element.

Ends at V3 and at the manifold unions F-03 and F-04.

## Out of scope

Anything electrical past the device: relays, contactors, the permissive chain,
receptacles, coil wiring. Those are MAIN-PANEL. Cable routing on the wall is
INTERCONNECT. The manifold itself and everything on it is DOSING.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| F-09 | Day tank outlet to V3 is the scope boundary. V3 is manual. Nothing downstream is designed here |
| G-03 | Fill control is a start float and a stop float with relay seal-in between them, both tanks |
| G-01 | Floats are hardwired to relays and invisible to the Pi |
| G-11 | Circulation submersible takes suction at the day tank bottom so the tank mixes |
| G-12 | Chiller and its loop pump are switched together on one contactor |

## Settled

- Tanks, pumps and chiller are bought and listed in decisions.md.
- Both tanks are open top.
- Room 62 to 65 F, under 60 percent humidity, not wet.

## Open, owned by WATER

- Fill solenoid requirement: coil voltage, port size, connection type, and
  whether it needs to hold closed on loss of power. Return a requirement and a
  search term. MAIN-PANEL cannot size the relay contact until this comes back.
- Which floats, their pilot duty rating, and their placement in both tanks.
- Dry run sense element: what it senses. Interface S-05 is blocked on this and
  MAIN-PANEL cannot wire the interlock without it.
- Leak sensor placement: where water can reach the floor or a wall.
- Chiller loop flow requirement against the DBE-200 datasheet, and whether the
  second submersible meets it.
- Day tank penetrations and hangers, including how both submersible cords and
  the return drop pass.
- Return drop must break the siphon path back to the tank. Confirm how.

## Assigned 2026-08-30: findings.md F-003, primary owner

Nothing in this system verifies anything at rest. Between batches the loop is
still and EC sits flat whether the circulation submersible is healthy or dead.
The first anyone knows is at the start of the next batch.

WATER holds this because it owns the circulation submersible, the day tank and
the placement of any sense element. MAIN-PANEL holds the other end because it
owns the relay and the dry run interlock chain. Neither may assume the other has
it. See decisions.md D-016.

BOSS's note, not a design instruction and not a conclusion: this sits next to
S-05, where WATER already owes what the dry run interlock senses. Whether at-rest
circulation verification and dry run protection are one question or two is for
WATER and MAIN-PANEL to answer. BOSS has not checked and is not assuming.

## Waiting on

| From | What |
|---|---|
| DOSING | Manifold inlet and outlet union type and orientation, F-03 and F-04 |
| MAIN-PANEL | The contact duty and terminal each float chain lands on, S-01 and S-02 |
| INTERCONNECT | How field cables leave the wet area |

## Do not

Do not add jug floats or dosing line flow meters. See decisions.md G-04 and
G-05. Do not set pipe size, tank fitting size or pump counts from memory.
