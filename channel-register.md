# The channel register

**The ONE record per token.** D-057, settling AUDIT run 2's B11.

channel-token.md declares what a channel IS. This file holds what each channel HAS.
**An attribute is recorded once, here. A subsystem file may reference it and may not
restate it.** Four files holding four attributes was close to the thing the
declaration's forbidden list calls a table in any medium.

Each subsystem returns its own attribute to BOSS, who writes it here. **No subsystem
edits this file**, on the same rule as the interface table.

The register is a table BINDING ATTRIBUTES TO ONE TOKEN, which the declaration
requires. It is not a table mapping one identity to another, which the declaration
forbids. The distinction is that every row is keyed by the token and no column is an
identity of its own.

| Token | Role | Jug | STEP pin | DIR pin | Cable core | Box | Product | Steps per ml, C-01 |
|---|---|---|---|---|---|---|---|---|
| CH1 | nutrient | 4000 mL | | | | | UNASSIGNED | |
| CH2 | nutrient | 4000 mL | | | | | UNASSIGNED | |
| CH3 | nutrient | 4000 mL | | | | | UNASSIGNED | |
| CH4 | nutrient | 4000 mL | | | | | UNASSIGNED | |
| CH5 | **pH DOWN** | **1000 mL** | | | | | pH down | |
| CH6 | **pH** | **1000 mL** | | | | | pH up by elimination, NOT stated | |
| CH7 | nutrient | 3785 mL, one US gallon | | | | | UNASSIGNED | |
| CH8 | nutrient | 3785 mL, one US gallon | | | | | UNASSIGNED | |

## The five unassigned products are a DECISION NOT MADE, not a missing record

Established 2026-09-01 by the owner, who checked rather than reconstructing. **Every
channel in the controller config is named "Channel 1" through "Channel 8". There are
no chemical names anywhere, and the config says so deliberately on its own line:
NOTHING THERE KNOWS WHAT IS PLUGGED INTO WHICH CHANNEL. Order, grouping and identity
are separate from the software.**

**So they are DELIBERATELY UNASSIGNED UNTIL COMMISSIONING, not pending. No subsystem
holds a row open waiting for them, and no subsystem assumes a product to get on with
its own work. The channel token exists precisely so identity can be carried without
the product being known.**

**C-09 is where they get assigned:** command one channel, watch which head turns,
which tube moves, which jug drops, which product. **That is the step that binds a
token to a product, and it happens with the jugs physically present.**

BOSS searched every markdown file for a channel-to-product list on 2026-09-01. **There
is none. The only occurrences of a product-like name are in channel-token.md's own
FORBIDDEN examples - "the Grow A line is not a channel name" - which are illustrations
of what is banned, not an assignment.** Nothing to strike.

## What the software does know, and it is all it knows

Six nutrient channels and two pH. **The two 1000 mL channels are the pH adjusters. The
controller independently marks CH5 as pH-down through its blocked-channels path, which
is a ROLE rather than a product. pH channels are excluded from every injection plan by
construction.**

CH6 is the other pH channel by elimination. **That is an inference, not a statement,
and it is marked as one.**

| Column | Who returns it | Blocked on |
|---|---|---|
| STEP pin, DIR pin | DISPLAY-BOX | S-12, and the Pi 5 header lookup |
| Cable core | INTERCONNECT | Not invoked yet, deliberately |
| Box | PUMP-BOXES | Its own decision, and the Position axis |
| Product | Owner | Five of eight are unnamed in any file |
| Full-jug volume | Owner, per G-05 | Jug volume undecided |
| Steps per ml | Owner measures, C-01 after C-17 | Both open |

**A channel is retired by marking the row retired. The row is never deleted, because
the logs still name it, and the token is never reassigned.**
