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
