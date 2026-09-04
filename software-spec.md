# Document 12: The Software Specification

The Pi application for the fertigation skid. Written by CONTROL-SOFTWARE
2026-09-02 under D-094, which names this document as the first real output of the
project.

**This is a specification, not code.** It states what the application must do,
must not do, and may not yet do. It is written so that a person who has read none
of the surrounding conversation can implement it, and so that a person auditing an
implementation can check it line by line.

**No figure in this document was invented.** Where a number is required, the
document names the number and where it comes from - a commissioning row, an owner
input, or a subsystem return. Section 10 is the complete list. A specification
carrying an invented figure is worse than one carrying a hole, because nothing in
this system measures delivered volume and a wrong number stays invisible until
plants die.

Status is stated at the end, in section 12. It is not "finished".

---

## 1. Scope

### 1.1 What this document specifies

The Raspberry Pi application, and only the application:

- The channel model and the token, of which this application is the definitional
  end (S-19, D-021).
- Dose planning, plan admission, sequencing and step commanding for eight
  channels.
- Booking dispensed volume and computing jug remainder (G-04, G-05).
- Commanding the driver permissive coil and evaluating its readback (G-09, S-07,
  S-08).
- Reading the three EZO process circuits: pH, EC, temperature.
- The verification model built on those readings (S-15, S-16, S-17).
- The fault model: what raises each fault, what it stops, what clears it.
- Durable state, its write ordering, and recovery across a power event or a
  watchdog reset.
- What a fault or a record REQUIRES of a screen. Nothing more about screens.

### 1.2 What is explicitly NOT in this document

| Not here | Why, and who owns it |
|---|---|
| Any Pi pin, any I2C address | S-12 is OPEN. DISPLAY-BOX proposes, BOSS freezes. Nothing may be built against an OPEN row (agents.md 9) |
| Any library, language, framework, or how the application is hosted | Not chosen. Section 11 |
| Any timing figure, settling time, sample rate, debounce length, steps-per-millilitre figure or part specification | Every one is a measurement that does not exist yet. Section 10 names each and its source |
| **The touch UI** | HELD by the owner, deliberately, because the fault model is still moving and he will not have a UI designed against a moving target (agents.md, "Held, by the owner"). This document states what a fault or a record REQUIRES of a screen and goes no further. No screens, no layout, no navigation, no controls beyond the requirement that certain actions must not exist |
| Anything electrical: levels, pull resistors, wetting circuits, conductor selection, glands | DISPLAY-BOX, MAIN-PANEL, PUMP-BOXES, INTERCONNECT. This application ends at the GPIO and I2C map (S-12) |
| Safety | Safety is the hardwired permissive chain (G-07, G-13). Software neither causes nor prevents a drop. No statement in this document may be read as a safety function |
| Level control, fill logic, transfer, circulation, chiller | Hardware. The panel runs without the Pi (G-26, D-052). See section 4.3 |
| Anything downstream of V3 | Out of project scope (D-001) |
| The five unassigned products | Deliberately unassigned until commissioning (D-077). C-09 binds a token to a product, with the jugs present. No product name appears in this document |

### 1.3 The document this one supersedes and does not discard

`subsystems/control-software-f004.md` and `subsystems/control-software-p09.md` are
this application's two prior returns. **As deliverables they are superseded by this
document.** As reasoning they stand: they carry the argument behind several rules
restated here, and where this document states a rule without its argument, the
argument is there. Two things in them are now WRONG and are corrected here:

- The f004 window-validity precondition ("the Pi commands the circulation relay,
  so it can require circulation commanded on") **has no source.** F-070, from
  G-26 and D-052. See section 6.4.
- The f004 and p09 treatment of P-09 as blocking is superseded: **P-09 is closed
  by measurement, C-18, D-093.** The fault model proceeds.

---

## 2. The frozen rules, restated as implementation constraints

**A reader must not have to open decisions.md to know what they may not do.** Each
constraint below is written as an instruction to the implementer. The trace number
is alongside so it can be checked against the source, not so it has to be.

### 2.1 Constraints on dosing and delivery

| # | Constraint | Trace |
|---|---|---|
| 2.1.1 | **Nothing measures delivered volume.** A dose is a commanded step count and a booked volume. Do not write, and do not leave room for, any code that assumes delivery feedback exists | G-04 |
| 2.1.2 | **There is no flow signal into the Pi anywhere.** No code may wait on one, poll one, time out against one, or hold a variable for one | D-007, S-13 |
| 2.1.3 | **Jug remaining volume is arithmetic only**, per channel, against a full-jug volume the operator enters. There are no jug sensors and none may be assumed | G-05 |
| 2.1.4 | **The volume the arithmetic runs on is WHAT WAS POURED.** It is not a container's capacity and it is not a configuration default. These are three different quantities and they are never one field | G-33, D-086, T-018 |
| 2.1.5 | **Exactly one dosing head turns at a time.** This is a thermal constraint, not a control preference, and it is mandatory until C-15 says otherwise. The sequencer serialises; there is no parallel path, not even one that is disabled | G-06, C-15 |
| 2.1.6 | **Dose arithmetic converts against the MEASURED delivery figure from C-01**, measured against real back pressure into the running manifold, never against a manufacturer's no-back-pressure figure | C-01, parts.md |
| 2.1.7 | **Steps per millilitre is derived, never stored as a typed constant**: motor steps per revolution, times the microstep factor recorded at C-17, divided by the millilitres per revolution measured at C-01. All three terms are recorded inputs. Do not assume the microstep factor; no file states one | C-17, C-01, T-012 |
| 2.1.8 | **A driver replacement voids C-01 for that channel.** The application will not carry a steps-per-millilitre figure across a driver change on the assumption that the configuration was reproduced. A voided figure blocks commanding that channel | commissioning re-measure triggers, channel-token.md change procedure |
| 2.1.9 | **A pump tube change voids C-01 for that channel**, on the change, not on a date | commissioning re-measure triggers, D-028 |

### 2.2 The rule that outranks convenience

| # | Constraint | Trace |
|---|---|---|
| 2.2.1 | **NO AUTOMATIC RE-DOSE. EVER.** Software never tops up, retries, re-doses or corrects on its own, on any reading of any check. If a check reports no movement, the batch STOPS and tells the operator, and the operator decides | G-16, D-017 |
| 2.2.2 | This is a **RULE, not a parameter.** No configurable retry count. No threshold anyone can turn up. No code path that could be enabled later. It is frozen before any code exists precisely so it cannot be argued into existence by a plausible edge case | G-16, D-017 |
| 2.2.3 | **The laundered version is also forbidden: there is no "resume dose" action, anywhere, under any name.** A remainder computed from an unknown delivered fraction is an automatic re-dose with a human as its trigger. What the operator may legitimately do is command a FRESH dose of a volume they choose, which is an ordinary dose. That distinction is the whole rule | G-16, p09 |
| 2.2.4 | **G-16 has no crash exemption.** A watchdog reset, a power restoration or an operator reset may not resume anything | G-16, D-033 |
| 2.2.5 | **A louder alarm invites exactly the forbidden correction.** On "pH moved the wrong way", the operator's instinct is to command the opposing pH channel. The corrective path must be STRUCTURALLY INCAPABLE of it, not merely discouraged, and no screen may offer it | G-16a |
| 2.2.6 | Consequence to hold on to, because it is why the whole class of settle-window timing bugs is not dangerous: with 2.2.1 in force, a settle-window timing error can only produce a FALSE STOP, which is loud and safe. **The direction of error is chosen, not accidental** | D-017 |

### 2.3 Constraints on what may be claimed

| # | Constraint | Trace |
|---|---|---|
| 2.3.1 | **Software may never report commanded state as measured state, anywhere** - not on a screen, not in a log, not in a variable name that a later reader will believe | parts.md |
| 2.3.2 | **No progress bar on a dose, and no delivered-fraction percentage anywhere.** A percentage computed from a step index renders a commanded count as a delivered fraction. It is the confident-wrong-answer shape and the one thing a tired operator will believe | G-19 |
| 2.3.3 | **An expected sign comes from a measurement, never from a label.** If a check derives what it expects from a product name, a mislabelled jug produces a mislabelled expectation and the check CONFIRMS the swap instead of catching it | G-32, D-083 |
| 2.3.4 | **Any run that turns a head records whether it COMPLETED.** A calibration run that did not complete is DISCARDED, never scaled. This covers doses, primes, purges, operator tests and C-01 calibration runs alike | G-20, D-034, F-016 |
| 2.3.5 | **Never leave an outcome slot absent.** An absent outcome read later as "no failure recorded" is passing by default. That is T-014's shape with no literal True in sight | p09, T-014 |
| 2.3.6 | **A figure that came from a configuration file, a template or a fixture is not evidence about the world.** Ask of any number the application consumes: did this come from the world, or from a file that had to contain something | T-018, G-33 |

### 2.4 Constraints from the hardware the application does not own

| # | Constraint | Trace |
|---|---|---|
| 2.4.1 | **A leak, an E-stop or a lost interlock drops motor power in hardware.** Software neither causes nor prevents it and must behave correctly when it happens mid-dose | G-07, G-13 |
| 2.4.2 | **The permissive contactor removes MOTOR SUPPLY (VM) from every driver at once. It does NOT remove VDD**, the driver logic supply, which stays live | G-09 as amended by D-031 |
| 2.4.3 | **EN is unwired and every driver defaults ENABLED. Software has no per-driver disable, permanently, and never will.** The drop handler's action is STOP TALKING TO THEM, not shut them down, and no comment, screen or document may imply otherwise | G-21, D-032 |
| 2.4.4 | **The Pi is powered independently and is not relay switched.** It has power whenever the panel does and stays alive through a permissive drop, so it can log and alert on it. No code may assume the Pi loses power with the system | P-07, parts.md |
| 2.4.5 | **Nothing in the panel can power cycle the Pi.** It reboots by software or by killing the panel, so **a watchdog is the only recovery path from a hang** | P-07 |
| 2.4.6 | **The panel runs without the Pi.** Fills, transfer, circulation and the chiller all operate on float and interlock logic. The Pi adds dosing and removes driver power. If it dies, the water system keeps running and only dosing stops | G-26, D-052 |
| 2.4.7 | **Probes read upstream of every injection point.** A reading reflects the day tank, not the dose just injected | G-10 |
| 2.4.8 | **Microstepping is set by pins and never over UART.** A UART-set factor reverts to the pin default on a rail dip, mid-batch, while every instrument reads healthy. The application does not set it and does not read it as authoritative: it uses the figure recorded at C-17 | D-075, D-080 |
| 2.4.9 | **A no-flow CONDITION may drop the manifold pump in hardware. A circulation VERIFICATION FAILURE may not.** They are different events. Hardware protects the pump; software protects the batch and stops it loudly under G-16 | G-25, D-038 |
| 2.4.10 | **The watchdog is fed from the sequencer and state loop, never from an independent timer thread.** A timer that keeps ticking while the sequencer is wedged passes forever and hides exactly what it names | D-033, T-014 |

### 2.5 Constraints on verification

| # | Constraint | Trace |
|---|---|---|
| 2.5.1 | **EC rise attributable to a dose is the only whole-loop check that exists.** Its window is anchored to the dose and extends past the last commanded step by the settling interval. It cannot attribute a change to a channel, it does not work at rest, and it does not move for pH up, pH down or fulvic | D-009, D-024, S-15, F-001 |
| 2.5.2 | **The pH probe attributes the two pH channels and nothing else.** It is DIRECTION-AWARE: it compares a SIGNED movement against a signed prediction. A magnitude-only pH check attributes nothing and is a duplicate of the EC check wearing the pH check's name | D-011, D-083, S-16 |
| 2.5.3 | **The two pH channels cannot be attributed at the same time.** If both fire in one window the movements cancel and pH shows the net. Attribute whichever was commanded, and treat a plan that fires both as a FAULT CONDITION that must not read as passing | S-16 constraint 1, D-011 |
| 2.5.4 | **Fulvic is unattributed and stays that way.** Do not solve it and do not warn about it as though it were a defect | D-013, S-17 |
| 2.5.5 | **Every implicit verification is delayed by an interval nobody has measured.** A check read too early reports a healthy dose as a failure. **No pass-or-fail verification logic ships until C-02 exists** | D-012, F-004 |
| 2.5.6 | **The readback discipline is asymmetric.** An apparent DROP is qualified over consecutive samples before acting. An apparent WELD latches on a SINGLE sample and is never cleared because later samples read open | D-030, F-011 |
| 2.5.7 | **Software may not "solve" an intermittent readback by lengthening its filter until the nuisance stops.** That change also hides a real drop, it looks like tuning, and it will be proposed by whoever is tired of the false stops. The fix is at the contact | D-030, F-011 |

### 2.6 Constraints on identity

| # | Constraint | Trace |
|---|---|---|
| 2.6.1 | **This application is the DEFINITIONAL end of the channel token.** It declares what channel N is; DISPLAY-BOX, INTERCONNECT, PUMP-BOXES and DOSING consume that declaration and match it. There is no translation table anywhere on the chain | D-021, S-19 |
| 2.6.2 | **Jugs are dedicated per channel for life.** A jug is refilled with the same product forever or it is retired | G-17, D-018 |
| 2.6.3 | **The jug change break point is at the jug. The tube stays with the channel** and is never moved between channels | G-18, D-020 |
| 2.6.4 | **A rule keyed to what a thing IS outlives a rule keyed to how big it is.** Where a rule can be written against a role rather than a dimension, it is | G-34 |
| 2.6.5 | **Attributes are recorded ONCE, in channel-register.md.** This document may reference an attribute and may not restate it | D-057 |

### 2.7 The one operational interlock

| # | Constraint | Trace |
|---|---|---|
| 2.7.1 | **NO DOSE DURING A DAY TANK FILL.** A fill changes tank volume while a dose is computed against it, and every verification is a delayed tank reading, so a fill inside a settle window corrupts the measurement | D-042 |
| 2.7.2 | The contact is wired so that CLOSED means NO FILL and OPEN means FILLING. **A severed cable therefore reads as filling and inhibits dosing.** The failure is a stop, not a permission. Software must not add logic that compensates for, qualifies, or times out this input; the safety of it is in the contact selection and software cannot improve on it | D-042, T-016, S-03 |

---

## 3. The channel model

The full declaration is `channel-token.md`, which this application owns and which
every other subsystem consumes. This section states what the declaration means for
the code. **Where the two differ, the declaration governs.**

### 3.1 What a channel is

**A channel is an identity, not a component.** It is one of the eight given dosing
paths. It is not the driver, the head, the pin, the cable core, the tube, the jug
or the product. Every one of those is an ATTRIBUTE and every one is replaceable
without the channel changing.

**The token IS the key.** There is no identity behind the token that the token
stands for. The application does not hold a channel object with a token attached
for display; the token is the primary key of every per-channel record, in memory,
on disk, in the log and on any screen.

**Canonical form:** uppercase `CH`, one digit, no space, no leading zero, no
punctuation. The set is `CH1` through `CH8`. Not `ch3`, not `CH 3`, not `CH03`,
not `#3`, not `3` alone. A message may put words around the token and may never
substitute words for it.

### 3.2 What is an attribute

An attribute is bound to a token and is never an identity of its own: which box
the head sits in, which pin drives it, which core carries it, which product it
doses, its steps-per-millilitre figure from C-01, its poured jug volume under
G-05, its role, its colour.

**Attributes live in `channel-register.md`, once.** The application reads them from
one record per token and never from a second place. In particular:

- **The set of pH-moving tokens is read from the register's role column.** It is
  never computed, never hard-coded as a pair, and never derived from "the other pH
  channel". Today the register carries one role marking and one inference that is
  marked as an inference; code must treat both as data it was given, and an
  implementation must not silently promote the inference to a fact.
- **Product names are not identity and are not present for five of the eight.**
  Verification never derives an expected sign from a product name (2.3.3).

### 3.3 What is forbidden in code

These come from the declaration's forbidden list and are the ones that bite an
implementer:

1. **Any translation table, in any medium** - a file, a code comment, a
   spreadsheet column, a laminated card, or an operator's head. If such a table
   would be USEFUL, the chain is already broken, and the fix is to correct the
   disagreeing end, never to write the table.
2. **A zero-based or offset internal index.** No array position is ever a channel
   identity. Per-channel state is stored in records keyed by the token, never in a
   positional list of eight values. A positional list is an off-by-one waiting for
   an editor to insert a line, and G-04 and G-05 guarantee nobody will ever see
   the result.
3. **Arithmetic on tokens.** No `N+1`, no "the next channel", no set computed from
   a neighbour. Sets are written out explicitly.
4. **Renumbering** for tidiness, to make pins contiguous, to match a header or a
   connector, or to reflect the box division. If the pin map is non-monotone, the
   pins are non-monotone and the tokens stay as they are.
5. **Two names for one channel, or one name for two things.** No internal driver
   ID alongside the token. No bare digit that could be a channel, a core or a
   terminal.
6. **A ninth channel, a spare labelled as a channel, or a token reused after
   retirement.** A retired token is marked retired, is never deleted because the
   logs still name it, and the sequencer refuses to command it.
7. **A default list ordered by anything but canonical order.** Other sorts are
   allowed only where the token is on every row.
8. **Any local abbreviation or alternative rendering.** A carrier that cannot hold
   the canonical form is a carrier defect reported to this application, never
   solved by inventing a short form.

### 3.4 Out of service

While software and the wall may disagree about a channel - during a rewire, a
relabel, a move, a driver change that voids C-01 - **the channel is OUT OF SERVICE
and the sequencer skips it.** Skipping is the sequencer declining to issue steps.
It is not a hardware disable and does not rely on one (2.4.3).

**A batch that requires an out-of-service channel STOPS and tells the operator.**
It does not substitute, skip past it, or reorder. That is G-16 applied to a
labelling change rather than to a check result, and for the same reason: the only
safe direction of error is the loud one.

### 3.5 What the token requires of a record and of a screen

- The token appears on every per-channel element of a record or a screen, always.
  A message that says only a product name rebuilds the translation table inside
  the operator's head, which is precisely where it cannot be checked.
- **The token in a message, an alarm and a log line is the same string as on the
  wall, character for character.** A log read a season later needs no key.

---

## 4. The I/O surface as it actually is

This section exists because **most of the panel is invisible and untouchable to
this application**, and an implementer who does not know that will write code that
waits for something that never arrives.

### 4.1 Outputs: what the Pi commands

| Output | What it is | Notes |
|---|---|---|
| **The driver permissive coil.** ONE output | The Pi's only switched load anywhere in the system. It energises the contactor that distributes motor supply (VM) to all eight drivers | S-07, S-09, D-052. Its readback is a separate input (4.2). The Pi's coil command is only one leg of a hardwired series chain: **dropping the command does not by itself prove VM is removed**, and what the command is in series with is S-07, which is OPEN |
| **Step and direction, per channel** | Pulse and level outputs into eight always-enabled drivers | S-10. These are signalling, not power. They are the application's ENTIRE influence on a driver |

**That is the complete list of outputs.** There is no enable, no reset, no
per-driver anything. **The application cannot disable, de-energise, halt or make
safe a driver.** Its only action against a driver in trouble is to stop issuing
pulses.

### 4.2 Inputs: what the Pi can observe

| Input | What it says | Status |
|---|---|---|
| **Permissive readback** | The position of an auxiliary contact on the permissive contactor. **It is not a measurement of the load conductor**: a welded main pole or an open load conductor reads whatever the aux reads | Circuit closed (D-029, S-08); the Pi-side input is part of S-12, OPEN |
| **Day tank fill in progress** | A dry contact. CLOSED means no fill, OPEN means filling, and a severed cable reads as filling | Circuit closed (D-042, S-03); the Pi-side input is part of S-12, OPEN |
| **pH** | A day tank reading, upstream of all injection | EZO circuit. S-11 and S-12 OPEN |
| **EC** | A day tank reading, upstream of all injection | EZO circuit. S-11 and S-12 OPEN |
| **Temperature** | A day tank reading | EZO circuit. S-11 and S-12 OPEN |
| **Dry-run interlock relay state** (S-20) | Whether the interlock relay is made. **It is a PERMISSION for circulation to run, not a statement that the pump is turning** | **OPEN**, and blocked on S-05. Nothing may be built against it. See 4.4 and 6.4 |

**That is the complete list of inputs.**

### 4.3 What the Pi cannot command

Stated plainly, because it is most of the panel and because the project's original
description said otherwise and was wrong (D-052, F-027):

- **The day tank fill.** A float seal-in. Not the Pi's.
- **The storage tank fill.** Same construction, separate relay. Not the Pi's.
- **The transfer pump.** A POLE on the day tank fill relay. Not a coil the Pi
  drives.
- **The manifold pump.** A POLE on the dry-run interlock relay. **The Pi cannot
  start it, cannot stop it, and cannot ask for it** (D-052, D-091). It runs when
  the interlock is made and the relay is energised, and it is off between batches.
  **Nothing commands intermittent circulation** - that is a closed question with an
  open consequence (F-057, D-091).
- **The chiller and its loop pump.** A contactor on its own circuit, and what
  energises its coil is unaccounted for anywhere in the project (D-064, S-18).
- **V3, the E-stop, the manual reset, the leak console, the permissive chain
  itself.** Hardware, by design.
- **Any driver's enable.** Permanently (2.4.3).

### 4.4 What the Pi cannot observe

- **Delivered volume, on any channel, ever.** Nothing measures it (G-04).
- **Direction of rotation, or that a head turned at all.** Nothing measures it.
  A severed direction conductor can run a head backwards while the books decrement
  forward, and no input sees it (S-10).
- **Flow, anywhere.** There is no flow signal (D-007). The flow cell is a fitting.
- **Whether the manifold pump is turning.** Between batches the loop is still
  and EC sits flat whether the pump is healthy or dead (F-001 limit 1, F-003).
- **Tank level.** The only level information in existence is the fill-in-progress
  contact (G-01, G-02). Software cannot know the level and must never adapt to it.
- **Jug level.** Arithmetic only (G-05).
- **Motor supply presence at any driver, logic supply presence, or any driver
  diagnostic.** No VM sense, no current sense, and no driver diagnostic or index
  signal lands at the Pi.
- **Which element of the permissive chain opened.** The Pi has no leak, E-stop or
  interlock input. **It yields a mismatch, never a cause, and nothing at all if
  both ends fail the same way.**
- **Chiller state**, as commanded or as measured. S-18 is OPEN and the sample
  tagging of D-027 has no source until it closes (F-043, D-064).
- **Contact bounce, on a single sample.**

### 4.5 Two things that follow and must be written into the code's shape

1. **Detection latency here is not a safety figure.** Safety already happened, in
   hardware, before software knew. Three latencies sit in series - contactor
   drop-out and auxiliary transfer, input conditioning, sampling and qualification -
   and none of them is on file. **So there is always a set of steps commanded after
   VM vanished and before software learned of it.** That is why delivery is
   expressed as a bound structure and not a number, and no amount of tightening
   removes it. Faster detection buys fewer pulses into a driver in an unknown state
   and a tighter bound. **It buys no safety at all and must not be argued for as if
   it did.**
2. **The application's read of its own commands is memory, not measurement.** It
   may record what it asked for, labelled as what it asked for (2.3.1).

---

## 5. The dose model

### 5.1 Objects

| Object | Definition |
|---|---|
| **Dose** | One channel, one commanded volume, converted to a commanded step count using that channel's C-01 figure and C-17 configuration. A dose is the unit that gets an intent record, a bound structure and an outcome slot |
| **Batch** | A first-class object holding the full set of doses **with all commanded volumes known before the first step is issued.** A batch is not a queue that grows |
| **Non-dose head movement** | A prime, a purge, an operator single-channel test, a C-09 trace dose, a C-01 calibration run. **Every one turns a head and puts product in the loop.** All pass through the same admission, the same intent record, the same booking and the same window rules as a dose. This is the case most likely to be missed, because a screen will call them something other than "dose" |

### 5.2 Plan admission

**Admission happens once, before any step is commanded**, against the complete
plan. A run-time check that fires when the second pH head starts has already let
the first dose into the tank, and nothing can say how much or undo it.

A plan is admitted only if ALL of the following hold. Each is a rejection, not a
warning, and a rejected plan does not start:

1. **Every token in the plan is a live token in the register**, not retired, not
   out of service (3.4).
2. **Every commanding channel has a valid, non-void C-01 figure and a recorded
   C-17 configuration.** A voided figure blocks that channel (2.1.8, 2.1.9).
3. **At most one pH-moving channel carries a nonzero commanded volume.** A plan
   carrying nonzero volumes on both is rejected as a fault condition, not
   corrected, not reordered, not split into two batches by software (2.5.3).
4. **No pH attribution window is open for the opposing pH channel** (5.6, 6.5).
   Until C-02 exists, the window-scoped form of this check cannot be computed and
   only the batch-scoped form of rule 3 is enforceable; that gap is stated in
   section 11 rather than approximated.
5. **The fill-in-progress input reads NO FILL** (2.7). Filling, or a severed
   cable, refuses admission.
6. **No latched weld fault is outstanding**, and no permissive drop is
   unacknowledged (7.2, 7.3).
7. **The permissive command and readback agree in the safe direction**, i.e. the
   application is not standing in an unresolved mismatch (7.2).

**What counts as "fired" for rules 3 and 4: commanded steps greater than zero.**
Not "the recipe names the channel". A zero-volume entry is not a violation. **A
dose too small to exceed the noise band still counts as fired** - it still moves
pH even though it cannot be attributed. The guard is on commanding; the band is on
detectability; the two thresholds are different numbers and must never be
conflated in code.

### 5.3 Sequencing

Doses run **strictly one at a time** (2.1.5). The sequencer:

1. Takes the next dose in the batch, having already written the batch plan
   durably at admission (8.2).
2. **Writes that dose's intent record durably before issuing any step** - token,
   commanded volume, commanded step count, and the C-01 figure and C-17
   configuration used. Written afterwards instead, a cut mid-dose leaves no record
   the channel was touched and the jug arithmetic under-books.
3. Issues steps for that channel alone, **writing the progress marker AHEAD of the
   steps it covers, never behind** (8.3).
4. Stops at the commanded count, closes the dose record, and books the volume.
5. **Does not start any dose whose attribution would land in another dose's open
   read window** (6.5). G-06 stops two heads turning together; it does not stop
   channel B starting a second after channel A stopped, and at the probe those two
   doses are simultaneous.
6. Feeds the watchdog from this loop, and only from this loop (2.4.10).

**A batch ends at last-READ, not at last-STEP.** If the record or a screen closes
the batch when the pumps stop, every verification is orphaned.

### 5.4 The bound structure of what was delivered

**Delivered volume is a bound structure, not a number, in every record where it
appears.** Three fields, always all three:

| Field | Definition |
|---|---|
| `commanded` | What the plan asked for, converted through C-01 |
| `ceiling` | The write-ahead marker that was durable at the moment commanding stopped. **The book is a ceiling on what was delivered, never a floor** |
| `floor` | **Zero.** Not "steps issued minus a few". Zero, until a subsystem returns something that narrows it, and nothing on this build does today |

**The step index at a halt is a COMMANDED count. It is evidence, not a delivered
figure**, and presenting it as a fraction is forbidden (2.3.2).

Each record also carries **provenance**, because the evidence is genuinely stronger
in one case than the other and a later reader must be able to tell which they hold:

- `PI ALIVE, BOUNDS WITNESSED` - the application was up throughout and observed
  the event.
- `RECONSTRUCTED FROM WRITE-AHEAD ON RESTART` - the application was not up, and
  the bounds are what the disk retained.

### 5.5 Booking rules

1. **The volume is booked as dispensed at commanding**, because G-04 leaves
   nowhere else to book it.
2. **A jug is decremented by the CEILING, at the moment the dose closes** -
   including a dose terminated by a permissive drop, where it is decremented
   immediately and not on operator acknowledgement. An operator who walks away
   must not leave the book under-booked.
3. **Over-booking is the chosen direction.** Over-booking makes the operator change
   a jug earlier than needed, which is annoying and safe. Under-booking runs a jug
   dry and draws air on a suction line, which is invisible, and it happens at the
   worst moment.
4. **A channel's remaining figure carries a flag once any interrupted dose has
   been booked against it**, so its low-jug warning is known to be conservative
   rather than exact.
5. **Accumulated over-booking is corrected by a physical event, never by
   software.** The reset is a jug change with the poured volume re-entered.
   **Software never corrects the book by an estimate, and the operator is never
   asked to type a delivered volume** - that guess would enter the one number G-05
   treats as authoritative, and it moves in the under-book direction. An
   operator's estimate belongs in a free-text note. Never in the arithmetic.
6. **Non-dose head movement books exactly like a dose** (5.1). A prime that is not
   booked is product removed from a jug that the arithmetic never sees.

### 5.6 Prohibitions

**Nothing in this list may be relaxed by configuration.**

1. **No automatic re-dose, top-up, retry, correction or completion of an
   interrupted fraction**, on any reading, at any time, for any reason (2.2).
2. **No resume action, under any name, in any interface** (2.2.3).
3. **No dose on another channel whose attribution would land in an open read
   window** (5.3.5).
4. **No re-baseline, zero or re-reference inside an open window.**
5. **No pass or fail evaluation inside the settle window**, and a flat reading
   inside it may not raise a dose failure or a circulation fault.
6. **No opposing pH dose while a pH attribution window is open**, and that window
   extends past the pump stopping by the settling interval. Overshoot correction by
   the opposing channel is legitimate only after the window closes and a fresh
   baseline is taken, and the corrective path must be structurally incapable of it
   sooner (2.2.5).
7. **No dose while the fill input reads filling or severed** (2.7).
8. **No batch closed at last-step** (5.3).
9. **No dose commanded on an out-of-service or retired token** (3.4).
10. **No second dose issued to "make up" a small commanded volume** that falls
    below the detectability band. Below the band the correct result is an outcome,
    not an action (6.3).

---

## 6. The verification model

**Nothing in this section ships until C-02 exists** (2.5.5, D-012). It is
specified now because writing it in today costs nothing, and retrofitting
direction-awareness or a fourth outcome onto a magnitude-only implementation
changes the outcome set, every operator message and the commissioning reference
data (D-083).

### 6.1 The phases of a dose, in order

Each phase states its own preconditions. **No phase is qualified by a later one.**

| # | Phase | What happens, with its conditions folded in |
|---|---|---|
| 1 | **Baseline** | Taken with no dose in flight and no window open, under the same conditions the later read will be taken under, and recorded as a VALUE AND A SPREAD. One number is not enough: without a spread there is no way to tell moved from drifted and every later comparison is unanchored |
| 2 | **Command** | Steps issued for exactly one channel, with the intent record and progress markers already durable (5.3). The volume is booked here |
| 3 | **Settle** | From the last commanded step to the earliest valid read. Its length is C-02, which does not exist. **No evaluation of any kind happens in this phase** |
| 4 | **Read** | Sampled over a window, not at a point, and compared against the baseline and its spread |
| 5 | **Decision** | One outcome from the set in 6.2, recorded explicitly, never absent |

### 6.2 The outcome sets

**The EC whole-loop check (S-15)** - four outcomes:

| Outcome | Meaning |
|---|---|
| `PASS` | Movement exceeded the band by the stated margin, in the window |
| `FAIL - NO MOVEMENT` | The window closed with no movement exceeding the band. **The batch stops and tells the operator** (2.2.1) |
| `INDETERMINATE` | The window was contaminated, voided, or ran past its ceiling without a stable read. **Not a failure, and it must not be folded into one** |
| `NOT VERIFIABLE AT THIS DOSE SIZE` | The predicted change for the commanded volume does not exceed the noise band by the stated margin. **This is an outcome, not a failure.** Small trim doses will land here, and a system that scores them as failures will fail constantly on the doses that matter least |

**The pH attribution check (S-16)** - the same four, plus a fifth that must never
be folded into failure:

| Outcome | Meaning |
|---|---|
| `WRONG DIRECTION` | Movement exceeded the band with the sign opposite the signed prediction |

**Why it stays separate**, both reasons, because either alone would be arguable:
it sends the operator somewhere different - no-movement points at the pump, the
tube and the jug level, wrong-direction points at which product stands on which
station - **and the two mean different things about the tank: no-movement means the
tank probably received nothing; wrong-direction means the tank DEFINITELY received
something, it was the wrong chemical, it is already mixed, it is already partly
downstream of V3, and it is unmeasurable and irreversible** (D-083).

### 6.3 Direction awareness

- The pH check compares a **signed** movement against a **signed** prediction.
- **The reference sign is the measured step for that token from C-03, and never a
  product name** (2.3.3, G-32). A swap present at commissioning is baked into the
  reference and confirms itself forever; that residual is named, not solved.
- **The EC check is not an attribution mechanism and direction adds none.** For the
  six nutrient channels EC moves the same way for all of them, so a crossed pair
  still confirms itself completely. An EC movement opposite the expected sense is
  recorded verbatim in the record and does not produce a pass; **it attributes
  nothing and does not identify a product.**
- **Because the check is signed, drift's DIRECTION matters**, where a
  magnitude-only check could treat drift as noise that only ever adds. **The drift
  half of C-08 is therefore load-bearing, not advisory.** No new commissioning row;
  a row that could have been optional becomes mandatory.

### 6.4 Window validity: what can actually be required, and what cannot

**This subsection replaces the window-validity precondition in
`subsystems/control-software-f004.md`, which is withdrawn.** That document said the
Pi commands the circulation relay so it can require circulation commanded on for
the whole window and void the window otherwise. **Under G-26 and D-052 the Pi
commands no such thing, so that precondition has no source** (F-070). D-091 closes
the question underneath it: nothing commands intermittent circulation at all.

**What the application CAN do, with the inputs that exist:**

1. **Void a window on a fill.** The fill-in-progress input is real, it is wired so
   that filling and severed both read as filling, and a fill dilutes the tank and
   drags both readings toward the makeup water, which is indistinguishable from a
   dose that failed. A window during which that input asserted is VOID, and its
   outcome is `INDETERMINATE`, recorded with the reason.
2. **Void a window on its own knowledge.** A permissive mismatch, a restart, a
   watchdog reset, an aborted batch, a probe read failure, or a second dose landing
   in the window all void it (7, 9).
3. **Record its own commanded state alongside every sample** - what it commanded
   on the permissive coil, which channel it was stepping - labelled as commanded
   (2.3.1).
4. **Refuse to claim verification when it cannot establish the window's validity.**
   `INDETERMINATE` is always available and is never a failure.

**What the application CANNOT do, stated plainly so nobody writes it:**

1. **It cannot require circulation.** It cannot command the pump, cannot start it
   for a window, cannot hold it on across one, and cannot stop it.
2. **It cannot confirm the loop is moving.** There is no flow signal and no
   observable that separates a running pump from a stopped one at rest (F-001 limit
   1, F-003).
3. **It cannot know a window sat inside a running period.** D-063 requires a
   window not to span a start or a stop, because a window that spans a transition
   measures two regimes. **That is a procedural condition on how a batch is run and
   on the C-02 measurement, and it is not enforceable in software.** An
   implementation must not fake enforcement by inferring the pump's state from
   anything.
4. **It cannot tag a sample with chiller state.** S-18 is OPEN and the chiller
   coil's driver is unaccounted for (D-064). D-027's tagging is specified and
   unimplementable, and a field left empty is honest where an inferred field is
   not.
5. **It cannot detect the slow failure that matters most.** The settling number's
   dominant input is circulation flow, which this design does not observe by
   choice. A fouled impeller, an intake screen, biofilm or scale lengthens the
   settling time silently and drifts the check toward reporting healthy doses as
   failures. **The mitigation is not a sensor. It is the event-driven re-measure
   list in commissioning.md** (F-004).

**Two claims here that must be kept separate, because one may be withdrawn and the
other may not** (T-022):

- **Claim A, which stands regardless:** the fill input can void a window, and the
  application must refuse to claim verification it cannot establish. This rests on
  S-03, whose circuit is closed, and on the outcome set.
- **Claim B, which may be withdrawn:** *if* S-20 is ever frozen, the application
  gains a read of the dry-run interlock relay, and a window during which that
  relay was not made may be voided. **This is a read of a PERMISSION, not of a
  turning pump**, so even then it can void a window and can never validate one.
  S-20 is OPEN and blocked on S-05, and **if S-05 resolves level-based, circulation
  verification is foreclosed permanently** (D-060). **Nothing in claim A depends on
  claim B.**

**And the honest check on my own scepticism** (T-019): the settling interval is
refused for want of C-02, but the noise band (C-08), the per-channel step
magnitudes (C-03, C-04), the detectability margin, the readback qualification
length and the write-ahead granularity rest on evidence that is no better. **None
of them is estimated here either.** Section 10 lists all of them together for
exactly that reason.

### 6.5 What a window is, and what closes it

- A window OPENS at the first commanded step of a dose and is anchored to that
  dose (D-024).
- It EXTENDS past the last commanded step by the settling interval.
- It CLOSES at a recorded outcome, and only at a recorded outcome. A window that
  is voided closes with `INDETERMINATE` and a reason.
- **An open window is durable state** (8.4). A restarted application must know it
  is standing inside one.
- **A fulvic dose must not reset or re-baseline an open pH or EC window.** That is
  the only requirement fulvic carries; it is unattributed and stays that way
  (2.5.4).

### 6.6 What each check can and cannot attribute

| Check | Can say | Cannot say |
|---|---|---|
| **EC (S-15)** | The loop moved and something arrived, during a dose | Which head delivered. Eight heads inject into one stream. A single stalled head, a collapsed tube or a dry jug produces a batch that completes with one nutrient missing while EC still moves, because the other seven delivered. It says nothing at rest, and nothing about pH up, pH down or fulvic |
| **pH (S-16)** | Which of the two pH channels moved the tank, and in which direction | Anything when both were commanded in one window - the movements cancel and pH shows the net. Anything about the six nutrient channels. Anything about a dose below the detectability band |
| **Fulvic (S-17)** | Nothing | Everything. Accepted, one unattributed channel of eight (D-013) |
| **Both** | That a change appeared in the DAY TANK after mixing | That the manifold, the head, the tube or the jug did anything in particular. The probes are upstream of every injection point (G-10) |

**What the pH check does NOT remove, so nobody treats it as a solution:** it is a
detector, not a preventer, and it acts a dose too late - the wrong chemical
reaches the tank once, in full, before anything is known. Small trim doses stay
below the band and a swap discovered only through them stays invisible. A swap
present at commissioning is baked into the reference. And it generalises nowhere
else (D-083).

---

## 7. The fault model

**Structure of every fault:** what raises it, what it stops, what clears it, and
what it must never do. **Faults accumulate: no fault clears another**, and
especially not a latched weld.

**Severity splits; the record never does.** The permissive drops on ordinary
shutdown too, so its handler runs on the NORMAL path, several times a day, most
often with nothing in flight. **It is not an exception handler.** A handler that
raises a loud fault every time the operator shuts the skid down gets switched off.
**The record written is byte-identical either way; only the severity differs, and
severity is decided from the application's own knowledge: did I command this drop,
and was anything in flight.** A drop the application commanded with nothing in
flight is informational. **A drop it did not command is a fault INCLUDING when
nothing was in flight** - that is the leak-or-E-stop-at-rest case and the one worth
waking someone for.

### 7.1 F-DROP: permissive mismatch, commanded ON and readback OPEN

**Raised by:** the readback reading open while the coil is commanded on,
**qualified over consecutive samples before acting** (2.5.6). It means the chain
tripped upstream, or the coil failed, or the contactor failed to pull in, or the
readback failed. **These are indistinguishable and the fault names none of them.**

**What it does, in this order.** The order is by irreversibility: stop widening the
unknown, capture the bounds, make them durable, poison everything derived from
them, then tell the human.

1. **Stop the step generator in software, at the source, for the channel in
   flight.** Not "ask the driver to stop": there is no such request, and no
   per-driver disable exists (2.4.3). Every pulse after this instant is a pulse
   into a driver in an unknown state and widens the ceiling on a dose nothing can
   measure. First, because its cost grows with delay.
2. **Latch the bounds atomically in memory:** commanded, ceiling, floor (5.4).
3. **Close the dose record durably as `TERMINATED-BY-PERMISSIVE`.** Never
   `COMPLETED`, never `FAILED`. It carries all three bounds and its provenance,
   and **the jug is decremented by the ceiling now, not on acknowledgement** (5.5).
4. **Void every open window and set every outcome slot explicitly to
   `INDETERMINATE - PERMISSIVE DROP`.** Never absent. Record whether a pH
   attribution window was open, because that gates recovery.
5. **Abort the batch as an object.** Remaining doses are marked `NOT COMMANDED`, a
   state distinct from failed. **The batch object is destroyed, not suspended: a
   batch that survives the event is a resume path wearing a different hat.**
6. **Record the event:** the commanded coil state, **the RAW readback sample trail
   either side of the transition and not merely the qualified verdict**, and the
   mismatch. **Do NOT record a cause** (4.4).
7. **Drop the application's own coil command and hold it dropped.** Two reasons:
   command and readback then agree in the safe direction, so a later weld test
   means something; and when the operator presses reset, **the contactor must not
   re-close underneath a command left standing from before the fault**, re-applying
   motor supply to eight enabled drivers at a moment nobody chose. Re-energisation
   must be the consequence of a human act. Caveat, and it is not optional: what the
   coil command is in series with is S-07, which is OPEN, so **nothing may assume
   that dropping the command removes motor supply by itself.**
8. **Do not touch circulation or the chiller.** The application cannot command
   either (4.3), and states are recorded, never changed.
9. **Then the screen**, last. It is the only step reconstructible from the log, so
   it must never be ahead of the durable writes.

**What it stops:** all commanding. No step, no prime, no purge, no test, no
calibration, on any channel, until recovery (7.9).

**What clears it:** nothing automatic. See 7.9.

**What it must never do:**

1. Never keep clocking steps, and **never let the generator run out its planned
   count on the theory that a de-powered driver ignores it.** Nothing on file says
   what the driver does, and the ceiling would advance by steps that certainly
   delivered nothing.
2. **Never claim software made the drivers safe.** No screen, comment or document
   may say "drivers de-energised".
3. **Never score the interruption as a dose failure.** Failed implies nothing was
   delivered, which is the under-book direction, which runs a jug dry and draws
   air. **Interrupted is not failed.**
4. Never let the interrupted dose's window produce a pass or a fail. **The
   poisoning is durable and survives the reset.**
5. Never re-baseline across the drop, and never carry a pre-drop baseline forward.
6. **Never auto-clear when the readback returns closed.** A returning signal says
   the contactor is made; it says nothing about why it dropped or what is in the
   tank. Clearing on the return of a signal is a condition that becomes true by
   itself.
7. **Never retry the coil command.** It chatters a coil against a dead chain, and
   if the operator restores the chain mid-poll it re-energises eight enabled
   drivers at an instant chosen by a timer.
8. Never name a cause (4.4).
9. Never clear a pre-existing fault, especially a latched weld.
10. Never leave an outcome slot absent.
11. Never restart or shorten another channel's still-open settle timer as though
    the system had been quiet.
12. Never keep the batch object alive pending reset.
13. **Never trim or roll the log for tidiness.** Those raw samples are the only
    evidence an intermittent contact will ever leave (F-011).
14. **Never stop sampling and logging.** The Pi is powered independently precisely
    so it can log and alert through this (2.4.4). Continuing to sample is correct;
    using those samples to verify a dose is not.

### 7.2 F-WELD: permissive mismatch, commanded OFF and readback CLOSED

**Raised by:** a single sample of the readback closed while the coil is commanded
off. **It latches on that single sample and is never cleared because later samples
read open** (2.5.6). A long qualification here is a filter that hides exactly the
failure the readback was built to catch. The consequence it names is eight drivers
live while software believes them dead.

**What it stops:** all commanding, and it blocks plan admission (5.2.6).

**What clears it:** an operator action recorded against the fault, after the
condition is addressed at the contactor. **It is never cleared by the signal
changing, by a restart, by a watchdog reset, or by any other fault.**

**Never:** never treat it as a sensor glitch and never lengthen the filter to
silence it (2.5.7). The chosen consequence of this asymmetry is that an oxidising
contact produces false stops and never a missed weld - the same chosen direction
of error as G-16.

### 7.3 F-PH-ATTRIBUTION: both pH-moving channels in one window

**Raised by:** two paths, which behave differently:

- **At plan admission**, by a plan carrying nonzero commanded volumes on both
  pH-moving channels (5.2.3). The batch does not start.
- **Mid-run**, by a violation detected after commanding has begun.

**What it stops:** at admission, the batch never starts. Mid-run, the batch aborts
and **pH is recorded as indeterminate for that batch permanently**, because
nothing can reconstruct it.

**How the evaluator must be built, because the dangerous implementation looks
correct:** the check is a **precondition that short-circuits before any comparison
is computed** - exactly one pH-moving channel commanded in this window, or emit the
fault and compute nothing. The dangerous version computes the movement, finds it in
the expected direction, scores a pass, and then overrides it; the net of an up and
a down dose can easily fall in the expected direction, and **an override that is a
later step in the code is an override somebody can remove.** "Must not read as
passing" is satisfied by never producing a pass value, not by suppressing one.

**What clears it:** at admission, fixing the plan. Mid-run, an operator resolution
recorded per open window. **Not by acknowledging an alarm mid-run**, and not by
waiting: a permissive drop or a violation cannot be resolved by elapsed time,
because elapsed time tells you nothing about what is in the tank.

**Never:** never offer, suggest or enable the opposing pH channel as a correction
(2.2.5).

### 7.4 F-CHECK-NO-MOVEMENT and F-CHECK-WRONG-DIRECTION

**Raised by:** a closed window with the corresponding outcome (6.2).

**What they stop:** the batch. It stops and tells the operator, who decides
(2.2.1). Remaining doses are marked `NOT COMMANDED`.

**What clears them:** operator acknowledgement, with the outcome and the bounds on
screen at the moment of acknowledging, recorded with it. The forward path is a new
batch planned from scratch.

**Never:** never re-dose, never top up, never adjust a threshold in response,
never offer the opposing channel (2.2). **Never fold `INDETERMINATE` or `NOT
VERIFIABLE AT THIS DOSE SIZE` into either of these.**

### 7.5 F-FILL-ASSERTED

**Raised by:** the fill-in-progress input reading filling - which is also what a
severed cable reads as, by design (2.7.2).

**What it stops:** admission of any plan, and the start of any further dose. **A
window during which it asserted is void** (6.4).

**What clears it:** the input reading no-fill again. This one is self-clearing
because it is a permission, not a failure - **and it is the only self-clearing item
in this section.**

**Never:** never qualify it, cross-check it, time it out, or treat a suspiciously
long "filling" as suspect. **Every one of those is logic added to compensate for a
contact, and none of them makes a severed cable safe** (T-016).

### 7.6 F-PROBE-READ

**Raised by:** the failure to obtain a required reading from an EZO circuit.

**What it stops:** any verification claim that depends on that probe. **Open
windows depending on it close as `INDETERMINATE` with the reason recorded.** It
does not by itself stop the water system, which runs without the Pi (2.4.6).

**What clears it:** readings resuming, plus the operator acknowledgement of any
window it voided. Windows it voided stay void.

**Never: never interpret a missing reading as "no movement".** That is the absent
outcome read as a verdict (2.3.5). Never substitute a last-known value. Never
back-fill a gap.

### 7.7 F-INCOMPLETE-RUN

**Raised by:** any run that turned a head and did not complete - a dose, a prime,
a purge, an operator test, a C-09 trace, and **most sharply a C-01 calibration
run** (2.3.4).

**What it stops:** the use of that run's result. **A calibration run that did not
complete is DISCARDED, never scaled.** A calibration cut short and recorded as
complete corrupts the figure every dose in this system divides by, and nothing
downstream notices (F-016).

**What clears it:** re-running the procedure from the start.

**Never:** never pro-rate, never estimate, never mark a partial run as complete
because the numbers look plausible.

### 7.8 F-JUG-LOW

**Raised by:** a computed remainder below the operator-entered warning level
(section 10, owner input).

**What it stops:** nothing on its own; it is a warning. **Whether it blocks a plan
whose commanded volume exceeds the computed remainder is not decided** - see
section 11.

**What clears it:** a jug change with the poured volume re-entered (5.5.5).

**Never:** never let it be silently satisfied by an operator typing a delivered
volume into the arithmetic. Never present a remainder that carries interruptions
without its flag (5.5.4).

### 7.9 Recovery from F-DROP, and the preconditions before anything is commanded again

**Between the drop and the reset:** the fault is latched and does not self-clear;
sampling and logging continue, including the readback, so the log shows how long
the permissive was open and whether it chattered - **which is the only place
evidence of an intermittent contact ever accumulates**; nothing is commanded on any
channel; the coil command is held dropped; and **no resume, retry or continue
action exists anywhere.**

**One thing that must not be displayed: "press reset now", as if the application
knew a reset would take.** The chain may still be tripped, a leak still wet, an
E-stop still latched, and the Pi has no input for any of it. The correct message
names only what software sees - the readback is open - and asks the operator to
clear the condition and reset, without naming which condition.

**All of the following must hold before anything is commanded again, and "the
readback came back" is not one of them by itself:**

1. **Readback qualified closed and stable** over an interval long enough to expose
   an intermittency. Necessary, not sufficient.
2. **Command and readback agreeing in BOTH directions, tested deliberately** - the
   weld test, run while the operator is standing there. **Flagged and not specified
   as buildable: that test commands the coil, which re-energises eight drivers
   whose enable defaults on.** Whether it is safe to run automatically is what
   C-18 observes (section 11).
3. **An explicit operator acknowledgement per interrupted dose, with the bounds on
   screen at the moment of acknowledging, recorded with it.** Not one global OK.
4. **Any open pH attribution window resolved by the operator** (7.3).
5. **The batch is not resumable.** The forward path is a new batch, planned from
   scratch, by a person who has seen the bounds.
6. **No latched weld fault outstanding** (7.2).

**Deliberately not required: proof that the drivers are powered. None exists.** The
application proceeds on commanded-plus-readback and says so.

### 7.10 What a fault and a record REQUIRE of a screen

This is the whole of what this document says about screens. The UI is HELD.

A fault presentation must carry:

- **The channel token**, character-identical to the wall (3.5).
- **All three bounds, and in plain words: the delivered amount is somewhere
  between the floor and the ceiling, and nothing in this system can measure it.**
- **That the jug was decremented by the ceiling, and why that direction was
  chosen.**
- **That the batch is stopped, that no part of it will be re-issued, and that the
  reset button will not resume anything.** Stated explicitly, because the
  operator's reasonable expectation of a reset button is exactly the opposite.
- For a permissive event, **two labelled facts and no synthesis**: what was
  commanded, and what the readback reads.
- The outcome by name, including `INDETERMINATE` and `NOT VERIFIABLE AT THIS DOSE
  SIZE` as themselves.

A fault presentation must NOT carry:

- **A progress bar or any delivered-fraction percentage** (2.3.2).
- **A cause** for a permissive drop (4.4).
- **Any claim about the drivers' power state** (2.3.1).
- **Any control that re-doses, resumes, tops up, or offers the opposing pH
  channel** (2.2).

---

## 8. Durable state

**The governing rule: a marker is written BEFORE the action it covers, never
after.** This direction is forced, not a preference (5.5.3).

### 8.1 What must survive, and why each

| Item | Why |
|---|---|
| **A clean-shutdown marker** | Its absence on boot is the only way software learns a cut happened. **Everything else is useless without it** |
| **The batch plan, written before the first step** | So the pH attribution guard can be re-evaluated on restart against what was intended |
| **A per-channel intent record, written before stepping**: token, commanded volume, commanded step count, and the C-01 figure and C-17 configuration used | Written on completion instead, a cut mid-dose leaves no record the channel was touched and the jug arithmetic under-books |
| **A progress marker, written AHEAD of the steps it covers** | It makes the book a ceiling on what was delivered, never a floor (5.4, 5.5) |
| **The settle window state**: open or closed, which channel, baseline value and spread, when taken, earliest valid read | Lose it and a restarted system cannot tell it is standing inside an open window, and may command an opposing pH dose into it |
| **The verification outcome slot, explicitly set** | Never absent (2.3.5) |
| **The permissive command and readback state, plus raw sample trails around transitions** | So a welded contact is not forgotten across a restart, and so intermittency leaves evidence |
| **Fault state, including every latch** | Faults accumulate and survive restarts (7) |
| **Jug remainders, and the interruption flag per channel** | G-05 arithmetic is the only record of jug contents that exists |
| **The watchdog reset count** | Otherwise reboot-hang-reboot looks like uptime |
| **The channel register's attributes as the application read them, and which C-01/C-17 figures are void** | So a voided figure cannot be silently revived by a restart |

### 8.2 Write ordering within a batch

1. Batch plan, durable → then admission may pass.
2. Dose intent record, durable → then the first step of that dose may be issued.
3. Progress marker for the next chunk, durable → then that chunk's steps may be
   issued.
4. Dose close with bounds and provenance, durable → then the jug decrement, durable
   → then the window opens for evaluation.
5. Outcome, durable → then the batch may proceed to the next dose or close.
6. **Screen last, always.** The screen is reconstructible from the record; the
   record is not reconstructible from the screen.

### 8.3 Write-ahead granularity

**It is a real parameter and nobody has stated it.** Coarse chunks over-book more
per interruption; fine chunks over-book less at the cost of a durable write per
chunk. **Both directions are safe under G-05, so it is a wear and throughput trade,
not a safety trade.** But the width of the ceiling in millilitres is set by steps
per millilitre, which does not exist until C-17 and then C-01. **It is chosen after
C-01, not before** (section 10).

### 8.4 What survives what

| Event | What survives | What is destroyed |
|---|---|---|
| **Permissive drop, Pi alive** | Everything, witnessed. Bounds are latched in memory and written | Every open window; the batch object |
| **Panel power lost, Pi alive** | Same as above from the application's point of view: it sees the readback mismatch and nothing more (4.4) | As above |
| **Pi power lost** | Only what was durably written before the event, marked `RECONSTRUCTED FROM WRITE-AHEAD ON RESTART` | Everything in memory. Any window open at the cut |
| **Watchdog reset** | Durable state, plus an incremented and surfaced reset count | Any window open at the reset, **recorded as DESTROYED BY RESET, never as a gap in the trace.** A gap looks like nothing happened |
| **Clean shutdown** | Durable state plus the clean-shutdown marker | Nothing that matters, provided no dose was in flight; a dose in flight makes it a drop (7.1) |

---

## 9. Startup, shutdown, watchdog, recovery

### 9.1 Startup

The boot state is fixed, with its conditions folded in: **the permissive coil
command is DROPPED, no channel is commanded, and arming is a human act.** The
application does not command the coil as part of coming up, on any path, including
after a watchdog reset.

Then, in order:

1. **Read the clean-shutdown marker.** Absent means a cut happened; that is the
   only way this is learned.
2. **Reconstruct from durable state**, marking every reconstructed bound with its
   provenance (5.4).
3. **Void every window that was open**, with `INDETERMINATE - POWER LOST` or
   `INDETERMINATE - RESET`. **A window spanning a restart is void and not
   resumable**: the baseline is stale and the mixing history is unknown. If the
   whole panel lost power, circulation stopped and the dose did not mix; if only
   the permissive dropped, circulation may have continued. **The application cannot
   distinguish these cases and must not pretend to** (4.3, 4.4).
4. **Re-raise every latched fault**, including a weld.
5. **If a pH attribution window was open at the cut, refuse the opposing pH channel
   until an operator resolves it** (7.3).
6. **Present the bounds of any dose that was in flight and require an explicit
   operator decision.** Never auto-resume: resuming means delivering a remainder
   computed from an executed fraction that is unknown, and nothing can check the
   result (2.2.3).
7. **Elapsed time across a restart is not computed** unless the display box
   provides a clock that survives a power cut. That is a DISPLAY-BOX fact adjacent
   to S-12 and it is not settled here (section 11). **Until it is answered, a
   window spanning a restart is void rather than have an untrustworthy elapsed time
   computed for it.**

### 9.2 Shutdown

**Ordinary shutdown drops the permissive.** It is the normal path, several times a
day (7). On a clean shutdown with nothing in flight: stop commanding, drop the coil
command, write the clean-shutdown marker last. On a shutdown with a dose in flight,
the F-DROP sequence applies in full (7.1) and the severity is informational only
if the application commanded the drop AND nothing was in flight.

### 9.3 The watchdog

**What it is for: recovering a HUNG Pi**, because nothing in the panel can power
cycle it and it reboots by software or by killing the panel (2.4.5). Its mechanism
is DISPLAY-BOX's; **the feeding discipline is this application's and it is what
decides whether the watchdog is real:**

> **It is fed from the loop whose death matters - the sequencer and state loop -
> and NEVER from an independent timer thread. A watchdog kicked by a timer that
> keeps ticking while the sequencer is wedged is a check whose condition is
> effectively a literal True: it passes forever and hides exactly what it names**
> (D-033, T-014).

**What the watchdog must NOT do:**

1. **It must not be presented as stopping motion.** A reset takes time and nothing
   controls the outputs during it. **Its coverage of a runaway dose is ZERO and it
   must never be recorded as a mitigation for one.** Safety is the permissive, in
   hardware.
2. **It must not resume anything on reboot.** G-16 has no crash exemption.
3. **It must not treat the fraction delivered across a reset as zero.** Assume the
   driver was enabled throughout and bound the volume as in 5.4. **A naive watchdog
   reset mid-dose is survivable ONLY because write-ahead already put the ceiling on
   disk.** Without it, every watchdog reset silently under-books, which is the
   direction that runs a jug dry.
4. **It must not carry an open settle window across the reset** (8.4).
5. **It must not trigger on a fault.** Faults stop and tell a human. A watchdog
   that reboots to clear a fault erases the state and converts a loud stop into a
   silent restart. **Liveness only.**
6. **It must not loop silently.** The reset count is durable and surfaced.
7. **It must not come up with the permissive coil commanded** (9.1).

---

## 10. The numbers this application needs, and where each comes from

**Every row names a source. No row states a value.** A figure that arrives without
a measurement behind it is not a figure.

| # | Number | What it is for | Source | Status |
|---|---|---|---|---|
| N-1 | Millilitres per revolution and per step, per channel, **measured against real back pressure into the running manifold** | The conversion from volume to step count. The manufacturer's figure is at no back pressure, so the real figure is lower by an unmeasured amount | **C-01**, owner measures | Not measured. Blocks all commanding |
| N-2 | The as-set microstep configuration, per driver, **set by pins** | The middle term of steps per millilitre. It is a setting, not a property | **C-17**, PUMP-BOXES sets, owner records | Not recorded. Blocks N-1 |
| N-3 | Motor steps per revolution | The first term of steps per millilitre | PUMP-BOXES, from the motor, via the owner (G-15) | Not on file |
| N-4 | `t_first` and `t_settle`, the settling times | The settle phase and the window ceiling | **C-02**, owner measures, procedure in `subsystems/dosing-f004-wet-side.md`. Measured, not derived | Not measured. Blocks all verification (D-012) |
| N-5 | pH and EC noise and drift band on this build | The band every verdict is compared against. **The drift half is load-bearing, not advisory, because the pH check is signed** | **C-08**, owner measures, in situ, over a window at least as long as the settling interval. **First in the measurement order** | Not measured |
| N-6 | Signed pH step per dose, pH up and pH down **separately** | **The reference SIGN for the direction check.** It comes from this measurement and never from a product name | **C-03**, owner measures, after C-08 then C-02 | Not measured |
| N-7 | EC step per dose, per EC-moving channel | Turning a measured EC change into a verdict | **C-04**, owner measures, after C-08 then C-02 | Not measured |
| N-8 | Loop turnover time | **A FLOOR for N-4 only**, useful for rejecting an obviously-too-short setting. One turnover is not mixing to homogeneity, and the multiplier between them is a property of this tank that no agent will quote | **C-07**, owner or derived by WATER | Not measured. **Never a substitute for N-4** |
| N-9 | Circulation flow under service conditions | Feeds N-8 | **C-10**, owner, method in `subsystems/water-s18-f003.md` | Not measured |
| N-10 | Day tank working volume and the fill band, both ends | The condition N-4 is stated at. **A settling figure without its level condition is not usable, because software has no way to notice when the condition stops holding** (4.4: there is no level input) | **C-11**, owner, with WATER stating what sets each end | Not measured |
| N-11 | Poured full-jug volume, per channel | The only input to jug arithmetic (G-05) | **Owner, at fill time.** **Not the register's seed column and not a container capacity** (G-33, T-018) | Entered per fill |
| N-12 | The low-remainder warning level | Raising F-JUG-LOW | **Owner input.** Nothing on file states one, and no default may be seeded | Not set. Section 11 |
| N-13 | The margin by which a predicted change must exceed the band to be claimed | Separating `PASS` from `NOT VERIFIABLE AT THIS DOSE SIZE` | **Derived at commissioning from N-5 with N-6 and N-7**, then confirmed by the owner. It is a policy on measured data, not a measurement | Not set. Blocked on N-5, N-6, N-7 |
| N-14 | Readback qualification length for the DROP direction | 7.1's "qualified over consecutive samples" | No measured contact behaviour exists. **Bounded by a rule instead: it may never be lengthened to silence nuisance stops** (2.5.7). The WELD direction needs no number: it is one sample | Not set. Section 11 |
| N-15 | Write-ahead granularity | 8.3 | **Chosen after N-1**, because the width of the ceiling in millilitres is set by steps per millilitre | Not set, deliberately |
| N-16 | Watchdog timeout, and whether an external reset input exists at all | 9.3 | **DISPLAY-BOX** owns the mechanism; **C-20** watches it fire and confirms it does not loop silently | Not set |
| N-17 | Probe sampling interval | Baseline spread, window sampling | Not on file. It interacts with N-5, which is measured over a window, so it is set with N-5 and not before | Not set |
| N-18 | Pin assignments and I2C addresses | Every input and output in section 4 | **S-12**, DISPLAY-BOX proposes, BOSS freezes | OPEN. Nothing may be built against it |
| N-19 | The EZO circuits' interface mode, per circuit | Reading any probe at all. The circuits ship in a mode that must be changed, by a procedure that differs per circuit type | **C-14**, owner, recorded per circuit individually | Not done |
| N-20 | The eight token colours | The colour axis of the token | **Owner, via DOSING**, a material availability question (G-15). One colour per token, bound once, in one table | Not bound. Blocks nothing but permanent carriers |

**Numbers this application must never hold:** a manufacturer's no-back-pressure
delivery figure; an assumed microstep factor; a placeholder settling time; a
seeded jug volume treated as a capacity or a poured volume; any figure copied from
a configuration file, a template or a fixture and cited as a measurement (2.3.6).

---

## 11. What cannot be specified yet, and the blocker for each

| # | What is not specified | Blocker |
|---|---|---|
| 11.1 | **Any binding of a function to a pin or an address** | **S-12 is OPEN.** DISPLAY-BOX proposes and BOSS freezes. Nothing is built against an OPEN row |
| 11.2 | **Any pass-or-fail verification logic at all** | **C-02 does not exist** (D-012). And by the same standard: C-08, C-03 and C-04 do not exist either, and the detectability margin rests on all three. **None of these is estimated here** |
| 11.3 | **Any dose commanding** | **C-17 then C-01 do not exist.** A steps-per-millilitre figure may not be assumed even as a placeholder: nothing downstream measures it, so a wrong number is invisible until plants die |
| 11.4 | **Whether the application gets any circulation-related input at all** | **S-20 is OPEN and blocked on S-05.** And a level-based S-05 forecloses circulation verification permanently (D-060). Claim B in 6.4 stands or falls here; claim A does not depend on it |
| 11.5 | **Sample tagging with chiller state**, as D-027 requires | **S-18 is OPEN**, and what energises the chiller contactor coil is unaccounted for anywhere in the project (D-064). D-027 is specified and unimplementable; the field stays empty rather than inferred |
| 11.6 | **Any positive confirmation that a settle window was valid** | **Structural, not pending.** There is no flow signal (D-007) and nothing commands or observes circulation (D-091, G-26). This is not waiting on a decision; it is a property of the design, and 6.4 states what is possible instead |
| 11.7 | **Whether an `INDETERMINATE` outcome stops the remainder of a batch** | **A decision nobody has made.** G-16 speaks only of "no movement". Both readings are consistent with the frozen rules and the difference is operational. **Owner's, and this document will not make it** |
| 11.8 | **Whether F-JUG-LOW blocks a plan whose commanded volume exceeds the computed remainder** | Same class as 11.7, plus N-12, which nobody has set |
| 11.9 | **Elapsed-time arithmetic across a restart** | **Whether the display box provides a clock that survives a power cut** is a DISPLAY-BOX fact adjacent to S-12, and it is unanswered. Until then, a window spanning a restart is void (9.1.7) |
| 11.10 | **Whether the weld test may be run automatically at recovery** | It commands the coil, which re-energises eight drivers whose enable defaults on. **C-18 is the measurement that observes this state and the reset transient**, and running C-18 is itself the decision to accept an uncharacterised state once, under observation (D-070, D-093). Until C-18 is run, the test is operator-initiated only |
| 11.11 | **What a driver does with a step asserted and motor supply absent** | The datasheet neither allows, forbids, sequences nor characterises it (D-070). **C-18 observes it.** The handler's first action - stop the step generator - holds regardless of the answer, which is why the fault model proceeds (D-093) |
| 11.12 | **Whether any Pi application already exists, and what its fault registry contains** | **S-14 is OPEN and UNVERIFIED.** A full search on 2026-08-30, recorded in `subsystems/control-software.md`, found no Pi application source in reach - not in the tree, the history, the remote, the machine or this conversation. **That is not a claim the project has no code.** If code exists, it is checked against this document; this document does not describe it |
| 11.13 | **Language, framework, persistence medium, and how the application is hosted** | Not chosen. **Section 8 states durability requirements independently of the medium**, so the choice does not block the rest |
| 11.14 | **Every screen** | **HELD by the owner** until the fault behaviour is settled. Sections 3.5 and 7.10 state what a record and a fault REQUIRE of a screen. Nothing else about the UI is written, and no agent asks for the requirements |
| 11.15 | **Which product sits on which token, and the token colours** | **Deliberately unassigned until commissioning** (D-077). C-09 binds a token to a product with the jugs present. The application carries product as an attribute it is given, never as identity, and never as the source of an expected sign |
| 11.16 | **A narrower floor than zero on delivered volume** | Nothing on this build can narrow it. If a per-driver indication that requires actual commutation ever lands at the Pi it becomes the only candidate, and **even then the book decrements the ceiling** - a second counter that can silently disagree with the commanded count must not become the booked one |

---

## 12. Status

**This document is PARTIAL, and it is partial in a specific and stated way.**

**Complete and implementable today, against the frozen rows:** the scope
boundaries; the frozen rules as constraints; the channel model and everything the
token requires of code and records; the I/O surface including what cannot be
commanded and cannot be observed; the dose model - objects, plan admission,
sequencing, the bound structure, booking, and the prohibitions; the phase structure
and outcome sets of the verification model, including direction-awareness and the
separation of the fifth outcome; the whole fault model including the ordered
permissive-drop handler, the asymmetric readback discipline and the recovery
preconditions; durable state, its write ordering and what survives what; startup,
shutdown and the watchdog's feeding discipline and prohibitions.

**Not implementable, with the blocker named:** every item in section 11, and every
row in section 10 whose status is "not measured" or "not set".

**Structurally impossible rather than pending, and it should not be read as a gap
waiting to close:** positive confirmation that a settle window was valid (11.6),
attribution for six of the eight channels (6.6), and any measurement of delivered
volume (2.1.1).

**One correction this document makes to a prior return of my own:** the
window-validity precondition in `subsystems/control-software-f004.md` is withdrawn,
because the premise that the Pi commands the circulation relay was removed by G-26
and D-052 (F-070). Section 6.4 states what replaces it and what cannot be replaced.

**One thing I have not verified and am not asserting:** whether an implementation
already exists on the Pi, on the owner's machine, or in a repository outside this
session's reach. S-14 stays OPEN. This document is written as a specification to
build to and to audit against, not as a description of anything that runs.

**I am not finished.** Per agents.md rule 7, that is BOSS's call after another
agent has built against this and found nothing, and the physical half of that
begins at C-09.
