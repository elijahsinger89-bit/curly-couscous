# MAIN-PANEL: the ladder schematic

Returned 2026-09-04, third invocation. **Nothing waited for.** The machine is drawn
as it stands and the holes are marked OPEN on the drawing rather than held back.

Read before drawing: agents.md rules 1-11; subsystems/main-panel.md,
main-panel-poles.md and main-panel-buy.md, all three mine; interface-table.md in
full; the G-rule table in decisions.md lines 50 to 91; parts.md in full;
findings.md; traps.md. Then, because the drawing needed them, order.md,
decisions.md D-029 to D-137, commissioning.md C-12 and C-23, and
subsystems/water.md.

**No file was edited. This file is the only output.**

## What the drawing is and is not

It is a LADDER of the main panel: rungs in order from supply, through the
permissive chain, to every load and every sense circuit. **It is not a wiring
diagram.** There is no terminal number, no wire gauge, no breaker size and no
contact rating in it. Where a rating decides something, the rung carries a
requirement and a search term and stops, per rule 3 and G-15.

**Every device is labelled with the name the tree already uses.** Where a device
has no name in the tree it is drawn as an empty box and marked OPEN, and the OPEN
table says what would name it.

**Relay names are envelope names, from order.md's envelope map, not socket
positions.** G-28 and T-013: a relay is labelled by name, never by position.

### Verification of the four items I was told had closed

Each was checked against the tree rather than taken from the briefing.

| Told | Found | Where |
|---|---|---|
| S-05 closed LEVEL-BASED, D-119, no flow element, D-060's timing element not bought | Confirmed | decisions.md D-119; interface-table.md S-05; order.md item 6 is now stale and still reads "0 or 1" |
| F-044 closed, D-108, no chiller contactor | Confirmed | decisions.md D-108 |
| F-086 closed, D-137, chiller and loop pump on ONE SWITCHED RECEPTACLE, dedicated circuit, both stop when the permissive drops, 6 A + 1.5 A + compressor inrush | Confirmed as a fact. **NOT confirmed as a design: nothing in the tree names the device that switches that receptacle** | parts.md "The chiller and its loop pump"; interface-table.md P-05 still names a "chiller contactor" |
| Fill valve is an ASCO 8210G095AC120/60, 120 VAC coil, inrush 0.58 A, holding 0.21 A, NC, spring closed | Confirmed, and the inrush is the sizing number | parts.md "The fill solenoid", D-136 |
| Enclosure IP65, D-110, top face designed to shed | Confirmed. The top-face half of F-025 did not close with it and is F-088 | decisions.md D-110 |
| Eight float POSITIONS, four per tank, D-127; part roster struck by D-118 | Confirmed | decisions.md D-118, D-127 |
| F-093 open and joint with WATER, no fail direction inherited | Confirmed | findings.md F-093 |
| F-094 routed to me | Confirmed, and D-130 attaches a guard to it | decisions.md D-130 |

---

## LEGEND

```
   --] [--     contact, OPEN when its device is at rest
   --]/[--     contact, CLOSED when its device is at rest
   --( )--     coil
   --(*)--     pilot lamp
   --[ NAME ]--   a named device or load
   --< ?nn >--    A BOX THE TREE DOES NOT FILL IN.  Keyed to the OPEN table
   ==>         a feed to a named bus, not a load
   ..........  a conductor leaving this panel through a gland
```

**A float is never drawn `] [` or `]/[`.** Its contact form is exactly what F-093
asks and this drawing inherits no answer. Every float is a `< ? >` box.

---

## THE LADDER

### SECTION A - 120 VAC. Left rail L1, right rail N.

```
   L1                                                                     N
    |                                                                     |
01  +---< ?1  MAIN DISCONNECT >-------------------------------------------+
    |         no disconnecting means is named anywhere in the tree
    |
02  +---< ?2  OVERCURRENT PROTECTION AND THE BRANCH SPLIT >
    |            |
    |            +==> BUS-A   panel loads, control supply, switched receptacles
    |            +==> BUS-B   chiller circuit, DEDICATED per D-137        < ?3 >
    |
03  BUS-A ---[ FUSE ]---[ R-PI  receptacle, NOT switched ]----------------+
    |            P-07, closed.  The Pi has power whenever the panel does
    |
04  BUS-A ---[ NDR-240-24  primary ]--------------------------------------+
    |            24 Vdc 10 A 240 W.  Output trim 23.76 to 28.28 V, F-010
    |
05  BUS-A ---< ?4  K-PERM 120 V BUS POLE, IN OR OUT >==> BUS-AP
    |            D-058 left this as the owner's pick and it was never made.
    |            Every rung 06 to 08 below hangs off BUS-AP if it is in,
    |            off BUS-A directly if it is out
    |
06  BUS-AP --] [--------[ FV-1  fill solenoid coil ]----------------------+
    |         K-FILL-S     ASCO 8210G095AC120/60, 120 VAC, NC, spring
    |         power pole   closed on power loss.  INRUSH 0.58 A     < ?5 >
    |
07  BUS-AP --] [--------[ R-XFER  receptacle, transfer pump ]-------------+
    |         K-FILL-D-P   P-03.  Panel mounted, cord plugs in from
    |         power pole   outside, D-046                           < ?6 >
    |
08  BUS-AP --< ?7 >-----[ R-CIRC  receptacle, circulation pump ]----------+
    |         K-DRY-P     P-04.  WHICH WAY THIS POLE FACES IS NOT ON FILE
    |         power pole  and it is the load-bearing hole in this drawing
    |
09  BUS-B ---< ?8  SWITCHING ELEMENT, UNNAMED >
    |            |
    |            +------[ R-CHIL  ONE receptacle: chiller + loop pump ]---+
    |                     JBJ Arctica DBE-200, 6 A, LRA NOT PUBLISHED
    |                     Danner Supreme Aqua-Mag 12 item 02712, 1.5 A
    |                     P-05's End A still names a "chiller contactor"
    |                     that D-108 says does not exist          < ?9, ?10 >
```

### SECTION B - 24 VDC. Left rail +V, right rail -V. Both from the NDR-240-24.

```
   +V                                                                    -V
    |                                                                     |
10  +==> the 24 V rail.  Everything below and rung 16 are on it.
    |    Nothing fixes the trim, so no coil, lamp or burden may be sized
    |    at 24 V.  G-31 read against F-010, and F-056                < ?11 >
    |
    |
    |    ---------------- THE PERMISSIVE STRING, G-07 ----------------
    |
11  +--]/[----< ?12 >----< ?13 >----< ?14 >----< ?15 >----+ node P
    |  E-STOP   LEAK       DAY TANK   STORAGE   STORAGE    |
    |  22 mm    CONSOLE    HIGH-HIGH  HIGH-HIGH LOW        |
    |  momentary  WB200      float      float    float     |
    |  NC       Form C leg                                 |
    |  parts.md  parts.md   D-134 says these two drop the  |
    |                       permissive.  Their lineage is  |
    |                       the 1st Edition set, G-40      |
    |                                                      |
12  |                     +--] [--+                        |
    |                     | RESET |                        |
    | node P -------------+       +--------+---( )---------+  K-PERM coil
    |                     +--] [--+        |   ( )            K-PERM-P coil
    |                       K-PERM         |                  IF SPLIT  < ?16 >
    |                       seal-in pole   |
    |                                      +  coils in PARALLEL, never in
    |                                         cascade, D-072
    |
13  +--] [------------------------------------------------==> node PB
    |  K-PERM pole            THE 24 V PERMISSIVE COIL BUS.  Every coil in
    |                         rungs 15, 18, 19, 20 and 22 is fed from here
    |
14  +--]/[--------------------------(*)-----------------------------------+
    |  K-PERM pole                  PL-R  "permissive lost"        < ?11 >
    |
    |
    |    ------------- THE DRIVER PERMISSIVE, G-09 as amended -------------
    |
15  < ?17  COIL POSITIVE: RAW 24 V, OR node PB >
    |            |
    |            +---( )---.......... ULN2003 SINK, BCM 18, display box
    |             22.32 #1     S-07 and S-09.  SUP-1 across the coil,
    |             coil         taken as given.  T-006 and T-007 apply:
    |                          the coil positive is HERE, the return is
    |                          4 ft away and the common must be traced
    |                          by hand
    |
16  +--] [-----------+----.......... P-06 to PUMP BOX A
    |  22.32 #1      |
    |  pole 1        +----.......... P-06 to PUMP BOX B
    |  terminals 1,2      One pole for VM distribution, both feeds off one
    |                     terminal downstream of it.  D-029, given
    |
17  node at rung 16 -------------(*)-------------------------------------+
    |                            PL-Y, across the OUTGOING rail, D-045.
    |                            Measured, not commanded.  PL-R and PL-Y
    |                            both lit is impossible: the contactor is
    |                            welded.  Exempt from G-24, across a supply
    |
18  node PB --< ?9  WHAT ENERGISES THE RUNG 09 SWITCHING ELEMENT >---( )--+
    |                                                          its coil
    |          D-137 says the chiller and loop pump stop "when the
    |          permissive drops".  THE PANEL HAS TWO THINGS BY THAT NAME
    |          and nothing says which one this is.  See finding 1
```

### SECTION C - THE FILL CHAINS. G-03: start float, stop float, relay seal-in.

```
   +V                                                                    -V
    |                                                                     |
    |    ---- STORAGE FILL.  Fills the storage tank from the building ----
    |
19  node PB --+--< ?18 >--+----< ?19 >-----------------+---( )------------+
    |          |  STORAGE  |     STORAGE                |  K-FILL-S coil
    |          |  FILL     |     FILL STOP              |
    |          |  START    |     float                  |
    |          |  float    |                            |
    |          |           |                            |
    |          +--] [------+                            |
    |             K-FILL-S                              |
    |             seal-in pole                          |
    |                                                   |
    |    K-FILL-S is a POWER envelope, order.md: seal-in and the fill
    |    solenoid, two spare poles.  PL-G does NOT sit here: order.md
    |    records the owner's gate 2 answer, PL-G means the DAY TANK
    |
    |
    |    ---- DAY TANK FILL.  Fills the day tank from storage ----
    |
20  node PB --+--< ?20 >--+----< ?21 >----< ?22 >-------+---( )---( )-----+
    |          |  DAY      |     DAY TANK   STORAGE LOW |   |       |
    |          |  TANK     |     FILL STOP  interlock?  |   |       |
    |          |  FILL     |     float      < ?15 >     |   |       |
    |          |  START    |                            | K-FILL K-FILL
    |          |  float    |                            | -D-Q   -D-P
    |          |           |                            | coil   coil
    |          +--] [------+                            |
    |             K-FILL-D                              |  PARALLEL, D-072.
    |             seal-in pole                          |  ONE STATE IN TWO
    |                                                   |  ENVELOPES
    |
21  +--] [--------------------------(*)-----------------------------------+
    |  K-FILL-D-Q pole              PL-G  "filling", day tank      < ?11 >
    |                               Agrees with S-03 by construction,
    |                               both being this relay's state
```

### SECTION D - THE DRY-RUN INTERLOCK. G-25, and S-05 as closed by D-119.

```
   +V                                                                    -V
    |                                                                     |
22  node PB --+--< ?23  DRY-RUN LEVEL FLOAT >--+--]/[--+---( )---( )------+
    |          |   WHICH POSITION, WHICH TANK, |  RESET |    |       |
    |          |   AND WHICH CONTACT FORM ARE  |  extra |  K-DRY  K-DRY
    |          |   ALL OPEN.  D-119 closed the |  block |  -Q      -P
    |          |   ELEMENT CLASS and named no  | < ?24 >|  coil    coil
    |          |   position.  F-093 is the     |        |
    |          |   contact form                |        |  PARALLEL, D-072
    |          |                               |        |
    |          +--] [--------------------------+        |
    |             K-DRY seal-in / latch pole
    |
    |    < ?25  WHICH STATE OF K-DRY IS THE DE-ENERGISED STATE >
    |
    |    THIS IS THE SINGLE MOST LOAD-BEARING UNSTATED FACT IN THE PANEL.
    |    It decides rung 08's pole sense, rung 22's RESET block form,
    |    F-093's answer, whether rung 05's 120 V bus pole is needed, and
    |    what the circulation pump does when the panel is dead.  See
    |    finding 2.  NO TIMING ELEMENT: D-060's other half was spent by
    |    D-119 and the device is not bought
    |
23  ***  THE RUNG THAT DOES NOT EXIST  ***
    |
    |    NOTHING IN THIS PANEL STARTS OR STOPS THE CIRCULATION PUMP.
    |    K-CIRC was deleted by D-058.  K-DRY is a PERMISSION and not a
    |    command, D-063's own words.  Under G-26 the Pi may not command it.
    |    So the pump runs whenever rung 08 permits.  See finding 3
```

### SECTION E - SENSE CIRCUITS TO THE PI. G-22 asked of every one.

All four are the same shape and none is a copy: a dry contact wetted from 24 V, an
optocoupler LED in series, **the burden IN THIS PANEL**, an isolated Pi input, sense
inverted. Sized independently under G-23, and the minimum belongs to the contact.

```
   +V                                                                    -V
    |                                                                     |
24  +--] [--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX, S-08          |
    |  22.32 |                                                            |
    |  #1    +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |  pole 2   45 to 55 mA total against the 22.32's 1000 mW minimum.
    |  term     TWO branches because at 42 mA an opto LED is near its
    |  3,4      continuous rating.  parts.md, GIVEN, not to be re-derived
    |
    |  SEVERED: Pi input stays HIGH, reads contact open, reads a drop.
    |  Chosen property, not an inheritance.  G-22 satisfied
    |
    |  ****  G-30 CONFLICT, ALREADY ON FILE AS F-055, NOT NEW HERE  ****
    |  Pole 1 of this same contactor is a tier-1 arcing power pole
    |  carrying up to 8 A.  Pole 2 is a sense pole.  G-30 says a power
    |  pole and a sense pole never share a relay.  S-08 HAS NOWHERE TO
    |  MOVE: D-029 established there is no auxiliary block and none was
    |  bought.  Reported, not resolved                              < ?26 >
    |
    |
25  +--]/[--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX, S-03          |
    |  K-FILL|                                                            |
    |  -D-Q  +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |  NC leg   about 12.5 mA against the 55.34's 300 mW minimum.  ONE
    |           branch.  Copying S-08's two-branch arrangement here would
    |           add a part for nothing, D-035
    |
    |  CLOSED means NO FILL.  OPEN means FILLING.  SEVERED reads as
    |  FILLING and dosing is inhibited.  D-042, by INVERSION.  T-016
    |
26  +--] [--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX
    |  K-FILL|                                     the D-042 DOSE INHIBIT
    |  -D-Q  +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |  NO leg   THE OTHER LEG OF THE SAME CHANGEOVER POLE.  Same common,
    |  SAME     same potential, exactly one conducting at any moment.
    |  POLE     G-27's complementary pair, and any state where both agree
    |  as 25    is a broken sense path
    |
    |  THIS CONDUCTOR HAS NO ROW IN interface-table.md              < ?27 >
    |
27  +--] [--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX, S-20          |
    |  K-DRY |                                                            |
    |  -Q    +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |
28  +--]/[--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX
    |  K-DRY |                                     S-20's COMPLEMENT
    |  -Q    +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |  SAME     order.md gives K-DRY-Q a "G-27 complementary pair to the
    |  POLE     Pi".  A pair is two conductors and two Pi inputs.  S-20's
    |  as 27    row describes ONE pole and ONE input                < ?28 >
    |
    |  FAIL DIRECTION OF THE S-20 PAIR: NOT ESTABLISHED HERE.  It cannot
    |  be, because it follows from ?25, the latch polarity.  Marked OPEN
    |  rather than inherited from S-03.  That is F-017's lesson and F-017
    |  was mine
    |
29  ***  F-094, AND IT HAS NO RUNG BECAUSE IT HAS NO DESTINATION  ***
    |
    |    +--< float NO leg >---> ?
    |    +--< float NC leg >---> ?
    |
    |    D-130 routed F-094 to me as a fail-detect on whichever floats
    |    have a spare leg.  G-27's construction rule requires BOTH legs
    |    to be READ and COMPARED.  G-01 makes floats invisible to the Pi
    |    and G-02 caps the Pi's level information at ONE dry contact.
    |    There is no reader in this panel that does not cost a coil, and
    |    the four-state topology has no spare coil.  See finding 4  < ?29 >
```

### SECTION F - THE FACE AND THE BAR

```
30  +--] [--+--(*)--+--(*)--+--(*)--+-------------------------------------+
    |  RESET |  PL-R |  PL-G |  PL-Y |
    |  THIRD    LAMP TEST while pressed.  Uses no hole: the RESET is
    |  BLOCK    already a momentary device on the face.  PL-R is DARK when
    | < ?24 >   healthy, so without this a failed PL-R and a healthy
    |           system look identical.  Requirement on the BUTTON, not a
    |           new penetration
    |
31  GROUND BAR, in this panel, CBL-07.  Every equipment ground from all
    four enclosures lands here.  The display box is polycarbonate and the
    pump boxes are plastic, so no box downstream offers a bonding path.
    Not a rung. Drawn because a ladder that omits it reads as though the
    bar were somebody else's                                       < ?30 >
```

**Rung count: 31.** Rungs 23 and 29 are drawn as absences and counted, because a
rung that should exist and does not is the thing this drawing is for.

---

## THE OPEN TABLE, KEYED BY RUNG

| Key | Rung | What is open | Owner | What would close it |
|---|---|---|---|---|
| ?1 | 01 | **No disconnecting means is named anywhere in the tree.** I looked in parts.md, order.md, my three files and interface-table.md P-01. Not present | MAIN-PANEL, P-01 | The owner's answer on whether the panel has its own disconnect or relies on the branch breaker. Search: `enclosure door interlocked disconnect switch DIN rail single phase`; `panel main switch 120 V 30 A DIN` |
| ?2 | 02 | Branch circuit arrangement: how many circuits arrive, their protection, and what shares each | MAIN-PANEL, P-01 | Owner states the supply. Then the sum of rungs 03 to 08 against each circuit |
| ?3 | 02, 09 | **The dedicated chiller circuit's rating.** 6 A chiller plus 1.5 A pump is continuous; the compressor inrush stacks on top and **parts.md states outright that the DBE-200's locked rotor current is NOT PUBLISHED and any inrush figure must be labelled an estimate** | MAIN-PANEL sizes, owner supplies the LRA | A measured or manufacturer-supplied LRA. Search: `JBJ Arctica DBE-200 locked rotor amperage nameplate`; `hermetic compressor branch circuit sizing FLA LRA single phase` |
| ?4 | 05 | **Whether K-PERM carries a 120 V bus pole.** D-058 raised it and left it as the owner's pick. The pick was never made and order.md's envelope map does not include it | Owner picks, MAIN-PANEL draws | The owner's answer. **Note it is no longer a free choice: see finding 2** |
| ?5 | 06 | The K-FILL-S pole's duty against the solenoid. **The number is the INRUSH, 0.58 A, not the 0.21 A holding figure** | MAIN-PANEL | The 55.34's rating for making and breaking an inductive 120 VAC load at that current, with electrical endurance. Search: `Finder 55.34 contact rating AC-15 pilot duty`; `Finder 55.34 electrical endurance inductive AC load 120 V` |
| ?6 | 07 | The transfer pump's nameplate. **The Anbull transfer pump is named in water.md and no electrical figure for it exists anywhere in the tree** | WATER returns it, MAIN-PANEL sizes | Nameplate FLA and LRA. Then the same contact-duty lookup as ?5 |
| ?7 | 08 | **Whether the K-DRY-P pole feeding R-CIRC is the NO or the NC side.** Follows entirely from ?25 | MAIN-PANEL, once ?25 is answered | ?25 |
| ?8 | 09 | **The device that switches R-CHIL is not named in any file.** D-108 removed the chiller contactor; D-137 created a switched receptacle and named no switch | MAIN-PANEL, and it is a purchase question | See finding 1. The load exceeds what a 55.34 pole class is described as carrying in parts.md and the panel already owns an unassigned 25 A contactor |
| ?9 | 09, 18 | **What energises that element's coil, and from which bus.** D-137 says "both stop when the permissive drops" and the panel has two things called the permissive | Owner, then MAIN-PANEL | See finding 1. Getting it wrong lets the Pi stop the chiller and the water system, which G-26 forbids |
| ?10 | 09 | **P-05 is an OPEN interface row whose End A names a device D-108 says does not exist.** Rule 9: nothing is built against an OPEN row | BOSS holds the row | Rewriting P-05's End A against D-137, then closing it |
| ?11 | 10, 14, 21, 30 | **Lamp and burden sizing at the BOTTOM of the trim range, not at 24 V.** F-056. PL-R and PL-G are on contacts and owe G-24 a minimum switching load; PL-Y is across a supply and is exempt | MAIN-PANEL | Each lamp's actual current. Search: `22 mm LED pilot light 24 V DC current consumption datasheet`; `relay minimum switching load LED indicator contact oxidation` |
| ?12 | 11 | **The permissive string's VOLTAGE CLASS.** See finding 5. CBL-06 puts the leak console's contact legs in the 120 V chain; order.md and parts.md make K-PERM's coil 24 Vdc. Both cannot be true of one string | BOSS holds CBL-06; MAIN-PANEL states the legs | One sentence saying what voltage the string runs at. It decides a cable purchase, the top-face bundle split and the E-stop's contact-block rating |
| ?13, ?14 | 11 | **Whether the day tank and storage high-high floats sit in the permissive string, and their contact form.** D-134 asserts they drop the permissive using 1st Edition float numbers. parts.md's own text says the string carries "float interlocks" without saying which | MAIN-PANEL and WATER jointly | A decision in this tree, under G-40, naming positions rather than LS numbers. Plus F-093's contact form |
| ?15 | 11, 20 | **Where the STORAGE LOW pump-down float lands.** It protects the transfer pump from running dry. Two candidates: the permissive string, or in series in the K-FILL-D coil circuit. Nothing in this tree says | MAIN-PANEL and WATER jointly | A decision. The two behave very differently: in the string a dry storage tank drops the drivers and both fills; in the K-FILL-D chain it only stops the transfer |
| ?16 | 12 | **Whether K-PERM splits into a quiet and a power envelope.** order.md recommends buying the fourth gold and the split itself is undecided | Owner | The owner's answer, which order.md says is used either way |
| ?17 | 15 | **Where the driver permissive contactor's coil positive is taken from.** F-019: from raw 24 V, one shorted output device on the logic board holds the contactor closed against a leak, an E-stop or a lost interlock, and G-07 is defeated. From node PB, G-07 holds. S-07 is OPEN and must state which | MAIN-PANEL and DISPLAY-BOX jointly, BOSS freezes | Writing it into the S-07 row. It costs nothing to choose correctly and cannot be got right by habit |
| ?18, ?19 | 19 | Storage fill start and stop float positions and contact forms | WATER returns the device and position, MAIN-PANEL the duty | F-093 for the form; D-118's requirements-first pass for the part; F-089's 24 V contact power under G-31 |
| ?20, ?21 | 20 | Day tank fill start and stop float positions and contact forms | As ?18 | As ?18 |
| ?22 | 20 | Whether a storage-low interlock sits in this chain | see ?15 | see ?15 |
| ?23 | 22 | **Which float is the dry-run element: which tank, which position, which trip level.** D-119 closed the element CLASS as level-based and named no position. D-116 forbids citing the 1st Edition set for it | WATER primary, MAIN-PANEL the electrical end | A decision naming a position. Then F-093 for the form |
| ?24 | 22, 30 | **The RESET device's contact blocks: how many and of which form.** At minimum one NO for K-PERM, one more for K-DRY whose form follows from ?25, and a third if it proves the lamps | MAIN-PANEL | ?25 first. Then search: `22 mm pushbutton contact block stacking NO NC depth`; `press to test pilot light 22 mm` |
| ?25 | 22 | **WHICH STATE OF K-DRY IS THE DE-ENERGISED STATE.** See finding 2 | MAIN-PANEL, and it is a design choice I am not making unilaterally because it is a choice and not a defect, rule 5 | The owner or BOSS choosing. Everything in finding 2 follows from it |
| ?26 | 24 | **Whether the 22.32's poles share one contact volume the way the 55.34's four do.** F-055, raised 2026-09-01, still open | Owner, one lookup | Search: `Finder 22.32 modular contactor contact chamber construction`; `modular contactor pole barrier arc chamber separation`. If they share, S-08 violates G-30 and has nowhere to move |
| ?27 | 26 | **The D-042 dose-inhibit conductor has no interface row.** It is the second leg of the S-03 changeover and it reaches the Pi | BOSS | A row, or an amendment to S-03 saying it is a pair |
| ?28 | 28 | **S-20's row describes one pole and one input; order.md builds a complementary PAIR** | BOSS | As ?27 |
| ?29 | 29 | **F-094 has no destination that G-01 and G-02 permit.** See finding 4 | MAIN-PANEL raised it; the rule is BOSS's | Either an amendment to G-02, or a hardware comparison element and the coil it costs, or a recorded decision that F-094 is declined on this build |
| ?30 | 31 | The ground bar itself, terminals, duct, DIN rail, the two panel-mount receptacles, the five gasketed top-face devices as one family, and the hood or slope. order.md lists all of these as **not covered, so nothing reads as complete** | MAIN-PANEL | A second order pass. Not started |

**OPEN marks on the drawing: 30 keys across 24 rungs.** Seven rungs carry no OPEN
mark: 03, 04, 13, 16, 17, 24 and 25.

---

## WHAT THE DRAWING REVEALED THAT NO FILE PREVIOUSLY SAID

Five. Each is stated with what I read, per rule 8, and each names the grade of any
impossibility, per rule 10 and G-36.

### FINDING 1. The chiller receptacle has no switching element, and the panel owns an unassigned 25 A contactor that D-108 orphaned

D-137 creates one switched receptacle carrying 6 A of chiller, 1.5 A of loop pump
and an unpublished compressor inrush, on a dedicated circuit. **It names no device
that switches it.** I searched parts.md, order.md, decisions.md D-108 and D-137,
interface-table.md P-05 and G-12, and my own three files. P-05's End A still reads
"MAIN-PANEL: chiller contactor, own circuit", which D-108 says does not exist.
order.md's item 5 still lists suppression for "the chiller contactor coil". order.md's
envelope map has six envelopes and none of them is this load.

**Two things follow that nobody has written down.**

**First, the class of device.** parts.md characterises the 55.34's power duty by "a
7 A break". This load is 7.5 A continuous before the compressor starts. The only
25 A device in this panel is the Finder 22.32, of which **two were bought and, since
D-108, only one has a job.** I am not assigning it: that is a design choice with a
purchase behind it and rule 5 says I stop. What I am recording is that the tree
believes it has one spare contactor and one homeless load and has not put them in
the same sentence.

**Second, and this is the sharper half. If that load lands on 22.32 #2, three things
change at once.** Its pole 2 becomes free, which is **exactly the spare pole S-18
needed** - and D-108 graded that exit as gone, upgrading D-064's claim from CURRENT
to STRUCTURAL on the reasoning that "there is no chiller contactor, so there is no
contact and no pole". **Under G-38 that grade is only true against the tree it was
graded on, and D-137 moved the tree three days later.** The grade is now CURRENT
again, and what would change it is naming the switching element. Second, F-055's
G-30 question applies a second time, to a second contactor. Third, the Pi would gain
a way to know whether chiller power was present, which is what S-18 has been open
for since D-059 reopened it.

### FINDING 2. Which state of K-DRY is the de-energised state is unstated, and F-093 is the same question wearing a different hat

You cannot draw rung 22 without choosing, and the tree contains both choices in
different files.

| | K-DRY energised means TRIPPED | K-DRY energised means PERMITTED |
|---|---|---|
| Dry-run float must | CLOSE on low level, an NO contact | OPEN on low level, an NC contact |
| Severed float conductor | Pump keeps running, protection silently absent | Pump stops. Fail-safe |
| Dead 24 V rail or open coil | Pump keeps running | Pump stops |
| Permissive drop, node PB lost | **K-DRY releases and the pump is FREED to run** | Pump stops |
| Clearing the latch needs | a momentary BREAK in the seal-in, an NC block | a momentary MAKE, an NO block |
| Matches the 1st Edition set | Yes: it draws both low-level stops NO | No |

**main-panel-buy.md, my own second pass, assumes the left column without saying
so**: it argues the latch "cannot be cleared by a normally open button" and needs "a
momentary BREAK in K-DRY's seal-in". Nothing else in the tree states a polarity.

**Three consequences nobody has connected.**

**F-093 is not a separate question.** It is routed as a contact-form question about
a float. It is actually a question about which state of the relay is de-energised,
and answering either answers the other. The two must be decided together or they
will be decided twice, inconsistently.

**D-058's argument for dropping K-PERM's 120 V bus pole is false in the left
column.** D-058 says the pole "may not be needed, since the pumps' coils already sit
on the permissive's 24 V bus". That holds for K-FILL-D-P, where energised means the
transfer pump runs. **It is exactly backwards for K-DRY-P in the left column, where
losing the bus releases the circulation pump instead of stopping it.** So ?4 is not
a free choice: in the left column the 120 V bus pole is required for an E-stop or a
leak to stop circulation at all.

**G-39's question has never been asked of this relay.** G-39 says to ask what an
actuator does with no power before asking anything else, and it was frozen off a
valve. The circulation pump's only interlock is a relay, and in the left column the
answer to "what does a dead panel do" is: it runs.

I am not choosing. It costs money in one direction, it is a choice rather than a
defect, and rule 5 says stop and ask.

### FINDING 3. Nothing in this panel starts or stops the circulation pump, and the free circulation-verification witness D-119 banked on depends on it doing so

This is rung 23, drawn as an absence.

What I read. **D-058 deleted K-CIRC**, making circulation a pole on K-DRY. **D-063
says the circulation pump is INTERMITTENT**, "it runs when the system needs the tank
mixed", "between batches it is off", and in the same entry, **"the dry-run interlock
is a PERMISSION for it to run, not a command that it should"** and "the exercise run
still has no command path. The Pi cannot command the circulation pump under G-26."
**parts.md, under D-137, says the circulation pump and the loop pump "BOTH RUN
CONTINUOUSLY".** water.md line 498 repeats it: "Two submersibles now sit in the day
tank and both run continuously."

**The topology is telling the truth and D-063 is the outlier.** With K-CIRC deleted
and G-26 forbidding a Pi command, there is no element between the permissive bus and
R-CIRC except K-DRY's permission. A permission with nothing behind it is a pump that
runs whenever the panel is up. parts.md and water.md have already converged on that
without either citing D-063.

**What this costs, and it is not tidiness.** D-119 closed S-05 level-based and
explicitly kept three surviving routes to circulation verification, of which **C-12,
the W-1 temperature-step witness, is the one it calls free.** commissioning.md C-12
reads: "the magnitude and timing of the PT-1000 step **when the pump starts after a
rest**, with the standing probe-section column at room temperature and the tank
chilled", precondition "**after a rest**". C-23 is a hazard row requiring the C-02
window to sit inside a running period and **not to span a start or a stop**.

**A pump that never stops has no rest and no start.** So C-12's step does not exist,
and the free route D-119 banked on is gone - not because anyone declined it, but
because the element that would have made it possible was deleted for a different
reason and nobody re-read C-12 against the deletion. **That is T-023's mechanism and
D-060's exact shape recurring: declining to pay makes the claim true with no step
anyone would notice.** The grade is CURRENT, not structural, and what would change
it is a single element that can turn the circulation pump off.

Also affected, and each cited from its own source rather than from this one: D-063's
own three "favourable consequences" all rest on the pump being off between batches,
including D-025's premise that continuous pump heat does not call the chiller.

### FINDING 4. F-094 has no reader. A fail-detected float needs a comparison, and G-01 and G-02 forbid the only one this panel has

D-130 routed F-094 to me as "a fail-detect on whichever floats have a spare leg". I
drew it and it does not land.

G-27's construction rule is that **both legs sit at the same potential on the same
cable, and any state where they agree is a broken sense path.** That requires
something to READ both legs and compare them. The panel has exactly one reader: the
Pi, through the sense circuits of section E.

**G-01: "Float switches are hardwired to relays and invisible to the Pi." G-02: "The
Pi gets exactly one level signal: a dry contact saying a day tank fill is in
progress."** Both are in the owner's not-revisitable table.

So the destinations are: a Pi input, which G-01 and G-02 forbid; a lamp, and all
five face holes are spoken for with no lamp-test hole among them; or a relay that
compares the two legs in hardware, which costs a coil per float and the four-state
topology has no spare coil. **The impossibility grade is CURRENT, not structural**,
and what would change it is either an amendment to G-02 or the purchase of comparison
relays. **I am not proposing either.**

Worth keeping alongside it, because D-130 anticipated the misreading: this does not
argue for skipping the overflow bulkhead. They catch different failures.

Note the two complementary pairs already in the design of record - S-03 with the
D-042 inhibit, and the S-20 pair - are **relay** contacts, not float contacts, so
they satisfy G-01 and are consistent with G-02 read as one level SIGNAL carried
complementarily. F-094 is different in kind because the changeover is in the tank.

### FINDING 5. The permissive string's voltage class is stated two ways, and a cable purchase and a routing decision both rest on it

CBL-06, in the interface table: the leak console "is POWERED, not a passive float.
**Its contact legs sit in the 120 V chain, so EVERY conductor in its cable must be
insulated for 600 V**, including the 24 V supply pair sharing that jacket."
parts.md repeats it.

But the string energises K-PERM, and order.md specifies K-PERM's coil as a DC coil
whose range must cover the whole 23.76 to 28.28 V trim band, which is the NDR's 24 V
rail. **A 24 Vdc coil is not energised by a 120 V string.**

Both cannot be true of one string. Either the string is at 24 Vdc and CBL-06's 600 V
requirement has lost its stated reason, or the string is at 120 V and something not
on file interposes between it and a 24 Vdc coil.

**It has already propagated twice, into my own files.** main-panel-poles.md puts "the
permissive string including the E-stop and the leak console legs" in routing class A,
120 V line, and concludes that the top-face bundle is 120 V-class and therefore the
longest 120 V run in the panel. main-panel-buy.md then splits the top-face bundle in
two on that basis. **If the string is 24 Vdc, the top-face bundle is homogeneous and
that split is unnecessary work.** It also decides the E-stop's contact-block rating,
which is a DC rating in one case and an AC one in the other, and a DC break is the
harder duty.

Reported, not resolved: CBL-06 is BOSS's row and D-005 says its terminations are not
changed unilaterally.

---

## WHAT WOULD TURN THIS INTO A WIRING-LEVEL DOCUMENT

In the order the work has to happen, because each item gates the next.

**1. Three answers, and nothing below can start without them.** ?25, the K-DRY latch
polarity, which carries F-093 and ?4 with it. ?8 and ?9, the chiller receptacle's
switching element and its coil source. ?17, where the permissive contactor's coil
positive is taken from. All three are choices, not lookups.

**2. The float pass, from requirements.** D-118 restarted it and it is not finished.
Eight positions need: what the float must DO, its contact form under F-093, and the
24 V contact power under F-089 and G-31. Until that returns, five rungs are boxes.

**3. Two nameplates.** The transfer pump and the circulation pump. Neither exists in
the tree. Both are WATER's to return and both size a contact.

**4. One LRA, or the recorded absence of one.** parts.md is explicit that the
DBE-200's is not published. Whatever sizes rung 09 has to be sized against a figure
that is labelled an estimate, everywhere it appears.

**5. Contact duty per pole, once 2 to 4 land.** One requirement per pole against the
relay's rating, never a figure carried from another pole, G-23. The fill solenoid's
0.58 A inrush is the first.

**6. The sense-circuit component values.** Four circuits, each sized independently at
the BOTTOM of the trim band per F-056, not at 24 V: opto series resistor and burden
for S-08 at 45 to 55 mA, and for each of S-03, the D-042 inhibit and the two S-20
legs at the 55.34's 300 mW floor. The burdens are all in this panel.

**7. Terminal numbers, and they come LAST.** My own file says terminal numbers are
assigned late. They are assigned after the envelope map is final, because a split
moves conductors between sockets. T-008, T-009 and T-010 apply at the count: count
landings and clamps, never jackets.

**8. The duct and gland plan**, which D-049 made load-bearing on a safety rule rather
than merely tidy, since the SHORT half of G-22 is answered by adjacency. Blocked in
part on ?12, the string's voltage class, which decides whether the top-face bundle is
one class or two.

**9. The second order pass.** order.md's own closing section lists what it does not
cover: the five gasketed devices as one family, the hood or slope, the two panel-mount
receptacles, the lamps with their burdens, the ground bar, terminals, duct and DIN
rail. Nothing in this drawing reads as complete while that list stands.

---

## Status

**Stopped part-way, not finished.** I do not declare myself finished and BOSS
declares it after another agent has built against this and found nothing, rule 7.

No file was edited. Nothing here was built against an OPEN interface row: where a
rung sits on one, the rung is drawn as a box and the row is named in the OPEN table.
No terminal number, wire gauge, breaker size, part number or contact rating is
stated from memory; every part named appears in parts.md and is cited to it, and
every rating is a requirement plus a search term.
