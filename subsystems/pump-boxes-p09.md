# PUMP-BOXES on P-09: the permissive-drop state

Returned 2026-08-30, PUMP-BOXES' first invocation. Nothing decided, no file it
owns changed. Reported STOPPED PART-WAY and did not declare itself finished.

**No datasheet has been pasted.** PUMP-BOXES searched the tree: TMC2209 appears
only in project prose. Questions 1, 2, 3 and 6 are therefore unanswered BY DESIGN
rather than by omission, and come back as requirements and search terms.

## Two documents are needed, not one. This is T-015's exact shape.

1. **The TMC2209 chip datasheet.** Governs chip behaviour.
2. **The Adafruit 6121 board schematic and pinout.** Governs THIS part.

They are not interchangeable. parts.md gives the PRINTED pin list. **A silkscreen
name is a net name, not a chip pin name**, and T-015 records "wrong pin names" as
one of the six symptoms of the last substitution. **The mapping from printed VDD
to whatever chip supply pin it feeds is the first thing to establish**, because
the sequencing answer and the EN threshold answer are both stated against chip pin
names and are meaningless until that mapping is known. Also needed from the board
document: whether MS1, MS2 and EN have onboard pull resistors, and what the board
does to VM before it reaches the chip.

**One thing derivable now.** parts.md says "Printed pins, and this is the complete
list", and no UART or serial pin is on it. **So any status readable only over the
driver's serial interface is not readable on this build.** DIAG and INDEX are the
only status outputs available. The owner should confirm against the board photo
whether an unprinted pad exists; PUMP-BOXES did not assert beyond what that line
says.

## The state, restated so it is not softened

Eight drivers, logic supply present, motor supply absent, enable asserted, Pi
awake and possibly still clocking STEP. **Entered on every fault and every
shutdown, and left only by a human pressing a button at a moment the Pi does not
choose.**

**PUMP-BOXES added a case the question set did not name, and it is worse than the
steady state: VM RETURNS while EN is still enabled and STEP may still be
clocking.** The reset is manual and asynchronous to software. Whatever the
datasheet says about the static VM-absent condition, it must also be read for the
RE-APPLICATION TRANSIENT. Same search, one extra question.

## Q1, what the driver does with STEP asserted and VM absent

Requirement: a statement of behaviour when the logic supply is in range and the
motor supply is below its operating minimum, covering (a) whether the step counter
or sequencer advances, (b) whether the output bridge is driven, tri-stated or
undefined, (c) whether a flag is set, (d) whether that flag latches or is
transient, (e) whether the part self-clears when VM returns or needs a reset, and
(f) what the bridge does during the VM re-application transient with EN already
asserted.

Search the chip datasheet PDF for these strings. **If a string is absent, that is
itself information: report it rather than inferring.**

    undervoltage / under voltage / UVLO / lockout
    charge pump / uv_cp
    GSTAT / DRV_STATUS / reset / drv_err
    power up / power-up / power on reset / POR
    VS   (the chip's motor supply symbol - confirm from the pin table first)

Sections to read regardless of search hits: the absolute maximum ratings table,
the pin description table, the block diagram, and anything titled power supply,
power up or initialization. **Ask for figure and table numbers back, not a
paraphrase.**

## Q2, is it damaging

Two things PUMP-BOXES can say from the build, and one it will not.

**Can say:** there is no external source that back-drives the motor. A
three-roller peristaltic head with a squeezed tube is not turned by the fluid, and
the motor body is in a sealed box with nothing coupled to it but the head. So the
classic unpowered-driver, spinning-motor, back-EMF hazard has no energy source
here. One candidate mechanism removed.

**Can say:** the motor windings stay connected to 1A, 1B, 2A and 2B through the
drop. Whether an unpowered bridge presents a path from those terminals into a dead
VM rail is a datasheet and architecture question.

**Will not say:** whether the part tolerates logic-present, motor-absent
indefinitely. And a warning about a sentence already in parts.md: **"with VDD
unconnected the driver does not respond to STEP or DIR at all" is a statement
about FUNCTION, not about TOLERANCE.** Does-not-respond is not is-not-stressed,
and it addresses VDD absent, not VM absent. It must not be read as answering
either question.

Search: `absolute maximum ratings` verbatim, `ESD`, `latch-up`, `latchup`, `input
voltage` with the supply symbol, and the pin description rows for STEP, DIR and EN,
specifically **any note giving a maximum input voltage RELATIVE TO THE SUPPLY**,
because that clause decides this question and the mirror case in Q4.

## Q3, DIAG and INDEX

What must come back: what asserts DIAG and whether undervoltage is among it;
**whether DIAG's function is fixed or configurable** (search DIAG together with
stall - if it can be a StallGuard output rather than an error output, which it is
on this board is an Adafruit schematic question and possibly a register question,
and with no UART pin printed a register-selected function may not be selectable at
all); whether DIAG is push-pull or open-drain and its drive capability, which is a
wiring requirement owed to DISPLAY-BOX under S-10; what INDEX indicates and
whether it is derived from the step sequencer, in which case Q3 and Q1 are the same
question; and **whether either output is valid, driven or defined when VM is
absent. A fault output that is itself undefined in the state it would report is
not a detector.**

Search: DIAG, INDEX, diagnostic output, error output, open load, short to ground,
overtemperature, prewarning, stall, StallGuard, plus the pin description rows.

**What PUMP-BOXES could answer now, and it changes the value of DIAG.** The Pi
already has a designed witness to a permissive drop: the S-08 auxiliary readback.
It is frozen, it is hardware, and it does not depend on any driver. So DIAG is not
needed as the primary witness.

**But that witness has two open findings against it.** F-011: S-08 is below the
minimum switching load of the contact producing it, and an oxidised contact fails
intermittently. F-013: BOSS does not know whether the readback is a real auxiliary
block or the 22.32's second 25 A pole doing dry-circuit duty. **The system's one
witness to this exact state is doubly suspect.**

That makes a per-driver witness worth more than it first looks, and it is not
free: eight DIAG returns is eight more conductors up a 4 ft and a 6 ft cable, eight
more logic board inputs and eight more rows in the S-12 map. Per-box OR-ing to two
signals is cheaper and loses per-channel granularity. **A real cost decision across
S-10, S-12 and INTERCONNECT, and it must not be taken until Q1 and Q3 are
answered, because if DIAG does not report undervoltage the whole trade
evaporates.**

## Q4, where VDD comes from, and the boundary defect underneath it

**The real content of this question is a defect in a frozen row, reported not
fixed:**

> **G-09 as written does not distinguish the two supplies.** G-09 says the
> permissive "removes power from every stepper driver at once", and PUMP-BOXES'
> own frozen slice says driver power is removed for all eight with no local bypass
> ever. **Both were written when everyone believed a stepper driver had one
> supply. parts.md has since established there are two.** Whether VDD is "driver
> power" under G-09 decides whether a permanently-live VDD is a legitimate option
> or a violation of a frozen row. PUMP-BOXES cannot rule on it.

That is T-002's second method exactly: an external fact arrived and created a seam
the table had no words for. It is also T-015's signature.

| Option | For | Against |
|---|---|---|
| **A. VDD from the display box, on the same cable as STEP and DIR, not switched by the permissive** | The logic common that STEP and DIR are referenced to is guaranteed shared with the Pi by construction, which is T-007's requirement met by the same conductor that carries the supply. DIAG stays readable. One supply defines both the Pi-side output level and the driver-side input threshold, the cleanest answer to S-10 on a non-isolated CMOS interface | Makes the uncharacterised state permanent and universal: eight enabled drivers with logic up and motors dead, on every fault and every shutdown. **Arguably breaks G-09.** Puts eight drivers' VDD current down a 4 ft and a 6 ft run as a new load on the display box supply, and nobody has that current figure |
| **B. VDD derived on the load side of the permissive, so the permissive removes both** | A drop is a genuinely dead driver. G-09 stands in its plain words with no interpretation. The state ceases to exist | Deletes any driver-local witness, leaving S-08 alone with F-011 and F-013 against it. And it creates the mirror case: the Pi, still awake, drives STEP and DIR into inputs whose supply is gone. parts.md says the driver ignores them; it does not say the inputs TOLERATE them. **That is the pin-description clause from Q2 and it must be read before B is chosen.** If inputs must not exceed their supply, B needs series limiting, or the Pi's outputs held low through the drop, or both |
| **C. VDD regulated locally in each box from the switched VM** | Behaves as B | A new part, a new heat source inside a sealed box C-15 has not measured, two more failure points, and a locally-referenced logic supply, **which is where T-015's two-returns-on-one-pin, parallel return path and ground loop came from last time** |

**True in every option, and the part PUMP-BOXES is most confident of:** the Pi's
logic return and the driver GND must be common **by a single defined path**, and
that path must exist regardless of which supplies are present. The boxes are
plastic and every equipment ground lands on a ground bar, so **the return is a
conductor somebody has to draw, not something the enclosure provides.** T-007 is
the failure where both ends land correctly and nothing flows. **If VM's return and
the logic return are separate conductors that meet at the ground bar and again at
the driver's GND terminal, that is a loop, and it will be reported as a ground
problem rather than as this decision.**

PUMP-BOXES did not pick. P-09 is OPEN, joint, and turns on four datasheet answers
plus one ruling on G-09's scope that is not its own.

## Q5, EN

**EN must be wired.** Not should. parts.md says unwired leaves it enabled, and
G-06's frozen slice says the box must survive the case where software does not
enforce one-at-a-time. An unwired EN means the box's only protection against a
stuck or floating STEP is software, which is the thing G-06 says not to rely on.

**Its power-up state, before any software runs, must be DISABLED, held there by
hardware.** DISPLAY-BOX has the matching open item already.

Not guessed: which electrical state is the disabled one, what threshold defines
it, whether that threshold is referenced to the logic supply. Search the pin
description row for EN, and confirm the chip's name for it - EN, ENN and enable
are all worth searching, and **if the chip pin name carries an inversion the board
silkscreen may not**. Plus enable, input logic levels, V_IH, V_IL.

**The trap, which does not need the datasheet to see: if EN is held disabled by a
passive pull, that pull must be referenced to the supply that defines the input's
threshold. If it is referenced to a supply that can be absent while the driver is
otherwise alive, there is a window in which the pull is dead and the input is
floating, which returns you to enabled-by-default at exactly the wrong moment. So
Q4 and Q5 are ONE question: EN's hold and VDD's origin are decided together.**

**Two consequences found by reading commissioning.md in full:**

- **C-13 changes meaning.** It measures standstill current, assumed at 30 percent
  of running. **If idle drivers are held disabled by EN, standstill current is not
  that figure at all.** C-13 must state the EN state it was measured in or it is
  not a number. C-15 has the same dependency: "three idle at standstill current"
  is a different thermal load if idle means disabled.
- **C-06 changes meaning, and this one is a genuine conflict.** C-06 asks whether
  the head holds against back-siphon with the jug above the inlet. **A de-energised
  stepper holds differently from an energised one. So an EN policy of "disable
  everything not dosing" is not a free safety improvement: it may remove the
  holding torque C-06 is about to test for.** That coupling is DOSING's and
  PUMP-BOXES' jointly and it was on no row.

Also open: **per-channel EN or one EN per box.** One per box is four fewer
conductors per cable and matches G-06; the cost is that disabling is no longer
per-channel, so a stuck STEP on one channel is not contained by disabling another.
An S-10, S-12 and INTERCONNECT decision. Note that **if EN is per-box then EN is a
BOX attribute and not a channel attribute, and nothing in software may treat it as
per-channel.**

## Q6, sequencing

Requirement: whether the two supplies may arrive and depart in any order, or
whether one must lead. Search: sequence, sequencing, power up, power-up, power
down, VCC_IO, VDD, VCC, and any note attached to the supply pins.

**The question most likely to be answered wrongly by the wrong document.** The
chip may state its requirement in terms of pin names the board does not expose or
has tied together. Establish the printed-VDD-to-chip-pin mapping FIRST, then read
the chip's sequencing statement against it. **A sequencing rule between two chip
pins the board has bridged is not a constraint on this build. A rule between two
pins the board brings out separately is one, and it directly decides A, B and C.**

## MS1 and MS2

No value stated. What PUMP-BOXES needs before it can set one:

1. The microstep table from the chip datasheet: which combinations select which
   factor, and what the pins select when left open. Search MS1, MS2, microstep,
   MRES, microstep resolution, interpolation, MicroPlyer. **The interpolation
   question matters: if the part internally interpolates to a fixed resolution
   regardless of the pins, then MS1 and MS2 select the INPUT step scale and not the
   motor's real resolution, and CONTROL-SOFTWARE's arithmetic means something
   different.**
2. Whether the 6121 has onboard pulls on MS1 and MS2, from the schematic. **Unwired
   is a setting, not an absence**, and C-17 cannot record what unwired means until
   this is known.
3. **The KPHM400-ST's full steps per revolution.** parts.md does not give it.
   PUMP-BOXES checked. It is a Kamoer lookup and it is the other term in C-17's
   arithmetic.
4. From DISPLAY-BOX and CONTROL-SOFTWARE via S-10: the maximum reliable STEP rate
   the logic board can generate over 4 ft and 6 ft, and the smallest dose volume
   software needs to command. **A microstep factor chosen alone can exceed a pulse
   source PUMP-BOXES does not own.**
5. Minimum STEP pulse width and maximum step frequency. Search STEP in the timing
   section, t_SH, t_SL, step frequency, timing diagram.

**The trade.** Finer microstepping gives smoother, quieter motion and a smaller
dose quantum, since the smallest commandable dose is one step's worth of volume.
Against: proportionally higher step rate for the same rpm, more demand on the pulse
source and cable, and the part people get wrong, **microstep positional accuracy
does not improve in proportion to the factor**, so a finer setting does not mean
proportionally finer DELIVERED volume. Under G-04 nothing measures delivered
volume, so an over-fine setting buys resolution that is invisible and unverifiable.

**The dominating cost is not electrical.** Changing MS1 or MS2 later re-runs C-17
and VOIDS C-01 for that channel, and C-01 is a per-channel physical calibration
against real back pressure. **Set once, before C-01, identically on all eight,
recorded, and never touched.**

## The 6121's VM range, for F-010

Search: Adafruit 6121 TMC2209 stepper motor driver breakout, then motor voltage,
VM, input voltage range, power. Chip datasheet: absolute maximum ratings, VS,
operating supply voltage, motor supply voltage.

**The instruction that matters more than the terms: the number that governs is the
BOARD's stated maximum, not the chip's.** A breakout's ceiling is usually set by
its onboard capacitor ratings or a regulator and is commonly below the chip's. **If
the two documents disagree, the lower one is this build's limit.**

**And check against the worst case, not against 24 V.** The rail is settable to
28.28 V and OVP does not trip until 29 V, **so the highest voltage the drivers can
see without any protection operating is 29 V.** If the board's maximum sits below
28.28 V, the finding is not "set the trim carefully", it is that **nothing
currently prevents someone setting it out of range**, and that goes back to
MAIN-PANEL and BOSS.

## What CONTROL-SOFTWARE needs from PUMP-BOXES and cannot have yet

1. The microstep factor.
2. Whether EN exists as a usable control, at what granularity, and its polarity.
   This decides whether software can positively disable a driver at all and whether
   a hardware-safe state exists at boot.
3. Whether any per-driver fault signal will reach them, and how many: zero, two or
   eight. Depends on Q1 and Q3.
4. The characterisation of the permissive-drop state. **Until P-09 closes,
   PUMP-BOXES cannot tell them stepping into a drop is harmless and cannot tell
   them it is reported. They must not assume either.**
5. A flag on CONTROL-SOFTWARE's own bookkeeping, named rather than answered:
   **during a VM-absent window, commanded steps are known-not-delivered.** Under
   G-04 and G-05 the books record commanded volume. What that means for a jug
   decrement across a permissive drop is theirs.
