# Commissioning list

Measurements that must be made against real parts, on this build, by the owner.
None of these may come from a datasheet or from any agent's memory. A figure
that arrives without a measurement behind it is not a figure.

BOSS owns this file. An agent that needs a number it cannot derive adds a row
here through BOSS rather than assuming one.

**C-09 IS FIRST.** D-022. Nothing below it is worth measuring until channel N is
proven to be what the wall says it is. A measurement taken against a mislabelled
channel is not a wrong number, it is a right number filed against the wrong
thing, and every later check confirms it.

| # | Measurement | Why it is needed | Who measures | Blocked on |
|---|---|---|---|---|
| C-01 | Delivered volume per head, per unit time and per step | Steps per millilitre. Nothing in the system measures delivered volume, so a wrong figure is invisible. G-04 | Owner | Heads mounted, tubing chosen |
| C-02 | Settling time for the tank-read verifications, as TWO numbers: t_first and t_settle | F-004. A check read too early reports a healthy dose as a failure. Must be measured, not derived: the tank has no mixer and both short-circuiting and dead zones are live at once | Owner. Full procedure in subsystems/dosing-f004-wet-side.md | Day tank filled at the HIGH end of the band, circulation running, **chiller in its D-023 held-off state, not its cycling state** |
| C-03 | pH step per single dose, pH up and pH down separately | S-16. The attribution must exceed probe noise and drift to mean anything | Owner | C-08, then C-02. NOT the other way round, see the ordering note below |
| C-04 | EC step per single dose, per EC-moving channel | S-15. Same reason as C-03 | Owner | C-08, then C-02. See the ordering note below |
| C-05 | Head discharge pressure against a flowing manifold | Only needed if a pressure-based option is ever chosen. Not currently needed | Owner | Not scheduled |
| C-06 | Whether the head holds against back-siphon with the jug above the inlet | Decides whether flooded suction is safe, and whether an anti-siphon device is required | Owner, with PUMP-BOXES stating what the head is | Jug placement |
| C-07 | Loop turnover time, day tank through manifold and back | Feeds C-02 as a FLOOR only. One turnover is not mixing to homogeneity, and the multiplier between them is a property of this tank's mixing that no agent will quote | Owner or derived by WATER from tank volume and circulation flow | Loop plumbed |
| C-08 | pH and EC noise and drift band ON THIS BUILD, measured in situ with the circulation pump running and **the chiller in its D-023 held-off state**, over a window at least as long as the settling interval | Added 2026-08-30. C-03 and C-04 both require a band to compare against and nothing scheduled it. Without it a measured change cannot be turned into a verdict, only into a timer. It cannot come from a datasheet: pump electrical noise, entrained air and the cable run all contribute, and datasheet noise is not this loop's noise. Found INDEPENDENTLY by CONTROL-SOFTWARE and by DOSING, both reading this file. Not found by BOSS | Owner | Probes live, loop circulating, no dose in flight |
| C-10 | Circulation flow at F-03, under SERVICE conditions, by catch and time at the return drop | Added 2026-08-30. C-07 presupposes a flow number and NO ROW PRODUCED ONE. Found by WATER reading this file in full, the same shape as the C-08 gap. A pump curve cannot supply it: the operating point is where the curve meets a system curve whose every term is open | Owner. Method in subsystems/water-s18-f003.md, including the failure modes that decide whether the number is real: do not lift the hose, keep the catch short, repeat at both ends of the fill band | Loop plumbed as built, valves in service positions |
| C-11 | Day tank working volume and the actual fill band: both ends, with the reason for each | Added 2026-08-30. DOSING's derivation needs it and names WATER as the source. Nothing scheduled it. The 40 gal on the parts list is nominal vessel capacity, not a working volume, and must not be used as one. The low end is a MEASUREMENT-QUALITY limit as well as a pump limit: a vortex draws air into the loop and air past a probe makes the spike that looks like an early arrival | Owner, with WATER stating what sets each end | Tank as built, floats chosen and set, transfer chain live for the surge measurement |
| C-12 | The W-1 transient: magnitude and timing of the PT-1000 step when the pump starts after a rest, with the standing probe-section column at room temperature and the tank chilled | Added 2026-08-30. W-1 is the free witness for F-003 and it is unusable without this. It is also the only F-003 option that costs nothing and adds nothing | Owner | Loop running, chiller in service, after a rest interval |
| C-09 | End-to-end channel trace. Command one channel alone, confirm by eye which head turns, which tube moves, which jug's level drops, and which product | Interface S-19. It is the ONLY check that catches a build-time labelling error or a numbering disagreement between software, wiring, head and jug, and those pass every other check in the system. Free, needs no hardware, and with translucent tubing needs no disassembly. Possible only because G-06 serialises the heads | Owner | Loop running, tokens applied. Repeat after ANY rewiring or renumbering |

Not on this list, deliberately: anything that can be read off a datasheet the
owner pastes in. This file is only for what the build itself has to tell us.

## Ordering note, C-02 against C-03, C-04 and C-08

The blocked-on column originally made C-03 and C-04 wait on C-02, which is
circular: measuring the settling time needs a dose whose signal is visible, and
knowing whether a signal is visible needs a band. DOSING caught it. The order is:

1. C-08 first. The baseline band, with nothing happening.
2. C-02 next, using a deliberately OVERSIZED single dose chosen for the clearest
   signal, so timing is read off a trace that is unambiguous.
3. C-03 and C-04 last, at real dose sizes, using the timing established in step 2.

Timing first with a big dose, magnitudes second with real ones.

## Re-measure triggers

No figure in this file is permanent. C-02 in particular has a dominant input that
this system cannot observe by choice: circulation flow. D-007 closed S-13 and
G-04 forbids meters, so flow degradation from a fouled impeller, an intake
screen, biofilm or scale is invisible, and it lengthens the settling time
silently.

Re-measure on any of these events, not on a calendar alone:

| Event | What to re-measure |
|---|---|
| Any plumbing change: manifold, ports, tubing runs, the return drop's landing point, the submersible's position in the tank | C-02, C-07. The return-versus-suction geometry changes short-circuiting more than anything else, and it can be changed by someone tidying a cord |
| Pump or impeller service, or any suspicion of reduced flow | C-02, C-07 |
| Probe replacement, recalibration or cleaning | C-08, then C-03 and C-04 |
| A product or recipe change | C-03, C-04. Different density and response, different detectability |
| Anything added to the loop: a filter, more plants served, a second manifold | C-02, C-07 |
| Any rewiring or renumbering of channels | C-09 |
| Periodically, to catch fouling before it is a false-fail generator | C-02, C-08, C-10 |
| A driver replaced, where the driver's step configuration is part of what PUMP-BOXES sets | **C-01 for that channel is VOID until re-measured.** CONTROL-SOFTWARE will not carry a steps-per-millilitre figure across a driver change on the assumption that the configuration was reproduced. Plus C-09 |

## Chiller state is part of the measurement condition

D-023 holds the chiller off across settle windows, so held-off is the NORMAL state
during a window. C-08 and C-02 must therefore be measured with the chiller held
off. Measured in its cycling state they would be measured under conditions that
will never occur in service. Found by WATER; C-08 did not name a chiller state at
all.
