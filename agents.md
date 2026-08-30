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
- When a thread stalls, assign a subsystem that has to BUILD against the
  interface and cannot proceed without an answer. Reviewing finds nothing.
  Using finds everything.
- When BOSS and a subsystem disagree, establish who has read what before
  arguing about who is right.
- To find a seam nobody owns, do not review the interface table. Assign work
  that cannot proceed without crossing it. See traps.md T-002.

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
