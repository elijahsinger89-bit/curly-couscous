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

### 2a. WITHDRAWN 2026-09-23, D-237. THE MOUNTING HOLE PATTERNS ARE NOT WANTED

**F-124 CLOSES. It asked for twelve numbers across four boxes and the answer is that a
hole pattern is not a drill specification.**

**The owner's method, now D1 step 10-01b: hold the box in position, level it, MARK
THROUGH ITS OWN MOUNTING HOLES, drill, fix.** No pattern on file, nothing to disagree
with the part in your hands.

**ONE THING SURVIVES FROM THE WITHDRAWN SECTION AND IT IS NOT A DIMENSION: whether each
box's holes go through the BACK WALL or through EXTERNAL FEET**, because a
through-the-back hole breaks the seal and a foot does not. **That is looked at, not
measured, and it is folded into 10-01b.**

**WHAT REPLACES IT IN THE BATCH: five devices, two figures each, MEASURED WITH A
CALIPER. F-128.** Depth off the rail and height above the rail for the Finder
94.74SMA-plus-55.34 assembly, the Altech 1C15UL/1D15UL outline, the Phoenix
4-HESILA 250 and the ABB AF09-30-10-13. **Four of five publish neither figure in the
frame a section view needs, so the shelf answers faster than the catalogue.**

**Plus the door-to-plate clear depth and the usable door area inside the sealing
perimeter.**

### 2b. THE WITHDRAWN TEXT, KEPT SO THE REASONING IS NOT LOST

**THE FOUR OUTLINES AND PLATES ARE NOW ON FILE. NO HOLE PATTERN IS, FOR ANY BOX,
INCLUDING THE MAIN PANEL.** Searched parts.md, enclosure-layout.md, build-book.md and
purchase-package.md.

**Without them a complete wall survey still produces no drill step.** M-02 gives the
position of the box on the wall; the pattern gives where the holes are relative to the
box. **One without the other locates nothing a drill can use.**

**Measured off the part, not looked up. It is the same evening and the same tape.**

| Per box | Why it is wanted and not just nice |
|---|---|
| **Hole centre spacing, both axes** | It is what gets drilled |
| **Hole or slot diameter** | A slot is an adjustment and a hole is not, **and which one it is changes whether the wall marking has to be exact** |
| **Through the back wall, or in external feet or flanges** | **A through-the-back hole BREAKS THE SEAL and an external foot does not.** This changes the gasketing question, not just the drilling, and it is the one that cannot be inferred from a listing photograph |

**Four boxes. Three figures each. Twelve numbers and it unblocks every mounting step in
D1 and the drill half of D3 sheet 3.8.**

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
