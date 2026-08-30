# MAIN-PANEL: the relay buy, the gasketed devices, and what D-042 did to the poles

Returned 2026-08-30, second pass. It acknowledges G-24, G-25, D-042, D-045 to D-048,
T-016 and T-017 and has built against them. **Two of them change its earlier
answer.** Stopped part-way.

## The relay count: confirmed with three corrections

**Definite: one, K-DRY.** G-25 makes it load-bearing rather than merely needed: the
hardware drop has to exist somewhere and it cannot live in the permissive string,
T-017.

**Correction A: the two interposers are ONE gate, not two.** Both contactor coils
are the same part with the same coil, so the answer is **0 or 2, never 1. Recording
them as two independently contingent relays invites buying one, and there is no
world in which one is right.**

**Correction B: the K-FILL-D split now has TWO gates, and D-042 made the second one
live.** D-042 puts a FIFTH pole demand on a four-pole relay:

| Demand on K-FILL-D | Class |
|---|---|
| seal-in | 24 V coil circuit |
| transfer pump receptacle | 120 V |
| S-03 fill in progress to the Pi | SELV, about 12.5 mA |
| **D-042 dose-inhibit, NC** | SELV, about 12.5 mA |
| PL-G | 24 V lamp |

**Five demands, four poles. It overflows UNCONDITIONALLY, unless S-03 and the D-042
inhibit are taken from the two legs of ONE changeover pole.**

They can be. **Both circuits are wetted at 24 V from this panel, both burdens are in
this panel, both are SELV. A changeover pole has one common at one potential, and
here both legs are at the same potential, which is exactly the case where sharing a
changeover is legitimate.** Common wetted at 24 V, NO leg one optocoupler branch, NC
leg the other, exactly one conducting at any moment, **which is the complementary
behaviour D-042 wants.** Each leg sized independently under G-23.

**So the gate is: EITHER mixed voltage classes are not permitted on one socket, OR
S-03 and the inhibit must be on physically separate poles. Either one alone forces
the relay.**

The trade, stated so the owner can pick: sharing costs nothing and buys the property
below. What it costs is common mode - a welded, oxidised or mechanically failed pole
takes both at once - **but they already share the same coil and the same cable
whether or not they share a pole, so most of the common mode exists regardless.**
Requirement: confirm both legs of a 55.34 changeover may be loaded simultaneously at
these currents, and the rated voltage between NO and NC legs.

If the slave is forced, split along the voltage boundary, which answers the
mixed-voltage gate in the same stroke: master carries seal-in, transfer pump and the
slave coil; slave carries the S-03/inhibit changeover and PL-G, with two spare.
**New failure mode if that is bought: the slave can fail to follow the master, and
S-03 then lies to the Pi about a fill that is running.** F-039.

### A free property that falls out of D-042, and MAIN-PANEL recommends taking it

**If S-03 and the inhibit are the two legs of one changeover and both ride the same
cable, a severed cable makes them CONTRADICT each other: one reads not filling, the
other reads filling. They are complementary by construction, so ANY STATE WHERE BOTH
AGREE IS A BROKEN SENSE PATH, and the Pi can detect it.**

**That converts a fail-safe into a FAIL-DETECTED, and it costs nothing** - both
circuits already exist and D-042 already bought them. **It is T-012's rule arriving
in hardware: derive it, or make the check an identity rather than a bound. Two
complementary contacts are an identity check on the sense path itself.**

Routed, not taken: the detection is CONTROL-SOFTWARE's and the input pair is
DISPLAY-BOX's.

**Correction C: the dry-run bypass relay needs a stated failure direction.** A timing
element in a protective chain has a mode the relay count does not show: **a timer
stuck in the bypassed state defeats dry-run protection permanently and silently.
T-014's shape in hardware.** Requirement: **the bypass must fail to PROTECTION
ACTIVE, not to BYPASSED**, and its behaviour on power-up, on interruption mid-bypass
and on component failure must be stated before it is bought. **That is G-22 asked of
a hardware element rather than a Pi input.**

## The reset question is answered and costs no relay, but it changes the RESET device

K-DRY latches, and something must clear it. **It cannot be cleared by a normally open
button and cannot be cleared from the permissive bus, because a dry tank does not
drop the permissive under G-25 so the bus never interrupts.** It needs a momentary
BREAK in K-DRY's seal-in.

**Proposed: the RESET button carries a second, NORMALLY CLOSED contact block in
series with K-DRY's seal-in.** One button, one action, both latches re-armed. No new
hole, no new relay, consistent semantics: RESET re-arms everything latched.

**Consequence: the RESET device now needs at least two contact blocks, one NO and one
NC, and three if it also proves the lamps.** A device-selection and stacking-depth
requirement behind the top face.

## The buy: do not buy five identical relays

**Coils: the requirement is a DC coil whose permitted continuous operating range
covers the WHOLE trim range, 23.76 to 28.28 V, not a coil nominally matched to
24 V.** Also needed: coil power and pull-in current, to answer the interposer gate
against DISPLAY-BOX's sink capability; and **the must-release voltage, because a coil
that does not release cleanly on a sagging rail is a permissive that does not drop.**

**Buy by DUTY. This is G-24's purchasing consequence.** The relays split into
low-level duty - the S-03/inhibit changeover, the lamp poles, the K-DRY contact to
the Pi, all well under the 300 mW minimum - and power duty - the receptacles, the
fill solenoid, the 120 V permissive bus. **A contact material suited to dry-circuit
switching generally cannot also carry a receptacle load, and using one at high
current can destroy the property you bought it for. The relays are not
interchangeable once bought, and which relay goes in which socket becomes a build
fact that must be labelled BY NAME, not by position. T-013.**

**Sockets:** one per new relay, and two things easy to miss: rated insulation between
poles, which is the open mixed-voltage gate; and **terminal clamp capacity per
conductor - T-009 and T-010 - any socket terminal expected to take two conductors
must be rated for two, and if it is not the second conductor goes to a terminal
block instead.**

**Suppression, and the choice is not the same for every coil.** The usual freewheel
diode lengthens drop-out time, **and two coils here are safety-chain devices where a
slower drop is a real cost: the master permissive latch and K-DRY.** So: K-PERM and
K-DRY get suppression chosen for FAST RELEASE, with the release-time penalty stated
rather than inherited. Everything else, both 22.32 coils included, gets suppression
chosen to protect whatever switches the coil, **where it also protects that contact
from arcing and therefore serves G-24.** One check MAIN-PANEL cannot do: whether the
socket accepts a suppression module AND the retaining clip at once.

Search terms returned: Finder 55.34 DC coil versions operating range must release
voltage; relay DC coil pull in drop out voltage percentage of nominal; Finder 55.34
minimum switching load gold plated contact option; Finder 55.34 AgNi versus gold
contact low level signal dry circuit; gold plated relay contact maximum current low
level switching degradation; relay contact material selection dry circuit versus
inductive load; Finder 94.74 socket DIN rail mount retaining clip technical data;
relay socket rated insulation voltage between poles; relay socket terminal two
conductors per clamp permitted; relay coil freewheel diode drop out time increase;
coil suppression diode versus diode zener versus RC snubber release time; DIN rail
relay socket coil suppression and indication module DC; contactor DC coil surge
suppression module; relay socket module slot compatibility with retaining clip;
Finder 55.34 changeover contact simultaneous loading NO and NC; relay changeover
contact voltage between normally open and normally closed.

## Lamps, and a routing recommendation

**All three lamps at 24 V class**, so the top-face bundle splits into two homogeneous
bundles rather than one mixed bundle needing everything insulated to the higher
voltage: E-stop and reset conductors are 120 V class because they are in the string,
the three lamp pairs are 24 V class, two separated bundles down the same height.

**PL-Y is exempt from G-24 entirely**, being across a supply rather than on a
contact, so it has no minimum switching load to satisfy. PL-G and PL-R still do.

## Receptacle placement, and the thing the owner should see first

**The panel's rating is set by its WORST penetration, and after D-046 that is the
receptacle face, not the top face.** D-047 gaskets five holes on top; D-046 puts open
receptacles with cord caps on another face, **and a standard cord cap does not
gasket. So buying five gasketed devices while leaving the receptacle face open buys a
rating the box does not have.** F-025 has to be answered for the whole box at once.
Remedies, the owner's pick: accept the receptacle face at a lower rating and orient
it so nothing lands on it, probably right in a room that is not wet; a while-in-use
cover; or a rated connector pair, which changes the pump cords and pulls in WATER and
INTERCONNECT.

Placement: **not the top face, not the bottom face** which is committed to cord
grips and would put a cord cap where every cable turns. **A side or front face,
oriented so a plugged-in cord hangs DOWN and away** - nothing lands on it and a
hanging cord drains rather than pools. **On the 120 V side of the box, adjacent to
the 120 V vertical duct**, so the switched hot reaches them without crossing to the
other class's duct: the single most useful placement constraint. Clearance for the
cord cap and its bend radius. Not facing where a jug is changed or a tank is filled.
**A cord anchor or hook beside each receptacle so a pulled cord loads the anchor and
not the receptacle's mounting.** Labelled by name, never by position, T-013. Grounds
to the CBL-07 bar. And each is a rectangular cutout consuming interior depth beside
the 120 V duct, to be checked before the rails are fixed.

## What gasketed devices constrain, force and cost

**It rules out "22 mm is 22 mm."** The hole diameter is not the seal. The seal is the
gasket, the bezel, the mounting torque, and the sleeper: **the range of panel
THICKNESS the device accepts. Requirement: the enclosure face's actual thickness,
measured, checked against every candidate's accepted range.** This can rule out an
otherwise correct device and it is not obvious until the parts are in hand.

**It rules out mixing families across the five holes** - three families is three
gasket systems, three thickness ranges and three torque procedures on one face,
validated by nobody. **All five from one series.**

**It rules out treating the hole finish as cosmetic. A step-drilled hole leaves a
burr and a slightly out-of-round edge, and the gasket now has to seal against it. The
hole finish is part of the seal, which it was not before.** A build step with an
acceptance condition: deburred, round, clean, torqued to spec.

**It forces the E-stop's rating to be stated IN THE ACTUATED POSITION.** A mushroom
gets struck and twisted on a face that will hold water, and a rating demonstrated on
an un-actuated device says nothing about the same device latched down after a year.
**D-048 makes this the only E-stop there is, so it does not get to be marginal.**

**It forces the RESET device to change**, per the reset resolution: at least one NO
and one NC block, three if it also proves the lamps. **And the top DIN rail moves
down**, because gasketed devices plus stacked blocks occupy depth and height behind
the face. Measure the deepest stack before fixing the top rail, not after.

**The real cost: D-047 and G-24 pull the lamps in opposite directions, and D-047
should win.** G-24's two remedies are a higher-current lamp element or a parallel
burden in the panel. **On a gasketed upward-facing face the first is a trap: a
higher-current element is generally shorter-lived, and every element replacement on
that face is a RE-SEAL EVENT on the one face where the seal matters most. You would
be solving a contact problem by buying a maintenance cycle on the worst possible
surface.** So keep the lamps low-current and long-lived and put the burden inside the
panel, which is parts.md's own reasoning with a third reason added by D-047.

## Does gasketed close the gap? No, and MAIN-PANEL says so plainly

**Five gasketed devices on an upward-facing surface give you five compliant seals and
one non-compliant system.**

1. A device rating does not raise the enclosure's rating. F-025 is still open.
2. **Standing water is a different duty from the duty these ratings are demonstrated
   against.** Ratings are generally specified against directed water or temporary
   immersion. **An upward-facing surface COLLECTS AND HOLDS INDEFINITELY; a vertical
   face sheds.** MAIN-PANEL refused to state which rating covers standing water: it
   is the lookup that decides the question.
3. **The gasket is the youngest part of the assembly and it ages.** On a vertical
   face that is latent. On a horizontal one it is immediately consequential, and the
   failure is invisible until something inside is already wet - **and what is
   directly inside, per the layout, is the permissive-chain relays.**
4. The E-stop is struck, repeatedly, on a surface that holds water, with no backup.

**Therefore a shield or hood is REQUIRED, not optional**, with every requirement a
constraint rather than a part: it must not compromise E-stop reachability or the
force an operator can apply; must not hide the three lamps from the normal sightline,
since they exist so the panel states its condition with no computer involved; must
shed away from the box and not onto the bottom face where every cord grip lives; must
be removable without breaking any device seal. **And sloping the surface is worth
more than covering it, if the enclosure can be mounted or capped so the top face is
not horizontal. A surface that sheds needs no hood.**

## Recorded, not proposed

PL-R lights for a leak, an E-stop or any lost interlock and cannot say which. **The
information exists in two places - a second contact block on the E-stop, and the leak
console's unused Form C leg - and there are no holes left to show it.** If the owner
ever wants "which interlock dropped" on the panel, that is where it lives, **and the
E-stop's block count is being decided right now, which is the cheap moment to leave
room for it.**
