# DOSING proposal for F-002: keyed identity on the wet path

Returned 2026-08-30. One proposal, two mechanisms, not a menu. Nothing bought,
nothing changed. DOSING reported stopped part-way and did not declare itself
finished. Task 1 is blocked from being built on F-06, which is OPEN.

## The division of labour

Keying prevents the wrong mate. Identity makes the right mate obvious and makes
every joint keying cannot reach auditable. Keying works when nobody is looking.
Identity works when keying is absent, worn or defeated.

| Where | Primary | Backup | Why |
|---|---|---|---|
| The jug-end break point of each suction line, the only joint broken as routine work | Keying | Identity | F-002's actual locus. Prevention beats detection at a joint broken repeatedly by a person in a hurry |
| The jug's contents, which product was poured in | Identity | none | Keying has zero reach here. A correctly keyed line drawing from a correctly stationed jug that somebody filled from the wrong drum is still F-002. This residual hole stays open |
| Head barbs and tube ends, broken only at pump-tube service | Identity | end-to-end trace | A key on a joint broken once a season buys nothing and costs a permanent leak path. Do not key these |
| The token chain from software channel to head to tube to jug | Identity | end-to-end trace | Keying cannot see a numbering disagreement at all |
| Between jug changes | neither | | Both are point-in-time defences at the moment of the change. Neither watches a healthy connection go bad. Stated out loud so nobody books this as continuous verification |

Sequence at the joint that matters: read identity, the key permits or refuses the
mate, read identity again after mating. Two independent chances plus a mechanical
stop.

## What identity has to be

- **Redundant coding on independent axes.** A channel is a number, a colour and a
  fixed physical position at once. Any one axis may be lost without losing
  identity. Colour alone fails in poor light and to a colour-blind operator, a
  number alone fails at arm's length, position alone fails the moment anything
  is moved.
- **Fading must not be a failure mode.** Preferred: identity that is not printed.
  Engraved, embossed, stamped, moulded or coloured through the body, so wear
  removes the marker rather than degrading it into something still readable and
  wrong. Where printing is unavoidable it goes under an overlaminate and onto
  the legibility check list.
- **Degradation must be unambiguous, not gradual.** Rules out bare digits that
  wear into each other and colour families that fade toward each other.
- **Chemical duty is the union of everything on the wall**, not each channel's own
  product. Drips land on neighbours and one rag wipes everything.
- **Readable from Z5** in the orientation the item actually sits in, without
  moving, lifting or rotating anything, in the room's real lighting. A mark on
  the back of a jug is not identity.
- **One token, no translation anywhere.** If any point needs "head 3 is channel C
  is Grow A", the translation table is the defect.

| End | Requirement | Owner of the carrier |
|---|---|---|
| Head | A permanent, non-printed channel token on the lid at each head's penetration, visible with the box closed, on the face seen from Z5, not obscured by the tubing it identifies. Unique across BOTH boxes, never "head 1 of box B" | PUMP-BOXES owns the carrier, DOSING owns the scheme |
| Tube ends | Both ends of every suction and delivery line. Cannot slide along soft wet tubing, cannot be re-seated onto a different tube by hand, survives wet, wiped and flexed, placed within reach of the joint it identifies. Must not obscure a translucent section being watched | DOSING |
| Jug station | The FIXED spot in Z4 carries the permanent channel token, at eye height from Z5, with the jug-side coupling half's parking point | DOSING |
| Jug | Carries what is in it: product name and fill date. Its identity is chemistry, not channel | DOSING |
| Suction wand or dip tube, if separable | Carries the channel token. It is the part that physically enters a jug and the part most easily carried to the wrong one | DOSING |

**DOSING departed from O-09 deliberately here.** O-09 said head, tube ends, jug.
DOSING splits it: the station carries channel, the jug carries product. Reason: a
jug is a reusable vessel, and channel identity written on a vessel travels with
the vessel. If jugs are ever refilled from bulk, rotated or washed, a channel
token on the jug body IS the mechanism that creates F-002.

**Owner decision this forces:** are jugs dedicated to one channel for their whole
life, or are they interchangeable vessels? If dedicated, mark the jug too and the
station scheme is belt and braces. If interchangeable, marking the jug body with
a channel is forbidden. DOSING cannot answer it: jug volume, placement and change
frequency are all still open in its own file.

**Legibility is a scheduled check, not an installation event.** A faded label
looks done, which is why F-002 survives. The scheme is not complete without a
recurring pass that reads every token and replaces any that had to be squinted
at, and a rule that an unreadable token stops a jug change rather than being
worked around.

## Failure modes of the proposal itself

The keyed coupling on the suction side is the expensive half.

1. **It is an air-ingress path before it is a leak path.** On suction a bad seal
   does not drip and announce itself, it draws air. That is failure e: the head
   turns, the books decrement, less or nothing is delivered. **The fix for F-002
   can manufacture failures c, d and e.** This is the central honest cost.
2. **That failure is visible only if it is made visible**, which needs translucent
   tubing, O-03, and the jug end in the sightline, O-04. Both are free and
   neither is decided. Taking the coupling without those two trades a detectable
   failure for an undetectable one.
3. **Restriction and dead volume.** Every coupling family adds both, shutoff and
   non-spill types add more. The suction side is where a peristaltic head can
   least afford it, and it stacks on whatever lift the jug placement asks for.
   PUMP-BOXES must state what the head can pull before a family is chosen.
4. **Prime.** Added dead volume must be cleared at every change. If the head
   cannot clear it unaided, priming becomes a commanded step, which drags in
   CONTROL-SOFTWARE and books nutrient the arithmetic must be told about.
5. **Seals and springs are wear items in acid and base.** A seal in the pH-down
   line is a scheduled replacement nobody has scheduled, and its end-of-life
   symptom is air ingress, which is silent.
6. **A key that can be forced is not a key.** If it mates with hand pressure when
   wrong, or the key wears round, prevention degrades into identity and nobody is
   told it degraded.
7. **Too few distinct codes.** If the family offers fewer distinct keys than there
   are channels, keying becomes grouping and all remaining discrimination falls
   back on labels. Verify from the datasheet BEFORE purchase. First question to
   ask of any candidate.
8. **Colour-coded is not keyed.** Colour-coded but mechanically identical
   couplings mate wrongly and look correct. Buying those believing they are
   prevention makes things worse than doing nothing, because now there is a
   defence people trust.
9. **Human defeat.** An operator who cannot mate the correct pair at the end of a
   long day will find a pair that does mate and will not report it. Needs the
   written rule that a refusal to mate is stop-and-check, never force-and-
   continue, and enough distinct codes that a wrong mate is impossible rather
   than merely awkward.
10. **Mechanical load and cross-contamination.** A coupling is a rigid heavy
    element at the jug end: it can pull the tube, transmit strain to the head
    barb, or lift a dip tube clear of the liquid, which is failure e again. It
    needs support independent of the tube. Disconnected halves have exposed
    wetted faces and need a per-channel parking point; acid and base halves must
    not share a drip catch or a rag.
11. **The leak path lands in the wettest zone**, where a puddle drops the
    permissive per G-08. A nuisance trip mid-dose leaves a partial dose that G-04
    makes unmeasurable.

Identity's own failure modes: a token applied wrongly at build time is permanent
and self-consistent, and every later check confirms it, so only an end-to-end
trace catches it. Renumbering in software without relabelling the wall is silent
and worse than the original failure. Adhesive fails on wet, cold, condensing
surfaces and on soft tubing. And the faded-label trap, already written into
INTERCONNECT's own file for conductors, applies here word for word.

## What it does to a jug change

**Precondition that decides whether any of this works.** Keying only defends the
joint that is actually broken. If a jug change is done by lifting a wand out of
the empty jug and dropping it into a full one, or by refilling in place, no
coupling is ever consulted and the key is decorative. The procedure must be
defined so the break point IS the keyed joint. That is a design commitment, not a
purchase.

| Step | New? |
|---|---|
| 1. At Z5, read the station token and the product on the incoming jug. They agree or stop | New, seconds |
| 2. Confirm no head is turning. Whether a jug change is permitted mid-batch is CONTROL-SOFTWARE's state to expose | New if not already a rule |
| 3. Break the coupling, catch the retained slug, park the jug-side half at its own channel's point, never the floor, never a shared tray with acid or base | New, the slowest added step |
| 4. Remove the empty jug | Unchanged |
| 5. Stand the new jug at its station | Unchanged |
| 6. Mate the coupling. It must seat without force. A refusal is stop-and-check | New |
| 7. Re-read the station token against the product now connected | New, seconds |
| 8. Prime and watch until the line runs continuously liquid with no air at the head | Not new, but longer, and mandatory rather than optional. Needs translucent tube to be verifiable at all |
| 9. Confirm the coupling is not weeping and the line stays liquid-full when idle | New. This is the check on the failure the coupling itself introduced |
| 10. Enter the new full-jug volume per G-05 | Unchanged |

**It is slower.** A break, a drip-management step, a mate, two reads and a weep
check added to every change, plus a longer prime. Slower every time, forever, in
exchange for removing a failure that occurs rarely and costs an entire
undetectable batch. DOSING did not make that trade and says so.

Faster in one respect: no hunting, no cross-referencing four labels, no doubt
about which line came off which jug when two are open at once.

It constrains layout: two-handed clearance at each station, halves parked without
crossing lines, all readable from Z5. Competes with M-02 and O-04 for the same
wall and floor. INTERCONNECT arbitrates.

## Numbering agreement, and what happens without it

Yes, and not as a mapping. As ONE token. The chain is software channel index,
logic board output S-12, cable core, driver, head in one of two boxes, head barb,
tube, keyed coupling, jug station, jug, product. Any point requiring a translation
is a defect, because the operator's real workflow is "the UI says channel N is
low, walk to the wall, find N", and a translation step is performed by a person,
at night, from memory.

**If they disagree, it is F-002 with no jug ever touched.** A head labelled N but
driven by software channel N+1 doses the wrong product every batch, permanently.
Worse, it passes the checks: S-16 attributes a pH movement to the channel that
was commanded, so the pH check confirms a movement that came from the wrong pump
and reads healthy. G-05 decrements the wrong jug, so the remainder warnings are
wrong too, and the jug that actually empties does so without warning.

Recorded by BOSS as interface S-19 and findings F-006.


## OWNER RULINGS, 2026-08-30. This section overrides the proposal above where they differ.

| Ruling | Effect on this proposal |
|---|---|
| G-17, D-018 | Jugs are dedicated per channel for life. DOSING's station-versus-jug split is resolved in favour of BOTH: the station carries the channel token and the jug body carries it too, permanently. That is only safe because the vessel never changes channel, which is exactly what dedication guarantees. The jug still carries product name and fill date |
| G-18, D-020 | The jug change break point is AT THE JUG. The tube stays with the channel. The tube is never moved between channels. This is the design commitment DOSING said was needed, and it is now made: the break point is defined rather than left to habit |
| D-019 | The keyed coupling is HELD, not taken and not declined. With dedicated jugs and a fixed break point the key was buying less than it looked, and DOSING's own air-ingress warning is the reason to wait. Revisit after C-09 exists and the procedure is in use |
| D-019 | Translucent tubing, O-03, and the jug end in the sightline from Z5, O-04, ARE taken. Both free. Both were named by DOSING as the preconditions without which the coupling trades a detectable failure for an undetectable one, and they stand on their own merit without it |
| D-021 | The channel token is DEFINED by CONTROL-SOFTWARE, S-19. Everything in the identity section above is a CARRIER requirement. DOSING does not choose the numbering |
| D-022 | C-09 is first in the commissioning order |

**The jug change procedure, as decided.** The break point is the jug end. The
tube belongs to the channel and stays with it. Nothing on the wet path is ever
moved from one channel to another. The residual hole DOSING named stays open and
named: a correctly stationed, correctly labelled jug that somebody filled from the
wrong drum is still F-002, and no mechanism here catches it. Product identity on
the jug and the fill date are what stand between that failure and the tank.

**What is no longer required by this proposal:** coupling chemical compatibility,
key code count, seal wear scheduling, dead volume and prime burden, parking
points for disconnected halves, and the coupling's own leak and air-ingress
failure modes. All of that returns if and when the coupling is revisited. It is
recorded rather than deleted so that the cost is not rediscovered from scratch.
