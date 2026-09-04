# D2 - ELECTRICAL SCHEMATIC

**The main panel. Rungs, in order, from supply through the permissive chain to every
load and every sense circuit.**

| | |
|---|---|
| Document | **D2**, per document-plan.md section 1.2 |
| Owner | **MAIN-PANEL** |
| Issue | 1, 2026-09-04 |
| Read by | The builder, before building the panel and while wiring it |
| Read when | With D1 and D3, before building starts. D5 and D4 are generated from this sheet, D3 and D6, and cannot be written before it |
| Built from | subsystems/main-panel-ladder.md, the ladder returned 2026-09-04 |

## HOW TO READ THIS SHEET

**This sheet is the single source of four kinds of fact and of nothing else**, per
document-plan.md section 3.2: **rung logic, what energises what, contact identity,
and device identity.** D4's pages carry "built from D2".

**What is deliberately not on this sheet, each with where it lives instead.**

| Not here | Where |
|---|---|
| Any conductor fact - endpoint, colour, gauge, length, fail behaviour of a conductor | **D5**, one CDR- row each |
| Any jacket, terminal or landing | **D6**, RUN- and TRM- rows |
| Any quantity, count, total or price | **D7, once.** No drawing sheet in this set carries a parts table |
| Any device position, rail, duct, face or gland | **D3** |
| Any reasoning, provenance or argument | **The tree.** decisions.md, findings.md, traps.md, the subsystem files |

**A wire schedule is not printed on this sheet.** The 1st Edition's schematic sheet
carried one and it disagreed with the receptacle sheet about a terminal assignment.
Observed in the 1st Edition set, unverified. G-45: two documents that must agree are
generated from one source, and D5 is that source.

### The OPEN convention

**A box the tree does not fill in is drawn, marked, and keyed.** Rule 9 and D-142's
precedent: a sheet is issued with its blocked items carrying real ids and saying what
blocks them. A sheet that waits for everything to close is not a sheet.

**Open keys are never renumbered and never reused.** ?1 to ?30 are cited by
subsystems/interconnect-schedules.md and subsystems/water-float-requirement.md as
they stand. A key that closes is marked CLOSED in place, with what closed it. New
keys are issued upward. This follows D-149: an id that changes meaning is retired,
never renumbered or suffixed.

---

## 1. DEVICE ROSTER

**G-28: which device goes in which position is a build fact, labelled BY NAME, never
by position. G-42: one device, one name, everywhere.** Label each device by its name
the moment it is unpacked, not at installation - the two relay contact types look
alike and a swapped pair is a defect that passes every check.

### 1.1 Relays. Six envelopes, four states. order.md.

| Name | Duty | Contact type | Poles used |
|---|---|---|---|
| **K-PERM** | quiet + coil | gold | latch/seal-in; 24 V coil bus; PL-R |
| **K-FILL-D-Q** | quiet | gold | seal-in; the S-03 changeover pair; PL-G |
| **K-DRY-Q** | quiet | gold | seal-in; the S-20 changeover pair |
| **K-FILL-S** | power | standard | seal-in; fill solenoid |
| **K-FILL-D-P** | power | standard | transfer pump |
| **K-DRY-P** | power | standard | manifold pump |

**A split pair is ONE STATE IN TWO ENVELOPES.** Its two coils are driven in
PARALLEL from one point, never in cascade. Whether K-PERM splits is ?16.

### 1.2 Contactors. NAMED HERE FOR THE FIRST TIME. F-105, D-151.

**These devices had no names. The ladder distinguished them as "KM-DRV" and
"#2" - a part number plus an ordinal, which are the two things G-28 and T-013 forbid
an identity from being. They are named now, in the same shape as the relays, and the
old designations are recorded so an older reader is not lost, per G-42.**

| Name | What it is | Was called |
|---|---|---|
| **KM-DRV** | **The driver permissive contactor.** Removes motor supply from all eight stepper drivers at once, G-09 as amended by D-031. Pole 1 distributes the rail, pole 2 is the S-08 readback | "KM-DRV", "the permissive contactor" |
| **KM-CHIL** | **The switching element for the chiller and loop-pump receptacle.** Named for the function D-137 created | "KM-CHIL", "the chiller contactor" |

**Two things this naming settles and one it does not.**

**KM- is used for contactors and K- for relays**, so a build sheet cannot confuse a
25 A modular contactor with a 4PDT plug-in in a socket. That distinction is G-28's
whole subject.

**KM-DRV is not K-PERM, and the sheet never says "the permissive" unqualified.**
K-PERM is the master permissive latch, hardware, re-armed only by RESET. KM-DRV is
the Pi-commanded contactor that KM-DRV's coil circuit gates downstream of it. Every
sentence in the tree reading "the permissive" without qualification is ambiguous
between them, and rung 18 is where that ambiguity costs something.

**KM-CHIL names a FUNCTION, not a part in hand.** Which device performs it is ?8 and
is still open. The panel owns a second Finder 22.32 which has had no assignment since
D-108; MAIN-PANEL does not assign it, because that is a choice rather than a defect.
If a different device is chosen, that device is KM-CHIL.

### 1.3 Field and face devices, as the tree names them

| Name | What it is |
|---|---|
| **E-STOP** | 22 mm momentary, normally closed, top face |
| **RESET** | 22 mm momentary, top face |
| **PL-R / PL-G / PL-Y** | Red permissive lost, green filling, yellow healthy |
| **WB200** | The leak console. Powered, Form C dry contact out |
| **FV-1** | The fill solenoid, ASCO 8210G095AC120/60 |
| **LS-1 to LS-8** | Float POSITIONS, not parts. D-127, D-145 |
| **R-PI / R-XFER / R-MAN / R-CHIL** | The four receptacles. **R-MAN was R-CIRC**; renamed with the device under D-144, G-42 |
| **NDR-240-24** | The 24 V supply |

---

## 2. THE LADDER

### LEGEND

```
   --] [--   contact, OPEN when its device is at rest
   --]/[--   contact, CLOSED when its device is at rest
   --]L[--   FLOAT, CLOSED ON LOW WATER, open on high
   --]H[--   FLOAT, CLOSED ON HIGH WATER, open on low
   --( )--   coil
   --(*)--   pilot lamp
   --[ X ]-- a named device or load
   --< ?n >- A BOX THE TREE DOES NOT FILL IN.  Keyed to section 3
   ==>       a feed to a named bus, not a load
   .......   a conductor leaving this panel through a gland
   [ARC] [COIL] [SENSE]   the pole's DUTY.  Section 4
```

**Every float is drawn `]L[` or `]H[` and never `] [`.** D-154 closed F-093 by
topology: every float is a series element in a 24 V coil chain, so severed equals
open equals coil drops, and the requirement is that each float be CLOSED in the state
that permits the action to continue. **Six close on low water. Two close on high: the
day tank low-low and the storage pump-down.** The two inverted ones are the build
hazard F-108 names.

---

### SECTION A - 120 VAC. Left rail L1, right rail N.

```
   L1                                                                     N
    |                                                                     |
01  +---< ?1  MAIN DISCONNECT >-------------------------------------------+
    |         no disconnecting means is named anywhere in the tree
    |
02  +---< ?2  OVERCURRENT PROTECTION AND THE BRANCH SPLIT >
    |            |
    |            +==> BUS-A   panel loads, control supply, three receptacles
    |            +==> BUS-B   chiller circuit, DEDICATED per D-137        < ?3 >
    |
03  BUS-A ---[ FUSE ]---[ R-PI  receptacle, NOT switched ]----------------+
    |            P-07, closed.  The Pi has power whenever the panel does
    |
04  BUS-A ---[ NDR-240-24  primary ]--------------------------------------+
    |            24 Vdc 10 A 240 W.  Output trim 23.76 to 28.28 V, F-010
    |
05  BUS-A ---< ?4  K-PERM 120 V BUS POLE, IN OR OUT >==> BUS-AP     [ARC]
    |            An owner's pick under D-058, never made.  Rungs 06 to 08
    |            hang off BUS-AP if it is in, off BUS-A directly if it is
    |            out.  See section 5, item 2: this is a free choice again
    |
06  BUS-AP --] [--------[ FV-1  fill solenoid coil ]----------------------+
    |         K-FILL-S     120 VAC, 2-way NC, spring closed on power
    |         power pole   loss.  INRUSH 0.58 A                [ARC] < ?5 >
    |
07  BUS-AP --] [--------[ R-XFER  receptacle, transfer pump ]-------------+
    |         K-FILL-D-P   P-03.  Panel mounted, cord plugs in from
    |         power pole   outside, D-046                      [ARC] < ?6 >
    |
08  BUS-AP --] [--------[ R-MAN  receptacle, manifold pump ]--------------+
    |         K-DRY-P     P-04.  NO pole: closed when K-DRY is ENERGISED,
    |         power pole  which is the permitted state.  ?7 CLOSED [ARC]
    |
09  BUS-B ---< ?8  KM-CHIL, the switching element >
    |            |
    |            +------[ R-CHIL  ONE receptacle: chiller + loop pump ]---+
    |                     6 A chiller, 1.5 A loop pump, plus an
    |                     UNPUBLISHED compressor inrush.  P-05  [ARC]
    |                                                     < ?9, ?10, ?31 >
    |
    |    ***  NOTHING IS IN SERIES WITH R-CHIL.  F-110.  ***
    |    K-DRY gates R-MAN and does not gate R-CHIL, so the loop pump has
    |    no dry-run protection while sharing the day tank with the pump
    |    that does.  Drawn as it stands.  < ?31 >
```

### SECTION B - 24 VDC. Left rail +V, right rail -V, both from the NDR-240-24.

```
   +V                                                                    -V
    |                                                                     |
10  +==> the 24 V rail.  Nothing fixes the trim, so no coil, lamp or
    |    burden is sized at 24 V.  G-31 read against F-010, and F-056
    |                                                              < ?11 >
    |
    |    ---------------- THE PERMISSIVE STRING, G-07 ----------------
    |
11  +--]/[-----< ?12 >-----]L[--------]L[----------------------+ node P
    |  E-STOP   WB200       LS-2       LS-8                    |
    |  momentary Form C     DAY TANK   STORAGE                 |
    |  NC        leg        HIGH-HIGH  HIGH-HIGH               |
    |                                                          |
    |  Four series elements, not five.  THE STORAGE LOW IS NOT  |
    |  IN THE STRING - see rung 20 and ?15 CLOSED         [COIL]|
    |                                                           |
12  |                     +--] [--+                             |
    |                     | RESET |                             |
    | node P -------------+  NO   +--------+---( )-----( )------+
    |                     +--] [--+        |  K-PERM   K-PERM-P
    |                       K-PERM         |  coil     coil IF SPLIT
    |                       seal-in pole   |                    < ?16 >
    |                                      +  coils in PARALLEL, D-072
    |                                                        [COIL]
    |
13  +--] [------------------------------------------------==> node PB
    |  K-PERM pole      THE 24 V PERMISSIVE COIL BUS.  Every coil in
    |            [COIL] rungs 15, 18, 19, 20 and 22 is fed from here
    |
14  +--]/[--------------------------(*)-----------------------------------+
    |  K-PERM pole                  PL-R  "permissive lost"  [SENSE] < ?11 >
    |
    |
    |    ------------- THE DRIVER PERMISSIVE, G-09 as amended -------------
    |
15  < ?17  COIL POSITIVE: RAW 24 V, OR node PB >
    |            |
    |            +---( )---.......... ULN2003 SINK, BCM 18, display box
    |             KM-DRV       S-07 and S-09.  SUP-1 across the coil,
    |             coil         taken as given.  T-006 and T-007: the coil
    |                   [COIL] positive is HERE, the return is 4 ft away,
    |                          and the common is traced by hand
    |
16  +--] [-----------+----.......... P-06 to PUMP BOX A
    |  KM-DRV        |
    |  pole 1  [ARC] +----.......... P-06 to PUMP BOX B
    |                     One pole for motor-supply distribution, both
    |                     feeds off one terminal downstream of it, D-029.
    |                     **24 V VOLTAGE CLASS, ARC DUTY** - D-150's own
    |                     example, and section 4
    |
17  node at rung 16 -------------(*)-------------------------------------+
    |                            PL-Y, across the OUTGOING rail, D-045.
    |                            Measured, not commanded.  PL-R and PL-Y
    |                            both lit is impossible: KM-DRV is welded.
    |                            Across a supply, so no minimum switching
    |                            load applies                     [SENSE]
    |
18  node PB --< ?9  WHAT ENERGISES KM-CHIL's COIL >---------------( )----+
    |                                                       KM-CHIL coil
    |          D-137: the chiller and loop pump stop "when the permissive
    |          drops".  **THE PANEL HAS TWO THINGS BY THAT NAME.**  Taken
    |          from node PB, K-PERM drops it and the Pi cannot.  Taken
    |          from KM-DRV, the Pi can stop the water system, which G-26
    |          forbids.  Nothing on file says which          [COIL] < ?9 >
```

### SECTION C - THE FILL CHAINS. G-03: start float, stop float, relay seal-in.

```
   +V                                                                    -V
    |                                                                     |
    |    ---- STORAGE FILL.  Building supply into the storage tank ----
    |
19  node PB --+--]L[------+----]L[-----------------------+---( )----------+
    |          |  LS-6     |     LS-7                    |  K-FILL-S coil
    |          |  STORAGE  |     STORAGE                 |         [COIL]
    |          |  FILL     |     FILL STOP               |
    |          |  START    |                             |
    |          |           |                             |
    |          +--] [------+                             |
    |             K-FILL-S seal-in pole  [COIL]          |
    |                                                    |
    |    PL-G is NOT here: order.md records the owner's answer, PL-G
    |    means the DAY TANK.  K-FILL-S has two spare poles
    |
    |
    |    ---- DAY TANK FILL.  Storage into the day tank, by pump ----
    |
20  node PB --+--]L[------+----]L[--------]H[------------+---( )---( )----+
    |          |  LS-1     |     LS-5      LS-3          |    |       |
    |          |  DAY      |     DAY TANK  STORAGE LOW   | K-FILL K-FILL
    |          |  TANK     |     FILL STOP pump-down     | -D-Q   -D-P
    |          |  FILL     |               ?15 CLOSED    | coil   coil
    |          |  START    |                             |       [COIL]
    |          |           |                             |
    |          +--] [------+                             |  PARALLEL, D-072.
    |             K-FILL-D seal-in pole  [COIL]          |  ONE STATE IN
    |                                                    |  TWO ENVELOPES
    |
21  +--] [--------------------------(*)-----------------------------------+
    |  K-FILL-D-Q pole              PL-G  "filling", day tank
    |                       [SENSE] Agrees with S-03 by construction, both
    |                               being this relay's state       < ?11 >
```

### SECTION D - THE DRY-RUN INTERLOCK. G-25, and S-05 as closed by D-119.

```
   +V                                                                    -V
    |                                                                     |
22  node PB --+--]H[-------------------+--] [--+---( )-----( )------------+
    |          |  LS-4                 | RESET |    |         |
    |          |  DAY TANK LOW-LOW,    |  NO   |  K-DRY-Q   K-DRY-P
    |          |  the S-05 dry-run     | second|  coil      coil  [COIL]
    |          |  element under G-11   | block |
    |          |                       | < ?24>|  PARALLEL, D-072
    |          |                       |       |
    |          +--] [------------------+       |
    |             K-DRY seal-in / latch pole   |
    |                                    [COIL]|
    |
    |    ?25 CLOSED.  **K-DRY ENERGISED IS THE PERMITTED STATE.**  Forced
    |    by D-154, not chosen: LS-4 is a series element in this coil chain
    |    and is CLOSED while the level is fine, so the coil is energised
    |    while the level is fine.
    |
    |    A SEVERED LS-4 CONDUCTOR, AN OPEN COIL, A LOST 24 V RAIL OR A
    |    PERMISSIVE DROP ALL DE-ENERGISE K-DRY AND STOP THE MANIFOLD PUMP.
    |    That is G-39's question answered for this relay.
    |
    |    The latch does not auto-restart when the level recovers: the
    |    seal-in is broken and only a momentary MAKE re-arms it.  NO
    |    TIMING ELEMENT: D-060's other half was spent by D-119 and the
    |    device is not bought.
    |
23  ***  THE MANIFOLD PUMP HAS NO COMMAND ELEMENT, AND THAT IS THE
    ***  DESIGN RATHER THAN A GAP.  D-143.
    |
    |    K-CIRC was deleted by D-058.  K-DRY is a PERMISSION and not a
    |    command, D-063's surviving half.  Under G-26 the Pi may not
    |    command it.  **The pump runs continuously whenever K-DRY permits,
    |    which is what the owner ruled.**  Drawn because a builder looking
    |    for a start element must find the sentence saying there is none.
    |
    |    What this costs is on file and is not repeated here: C-12 is
    |    void, C-23 is reduced, and F-003 is restated as F-102
```

### SECTION E - SENSE CIRCUITS TO THE PI. G-22 asked of every one.

All four are the same shape and none is a copy: a dry contact wetted from 24 V, an
optocoupler LED in series, **the burden IN THIS PANEL**, an isolated Pi input, sense
inverted. Sized independently under G-23: **the minimum switching load belongs to the
contact and no figure is carried from another.**

```
   +V                                                                    -V
    |                                                                     |
24  +--] [--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX, S-08          |
    |  KM-DRV|                                                            |
    |  pole 2+--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |        [SENSE]  Two branches, 45 to 55 mA total against the
    |                 22.32's 1000 mW minimum.  At 42 mA an opto LED is
    |                 near its continuous rating, so the burden is a
    |                 second branch.  parts.md, GIVEN, not re-derived
    |
    |  SEVERED: the Pi input stays HIGH, reads contact open, reads a drop.
    |  A chosen property, not an inheritance
    |
    |  ****  G-30 CONFLICT, F-055.  Pole 1 of KM-DRV is an ARC pole
    |  carrying up to 8 A and pole 2 is a SENSE pole.  S-08 HAS NOWHERE
    |  TO MOVE: there is no auxiliary block and none was bought.  Marked,
    |  not resolved                                                < ?26 >
    |
25  +--]/[--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX, S-03          |
    |  K-FILL|                                                            |
    |  -D-Q  +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |  NC leg [SENSE]  ONE branch, about 12.5 mA against the 55.34's
    |                  300 mW minimum.  Copying S-08's two-branch
    |                  arrangement here would add a part for nothing
    |
    |  CLOSED means NO FILL.  OPEN means FILLING.  SEVERED reads as
    |  FILLING and dosing is inhibited.  D-042, by inversion.  T-016
    |
26  +--] [--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX
    |  K-FILL|                              the D-042 DOSE INHIBIT
    |  -D-Q  +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |  NO leg [SENSE]  THE OTHER LEG OF THE SAME CHANGEOVER POLE as 25.
    |  SAME            Same common, same potential, exactly one
    |  POLE            conducting.  G-27: any state where both agree is a
    |                  broken sense path                          < ?27 >
    |
27  +--] [--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX, S-20          |
    |  K-DRY |                                                            |
    |  -Q    +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |        [SENSE]
    |
28  +--]/[--+--[ Ropto ]--[ LED ]--......... to DISPLAY-BOX
    |  K-DRY |                              S-20's COMPLEMENT
    |  -Q    +--[ BURDEN, IN THIS PANEL ]-----------------------------+---+
    |  SAME  [SENSE]   order.md gives K-DRY-Q a G-27 complementary pair.
    |  POLE            A pair is two conductors and two Pi inputs        
    |  as 27                                                      < ?28 >
    |
    |  With ?25 closed, this pair's sense is fixed: K-DRY energised is the
    |  permitted state, so the NO leg conducts while the manifold pump is
    |  permitted.  ESTABLISHED FROM THIS BUILD'S TOPOLOGY, INHERITED FROM
    |  NOTHING, per F-017
    |
29  ***  F-094 IS DRAWN AND HAS NO DESTINATION  ***
    |
    |    +--< float spare changeover leg >---> ?
    |
    |    G-27 requires both legs to be READ and COMPARED.  G-01 makes
    |    floats invisible to the Pi, G-02 caps the Pi at one level
    |    signal, all five face holes are spoken for, and a comparison
    |    relay costs a coil the four-state topology does not have.
    |    CURRENT, not structural.  D-154 confirms the reader still does
    |    not exist                                                < ?29 >
    |
    |    NOTE: F-108's changeover requirement is a DIFFERENT requirement
    |    and it survives this.  It needs no reader: it makes the fail
    |    direction a terminal choice at the panel instead of an
    |    orientation in a tank
```

### SECTION F - THE FACE AND THE BAR

```
30  +--] [--+--(*)--+--(*)--+--(*)--+-------------------------------------+
    |  RESET |  PL-R |  PL-G |  PL-Y |                            [SENSE]
    |  THIRD    LAMP TEST while pressed.  Uses no hole.  PL-R is DARK when
    |  BLOCK    healthy, so without this a failed PL-R and a healthy system
    | < ?24 >   look identical
    |
31  GROUND BAR.  Every equipment ground from all four enclosures lands
    here, CBL-07.  The display box is polycarbonate and the pump boxes are
    plastic, so no box downstream offers a bonding path.  Drawn because a
    sheet that omits it reads as though the bar were somebody else's < ?30 >
```

**Rung count: 31.** Rung 29 is drawn as an absence and counted. **Rung 23 was drawn
as an absence in issue 0 of the ladder and is now a stated property**, D-143 having
answered it.

**Build order inside the panel: left to right, top to bottom**, as the 1st Edition
schematic instructed. Observed in the 1st Edition set, unverified. G-40b: it did
this, and this build has no reason to differ.

---

## 3. THE OPEN SCHEDULE

**25 live, 6 closed, 31 issued.** Keys are stable across issues.

### 3.1 Closed since issue 0 of the ladder

| Key | Rung | Closed by |
|---|---|---|
| **?7** | 08 | **?25.** K-DRY-P's pump pole is the NO side |
| **?13** | 11 | **D-154.** LS-2 is a series leg of the 24 V permissive string, closed on low water |
| **?14** | 11 | **D-154.** LS-8 as LS-2, in series with it |
| **?15** | 11, 20 | **MAIN-PANEL's ruling, section 5 item 1.** The storage low lands in the K-FILL-D coil chain and NOT in the permissive string |
| **?22** | 20 | As ?15. The two candidate landings collapse to one |
| **?25** | 22 | **D-154, by consequence.** K-DRY energised is the permitted state |

### 3.2 Live

| Key | Rung | What is open | Owner | What would close it |
|---|---|---|---|---|
| ?1 | 01 | No disconnecting means is named anywhere in the tree | MAIN-PANEL, P-01 | The owner's answer on whether the panel has its own disconnect or relies on the branch breaker. Search: `enclosure door interlocked disconnect switch DIN rail single phase` |
| ?2 | 02 | Branch circuit arrangement: how many circuits arrive, their protection, what shares each | MAIN-PANEL, P-01 | Owner states the supply, then the sum of rungs 03 to 09 against each circuit |
| ?3 | 02, 09 | The dedicated chiller circuit's rating. 6 A plus 1.5 A is continuous and the compressor inrush stacks on it. **parts.md states the DBE-200's locked rotor current is not published and any inrush figure must be labelled an estimate** | MAIN-PANEL sizes, owner supplies the LRA | A measured or manufacturer LRA. Search: `JBJ Arctica DBE-200 locked rotor amperage nameplate`; `hermetic compressor branch circuit sizing FLA LRA single phase` |
| ?4 | 05 | Whether K-PERM carries a 120 V bus pole | Owner picks, MAIN-PANEL draws | The owner's answer. **It is a free choice again - see section 5 item 2** |
| ?5 | 06 | The K-FILL-S pole's duty against FV-1. **The sizing event is the 0.58 A INRUSH at make and break, not the 0.21 A holding figure** | MAIN-PANEL | The 55.34's rating for an inductive 120 VAC load at that current, with electrical endurance. Search: `Finder 55.34 contact rating AC-15 pilot duty`; `Finder 55.34 electrical endurance inductive AC load 120 V` |
| ?6 | 07 | The transfer pump's nameplate. No electrical figure for it exists anywhere in the tree | WATER returns it, MAIN-PANEL sizes | Nameplate FLA and LRA, then the ?5 lookup |
| ?8 | 09 | **Which device is KM-CHIL.** Nothing on file names it. The panel owns a second Finder 22.32 unassigned since D-108 | MAIN-PANEL, and it is a purchase question | An owner's choice. The load exceeds the 55.34 class described in parts.md |
| ?9 | 09, 18 | **What energises KM-CHIL's coil, and from which bus.** Node PB or KM-DRV. Getting it wrong lets the Pi stop the water system, which G-26 forbids | Owner, then MAIN-PANEL | One sentence naming the bus |
| ?10 | 09 | **P-05 is an OPEN interface row whose End A names a chiller contactor D-108 says does not exist.** Rule 9 | BOSS holds the row | Rewriting P-05's End A against D-137 and KM-CHIL's name, then closing it |
| ?11 | 10, 14, 21, 30 | **Lamp and burden sizing at the BOTTOM of the trim range, not at 24 V.** F-056. PL-R and PL-G sit on contacts and owe G-24 a minimum switching load; PL-Y is across a supply and is exempt | MAIN-PANEL | Each lamp's actual current. Search: `22 mm LED pilot light 24 V DC current consumption datasheet`; `relay minimum switching load LED indicator contact oxidation` |
| ?12 | 11 | **CBL-06's text puts the WB200's contact legs in the 120 V chain. Three sources now say the string is 24 V** - D-154, water-float-requirement.md, and order.md's 24 Vdc K-PERM coil. **CBL-06's text is stale and the row still reads the other way** | BOSS owns the row. Reported, never fixed, per rule 2 | Correcting CBL-06. It decides the leak-console cable purchase, the E-stop's contact-block rating as a DC break, and whether the top-face bundle is one class or two |
| ?16 | 12 | Whether K-PERM splits into a quiet and a power envelope | Owner | order.md recommends buying the fourth gold, which is used either way |
| ?17 | 15 | **Where KM-DRV's coil positive is taken from.** F-019: from raw 24 V, one shorted output device on the logic board holds KM-DRV closed against a leak, an E-stop or a lost interlock and G-07 is defeated. From node PB, G-07 holds. **S-07 is OPEN and must state which** | MAIN-PANEL and DISPLAY-BOX jointly, BOSS freezes | Writing it into S-07. It costs nothing to choose correctly and cannot be got right by habit |
| ?18, ?19 | 19 | LS-6 and LS-7 as PARTS, and their trip heights | WATER, against S-01 | The float requirement's remaining half. **Their fail direction and contact sense are closed by D-154 and are drawn** |
| ?20, ?21 | 20 | LS-1 and LS-5 as parts, and their trip heights | WATER, against S-02 | As ?18 |
| ?23 | 22 | LS-4 as a part, and its trip height | WATER | As ?18. **Which position it is closed under D-154 and G-11: the day tank low-low** |
| ?24 | 22, 30 | **The RESET device's contact blocks: how many.** At minimum one NO for K-PERM and a second NO for K-DRY, plus a third if it proves the lamps. **The form is now settled - see section 5 item 3** | MAIN-PANEL | Search: `22 mm pushbutton contact block stacking depth NO`; `press to test pilot light 22 mm` |
| ?26 | 24 | **Whether the 22.32's poles share one contact volume the way the 55.34's four do.** F-055, open since 2026-09-01 | Owner, one lookup | Search: `Finder 22.32 modular contactor contact chamber construction`; `modular contactor pole barrier arc chamber separation`. If they share, S-08 violates G-30 and has nowhere to move |
| ?27 | 26 | **The D-042 dose-inhibit conductor has no interface row.** F-107 | BOSS creates rows | **Answered in section 5 item 4** |
| ?28 | 28 | **S-20's row describes one pole and one input while order.md builds a pair.** F-107 | BOSS | As ?27 |
| ?29 | 29 | **F-094 has no reader** | MAIN-PANEL raised it, the rules are BOSS's | An amendment to G-02, or a comparison relay and the coil it costs, or a recorded decision declining it. **Under G-44 the burden is on the addition** |
| ?30 | 31 | The ground bar, terminals, duct, DIN rail, the two panel-mount receptacles, the five gasketed top-face devices as one family, and the hood or slope. order.md lists all of these as not covered | MAIN-PANEL | A second order pass. Not started |
| **?31** | 09 | **NEW. F-110: the loop pump has no dry-run protection.** K-DRY gates R-MAN and not R-CHIL, and the two pumps share the day tank. **The failure is silent and self-masking: stagnant water satisfies the chiller's own sensor, the compressor stops, the tank warms, and nothing reports it** | WATER and MAIN-PANEL jointly | See section 5 item 5 |

---

## 4. DUTY CLASSIFICATION

**D-150 splits the class column in two. VOLTAGE CLASS drives insulation and
segregation and is INTERCONNECT's vocabulary. DUTY drives G-30's separation of power
from sense and is MAIN-PANEL's. This is the DUTY vocabulary.**

**It is not new.** It is D-072's three tiers stated as a vocabulary, so nothing is
invented and nothing has to be reconciled. G-44: an addition must say what it
prevents, and a fourth value would have to.

| Value | The one question it answers | Where it appears on this sheet |
|---|---|---|
| **ARC** | Does this pole break a load that arcs | Rungs 05, 06, 07, 08, 09, 16 |
| **COIL** | Does this pole break a suppressed coil, and nothing else | Rungs 11, 12, 13, 15, 18, 19, 20, 22 |
| **SENSE** | Does this pole carry a sense or indication current and break nothing that arcs | Rungs 14, 17, 21, 24, 25, 26, 27, 28, 30 |

**The three rules that use it.**

**G-30. ARC and SENSE never share a relay.** That is what the six-envelope split in
section 1.1 buys, and it is why order.md orders two contact types.

**COIL rides with SENSE only on two conditions**, both from D-072: suppression sits
AT THE COIL and not at the driving contact, and the coil current is checked against
the gold-consumption threshold. Where an envelope splits, all COIL goes with ARC.

**Duty is a property of the POLE, not of the conductor.** D5 derives each
conductor's duty from the pole it leaves, citing this section. G-45: it is generated
from one source rather than agreed between two.

**The case that made the split necessary, D-150's own: rung 16 is 24 V voltage class
and ARC duty.** Eight drivers with bulk capacitors on a DC break with no zero
crossing. A single column sorted by voltage put it with the quiet 24 V runs.

**And a case the tree had not classified: every float conductor is COIL duty**, being
a series element in a coil chain under D-154. **Per F-112 that break is DC and
inductive**, which is a different contact problem from an AC break at the same power,
and it belongs in the float requirement.

---

## 5. NOT PART OF THE ISSUED SHEET - MAIN-PANEL'S RETURN

**Sections 1 to 4 are D2. This section is the agent return that produced them and is
removed when the sheet is issued**, per document-plan.md section 3.2: no delivered
document carries reasoning. It is here because MAIN-PANEL was given one file.

### 1. A RULING: the storage low lands in the K-FILL-D chain, not the permissive string

WATER handed the landing to MAIN-PANEL with its half stated: the position protects
one device, the transfer pump, and an empty storage tank is not a hazard to anything
else. In the string it would drop the drivers, both fills, the manifold pump and the
chiller, and convert a refill errand into a full permissive reset.

**Ruled: the K-FILL-D coil chain.** Under G-44 the burden is on the wider scope and
nobody has argued for it. It removes a leg from the string rather than adding one.
?15 and ?22 close together and the ladder now draws LS-3 once.

### 2. ?25 CLOSED BY D-154, AND NOBODY NOTICED. THREE THINGS FOLLOW.

**D-154 answered the ladder's most load-bearing open mark without naming it.** Every
float is a series element in a 24 V coil chain, and LS-4 is CLOSED while the level is
fine. So K-DRY's coil is energised while the level is fine: **K-DRY energised is the
PERMITTED state.**

**a. The fail behaviour is now stated rather than open.** A severed LS-4 conductor,
an open coil, a lost rail or a permissive drop all de-energise K-DRY and stop the
manifold pump. G-39's question - what does it do with no power - is answered for the
one relay in this panel where it had never been asked.

**b. ?4 is a free choice again.** The ladder's finding 2 warned that D-058's argument
for dropping K-PERM's 120 V bus pole - "the pumps' coils already sit on the
permissive's 24 V bus" - is false where K-DRY energised means tripped. **D-154
selected the other column, so D-058's argument holds and the warning is withdrawn.**
The pole is now a redundancy question and not a safety one.

**c. ONE CORRECTION TO MAIN-PANEL'S OWN FILE.**
`subsystems/main-panel-buy.md` proposes that RESET carry a **normally closed** block
in series with K-DRY's seal-in, on the reasoning that the latch "cannot be cleared by
a normally open button". **That reasoning presupposed the energised-when-tripped
construction and it is wrong under D-154.** K-DRY is cleared by a momentary MAKE, so
**the second block is NORMALLY OPEN, not normally closed.** Withdrawn here; BOSS to
annotate that file, per D-051.

### 3. F-105: the contactors are named KM-DRV and KM-CHIL

Section 1.2 carries the names, what each is, and what each was called. Two points for
the record.

**KM- rather than K-.** A 25 A modular contactor and a 4PDT plug-in in a socket are
not interchangeable and G-28 exists to stop them being confused. A prefix that
separates the classes costs one letter.

**KM-DRV is deliberately not named "permissive".** The panel already has K-PERM, and
the ladder's finding 1 was that "the permissive" names two different things in
sentences that decide what stops the water system. Naming the contactor for its LOAD
rather than for its role removes the collision at the source rather than by a rule
saying to be careful, which is G-45's shape applied to a name.

**KM-CHIL names a function, not the part in hand.** ?8 stays open and MAIN-PANEL
assigns no device.

**G-42 requires this rename be applied to the whole tree in one pass or not at all.**
MAIN-PANEL may write one file, so the pass is BOSS's. Occurrences to change are in
`interface-table.md` S-08 and S-18, `parts.md`, `order.md`,
`subsystems/main-panel*.md`, `subsystems/interconnect-schedules.md` and
`subsystems/pump-boxes-p09.md`. **Both old designations are recorded in section 1.2,
so an older reader is not lost.**

### 4. F-107 ANSWERED: THE ROWS ARE MISSING, NOT THE CONDUCTORS WRONG

**The two rowless conductors are the ladder's ?27 and ?28 exactly.**

| Run | The conductor | End A | End B |
|---|---|---|---|
| **RUN-007** | **The D-042 dose-inhibit leg** | MAIN-PANEL: the **NO leg** of the K-FILL-D-Q changeover pole whose NC leg carries S-03. Common wetted at 24 V, optocoupler and burden in the main panel | DISPLAY-BOX: a **second** isolated Pi input, sense inverted |
| **RUN-008** | **S-20's complementary leg** | MAIN-PANEL: the **NC leg** of the K-DRY-Q changeover pole whose NO leg carries S-20. Same shape | DISPLAY-BOX: a **second** isolated Pi input, sense inverted |

**Neither conductor is wrong.** The dose inhibit is required by D-042 and is in
order.md's envelope map as "the S-03 / D-042 changeover pair". The K-DRY pair is in
order.md as "the G-27 complementary pair to the Pi". Neither is MAIN-PANEL's to
delete.

**RECOMMENDED SHAPE, and it is not two new rows. Amend S-03 and S-20 to state that
each is a complementary PAIR of two conductors from ONE changeover pole.**

The reason is G-45. An interface row is a CROSSING, and each of these is one
changeover pole crossing to one display box. **Creating S-21 and S-22 would create
two rows that must agree with S-03 and S-20 about the same pole, the same relay, the
same wetting circuit and the same burden - which is a written contract where one row
would be a mechanism.** D5 then carries two CDR- rows citing one S- row, and the wire
table's column 10 rule is satisfied: each conductor has an interface row, and one row
may back two conductors when it says so.

**The G-44 test on each, because the burden is now on the addition.**

| | What failure it prevents | What it costs |
|---|---|---|
| The S-03 pair | S-03's inversion already makes a severed cable read as FILLING, so dosing is already fail-safe. **What the pair adds is that the operator is TOLD the path broke instead of being blocked from dosing forever with no cause shown** | One conductor in an existing jacket, one opto and burden, one Pi input, one comparison in software. **The changeover pole and the envelope are already in the order** |
| The S-20 pair | The same, on the dry-run report | The same |

**Both pass and MAIN-PANEL keeps both.** The cost is one conductor in a jacket that
is already being pulled. **But the S-20 pair should not be built before ?17 and S-20
itself close**, and if the owner declines either pair under G-44 the conductor goes
and no row is ever created, which is cheaper than creating a row and deleting it.

### 5. F-110: the loop pump has no dry-run protection, and MAIN-PANEL's half is one sentence

**The electrical half is simply true and is now drawn: K-DRY's power pole gates R-MAN
and nothing is in series with R-CHIL.** Rung 09 says so on the sheet.

**MAIN-PANEL states no remedy, and G-44 is the reason rather than an excuse.** The
obvious remedy is to put R-CHIL behind a contact of K-DRY, and it must say what it
prevents and what it costs:

- **What it prevents:** the loop pump running dry on the same tank level that already
  stops the manifold pump.
- **What it costs to build:** nothing. K-DRY-P has three spare poles and one is an ARC
  pole in an ARC envelope, which is the correct duty for this load under section 4.
- **What it costs to operate:** a dry-run trip now stops the CHILLER as well as the
  manifold pump, and the chiller is the one load in this panel with a compressor. A
  latched trip cycles it off until a human presses RESET.
- **What it costs to repair:** nothing.

**Three things MAIN-PANEL will not decide, and they are the reason this is routed
rather than ruled.** Whether the loop pump is damaged by running dry at all is a
datasheet question named in WATER's file. Whether a chiller compressor should be
gated by a level float is a question about the chiller, not the panel. And **?9 is
upstream of it: until it is known what energises KM-CHIL's coil, adding a second
condition to that coil is designing against an open row.**

**The self-masking half is not MAIN-PANEL's at all** and is not addressed here:
stagnant water satisfying the chiller's own sensor is a wet-side failure with no
electrical end in this panel.

### 6. STATUS

**Stopped part-way, not finished.** MAIN-PANEL does not declare itself finished; BOSS
does that after another agent has built against this and found nothing, rule 7.

**What is issuable today:** sections 1 to 4, as D2, with 25 live OPEN marks carrying
real keys and named owners. That is a sheet a person can build the panel's logic from
and see exactly where it stops.

**What no agent may do against it:** build any rung carrying a live key, per rule 9.
Six rungs carry none: 03, 04, 13, 16, 17 and 27.

**Nothing here states a terminal number, a wire gauge, a breaker size, a part number
or a contact rating from memory.** Every part named appears in parts.md; every rating
is a requirement plus a search term.
