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

## Facts arrived 2026-08-30, read parts.md before anything else

The heads are Kamoer KPHM400-ST: head, motor and stepper in ONE unit, panel-mount
flange, **motor body INSIDE the box and head OUTSIDE it**. That is why the boxes
are sealed and the heads are not. Boxes are 16 by 8 by 6 in and already owned.

The drivers are Adafruit 6121, screw terminals, non-isolated CMOS, pins STEP DIR
EN MS1 MS2 DIAG INDEX VDD GND VM 1A 1B 2A 2B. **No differential pairs, no opto.**
VDD is a separate 3.3 to 5 V logic supply and the motor terminal block does not
generate it; with VDD unconnected the driver ignores STEP and DIR entirely. **EN
unwired leaves the driver ENABLED.** Vref pot set with a meter before power. Each
driver needs a stick-on heatsink. 1.0 A per driver.

Read traps.md T-015 before drafting anything for these drivers. The exact failure
it records is designing for an opto-isolated differential driver and buying a
non-isolated CMOS breakout.

## Open, owned by PUMP-BOXES, added or sharpened 2026-08-30

- **MS1 and MS2: the microstep setting.** Searched every markdown file: no file
  states a value and nobody has assumed one. Set it, then it is recorded at C-17,
  then CONTROL-SOFTWARE uses it. In that order. Steps per millilitre is motor
  steps per revolution times this factor divided by ml per revolution, so this is
  an input to somebody else's arithmetic and not a local choice.
- **Where VDD comes from, and whether the permissive removes it.** Interface P-09,
  new and open. The permissive contactor removes VM. It does not by itself
  de-power the logic side. Both cases must be reasoned about explicitly: VM
  present with VDD absent, and VDD present with VM absent.
- **EN default-enabled.** The power-up default is on. What that means for the
  moment power arrives, before software runs, is a real question and it is shared
  with DISPLAY-BOX.
- **The 6121's VM range, from the datasheet the owner pastes.** The rail it sits
  on is settable from 23.76 to 28.28 V with nothing fixing the trim, F-010.
  Nobody has stated whether that is inside the part's range and BOSS will not
  state it from memory. This blocks P-06.
- **Mechanical load: about 304 g per unit, eight of them, hanging through two
  plastic lids.** Lid stiffness, the panel-mount face as a sealing surface, and
  box mounting to the wall. The owner attributed this to WATER; the lids and boxes
  are PUMP-BOXES', and the wall is INTERCONNECT's.
- **Thermal, C-15.** Four motor bodies and four drivers in one sealed plastic box.
  G-06, one pump at a time, is a THERMAL constraint and the only thing that could
  ever relax it is that measurement.
- **The pump tube is NOT yours.** Interface F-10 closed by D-028: DOSING owns it,
  including the change interval and procedure. Your head is a mechanical mount
  that happens to have a tube in it, and you stop at the barb per D-006. What you
  do owe DOSING is whatever the head requires of a tube change: access, clearance,
  and whether the box must be opened to do it.

## P-09 answered as far as the project's own facts reach, 2026-08-30

subsystems/pump-boxes-p09.md. Q1, Q2, Q3 and Q6 are unanswered because no
datasheet is in the tree, and PUMP-BOXES returned requirements and search terms
instead of guesses. Q4 and Q5 are answered to the edge of what is known and both
are gated on the same two documents plus one ruling that is the owner's: whether
VDD falls inside G-09's word "power", findings F-014.

**Two documents are needed, not one: the TMC2209 chip datasheet AND the Adafruit
6121 board schematic. A silkscreen name is a net name, not a chip pin name.**

## Previously open, now closed by parts.md

- Head barb form and size: 3/16 in straight connector mating 4.8 mm ID tube. F-05
  and F-06 are closed on size.
- Motor requirement: there is no separate motor. It is one unit.
- Driver current: 1.0 A per driver, 71 percent of the part's rating.

- Driver supply voltage and the current each driver draws, from the 6121
  datasheet the owner supplies. P-06 is blocked on this.
- Motor requirement for the heads: what each head needs to turn against its
  own load. Return a requirement and a search term. Do not pick a motor.
- Driver current is set by the Vref pot. **RETRACTED 2026-09-01: the reinforcement
  that there is no printed UART pin is VOID. UART is JP4 pin 9 to PDN_UART, so a
  serial route exists.** The pot may still be the chosen method; the reason given for
  it is gone. And the "before any power" half is unexecutable, F-061.
- Enclosure heat with four drivers in a closed plastic box, and whether the box
  needs venting given the room is 62 to 65 F and under 60 percent humidity.
- Head barb form and size, returned to DOSING for F-05 and F-06.
- Lid penetration and sealing for the heads, CBL-05.
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

## OPEN, routed 2026-09-03 by D-096. THE DIR LEVEL REVERSED.

You said no datasheet could close the noise half and you named the three numbers
that would close the level half. The owner returned them and **the level went the
other way from what D-069 recorded.**

| Quantity | Value |
|---|---|
| DIR internal pull-down | 132 k min, **166 k typical**, 200 k max |
| STEP internal pull-down | **NONE.** Pin type is DI with no (pd) |
| VINLO max | **0.30 x VCC_IO**, so 0.99 V at 3.3 V |
| VINHI min | **0.70 x VCC_IO**, so 2.31 V at 3.3 V |

**A FLOATING DIR FLOATS HIGH.** The 20 k plus green LED branch to VDD beats a
166 k internal pull-down by an order of magnitude.

Three things follow and all three are yours:

1. **The external pull-down is now load-bearing for the LEVEL, not only for the
   hold.** Size it against 166 k typical in parallel AND against the 20 k plus LED
   branch pulling the other way, to a pin voltage below VINLO. **It is no longer a
   leakage-scale question and every prior sizing discussion assumed it was.**
2. **G-29's convergence on DIR is broken again.** Severed goes HIGH by the board.
   Shorted to a return-paired neighbour goes LOW. Opposite once more, which is the
   condition D-049 and G-22 called unsafe in both directions. Say what the pairing
   should now be, or say that pairing can no longer deliver convergence here.
3. **STEP has no chip contribution at all.** Your F-060 question is unchanged in
   substance and now better founded than when you asked it.

Return a requirement and a search term for anything you do not have. **Do not
state a resistance value from memory and do not fit a pull-up on your own
initiative** - D-062 is still the owner's gate and its question has flipped to
"is DIR HIGH the safe rotation".
