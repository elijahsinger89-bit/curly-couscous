# Established facts about real parts

Owner-supplied, 2026-08-30. These are FACTS, not decisions and not assumptions.
No agent may contradict a line in this file, and no agent may extend it from
memory. Anything not stated here is not known.

Every figure below came from the owner with the part in hand or the datasheet
open. BOSS did not derive any of it.

## Peristaltic pump heads: Kamoer KPHM400-ST

Head, motor and stepper are ONE UNIT. The flange is a panel-mount face.

**The head mounts THROUGH the pump box lid: the motor body INSIDE the box, the
head OUTSIDE it.** That is why the boxes are sealed and the heads are not.

Consequences that follow from this and were not previously on file:
- The motor is a heat source inside a sealed box. See the thermal constraint below.
- The lid penetration is a sealing face, not a clearance hole.
- The wet path never enters the box.

### Manufacturer figures, supplied 2026-08-30

| Item | Figure |
|---|---|
| Flow | 400 ml/min at 400 rpm, water, no back pressure, 20 C. **= 1.0 ml PER REVOLUTION**, roughly linear with speed |
| Tube | PharMed BPT, code B25 / 25#, 4.8 mm ID x 8.0 mm OD, 3/16 in ID x 5/16 in OD, 1.6 mm wall, **about 1000 h life** |
| Barb | 3/16 in straight connector, to mate the 4.8 mm ID tube |
| Head | 3 rollers, fixed-tube "null head" so the installed tube does not walk. External tubing connects to the ends of that short BPT piece, or via the 3/16 barbs |
| Unit | 24 V stepper, complete assembly, **about 304 g** |
| Driver | not included. It is the ADA6121 |

**THE 1.0 ML FIGURE IS SPECIFIED AT NO BACK PRESSURE.** Every dose here injects
into a pressurised circulating manifold, so the real delivered volume per
revolution is LOWER, and nothing in this system measures it. That is a
calibration, per channel, and it is what makes the jug bookkeeping mean anything.
Without it G-05 decrements against a number known to be wrong in a known
direction. Commissioning C-01, now sharpened.

**STEPS PER ML IS NOT A PUMP PROPERTY.** It is motor steps per revolution, times
the driver microstep factor, divided by ml per revolution. The 6121 has MS1 and
MS2 and **nothing has stated what they are set to.** That is an input
CONTROL-SOFTWARE needs and PUMP-BOXES owns. Commissioning C-17.

**THE TUBE IS A CONSUMABLE, about 1000 h.** A worn tube delivers less per
revolution while every instrument reads healthy, which is F-001 arriving slowly
instead of suddenly. The back-pressure calibration also drifts over tube life, so
the re-measure trigger is a TUBE CHANGE, not a date. On the event list in
commissioning.md.

**THE FIXED-TUBE NULL HEAD SHAPES THE JUG PATH.** The installed BPT loop is short
and external tubing joins at its ends. So the break point in the jug change
procedure, and any keyed coupling if one is ever taken, sits on EXTERNAL TUBING
and never on the pump tube.

**STILL NOT KNOWN, still not to be invented:** the microstep setting, and the
delivered volume per revolution against real back pressure.

## Stepper drivers: Adafruit 6121, TMC2209 breakout, SCREW TERMINALS

Printed pins, and this is the complete list:

    STEP  DIR  EN  MS1  MS2  DIAG  INDEX  VDD  GND  VM  1A  1B  2A  2B

- **There are no PUL+, DIR+ or differential pairs.** Anything written for an
  opto-isolated differential driver does not apply to this part.
- **VDD is a separate logic supply pin, 3.3 to 5 V. The motor terminal block does
  not generate it. With VDD unconnected the driver does not respond to STEP or DIR
  at all.**
- **EN unwired leaves the driver ENABLED.** Default state is on, not off, **and
  by D-032 it STAYS unwired.** Software therefore has no per-driver disable, ever.
- Vref: **the instruction as first written, "set the pot with a meter before any power
  is applied", is UNEXECUTABLE. See findings F-061. VREF is scaled off 5VOUT and the
  5 V regulator is sourced from VS, so with no power there is nothing to measure. The
  rail that must be present is VS.** Not rewritten here, because the two-step reading
  is a reading and not the owner's stated intent.
- **One piece of good news that falls out of the same fact: because VREF is referenced
  to the regulated 5VOUT rather than to VS, the motor current setting is to first
  order INDEPENDENT of the 23.76 to 28.28 V trim. Turning the trim does not walk the
  current, so C-16's trim position does not propagate into C-01's arithmetic** - one
  less coupling than F-010 implies. Worth confirming against 5VOUT's regulation spec.
- Each driver needs a stick-on heatsink.

### The Adafruit 6121 schematic, Rev A, 2024-12-18. Eagle .sch and .brd published.

**Adafruit published the SCHEMATIC, not only a pinout. The mapping below is read
from it.**

Header JP4, a 2x5. Silkscreen to chip pin:

| Silk | JP4 | Chip net | QFN |
|---|---|---|---|
| VDD | 1 | **VCC_IO** | 15 |
| GND | 2 | GND | 3, 18, 25, paddle |
| DIR | 3 | DIR | 19 |
| STEP | 4 | STEP | 16 |
| MS1 | 5 | MS1_AD0 | 9 |
| MS2 | 6 | MS2_AD1 | 10 |
| DIAG | 7 | DIAG | 11 |
| INDEX | 8 | INDEX | 12 |
| UART | 9 | PDN_UART | 14 |
| EN | 10 | **ENN** | 2 |

Terminal block JP1, component side left to right, silk reads **+ - 2B 2A 1A 1B**:

| Silk | Chip net | QFN |
|---|---|---|
| **+** | **VS** | 22 and 28 |
| **-** | GND | |
| 2B | OB2 | 1 |
| 2A | OB1 | 26 |
| 1A | OA1 | 24 |
| 1B | OA2 | 21 |

**NOTE THE TERMINAL BLOCK SILK IS "+" AND "-", NOT "VM". Any subsystem calling that
pin VM is using a chip-adjacent name rather than what is printed. Confirm against a
board in hand before it goes on a build sheet.** See findings F-051.

**VDD ON SILK IS ONLY VCC_IO. Motor + is only VS. They are not tied together.**

Other chip pins on the board, not brought out: **CLK** QFN 13 hard-tied to GND,
internal oscillator. **STDBY** QFN 20 left open. **SPREAD** QFN 7 to solder jumper
SPRD / SJ1, open floats and closed ties to VDD. **VREF** QFN 17 from the ILimit pot,
**scaled off 5VOUT QFN 8, NOT off VDD.** Charge pump CPO-CPI 22 nF, VCP to VS,
BRA/BRB through 0.05 ohm.

### Board in hand, 2026-09-01. Photograph, read by BOSS.

**This is the confirmation F-051 asked for, and it both confirms and corrects.**

Observed, and marked as read from a photograph rather than from a board on a bench:

| What is printed | Note |
|---|---|
| Terminal block silk: **a circled plus and a circled minus symbol, then 2B 2A 1A 1B** | **F-051 CONFIRMED and sharpened: the part does not say VM, and it does not say the WORDS plus and minus either. It carries two SYMBOLS.** A build sheet cannot quote a symbol, so it must name the terminal by position and by what it does |
| Header silk, two staggered rows of five. Top: **VDD DIR MS1 DIAG UART**. Bottom: **GND STEP MS2 INDEX EN** | Reading down the columns gives VDD/GND, DIR/STEP, MS1/MS2, DIAG/INDEX, UART/EN, **which matches the JP4 1-to-10 mapping exactly.** Confirmed in situ |
| **ILimit 0->2A**, printed beside the pot | **The board prints a current range on itself.** 1.0 A per driver is therefore half of what the board's own silk advertises, which is consistent with the 71 percent of the part's rating already on file, and it is worth knowing that the printed range and the part's rating are two different numbers |
| **SPRD** solder jumper, silk visible | Matches the schematic's SJ1 |
| **F, B, S** silk beside three LEDs | Matches the schematic: green F conducts when DIR is low, red B when DIR is high, yellow S on STEP |
| 22 uF 35 V electrolytic | Matches the bulk cap already recorded |

**AND ONE CORRECTION THAT MATTERS TO A DECISION IN FLIGHT.**

parts.md has said since 2026-08-30 that the 6121 is "a TMC2209 breakout with SCREW
TERMINALS". **That is true of JP1, the power and motor block, and it is NOT true of
the logic side. The logic side is a 0.1 in header footprint, and the photograph shows
a 10-pin header strip supplied LOOSE and UNSOLDERED.**

**JP4 SHIPS AS BARE PADS with the strip loose. That answers the gate PUMP-BOXES
named: it is soldered flying leads or a soldered connector of the builder's choosing,
not a plug-on assembly out of the box.**

**And the photograph confirms PUMP-BOXES' correction to its own segment-5 answer: the
top header row reads VDD DIR MS1 DIAG UART left to right, so VDD AND DIR ARE
PHYSICALLY ADJACENT ON THE BOARD.** DIR's nearest opposite-potential neighbour is not
four feet away in a cable. It is on the connector, where G-29's pairing cannot reach.

**So the drivers ship with the logic connector not fitted. Soldering it is a build
step nobody had.** And it changes the landing analysis PUMP-BOXES is mid-flight on:
it ruled out putting a resistor lead into the driver's own screw terminal on T-009
and T-010 grounds, **but there is no screw terminal on the logic side to rule out.**
The real options there are a soldered pad, a header pin, or a socket. See F-054.

### Board pulls, read from the Eagle nets. THIS IS THE D-062 ANSWER.

| Pin | What is actually there | Chip type |
|---|---|---|
| **EN / ENN** | **EXPLICIT 20k PULLDOWN, R3, EN to GND. No LED on EN. Left open, ENN is low, DRIVER ENABLED** | DI only, **NO internal pull** |
| **STEP** | **BOARD PULLDOWN plus an LED load.** R5 20k pack: one section STEP to 20k to GND, a DC pulldown; one section STEP to 20k to a yellow LED, silk S, to GND. **Floating STEP is pulled low. The LED is load when STEP is high, not a pull-up** | DI only, **NO internal pull** |
| **DIR** | **NO DEDICATED PULL-UP OR PULLDOWN RESISTOR ON THE BOARD.** What is on DIR is two indicator LEDs: DIR to red LED silk B to 20k to GND, conducting when DIR is high; and VDD to 20k to green LED silk F to DIR, conducting when DIR is low. **That is LED loading, not a defined logic pull** | **DI (pd), INTERNAL PULLDOWN** |

**So a floating DIR goes LOW, via the CHIP's internal pulldown rather than via
anything on the board. EN and STEP have real board pulldowns. DIR does not, and its
defined level comes from inside the chip.**

### DIR, STEP and the thresholds. THIS CORRECTS AN EARLIER ENTRY.

| Fact | Figure |
|---|---|
| DIR internal pull-down | **132 k min, 166 k TYPICAL, 200 k max.** Not the STANDBY pin's tighter 80 to 120 k row |
| **STEP internal pull-down** | **NONE. Pin type is DI with no (pd). The pins marked (pd) are DIR, MS1, MS2 and STDBY only** |
| VINLO max | **0.30 x VCC_IO**, so 0.99 V at 3.3 V |
| VINHI min | **0.70 x VCC_IO**, so 2.31 V at 3.3 V |
| Hysteresis | 0.12 x VCC_IO, about 0.40 V typical |
| Input leakage | plus or minus 10 uA, **IN ADDITION to the pull-down** |

The 0.44 and 0.56 figures in the datasheet's Fig 13.1 are **typical Schmitt trips, not
guaranteed. Use 0.30 for a does-it-read-low ruling.**

> **A FLOATING DIR FLOATS HIGH, NOT LOW. THIS REVERSES WHAT parts.md SAID BEFORE.**
>
> The internal pull-down sinks about 20 uA at 3.3 V. **The board's green LED branch
> pulls UP to VDD through 20k and an LED, and a normal indicator LED with a 20k series
> resistor WINS against 166 k by an order of magnitude.** The pin sits above VINHI.

See findings F-059, corrected, and D-096.

### VS and VCC_IO sequencing: the datasheet is SILENT, and that is the result

Checked TMC2209 rev 1.09, the PDF Adafruit ships, and 1.08. **THERE IS NO REQUIRED
POWER-UP OR POWER-DOWN ORDER between VS and VCC_IO.**

What it does state: **VCC_IO is the 3.3 to 5 V IO supply for all digital pins and
DOES NOT SUPPLY THE IC LOGIC PART.** Logic and the 5 V regulator are sourced from
VS. Separate undervoltage and reset detectors on VS, 5VOUT and VCC_IO, and cycling
any of the three resets the chip to power-on defaults, **the datasheet saying it is
easiest and safest to cycle VCC_IO.** Absolute max and operating ranges treat VS and
VCC_IO as independent rails. The standby chapter says VCC_IO shall remain active
while STDBY shuts the internal regulator, **which is VS PRESENT, not VS absent.**

**IT DOES NOT ALLOW, FORBID, SEQUENCE OR CHARACTERISE "VS ABSENT WHILE VCC_IO IS
LIVE." No pin leakage figure, no clamp current, no STEP or UART behaviour in that
state.** All it implies is that with VS below its undervoltage threshold the VS
detector is in reset and the core regulator has no input.

**That is not a sequencing rule and it is not a characterisation. P-09 CANNOT BE
CLOSED FROM DOCUMENTATION. It closes by MEASUREMENT or by REMOVING THE STATE.**

### VS range

| Source | Figure |
|---|---|
| TMC2209 operating, internal 5 V regulator | 5.5 to 29 V |
| Absolute max with inductive load | 32 V |
| Absolute max supply and bridge spike | 33 V |
| **Adafruit 6121 board, the only VM figure published, labelled neither recommended nor absolute** | **5 to 29 V DC** |

**No VM regulator and no clamp on the board.** The 22 uF 35 V bulk cap is above 29 V
so it does not pull the limit down.

**And the abs-max footnote that matters more than the number: stray inductance in
GND and VS rings the supply when driving an inductive load, from fast switching
slopes plus body diode reverse recovery, and even small trace inductance generates
several volts of overshoot. A METER READING 28 V DC CAN RING TOWARD 32.**

**That is a WIRING requirement, not a voltage setting: keep VS and its return short
and paired, and the local bulk cap is what absorbs the ring.** See F-052.

## Motor current

- 1.0 A per driver, which is 71 percent of the part's rating.
- Eight drivers is 8.0 A worst case connected on the 24 V rail.
- **Standstill current has never been measured** and is currently assumed at 30
  percent of running. That is an assumption, labelled as one. Commissioning C-13.

## 24 V supply: Mean Well NDR-240-24

24 Vdc, 10 A, 240 W.

**VDD is fed from the display box 5 V rail, which is the Pi's own supply, and is
NOT switched by the permissive.** D-031. The permissive removes MOTOR supply only.

**It has a front panel output trimmer with a 24 to 28 V adjustment range and plus
or minus 1 percent tolerance, so the rail is settable anywhere from 23.76 to
28.28 V. Over-voltage protection does not trip until 29 V. Nothing fixes the trim
position. Everything on that rail sees whatever it is set to.**

The rail is not 24 V. It is whatever the trimmer is at. See findings F-010.

## Relays and contactors

| Part | What | Minimum switching load |
|---|---|---|
| Finder 55.34, four off, on 94.74SMA sockets | 4PDT relays | 300 mW at 5 V and 5 mA |
| Finder 22.32, two off | Modular contactors, 24 Vdc coils, 2 NO, 25 A | 1000 mW at 10 V and 10 mA |

**Minimum switching load matters and differs between them. A contact switching
below its minimum load oxidises.** See findings F-011.

### How to read a minimum switching load, established 2026-09-01

**IT IS A POWER REQUIREMENT. THE V/mA PAIR IS A REFERENCE COORDINATE, NOT AN
OPERATING POINT.**

The 55.34 AgNi publishes 300 mW (5/5), **and 5 V times 5 mA is 25 mW, so the pair
cannot be a legal operating point.** Finder's own worked examples: at 5 V you need
60 mA; **at 24 V you need 12.5 mA**; at 5 mA you need 60 V. The 22.32 publishes
1000 mW (10/10) and reads the same way.

**So there is ONE requirement per contact, not three independent floors. A current
figure that clears its reference coordinate is not a margin.** The roughly 12.5 mA
at 24 V already on file for the 55.34 is the correct figure and it clears 300 mW
exactly, so it is a floor and not a margin.

**The mechanism, class behaviour and not Finder-specific: Holm fritting.** Silver
and AgNi grow sulfide and oxide films. **A-fritting is voltage punching a channel
through the film. B-fritting is current heating that channel until the film displaces
and a metal bridge forms. Power is how makers package both into one published
region.** Wipe helps and cannot be relied on at dry-circuit levels on a power
contact.

**Gold variants.** Option 5 on the 55.34 is AgNi plus hard gold, **whole relay, poles
cannot be mixed at order time.** Gold floor is 50 mW at 5 V and 2 mA. **Gold is
consumed by switching above roughly 30 V and 100 mA, after which the contact reverts
to AgNi and the 300 mW floor returns.**

### THE THING THAT KILLS MIXED DUTY IS NOT THE PLATING

**The 55.34 plug-in is RT I, dust protected and NOT wash tight, and ALL FOUR POLES
SHARE ONE VOLUME. A 7 A break throws silver vapour, oxide and carbon into that
volume and it lands on the quiet pole.** Zettler states it for the class: very
different loads, high load and measuring signal, shall not be switched by the same
relay, because erosion from switching high loads may pollute the low level contacts.
**That is not Finder, and Finder is silent on mixed poles.**

**So the gold plating on a quiet pole survives AND the contact still degrades. The
failure arrives by a path that is not the one being argued about.**

**IF ANY RELAY CARRIES BOTH A POWER POLE AND A SENSE POLE, THE DEBRIS PATH APPLIES,
AND NO CONTACT MATERIAL OR BURDEN VALUE ADDRESSES IT.** That is why the browser
build DELETED its low-level contact rather than improving it. See G-30.

## Chiller: JBJ Arctica DBE-200

115 V, 6 A, 3000 BTU/h, R-134a, no internal pump. **Required flow 420 to 1920
gph.**

**Its locked rotor current is NOT PUBLISHED anywhere. Any inrush figure is an
estimate and must be labelled as one, everywhere it appears.**

## Day tank temperature control

- Setpoint 66 F, plus or minus 2 F.
- Pulls down at 68 F, stops at 64 F. Four degrees of deadband.
- Room runs 62 to 65 F.

**So the setpoint sits at or above room temperature and the chiller has very
little work to do.** See the S-18 reassessment in decisions.md D-025.

## Probes: Atlas Scientific EZO

| Circuit | Carrier | Why |
|---|---|---|
| EZO pH | ISCCB-2 | pH and EC share a solution and must be isolated from each other |
| EZO EC | ISCCB-2 | as above |
| EZO RTD, with PT-1000 | **NO CARRIER** | A resistance measurement has no solution ground path, so there is nothing to isolate |

**THE EZO CIRCUITS SHIP IN UART MODE, NOT I2C. Each must be manually switched to
I2C with a jumper procedure before the Pi can see it, and the mode pin differs by
circuit type.** Commissioning C-14. This is a build step nobody had.

This also closes DISPLAY-BOX's open question about three circuits on two carriers:
it is one carrier each for pH and EC, and none for RTD, for a stated reason.

## Enclosures

**ALL FOUR FOOTPRINTS AND ALL FOUR PLATES ARE NOW OWNER-GIVEN, 2026-09-23, D-226.**
Outlines and plates only. **MOUNTING HOLE PATTERNS ARE NOT GIVEN FOR ANY OF THE FOUR,
main panel included, and none has ever been in this tree. F-124.**

| Box | Overall, mm | Overall, in | Plate, mm | Note |
|---|---|---|---|---|
| Main panel | **508 x 419 x 201** | 20.0 x 16.5 x 7.9 | **468 x 379** | Qilipsu. Ordered and delivered, T-030 |
| Display box | **300 x 300 x 150** | 11.8 x 11.8 x 5.9 | **260 x 260** | NEMA 4X polycarbonate, gasketed display cutout |
| Pump box A | **406 x 203 x 152** | 16.0 x 8.0 x 6.0 | **381 x 178** | Sealed. Heads pass through the lid |
| Pump box B | **406 x 203 x 152** | 16.0 x 8.0 x 6.0 | **381 x 178** | Sealed. Heads pass through the lid |

**CORRECTION, and it is a real one, not a tightening: the display box was carried here
and in D7 as "roughly 300 by 250 by 130 mm".** It is **300 x 300 x 150**. The middle
dimension is 50 mm larger and the depth 20 mm larger. **Nothing was sized against the
old figures - the display box interior sheet was never written - so the correction
costs nothing today and would have cost a sheet tomorrow.**

**THE THREE NEW PLATE FIGURES ARE WHAT MATTER MORE THAN THE OUTLINES. F-123.** The main
panel's interior sheets exist only because 468 x 379 was known. **The pump box and
display box interior sheets were recorded in D3 as "unwritten rather than blocked" -
they were blocked, on these three figures, and no list carried the blocker.**

**Plastic gives no bonding path, so every equipment ground lands on a ground bar
rather than on the box.**

## The Raspberry Pi 5 header at power-on

**There is no official per-pin table, and the provenance of what exists matters.**

The 40-pin header is RP1 bank 0, GPIO0 to GPIO27. **BCM2712 pad and device-tree
defaults do NOT describe those pins, and RP1's own table lists the pull reset as
"varies" with no per-pin column.**

**At pad reset: output disable 1, input enable 0, drive 4 mA, Schmitt on. So the pin is
NOT a software input at power-on and its function is NONE, neither input nor output
enabled. THE PAD PULLS STILL ACT ON THE PIN VOLTAGE.**

| Pins | Pad default |
|---|---|
| GPIO0 to GPIO8 | **PULL-UP** |
| GPIO9 to GPIO27 | **PULL-DOWN** |
| **GPIO2 and GPIO3** | **STRONGLY HIGH. On-board 1.8 to 2 k pull-ups to 3.3 V. The weak pad pull cannot fight them. No other I2C mux on the header has those resistors** |

Pad resistance roughly 50 k typical: pull-up 37 to 86 k, pull-down 35 to 98 k.

**PROVENANCE, and it is not a datasheet.** The per-pin map exists only in statements
from Raspberry Pi engineers on the forum, March 2024 and January 2025, repeated for CM5
and Pi 5. **It is the only Pi 5 specific source and it appears in no datasheet.** Recorded
with its source rather than as a specification, per T-018's discipline in reverse: this
is not a seed, it is a real observation from a non-authoritative source, and the
difference is worth carrying.

**The HAT+ spec says outright: if you need a defined level at power-on, FIT AN EXTERNAL
RESISTOR. Do not trust the pad.** That makes DISPLAY-BOX's physical-pull requirement
authoritative rather than prudent.

**For the fail-direction sweep: GPIO0 to 8 weakly high, GPIO9 to 27 weakly low, GPIO2
and 3 STRONGLY high, nothing floating, and any pin that must be safe the instant 3.3 V
appears needs an external pull, because 50 k is weak and firmware can change it at step
three.**

## DIAG and INDEX, and why the ruling cannot rest on the datasheet

**DIAG is pin 11, ACTIVE HIGH.** Its sources: StallGuard stall in StealthChop only;
overtemperature shutdown, latched; short to GND, latched; short to VS, latched; and
**charge-pump undervoltage uv_cp, which is NOT latched and disables the driver while
set. Open load is informative only and does NOT reach DIAG.**

**INDEX is pin 12 and is NOT a fault pin by default.** It pulses **once per electrical
rotation at microstep 0.** It can be remapped to overtemperature prewarning or to the
internal step generator by GCONF bits, and it reports nothing else.

**BOTH ARE PUSH-PULL, NOT OPEN DRAIN.** The datasheet never uses either phrase, but the
pin type is DO rather than OD and the DC table specifies VOUTHI at minus 2 mA, **which
means the pad SOURCES.** CMOS push-pull into VCC_IO. **No pull-up required, no Hi-Z
line.**

### The two undervoltages must not be conflated

**uv_cp is charge-pump undervoltage on a LIVING chip, and it IS a documented DIAG
source.**

**VUV_VS is the VS reset threshold, typically 4.2 V, and it takes the CORE into reset,
because the 5 V regulator that feeds logic derives from VS. VCC_IO staying up does not
prevent that.**

> **For the state VS below VUV_VS with VCC_IO valid, the datasheet does NOT say whether
> DIAG or INDEX is high, low or Hi-Z, does not say whether the pad remains a driven
> output while the core is held in reset, and does not offer DIAG as a VS-present
> detector.**
>
> **SO DIAG IS NOT A SPECIFIED DETECTOR FOR VM ABSENT.** A fault output undefined in the
> state it would report is not a detector. **If the ruling depends on that, it cannot be
> made from the PDF and only C-18 can settle it.**

## The main panel face, as decided

**Door-mounted devices, all five on the TOP FACE of the main panel, five 22 mm
holes, step drilled. Nothing else penetrates that face. Every cord grip is on the
BOTTOM face.**

| Device | Type | Function |
|---|---|---|
| E-STOP | momentary, normally closed | Breaks the permissive string |
| RESET | momentary, normally open | Latches the master permissive relay |
| PL-G | green pilot lamp | Filling |
| PL-R | red pilot lamp | Permissive lost |
| PL-Y | yellow pilot lamp | Healthy |

**The E-stop and reset are hardware, not software.** The Pi cannot override the
E-stop and cannot re-close the permissive. Only the reset button does that.

**The three lamps are driven from RELAY POLES, not from the Pi. So the panel tells
you its state with no computer involved, and that is deliberate.**

**Decided 2026-08-30: PL-Y is a lamp across the outgoing 24 V rail, downstream of
the permissive contactor**, D-045. It shows that motor supply actually ARRIVED,
which is measured rather than commanded, and it costs no coil. **PL-R and PL-Y both
on is an impossible state: if you see it, the contactor is welded.** It forces PL-Y
to be 24 V class specifically.

**The receptacles are PANEL MOUNTED in the enclosure face and cords plug in from
outside**, D-046. They are not fed through cord grips.

**The top face is treated as needing GASKETED DEVICES**, D-047. The enclosure's own
rating is still unchosen, F-025.

That is the whole panel face.

Consequence for MAIN-PANEL, routed rather than decided: three lamps driven from
relay poles is a claim on the pole budget, alongside the fill chains, the seal-ins
and the interlocks. Which pole drives PL-Y "healthy", and what "healthy" means as
a contact rather than as a word, is MAIN-PANEL's to answer.

## The wall

**8 ft by 8 ft. That is the layout envelope. Everything mounts on that one wall: four
enclosures, the manifold, the tubing raceway and the jug stations.**

Z5, M-02 and the station run are all consequences of how those are placed inside it.

### The sightline. ONE REAL COORDINATE, 2026-09-23, D-226

**EYE LEVEL IS 1829 mm FROM THE FLOOR, 6 ft. Owner-measured.** It is the first real
number on the Y axis and it is the only one. **X is still entirely open and so is
every other Y.**

**M-02 IS NOT CLOSED BY IT.** wall-survey.md asks for coordinates from one named datum
per item, and a single Y shared by four items is neither a datum nor per item.

**WHAT IT DOES NOT DO, counted rather than characterised, per T-031:**

| | |
|---|---|
| RUN- cut lengths | **Still blocked.** Wall run is dominated by X and X is open |
| D6's position and spacing cells | **Still blocked** |
| D1's dimensioned half | **Still blocked** |
| D3 sheet 3.8 | **Still blocked, and now on TWO things**: the survey, and a mounting-hole pattern for any box at all. F-124 |

**WHAT IT DOES DO: three of D3's sheets become writable, and it is the plates that do
it, not the sightline.** Pump box A, pump box B and the display box interiors, owned by
PUMP-BOXES and DISPLAY-BOX.

### The anti-siphon constraint belongs to the JUG SHELF. G-58, D-227

**EVERY LIQUID LEVEL STAYS BELOW THE MANIFOLD, so a failed tube cannot siphon a
container into the tank.**

**THE CONSTRAINED THING IS THE CONTAINER LEVEL AND NOT THE PUMP POSITION.** The siphon
path runs container to manifold. **The pump head is not on that path and its height
does not appear in it.**

| Item | What the rule says about it |
|---|---|
| **Jug shelf** | **BELOW the manifold. This is the constraint and it is the whole of it** |
| Pump box A, Pump box B | **FREE with respect to siphoning.** Above the manifold is safe, below it is safe |
| Manifold | The ceiling the jug shelf is measured against |

**Recorded here as owner's correction of his own earlier framing, which attached the
rule to the pump boxes.** G-58: **a constraint attaches to the thing whose value it
bounds, and a constraint filed against the wrong item is a constraint the next editor
satisfies without fixing anything.**

## Cable runs, measured on the wall, and the CUT LENGTHS

**Cut length is the wall run PLUS 3 FT: 6 in drip loop per grip, 12 in service per
end.**

| From | To | Wall run | **Cut** |
|---|---|---|---|
| Panel | Pump box A | 6 ft | **9 ft** |
| Panel | Pump box B | 8 ft | **11 ft** |
| Panel | Display box | 4 ft | **7 ft** |
| Display | Pump box A | 4 ft | **7 ft** |
| Display | Pump box B | 6 ft | **9 ft** |

**The probe run is within 6 ft of the display box, the same run as the tank.**

**T-020 applies to this table when it reaches a build procedure: the allowance is
folded into the cut step and never stated after it.**

## Cable runs, measured on the wall and already doubled for slack

| From | To | Length |
|---|---|---|
| Panel | Pump box A | 6 ft |
| Panel | Pump box B | 8 ft |
| Panel | Display box | 4 ft |
| Display | Pump box A | 4 ft |
| Display | Pump box B | 6 ft |

Everything is a short run. These are measured figures, not estimates, and they
already include the slack.

## The permissive chain, as built

A hardwired series string of dry contacts: E-stop, leak console, float interlocks.
**It latches a master relay.** Every fill chain and the driver permissive contactor
sit DOWNSTREAM of it, so a leak, an E-stop or a lost interlock drops everything in
hardware, independent of the Pi.

**The Pi cannot override it and cannot re-close it. A manual reset button does
that.**

## The leak console is POWERED, not a passive float

It takes 24 V and returns a Form C dry contact into the permissive string.

**Its contact legs sit in the 120 V chain, so every conductor in its cable must be
insulated for 600 V.**

**The part is a Winland WaterBug WB200.**

> **THE FLOAT ROSTER THAT STOOD HERE IS 1ST EDITION LINEAGE, UNVERIFIED. STRUCK
> 2026-09-03 BY D-118, ON THE OWNER'S CONFIRMATION.**
>
> This file said "the float switches are LS-1 through LS-8, pilot duty, nobody has
> traced that chain against the actual SJE part". **The owner confirms that roster
> came from the same body of work as the 1st Edition document set. It is not an
> independent arrival.** So it was a 1ST EDITION FACT sitting under "established
> facts about real parts", and checking it against the 1st Edition drawings would
> have been checking a document against itself. **G-37 confirmed inside the
> authoritative file.** F-090.
>
> **It is not the incumbent. THE FLOAT PASS RESTARTS FROM REQUIREMENTS: ask what a
> float must DO at each position, then find a part. The old roster is ONE CANDIDATE
> among others and carries no priority for having been here first.**
>
> **And the requirement carries F-089 with it: the 1st Edition floats switch a
> 120 VAC coil and this build's control voltage is 24 V. Under G-31 that is a fifth
> of the contact power at the same current. That belongs in the REQUIREMENT, not in
> a part comparison.**

## The Pi is powered independently of everything else

Its receptacle is **fused and NOT relay switched**. The Pi has power whenever the
panel does.

- **It stays alive through a permissive drop and can log and alert on it.** No
  software may assume it loses power with the system.
- **Nothing in the panel can power cycle the Pi.** It reboots by software or by
  killing the panel, **so a watchdog is the only recovery path.**

## What the Pi drives, from the browser package

**ONE coil: the driver permissive contactor.** One output, **BCM 18**, through a
**ULN2003 sinking the coil return**, with **SUP-1 across the coil**. Nothing else.

**THE PANEL RUNS WITHOUT THE PI**, G-26. Fills, transfer, circulation and chiller
all operate on float and interlock logic with no computer involved. The Pi adds
dosing and removes driver power. **If it dies, the water system keeps running and
only dosing stops.**

Note the topology this fixes: the transfer pump is a POLE on the day tank fill
relay, the manifold pump is a POLE on the dry-run interlock relay, and the
chiller is a CONTACTOR on its own circuit. None of the three is a Pi-driven coil.

## The permissive readback

The Pi drives the driver-permissive contactor coil AND reads back a real auxiliary
contact on that contactor, so it can tell commanded state from actual state.

It exists specifically to catch a welded contact, where the Pi commands the rail
off and eight drivers stay live.

**Do not let software report commanded state as measured state anywhere.**

### The readback circuit, as built. Given by the owner, not derived.

**There is no auxiliary contact block on the 22.32. None is in the parts list and
none was ever bought.**

| Pole | Terminals | Use |
|---|---|---|
| 1 | 1 and 2 | Carries the 24 V rail out to both pump boxes. **One pole for VM distribution, not two: both pump box feeds come off one terminal downstream of it** |
| 2 | 3 and 4 | Was unwired and free. **The readback was granted onto it** |

So a 25 A power pole is the readback contact. **But it is not a bare 3.3 V logic
input, and that is what saves it.**

The circuit: pole 2 is wetted from 24 V. Two parallel branches sit across the
contact, one carrying an optocoupler LED through a series resistor and one a bare
burden resistor, **sized together so the contact sees 45 to 55 mA against the
22.32's 1000 mW minimum switching load.** The optocoupler transistor pulls a Pi
input low.

**The burden sits in the MAIN PANEL, not at the Pi.** So the contact stays wetted
even if the cable is unplugged or a conductor breaks. Two reasons, both stated by
the owner: a power contact left switching 14 mA oxidises, and **the failure of the
cable must not degrade the contact it senses.**

**The sense reads INVERTED: contact closed means LED on means the Pi input goes
LOW.**

Do not re-derive this circuit. It is recorded as given.

**The fail direction is a CHOSEN PROPERTY, not an inheritance.** A broken cable or
a dead LED leaves the Pi input high, which reads as contact open, which reads as a
drop. That is the false-stop direction, the same one D-017 and D-030 chose. It
holds for S-08 and for S-03. See G-22.

### The S-03 sense circuit: same topology, DIFFERENT NUMBERS. Do not copy S-08.

Same shape: a dry contact wetted at 24 V, one branch through an optocoupler LED
and series resistor, **the burden in the MAIN PANEL**, an isolated input at the
Pi, sense inverted. Same two reasons verbatim: a contact left below its minimum
switching load oxidises, and a cable failure must not degrade the contact it
senses.

**Different numbers, and that is why it is not a copy:**

| Contact | Minimum switching load | At 24 V |
|---|---|---|
| Finder 22.32, S-08 | 1000 mW at 10 V and 10 mA | about 41.7 mA |
| Finder 55.34, S-03 | 300 mW at 5 V and 5 mA | about 12.5 mA |

**S-03 needs roughly a third of the current, and that difference is what makes
S-08 need two parallel branches and S-03 not.** At 42 mA an optocoupler LED is
near its continuous rating, so S-08 splits into a sense branch and a bare burden
branch. At 12.5 mA a single series branch carries the whole loop and the LED sits
in its normal operating band. **S-03 is the simpler circuit, and copying S-08's
two-branch arrangement onto it would add a part for nothing.**

MAIN-PANEL gets both minimums explicitly and sizes each independently. **Neither
figure may be carried from the other. Both are RELAY properties, not circuit
properties: a minimum switching load belongs to a contact.**

## Not known, and not to be invented

The KPHM400-ST flow rate per revolution, its tube size and its barb size. Every
part number, quantity and size not stated in this file. Ask the owner.

## The fill solenoid. ORDERED AND FULLY SPECIFIED. Owner, 2026-09-04. D-136.

**ASCO 8210G095AC120/60.**

| Property | Value |
|---|---|
| Connection | 3/4 in NPT |
| Body, seals | Brass body, NBR seals |
| Action | **2-way NORMALLY CLOSED** |
| Coil | **120 VAC 60 Hz**, Class F, 10.1 W |
| **INRUSH** | **0.58 A** |
| **HOLDING** | **0.21 A** |
| Cv | 5 |
| **Minimum operating pressure differential** | **0 psi.** Max 150 psi |
| Operation | **DIRECT-LIFT hung diaphragm. NOT pilot-operated** |
| Orientation | Any. Coil-up preferred for long life |
| Power loss | **Spring returns CLOSED** |
| Installation | Between unions |

**THE 0 PSI IS THE PROPERTY THAT DECIDED IT.** A pilot-operated valve needs a
pressure difference to open and **will not open on a low-pressure supply, which is
a valve that fails closed for the wrong reason.** The owner's warning, recorded
because it will mislead someone later: **distributors sometimes print "pilot
operated" on this family. THE 0 PSI MINIMUM IS WHAT MATTERS**, not the wording on a
listing.

**AND THE NUMBER MAIN-PANEL NEEDS IS THE INRUSH, NOT THE HOLDING FIGURE. A RELAY
CONTACT MAKES AND BREAKS 0.58 A.** Sizing a contact against 0.21 A is sizing it
against the wrong event.

## The chiller and its loop pump. F-086 CLOSES. Owner, 2026-09-04. D-137.

| | |
|---|---|
| Chiller | **JBJ Arctica DBE-200**, 1/10 HP, 115 V, **6 A**, 3000 BTU/h, **NO internal pump** |
| Loop pump | **Danner Supreme Aqua-Mag 12, item 02712** |
| Rated | 1200 GPH, **about 840 to 940 GPH at 4 to 6 ft head** |
| Electrical | 110 W, **1.5 A at 120 V** |
| Connections | 3/4 in FPT inlet, 3/4 in MPT outlet |
| Duty | Continuous, oil-free magnetic drive, submersible or inline |

**SO THERE ARE TWO SUBMERSIBLES IN THE DAY TANK AND BOTH RUN CONTINUOUSLY:** the
manifold pump and this one.

**G-12 WAS RIGHT THAT A LOOP PUMP EXISTS AND WRONG ABOUT WHAT SWITCHES IT.** Both
the chiller and this pump share **ONE SWITCHED RECEPTACLE ON A DEDICATED CIRCUIT,
so both stop when the permissive drops.**

**MAIN-PANEL NEEDS BOTH FIGURES AND THE THIRD ONE THAT IS NOT WRITTEN DOWN: 1.5 A
of pump on top of the chiller's 6 A on the same circuit, AND THE COMPRESSOR INRUSH
STACKS ON TOP OF THAT.**

**DO NOT BUY THE VENTURI OR AIR-FRACTIONATING VERSION OF THIS PUMP. Air in a heat
exchanger is the opposite of what a chiller loop wants.**

## Panel component dimensions. OWNER'S LOOKUPS, 2026-09-23. D-194.

**Eleven lookups run. These are measured or manufacturer figures from the owner, not
derived by any agent.**

### 1. Cord grips. NO MANUFACTURER PUBLISHES A MINIMUM CENTRE-TO-CENTRE. GEOMETRY DECIDES IT.

| Thread | Clearance hole | Wrench flats |
|---|---|---|
| 3/8 NPT | 0.670 to 0.680 in | 0.75 in |
| 1/2 NPT | 0.875 in | 0.95 to 0.98 in |

**USE 1.10 IN C-C FOR 3/8 AND 1.30 IN C-C FOR 1/2. Mixed pair: 1.15 to 1.20 in.**

**The geometric floor is the flat width itself, but TWO ADJACENT DOME NUTS HAVE TO
TAKE A WRENCH.** Across-corners is about 1.15x flats **and that is what collides
first when a nut rotates** - the collision is dynamic, not static.

### 2. Enclosure. 16 BY 12 IS NOT A STANDARD POLYCARBONATE FOOTPRINT.

**Stahlin, Allied Moulded, Integra and Hoffman ALL SKIP IT.** They go 14 x 12 x 6,
then 16 x 14 x 7 or 8. **And the panel is always smaller than the box by roughly
1.25 in each way.**

| Box | Panel |
|---|---|
| 14 x 12 | 12.75 x 10.88 |
| 16 x 14 | 14.75 x 12.88 |
| Hoffman QLINE I 400 x 300 | 14.17 x 10.24 |

> **STRUCK 2026-09-23 BY THE OWNER. THIS BOX WAS NEVER OWNED.**
>
> ~~The box the owner actually holds is a QILISU, overall 425 x 340 x 183 mm, mounting plate 359 x 271 mm.~~
>
> **IT IS A LISTING HE WAS LOOKING AT WHILE SHOPPING. He pasted the drawing and it entered this file as though it were the box on his shelf.** It is a box he CONSIDERED AND DID NOT BUY.
>
> **THE BOX IS THE QILIPSU: overall 508 x 419 x 201 mm, MOUNTING PLATE 468 x 379 mm.** Ordered and delivered. **One box, not two.** F-120 closed, T-030.

**A 16 x 14 step-down gives 375 x 327. A true 16 x 12 gives about 360 x 260 at best,
and that is metric QLINE I rather than a 16 x 12.**

### 3. Wire duct.

Inch widths: 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 6 in. Metric DIN 43659: 25, 40, 60,
80, 100, 150 mm.

**FILL IS 50 PERCENT OF INTERIOR CROSS-SECTION, from NFPA 79 section 13.5.2, NOT
NEC.** Panduit and T&B size their tables to it.

**Knock nominal W x H down to about 90 percent for wall thickness, then fill 50
percent of that.** Catalog shortcut: N = (W x H) / (1.75 x D squared).

**Shop practice designs to 30 to 40 percent so the cover still snaps on. The LIMIT is
50.**

### 4. 94.74SMA socket with 55.34 relay.

Rail occupancy **30 mm**. Height above rail, socket plus relay plus 094.71 metal
clip, **70.5 mm - use 71 mm for cover clearance.**

### 5. Finder 22.32, one module.

Rail occupancy **17.5 mm**. Height above rail **88.8 mm**. Depth off rail **60.8 mm**.
**9 mm air gap to the next 22.32 if ambient over 40 C with contacts over 20 A.**

### 6. NDR-240-24.

**63 x 125.2 x 113.5 mm, W x H x D.** Clearance **40 mm above, 20 mm below, 5 mm each
side, 15 mm from another heat source.**

**VERTICAL MOUNTING ONLY, AC IN AT THE BOTTOM, DC OUT AT THE TOP. ANY OTHER
ORIENTATION VOIDS THE COOLING FIGURES.**

**Vertical budget at full load: 125.2 + 40 + 20 = 185 mm.**

### 7. Terminal block.

**6.2 mm per way** confirmed. **McMaster lists 70 mm overall height INCLUDING THE DIN
CLIP, WHICH IS NOT HEIGHT ABOVE THE RAIL** - equivalent parts at the same pitch give
**44 mm above the rail and 56 mm off the rail face.**

**Use 6.2 mm per way, 70 mm vertical envelope, 56 mm depth. End plates add 1 to 2 mm
outside the pitch.**

### 8. Ground bar. THE PART BOUGHT IS NOT A STANDOFF BAR.

**McMaster 2450K14: a tin-plated copper block, 5.75 x 0.50 x 0.50 in, twelve 1/4-28
tapped holes, 14 to 6 AWG, NO INSULATORS AND NO MOUNTING HARDWARE.**

**It sits on the panel or bolts through its own ends. There is no published
mounting-hole C-C.** If drilled through the half-inch section, **holes must be at
least 5.0 in apart to miss the taps.**

**A true insulated 12-way bar is a 12.5 x 2.5 in envelope at 9 in C-C, and that is
not what is on the shelf.**

### 9. 94.74SMA module and clip together: YES.

**The SMA ships with the 094.71 metal clip and the coil-side slot takes the 99.01
module. Both fit, neither is sacrificed, and the module sits INSIDE the socket
envelope so it adds no height.**

**Do NOT use a 99.02 - that is the box-clamp family. The plastic 094.91.3 clip is
INSTEAD OF the metal one, not in addition.**

### 10. 22 mm device stack depth.

Schneider XB5A with ZBE screw blocks, **measured from the front face of the panel
with the gasket compressed:**

| Rows | Depth |
|---|---|
| 1 | 43 mm |
| 2 | 55 mm |
| 3 | 68 mm |

**A DOUBLE BLOCK IS TWO ROWS. Side-by-side blocks add no depth - only stacked rows
do. Plan 68 mm if three rows are possible.**

### 11. Panel-mount receptacle. A STANDARD 15 A DUPLEX DOES NOT PANEL-MOUNT.

**It screws to a DEVICE BOX by the yoke, strap holes 3.281 in apart, and the body
sits in the box rather than in the panel.** A weatherproof in-use cover mounts to
that box, not through a sheet face.

**What does panel-mount is a SINGLE snap-in 5-15R: cutout 26 x 22 mm, 25 to 33 mm
behind the panel.**

**AND THE BUILD USES DEVICE BOXES, NOT PANEL CUTOUTS: Bell 5320-0 weatherproof boxes
with TayMac covers, mounted to the wall BESIDE the panel and fed by cord grips. SO
THIS LOOKUP CONSTRAINS NOTHING INSIDE THE ENCLOSURE.**

## The five panel devices. OWNER, 2026-09-23. D-200, D-201, D-202.

### 1. Disconnect. NO PART. ZERO RAIL MILLIMETRES.

**A lockable 2-pole building breaker upstream opens both incoming legs together and
can be locked OFF.** OSHA and NFPA 79 care that the source is isolated and locked,
**not that a second isolator sits on the plate.**

**A DIN isolator earns its place ONLY IF a LOCAL VISIBLE open point is needed without
walking to the building panel, or if the two entering circuits are not on the same
2-pole breaker.** Neither holds. **If that changes: ABB SD202/25, 2P 25 A load-break,
35 mm, padlock adapter 2CDD282001R0001.**

### 2. BUS-A overcurrent. Altech 1C15UL. 1P, C curve, 15 A, UL 489, 10 kA at 120 V, 17.5 mm.

### 3. BUS-B overcurrent. Altech 1D15UL. Same family, D curve, UL 489, 10 kA, 17.5 mm.

> **UL 489, NOT UL 1077, IS A REQUIREMENT ON THE LINE AND NOT A PREFERENCE.** A
> supplementary protector is not legal branch protection under the NEC. **The common
> IEC parts - ABB S201-C15, Schneider M9F11115, Eaton FAZ-C15/1 without the NA suffix
> - are all UL 1077, many fully rated only two-pole at 240 or 415 V with the
> single-pole 120 V interrupt weaker or unlisted.**

**THE D CURVE DOES NOT SOLVE THE UNKNOWN LRA. It moves the magnetic wall from 5-10x
to 10-20x, which on 15 A is 150 to 300 A.**

| Fault current | What happens |
|---|---|
| 7.5 A continuous, 0.5x In | **The thermal element never moves** |
| Under 150 A | **Will not instantaneous trip** |
| 150 to 240 A | **May or may not. Nuisance trip on a sticky start is possible** |
| Over 240 A | Clears under 100 ms - **a stall rather than a start** |

A small 120 V hermetic LRA is typically **4 to 8 times compressor FLA for 50 to 200
ms**. A C curve starts tripping at 75 A, so D is right **and it is not unlimited
headroom.**

**SO THE COMPRESSOR NAMEPLATE READING DECIDES WHETHER THIS BREAKER IS CORRECT. If the
measured LRA is over 120 to 150 A, the answer is a larger breaker sized to the wire,
or a motor-rated protector.**

### 4. R-PI fuse holder. Phoenix Contact PT 4-HESILED 250 (5x20), or spring-cage ST 4-HESILED 250, order 3036563. 6.2 mm rail.

**THE INDICATOR HAS NO MINIMUM LOAD CURRENT, BECAUSE THE LAMP SITS ACROSS THE FUSE
AND NOT IN SERIES WITH THE LOAD.** Fuse good, LED shorted out, dark. **Fuse open, full
120 V across the LED and its resistor, lamp lights.**

**So the Pi brick's 0.23 A is irrelevant, and when the fuse blows the load current is
ZERO and the lamp still sees 120 V.** The datasheet's 0.4 to 0.95 mA is **LEAKAGE
through the indicator while the fuse is open, not a lighting threshold.**

**USE THE 250 V VERSION. A 24 V LED version dies on 120 V.**

### 5. KM-CHIL. ABB AF09-30-10-13, 45 mm rail. Alternative Schneider LC1D09G7, same width.

**THE FINDER 22.32 IS THE WRONG PART AND THE NUMBERS SHOW WHY: its 25 A is AC-1
RESISTIVE, its AC-3 motor rating is typically 8 A or less, and it is not built for
compressor make and break.** The load is **8.7 A** - 7.2 A compressor FLA at 1/3 HP
115 V, plus 1.5 A pump.

| | AC-3 | AC-1 | Listing |
|---|---|---|---|
| AF09-30-10-13 | 9 A | 25 A | UL 3/4 HP at 120 V, **coil 100 to 250 V AC or DC** |
| LC1D09G7 | 9 A | 25 A | 1/3 HP at 115 V, 120 V coil |

**COIL DROP-OUT DECIDES IT AND IT FAVOURS THE ABB. A standard AC magnet coil chatters
and can WELD on a brown-out** - TeSys D pulls in at 0.85 to 1.1x Un and drops out at
0.3 to 0.6x Un. **The ABB electronic coil operates across 100 to 250 V, stays sealed
to about 100 V, then opens cleanly.**

**Take the ABB: it REMOVES the failure mode rather than tolerating it.**

**KM-CHIL STAYS BLOCKED on the open rung that decides its coil's bus.**

### On the shelf, and candidates rather than the specification

**Control Gear CGMB1C15 (1P 15 A C) and CGMB1D15 (1P 15 A D), both delivered, plus a
CGMB1D06.** So BUS-A and BUS-B may need no purchase - **but whether they are UL 489
or UL 1077 is UNKNOWN, and by the requirement above that decides whether they are
usable.**

**Also on the shelf: Conta-Clip 2190.2 DIN fuse holder, 5 x 20 mm, with a 2046.2 end
plate and five 3 A glass fuses. NO INDICATOR.** It is the part the parallel build
specified before anyone asked for one.

