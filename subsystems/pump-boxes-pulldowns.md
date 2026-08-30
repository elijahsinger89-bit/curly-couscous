# PUMP-BOXES on the STEP and DIR pull-downs, D-043

Returned 2026-08-30. No file changed. Stopped part-way. It re-read the tree first
and states it was on stale ground; it **accepts D-031 and D-032 and records that its
option B is not taken and its EN position is overruled**, noting that F-015 was its
own finding used against it correctly.

## The value: not statable, and the bounding matters more than the number

**Four bounds squeeze it and only two are in a datasheet.**

1. **Too large:** fails to hold the pin down against input leakage, or against an
   internal pull-up as a divider. Datasheet.
2. **Too large again, and no datasheet can close it.** F-018's actual threat is not
   leakage, it is **coupled noise from 24 V motor conductors at 1.0 A**. Coupled
   current is a property of this cable, this run and this routing, none of which is
   chosen. **The datasheet bounds this value and the INSTALLATION decides it.** So
   sit well inside the bound rather than at it, and verify by measurement.
3. **Too small:** sixteen pull-downs are a DC load on DISPLAY-BOX's outputs whenever
   a line is driven high.
4. **Too small again, and this one is new.** See the short case below.

**The single most load-bearing datasheet fact: whether the chip has an internal pull
on STEP and DIR, and in which sense.** An internal pull-UP makes the external
pull-down a divider against a stated resistance and changes the value by orders of
magnitude. An internal pull-DOWN may satisfy D-043 already, leaving only the
question of whether it is strong enough against F-018's coupled noise. **And the
board schematic half cannot be substituted: if the 6121 fits pull-UPS, the fix is
not a bigger resistor, it is a different fix.**

## The interaction nobody had stated: two agents own one divider

F-020 requires DISPLAY-BOX to fit **series current limiting** on STEP and DIR.
D-043 requires PUMP-BOXES to fit a **pull-down** at the other end of the same
conductor.

> **A series resistor at one end and a pull-down at the other IS A VOLTAGE DIVIDER.**
> The driver input must still see V_IH after it, across 4 ft or 6 ft. **Neither value
> can be chosen independently of the other, and each is currently assigned to a
> different agent on opposite sides of a gland, with no row saying they interact.**

**T-015's shape in miniature: two individually plausible, individually small fixes,
each correct in isolation, that fail together.** Both values must be settled in one
calculation, by one agent, in one sitting, and both ends record the same working.

**A third term in the same divider:** the RC formed by the pull-down against cable
plus input capacitance slows the STEP falling edge, and that budget tightens as the
microstep factor rises because step frequency rises with it. **So C-17 is an input
to this resistor value, and the resistor value is an input to whether a given
microstep factor is deliverable over 6 ft.** Three-way coupling.

## G-22's second question, asked of the fix itself, and DIR does not survive it

Two candidate adjacent rails, and a pull-down helps against neither:

- **Short to 5 V:** the line is held permanently high, and the pull-down becomes a
  standing DC load across that rail. **A second lower bound nobody had: too small a
  pull-down turns one short-to-VDD into exactly the brownout F-020 names, the
  pump-box fault that reaches 6 ft up the cable and takes down the Pi that D-031
  kept alive on purpose.** The fix that closes G-22's first question sizes the
  severity of a hazard already on file for the second.
- **Short to a 24 V motor conductor:** not a wrong logic level but an overvoltage
  into a CMOS input on a non-isolated part. **A destruction case, and it bears on
  whether STEP and DIR may share a jacket with VM at all.**

**And the hard conclusion, which needs no datasheet figure:**

> A pull-down defines DIR as LOW when severed. A short to the 5 V conductor defines
> DIR as HIGH. **Those are necessarily opposite. Whichever rotation is safe, exactly
> one of G-22's two failures produces the other rotation** - the backwards-running
> head that S-10 calls the worst outcome in the sweep.
>
> **THEREFORE DIR CANNOT BE MADE FAIL-SAFE AGAINST BOTH G-22 QUESTIONS BY ANY
> RESISTOR AT THE DRIVER END.** D-043's fix closes the severed case and is
> structurally incapable of closing the short case.

Two ways out, neither PUMP-BOXES' to choose: close the short case by **cable
construction**, keeping the 5 V VDD and the 24 V motor conductors out of adjacency
with DIR or placing a grounded conductor beside it; **or record it as an accepted
residual, which G-22 calls a defect rather than a tolerance and so needs an owner's
ruling, not an agent's silence.**

## D-043 says "pull-down", and whether DOWN is the safe direction is not known

For STEP it is unambiguous: a static level is not a clock, so low is the
non-clocking state whichever edge the part triggers on.

**For DIR, nobody knows whether down is safe.** The chain has three links and only
one is a datasheet: which DIR level gives which rotation, chip datasheet; which
rotation gives which flow through the KPHM400-ST **as mounted**, Kamoer, and it
depends on head orientation which is still open with DOSING; and which flow
direction is safe, DOSING's.

**If DIR low turns out to be the direction that draws from the manifold toward the
jug, then a pull-down on DIR is fail-UNSAFE and D-043's own wording needs
revisiting.** PUMP-BOXES did not substitute a pull-up on its own initiative,
because that would be changing an owner ruling on the strength of a guess.

## Where it physically lands

**The obvious answer is ruled out by traps.md, not by judgement.** A resistor lead
jammed into the driver's own screw terminal alongside the field conductor: T-009 and
T-010. **A clamp sized for stranded field wire, asked to retain a thin solid lead
and that wire, compresses the stranded one and lets the lead back out. And the
failure mode is the exact failure the part was installed to prevent** - a
backed-out pull-down leaves a floating input on an enabled driver, nothing
indicates it, the box looks correctly built, and nothing downstream measures
direction or delivery. **Silent and self-confirming.** It is also disturbed on every
driver change.

**So the pull-downs do not land in the driver's own terminals.** That is stated as a
conclusion rather than an option.

| Option | For | Against |
|---|---|---|
| **A. A terminal landing field on the box wall**, resistors across it, short jumpers to the drivers | One defined landing per signal. Resistors on a screw-retained field rather than in a clamp shared with field wire. **A driver swap unlands the jumper, not the pull.** The common GND rail gives the box one defined return point, serving T-007 and T-015 directly. No fabrication, no lead time | **Doubles the landing count per signal**, which is T-008 and T-010 territory and must be counted honestly. Consumes wall area. A bare lead in a strip clamp is still a lead in a clamp unless the block accepts a component or the leads are ferruled |
| **B. One small carrier board per box** | Soldered joints cannot back out, so the silent-floating mode is gone. Nothing disturbed by a driver change. One place to also carry F-020's mitigation and the DIR segregation. **One defined ground reference point, the direct answer to T-015's two-returns-on-one-pin** | A fabricated part, design time, lead time, one more thing to get wrong. Over-solution if the breakout already fits the pulls |

**The decision rule: count the components that end up at the driver end, per input.
One per input and Option A is credible. More than one - which happens if F-020's
series limiting or the DIR short-case mitigation also lands there - and a terminal
strip stops being credible and it is Option B.** Nobody can count that yet.

Two dependencies that keep this open regardless of the datasheet: **there is no
internal layout to land anything in** (the lid penetrations are open, the four motor
bodies hang from wherever they land and are the dominant obstruction and heat
source, and free wall area is what is left after them, which is unknown), and
**anything added must not block airflow around four driver heatsinks in a sealed box
whose rise C-15 has not measured.**

Derivable now and constraining: **it mounts to the box BODY, not the lid.** The
motor body is inside and the head outside, so the lid is a heavy serviceable
assembly carrying four motors, removed as a unit. Anything on it moves with it and
drags wiring.

**Recommendation, as a recommendation: hold at Option A unless the component count
per input exceeds one, and read the board schematic before assuming any of it is
needed at all. If the 6121 already fits adequate pull-downs this may cost nothing,
and if it fits pull-ups the fix is not this fix.**

## What PUMP-BOXES owes others

- **DISPLAY-BOX and BOSS:** the divider across the gland. Settle both values
  together, record the same working at both ends.
- **INTERCONNECT and BOSS:** DIR's short case cannot be closed by any resistor at
  the driver end. Cable construction, or an owner's ruling on an accepted residual.
- **DOSING:** which rotation is safe, which needs head orientation as mounted.
- **CONTROL-SOFTWARE, one flag:** a severed DIR is undetectable by software, nothing
  measures direction, and G-04 measures nothing at all. **The resting direction is
  now a hardware property, so parts.md's standing rule gains a new instance: the
  direction COMMANDED is not evidence of the direction that HAPPENED.**
- **BOSS, a candidate commissioning row:** lift each STEP and DIR conductor at the
  display end and confirm with a meter that the driver terminal actually sits below
  V_IL. Sixteen measurements, cheap, per-driver because the part is per-driver. Now
  C-21.
