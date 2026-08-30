# The channel token

Declared by CONTROL-SOFTWARE 2026-08-30 under interface S-19 and decision D-021.
CONTROL-SOFTWARE is the definitional end. Every other subsystem CONSUMES this and
matches it. Nobody else defines a channel.

This file sits at the root, beside the interface table, because every subsystem
reads it. It is not a subsystem document.

## What a channel is

**A channel is an identity, not a component.** It is one of the eight given dosing
paths. It is not the driver, not the head, not the pin, not the core, not the
tube, not the jug and not the product. Every one of those is an ATTRIBUTE of a
channel and every one is replaceable without the channel changing. If every
physical item on the path were replaced one at a time it would still be the same
channel, because the channel is what those items agree they are.

**The token is its name, and the name is the identity.** There is no identity
behind the token that the token stands for. Software does not hold a channel
object with a token attached for display. The token IS the key. A name that
stands for something else can be mis-mapped. A name that stands for nothing else
cannot.

## Canonical form

    CH1  CH2  CH3  CH4  CH5  CH6  CH7  CH8

Exactly one written form. Uppercase CH, one digit, no space, no leading zero, no
punctuation. Not ch3, not CH 3, not CH03, not #3, not 3 alone. Spoken as "channel
three". A UI or a message may put words around the token, "CH3 low", but may
never substitute words for it.

Why this form:

- It matches the operator's actual sentence, from F-006: the UI says channel N is
  low, walk to the wall, find N. Any token that is not the N in that sentence puts
  a translation in the walk.
- The CH prefix gives the token its own namespace. INTERCONNECT labels conductors
  and MAIN-PANEL labels terminals. A bare 3 on a wall can belong to any of them.
  CH3 cannot.
- The set is 1 through 8. It contains no 0 and no 9. Stated rather than left to
  luck: a 6 read upside down is 9, and 9 is not a valid token, so an inverted read
  fails loudly instead of silently becoming another channel. There is no
  rotation-ambiguous pair inside the set.
- Bare digits wear into each other, which is the gradual degradation DOSING rules
  out. The digit axis alone does not satisfy that requirement. It does not have
  to: it is one axis of several and the carriers are non-printed. Named as a known
  weakness of this axis rather than hidden.

## What carries the token

Exhaustive for the chain in F-006: the step and direction output at S-12; the
cable core carrying it; the driver; the head; the lid penetration; both ends of
the suction line; both ends of the delivery line; the jug station; the jug body.

In software: the commanded step count, the booked volume, the jug remainder, the
fault, the log line, the config record, and every screen that names a channel.

**Attributes, bound to the token, never identities of their own:** which box the
head sits in, which pin drives it, which core carries it, which product it doses,
its steps per millilitre from C-01, its full-jug volume under G-05. Any of these
may change without the token changing. None may ever be used to name a channel.

## What each consumer is handed, and what it may not invent

Each gets the same eight tokens. Nobody gets a mapping, because there is nothing
to map.

| Consumer | Handed | Must not invent |
|---|---|---|
| DISPLAY-BOX, at the S-12 pin map | The eight tokens as the ROW KEYS of the step and direction section. The map is a table keyed by token, valued by whatever pin DISPLAY-BOX assigns | A driver number, an output number or a channel index of its own. A zero-based ordering. A renumbering so the pins come out tidy or contiguous. **If the header forces a non-monotone pin order, the pins are non-monotone and the tokens stay as they are.** Renumbering to make the pin map neat is the single most likely origin of this failure, because it looks like tidiness at the time. Also: no token derived from bus enumeration order or board position |
| INTERCONNECT, at the cable core | The eight tokens, applied as conductor identity at BOTH ends of every core carrying a per-channel signal | A per-cable restart if the eight are split across more than one cable. A renumbering to match a connector's pin order or a core's position in a bundle. A channel token for a spare core: a spare is a spare, there is no ninth channel. Where INTERCONNECT's own conductor scheme applies a code, the channel token appears IN ADDITION and the two are never merged or abbreviated into each other |
| PUMP-BOXES, at driver, head and box | The eight tokens, and the rule that the box is an attribute and not part of the name. Which tokens live in which box is PUMP-BOXES' decision and CONTROL-SOFTWARE's to receive: the definition does not wait on the box division | "head 1 of box B", any box-local numbering, or a board silkscreen designator used as channel identity. A replaced driver inherits the token of the position it lands in and does not bring a number with it |
| DOSING, at tube, jug station and jug body | The eight tokens for both ends of every suction and delivery line, for the fixed station, and, because of G-17, for the jug body itself. The jug carries the token AND the product name AND the fill date | The product name as identity or synonym: "the Grow A line" is not a channel name. A station token that differs from the jug token standing at it. A renumbering when a product changes. Under G-18 the tube stays with the channel, so a tube end token is permanent, and a tube that is ever moved must be re-tokened, which is a channel change under the change procedure below, not a maintenance action |

**Everyone.** The carrier is yours. The scheme is CONTROL-SOFTWARE's. It says what
must be carried. It does not say what the carrier is made of, how it is fixed, or
where on the item it sits.

## The axes

DOSING's carrier requirements stand unaltered: redundant coding on independent
axes, non-printed where possible, unambiguous rather than gradual degradation,
readable from Z5 without moving anything. This declares what those carriers carry.

| Axis | Status | Rule |
|---|---|---|
| Number, the digit of the token | BOUND | The axis that matches the UI and the operator's sentence, and the one that must never be translated |
| Position, canonical order | BOUND | CH1 to CH8 ascend in one consistent direction read from Z5, wherever the eight appear as a row: heads on lids, stations along the wall, tube ends, and every list of eight in the UI. **The order never restarts, never reverses between one row of eight and another, and never renumbers across a box boundary.** If the wall layout makes a monotone run impossible somewhere, that is reported to CONTROL-SOFTWARE as a defect in this declaration. It is not solved locally by reversing a row |
| Colour | DECLARED, NOT YET BOUND | One colour per token, one to one, permanent, identical in the UI and on the wall. Maximally separated hues, distinguishable to a colour-blind operator, no two that fade toward each other, and colour is never the sole differentiator anywhere. The binding waits on the owner |

## Two rules the UI owes the wall

1. **The token appears on every per-channel element of the UI, always.** A warning
   that says only "Grow A is low" rebuilds the translation table inside the
   operator's head, which is precisely where it cannot be checked. Product name is
   secondary and never a substitute.
2. **The token in a message, an alarm and a log line is the same string as on the
   wall, character for character.** A log read a season later needs no key.

## One binding rule that comes from S-16, not from legibility

The two most dangerous channels to confuse are pH up and pH down. Their movements
cancel, and S-16 attributes to the COMMANDED channel, so a swap between them is
invisible to the only check that looks at them.

**pH up and pH down shall not receive adjacent tokens and shall not receive
neighbouring colours.** Far apart on every axis at once. Declared now, applied
once the products are assigned.

## Forbidden

The line to hold: **a table binding attributes to one token is required. A table
mapping one identity to a different identity is the defect.** "CH3's pin is X,
CH3's core is Y, CH3's box is B, CH3's product is P" is the correct shape, and
there is exactly one such record per token. "software channel 3 = head B2 = core 7
= jug Grow A" is forbidden, because its existence proves those things have
identities of their own.

1. **Any translation table, in any medium.** A file, a code comment, a spreadsheet
   column, a laminated card taped to the wall, or an operator's head. If such a
   table would be USEFUL, the chain is already broken, and the fix is to correct
   the disagreeing end, never to write the table.
2. **Renumbering.** For tidiness, to make pins contiguous, to match a header, a
   connector or the box division, or to reflect something being physically moved.
   Renumbering in software without relabelling the wall is silent and worse than
   the original failure.
3. **A zero-based or offset internal index.** No array position is ever a channel
   identity. Per-channel state is stored in RECORDS KEYED BY THE TOKEN, never in a
   positional list of eight values. A positional list is an off-by-one waiting for
   an editor to insert a line, and G-04 and G-05 guarantee nobody will ever see
   the result.
4. **Arithmetic on tokens.** No N+1, no "the next channel", no "the other pH
   channel" computed from a neighbour. Sets are written out explicitly. This is
   the exact generator of the off-by-one this row exists to prevent.
5. **Two names for one channel, or one name for two things.** No internal driver
   ID alongside the token. No bare digit that could be a channel, a core or a
   terminal.
6. **The product as identity.** Retiring or swapping a product does not rename a
   channel.
7. **Box-local, cable-local or connector-local numbering.** Including "head 1 of
   box B".
8. **A ninth channel, a spare labelled as a channel, or a token reused after
   retirement.**
9. **Closing a gap.** If a channel is retired the remaining tokens do not shift
   down to make the set contiguous.
10. **Any local abbreviation or alternative rendering.** If a carrier cannot hold
    the canonical form, that is a carrier defect reported to CONTROL-SOFTWARE. It
    is never solved by inventing a short form at the wall.
11. **Deriving a token from hardware enumeration order.**
12. **A default UI list ordered by anything but canonical order.** Other sorts are
    allowed only where the token is on every row.

## When a channel has to change

Universal rules for every case:

- The change is made in ONE place first, the channel's record, and every carrier
  is brought into agreement in the same working session. No overnight partial
  state.
- While software and the wall may disagree, the channel is **OUT OF SERVICE**:
  software refuses to command it, and a batch that requires it STOPS and tells the
  operator. It does not substitute, skip or reorder. That is G-16 applied to a
  labelling change rather than to a check result, and for the same reason: the
  only safe direction of error is the loud one.
- **C-09 is re-run for all eight channels, never for the one that changed.** A
  crossing always involves at least two channels and a partial trace cannot see
  the half it did not trace. C-09 is free. A partial C-09 is not a cheaper C-09,
  it is a different and much weaker test.

| Case | The token | What else must be re-run |
|---|---|---|
| A head is moved between boxes | Goes with the channel to the new location. The vacated location is left carrying NO token at all and never inherits a neighbour's. Box, core and possibly pin update as attributes. Nothing renumbers | C-09 all eight. C-01 for the moved channel if its tubing or head orientation changed |
| A driver is replaced | Unchanged. The replacement inherits the token of the position and wiring it lands in. A driver is a consumable attribute | C-09, all eight if anything was unlanded and relanded. **And: if the driver's step configuration is part of what PUMP-BOXES sets, steps per millilitre for that channel is no longer the measured figure. C-01 for that channel is VOID until re-measured.** CONTROL-SOFTWARE will not carry a steps-per-millilitre figure across a driver change on the assumption that the configuration was reproduced |
| A product is retired, channel kept | Unchanged. G-17 means the jug is retired with its product, since that jug can only ever have held it. A new jug is stationed at the same station, same token, new product name and fill date. Whether the tube and head that carried the old chemistry may carry the new one is DOSING's and PUMP-BOXES' call. If the tube is replaced its ends are re-tokened in the same session | Full-jug volume re-entered per G-05. C-03 or C-04 for that channel. C-09 all eight if any wet-path item was disconnected. The F-002 residual is unchanged: a correctly stationed, correctly tokened jug filled from the wrong drum is caught by nothing here |
| A channel is retired outright | **The token is retired with it and is never reassigned.** Under G-17 that also retires a vessel: the jug is dedicated for life, leaves with the channel, and cannot be re-stationed. The live set becomes a subset of the eight with a gap in it, and the gap stays. Software marks the token retired and refuses to command it. It does not delete it, because the logs still name it | C-09 for the seven that remain. The retired one has nothing to trace, and the point of re-running is that its neighbours' wiring was disturbed |

**What must never happen in any case: discovering a disagreement at C-09 and
fixing it by relabelling the carrier that disagrees.** That converts a detected
crossing into a permanent silent one, and every later check confirms it. The fix
is to determine which end departed from this declaration, correct that end, and
re-run all eight.

## Open, and what it does not block

Declarable now, complete, consumable today: the identity, the canonical form, the
number and position axes, the attribute-versus-identity line, what every consumer
is handed and forbidden, the whole forbidden list, the change procedure, the C-09
script and the UI trace mode. **DISPLAY-BOX can key the S-12 map on tokens now.
PUMP-BOXES can return its box division now. INTERCONNECT can label cores now.
DOSING can token tubes and stations now. None of them is waiting.**

| From | What | Blocks |
|---|---|---|
| Owner, via DOSING | The colour set actually available in a non-printed, colour-through carrier meeting DOSING's union chemical duty. CONTROL-SOFTWARE will not name colours from memory: it is a material availability question and G-15 makes it the owner's lookup. The eight colours are bound once, in one table, when the set is known | The colour axis only. Not the definition, not C-09, which runs on number and position. It DOES sit ahead of permanently applying carriers, since engraving twice is rework |
| Owner | Which product sits on which token. Searched every markdown file: only three products are named anywhere in the tree, pH up, pH down and fulvic. The other five are not named in any file | The jug product labels and the S-16 non-adjacency rule. Not the definition |
| PUMP-BOXES | Which tokens go in which box. Theirs to decide, CONTROL-SOFTWARE's to record as an attribute | Nothing |
| INTERCONNECT | Whether a monotone ascending run from Z5 is achievable across the wall it arbitrates. If not, report it | Nothing, unless the answer is no |
| DOSING | Whether a tube-end carrier can hold the canonical three-character form without obscuring the translucent section being watched | Nothing, unless the answer is no, in which case it returns to CONTROL-SOFTWARE and not to a locally invented short form |
| Owner | Whether C-09's trace doses may go into a live tank, or whether C-09 rides the first real batch | C-09's scheduling, not its content |

Status: CONTROL-SOFTWARE reported stopped part-way and did not declare itself
finished. Per agents.md rule 7 this is finished only when another agent has built
against it and found nothing, and the physical half of that is C-09.
