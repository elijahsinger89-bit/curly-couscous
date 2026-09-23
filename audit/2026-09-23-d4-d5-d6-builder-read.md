# Builder read, end to end, of D4, D5 and D6

**2026-09-23. Read in order: wiring-instructions.md (D4), wiring-schedule.md (D5),
cable-and-terminal-schedule.md (D6). Read cumulatively, as a person at a bench holding
the parts, the wall and these three documents and nothing else.**

**Nothing was fixed and no file was edited.** Every hit below names its document, its
page or section, and its step or row id. Where a step is said to assume something
untold, the earlier step I expected to find it in is named.

**Read against agents.md's G-49 and KEEP IT SIMPLE, and against decisions.md's G-rule
table.**

---

## THE HEADLINE, BEFORE THE CATEGORIES

**The regeneration did NOT duplicate or drop a joint.** I checked by reading and then
confirmed mechanically: 125 joint steps across eight pages, no CDR- id appearing twice
on one page, every one of D5's sixty-four conductors appearing on exactly the pages its
two ends imply, and the three conductors whose far end is the building branch circuit
appearing once because that end is on no page. **D4's own count of 173 and 125 is
correct and reproducible.** This is the category the read was most warned about and it
is clean. Section 4 below says so in full rather than leaving silence to be read as a
finding.

**What the read DID find is concentrated in two places, and both are the shape the
generation was supposed to make impossible:**

**1. D4 STATES AS SETTLED FACT TWO THINGS D5 RECORDS AS OPEN**, and one of them is
printed as a page title. **The channel-to-box division, and the landing of the two
high-high floats.** These are not renderings of a D5 row. They are facts D4 acquired
somewhere between D5 and the page, and a builder has no way to know it.

**2. The six steps at the top of every page are a LOOP that no step says to repeat**,
and two of the six tell the builder to strip and to land while every joint on the page
is blocked from being landed. D4's own status calls all forty-eight of them "ready".

---

## 1. STEPS WITH TWO ACTIONS

**One shape, repeated on all eight pages, and it is the fifth step of every page.**

> **P1-05. Look at what is already under the terminal, then land this end.**
> If anything is already under that clamp, the joint step says so. If it does not, and
> something is there, stop and do not land.
> ACCEPT: the clamp holds against a firm pull and no bare conductor shows outside it.

**Two verbs, joined by "then", and only the second one has an acceptance condition.**
The look is the whole protection - it is what stops a second conductor going under a
clamp meant for one - and a builder who lands without looking produces a joint that
passes the printed ACCEPT exactly. G-49 clause 1: a step with two verbs can be half
done and look finished. This is that, and the half that gets skipped is the half the
step exists for.

**Same defect at P2-05, P3-05, P4-05, P5-05, P6-05, P7-05 and P8-05.** Split it and the
look gets its own accept condition.

**AND THE SEVEN COPIES ARE NOT THE SAME STEP**, which is a second finding on the same
line. D4's own introduction says **"Every page begins with the same six steps, printed
in full. They repeat because you may be holding one page and no others."** P1-05 carries
the stop rule - "If it does not, and something is there, stop and do not land" - and the
WHY beneath it. **P2-05 through P8-05 carry neither.** A builder holding only page 2 is
told to look and is never told what to do about what he sees. The promise that the six
are printed in full is not kept.

**The same divergence hits the label rule where it matters most.** P2-02 and P3-02 say
to write the channel token **"unabbreviated and not run together"**. **P4-02 says only
"write both."** Page 4 is the page whose builder writes CH5 through CH8, and it is the
one page that drops the rule channel-token.md exists to enforce and that D5 section 1.5
states as the reason the column exists.

**Outside the numbered steps, two page headers carry actions with no step number, no
acceptance condition and more than one verb each.** They are treated in section 2,
because their larger problem is what they assume.

---

## 2. STEPS THAT ASSUME SOMETHING THE BUILDER WAS NOT TOLD TO DO

**This is the largest category, and the cause is single: D4 is a book of LANDINGS with
no book of ASSEMBLY in front of it, and it never says so.**

### 2.1 Nothing has been built, mounted or brought into a box before P1-07

**P1-07 is the first joint on the first page** and it says **"Land CDR-042. Far end: the
building branch circuit."** To do it the builder needs: the panel mounted, a rail in it,
the line input device fitted, a cord grip in the bottom face, and the cable fed through
that grip.

**No step anywhere in D4 does any of those, and no page says another document does.**
I looked for the step that should precede P1-07 and there is none: page 1 opens with a
bonding warning and goes straight to P1-01, and P1-01 through P1-06 are read, write,
write, strip, land, tick. **The document's "WHAT IS NOT ON THESE PAGES" section names
three exclusions - panel-internal conductors, wall routes, and two reported items - and
mounting is not among them.**

This reaches every page. P3-07 lands on a driver supply terminal in pump box A and no
step fits a driver or a plate. P2-07 lands on a 5 V rail in the display box and no step
fits a rail or says where 5 V comes from. **Page 2's own header says the Pi supply "is
not on this page", so the one cable that could produce a 5 V rail is excluded by name
and nothing replaces it.**

### 2.2 The six opening steps are a loop and no step says to repeat them

**P1-01 to P1-06 are numbered as ordinary steps, done once, in order.** A builder
following the numbers does them once and then lands forty-two conductors without
labelling or stripping any of them.

**The loop is real and the document knows it.** P1-06 says **"Tick the joint step on
this page"** - a joint step, singular, chosen from the forty-two below. The blocked
table calls the forty-eight **"the joint sequences"**. **But no sentence on any page
says "run steps 01 to 06 for every joint step below."** The introduction explains how to
read a step and never says how many times to read these six.

**It is the cheapest fix in the document and it is not there.**

### 2.3 P1-04 and P1-05 are live work on a page where nothing may be landed

**Every one of the 125 joints is BLOCKED.** D4 says so twice and the reason is F-106:
nobody has looked at a terminal. **Yet P1-04 says "Strip the end you are about to land"
with a live acceptance condition, and P1-05 says to land it.** And the status section
says **"48 of them are the joint sequences, which are ready."**

**A stripped conductor cannot be un-stripped, which is G-49 clause 4's own example one
size down.** Reading, labelling and ticking are genuinely ready. **Stripping and landing
are not, and calling all six ready is the document telling a builder to begin.**

### 2.4 The EZO jumpers: an action in a header, on parts nothing installed

Page 2, above P2-01, unnumbered:

> **BEFORE YOU LAND ANYTHING IN THIS BOX:** each of the three EZO circuits ships set to
> UART and has to be moved to I2C with a jumper, and the jumper is not in the same place
> on all three.

**This is the only precondition anywhere in D4 and it is the one paragraph that is not a
step.** It has no number, so it cannot be ticked, cannot be marked done and cannot be
referred to. **It has no acceptance condition: nothing tells the builder how to know a
jumper is in the I2C position.** It says the position differs across the three and does
not say where any of them is, so the builder stops and asks - and the paragraph is not
marked blocked.

**And it assumes the three EZO circuits and their carriers are already mounted in the
box.** No step in D4 fits them. I expected to find that step before P2-01 and there is
none; D6 section 3.3 confirms the far end of RUN-016 is "the EZO circuits and their
carriers" and D5 section 5 confirms the probe leads are supplied and land no conductor,
so **no page in D4 will ever mention these parts again.** The builder is told to modify
three boards he was never told to fit, in a box whose page otherwise never names them.

### 2.5 Page 2's header names probes that appear in no step

The same header lists the bottom-face order as **"probes alone at one end, then the two
driver cables..."**. **No step on page 2 lands a probe conductor.** D5 section 5 gives
the reason - a supplied assembly lands nothing - but **that reason is in D5 and the
builder holds page 2.** A person counting entries against steps finds one entry with no
work and no explanation of why.

### 2.6 P1-33 lands into an arrangement no step creates

> **P1-33. Land CDR-033.** ... WHY THIS ONE HAS TWO BRANCHES AND THE OTHERS DO NOT: this
> contact needs 45 to 55 mA to stay clean, which is more than the diode alone should
> carry continuously, so the loading resistor is a second branch and it is a part rather
> than an option.

**The second branch is a part. No step fits it.** The section header above P1-33 states
it as already true: "the loading resistor IN THIS PANEL". **D4's own exclusions section
says the burden branches "are rows in D5 that MAIN-PANEL fills, and they will appear on
page 1 when they exist."** So the step lands a conductor into a two-branch arrangement
whose second branch is not built, not scheduled and not mentioned as absent at the step.
I expected the fitting step between P1-32 and P1-33.

**This is section 5's shape as well - a step landing on something a later step installs -
except that here there is no later step.**

### 2.7 The floats: a terminal that may not exist

Page 5 header: **"THE FLOAT CORD IS NOT A CABLE YOU CUT. Its weight clamps onto it, the
tie is the trip height."** D6 marks RUN-012 and RUN-013 **provision "Supplied"** and
their A face **"n/a, a float has no faces."**

**Then P5-07 says "Land CDR-047 ... LS-1, day tank fill start, one terminal."** D5's row
says **"LS-1 {day tank fill start}, both switch terminals"**.

**So D5 and D4 have the builder landing two conductors on a float's terminals, and D4's
own header and D6's provision column describe an integral cord that is not cut.** One of
these is wrong and the builder cannot tell which with the parts in his hand. **He stops
and asks, and no step is marked blocked for it** - P5-07's blocker is the float part not
being chosen, which is a different question.

### 2.8 Page 5 and page 6 order work on a tank that no step prepares

> **BEFORE ANYTHING GOES IN THE TANK: mark every trip height on the pipe.**

**Unnumbered, no acceptance condition, and the trip heights are stated nowhere in any of
the three documents.** The float part is not chosen, which is P5-07's blocker, so the
heights cannot be known. **The builder stops. Nothing marks it blocked.**

It also assumes: a standpipe exists, it is fitted, the floats are clamped to their cords
at a height, and the cords are tied. **No step in D4 does any of that.** I expected them
before P5-07 and there are none. D6 section 4 treats the standpipe as a built thing
throughout and D-121 is cited as owning the method, but **the method is in the tree and
not on the page, and the page is what the builder holds.**

### 2.9 The pull-down resistor on page 3, asserted as fitted

> **One thing in this box that is not a conductor and is not on this page:** each driver
> **has** a pull-down resistor on its direction input.

**D5's CDR-015 row does not say the pull-down exists. It says the opposite:** "The fix
is a pull-down AT THE DRIVER END, PUMP-BOXES', D-043", listed under BLOCKED. **D4 states
in the present tense a part D5 records as an outstanding remedy**, and then tells the
builder it is checked at commissioning - which is a check three sections away for a part
nobody has fitted. Page 4 repeats it: "Same pull-down note as box A applies here, on all
four drivers."

---

## 3. ACCEPTANCE CONDITIONS, BOTH DIRECTIONS

### 3.1 The inverse check, run first because it was the one that miscounted before

**I checked every step in D4 for a BLOCKED marker carrying a live ACCEPT alongside it.
There is not one.** Every step in the document is either blocked with no acceptance
condition, or unblocked with one. **No step is both.** The seven that existed in the
build book's first issue have no counterpart here.

**Every blocked step also names what is missing and who owns it.** I checked all 125,
following the "as P1-07" chains, and every one resolves to a named missing thing and a
named owner.

**That is a genuine clean result on the sharpest of the four checks and I am reporting
it as one.**

### 3.2 But the blocked steps name the wrong missing thing in two places

**A blocked step is exempt from carrying an acceptance condition because it names what
is missing instead. That makes the named blocker load-bearing, and twice it is wrong.**

**P1-29 and P1-31, and their partners P1-30 and P1-32:**

> **P1-29. Land CDR-053.** Far end: LS-2, day tank high-high, page 5. Sits in series in
> the permissive string.
> BLOCKED. Missing: the terminal marking on the permissive string, and S-02.

**The missing thing is not the marking.** D5's row for CDR-053 and CDR-054 has the **To
column itself OPEN**, blocked on **"whether the high-high floats sit in the permissive
string, and their landing, is open - D2's ?13 and ?14, MAIN-PANEL and WATER jointly."**
Same for CDR-061 and CDR-062 at P1-31.

**So D4 tells the builder the destination is known and only its marking is missing, when
D5 says the destination is not decided.** Even if every terminal in the build were read
tomorrow, these four steps would still be blocked, and the blocked table's promise that
one afternoon with a pen "clears the condition that stops all 125" is not true of them.
P5-13 and P6-13 repeat the same assertion at the float end.

**P7-09 against P1-12, on one conductor:**

P7-09 says CDR-046's far end is **"the ground bar, page 1"**. On page 1 the same
conductor is P1-12, filed under **Fill solenoid**, worded **"Carries equipment grounding
for the valve"**, blocked on **"the terminal marking, and P-02"**. **It never says ground
bar, and it is not in page 1's ground bar group.** D5's row is unambiguous: CDR-046 goes
to MAIN-PANEL {ground bar}, and the ground bar is **not bought**, which is what P1-43
says blocks every other bar landing. **P1-12 names a blocker that is not the real one and
omits the one that is.** CDR-044 at P1-09 has the same problem: it lands at the single
point by D5's row and is blocked on P-01 and a marking, with no mention of the bar.

### 3.3 Acceptance conditions that are not observable at that moment

**P1-03 and its copies on all eight pages: "ACCEPT: both ends read the same."**

On pages 5 and 6 the two ends of a float conductor are the tank and the main panel.
**A builder at the standpipe cannot see the panel end.** The condition is right for a
conductor labelled on the bench before it is run and unobservable for one already
installed, and nothing on the page says which case he is in.

**P1-01 and its copies: "ACCEPT: you can say where the far end of this conductor goes
without reading it again."**

**This is the one acceptance condition in the document that nothing outside the
builder's head can witness**, and a builder who has it wrong satisfies it exactly as
well as one who has it right. It is a useful instruction and it is not a check.

---

## 4. DUPLICATED OR DROPPED STEPS FROM THE REGENERATION

**Nothing. Read for it, then confirmed mechanically, and the read agrees with the
count.**

- **No CDR- id appears twice on one page.** Page 1 carries 42 distinct ids, page 2
  carries 34, pages 3 and 4 carry 14 each, pages 5 and 6 carry 8 each, page 7 carries 3,
  page 8 carries 2.
- **All sixty-four of D5's conductors appear in D4, and D4 introduces none that D5 does
  not have.** The two sets match exactly.
- **Every spanning conductor appears on exactly two pages**, and the only three that
  appear once are CDR-042, CDR-043 and CDR-044, whose far end is the building branch
  circuit, which is not an enclosure and has no page. That is correct.
- **125 joints plus 48 sequence steps is 173**, which is what both the blocked table and
  the status section say.

**The parallel build's three-steps-across-two-sections defect has no instance here.**

**What the regeneration DID lose is in section 6, and it is not a step. It is a fact.**

### 4.1 One dropped CONDUCTOR, and it is D5's loss rather than D4's

**D6 section 2.4 states which jackets carry a grounding conductor, and RUN-015, the leak
console jacket, is on the yes list** - "RUN-010, RUN-011, RUN-015, the LINE field
jackets: Yes. A LINE circuit's equipment ground goes home in its own jacket."

**D5's RUN-015 group has two rows, CDR-063 and CDR-064, and neither is a grounding
conductor.** RUN-010 has CDR-044 and RUN-011 has CDR-046; **RUN-015 has nothing.**

**So page 8 of D4 has two steps where it should have three, and page 1 is missing the
matching bar landing.** D4 could not have produced the step, because the row does not
exist for it to render. **It is a dropped conductor, one document upstream of where the
read was told to look for dropped steps.**

---

## 5. SEQUENCE PROBLEMS A PERSON WOULD HIT

### 5.1 No page states what must be true before it starts

**G-50 was frozen 2026-09-05, the same day D4 was regenerated**, and requires every
section of a sequenced document to state what must be true before it starts and what is
true after it ends.

**No page in D4 carries either.** There is no precondition line and no postcondition
line on any of the eight. **The single exception is page 2's EZO paragraph**, which is
the one place a writer confronted what a section assumes - and, exactly as G-50 predicts,
it is also the one place where a real assembly dependency surfaced.

**The consequence is not abstract.** There is no statement of which page is done first,
no statement that page 1 must exist before the pages that land into it, and **no page
ends by naming what must come first.** Page 1's supply steps and page 7's valve steps and
page 5's tank steps are presented as eight independent packets, and they are not.

### 5.2 Page 1 states an order and then breaks it

The section heading reads **"The ground bar. Last, and all together"**, and the page
opens with **"Every green conductor in this build ends at that bar and nowhere else."**

**Two green conductors are landed on that bar earlier in the page and not in that group:
CDR-044 at P1-09 and CDR-046 at P1-12.** A builder who works the page in order lands two
conductors on the bar, reaches P1-43, and is told the bar is not bought.

**And that is the deeper problem: P1-43 says the bar is not bought.** P1-09 and P1-12
land on it thirty steps earlier without saying so. **The page sends the builder at a part
that does not exist and only admits it later.**

### 5.3 A builder is sent away mid-page and the page continues

**Every joint step on pages 1, 5, 6, 7 and 8 names its far end as another page.** P1-10
says "the fill solenoid coil, page 7". P5-07 says "the K-FILL-D coil chain, page 1".
**Neither says whether to go there, when, or with what.** The introduction says "Take the
page for the box in front of you and nothing else", which is the right instruction, but
the pages then continue as though the builder has both ends in reach - which is what
P1-03's accept condition requires.

### 5.4 Page 5 and page 6 contradict their own opening line

**Page 5 opens "There is no box here and no face to choose."** Two lines later: "the
cords run UP the pipe, tied at intervals, and leave through a grip with the **drip loop
OUTSIDE the box**." **Page 6 repeats it.** Whatever box is meant, the page has just said
there isn't one, and the builder has no way to resolve it.

### 5.5 The terminal that two cables leave, and the one that may be three

**P1-05's WHY says "this panel has one terminal that two cables genuinely leave"**, and
P1-13 and P1-14 are that terminal, correctly flagged in advance with "BEFORE YOU CLOSE
THAT CLAMP".

**But P1-15 and P1-16 both land on "the 24 V rail negative", and neither warns the
other.** So do P1-34, P1-40 and P8-08's partner P1-42. **P1-05's stop rule says: if the
joint step does not say something is already there and something is, stop and do not
land.** A rail is probably many terminals and probably fine - **and the page never says
so, so the builder stops at P1-16 and asks.** The one place the document promises to warn
him is the one place he cannot tell whether the promise applies.

---

## 6. DISAGREEMENTS BETWEEN THE THREE

**D4 must state no fact of its own. These are the places it does, and the places D5 and
D6 disagree with each other.**

### 6.1 THE CHANNEL-TO-BOX DIVISION. D4 states it; D5 says PUMP-BOXES has not returned it

**This is the most consequential finding in the read.**

**D5 is explicit, twice.** The per-channel group header: **"Their JACKET does not
[exist], because PUMP-BOXES has not returned which tokens sit in which box - so column 2
is OPEN on every one and is the only place in this document where it is."** Every one of
the sixteen rows carries **"BLOCKED: S-10, and the box division."** D5's own priority
list puts **"PUMP-BOXES' box division"** second of the four things that would move the
most. **D6 agrees:** RUN-004 is blocked on "PUMP-BOXES' open division of the eight
channels."

**D4 states the division as settled, in four places, and one of them is a page title:**

> **Channels CH1 to CH4 go to pump box A. Channels CH5 to CH8 go to pump box B.**
> Straight split, in order, nothing interleaved, so you can tell which channels are in a
> box by looking at the box rather than at a table.

> **PAGE 3. PUMP BOX A. This box holds channels CH1, CH2, CH3 and CH4.**

> **PAGE 4. PUMP BOX B. This box holds channels CH5, CH6, CH7 and CH8.**

**And every one of the sixteen step-and-direction steps on page 2 names a box:** P2-11
"the CH1 driver, **box A**", P2-19 "CH5 step, **box B**". **D5's To column for those rows
names no box at all - it says `{the driver assigned CH1}`.**

**The box is where D4 got it from, and D4 is a view.** A view cannot know which box a
channel is in when its source says nobody has said. **Sixteen steps, two page titles and
one stated rule rest on it, and the builder is told he can tell which channels are in a
box by looking at the box.**

### 6.2 THE HIGH-HIGH FLOAT LANDINGS. D4 states them; D5 has the cell OPEN

Covered at 3.2 as a blocker defect; it is also a drift and belongs here.

**D5, CDR-053/054 and CDR-061/062: the To column is OPEN.** D4 asserts **"the permissive
string"** at P1-29, P1-31, P5-13 and P6-13, and files the two page-1 pairs under a
section heading called **"High-high floats"** with a full paragraph explaining the latch.

**And D6 disagrees with itself on the same two floats.** RUN-013's End B reads
**"MAIN-PANEL: K-FILL-S and permissive coil chains"** - asserting the permissive landing
D5 holds open. **RUN-012's End B reads "MAIN-PANEL: K-FILL-D and K-DRY coil chains"** -
naming no permissive landing at all, although LS-2 is a day tank float and is in
RUN-012. **So one of D6's two float jackets asserts the open answer and the other omits
it.**

### 6.3 D6's RUN-013 End B omits the one landing everybody flags as surprising

**LS-3 is the storage tank float that lands in the DAY TANK fill chain.** D5 says so
plainly. D4 says so twice and in capitals - P1-25's "READ THE FAR END TWICE" and P6-11's
"READ THAT FAR END TWICE ... It is the one float whose chain is not the one its tank
suggests."

**D6's RUN-013 End B names "K-FILL-S and permissive coil chains" and does not name
K-FILL-D.** The jacket carries LS-3's two conductors and its End B cell leaves out where
they go. **The same cell is wrong in both directions: it asserts a landing D5 holds open
and omits one D5 has filled.**

### 6.4 D5 and D6 describe D4 as a different document

**D5 says so twice:**

> **D4 is a generated VIEW of this list, one page per conductor - never a
> transcription**

> **D4 will therefore have no page for these six** ... A page per conductor over a cable
> nobody terminates would be a page describing nothing.

**D4 is one page per enclosure and says so in its first line.** D4's own exclusions
section reports that document-plan.md carries the same stale description and calls it
"stale rather than wrong" - **but it does not report that D5, its own source, carries it
too, in the section that tells the reader what D4 is.** Under G-37 a stale description in
two files is not two sources; it is one claim wearing two hats, and D5 is the one that
matters because D4 is generated from it.

### 6.5 KM-DRV pole 1: D4 says land on the pole; D5 and D6 say downstream of it

**P1-13: "Land CDR-002. ... Missing: the terminal marking on KM-DRV pole 1"**, and P1-14
puts CDR-005 on the same terminal.

**D5's note is different:** "parts.md: one pole for motor-supply distribution, **both
feeds off one terminal downstream of it.** T-010 is live at that landing and is D6's
check, not this document's."

**D5 distinguishes the pole from the terminal downstream of it. D4 collapses them into
"KM-DRV pole 1", and so does D6's TRM row.** The two-cables warning is right either way;
**which piece of metal the two cables land on is not the same question and D4 answers it
with a name D5 does not use.**

### 6.6 D5 and D6 disagree on which jackets have no conductors

**D5 section 5: "Six of D6's nineteen jackets contribute no CDR- row"** - RUN-009,
RUN-014, RUN-016, RUN-018, RUN-019 and RUN-020.

**D6 section 2.2: "RUN-009, RUN-018, RUN-019 and RUN-020 have no CDR- children ... D5
will never name these four ids."** **Four against six.** D6 leaves RUN-014 and RUN-016
off its list and D5 puts them on.

**And the rule underneath does not hold either way.** D5's section 1.6 says "A supplied
assembly has no conductors in this list." **D6 marks RUN-012 and RUN-013 provision
"Supplied", and D5 enumerates sixteen conductors in them.** So "supplied" does not
predict the absence of rows, and the two documents have no shared test for which jackets
have children.

### 6.7 D6's terminal schedule has no landing point for most of D4's blocked steps

**D6 section 3.3 lists fifteen TRM- landing points and says so.** They are the contactor,
four relays, four ground bars, the solenoid, the console, two driver groups and the logic
board.

**D4's blocked steps name, as the missing marking:** the 24 V rail negative (P1-15,
P1-34, P1-40), the 24 V rail positive (P1-41), the neutral (P7-08), the line input
(P1-07), the permissive string (P1-29, P1-31), the K-FILL-S, K-FILL-D and K-DRY coil
chains (P1-17, P1-21, P1-27), the display box 5 V rail and 5 V return (P2-07, P2-08).
**Not one of those has a TRM- row.**

**D5 section 7 excludes panel-internal CONDUCTORS from this issue, which is a different
thing from excluding LANDING POINTS for conductors that do cross.** D6 states no such
exclusion and presents its fifteen as the set. **So D4's steps are blocked on markings
for landing points that the terminal schedule does not carry**, and the afternoon with a
pen that D4 and D5 both nominate as the unblocker has no row to write half of them into.

### 6.8 D4 gives a reason for the two-branch sense circuit that D5 does not

**P1-33: "this contact needs 45 to 55 mA to stay clean, which is more than the diode
alone should carry continuously, so the loading resistor is a second branch".**

**D5's CDR-033 row gives the figure and a different reason: "The burden is a second
branch IN THE PANEL, so the contact stays wetted when this cable is unplugged."** D4's
own section header above P1-33 carries D5's reason correctly. **The clause about what the
diode can carry continuously is in neither D5 nor D6.** It is a fact about a part, in the
document that is supposed to hold none, and under G-15 it is the kind of figure no agent
states.

### 6.9 K-DRY and K-DRY-Q, a name D6 flags as unstable and D4 uses both ways

**D6's TRM row says it plainly:** "The relay is called K-DRY in the interface table and
K-DRY-Q in order.md, **so the id is unstable until one name wins.**"

**D4 uses both names on one page with no note.** P1-27 lands into "the K-DRY coil chain";
P1-37 lands from "the K-DRY-Q changeover pole". D5 does the same. **If they are one
device, G-42 is broken in the document a builder holds; if they are two, nothing on the
page says which is which.** D6 knows the question is open and D4 carries none of it.

---

## ALSO REPORTED, BRIEFLY

### Facts stated in a document that another document owns

- **D4, page 1 header: "Nothing but the five 22 mm devices goes in the top."** A count of
  devices. D6 section 1.1 attributes it to parts.md. **D4 states it without the
  attribution D6 carries.**
- **D4, page 5 closing note: "six of the eight in this build close on LOW water and two
  close on HIGH."** A per-part property of a part D4's own P5-07 says is not chosen.
  Stated in neither D5 nor D6. **This is WATER's and D2's.**
- **D4, page 5 header: "Two pump cords share this pipe and they are 120 VAC."** A count
  and a class, both D6's. D6 section 4 ties RUN-012, RUN-013, RUN-019 and **part of**
  RUN-020 to one pipe and puts RUN-019 on the day tank standpipe; **it never says two,
  and it never assigns a pump cord to the storage standpipe that page 6's "same rules"
  implies.**
- **D4, page 2 header: the Pi supply "crosses at a panel-mount USB-C bulkhead."** D6's
  section 5 lists that bulkhead as a requirement and a search term - **a lookup the owner
  has not run.** D4 states the entry hardware as chosen.
- **D4, page 3 and page 4: "each driver has a pull-down resistor on its direction
  input."** D5 records it as an owed fix. Covered at 2.9.
- **D4's blocked table, three rows whose counts a builder cannot reproduce.** "The ground
  bars are not bought - 12": I count **sixteen** steps blocked on a bar not being bought
  (P1-43 to P1-48, P2-35 to P2-40, P3-19, P3-20, P4-19, P4-20), before counting P1-09,
  P1-12 and P7-09, which land on a bar and cite other blockers. **"The logic board does
  not exist yet - 34": I count twenty-four** (P2-11 to P2-34); thirty-four is page 2's
  total joint count, including four 5 V rail steps and six bar steps that are blocked on
  other things. **"The valve's coil leads are not identified - 3": two** (P7-07, P7-08);
  P7-09 is blocked on the valve's grounding point, which the step itself says is a
  different thing. **The count check that passed did not read this table.**

### Steps where a builder stops and asks, and nothing is marked blocked

1. **Page 2, the EZO paragraph.** Which jumper, in which position, on which of the three.
2. **Page 5 and page 6, "mark every trip height on the pipe."** No heights anywhere, and
   the float is not chosen.
3. **P5-07 through P5-14 and P6-07 through P6-14.** Is there a terminal at the float, or
   is the cord integral and uncuttable. The page says both.
4. **Page 5 and page 6, "the drip loop OUTSIDE the box"** on pages that open by saying
   there is no box.
5. **P1-16, P1-34, P1-40, P1-42.** Something is already on the 24 V rail negative and the
   step does not say so, which P1-05 defines as a stop.
6. **P1-01 through P1-06, on every page.** Do these repeat for each joint.
7. **P1-07.** How does the cable get into the panel, and what is it landing on.
8. **P1-12 against P7-09.** Is CDR-046's panel end the ground bar, and does it belong in
   the group the page calls "Last, and all together".
9. **Page 8's opening.** Where the sensor may sit is called "a real question and not a
   convenience" and then left to the builder; D6 says F-104 governs it and D6 is not in
   his hand.

---

## WHAT IS GOOD, SAID PLAINLY

**These are not padding. They are the checks that came back clean and they are worth as
much as the hits.**

- **The regeneration is faithful at the level it was most at risk.** No duplicated joint,
  no dropped joint, exact correspondence with D5's sixty-four rows, and a step count that
  reproduces on a read.
- **No blocked step carries a live acceptance condition.** The defect that was miscounted
  as ready in the build book's first issue has zero instances here.
- **Every blocked step names what is missing and who owns it**, all 125, chains resolved.
- **The joint steps themselves are single-verb throughout.** Every one is "Land CDR-nnn".
  The two-action defect is confined to the shared sequence step and to two headers.
- **The labelling scheme is the document's strongest idea and it is carried through.**
  Label at both ends, before landing, as steps 2 and 3 of every page, with the reason
  attached - and D5's column 13 backs each one. It is what makes the build survivable
  while F-106 is open, and both documents know it.
- **The WHY notes are used the way G-49 clause 6 asks.** They appear where a builder
  would reasonably do it differently - the LS-3 far end, the high-high latch, the coil
  return direction, the shared common, the DIN-rail grounding block - and not on steps
  that are just work.
- **Page 3 and page 4 agree with D6 on entry order, on hand and on the no-mirroring
  rule**, and D6's RUN-002 note and D4's page 4 header say the same thing in different
  words without contradicting.
- **Page 2's bottom-face order matches D6's entry 1 through 8 exactly**, probes at one
  end and the Pi supply at the other.
- **D6 section 2.3 and section 2.4 are models of what G-47 asked for**: a cost claimed
  for someone else's box, found to be invisible rather than free, and recorded against the
  document that made the claim.

---

## THE ONE THING, IF ONLY ONE IS ACTED ON

**Section 6.1.** Sixteen steps, two page titles and a stated rule say which channels are
in which box. **D5 says nobody has answered that, and D5 is where D4 comes from.** Every
other finding here costs a builder a question. **That one costs him a box.**
