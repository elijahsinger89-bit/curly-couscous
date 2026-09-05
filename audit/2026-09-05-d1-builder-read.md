# D1 build book, end-to-end builder read

**Date** 2026-09-05
**Read** agents.md in full (G-49 and KEEP IT SIMPLE), decisions.md's G-rule table only
(52 rows, G-01 to G-50 and G-40b), then build-book.md start to finish, in order, 2326
lines, 33 build sections plus the check section and the status section.
**Posture held** I know how to use tools and nothing about this machine. At every step
only what came before it is known.
**Not re-run** the sequence check in section 34. Nothing below re-derives it. Where a
finding touches the same ground, it is because the check's own section 34.5 says a
section that names the wrong precondition passes it.

**The book is good.** It is written to G-49 far more consistently than not, the WHY
notes are the best thing in it, and several of the items below are found only because
the book set a standard high enough to be measured against. What follows is what a
formal check cannot see.

---

## 1. STEPS THAT CONTAIN TWO ACTIONS

G-49 clause 1. A step with two verbs can be half done and look finished. The book
splits mark from cut correctly in sections 7, 8 and 9, which is what makes the
exceptions visible.

| Step | Quoted | The two actions |
|---|---|---|
| **2-03** | "Lay out the parts D7 lists for the mechanical build and check each one against its line." | lay out; check |
| **5-01** | "Measure the wall and write the figures down." | measure; record. 5-03, 5-04 and 5-05 are each written as a single "Record", so this one is out of pattern with its own section |
| **7-06** | "Mark and cut the receptacle openings in the face D3 states." | mark; cut. 7-02/7-03 and 7-04/7-05 split exactly this pair into two steps each |
| **8-01** | "Take the lid off each box and set both lids aside." | remove; set aside - and a third, unwritten action, see 2.1 below |
| **9-01** | "Open the box and take out the back plate." | open; remove |
| **9-07** | "Fit a cord grip to each bottom-face entry and the bulkhead to its opening." | fit grips; fit bulkhead. Two different parts in two different openings. 7-09 and 8-08 are the same step without the second half |
| **10-01** | "Transfer each mounting position from the layout onto the wall and mark it." | transfer; mark |
| **13-10** | "Lift the populated plate into the mounted enclosure and fix it." | lift; fix. Half done is a plate resting in an enclosure unfixed, which looks finished |
| **15-06** | "Set each of the three EZO circuits from UART to I2C, and record which pin and which procedure was used for each one, per C-14." | set; record - and its own WHY says the record is the half nobody can repeat without |
| **15-07** | "Lift the populated back plate into the mounted box and fix it." | as 13-10 |
| **18-03** | "Stand each pipe in its tank and hang it on its U-bolt." | stand; hang |
| **19-01** | "Decide the working volume and the fill band, both ends, with the reason for each." | two decisions and two reasons in one step |
| **20-07** | "Fit the bulkhead and seal it." | fit; seal. On the most irreversible object in the build, and 20-05/20-06 immediately above are split |
| **23-02**, **23-03** | "Lower the day tank pipe into its tank and hang it on its U-bolt." | lower; hang |
| **25-03** | "Bring the line over the storage tank rim and turn its outlet downward into open air." | route; orient |
| **31-03** | "Take D6 and cut each jacket." | take up the document; cut. And "each jacket" is every cable cut in the build in one step, on the one operation the book itself says cannot be undone |

**31-03 is the one to fix first.** T-020 and the book's own 1.2 are about cut cable,
and this is the step that cuts all of it, under one number, with one tick.

---

## 2. STEPS THAT ASSUME SOMETHING THE BUILDER WAS NOT TOLD TO DO

Each names the earlier step I expected to find it in.

### 2.1 The lids are never marked, but two later steps depend on the mark

**8-01** ACCEPT reads "two open box bodies and two lids, each lid marked with the box
it came off." No step tells the builder to mark a lid. **14-01** ACCEPT then reads
"two lids, each still marked with the box it came off in 8-01", and **14-09** ACCEPT
"each marked with its box". I expected a step between 8-01 and 8-02 saying to write
the box's name on its lid. The instruction exists only inside an acceptance
condition, which is the one place a builder reads after the work rather than before
it.

### 2.2 Three of the four ground bars are never installed

**13-08** fits the main panel's bar and BB-17 records it. **31-08** is "Land the
ground bars last, per D4", and its own note says "Each remote enclosure has its own
local bar". **32-01** then asks the builder to confirm every green conductor "ends at
a bar", and BB-36 is "no bond exists outside a bar".

No step fits a bar in pump box A, pump box B or the display box. I expected one in
section 14 alongside 14-08 (which exists for exactly this reason: "a conductor cannot
be landed on a part a later step installs") and one in section 15 alongside 15-05.
**This is the book's own defect shape 2, inside the book, on the one class of
conductor the book says has nowhere else to go.**

### 2.3 The tanks' cord grips are never cut or fitted

**22-15** is "Take each tank's float cords out through that tank's cord grip", and
BB-26 and section 31's precondition list both depend on it. Section 20 is the only
section that penetrates a tank wall and it cuts one hole per tank, for the overflow
bulkhead. Sections 7, 8 and 9 fit cord grips to the four enclosures only. I expected
a grip hole beside 20-05 and a grip fitted beside 20-07, cut while the tank is empty
and the standpipe is out, which is the whole argument of 18-06 and 20-01.

The same gap is smaller at **30**: WB200 is "fed through its own cord grip" and no
step fits that one either.

### 2.4 The chiller is never placed, and BB-08 does not produce its position

**27-07** is BLOCKED "Missing: BB-08 for where the chiller stands". BB-08 produces a
mounting position for the main panel, both pump boxes, the display box, the manifold
and every jug station, a floor position for each tank, and a standing position for a
jug change. **The chiller is not in it**, and 6-01 covers "every wall-mounted item"
only. No step anywhere sets the chiller in place, the way 16-01 stands a tank and
26-01 places the transfer pump. When section 6 lands, 27-07 is still blocked and
nobody named in it owns the gap. Section 27's postcondition BB-31 nevertheless
asserts the loop is plumbed.

### 2.5 The bench does not carry the documents the book sends the builder to

**2-01** puts seven documents on the bench, D2 to D7 and this book, and its ACCEPT
counts them. Later steps then work from **terminal-survey.md** (4-01, 4-03, whose
ACCEPT is "it is on the bench with D2 to D7"), **parts.md** (2-05, 7-02, 25-02),
**subsystems/entry-faces.md** (6-06, 8-02, 9-02, 10-03), **subsystems/water-float-
requirement.md** (6-07, 19, 22-09), **channel-token.md** (1.4) and **C-14 in D8**
(15-06). I expected these in 2-01. A builder who packed to 2-01's accept condition
reaches 4-01 with nothing to open.

### 2.6 Consumables that steps use and no step or line produces

The book flags a paint pen (21-11), a U-bolt (18-01), a cradle (27-01), a bracket
(25-04), a support (16-01) and a heatsink (14-07) as D7 lines with requirements and
search terms. It does not do the same for:

- **solvent cement** - used at 11-04, 17-04, and relied on by name at 11-07, 17-05,
  27-10 and 31-02 ("the time its cement's label states"). Expected at 11-01, which
  says "before any cement is opened" and is the first place it appears.
- **the cable ties** at 22-01 to 22-08 ("Clamp LS-1's external weight on its mark ...
  with a cable tie") and the tie material at 22-11, 22-13 and 27-06. Expected at
  22-01, in the same form as 21-11's paint pen, and it is the same duty: permanent
  immersion in fertiliser solution.
- **the marker** at 3-02, on every device in the build.

### 2.7 Smaller ones, same shape

- **31-05** says "Pull every jacket through its glands". Sections 7, 8 and 9 fit
  **cord grips**. The book uses gland and cord grip for the same thing (7-09, 8-08,
  9-07 against 6-BLOCKED, 13-11, 31-03, 31-05) and G-42 is one device, one name,
  everywhere. A builder looking for glands he has fitted has fitted none.
- **22-01** names "LS-1's external weight" as a thing the float has. Nothing before
  it says the float has an external weight; the float part is not chosen. The step is
  blocked, so this is minor, but the weight is also the pivot the whole trip height
  depends on.

---

## 3. ACCEPTANCE CONDITIONS THAT ARE MISSING OR NOT OBSERVABLE AT THAT MOMENT

### 3.1 The book's very first working step cannot be accepted, and is not blocked

**2-01** ACCEPT: "seven documents, each with its own name at the top of its first
page." **D3 does not exist** - stated at 6-BLOCKED, 7-02, 7-06, 13-02, 14-02, 15-02.
So the accept condition of step 2-01 is unsatisfiable, the step carries no BLOCKED
line, and 4-03's accept ("on the bench with D2 to D7") repeats it. Compare 7-02,
which blocks on the same fact and says who owns it.

### 3.2 Seven steps carry live accept conditions for work their inputs cannot have produced

The book elsewhere uses a clean pattern - "BLOCKED. Missing: nothing to check until X
is done" (10-06, 12-02, 13-10, 15-07, 16-03, 18-04, 20-06, 21-10). These seven do not
use it, and every cutting step feeding them is blocked:

| Step | Its accept | Every input blocked |
|---|---|---|
| 7-07 | "run a finger round each edge" | 7-02 to 7-06 |
| 7-08 | "hold it to the light ... find nothing" | as above |
| 8-06 | "run a finger round each edge" | 8-02 to 8-05 |
| 8-07 | "hold each to the light" | as above |
| 9-05 | "run a finger round each edge" | 9-02 to 9-04 |
| 9-06 | "hold both to the light" | as above |
| 13-05 | "hold the plate to the light and find nothing" | 13-02 to 13-04 |

Each of these passes today by doing nothing, and each is counted in section 35's "52
are ready to work today". A builder ticks seven boxes and has deburred nothing.

### 3.3 A cure is asserted at 31-02 with no record that any step creates

**31-02** ACCEPT: "every solvent joint made in sections 11, 17, 24, 25, 26, 27 and 28
has had the time its cement's label states." 11-07, 17-05 and 27-10 say to leave the
work undisturbed until the label time has elapsed. **No step records when a joint was
made.** Section 18 shows the book knows how to do this - 18-05 exists solely to write
a number down with its units and its two faces. At 31-02 the builder is asked to
confirm elapsed time against nothing. It is also the only unblocked step in section
31.

### 3.4 Partial accepts a builder has to adjudicate

- **11-04** "ACCEPT for the joints that are not blocked". Which joints are the
  injection port joints is DOSING's open item, so the builder decides which of his
  own joints the accept applies to.
- **5-06** ACCEPT: "the record has left your hands and section 6's precondition is
  somebody else's work." The second clause is not observable by the person holding
  the book.
- **24-01** ACCEPT (when unblocked): "water poured in at the bulkhead end would run
  the whole way without standing anywhere" - a thought experiment unless water is
  actually poured, and 24-07 exists because the sag that breaks it appears later.

### 3.5 Blocked steps with no owner named

The convention in 1.2 is that a blocked step says what is missing **and who owns it**.
Most do. **20-03** ("Missing: BB-23 and 20-02"), **20-05**, **21-10**, **23-04**,
**23-05**, **26-05**, **26-06**, **27-03** and **28-07** name a missing item and no
owner. Each is recoverable by chasing the step it points at; none is a defect on its
own; together they are the edge of the convention fraying.

---

## 4. SEQUENCE PROBLEMS A PERSON WOULD HIT

### 4.1 Sections 17, 18 and 19 are a closed loop, and it is a hard stop

**17-01** "Cut one pipe per tank. BLOCKED for the length ... The length is set by the
tank in front of you and by the trip heights, **which do not exist until section
19**."

Section 19's precondition is BB-22, section 18. Section 18's precondition is BB-21,
**section 17, including its cure**. So 17 waits on 19, 19 waits on 18, 18 waits on 17.

The check's 34.2 records two candidate cycles and breaks both. **This is a third and
it is not recorded**, because it lives inside a step's blocked note rather than in a
precondition list, which is precisely what 34.5 warns the check cannot see.

The book gives the escape - "Cut long and cut again if you must. A pipe cut short is a
pipe bought twice" - but it leaves 17-01 marked BLOCKED, and 1.2 tells the builder
that a blocked step is stepped over and never substituted. A builder obeying the
convention steps over 17-01, and 17-02 to 17-05 then have no pipe. **Either 17-01 is
not blocked and the cut-long rule is its instruction, or the loop stands.** It cannot
be both.

### 4.2 The float purchase makes section 6 a precondition of D7, which must precede step 1

**2-02**: "Confirm D7 has been worked and the buy is done ... **D7 comes before this
book, not after it.**" Section 22's header: "**AND THE FLOAT CANNOT BE BOUGHT UNTIL
SECTION 6 EXISTS.** F-100." 6-07 produces the span terms that gate it.

So the book requires a finished D7 before its own step 1 and produces a D7 input at
its own section 6. A person reading in order meets this at page one of section 22 and
discovers the buy he was told to finish could not have been finished. The same shape
is behind eight other steps - 10-02 fixings, 13-08 ground bar, 14-07 heatsink, 16-01
support, 18-01 U-bolt, 21-11 paint pen, 25-04 bracket, 27-01 cradle - each of which
says "no file read for this book states it as bought" and then writes a requirement
and a search term. 2-02's accept can pass with all nine absent.

### 4.3 Section 29 runs tubing to heads on lids that section 32 then installs

BB-18 ends section 14 with "the lids not yet fitted", and 14-09 puts both lids on the
bench. Section 29 then runs sixteen tubes "from its jug station to its head's suction
barb, **through the lid penetration**" - to heads mounted on lids that are lying on a
bench, from stations fixed to the wall. **32-03** and **32-04** then lift those lids
onto the boxes, carrying eight motor bodies, eight heads and sixteen tubes, and its
accept condition is "no tubing or conductor is pinched at the sealing face."

This is the book's own defect shape 2 - work landed on a part a later section installs
- one class over from conductors. 34.4's check for it looked only at conductors and at
section 31's preconditions.

### 4.4 Section 22 threads the cords out through the grip before section 23 hangs the pipe

**22-15** takes each tank's float cords out through the tank's grip and **22-16** forms
the drip loop outside it, both with the pipes on the bench (18-06 put them there).
**23-02** and **23-03** then lower those pipes into the tanks. Lowering pulls cord
through the grip, and nothing in section 23 re-checks the drip loop that BB-26
asserts. A person threads after hanging, not before.

### 4.5 18-01 and 18-02 clamp the U-bolt before 18-03 stands the pipe in it

"**18-01.** Fit a U-bolt with a backing plate over the tank's drum lip, to each pipe."
"**18-02.** Tighten the U-bolt nuts underneath the lip, snug and not crushed."
"**18-03.** Stand each pipe in its tank and hang it on its U-bolt."

If 18-01 and 18-02 have clamped the U-bolt to the lip around the pipe, 18-03 has
nothing to do; if they have not, 18-02 tightens a clamp on nothing. The three steps
cannot all be right, and 18-02's WHY - a crushed lip on a bought tank is not
recoverable - is the reason it matters which.

### 4.6 20-04 checks clearance against four things later sections install

**20-04** confirms the marked hole is clear of "the standpipe's hang point, the return
drop's landing, the transfer discharge, the submersible cords and every penetration
and hanger M-01 carries." The return drop's landing is fixed at **28-06**, the
transfer discharge at **26-04**, the submersible cords are laid at **27-05**. Three of
the five do not exist when 20-04 is worked, and 20-04 is the check standing between
the builder and the most irreversible cut in the build.

### 4.7 "52 are ready to work today" is not reachable work

Section 35 reports 52 of 237 steps ready today. Section 1.3 says: "**If you reach a
section whose preconditions are not all true, stop. Do not start it.**" Applying that
rule, the sections a builder can open tonight are 1, 2, 3, 4, 5 and 11 - section 7
needs BB-09, section 13 needs BB-13, section 17 needs BB-20, section 32 needs BB-35.
On my count that is roughly half the 52, and the other half sits behind a closed
door - including all six of section 32's unblocked steps, which confirm the state of
wiring that does not exist.

The number is a count of steps with no blocker of their own, presented as a count of
work that can be done. Both are useful; they are not the same number, and the one on
the page is the one a person will act on.

### 4.8 Section 6 is addressed to somebody other than the reader

Section 5 ends by handing the record away (5-06) and section 6 is that person's work -
the book says so, and 34.4 counts it as handled. It is handled honestly. What is left
is that section 6 sits in a book whose stated reader is "the builder, from the first
fixing to the last lid", and its seven steps are instructions to INTERCONNECT, DOSING
and PUMP-BOXES. A builder reading in order works 5-06, turns the page, and reads seven
steps he must not do. Nothing marks the change of audience the way 1.2 marks a blocked
step.

---

## 5. FACTS ANOTHER DOCUMENT OWNS, RESTATED HERE

D1's own table in 1.1 gives each of these away, and section 35 states that "**No count
of anything the build contains appears anywhere in this book.**" These are the
restatements I found. Each is a drift surface.

| Where | What is restated | Who owns it |
|---|---|---|
| **Section 4 header** | "**ALL 125 JOINTS IN D4**" | D4/D5. wiring-instructions.md carries 125 as its own count. Repeated in section 33 |
| **7-02, 7-03** | "the **five** top-face device holes", "each of the **five** top-face holes" | parts.md, which carries the count and the size. 7-02's own last sentence says "The hole size and the count are parts.md's and D3's and are not repeated here", in the same step that repeats the count |
| **8-02** | "the motor supply entry is at the **left end** and the step-and-direction entry is at the **right end**" | subsystems/entry-faces.md 2.3. The step says "this book does not restate its reasoning" - it restates the fact, which is the half that can drift |
| **9-04** | "at the **right-hand end** of the bottom face" | D6 |
| **6-06** | "a gap between its **entry 7** and its **entry 8**" | entry-faces.md 3.3 and D6 |
| **Section 14 header, 29-08** | "Box A carries **CH1 to CH4** and box B carries **CH5 to CH8**" | D-178 and channel-token.md. Stated twice in the book |
| **15-04** | pH and EC each on a carrier, RTD on no carrier | DISPLAY-BOX and D3 |
| **21-02 to 21-09, 22-01 to 22-08** | which of LS-1 to LS-8 is on which tank's pipe | D2's roster and water-float-requirement.md |
| **19-02** | "the **four** trip heights", "the largest differential **of the eight**" | WATER |
| **22-10 to 22-13** | "the **four** float cords" per tank | as above |
| **15-06** | "the **three** EZO circuits" | DISPLAY-BOX |
| **25-02** | "FV-1 is orientation-tolerant and flow-directional ... mountable in any orientation with coil-up preferred for long life" | parts.md, quoted as a spec |
| **16-01** | "the storage tank is cone bottom and open top" | parts.md |
| **17 header** | "**THE PIPE IS PVC**" | a material spec, cited to D-121 |
| **13-08** | "the **copper** ground bar" | a material spec on a part the same step says is not bought |
| **Section 27 header** | "**TWO SUBMERSIBLES** SIT IN THE DAY TANK AND **BOTH RUN CONTINUOUSLY**" | device function, which 1.1 gives to D2 |
| **Section 33** | "C-24 lifts each float's conductor at the panel terminal in turn" | commissioning.md |

Two of these are worth separating from the rest. **The five top-face holes and the 125
joints are counts**, and they are the exact thing section 35 says the book contains
none of. **The pump box entry order in 8-02 is a fact about which cable lands where**,
restated one document away from the one that owns it, and it is the fact that 14-06's
whole no-crossing argument rests on.

**One count error inside the book's own scope.** Section 1.5: "**Six differences**,
each stated so nobody reads a missing sheet as an oversight" - the table below it has
**seven** rows, and decisions.md's own record of this document says INTEGRATOR
"differs from document-plan's sheet list in **seven** named places".

---

## 6. STEPS WHERE YOU WOULD HAVE TO STOP AND ASK, AND WHICH ARE NOT MARKED BLOCKED

1. **2-01.** D3 does not exist. You must ask whether to proceed without it, and the
   step gives you no owner to ask.
2. **4-01.** terminal-survey.md was not on the bench per 2-01. You ask where it is.
3. **11-04.** You must ask DOSING which of your joints are the port joints before the
   partial accept means anything.
4. **31-02.** You must ask whoever made each wet joint when they made it, because no
   step recorded it.
5. **32-03 / 32-04.** You must ask how a lid carrying four motors, four heads and
   eight tubes is offered up to a wall-mounted box without disturbing tubing that was
   run to it on the bench.
6. **32-01.** You must ask where the bars are in the three enclosures that never got
   one.

Two blocked steps carry a blocker that contradicts itself and would send a builder to
ask anyway: **24-03** and **30-02** both read "the placement is the owner's under
F-104, **which he has closed**" and are nevertheless BLOCKED on it.

---

## 7. SEPARATE CHECK: M-02'S TWO HALVES, AGAINST EVERY STEP BLOCKED ON IT

**The question.** D-185: D-090 answers the ENVELOPE (the wall's size, five measured
cable runs, and the cut rule). What is open is the ARRANGEMENT - where things sit
inside it. A step blocked on the answered half could be worked tonight.

**Method.** Every step naming M-02, "the wall layout", BB-08 or BB-09 as a blocker,
plus every step inheriting one of those by an "as NN-nn" reference.

**35 steps name it directly. 51 including inheritors.**

| Section | Steps naming it directly | What each is actually waiting for |
|---|---|---|
| 6 | 6-01, 6-02, 6-03, 6-04, 6-06, 6-07 | positions, spacings, a span between two positions |
| 7 | 7-04, 7-05, 7-09 | entry positions within a face |
| 8 | 8-02, 8-03, 8-08 | entry positions within a face |
| 9 | 9-02, 9-03, 9-04, 9-07 | entry positions within a face |
| 10 | 10-01, 10-02, 10-03, 10-04, 10-05 | mounting positions |
| 12 | 12-01, 12-03 | mounting positions |
| 16 | 16-01, 16-02 | floor positions |
| 20 | 20-04 | clearance between positions |
| 24 | 24-01, 24-04 | where a tank stands relative to the track |
| 25 | 25-04 | a bracket's position |
| 26 | 26-01, 26-02 | a pump's position and a route |
| 27 | 27-07 | where the chiller stands, which BB-08 does not produce (2.4) |
| 29 | 29-18 | a sightline between two positions |
| 31 | 31-03, 31-04 | gland positions and which way a cable runs on the wall |

**RESULT: 35 of 35 are blocked on the POSITIONS. Zero are blocked on the SIZE. No step
in this book could be unblocked tonight by D-090's envelope alone.**

That is the honest count, and it is a good result for the book: it does not
mis-attribute a single step to the wrong half of M-02.

**Where the wrong half does appear is in the prose, twice, and both are drift
surfaces:**

- **Section 1.6:** "Until it exists, every dimension in this book is blocked: every
  mounting position, every gland position, every tank position, **every cable
  length**, and the float cord length." Cable length is D-090's answered half - five
  measured runs and a cut rule of wall run plus 3 ft. **It is not blocked on M-02.**
  What it is blocked on is **F-099**, the two parts.md tables carrying those same five
  figures under contradictory allowance rules - which **31-01 names correctly** as the
  first step of section 31. So the book contains both the right blocker and the wrong
  one, 1900 lines apart, and 1.6 is the one a builder reads first.
- **Section 33** repeats 1.6's sentence, and section 35 repeats it again as "every
  dimension ... M-02 ... an evening with a tape measure."

**Two things that could be worked tonight, which are not steps blocked on the wrong
half but are next to them:**

1. **6-07, the float cord span terms.** This is the step that gates the float
   purchase under F-100, which gates section 22, which is a precondition of section
   31. Its exact value needs the arrangement. But a **bound** on the worst-case span
   follows from D-090's envelope and the cut rule without any arrangement at all, and
   the requirement 6-07 feeds is a **disqualification** test - "a float whose supplied
   cord does not reach is disqualified". A conservative bound disqualifies the same
   floats a measured span would. **Worth putting to INTERCONNECT and WATER tonight:
   can the float search start against a bound from the envelope?** If yes, the
   longest-lead purchase in the book stops waiting on the arrangement.
2. **5-01, "Measure the wall and write the figures down."** The wall's size is already
   on file under D-090, recorded in parts.md, and 5-01's own WHY says so - "parts.md
   states the layout envelope; nothing in this tree states what is actually on that
   wall." The genuinely unknown work in section 5 is 5-02 to 5-05: the fixings, the
   stub, the branch circuit and the drain track. **5-01 could be reduced to a
   confirmation against D-090 rather than a fresh measurement**, which also removes a
   second place the envelope can be written down.

---

## 8. WHAT IS GOOD, SAID PLAINLY

The WHY notes are the strongest thing in this document set. 7-08, 13's duct rule,
18-04, 19-04, 20-07, 22-09, 24-05, 28-05 and 30-03 each tell a builder what he is
about to trade away, which is the one thing that stops him improving the design at
2am. Four sections end at a cure and each names the wait as its own last step, with
the next section restating it - that is defect shape 1 handled properly, four times.
Section 29's one-step-per-channel expansion, and its stated reason, is G-49 clause 1
applied deliberately at a cost of fourteen extra step numbers. 14-08 is the book
seeing defect shape 2 inside a single section and splitting the step for it.
Section 34.5 is honest about what the check cannot do, and it is right.
