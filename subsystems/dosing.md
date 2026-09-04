# DOSING

Read first: agents.md, interface-table.md, decisions.md, traps.md.

## Scope, owned completely

**THE JUG STATION is DOSING's, and this scope list did not say so until 2026-09-01.**
AUDIT's C22 asked whether DOSING knew it owed eight fixed, ordered, tokened stations;
DOSING confirmed it owns them and that the word appeared only in its F-002 proposal
and in the rulings written on top of it. Corrected here by BOSS, whose file it is.

The PVC dosing manifold as a physical assembly: the vertical probe section, the
probe wet fittings, the flow cell, every injection port, and the manifold body
between the two unions. The entire wet path from the manifold back to the pump
heads and on to the jugs: dose delivery tubing, head suction tubing, the
nutrient jugs, jug placement, and how a jug is changed without spilling or
losing prime.

Ends at the manifold unions FL-03 and FL-04, and at the pump head barbs FL-05 and
FL-06.

## Out of scope

The pump heads themselves and everything inside the pump boxes, including the
lid penetrations. That is PUMP-BOXES. The EZO circuits and carriers are
DISPLAY-BOX. Cable runs are INTERCONNECT. The day tank and the return drop are
WATER.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| G-10 | Probes sit first in line in a vertical section, ahead of every injection point, so a bubble cannot corrupt a reading |
| G-04 | No flow meters on the dosing lines. Nothing measures what a head actually delivered |
| G-05 | No level sensors on the jugs. Remaining volume is arithmetic |
| D-006 | DOSING owns manifold to head to jug as one path. PUMP-BOXES stops at the barb |

## Settled

- Manifold is PVC and the owner has the PVC.
- Injection is downstream of all three probes.
- The loop returns to the day tank by an open drop, WATER's side.

## Open, owned by DOSING

- Probe wet fitting requirement for each EZO probe, per the probe body. Return
  a requirement and a search term, not a part number.
- Injection port arrangement: how a port is made in PVC, and whether ports need
  a check to stop backflow into a dose line when its head is idle. Report the
  requirement, do not pick a part.
- Tubing selection for delivery and suction, against the head barb PUMP-BOXES
  returns and against nutrient chemical compatibility.
- Jug placement: height relative to the head, so a head is not asked to lift
  more than it can and so a jug change is possible without a tool.
- Whether a dose line can siphon when the head is idle, given jug height.
- Manifold orientation and mounting on the dosing wall, M-02, jointly with
  PUMP-BOXES.

## Settled 2026-08-30: the flow cell is a fitting, not an instrument

There is no flow signal into the Pi. The flow cell is a PVC body that holds the
probes in the moving stream. No output, no contact, no wire. Decision D-007,
interface S-13. Do not build a sensor pocket, a tapping or a wire route for it.

## Open design question routed to DOSING, answer only, change nothing

Read findings.md F-001 first. The only verification that exists is EC rising
during a dose, which confirms the manifold flowed but not which of the eight
heads delivered, and does nothing at rest or for pH up, pH down and fulvic.

Answer three things for your path, manifold to head to jug:
- what would it take to confirm a per-channel dose actually moved
- what it would cost
- where it would land physically

ANSWERED 2026-08-30. Nineteen options are in
subsystems/dosing-verification-options.md, ranked by cost, each with a
requirement, a search term, the numbers it needs, its physical landing and its
crossings. O-19, a flow meter per channel, is written down honestly costed and
neither softened nor advocated. Nothing is decided and nothing was changed.

Two things came out of that answer and are now BOSS-held:
- findings.md F-002, a jug reconnected to the wrong channel, which no
  flow-measuring option catches.
- interface-table.md S-16, the pH probe appearing to cover two of the three
  channels F-001 calls EC-invisible. That extends FROZEN row S-15, so it is the
  owner's decision.

DOSING did not declare itself finished and BOSS has not declared it finished.

## Owner rulings on that answer, 2026-08-30

| Ruling | Effect on DOSING |
|---|---|
| D-011 | pH attributes pH up and pH down. S-16 frozen with two constraints |
| D-013 | Fulvic stays unattributed. Do not solve it |
| D-014 | O-19, a flow meter per channel, is off the table. Do not bring it back unless something changes |
| D-015 | F-002 outranks the option list. O-09 and O-11 come back as their own proposal, separate from the nineteen |
| D-012, F-004 | Every tank-read check is delayed by an unmeasured interval. DOSING and CONTROL-SOFTWARE answer the settling time between them |

## Both tasks answered 2026-08-30, neither finished

1. F-002 proposal: subsystems/dosing-f002-proposal.md. Blocked from being built
   on FL-06, which is OPEN, and on DOSING's own open items: tubing selection, jug
   placement, the siphon question.
2. Wet side of F-004: subsystems/dosing-f004-wet-side.md. Blocked on WATER
   returning circulation flow at FL-03, DISPLAY-BOX returning probe response, and
   DOSING's own manifold volumes.

Four things DOSING found and did not fix, now BOSS-held: interface S-19 and
findings F-006, the channel token nobody owned; commissioning C-09, the
end-to-end trace; commissioning C-08 restated as an in-situ measurement, found
independently of CONTROL-SOFTWARE; and the C-02 ordering circularity, now fixed
in commissioning.md.

## Owner rulings on the F-002 proposal, 2026-08-30

| Ruling | Effect |
|---|---|
| G-17, D-018 | Jugs are DEDICATED per channel for life. Not interchangeable vessels. A jug is refilled with the same product forever or it is retired. So the channel token goes on the jug body permanently, as well as on the station |
| G-18, D-020 | The jug change break point is AT THE JUG. The tube stays with the channel and is NEVER moved between channels. This makes the key optional rather than load-bearing |
| D-019 | The keyed coupling is NOT taken yet. Held, not declined. DOSING's air-ingress warning is the reason: on a suction line a bad seal does not drip, it draws air, the head turns, the books decrement and nothing is delivered. Trading a visible failure for an invisible one is the wrong trade, and dedicated jugs plus a fixed break point already remove most of what the key was buying |
| D-019 | TAKEN INSTEAD, both free, both preconditions DOSING itself named: translucent tubing O-03, and the jug end in the operator's sightline from Z5, O-04. Both make air ingress visible |
| D-021 | The channel token is DEFINED by CONTROL-SOFTWARE. DOSING carries it on the tube, the jug station and the jug body. DOSING does not define it and does not invent a numbering |
| D-022 | C-09, the end-to-end trace, is FIRST in the commissioning order |

Revisit the coupling after C-09 exists and the jug procedure is in use.

## Unblocked 2026-08-30 by parts.md

FL-05 and FL-06 are closed on size: 3/16 in straight barb mating PharMed BPT B25,
4.8 mm ID by 8.0 mm OD, 1.6 mm wall. The F-002 proposal was blocked on FL-06 and is
no longer blocked on size. Tubing selection is still DOSING's: chemical
compatibility per product, and translucency under D-019.

**The fixed-tube null head shapes the jug path and it matches what DOSING
proposed.** The installed BPT loop is short and external tubing joins at its ends,
so the break point at the jug, and any keyed coupling if one is ever taken, sits on
external tubing and never on the pump tube. Confirmed, not assumed.

**New and unowned: interface F-10, the pump tube itself.** PharMed BPT B25, wetted,
a consumable at about 1000 h, inside PUMP-BOXES' head and part of DOSING's wet
path. D-006 gave DOSING the wet path and stopped PUMP-BOXES at the barb, which
leaves the tube between them. Answer jointly with PUMP-BOXES. Whoever owns it also
owns the change interval, the change procedure, and telling CONTROL-SOFTWARE that
C-01 is void for that channel.

**F-10 is CLOSED: DOSING owns the pump tube.** D-028. It is wetted, it is a
consumable, and it is in the path DOSING already owns end to end. The head is a
mechanical mount that happens to have a tube in it, and PUMP-BOXES stops at the
barb per D-006. DOSING therefore also owns the change interval, the change
procedure, and telling CONTROL-SOFTWARE that C-01 is void for that channel after a
change.

**A worn tube is F-001 arriving slowly.** It delivers less per revolution while
every instrument reads healthy, and the back-pressure calibration drifts across
tube life. The re-measure trigger is a tube change, not a date.

## Waiting on

| From | What |
|---|---|
| PUMP-BOXES | Head barb form and size, FL-05 and FL-06. Lid penetration, CBL-05 |
| DISPLAY-BOX | Probe cable termination and length limits, S-11 |
| WATER | Union type at FL-03 and FL-04, and manifold pump flow through the manifold |

## Do not

Do not decide port count, manifold diameter, tubing size or jug volume from
memory. Counts come back when the requirement is known.

## OPEN, routed 2026-09-03 by D-103. TWO ITEMS, AND NEITHER IS A REVERSAL.

**1. D-084's residual, and the sentence is the OWNER'S, not BOSS's.** F-077.

D-084 records: "a product outside those three duty classes arriving on any channel
invalidates the carrier specification, and **NOTHING WILL DETECT THAT AT ASSIGNMENT
TIME.**"

AUDIT's observation: **D-077 makes assignment time BE commissioning, and C-09 is a
commissioning row that already confirms which product is on which channel by eye -
first in the order under D-022, free, jugs in hand.** So there is a place to look
where the entry says there is none.

**What is offered, and it is one question:** add to C-09's script, per channel, is
this product an acid, a base, or a salt solution. **The three duty classes D-084
specifies against are exactly the three answers, so the test is already sized by
the specification it protects.**

**Return whether that question is SUFFICIENT** - whether a product can fall outside
all three classes while still answering one of them, and whether an operator can
answer it correctly from a label. **Do not return whether the residual is
accepted. That is the owner's and it stays his.**

**2. F-078, for your information and not for action.** D-013's premise, "fulvic
moves neither EC nor pH meaningfully", has no measurement named anywhere AUDIT
searched, and C-04 is scoped "per EC-moving channel" so the assumption excludes
the channel from the test that would check it. **Fulvic stays unattributed - the
owner froze that twice and O-19 does not come back.** This is recorded so that if
you ever measure a fulvic dose for another reason, you know the premise underneath
S-17 was never measured.

## GATED TO C-02, routed 2026-09-03 by D-104. YOUR FILE IS A COMMISSIONING PROCEDURE AND IT INSTRUCTS THE IMPOSSIBLE.

**subsystems/dosing-f004-wet-side.md says the settling timer must be gated on the
manifold pump being COMMANDED ON.** commissioning.md names that file as C-02's
FULL PROCEDURE.

**Under G-26 and D-052 the Pi commands one coil, the driver permissive, and nothing
else. There is no circulation-commanded signal. There never will be one while G-26
stands.** The claim it inherited traces back through control-software-f004.md to
S-09 as first written, and S-09 as first written came from the owner's original
project description, which D-052 records verbatim as "That was loose." F-079.

**This is the highest-priority item in the sweep and the reason is not severity, it
is audience: it is an instruction to a PERSON standing at the tank with a
stopwatch, not a claim in a document nobody executes.** C-23 governs the same
measurement and says the operator is the only enforcement. Your file says something
different, and the two are read by the same person on the same day.

C-02's row now carries a flag pointing here. **Rewrite the procedure so the
condition is what the operator can actually verify** - look at the pump, confirm it
is running, confirm it will still be running at the end of the window - **and not a
signal state. Nothing else in the procedure is in question.**

Write in ONE pass at the end.
