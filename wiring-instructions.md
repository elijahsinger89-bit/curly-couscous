# D4. Wiring instructions

**A page per enclosure. Regenerated 2026-09-23 from the corrected D5.**

**This is a VIEW of D5, wiring-schedule.md.** Nothing here is a fact of its own: every
conductor id, landing, label and warning comes from a CDR- row there. **Change a row
in D5 and this document changes with it.**

**WHY THIS ISSUE EXISTS.** A builder read of D4, D5 and D6 found that **this document
stated three things as settled that D5 recorded as open** - which channels are in which
pump box, where the two high-high floats land, and what the leak console does when its
supply fails. **Each was a real decision that had been entered here instead of at the
source.** A view that is ahead of its source is not a view, G-54. **The facts were
entered at D5 and this document was regenerated from it. Nothing was typed into a page.**

**The same read found a conductor missing altogether**, the leak console's grounding
conductor, now CDR-065. **This issue has 127 joints where the last had 125.**

**You need to know how to use tools. You do not need to know anything about this
machine. If it is not on the page it does not happen.**

**Take the page for the box in front of you and nothing else.** A conductor that runs
between two boxes appears on both pages, and each page tells you only the end you are
holding.

## What this document does NOT do, and it matters before you pick up a page

**NOTHING HERE MOUNTS, FITS, DRILLS OR FEEDS A CABLE THROUGH ANYTHING. This is a book
of landings and it assumes a built machine.**

**All of that is D1, the build book**, and each page below names the D1 sections it
needs by their BB- numbers. **"It is elsewhere" is not the same as "the builder was
told", so every page states it as a precondition rather than leaving it to be
noticed.** D1 section 31 is where this document is picked up, and its own rule is the
reason: **no conductor is landed on a part a later section installs.**

**Also not here:** conductors that never leave the main panel, which are D5 rows
MAIN-PANEL fills; and which way a cable runs on the wall, which is an open cell in D6
while M-02's arrangement half is open. **No step implies a route.**

## How to read a step

**Every step is numbered and the numbers are per page.** 3-09 is page 3, step 9.
**Numbers are never silently changed. If a step is ever inserted it takes a letter -
3-09a - and a REVISION line appears at the top of that page saying so.** There are no
revision lines yet.

**Steps 01 to 07 of every page are a LOOP. Run all seven, in order, once for every
joint step on that page.** They are printed in full on all eight pages and they are
identical on all eight.

**Nothing on a page refers to a step by its number.** Where one joint depends on
another, the other is named by its CDR- id, **because a step number is a position in a
list and a position changes when a list does.**

**Every step ends with ACCEPT: how you know it is right, checked at that moment.** If
you cannot see the accept condition, the step is not done.

**A step that says BLOCKED has no accept condition yet.** It says what is missing and
who owns it. **Do not substitute, do not pick a likely terminal, do not skip ahead.
Leave that joint and go to the next step.** A blocked step stays in its place so you
know you are stepping over it rather than finding out later that something was left
out.

**EVERY JOINT IN THIS DOCUMENT IS BLOCKED TODAY.** The pages are written so that the
work is ready the moment its blocker clears, and the closing section says which blocker
clears what.

---

# PAGE 1. MAIN PANEL

**Cables enter the BOTTOM face. Nothing but the five 22 mm devices goes in the top.**

**THE GROUND BAR IS THE ONLY BONDING POINT IN THIS PANEL.** If you find a convenient
screw, do not use it. Every green conductor in the build ends at that bar and nowhere
else, and all nine of this page's bar landings are in one group at the end.

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-17**, D1 section 13. The main panel backplate is populated and installed in the mounted enclosure, with its ground bar fitted. **Every device this page lands on is on that plate** - the rails, the relay sockets, the contactor, the fuse and the loading resistors of all four sense circuits. **No step on this page fits any of them.**

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing in the main panel is labelled at both ends, landed and ticked.**

**STEPS 1-01 TO 1-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**1-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**1-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**1-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**1-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**1-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**1-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**1-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## Supply

**1-08. Land CDR-042.**
THIS END: MAIN-PANEL, the line input `{terminal}`
FAR END: The building branch circuit. **It is on no page: it is not an enclosure**
CARRIES: Supply, line
LABEL, BOTH ENDS: CDR-042
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **P-01 is an OPEN interface row**, so nothing is built against it
WHY IT IS NOT JUST A MARKING: **no disconnecting means is named anywhere in this build.** Do not assume the branch breaker is it.

**1-09. Land CDR-043.**
THIS END: MAIN-PANEL, the neutral `{terminal}`
FAR END: The building branch circuit
CARRIES: Supply, neutral
LABEL, BOTH ENDS: CDR-043
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and P-01 is OPEN

## Fill solenoid

**1-10. Land CDR-001.**
THIS END: MAIN-PANEL, K-FILL-S, the solenoid pole
FAR END: The fill solenoid coil, **page 7**
CARRIES: Switched 120 VAC to the coil
LABEL, BOTH ENDS: CDR-001
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **P-02 is an OPEN interface row**
WHY THIS POLE IS NOT LIKE THE OTHERS: it makes and breaks **0.58 A of inrush**, not the 0.21 A the valve holds at. Anything chosen for the holding figure is chosen for the wrong event.

**1-11. Land CDR-045.**
THIS END: MAIN-PANEL, the neutral `{terminal}`
FAR END: The fill solenoid coil, **page 7**
CARRIES: Coil return
LABEL, BOTH ENDS: CDR-045
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and P-02 is OPEN

## Motor supply out to the pump boxes

**1-12. Land CDR-002.**
THIS END: MAIN-PANEL, KM-DRV pole 1
FAR END: Pump box A driver supply, **page 3**
CARRIES: Motor supply positive to box A
LABEL, BOTH ENDS: CDR-002
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **P-06 is an OPEN interface row**: both ends must agree the voltage and the conductor before either box is built
**BEFORE YOU LOOK UNDER THAT CLAMP: CDR-005 lands on this SAME TERMINAL, at the next step.** Two cables leave one terminal here and that is intended, and this is the only terminal on this page where a step tells you so in advance.

**1-13. Land CDR-005.**
THIS END: MAIN-PANEL, KM-DRV pole 1, **the same terminal CDR-002 lands on**
FAR END: Pump box B driver supply, **page 4**
CARRIES: Motor supply positive to box B
LABEL, BOTH ENDS: CDR-005
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and P-06 is OPEN

**1-14. Land CDR-003.**
THIS END: MAIN-PANEL, the 24 V rail negative
FAR END: Pump box A, **page 3**
CARRIES: Motor supply return, box A
LABEL, BOTH ENDS: CDR-003
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and P-06 is OPEN
**FIVE CONDUCTORS LAND ON THE 24 V RAIL NEGATIVE ON THIS PAGE: CDR-003, CDR-006, CDR-034, CDR-031 and CDR-064.** A rail is many terminals and no step can say which one is free when you get there, **so step 1-05's stop rule does not apply to the rail** - land on a free terminal and record how many are under it. **Two of RUN-007's and RUN-008's returns may join them later and are not yet enumerated.**

**1-15. Land CDR-006.**
THIS END: MAIN-PANEL, the 24 V rail negative
FAR END: Pump box B, **page 4**
CARRIES: Motor supply return, box B
LABEL, BOTH ENDS: CDR-006
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and P-06 is OPEN

## Storage fill chain

**1-16. Land CDR-055.**
THIS END: MAIN-PANEL, the K-FILL-S coil chain
FAR END: LS-6, storage fill start, **page 6**
CARRIES: One leg of a float in series in the coil chain
LABEL, BOTH ENDS: CDR-055
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **S-01 is an OPEN interface row**
WHY EVERY FLOAT LOOKS LIKE THIS: **no float in this build switches a load.** Each one interrupts a coil circuit, so a broken float conductor stops a fill rather than starting one.

**1-17. Land CDR-056.**
THIS END: MAIN-PANEL, the K-FILL-S coil chain
FAR END: LS-6, **page 6**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-056
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-01 is OPEN

**1-18. Land CDR-057.**
THIS END: MAIN-PANEL, the K-FILL-S coil chain
FAR END: LS-7, storage fill stop, **page 6**
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-057
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-01 is OPEN

**1-19. Land CDR-058.**
THIS END: MAIN-PANEL, the K-FILL-S coil chain
FAR END: LS-7, **page 6**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-058
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-01 is OPEN

## Day tank fill chain

**1-20. Land CDR-047.**
THIS END: MAIN-PANEL, the K-FILL-D coil chain
FAR END: LS-1, day tank fill start, **page 5**
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-047
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **S-02 is an OPEN interface row**

**1-21. Land CDR-048.**
THIS END: MAIN-PANEL, the K-FILL-D coil chain
FAR END: LS-1, **page 5**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-048
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-02 is OPEN

**1-22. Land CDR-049.**
THIS END: MAIN-PANEL, the K-FILL-D coil chain
FAR END: LS-5, day tank fill stop, **page 5**
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-049
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-02 is OPEN
WHY THIS ONE IS WORTH CARE: **nothing in this system measures a level, so LS-5 is the only thing that knows the day tank is full.** The overflow pipe is its second line and there is no third.

**1-23. Land CDR-050.**
THIS END: MAIN-PANEL, the K-FILL-D coil chain
FAR END: LS-5, **page 5**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-050
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-02 is OPEN

**1-24. Land CDR-059.**
THIS END: MAIN-PANEL, the K-FILL-D coil chain
FAR END: LS-3, storage low, **page 6**
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-059
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-01 is OPEN
**READ THE FAR END TWICE.** LS-3 is in the STORAGE tank and lands in the DAY TANK chain. That is intended: a low storage tank stops the transfer rather than dropping the whole plant.

**1-25. Land CDR-060.**
THIS END: MAIN-PANEL, the K-FILL-D coil chain
FAR END: LS-3, **page 6**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-060
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-01 is OPEN

## Dry-run interlock

**1-26. Land CDR-051.**
THIS END: MAIN-PANEL, the K-DRY coil chain
FAR END: LS-4, day tank low-low, **page 5**
CARRIES: Series leg, the dry-run element
LABEL, BOTH ENDS: CDR-051
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-02 is OPEN
WHY: a broken conductor here de-energises K-DRY and stops the manifold pump. **That is the safe direction and it comes from the way the chain is built, not from a choice anyone can undo at a terminal.**

**1-27. Land CDR-052.**
THIS END: MAIN-PANEL, the K-DRY coil chain
FAR END: LS-4, **page 5**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-052
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-02 is OPEN

## High-high floats

**These two floats stop the whole plant and it stays stopped until a person resets
it.** A high-high trip means a fill-stop float has already failed, and if the trip
cleared itself when the level dropped the machine would cycle between high-high and
normal forever and nobody would ever learn a float had failed. **The latch is what
makes the failure visible.**

**1-28. Land CDR-053.**
THIS END: MAIN-PANEL, the permissive string
FAR END: LS-2, day tank high-high, **page 5**
CARRIES: Series leg, overfill backstop
LABEL, BOTH ENDS: CDR-053
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen - **and for the permissive string that is not one device but a series path across sockets, so which physical terminal it is is MAIN-PANEL's and is not stated**; and S-02 is OPEN

**1-29. Land CDR-054.**
THIS END: MAIN-PANEL, the permissive string
FAR END: LS-2, **page 5**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-054
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-02 is OPEN

**1-30. Land CDR-061.**
THIS END: MAIN-PANEL, the permissive string
FAR END: LS-8, storage high-high, **page 6**
CARRIES: Series leg, overfill backstop
LABEL, BOTH ENDS: CDR-061
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen, as CDR-053; and S-01 is OPEN

**1-31. Land CDR-062.**
THIS END: MAIN-PANEL, the permissive string
FAR END: LS-8, **page 6**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-062
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-01 is OPEN

## Sense circuits to the display box

**All four are the same shape: a dry contact fed from 24 V, a light-emitting diode at
the far end inside the display box, and the loading resistor IN THIS PANEL.** The
resistor stays here so the contact keeps its load even when the cable is unplugged.
**The resistor is fitted on the backplate before this page starts - it is part of
BB-17 and no step here fits it.**

**1-32. Land CDR-033.**
THIS END: MAIN-PANEL, KM-DRV pole 2
FAR END: The display box optocoupler, **page 2**
CARRIES: Permissive readback, wetted feed
LABEL, BOTH ENDS: CDR-033
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen
WHY THIS ONE HAS TWO BRANCHES AND THE OTHERS DO NOT: **this contact needs 45 to 55 mA to stay clean.** The loading resistor is a second branch across the contact, and it is a part rather than an option.

**1-33. Land CDR-034.**
THIS END: MAIN-PANEL, the 24 V rail negative
FAR END: The display box, **page 2**
CARRIES: Readback loop return
LABEL, BOTH ENDS: CDR-034
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen

**1-34. Land CDR-036.**
THIS END: MAIN-PANEL, K-FILL-D-Q, the normally closed leg of the changeover pole
FAR END: The display box, **page 2**
CARRIES: Fill in progress. CLOSED means NO FILL
LABEL, BOTH ENDS: CDR-036
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen
**DO NOT COPY CDR-033's ARRANGEMENT ONTO THIS ONE:** this contact needs about 12.5 mA and one branch carries it. A second branch here adds a part for nothing.

**1-35. Land CDR-037.**
THIS END: MAIN-PANEL, K-FILL-D-Q, the normally open leg of **the SAME pole CDR-036 leaves**
FAR END: The display box, **page 2**
CARRIES: The dose-inhibit leg
LABEL, BOTH ENDS: CDR-037
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen
**CDR-036 AND CDR-037 MUST STAY IN ONE CABLE.** They are the two legs of one changeover and exactly one conducts at a time. **If they are ever seen agreeing, the sense path is broken** - which is the whole reason there are two of them.

**1-36. Land CDR-039.**
THIS END: MAIN-PANEL, K-DRY-Q, the normally open leg of the changeover pole
FAR END: The display box, **page 2**
CARRIES: Dry-run relay state
LABEL, BOTH ENDS: CDR-039
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **S-20 is an OPEN interface row**

**1-37. Land CDR-040.**
THIS END: MAIN-PANEL, K-DRY-Q, the normally closed leg of **the SAME pole CDR-039 leaves**
FAR END: The display box, **page 2**
CARRIES: The complement of CDR-039
LABEL, BOTH ENDS: CDR-040
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-20 is OPEN
**SAME RULE AS CDR-036 AND CDR-037:** one pole, one cable, and both legs agreeing means a broken path.

## Permissive coil drive

**1-38. Land CDR-030.**
THIS END: MAIN-PANEL, the KM-DRV coil
FAR END: The display box logic board output, **page 2**
CARRIES: **The coil RETURN.** The device at the far end pulls it down, and the coil's positive is taken here in the panel
LABEL, BOTH ENDS: CDR-030
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **S-07 is an OPEN interface row which must still state where the coil positive is taken from** - from raw 24 V, one shorted output device at the far end holds this contactor closed against the E-stop
WHY THE DIRECTION MATTERS: **the far device can only sink.** Wired the other way round the coil can never operate, and both ends still look correct on their own.

**1-39. Land CDR-031.**
THIS END: MAIN-PANEL, the 24 V rail negative
FAR END: The display box logic board common, **page 2**
CARRIES: The shared common the far device switches against
LABEL, BOTH ENDS: CDR-031
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and S-07 is OPEN
WHY THIS CONDUCTOR EXISTS AT ALL: **without it no current can flow, and both ends still land correctly and look finished.** Trace the loop by hand before you believe it.

## Leak console

**1-40. Land CDR-063.**
THIS END: MAIN-PANEL, the 24 V rail positive
FAR END: The leak console, **page 8**
CARRIES: Console supply, positive
LABEL, BOTH ENDS: CDR-063
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **CBL-06 is an OPEN interface row**
WHY THIS CABLE IS HEAVIER THAN 24 V NEEDS: **the same jacket carries the console's contact legs, which sit in the 120 V chain**, so every conductor in it takes the higher insulation rating including this one.

**1-41. Land CDR-064.**
THIS END: MAIN-PANEL, the 24 V rail negative
FAR END: The leak console, **page 8**
CARRIES: Console supply, return
LABEL, BOTH ENDS: CDR-064
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and CBL-06 is OPEN
WHAT HAPPENS IF IT BREAKS: **the console's output opens, exactly as it does for a leak, and the permissive drops.** A dead leak detector cannot read as no leak.

## The ground bar. Last, and all together

**EVERY GREEN CONDUCTOR IN THIS BUILD ENDS AT THIS BAR AND NOWHERE ELSE.** If you
find a convenient screw, do not use it.

**All nine are here and none is landed earlier in the page.** CDR-044 arrives with the
supply and CDR-046 with the valve, and both land on the bar rather than in those
groups, **because a page that says the bar is last and then lands on it thirty steps
earlier is a page that sends a builder at a part before admitting it does not exist.**

**1-42. Land CDR-004.**
THIS END: MAIN-PANEL, the ground bar
FAR END: Pump box A local bar, **page 3**
CARRIES: Brings box A's local bar home
LABEL, BOTH ENDS: CDR-004
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**1-43. Land CDR-007.**
THIS END: MAIN-PANEL, the ground bar
FAR END: Pump box B local bar, **page 4**
CARRIES: Brings box B's local bar home
LABEL, BOTH ENDS: CDR-007
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**1-44. Land CDR-032.**
THIS END: MAIN-PANEL, the ground bar
FAR END: The display box local bar, **page 2**
CARRIES: Grounding in the coil-drive jacket
LABEL, BOTH ENDS: CDR-032
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**1-45. Land CDR-035.**
THIS END: MAIN-PANEL, the ground bar
FAR END: The display box local bar, **page 2**
CARRIES: Grounding in the readback jacket
LABEL, BOTH ENDS: CDR-035
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**1-46. Land CDR-038.**
THIS END: MAIN-PANEL, the ground bar
FAR END: The display box local bar, **page 2**
CARRIES: Grounding in the S-03 jacket
LABEL, BOTH ENDS: CDR-038
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**1-47. Land CDR-041.**
THIS END: MAIN-PANEL, the ground bar
FAR END: The display box local bar, **page 2**
CARRIES: Grounding in the S-20 jacket
LABEL, BOTH ENDS: CDR-041
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**1-48. Land CDR-044.**
THIS END: MAIN-PANEL, the ground bar
FAR END: The building branch circuit. **It is on no page**
CARRIES: **The system's equipment ground, arriving at the single point**
LABEL, BOTH ENDS: CDR-044
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars; and P-01 is OPEN
WHY: **if this one is missing, every local bar in the build loses its path home at once and nothing reports it.**

**1-49. Land CDR-046.**
THIS END: MAIN-PANEL, the ground bar
FAR END: The fill solenoid, **page 7**
CARRIES: Equipment grounding for the valve
LABEL, BOTH ENDS: CDR-046
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars; and P-02 is OPEN

**1-50. Land CDR-065.**
THIS END: MAIN-PANEL, the ground bar
FAR END: The leak console, **page 8**
CARRIES: Equipment grounding for the console
LABEL, BOTH ENDS: CDR-065
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars; and CBL-06 is OPEN
**THIS CONDUCTOR WAS MISSING FROM D5 UNTIL 2026-09-23.** D6 always required it and the schedule had two conductors in the console's jacket where it needed three, so this page had eight bar landings where it needed nine.

---

# PAGE 2. DISPLAY BOX

**Cables enter the BOTTOM face.** Left to right facing the display: probes alone at one
end, then the two driver cables, then the coil drive, then the two changeover pairs,
then the readback, then the Pi supply at the far end.

**TWO OF THOSE EIGHT ENTRIES HAVE NO STEP ON THIS PAGE AND THAT IS CORRECT.** The
probe leads and the Pi's USB-C cable are supplied assemblies that end in connectors,
so nothing lands their conductors. **You will count eight entries and find six with
work.**

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-19**, D1 section 15. The display box back plate is populated and installed with its local ground bar fitted, **the logic board is built**, and **the three EZO circuits have been set to I2C and recorded per C-14**. The EZO jumpers are D1's work and are not a step here: **they are done with the box open, before the plate goes in, and the jumper is not in the same place on all three.**

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing in the display box is labelled at both ends, landed and ticked.**

**STEPS 2-01 TO 2-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**2-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**2-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**2-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**2-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**2-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**2-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**2-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## Driver logic supply

**2-08. Land CDR-008.**
THIS END: DISPLAY-BOX, the 5 V rail
FAR END: Pump box A driver VDD, **page 3**
CARRIES: Driver logic supply to box A. **It stays live when the permissive drops; only motor supply is removed**
LABEL, BOTH ENDS: CDR-008
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX
WHY IT IS NOT SWITCHED, AND WHY THAT MATTERS HERE: **if this conductor is broken while the logic board is still driving step and direction into those pins, that is the one condition the drivers must never see.** It pushes current through their input protection on four drivers at once.

**2-09. Land CDR-009.**
THIS END: DISPLAY-BOX, the 5 V return
FAR END: Pump box A driver ground, **page 3**
CARRIES: Logic supply return, **and the reference the step and direction levels are measured against**
LABEL, BOTH ENDS: CDR-009
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX
WHY BOTH: **without this common the far board does nothing and both ends still look correctly landed.**

**2-10. Land CDR-011.**
THIS END: DISPLAY-BOX, the 5 V rail
FAR END: Pump box B driver VDD, **page 4**
CARRIES: Driver logic supply to box B
LABEL, BOTH ENDS: CDR-011
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX

**2-11. Land CDR-012.**
THIS END: DISPLAY-BOX, the 5 V return
FAR END: Pump box B driver ground, **page 4**
CARRIES: Logic supply return and level reference
LABEL, BOTH ENDS: CDR-012
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX

## Step and direction. Sixteen conductors

**CH1 to CH4 go to pump box A in RUN-003. CH5 to CH8 go to pump box B in RUN-004.**
Straight split, in order, nothing interleaved, so you can tell which channels are in a
box by looking at the box rather than at a table. **D-178, and it is D5's row that says
so** - it was stated only here for eighteen days and that was a defect, F-119.

**Write the channel token on the conductor as well as its CDR number.** Do not shorten
either and do not run them together. **The token is the same at both ends and does not
start again at CH1 in the second box.**

**2-12. Land CDR-014.**
THIS END: DISPLAY-BOX, the logic board `{CH1 STEP}`
FAR END: The CH1 driver, **pump box A**, **page 3**
CARRIES: Step pulses, CH1
LABEL, BOTH ENDS: CDR-014 and CH1
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**
WHY A BROKEN STEP LINE IS NOT SIMPLY NO STEPS: **it leaves an input floating on a driver that is switched on by default**, in a box where four motor drives are running. Noise can clock it and nothing anywhere records the doses it produces.

**2-13. Land CDR-015.**
THIS END: DISPLAY-BOX, the logic board `{CH1 DIR}`
FAR END: The CH1 driver, **pump box A**, **page 3**
CARRIES: Direction, CH1
LABEL, BOTH ENDS: CDR-015 and CH1
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**2-14. Land CDR-016.**
THIS END: DISPLAY-BOX, the logic board `{CH2 STEP}`
FAR END: The CH2 driver, **pump box A**, **page 3**
CARRIES: Step pulses, CH2
LABEL, BOTH ENDS: CDR-016 and CH2
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**

**2-15. Land CDR-017.**
THIS END: DISPLAY-BOX, the logic board `{CH2 DIR}`
FAR END: The CH2 driver, **pump box A**, **page 3**
CARRIES: Direction, CH2
LABEL, BOTH ENDS: CDR-017 and CH2
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**2-16. Land CDR-018.**
THIS END: DISPLAY-BOX, the logic board `{CH3 STEP}`
FAR END: The CH3 driver, **pump box A**, **page 3**
CARRIES: Step pulses, CH3
LABEL, BOTH ENDS: CDR-018 and CH3
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**

**2-17. Land CDR-019.**
THIS END: DISPLAY-BOX, the logic board `{CH3 DIR}`
FAR END: The CH3 driver, **pump box A**, **page 3**
CARRIES: Direction, CH3
LABEL, BOTH ENDS: CDR-019 and CH3
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**2-18. Land CDR-020.**
THIS END: DISPLAY-BOX, the logic board `{CH4 STEP}`
FAR END: The CH4 driver, **pump box A**, **page 3**
CARRIES: Step pulses, CH4
LABEL, BOTH ENDS: CDR-020 and CH4
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**

**2-19. Land CDR-021.**
THIS END: DISPLAY-BOX, the logic board `{CH4 DIR}`
FAR END: The CH4 driver, **pump box A**, **page 3**
CARRIES: Direction, CH4
LABEL, BOTH ENDS: CDR-021 and CH4
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**2-20. Land CDR-022.**
THIS END: DISPLAY-BOX, the logic board `{CH5 STEP}`
FAR END: The CH5 driver, **pump box B**, **page 4**
CARRIES: Step pulses, CH5
LABEL, BOTH ENDS: CDR-022 and CH5
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**
WHY A BROKEN STEP LINE IS NOT SIMPLY NO STEPS: **it leaves an input floating on a driver that is switched on by default**, in a box where four motor drives are running. Noise can clock it and nothing anywhere records the doses it produces.

**2-21. Land CDR-023.**
THIS END: DISPLAY-BOX, the logic board `{CH5 DIR}`
FAR END: The CH5 driver, **pump box B**, **page 4**
CARRIES: Direction, CH5
LABEL, BOTH ENDS: CDR-023 and CH5
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**2-22. Land CDR-024.**
THIS END: DISPLAY-BOX, the logic board `{CH6 STEP}`
FAR END: The CH6 driver, **pump box B**, **page 4**
CARRIES: Step pulses, CH6
LABEL, BOTH ENDS: CDR-024 and CH6
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**

**2-23. Land CDR-025.**
THIS END: DISPLAY-BOX, the logic board `{CH6 DIR}`
FAR END: The CH6 driver, **pump box B**, **page 4**
CARRIES: Direction, CH6
LABEL, BOTH ENDS: CDR-025 and CH6
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**2-24. Land CDR-026.**
THIS END: DISPLAY-BOX, the logic board `{CH7 STEP}`
FAR END: The CH7 driver, **pump box B**, **page 4**
CARRIES: Step pulses, CH7
LABEL, BOTH ENDS: CDR-026 and CH7
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**

**2-25. Land CDR-027.**
THIS END: DISPLAY-BOX, the logic board `{CH7 DIR}`
FAR END: The CH7 driver, **pump box B**, **page 4**
CARRIES: Direction, CH7
LABEL, BOTH ENDS: CDR-027 and CH7
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**2-26. Land CDR-028.**
THIS END: DISPLAY-BOX, the logic board `{CH8 STEP}`
FAR END: The CH8 driver, **pump box B**, **page 4**
CARRIES: Step pulses, CH8
LABEL, BOTH ENDS: CDR-028 and CH8
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-10 is an OPEN interface row**

**2-27. Land CDR-029.**
THIS END: DISPLAY-BOX, the logic board `{CH8 DIR}`
FAR END: The CH8 driver, **pump box B**, **page 4**
CARRIES: Direction, CH8
LABEL, BOTH ENDS: CDR-029 and CH8
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

## Permissive coil drive

**2-28. Land CDR-030.**
THIS END: DISPLAY-BOX, the logic board output `{BCM 18}`, the sinking driver
FAR END: The KM-DRV coil, **page 1**
CARRIES: **The coil RETURN, and this board pulls it down.** The coil's positive is taken in the panel
LABEL, BOTH ENDS: CDR-030
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-07 is OPEN
WHY THE DIRECTION MATTERS: **this device can only sink.** Wired the other way the coil can never operate and every check still passes, because each end looks correct on its own.

**2-29. Land CDR-031.**
THIS END: DISPLAY-BOX, the logic board common
FAR END: The 24 V rail negative, **page 1**
CARRIES: The shared common
LABEL, BOTH ENDS: CDR-031
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-07 is OPEN

## Sense inputs

**All four arrive as a 24 V loop through a light-emitting diode in this box. The
loading resistor is in the main panel, not here.** Sense is inverted on every one.

**2-30. Land CDR-033.**
THIS END: DISPLAY-BOX, the S-08 optocoupler diode
FAR END: KM-DRV pole 2, **page 1**
CARRIES: Permissive readback
LABEL, BOTH ENDS: CDR-033
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX
WHAT A BREAK DOES, AND IT IS DELIBERATE: **a cut cable or a dead diode leaves this input high, which reads as the contactor having dropped.** That is the safe way round and it was chosen.

**2-31. Land CDR-034.**
THIS END: DISPLAY-BOX, the S-08 diode return
FAR END: The 24 V rail negative, **page 1**
CARRIES: Readback loop return
LABEL, BOTH ENDS: CDR-034
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX

**2-32. Land CDR-036.**
THIS END: DISPLAY-BOX, the S-03 optocoupler diode
FAR END: K-FILL-D-Q, the normally closed leg, **page 1**
CARRIES: Fill in progress
LABEL, BOTH ENDS: CDR-036
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX
WHAT A BREAK DOES: **it reads as FILLING, so dosing is held off.** The failure is a stop, not a permission.

**2-33. Land CDR-037.**
THIS END: DISPLAY-BOX, the dose-inhibit optocoupler diode
FAR END: K-FILL-D-Q, the normally open leg of the same pole, **page 1**
CARRIES: The dose-inhibit leg
LABEL, BOTH ENDS: CDR-037
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX
**CDR-036 AND CDR-037 COME FROM ONE POLE AND STAY IN ONE CABLE.** If they ever read the same, the sense path is broken, **and telling you that is what the second one is for.**

**2-34. Land CDR-039.**
THIS END: DISPLAY-BOX, the S-20 optocoupler diode
FAR END: K-DRY-Q, the normally open leg, **page 1**
CARRIES: Dry-run relay state
LABEL, BOTH ENDS: CDR-039
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and **S-20 is an OPEN interface row**

**2-35. Land CDR-040.**
THIS END: DISPLAY-BOX, the complement optocoupler diode
FAR END: K-DRY-Q, the normally closed leg of the same pole, **page 1**
CARRIES: The complement of CDR-039
LABEL, BOTH ENDS: CDR-040
BLOCKED. Missing: the display box logic board does not exist yet. Owner: DISPLAY-BOX; and S-20 is OPEN
**SAME PAIR RULE AS CDR-036 AND CDR-037.**

## Grounding

**This box is polycarbonate. Nothing bonds through the box itself, which is exactly
why it has a local bar**, and the bar is the only bonding point in it.

**2-36. Land CDR-010.**
THIS END: DISPLAY-BOX, the local ground bar
FAR END: Pump box A local bar, **page 3**
CARRIES: Grounding in the box A driver jacket
LABEL, BOTH ENDS: CDR-010
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**2-37. Land CDR-013.**
THIS END: DISPLAY-BOX, the local ground bar
FAR END: Pump box B local bar, **page 4**
CARRIES: Grounding in the box B driver jacket
LABEL, BOTH ENDS: CDR-013
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**2-38. Land CDR-032.**
THIS END: DISPLAY-BOX, the local ground bar
FAR END: The main panel ground bar, **page 1**
CARRIES: Grounding in the coil-drive jacket
LABEL, BOTH ENDS: CDR-032
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**2-39. Land CDR-035.**
THIS END: DISPLAY-BOX, the local ground bar
FAR END: The main panel ground bar, **page 1**
CARRIES: Grounding in the readback jacket
LABEL, BOTH ENDS: CDR-035
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**2-40. Land CDR-038.**
THIS END: DISPLAY-BOX, the local ground bar
FAR END: The main panel ground bar, **page 1**
CARRIES: Grounding in the S-03 jacket
LABEL, BOTH ENDS: CDR-038
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**2-41. Land CDR-041.**
THIS END: DISPLAY-BOX, the local ground bar
FAR END: The main panel ground bar, **page 1**
CARRIES: Grounding in the S-20 jacket
LABEL, BOTH ENDS: CDR-041
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

---

# PAGE 3. PUMP BOX A

**This box holds CH1, CH2, CH3 and CH4.**

**Cables enter the BOTTOM of the box body, not the lid.** The lid carries the pump
heads and lifts off as a unit; anything landed on it drags wiring with it. **Two
entries: motor supply at the end where the drivers' power blocks face, step and
direction at the end where their pin headers face. Nothing crosses the box.**

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-18**, D1 section 14. This box carries its motors and heads on its lid, its drivers and its local ground bar on the box body, every driver set the same way round, **with the lid not yet fitted.**

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing in pump box A is labelled at both ends, landed and ticked.**

**STEPS 3-01 TO 3-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**3-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**3-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**3-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**3-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**3-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**3-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**3-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## Motor supply

**3-08. Land CDR-002.**
THIS END: PUMP-BOX-A, the driver supply block `{+ side}`
FAR END: KM-DRV pole 1, **page 1**
CARRIES: Motor supply positive
LABEL, BOTH ENDS: CDR-002
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **P-06 is an OPEN interface row**
**DO NOT TAKE THE NAME FOR THIS TERMINAL FROM ANY DOCUMENT.** It is marked with a symbol and not a word, and every file in this project has called this pin by a name that is not printed on the part.

**3-09. Land CDR-003.**
THIS END: PUMP-BOX-A, the driver supply block `{- side}`
FAR END: The 24 V rail negative, **page 1**
CARRIES: Motor supply return
LABEL, BOTH ENDS: CDR-003
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and P-06 is OPEN

## Driver logic supply

**3-10. Land CDR-008.**
THIS END: PUMP-BOX-A, the driver `{VDD}`
FAR END: The display box 5 V rail, **page 2**
CARRIES: Driver logic supply. **It stays live when the permissive drops**
LABEL, BOTH ENDS: CDR-008
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and P-09's remaining half is open: what a driver does with STEP asserted and motor supply absent is uncharacterised

**3-11. Land CDR-009.**
THIS END: PUMP-BOX-A, the driver `{GND}`
FAR END: The display box 5 V return, **page 2**
CARRIES: Logic supply return and level reference
LABEL, BOTH ENDS: CDR-009
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen

## Step and direction, CH1 to CH4

**This box holds CH1, CH2, CH3 and CH4, and pump box B holds the
other four.** D-178, straight split, in order. **Write the channel token on the
conductor as well as its CDR number, unabbreviated and not run together.**

**3-12. Land CDR-014.**
THIS END: PUMP-BOX-A, the CH1 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH1
LABEL, BOTH ENDS: CDR-014 and CH1
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**
**DO NOT WORK OUT WHICH DRIVER IS CH1 FROM ITS POSITION ON THE PLATE.** The channel is whatever the token says it is at both ends, and **a driver fed by the wrong channel doses the wrong product every batch and passes every check in the machine.**

**3-13. Land CDR-015.**
THIS END: PUMP-BOX-A, the CH1 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH1
LABEL, BOTH ENDS: CDR-015 and CH1
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**3-14. Land CDR-016.**
THIS END: PUMP-BOX-A, the CH2 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH2
LABEL, BOTH ENDS: CDR-016 and CH2
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**

**3-15. Land CDR-017.**
THIS END: PUMP-BOX-A, the CH2 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH2
LABEL, BOTH ENDS: CDR-017 and CH2
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN

**3-16. Land CDR-018.**
THIS END: PUMP-BOX-A, the CH3 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH3
LABEL, BOTH ENDS: CDR-018 and CH3
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**

**3-17. Land CDR-019.**
THIS END: PUMP-BOX-A, the CH3 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH3
LABEL, BOTH ENDS: CDR-019 and CH3
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN

**3-18. Land CDR-020.**
THIS END: PUMP-BOX-A, the CH4 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH4
LABEL, BOTH ENDS: CDR-020 and CH4
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**

**3-19. Land CDR-021.**
THIS END: PUMP-BOX-A, the CH4 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH4
LABEL, BOTH ENDS: CDR-021 and CH4
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN

## Grounding

**This box is plastic. Nothing bonds through the box, so the local bar is the only
bonding point in it and nothing else in here bonds anywhere.**

**3-20. Land CDR-004.**
THIS END: PUMP-BOX-A, the local ground bar
FAR END: The main panel ground bar, **page 1**
CARRIES: Brings this box's local bar home
LABEL, BOTH ENDS: CDR-004
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**3-21. Land CDR-010.**
THIS END: PUMP-BOX-A, the local ground bar
FAR END: The display box local bar, **page 2**
CARRIES: Grounding in the driver jacket
LABEL, BOTH ENDS: CDR-010
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

---

# PAGE 4. PUMP BOX B

**This box holds CH5, CH6, CH7 and CH8.**

**Same face and same entry order as box A. These two boxes are built the same way round
- left is left on both - so do not mirror anything.**

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-18**, D1 section 14, as page 3.

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing in pump box B is labelled at both ends, landed and ticked.**

**STEPS 4-01 TO 4-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**4-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**4-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**4-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**4-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**4-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**4-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**4-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## Motor supply

**4-08. Land CDR-005.**
THIS END: PUMP-BOX-B, the driver supply block `{+ side}`
FAR END: KM-DRV pole 1, **page 1**
CARRIES: Motor supply positive
LABEL, BOTH ENDS: CDR-005
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **P-06 is an OPEN interface row**
**DO NOT TAKE THE NAME FOR THIS TERMINAL FROM ANY DOCUMENT.** It is marked with a symbol and not a word, and every file in this project has called this pin by a name that is not printed on the part.

**4-09. Land CDR-006.**
THIS END: PUMP-BOX-B, the driver supply block `{- side}`
FAR END: The 24 V rail negative, **page 1**
CARRIES: Motor supply return
LABEL, BOTH ENDS: CDR-006
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and P-06 is OPEN

## Driver logic supply

**4-10. Land CDR-011.**
THIS END: PUMP-BOX-B, the driver `{VDD}`
FAR END: The display box 5 V rail, **page 2**
CARRIES: Driver logic supply. **It stays live when the permissive drops**
LABEL, BOTH ENDS: CDR-011
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and P-09's remaining half is open: what a driver does with STEP asserted and motor supply absent is uncharacterised

**4-11. Land CDR-012.**
THIS END: PUMP-BOX-B, the driver `{GND}`
FAR END: The display box 5 V return, **page 2**
CARRIES: Logic supply return and level reference
LABEL, BOTH ENDS: CDR-012
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen

## Step and direction, CH5 to CH8

**This box holds CH5, CH6, CH7 and CH8, and pump box A holds the
other four.** D-178, straight split, in order. **Write the channel token on the
conductor as well as its CDR number, unabbreviated and not run together.**

**4-12. Land CDR-022.**
THIS END: PUMP-BOX-B, the CH5 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH5
LABEL, BOTH ENDS: CDR-022 and CH5
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**
**DO NOT WORK OUT WHICH DRIVER IS CH5 FROM ITS POSITION ON THE PLATE.** The channel is whatever the token says it is at both ends, and **a driver fed by the wrong channel doses the wrong product every batch and passes every check in the machine.**

**4-13. Land CDR-023.**
THIS END: PUMP-BOX-B, the CH5 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH5
LABEL, BOTH ENDS: CDR-023 and CH5
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN
**WHY THIS IS THE WORST ONE IN THE BUILD:** a broken direction line leaves the direction undefined on a driver that is switched on by default. **The head then runs backwards, pulling from the manifold toward the jug, while the software counts a dose delivered forward.** Nothing measures direction and nothing measures delivery, so nothing catches it. **The pull-down that fixes it goes at the DRIVER end and is not fitted.**

**4-14. Land CDR-024.**
THIS END: PUMP-BOX-B, the CH6 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH6
LABEL, BOTH ENDS: CDR-024 and CH6
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**

**4-15. Land CDR-025.**
THIS END: PUMP-BOX-B, the CH6 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH6
LABEL, BOTH ENDS: CDR-025 and CH6
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN

**4-16. Land CDR-026.**
THIS END: PUMP-BOX-B, the CH7 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH7
LABEL, BOTH ENDS: CDR-026 and CH7
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**

**4-17. Land CDR-027.**
THIS END: PUMP-BOX-B, the CH7 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH7
LABEL, BOTH ENDS: CDR-027 and CH7
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN

**4-18. Land CDR-028.**
THIS END: PUMP-BOX-B, the CH8 driver `{STEP}`
FAR END: The display box logic board, **page 2**
CARRIES: Step pulses, CH8
LABEL, BOTH ENDS: CDR-028 and CH8
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and **S-10 is an OPEN interface row**

**4-19. Land CDR-029.**
THIS END: PUMP-BOX-B, the CH8 driver `{DIR}`
FAR END: The display box logic board, **page 2**
CARRIES: Direction, CH8
LABEL, BOTH ENDS: CDR-029 and CH8
BLOCKED. Missing: the marking on the driver terminal has not been read. **The terminal carries a SYMBOL, not a word, and every file in this project has called this pin by a name that is not printed on the part.** Owner: anyone with a board in hand and a pen; and S-10 is OPEN

## Grounding

**This box is plastic. Nothing bonds through the box, so the local bar is the only
bonding point in it and nothing else in here bonds anywhere.**

**4-20. Land CDR-007.**
THIS END: PUMP-BOX-B, the local ground bar
FAR END: The main panel ground bar, **page 1**
CARRIES: Brings this box's local bar home
LABEL, BOTH ENDS: CDR-007
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

**4-21. Land CDR-013.**
THIS END: PUMP-BOX-B, the local ground bar
FAR END: The display box local bar, **page 2**
CARRIES: Grounding in the driver jacket
LABEL, BOTH ENDS: CDR-013
BLOCKED. Missing: the ground bar is not bought. Owner: MAIN-PANEL provides all four bars

---

# PAGE 5. DAY TANK STANDPIPE

**There is no enclosure here.** The float cords run UP the pipe, tied at intervals in
the float tie group, and leave the tank through a cord grip with the drip loop OUTSIDE
the grip.

**THE FLOAT CORD IS NOT A CABLE YOU CUT.** Its weight clamps onto it and the tie is the
trip height. **If a cord will not reach the panel, stop: that is a purchase, not a
splice**, and cutting one moves a trip height you cannot put back.

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-25**, D1 section 21. Every trip height is marked permanently on each pipe. **The heights are D1's and no step here states one.**
- **BB-26**, D1 section 22. Every float is clamped at its mark and every cord is laid and tied on its pipe in the float tie group.
- **BB-27**, D1 section 23. Both standpipes are hung in their tanks and **every float cord is already out through its tank's cord grip.** Nothing on this page feeds a cord through anything.

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing at a day tank float is labelled at both ends, landed and ticked.**

**STEPS 5-01 TO 5-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**5-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**5-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**5-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**5-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**5-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**5-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**5-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## The four day tank floats

**Both conductors of every float go all the way to the panel. No float is joined to
another out here**, so each one can be tested on its own with a meter at the panel and
a failed float is identified instead of a chain being open somewhere.

**5-08. Land CDR-047.**
THIS END: LS-1, day tank fill start `{terminal}`, on the standpipe
FAR END: The K-FILL-D coil chain, **page 1**
CARRIES: One leg of a series element in a coil chain
LABEL, BOTH ENDS: CDR-047
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and **S-02 is an OPEN interface row**

**5-09. Land CDR-048.**
THIS END: LS-1, day tank fill start `{terminal}`, on the standpipe
FAR END: The K-FILL-D coil chain, **page 1**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-048
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-02 is OPEN

**5-10. Land CDR-049.**
THIS END: LS-5, day tank fill stop `{terminal}`, on the standpipe
FAR END: The K-FILL-D coil chain, **page 1**
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-049
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-02 is OPEN
**WHY THIS FLOAT IS THE IMPORTANT ONE:** it is the only thing that knows the day tank is full. The overflow pipe is its second line and there is no third.

**5-11. Land CDR-050.**
THIS END: LS-5, day tank fill stop `{terminal}`, on the standpipe
FAR END: The K-FILL-D coil chain, **page 1**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-050
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-02 is OPEN

**5-12. Land CDR-051.**
THIS END: LS-4, day tank low-low `{terminal}`, on the standpipe
FAR END: The K-DRY coil chain, **page 1**
CARRIES: Series leg. **This is the float that stops the manifold pump running dry**
LABEL, BOTH ENDS: CDR-051
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-02 is OPEN

**5-13. Land CDR-052.**
THIS END: LS-4, day tank low-low `{terminal}`, on the standpipe
FAR END: The K-DRY coil chain, **page 1**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-052
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-02 is OPEN

**5-14. Land CDR-053.**
THIS END: LS-2, day tank high-high `{terminal}`, on the standpipe
FAR END: The permissive string, **page 1**
CARRIES: Series leg, overfill backstop
LABEL, BOTH ENDS: CDR-053
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-02 is OPEN
**WHAT THIS FLOAT DOES:** it stops the whole plant and it stays stopped until a person resets it. **If it has tripped, LS-5 has already failed**, and a trip that cleared itself would hide that forever.

**5-15. Land CDR-054.**
THIS END: LS-2, day tank high-high `{terminal}`, on the standpipe
FAR END: The permissive string, **page 1**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-054
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-02 is OPEN

---

# PAGE 6. STORAGE STANDPIPE

**Same as page 5: no enclosure, cords up the pipe in the float tie group, out through
the tank's cord grip with the drip loop outside it, and the cord is never cut.**

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-25**, **BB-26** and **BB-27**, D1 sections 21, 22 and 23, as page 5.

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing at a storage float is labelled at both ends, landed and ticked.**

**STEPS 6-01 TO 6-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**6-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**6-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**6-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**6-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**6-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**6-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**6-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## The four storage floats

**Both conductors of every float go all the way to the panel**, for the same reason as
page 5.

**6-08. Land CDR-055.**
THIS END: LS-6, storage fill start `{terminal}`, on the standpipe
FAR END: The K-FILL-S coil chain, **page 1**
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-055
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and **S-01 is an OPEN interface row**

**6-09. Land CDR-056.**
THIS END: LS-6, storage fill start `{terminal}`, on the standpipe
FAR END: The K-FILL-S coil chain, **page 1**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-056
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-01 is OPEN

**6-10. Land CDR-057.**
THIS END: LS-7, storage fill stop `{terminal}`, on the standpipe
FAR END: The K-FILL-S coil chain, **page 1**
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-057
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-01 is OPEN

**6-11. Land CDR-058.**
THIS END: LS-7, storage fill stop `{terminal}`, on the standpipe
FAR END: The K-FILL-S coil chain, **page 1**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-058
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-01 is OPEN

**6-12. Land CDR-059.**
THIS END: LS-3, storage low pump-down `{terminal}`, on the standpipe
FAR END: **The K-FILL-D coil chain**, page 1
CARRIES: Series leg
LABEL, BOTH ENDS: CDR-059
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-01 is OPEN
**READ THAT FAR END TWICE.** This float is in the STORAGE tank and lands in the DAY TANK fill chain. **It is the one float whose chain is not the one its tank suggests**, and it is intended: a low storage tank stops the transfer rather than dropping the plant.

**6-13. Land CDR-060.**
THIS END: LS-3, storage low pump-down `{terminal}`, on the standpipe
FAR END: **The K-FILL-D coil chain**, page 1
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-060
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-01 is OPEN

**6-14. Land CDR-061.**
THIS END: LS-8, storage high-high `{terminal}`, on the standpipe
FAR END: The permissive string, **page 1**
CARRIES: Series leg, overfill backstop
LABEL, BOTH ENDS: CDR-061
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-01 is OPEN
**WHAT THIS FLOAT DOES:** as LS-2 on page 5. It stops the whole plant and stays stopped until a person resets it.

**6-15. Land CDR-062.**
THIS END: LS-8, storage high-high `{terminal}`, on the standpipe
FAR END: The permissive string, **page 1**
CARRIES: The float's other leg
LABEL, BOTH ENDS: CDR-062
BLOCKED. Missing: the float part is not chosen, so it has no terminals to read. Owner: WATER returns the float; and S-01 is OPEN

---

# PAGE 7. FILL SOLENOID

**No enclosure. The entries are the valve's own.**

**With no power this valve springs CLOSED.** That was decided before the valve was
chosen, and it is why a dead panel does not leave a fill running.

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-29**, D1 section 25. FV-1 is installed in the fill line between its unions, with the line run from the building supply through it. **No step here fits the valve.**

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing at FV-1 is labelled at both ends, landed and ticked.**

**STEPS 7-01 TO 7-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**7-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**7-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**7-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**7-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**7-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**7-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**7-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## The valve's three conductors

**7-08. Land CDR-001.**
THIS END: FV-1, the coil lead `{marking}`
FAR END: K-FILL-S, the solenoid pole, **page 1**
CARRIES: Switched 120 VAC to the coil
LABEL, BOTH ENDS: CDR-001
BLOCKED. Missing: the valve's coil leads are not identified. **Nobody has looked at the valve, and terminal-survey.md does not list it** - see the closing section. Owner: anyone with the valve in hand; and P-02 is OPEN

**7-09. Land CDR-045.**
THIS END: FV-1, the coil lead `{marking}`
FAR END: The neutral, **page 1**
CARRIES: Coil return
LABEL, BOTH ENDS: CDR-045
BLOCKED. Missing: the valve's coil leads are not identified. **Nobody has looked at the valve, and terminal-survey.md does not list it** - see the closing section. Owner: anyone with the valve in hand; and P-02 is OPEN

**7-10. Land CDR-046.**
THIS END: FV-1, the grounding point `{marking}`
FAR END: The main panel ground bar, **page 1**
CARRIES: Equipment grounding for the valve
LABEL, BOTH ENDS: CDR-046
BLOCKED. Missing: the valve's coil leads are not identified. **Nobody has looked at the valve, and terminal-survey.md does not list it** - see the closing section. Owner: anyone with the valve in hand; and the ground bar is not bought

---

# PAGE 8. LEAK CONSOLE

**Remote, in no enclosure, fed through its own cord grip.**

**MUST BE TRUE BEFORE THIS PAGE STARTS:**
- **BB-06**, D1 section 4. Every device on the shelf has had its terminals read and terminal-survey.md is filled in. **This is what closes F-106, and F-106 blocks every joint step in this document.**
- **D1 step 31-01.** F-099 is closed, so no cable has been cut against two tables that disagree about the allowance.
- **D1 step 31-05.** Every jacket is cut, marked at both ends, routed on the wall and pulled through its cord grips. **A conductor spans the cord grip and is one row, so landing one end before its jacket is pulled means pulling a landed conductor.**
- **BB-34**, D1 section 30. WB200 is mounted at the position the owner set, with its own cord grip fitted, and **its sensor is placed on the floor clear of every overflow discharge point.** Where the sensor sits is decided in D1 and is not a choice made at this page.

**TRUE AFTER IT ENDS:**
- **Every conductor D5 lists as landing at WB200 is labelled at both ends, landed and ticked.**

**STEPS 8-01 TO 8-07 ARE A LOOP. RUN ALL SEVEN, IN ORDER, ONCE FOR EVERY JOINT
STEP BELOW.** They are printed in full on every page because you may be holding one
page and no others, and they are identical on all eight.

**8-01. Read the whole joint step before you touch the conductor.**
ACCEPT: you can say aloud where the far end of this conductor goes, and which page it
is on, without reading the step again.

**8-02. Write the conductor's label on one end.**
The label is printed in the joint step. Where the step also gives a channel token,
write both, unabbreviated and not run together.
ACCEPT: the end reads exactly what the joint step's label says, character for
character.

**8-03. Write the same label on the other end.**
ACCEPT: both ends read the same. **If the far end is already installed and you cannot
see it, do not tick this step** - it belongs to whoever runs the far end's page, and
the conductor is not landed until it is done there.
WHY: a conductor labelled at one end only is worse than one labelled at neither,
because it looks done. **Until the terminals are surveyed the label is the only thing
that tells one conductor from another.**

**8-04. Strip the end you are about to land.**
ACCEPT: every strand is intact, none is cut short, and no strand is nicked.

**8-05. Look at what is already under the terminal you are about to land on.**
ACCEPT: you can say how many conductors are already under that clamp.
WHY, AND IT IS THE HALF THAT GETS SKIPPED: **if the joint step does not say something
is already there and something is, STOP AND DO NOT LAND.** A clamp carrying more
conductors than it is meant to passes every check a landed joint gets and fails later.

**8-06. Land this end.**
ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**8-07. Tick the joint step on this page.**
ACCEPT: the box beside the step number is marked.
WHY THE TICK IS HERE: the page in your hand is the worksheet. **D5 is the record of
what the build is, not the record of what you have done.**

## The console's three conductors

**8-08. Land CDR-063.**
THIS END: WB200, the supply terminal `{marking}`
FAR END: The 24 V rail positive, **page 1**
CARRIES: Console supply, positive
LABEL, BOTH ENDS: CDR-063
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and **CBL-06 is an OPEN interface row**
WHY THIS CABLE IS HEAVIER THAN 24 V NEEDS: **the same jacket carries the console's contact legs, which sit in the 120 V chain**, so every conductor in it takes the higher insulation rating including this one.

**8-09. Land CDR-064.**
THIS END: WB200, the supply terminal `{marking}`
FAR END: The 24 V rail negative, **page 1**
CARRIES: Console supply, return
LABEL, BOTH ENDS: CDR-064
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and CBL-06 is OPEN
WHAT HAPPENS IF THE CONSOLE LOSES POWER: **its output opens, exactly as it does for a leak, and the permissive drops.** A dead leak detector cannot read as no leak.

**8-10. Land CDR-065.**
THIS END: WB200, the grounding point `{marking}`
FAR END: The main panel ground bar, **page 1**
CARRIES: Equipment grounding for the console
LABEL, BOTH ENDS: CDR-065
BLOCKED. Missing: the printed identifier on that terminal has not been read. **F-106, and D1 section 4 closes it** - terminal-survey.md is the form. Owner: anyone with the parts in hand and a pen; and the ground bar is not bought
**THIS STEP DID NOT EXIST BEFORE 2026-09-23.** D6 always required a grounding conductor in this jacket and D5 enumerated two where it needed three, **so this page had two steps where it needed three.** It was found by reading the three documents against each other and by no check inside any one of them.

---
# WHAT IS BLOCKED, AND WHAT CLEARS IT

**183 numbered steps: 56 loop steps, seven on each of eight pages, and 127 joints.
Every one of the 127 joints is blocked.**

**The counts below are per joint step and reproduce on a read of the pages.** The last
issue's table did not, and a builder who cannot reproduce a count has to check the
whole document to find out which number to trust.

| What is missing | Joints | Where | Who clears it |
|---|---|---|---|
| **The printed identifier on a terminal in the main panel or on the console** | **37** | page 1 except its bar group, page 8 | **D1 section 4**, terminal-survey.md. One evening with the parts and a pen |
| **The logic board does not exist** | **28** | page 2 | DISPLAY-BOX, and **BB-19** is where it gets built |
| **The printed identifier on a driver terminal** | **24** | pages 3 and 4 | **D1 section 4.** The 6121 is group 1 of the survey: read ONE and confirm the other seven match |
| **The four ground bars are not bought** | **19** | page 1's bar group, page 2's grounding group, and one pair in each pump box | MAIN-PANEL provides them; D7 buys them |
| **The float part is not chosen, so it has no terminals to read** | **16** | pages 5 and 6 | WATER, against S-01 and S-02 |
| **Nobody has looked at the valve's coil leads** | **3** | page 7 | Anyone with the valve. **And see the sequence check: D1 section 4 does NOT clear this one** |

**Open interface rows sit behind whole groups as well** - P-01, P-02, P-06, S-07,
S-10, S-20, S-01, S-02 and CBL-06 - and each joint names the one that blocks it.
**Nothing is built against an open row.**

## The one evening that clears the most

**Working D1 section 4 and filling terminal-survey.md clears 61 of the 127 joints**:
the 37 in the panel and at the console, and the 24 at the drivers. **It is not a
decision, a purchase or a design.**

**It does not clear all of them, and the last issue said it did.** The 28 display box
joints need a board that does not exist, the 19 bar joints need bars nobody has
bought, the 16 float joints need a float nobody has chosen, and **the 3 valve joints
need a device the survey does not list.**

**Until any of it clears, the labels are what carries the build.** That is why writing
the label is steps 02 and 03 on every page and landing is step 06: **a conductor
labelled at both ends can be identified without knowing the name of the terminal it
goes to.**

---

# THE SEQUENCE CHECK, RUN ON THIS DOCUMENT

**G-50. Every page states what must be true before it starts and what is true after it
ends, so that a section requiring X comes after the section producing X. This is the
result of running that comparison.**

**1. NO PAGE DEPENDS ON ANOTHER PAGE'S POSTCONDITION. The eight are independent and
may be worked in any order.**

Every precondition on every page resolves either into D1, as a BB- number, or into a
D1 step this document does not own. **Not one names another D4 page.** That is not an
accident of drafting: a conductor spanning two boxes is landed at one end on one page
and at the other end on the other, **and neither landing produces anything the other
needs.** D1 step 31-06 already says the pages may be worked in any order, **and this
check confirms it rather than assuming it.**

**2. FIVE DEPENDENCIES WERE LIVING IN BLOCKED NOTES AND ARE NOW PRECONDITIONS.**

F-116 is the reason this sweep was run at all: the same check passed a closed loop in
D1 because the dependency sat in prose rather than in a precondition, **and G-50 only
reads preconditions.** Swept here, five turned up:

| It was a blocked note saying | It is now a precondition naming |
|---|---|
| "nobody has looked at a terminal" | **BB-06**, D1 section 4 |
| "the ground bar is not bought" | **BB-17, BB-18, BB-19**, which fit the four bars |
| "the logic board does not exist yet" | **BB-19** |
| "the float part is not chosen" | **BB-25, BB-26, BB-27**, which are themselves blocked on it |
| nothing at all - the jackets were assumed pulled | **D1 step 31-05**, every jacket pulled through its cord grips before any end is landed |

**3. THE SWEEP FOUND ONE REAL DEFECT AND IT IS NOT MINE TO FIX. terminal-survey.md
does not list FV-1.**

Page 7's three joints are blocked on the valve's coil leads. **This document and D5
both nominate D1 section 4 as the thing that closes F-106**, and D1 section 4's own
text says it closes it. **The survey's three device groups list the drivers, the
relays and their sockets, the contactors, the supply, the two logic parts, the Pi
header, the EZO carriers, the USB-C bulkhead, the ground bar, the fuse holder, the
inrush limiters, the WaterBug and the four enclosures. The fill solenoid is not among
them.**

**So an evening spent on the survey would leave page 7 blocked and nothing would say
why.** Routed to whoever owns terminal-survey.md. **I have not added the valve to
someone else's form** and I have not quietly dropped the claim from this document's
blocked table, which now says so in its own row.

**4. ONE ORDERING DEFECT INSIDE PAGE 1, FIXED HERE.**

The previous issue landed CDR-044 with the supply group and CDR-046 with the valve
group, **thirty steps before the page's bar group admits the bar is not bought.** Both
land on the bar. **They are in the bar group now**, with CDR-065, and the page's claim
that the bar is last and all together is true.

---

# WHAT THIS ISSUE CHANGED, AND WHAT IT DELIBERATELY DID NOT

**Changed, all of it by regeneration from a corrected D5 and none of it typed onto a
page:** the channel-to-box division and the high-high float landings now come from D5
rows rather than from this document; the console's fail behaviour is D5's answer;
**CDR-065 exists and page 8 has three steps where it had two, and page 1 has nine bar
landings where it had eight.**

**Changed in the format:** the loop is stated as a loop and is identical on all eight
pages; the look and the land are two steps with two acceptance conditions rather than
one step with two verbs; every page carries preconditions and a postcondition; and no
step refers to another by its number.

**NOT changed, and each is somebody else's:**

- **K-DRY and K-DRY-Q.** This document uses both, on one page, exactly as D2, order.md
  and D5 do. **D6 records that the name is unstable until one wins.** Renaming a device
  across the tree is BOSS's under G-42 and a subsystem does not do it quietly, **so the
  pages carry the tree's own inconsistency rather than a local invention.**
- **Which physical terminal the permissive string offers.** The landing is settled,
  D-154 and D-179. **The string is a series path across sockets rather than one device,
  and which piece of metal a float leg lands on is MAIN-PANEL's.** The four joints say
  so instead of naming a marking that does not exist.
- **The pull-down resistors at the driver direction inputs.** The last issue said each
  driver **has** one. **D5 records them as an owed fix and not as a fitted part**, so
  this issue states it in the fail warning on every direction joint and claims nothing
  about what is in the box.
