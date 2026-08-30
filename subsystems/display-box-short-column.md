# DISPLAY-BOX: the short column, G-22's second half

Returned 2026-08-30. No file changed. Stopped part-way, not declared finished.

## The structural result, which outranks any row and limits G-22 as worded

> **For an optocoupler sense loop, SEVERED and SHORTED-TO-AN-ENERGISED-NEIGHBOUR
> fail in OPPOSITE directions, always. Severed extinguishes the LED. A short to a
> live neighbour lights it. You can choose which of the two is the safe reading.
> YOU CANNOT MAKE BOTH SAFE.**

That holds identically for S-08, S-03 and S-20, because all three are the same
given topology. **It is not a defect in the topology - no two-state sense line can
report three states - but it is a limit on G-22 as worded.** See findings F-028 and
D-049.

What follows, and it is the useful half:

1. **Choose the severed case as the safe one, on frequency.** A pulled cable, a
   broken strand, a backed-out terminal and a corroded crimp are ordinary. An
   insulation failure to one specific energised neighbour is not. That is the
   choice already made for S-08 and it is the right one.
2. **The short case is then managed by ADJACENCY, not by circuit design** - which
   conductor sits next to which, in which jacket, in which duct. **That moves it out
   of DISPLAY-BOX and into MAIN-PANEL's duct plan and INTERCONNECT's cable schedule,
   and it is the reason those two pieces of work are load-bearing on G-22 rather
   than merely tidy.**

**Severed is answered by the circuit. Shorted is answered by the wiring plan.**

## What each signal is next to, and who knows

| Domain | Contents | Who knows the adjacency |
|---|---|---|
| Main panel interior | MAIN-PANEL's classes A, B, C, two vertical wireways | MAIN-PANEL, returned |
| Panel to display box, 4 ft | Five coil-drive pairs, S-08, S-03 and S-20 sense pairs. **Every conductor is 24 V class** | INTERCONNECT. Schedule OPEN, pair assignment does not exist yet |
| Display box to pump boxes, 4 ft and 6 ft | 8 STEP, 8 DIR, the VDD feed and its return, on the same wall as P-06 | INTERCONNECT for the duct, PUMP-BOXES inside the gland |
| Display box interior | Five 24 V-class conductors landing beside 3.3 V logic and the optocoupler barrier | DISPLAY-BOX |

**One adjacency stated as fact rather than guess**, from the printed pin list in
parts.md: **VDD and VM are two positions apart on one screw terminal block,
separated only by GND. That is the closest approach between the 5 V rail and the
24 V motor rail anywhere in this build, and it is a screw terminal, not a trace.**

## The sweep, both columns

| Signal | Severed | Shorted to its realistic neighbour | Safe? |
|---|---|---|---|
| S-08 readback | Reads open, reads a drop | Pair to pair: bypasses the LED, reads open, same as severed. **To a live 24 V neighbour: forces the LED on, reads contactor CLOSED** | Severed safe. Pair-short safe. **Short to a live neighbour UNSAFE while commanded on: it masks a real drop** |
| S-03 fill contact | Reads not filling | As S-08 | Severed now closed by inversion, D-042. Short inherits that answer |
| **S-20, K-DRY pole, new** | Reads de-energised | As S-08 | **Establish before wiring, do not inherit. See below** |
| EZO pH, EC | Datasheet | Datasheet, plus the carrier isolation question | Cannot answer |
| EZO RTD | Datasheet | **No carrier, so no isolation barrier between its field cable and the shared I2C bus** | Cannot answer, **and it is the asymmetric one** |
| S-07 coil drive | Coil drops. Safe | Node to +24 V: coil sees no potential, de-energises. **Node to 0 V: coil energised permanently and the Pi cannot drop it** | Severed safe, short-to-rail safe, **short to 0 V unsafe, and F-019's requirement is exactly what contains it** |
| S-09, four drives | Coils drop. Safe | As S-07 | Same, **and G-03's hardware seal-in is what makes a stuck-on fill survivable** |
| S-10 STEP x8 | Floating CMOS input, F-018 | **To another STEP: two heads step together.** To a static rail: probably one step, datasheet-dependent. **To a switching conductor: edges, and edges are steps** | Severed unsafe. **STEP-to-STEP unsafe and it is the most likely adjacency of all** |
| S-10 DIR x8 | Floating, direction undefined | To another DIR: benign if all channels run one way. **To a live rail: direction inverted, head reverses** | Unsafe, **and the same single decision fixes both columns** |
| P-09 VDD | Driver deaf, motion safe. Short can brown out the Pi | **To VM at the driver terminal block: 24 V onto the 5 V rail and onto the Pi's own supply** | **UNSAFE, and F-020 needs sharpening from overcurrent to OVER-VOLTAGE** |
| All outputs, boot | High-Z, needs physical pulls | Unchanged | Safe only with physical pulls |

## The one short that defeats G-09 by itself

MAIN-PANEL's class C contains the S-03 and S-08 optocoupler branches and their
burdens **plus the coil-drive pairs from the display box**. The 4 ft wall cable is
the same population. **So in both the duct and the jacket, the permissive coil
drive S-07 and its own readback S-08 are same-class neighbours.**

> **A short between the S-07 conductor and the S-08 sense conductor makes the
> readback follow the command.**

That is precisely and only the failure G-09 exists to detect, and parts.md's
standing rule is defeated in hardware by one fault **with software behaving
perfectly**. Worse in the D-030 direction: **it removes weld detection, because
readback-closed-while-commanded-off can no longer occur when the readback is
stapled to the command.**

**Class separation does not address it, and this is the gap in an otherwise sound
scheme: MAIN-PANEL's classes separate by voltage and by power-versus-signal, which
is right for shock and for noise. Command and readback are the same class as each
other. Any scheme that sorts only by class puts them together.**

Requirement, costing nothing before the schedule is written and a re-pull after:
**the permissive coil drive and the S-08 readback shall not share a pair, shall not
be adjacent within a bundle, and preferably shall not share a jacket. It is the one
conductor pair in this build whose INDEPENDENCE IS THE DELIVERABLE.**

## S-20, established rather than inherited

The first of the three sense circuits to arrive AFTER F-017, so the lesson can be
applied before anything is wired. **S-20 exists to un-silence exactly what
MAIN-PANEL's fourth reason for G-25 names: a hardware drop is silent and the Pi
goes on believing the loop is turning.**

- **Severed reads the de-energised state. If the wiring is arranged so that
  de-energised means K-DRY not tripped, a severed S-20 reads HEALTHY and
  re-silences the very failure the signal was created to make audible.** F-017's
  shape, in a new row, avoidable because nothing is built.
- **Requirement: the loop must be ENERGISED WHEN CIRCULATION IS PROVEN**, so a
  severed cable, a dead LED, a lost 24 V wetting or a failed pole all read tripped
  or not-proven. Never healthy. **A false stop here is cheap. A false healthy is the
  thing G-25 was written against.**
- **Short, pair to pair: bypasses the LED, reads not-proven. Same direction as
  severed. Safe** - and that follows directly from the polarity choice. **One choice
  makes both the severed case and the likelier short case safe, which is better than
  S-08 manages.**
- Short to a live neighbour: reads proven. Unsafe, and the adjacency plan carries it.

**S-20 is the cheapest row on the list to get right, because it is the only one
where nothing has been wired yet.**

## S-10, and the requirement that collapses both columns into one

**What DISPLAY-BOX will not state:** whether STEP is edge-triggered or
level-sensitive, which edge, minimum pulse width, and whether there is an input
filter. Those four decide whether a static short to 5 V is one step or continuous
running, and they are datasheet facts.

**What it can say without the datasheet: a hard DC short to a static rail is not a
clock. The dangerous shorts on STEP are the ones that produce EDGES** - a
chattering or intermittent short, and a short to a conductor that itself switches.
And the likeliest source of edges is the obvious one:

> **STEP shorted to another channel's STEP means two heads step together. That
> violates G-06 IN HARDWARE, where software cannot prevent it, and G-06 is a
> THERMAL constraint. It also doses a channel the books never decrement.**

Eight STEP conductors in one jacket makes that the single most probable short in
the build.

**The requirement, and it answers both columns at once: pair every STEP and every
DIR with its own return conductor, so the nearest neighbour of every signal
conductor is a ground return rather than another signal.** The realistic adjacent
short then pulls the signal LOW - no clock, no motion, the safe direction - instead
of coupling two channels. Twisting each pair also buys the noise immunity the
severed column already needed.

**The cost, not hidden: S-10 goes from 16 conductors to 32.** INTERCONNECT's cable
and gland fill, PUMP-BOXES' terminal count, and **cheaper now than after the cable
is bought.**

**And the two columns converge on one decision.** The severed column required pull
resistors holding DIR to the forward direction; the short column requires that a
conductor pulled low also means forward. **Both are satisfied by the same choice:
the resting, failed and shorted-low state of DIR must be the direction that pumps
into the manifold.** One decision, two failure modes, no conflict.

## P-09, sharpened from over-current to over-voltage

**VDD and VM are two screw terminals apart on every one of the eight drivers,
separated by GND. A slipped strand, a mislanded conductor or a loosened terminal
puts 24 V directly onto the 5 V feed, which runs back 4 ft or 6 ft onto the Pi's own
unswitched supply. A fuse sized for overcurrent does not protect against a 24 V
source applied to a 5 V rail. It may not even open.**

Sharpened requirement: **protection at the display-box end that survives an APPLIED
OVER-VOLTAGE, not only an over-current.** And it is a build-step requirement as much
as a circuit one, which is where T-008 and T-009 live: **the landing order on the
driver terminal block, verified per driver, counted at landings rather than at
jackets.**

The series resistors already required on STEP and DIR do double duty here. **One
mitigation, two failure modes.**

## The RTD, and what the isolation reasoning does not cover

parts.md's reason that RTD needs no carrier is about the SOLUTION path and is sound
on its own terms. **It does not address a short in the probe cable or at the
fitting.** The PT-1000 leads run from the manifold, through the duct, into the box
and onto a circuit sharing the I2C bus with pH and EC, **with no isolation barrier
anywhere in that path. pH and EC each have one. The RTD does not.** And one bus
failure removes all three process measurements at once.

Whether that matters depends on what the probe cable runs next to, **which
DISPLAY-BOX does not know and will not assume.** INTERCONNECT's, whose file already
lists probe-cable separation as open. Named as a question with an owner.

## Confirmations, stated as confirmations

1. **The optocoupler isolation holds.** No short on the panel-to-display cable can
   put 24 V into the Pi. **Worth naming precisely: ISOLATION PROTECTS THE PI, IT
   DOES NOT PROTECT THE TRUTH.** Every unsafe short in this column falsifies a
   reading; none damages the controller. Chosen, not lucky.
2. **The panel-to-display cable is class-homogeneous**, so **there is no cross-class
   short available in that jacket at all.** That falls out of burdens-in-the-panel
   and contacts-wetted-at-24 V, decisions made for other reasons.
3. **MAIN-PANEL's two-wireway, three-class arrangement is sound for what class
   separation can do.** Checked against every signal landing on the board. Its one
   gap is the command/readback adjacency, which no class scheme can catch.
4. **G-03's hardware fill seal-in backstops a shorted fill relay drive.** A drive
   shorted to 0 V energises its relay permanently and the Pi cannot drop it, but the
   stop float is in the hardware chain so the fill still terminates. **A decision
   made for level control contains a display-box output fault. Worth having written
   down before anyone simplifies the chain later.**
5. F-019 already contains the shorted-output case. No new requirement.
6. The DIR polarity decision covers severed and shorted with one choice.

## PL-Y, one line, not DISPLAY-BOX's

MAIN-PANEL's option 2.7 measures **the same physical fact S-08 reports to the Pi, by
a wholly independent path**: no contact, no optocoupler, no cable, no computer.
**That is an independently-failing corroborator of the S-08 reading - the property
CONTROL-SOFTWARE wanted from DIAG, and it partly de-fangs F-011 for the human
standing at the panel. A benefit of MAIN-PANEL's proposal nobody had named.**

## Requirements returned

| # | Requirement | Owner |
|---|---|---|
| 1 | STEP and DIR each paired with a return conductor. **16 becomes 32** | INTERCONNECT, PUMP-BOXES |
| 2 | S-07 and S-08 not paired, not adjacent, preferably not one jacket | MAIN-PANEL duct, INTERCONNECT cable |
| 3 | S-20 energised when circulation is proven, so every failure reads not-proven | MAIN-PANEL, blocked on WATER's S-05 |
| 4 | VDD feed protected against applied over-voltage, not only over-current | DISPLAY-BOX |
| 5 | Driver terminal landing order verified per driver | PUMP-BOXES, T-008 and T-009 |
| 6 | 24 V-class landings segregated from Pi-side copper inside the box, barrier creepage preserved | DISPLAY-BOX |
| 7 | Whether the PT-1000 leads share a duct with anything energised | INTERCONNECT |
| 8 | **Whether the Pi drives the two fill coils at all** | MAIN-PANEL and CONTROL-SOFTWARE, through BOSS |

**C-19 as written tests the severed column only.** Testing the short column means
deliberately shorting a conductor to a live neighbour on a built panel, which is a
second and more invasive procedure, and DISPLAY-BOX would not propose it without
the owner ruling on whether it is safe to perform.
