# The terminal survey. F-106.

**This closes the one thing that blocks all 111 rows of D4.** No decision, no
lookup, no money. **Parts in front of you and something to write with.**

Fill this in once. **Everything downstream reads it and nothing else asks for it
again.**

## The form, per device

**For every device below, record its terminals IN PHYSICAL ORDER, and record the
DATUM you ordered them from.**

| Field | What to write |
|---|---|
| **1. DATUM** | **The physical feature you are facing and the direction you counted.** "Facing the terminal block with the DIN clip toward me, left to right." **Not optional and not "left to right" alone** - the 1st Edition's height contradictions were a datum problem, and this is the same defect one level down |
| **2. POSITION** | 1, 2, 3... in that order. **Always recorded, for every terminal, even one with a perfect legend** - it is the fallback identity and the only one that always exists |
| **3. LEGEND, VERBATIM** | **Exactly as printed. Same case, same punctuation, same spacing.** Do not tidy it, do not expand an abbreviation, do not correct an apparent typo - **if the part says VM and the datasheet says VS, the part wins and the discrepancy is the finding** |
| **4. LEGEND TYPE** | One of: **TEXT** / **SYMBOL** / **NONE**. See the convention below |
| **5. ANYTHING ELSE PRINTED NEARBY** | **Silk that is NOT a terminal legend but sits close enough to be mistaken for one.** Part numbers, polarity marks, revision codes, arrows, a manufacturer's logo. **This is the field that stops a future reader naming a terminal after a revision code** |

## The convention for a terminal with no legend

**F-051 already set it and this generalises it.** The Adafruit board's motor terminal
is a circled plus and a circled minus - **a build sheet cannot quote a symbol.**

| Type | What you write | What the build sheet will do with it |
|---|---|---|
| **TEXT** | The characters, verbatim | Name the terminal by its legend |
| **SYMBOL** | The word **SYMBOL**, then a plain-words description: "circled plus", "circled minus", "earth symbol", "arrow pointing right". **Mark it NOT QUOTABLE** | **Name the terminal by POSITION AND FUNCTION.** The description is for a human confirming they are at the right terminal, never for a build sheet to print |
| **NONE** | The words **NO LEGEND** | Name by POSITION AND FUNCTION |

**One rule covers all three: a terminal is identified by POSITION FIRST and by
legend second.** Position always exists. A legend may not, may be a symbol, or may
be wrong.

**And record a legend you distrust rather than fixing it.** If two terminals appear
to carry the same legend, write both down as they are and flag it. **That is a
finding about the part, not an error to correct at the bench.**

## The devices, and why each one is needed

**Grouped by what is blocked on it, so a partial pass still unblocks something.**

### Group 1. Unblocks the most D4 rows. Do these first.

| Device | Count | What lands there |
|---|---|---|
| **Adafruit 6121 TMC2209 breakout** | **8** | Motor supply, STEP, DIR, VDD, motor phases. **Survey ONE and confirm the other seven match** - if any differs, that is a finding and all eight need recording |
| **Finder 55.34 relay, and its 94.74SMA socket** | **4** | **The SOCKET is what a conductor lands on, not the relay.** Record both: the relay's own legend and the socket's terminal numbering, and say whether they agree |
| **Finder 22.32 contactor** | **2** | **KM-DRV and KM-CHIL.** S-08's readback is on one of them, pole 2 |
| **Mean Well NDR-240-24** | 1 | The 24 V rail's output terminals, its input terminals, and **the trim pot's own marking if it has one** |
| **ULN2003** | **12 held, fewer used** | **If it is a bare DIP, say so** - a DIP has pin numbers and no legends, and that is a NONE case with a pin-1 datum |
| **74AHCT125** | **4 held** | As above |

### Group 2. Unblocks the display box page.

| Device | Count | What lands there |
|---|---|---|
| **Raspberry Pi 5 GPIO header** | 1 | **Pin 1 datum and the header's own silk.** parts.md holds the pin map from the owner; this records what is PRINTED ON THE BOARD, which is a different fact |
| **Atlas Scientific EZO carrier boards** | 3 | pH, EC, RTD. **The three differ, per C-14** |
| **USB-C bulkhead** | 1 | Both faces, if it carries any marking |

### Group 3. Unblocks the panel page and the field pages.

| Device | Count | What lands there |
|---|---|---|
| **Ground bar** | 1 | Whether its landings are numbered at all |
| **Fuse holder** | 1 | Line and load marking, if any |
| **Inrush current limiters** | 2 | Polarity or orientation marking, if any |
| **Winland WaterBug WB200** | 1 | **Supply terminals, Form C terminals, and the sensing-circuit terminals.** Its C-NC output is answered; this is the legend, not the behaviour |
| **The four enclosures** | 4 | **Nothing to survey unless a face carries printed text.** Recorded here so nobody wonders whether they were missed |

## What NOT to do

**Do not survey a part you have not got.** A blank row that says NOT ON SHELF is
worth more than a guess, and it tells the schedule which rows stay blocked.

**Do not merge two devices' surveys because they look identical.** Record one, then
CONFIRM the others against it, and say you confirmed rather than assuming.

**Do not photograph it instead.** A photograph is a source someone has to re-read
every time. **This sheet is read once and cited forever** - that is the whole point
of doing it once.
