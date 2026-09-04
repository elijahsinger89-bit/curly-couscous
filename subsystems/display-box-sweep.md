# DISPLAY-BOX: the G-22 fail-safe sweep, S-12, and the watchdog

Returned 2026-08-30, first invocation. No file changed. Stopped part-way, not
declared finished. Census taken from the interface rows and subsystem files named
in its report; DIAG and INDEX are discussed in control-software-p09.md but **no row
lands either at a Pi input**, so they are not in the census. That is a statement
about what was read, not an absence claim about the build.

## The finding that matters most: S-03's fail direction was ASSERTED, not established

The S-03 row said a severed cable reads as contact open, which is the safe state,
and that this is a chosen property. **The first half follows from the circuit. The
second half was never established for S-03. It was inherited from S-08, which is
precisely what G-22 exists to forbid.** BOSS wrote it. See findings F-017.

- On S-08, contact open means THE PERMISSIVE DROPPED. Stop, loud. Safe by D-030.
- On S-03, contact open means **NO DAY TANK FILL IS IN PROGRESS.** Whether that is
  safe depends entirely on what software does with it, and that question has been
  open since the F-004 pass: whether a dose may start while a fill is in progress.

If the answer is the expected one, do not dose during a fill, then as currently
sensed:

> **A SEVERED CABLE READS AS PERMISSION TO DOSE.**

That is the unsafe direction, and under G-22 that is a defect, not a tolerance.

**The direction is cheap to reverse before the contact is wired and a rewire
after.** Take the sense from the complementary pole so the loop is energised when
NO fill is in progress. Then LED on and Pi low means clear to dose, and a severed
cable, a dead LED or lost 24 V all read as "filling", which blocks a dose. Same
topology, same 12.5 mA sizing under G-23, one different pole. **It costs a pole
out of a budget D-037 already says is tight**, so it is MAIN-PANEL's and the
owner's call.

**It cannot be settled until the owner answers the dosing-during-fill question.
That one answer determines which direction is safe, and the wiring must follow the
answer rather than precede it.**

## The sweep

| Signal | Severed cable | Safe? |
|---|---|---|
| S-08 readback | Reads contact open, reads a drop | **Safe.** False stop. Confirmed |
| S-03 fill contact | Reads "not filling" | **UNRESOLVED, and unsafe for the expected use.** F-017 |
| EZO pH, EC, RTD | Unknown, datasheet | **Cannot answer.** Requirement and search terms returned |
| S-07 permissive coil | Coil drops, VM removed | **Safe**, conditional on where the coil positive comes from. See F-019 |
| S-09, four relay drives | Coils drop, loads off | **Safe.** No readback exists on any of the four |
| S-10 STEP, eight of them | Floating CMOS input on an enabled, powered driver | **UNSAFE.** Not "no steps". F-018 |
| S-10 DIR, eight of them | Floating input, direction undefined, head may reverse | **UNSAFE.** F-018 |
| P-09 VDD feed | Driver goes deaf, motion safe. But a short can brown out the Pi | Motion safe, **supply path unsafe.** F-020 |
| All outputs, boot window | Pins high-Z before software | **Safe ONLY with physical pulls, never software pulls** |

### Inputs, detail

**S-08.** Safe as recorded. Two things added. A **short** across the sense pair or
an optocoupler transistor failed on holds the input low, reading contact closed.
Commanded off that latches a weld, loud and safe. **Commanded ON it reads healthy
while the contactor may be open: the Pi then clocks eight channels into drivers
with no VM, delivers nothing, and books the volume under G-04.** Silent
under-delivery, and nothing else catches it on the fulvic channel. And: the
optocoupler transistor PULLS LOW, so something must hold the line high, and **it
must be a physical resistor, not an internal Pi pull configured in software.
Before software runs the pin is high-Z and an internal pull is unconfigured, so
the fail-safe property does not exist during boot unless the pull is a component.**
Same at S-03.

**The three EZO circuits.** A severed probe cable is a different question from a
severed signal cable and DISPLAY-BOX will not answer it from memory. **Requirement:
a disconnected or failed probe must be distinguishable at the Pi from a plausible
in-range reading. If it is not, the failure is unsafe, because a plausible wrong pH
is what an operator sizes a dose against.** Search: Atlas Scientific EZO pH circuit
disconnected probe reading error response; Atlas Scientific EZO EC probe
disconnected output; Atlas Scientific EZO RTD PT-1000 open sensor reading. The
PT-1000 is where a guess is tempting: an open element is a resistance excursion in
a known direction, but **what the circuit REPORTS for it is the circuit's
behaviour, not Ohm's law.**

**Common-mode point nobody had written down: all three circuits sit on ONE I2C bus.
A single shorted or broken SDA or SCL removes pH, EC and temperature
simultaneously. The three process measurements are not independent failures.** Safe
if and only if a failed read is never presented as a value: **a stale last-good
reading served as current is the unsafe direction, and it is parts.md's
commanded-versus-measured rule in a second costume.** The discipline is
CONTROL-SOFTWARE's; the hardware fact is DISPLAY-BOX's and is handed over.

Also: the ISCCB-2 carriers isolate pH and EC on the SOLUTION side, which is why RTD
needs none. **Whether they also isolate the I2C side is a carrier property nobody
has stated.** Search: Atlas Scientific ISCCB-2 isolated carrier board I2C isolation
data lines.

**The touch display.** Internal, so no wall cable severs it. A dead display removes
the only route by which a fault stops and tells the operator under G-16. It
energises nothing so it is not unsafe in G-22's sense, **and the offset is already
designed in: PL-R and PL-G are driven from relay poles, so the panel still states
its condition with the computer dead.**

### Outputs, detail

**S-07, the permissive coil drive.** Severed cable or severed shared common means
the coil de-energises, the contactor drops, VM is removed. **Fail-safe by
construction, because its safe state is de-energised and a break de-energises.** It
also self-reports: a break while commanded on shows at S-08 as an apparent drop.

**The unsafe failure is not the severed cable, it is a SHORTED OUTPUT DEVICE**,
which energises the coil regardless of what the Pi wants. Whether that can defeat
G-07 depends on something nothing on file states: **where the coil positive is
taken from.** Downstream of the master latch, a shorted transistor still cannot
hold it in when the chain opens and G-07 holds. **From raw 24 V, a single shorted
transistor on the logic board holds the permissive contactor closed against a leak,
an E-stop or a lost interlock, which is a direct violation of a frozen row.**
Findings F-019.

**S-09, four relay coil drives.** All four fail off, and off is safe for each: a
fill that fails to start is safe, a fill that fails to stop is not; transfer pump
off is safe; **manifold pump off is electrically safe and DISPLAY-BOX refused to
dress it up as free** - G-11's mixing stops, which corrupts any open settle window
and lengthens the interval per F-004, a run in progress must be recorded as not
completed under G-20, and injecting into a static manifold is DOSING's to rule on;
chiller off is safe and D-027 says the duty is low anyway.

**All four have NO readback.** G-09 gives one to the permissive contactor only. So
commanded state is the only state that exists, parts.md forbids presenting it as
measured, and **a severed relay drive is invisible to the Pi forever.** Not a defect
in the severed direction, but the reason nobody will ever notice one.

**One common conductor takes out all five coil drives at once**, all in the safe
direction, simultaneously and invisibly. Whether the common is shared or per-drive
is a deliberate cost decision for MAIN-PANEL and INTERCONNECT.

**The unsafe direction for all five is the BOOT WINDOW, not the cable. Every coil
drive output stage must be held de-energised by a PHYSICAL PULL-DOWN on the logic
board, not by a software-configured internal Pi pull.** The GPIOs are high-Z at
reset and during boot, which is exactly the window before any software exists to
configure anything. **This is also what makes the watchdog rule "must not come up
with the permissive coil commanded" physically true: during a watchdog reset the
pins go high-Z and the physical pull is the only thing holding the contactor off.**

**S-10, STEP and DIR, sixteen outputs. This is where the sweep found the unsafe
direction, and it is the third case the brief was looking for.**

The tempting answer is that a severed STEP means no steps, so it fails safe. **That
answer is wrong, and it is wrong for reasons already in parts.md and D-032.**

- A severed STEP leaves a **CMOS input on the driver undriven.** The 6121 is
  non-isolated CMOS: no opto, no differential pair, nothing that defines the pin
  when the conductor is gone. An undriven CMOS input floats.
- **EN is unwired and the driver defaults ENABLED, permanently, per G-21. VDD stays
  live through a permissive drop per D-031.** So the driver is listening, powered
  and enabled, with a floating input.
- The cable runs alongside 24 V motor conductors carrying 1.0 A per driver.
- **So a severed STEP line is not "no motion". It is an undriven input on a live,
  enabled driver, and coupled noise can clock it.** Software has no per-driver
  disable, ever, so the only backstop is the permissive removing VM from all eight
  at once. **That is the residual D-032 recorded rather than argued away, and this
  is where it lands.**
- **A severed DIR is worse.** Floating DIR on an enabled driver means the direction
  is undefined, and a dosing head that runs backwards draws from the manifold
  toward the jug or pushes tank liquid up the suction line. **Nothing measures
  direction, nothing measures delivery under G-04, and the books decrement as
  though it dosed forward under G-05.**

**The fix has to live at the driver end, inside the pump boxes: pull resistors on
STEP and DIR sized against the driver's input thresholds. A pull at the display end
does nothing once the conductor is cut, which is the whole point of the failure.**
That makes it PUMP-BOXES' component on their side of the gland. The polarity of the
DIR pull is a chemistry-facing decision, which direction is "into the manifold",
and belongs to PUMP-BOXES and DOSING between them. **Separately and additionally**,
the display end needs a low-impedance drive for noise immunity over 4 ft and 6 ft
alongside motor conductors. **Both, not either, and they are not substitutes.**

Search: TMC2209 datasheet STEP DIR input logic threshold VIH VIL; TMC2209 datasheet
input pin internal pull-up pull-down STEP DIR EN; Adafruit 6121 TMC2209 breakout
schematic STEP DIR input pull resistors. **Two documents, per PUMP-BOXES' standing
point. If the breakout already fits pulls this may cost nothing; if not it is eight
or sixteen resistors, and nobody has established which. Do not assume the friendly
case.**

**A residual on STEP that no resistor fixes:** a severed STEP that genuinely
produces no motion is caught by the EC check or the pH check as no movement, which
stops the batch loudly. **Except on fulvic, which S-17 closed as permanently
unattributed. A severed STEP on the fulvic channel is a silent no-delivery with the
books recording a delivery.** That is F-001's existing shape, not a new defect, and
D-013 says do not solve it. Recorded so it is not rediscovered as new.

**P-09, the 5 V VDD feed.** Severed VDD makes the driver deaf, so **the motion
direction is safe**; the books still record a dose that did not happen, same
invisible under-delivery, same fulvic hole.

**But the severed case recreates the exact state D-031 forbids, one driver at a
time.** D-031's reason 2 was that 5 V buffer outputs driving STEP and DIR into pins
whose VDD is zero is an overdrive through the input protection diodes. D-031
prevented that for all eight on every drop. **A broken VDD conductor recreates it
for the drivers downstream of the break, and nothing prevents it.** Mitigation is
DISPLAY-BOX's and cheap: series current limiting on STEP and DIR, sized so a driver
with no VDD cannot be back-fed through its protection diode.

**And the unsafe direction nobody had named: this conductor can take the Pi down.**
VDD comes off the Pi's own 5 V rail, unswitched, and runs 4 ft and 6 ft into two
boxes containing eight drivers and eight motors. **A short on that conductor, or one
driver failing short on VDD, browns out the controller from 6 ft away. The Pi is
deliberately independent of the permissive precisely so it survives a drop and can
log it, and this conductor is a path by which a pump-box fault defeats that.**
Requirement: current limiting or fusing on the VDD feed at the logic board, per run
at minimum. Findings F-020.

## G-22 has no check behind it

**Nothing in commissioning.md tests a fail direction.** All eighteen rows read.
C-18 exercises the permissive-drop state, which is adjacent and is not this. **G-22
is currently a design claim with no check, and per T-014's lesson a claim nobody
tested is a claim nobody has.** The cheap version disconnects each sense conductor
in turn, at the gland, and records what the Pi reports. No instruments. Now
commissioning C-19.

## S-12, the map

**The map is not a list of pin numbers. That is the shape that lets it be wrong
quietly.** Four columns per signal, three specifiable today:

1. **Signal name**, from the interface table, never a position or an index.
2. **Direction**, in or out.
3. **Asserted sense at the Pi. Both given sense circuits are INVERTED: contact
   closed means the input goes LOW. That inversion is a property of the map, not a
   software convention.** A map that omits it lets CONTROL-SOFTWARE assume
   active-high and hand the operator a fill state or a permissive state that is
   exactly backwards.
4. **State before software runs.** Every output is high-Z plus a physical pull, and
   the pull's direction is part of the map.

Pin numbers fill column 5 when the lookups come back.

**Section A, per-channel, keyed by the channel token.** CH1 to CH8, canonical form,
one record per token, STEP pin and DIR pin. Committed in advance: **if the header
forces a non-monotone pin order, the pins come out non-monotone and the tokens stay
exactly as they are.** Box and cable core are NOT in this table: they are
PUMP-BOXES' and INTERCONNECT's attributes of the same token, recorded once each in
their own place. **Duplicating them here would create a second place for them to
disagree, which is the translation table channel-token.md forbids.**

**Section B, seven named discrete signals**, all defined in shape and blocked on
pin numbers: permissive coil drive out, permissive readback in and inverted, fill
in progress in and inverted with its sense contingent on F-017, and four relay coil
drives out.

**Section C, I2C.** Three circuits on one bus, pH and EC on carriers, RTD on none.
Addresses blocked twice over: they are datasheet facts, and **C-14 must happen
first because the circuits cannot be seen on the bus at all until the jumper
procedure is done. And the mode pin differs by circuit type, so C-14 is THREE
DIFFERENT PROCEDURES, not one repeated three times.** C-14 must record which pin
and which procedure was used for each circuit individually, **or nobody can repeat
it after a board swap and the next person applies the pH procedure to the RTD
circuit.** A collision risk to check rather than assume: if two or three circuits
carry the same default address the map cannot be written until they are separated,
and separating them happens before the box is closed.

**What blocks the rest:**

1. The Pi 5 header: which pins are GPIO and **what each does at boot**. The
   boot-state half is load-bearing on the whole output sweep.
2. **The header budget, and it may be the binding constraint.** The census needs 16
   STEP and DIR, plus permissive coil, readback, fill contact and four relay
   drives: **23 GPIO**, plus I2C, plus a watchdog feed, plus whatever the display
   consumes. **If it comes up short, the shortage must fall on the slow signals and
   NEVER on STEP. An I2C GPIO expander cannot carry a step clock: step timing is
   real-time and an expander puts a bus transaction in the middle of it.** Stated
   now so that if the budget bites it is not resolved by whatever is easiest at the
   time.
3. What the 7 in display consumes, and whether its touch controller shares an I2C
   bus with the EZO circuits.
4. **The DIAG and INDEX ruling, and this decides whether freezing S-12 now is worth
   doing. If either is landed, S-12 grows by up to sixteen inputs and the header
   budget question changes completely. Freezing S-12 before that ruling means
   freezing a map known in advance to need reopening.**
5. **Whether an RTC is fitted.** If it is, it is on I2C, it takes an address, and it
   belongs in section C. Settle before the freeze.
6. CONTROL-SOFTWARE's confirmation of the census.

## The watchdog, hardware side

1. **External to the Pi.** A watchdog whose timer and reset path both live inside
   the SoC that is hung is being asked to recover a hang it is part of.
2. **Its lever must be a real reset.** P-07 closes every other route. **If no
   external reset input is available on a Pi 5, the watchdog as specified cannot be
   built and P-07's "watchdog is the only recovery path" becomes an open item
   rather than a plan.** Worth checking early. Search: Raspberry Pi 5 reset pin
   external reset header.
3. The feed is a GPIO output the sequencer physically toggles: one more claim on
   the budget.
4. **It must require TRANSITIONS, not a level. This is the hardware half of D-033
   and without it the software discipline buys nothing: A HUNG PI HOLDS ITS LAST
   OUTPUT LEVEL. A watchdog satisfied by a static high is fed forever by a dead
   process** - the same literal-True failure D-033 was written to prevent, moved to
   the hardware side where nobody would look for it. A windowed watchdog, faulting
   on too-fast as well as too-slow, additionally catches a tight retry loop
   spinning the feed.

Two consequences of rules already written: **if the watchdog can present an "I
reset you" indication at boot, a reset becomes MEASURED**; without it the Pi infers
a reset from its own uptime and cannot distinguish a watchdog reset from an
operator reboot from a power cut, three events and one indication. And **the
physical pull-downs are the only thing holding the contactor and the four relays
off through a reset and through boot.** The watchdog requirement and the output
sweep are the same requirement seen from two directions.

**No commissioning row exercises a watchdog. A watchdog nobody has watched fire is
the silent-loop case waiting to happen.**

## The clock, closed to one lookup

**No file states one exists and no file states one does not.** DISPLAY-BOX searched
every markdown file for RTC, real-time clock, clock and battery: the only hits are
the EZO RTD circuit, which is a temperature circuit. Whether the Pi 5 carries an
RTC and whether it needs a battery fitted is a hardware fact it will not state.

**What is settled without waiting for that answer:**

- **The clock question and the settle-window question are two questions and have
  been travelling as one. An RTC does NOT rescue a settle window across a restart.**
  A reset mid-window means the window is destroyed, recorded as destroyed and not
  as a gap, and that holds whether or not the wall clock survived. **So
  CONTROL-SOFTWARE's interim discipline is not a workaround waiting on hardware. It
  is the rule.**
- **What the clock buys is the RECORD, not the arithmetic.** Under G-20 every run
  that turns a head records whether it completed, and those records are read a
  season later. C-16, C-13, C-01 and C-09 all produce records whose date is part of
  their value.
- **The two are separable and only one needs hardware. Interval arithmetic within
  one uptime wants a MONOTONIC clock, which needs no RTC and cannot be stepped by a
  network time correction mid-window** - a real hazard for interval arithmetic done
  on wall time. **CONTROL-SOFTWARE can and should use a monotonic source for every
  interval today, regardless of how the RTC question resolves.** That is the useful
  half and it is available now.
- Whether the Pi has any network path at all is not stated in any file, so time
  arriving from a network after a boot cannot be assumed.

---

> **ANNOTATION 2026-09-03, D-122. NOT A REWRITE OF WHAT DISPLAY-BOX RETURNED.**
>
> **This file says "the fulvic channel" twice, at the two places about a silent
> no-delivery. There is no fulvic channel.** Under D-105 role is a per-channel
> setting and under D-122 fulvic is a PRODUCT, not a role: it is a nutrient by
> role, and not moving EC meaningfully is a product attribute in the channel
> register.
>
> **So the sentences stand in substance and their subject moves: the channel that
> is silent is whichever channel is ASSIGNED fulvic, and which channel that is
> comes from C-09.** The finding those sentences carry - that a severed STEP there
> is a silent no-delivery, and that nothing else catches under-delivery on it - is
> unaffected and is not softened by this.
>
> **The file is left as DISPLAY-BOX returned it because a returned answer is a
> record of what an agent said, not a working document. BOSS annotates and does not
> edit.** The corrected wording is in interface-table.md S-17.
