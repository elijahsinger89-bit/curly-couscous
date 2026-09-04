# WATER on S-18, F-003 and the three numbers DOSING is blocked on

Returned 2026-08-30, WATER's first invocation. Nothing decided, no file it owns
changed. WATER reported stopped part-way and did not declare itself finished.

## S-18: the direction is confirmed, two things it does not say are objected to

**The compressor is not the problem.** Holding a compressor off longer than it
would otherwise be off is the protected direction. Every compressor protection
that exists, anti-short-cycle delay, minimum off time, crankcase management,
restart delay, exists to enforce MORE off time, never less. Nothing in
refrigeration practice is damaged by extra idle.

**But the wear metric is starts per hour, not off time, and a hold-off does not
add off time. It fragments the chiller's own cycle.**

- A hold-off beginning while the compressor is running creates a FORCED SHORT RUN
  followed by a forced off. Short runs are the classic oil-return and
  motor-heating problem, not long offs.
- At release the tank has drifted, so the chiller's own thermostat is now calling
  and it starts. That start would not have existed if the cycle had been left
  alone.
- Repeat several times a batch and compressor STARTS go up while average run
  length goes down. That is short-cycling by a different route, arrived at from
  outside.

So D-023 is safe if and only if a hold-off never truncates a run in progress, or
the windows are long relative to the chiller's natural cycle. Neither condition is
stated, and **nothing in this system can see whether the compressor is running.**
WATER read decisions.md, interface-table.md, main-panel.md and control-software.md:
no row carries chiller status back to the Pi, and S-09 is a coil drive outward
only. The condition cannot be enforced, only approximated by making the window
long.

### The second objection, which nobody had named: G-12

G-12 is frozen. The chiller and its loop pump are on ONE contactor. So "hold the
chiller off" does not hold off a chiller. It de-energises the chiller AND the
chiller loop submersible together.

1. Flow through the chiller stops at the same instant the compressor does.
   Whether that machine tolerates zero flow at shutdown, and whether it wants
   pump run-on, is a manual question.
2. **If the chiller loop submersible draws from and returns to the day tank, D-023
   removes a mixing source during exactly the window in which we are waiting for
   the tank to mix.** F-004 leg 5 says mixing is the dominant leg of t_settle and
   that agitation is only the bottom suction and the return drop's plunge. If a
   second return jet exists and D-023 switches it off, **D-023 lengthens the very
   interval it is applied across.** It buys read cleanliness with settle time.

WATER checked F-08, P-05, water.md and dosing-f004-wet-side.md: **no file states
which tank the chiller loop submersible sits in.** It is WATER's open placement
item. WATER is not asserting the consequence, it is reporting that G-12 plus D-023
makes that placement load-bearing on settle time in a way it was not before.

### Datasheet numbers needed, none stated from memory

| Number | Why it decides this | Search term |
|---|---|---|
| Anti-short-cycle or restart delay, and whether it survives a power interruption | If the unit holds its own delay across a power cut the hold-off is self-protecting and the first objection largely evaporates. If the delay is lost with power, every release is an immediate unprotected restart | JBJ Arctica DBE-200 manual compressor delay restart |
| Minimum run time and oil return requirement | Sets how short a truncated run may be, so how long a settle window must be to be safe | JBJ Arctica minimum run time compressor short cycling |
| Behaviour on loss and restoration of power: auto restart, setpoint retention, or a latched fault | If it latches or needs a manual restart, a hold-off leaves the chiller OFF after the batch and nobody finds out until the tank is warm | JBJ Arctica DBE-200 power failure restart setpoint memory |
| Internal flow switch or low-flow lockout, and behaviour when flow stops | G-12 stops flow and compressor together. A machine that faults on flow loss faults every hold-off | JBJ Arctica chiller flow switch low flow alarm |
| Whether flow must continue after compressor shutdown, and freeze protection with stagnant water in the barrel | The direct consequence of G-12, and the one WATER would check first | JBJ Arctica DBE-200 pump run on stagnant water freeze |
| Rated cycles per hour, if published | The only figure that turns "several times a batch" into safe or unsafe | JBJ Arctica DBE-200 specifications cycles per hour duty |

If the manual answers the first and fifth benignly, D-023 is confirmed outright.
If either is unfavourable, D-023 needs a minimum window length and a minimum
recovery period between windows, and those are numbers, not decisions WATER can
invent.

### What a hold-off does to tank temperature

**No file states a day tank temperature setpoint.** WATER searched decisions.md,
interface-table.md, commissioning.md, water.md and dosing-f004-wet-side.md.
Without it the direction of drift cannot be stated, only what drives it.

- **The sign of the drift is set by setpoint versus room.** Below 62 to 65 F the
  tank warms during a hold-off. At or above room the chiller barely runs, the
  hold-off is nearly free, and most of S-18 is moot. That single unknown decides
  how much D-023 costs.
- **During a settle window the heat balance is the worst it ever gets, and this is
  deliberate but was unstated.** The manifold pump must keep running
  through the window, because settling counts circulating time. A submersible puts
  essentially all its electrical input into the water it sits in. So a heat source
  runs while the heat sink is switched off. The drift is one-directional and
  accumulates across several windows in one batch if the chiller cannot fully
  recover between them.
- Working against it: both tanks are open top, so evaporation removes heat
  continuously and the room's dehumidifying AC sustains it. WATER put no number on
  it.
- **The shape of the disturbance changes, and this is a better argument for D-023
  than magnitude.** A cycling compressor gives the trace STEPS. A hold-off gives a
  slow monotonic SLOPE. A slope is far easier to distinguish from a dose and far
  easier to subtract.
- **A benefit BOSS did not claim:** the chiller stratifies the tank, and
  stratification suppresses convection and makes mixing worse. Holding it off
  during the window reduces stratification during the window, which helps
  t_settle and partly offsets the G-12 mixing loss.
- **The disturbance is deferred, not removed.** At release the chiller restarts,
  cold water re-enters, temperature and compensated EC move. If the next window
  follows soon, the previous release's thermal transient is still in flight.
  Window spacing and chiller recovery interact and nothing on file said so.

## F-003: the reframe that changes the question

**No sense element can verify a stopped pump.** At rest the pump is off by design.
A flow switch reads no-flow, a current switch reads no-current, a pressure switch
reads no-pressure, and all three are the CORRECT readings for a healthy idle pump.
They are also the correct readings for a dead one. Adding an instrument does not
answer F-003, it answers a different question.

**So the first half of F-003 is not a sensing question. It is a scheduling
question.** The only way to know a stopped pump is alive is to run it. Sensing
only ever answers "what witnesses the exercise".

### Half one, the exercise. Costs nothing.

The manifold pump is commanded on for a short exercise run on a defined
trigger: a rest interval elapsing, and unconditionally at batch start before the
first dose. It needs no hardware. CONTROL-SOFTWARE schedules it, MAIN-PANEL's
relay switches it, WATER owns only that the pump and tank permit it, and they do.

Two constraints WATER owns on it: the exercise must not run with the tank below
the submersible's minimum submergence, which is the same condition S-05 protects
against; and exercise running is circulating time, so an exercise firing inside a
settle window is a contaminant in the same way a fill is.

### Half two, what witnesses it

| ID | Option | Proves | Plumbing | New failure modes | Panel |
|---|---|---|---|---|---|
| W-1 | **The probes already in the loop.** At rest the water standing in the vertical probe section sits in room air at 62 to 65 F while the tank is chilled and stratified. The standing column drifts toward room temperature. On pump start that column is displaced by tank water and the PT-1000 sees a step within the transport time. **No step means no flow.** Temperature is the witness, not EC or pH: temperature has a guaranteed physical driver here because the chiller creates the differential deliberately | Flow through the WHOLE loop, tank to pump to F-03 to probe section | None | False fail when tank and room converge or the rest was short. Diagnostic only, arrives seconds late and in software, protects nothing, and is not a substitute for S-05 | None |
| W-2 | Current sensing on the pump cord | Motor energised and drawing. Catches a dead motor, a tripped overload, a failed or welded relay, a pulled cord, a lost circuit | None | **Reports healthy through the failure that matters most.** A submersible with a fouled or broken impeller, an air-locked volute or a blocked intake still draws current. Current is not flow, and F-004 names silent flow degradation as the dominant hidden input to the whole settling time | A device, a contact, an inrush blanking decision |
| W-3 | A flow-proving element in the wet path | Flow is actually occurring, which is the thing | A body, two unions, a new leak path into the permissive chain via G-08, plus added restriction that reduces the very flow it measures | Stuck-made reports healthy forever, which is F-003 one layer up. **Closed by the free self-test below.** Fouling in nutrient solution | One dry contact, and the start-up bypass conflict with S-05 |
| W-4 | Pressure at the discharge | Less than W-3 for less money. A dead-headed pump against a closed valve makes pressure with no flow | as W-3 | Rejected by WATER | as W-3 |
| W-5 | **The operator's eyes at the return drop.** If the drop is an open atmospheric air gap, which it must be to break the siphon, flow is directly visible and audible. The one point in the loop where flow is an unambiguous event to a human | Everything the instruments miss | None. Requires the drop be in sightline | Human, not automatic | None |

**The strongest single idea in the answer, and it is free.** For W-3: the pump DOES
stop between batches. Place the element where the at-rest state is a KNOWN-OPEN
state, and the rest interval becomes the element's own self-test. **An element
that never opens between batches is stuck.** The running interval proves the loop,
the resting interval proves the element, each state checks the other, and the
"worse than none" trap closes. It costs nothing beyond the element and a software
rule, and it converts the at-rest interval from a blind spot into a test.

W-3 placement is a real choice WATER did not make: at the pump discharge before
F-03 proves the pump, simplest and cleanest; at the return drop after F-04 proves
the ENTIRE loop including the manifold, catching the other half of F-004's silent
degradation, but sits in an open splashing aerating atmospheric path outside the
pressure boundary and will foul with nutrient deposit. WATER needs the return drop
arrangement settled first, because the two decisions are the same decision.

W-3 requirement, to be matched against a datasheet the owner pastes: wetted
materials compatible with nutrient solution and pH-adjusted water; dry contact
rated for pilot duty on MAIN-PANEL's chain; actuation flow adjustable below normal
service flow and above zero; mounting orientation and straight-run requirement;
serviceable without cutting pipe. Search terms: paddle flow switch PVC dry contact
pilot duty; inline liquid flow switch adjustable set point plastic; shuttle piston
flow switch chemical compatible. For W-2, MAIN-PANEL's not WATER's: split core
current sensing switch adjustable trip point pilot duty.

**WATER's recommendation, stated as a recommendation:** W-1 plus W-5 first,
because both are free and neither forecloses anything, and hold W-3 pending the
return drop geometry. Which is exactly what D-019 did with the keyed coupling, for
the same reason.

W-1 needs one thing before it is usable: the magnitude and timing of that
transient, measured. Nobody had written that commissioning row.

## S-05 and F-003: TWO questions, with one asymmetrically available shared answer

1. **They sense at different points in the causal chain.** Dry-run is about the
   SUPPLY, is there water at the intake. At-rest verification is about the RESULT,
   is water arriving at the far end.
2. **The mapping is asymmetric, and this is the sentence that matters.** A
   FLOW-proving element senses the result and would also catch a dry tank, so it
   can subsume dry-run protection. A LEVEL element senses the supply and can NEVER
   subsume circulation verification: it reads healthy through a fouled impeller, an
   air-locked volute, a blocked intake screen and a shut valve. **So choosing a
   level-based answer for S-05 forecloses the shared solution, and choosing a
   flow-based one keeps it open. S-05 should not be answered before F-003 is.**
3. **Opposite timing requirements that conflict inside one element.** Dry-run must
   act fast, within whatever the pump tolerates running dry. Circulation
   verification must NOT act on a transient, because flow takes time to establish
   at every start and any flow element reads open during that time. The same
   contact wants a start-up bypass for one duty and no bypass for the other. That
   conflict lands in MAIN-PANEL's chain and must be resolved there before one
   element is asked to do both.
4. **Different consequences and different owners.** Dry-run drops the pump in
   hardware, independent of the Pi. Circulation verification stops a BATCH and
   tells the operator, which is software under G-16. Wiring one element to do both
   means a circulation fault also drops the pump in hardware. That may be right,
   but it must be a decision and not a side effect.
5. **The at-rest half is not a sensing question at all.** Dry-run protection
   entirely is. A single answer cannot cover both halves because one half has no
   sensor in it.

If the owner chooses one element it must be a flow-proving element in the
discharge with: a pilot-duty dry contact into MAIN-PANEL's chain; an actuation
point below normal service flow and above zero; a start-up bypass whose duration
MAIN-PANEL owns and which must be shorter than the pump's dry-run tolerance; the
known-open-at-rest self-test; and an explicit ruling on whether a verification
failure may drop the pump in hardware. Even then it is one element answering two
questions, not one question.

**WATER deliberately did not return the S-05 sensing method in this pass**,
because returning it early would foreclose F-003. Reported as a dependency, not
as a stall.

## The three numbers DOSING is blocked on

### Circulation flow at F-03

**Requirement:** a volumetric flow rate at F-03 under SERVICE conditions: the
manifold as built with its probe section and all injection ports, every valve in
its normal running position, the return drop as built, the day tank at a stated
level, in the service solution at service temperature, with the strainer in
whatever condition it is in.

**Why a pump curve cannot supply it:** a curve is head against flow for the pump
alone. The operating point is where that curve meets the SYSTEM curve, and the
system curve is unknown in every term here: manifold diameter and ports are OPEN,
F-05 and F-06 are OPEN, the probe section is not specified, valve positions are not
recorded, and the strainer's condition changes over time. A curve reading is a
number with nothing behind it, which commissioning.md's own preamble rejects.

**Method, with what he owns: catch and time at the return drop.** It is an open
atmospheric discharge, so it can be diverted into a graduated container for a
timed catch with a bucket and a phone timer. The method's failure modes decide
whether the number is real:

- **Do not lift the hose to catch it.** Raising the discharge adds static head, the
  pump backs down its curve and the reading is low. The catch container's rim must
  sit at the same elevation as the normal landing point.
- Keep the catch short enough that the day tank level does not fall materially. A
  falling level changes both submergence and return head, so a long catch measures
  a moving system.
- Catch into a container standing in the tank if that is what it takes to keep the
  elevation and return the water.
- Repeat at the high and low ends of the fill band. DOSING needs the high-end
  number, since high level is the slowest mixing condition.
- Repeat after any re-measure trigger event.

Search term for the method, not a part: catch and time bucket test pump flow rate
measurement.

**One method to explicitly avoid:** dosing a slug and reading the EC approach
curve looks like a flow measurement and is not one. The tank is not ideally mixed,
so that curve yields mixing behaviour, not flow. It would give a confident wrong
number.

**A ruling WATER asked for before proposing any instrument here:** D-007 closed
S-13, no flow SIGNAL into the Pi. G-04 forbids flow meters ON THE DOSING LINES.
Neither, read literally, forbids a one-time commissioning measurement on the
circulation loop. WATER is not treating that as permission. If catch-and-time
proves inadequate, a borrowed or rented clamp-on device is a question for the
owner. Search term if it ever comes to that: clamp-on ultrasonic flow meter rental
PVC pipe.

### Day tank working volume and the fill band

**Not one number, a band, with both ends and the reason for each.** The 40 gal in
the parts list is the vessel's nominal capacity, not a working volume, and must
not be used as one.

**The HIGH end** is set by the stop float actuation point, minus freeboard for the
return drop's plunge and splash (the tank is open top, so overflow goes on the
floor, which is a leak-console event that drops the whole system via G-08 - the
freeboard is a safety margin, not a nicety, and it ties to S-04 placement), minus
SURGE (the volume that still arrives after the stop float actuates: relay dropout,
transfer pump coast-down, and liquid in transit in the transfer line, a measured
quantity on this build), minus the total dose volume of a batch, because dosing
adds volume after the fill has stopped. That last figure is DOSING's.

**The LOW end** is the higher of the start float actuation point and the
submersible's minimum submergence: intake covered, motor covered if it is
water-cooled by immersion, and enough depth above the intake to prevent vortexing.
**The vortex constraint is usually binding and it is not only a pump-protection
issue.** A vortex draws air into the loop, and air past the probes produces exactly
the spike DOSING warns about in step 4 of its procedure, the one that looks like an
early arrival. So the low end of the band is a MEASUREMENT-QUALITY limit as well
as a pump limit.

**And a hazard neither float covers.** V3 is manual and out of scope, and 36 plants
are served downstream. The operator can draw the tank down independently of the
fill chain. If draw exceeds refill, level reaches the intake regardless of where
the start float sits. **That is the dry-run case and it is why S-05 exists.** The
low end of the band and the S-05 trip point are the same physical elevation
question asked twice.

| Needed before the band can be stated | From | Search term |
|---|---|---|
| Actual internal dimensions and shape of the day tank as built, measured, not from the nameplate | Owner, tape measure | none, it is a measurement |
| Submersible minimum submergence, and whether the motor is water-cooled by immersion | Pump datasheet | submersible pump minimum submergence water level requirement |
| Float actuation depth and differential | Float datasheet once floats are chosen | vertical float switch pilot duty differential |
| Surge volume after stop-float actuation | Measured on this build | none |
| Maximum total dose volume per batch | DOSING | — |

### The return drop and short-circuiting

**Yes it can be arranged so it does not short-circuit, and yes it can be ruined by
someone tidying a cord. Both halves of DOSING's warning are correct and the second
is the one that needs engineering.**

Fixed constraints: G-11 puts suction at the tank bottom, so suction location is not
a variable. The return must discharge ABOVE maximum liquid level, an air gap, or
the loop siphons back when the pump stops. Consequence, already recorded as F-004
leg 4: an air-gap drop is a free-falling stream and it entrains air, and that air
reaches the probes.

1. **Never directly above the intake.** A plunging jet penetrates downward and
   carries entrained air with it. If the suction sits under the landing point that
   path is simultaneously the short-circuit path AND an air delivery pipe to the
   pump intake and thence to the probes. Both penalties at once. This rule must be
   physically enforced, not intended.
2. **Maximum horizontal separation, and aim the jet.** Vertical separation is
   already maximal. The free variables are horizontal position and the DIRECTION of
   the plunge. Directing it tangentially to set up a slow rotation converts a point
   jet into whole-tank circulation and attacks the dead zones in corners and below
   the intake. **WATER calls this the highest-value free decision available on the
   entire settling-time problem, and it costs a bracket angle.**
3. **Standoff at the intake.** The submersible must not sit flat on the floor: it
   starves, and on a flat bottom it sits in sediment. Needs the tank geometry.
4. **The anti-tidying requirement, which is the real answer to DOSING.** Position is
   held by a MECHANICAL FIXTURE, not by where a cord happens to rest. The return
   drop rigidly clamped to a bracket at the rim so it cannot be swung or lifted.
   The submersible in a fixed cradle, foot or standoff, or fastened to a bottom
   plate, NOT hung by its cord: a cord-hung pump is a pump whose position is a
   suggestion. Both cords strain-relieved at the rim so the cord carries no
   positioning duty at all. **Both positions marked on the tank, so a displacement
   is visible at a glance without anyone measuring.** Free, and the only thing that
   survives a person who is being helpful. This is M-01 work. Search terms: tank rim
   pipe mounting bracket clamp; cord grip strain relief bulkhead; submersible pump
   mounting foot bracket.
5. **Two mutually exclusive families, named rather than chosen.**
   (a) Free air-gap drop above max level. Siphon broken by geometry. Entrains air.
   Aiming limited to what a falling stream can do. **Its failure mode is visible:**
   you can see and hear whether it is flowing, which is also W-5.
   (b) Submerged return with an anti-siphon vent hole above max level. Much better
   directed mixing, far less air entrainment, properly aimable. **But the siphon
   break now depends on a small hole staying clear, and that hole fouls shut
   silently in nutrient solution.**
   WATER will not take (b) without a ruling: trading a visible failure for an
   invisible one is the wrong trade, which is D-019's reasoning applied unchanged.
6. **The verification already exists and belongs to someone else.** F-004's
   procedure step 4: an overshoot then fall-back in the settling trace is the
   signature of a slug reaching the probe before the tank is uniform, which is
   short-circuiting. And a t_settle materially faster than one loop turnover means a
   short-circuit path exists. **So the geometry decision is checked by a measurement
   already scheduled at C-02, at no extra cost.** That should be written down as the
   acceptance criterion for the arrangement.
7. **The chiller loop complicates this.** If its submersible sits in the day tank
   there are TWO suctions and TWO returns in one tank, four positions to fix, and
   their mutual arrangement matters as much as the circulation pair's. And per D-023
   one of those jets is switched off during exactly the settle window. No file states
   which tank it sits in. That placement is WATER's, it is open, and it is now
   coupled to S-18 and to C-02.

## Still owed by WATER and untouched in this pass

The fill solenoid requirement P-02, which MAIN-PANEL is blocked on. Which floats,
their pilot duty and placement, S-01 and S-02. Leak sensor placement S-04. The
S-05 sensing method, deliberately held pending the F-003 ruling. The chiller loop
flow requirement against the DBE-200 datasheet and whether the second submersible
meets it. Day tank penetrations and hangers M-01. The choice between return-drop
families (a) and (b).
