# MAIN-PANEL: the pole budget, PL-Y, the panel face, and the F-003 ruling

Returned 2026-08-30, first invocation. No file changed. Stopped part-way, not
declared finished.

## THE BUDGET IS NOT POLES. IT IS COILS. Everything follows from this.

Four 55.34 relays give sixteen changeover poles. **But all four poles of one relay
move together on one coil. So the panel does not have sixteen poles to spend. It
has FOUR INDEPENDENTLY COMMANDABLE STATES, four poles each.** Every function that
must be true or false independently of the others consumes an entire relay, and
its poles can then only say that same one thing.

### Independent states the design already requires

| # | Function | Why it needs its own coil |
|---|---|---|
| 1 | Master permissive latch | It latches and seals in against the series string and only RESET re-closes it, G-07 and G-13. Nothing else has that state |
| 2 | Storage fill seal-in | G-03: start float, stop float, seal-in. Drives the fill solenoid |
| 3 | Day tank fill seal-in | G-03 again, separate tank, separate floats. Drives the transfer pump, **and its state IS S-03** |
| 4 | Circulation pump | Commanded by the Pi, and the F-003 exercise run needs it commandable independently of both fills |
| 5 | Dry-run interlock | Must drop the circulation pump fast and independently of the Pi, and **it cannot be folded into the permissive string, see below** |
| 6 | Interposer for the permissive contactor coil | ONLY if the logic board cannot drive a 22.32 coil directly. OPEN |
| 7 | Interposer for the chiller contactor coil | Same question |

**Four relays. Five required states as a floor. Seven if both contactor coils need
interposing.**

### The shortfall, stated plainly

> **The panel needs five independently commanded states as a floor and has four
> relays. The dry-run interlock has no coil. If DISPLAY-BOX returns that the logic
> board cannot drive a 22.32 coil directly, each contactor coil takes another whole
> relay and the shortfall becomes three. PL-Y's problem is not a missing pole -
> spare poles exist - it is that EVERY SPARE POLE BELONGS TO A RELAY WHOSE STATE IS
> NOT "HEALTHY".**

Tightest arrangement MAIN-PANEL could draw, roughly 13 to 15 poles of 16 used:

| Relay | Poles | Spare |
|---|---|---|
| K-PERM, master latch | seal-in, permissive bus 120 V class, permissive bus 24 V class, PL-R on the NC side | **0, FULL** |
| K-FILL-S, storage | seal-in, fill solenoid, PL-G share if filling means either fill | 1 to 2 |
| K-FILL-D, day tank | seal-in, transfer pump 120 V, **S-03 to the Pi**, PL-G | **0, FULL** |
| K-CIRC | circulation pump 120 V, optional dry contact to the Pi | 2 to 3 |
| K-DRY | interrupt K-CIRC, dry contact to the Pi | **RELAY DOES NOT EXIST** |
| 22.32 #1, permissive | 24 V rail to both pump boxes, S-08 readback | **0, FULL** |
| 22.32 #2, chiller | chiller, loop submersible per G-12 | 0, unless one pole carries both |

Two things make K-PERM full rather than roomy:

- **A changeover pole has ONE common at ONE potential.** You cannot put the 120 V
  permissive bus on a pole's NO and a 24 V lamp on the same pole's NC. So PL-R needs
  its own pole, and the two voltage classes of the permissive bus need one pole
  each unless one feeds the other through an interposer, which costs a relay again.
- **K-FILL-D is required to carry a 120 V receptacle load and a roughly 12.5 mA SELV
  sense pole on adjacent poles of one socket.** That is a mixed-voltage socket. It
  may be permissible and it may not. **Requirement: rated insulation voltage and
  dielectric strength between adjacent poles of the 55.34 in the 94.74SMA socket,
  and whether the manufacturer permits mixed voltage classes across one relay. If
  not, K-FILL-D splits and the panel is short one MORE relay.** Search: Finder 55.34
  rated insulation voltage between contact poles; Finder 94.74 socket technical data
  dielectric strength contact to contact; relay socket mixed voltage adjacent poles
  segregation.

### The dry-run interlock cannot be hidden in the permissive string

The cheapest fix to the coil shortage would be to put the dry-run element straight
into the permissive series string, which costs zero relays. **It does not work if
the element is flow-proving, and WATER's F-003 answer makes flow-proving the only
element that can serve both duties.**

A flow element reads open at rest and open through every start-up transient. Put it
in the string and **the permissive cannot latch until there is flow, there cannot be
flow until the pump runs, and the pump needs the permissive. That is a deadlock, and
it appears only when you trace the loop by hand: T-007's shape applied to a chain
rather than to a coil.** It also drops the drivers and both fills for a dry tank,
far broader than the fault.

**The fifth relay is not optional.**

## What is actually available, and what a lamp on each would MEAN

| # | Contact | What a lamp there means | Note |
|---|---|---|---|
| 2.1 | K-PERM spare pole | The master permissive relay is latched | **This is PL-R inverted and nothing more. Two lamps, one bit.** The candidate the owner suspected, and he is right about it |
| 2.2 | K-CIRC spare poles | The panel is COMMANDING the circulation pump on | Commanded, not measured. parts.md's rule applies to a lamp as much as to software. Not health, an echo of an instruction |
| 2.3 | K-FILL-S spare poles | The storage fill relay is closed | PL-G's other half if filling covers both fills |
| 2.4 | K-DRY spare poles, IF the fifth relay is bought | The dry-run sense element currently reads made | **The ONLY contact in the whole panel that would say something about the WET SIDE rather than about the panel's own commands, and the closest thing to "healthy" that could ever exist here.** It does not exist yet: S-05 is open and WATER is holding it |
| 2.5 | The leak console's unused Form C leg | The leak console reports no leak | **A genuinely distinct bit: PL-R lights for a leak, an E-stop or any lost interlock and cannot tell you which.** Cost: the common is shared with the string leg so this sits at 120 V class, and C-06 already requires every conductor in that jacket to be 600 V rated |
| 2.6 | 22.32 #2 pole 2, only if one pole may carry both chiller loads | The chiller circuit is energised | **Nothing states whether G-12 means one pole per load or one pole feeding both.** Needs the loop submersible's nameplate and locked rotor, and parts.md is explicit that the DBE-200's LRA is not published and any inrush figure must be labelled an estimate |
| 2.7 | **Not a contact: a lamp across the outgoing 24 V rail, downstream of the permissive contactor** | **Motor supply is actually PRESENT on the conductor leaving this panel for the pump boxes** | MAIN-PANEL's recommendation. See below |
| 2.8 | Not a contact: a lamp across the NDR-240-24 output | Line power is present and the 24 V supply is up | Costs no pole, and **it is the only lamp still lit when everything else has dropped, which is exactly how you tell a dead panel from a tripped one** |

### The recommendation, marked as a recommendation

**No contact in this panel means healthy, and the owner is right that none exists.**
Of the real options only two carry a bit no other lamp carries: 2.4, which does not
exist yet, and 2.7, which does.

**PL-R shows the permissive STRING. A lamp downstream of the permissive contactor
shows whether the MOTOR SUPPLY ACTUALLY ARRIVED**, which is a different failure: a
coil drive that never energised, a contactor that did not pull in, a lost rail. **It
is MEASURED, not commanded. It is the panel's own eyes on the same physical fact
S-08 reports to the Pi, shown with no computer involved, which is the stated reason
the lamps exist at all.** It costs no pole, which is decisive. Its failure direction
is safe: a burnt lamp reads no motor supply, a false alarm.

Paired with PL-R it gives two independent bits instead of one repeated one:

| PL-R | PL-Y as 2.7 | State |
|---|---|---|
| off | on | Permissive string made and motor supply present |
| off | off | String made, motor supply absent: coil drive, contactor or rail |
| on | off | Permissive lost, everything down |
| on | on | **Impossible. If you see it, the contactor is welded** |

Two caveats not papered over: it shows the rail at the PANEL end of P-06, not at
the pump boxes, and sensing at the far end needs a return conductor and adds a
cable failure mode. And the lamp must tolerate the whole trim range, 23.76 to
28.28 V per F-010. Search: 22 mm LED pilot light DC wide voltage range 18 to 30 V
panel mount.

**If the owner wants PL-Y to mean something about the wet side, it is blocked behind
S-05 and F-003 and should stay UNWIRED until they close. An unwired lamp is honest.
A lamp relabelled to what it actually shows is better than a lamp labelled healthy
showing a relay coil.**

## PL-G and PL-R

**PL-R has an obvious contact and competes with nothing:** the NC side of a K-PERM
pole, lit whenever the master relay is de-energised, no logic needed. **One caveat
that matters: PL-R is DARK when the system is healthy, so a failed lamp is
indistinguishable from a healthy system.** The face has no lamp-test position and
all five holes are spoken for. **The cheap fix uses no hole: the RESET button is
already a momentary device on the face, and a second contact block on it can prove
all three lamps while it is pressed.** A requirement on the button, not a new
penetration. Search: 22 mm pushbutton auxiliary contact block stacking; press to
test pilot light 22 mm.

**PL-G has a contact, but only after the owner says which fill it means.** Day tank
means the fourth pole of K-FILL-D, free, **and it agrees with S-03 by construction
since both are that relay's state, which is a good property worth keeping.** Either
tank means a pole on K-FILL-S as well, in parallel. **Nothing states which fill PL-G
means.** MAIN-PANEL checked parts.md, its own file, G-02 and G-03, and the S-03 row.

They do not compete with each other. **PL-G takes the LAST free pole on K-FILL-D**,
the relay already carrying the seal-in, the transfer pump and S-03. That relay is
full the moment PL-G lands, and if the mixed-voltage question comes back
unfavourably it was already over-full.

**The third lamp is the one with no contact. PL-G and PL-R each name a state a
single relay already holds. PL-Y names a summary, and no relay holds a summary.**

## F-011 applies to all three lamps, and that is a promotion nobody made

F-011 names two contacts below minimum switching load, S-03 and S-08. **It stops
there and it should not. Every lamp driven from a relay pole is a third instance of
the same defect:** the 55.34's minimum is 300 mW at 5 V and 5 mA, and a modern LED
pilot lamp may well sit under it. **An oxidised lamp contact gives you an indicator
that works until it does not, which is the failure F-011 was written about, on the
devices whose whole job is to be believed.**

**D-036 and G-22 promoted "what does a severed cable read as" from two circuits to
every input. The same promotion is owed to F-011: ask it of every CONTACT, not only
of the two that feed the Pi.**

Requirement per lamp: the lamp's actual operating current against the minimum
switching load of the contact driving it, and if below, either a lamp that draws
more or a parallel burden, **which is precisely what S-08 already does and the
reasoning is already on file. G-23 applies: each contact's minimum is its own.**
Search: 22 mm LED pilot light current consumption 24 V DC datasheet; pilot lamp
incandescent versus LED current draw relay contact; relay minimum switching load LED
indicator contact oxidation.

## The panel face: routing, separation, DIN rail

**What the ordering does: everything travels the full height, twice, in opposite
directions.** Five devices' conductors run from the top face down the whole box.
A dozen field cables enter at the bottom and run up. They share the interior and
pass each other.

**The critical consequence: the E-stop and reset are in the permissive series
string, and the leak console's contact legs are in the 120 V chain. So the top-face
bundle is 120 V-class wiring, and the face gives it the longest run in the panel.
The one bundle you most want short and undisturbed is the one the face makes
longest.**

Three classes: **A**, 120 V line, branch circuits, receptacles, chiller and its
loads, the permissive string including the E-stop and the leak console legs, and any
pole switching 120 V. **B**, 24 V power: the supply output, all coils, and P-06, the
heaviest 24 V conductor in the box. **C**, SELV signal: the S-03 and S-08
optocoupler branches AND THEIR BURDENS, which parts.md puts in this panel, plus the
coil-drive pairs from the display box.

**The lamps have no class yet and that decides the routing.** 120 V-class lamps make
the top-face bundle homogeneous. 24 V lamps put two classes down the same height and
need either two separated runs or every conductor insulated to the highest voltage
present, which is C-06's rule applied inside the box. **Requirement: state the pilot
lamp voltage class before any top-face wiring, and note that option 2.7 forces PL-Y
to be 24 V-class specifically.**

**Layout that falls out of it:** two vertical wireways, one per side, dedicated by
class, 120 V down one and 24 V plus signal down the other, never sharing a duct and
crossing once, at right angles, at a defined point. With devices at the top and
glands at the bottom, **vertical ducts do the real work here and horizontal ones are
secondary; size them for fill before placing rails, not after.**

DIN rails horizontal, order set by the two ends of the box: **top rail** nearest the
five devices carries K-PERM and the permissive-chain relays, the top-face terminals
and the lamp supply, putting the shortest possible run on the string; **middle**
carries the four 55.34s on sockets, the two 22.32s and the 24 V distribution;
**bottom rail** nearest the glands carries field terminals, receptacle terminations
and **the ground bar, which C-07 makes this panel's responsibility because no
plastic box downstream offers a bonding path.**

**The supply pulls in two directions and the resolution is free.** It wants to be low
because P-06 is the heaviest 24 V conductor and its gland is on the bottom face. But
it is the panel's heat source and heat rises, and enclosure heat rise is already open
with no measurement behind it. **Put the supply low and reserve the column directly
above it as the vertical wireway rather than as a component rail. A duct above a heat
source is better than a relay above one, and that column is space the top-to-bottom
runs need anyway.**

**Glands: group by class along the bottom face, matched to the ducts**, so no cable
crosses the box to reach its own class's duct. Positions are INTERCONNECT's.
**T-008 applies at the count: count landings, not jackets.**

### Three things about the face MAIN-PANEL would not pass over silently

**(a) If TOP face means the enclosure's roof, all five holes are upward-facing
penetrations, and the room moves water tank to tank.** That is the orientation in
which a gasketed device is least able to keep water out, and anything that gets past
lands on the device's own contact block and then on whatever sits below it, which in
the layout above is the permissive-chain relays. **No environmental rating is stated
anywhere for the main enclosure; NEMA 4X is stated only for the display box.** The
top penetrations make that unstated rating load-bearing. Requirement: the
enclosure's rating and each 22 mm device's rating in that orientation, plus a drip
shield or hood if they do not match.

**(b) The receptacles have no stated home.** P-03 and P-04 are relay-switched
receptacle to pump cord. **A cord cap does not pass through a cord grip.** The face
decision covers the top face and the cord grips and says that is the whole panel
face. Nothing states where the receptacles are mounted, and a duplex receptacle
needs a rectangular cutout rather than a 22 mm hole. **Either they go on another
face, or the pump cords are cut and hardwired through grips and stop being corded.**

**(c) S-06 may now be in conflict with the face.** S-06 reads E-stop and manual reset
to "operator, mounted location", with INTERCONNECT owning where they land on the
wall. parts.md now puts both on the panel's top face. **Either S-06 is satisfied by
the panel face, or there is a second, remote E-stop.**

## The F-003 ruling

MAIN-PANEL accepts WATER's reframe and has one constraint on the exercise: **the
exercise needs K-CIRC to stay its own relay. The moment K-CIRC is shared to solve
the coil shortage, the exercise stops being independently commandable.** It must
also be inhibited below minimum submergence, in hardware, not software. And the
start-up bypass duration is MAIN-PANEL's but cannot be stated: it must be shorter
than the pump's dry-run tolerance and longer than the time flow takes to establish,
**and neither number exists on file. If the bypass is a timing relay it is a SIXTH
COIL and the shortfall grows again.**

> **THE RULING. A no-flow CONDITION at the discharge MAY drop the pump in hardware.
> A circulation VERIFICATION FAILURE MAY NOT. These are not the same event and they
> must not be wired to the same decision.**

The hardware drop protects the PUMP: dry-run protection, acting on the raw contact,
with dry-run timing, and its consequence is that the pump stops. The software stop
protects the BATCH: a judgement after a qualification window, and its consequence is
that the batch stops and tells the operator under G-16. **It may never drop anything
in hardware.**

Five reasons, and the fourth is the one MAIN-PANEL would not give up:

1. **A hardware drop on "no flow proved" is a latch that feeds itself.** The pump is
   the only thing that can make flow. The instant it is dropped the element reads
   no-flow forever and the condition can never clear on its own.
2. **The two duties want opposite bypasses and one contact cannot have both.** A
   bypass long enough to ride out verification's start-up transient is longer than
   the pump's dry-run tolerance, so one contact serving both either nuisance-trips
   or defeats the protection.
3. **The exercise run would defeat itself.** The exercise starts against a no-flow
   reading by definition, so it would trip the pump every time it ran: the whole
   first half of F-003, cancelled by its own protection.
4. **A hardware drop is SILENT, and every check downstream is a delayed tank
   reading.** If the pump is dropped in hardware the Pi still believes the loop is
   turning, and S-15, S-16 and F-004 go on comparing tank readings taken from a
   still tank. **That is the confident-wrong-answer shape this project has already
   been bitten by. A batch stop is loud. A pump that quietly went away is not.**
5. A hardware drop that clears itself when flow returns is an automatic recovery of
   a safety state, which G-16's spirit forbids; and one that latches needs a reset,
   **and the panel face has exactly one reset button, already committed to the
   master permissive.**

**If one flow element serves both duties:** its contact goes to K-DRY, the fifth
relay, with dry-run timing and a bypass not yet sizeable. **K-DRY interrupts K-CIRC
and LATCHES; it does not auto-restart when flow returns.** A SECOND POLE of the same
relay goes to the Pi as a dry contact, and the verification judgement is made in
software off that pole under G-16. **One element, one relay, two poles, two
different consequences, two different reset paths.**

That second pole is **a 55.34 contact feeding a Pi input: S-03's circuit shape, not
S-08's. A THIRD instance of that circuit, and nobody has an interface row for it.**
Now S-20.
