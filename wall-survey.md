# The wall survey. M-02. The form to measure in.

**COORDINATES FROM ONE DATUM, PLUS THE CONSTRAINTS THAT MUST SURVIVE A MOVE.** Not a
word sketch, not relationships.

**Why coordinates rather than relationships: RUN- cut lengths are computed as wall
run plus 3 ft under D-090, and a relationship does not produce a length.** "The
display box is left of the panel" cannot be cut from.

**Why constraints as well as coordinates: a coordinate says WHERE something is and
nothing about WHAT BREAKS IF IT MOVES.** That is G-50's shape on geometry - the
number is the value, the constraint is what makes a later change checkable.

## 1. THE DATUM. One, named physically, both axes stated.

**State it as a thing you can touch, and state which way each axis runs.** For
example: *"Origin is the bottom-left corner of the wall as I face it. X runs right
along the floor. Y runs up."*

**Not optional and not "left to right".** D-129 and the 1st Edition's two-datum
contradiction are the same defect one level up: **the same numbers appeared under
"end cap face" and under "tank floor" and both were written by people who knew which
they meant.**

**If the wall is not square, or the floor is not level, say so and say what you
measured against instead.** A datum on an out-of-square wall is still one datum; an
unstated correction is not.

## 2. PER ITEM: A NAMED FEATURE, NOT THE ITEM.

**"The panel at X, Y" is ambiguous - the panel's WHAT?** Its outline corner, its
centre, or the mounting hole a person drills.

**For each item give: the named feature, its X and Y, and the item's overall extent
from that feature.** F-051's rule on terminals applied to geometry: **name the thing
you measured to.**

| Item | What is wanted |
|---|---|
| Main panel | **The mounting-hole coordinates**, because that is what gets drilled. Plus the outline extent, because that is what collides |
| Display box | Mounting holes, outline, **AND HEIGHT ABOVE THE FLOOR** - M-03 is operator reach and sightline and is still open |
| Pump box A, Pump box B | Mounting holes and outline, each separately even though they are one build |
| Manifold | Both ends, and its run between them |
| Tubing raceway | Both ends, and its run |
| Jug stations | One per station, and say which station is which - **or say they are not yet assigned, which is also an answer** |
| **The floor track drain** | Where it crosses the wall's footprint, because FL-11 and FL-12 discharge into it |
| **Both tanks** | Their footprints relative to the wall, because the standpipes' cords run from them to the panel |

**Where mounting holes differ from the outline, GIVE BOTH.** They answer different
questions: **holes are what a person drills, outline is what collides with the next
thing.**

## 3. THE CONSTRAINTS. What must not change if something moves.

**For each item, one line: what fixes it there.** If nothing does, say "free" - that
is the most useful answer of all, because it names what a later change may move
without asking.

Examples of the kind of thing this catches:

- **"The display box is at this height because that is eye level standing."** Move
  it and M-03 reopens.
- **"The main panel is here because the building breaker is on the other side of that
  wall."** Move it and the supply run changes.
- **"The pump boxes are adjacent because they are one build."** Move one and they
  stop being one build.
- **"This jug station is here because the forearm hazard rule needs clearance at the
  acid station."**

**A constraint nobody writes down is a constraint the next editor breaks for free.**

## 4. WHAT THIS UNBLOCKS, so the measuring is aimed

| Closing M-02 releases | Why |
|---|---|
| **D3, the enclosure layout sheets** | Gated on this and nothing else |
| **D6's last position and spacing cells** | The balance of the cable schedule |
| **RUN- cut lengths** | Wall run plus 3 ft, D-090 |
| **D1's dimensioned half** | Every position, spacing and dimension step |

## 5. WHAT NOT TO DO

**Do not design it to fit the documents.** If two things collide, say they collide -
**that is a finding about the wall, and it is cheaper before anything is drilled than
after.**

**Do not round to tidy numbers.** A measured 412 mm is worth more than a tidy 400,
and under T-018 a number that looks chosen rather than measured gets treated as a
seed by whoever reads it next.

**Do not give a dimension you did not measure.** "I have not measured this one" is an
answer and it blocks only its own rows.
