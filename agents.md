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
