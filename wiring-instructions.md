# D4. Wiring instructions

**A page per enclosure. Regenerated 2026-09-05 in the G-49 procedure format.**

**This is a VIEW of D5, wiring-schedule.md.** Nothing here is a fact of its own: every
conductor id, landing, label and warning comes from a CDR- row there. **Change a row
in D5 and these pages change with it.** No data changed in this regeneration - only
the shape it renders in.

**You need to know how to use tools. You do not need to know anything about this
machine. If it is not on the page it does not happen.**

**Take the page for the box in front of you and nothing else.** A conductor that runs
between two boxes appears on both pages, and each page tells you only the end you are
holding.

## How to read a step

**Every step is numbered and the numbers are per page.** P3-09 is page 3, step 9.
**Numbers are never silently changed. If a step is ever inserted, it takes a letter -
P3-09a - and a REVISION line appears at the top of that page saying so.** There are no
revision lines yet.

**Every step ends with ACCEPT: how you know it is right, checked at that moment.** If
you cannot see the accept condition, the step is not done.

**A step that says BLOCKED has no accept condition yet.** It says what is missing and
who owns it. **Do not substitute, do not pick a likely terminal, do not skip ahead.
Leave that joint and go to the next step.** A blocked step stays in its place on the
page so you know you are stepping over it rather than finding out later that something
was left out.

**Every page begins with the same six steps, printed in full.** They repeat because
you may be holding one page and no others.

---

# PAGE 1. MAIN PANEL

**Cables enter the BOTTOM face. Nothing but the five 22 mm devices goes in the top.**

**THE GROUND BAR IS THE ONLY BONDING POINT IN THIS PANEL.** If you find a convenient
screw, do not use it. Every green conductor in the build ends at that bar and nowhere
else.

**P1-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P1-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step gives a channel token as well,
write both, unabbreviated and not run together.
ACCEPT: the label reads exactly what the joint step says, character for character.

**P1-03. Write the same label on the other end.**
ACCEPT: both ends read the same.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **You will not be able to tell later which wire this is: the
terminal it lands on has no name yet.**

**P1-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P1-05. Look at what is already under the terminal, then land this end.**
If anything is already under that clamp, the joint step says so. If it does not, and
something is there, stop and do not land.
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.
WHY: a clamp carrying more conductors than it is meant to passes inspection and fails
later, and this panel has one terminal that two cables genuinely leave.

**P1-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY: the tick is on the page in your hand. D5 is the record of what the build is, not
the worksheet for what you have done.

## Supply

**P1-07. Land CDR-042.** Far end: the building branch circuit. Carries the supply line.
BLOCKED. Missing: the terminal marking on the panel's line input, and P-01 is an open
interface row. Owner: anyone with the part in hand and a pen, for the marking; BOSS
for P-01.
WHY IT IS NOT JUST A MARKING: no disconnecting means is named anywhere in this build.
Do not assume the branch breaker is it.

**P1-08. Land CDR-043.** Far end: the building branch circuit. Carries the supply
neutral.
BLOCKED. Missing: the terminal marking, and P-01. Owner: as P1-07.

**P1-09. Land CDR-044.** Far end: the building branch circuit. Carries the system's
equipment ground, arriving at the single point.
BLOCKED. Missing: the terminal marking, and P-01. Owner: as P1-07.
WHY: if this one is missing, every local ground bar in the build loses its path home
at once and nothing reports it.

## Fill solenoid

**P1-10. Land CDR-001.** Far end: the fill solenoid coil, page 7. Carries switched
120 VAC to the coil.
BLOCKED. Missing: the terminal marking on K-FILL-S, and P-02 is an open interface row.
Owner: as P1-07.
WHY THIS POLE IS NOT LIKE THE OTHERS: it makes and breaks 0.58 A of inrush, not the
0.21 A the valve holds at. Anything chosen for the holding figure is chosen for the
wrong event.

**P1-11. Land CDR-045.** Far end: the fill solenoid coil, page 7. Carries the coil
return.
BLOCKED. Missing: the terminal marking, and P-02. Owner: as P1-07.

**P1-12. Land CDR-046.** Far end: the fill solenoid, page 7. Carries equipment
grounding for the valve.
BLOCKED. Missing: the terminal marking, and P-02. Owner: as P1-07.

## Motor supply out to the pump boxes

**P1-13. Land CDR-002.** Far end: pump box A driver supply, page 3. Carries motor
supply positive to box A.
BLOCKED. Missing: the terminal marking on KM-DRV pole 1, and P-06 is an open interface
row. Owner: as P1-07.
BEFORE YOU CLOSE THAT CLAMP: CDR-005 lands on this same terminal at P1-14. Two cables
leave one terminal here and that is intended.

**P1-14. Land CDR-005.** Far end: pump box B driver supply, page 4. Carries motor
supply positive to box B. Same terminal as P1-13.
BLOCKED. Missing: as P1-13.

**P1-15. Land CDR-003.** Far end: pump box A, page 3. Carries motor supply return.
BLOCKED. Missing: the terminal marking on the 24 V rail negative, and P-06. Owner: as
P1-07.

**P1-16. Land CDR-006.** Far end: pump box B, page 4. Carries motor supply return.
BLOCKED. Missing: as P1-15.

## Storage fill chain

**P1-17. Land CDR-055.** Far end: LS-6, storage fill start, page 6. One end of a float
that sits in series in the K-FILL-S coil chain.
BLOCKED. Missing: the terminal marking on the K-FILL-S coil chain, and S-01 is an open
interface row. Owner: as P1-07.
WHY EVERY FLOAT LOOKS LIKE THIS: no float in this build switches a load. Each one
interrupts a coil circuit, so a broken float conductor stops the fill rather than
starting one.

**P1-18. Land CDR-056.** Far end: LS-6, page 6. The float's other terminal.
BLOCKED. Missing: as P1-17.

**P1-19. Land CDR-057.** Far end: LS-7, storage fill stop, page 6.
BLOCKED. Missing: as P1-17.

**P1-20. Land CDR-058.** Far end: LS-7, page 6. The float's other terminal.
BLOCKED. Missing: as P1-17.

## Day tank fill chain

**P1-21. Land CDR-047.** Far end: LS-1, day tank fill start, page 5.
BLOCKED. Missing: the terminal marking on the K-FILL-D coil chain, and S-02 is an open
interface row. Owner: as P1-07.

**P1-22. Land CDR-048.** Far end: LS-1, page 5. The float's other terminal.
BLOCKED. Missing: as P1-21.

**P1-23. Land CDR-049.** Far end: LS-5, day tank fill stop, page 5.
BLOCKED. Missing: as P1-21.
WHY THIS ONE IS WORTH CARE: nothing in this system measures a level, so LS-5 is the
only thing that knows the day tank is full. The overflow pipe is its second line and
there is no third.

**P1-24. Land CDR-050.** Far end: LS-5, page 5. The float's other terminal.
BLOCKED. Missing: as P1-21.

**P1-25. Land CDR-059.** Far end: LS-3, storage low, page 6. Sits in series in the
K-FILL-D coil chain.
BLOCKED. Missing: as P1-21.
READ THE FAR END TWICE: LS-3 is in the STORAGE tank and lands in the DAY TANK chain.
That is intended. It stops the transfer when the storage tank is low, rather than
dropping the whole plant.

**P1-26. Land CDR-060.** Far end: LS-3, page 6. The float's other terminal.
BLOCKED. Missing: as P1-21.

## Dry-run interlock

**P1-27. Land CDR-051.** Far end: LS-4, day tank low-low, page 5. Sits in series in
the K-DRY coil chain.
BLOCKED. Missing: the terminal marking on the K-DRY coil chain, and S-02. Owner: as
P1-07.
WHY: a broken conductor here de-energises K-DRY and stops the manifold pump. That is
the safe direction and it comes from the way the chain is built, not from a choice
anyone can undo at a terminal.

**P1-28. Land CDR-052.** Far end: LS-4, page 5. The float's other terminal.
BLOCKED. Missing: as P1-27.

## High-high floats

**These two floats stop the whole plant and stay stopped until a person resets it.**
A high-high trip means a fill-stop float has already failed, and if the trip cleared
itself when the level dropped, the machine would cycle between high-high and normal
forever and nobody would ever learn a float had failed. **The latch is what makes the
failure visible.**

**P1-29. Land CDR-053.** Far end: LS-2, day tank high-high, page 5. Sits in series in
the permissive string.
BLOCKED. Missing: the terminal marking on the permissive string, and S-02. Owner: as
P1-07.

**P1-30. Land CDR-054.** Far end: LS-2, page 5. The float's other terminal.
BLOCKED. Missing: as P1-29.

**P1-31. Land CDR-061.** Far end: LS-8, storage high-high, page 6. Sits in series in
the permissive string.
BLOCKED. Missing: the terminal marking on the permissive string, and S-01. Owner: as
P1-07.

**P1-32. Land CDR-062.** Far end: LS-8, page 6. The float's other terminal.
BLOCKED. Missing: as P1-31.

## Sense circuits to the display box

**All four are the same shape: a dry contact fed from 24 V, a light-emitting diode at
the far end inside the display box, and the loading resistor IN THIS PANEL.** The
resistor stays here so the contact keeps its load even when the cable is unplugged.

**P1-33. Land CDR-033.** Far end: the display box optocoupler, page 2. Carries the
permissive readback feed.
BLOCKED. Missing: the terminal marking on KM-DRV pole 2. Owner: as P1-07.
WHY THIS ONE HAS TWO BRANCHES AND THE OTHERS DO NOT: this contact needs 45 to 55 mA to
stay clean, which is more than the diode alone should carry continuously, so the
loading resistor is a second branch and it is a part rather than an option.

**P1-34. Land CDR-034.** Far end: the display box, page 2. Carries the readback loop
return.
BLOCKED. Missing: the terminal marking on the 24 V rail negative. Owner: as P1-07.

**P1-35. Land CDR-036.** Far end: the display box, page 2. Carries fill-in-progress,
from the normally closed leg of the K-FILL-D-Q changeover pole.
BLOCKED. Missing: the terminal marking on K-FILL-D-Q. Owner: as P1-07.
DO NOT COPY P1-33's ARRANGEMENT ONTO THIS ONE: this contact needs about 12.5 mA and
one branch carries it. A second branch here adds a part for nothing.

**P1-36. Land CDR-037.** Far end: the display box, page 2. Carries the dose-inhibit
leg, from the normally open leg of the SAME pole as P1-35.
BLOCKED. Missing: as P1-35.
CDR-036 AND CDR-037 MUST STAY IN ONE CABLE. They are the two legs of one changeover
and exactly one conducts at a time. If they are ever seen agreeing, the sense path is
broken - which is the whole reason there are two of them.

**P1-37. Land CDR-039.** Far end: the display box, page 2. Carries the dry-run relay
state, from the normally open leg of the K-DRY-Q changeover pole.
BLOCKED. Missing: the terminal marking on K-DRY-Q, and S-20 is an open interface row.
Owner: as P1-07.

**P1-38. Land CDR-040.** Far end: the display box, page 2. The complement of CDR-039,
from the normally closed leg of the SAME pole.
BLOCKED. Missing: as P1-37.
SAME RULE AS P1-36: one pole, one cable, and both legs agreeing means a broken path.

**One thing about KM-DRV while you are at it, and it is marked rather than solved:**
pole 1 carries the motor supply and arcs, and pole 2 is this quiet sense pole, in the
same device. There is nowhere else for the sense pole to go. **Do not move it on your
own judgement.**

## Permissive coil drive

**P1-39. Land CDR-030.** Far end: the display box logic board output, page 2. This
conductor is the COIL RETURN: the device at the far end pulls it down, and the coil's
positive is taken here in the panel.
BLOCKED. Missing: the terminal marking on the KM-DRV coil, and S-07 is an open
interface row which must still say where the coil positive is taken from. Owner: as
P1-07.
WHY THE DIRECTION MATTERS: the far device can only sink. Wired the other way round the
coil can never operate, and both ends still look correct on their own.

**P1-40. Land CDR-031.** Far end: the display box logic board common, page 2. Carries
the shared common the far device switches against.
BLOCKED. Missing: the terminal marking on the 24 V rail negative, and S-07. Owner: as
P1-07.
WHY THIS CONDUCTOR EXISTS AT ALL: without it no current can flow, and both ends still
land correctly and look finished. Trace the loop by hand before you believe it.

## Leak console

**P1-41. Land CDR-063.** Far end: the leak console, page 8. Carries the console supply
positive.
BLOCKED. Missing: the terminal marking on the 24 V rail positive, and CBL-06 is an
open interface row. Owner: as P1-07.
WHY THIS CABLE IS HEAVIER THAN 24 V NEEDS: the same jacket carries the console's
contact legs, which sit in the 120 V chain, so every conductor in it takes the higher
insulation rating including this one.

**P1-42. Land CDR-064.** Far end: the leak console, page 8. Carries the console supply
return.
BLOCKED. Missing: as P1-41.
WHAT HAPPENS IF IT BREAKS, NOW ANSWERED: the console's contact is closed only while it
is powered and dry. A broken supply and a wet floor do the same thing - the contact
opens and the permissive drops. **A dead leak detector cannot read as no leak.**

**The console's contact legs are not on this page.** MAIN-PANEL states which legs it
uses and has not yet.

## The ground bar. Last, and all together

**P1-43. Land CDR-004.** Far end: pump box A local bar, page 3. Brings box A's local
bar home.
BLOCKED. Missing: the terminal marking on the ground bar, which is not bought yet.
Owner: MAIN-PANEL provides the bar.

**P1-44. Land CDR-007.** Far end: pump box B local bar, page 4.
BLOCKED. Missing: as P1-43.

**P1-45. Land CDR-032.** Far end: the display box local bar, page 2.
BLOCKED. Missing: as P1-43.

**P1-46. Land CDR-035.** Far end: the display box local bar, page 2.
BLOCKED. Missing: as P1-43.

**P1-47. Land CDR-038.** Far end: the display box local bar, page 2.
BLOCKED. Missing: as P1-43.

**P1-48. Land CDR-041.** Far end: the display box local bar, page 2.
BLOCKED. Missing: as P1-43.

**Three things about this group:**

- **One green conductor per CABLE, not one per device.** The bars are joined to each
  other; individual devices do not each run back here.
- **Do not fit a grounding terminal block on the DIN rail anywhere in this build.** It
  bonds to the rail, the rail bonds to the backplate, and the backplate is plastic, so
  it bonds to nothing. Seven were bought on the parallel build and are going back.
- **A conductor landing on this bar is insulated for the highest voltage anywhere on
  the bar**, not for what it carries. The ground is common to everything, so the bar
  is in the 120 V chain even where the box around it holds only 24 V.

---

# PAGE 2. DISPLAY BOX

**Cables enter the BOTTOM face.** Left to right facing the display: probes alone at one
end, then the two driver cables, then the coil drive, then the two changeover pairs,
then the readback, then the Pi supply at the far end.

**One entry is not a gland: the Pi supply crosses at a panel-mount USB-C bulkhead.** A
USB-C plug will not fit through a gland bore and the cable is not one to cut and
re-make. **There is no joint to do for it and it is not on this page.**

**BEFORE YOU LAND ANYTHING IN THIS BOX:** each of the three EZO circuits ships set to
UART and has to be moved to I2C with a jumper, and the jumper is not in the same place
on all three. **Do that with the box open, before wiring, because the box has to be
open for it and you will not want to open it again.**

**P2-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P2-02. Write the conductor's label on one end.**
Where the step gives a channel token as well, write both, unabbreviated and not run
together.
ACCEPT: the label reads exactly what the joint step says, character for character.

**P2-03. Write the same label on the other end.**
ACCEPT: both ends read the same.
WHY: a conductor labelled at one end only is worse than one labelled at neither. In
this box sixteen conductors look identical and none of their terminals has a name yet.

**P2-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P2-05. Look at what is already under the terminal, then land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**P2-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.

## Driver logic supply

**P2-07. Land CDR-008.** Far end: pump box A driver VDD, page 3. Carries the driver
logic supply to box A. It stays live when the permissive drops; only motor supply is
removed.
BLOCKED. Missing: the terminal marking on the 5 V rail. Owner: anyone with the part in
hand and a pen.
WHY IT IS NOT SWITCHED, AND WHY THAT MATTERS HERE: if this conductor is broken while
the logic board is still driving step and direction into those pins, that is the one
condition the drivers must never see. It pushes current through their input protection
on four drivers at once.

**P2-08. Land CDR-009.** Far end: pump box A driver ground, page 3. Carries the logic
supply return, and it is also the reference the step and direction levels are measured
against.
BLOCKED. Missing: the terminal marking on the 5 V return. Owner: as P2-07.
WHY BOTH: without this common the far board does nothing and both ends still look
correctly landed.

**P2-09. Land CDR-011.** Far end: pump box B driver VDD, page 4.
BLOCKED. Missing: as P2-07.

**P2-10. Land CDR-012.** Far end: pump box B driver ground, page 4.
BLOCKED. Missing: as P2-08.

## Step and direction. Sixteen conductors

**Channels CH1 to CH4 go to pump box A. Channels CH5 to CH8 go to pump box B.**
Straight split, in order, nothing interleaved, so you can tell which channels are in a
box by looking at the box rather than at a table.

**Write the channel token on the conductor as well as its CDR number.** Do not
shorten either and do not run them together. The token is the same at both ends and
does not start again at CH1 in the second box.

**P2-11. Land CDR-014.** Far end: the CH1 driver, box A, page 3. Carries step pulses
for CH1. Label: CDR-014 and CH1.
BLOCKED. Missing: the terminal marking on the logic board, which does not exist yet,
and S-10 is an open interface row. Owner: DISPLAY-BOX for the board; BOSS for S-10.
WHY A BROKEN STEP LINE IS NOT SIMPLY NO STEPS: it leaves an input floating on a driver
that is switched on by default, in a box where four motor drives are running. Noise can
clock it and nothing anywhere records the doses it produces.

**P2-12. Land CDR-015.** Far end: the CH1 driver, box A, page 3. Carries direction for
CH1. Label: CDR-015 and CH1.
BLOCKED. Missing: as P2-11.
WHY THIS IS THE WORST ONE IN THE BUILD: a broken direction line leaves the direction
undefined on a driver that is switched on by default. The head then runs backwards,
pulling from the manifold toward the jug, while the software counts it as a dose
delivered forward. Nothing measures direction and nothing measures delivery, so
nothing catches it.

**P2-13. Land CDR-016.** CH2 step, box A. Label: CDR-016 and CH2. BLOCKED as P2-11.
**P2-14. Land CDR-017.** CH2 direction, box A. Label: CDR-017 and CH2. BLOCKED as
P2-12, and the same warning applies.
**P2-15. Land CDR-018.** CH3 step, box A. Label: CDR-018 and CH3. BLOCKED as P2-11.
**P2-16. Land CDR-019.** CH3 direction, box A. Label: CDR-019 and CH3. BLOCKED as
P2-12, same warning.
**P2-17. Land CDR-020.** CH4 step, box A. Label: CDR-020 and CH4. BLOCKED as P2-11.
**P2-18. Land CDR-021.** CH4 direction, box A. Label: CDR-021 and CH4. BLOCKED as
P2-12, same warning.
**P2-19. Land CDR-022.** CH5 step, box B. Label: CDR-022 and CH5. BLOCKED as P2-11.
**P2-20. Land CDR-023.** CH5 direction, box B. Label: CDR-023 and CH5. BLOCKED as
P2-12, same warning.
**P2-21. Land CDR-024.** CH6 step, box B. Label: CDR-024 and CH6. BLOCKED as P2-11.
**P2-22. Land CDR-025.** CH6 direction, box B. Label: CDR-025 and CH6. BLOCKED as
P2-12, same warning.
**P2-23. Land CDR-026.** CH7 step, box B. Label: CDR-026 and CH7. BLOCKED as P2-11.
**P2-24. Land CDR-027.** CH7 direction, box B. Label: CDR-027 and CH7. BLOCKED as
P2-12, same warning.
**P2-25. Land CDR-028.** CH8 step, box B. Label: CDR-028 and CH8. BLOCKED as P2-11.
**P2-26. Land CDR-029.** CH8 direction, box B. Label: CDR-029 and CH8. BLOCKED as
P2-12, same warning.

**Sixteen more conductors will join these**, one return paired with every step and
direction line so that each signal's nearest neighbour is a ground return rather than
another signal. **They are required and not yet issued.** When they arrive, the two
cables to the pump boxes get new numbers and the old numbers are retired.

## Permissive coil drive

**P2-27. Land CDR-030.** Far end: the KM-DRV coil, page 1. This conductor is the coil
RETURN and this board pulls it down; the coil's positive is taken in the panel.
BLOCKED. Missing: the terminal marking on the logic board, which does not exist yet,
and S-07. Owner: DISPLAY-BOX; BOSS for S-07.
WHY THE DIRECTION MATTERS: this device can only sink. Wired the other way the coil can
never operate and every check still passes, because each end looks correct on its own.

**P2-28. Land CDR-031.** Far end: the 24 V rail negative, page 1. Carries the shared
common.
BLOCKED. Missing: as P2-27.

## Sense inputs

**All four arrive as a 24 V loop through a light-emitting diode in this box. The
loading resistor is in the main panel, not here.**

**P2-29. Land CDR-033.** Far end: KM-DRV pole 2, page 1. Permissive readback.
BLOCKED. Missing: the terminal marking on the logic board. Owner: DISPLAY-BOX.
WHAT A BREAK DOES, AND IT IS DELIBERATE: a cut cable or a dead diode leaves this input
high, which reads as the contactor having dropped. That is the safe way round and it
was chosen.

**P2-30. Land CDR-034.** Far end: the 24 V rail negative, page 1. Readback loop return.
BLOCKED. Missing: as P2-29.

**P2-31. Land CDR-036.** Far end: K-FILL-D-Q normally closed leg, page 1. Fill in
progress.
BLOCKED. Missing: as P2-29.
WHAT A BREAK DOES: it reads as FILLING, so dosing is held off. The failure is a stop,
not a permission.

**P2-32. Land CDR-037.** Far end: K-FILL-D-Q normally open leg, page 1. The
dose-inhibit leg.
BLOCKED. Missing: as P2-29.
CDR-036 AND CDR-037 COME FROM ONE POLE AND STAY IN ONE CABLE. If they ever read the
same, the sense path is broken, and telling you that is what the second one is for.

**P2-33. Land CDR-039.** Far end: K-DRY-Q normally open leg, page 1. Dry-run relay
state.
BLOCKED. Missing: the terminal marking on the logic board, and S-20 is an open
interface row. Owner: DISPLAY-BOX; BOSS for S-20.

**P2-34. Land CDR-040.** Far end: K-DRY-Q normally closed leg, page 1. The complement
of CDR-039.
BLOCKED. Missing: as P2-33.
SAME PAIR RULE AS P2-32.

**The return arrangement for these two pairs is not settled** - whether each loop takes
its own return or two loops share one. **That is one more conductor, or two, and
nobody can say which yet.**

## Grounding

**P2-35. Land CDR-010.** Far end: pump box A local bar, page 3.
BLOCKED. Missing: the terminal marking on this box's local bar, which is not bought.
Owner: MAIN-PANEL provides the bars.

**P2-36. Land CDR-013.** Far end: pump box B local bar, page 4.
BLOCKED. Missing: as P2-35.

**P2-37. Land CDR-032.** Far end: the main panel ground bar, page 1.
BLOCKED. Missing: as P2-35.
WHY THIS BOX HAS A BAR AT ALL: it is polycarbonate. Nothing bonds through the box
itself, so the bar is the only bonding point in it.

**P2-38. Land CDR-035.** Far end: the main panel ground bar, page 1.
BLOCKED. Missing: as P2-35.

**P2-39. Land CDR-038.** Far end: the main panel ground bar, page 1.
BLOCKED. Missing: as P2-35.

**P2-40. Land CDR-041.** Far end: the main panel ground bar, page 1.
BLOCKED. Missing: as P2-35.

---

# PAGE 3. PUMP BOX A

**This box holds channels CH1, CH2, CH3 and CH4.**

**Cables enter the BOTTOM of the box body, not the lid.** The lid carries the pump
heads and lifts off as a unit; anything landed on it drags wiring with it. **Two
entries: motor supply at the end where the drivers' power blocks face, step and
direction at the end where their pin headers face. Nothing crosses the box.**

**P3-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P3-02. Write the conductor's label on one end.**
Where the step gives a channel token as well, write both, unabbreviated and not run
together.
ACCEPT: the label reads exactly what the joint step says, character for character.

**P3-03. Write the same label on the other end.**
ACCEPT: both ends read the same.
WHY: eight of the conductors in this box look identical and their terminals have no
names yet.

**P3-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P3-05. Look at what is already under the terminal, then land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**P3-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.

## Motor supply

**P3-07. Land CDR-002.** Far end: KM-DRV pole 1, page 1. Motor supply positive.
BLOCKED. Missing: the marking on the driver supply terminal. Owner: anyone with the
board in hand and a pen.
DO NOT TAKE THE NAME FROM ANY DOCUMENT: this terminal is marked with a symbol and not
a word. Every file in this project called this pin by a name that is not printed on
the part.

**P3-08. Land CDR-003.** Far end: the 24 V rail negative, page 1. Motor supply return.
BLOCKED. Missing: as P3-07.

## Driver logic supply

**P3-09. Land CDR-008.** Far end: the display box 5 V rail, page 2. Driver logic
supply. It stays live when the permissive drops.
BLOCKED. Missing: the marking on the driver's logic supply pin. Owner: as P3-07.

**P3-10. Land CDR-009.** Far end: the display box 5 V return, page 2. Logic supply
return and level reference.
BLOCKED. Missing: as P3-09.

## Step and direction, CH1 to CH4

**P3-11. Land CDR-014.** Far end: the display box logic board, page 2. CH1 step.
Label: CDR-014 and CH1.
BLOCKED. Missing: the marking on the driver's step pin, and S-10 is an open interface
row. Owner: as P3-07; BOSS for S-10.
DO NOT WORK OUT WHICH DRIVER IS CH1 FROM ITS POSITION ON THE PLATE. The channel is
whatever the token says it is at both ends, and a driver fed by the wrong channel doses
the wrong product every batch and passes every check in the machine.

**P3-12. Land CDR-015.** CH1 direction. Label: CDR-015 and CH1.
BLOCKED. Missing: as P3-11.
WHY THIS ONE MATTERS MOST: with this conductor broken the head can run backwards and
pull from the manifold into the jug, while the software counts a dose forward.

**P3-13. Land CDR-016.** CH2 step. Label: CDR-016 and CH2. BLOCKED as P3-11.
**P3-14. Land CDR-017.** CH2 direction. Label: CDR-017 and CH2. BLOCKED as P3-12.
**P3-15. Land CDR-018.** CH3 step. Label: CDR-018 and CH3. BLOCKED as P3-11.
**P3-16. Land CDR-019.** CH3 direction. Label: CDR-019 and CH3. BLOCKED as P3-12.
**P3-17. Land CDR-020.** CH4 step. Label: CDR-020 and CH4. BLOCKED as P3-11.
**P3-18. Land CDR-021.** CH4 direction. Label: CDR-021 and CH4. BLOCKED as P3-12.

## Grounding

**P3-19. Land CDR-004.** Far end: the main panel ground bar, page 1. Brings this box's
local bar home.
BLOCKED. Missing: the marking on this box's local bar, which is not bought. Owner:
MAIN-PANEL provides the bars.
WHY THIS BOX HAS A BAR: it is plastic. Nothing bonds through the box, so the local bar
is the only bonding point in it and nothing else in here bonds anywhere.

**P3-20. Land CDR-010.** Far end: the display box local bar, page 2.
BLOCKED. Missing: as P3-19.

**One thing in this box that is not a conductor and is not on this page:** each driver
has a pull-down resistor on its direction input. **It is a safety part whose failure is
silent: a lead that has backed out leaves a floating input on a driver that is switched
on, and the box looks correctly built.** It is checked with a meter at commissioning,
one driver at a time.

---

# PAGE 4. PUMP BOX B

**This box holds channels CH5, CH6, CH7 and CH8.**

**Same face and same entry order as box A. These two boxes are built the same way
round - left is left on both - so do not mirror anything.**

**P4-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P4-02. Write the conductor's label on one end.**
Where the step gives a channel token as well, write both.
ACCEPT: the label reads exactly what the joint step says, character for character.

**P4-03. Write the same label on the other end.**
ACCEPT: both ends read the same.

**P4-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P4-05. Look at what is already under the terminal, then land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**P4-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.

## Motor supply

**P4-07. Land CDR-005.** Far end: KM-DRV pole 1, page 1. Motor supply positive.
BLOCKED. Missing: the marking on the driver supply terminal. Owner: anyone with the
board in hand and a pen.
DO NOT TAKE THE NAME FROM ANY DOCUMENT: the terminal is marked with a symbol, not a
word.

**P4-08. Land CDR-006.** Far end: the 24 V rail negative, page 1. Motor supply return.
BLOCKED. Missing: as P4-07.

## Driver logic supply

**P4-09. Land CDR-011.** Far end: the display box 5 V rail, page 2. Driver logic
supply.
BLOCKED. Missing: the marking on the driver's logic supply pin. Owner: as P4-07.

**P4-10. Land CDR-012.** Far end: the display box 5 V return, page 2. Logic supply
return and level reference.
BLOCKED. Missing: as P4-09.

## Step and direction, CH5 to CH8

**P4-11. Land CDR-022.** Far end: the display box logic board, page 2. CH5 step.
Label: CDR-022 and CH5.
BLOCKED. Missing: the marking on the driver's step pin, and S-10. Owner: as P4-07;
BOSS for S-10.
DO NOT WORK OUT WHICH DRIVER IS CH5 FROM ITS POSITION ON THE PLATE.

**P4-12. Land CDR-023.** CH5 direction. Label: CDR-023 and CH5.
BLOCKED. Missing: as P4-11.
WHY THIS ONE MATTERS MOST: with this conductor broken the head can run backwards and
pull from the manifold into the jug, while the software counts a dose forward.

**P4-13. Land CDR-024.** CH6 step. Label: CDR-024 and CH6. BLOCKED as P4-11.
**P4-14. Land CDR-025.** CH6 direction. Label: CDR-025 and CH6. BLOCKED as P4-12.
**P4-15. Land CDR-026.** CH7 step. Label: CDR-026 and CH7. BLOCKED as P4-11.
**P4-16. Land CDR-027.** CH7 direction. Label: CDR-027 and CH7. BLOCKED as P4-12.
**P4-17. Land CDR-028.** CH8 step. Label: CDR-028 and CH8. BLOCKED as P4-11.
**P4-18. Land CDR-029.** CH8 direction. Label: CDR-029 and CH8. BLOCKED as P4-12.

## Grounding

**P4-19. Land CDR-007.** Far end: the main panel ground bar, page 1.
BLOCKED. Missing: the marking on this box's local bar, which is not bought. Owner:
MAIN-PANEL provides the bars.

**P4-20. Land CDR-013.** Far end: the display box local bar, page 2.
BLOCKED. Missing: as P4-19.

**Same pull-down note as box A applies here**, on all four drivers.

---

# PAGE 5. DAY TANK STANDPIPE

**There is no box here and no face to choose.** The cords run UP the pipe, tied at
intervals, and leave through a grip with the drip loop OUTSIDE the box.

**Float cords and pump cords go in SEPARATE TIE GROUPS.** Two pump cords share this
pipe and they are 120 VAC.

**THE FLOAT CORD IS NOT A CABLE YOU CUT.** Its weight clamps onto it, the tie is the
trip height, and setting a level later means moving the tie and never the wiring. **If
a cord will not reach, stop. That is a purchase, not a splice.**

**BEFORE ANYTHING GOES IN THE TANK: mark every trip height on the pipe.** Nothing in
this system measures a level, so a float that has slipped is invisible unless the pipe
carries its own scale.

**P5-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P5-02. Write the conductor's label on one end.**
ACCEPT: the label reads exactly what the joint step says, character for character.

**P5-03. Write the same label on the other end.**
ACCEPT: both ends read the same.
WHY: eight conductors leave this pipe and four of the floats look alike.

**P5-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P5-05. Look at what is already under the terminal, then land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**P5-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.

**Both conductors of every float go all the way to the panel. No float is joined to
another out here.** That way each float can be tested on its own with a meter at the
panel, and a failed one is identified instead of a chain being open somewhere.

**P5-07. Land CDR-047.** Far end: the K-FILL-D coil chain, page 1. LS-1, day tank fill
start, one terminal.
BLOCKED. Missing: the float part is not chosen and its terminals have no marking.
Owner: WATER returns the float; S-02 is open.

**P5-08. Land CDR-048.** LS-1, the other terminal. Far end: page 1.
BLOCKED. Missing: as P5-07.

**P5-09. Land CDR-049.** Far end: the K-FILL-D coil chain, page 1. LS-5, day tank fill
stop, one terminal.
BLOCKED. Missing: as P5-07.
WHY THIS FLOAT IS THE IMPORTANT ONE: it is the only thing that knows the day tank is
full. The overflow pipe is its second line and there is no third.

**P5-10. Land CDR-050.** LS-5, the other terminal. BLOCKED. Missing: as P5-07.

**P5-11. Land CDR-051.** Far end: the K-DRY coil chain, page 1. LS-4, day tank
low-low, one terminal. This is the float that stops the manifold pump running dry.
BLOCKED. Missing: as P5-07.

**P5-12. Land CDR-052.** LS-4, the other terminal. BLOCKED. Missing: as P5-07.

**P5-13. Land CDR-053.** Far end: the permissive string, page 1. LS-2, day tank
high-high, one terminal.
BLOCKED. Missing: as P5-07.
WHAT THIS FLOAT DOES: it stops the whole plant and it stays stopped until a person
resets it. If it has tripped, LS-5 has already failed, and a trip that cleared itself
would hide that forever.

**P5-14. Land CDR-054.** LS-2, the other terminal. BLOCKED. Missing: as P5-07.

**One thing to know before the floats are chosen: six of the eight in this build close
on LOW water and two close on HIGH, and once they are on the pipe you cannot tell them
apart by looking.**

---

# PAGE 6. STORAGE STANDPIPE

**Same rules as page 5: cords up the pipe, drip loop outside the box, separate tie
groups, the cord is never cut, and every trip height marked on the pipe before
anything goes in the tank.**

**P6-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P6-02. Write the conductor's label on one end.**
ACCEPT: the label reads exactly what the joint step says, character for character.

**P6-03. Write the same label on the other end.**
ACCEPT: both ends read the same.

**P6-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P6-05. Look at what is already under the terminal, then land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**P6-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.

**Both conductors of every float go all the way to the panel**, for the same reason as
page 5.

**P6-07. Land CDR-055.** Far end: the K-FILL-S coil chain, page 1. LS-6, storage fill
start, one terminal.
BLOCKED. Missing: the float part is not chosen and its terminals have no marking.
Owner: WATER returns the float; S-01 is open.

**P6-08. Land CDR-056.** LS-6, the other terminal. BLOCKED. Missing: as P6-07.

**P6-09. Land CDR-057.** Far end: the K-FILL-S coil chain, page 1. LS-7, storage fill
stop, one terminal.
BLOCKED. Missing: as P6-07.

**P6-10. Land CDR-058.** LS-7, the other terminal. BLOCKED. Missing: as P6-07.

**P6-11. Land CDR-059.** Far end: **the K-FILL-D coil chain**, page 1. LS-3, storage
low pump-down, one terminal.
BLOCKED. Missing: as P6-07.
READ THAT FAR END TWICE: this float is in the STORAGE tank and lands in the DAY TANK
fill chain. It is the one float whose chain is not the one its tank suggests, and it is
intended: a low storage tank stops the transfer rather than dropping the plant.

**P6-12. Land CDR-060.** LS-3, the other terminal. Far end: the K-FILL-D coil chain,
page 1. BLOCKED. Missing: as P6-07.

**P6-13. Land CDR-061.** Far end: the permissive string, page 1. LS-8, storage
high-high, one terminal.
BLOCKED. Missing: as P6-07.
WHAT THIS FLOAT DOES: as LS-2 on page 5. It stops the whole plant and stays stopped
until a person resets it.

**P6-14. Land CDR-062.** LS-8, the other terminal. BLOCKED. Missing: as P6-07.

---

# PAGE 7. FILL SOLENOID

**No box. The entries are the valve's own.**

**P7-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P7-02. Write the conductor's label on one end.**
ACCEPT: the label reads exactly what the joint step says, character for character.

**P7-03. Write the same label on the other end.**
ACCEPT: both ends read the same.

**P7-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P7-05. Look at what is already under the terminal, then land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**P7-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.

**P7-07. Land CDR-001.** Far end: K-FILL-S, page 1. Switched 120 VAC to the coil.
BLOCKED. Missing: the coil leads are not identified. Nobody has looked at the valve and
no file in this project says which lead is which. Owner: anyone with the valve in hand.

**P7-08. Land CDR-045.** Far end: neutral, page 1. Coil return.
BLOCKED. Missing: as P7-07.

**P7-09. Land CDR-046.** Far end: the ground bar, page 1. Equipment grounding for the
valve.
BLOCKED. Missing: the valve's grounding point is not identified. Owner: as P7-07.

**One thing worth knowing while you are at this valve: with no power it springs
CLOSED.** That was decided before the valve was chosen, and it is why a dead panel does
not leave a fill running.

---

# PAGE 8. LEAK CONSOLE

**Remote, in no box, fed through its own cord grip, with its sensor on the floor.**

**Where the sensor sits is a real question and not a convenience: it must not sit where
normal overflow discharge can splash or pool on it.** The floor drain is a track, and a
floor built to move water to a track hides a leak from a sensor sitting elsewhere on
it.

**P8-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say where the far end of this conductor goes without reading it again.

**P8-02. Write the conductor's label on one end.**
ACCEPT: the label reads exactly what the joint step says, character for character.

**P8-03. Write the same label on the other end.**
ACCEPT: both ends read the same.

**P8-04. Strip the end you are about to land.**
ACCEPT: every strand is intact and none is cut short.

**P8-05. Look at what is already under the terminal, then land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**P8-06. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.

**P8-07. Land CDR-063.** Far end: the 24 V rail positive, page 1. Console supply,
positive.
BLOCKED. Missing: the console's supply terminal marking, and CBL-06 is an open
interface row. Owner: anyone with the console in hand and a pen; BOSS for CBL-06.
WHY THIS CABLE IS HEAVIER THAN 24 V NEEDS: the same jacket carries the console's
contact legs, which sit in the 120 V chain, so every conductor in it takes the higher
insulation rating including this one.

**P8-08. Land CDR-064.** Far end: the 24 V rail negative, page 1. Console supply,
return.
BLOCKED. Missing: as P8-07.
WHAT HAPPENS IF THE CONSOLE LOSES POWER: its contact opens, exactly as it does for a
leak, and the permissive drops. **A dead leak detector cannot read as no leak.**

**Not on this page: the console's contact legs, and its sensor lead.** MAIN-PANEL
states which legs it uses and has not yet. The sensor lead comes with the sensor and
nothing lands its conductors here.

---

# WHAT IS BLOCKED, AND THE ONE THING THAT UNBLOCKS MOST OF IT

**173 numbered steps. 48 of them are the joint sequences, which are ready. 125 are
joints and every one of the 125 is blocked.**

| What is missing | Steps | Who |
|---|---|---|
| **The identifier printed on a terminal. Nobody has looked at a part and written it down** | **125**, every joint | **Anyone with the parts in hand and a pen.** It is not a decision, a purchase or a design |
| The logic board does not exist yet | 34 | DISPLAY-BOX |
| The float part is not chosen | 16 | WATER |
| Open interface rows behind whole groups: P-01, P-02, P-06, S-07, S-10, S-20, S-01, S-02, CBL-06 | in their groups | BOSS |
| The ground bars are not bought | 12 | MAIN-PANEL |
| The valve's coil leads are not identified | 3 | Anyone with the valve |

**Reading a terminal marking is the cheapest thing in this document and it is the only
blocker on every single joint.** One afternoon with the parts and a pen clears the
condition that stops all 125.

**Until then the labels are what carries the build.** That is why writing the label is
step 2 and 3 on every page and landing is step 5: **a conductor labelled at both ends
can be identified without knowing the name of the terminal it goes to.**

---

# WHAT IS NOT ON THESE PAGES, AND WHY

**Conductors inside the main panel that never leave it.** The rails, the permissive
string, the seal-in poles, the coil buses, the lamps and the loading resistors. They
are rows in D5 that MAIN-PANEL fills, and they will appear on page 1 when they exist.
**Page 1 as it stands is the crossings only.**

**Any route between two boxes.** No step above says which way a cable runs on the wall,
because the wall layout does not exist. **That is not a missing field on these pages -
it is an open cell in D6, and it stays open while M-02 is open.**

**Two things reported rather than written onto a page**, because nothing in D4 may be a
fact of its own: document-plan.md still describes D4 as "one page per conductor", which
predates the ruling that made it a page per enclosure and is stale rather than wrong;
and the sixteen paired returns for step and direction are required and not yet issued,
so no step lands one.

---

# STATUS

**Stopped part way, and this document is finished only when somebody has tried to land
a wire from it.**

**Eight pages. 173 numbered steps, of which 125 are joints and all 125 are blocked.**
The numbers are page-scoped and none has been changed. **What exists is the order the
work is done in, one action per step, with the reason attached wherever a builder would
otherwise reasonably do it differently.**
