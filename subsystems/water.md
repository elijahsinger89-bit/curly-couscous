# WATER

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

Tap connection. Fill solenoid as a device, its placement and its plumbing.
100 gal cone bottom storage tank. All float switches in the system: which
floats, what type, pilot duty rating needed, and exactly where each one sits in
each tank. Anbull transfer pump and its plumbing. 40 gal day tank. Both
hi-flow submersibles as devices and their placement. All day tank penetrations
and hangers. The JBJ Arctica DBE-200 chiller and the whole chiller loop
plumbing. The manifold return drop back to the day tank. Physical placement of
the leak detection sensors and of the dry run sense element.

Ends at V3 and at the manifold unions F-03 and F-04.

## Out of scope

Anything electrical past the device: relays, contactors, the permissive chain,
receptacles, coil wiring. Those are MAIN-PANEL. Cable routing on the wall is
INTERCONNECT. The manifold itself and everything on it is DOSING.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| F-09 | Day tank outlet to V3 is the scope boundary. V3 is manual. Nothing downstream is designed here |
| G-03 | Fill control is a start float and a stop float with relay seal-in between them, both tanks |
| G-01 | Floats are hardwired to relays and invisible to the Pi |
| G-11 | Circulation submersible takes suction at the day tank bottom so the tank mixes |
| G-12 | Chiller and its loop pump are switched together on one contactor |

## Settled

- Tanks, pumps and chiller are bought and listed in decisions.md.
- Both tanks are open top.
- Room 62 to 65 F, under 60 percent humidity, not wet.

## Open, owned by WATER

- Fill solenoid requirement: coil voltage, port size, connection type, and
  whether it needs to hold closed on loss of power. Return a requirement and a
  search term. MAIN-PANEL cannot size the relay contact until this comes back.
- Which floats, their pilot duty rating, and their placement in both tanks.
- Dry run sense element: what it senses. Interface S-05 is blocked on this and
  MAIN-PANEL cannot wire the interlock without it.
- Leak sensor placement: where water can reach the floor or a wall.
- Chiller loop flow requirement against the DBE-200 datasheet, and whether the
  second submersible meets it.
- Day tank penetrations and hangers, including how both submersible cords and
  the return drop pass.
- Return drop must break the siphon path back to the tank. Confirm how.

## Assigned 2026-08-30: findings.md F-003, primary owner

Nothing in this system verifies anything at rest. Between batches the loop is
still and EC sits flat whether the circulation submersible is healthy or dead.
The first anyone knows is at the start of the next batch.

WATER holds this because it owns the circulation submersible, the day tank and
the placement of any sense element. MAIN-PANEL holds the other end because it
owns the relay and the dry run interlock chain. Neither may assume the other has
it. See decisions.md D-016.

BOSS's note, not a design instruction and not a conclusion: this sits next to
S-05, where WATER already owes what the dry run interlock senses. Whether at-rest
circulation verification and dry run protection are one question or two is for
WATER and MAIN-PANEL to answer. BOSS has not checked and is not assuming.

## Answered 2026-08-30, first invocation, nothing finished

subsystems/water-s18-f003.md. S-18 conditionally confirmed with two objections.
F-003 reframed: no sensor verifies a stopped pump, so the first half is a
scheduling question and the exercise run is free. S-05 and F-003 established as
two questions, and the S-05 sensing method deliberately held so that answering it
early does not foreclose the shared flow-based solution.

Three numbers returned as methods rather than figures, now commissioning C-10,
C-11 and C-12.

## Open, added or sharpened by that pass

- **Which tank the chiller loop submersible sits in.** No file states it. It is now
  load-bearing on the settling time through F-008, and coupled to S-18 and C-02.
- **The return drop family: (a) free air-gap drop, visible failure, entrains air,
  limited aiming; or (b) submerged return with an anti-siphon vent hole, better
  mixing and less air, but the siphon break depends on a small hole staying clear
  and that hole fouls shut silently.** WATER will not take (b) without a ruling,
  on D-019's reasoning: trading a visible failure for an invisible one is the
  wrong trade.
- **Aim the return jet tangentially.** WATER calls this the highest-value free
  decision available on the whole settling-time problem, and it costs a bracket
  angle.
- **Position held by fixture, not by cord.** The drop rigidly clamped, the
  submersible in a cradle or fastened, both cords strain-relieved so they carry no
  positioning duty, and both positions marked on the tank so a displacement is
  visible without measuring. A cord-hung pump is a pump whose position is a
  suggestion. M-01 work.
- **The acceptance criterion for whatever geometry is chosen already exists:**
  C-02's trace. An overshoot then fall-back means a slug reached the probe before
  the tank was uniform, and a t_settle materially faster than one turnover means a
  short-circuit path exists.

## Waiting on

| From | What |
|---|---|
| DOSING | Manifold inlet and outlet union type and orientation, F-03 and F-04 |
| MAIN-PANEL | The contact duty and terminal each float chain lands on, S-01 and S-02 |
| INTERCONNECT | How field cables leave the wet area |

## Do not

Do not add jug floats or dosing line flow meters. See decisions.md G-04 and
G-05. Do not set pipe size, tank fitting size or pump counts from memory.

## FOR YOUR INFORMATION, 2026-09-03, D-101. S-05 WAS CARRYING A COST NOBODY TOLD YOU ABOUT.

You held S-05 open deliberately, on the ground that a FLOW-proving element can
subsume dry-run protection while a LEVEL element can never subsume circulation
verification. That reasoning stands and D-060 priced it: flow-proving costs a
timing element, level-based costs the capability permanently.

**What you were not told is that document 12 has since described that capability as
STRUCTURALLY IMPOSSIBLE, in three places, and commissioning C-23 copied the claim.**
AUDIT run 3 found it and D-101 reverses it. **The claim was wrong.** C-23 is
corrected, D-095 is superseded in part, and the document is with CONTROL-SOFTWARE.

Nothing is being asked of you and S-05 is not being reopened. **This is here so that
if S-05 comes back to you, you decide it against D-060's real price and not against
a capability someone had written off.** T-023 is why it is worth telling you at all:
nobody pays for a door they have been told is bricked up.

## SECOND TIME IN ONE DAY, 2026-09-03, D-103. S-05 AGAIN, AND THIS TIME IT IS IN THE FROZEN FILE.

This morning you were told document 12 had written off circulation verification.
**AUDIT then graded decisions.md itself and found that D-060 - the entry BOSS
cited as the authority for saying the door was open - overstates in the same
direction.** F-076.

Your own S-05 row says a LEVEL element forecloses **the shared solution**: that
this element cannot subsume circulation verification. **D-060 escalated that to
"circulation verification is foreclosed permanently", which is a claim about every
route rather than about one element.** Three things on the table say otherwise:

- **F-003 is separately assigned** by D-016, to you, with MAIN-PANEL at the other
  end. S-05's row says S-05 must not be answered before F-003 is.
- **C-12's W-1 transient** - the standing probe-section column at room temperature
  against a chilled tank - which C-12 calls the only F-003 option that costs
  nothing and adds nothing.
- **S-20 exists on EITHER fork.** Circulation is a pole on K-DRY under D-058, so
  the Pi can read whether the pump was energised no matter how S-05 resolves.

D-060 is annotated, not rewritten. **S-05 stays open and BOSS is not answering it.**

What is asked of you, and only this: **when S-05 does come back, decide it against
D-060's real price - one timing element for the flow-proving fork - and against
what F-003 and C-12 and S-20 actually leave open.** Not against a foreclosure that
was written more strongly than your own row supports. T-023.

## THREE ANSWERS AND ONE NEW OPEN ITEM, 2026-09-03. D-108 THROUGH D-111.

**1. THE CHILLER IS ENTIRELY SELF-CONTAINED, D-108.** It plugs in, senses its own
water with its own built-in sensor, and cycles its own compressor. **F-044 closes:
there is no chiller contactor.**

**The Pi's day tank temperature reading is for the DOSE, not for control.** It
compensates pH and EC. **It is not a control input to anything.**

**2. AND THAT FORCES YOUR NEW ITEM, F-086.** G-12 is frozen and says the chiller
and its LOOP PUMP are switched together by one contactor, with the reason "the
chiller has no internal pump". **No contactor means nothing on file switches the
loop pump.** The chiller controlling itself says nothing about what moves water
through it.

**BOSS has not chosen between the four possibilities and neither should you: G-12
wrong about the internal pump, the loop pump on its own switch nobody recorded, it
runs continuously, or it is on the chiller's own cord.** It is one question and it
is with the owner. **Do not design around any of the four.**

**3. ALL PVC IS 3/4 INCH SCHEDULE 80, D-109.** That is the manifold diameter and
**the port arrangement is downstream of it. Schedule 80, not 40**, so wall
thickness and inside diameter differ from the common case and **any threaded port
is into a thicker wall.**

**Derive nothing from it and return search terms instead.** What follows - port
count, spacing, thread engagement, pressure drop, and whether C-10's catch-and-time
method is affected by the bore - is yours to ask for, not to compute. **One
dimension and a schedule is not a hydraulic model.**

**4. THE FILL VALVE IS A SOLENOID. D-114 REVERSES D-111 THE SAME DAY.**

**Energise to open, spring closed on power loss. Installed with unions either side
so it can be replaced without cutting pipe.**

**Everything the previous routing said about a motorized ball valve is WITHDRAWN.**
There is no travel-time number to check your float bands against, no two/three/five
wire relay fork, and **no auxiliary position contact - so the "only direct
confirmation in the water path that a commanded thing moved" is gone. Do not design
around it. It was never there.**

**The fail state is why, and it is the whole reason:** a motorized valve holds
position without power, so a power failure mid-fill leaves it open and the day tank
overfills. **On a valve that fills a tank, hold-last is the wrong failure.** And the
speed is the same point: **the float that stops the fill is the only thing stopping
it**, so seconds of travel put an unmeasured volume past the switching point every
time.

**That is now G-39, frozen beside G-22: when choosing an actuator, ask what it does
with no power BEFORE asking anything else. Every other property is a preference.**

**Still open and with the owner: voltage, pipe size, and whether it is normally
closed.** Search terms are in findings.md under F-087. **One of them is yours to
have an opinion on before he looks: MINIMUM OPERATING PRESSURE DIFFERENTIAL.** A
pilot-operated solenoid needs a pressure difference to open at all. **Say what the
supply actually offers at the fill point, or say that nothing establishes it - do
not assume a house pressure.**

## THE 1ST EDITION SET IS READ. TWO GUARDS BEFORE ANY PROPOSAL, D-116.

audit/2026-09-03-1st-edition-floats-and-wall.md. 24 float proposals, 26 wall
proposals, every one written as "observed in the 1st Edition set, unverified,
confirm or replace". **G-40 is frozen: it is a citation, not a source. Where it
disagrees with this tree, THE TREE WINS. You may not cite it for anything.**

**GUARD 1, AND READ IT BEFORE YOU OPEN THE FILE. The old set closes dry-run
protection with the day tank low-low float, which is a LEVEL element.**

**That is exactly the choice you are holding S-05 open to avoid foreclosing.** Your
own row says a level element can never subsume circulation verification, and D-060
prices the flow-proving fork at one timing element.

**S-05 STAYS OPEN. Do not adopt the old set's dry-run answer, and do not treat it
as a starting proposal for S-05.** It is a starting proposal for FLOATS, which is a
different question that happens to share a device. **The danger is not that the
answer is wrong. It is that an open question would close because the old set
already answered it, with nobody deciding to close it.**

**GUARD 2, F-089. The old set's floats are rated to switch a 120 VAC coil and this
build's control voltage is 24 V.** Under G-31 that is a fifth of the contact power
at the same current. **It lands on S-01 and S-02 directly. G-24 says the minimum
switching load question is asked of every contact, and this is the first time
anyone has asked it of a float.** Joint with MAIN-PANEL.

**AND ONE THING BLOCKS THE WHOLE FLOAT PASS UNTIL THE OWNER ANSWERS IT, F-090.**
parts.md carries LS-1 through LS-8 on a named part, with its own note that nobody
traced the chain. **The 1st Edition set has exactly that roster on exactly that
part.** Either they converged independently or **the tree's roster is inherited
from the set you would be checking it against, which is circular.** Do not confirm
a float proposal against parts.md until that is settled.

## THE STANDPIPE. D-117, AND IT IS THE MOST VALUABLE THING IN THE OLD SET.

S-01 and S-02 both wait on you for "the physical location", and **nothing in this
tree says what a float is ATTACHED to.** The old set's answer: **one rigid pipe per
tank carrying every float and every cord, hung off the rim, nothing hanging off a
float body.**

**It contains no figure, so it survives every number in the old set being wrong.**
G-34's shape arriving from a source where every dimension is suspect. **And it
unblocks S-01, S-02 and CBL-04 together, because a cord route is a consequence of a
mounting method.**

**Your own file already states the principle and never applied it here:** "Position
held by fixture, not by cord. A cord-hung pump is a pump whose position is a
suggestion."

Two frozen facts make a drifted FLOAT worse than a drifted pump: **nothing in this
system measures a level, so a float that has moved is invisible**, and **D-114
makes the fill-stop float the only thing stopping the fill.**

**It is a proposal, not a decision. It is with the owner.** Do not size a pipe, do
not choose a mounting, do not name a part.
