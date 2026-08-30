# Traps

Failure modes this project has actually hit, written so the next agent
recognises one. Not hypotheticals. A trap goes in here after it has bitten.

## T-001 Splitting one discipline across two agents and calling the result a boundary

Hit on 2026-08-30, by BOSS, in the first agent proposal.

Storage-and-fill and day-tank-and-loops were proposed as two agents. The day
tank floats sat in one agent's tank and belonged to the other's fill chain. The
transfer pump discharged into the other agent's tank. The manifold suction and
return were two more crossings. Four seams between two agents doing the same
plumbing in the same room, for one builder.

How to recognise it: the split follows a process step, tap then storage then day
tank, rather than a physical thing. Count the crossings the split creates. If
the same person with the same tools works both sides and the crossings exist
only because of the split, it is not a boundary.

Corrected by merging into WATER. See decisions.md D-003.

## T-002 A seam that both agents end before reaching

Hit on 2026-08-30, by BOSS, in the same proposal.

PUMP-BOXES ended at the head barb. DOSING ended at the tubing back to the
manifold. Between them sat the nutrient jugs, the suction tubing, and how a jug
is placed and changed. Nobody owned it and the interface table would not have
caught it, because a crossing needs two named ends and this had none.

How to recognise it: read the scope-ends of every adjacent pair and ask what
physically sits between them. An unowned gap does not appear as a row in the
interface table. It appears as nothing at all, which is why it survives.

Corrected by giving the whole wet path to DOSING. See decisions.md D-006.

## T-003 Asserting from absence

Not yet hit in this project. Seeded because BOSS's own instructions name it as
the single most common error in this pattern.

"There is no interlock for X" requires having looked at the file or the panel.
If you have not looked, the sentence is "I have not checked whether there is an
interlock for X." AUDIT is invoked without source access precisely so its output
is questions rather than assertions. Any agent that writes an absence claim must
name what it read to establish it.

Move this entry's first line when it is hit for real.
