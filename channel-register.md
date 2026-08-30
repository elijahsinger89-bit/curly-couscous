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

| Token | STEP pin | DIR pin | Cable core | Box | Product | Full-jug volume | Steps per ml, C-01 |
|---|---|---|---|---|---|---|---|
| CH1 | | | | | | | |
| CH2 | | | | | | | |
| CH3 | | | | | | | |
| CH4 | | | | | | | |
| CH5 | | | | | | | |
| CH6 | | | | | | | |
| CH7 | | | | | | | |
| CH8 | | | | | | | |

Every cell is empty and that is correct. Nothing is known yet.

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
