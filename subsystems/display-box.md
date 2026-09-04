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

---

## 2026-09-04. P-07's FORM AT THE DISPLAY BOX END. ANSWERED BY DISPLAY-BOX.

**Asked because INTERCONNECT declined to spend face width on the one gap that carries
a named failure, and was right to decline.** cable-and-terminal-schedule.md 2.3: the
allowance has a prior claim on it from an expected split under F-030, and committing
an allowance before the step that consumes it is known is T-020's shape. Its item 4
offers a cheaper resolution - that the LINE entry stops being an entry - and routes
the call here.

**What I read to answer it:** agents.md rules 1 to 11 and BOSS's working rules; this
file; entry-faces.md sections 3.1 to 3.3 and 5; parts.md on the display box enclosure,
on the Pi being powered independently, and on the 5 V rail feeding VDD; interface-table
rows P-07, P-09 and CBL-03; D-046, D-047, D-049, D-092, D-146; F-019, F-030; T-020;
G-26, G-44; and cable-and-terminal-schedule.md rows RUN-006, RUN-007, RUN-008, RUN-009
with section 2.3.

---

### 1. THE FORM

**A CABLE ENTERING THROUGH A GRIP IN THE BOTTOM FACE, LANDING INSIDE THE BOX ON THE
BACK PLATE. NOT A CORD CAP INTO A RECEPTACLE IN THE BOX FACE.**

**No receptacle goes in any face of this box.**

### 2. THE REASON FROM WHAT IS INSIDE MY BOX

**2.1 P-07 already has its cord cap, and it is at the other end.** The frozen row's
End A is "MAIN-PANEL: fused, NOT relay switched receptacle". **D-046 is already
satisfied by that receptacle.** D-046's sentence is about the panel's own face: the
receptacles are panel mounted and the cords plug into them from outside. **It settles
what the SOURCE end does with a cord. Reading it as a rule for every face turns a
decision about one enclosure into a decision about four**, and this box was not in it.
**A second cap at my end does not honour the precedent twice. It puts a second
disconnecting means on the one supply in this build that must never be switched.**

**2.2 What that supply is for, from the frozen rows.** P-07: the Pi has power whenever
the panel does, stays alive through a permissive drop, and **nothing in the panel can
power cycle it, so a watchdog is the only recovery path.** P-09: the 5 V rail in this
box is the Pi's own supply and is **UNSWITCHED**, and it leaves this box as VDD to
eight drivers in two boxes. **A plug in my face sits upstream of both.** It is a
disconnect that a knee, a service pull on the cord, or its own weight can operate, on
a supply whose whole stated property is that nothing operates it.

**2.3 And the loss would be silent.** G-26: the panel runs without the Pi, so the water
system keeps running and only dosing stops. **An unplug at my face is a power cycle
nothing commands, nothing observes and nothing logs**, on the one node whose recovery
path is a watchdog that is also unpowered. **The gland form has no such device to
fail.** A grip clamps the jacket; a cap is held by friction.

**2.4 The box is opened as a build step and as a service step.** C-14 switches each EZO
circuit from UART to I2C by a jumper procedure before the box is closed, and the mode
pin differs by circuit type. **Every landing in this box is on the back plate.** A
glanded cable lands with them. A face receptacle is a live LINE terminal set in the
region behind the face, present and energisable while the box is open for a procedure
that is on the commissioning list.

### 3. THE REASON FROM D-047's SHED PRINCIPLE, AND IT CUTS AGAINST THE CHEAP ANSWER

**D-047 and D-092 are the same principle stated twice: the design sheds rather than
seals, and the assembly's rating is set by its WORST penetration regardless of what is
fitted above.** D-092's reasoning names what the worst penetration was on the main
panel, in its own words: five upward-facing holes **and four receptacles whose cord
caps do not seal.**

**So the tree's own position is that a receptacle with a cord cap in it is a
non-sealing penetration.** The main panel accepted being unrated as assembled because
it already had five of the other kind. **This box has none.** Its only device
penetration today is the gasketed display cutout, and entry-faces.md 3.2 already calls
that the youngest part in the assembly under D-092's argument. **Putting a receptacle
in this face imports the main panel's unrated-as-assembled condition into a box that
does not currently have it, to save face width.** That is the trade running backwards.

**And it has an orientation, which the question asked me to say plainly rather than
dodge.** Rule 1 of entry-faces.md leaves this box exactly one entry face, the bottom.
**A receptacle there faces DOWN.** The cap is inserted upward and then retained against
its own weight and the weight of the cord by friction alone, on the one supply that
must never open. A grip on that same face clamps. **The bottom face is the right face
for a grip and the wrong face for a plug, and there is no other face to move the plug
to** - the front is the display and the face that opens, the back is the wall, and the
top and sides are rule 1 and B-16.

### 4. THE CORRECTION THAT MATTERS, REPORTED AND NOT FIXED, PER RULE 2

**The receptacle form does not remove LINE from this face, so it does not remove the
named failure.** cable-and-terminal-schedule.md 2.3 item 4 expects that it would. It
does not, and the reason is inside my box rather than on the face.

**LINE has to reach whatever makes the 5 V rail, and that is inside this box under
P-09.** A receptacle in the face is fed from LINE terminals on its back, in the same
band of the same face, with the same neighbours. **It is a larger penetration than a
grip, not a smaller one, and its conductors are BARE of their jacket at the point where
they are closest to entry 7.** A glanded cable keeps its conductors inside a jacket all
the way to its landing. **D-049's short case and F-019's are about what a LINE
conductor is next to. Swapping the hole's hardware changes neither.**

**Grade, per rule 10: CURRENT.** What would change it: the AC-DC conversion mounting
OUTSIDE this box, so that what crosses my face is a low-voltage cord and the LINE class
leaves the face entirely. **That is the only move that actually removes the named
failure, it is not the receptacle, and it is mine.** See section 7.

**Consequence for INTERCONNECT, stated so it is not waited on:** the gap between entry
7 and entry 8 survives this answer. **Spacing is still the remedy and it is still
INTERCONNECT's.** What this answer does is take P-07 off the list of things that
spacing waits on. **It now waits only on F-030.**

### 5. WHAT IT DOES TO THE ENTRY ORDER: NOTHING

**The order in entry-faces.md 3.3 is unchanged. RUN-009 remains entry 8 of 8, at the
right end, LINE, as far from the probes as this face allows.**

Both rules that generated the order are untouched. Rule A is a susceptibility ramp with
Pi power at the far end, and this answer keeps Pi power as an entry at the far end.
Rule B holds RUN-005 and RUN-006 apart with RUN-007 and RUN-008 in the gap, and nothing
here moves any of the four. **The face was already stated for the Pi's supply however
it is provided, and it did not need restating.**

### 6. WHAT IT COSTS, G-44, ON ALL THREE

**Under G-44 the burden is on the addition, and the addition here is the receptacle:
this box has no device in any face except the display cutout. The burden is equally on
a change made because it is cheap.**

| | **Grip and cable, chosen** | **Receptacle and cap, refused** |
|---|---|---|
| **What failure does it prevent** | It is the incumbent, not an addition. It carries no burden | **None is named.** It was proposed to save face width, and the width it would save is not yet established as needed: the spacing is unspent and waits on F-030 |
| **BUILD** | One more grip on a face that already takes seven. No new class of part, no new hole shape, no orientation to get right | A device in the face, its own opening, its orientation, and LINE terminals behind the face that must be dressed clear of entry 7. Plus a cap fitted at my end of the cable |
| **OPERATE** | Nothing to operate. That is the point: P-07 says nothing may power cycle the Pi | A disconnect at the unwatched end of the one unswitched supply, upstream of the Pi AND of the VDD rail to eight drivers. Its failure mode is silent under G-26 |
| **REPAIR** | The cable lands on the back plate with every other landing. The box opens for C-14 with no live face device inside it | It is one part that can be unplugged for a swap, which is the only real win and it is small. Against it: a second seal of the class D-092 calls non-sealing, on a box whose only other one is the display cutout |

**Two answers both work at the face. G-44 is the tie-breaker and it points at the
simpler one, which is also the incumbent.**

### 7. WHAT I HAVE NOT ANSWERED, NAMED RATHER THAN LEFT IN ABSENCE

**Where the AC-DC conversion for the Pi physically mounts is not stated anywhere I
read.** I looked at parts.md's "The Pi is powered independently of everything else"
section and its enclosures table, at interface-table rows P-07 and P-09, and at
RUN-009 in the schedule. **P-07 closed WHETHER the Pi is fed separately. It did not
state WHERE the conversion happens**, and this file still carries "power into this box"
as open.

**It matters and it is mine, because it decides the CLASS of entry 8, not its form.**
Conversion inside the box means LINE crosses my face. Conversion outside means a
low-voltage cord crosses it and the LINE class leaves this face for good, which is what
INTERCONNECT was hoping the receptacle would do.

**I state no part and no number for it, per rule 3.** What settles it: the form the
Pi's supply is actually bought in, and whether the 5 V rail can be regulated where it
must be, given P-09 exports that same rail to both pump boxes over a wall run.
**Requirement and search terms on request. I will not guess it, and it does not block
the answer above** - the entry is a cable through a grip either way, and only its class
is in question.

### 8. STATUS

**Finished as a unit of work, and not self-declared finished per rule 7.** The form is
stated, the entry order is unchanged, and RUN-009's provision cell can be filled at my
end: a cable that lands inside this box, so it has a TRM- landing point here whatever
the panel end is called. **The panel end is MAIN-PANEL's and D-046 already settled it.**

**Nothing above states a dimension, a gland size, a gland count, a position, a spacing,
a part number or a rating.**
