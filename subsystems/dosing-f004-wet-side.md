# DOSING on F-004: the wet side of the settling time

> **STOP. CORRECTION 2026-09-03, D-105, BEFORE YOU RUN ANYTHING IN THIS FILE.**
>
> **commissioning.md names this file as C-02's FULL PROCEDURE, so a person runs it.**
>
> **The gating sentence below is WRONG and is not to be executed. There is no
> circulation-commanded signal and there cannot be one under G-26 and D-052: the Pi
> commands ONE coil, the driver permissive, and nothing else. Do not look for that
> signal, do not wait for it, and do not treat its absence as a fault.**
>
> **What the operator does instead is C-23, in commissioning.md: look at the pump,
> confirm it is running, confirm it will still be running at the end of the window,
> and start the window only then. If the pump starts or stops mid-window the run is
> DISCARDED, not adjusted.**
>
> **The PHYSICS in this file is unaffected and stands: the settling clock counts
> CIRCULATING time and not wall-clock time, and if the loop stops, settling stops.
> That is the part DOSING established and it is why the operator condition exists at
> all. Only the mechanism for knowing it was wrong.** F-079.
>
> Body rewrite routed to DOSING. This banner is the safety fix and it is BOSS's.

Returned 2026-08-30. CONTROL-SOFTWARE answered what to do with the number, in
subsystems/control-software-f004.md. This is what the number is made of. Nothing
decided, nothing changed. DOSING reported stopped part-way.

## Every leg of the delay, in order

| # | Leg | Note |
|---|---|---|
| 1 | Head start-up, step command to first liquid motion, including the pump tube re-rounding after sitting occluded | PUMP-BOXES' domain, named because it is part of the interval |
| 2 | Delivery line dead volume, head to injection port | Near zero if the line is liquid-full: the incoming dose displaces an equal volume out the port at once. **If the line contains air or the head lost prime, the whole dead volume must be pushed first, and that can exceed a small dose entirely.** Then the dose lands nowhere and the check fails correctly. Differs per channel with run length |
| 3 | Manifold transport, injection port to outlet union F-04 | Internal volume downstream of THAT port over loop flow. Ports sit at different positions, so this differs per channel. Likely the smallest leg, and likely is not a number |
| 4 | Return drop back into the day tank | WATER's, an open drop. Fast, and it entrains air, which matters for reading the trace |
| 5 | **Tank mixing** | The dominant leg and the one that resists calculation. A small slug enters a large volume with NO mixer: agitation is only the bottom suction per G-11 and the return drop's plunge. Sub-mechanisms: dead zones in corners and below the suction inlet; short-circuiting if the return lands near the suction; density-driven sinking of dense concentrate or acid entering at the surface; thermal stratification from the chiller loop, which suppresses convection and makes stratification persist |
| 6 | Uptake at the submersible inlet | Concentration at the bottom inlet is not the tank average until mixing is done. Short-circuit gives an early unrepresentative high reading, a long path gives a late one. **First arrival is not the settled value** |
| 7 | Transport from tank inlet through the pump body, F-03, and up the vertical probe section | Volume over flow |
| 8 | Probe and circuit response | DISPLAY-BOX's number from the datasheets. Plus the temperature-compensation path: EC is temperature compensated, so if the PT-1000's own response lags, compensated EC keeps moving after true EC has settled. Flagged as a question for DISPLAY-BOX and CONTROL-SOFTWARE, not asserted |
| 9 | Number of loop passes to homogeneity | The reading does not settle on one transit. It approaches a final value over repeated turnovers until the remaining change is below probe noise |

**Two times fall out, and both are needed.**

- **t_first**, the earliest a real change can possibly appear. Reading before it
  is guaranteed flat, and a check that reads before it reports a healthy dose as
  a failure. This is the failure F-004 names.
- **t_settle**, when the reading has stopped changing within the probe's own noise
  band, so its MAGNITUDE can be compared against an expected step. This is what
  C-03 and C-04 need to mean anything.

Never sample before t_first. Never judge magnitude before t_settle.

**One wet-side constraint handed to CONTROL-SOFTWARE:** the settling clock counts
CIRCULATING time, not wall-clock time. If the loop stops, settling stops. The
timer must be gated on the circulation pump being commanded on, and per F-003
nothing can confirm it is actually running, so commanded-on is the best available
and its weakness is to be recorded rather than hidden.

> **THAT SENTENCE IS WITHDRAWN, 2026-09-03, D-105. THERE IS NO COMMANDED-ON SIGNAL.**
> It traces through control-software-f004.md to S-09 as first written, and S-09 as
> first written came from the owner's original project description, which D-052
> records verbatim as "That was loose." F-027, D-052 and G-26 killed it on
> 2026-08-30 and it survived here because nothing re-derived it. F-079, and the
> shape is G-37: a citation is not a source.
>
> **The constraint it was trying to express is real and survives: settling counts
> circulating time. The operator enforces it under C-23. Software cannot, and per
> G-36 that half is STRUCTURAL - it follows from G-26 - while whether the Pi can
> OBSERVE circulation is CURRENT and turns on S-20.**

## Derivable, or measured? Measured.

The derivation is worth doing only as a sanity bound, never as the number in
service.

Legs 2, 3, 4 and 7 are arithmetic, volume over flow, if the volumes and the flow
are known. They are not known: manifold diameter and port arrangement are open,
tubing is open, circulation flow at F-03 is owed by WATER, and F-05 and F-06 are
OPEN.

Leg 5 is where a derivation stops being trustworthy, for reasons specific to this
tank:

- **The tidy formula assumes a mixer this tank does not have.** Treating the tank
  as ideally stirred gives an exponential approach with a time constant of tank
  volume over loop flow, which assumes instantaneous perfect mixing. With only a
  bottom suction and a surface return, both failure directions are live at once:
  short-circuiting makes the first reading arrive too early and too high, dead
  zones make true settling far later than the formula. The two errors do not
  cancel and neither is small.
- **The formula's main input is the one number the system cannot know.** Day tank
  volume at dose time is a band, not a value, and per G-01 and G-02 the Pi has no
  level information beyond the fill-in-progress contact. Even a perfect
  derivation could not be evaluated at run time. Only a fixed conservative time
  can be applied, anchored to the slowest condition.
- **Density and temperature effects are invisible to volume over flow.**
  Concentrate and acid are denser than the tank contents and enter at the surface
  through an open drop. The chiller stratifies the tank.
- **The tank geometry is not established.** The parts table says 40 gal
  food-grade, open top, and nothing about shape. Shape drives dead zones. DOSING
  refused to assume one.

**Use the derivation this way and no other.** A settled reading cannot be faster
than one loop turnover and in practice needs several. If the measurement comes
back materially faster than one turnover, the measurement is not wrong about the
reading: it has found a short-circuit path from the return drop to the
submersible inlet, which is a real finding about the plumbing. That is the
derivation's whole value.

| Number the derivation needs | Who |
|---|---|
| Day tank working volume, high and low ends of the fill band | WATER, it owns the tank and the floats that set the band |
| Circulation flow actually through the manifold at F-03, measured against real restriction, not read off a pump curve | WATER. OPEN |
| Loop turnover time | C-07 |
| Manifold internal volume downstream of each injection port | DOSING, once diameter and ports settle |
| Delivery line internal volume per channel | DOSING, blocked on F-05 and F-06 |
| Return drop path and volume | WATER |
| Probe response time and EZO sampling or averaging | DISPLAY-BOX from the datasheets |
| Probe noise and drift band IN THIS LOOP with the pump running | Must be measured in situ. Datasheet noise is not this loop's noise: pump electrical noise, entrained air and the cable run all contribute. C-08 |
| Expected probe step per single dose, per channel | Owner, C-03 and C-04 |

## The procedure, with what the owner already owns

Nothing here needs a part he does not have.

**Preconditions.** Loop plumbed and running. Day tank at the HIGH end of its
normal band, the slowest condition, so the number is conservative. Circulation
running long enough that the trace is flat. All heads idle. No fill in progress,
since a fill both dilutes and changes level. Chiller in whatever state is normal,
and note which. Record level, temperature and time.

1. Start logging before anything happens, fastest rate the Pi will read,
   timestamped. Let it run quiet long enough to capture drift as well as noise.
2. **Establish the baseline band** from that quiet stretch: peak-to-peak spread
   with nothing happening. Everything afterwards is judged against this band.
   Without it no settling time means anything, because "stopped changing" is
   undefined. The most important step and the one most likely to be skipped.
3. Dose one channel alone, one that moves EC strongly, with a deliberately large
   single uninterrupted dose so the step sits far above the band. Record the
   command time exactly.
4. Read three things off the one trace:
   - **t_first**, the first sample that leaves the band AND KEEPS GOING. Not a
     single excursion: the return drop aerates the tank and a bubble past a probe
     makes a spike that looks exactly like an early arrival.
   - **Shape**: monotonic rise to a plateau, or overshoot and fall back? An
     overshoot is the signature of a slug reaching the probe before the tank is
     uniform, which is short-circuiting between the return drop and the
     submersible inlet. Worth knowing on its own.
   - **t_settle**, after which the reading no longer changes by more than the
     band, over a window at least as long as one loop turnover.
5. Repeat the identical dose several times, changing nothing. One run is not a
   settling time. **If runs disagree by more than the band, mixing is not
   repeatable and no fixed timer is safe.** Report that rather than averaging it
   away.
6. Repeat at the low end of the tank band, to see how much the number moves.
7. Repeat for the pH channels separately, on the pH probe. Different probe,
   different response, and pH into a buffered solution behaves nothing like EC
   into water. pH up and pH down separately, never together: S-16 makes a batch
   firing both a fault and it would make the measurement meaningless too.
8. Repeat with the smallest dose a real recipe uses. If that step does not clear
   the band at all, that channel at that dose size is not verifiable at any
   settling time. That is a legitimate answer and it needs recording, not fixing.
9. One run with the chiller in its cycling state if that is normal, to see whether
   temperature movement rides into the EC trace.
10. Record everything against tank level, dose size, channel, temperature and date.

**Two honest notes.** A test dose is real nutrient into a real tank: the G-05
arithmetic must be told, and the chemistry changes. First runs on plain water are
safer and establish the method and the transport legs, but the numbers used in
service should be confirmed in the real solution at the real level, because
buffering and density both differ.

## One number or many

Not one number.

| Axis | Why |
|---|---|
| Per channel, for t_first | Delivery line lengths differ, the heads sit in two boxes at different distances, and the ports sit at different positions. Probably small next to mixing, and probably is why they get measured rather than assumed |
| Per channel, second and bigger reason | Different products, densities and chemistry. The pH channels settle differently because both probe and response differ, and a buffered solution moves non-linearly. Fulvic has no usable signal and stays that way per D-013 |
| Per dose size, for t_first | A larger dose crosses the band sooner, a small dose crosses later or never |
| Per dose size for the USABLE t_settle | What matters is when the remaining change drops below the band. A small step gets there sooner in absolute terms, or is invisible from the start |
| Per tank level | A band, not a number, and software cannot see it |

Two shapes are available and the choice belongs to CONTROL-SOFTWARE and the
owner: one conservative worst-case gate applied to everything, at the cost of
materially longer batches, or per-channel numbers with the small-dose cases
marked unverifiable. Either way the per-channel measurements have to exist first.

## What makes the number change later

- **Tank level.** Changes continuously in service and the Pi cannot see it. Take
  the number at the slowest condition. A number taken at the fastest is wrong
  forever and always in the unsafe direction.
- **Circulation flow degrading.** Fouled impeller or intake screen, biofilm or
  scale in the manifold, a valve knocked partly shut. Flow falls, settling
  lengthens. **And nothing in this system measures flow**, by choice: D-007
  closed S-13 and G-04 forbids meters. The settling number's dominant input is
  the one thing the design cannot observe. DOSING calls this the most important
  line in the section and BOSS agrees.
- **Probe ageing.** A fouled bulb or coated cell slows the response and widens the
  band, so a check calibrated at commissioning slowly becomes a false-fail
  generator. No probe calibration or cleaning interval exists anywhere on file.
  Logged as findings F-007.
- **Temperature and the chiller.** Viscosity, compensated EC, and thermal
  stratification that changes mixing. See S-18.
- **Any physical work in the room.** Manifold diameter or port positions, tubing
  runs, the return drop's landing point, the submersible's position in the tank.
  The return-versus-suction geometry changes short-circuiting more than anything
  else here, and it can be changed by someone tidying a cord.
- **A product or recipe change.** Different density, EC and pH response,
  detectability.
- **Anything added to the loop later**: a filter, more plants served, a second
  manifold.

The re-measure trigger is therefore an event list, not a calendar. It is written
into commissioning.md.
