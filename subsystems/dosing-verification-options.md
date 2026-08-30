# Per-channel dose verification: options returned by DOSING

Answer to findings.md F-001, returned 2026-08-30. Nothing here is decided,
chosen, added or built. No part number, size, count or price appears in it.
Read findings.md F-001 and decisions.md D-010 first.

## What DOSING did not answer, and why

F-001 limit 1, nothing verifies anything at rest, is about the circulation
submersible sitting dead between batches. That pump is WATER's device on a
MAIN-PANEL relay and is not on DOSING's path. Limit 1 is unrouted. BOSS owns
routing it.

DOSING answered limits 2 and 3: which of the eight heads delivered, and the
channels EC cannot see.

## The failure set on DOSING's path

| # | Failure | Owner |
|---|---|---|
| a | Motor did not turn | PUMP-BOXES, not DOSING |
| b | Head turned, pump tube collapsed, worn or burst | PUMP-BOXES owns the head, DOSING owns the tube approaching it |
| c | Suction line kinked, collapsed or blocked | DOSING |
| d | Jug dry | DOSING |
| e | Suction line out of the liquid, drawing air | DOSING |
| f | Delivery line off, split, or dosing onto the floor | DOSING |
| g | Injection port blocked or check stuck shut, head deadheads | DOSING |
| h | Siphon or backflow delivering when not commanded | DOSING |
| i | Wrong jug on the wrong channel after a jug change | DOSING |

Failure i is recorded separately as findings.md F-002. It produces the exact
F-001 symptom and no flow-measuring option catches it.

## Two structural facts that decide most of the costing

**Discharge side versus suction side.** Anything between the pump box lid and an
injection port costs wall space and pushes the manifold and the pump boxes
apart, which is M-02 and INTERCONNECT arbitrates. It adds nothing to a jug
change. Anything between the lid and the jug sits in the space the operator's
arms occupy during a jug change and must be broken or re-primed every time.

**G-06 is a verification asset.** Only one head turns at a time is already
mandatory, so any single measurement anywhere is automatically attributable to a
channel. Several options below cost one device instead of eight for that reason
alone.

## Zones

| Zone | What |
|---|---|
| Z1 | Manifold body between the unions, probe section first, ports downstream. Nothing added here |
| Z2 | Dose delivery run, pump box lid through C-05 to the injection ports |
| Z3 | Head suction run, lid down to the jugs |
| Z4 | Jug standing area, not yet placed |
| Z5 | Operator standing position for a jug change. Every visual option must be readable from here or it will not be read |

## Tier 0: no money, no hardware in the wet path

| ID | Option | Catches | Misses | Cost and consequence | Crossing |
|---|---|---|---|---|---|
| O-01 | Time-slice the doses and read the probes that already exist. One channel, wait a loop turnover, read, next | b c d e f g for any channel whose product moves a probe. pH attributes pH up and pH down | i entirely. Fulvic. Any dose under probe noise | Money none, plumbing none. Batches get materially longer. A batch aborted mid-sequence is unmeasurable per G-04 | CONTROL-SOFTWARE owns the sequencing and the settle timer. Extending S-15 is BOSS's call |
| O-02 | Operator-commanded single-channel test or purge, watched | b to g by eye | i unless the operator knows which jug should move | Money none. A test purge injects nutrient the arithmetic must book | CONTROL-SOFTWARE owns the UI command |
| O-03 | Choose translucent tubing where a compatible option exists, turning the whole path into a sight glass | c d e f h by eye | a b g i | Money likely nil, tubing is bought either way. Prerequisite for O-04, O-05, O-06, O-14. Light can grow algae in some products | none |
| O-04 | Place jugs, suction feet and dose lines in the operator's sightline from Z5 | d e, partially c f | a b g i | Money none. Competes with shortest run and with M-02 wall space | M-02, INTERCONNECT |
| O-05 | Flooded suction, jug liquid level above the head inlet, so air in a line is unambiguously a fault | c d e h, self-announcing between visits | a b g i | Money none for the geometry. Makes the siphon question load-bearing. Siphoning delivers uncommanded nutrient, a worse failure than the one detected. A raised jug is heavier to lift | PUMP-BOXES returns whether the head holds against back-siphon |
| O-06 | Watch the prime at every jug change | a b c d e at jug-change frequency | Nothing between changes | Money none. Work the operator does anyway | CONTROL-SOFTWARE if the prime is commanded from the UI |
| O-07 | Reconcile the jug against the booked remainder at every jug change, by scale | a to h cumulatively, i after the fact. One jug of latency | Nothing quickly | Money none if a scale is owned. The only option that directly tests the G-05 arithmetic. Largest Tier 0 addition to a jug change | CONTROL-SOFTWARE must display the booked figure |
| O-08 | Marked or graduated translucent jugs read every batch | Same set as O-07, faster and coarser | | Money trivial. A mark that reads plausibly when wrong | none |
| O-09 | Channel identity carried at all three ends: head, both tube ends, jug | i, at the moment of the change | Everything else | Money trivial. The only Tier 0 option that touches i. A faded label is worse than none, it looks done | PUMP-BOXES for head marking, CONTROL-SOFTWARE for the channel numbering |
| O-10 | Route the wet path so a rupture drips on sensed floor and drops the permissive | f, and only a wet f | A stalled or deadheaded channel is silent | Money none. A nuisance trip stops a batch mid-dose, which G-04 makes unmeasurable afterwards | WATER places the sensors, MAIN-PANEL owns the console |

Search terms returned: conductivity step response verification chemical dosing;
single channel dose sequencing; chemically resistant translucent flexible
tubing; tubing chemical compatibility chart; anti-siphon valve chemical
injection; flooded suction dosing pump; digital platform scale; drawdown
reconciliation chemical metering; chemical resistant graduated label tape;
translucent carboy level strip; chemical resistant wire marker; solvent
resistant label tape.

## Tier 1: small money, wet-path hardware, no wire and no software

| ID | Option | Catches | Cost and consequence | Lands |
|---|---|---|---|---|
| O-11 | Keyed or uniquely coded couplings on the suction side | i, by prevention | One coupling pair per channel. Two new wetted separations per suction line, on the side broken most often. A coupling is a leak and an air-ingress point, and air ingress is what O-05 exists to make visible. Materially improves the jug change, the best option on that axis | Z3 at the jug end, Z4 |
| O-12 | Tracer dye in a channel | b to g for the dyed channel | Recorded for completeness, not recommended by DOSING. Contaminates a nutrient, unknown effect on the pH and EC readings O-01 depends on, unknown effect downstream of V3 which is out of scope. Must be re-added at every jug change | Z4 |
| O-13 | Clear witness section or drip chamber on each dose line at the injection port | b to f while a dose runs, per channel | One part and two wetted joints per dose line. May trap an air pocket that then travels to the port. Nothing at a jug change | Z2, lengthens the run, M-02 consequence |
| O-14 | Mechanical inline sight flow indicator per dose line | b to f while a dose runs | One per channel, two wetted joints. Void if head output is below the indicator's threshold, which is a datasheet number against a measured number, neither available. A stuck indicator reads flow on a dead channel | Z2, plus an orientation constraint |
| O-15 | Draw-down column and valve teed into each suction line | a to h quantitatively, per channel, no power. Doubles as the steps-per-millilitre calibration jig CONTROL-SOFTWARE already needs | Highest Tier 1 money and the most complex plumbing: a tee, a valve and a column on the suction side of every channel, which must hold vacuum without drawing air. A valve left wrong starves a head mid-batch, causing the very failure being detected. Worst jug-change burden of any option, it sits in the operator's working space and every change re-primes through it | Z3 and Z4, vertical, competing with the space a jug is lifted through |

Search terms returned: keyed quick disconnect coupling chemical; colour coded
tube coupling non-spill; food safe tracer dye fertigation; inline sight glass
barbed fitting; drip chamber tubing; inline sight flow indicator low flow; ball
type flow indicator barbed; chemical injection drawdown calibration column;
calibration cylinder metering pump.

## Tier 2: money, wire and software

Every option here needs a signal path off the wet path. DOSING owns no wire.
Each drags in INTERCONNECT for the run, DISPLAY-BOX for the input and the S-12
map, and CONTROL-SOFTWARE for what the reading means. Each contradicts D-010 as
recorded, and two contradict G-04 or G-05. Any of them is a BOSS decision
reversing a recorded one, not a DOSING change.

| ID | Option | Catches | Honest cost |
|---|---|---|---|
| O-16 | One weigh platform under all the jugs. Possible only because G-06 serialises the heads, so one mass reading attributes to the running channel | a to h quantitatively, per channel, unattended. Closes the G-05 books-versus-reality gap continuously. Misses i on a single shared platform | One device, one signal path, zero wetted joints, its strongest feature. Binding constraint is resolution against tare: a single smallest dose must be visible against the mass of every full jug on the platform, and DOSING will not guess that ratio. A hand on a jug, a line tugging, a jug half-on, thermal drift all produce false verdicts rather than missing ones. Fixes all eight jugs to one surface, foreclosing the layout freedom O-04 and O-05 need. Measures the shelf not the jug, so whether it violates G-05 is BOSS's ruling |
| O-17 | Non-invasive clamp-on air-in-line or drop detection per channel | c d e on the suction side; b c d e f on the discharge side if it resolves the pulse. A stalled head with a full line reads liquid and passes. Misses g h i | Zero wetted joints, cannot leak or contaminate. Eight devices, eight runs, eight inputs on a logic board whose map is not frozen. A clouded or algaed tube gives a false pass or false alarm. On the suction side it must be unclipped at a jug change |
| O-18 | Pressure switch per dose line, dry contact when the head pushes against the manifold | a b c g, partially d. Yes/no, not a volume. Misses h i | Two wetted joints per line in the pressurised section. A switch that latches closed reports a healthy channel forever, the failure mode that makes a verification worse than none. Needs the head's real discharge pressure, which the owner must measure |
| O-19 | A flow meter on every dosing line. The option the owner expects to decline. Forbidden by G-04 in four files | a to h per channel, quantitatively, unattended, all eight channels including fulvic, without depending on a probe response, an operator's eye or a settle gap. **Misses i**: eight healthy readings are fully consistent with two jugs swapped | Most expensive line by a wide margin: eight devices plus cable plus eight inputs. Sixteen new leak paths in a system where a leak drops the permissive per G-08. Orientation and straight-run constraints per device, lengthening Z2 and forcing the greatest manifold-to-box spacing on the wall, M-02, with eight signal cables along the wettest run, INTERCONNECT's separation problem. A meter reading zero on a healthy channel stops batches for nothing; a scaled rotor over-reports and silently under-doses, which is F-001 with a green light on top. Eight calibrations that must each be verified against a physical measurement the owner performs anyway, so O-15's calibration work is added to, not avoided. Clamp-on ultrasonic is the only variant with no wetted joints and the most likely to fall below its sensing range on a small pulsed line |

DOSING neither advocated for nor against O-19. It is the only option that answers
the question completely and the most expensive in every column.

Search terms returned: platform scale digital output; load cell platform serial
output; clamp on optical liquid detection tube; air in line bubble detector
non-invasive; drop counter sensor; low pressure switch dry contact chemically
compatible; adjustable pressure switch barbed; low flow oval gear flow meter
chemical; micro flow meter pulse output; clamp on ultrasonic flow meter small
bore.

## Considered and dropped, with the reason

| Idea | Why dropped |
|---|---|
| Move a probe downstream of the injection points so it reads the result rather than the tank | G-10 freezes probes first in line ahead of every injection point. DOSING was told to change nothing about the manifold. Named and dropped, not evaluated |
| A sight window in the pump box lid, or motor stall detection in the driver | Head, lid and driver are PUMP-BOXES. Whether the 6121 breakouts can detect a stall is a datasheet question for them. Note: neither reaches the wet path. A head that turns perfectly with a collapsed tube or a dry jug is failure b, c or d, and rotation sensing passes it |
| Temperature as a third attribution channel | Whether a dose moves temperature measurably is a number nobody has established. DOSING would not expect it to and refused to assert it |
| Jug volume as a verification lever | Not an option, a consequence. Jug volume is undecided and it sets how long a silent divergence can run before O-07 or O-08 surfaces it |

## Numbers needed before any of this narrows, and who returns each

| Number | Who |
|---|---|
| Head discharge barb form and OD, F-05 and F-06 | PUMP-BOXES, currently blocking |
| Actual delivered volume per head, per unit time and per step | The owner measures. Must not come from a datasheet |
| Head suction lift, and whether the head holds against back-siphon | PUMP-BOXES from the head |
| Loop volume and turnover time through the manifold | WATER, from circulation flow at F-03 and the day tank |
| Probe resolution, noise and drift | DISPLAY-BOX from the EZO datasheets |
| Probe step per single-channel dose, per channel | The owner measures, dosing one channel alone into the running loop |
| Chemical compatibility per product | The owner, from the labels of the products he has |
| Smallest dose mass and total full-jug mass | The owner, once jug volume and dose sizes are chosen |
| Where the leak sensors sit | WATER |

## Status

DOSING reported stopped part-way and did not declare itself finished. Nothing is
decided, nothing is added, no file it owns was changed. Several options are
blocked on F-05 and F-06, which are OPEN.
