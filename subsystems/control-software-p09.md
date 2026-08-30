# CONTROL-SOFTWARE on P-09: the software half of a permissive drop

Returned 2026-08-30, fourth pass. No file changed, no code written. Reported
stopped part-way and did not declare itself finished. Nothing here is buildable:
P-09, S-07 and S-08 are all OPEN.

## The framing, which changes the priority of everything below

The permissive chain drops on a leak, an E-stop or a lost interlock. **Its two
named non-fault users are the manual reset and ordinary shutdown.** So this
handler runs on the NORMAL path, probably several times a day, most often with
nothing in flight. **It is not an exception handler.**

A handler that raises a loud fault every time the operator shuts the skid down
gets the same treatment F-004 predicted for a crying-wolf settle check: the
operator stops reading it. The resolution is a SEVERITY split and never a RECORD
split. The record written is byte-identical either way.

## What the software does, in order

Order is by irreversibility: stop widening the unknown, capture the bounds, make
them durable, poison everything derived from them, then tell the human.

| # | Step | Why here |
|---|---|---|
| 1 | **Stop the step generator**, in software, at the source, for the channel in flight | Not "ask the driver to stop": there is no such request. EN is unwired and defaults ENABLED, so **the Pi holds no disable line.** Under P-09 case B the driver still has logic supply and is still listening, so every pulse after this instant is a pulse into a driver in an unknown state and widens the ceiling on a dose nothing can measure. First because its cost grows with delay |
| 2 | **Latch the bounds in memory, atomically:** commanded, ceiling, floor | commanded = what the plan asked. ceiling = the write-ahead marker already durable. **floor = zero today. Not "steps issued minus a few". Zero, until PUMP-BOXES returns something that narrows it.** The step index at the halt is evidence, not a delivered figure: it is a commanded count and parts.md forbids presenting it as measured |
| 3 | **Close the dose record durably** as TERMINATED-BY-PERMISSIVE. Never COMPLETED, never FAILED | Carries all three bounds plus provenance. **Decrement the jug by the ceiling NOW, not on operator acknowledgement.** An operator who walks away must not leave the book under-booked |
| 4 | **Void every open window, set every outcome slot explicitly** to INDETERMINATE - PERMISSIVE DROP | Never absent. An absent outcome read later as "no failure recorded" is passing by default, which is T-014's shape with no literal True in sight. Record whether a pH attribution window was open, because that gates recovery |
| 5 | **Abort the batch as an object.** Remaining doses marked NOT COMMANDED, a distinct state from failed | The batch object is destroyed, not suspended. **A batch that survives the event is a resume path wearing a different hat** |
| 6 | **Record the permissive event:** commanded coil state, the RAW readback sample trail either side of the transition, not just the debounced verdict, and the mismatch. Commanded circulation and chiller states alongside, per D-027 | **Do NOT record a cause.** The Pi has no leak, E-stop or interlock input. It cannot know which one opened |
| 7 | **Drop the software's own coil command and hold it dropped** | Two reasons, and the second is the non-obvious one: command and readback then agree in the safe direction so the later weld test means something; and **when the operator presses reset, the contactor must not re-close underneath a command left standing from before the fault, re-applying VM to eight ENABLED drivers at a moment nobody chose.** Re-energisation must be the consequence of a human act. Caveat: what the coil command is in series with is S-07, OPEN, so nothing may assume dropping the command removes VM by itself |
| 8 | **Do not touch circulation or the chiller** | The permissive's load is driver VM. Circulation is the tank's only mixing source and every future re-measure depends on it. Stopping it reflexively costs mixing and buys nothing. States recorded, not changed |
| 9 | **Then the UI**, last | The screen is the only step reconstructible from the log, so it must never be ahead of the durable writes. **Severity is decided here and only here, from software's own knowledge: did I command this drop, and was anything in flight.** A drop the software commanded with nothing in flight is informational. **A drop it did not command is a fault INCLUDING when nothing was in flight** - that is the leak-or-E-stop-at-rest case and the one worth waking someone for |

## How the software knows, and what that knowledge is worth

**The complete input list is one bit and one memory:** the S-08 readback as
conditioned by DISPLAY-BOX, and the Pi's own record of what it commanded at S-07.
That is all. No VM sense, no current sense, no DIAG or INDEX at the Pi, no flow,
no level beyond S-03.

| Commanded | Readback | Meaning |
|---|---|---|
| on | closed | consistent, permissive BELIEVED made |
| **on** | **open** | **this event.** Chain tripped upstream, or coil failed, or contactor failed to pull in, or the readback failed. Indistinguishable |
| off | closed | the welded case G-09 exists for, or a shorted or wetted readback |
| off | open | consistent |

**It yields a mismatch, never a cause, and nothing at all if both ends fail the
same way.**

What it cannot tell you, each a sentence software must never put on a screen:
whether VM is present at any driver (**it is the position of an auxiliary contact,
not a measurement of the load conductor; a welded main pole or an open load
conductor reads whatever the aux reads**); whether VDD is present; which upstream
element opened; whether a motor turned or how far; contact bounce, on a single
sample.

**How fast: unknown, and structurally so.** Three latencies in series, none of them
on file: contactor drop-out and aux transfer, input conditioning and filtering,
and sampling plus debounce. **So there is always a set of steps commanded after VM
vanished and before software learned of it.** That is why the answer is a bound
structure and not a number, and no amount of tightening removes it.

**The reframe that matters: detection latency here is not a safety figure.** Safety
already happened, in hardware, before software knew. That is G-07's entire point.
Faster detection buys exactly two things, fewer pulses into a VM-less driver and a
tighter floor. **It buys no safety at all and must not be argued for as if it did.**

### The asymmetric readback discipline, which is the part that decides whether S-08 is usable

F-011 says the contact may oxidise and fail intermittently. Treat the readback as
a noisy channel, and treat the two mismatch directions **asymmetrically, because
their failure costs are opposite:**

| Direction | Worst case | Discipline |
|---|---|---|
| Readback open while commanded on, an apparent DROP | A nuisance stop of a healthy batch. Loud, safe, recoverable | Qualify over consecutive samples, then act |
| Readback closed while commanded off, an apparent WELD | **Eight drivers live while software believes them dead** | **Latch on a SINGLE sample. Never clear it because later samples read open.** A long qualification here is a filter that hides exactly the failure G-09 was built to catch |

So an oxidising contact produces false stops, never missed welds. **The same
chosen direction of error as D-017**, and it should be recorded as the same choice
rather than rediscovered.

Two prohibitions that follow. **Raw samples around every transition are logged,
not just the debounced verdict** - an intermittency smoothed away leaves no
evidence and F-011 becomes unfalsifiable. And **software must not be permitted to
"solve" F-011 by lengthening its filter until the nuisance stops.** That change
also hides a real drop, it looks like tuning, and it will be proposed by whoever
is tired of the nuisance stops. The fix is at the contact.

## What the software must NEVER do

**The obvious one:** never re-dose, re-issue, resume, top up or complete the
interrupted fraction. G-16, absolute.

**And the laundered version of it: NO "RESUME DOSE" BUTTON.** A remainder computed
from an unknown fraction is an automatic re-dose with a human as its trigger. What
the operator may legitimately do is command a FRESH dose of a volume they choose,
which is an ordinary dose. **That distinction is the whole rule.**

1. Never keep clocking STEP, and never let the generator run out its planned count
   on the theory that a de-powered driver ignores it. Nothing on file says what it
   does, and the ceiling would advance by steps that certainly delivered nothing.
2. **Never claim software can make the drivers safe.** EN is unwired and
   default-enabled. There is no disable. The handler's action is STOP TALKING TO
   THEM, not shut them down, and no comment, screen or document may imply otherwise.
3. Never score the interruption as a dose failure. Failed implies nothing was
   delivered, which is the under-book direction, which runs a jug dry and draws
   air. **Interrupted is not failed.**
4. Never let the interrupted dose's window produce a pass or a fail. **The
   poisoning is durable and must survive the reset.**
5. Never re-baseline across the drop, and never carry a pre-drop baseline forward.
6. **Never auto-clear the fault when the readback returns closed.** A returning
   signal says the contactor is made. It says nothing about why it dropped or what
   is in the tank. Clearing on the return of a signal is a condition that becomes
   true by itself, T-014 without a literal True in it.
7. Never retry the coil command. It chatters a coil against a dead chain, and if
   the operator restores the chain mid-poll it re-energises eight ENABLED drivers
   at an instant chosen by a timer.
8. Never report commanded as measured. No UI element may read "drivers
   de-energised". It may read "permissive commanded: off / readback: open", two
   labelled facts.
9. Never name the cause. "E-stop pressed" on that screen is fabrication.
10. Never let this event clear a pre-existing fault, especially a latched weld.
    Faults accumulate.
11. Never leave an outcome slot absent.
12. Never restart or shorten another channel's still-open settle timer as though
    the system had been quiet.
13. Never keep the batch object alive pending reset.
14. **Never trim or roll the log for tidiness.** Those raw samples are the only
    evidence F-011 will ever leave.
15. Never stop sampling and logging. The Pi is powered independently specifically
    so it can log and alert through this. Continuing to sample is correct; using
    those samples to verify a dose is not.
16. Never reflexively change circulation or chiller commands.

## The unknown fraction: five things new to this case

Extends subsystems/control-software-f004.md. The write-ahead rule, the
ceiling-not-floor direction, the pre-step intent record, the explicit outcome slot
and the void-on-restart rules all stand unchanged.

**1. Provenance is a field, because the evidence here is genuinely stronger.**
F-004 wrote write-ahead for the case where the Pi may be down and the record is a
RECONSTRUCTION. Here the Pi is up throughout, so the record is WITNESSED. Two
record types, one book, and a later reader must be able to tell which they hold:
`TERMINATED-BY-PERMISSIVE, PI ALIVE, BOUNDS WITNESSED` and `UNKNOWN, RECONSTRUCTED
FROM WRITE-AHEAD ON RESTART`.

**2. Three numbers in the record, one decremented.** G-05 decrements the ceiling.
The record keeps all three, because the operator's decision needs the spread and a
single surviving number destroys it.

**3. Write-ahead granularity is a real parameter and nobody has stated it.** Coarse
over-books more per interruption, fine over-books less at the cost of a durable
write per chunk. Both directions are safe under G-05, so it is a wear and
throughput trade, not a safety trade. **But the width of the ceiling in millilitres
is set by steps per millilitre, which does not exist until C-17 then C-01.**
Choosing one now would be T-012's shape. Flagged as following C-01.

**4. Accumulated over-booking is corrected by a physical event, never by
software.** Repeated interruptions drift the book conservative by an unknown
amount. The channel's remaining figure is flagged as carrying interruptions so the
low-jug warning is known to be conservative rather than exact. The reset is a jug
change re-entering the user volume under G-05. **Software never corrects the book
by an estimate, and the operator is never asked to type a delivered volume** -
that guess would enter the one number G-05 treats as authoritative, and it moves
in the under-book direction. An operator's estimate belongs in a free-text note.
Never in the arithmetic.

**5. Head movement that is not a dose.** A prime, a purge, an operator test, or a
**C-01 calibration run** interrupted by a drop has the identical bookkeeping
problem and usually no batch object to abort. All pass through the same intent
record and the same ceiling booking. **The sharp one is C-01: a calibration run cut
short and recorded as if it completed silently corrupts the figure every dose in
this system divides by, and G-04 guarantees nothing downstream notices.** Findings
F-016.

## What the operator sees

Per channel, keyed by the CH token, log string character-identical to the wall.

- CHn, dose interrupted by a permissive drop, at a stated time.
- The three numbers, and in plain words: **the delivered amount is somewhere
  between the floor and the ceiling, and nothing in this system can measure it.**
  G-04 stated on the screen rather than assumed to be known.
- **NO PROGRESS BAR.** A percentage computed from step index renders a commanded
  count as a delivered fraction: the confident-wrong-answer shape, and the one
  thing a tired operator will believe.
- The jug has been decremented by the ceiling, and why that direction was chosen.
- The batch is stopped, no part of it will be re-issued, **and the reset button
  will not resume anything.** Say it explicitly, because the operator's reasonable
  expectation of a reset button is exactly the opposite.
- The check for that dose is INDETERMINATE, not failed.
- What it does not say: the cause, and any claim about the drivers' power state.

## Recovery

**Between the drop and the reset:** a latched fault that does not self-clear;
sampling and logging continue, including the readback, so the log shows how long
the permissive was open and whether it chattered, **which is the only place F-011
evidence ever accumulates**; nothing commanded on any channel, no step, no prime,
no test, no calibration; its own coil command held dropped; and **no resume, retry
or continue action anywhere in the UI.**

One thing it must NOT display: "press reset now", as if it knew a reset would
take. The chain may still be tripped, a leak still wet, an E-stop still latched,
and the Pi has no input for any of it. The correct message names only what
software sees, readback open, and asks the operator to clear the condition and
reset, without naming which condition.

**Preconditions before it commands anything again. All must hold, and "the
readback came back" is not one of them by itself:**

1. Readback qualified closed and stable over an interval long enough to expose the
   intermittency F-011 predicts. Necessary, not sufficient.
2. Command and readback agreeing in BOTH directions, tested deliberately: the G-09
   weld test, run now because the operator is standing there. **Flagged, not
   specified: that test commands the coil, which re-energises eight drivers whose
   EN default is ENABLED.** Whether it is safe to run automatically depends on P-09
   and on the shared power-up-behaviour item. Not written as buildable.
3. **An explicit operator acknowledgement per interrupted dose**, with the bounds
   on screen at the moment of acknowledging, recorded with it. Not one global OK.
4. **Any open pH attribution window resolved by the operator.** A permissive drop
   is worse than a restart in one respect: **it cannot be resolved by waiting,
   because elapsed time tells you nothing about what is in the tank.** S-16
   constraint 1 is enforced here or it is not enforced.
5. **The batch is not resumable.** The forward path is a new batch, planned from
   scratch, by a person who has seen the bounds. The only G-16-compatible route.
6. No latched weld fault outstanding.

**Deliberately not required: proof that the drivers are powered. None exists.**
Software proceeds on commanded-plus-readback and says so on the screen.

## The watchdog

**What it must do:** recover a HUNG Pi, because P-07 closes off every other route.
Its only lever is a Pi reset. The mechanism is DISPLAY-BOX's. **The feeding
discipline is CONTROL-SOFTWARE's and it decides whether the watchdog is real:**

> **It must be fed from the loop whose death matters, the sequencer and state
> loop, and NEVER from an independent timer thread. A watchdog kicked by a timer
> that keeps ticking while the sequencer is wedged is a check whose condition is
> effectively a literal True: it passes forever and hides exactly what it names.
> T-014, in the one place on this build where it costs the most.**

What it must NOT do:

1. **It must not be presented as stopping motion.** A reset takes time and nothing
   controls the outputs during it. It cannot end a runaway dose. Safety is the
   permissive, in hardware. **Its coverage of runaway dose is ZERO and it must
   never be recorded as a mitigation for one.**
2. **It must not resume anything on reboot.** Auto-resume across a watchdog reset
   is an automatic re-dose regardless of the trigger being a crash. **G-16 does not
   have a crash exemption.**
3. **It must not treat the fraction delivered across a reset as zero.** Software
   must assume the driver was ENABLED throughout and bound the volume exactly as
   above. **A naive watchdog reset mid-dose is survivable ONLY because write-ahead
   already put the ceiling on disk.** Without it every watchdog reset silently
   under-books, which is the direction that runs a jug dry.
4. **It must not carry an open settle window across the reset.** The window is
   void, and **a reset mid-window must be recorded as having DESTROYED the window,
   not as a gap in the trace.** A gap looks like nothing happened.
5. **It must not trigger on a fault.** Faults stop and tell a human. A watchdog
   that reboots to clear a fault erases the state and converts a loud stop into a
   silent restart. Liveness only.
6. **It must not loop silently.** Reset counts durable and surfaced, because
   reboot-hang-reboot otherwise looks like uptime.
7. **It must not come up with the permissive coil commanded.** Boot state is coil
   dropped, channels un-commanded, arming by a human act.

## What it needs from PUMP-BOXES, and exactly which answers move

**STEP asserted, VM absent.** If the driver latches a fault that persists after VM
returns, recovery gains a step, and **if clearing it needs a VDD power cycle the
Pi cannot do it** - a fault software can perhaps see and definitely not clear. If
it simply ignores STEP, step 1 stays first but drops from urgent to hygienic. If
VM returning with STEP asserted does something ugly, recovery gains preconditions
and the weld test may not be safe to run automatically. If clocking a VM-less
driver stresses the part, **the F-011 debounce trade reverses direction**, because
the argument above is that slower detection costs little.

**DIAG and INDEX, the biggest single lever on this answer.** INDEX, if it indicates
something requiring actual commutation, is **the only candidate on this entire
build for narrowing the floor below zero-to-ceiling.** It would not measure volume,
but it would separate "the driver did nothing" from "the driver did something",
which today is unknowable. DIAG, if it lands at the Pi, is a **per-channel,
independently-failing corroborator of the S-08 contact**, which partly de-fangs
F-011: two indications that fail differently instead of one oxidising contact.

Two cautions so neither is adopted wishfully: **if DIAG is shared or wire-ORed
across drivers it cannot attribute, and it becomes another whole-loop check with
F-001's exact limits, a new instrument with an old blindness.** And an INDEX-derived
count is a SECOND counter that can silently disagree with the commanded count;
which one the book decrements must be settled before it is used, **and the answer
must remain the ceiling.**

**Where VDD comes from decides the shape of everything above.**

| Case | What changes |
|---|---|
| A, VDD removed with VM | Drivers fully dead, STEP inert, step 1 is bookkeeping only. New problem: both supplies return together at re-energisation with EN default-enabled, so **sequencing at power-up becomes the risk**, and recovery must require the Pi's outputs in a known idle state first |
| B, VDD independent | The case posed. Logic alive, motor supply gone, driver listening, no software disable. Everything about stopping STEP is load-bearing |
| C, VDD from the Pi's own logic domain | **Pi power state and driver logic state become COUPLED, and a watchdog reset may glitch VDD across eight drivers. The reset's blast radius extends past the Pi**, and this must be stated before anything about reset behaviour is written |

**One thing does not change in any of the three: EN unwired means software has no
disable.** That single fact is why this whole answer is stop talking to it rather
than shut it down.

**A standing request: if EN is ever landed on a Pi output, CONTROL-SOFTWARE wants
to be told**, because it is the difference between a drop handler that can ACT and
one that can only ABSTAIN. Several answers get better and none get worse.
