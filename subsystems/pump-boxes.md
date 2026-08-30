# PUMP-BOXES

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

Two plastic boxes on the dosing wall. Four peristaltic pump heads and four
Adafruit 6121 TMC2209 breakouts in each. Head mounting through the lids and the
lid penetrations. Internal wiring, driver power distribution, step and direction
landing, driver current setting hardware, heat and enclosure ventilation, box
mounting.

Ends at the box glands and at the head barbs.

## Out of scope

Everything wet: tubing, jugs, priming, chemical compatibility. That is DOSING.
The permissive contactor is MAIN-PANEL. The step and direction source is
DISPLAY-BOX. Cable runs are INTERCONNECT.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| G-09 | Driver power arrives through the permissive contactor and is removed for all eight drivers at once. There is no local bypass of it, ever |
| G-06 | Only one head turns at a time. Software enforces it, but the box must survive the case where it does not |
| D-006 | PUMP-BOXES ends at the head barb. The tubing and jugs belong to DOSING |

## Settled

- Two boxes, four heads and four drivers each, heads through the lids.
- Eight heads and eight 6121 breakouts are bought.
- Room is 62 to 65 F, under 60 percent humidity.

## Open, owned by PUMP-BOXES

- Driver supply voltage and the current each driver draws, from the 6121
  datasheet the owner supplies. P-06 is blocked on this.
- Motor requirement for the heads: what each head needs to turn against its
  own load. Return a requirement and a search term. Do not pick a motor.
- Driver current setting method on the 6121 and whether it is set in hardware or
  over the driver's own interface.
- Enclosure heat with four drivers in a closed plastic box, and whether the box
  needs venting given the room is 62 to 65 F and under 60 percent humidity.
- Head barb form and size, returned to DOSING for F-05 and F-06.
- Lid penetration and sealing for the heads, C-05.
- Wall position relative to the manifold, M-02, jointly with DOSING.
- How the two boxes divide the eight channels, and whether both boxes take one
  cable each or share one. Coordinate with INTERCONNECT, do not decide alone.

## Waiting on

| From | What |
|---|---|
| MAIN-PANEL | Permissive contactor load side conductor and voltage, P-06 |
| DISPLAY-BOX | Step and direction signal form, levels and drive capability, S-10 |
| DOSING | Tubing outside diameter at the barb, and whether the tubing route sets head orientation |
| INTERCONNECT | Cable entry side and gland positions |

## Do not

Do not state a motor part number, a current setting, a step count per millilitre
or a wire gauge from memory. Do not assume a head calibration figure: nothing in
this system measures delivered volume, so a wrong figure is invisible.
