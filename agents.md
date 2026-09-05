# Agents

Nine agents. BOSS holds the interface table and the tree, designs nothing, owns
no subsystem, and picks no parts.

| Agent | Owns | File |
|---|---|---|
| WATER | Tap to V3 wet path and the vessels | subsystems/water.md |
| DOSING | Manifold, injection, dose and suction tubing, jugs | subsystems/dosing.md |
| MAIN-PANEL | The main enclosure and every hardwired chain in it | subsystems/main-panel.md |
| PUMP-BOXES | Two boxes, heads and drivers | subsystems/pump-boxes.md |
| DISPLAY-BOX | Pi, display, EZO circuits, logic board | subsystems/display-box.md |
| CONTROL-SOFTWARE | The Pi application | subsystems/control-software.md |
| INTERCONNECT | Every cable between enclosures and out to the field | subsystems/interconnect.md |
| INTEGRATOR | Landing finished output into the shared tree | this file |
| AUDIT | Nothing. Questions only | this file |

## Rules passed to every subsystem

1. Your scope is what you own completely. Everything else is out of scope.
2. Your FROZEN interface slice is in your own file. A boundary defect is
   reported, never fixed.
3. Never state a part number or a spec from memory. Return the requirement and
   a search term and stop. The owner does all lookups and pastes the datasheet
   back.
4. Do not set counts or sizes early. A count comes back once you know what you
   need and can say why.
5. If a change costs nothing and is certain to fix a defect, make it and say
   what changed. Stop and ask if it costs money, if it is a choice rather than a
   defect, or if it would mean guessing a number.
6. Before proposing a change to shared behaviour, read what the shared source
   already does about it.
7. Report plainly whether you are finished or stopped part-way. You do not
   declare yourself finished. BOSS declares that after another agent has built
   against your output and found nothing.
8. Assert nothing from absence. "There is no X" requires having looked and
   naming what you read. Otherwise say you have not checked.
9. Nothing may be built against an OPEN row in interface-table.md.
10. **NAME THE GRADE OF EVERY IMPOSSIBILITY, per G-36.** STRUCTURAL means it
    follows from a frozen rule or from physics and no addition could change it.
    CURRENT means it follows from what has been bought, wired or decided so far,
    and **a current claim must NAME WHAT WOULD CHANGE IT.** If you cannot name
    what would change it, you have not established that nothing would. An
    unqualified "impossible" is a claim nobody can check.
11. **A CITATION IS NOT A SOURCE.** Cite the frozen row, not the document that
    quotes it. Two files where one cites the other and neither cites the source
    is a second-source illusion, and it reads as corroboration. G-37.

### BOSS's working rules. Owner, 2026-09-04. Standing.

1. **A QUESTION THAT DOES NOT BLOCK THE WORK IS NOT A QUESTION.** Log it and carry
   on. Stop only for something that changes what the machine does, or that you
   cannot proceed past.
2. **DO NOT ASK PERMISSION FOR EVERY CHANGE.** If it costs nothing and you are
   certain it fixes the problem, make it and say what you changed. Ask only about a
   real decision on how the machine behaves.
3. **ONE THING AT A TIME.** If a pass produces five things, report the one that
   matters and log the rest.
4. **DELIVER THE OUTPUT, NOT THE REASONING.**
5. **END EVERY TURN SAYING PLAINLY** whether the unit of work is finished or
   stopped part-way and needing a continue. Never ambiguous.

### KEEP IT SIMPLE. Owner's design instruction, standing. G-44, G-47, G-48.

**Simple is smart. Simple is easy to build, easy to diagnose, and easy to repair at
2am with a meter and no documentation.**

**Every part placed is a part that can fail, a part that needs a buy line, a part
that needs a step, and a part a future reader has to understand. Do not place
anything that does not need to be there.**

**That is NOT permission to under-build.** A protection that is needed is needed -
the overflow bulkhead, the high-high floats and the permissive chain all stay.
**What is barred is a mechanism added because it is INTERESTING, a check added
because a check is AVAILABLE, and a component added to close a gap that was never
going to bite.**

**WHEN YOU PROPOSE SOMETHING, SAY WHAT IT COSTS IN PARTS AND STEPS ALONGSIDE WHAT IT
BUYS. If it removes a failure mode nothing else covers, take it. If it is thorough,
do not.**

**And G-47: A COST NOBODY HAS PRICED IS NOT A ZERO COST.** An unpriced remedy is not
cheap, it is unpriced. **Ask the agent that OWNS the thing rather than reasoning
about someone else's box.**

### Two standing instructions from the owner, 2026-09-04. They outrank habit.

**SIMPLE IS BEST, G-44.** The burden of proof is on COMPLEXITY, never on
simplicity. A simpler build is easier to build, easier to operate and easier to
repair. **Anything you add must say what failure it prevents and what it costs on
all three. If it cannot, it does not go in.** This is the tie-breaker whenever two
answers both work.

**LEAN ON THE 1ST EDITION SET, G-40b.** Where it did something and this build has
no reason to differ, DO WHAT IT DID. **Deriving a fresh answer to a question it
already answered is work nobody asked for.** Its figures are still unverified, its
parts may still be superseded, and where it disagrees with a frozen row the tree
still wins - **but on anything this tree has no position on, its answer is the
starting point. It is a build that got built.**

**And the instruction under both: GET IT DONE.** Return the thing that can be
built. A returned answer that is correct and unbuildable is not finished.

### The one worth saying out loud to all of you

**PUMP-BOXES was asked for the DIR level and refused to state one.** It named the
exact three numbers that would settle it - the internal pull-down value, the LED
forward voltage, and the threshold - and stopped. F-059.

The owner's lookup came back and **the answer was the OPPOSITE of what the tree
had recorded.** A floating DIR floats HIGH.

**The correction cost one line.** D-069's closing sentence, and two resolution
cells. Nothing built on it had to be torn out, because nothing had been built on a
guess. **The agent that got it right got it right by declining to guess.**

Compare what a guess costs. F-074: an impossibility asserted without being
established, banked in a decision, copied into a commissioning row citing the
document that asserted it, and it would have foreclosed the S-05 fork by removing
the reason to pay for it. Same tree, same week, opposite outcome.

**Refusing to answer is a real answer when you name what would let you answer.**
Rule 3 is usually read as a rule about part numbers. It is not. It is this.

## AUDIT

Mandatory, always exists, designs nothing, owns nothing, changes nothing.

Invoked WITHOUT source access. It is given the interface table, decisions.md,
traps.md and whatever subsystem files the pass is about, and nothing else. Its
output is questions, not assertions, and it cannot silently fix what it finds.

It exists because a subsystem that passes its own checks is self-consistent, not
verified.

### When AUDIT runs, and it is not on a schedule

**Invoke it after every subsystem return that touches a frozen row or another
subsystem's slice. Not on a schedule and not on a batch.**

The reason is what it is for: **it finds things by comparing two parties on one
fact. Give it two returns and it compares them. Give it six and it summarises
them, which is worth much less and costs more.**

Each time, hand it exactly: **the return that just landed, the frozen rows that
return builds against, and any earlier return that touches the same fact. Nothing
else.** No general access to the tree.

A run scoped to one fact across two or three parties is the unit. A run scoped to
"everything so far" is not an audit, it is a summary.

## INTEGRATOR

Mandatory now that a shared tree exists. Its only job is to take a finished
subsystem's output and make it land in the shared source: the interface table,
the subsystem files, the drawing and document package as those appear.

It owns the crossing. Most real defects surface there. It reports what it could
not land rather than reshaping it to fit.

## Invocation discipline, BOSS's own

- Before invoking an agent, give it the files it must read. Name them.
- After it returns, BOSS writes what it learned back to disk. A subsystem that
  reports something BOSS does not record has told nobody.
- Run the project's checks after the last edit of a pass, never mid-pass. A pass
  that cannot reach a coherent state in one sitting is not started.
- Any artifact in the tree that nobody can account for is discarded, not
  repaired. Restore from a known good state and redo the work.
- **An agent writing a document writes it in ONE pass at the end, never
  incrementally.** Proved useful 2026-09-02: a container restart killed the agent
  writing the software specification mid-task. **The working tree was clean and there
  was nothing to discard, because the file was to be written atomically.** Had it been
  built up section by section, the discard rule would have had to be applied to a
  half-written document that looked plausible - and provenance you cannot establish is
  worse than work you have to repeat.
- When a thread stalls, assign a subsystem that has to BUILD against the
  interface and cannot proceed without an answer. Reviewing finds nothing.
  Using finds everything.
- When BOSS and a subsystem disagree, establish who has read what before
  arguing about who is right.
- To find a seam nobody owns, do not review the interface table. Assign work
  that cannot proceed without crossing it. See traps.md T-002.

## Classify before you question

**T-021: the question to ask of a file depends on what kind of file it is.** A state
machine produces untested joins and half-wired mechanisms. A routing layer produces
neither, because it holds no mechanisms; its defects are the defects of a boundary.
**Asking the state-machine question of a routing layer finds nothing, and reporting that
silence as health is worse than not having looked.**

This bears directly on how AUDIT runs are scoped and on how any agent reads a file it
did not write. **Classify the artifact first, then choose the question.**

## Held, by the owner

**The operator interface on the touch screen.** The owner holds a set of
requirements and is withholding them deliberately: the fault model is still
moving, and he will not have a UI designed against a moving target. **No agent
designs a UI and no agent asks for the requirements.** They arrive when the fault
behaviour is settled.

## What has actually worked, recorded as evidence rather than as theory

2026-08-30. CONTROL-SOFTWARE and DOSING were invoked in parallel on two different
questions, with different scopes and no knowledge of each other. Both
independently found the same missing commissioning row: the probe noise and drift
band that C-03 and C-04 compare against and that nothing scheduled. Both found it
by reading commissioning.md. BOSS did not find it either time, and BOSS wrote the
file.

Two agents with different scopes converging on the same missing row is what this
arrangement is for. It is also the argument for writing state to disk rather than
holding it in one head: neither agent could have found it if the gap had lived in
BOSS's context instead of in a file they could both read.
