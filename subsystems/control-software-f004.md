# CONTROL-SOFTWARE on F-004: the software side of the delayed check

Returned 2026-08-30. Nothing decided, no code written, no file it owns changed.
It reported stopped part-way and did not declare itself finished. Read
findings.md F-004 and interface rows S-15 and S-16 first.

## A dose is five phases, and the software holds a state for each

| Phase | What happens | Note |
|---|---|---|
| 1 Baseline | Sample the probe with the loop circulating and no dose in flight. Record a value AND a spread | One number is not enough. Without a spread there is no way to tell moved from drifted, and every later comparison is unanchored. The baseline must be taken under the same conditions as the read |
| 2 Command | Steps issued for exactly one channel. The volume is booked as dispensed here, because G-04 leaves nowhere else to book it | |
| 3 Settle | Last step to earliest-valid-read | This is the window defined by the number nobody has |
| 4 Read | Sample over a window, not at a point. Compare against baseline plus spread | |
| 5 Decision | Pass, fail, or INDETERMINATE. Three outcomes, never two | A two-outcome evaluator is the defect F-004 describes: "not yet arrived" has nowhere to go and lands in whichever bucket is the default |

## What the software must not do inside the settle window

This list is the real deliverable, more than the phase list.

1. **No automatic re-dose, top-up, retry or correction on the strength of "no
   movement yet".** CONTROL-SOFTWARE calls this the single most dangerous thing
   this software can do: it turns a healthy dose into a double dose, G-04 means
   nothing measures the excess, G-05 means the jug arithmetic books only what was
   commanded, and the tank and the books diverge in a direction nobody can see.
   Every other error in its answer is recoverable. This one is not.
2. No pass or fail evaluation inside the window, and a flat reading inside it may
   not raise a dose failure or a circulation fault. T-005 as a code rule.
3. No dose on another channel whose attribution would land in the same read
   window. G-06 stops two heads turning together. It does not stop channel B
   starting a second after channel A stopped, and at the probe those two doses
   are simultaneous.
4. No re-baseline, zero or re-reference mid-window.
5. No window treated as valid if a day tank fill asserted during it. A fill
   dilutes the tank and drags EC and pH toward the makeup water, which is
   indistinguishable from a dose that failed. This is one of the two things the
   fill-in-progress contact is actually for. S-03 is OPEN so this is specified,
   not buildable.
6. No batch declared complete at last-step. A batch ends at last-read. If the UI
   or the log closes the batch when the pumps stop, every verification is
   orphaned.

## Two preconditions the software can assert, and the residue it cannot

The Pi commands the circulation relay, S-09, so it can require circulation
commanded on for the whole window and void the window otherwise. The residue is
F-001 limit 1 and F-003: commanded on is not running, and nothing confirms the
difference.

The chiller is raised as a question, not decided: chiller cycling moves tank
temperature and temperature moves both the pH and the EC readings, so a chiller
cycle inside a settle window is a contaminant. Whether to hold the chiller off
across settle windows is a process trade, temperature excursion against read
cleanliness, and belongs to the owner and WATER. Recorded as interface S-18.

## The read trigger should be a floor, a stability test, and a ceiling

Reading on a bare timer is fragile. Reading on stability alone is a trap, because
a dose that never arrived is also perfectly stable. So: before the floor,
stability means nothing; between floor and ceiling, stability triggers the read;
past the ceiling, the result is indeterminate rather than fail. This reduces
sensitivity to getting the floor exactly right. It does not remove the need for
it, and it adds a noise band as a third number.

## Which direction of error is worse: too early, and not close

| Direction | What it costs |
|---|---|
| Too early | A healthy dose scored as a failure. If failure triggers automatic remediation it becomes the unmeasurable overdose above. If it triggers stop-and-tell, it costs a nuisance stop and, over time, credibility: an operator who learns the check cries wolf stops reading it or switches it off, and the free check D-009 was worth freezing is gone. A quieter version: an early read whose result is discarded but whose sample is retained poisons the next baseline |
| Too late | The signature degrades into drift, and the day tank is open-topped so pH drifts with gas exchange regardless of dosing. The window gets easier to contaminate. Batch time grows, and if O-01 time-slicing is adopted it multiplies by the number of channels checked. It does not produce a confident wrong answer, it produces indeterminate |

Too early is worse for three reasons: it yields a wrong answer wearing the
costume of a right one, which is the "verification worse than none" shape of
F-004 and T-005; its natural in-software remedy creates a condition G-04
guarantees nobody can detect or reverse; and it is worst on exactly the two
channels S-16 attributes, where an unintended extra dose is a process excursion
into water that goes downstream of V3.

The bias runs late. But the way that bias is expressed is not "pick a generous
number", it is D-012 as written: with no measured interval, no pass or fail
evaluation ships at all. A guessed-long placeholder is still a guess and is
invisible until it is wrong.

Note the loop: an over-conservative figure makes batches long, the predictable
human response is to shorten the settle time, and that reintroduces the early
read through the back door. Too late becomes too early by way of impatience.

## The input has two axes, not one number

**Axis one, time. ONE interval, a property of the loop, not of the channel.**
All eight ports inject into one manifold and everything lands in one tank, so
transport plus mix is common to every channel and every dose size. A tiny dose
does not mix into a 40 gallon tank appreciably faster than a larger one. Eight
figures would be eight measurements of the same thing.

That figure carries a condition that must not be dropped. If the interval varies
with day tank level, software cannot adapt, because per G-01 and G-02 the only
level input in existence is a dry contact saying a fill is in progress. Software
cannot know the level. So either the figure is stated as the worst case at the
fullest level the tank operates at, or the batch procedure fixes the starting
level and the figure is stated for that level. A figure without its level
condition is not usable, because software has no way to notice when the
condition stops holding.

**Axis two, magnitude. Per channel, and a RULE, not a lookup table.**
Verification is claimed only when the predicted change for the commanded volume
exceeds the noise band by a stated margin. Below that the correct result is "not
verifiable at this dose size", a third outcome and not a failure. Small trim
doses will land under the band, and a system that scores them as failures will
fail constantly on the doses that matter least.

**The shape the answer must arrive in to be usable:**

1. One settling interval, with the conditions it holds under stated: day tank
   level, circulation commanded and running, which injection port, loop
   otherwise undisturbed.
2. Whether it was derived or measured. A derivation from tank volume and loop
   flow gives one turnover, and one turnover is not mixing to homogeneity. The
   multiplier between them is a property of this tank's mixing and
   CONTROL-SOFTWARE refused to quote one. A derived figure is a floor, useful for
   rejecting an obviously-too-short setting. It is not the answer. C-07 feeds
   C-02 exactly this way.
3. Per-channel change per millilitre at the probe, C-03 and C-04.
4. A measured noise and drift band for pH and for EC on this build, over a window
   at least as long as the settling interval. **This was not a row on
   commissioning.md.** C-03 and C-04 require it and nothing scheduled it. Added
   as C-08.
5. Whether the interval varies with tank level, and if so the level it is stated
   at.

A bare interval with no conditions and no noise band cannot be turned into pass
or fail logic. It can only be turned into a timer, and a timer with no band is
the thing that reports healthy doses as failures.

## Enforcing S-16 constraint 1

**Where the check lives: at plan admission, before any step is commanded.** Not
at run time. A run-time check that fires when the second pH head starts has
already let the first dose into the tank, and G-04 means nothing can say how much
or undo it. The sequencer needs a batch as a first-class object with its full
commanded set known before the first step, and a gate that rejects a plan
carrying nonzero volumes on both pH up and pH down.

**The batch is the weak form of the guard.** The real exclusion domain is the
settling window. Two opposing pH doses in two consecutive batches, close enough
that the second lands while the first is still settling, produce exactly the
cancellation S-16 describes. So the correct rule is: no opposing pH dose while a
pH attribution window is open, and that window extends past the pump stopping by
the settling interval. Constraint 1 therefore cannot be fully enforced until C-02
arrives. Only the batch-scoped form is buildable today.

**Does G-06 help? Barely, and not where it matters.** Serialising the pumps makes
"attribute whichever was commanded" well-defined at the pump end. It does nothing
at the probe end: because the probe reads the tank after mixing, two doses
separated by seconds at the head are simultaneous at the probe. The observable is
not serialised even though the actuator is. G-06 is a genuine verification asset
for measurements taken in the manifold, at the head or on the suction side, which
is how DOSING used it. It does not survive the trip to the tank, and S-16's whole
subject is the tank.

**What the fault logic must do.** Gate the evaluator on a precondition that
short-circuits before any comparison is computed: exactly one pH-moving channel
commanded in this window, or emit fault and compute nothing. The dangerous
implementation computes the movement, finds it in the expected direction, scores
a pass and then tries to override it, because the net of an up and a down dose
can easily fall in the expected direction and an override that is a later step in
the code is an override somebody can remove. "Must not read as passing" is
satisfied by never producing a pass value, not by suppressing one.

The fault is a distinct state, not a failed check: "invalid, not attributable",
plus a fault. A plan-level violation blocks the batch from starting and is
cleared by fixing the plan, not by acknowledging an alarm mid-run. A violation
detected mid-run aborts the batch and records pH as indeterminate for that batch
permanently, because G-04 means it can never be reconstructed.

**Edge cases the enforcement creates**

| Case | Rule |
|---|---|
| What counts as fired | Commanded steps greater than zero, not "the recipe names the channel". A zero-volume entry is not a violation. A dose too small to exceed the noise band still counts as fired: it still moves pH even though it cannot be attributed. The guard is on commanding, the band is on detectability, and the two thresholds must not be conflated in code |
| Partial doses | A dose cut short by a permissive drop delivered an unknown fraction. It counts as fired and it poisons the window |
| Doses that do not look like doses | Priming a pH line, a purge, an operator single-channel test, a C-01 calibration run. Every one turns a pH head and puts product in the loop. All pass through the same guard and all open or poison the window. This is the case most likely to be missed, because the UI will call them something other than "dose" |
| Overshoot correction | The obvious fix for an overshot pH down is a pH up, which is the forbidden pattern if it lands in the open window. Reversal is legitimate only after the window closes and a fresh baseline is taken, and the corrective logic must be structurally incapable of reversing sooner |
| Restart with a window open | If pH up was in flight when power dropped, the software must know on restart that a pH window was open with unknown content, and must refuse pH down until an operator resolves it |
| Fulvic | Unattributed per D-013 and not solved. The only requirement is negative: a fulvic dose must not reset or re-baseline an open pH or EC window |

## State that must survive a power cut mid-settle

Two cases behave differently and both must be handled. The permissive removes
driver power, P-06 and G-09; whether the Pi itself stays up depends on P-07,
which is OPEN. If the permissive drops and the Pi stays up, the software sees the
G-09 readback mismatch and knows the step index at which commanding stopped, but
not how many of the last steps executed, so it holds an upper and a lower bound
and the truth is between them. If the Pi goes down too, only what was durably
written before the event survives.

What must be written, and written BEFORE the action rather than after:

| Item | Why |
|---|---|
| A clean-shutdown marker | Its absence on boot is the only way software learns a cut happened. Everything else is useless without it |
| The batch plan, before the first step | So the S-16 guard can be re-evaluated on restart against what was intended |
| A per-channel intent record before stepping: channel, commanded volume, step count, and the calibration figure used | Written on completion instead, a cut mid-dose leaves no record the channel was touched and the jug arithmetic under-books |
| A progress marker written AHEAD of the steps it covers, never behind | This direction is forced, not a preference. Writing ahead makes the book a ceiling on what was delivered, never a floor. Given G-05, over-booking makes the operator change a jug earlier than needed, which is annoying and safe. Under-booking runs a jug dry and draws air, which is DOSING's failures d and e, invisible, at the worst moment |
| The settle window state: open, which channel, baseline value and spread, when taken, earliest-valid-read | Lose it and a restarted system cannot tell it is standing inside an open window, and may command an opposing pH dose into it and silently violate S-16 |
| The verification outcome slot, explicitly set to indeterminate-power-lost | Not left absent. An absent outcome read later as "no failure recorded" is passing by default, the same defect as the override above |
| The G-09 permissive command and readback state | So a welded contact is not forgotten across a restart |

Restart rules that follow:

- Never auto-resume a partially delivered dose. Resuming means delivering a
  remainder computed from a step count whose executed fraction is unknown, and
  per G-04 nothing can check the result. Present the bounds, require an explicit
  operator decision.
- Any settle window open at the cut is void, not resumable. The baseline is stale
  and the mixing history is unknown: if the whole panel lost power, circulation
  stopped and the dose did not mix; if only the permissive dropped, circulation
  may have continued. The software commands the circulation relay so it knows
  what it asked for. It does not know whether the relay had power, cannot always
  distinguish these cases, and must not pretend to.
- Elapsed time across a restart is the quiet problem. Whether the display box
  provides a clock that survives a power cut is a DISPLAY-BOX fact adjacent to
  S-12, and CONTROL-SOFTWARE asserted nothing either way. Until it is answered, a
  window spanning a restart is void rather than have an untrustworthy elapsed
  time computed for it.

## Blocked, with the number and the source named

| What is blocked | Number needed | From |
|---|---|---|
| Any pass or fail verification at all, per D-012 | Settling interval C-02, with its tank-level condition | Owner measures. DOSING says what sets it. C-07 feeds it as a floor |
| The window-scoped S-16 guard, the form that actually works | C-02 | as above |
| Turning a measured change into a verdict | Per-channel change per millilitre, C-03 and C-04 | Owner |
| The noise band those verdicts are compared against | pH and EC noise and drift on this build, over a window at least as long as the settle interval | Owner. Added as C-08 |
| Commanding any dose at all | Steps per millilitre, C-01 | Owner |
| Whether a fill can invalidate a settle window in practice | S-03, and whether dosing during a fill is permitted | Owner. Row is OPEN |
| Anything with a pin or an address in it | S-12 | DISPLAY-BOX proposes, BOSS freezes |
| Interval arithmetic across a restart | Whether the display box has a clock that survives power loss | DISPLAY-BOX |

## Answerable now, and answered

The phase structure and the prohibition list. The three-outcome result. The
plan-time S-16 guard in its batch-scoped form. The write-ahead and over-book
direction for durable state. The void-on-restart rules. The separation of the
time axis from the magnitude axis.
