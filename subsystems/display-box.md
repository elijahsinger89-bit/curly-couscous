# DISPLAY-BOX

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

The display enclosure and its contents: Raspberry Pi 5, 7 in touch display,
three Atlas Scientific EZO circuits on two ISCCB-2 carriers, and the hand-built
logic board. The logic board is the whole electrical interface between the Pi's
3.3 V world and everything else: relay coil drives, permissive coil drive,
permissive auxiliary readback input, the day tank fill dry contact input, and
step and direction outputs to eight drivers. Box layout, mounting, cooling,
screen position and operator reach.

Ends at the logic board terminals and the box glands.

## Out of scope

The Pi application. That is CONTROL-SOFTWARE, and the seam between you is S-12,
the pin and address map. Relays, contactors and the permissive chain are
MAIN-PANEL. Probe wet fitting and placement are DOSING. Cable runs are
INTERCONNECT.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| G-09 | The Pi drives the permissive coil and reads back an auxiliary contact. The readback exists to catch a welded contact, so it must reflect the contactor's real state, not the Pi's command |
| G-02 | The only level signal into this box is one dry contact, day tank fill in progress |
| G-07 | Nothing on the logic board can hold the permissive chain closed. Software cannot defeat a leak, an E-stop or a lost interlock |
| S-12 | The pin and address map is written down and frozen before CONTROL-SOFTWARE builds against it. It does not live in your head |

## Settled

- Pi 5, display, three EZO circuits and two ISCCB-2 carriers are bought.
- EZO circuits are read over I2C.
- Three EZO circuits sit on two carriers, so one carrier holds more than one.
  Confirm the addressing consequence from the ISCCB-2 datasheet the owner
  supplies. Do not assume it.

## Open, owned by DISPLAY-BOX

- The GPIO and I2C map, S-12. Propose it, write it into this file, and hand it
  to CONTROL-SOFTWARE to build against. It is not frozen until BOSS says so.
- Output stage for each relay and contactor coil drive: what the Pi can drive
  directly and what needs isolation, given the coils are MAIN-PANEL's.
- Input conditioning for S-03 and S-08, both dry contacts coming from another
  enclosure over a wall cable.
- Step and direction output form for eight drivers over a cable run, S-10:
  levels, drive capability and noise immunity.
- Power into this box, P-07, and whether the Pi is fed from the NDR-240-24 or
  separately.
- Behaviour of every output at Pi power-up and during boot, before software
  runs. Nothing may pull in a relay or step a driver because a pin floats.
- Box layout, heat, and screen reach, M-03.
- Whether the box provides a clock that survives a power cut. Raised by
  CONTROL-SOFTWARE 2026-08-30, which asserted nothing either way. All of its
  settle-window logic is interval arithmetic, and until this is answered any
  window spanning a restart must be treated as void rather than have an elapsed
  time computed for it that cannot be trusted. Adjacent to S-12.

## Waiting on

| From | What |
|---|---|
| MAIN-PANEL | Coil voltage and current for each drive, aux contact form, dry contact form |
| PUMP-BOXES | Driver step and direction input requirements from the 6121 datasheet |
| DOSING | Probe cable length and routing, S-11 |
| CONTROL-SOFTWARE | Which signals it actually needs, before the map is frozen |

## Do not

Do not state a pin number, an I2C address, a resistor value or a part number
from memory. The Pi 5 header and the EZO addressing come from the owner's
datasheets, not from recall.
