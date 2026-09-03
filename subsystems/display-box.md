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

## YOU CONSUME THE CHANNEL TOKEN. Read channel-token.md.

Added 2026-08-30 after AUDIT found that this file contained no mention of the token
and spoke only of "eight drivers". Findings F-036.

**The eight tokens CH1 to CH8 are the ROW KEYS of the step and direction section of
the S-12 map.** The map is a table whose key column is the token and whose value is
whatever pin you assign.

**You must not invent:** a driver number, an output number or a channel index of
your own; a zero-based ordering; a renumbering so the pins come out tidy or
contiguous; or a token derived from bus enumeration order or board position.

**If the header forces a non-monotone pin order, the pins are non-monotone and the
tokens stay as they are.** The declaration names renumbering-for-tidiness as the
single most likely origin of this failure, because it looks like tidiness at the
time it is done.

**This reaches your fail-safe sweep as well: those sixteen rows are keyed by token,
not by output number.** T-013.

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
- **CLOSED by parts.md: EZO pH on one ISCCB-2, EZO EC on the other, EZO RTD on NO
  carrier.** pH and EC share a solution and must be isolated from each other; a
  resistance measurement has no solution ground path, so there is nothing to
  isolate.
- **The EZO circuits SHIP IN UART MODE, not I2C. Each must be manually switched
  with a jumper procedure before the Pi can see it, and the mode pin differs by
  circuit type.** Commissioning C-14, and it must happen before the box is closed.

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
  **Sharpened 2026-08-30: EN unwired leaves the 6121 ENABLED, so the driver's
  power-up default is on, not off.** Interface P-09.
- **The Pi is powered independently and nothing in the panel can power cycle it,
  so a watchdog is the only recovery path.** That is a display-box hardware
  question as much as a software one.
- **The box is NEMA 4X polycarbonate with a gasketed display cutout, so it offers
  no bonding path. Every equipment ground lands on a ground bar, not on the box.**
- Read traps.md T-006 and T-007 before drafting any coil drive. An open-collector
  device sinks and cannot source, and a remote open-collector driver needs a
  shared common back to the supply it switches against. The coils are in the main
  panel, 4 ft away, which is exactly the remote-board case.
- **F-011: the two contacts feeding this box, S-03 and S-08, are below the
  minimum switching load of the contacts that produce them.** An oxidised aux
  contact on S-08 fails intermittently, and an intermittently open readback either
  reports a welded contactor that is fine or misses one that is not.
- Box layout, heat, and screen reach, M-03.
- Whether the box provides a clock that survives a power cut. Raised by
  CONTROL-SOFTWARE 2026-08-30, which asserted nothing either way. All of its
  settle-window logic is interval arithmetic, and until this is answered any
  window spanning a restart must be treated as void rather than have an elapsed
  time computed for it that cannot be trusted. Adjacent to S-12.

## Assigned 2026-08-30: the fail-safe sweep, G-22 and D-036

Every failure of a sense path must read as the safe state. Two circuits have it by
design, S-08 and S-03. **Enumerate EVERY signal crossing the logic board in both
directions, inputs the Pi reads and outputs it drives, and for each one answer
what a severed cable reads as or does, whether that is the safe state, and what
safe means for that particular signal.** An input that reports a fault falsely is
safe. An output that energises something falsely is not. **An input that fails in
the unsafe direction is a defect, not a tolerance.**

Include the outputs. A severed coil drive is a different question from an input,
and a step or direction line to a driver whose EN defaults ENABLED is a third.

**EXTENDED 2026-08-30 by D-039: TWO COLUMNS PER SIGNAL.** The severed case is one
failure mode. **The other is a SHORT, and for outputs it is often the dangerous
one.** A severed step line stops a pump; a step line shorted to the 5 V rail
asserts it permanently, and with EN defaulting enabled that is a driver being
clocked or held by something other than the Pi. **The adjacent conductor in a duct
or a jacket is the realistic short, not ground in the abstract, so the answer must
say what each signal is actually next to.** This may confirm the pair and class
work rather than find anything, which is a fine outcome.

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

## OPEN, routed 2026-09-03 by D-098. PI 5 PAD DEFAULTS, FOR THE THIRD-CASE SWEEP.

Recorded in parts.md with its provenance. Read the provenance before you use the
numbers: **they are forum statements by Raspberry Pi engineers, not a datasheet.**

| Pins | Power-on state |
|---|---|
| GPIO0 to GPIO8 | pulled UP |
| GPIO9 to GPIO27 | pulled DOWN |
| Pad pull strength | about 50 k |
| **GPIO2 and GPIO3** | **held strongly HIGH by 1.8 to 2 k. Not a pad default** |

The rule that comes out of it, and it is the part that binds: **the HAT+
specification says fit an external resistor, so an external pull is authoritative
and the pad default is a fallback nobody designs against.** Every pin whose
power-on level matters gets its own external pull.

**GPIO2 and GPIO3 are excluded outright from any signal whose safe power-on state
is low.** That is a hard exclusion. A 1.8 k hold is not something an external
pull-down of any sane value argues with.

Apply this to the third-case sweep, both columns per signal as the owner asked:
what a SEVERED conductor does and what a SHORT TO ITS REALISTIC NEIGHBOUR does,
**now with a third column for what the pin does in the window between Pi power-on
and software taking the pin.** Do not state a pin number or a resistor value from
memory.
