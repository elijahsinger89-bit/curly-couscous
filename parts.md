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
- **EN unwired leaves the driver ENABLED.** Default state is on, not off.
- Set the Vref pot with a meter before any power is applied.
- Each driver needs a stick-on heatsink.

## Motor current

- 1.0 A per driver, which is 71 percent of the part's rating.
- Eight drivers is 8.0 A worst case connected on the 24 V rail.
- **Standstill current has never been measured** and is currently assumed at 30
  percent of running. That is an assumption, labelled as one. Commissioning C-13.

## 24 V supply: Mean Well NDR-240-24

24 Vdc, 10 A, 240 W.

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

| Box | Size | Note |
|---|---|---|
| Main panel | roughly 20.7 by 16.6 in | |
| Two pump boxes | 16 by 8 by 6 in, already owned | Sealed. Heads pass through the lids |
| Display box | roughly 300 by 250 by 130 mm | NEMA 4X polycarbonate, gasketed display cutout |

**Plastic gives no bonding path, so every equipment ground lands on a ground bar
rather than on the box.**

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

## The Pi is powered independently of everything else

Its receptacle is **fused and NOT relay switched**. The Pi has power whenever the
panel does.

- **It stays alive through a permissive drop and can log and alert on it.** No
  software may assume it loses power with the system.
- **Nothing in the panel can power cycle the Pi.** It reboots by software or by
  killing the panel, **so a watchdog is the only recovery path.**

## The permissive readback

The Pi drives the driver-permissive contactor coil AND reads back a real auxiliary
contact on that contactor, so it can tell commanded state from actual state.

It exists specifically to catch a welded contact, where the Pi commands the rail
off and eight drivers stay live.

**Do not let software report commanded state as measured state anywhere.**

## Not known, and not to be invented

The KPHM400-ST flow rate per revolution, its tube size and its barb size. Every
part number, quantity and size not stated in this file. Ask the owner.
