# WATER: the float requirement, the overflow and air gap price, F-103 and F-102

Returned 2026-09-04. Written in one pass at the end, per the invocation discipline.

Names used are the current ones: the MANIFOLD PUMP per D-144 and G-42, and fluid
interface rows FL-nn per D-145 and G-43.

**F-104 is not addressed here. The owner has closed it, the leak sensor stays where it
is, and its placement is not reconsidered. No track-drain reasoning is carried into any
other section of this file.**

## What I read before writing

agents.md rules 1 to 11. subsystems/water.md in full, including everything appended
from 2026-09-03 onward. interface-table.md including the D-145 namespace block, the
fluid, power, signal, cable and mechanical tables, and the D-146 gland allocation.
decisions.md: the G-rule table G-01 to G-43, the "Parts the owner already has" table,
D-025, D-049 by its G-22 amendment text, D-063, D-108 to D-121, D-126 to D-139, and
D-143 to D-147. parts.md: the chiller section, the day tank temperature control
section, the fill solenoid section, the chiller-and-loop-pump section, the leak
console section with the struck LS roster, and the "Not known, and not to be
invented" section. commissioning.md: all rows, the ordering note, the re-measure
triggers, and the chiller-state note. findings.md rows F-089 and F-093 to F-104.
subsystems/main-panel-ladder.md sections A to D, the open-mark table, and findings 1
to 5. subsystems/interconnect.md in full. subsystems/water-s18-f003.md sections on
the hold-off, F-003 and the S-05 asymmetry. order.md envelope map and list.

Not read: the 1st Edition audit files, deliberately. G-40 says they are a citation
and not a source, and nothing below needs one.

---

# 1. THE FLOAT REQUIREMENT

D-118 struck the inherited part roster and restarted this from requirements. What
follows is what a float must DO at each of D-127's eight positions. It names no
part, no height, no band and no cord length. Where a number is required to close a
statement, the number is asked for rather than supplied.

## 1.0 Five things that are true of all eight, established before the positions

### (a) Every one of the eight is a series element in a 24 V coil chain

Read off the ladder rather than assumed. Rung 11 puts the two high-high positions
and, on one of its two candidate landings, the storage low position in series in the
permissive string ahead of the K-PERM coil. Rung 19 puts the two storage fill
positions in series in the K-FILL-S coil chain. Rung 20 puts the two day tank fill
positions, and the storage low on its other candidate landing, in series in the
K-FILL-D coil chain. Rung 22 puts the dry-run position in series in the K-DRY coil
chain. Every chain is fed from the 24 V side, node PB or the +V rail.

**No float in this build switches a load. Every float interrupts a coil circuit.**
That single fact drives (b), (c) and (d).

### (b) The fail direction is therefore FORCED, not chosen, and it is the same everywhere

G-22 asks what a severed conductor does. On a series element in a coil chain, severed
equals open equals coil de-energised. So the fail direction is decided entirely by
which water state is wired CLOSED.

**The requirement: at every one of the eight positions, the float element must be
CLOSED in the state that PERMITS the action to continue, so that a severed conductor
de-energises the coil and the action stops.**

This is not inherited from anywhere. It follows from D-049's amendment to G-22 - the
severed case is chosen safe, on frequency - applied to a topology that is already
drawn. It happens to agree with the 1st Edition set on six positions and to
contradict it on two. That agreement is a coincidence of construction and is recorded
as such, on D-119's precedent: the same answer arriving as a derivation is a
different thing from the same answer arriving as an inheritance.

### (c) The short case is worse here than G-22 and D-049 anticipated, and the mounting method is why

D-049 hands the short case to adjacency - to the wiring plan - and not to circuit
design. That escape works when the wiring plan is free to choose what lies next to
what. **D-121's standpipe removes that freedom by construction.** One rigid pipe per
tank carries every float cord and every pump cord, tied at intervals, in water. So
every float conductor's realistic neighbour is another float conductor of the same
tank, and per the D-142 raise, at least one realistic neighbour is a 120 VAC pump
cord.

Two consequences, both stated and neither solved here:

- A short between two float pairs on one standpipe can bridge a high-high to a fill
  float and produce "level is fine" on a chain that is not fine. Severed is safe;
  shorted-to-neighbour is not, and adjacency cannot be designed away on a bundle
  whose whole purpose is to hold everything together.
- The float cord's voltage rating cannot be established against its own 24 V use.
  CBL-06 already sets the precedent in this tree: the leak console's contact legs sit
  in the 120 V chain, so every conductor in that cable is required to be insulated
  for 600 V including the 24 V pair sharing the jacket. The same argument reaches a
  24 V float cord tied against a 120 V pump cord on a pipe standing in water.

**Routed, not solved: this is INTERCONNECT's separation question and MAIN-PANEL's
chain question. WATER's half is to state that the mounting method it owns is what
creates the adjacency.**

### (d) F-089, restated as a requirement, and it has a second half nobody has stated

F-089 as routed: the contact must switch a 24 V control circuit, and under G-31 a
minimum switching load is ONE POWER requirement and not three independent floors, so
this is a fifth of the contact power of the 120 VAC coil the old set's floats were
rated for.

**The requirement, expressed the way G-31 requires:** for each position, the float's
published minimum switching load, expressed as a POWER, must be at or below the power
that position's coil circuit actually presents at its worst case. Clearing a
published V/mA reference coordinate is not a margin. G-24 makes this question
mandatory for every contact and it has never been asked of a float.

**The worst case is not 24 V.** F-010 and ladder mark ?11: the NDR-240-24 rail is
settable across a band and nothing fixes the trim, so no coil, lamp or burden may be
sized at 24 V. The float's minimum switching load must be cleared at the LOW end of
the trim band, where the coil circuit presents the least power. C-16 records the trim
as actually left, and it is a commissioning measurement rather than a design figure.

**The second half, which is not in F-089 and which I am adding: the change is not
only 120 V to 24 V. It is AC to DC, and it is inductive.** The old set's floats
switched a 120 VAC coil. Every coil in this build's chains is a DC coil - order.md
specifies relay coils covering the whole trim band with a stated must-release voltage,
and calls the chiller element's coil a 24 Vdc contactor coil. Three things follow and
all three are requirements on the part rather than on the panel:

1. A pilot-duty rating stated for AC does not transfer to DC. A DC contact rating is
   normally much lower for the same contact, because there is no zero crossing to
   extinguish an arc.
2. Breaking an inductive DC coil produces a kick across the float contact, and that
   contact is at the far end of a long cord in a tank. **Suppression must be at the
   coil, in the panel, not at the float.** order.md already places suppression at the
   coil for every envelope and item 4 covers fast-release suppression. WATER's
   requirement is only that the float contact must not be the sole absorber of coil
   break energy, and that the suppression choice must not raise release time past
   what a permissive is allowed to take.
3. The load is small and steady - a coil holding current, continuously, for months.
   That is the exact condition G-24 exists for: an under-loaded contact oxidises. So
   the minimum switching load question here is not academic; it is the dominant
   lifetime question for all eight.

**BLOCKED, and named as blocked: WATER cannot state the number.** The coil burden per
chain is MAIN-PANEL's, P-08 is internal to MAIN-PANEL, and main-panel-ladder.md's own
FINDING 5 records that the permissive string's voltage class is stated two ways in
the tree - CBL-06 and parts.md say the string's legs sit in a 120 V chain, while
order.md specifies a DC coil on the 24 V rail. Until that is settled, the two
high-high positions do not have an established switching voltage at all, let alone a
power. Under rule 9 nothing is built against it.

### (e) The differential requirement is a BUILD parameter and it is asymmetric by position

D-131: the differential is set by tether length, so it is a thing this build chooses
rather than a thing the part provides. No datasheet can supply it. So the requirement
asks what band each POSITION needs.

Two structural facts decide the answer, and neither is in any datasheet:

**Fact 1. G-03's seal-in makes the differential of a PAIRED float nearly irrelevant.**
In a start float, stop float, relay seal-in arrangement, the start float's MAKE point
starts the fill and the seal-in then holds the coil, so the start float's break point
never matters. The stop float's BREAK point ends the fill, and its make point never
matters. **The working band is the vertical SEPARATION OF THE TWO CLAMPS, not either
tether length.** That covers four of the eight positions.

**Fact 2. For the four UNPAIRED positions the float's own tether IS the hysteresis,
and its only job is anti-chatter.** Two of those four - both high-highs - feed a chain
that latches through a manual reset, so they never re-arm by themselves and their
differential has no cycling duty at all. The dry-run position feeds K-DRY, which
also latches and needs a reset block, so the same applies. **Only the storage low
position controls a genuine recycling behaviour**, because breaking K-FILL-D's chain
drops the seal-in and the transfer restarts as soon as storage recovers and the day
tank start float is still made.

**So the requirement per position, in words and with no figure:**

| Class | What sets the band | What the tether must satisfy |
|---|---|---|
| The four fill-control positions | The separation of the two clamps | Short enough that the trip level is well defined against its paint mark; short enough that the pair's arcs cannot overlap; long enough to exceed surface disturbance at that height |
| The two high-highs and the dry-run | Nothing - a human resets the chain | Exceed the surface disturbance amplitude at that position, and nothing more. A long tether here only smears the trip level |
| The storage low | The band that must be recovered before the transfer may restart | Long enough that the transfer pump cannot cycle against a slowly refilling storage tank |

**And the input that decides all of them is hydraulic, not electrical: the surface
disturbance amplitude at each position, which is caused by things WATER places.** The
return drop's landing point, the transfer discharge, and the two continuously running
submersibles in the day tank all disturb the surface that the day tank floats read.
Nothing has measured it and no datasheet contains it. It is a commissioning
observation, taken while filling slowly per D-131's confirm-each-float step.

**One position is a conflict rather than a requirement, and it must be flagged now:**
the day tank low-low needs the LARGEST differential of the eight, because low level is
when the two submersibles are nearest the surface and vortexing is worst - C-11 names
the vortex explicitly - and it is the position where the least depth is available to
spend on a tether. That conflict is resolved by geometry, not by a part, and it may
force the low-low trip higher than the pump's bare submergence limit.

**One vessel fact that changes what a tether length MEANS:** the storage tank is
cone-bottom. The same tether gives a very different volume band at different heights,
and near the bottom of a cone it gives almost none. So the storage low position's band
must be specified in LEVEL and checked in VOLUME, and the two are not proportional in
that vessel.

## 1.1 The eight positions

Positions, not parts. LS-n is a position identity per the D-145 namespace. The ladder
marks in brackets are main-panel-ladder.md's open marks, so MAIN-PANEL can match rows
to positions without a translation step.

---

### DAY TANK 1. HIGH-HIGH [ladder ?13]

**What it must do.** Detect that the day tank has risen above its normal working top,
which means the day tank fill-stop position has failed to stop the transfer. It is the
instrumented backstop under D-134, and the overflow sits above it.

**What it switches.** A series leg of the 24 V permissive string, ahead of K-PERM,
alongside the E-stop, the leak console and the storage high-high. Dropping K-PERM
removes driver VM under G-09 and removes node PB, which drops K-FILL-D and its
transfer pump pole, K-FILL-S and its fill solenoid, and K-DRY. **One float stops the
whole plant, and clearing it requires a human at the reset.**

**If it fails to trip.** The only remaining line is the overflow, which is
uninstrumented per F-095. A fill-stop failure plus a high-high failure equals water
down the drain with nobody told.

**If it trips spuriously.** Everything stops, loudly, and the operator finds out. That
is the correct failure under G-16's shape: a stop rather than a permission.

**A severed conductor must read as: TRIPPED.** The element is closed while the level is
below the mark and opens on rising past it. Severed opens the string, K-PERM drops, the
plant stops. Forced by the series topology.

**Differential:** anti-chatter only. Must exceed the surface disturbance at that
height, which in the day tank is caused by the return drop and the transfer discharge.

---

### DAY TANK 2. FILL STOP [ladder ?21]

**What it must do.** Break the K-FILL-D coil chain when the day tank reaches the top of
its working band, stopping the transfer pump.

**What it switches.** A series element in K-FILL-D's coil chain. K-FILL-D-P switches the
transfer pump receptacle P-03. K-FILL-D-Q carries PL-G and the S-03 dose inhibit, so
this float also ends the dosing inhibit.

**If it fails to open.** The day tank fills past its band. D-114's sentence applies with
full force here and is worth restating in its day tank form: **the day tank is filled by
a PUMP, not by a spring-closed valve, so this float is the only thing that stops the
fill and there is no fail-closed actuator behind it.** The high-high then trips and the
plant stops and reports. If the high-high also fails, the overflow.

**If it fails open.** The fill never latches or drops early, the day tank runs low,
and eventually the low-low trips. A stop, and safe.

**A severed conductor must read as: STOP FILLING.** Closed below the stop mark, open at
and above it. Severed drops K-FILL-D and the transfer pump.

**Differential:** irrelevant to the cycle, per fact 1 above. Only the break point
matters. Requirement is that the break point be repeatable against its paint mark.

---

### DAY TANK 3. FILL START [ladder ?20]

**What it must do.** Make the K-FILL-D coil chain when the day tank falls to the bottom
of its working band, so the seal-in can pick up and the transfer runs.

**What it switches.** The same coil chain, in series ahead of the seal-in pole.

**If it fails to make.** No automatic refill. The day tank drains to the low-low, the
dry-run trips, the manifold pump stops. A stop, and safe, but note that today it is
reported to nobody, because S-20 is OPEN.

**If it sticks made.** This is the interesting one and it defeats G-03. With the start
float stuck closed, the stop float breaks the chain, the coil drops, and the start
float immediately re-makes it. **The transfer pump then chatters at the stop level
indefinitely.** That is not a flood and it is not detected: the tank sits at the top of
its band, which looks correct, while the transfer pump and its relay wear out. Nothing
in this system would report it. It is the failure this position has that the others do
not.

**A severed conductor must read as: DO NOT START A FILL.** The element is closed when
the level is LOW and open when the level is high, so severed reads as "level is high,
do not start". Note that this is the same physical sense as the fill-stop and the
high-high: closed on low water, open on high water. All three day tank upper positions
share one orientation.

**Differential:** irrelevant to the cycle. The make point is everything.

---

### DAY TANK 4. LOW-LOW, and it is the S-05 dry-run element [ladder ?23]

**WATER's half of ladder mark ?23, which asks which tank and which position the dry-run
element is.** It is the day tank low-low, and that is forced rather than chosen: G-11
gives the manifold pump suction at the DAY TANK bottom, so the level that starves the
manifold pump is the day tank level. No other position can sense it.

**What it must do.** Detect that the day tank has fallen to the level at which a
submersible in it loses submergence, and drop the manifold pump in hardware. G-25
permits exactly this: a no-flow CONDITION may drop the pump in hardware.

**What it switches.** The K-DRY coil chain, which latches through a seal-in and needs a
momentary reset block [ladder ?24]. K-DRY-P switches the manifold pump receptacle P-04.
K-DRY-Q is the second pole intended for S-20 to the Pi, and S-20 is OPEN.

**AND THE REQUIREMENT NAMES A HOLE IN WHAT IT PROTECTS.** Two submersibles run
continuously in this tank, D-143. K-DRY gates only the manifold pump receptacle. The
chiller and its loop pump sit on one receptacle gated by the permissive through an
element the ladder cannot name [?8, ?9]. **So the day tank low-low protects one of the
two submersibles in the tank and not the other.** The loop pump is described in
parts.md as oil-free magnetic drive, which is the class that does not survive dry
running, and the chiller's own protection senses its own water and not the tank,
D-108. This is stated as a requirement question and not designed: does the dry-run
element protect ONE submersible or BOTH? The tree's answer today is one, and nothing on
file says that was decided.

**The trip level requirement, therefore:** it is set by whichever submersible loses
submergence FIRST, not by the one the relay happens to protect. WATER owns both
placements under M-01 and will return the level once both are placed. C-11's low end is
the same number seen from the measurement side: below it a vortex draws air into the
loop, and air past a probe makes the spike that looks like an early arrival.

**If it fails to trip.** The manifold pump runs dry and is destroyed, and the probe
section reads air. Nothing else in the system would say so.

**If it trips spuriously.** Circulation stops. Per F-102 nobody would know, and per
C-23 as reduced the operator is the only check.

**A severed conductor must read as: TRIPPED, PUMP STOPPED.** This is the position F-093
was raised about, and this is my half of it.

**Stated against G-22 and D-049:** the element must be CLOSED while the level is fine
and OPEN on low level, in series in K-DRY's coil chain, so that severed de-energises
K-DRY and stops the pump. **That is the OPPOSITE of the direction the 1st Edition set
draws for both low-level stops, and it is not derived from that set in either
direction.** It is derived from the series topology plus D-049's choice of the severed
case as the safe one.

**What that costs MAIN-PANEL, taken from their own FINDING 2 table so the two halves
agree:** it puts this build in the right-hand column, K-DRY energised means PERMITTED.
Consequences MAIN-PANEL already enumerated and which WATER accepts as the price of the
fail direction: clearing the latch needs a momentary MAKE, an NO reset block, not the
break that main-panel-buy.md assumed; a dead 24 V rail or an open coil stops the pump;
and a permissive drop stops the pump. **G-39's question, which MAIN-PANEL asked of this
relay and nobody answered: what does a dead panel do? In this direction it stops the
pump, which is the right answer for a submersible whose protection is the relay.**

**And one consequence for the rest of the tree that follows from it:** "the manifold
pump runs continuously", D-143, means "runs whenever the permissive is up". An E-stop,
a leak alarm or either high-high stops it. C-23 as reduced already tells the operator to
confirm both pumps running by eye before and after a window; this is the reason that
instruction is not redundant.

**Differential:** the largest of the eight, and the position with the least depth to
spend. See the conflict named in 1.0(e).

---

### STORAGE 1. HIGH-HIGH, LS-8 [ladder ?14]

**What it must do.** Detect that the storage tank has risen above its working top, which
means the storage fill-stop failed or the fill solenoid failed to close. D-127 records
it as a hardware backstop in series with the day tank high-high.

**What it switches.** The same permissive string leg class as the day tank high-high, in
series with it. Same total consequence: everything stops and a human resets.

**If it fails to trip.** The storage overflow, uninstrumented.

**If it trips spuriously.** Whole plant stop, reported.

**A severed conductor must read as: TRIPPED.** Closed below the mark, open above.

**Differential:** anti-chatter only. Storage's surface is disturbed by the air-gapped
fill discharge, which under D-138 now falls into the tank from above rather than
entering through a fitting. That is a new disturbance created by the air gap
requirement and it lands directly on this position's band.

**One asymmetry between the tanks worth recording:** the storage fill source is a
spring-closed solenoid, D-114 and G-39, so a permissive drop closes it mechanically.
The day tank fill source is a pump, which stops only because its receptacle is
de-energised. **Storage has a fail-closed actuator behind its floats and the day tank
does not.** The single failure that defeats storage's whole float set is a
mechanically stuck valve, and that case is the one the storage overflow exists for
alone.

---

### STORAGE 2. FILL STOP [ladder ?19]

**What it must do.** Break the K-FILL-S coil chain at the top of the storage fill band,
de-energising the fill solenoid coil so the valve springs closed.

**What it switches.** A series element in K-FILL-S's coil chain. K-FILL-S carries the
seal-in and the fill solenoid.

**Note for F-089 specifically:** the number MAIN-PANEL was given for the solenoid, the
inrush that a relay contact makes and breaks, is the K-FILL-S CONTACT's requirement,
D-136. **The FLOAT does not see it.** The float sees the K-FILL-S COIL, on the 24 V DC
rail. The two must not be conflated, and G-23 already says so: a minimum switching load
belongs to a contact, and no figure is carried from one contact to another.

**If it fails to open.** The tank fills past its band, the storage high-high trips, the
plant stops and reports. If the high-high also fails, the storage overflow.

**If it fails open.** Storage never fills, the storage low eventually stops the
transfer, the day tank runs down, the low-low trips. A chain of stops, all safe, none
reported today.

**A severed conductor must read as: STOP FILLING.** Closed below the stop mark, open
above.

**Differential:** irrelevant to the cycle. Break point only.

---

### STORAGE 3. FILL START [ladder ?18]

**What it must do.** Make the K-FILL-S coil chain when storage falls to the bottom of
its fill band.

**What it switches.** The same chain, ahead of the seal-in pole.

**If it fails to make.** No automatic fill of storage. Same chain of stops as above.

**If it sticks made.** Same defeat of G-03 as the day tank fill start: the solenoid
chatters at the stop level. Worse here than in the day tank, because the load being
chattered is a solenoid coil with an inrush, D-136, and the relay contact that makes
and breaks it is sized for that event once per fill, not continuously.

**A severed conductor must read as: DO NOT START A FILL.** Closed on low water, open on
high.

**Differential:** irrelevant to the cycle. Make point only.

---

### STORAGE 4. STORAGE LOW, the pump-down float, LS-3 [ladder ?15 and ?22]

**What it must do.** Stop the transfer pump before storage is drawn down past the point
where the transfer pump loses suction.

**What it switches - and this is genuinely undecided, so WATER returns the requirement
and not the landing.** The ladder draws this position under one mark in TWO PLACES: as a
leg of the permissive string in rung 11, and as a series element inside K-FILL-D's coil
chain in rung 20. They behave completely differently. In the string, an empty storage
tank drops the drivers, both fills, circulation and the chiller. In the K-FILL-D chain
it stops only the transfer.

**WATER's half, stated as a requirement about the device rather than as a panel
choice:** this position protects ONE device, the transfer pump. **An empty storage tank
is not a hazard to anything else.** The day tank can be full and perfectly usable, the
loop can circulate, and dosing can proceed while storage is empty. Stopping the whole
plant because an upstream reservoir has run out is a stop with no safety content in it,
and it converts a refill errand into a full permissive reset. **So the minimum scope
that achieves the protection is the K-FILL-D chain, and WATER states no reason for the
wider scope.** MAIN-PANEL rules on the landing.

**If it fails to open.** The transfer pump runs dry. Nothing reports it.

**If it fails open.** No transfer. The day tank runs down to the low-low. Safe.

**A severed conductor must read as: DO NOT TRANSFER.** The element is CLOSED while
storage level is fine and OPEN on low, which is the same sense as the day tank low-low
and the opposite of the six above it.

**Differential:** the only one of the eight with a real cycling duty. It must be long
enough that the transfer pump cannot restart against a storage tank that has recovered
only a trickle. And it is the one measured in a cone, so the level band and the volume
band are not proportional - see 1.0(e).

**Height dependency WATER owns and has not closed:** this position's trip level is set
by where the transfer pump takes suction, and nothing on file states whether the
transfer pump is submersible in storage or draws externally from the cone bottom. It
also must sit BELOW the storage fill start, or the fill start is never reached. That
ordering is a requirement on the marks, not a number.

---

## 1.2 The result of 1.1, collected, because it is a build hazard

**Six of the eight are CLOSED ON LOW WATER, OPEN ON HIGH WATER:** both fill starts, both
fill stops, both high-highs.

**Two of the eight are CLOSED ON HIGH WATER, OPEN ON LOW WATER:** the day tank low-low
and the storage low.

**Those two are the inverse of the other six, on the same standpipe, in the same tank
as some of them, and if the parts are identical they are indistinguishable by eye once
installed.** A float installed the wrong way up silently inverts the fail direction of
the two positions where an inverted fail direction is most dangerous. That is a build
hazard that the requirement must remove rather than warn about.

**AND IT IS THE STRONGEST SURVIVING ARGUMENT FOR A CHANGEOVER FLOAT, and it is not
F-094's argument.** F-094 asked for SPDT as a fail-DETECT under G-27, and
main-panel-ladder.md FINDING 4 established that a fail-detected float has no reader in
this panel: G-01 forbids the Pi, G-02 forbids a second level signal, no face hole is
free for a lamp, and there is no spare coil for a comparison relay. That grade is
CURRENT and MAIN-PANEL named what would change it.

**The changeover has a second value that survives FINDING 4 completely: on a changeover
float both senses are available at the panel from ONE physical installation.** The fail
direction becomes a wiring choice at a terminal a person can see and check, instead of
an orientation choice in a tank a person cannot. Eight floats installed identically,
two of them wired to the other leg. **That removes the inversion hazard for free, and
it is a requirement WATER can state without any reader existing.**

Requirement, therefore: **a changeover contact, for the reason above, and not for
F-094's reason.** F-094's reason remains routed to MAIN-PANEL and remains without a
reader.

## 1.3 Nothing tests any of this, and C-19 does not cover it

C-19 is the fail-direction test: disconnect each sense conductor in turn at the gland
and record **what the Pi reports**. It exists because G-22 was a design claim with no
check behind it, and per T-014 a claim nobody tested is a claim nobody has.

**G-01 makes all eight floats invisible to the Pi. So C-19 does not reach a single one
of them.** Everything in section 1 above - eight fail directions, two of them inverted
relative to the other six - is today an intention with no scheduled check.

**What is required, and it is free and needs no instrument:** with the plant live, open
each float conductor in turn at the panel terminal and confirm the plant does the safe
thing named in 1.1 for that position - the fill stops, the transfer stops, the manifold
pump stops, or the permissive drops. It is the same argument C-19 was created on,
applied to the contacts C-19 cannot see. **It is also the only thing that would catch an
inverted float before the tank is full.**

BOSS owns commissioning.md and I have not edited it. This is returned as a required row.

## 1.4 F-100, the cord, and exactly what I need from INTERCONNECT

D-131 makes the cord the strain member, the trip-height datum and the signal path at
once: the tie clamps the weight on the cord, the tie IS the trip height, and
commissioning says adjust the tie and never the wiring. So the cord cannot be cut at
the tank and cannot be broken at a junction there.

**That makes cord length a GATE ON PART SELECTION, not a preference.** A float that
answers every requirement in sections 1.0 to 1.2 and whose supplied cord does not reach
the panel gland is disqualified, and the only remedies D-131 leaves are a splice in the
wet zone or moving a mounted panel, both of which it forbids. **So the cord length must
be produced BEFORE the part search, which means INTERCONNECT's wall layout gates the
float purchase. That dependency is not drawn anywhere.**

**The span, term by term. WATER owns the first two and the last one. Every term between
them is INTERCONNECT's, and I am not stating any of them.**

| Term | Owner | Status |
|---|---|---|
| 1. Trip mark to the top of the standpipe | WATER | Available once trip heights are decided, and they are gated by C-11 and by section 2 below |
| 2. Standpipe top, over the rim, to the tank's cord-exit grip | WATER | Available once the standpipe and the grip position are set |
| 3. Tank position relative to the main panel, both tanks | **INTERCONNECT** | Needed. This is the wall layout, and M-02's arbitration |
| 4. The route from that grip to the panel: horizontal run, vertical rise, up-and-over versus along, and whether it shares a tray or duct | **INTERCONNECT** | Needed |
| 5. Which panel face these enter, and where on it | Face is MAIN-PANEL's under D-146, position on the face is **INTERCONNECT's** | Needed |
| 6. Drip loop allowance at the tank grip and at the panel gland | **INTERCONNECT**, its own stated convention | Needed as an allowance rule, not a number I supply |
| 7. Service loop and termination slack at the panel | **INTERCONNECT** | Needed |
| 8. Re-clamp allowance | **WATER** | See below. Nobody else can give it |

**Term 8 is the one that is mine and that has no analogue in any other cable in this
build.** D-131 requires that commissioning adjust the tie and never the wiring, so the
weight clamp must be able to travel up and down its mark over the full plausible
adjustment range of that position with the far end of the cord not moving. **The
allowance is at least the full adjustment range of that position's trip mark, taken in
the direction that lengthens the required span - the clamp moving DOWN the pipe pulls
cord into the tank.** That range is not a number today because the trip heights are not
set. It is stated as a rule so it survives every height being wrong.

**And the terms are not per-cable, they are per-position:** eight positions, eight cords,
four leaving each tank, all converging on one panel. Term 1 differs for every one of
them because every position has a different mark on the pipe. So what INTERCONNECT
returns is not one length; it is terms 3 to 7 as a rule, applied eight times.

**What I need from INTERCONNECT, stated as one request:** the wall layout, the route
class from each tank's cord grip to the panel, and the drip-loop and service
allowances, expressed so that WATER can add terms 1, 2 and 8 to them per position.
**I state no number and I am not asking INTERCONNECT for one either - I am asking for
the terms of the sum.**

## 1.5 Search terms, for everything section 1 cannot state

Contact and duty, against F-089 and G-31:
- `float switch minimum switching load milliwatts low level dry circuit`
- `pilot duty float switch DC contact rating inductive relay coil`
- `AC pilot duty rating versus DC rating same contact float switch`

Form, against 1.2:
- `SPDT changeover tethered float switch normally open normally closed both legs`

Cord, against F-100:
- `float switch available supplied cord lengths options`
- `float switch cable jacket voltage rating 600 V submersible`
- `float switch cord chemical compatibility pH adjusted nutrient solution`

Mounting and differential, against D-131:
- `external cable weight tethered float switch differential versus tether length`
- `float switch mounting clamp to standpipe cable tie weight`

Wetted materials:
- `float switch float body material compatibility fertiliser solution long immersion`

---

# 2. THE OVERFLOW AND THE AIR GAP, PRICED

Both tanks, both requirements, D-130 and D-138. The drain is a 6 in track and the
overflow may enter it anywhere, D-147, so the entry point is free.

## 2.1 What the overflow costs, in plumbing terms

**a. Two irreversible holes in two bought tanks.** A bulkhead near the top of each tank
wall. This is the single largest cost and it is not the fitting: **it is that the hole
cannot be moved.** A bulkhead sited before the trip heights are settled is a scrapped
tank, and both tanks are already bought and listed in decisions.md.

**b. A gasket needs a flat land, and one of the two tanks is a cone bottom.** The upper
wall of a cylindrical tank is a curve in one axis, and a bulkhead gasket seating on a
curve is a leak that appears later. Whether either tank has a flat moulded boss near
the top is a question for the owner with the tanks in front of him. It changes the
fitting class and it may change the landing height.

**c. Two gravity runs to the track, and gravity is the constraint.** Continuous fall
from each bulkhead to the track, no trap, no low point, no rise anywhere. That
constrains the run's route absolutely, and the route crosses the wall INTERCONNECT is
laying out. Its own file already requires routing above any spill path and drip loops
where a cable enters a box from above. **An overflow line is a permanent wet-side
object on a wall that four enclosures and seventeen cable runs are competing for, and
it cannot go over or under anything.** That is a real claim on wall space and it should
enter M-02's arbitration.

**d. It must discharge to the track through an air gap, and that is a SECOND air gap
this build now needs.** A pipe that terminates below the track's water surface, or that
is connected to the drain, is a back-siphon path from the drain into the tank. **So
there are two air gaps in this system and they protect opposite sides: the fill air gap
protects the municipal SUPPLY from the tank, D-138; the overflow air gap protects the
TANK from the drain.** D-138 names only the first. Nothing on file names the second.

**e. Sizing is set by the fill rate, and it must not be inherited from D-109.** D-109
says all PVC is 3/4 in Schedule 80, and that is stated as the manifold diameter with
the port arrangement downstream of it. **The overflow's capacity requirement is a
different question with a different driver: it must swallow the full inflow with the
fill-stop failed.** For storage that is the solenoid's flow at the actual supply
pressure; for the day tank it is the transfer pump's delivered flow into a full tank.
**Neither number is on file.** Both are measurable rather than lookup-able - the same
catch-and-time method C-10 already specifies for FL-03. **I state no size. What I state
is that taking the manifold's diameter for the overflow because it is the diameter this
project uses would be inheriting a number across a change of duty, which is the T-018
family.**

**f. The port fouls, and it fouls silently, and it has nothing behind it.** An open port
in an open-top tank collects debris and grows biofilm at the waterline, which is
exactly where it sits. **This is the same shape WATER already refused once:** in the
return-drop family, WATER refused the submerged return with an anti-siphon vent hole on
the ground that the siphon break depends on a small hole staying clear and that hole
fouls shut silently, and that trading a visible failure for an invisible one is the
wrong trade, D-019's reasoning. **An overflow port that fouls shut is the same trade,
and unlike the return drop it is the last line.** That is an argument for a port that is
large relative to the debris it will meet and inspectable without disassembly, and it is
an argument against a screen. It is also the strongest argument in this section for
answering F-095.

**g. It takes rim and wall real estate that is already contended.** In the day tank the
same upper wall and rim carry: the standpipe's U-bolt over the drum lip, the standpipe
itself with its cord bundle, the return drop's landing, the two submersible cords, and
M-01's penetrations and hangers. **The overflow must not sit under the return drop's
splash and must not sit where the standpipe or its cord run is.** M-01 grows by one item
and its clearances get tighter.

**h. It changes a C-02 re-measure trigger's scope.** commissioning.md lists "any
plumbing change: manifold, ports, tubing runs, the return drop's landing point, the
submersible's position in the tank" as a C-02 and C-07 re-measure. Cutting two bulkheads
is a plumbing change made on the vessels those rows measure, so **the overflow work must
be finished before C-02 and C-07 are run, or they are run twice.**

**i. One constraint that comes from D-133 and stands unchanged:** normal overflow
discharge must not be able to splash or pool on the leak sensor, because if it does then
every overflow reads as a leak and the alarm stops meaning anything. **The overflow's
entry into the track is free under D-147, so this is satisfied by choosing the entry
point away from where the sensor already is.** No sensor placement is proposed or
reconsidered here.

## 2.2 What must be DECIDED before anything is cut, in order

This is the ordering answer, and it is the part of the price that is not money.

1. **The day tank working volume and fill band, C-11, both ends with the reason for
   each.** Its own blocked-on column says "floats chosen and set". That is not circular:
   the band is a decision about the water, and the float marks follow it.
2. **The four day tank trip heights and the four storage trip heights**, marked on each
   standpipe from the end cap face per D-131, with the differentials of 1.0(e) chosen.
3. **The high-high mark on each tank**, which is item 2's topmost mark.
4. **The overflow's landing height, above the high-high**, D-134.
5. **The tank rim, and the fill air gap above it**, D-138.
6. Only then: cut.

**AND ONE THING IN THAT LIST HAS NO DATUM YET, AND IT IS THE SAME DEFECT D-129 FOUND IN
THE OLD SET.** D-131 fixes the float marks to **the standpipe's end cap face**. A
bulkhead is a hole in a **tank wall**, and an air gap is measured from the **tank's flood
rim**. Those are different datums on different objects, separated by however far the end
cap stands off the tank floor and by however far the rim stands above the water.
**D-129's second contradiction was precisely this: the old set stated the datum two ways,
end cap face and tank floor, with the same numbers under both. This build now has the
same two datums, in the same tank, for the first time.** The requirement: **the offset
between the standpipe end cap face and the tank floor is measured once, per tank, and
recorded, before any height in the list above is written down.** It costs one
measurement and it is the cheapest item in this entire return.

## 2.3 What the AIR GAP costs, and the interaction nobody has drawn

**a. FL-02 stops being a connection.** With an air gap, the fill line comes over the
storage rim and discharges downward into open air. The interface row reads "WATER: fill
solenoid outlet | WATER: storage tank inlet", and "inlet" describes a fitting. **That row
is now wrong in wording. Reported, not fixed - BOSS owns the table.**

**b. The gap is measured from the FLOOD-LEVEL RIM, and on a tank with an overflow the
flood level is set by the overflow, not by the rim.** So the air gap dimension is
referenced to the overflow, which is referenced to the high-high, which is referenced to
a float mark on a standpipe. **D-130 and D-138 are one dimension chain, not two
requirements, and nothing on file says so.** That is the answer to "what interacts with
what": they interact through the datum, and the datum is item 2.2 above.

**c. THE FREEBOARD STACK, AND IT MAY NOT CLOSE.** Everything from here up has to fit
inside a tank height that is already bought:

fill band top -> fill stop mark -> separation -> high-high mark -> separation ->
overflow invert -> the tank rim -> the air gap -> the fill line outlet.

**Every gap in that chain is currently unset, and the total is a height budget on a
vessel nobody can make taller.** Nobody has added it up, and it cannot be added up until
the differentials of 1.0(e) are chosen. **That is why the float requirement and the
overflow pricing are one pass and not two, and it is the single most useful thing in
this section.** If the stack does not close, the thing that gives is the working volume,
C-11, which is DOSING's input.

**d. Splash and entrainment.** A gap discharge into an open tank splashes and entrains
air. It lands in STORAGE, not in the day tank, so it is one transfer away from the
probes, and C-11 already names air past a probe as the spike that looks like an early
arrival. It is not dismissed, it is deferred by one vessel. It also disturbs the storage
surface, which lands on the storage high-high's differential per 1.1.

**e. A rigid, bracketed outlet over an open tank.** The fill line's discharge end is
unsupported by definition. It needs a fixture, and the fixture must not be where the
standpipe, the transfer suction or the overflow is. Another M-01-class item, on the
storage tank.

**f. A question D-138 does not answer, and the price depends on it: is the air gap a
requirement on BOTH tanks or on one?** D-138's reason is backflow protection of the
municipal supply, and only the storage tank is connected to municipal supply. The day
tank is filled from storage by a pump. **On D-138's stated reason, the air gap attaches
to the storage fill only. On D-130's pattern it would be both.** There is a separate
reason to air-gap the transfer discharge into the day tank - it prevents back-siphoning
the day tank into storage when the transfer pump stops - but that is a different
requirement with a different justification, and I am not merging them. **Question to the
owner, because it doubles or halves this half of the price.**

## 2.4 IS DETECTION CHEAP? Answered in two halves, and the halves differ

**THE SENSOR IS CHEAP. THE READER DOES NOT EXIST. So as an electrical signal, NO.**

This is not speculation and it is not new: main-panel-ladder.md FINDING 4 established
it for a different device this week. A new contact in the wet field needs somewhere to
land, and the panel's inventory of destinations is closed:

- **A Pi input.** G-01: floats are hardwired to relays and invisible to the Pi. G-02: the
  Pi gets exactly one level signal, a dry contact saying a day tank fill is in progress,
  and it is described as deliberate and as the only level information software has. Both
  are in the owner's not-revisitable table. An overflow detector is a second level
  signal.
- **A lamp.** parts.md fixes the panel face and all five 22 mm holes are spoken for.
  MAIN-PANEL records there is not even a lamp-test hole among them.
- **A relay.** order.md's envelope map allocates six envelopes across four relays in hand
  plus three gold bought, with one standard spare and zero spare if K-PERM splits. A new
  input that must do anything other than break an existing chain needs a coil.
- **Break an existing chain.** This is the only free destination, and it is wrong: an
  overflow that drops the permissive turns a successful protection into a plant stop, and
  it is a stop that occurs precisely when the tank has just been saved.

**Grade, per G-36 and rule 10: CURRENT, not structural. What would change it: an
amendment to G-02 admitting a second level signal to the Pi, or a panel face that has a
hole to spare, or the purchase of one relay envelope.** Declining to pay does not make
this true retroactively, because the overflow gets built either way - so it is the
recoverable kind and not the self-fulfilling kind.

**THE OTHER HALF, AND IT IS THE ONE THAT ANSWERS F-095: F-095 DOES NOT ASK FOR AN
ALARM. IT ASKS FOR A RECORD.**

Read the finding's own words: "a fill-stop float can have been failing for weeks with
the only evidence down a drain", and "the next overflow looks the same". **The question
is "has this ever run since I last looked", not "is it running now".** An alarm answers
the second and needs a reader. A record answers the first and needs an eye.

**A non-electrical witness that latches until a human resets it costs zero panel
resources, zero interface rows, zero conductors and zero relay envelopes.** It has no
reader problem because the reader is the person doing the walk-round. It is in WATER's
scope entirely, it does not touch MAIN-PANEL, and it does not need G-02 amended. **I
name no part and propose no mechanism, because a mechanism is a design and this is a
price.** What I state is that the requirement is achievable in the class of things that
cost nothing here, and the requirement is: **the overflow's discharge must make a
persistent, human-readable mark that it has run, and clearing that mark must require a
deliberate human act.**

**AND THE THING THAT ACTUALLY COSTS ALMOST NOTHING NOW AND A LOT LATER IS NOT THE
DEVICE. IT IS THE PROVISION.** Cutting a bulkhead is a one-time irreversible act on a
bought tank; adding a branch or a boss to the overflow run while it is being assembled
is free; adding either afterwards means cutting a line that is already routed and
sloped. **So the recommendation, stated as a recommendation: build the provision into
each overflow run now, and leave the device decision open.** That is what D-019 did with
the keyed coupling and it is the same reasoning.

**AND ONE CONFLICT TO ROUTE RATHER THAN RESOLVE.** F-095 offers "a flow switch" as a
candidate. **D-119 says, in the owner's words: "There is no flow element anywhere and
there is not going to be one."** Read literally that already answers half of F-095's own
suggestion list, and it was written about the dry-run element rather than about an
overflow tell-tale. **I will not decide whether D-119's sentence reaches this. It is
BOSS's, and D-116's guard is the reason I am flagging it instead of picking: an open
question must not close because a decision made elsewhere happens to cover the words.**

## 2.5 Do I have a reason to depart from D-134's "above the high-high"? No.

D-134's ordering is correct and the reasoning holds under everything in section 2. The
high-high is reported and the overflow reports to nobody; putting the overflow below it
would let the silent protection absorb every fill-stop failure forever.

**And section 2.3(c) sharpens it into a real risk rather than a preference:** the
overflow being above the high-high is what makes the freeboard stack tight. If the stack
does not close, **the tempting fix is to drop the overflow below the high-high and
recover the height. That is the exact trade D-134 forbids, and it will look like a
purely dimensional decision at the moment someone is holding a hole saw.** Recorded here
so it is recognisable when it arrives.

**One consequence of the ordering that lowers the value of instrumenting the overflow,
and which I state because it cuts against my own section 2.4:** with the overflow above
the high-high, and with both fill sources gated by node PB, **an overflow requires a
DOUBLE failure** - the fill-stop float and the high-high float, or a mechanically stuck
solenoid. F-095's residual is real but it is a second-order event, and that is an
argument for the cheap record and against paying for a reader.

## 2.6 Search terms for section 2

- `bulkhead tank fitting flat mounting surface curved tank wall gasket`
- `polyethylene tank overflow bulkhead fitting installation`
- `tank overflow line sizing gravity full inflow rate`
- `indirect waste air gap discharge to floor drain`
- `air gap fill above flood level rim tank`

Measurements rather than lookups, and both by C-10's catch-and-time method:
the fill solenoid's delivered flow at the actual supply, and the transfer pump's
delivered flow into a full day tank.

---

# 3. F-103, THE THERMAL ARITHMETIC

## 3.1 The arithmetic

Inputs, all cited to parts.md, which is authoritative under D-026, and none from memory:

| Quantity | Value | Where |
|---|---|---|
| Chiller nameplate capacity | 3000 BTU/h | parts.md, chiller section and the chiller-and-loop-pump table |
| Chiller loop pump electrical input | 110 W | parts.md, chiller-and-loop-pump table |
| Manifold pump electrical input | **not on file** | parts.md's "Not known, and not to be invented"; the manifold pump appears only as "hi-flow submersible, 120 V corded" in the owner's parts table |
| Day tank setpoint | 66 F, pulls down at 68, stops at 64 | parts.md, day tank temperature control |
| Room | 62 to 65 F | parts.md, same section |

A submersible puts its ENTIRE electrical input into the water, because both the motor
losses and the hydraulic work are dissipated inside the water circuit. WATER stated
that in its first pass and D-025 states it too. So watts in equals watts of heat.

Unit conversion, definitional and not a spec: 1 W = 3.412 BTU/h.

- **Chiller capacity: 3000 BTU/h = 879 W.**
- **Loop pump: 110 W = 375 BTU/h.**
- **Loop pump alone consumes 12.5 percent of nameplate capacity, continuously, forever.**
- **Remaining budget for the manifold pump before nameplate is fully consumed: 769 W, or
  2625 BTU/h.**

**So the margin, stated as the finding asks: the manifold pump would have to draw more
than 769 W on its own to consume the whole nameplate with the loop pump.** If it is
comparable to the loop pump, the pair take about 220 W, 750 BTU/h, **25 percent of
nameplate, leaving 75 percent.**

**I do not know that it is comparable and I do not assume it.** The break-even is stated;
the figure that closes it is a nameplate reading, and it is one of two figures WATER
already owes and nobody has - main-panel-ladder.md mark ?6 records the same absence for
the transfer pump.

## 3.2 The margin is larger than the finding feared, and here is why

**The room is a HEAT SINK, not a heat source.** The tank band is 64 to 68 F; the room is
62 to 65 F. **The tank sits at or above the room across most of its band**, so ambient
gain is near zero or negative, and both tanks are open top so evaporation removes heat
continuously. parts.md says it in its own words: the setpoint sits at or above room
temperature and the chiller has very little work to do.

**That inverts the finding's framing in a useful direction.** F-103 says the pump heat is
"a continuous load the chiller carries on top of the room". **It is not on top of the
room. With the room at or below the tank, the pump heat is very nearly the ENTIRE load,
and it is the only load that does not go away.** The number is smaller than feared and
the structure is worse than described: it is the whole thing.

**And that makes the chiller's duty cycle directly readable from the arithmetic:** at
12.5 to 25 percent of capacity, the compressor runs 12.5 to 25 percent of the time, less
whatever the room takes away.

## 3.3 So the failure F-103 names does not occur, and a different one becomes likely

**"The tank does not reach temperature" requires the load to exceed capacity.** At one
eighth to one quarter of nameplate, with the room helping, it does not. **I state that as
the answer and I state the four things that could still break it:**

1. **3000 BTU/h is a nameplate at an unstated rating condition.** Capacity falls as the
   water setpoint falls and as condenser air warms. At 66 F water in a 62 to 65 F room
   the condition is mild and the derating should be small, but "should be" is not a
   number. **Needed: the capacity table or the rating condition for this chiller.**
   Search: `aquarium chiller capacity rating condition water temperature ambient
   derating`.
2. **Capacity is conditional on loop flow.** parts.md gives the chiller a required flow
   band and gives the loop pump a delivered range at 4 to 6 ft head that sits inside that
   band. **If actual head is higher than 6 ft the flow falls, and below the band's floor
   the rated capacity does not apply.** Nothing has measured it - see 5.6 below.
3. **A fouled exchanger or a fouled intake reduces effective capacity silently**, and
   nothing here measures it. commissioning.md's re-measure trigger list already treats
   silent flow degradation as the dominant hidden input for the manifold loop; the chiller
   loop has the same exposure and no row.
4. **The manifold pump's figure is unknown.** If it is very large the arithmetic changes.
   The break-even is in 3.1.

**THE LIKELY RESIDUAL IS THE OPPOSITE PROBLEM AND NOBODY HAS NAMED IT: SHORT CYCLING.**
A compressor loaded at one eighth of capacity into a 4 F deadband cycles on a rhythm set
by the tank's thermal mass. **I will not compute a cycle time, because the number it
needs is the day tank's WORKING volume and C-11 explicitly says the 40 gal on the parts
list is nominal vessel capacity and must not be used as one.** What I state is the
direction and the two figures that would settle it: **C-11's working volume, and the
compressor's minimum run time or minimum off time.** Search:
`compressor short cycling minimum off time small refrigeration circuit`.

**And it lands on a commissioning row rather than on nothing:** a cycling compressor puts
STEPS in the temperature trace, and C-02 and C-08 are measured in normal service with
chiller state recorded against every sample, D-027. WATER's earlier pass observed that a
cycling compressor gives steps and a held-off chiller gives a slope, and that a slope is
far easier to subtract. **So the thermal consequence of D-143 that actually reaches this
build is a measurement-quality one, on rows that are already scheduled.**

## 3.4 The provenance F-103 does not carry, and it matters

**This is D-025's question coming back, and it has been open since 2026-08-30, not since
yesterday.** D-025 wrote, in terms: the manifold pump puts essentially all of its
electrical input into the water it sits in and it runs continuously through a settle
window, so "the chiller rarely runs" may not hold during the window, "nobody has measured
that", and it is a question for C-02's trace and for WATER.

**D-063 then closed it with a sentence that D-143 has now reversed:** its third
"favourable consequence" was "D-025's premise survives. Continuous pump heat was the
thing that might have called the chiller more than the setpoint suggests. An intermittent
pump does not put continuous heat into the tank."

**D-143 reverses D-063. So that consequence falls with it, and D-025's question is live
again in exactly the form D-025 asked it.** F-103 is that question, re-found from the
other end four days later.

**Recording it under G-38:** D-063's consequence 3 was a claim graded against a tree in
which the pump was intermittent. The tree moved. The claim was not re-graded, and F-103
had to be discovered again rather than read off the file.

## 3.5 And the real hole is not the arithmetic. It is that a loop pump failure is silent and self-masking

This follows from the arithmetic rather than from it, and it is not in F-102 or F-103.

D-108: the chiller "senses its own water with its own built-in sensor, and it cycles its
own compressor". Its sensor is in ITS water, not in the tank.

**If the loop pump fails, the water standing in the chiller is chilled below setpoint
within moments and stays there. The chiller's own sensor is satisfied and the compressor
stops. Meanwhile the manifold pump keeps putting its input into the tank and the tank
warms, with the chiller sitting idle and reporting nothing.** The protection satisfies
itself on a stagnant sample.

**Nothing in this system would say so.** D-108 makes the Pi's tank temperature a dose
compensation and explicitly not a control input; G-01 and G-02 give no level or
temperature path into the panel; and per 1.1 the day tank low-low does not gate the loop
pump anyway.

**Grade, per G-36 and rule 10: CURRENT.** What would change it: the location of the
chiller's internal sensor, which is a datasheet question and not something I will assert
- if that sensor is in the tank rather than in the chiller body, this dissolves.
**Stated as a question with its reasoning shown, exactly because I cannot establish it
from what I read.** Search: `aquarium chiller internal temperature sensor location
inline versus body`.

**It is F-102's shape landing on the other pump, and F-102 was routed to me about the
manifold pump only.**

---

# 4. F-102. NOBODY KNOWS IT IS STILL MOVING WATER

F-003 restated by D-143: the at-rest premise is gone because there is no at-rest case,
and the pump can fail while running with nothing detecting it.

**What is NOT available, and each was available before D-143:**

- **W-1, the PT-1000 step when the standing probe column is displaced on pump start.**
  Gone. C-12 is void. No rest, no start, no transient. Spent, not declined.
- **The free self-test** - placing an element where the at-rest state is a known-open
  state so the rest interval tests the element. Gone with the rest interval. It was the
  best idea in WATER's first pass and it depended entirely on the pump stopping.
- **W-3, a flow-proving element.** Barred by D-119 in the owner's words, and no timing
  element was ordered.
- **W-4, discharge pressure.** Rejected by WATER on its own merits; nothing has changed.

**What IS available and does not answer the question:**

- **W-2, current sensing on the pump cord.** MAIN-PANEL's device. It proves the motor is
  energised and drawing, and it reports healthy through a fouled impeller, an air-locked
  volute and a blocked intake - which are exactly the failures F-102 is about.

**What IS available and does answer it, and it is free:**

**W-5, the operator's eye at the return drop.** The return drop must be an open
atmospheric air gap to break the siphon path back to the tank - a standing open item in
water.md, and WATER already refused the submerged alternative on D-019's reasoning. **At
an air-gapped drop, flow is directly visible and audible: the one point in the loop where
flow is an unambiguous event to a human.** D-143 makes it stronger, not weaker, because
it now works at any moment rather than only during a batch.

**What it costs WATER: a bracket orientation.** The requirement returned is that **the
return drop's landing point is chosen for SIGHTLINE as well as for mixing.** It joins the
return-drop family question already open in water.md and adds a criterion to it. It needs
no part, crosses no interface and is available today.

**And it is not a new procedure - it makes an existing required one performable.** C-23 as
reduced already tells the operator to confirm both pumps are running by eye before and
after every measurement window, because a pump that has failed looks exactly like a pump
that is running. Today the only things to look at are a cord and a receptacle, which prove
energisation and not flow.

**The residual stands: between two human observations, nothing knows the manifold pump is
moving water. Grade: CURRENT. What would change it: D-119 reopened to admit one flow
element, or G-02 amended to admit a second signal to the Pi.** Neither is mine and I
propose neither.

---

# 5. THINGS I FOUND THAT WERE NOT ROUTED TO ME

Each names what I read.

**5.1 One of the two owned submersibles is now unallocated, or a row is stale.**
decisions.md's "Parts the owner already has" lists "Two hi-flow submersibles, 120 V
corded" with the note "WATER, one circulation and one chiller loop". D-137 then bought a
separate loop pump and parts.md records it. water.md's scope line still reads "Both
hi-flow submersibles as devices and their placement". **Either there is a spare pump
nobody has accounted for, or the parts row is stale.** It matters beyond tidiness: if the
second owned submersible is in fact the loop pump, D-137's purchase is a duplicate; if it
is spare, F-103's arithmetic is unaffected but the manifold pump's identity is the one of
two the owner should read the nameplate off.

**5.2 The chiller loop pump has no dry-run protection, and it shares the tank with the
one that does.** Ladder rung 22 puts K-DRY in front of the manifold pump receptacle only;
rungs 09 and 18 put the chiller and loop pump on one receptacle gated by the permissive
through an element the ladder cannot name. Nothing in D-119, S-05 or G-25 says which
submersible the dry-run element protects. Detailed at DAY TANK 4 in 1.1.

**5.3 There is no interface row for the overflow discharge, and none for the air gap.**
I read all ten fluid crossings FL-01 to FL-10 as they stand after D-145. FL-01 is the
building supply to the solenoid inlet; there is no row for a tank overflow leaving WATER's
scope and entering the building's floor drain, on either tank. D-130 made it a requirement
on both tanks on 2026-09-04. **Rule 9 says nothing is built against an OPEN row; here
there is no row at all, on a requirement that ends in two irreversible holes.**

**5.4 FL-02's wording presumes a connected inlet that D-138 forbids.** Detailed at 2.3(a).

**5.5 C-19 cannot reach any of the eight floats.** C-19 records what the Pi reports; G-01
makes floats invisible to the Pi. So the eight fail directions established in section 1
have no scheduled check. Detailed at 1.3.

**5.6 Nothing measures chiller loop flow.** C-10 measures circulation flow at FL-03, which
is the manifold loop. FL-08 is the chiller loop and no commissioning row touches it. The
chiller's rated capacity is conditional on a flow band, so the arithmetic in section 3
rests on an unmeasured quantity. I read all of commissioning.md's rows to establish this.

**5.7 This build now has two datums for heights in the same tank.** D-131 fixes float
marks to the standpipe end cap face; a bulkhead and an air gap are referenced to the tank.
**That is the same defect D-129 recorded in the old set** - two datums, same numbers -
arriving in this build for the first time, and it arrives the moment the overflow becomes
a requirement. Detailed at 2.2, with the one-measurement fix.

**5.8 The standpipe closes D-049's escape route for the float signals.** D-049 hands the
short case to adjacency and the wiring plan; D-121's standpipe guarantees the adjacency by
construction, including 24 V float cords against 120 V pump cords in water. INTERCONNECT
raised the separation half in D-142's summary; the G-22 half is not raised anywhere.
Detailed at 1.0(c).

**5.9 A chiller loop pump failure is silent and self-masking.** Detailed at 3.5, graded
CURRENT, with the datasheet question that would settle it.

**5.10 The freeboard stack has never been added up, on tanks that are already bought.**
Detailed at 2.3(c).

**5.11 D-119's "no flow element anywhere" and F-095's suggested flow switch are on a
collision course.** Detailed at 2.4, routed to BOSS rather than resolved.

**5.12 A stuck-made fill START float defeats G-03 and produces a wear failure nothing
reports.** Detailed at DAY TANK 3 and STORAGE 3. The seal-in is drawn to prevent
chattering at one point; a start float that never releases reinstates it.

---

# 6. STATUS

**Not finished, and I do not declare myself finished in any case, per rule 7.**

**What is complete and can be built against once BOSS accepts it:** the fail direction
for all eight positions, sections 1.1 and 1.2, which is my half of F-093; the requirement
shape for F-089 including its AC-to-DC half; the differential requirement per position
under D-131; the cord requirement and the terms I need from INTERCONNECT under F-100; the
overflow and air gap price and its ordering; the thermal arithmetic and its margin; and
the F-102 answer.

**What is BLOCKED and on whom:**

| Blocked | On |
|---|---|
| The float's minimum switching load as a NUMBER | MAIN-PANEL's coil burden per chain, at the low end of the trim band. And behind it, main-panel-ladder.md FINDING 5: the permissive string's voltage class is stated two ways in the tree |
| Any float PART selection | The cord length, which is blocked on INTERCONNECT's terms 3 to 7 in 1.4. A part cannot be chosen against positions and contact duty alone without realising F-100's self-fulfilling grade |
| Every trip height, and therefore the overflow and the air gap | C-11's working volume and fill band, and the datum measurement in 2.2 |
| The storage low position's landing | MAIN-PANEL, with WATER's minimum-scope requirement stated in 1.1 |
| The dry-run element's protective scope | 5.2. One question, and it is the owner's |
| The chiller capacity number's validity | The rating condition, and chiller loop flow, 5.6 |

**Nothing here has been built against an OPEN row.** S-01, S-02, S-04, S-20, FL-03, FL-04
and P-02 are all open and are cited as requirements addressed to them, never as
established facts. I have edited no other file.

**I have stated no part number, no gauge, no length, no height, no band and no spec from
memory. Every figure in section 3 is cited to parts.md with its section named, and the
only other arithmetic is a unit conversion.**
