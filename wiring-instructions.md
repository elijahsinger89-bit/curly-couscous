# D4. Wiring instructions

**A page per enclosure. Issued 2026-09-05.**

**This is a VIEW of D5, wiring-schedule.md, and nothing on it is a fact of its own.**
Every conductor id, landing, function, label and fail note below comes from a CDR- row
there. **D4 and D5 cannot disagree, so no rule is written here saying they must.**
G-45.

**Who holds this.** The person with strippers in hand, at the bench, working one
enclosure at a time. **Take the page for the box in front of you and nothing else.**

**Why a page per enclosure and not a page per wire.** D-171. A conductor is one
conductor and it spans the gland; it appears on the page of each box it lands in, with
its far end named as context. **So one joint gets one instruction, and you never hold
two pages to land one wire.**

**Nobody may land anything from this yet.** Every row below carries at least one
blocked cell and says what it is. Section 10.

---

## 0. THE STANDING JOINT STEPS

**These four repeat at the top of every page and they are the same every time.** They
are steps, not quantities, and under G-41 steps repeat in full because you may be
holding one page and no others.

1. **Write the label on BOTH ends of the conductor before you land either end.** The
   label is in the row. **A conductor labelled at one end only is worse than one
   labelled at neither, because it looks done.**
2. **Land it at the terminal NAMED in the row.** Never at a terminal counted by its
   position in a list. If the row says the terminal is not yet named, do not land it -
   see step 4.
3. **Tick the conductor off on D5**, the schedule, not on this page.
4. **If a cell in the row says BLOCKED, stop at that joint and leave it.** Do not
   substitute, do not pick a likely terminal, and do not tick it. **Move to the next
   joint on the page.**

**And the joint you do NOT do on this page:** where the row names a far end in another
box, that end is landed on that box's page. **One joint, one instruction.**

---

## 1. PAGE ORDER, AND WHY

**No file states the order the enclosures are wired in, so this is INTERCONNECT's and
here is the reason.** Inside the main panel the order follows D2's rungs, top to
bottom, which is the old set's "build left to right, top to bottom" and which this
build has no reason to differ from. **Across the boxes: the main panel first, because
every jacket but two has an end in it and the single-point ground bar is there; then
the display box, which is the other end of most of them; then the two pump boxes,
which are ONE BUILD and not a mirrored pair, so they are done back to back with the
same page shape; then the field.**

| Page | Rows |
|---|---|
| **1. MAIN PANEL** | 42 |
| **2. DISPLAY BOX** | 34 |
| **3. PUMP BOX A** | 7 |
| **4. PUMP BOX B** | 7 |
| **5. DAY TANK STANDPIPE** | 8 |
| **6. STORAGE STANDPIPE** | 8 |
| **7. FILL SOLENOID** | 3 |
| **8. LEAK CONSOLE** | 2 |

**Eight pages, 111 rows, for 64 conductors.** The difference is the spanning ones:
they are landed twice and instructed twice, once on each page, and they are still one
conductor with one id.

---

## PAGE 1. MAIN PANEL

**Entry face: BOTTOM.** Every cord grip is on the bottom; nothing but the five 22 mm
devices penetrates the top. **A drip loop goes outside the box at every grip.**

**Standing joint steps: section 0. Do them on every row.**

**One thing about this page before you start: THE GROUND BAR IS THE SINGLE POINT AND
NOTHING BONDS ANYWHERE ELSE.** If you find a convenient screw, do not use it. The bar
is the last group on this page and every green conductor in the build ends there.

### 1a. Supply, D2 rung 01 to 02

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-042 | **BLOCKED, F-106**: main panel line input, terminal not named | The building branch circuit | Supply, line | CDR-042 | **No disconnecting means is named anywhere in this build.** Do not assume the branch breaker is it |
| CDR-043 | **BLOCKED, F-106**: neutral, terminal not named | The building branch circuit | Supply, neutral | CDR-043 | |
| CDR-044 | **BLOCKED, F-106**: the ground bar | The building branch circuit | **The system's equipment ground, arriving at the single point** | CDR-044 | If this one is missing, every local bar downstream loses its path home at once and nothing reports it |

**Also blocked on this group: P-01 is an OPEN interface row.** Nothing is landed here
until it closes. **And RUN-010 may become two jackets**, because the chiller and loop
pump are on a dedicated circuit and P-01 names one.

### 1b. The fill solenoid, D2 rung 06

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| **CDR-001** | **BLOCKED, F-106**: K-FILL-S, the solenoid pole | The fill solenoid coil, page 7 | Switched 120 VAC to the coil | CDR-001 | **This contact makes and breaks 0.58 A INRUSH, not the 0.21 A holding figure.** Sizing anything here against the holding figure is sizing against the wrong event |
| CDR-045 | **BLOCKED, F-106**: neutral | The fill solenoid coil, page 7 | Coil return | CDR-045 | |
| CDR-046 | **BLOCKED, F-106**: the ground bar | The fill solenoid, page 7 | Equipment grounding for the valve | CDR-046 | |

**Blocked on P-02**, which is OPEN. The valve itself is fully specified.

### 1c. Motor supply out to the pump boxes, D2 rung 16

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-002 | **BLOCKED, F-106**: KM-DRV, pole 1 | Pump box A driver supply, page 3 | Motor supply positive, box A | CDR-002 | **CDR-002 and CDR-005 leave ONE terminal.** Count what is under that clamp before you close it |
| CDR-005 | **BLOCKED, F-106**: KM-DRV, pole 1, the same terminal | Pump box B driver supply, page 4 | Motor supply positive, box B | CDR-005 | As above |
| CDR-003 | **BLOCKED, F-106**: the 24 V rail, -V | Pump box A, page 3 | Motor supply return, box A | CDR-003 | |
| CDR-006 | **BLOCKED, F-106**: the 24 V rail, -V | Pump box B, page 4 | Motor supply return, box B | CDR-006 | |

**Blocked on P-06**, which is OPEN: both ends must agree the voltage and the conductor
before either box is built.

### 1d. The storage fill chain, D2 rung 19

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-055 | **BLOCKED, F-106**: K-FILL-S coil chain | LS-6 storage fill start, page 6 | Series element in the coil chain | CDR-055 | **Every float interrupts a coil circuit and switches no load.** Severed equals open equals the fill stops |
| CDR-056 | **BLOCKED, F-106**: K-FILL-S coil chain | LS-6, page 6 | The float's other terminal | CDR-056 | |
| CDR-057 | **BLOCKED, F-106**: K-FILL-S coil chain | LS-7 storage fill stop, page 6 | Series element | CDR-057 | |
| CDR-058 | **BLOCKED, F-106**: K-FILL-S coil chain | LS-7, page 6 | The float's other terminal | CDR-058 | |

### 1e. The day tank fill chain, D2 rung 20

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-047 | **BLOCKED, F-106**: K-FILL-D coil chain | LS-1 day tank fill start, page 5 | Series element | CDR-047 | |
| CDR-048 | **BLOCKED, F-106**: K-FILL-D coil chain | LS-1, page 5 | The float's other terminal | CDR-048 | |
| CDR-049 | **BLOCKED, F-106**: K-FILL-D coil chain | LS-5 day tank fill stop, page 5 | Series element | CDR-049 | **This is the float that is the only thing that knows the tank is full.** The overflow is its second line and nothing else is |
| CDR-050 | **BLOCKED, F-106**: K-FILL-D coil chain | LS-5, page 5 | The float's other terminal | CDR-050 | |
| CDR-059 | **BLOCKED, F-106**: K-FILL-D coil chain | LS-3 storage low, page 6 | Series element. **It is in the DAY TANK chain, not the permissive string** | CDR-059 | A dry storage tank then stops the transfer only, rather than dropping the drivers and both fills |
| CDR-060 | **BLOCKED, F-106**: K-FILL-D coil chain | LS-3, page 6 | The float's other terminal | CDR-060 | |

### 1f. The dry-run interlock, D2 rung 22

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-051 | **BLOCKED, F-106**: K-DRY coil chain | LS-4 day tank low-low, page 5 | Series element, **the dry-run element** | CDR-051 | Severed here de-energises K-DRY and stops the manifold pump. That is the safe direction and it is forced by the topology, not chosen |
| CDR-052 | **BLOCKED, F-106**: K-DRY coil chain | LS-4, page 5 | The float's other terminal | CDR-052 | |

### 1g. The high-high floats

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-053 | **BLOCKED**: the chain is not decided | LS-2 day tank high-high, page 5 | Series element, overfill backstop | CDR-053 | **Whether the high-high floats sit in the permissive string is open, D2's ?13 and ?14, MAIN-PANEL and WATER jointly.** There is no terminal to name because there is no chain to name it in |
| CDR-054 | **BLOCKED**, as CDR-053 | LS-2, page 5 | The float's other terminal | CDR-054 | |
| CDR-061 | **BLOCKED**, as CDR-053 | LS-8 storage high-high, page 6 | Series element, overfill backstop | CDR-061 | |
| CDR-062 | **BLOCKED**, as CDR-053 | LS-8, page 6 | The float's other terminal | CDR-062 | |

### 1h. The sense circuits to the Pi, D2 rungs 24 to 28

**All four are the same shape and none is a copy: a dry contact wetted from 24 V, an
optocoupler LED at the far end, THE BURDEN IN THIS PANEL, sense inverted.** The burden
stays here so the contact remains wetted if the cable is unplugged or a conductor
breaks.

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-033 | **BLOCKED, F-106**: KM-DRV, pole 2 | Display box optocoupler, page 2 | Permissive readback, wetted feed | CDR-033 | **45 to 55 mA across both branches, at make and break.** The second branch is the burden and it is a part, not an option: at 42 mA an opto LED is near its continuous rating |
| CDR-034 | **BLOCKED, F-106**: the 24 V rail, -V | Display box, page 2 | Readback loop return | CDR-034 | |
| CDR-036 | **BLOCKED, F-106**: K-FILL-D-Q, the NC leg of the changeover pole | Display box, page 2 | Day tank fill in progress. **CLOSED means NO FILL** | CDR-036 | **About 12.5 mA, ONE series branch.** Do not copy the two-branch arrangement from CDR-033: it would add a part for nothing |
| CDR-037 | **BLOCKED, F-106**: K-FILL-D-Q, **the NO leg of the SAME pole** | Display box, page 2 | The dose-inhibit leg | CDR-037 | **CDR-036 and CDR-037 are the two legs of one changeover pole and must stay in one cable.** Split them and the pair stops being a fail-detect |
| CDR-039 | **BLOCKED, F-106**: K-DRY-Q, the NO leg | Display box, page 2 | Dry-run relay state to the Pi | CDR-039 | |
| CDR-040 | **BLOCKED, F-106**: K-DRY-Q, **the NC leg of the SAME pole** | Display box, page 2 | The complement of CDR-039 | CDR-040 | **Same rule as CDR-036 and CDR-037: one pole, one cable.** If both legs ever read the same, the sense path is broken |

**CDR-039 and CDR-040 are blocked on S-20 as well**, which is an OPEN row.

**And one thing to know while you are at KM-DRV:** pole 1 is an arcing pole carrying
the motor supply and pole 2 is this sense pole, **in the same device, and S-08 has
nowhere else to go.** It is marked and not resolved. Do not move it on your own
judgement.

### 1i. The permissive coil drive, D2 rung 15

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-030 | **BLOCKED, F-106**: the KM-DRV coil | Display box logic board output, page 2 | **The coil RETURN.** The far device sinks, so the coil positive is taken here and this conductor is the return | CDR-030 | **Get this backwards and the coil can never operate while both ends look correct.** Also blocked on S-07, which must state where the coil positive comes from: from raw 24 V one shorted output device holds the contactor closed against the E-stop |
| CDR-031 | **BLOCKED, F-106**: the 24 V rail, -V | Display box logic board common, page 2 | The shared common the far driver switches against | CDR-031 | **Without this the drive does nothing and both ends still look correctly landed.** Trace the loop by hand |

### 1j. The leak console, D2 rung 11

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-063 | **BLOCKED, F-106**: the 24 V rail, +V | The leak console, page 8 | Console supply, positive | CDR-063 | **Every conductor in this cable is insulated for the higher rating even though this one carries 24 V**, because its jacket holds contact legs in the 120 V chain |
| CDR-064 | **BLOCKED, F-106**: the 24 V rail, -V | The leak console, page 8 | Console supply, return | CDR-064 | **What this console's contact does when its own supply fails is not on file anywhere, and its legs are in the permissive chain.** Do not assume a direction |

**The console's contact legs are not on this page.** MAIN-PANEL states which legs it
uses and nobody has yet.

### 1k. The ground bar, D2 rung 31. LAST, AND ALL AT ONCE

**Every green conductor in the build ends here. Do them as one job.**

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-004 | **BLOCKED, F-106**: the ground bar | Pump box A local bar, page 3 | Daisies box A's bar home | CDR-004 | |
| CDR-007 | **BLOCKED, F-106**: the ground bar | Pump box B local bar, page 4 | Daisies box B's bar home | CDR-007 | |
| CDR-032 | **BLOCKED, F-106**: the ground bar | Display box local bar, page 2 | Daisies the display box home | CDR-032 | |
| CDR-035 | **BLOCKED, F-106**: the ground bar | Display box local bar, page 2 | Grounding in the readback jacket | CDR-035 | |
| CDR-038 | **BLOCKED, F-106**: the ground bar | Display box local bar, page 2 | Grounding in the S-03 jacket | CDR-038 | |
| CDR-041 | **BLOCKED, F-106**: the ground bar | Display box local bar, page 2 | Grounding in the S-20 jacket | CDR-041 | |

**Three things about this group and they are the reason it is last:**

- **One green conductor per CABLE, not one per device.** The bars are daisied home;
  devices do not each run back here.
- **Do not fit a DIN-rail grounding terminal block anywhere in this build.** It bonds
  to the rail, the rail bonds to the plate, **and the plate is plastic, so it bonds to
  nothing.** The parallel build bought seven and is returning them.
- **A conductor landing on this bar is insulated for the highest voltage anywhere on
  the bar**, not for what it carries. The bar is in the 120 V chain even in a box that
  holds only 24 V, because the ground is common.

**The bar itself is not bought yet.**

---

## PAGE 2. DISPLAY BOX

**Entry face: BOTTOM, every cable.** Entries left to right facing the display: probes
alone at one end, then the two driver jackets, then the coil drive, then the two
changeover pairs, then the readback, then the Pi supply at the far end. **A drip loop
goes outside the box at every grip.**

**One entry on this face is NOT a grip: the Pi supply crosses at a panel-mount USB-C
bulkhead.** A USB-C connector will not pass a grip bore and re-terminating a USB-C
cable is not a thing anyone should do.

**Standing joint steps: section 0.**

**Before you open this box: each EZO circuit ships in UART mode and must be switched
to I2C with a jumper, and the mode pin differs by circuit type. Do that first. The box
has to be open for it.**

### 2a. Driver logic supply, box A and box B

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-008 | **BLOCKED, F-106**: the 5 V rail | Pump box A driver VDD, page 3 | Driver logic supply, box A. **Unswitched: the permissive removes motor supply only** | CDR-008 | **If this is broken while the logic board still drives step and direction into those pins, that is the one state the drivers must never see.** It is an overdrive through the input protection diodes on four drivers |
| CDR-009 | **BLOCKED, F-106**: the 5 V return | Pump box A driver ground, page 3 | Logic supply return, and the reference the step and direction levels are measured against | CDR-009 | Without this common the drive does nothing and both ends look correct |
| CDR-011 | **BLOCKED, F-106**: the 5 V rail | Pump box B driver VDD, page 4 | Driver logic supply, box B | CDR-011 | As CDR-008 |
| CDR-012 | **BLOCKED, F-106**: the 5 V return | Pump box B driver ground, page 4 | Logic supply return and level reference | CDR-012 | As CDR-009 |

### 2b. Step and direction, sixteen conductors

**Every one of these is blocked twice: the terminal is not named, F-106, and WHICH
PUMP BOX each channel goes to is not decided.** Land none of them.

**The token is the conductor's identity at both ends and it does not restart when the
eight split across two cables.** Write the token on the conductor in addition to the
CDR- id, and never merge or abbreviate the two into each other.

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-014 | **BLOCKED, F-106**: logic board, CH1 STEP | **BLOCKED**: the driver assigned CH1, box not decided | Step pulses, CH1 | CDR-014 + CH1 | **A severed step line is not "no steps": it is an undriven input on a driver that is enabled by default, in a box where four choppers run. Noise can clock it and the books never record it** |
| CDR-015 | **BLOCKED, F-106**: logic board, CH1 DIR | **BLOCKED**: the driver assigned CH1 | Direction, CH1 | CDR-015 + CH1 | **THE WORST FAILURE IN THIS BUILD. A severed direction line leaves the direction undefined on a driver that is enabled by default, so a head runs backwards, drawing from the manifold toward the jug, while the books decrement as though it dosed forward. Nothing measures direction and nothing measures delivery.** The fix is a pull-down AT THE DRIVER END, not here |
| CDR-016, CDR-017 | **BLOCKED**: CH2 STEP, CH2 DIR | **BLOCKED**: the driver assigned CH2 | Step and direction, CH2 | CDR-016 + CH2, CDR-017 + CH2 | As CH1 |
| CDR-018, CDR-019 | **BLOCKED**: CH3 STEP, CH3 DIR | **BLOCKED**: the driver assigned CH3 | Step and direction, CH3 | CDR-018 + CH3, CDR-019 + CH3 | As CH1 |
| CDR-020, CDR-021 | **BLOCKED**: CH4 STEP, CH4 DIR | **BLOCKED**: the driver assigned CH4 | Step and direction, CH4 | CDR-020 + CH4, CDR-021 + CH4 | As CH1 |
| CDR-022, CDR-023 | **BLOCKED**: CH5 STEP, CH5 DIR | **BLOCKED**: the driver assigned CH5 | Step and direction, CH5 | CDR-022 + CH5, CDR-023 + CH5 | As CH1 |
| CDR-024, CDR-025 | **BLOCKED**: CH6 STEP, CH6 DIR | **BLOCKED**: the driver assigned CH6 | Step and direction, CH6 | CDR-024 + CH6, CDR-025 + CH6 | As CH1 |
| CDR-026, CDR-027 | **BLOCKED**: CH7 STEP, CH7 DIR | **BLOCKED**: the driver assigned CH7 | Step and direction, CH7 | CDR-026 + CH7, CDR-027 + CH7 | As CH1 |
| CDR-028, CDR-029 | **BLOCKED**: CH8 STEP, CH8 DIR | **BLOCKED**: the driver assigned CH8 | Step and direction, CH8 | CDR-028 + CH8, CDR-029 + CH8 | As CH1 |

**Sixteen more conductors will join these**, one return paired with every step and
direction line, so that the nearest neighbour of every signal is a ground return
rather than another signal. **They are required and not yet issued.** When they are,
the two jackets to the pump boxes get new ids and the old ones retire.

### 2c. The permissive coil drive

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-030 | **BLOCKED, F-106**: logic board output, BCM 18, the sinking driver | The KM-DRV coil, page 1 | **This conductor is the coil RETURN and this device SINKS it.** The coil positive is taken in the panel | CDR-030 | Getting the direction of this backwards produces a coil that can never operate, and every check still passes because each end looks correct on its own |
| CDR-031 | **BLOCKED, F-106**: logic board common | The 24 V rail -V, page 1 | The shared common | CDR-031 | |

### 2d. The sense inputs

**All four arrive as a 24 V loop through an optocoupler LED in this box. The burden is
in the main panel, not here.** Sense is inverted on every one.

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-033 | **BLOCKED, F-106**: the S-08 optocoupler LED | KM-DRV pole 2, page 1 | Permissive readback | CDR-033 | **A severed cable or a dead LED leaves this input HIGH, which reads as the contactor dropped. That is the safe direction and it was chosen, not inherited** |
| CDR-034 | **BLOCKED, F-106**: the S-08 LED return | The 24 V rail -V, page 1 | Readback loop return | CDR-034 | |
| CDR-036 | **BLOCKED, F-106**: the S-03 optocoupler LED | K-FILL-D-Q NC leg, page 1 | Fill in progress | CDR-036 | **Severed reads as FILLING and dosing is inhibited. The failure is a stop, not a permission** |
| CDR-037 | **BLOCKED, F-106**: the dose-inhibit optocoupler LED | K-FILL-D-Q NO leg, page 1 | The dose-inhibit leg | CDR-037 | **CDR-036 and CDR-037 come from one changeover pole in one cable. If both ever read the same, the sense path is broken and that is what the pair is for** |
| CDR-039 | **BLOCKED, F-106**: the S-20 optocoupler LED | K-DRY-Q NO leg, page 1 | Dry-run relay state | CDR-039 | Blocked on S-20 as well, an OPEN row |
| CDR-040 | **BLOCKED, F-106**: the complement optocoupler LED | K-DRY-Q NC leg, page 1 | The complement of CDR-039 | CDR-040 | Same pair rule as CDR-036 and CDR-037 |

**The return arrangement of the two pairs is not settled**: whether each LED loop takes
its own return or the two share one. **That is two more conductors, or one, and nobody
can say which yet.**

### 2e. Grounding

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-010 | **BLOCKED, F-106**: the local ground bar | Pump box A local bar, page 3 | Grounding | CDR-010 | |
| CDR-013 | **BLOCKED, F-106**: the local ground bar | Pump box B local bar, page 4 | Grounding | CDR-013 | |
| CDR-032, CDR-035, CDR-038, CDR-041 | **BLOCKED, F-106**: the local ground bar | The main panel ground bar, page 1 | Grounding, one per jacket to the panel | CDR-032, CDR-035, CDR-038, CDR-041 | **This box is polycarbonate. It offers no bonding path, which is exactly why the local bar exists** |

**Not on this page: the Pi supply.** It arrives as a USB-C cable at a bulkhead. It is a
supplied assembly, nothing lands its conductors, and there is no joint to make.

---

## PAGE 3. PUMP BOX A

**Entry face: BOTTOM of the box body, not the lid.** The lid carries the heads and
comes off as a unit; anything landed on it drags wiring. **Two entries: motor supply
at the power-block end, step and direction at the logic-header end.** Nothing crosses
the box.

**Standing joint steps: section 0.**

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-002 | **BLOCKED, F-106**: driver supply block, the + side | KM-DRV pole 1, page 1 | Motor supply positive | CDR-002 | **The terminal is marked with a symbol, not a word.** Nobody has read it and no file may be trusted for it: the tree called this pin VM for weeks and the part does not |
| CDR-003 | **BLOCKED, F-106**: driver supply block, the - side | The 24 V rail -V, page 1 | Motor supply return | CDR-003 | As CDR-002 |
| CDR-008 | **BLOCKED, F-106**: driver VDD | Display box 5 V rail, page 2 | Driver logic supply. **It stays live through a permissive drop** | CDR-008 | |
| CDR-009 | **BLOCKED, F-106**: driver ground | Display box 5 V return, page 2 | Logic supply return and level reference | CDR-009 | |
| CDR-004 | **BLOCKED, F-106**: the local ground bar | The main panel ground bar, page 1 | Daisies this box home | CDR-004 | **This box is plastic. The local bar is the only bonding point in it and nothing else bonds** |
| CDR-010 | **BLOCKED, F-106**: the local ground bar | Display box local bar, page 2 | Grounding in the driver jacket | CDR-010 | |
| **Eight step and direction conductors** | **BLOCKED**: which channels are in this box is not decided | Display box logic board, page 2 | Step and direction for the channels assigned here | Each carries its CDR- id and its channel token | **Do not assign channels to boxes at the bench.** The token is declared elsewhere and a box that takes the wrong four doses the wrong product every batch and passes every check |

**Also on this box and not a conductor:** the pull-down at each driver's direction
input is a component this box owns, and it is a safety part whose failure is silent
and self-confirming. **A backed-out lead leaves a floating input on an enabled driver
and the box looks correctly built.** It is checked with a meter at commissioning, per
driver.

---

## PAGE 4. PUMP BOX B

**Same face, same entry order, same hand as box A.** These two boxes are one build and
not a mirrored pair: left is left on both.

**Standing joint steps: section 0.**

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-005 | **BLOCKED, F-106**: driver supply block, the + side | KM-DRV pole 1, page 1 | Motor supply positive | CDR-005 | As page 3: the terminal is a symbol, not a word |
| CDR-006 | **BLOCKED, F-106**: driver supply block, the - side | The 24 V rail -V, page 1 | Motor supply return | CDR-006 | |
| CDR-011 | **BLOCKED, F-106**: driver VDD | Display box 5 V rail, page 2 | Driver logic supply | CDR-011 | |
| CDR-012 | **BLOCKED, F-106**: driver ground | Display box 5 V return, page 2 | Logic supply return and level reference | CDR-012 | |
| CDR-007 | **BLOCKED, F-106**: the local ground bar | The main panel ground bar, page 1 | Daisies this box home | CDR-007 | |
| CDR-013 | **BLOCKED, F-106**: the local ground bar | Display box local bar, page 2 | Grounding in the driver jacket | CDR-013 | |
| **Eight step and direction conductors** | **BLOCKED**: which channels are in this box is not decided | Display box logic board, page 2 | Step and direction for the channels assigned here | Each carries its CDR- id and its channel token | As page 3 |

---

## PAGE 5. DAY TANK STANDPIPE

**There is no enclosure here and no face to choose.** The cords run UP the pipe, tied
at intervals, and leave through a grip **with the drip loop OUTSIDE the box.**

**Float cords and pump cords go in SEPARATE TIE GROUPS.** Two pump cords share this
pipe and they are 120 VAC.

**The float cord is not a cable you cut.** The weight clamps to it, the tie is the trip
height, and commissioning says adjust the tie and never the wiring. **If a cord will
not reach, stop: that is a purchasing question, not a splice.**

**Standing joint steps: section 0.**

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-047, CDR-048 | **BLOCKED, F-106**: LS-1, day tank fill start, both switch terminals | K-FILL-D coil chain, page 1 | Series element in a coil chain | CDR-047, CDR-048 | **Both conductors of every float come home. No series link is made at the tank** |
| CDR-049, CDR-050 | **BLOCKED, F-106**: LS-5, day tank fill stop, both terminals | K-FILL-D coil chain, page 1 | Series element | CDR-049, CDR-050 | **This float is the only thing that knows the tank is full** |
| CDR-051, CDR-052 | **BLOCKED, F-106**: LS-4, day tank low-low, both terminals | K-DRY coil chain, page 1 | Series element, the dry-run element | CDR-051, CDR-052 | |
| CDR-053, CDR-054 | **BLOCKED, F-106**: LS-2, day tank high-high, both terminals | **BLOCKED**: the chain is not decided | Series element, overfill backstop | CDR-053, CDR-054 | |

**And two things about this pipe that are not joints:**

- **Mark every trip height on the pipe before anything goes in the tank.** Nothing in
  this system measures a level, so a float that has slipped is invisible unless the
  pipe carries its own scale.
- **The float part is not chosen.** Six of the eight close on low water and two close
  on high, and the two inverted ones sit on these same pipes and are indistinguishable
  by eye once installed.

---

## PAGE 6. STORAGE STANDPIPE

**Same rules as page 5: cords up the pipe, drip loop outside, separate tie groups,
and the cord is not cut.**

**Standing joint steps: section 0.**

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-055, CDR-056 | **BLOCKED, F-106**: LS-6, storage fill start, both terminals | K-FILL-S coil chain, page 1 | Series element | CDR-055, CDR-056 | |
| CDR-057, CDR-058 | **BLOCKED, F-106**: LS-7, storage fill stop, both terminals | K-FILL-S coil chain, page 1 | Series element | CDR-057, CDR-058 | |
| CDR-059, CDR-060 | **BLOCKED, F-106**: LS-3, storage low pump-down, both terminals | **K-FILL-D** coil chain, page 1 | Series element. **It lands in the DAY TANK chain, not this tank's** | CDR-059, CDR-060 | Read that far end twice. It is the one float whose chain is not the one its tank suggests |
| CDR-061, CDR-062 | **BLOCKED, F-106**: LS-8, storage high-high, both terminals | **BLOCKED**: the chain is not decided | Series element, overfill backstop | CDR-061, CDR-062 | |

---

## PAGE 7. FILL SOLENOID

**No enclosure. The entries are the valve's own and the valve is fully specified.**

**Standing joint steps: section 0.**

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-001 | **BLOCKED**: the coil lead. **Nobody has looked at the part and the leads are not identified in any file** | K-FILL-S solenoid pole, page 1 | Switched 120 VAC to the coil | CDR-001 | |
| CDR-045 | **BLOCKED**: the coil lead, as CDR-001 | Neutral, page 1 | Coil return | CDR-045 | |
| CDR-046 | **BLOCKED**: the valve's grounding point | The ground bar, page 1 | Equipment grounding | CDR-046 | |

**One thing worth knowing while you are at this valve: with no power it springs
CLOSED.** That was chosen before the part was, and it is why a dead panel does not
leave a fill running.

---

## PAGE 8. LEAK CONSOLE

**Remote, in no enclosure, fed through its own cord grip, with its sensor on the
floor.** Its position on the wall is the owner's and is not fixed.

**Standing joint steps: section 0.**

| CDR | Lands here | Far end | What it is for | Label both ends | Watch |
|---|---|---|---|---|---|
| CDR-063 | **BLOCKED, F-106**: the console's supply terminal | The 24 V rail +V, page 1 | Console supply, positive | CDR-063 | **Every conductor in this cable carries the higher insulation rating even though this one is 24 V**, because the jacket also holds contact legs that sit in the 120 V chain |
| CDR-064 | **BLOCKED, F-106**: the console's supply terminal | The 24 V rail -V, page 1 | Console supply, return | CDR-064 | **What this console's contact does when its own supply fails is on file nowhere.** Do not assume it fails to "no leak" |

**Not on this page: the console's contact legs, and its sensor lead.** MAIN-PANEL
states which legs it uses. The sensor lead is supplied with the sensor and nothing
lands its conductors here.

**And a placement note that is not a joint: the sensor must not sit where normal
overflow discharge can splash or pool on it.** The floor drain is a track and a floor
built to move water to a track hides a leak from a floor sensor, so where this sensor
goes is a real question and not a convenience.

---

## 10. WHAT IS BLOCKED, AND THE ONE REQUEST THAT UNBLOCKS MOST OF IT

**All 111 rows carry at least one blocked cell. Not one joint can be made.**

| Blocker | Rows | Who |
|---|---|---|
| **F-106: nobody has looked at a part and written down what is printed on its terminals** | **111**, every row | Anybody with the parts in hand and a pen. **It is not a decision, a purchase or a design** |
| **Which pump box each channel goes to** | 18 | PUMP-BOXES |
| **Whether the high-high floats sit in the permissive string** | 8 | MAIN-PANEL and WATER jointly |
| **The leak console's de-energised contact state** | 4 | The owner's lookup |
| **OPEN interface rows behind whole groups** | P-01, P-02, P-06, S-07, S-20, S-11, S-04, and CBL-01 to CBL-04 | Named in each group |

**F-106 is the one to do first and it is the cheapest thing in this document.** Every
row above says "the terminal is not named" for the same reason, and one afternoon with
the parts and a pen fills 111 cells. **Until then the label column is what carries the
build: a conductor labelled at both ends is identifiable without its terminal
marking**, which is why step 1 comes before step 2.

---

## 11. TWO THINGS TO REPORT RATHER THAN WRITE INTO A PAGE

**1. document-plan.md still says D4 is "one page per conductor".** D-171 makes it a
page per enclosure, and this document is built the second way on the coordinator's
instruction and on D-171's own words. **The plan's D4 section predates the ruling and
is stale, not wrong on purpose.** BOSS's to correct.

**2. One thing a builder needs that D5 has no column for, so it is not on a page.**
Every group above has a ROUTE from one box to another and no row can say which way it
goes, because the wall layout does not exist. **That is a real gap and it is not a
missing D4 field: it is D6's route cell, open on every jacket while M-02 is open.** I
have not written a route onto any page and no page implies one.

**Everything else on every page above came from a CDR- row in D5.** Where I wanted to
say something D5 does not hold, it is in this section instead of in a page.

---

## 12. STATUS

**Stopped part way. INTERCONNECT does not declare this finished** - and this document
in particular is finished only when somebody has tried to land a wire from it.

**Eight pages, 111 rows, 64 conductors, and every joint blocked.** What exists is the
shape a builder works from and the reason each joint cannot be made yet. **Nothing on
these pages is a fact of its own: change a row in D5 and the page changes with it.**

**Panel-internal conductors are not on page 1.** They are D5 rows that MAIN-PANEL
fills, and they will appear on page 1 when they exist. **Page 1 as it stands is the
crossings only, and it says so rather than reading as a complete panel.**
