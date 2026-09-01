# The order

MAIN-PANEL's final list, 2026-09-01, after both gates cleared: the four 55.34s in
hand are STANDARD contact, and PL-G means the day tank.

**BOSS states no part number.** Every line is a requirement plus a search term. The
owner does the lookups, per G-15.

## Envelope map, as built

Rule applied throughout, per G-30 and D-072: **tier 1, arcing loads, and tier 3, sense
contacts and lamps, never share an envelope.** Tier 2, seal-ins and latches and the
coil bus, rides with tier 3 where it forces no extra envelope, on two conditions:
**suppression at the coil, and the coil current checked against the gold-consumption
threshold.** Where an envelope splits, all tier 2 goes with tier 1.

| Envelope | Duty | Material | Poles used | Spare |
|---|---|---|---|---|
| K-PERM | quiet + tier 2 | **GOLD, buy** | latch/seal-in; 24 V coil bus; PL-R | 1 |
| K-FILL-D-Q | quiet | **GOLD, buy** | seal-in; S-03 / D-042 changeover pair; PL-G | 1 |
| K-DRY-Q | quiet | **GOLD, buy** | seal-in/latch; G-27 complementary pair to the Pi | 2 |
| K-FILL-S | power | standard, from stock | seal-in; fill solenoid | 2 |
| K-FILL-D-P | power | standard, from stock | transfer pump | 3 |
| K-DRY-P | power | standard, from stock | circulation pump | 3 |

**Six envelopes. Three gold bought, three standard drawn from the four in hand, one
standard spare.** If K-PERM splits: **seven envelopes, four gold bought, four standard
drawn, zero standard spare.**

**Each split pair is ONE STATE IN TWO ENVELOPES, coils wired in PARALLEL from one
circuit and not in cascade.** The four-state topology is unchanged.

## The list

| # | Item | Min | If K-PERM splits |
|---|---|---|---|
| 1 | 55.34 4PDT, **AgNi plus hard gold** | **3** | **4** |
| 2 | 55.34 4PDT, standard | 0 | 0 |
| 3 | 94.74SMA sockets | **2** | **3** |
| 4 | Suppression, **fast release** | 3 | 4 |
| 5 | Suppression, ordinary | 4 | 4 |
| 6 | Timing element | 0 or 1 | same |

Item 1 is for quiet envelopes only and **never carries a power pole: the gold is
consumed above roughly 30 V and 100 mA and reverts to AgNi.** Item 2 is covered by the
four in hand. Item 3 is one per envelope BUILT: **a spare relay reuses the socket of
the one it replaces, so no spare socket is needed.** Item 4 covers K-PERM, both
envelopes if split, plus K-DRY-Q and K-DRY-P. Item 5 covers K-FILL-S, K-FILL-D-Q,
K-FILL-D-P and the chiller contactor coil. **Item 6 only if the S-05 fork lands
flow-proving, and that fork is not decided.**

**Not ordered, each for a stated reason.** Interposers, zero: G-26 leaves one Pi-driven
coil and the browser package already drives it. Suppression for the permissive
contactor coil, zero: SUP-1 is already across it in the corrected package, taken as
given and not respecified. **And item 5's chiller element is the one line MAIN-PANEL
would hold** - not because the coil is unknown, it is a 24 Vdc contactor coil, but
because the element choice can depend on what switches it, which is D-064. **It does
not gate the order.**

## Requirements per item

**Relays:** 4PDT plug-in, **coil range covering the WHOLE trim band per F-010 rather
than a coil nominally matched to 24 V**, with must-release voltage stated, because a
coil that does not release cleanly on a sagging rail is a permissive that does not
drop. `Finder 55.34 contact material options AgNi hard gold ordering code`; `Finder
55.34 DC coil operating range must release voltage`

**Sockets:** matching 4PDT, DIN rail, retaining clip, **rated insulation between
poles** - the mixed-voltage question, still separately open, and G-30 does not answer
it - and **clamp capacity per conductor**, T-009 and T-010. `Finder 94.74 socket
technical data retaining clip DIN rail`; `relay socket rated insulation voltage
between poles`

**Suppression, both grades: located AT THE COIL, not at the driving contact. Under
G-30 that placement is load-bearing.** Confirm the element can coexist with the
retaining clip in the socket; if not it lands on terminal blocks and becomes
terminal-plan work. `coil suppression diode versus diode zener versus RC snubber
release time`; `DIN rail relay socket coil suppression module compatibility retaining
clip`

**Timing element: must fail to PROTECTION ACTIVE, never to bypassed.** `timing relay
behaviour on power up and power interruption fail safe`

## G-28 applies AT DELIVERY, not at installation

**The two types look alike.** Label each relay by name to its envelope the moment it
is unpacked, never by position, per T-013. **A swapped pair is a defect that passes
every check: the gold relay silently degrades in a power envelope, and the standard
one carries the Pi-facing signals with the 300 mW floor and no gold.**

## MAIN-PANEL's recommendation: BUY THE FOURTH GOLD

Two independent reasons already point at splitting K-PERM and neither is resolved: the
coil-bus current, since that pole breaks the permissive contactor coil plus every
downstream relay coil at once in the same envelope as PL-R; and fast release versus
arc quench, which pull opposite ways on the one envelope that must do both.

**But the decisive argument is what the fourth gold does if the split never happens.
At the minimum there is one standard spare and ZERO GOLD SPARES, and under G-30 a
standard relay cannot substitute for a gold one. The envelopes with no spare are
exactly the ones carrying every Pi-facing signal and both contact-driven lamps.**

**So the fourth gold is used either way: as K-PERM-Q if the split happens, or as the
only gold spare in the panel if it does not.** Against that, resolving it later means a
second order, a second delivery, and rewiring an envelope already built and labelled.

**Buy four gold and three sockets.**

## Not covered by this order, so nothing reads as complete

The five gasketed top-face devices as ONE FAMILY, with the RESET carrying at least an
NO and an NC block. The hood or sloped cap, gated on F-025. The two panel-mount
receptacles per D-046. The lamps themselves with their burdens. The ground bar.
Terminals, duct and DIN rail.

**And one sizing item that must be settled BEFORE the lamp burdens are chosen:** per
G-31 read against F-010, **the 300 mW floor must be met at the BOTTOM of the trim
range or at whatever C-16 records, not at 24 V.** S-08's 45 to 55 mA window carries
headroom and survives it. **S-03 as stated sits on the floor at 24 V and does not.**
Five circuits are affected: S-03, the D-042 inhibit, the K-DRY pair, PL-R and PL-G.
See F-056.
