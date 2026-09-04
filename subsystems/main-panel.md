# MAIN-PANEL

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

The 20.7 x 16.6 in enclosure and everything in it. Line input and protection.
The four Finder 55.34 relays and two Finder 22.32 contactors. The Mean Well
NDR-240-24 supply. Terminal blocks. Relay-switched receptacles. Every hardwired
chain: the storage fill seal-in, the day tank fill seal-in, the dry run
interlock, and the permissive series string including the leak console, the
E-stop and the manual reset. Internal layout, DIN rail, wire routing, glands.

Ends at its own terminals and glands.

## Out of scope

Where a float, leak sensor or E-stop physically sits, and what device it is:
WATER places field devices, INTERCONNECT places the operator devices on the
wall. Anything inside the display box or the pump boxes. Cable runs between
enclosures.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| G-07 | The permissive chain is a hardwired series string. A leak, an E-stop or a lost interlock drops everything independent of the Pi |
| G-08 | The leak console is wired into the permissive chain and drops power in hardware |
| G-09 | The permissive contactor removes power from every stepper driver at once, and provides an auxiliary contact for readback |
| G-13 | E-stop and manual reset are in the chain and are not software |
| G-03 | Both fills are start float, stop float, relay seal-in |
| G-01, G-02 | Floats are invisible to the Pi. The only signal to the Pi is one dry contact, day tank fill in progress |
| G-12 | Chiller and its loop pump on one contactor, own circuit |
| D-005 | MAIN-PANEL owns the permissive chain physically. Its terminations S-07 and S-08 are BOSS-owned interfaces and are not changed unilaterally |

## Settled

- Relays, contactors, supply and enclosure are bought, listed in decisions.md.
- Pumps and the chiller are 120 V corded and switch as loads, not as coils.
- No electrical inspection. That does not license unsafe work.

## Open, owned by MAIN-PANEL

- Line input, protection and branch circuit arrangement, P-01.
- Contact duty for each switched load, once WATER returns the solenoid coil
  requirement and the pump nameplate data.
- Which of the two 22.32 contactors is the permissive and which is the chiller,
  and whether the auxiliary contact needed for S-08 exists on the part the owner
  has. Report the requirement, do not assume the contactor has an aux.
- Seal-in logic for both fills, drawn as a chain, with the float contact duty it
  requires.
- Dry run interlock wiring. Blocked on WATER returning what it senses, S-05.
- Reset behaviour: what the manual reset re-arms and what stays dropped.
- Enclosure heat rise with the NDR-240-24 inside a closed box at 62 to 65 F.
- Terminal and gland plan. Terminal numbers are assigned late, not now.

## Assigned 2026-08-30: findings.md F-003, second end

Nothing verifies that the manifold pump is alive at rest. MAIN-PANEL
owns the relay that switches it and the dry run interlock chain, so it holds the
electrical end of this. WATER is primary and owns the pump, the tank and any
sense element placement. Neither may assume the other has it. See decisions.md
D-016 and interface row S-05, which is already open on what the dry run
interlock senses.

## Panel face decided 2026-08-30, lay out against it

Read parts.md. Five 22 mm step-drilled holes on the TOP face: E-stop momentary
NC, reset momentary NO, and three pilot lamps, green filling, red permissive lost,
yellow healthy. Nothing else penetrates that face. **Every cord grip is on the
BOTTOM face.**

The lamps are driven from relay poles and not from the Pi, deliberately, so the
panel states its condition with no computer involved.

## Open, added or sharpened 2026-08-30

- **The pole budget.** Three lamps on relay poles is a claim on the same poles as
  the fill chains, the seal-ins and the interlocks. **And the 22.32's poles are
  now both spoken for: pole 1 carries the 24 V rail out to both pump boxes, pole 2
  is the readback.** What drives PL-Y "healthy", and what healthy means as a
  contact rather than as a word, is yours.
- **The S-08 readback circuit is decided and is recorded in parts.md as given.**
  The aux exists: it is pole 2 of the 22.32. Do not re-derive the wetting circuit.
  Build to it.
- **S-03 is NOT covered by that decision.** The wetting circuit was designed for
  S-08. The day tank fill-in-progress contact feeding the Pi has not been
  addressed and F-011 still stands against it unresolved.
- **G-09 is amended, D-031: the permissive removes MOTOR SUPPLY only.** VDD is fed
  from the display box 5 V rail and is not switched by you.
- Read traps.md T-006 and T-007 before wiring any coil driven from the display
  box. The logic board is 4 ft away and that is exactly the remote-board case.

## Assigned 2026-08-30: the pole budget and PL-Y, D-037

**PL-Y is not a lamp question.** A lamp driven from a relay pole can only show a
CONTACT, and the owner does not think a single contact meaning "healthy" exists.
He will not define it in the abstract and will pick from real options.

Work out the pole budget first, accounting for every pole the design already
needs, and note that **both 22.32 poles are spoken for: pole 1 carries the 24 V
rail to both pump boxes, pole 2 is the S-08 readback.** Say plainly if the poles do
not add up, and what is short. Then list what contacts are actually available and
what a lamp on each would MEAN, in plain sentences.

**The pole budget is the useful half of this. It may be the thing that decides
what the lamps can say.**

## Both sense circuits are given, not yours to derive

parts.md records S-08 and S-03 as built. Build to them. **Size each independently:
the 22.32's minimum is about 41.7 mA at 24 V, the 55.34's is about 12.5 mA, and
G-23 says a minimum switching load belongs to a contact and no figure is carried
from the other.** S-08 needs two branches because at 42 mA an opto LED is near its
continuous rating. S-03 does not, and copying the two-branch arrangement onto it
would add a part for nothing.

## Waiting on

| From | What |
|---|---|
| WATER | Solenoid coil requirement P-02, float devices and duty S-01 S-02, leak sensor placement S-04, dry run sense element S-05 |
| DISPLAY-BOX | Coil drive form for S-07 and S-09, readback form for S-08, and what the logic board can sink or source |
| PUMP-BOXES | Driver supply voltage and current draw for P-06 |
| INTERCONNECT | Gland positions and cable entry side |

## Do not

Do not state a terminal number, wire gauge, breaker size or part number from
memory. Return the requirement and a search term.

## THREE THINGS ROUTED FROM THE SCHEDULES, 2026-09-04. ONE IS A NAMING DUTY.

**1. F-105, AND IT IS YOURS TO FIX BECAUSE YOU OWN THE DEVICES. THE DRIVER
PERMISSIVE CONTACTOR HAS NO NAME.**

order.md gives six real envelope names. **This device has none, and your own ladder
distinguishes two of them as "22.32 #1" and "#2". That is A PART NUMBER PLUS AN
ORDINAL - the two things G-28 and T-013 forbid an identity from being.**

You named the relays: K-FILL-S, K-FILL-D, K-DRY, K-PERM. **The contactors were
never named.** And **S-08's terminal is on one of them**, so the terminal schedule
cannot write a row until they have names.

**G-28 makes which relay goes in which socket a BUILD FACT labelled BY NAME. A
build sheet cannot say "the second 22.32".** Name them. BOSS does not name a device
it does not own.

**2. F-107. TWO RUNS CARRY A CONDUCTOR WITH NO INTERFACE ROW** - RUN-007 and
RUN-008, corresponding to the two unnumbered items on your own ladder. **A conductor
with no interface row does not exist under the wire table's rules, and yet two are
needed to build what you drew.**

**Either the interface rows are missing or the conductors are wrong. BOSS does not
guess which.** Say which, with both ends named, and BOSS creates the rows.

**3. THE CLASS COLUMN SPLITS IN TWO, D-150, and your G-30 work is why.**
INTERCONNECT found that the schema's four buckets sorted by VOLTAGE while G-30 sorts
by DUTY - **the driver motor supply being a POWER DUTY AT A CONTROL VOLTAGE.**

**So class becomes two columns: VOLTAGE CLASS, driving insulation and segregation,
and DUTY, driving G-30's separation of power from sense.** A conductor can be low
voltage and high duty and until now nothing could say so.

**The DUTY vocabulary is yours to state.** BOSS sets no threshold. INTERCONNECT
states the voltage vocabulary.

**Still open with you from the ladder: the chiller receptacle's switching element,
which state of K-DRY is the de-energised state, F-093's fail direction jointly with
WATER, and F-094 having no reader.**
