# AUDIT: the downstream trace of "CH5 and CH6 are the pH pair"

Run 2026-09-03, by AUDIT, on the owner's instruction recorded in D-105.

**AUDIT changes nothing.** This file is the only file written by this run. Nothing
else in the tree was edited, and every item below is reported rather than fixed.

**No part number and no specification appears here from memory.** Nothing is
asserted from absence: every file read is named in section 1, every search is
named in section 2, and where I did not look I say so in section 6.

## What this run was asked

Grade every decision, finding, rule, interface row, commissioning row and document
section that is downstream of "CH5 and CH6 are the pH pair" on **which of three
different facts it actually needs**, then give the verdict under D-105.

| Dependency | What it needs |
|---|---|
| **PAIR-IS-pH** | Only that two of the eight channels are pH adjusters moving the probe in opposite directions. It does not care which two |
| **PAIR-IS-ADJACENT** | The two pH channels next to each other in the numbering, or maximally separated, or in some specific positional relationship. Colour separation, cable cores, physical layout, ordering rules |
| **IDENTITY-OF-CH6** | CH6 specifically to be pH-up. Nothing weaker will do |

| Verdict | Meaning |
|---|---|
| **DISSOLVES** | The item stops existing, because the property it was about is no longer fixed |
| **SURVIVES UNCHANGED** | It depends only on PAIR-IS-pH, which D-105 preserves as a per-channel setting |
| **MUST BE REWRITTEN** | It depends on adjacency or on CH6's identity, and those are now assignment-time properties |
| **WAS NEVER ABOUT CH6** | It was filed as downstream but is not |

The two things held together throughout, both taken as given:

1. **The owner's CH6 argument is sound.** Eight channels, two of them pH, CH5
   marked pH-down by ROLE through the controller's blocked-channels path, no third
   pH role, therefore CH6 is pH-up by elimination **from a role marking** and not
   from the retracted seed. That argument is better than the one it replaces and I
   have not tried to undermine it.
2. **D-105 makes role a per-channel setting.** Any channel may carry nutrient,
   pH-up or pH-down. No channel's role comes from its number any more.

Both at once means the CH6 answer is now **true and no longer load-bearing.** It
describes the configuration that exists today. It is not a property of the build.

---

## 1. What I read

Read in full:

- `agents.md`, rules 1 to 11, the AUDIT section, and "Classify before you question"
- `channel-register.md`
- `channel-token.md`
- `colour-map-proposal.md`
- `commissioning.md`
- `interface-table.md`, all subsystem, cable and mechanical rows

Read in the parts named:

- `decisions.md` - the frozen rule table at lines 43 to 90 (G-01 to G-37, including
  G-17, G-18, G-21, G-26, G-32 as amended, G-33, G-34, G-36, G-37); D-077 and D-078
  at 1120 to 1160; D-083 at 1206 to 1278; D-084, D-085, D-086, D-087, D-088 at 1278
  to 1360; D-089 and D-090 at 1355 to 1400; D-099 to D-101 at 1560 to 1620; the
  second-source confirmed table, D-105, D-106 and D-107 at 1800 to 1935
- `findings.md` - F-060 to F-080, and F-063 in its own row; the header note
- `traps.md` - T-018, T-019, T-020, T-021, T-022, "What survived the seed
  retraction", T-023, at lines 340 to 509
- `software-spec.md` - the heading list; 2.5.1 to 2.5.3 and 2.2.5; section 3 in full
  (3.1 to 3.5, including 3.2); 5.1, 5.2, 5.6; 6.3, 6.5, 6.6; 7.3, 7.4; the N-5 and
  N-6 rows of section 10
- `subsystems/control-software.md` - the D-105 section at 284 to 320, and the
  colour note at 237
- `subsystems/dosing.md` - scope, the F-001 routing, the owner rulings at 55 to 125
- `subsystems/dosing-f002-proposal.md` - the carrier table and the jug station
  split at 40 to 70, the procedure and owner rulings at 130 to 203
- `subsystems/dosing-f004-wet-side.md` - the D-105 correction header, the procedure
  steps 4 to 10, and the "one number or many" table at 150 to 185
- `order.md` and `parts.md` - searched for channel, token, marker, colour, label and
  the pH tokens. **Neither file contains a channel token, a channel colour or a
  channel marker line item.** That is a checked absence, not an assumed one
- `audit/2026-09-03-second-source-sweep.md` - chains 6 to 26, CONFIRMED 3, and open
  questions 3 to 7
- `audit/2026-09-03-decisions-impossibility-grading.md` - rows 33 and 55, and line 28
- `audit/2026-09-03-doc12-vs-frozen.md` - lines 91, 122, 125, 434 to 454, 503, 551

Not read, and named so nobody reads silence as coverage:
`subsystems/water.md`, `water-s18-f003.md`, `main-panel.md`, `main-panel-buy.md`,
`main-panel-poles.md`, `pump-boxes.md`, `pump-boxes-p09.md`,
`pump-boxes-pulldowns.md`, `display-box.md`, `display-box-sweep.md`,
`display-box-short-column.md`, `control-software-f004.md`, `control-software-p09.md`,
`interconnect.md`, `dosing-verification-options.md`,
`audit/2026-08-30-channel-token.md`, `audit/2026-08-30-displaybox-vs-mainpanel.md`.
**All of these were reached by the tree-wide greps in section 2 and none returned a
hit on the pH pair, the pH roles or the adjacency rule** except the ones listed as
items below. A grep hit is weaker than a read, and I say so.

## 2. The searches I ran

Every one was run over the whole tree with `--include=*.md` from the repository root
unless noted.

| # | Search | Why | What it turned up |
|---|---|---|---|
| 1 | `find` for every `.md` file in the tree | To know the population before searching it | 36 files |
| 2 | `CH5\|CH6`, excluding `audit/` | The token pair by name | 8 files: `traps.md`, `decisions.md`, `findings.md`, `channel-token.md`, `colour-map-proposal.md`, `channel-register.md`; plus zero hits in `order.md`, `parts.md`, `commissioning.md`, `software-spec.md`, `interface-table.md` and every subsystem file |
| 3 | `pH pair\|pH channel\|pH adjust\|pH-up\|pH up\|pH-down\|pH down\|two pH\|pH station`, case-insensitive | The pair by role rather than by token, which is where the survivors live | `traps.md`, `decisions.md`, `findings.md`, `interface-table.md`, `channel-token.md`, `commissioning.md`, `software-spec.md`, `dosing-verification-options.md`, `control-software-f004.md`, `control-software.md`, `dosing-f002-proposal.md`, `dosing.md`, `dosing-f004-wet-side.md` |
| 4 | `adjacen\|non-neighbour\|neighbouring colour\|maximally separated\|separation`, case-insensitive | PAIR-IS-ADJACENT items that never name a token | Found `subsystems/control-software.md` lines 312 to 314, which is the restatement instruction and which no starting-list item pointed at. Also confirmed that every other "adjacency" hit in the tree is about conductors and relay poles, not channels |
| 5 | `\brole\b`, case-insensitive | What is already keyed to role and therefore already safe | `traps.md` 471 to 478, G-32, G-34, `channel-register.md` role column, `software-spec.md` 2.6.4 and 3.2, `commissioning.md` C-09, `subsystems/control-software.md` 284 to 320 |
| 6 | `marker` and `station`, case-insensitive | Whether anything physical is already committed to a token | Markers exist only as decisions and proposals. Stations are DOSING's and carry the token, not the role |
| 7 | `F-063\|F-064\|F-066\|F-071\|F-080\|D-085\|D-086\|D-099\|D-105` | Citations of the items, to catch consumers the starting list omitted | Found `subsystems/control-software.md` 284 to 320 and `subsystems/dosing-f004-wet-side.md` header as D-105 consumers |
| 8 | `wall length\|the gap\|injection plan\|injection group\|blocked-channel\|blocked channel` | The plan-builder mechanism and D-085's subject | `channel-register.md` 80 to 81, D-077, D-085, D-105 |
| 9 | `forearm\|acid or base\|hazard rule` | Whether DOSING's chemistry hazard rule is keyed to role or to token | Keyed to the product's chemistry. `traps.md` 471 to 474 and D-088 |
| 10 | `label\|marker\|token\|colour\|dosing` in `order.md`; `pH up\|pH down\|pH pair\|CH5\|CH6` in `parts.md` | Whether anything has been bought against the pair | **Nothing. No channel marker, colour or label is on order and none is in the parts list.** This is what makes the marker gate still free |

**What the method does not find**, stated because agents.md rule 8 requires it: a
downstream item that depends on the pair without using any of the words in searches
2, 3, 4 or 5. I searched by wording and by citation. An item that assumes the pair
silently would not surface. This is the same limit `audit/2026-09-03-second-source-sweep.md`
records as its own open question 5.

---

## 3. The graded table

63 items. Where an item needs two of the three facts, the stronger one is the
primary and the other is named in the row.

| # | ID or location | What it says | Dependency | Verdict |
|---|---|---|---|---|
| 1 | **F-063** | The S-16 non-adjacency rule is violated, because the two pH channels are CH5 and CH6 and they are adjacent tokens | **PAIR-IS-ADJACENT**, plus IDENTITY-OF-CH6 to know the rule is violated at all | **DISSOLVES** |
| 2 | **F-064** | The Position axis constrains the SEQUENCE of the eight tokens and says nothing about SPACING | None of the three. It is a reading of the ordering rule and depends on no volume and no role | **WAS NEVER ABOUT CH6** |
| 3 | **F-065** | The suction pickup is UNSPECIFIED rather than mis-specified. Core finding | None of the three | **WAS NEVER ABOUT CH6** |
| 4 | **F-066** | The two smallest containers are the two pH channels, so the pair the system most wants left alone is handled most often | **IDENTITY-OF-CH6**, through the two-1000-mL pairing | **DISSOLVES** |
| 5 | **F-071** | The size axis already separates the pH pair for free. Withdrawn by DOSING 2026-09-02 | **IDENTITY-OF-CH6** | **DISSOLVES** (already withdrawn; D-105 removes the last route by which a vessel size could imply a role) |
| 6 | **F-080**, the defect half | Six files state the pairing flat; CH6's origin is a retracted seed | **IDENTITY-OF-CH6** | **DISSOLVES**. D-105 says so in terms |
| 7 | **F-080**, the marker gate | The channel markers are not made until C-09 has bound tokens to products | PAIR-IS-pH. The gate needs only that role and product are established at C-09 | **SURVIVES UNCHANGED**, and D-105 extends it to bind role as well as product |
| 8 | **F-002** | A jug reconnected to the wrong channel produces the F-001 symptom and no flow option catches it | None of the three | **WAS NEVER ABOUT CH6** |
| 9 | **D-011 and S-16 constraints 1 and 2** | The pH probe attributes the two pH channels; both in one window is a fault that must not read as passing | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 10 | **D-083**, the body | S-16 is direction-aware. Constraint 3. Four outcomes, not three. A magnitude-only pH check is a duplicate of S-15 wearing S-16's name | PAIR-IS-pH. The whole argument is that the two pH channels move the observable in OPPOSITE directions, which is role, not number | **SURVIVES UNCHANGED** |
| 11 | **D-083**, the closing convergence note | "CH5-versus-CH6 is the ONE confusion on this build where direction is a discriminator at all" | **IDENTITY-OF-CH6**. The claim underneath is about roles; only the naming is about tokens | **MUST BE REWRITTEN** |
| 12 | **D-077**, the decision | The five products are deliberately unassigned until commissioning. C-09 binds a token to a product | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 13 | **D-077**, its recorded summary of what the software knows | "The two 1000 mL channels are the pH adjusters ... CH6 is the other pH channel by elimination" | **IDENTITY-OF-CH6** | **MUST BE REWRITTEN** |
| 14 | **D-078** | The jug sizes are not uniform and that is a constraint. Names CH5 and CH6 as the 1000 mL pair | None of the three. It is about seeds, and D-086 and D-087 already qualified it | **WAS NEVER ABOUT CH6** |
| 15 | **D-085**, the substance | No extra wall length for the pH gap. The signed check made a swap a bounded one-dose error plus a loud stop, so the physical remedy is not worth wall length. Reopens if the signed check is ever removed | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 16 | **D-085**, its subject line | "the CH5 and CH6 gap" | **PAIR-IS-ADJACENT** | **MUST BE REWRITTEN** |
| 17 | **D-086** | The jug figures are defaults, not containers. Three conclusions rested on them | None of the three. It is the retraction, upstream of the trace | **WAS NEVER ABOUT CH6** |
| 18 | **D-088 and T-022** | F-064 and F-071 separated, because D-085 spends the opening | None of the three | **WAS NEVER ABOUT CH6** |
| 19 | **D-099** and its colour table | The colour map is accepted. CH5 blue, CH6 yellow, bound one to one and permanently | **PAIR-IS-ADJACENT**, plus IDENTITY-OF-CH6 for why the strongest separation sits at 5 and 6 | **MUST BE REWRITTEN.** The binding is frozen and D-105 did not reopen it; what must be rewritten is its stated reason. See section 5 |
| 20 | **D-106** | The C-09 script takes the duty-class question and the role question | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 21 | **G-32 as amended by D-105** | An expected sign comes from a measurement, never from a label, and the same rule now binds on role | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 22 | **G-34** | Where a rule can be written against a role rather than a dimension, it should be | None of the three | **WAS NEVER ABOUT CH6.** D-105 vindicates it |
| 23 | **G-17 and G-18** | Jugs dedicated per channel for life; the tube stays with the channel | None of the three | **WAS NEVER ABOUT CH6**, and they are why renumbering was never the fix |
| 24 | **`channel-token.md`, "One binding rule that comes from S-16"** | "pH up and pH down shall not receive adjacent tokens and shall not receive neighbouring colours." Declared now, applied once the products are assigned | **PAIR-IS-ADJACENT** | **MUST BE REWRITTEN.** It becomes a constraint on the ASSIGNMENT, not on the numbering. `subsystems/control-software.md` 311 to 315 already says this and names it CONTROL-SOFTWARE's to do |
| 25 | **`channel-token.md`, the Position axis** | CH1 to CH8 ascend in one consistent direction from Z5, never restart, never reverse | None of the three | **WAS NEVER ABOUT CH6** |
| 26 | **`channel-token.md`, forbidden item 2** | No renumbering, for any reason | None of the three | **WAS NEVER ABOUT CH6.** It is what made the rule unsatisfiable, not a consequence of the pair |
| 27 | **`channel-token.md`, forbidden item 4** | No arithmetic on tokens, no "the other pH channel" computed from a neighbour. Sets written out explicitly | PAIR-IS-pH | **SURVIVES UNCHANGED**, and gains force under D-105 |
| 28 | **`channel-token.md`, the Open table, owner row** | Which product sits on which token BLOCKS the jug labels and the S-16 non-adjacency rule | **PAIR-IS-ADJACENT** | **MUST BE REWRITTEN.** It now blocks on the ROLE assignment as well as the product |
| 29 | **`channel-register.md`, the Role column, CH5 and CH6 rows** | CH5 "pH DOWN"; CH6 "pH", product "pH up by elimination, NOT stated" | **IDENTITY-OF-CH6** | **MUST BE REWRITTEN.** The column is now a per-channel setting verified at C-09, not a derived fact |
| 30 | **`channel-register.md`, "What the software does know"** | Six nutrient and two pH; the two 1000 mL channels are the pH adjusters; CH6 is the other by elimination | **IDENTITY-OF-CH6** | **MUST BE REWRITTEN** |
| 31 | **`channel-register.md`, header conclusion 1** | That the two 1000 mL channels are the pH adjusters, so the size axis separates the pair for free | **IDENTITY-OF-CH6** | **DISSOLVES** |
| 32 | **`channel-register.md`, header conclusion 2** | F-066, that the smallest containers are handled most often | **IDENTITY-OF-CH6** | **DISSOLVES** |
| 33 | **`channel-register.md`, header conclusion 3** | DOSING's three depth classes for the suction pickup | None of the three. It rests on the seed, not on any role | **WAS NEVER ABOUT CH6** |
| 34 | **`channel-register.md`, "What does NOT rest on it"** | CH5 is marked pH-down through the blocked-channels path, a ROLE marking and not a default | PAIR-IS-pH | **SURVIVES UNCHANGED**, with the note that under D-105 this describes a SETTING and not a fixed property. See section 6 |
| 35 | **`colour-map-proposal.md`, constraint 1** | "CH5 and CH6 maximally separated. They are the pH pair and they are adjacent tokens, F-063" | **PAIR-IS-ADJACENT**, plus IDENTITY-OF-CH6 | **MUST BE REWRITTEN** |
| 36 | **`colour-map-proposal.md`, the CH5 and CH6 table rows** | Blue and yellow, "pH. Maximally separated from CH6 on the blue-yellow axis AND on lightness" | **IDENTITY-OF-CH6** | **MUST BE REWRITTEN** |
| 37 | **`colour-map-proposal.md`, "What is honest about this proposal"** | "The CH5-versus-CH6 binding is the strongest that exists, and it is the one that matters" | **IDENTITY-OF-CH6** | **MUST BE REWRITTEN** |
| 38 | **`colour-map-proposal.md`, "Not established"** | If the available carrier colour set is smaller than eight, the table is rebuilt and **the CH5 and CH6 binding is protected first** | **IDENTITY-OF-CH6** | **MUST BE REWRITTEN.** This one has a future action attached and is the most urgent of the four. See section 5 |
| 39 | **`colour-map-proposal.md`, constraints 2, 3 and 4, and the white/grey/black weakness note** | Colour-blind distinguishability, no two adjacent tokens both neutral, green excluded, and the honest note that white, grey and black are three points on one axis | None of the three | **WAS NEVER ABOUT CH6** |
| 40 | **`colour-map-proposal.md`, the marker-not-insulation finding and the T-011 resolution** | The channel colour is carried on the marker, not the conductor insulation | None of the three | **WAS NEVER ABOUT CH6.** It is the durable half of the proposal |
| 41 | **`software-spec.md` 3.2**, first two bullet sentences | The set of pH-moving tokens is read from the register's role column. Never computed, never hard-coded as a pair, never derived from "the other pH channel" | PAIR-IS-pH | **SURVIVES UNCHANGED.** It anticipated D-105 |
| 42 | **`software-spec.md` 3.2**, third sentence | "Today the register carries one role marking and one inference that is marked as an inference; code must treat both as data ... must not silently promote the inference to a fact" | **IDENTITY-OF-CH6** | **MUST BE REWRITTEN.** `subsystems/control-software.md` 317 to 320 calls it "moot in the right direction" |
| 43 | **`software-spec.md` 2.5.2 and 2.5.3** | The pH probe attributes the two pH channels and nothing else; it is direction-aware; the two cannot be attributed at the same time | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 44 | **`software-spec.md` 2.2.5, 5.6.6, 7.3 "Never", 9.1.5** | Never offer, suggest or enable the opposing pH channel as a correction; no opposing pH dose while a window is open; on restart refuse the opposing channel | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 45 | **`software-spec.md` 5.2.3 and 5.2.4** | At most one pH-moving channel carries a nonzero commanded volume; no window open for the opposing channel | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 46 | **`software-spec.md` 6.3** | The check compares a signed movement against a signed prediction; the reference sign is C-03's measured step and never a product name | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 47 | **`software-spec.md` 6.6** | What each check can and cannot attribute. pH says which of the two pH channels moved the tank and in which direction | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 48 | **`software-spec.md` 7.3 and 7.4** | F-PH-ATTRIBUTION as a short-circuiting precondition; F-CHECK-WRONG-DIRECTION kept separate from no-movement | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 49 | **`software-spec.md` N-5 and N-6** | The noise and drift band, and the signed pH step per dose measured for pH up and pH down separately | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 50 | **`software-spec.md` 2.6.4** | A rule keyed to what a thing IS outlives a rule keyed to how big it is | None of the three | **WAS NEVER ABOUT CH6** |
| 51 | **`commissioning.md` C-03** | pH step per single dose, pH up and pH down separately, and signed | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 52 | **`commissioning.md` C-09, question (b)** | Is this channel's role setting the role this product actually has | PAIR-IS-pH | **SURVIVES UNCHANGED.** Created by D-105 and D-106 |
| 53 | **`commissioning.md` C-02 and `subsystems/dosing-f004-wet-side.md` step 7** | Repeat for the pH channels separately, on the pH probe. pH up and pH down separately, never together | PAIR-IS-pH | **SURVIVES UNCHANGED**, with the note that "the pH channels" is now read from the role setting rather than known in advance |
| 54 | **`subsystems/dosing-f004-wet-side.md`, "one number or many", per-channel row** | The pH channels settle differently because both probe and response differ | PAIR-IS-pH | **SURVIVES UNCHANGED** |
| 55 | **DOSING's station hazard rule**, recorded at D-088 and `traps.md` 471 to 474 | No acid or base container stationed where breaking or lifting it puts it above the operator's forearms | PAIR-IS-pH. It is keyed to the product's chemistry, which is why it survived the seed retraction | **SURVIVES UNCHANGED**, with a scheduling consequence in section 6 |
| 56 | **Interface row S-16** | Frozen with three constraints. Attribution of the pH up and pH down channels | PAIR-IS-pH. The row names ROLES, not tokens, in every clause | **SURVIVES UNCHANGED** |
| 57 | **Interface row S-19** | CONTROL-SOFTWARE defines channel N; a crossed pair confirms itself; verified only by C-09 | None of the three | **WAS NEVER ABOUT CH6** |
| 58 | **T-018** | A seed value read as a measurement of the world | None of the three | **WAS NEVER ABOUT CH6** |
| 59 | **T-019** | Partial scepticism. Careful about one input and credulous about another in the same sentence | None of the three. The generalisation stands whatever F-066 was about | **WAS NEVER ABOUT CH6** |
| 60 | **T-022** | A withdrawn claim filed under a surviving claim's label | None of the three | **WAS NEVER ABOUT CH6** |
| 61 | **`traps.md`, "What survived the seed retraction"** | Anything keyed to ROLE rather than to VOLUME survived intact. CH5 is pH-down because the controller marks it so | PAIR-IS-pH | **SURVIVES UNCHANGED.** The lesson is exactly right and D-105 is its second confirmation. Only the CH5 illustration dates, and that is noted in section 6 |
| 62 | **`audit/2026-09-03-second-source-sweep.md` CONFIRMED 3, chains 15 to 21, open question 4** | "Whether CH6 is the second pH channel" as a live open question | **IDENTITY-OF-CH6** | **DISSOLVES as a live question.** The record of the run stands as a record. See section 6 on whether audit files are corrected |
| 63 | **`audit/2026-09-03-decisions-impossibility-grading.md` row 55** | D-085 graded: the gap was justified when a swap was permanently invisible | PAIR-IS-pH | **SURVIVES UNCHANGED**, historical |

### Counts

| Dependency | Count |
|---|---|
| PAIR-IS-pH | 25 |
| PAIR-IS-ADJACENT | 6 |
| IDENTITY-OF-CH6 | 14 |
| None of the three | 18 |
| **Total** | **63** |

| Verdict | Count |
|---|---|
| DISSOLVES | 7 |
| SURVIVES UNCHANGED | 25 |
| MUST BE REWRITTEN | 13 |
| WAS NEVER ABOUT CH6 | 18 |
| **Total** | **63** |

Four of the six PAIR-IS-ADJACENT items and four of the fourteen IDENTITY-OF-CH6 items
live in two files, `colour-map-proposal.md` and `channel-register.md`. The rewrite is
concentrated, not spread.

---

## 4. The four verdict groups expanded

### 4.1 DISSOLVES - 7 items

**Items 1, 4, 5, 6, 31, 32, 62.**

All seven asserted something about a fixed relationship between a token number and a
pH role, or between a vessel size and a pH role. D-105 removes the fixture. There is
no smaller version of any of them left over.

- **F-063 (item 1).** Tested in section 5. It dissolves.
- **F-066 (item 4)** and **register conclusion 2 (item 32)** are one claim in two
  places. D-086 had already qualified the vessel half. D-105 removes the remaining
  half: even a stated container size could not now imply a role, because the role is
  a setting and the container is an attribute of a station. There is nothing to
  requalify.
- **F-071 (item 5)** and **register conclusion 1 (item 31)** are the size-axis
  narrowing, withdrawn by its author on 2026-09-02. It dissolves twice over.
- **F-080's defect half (item 6).** D-105 disposes of it explicitly. Note that F-080
  as a whole does not dissolve: its marker gate is item 7 and survives.
- **The second-source sweep's open question 4 (item 62)** asked whether CH6 is the
  second pH channel. Under D-105 the question has no referent to settle. The audit
  file records a run and is not a live claim; I have not touched it.

### 4.2 SURVIVES UNCHANGED - 25 items

**Items 7, 9, 10, 12, 15, 20, 21, 27, 34, 41, 43 to 49, 51 to 56, 61, 63.**

This is the largest group and it is the reassuring one. **Every mechanism that
actually does work needs only PAIR-IS-pH.** The signed check, the four outcomes, the
one-pH-channel-per-window guard, the forbidden opposing-channel correction, C-03's
separate signed measurement, C-09's role question, the S-16 row itself: none of them
names a token anywhere in its operative text. They name ROLES.

That is not luck. **G-34 was frozen 2026-09-02 out of exactly this observation**, and
D-105 is its second confirmation on a bigger scale: a rule keyed to what a thing IS
outlived, again, a rule keyed to which number it wears.

Two survivors carry a note rather than a change:

- **Item 34.** "CH5 is marked pH-down through the blocked-channels path" is still
  true and still a role marking. But under D-105 the blocked-channels path is the
  FIXED LIST that D-105 replaces with the per-channel role setting. So this sentence
  now describes today's configuration, not a permanent property. I cannot settle
  whether the config's blocked list survives D-105 as a mechanism; see section 6.
- **Item 53.** C-02's procedure says "repeat for the pH channels separately". Which
  channels those are is now known only after the role assignment. C-09 is first in the
  commissioning order under D-022, so the ordering already covers it, but the
  procedure text assumes the reader knows which two before starting.

### 4.3 MUST BE REWRITTEN - 13 items

**Items 11, 13, 16, 19, 24, 28, 29, 30, 35, 36, 37, 38, 42.**

Two shapes, and they need different repairs.

**Shape one, six items: a claim about roles written in the language of tokens.**
Items 11, 13, 16, 29, 30, 42. D-083's closing sentence, D-077's recorded summary,
D-085's subject line, the register's Role column and its "what the software does
know" section, and one sentence of `software-spec.md` 3.2. The claim underneath each
is sound and role-keyed. Only the naming has to change. These are the cheap ones.

**Shape two, seven items: a constraint whose direction has reversed.** Items 19, 24,
28, 35, 36, 37, 38. The non-adjacency rule and everything the colour map built on it.
This is not a naming change and section 5 is about it.

**One rewrite already has an owner and is not orphaned:** item 24, the declaration's
S-16 binding rule. `subsystems/control-software.md` lines 311 to 315 already instructs
CONTROL-SOFTWARE to restate it as a constraint on the assignment, and observes that
this is strictly better because as written it was unsatisfiable without renumbering,
which forbidden item 2 forbids. **That is correct and it is the single most important
sentence in the D-105 aftermath.** I found it by search 4, not from the starting list.

### 4.4 WAS NEVER ABOUT CH6 - 18 items

**Items 2, 3, 8, 14, 17, 18, 22, 23, 25, 26, 33, 39, 40, 50, 57 to 60.**

Three of these were filed as downstream and are the ones worth saying out loud.

- **F-064 (item 2)** was written "answering D-078, read against F-063" and sits in
  findings.md immediately beside F-063. **It is not downstream of the pair at all.**
  It is a reading of the Position axis: sequence is constrained, spacing is not. It
  depends on no volume, no adjacency and no role. D-088 and T-022 already fought to
  keep it separate from F-071 for exactly this reason, and **D-105 is the second
  occasion on which that separation pays.** If F-063's dissolution were applied to
  everything filed near it, F-064 would go with it and D-085's free half would be
  lost a second time.
- **The colour map's constraints 2, 3 and 4 (item 39)** and the marker-not-insulation
  finding (item 40) are the durable content of `colour-map-proposal.md`. Colour-blind
  distinguishability, no two adjacent tokens both neutral, green excluded, and colour
  on the marker rather than the insulation are all true of an eight-way channel
  identity axis regardless of which channels carry pH. **When the file is rewritten,
  this is what stays.**
- **T-018, T-019 and T-022 (items 58 to 60)** are general lessons. Each was learned
  on this material and none depends on it. T-019 in particular is worth re-reading
  in this context: partial scepticism is what let the pairing through, and the test
  it prescribes is the one that would have caught it.

---

## 5. The owner's expectation, tested: does F-063 dissolve rather than shrink

**Yes. Tested, not assumed.**

F-063 is four claims in one row. Taken one at a time:

| The claim | What happens under D-105 |
|---|---|
| a. `channel-token.md` declares that pH up and pH down shall not receive adjacent tokens or neighbouring colours | **Not F-063's.** The RULE is the declaration's and traces to S-16. F-063 is the report of a violation, not the rule |
| b. The two pH channels are CH5 and CH6, and they are adjacent | **Dissolves.** Any two channels could be the pair. There is no fixed pair to be adjacent |
| c. Both are 1000 mL while the other six are not, so the physical differentiator is weakest where confusion is most dangerous | **Already withdrawn** as F-071 on 2026-09-02, on D-086 and T-018 |
| d. It is not fixable by renumbering: forbidden item 2 forbids it, and G-17 and G-18 fix jugs and tubes to channels for life. What remains is the colour axis and physical station separation | **The premise dissolves.** The reason renumbering was the only fix is that the pair was fixed to numbers. It is not any more |

**Nothing shrinks.** There is no residual "F-063 but smaller". The pair-versus-pair
confusion that D-083 called the one confusion where direction is a discriminator
still exists as a hazard, but it is now a hazard of the ASSIGNMENT, and the tree
already carries the mechanism for it: C-09's role question, added by D-106 the same
day. That is not F-063 in reduced form; it is a different item with its own ID.

### What survives F-063's dissolution, and whether it should

**Three survive legitimately.**

1. **The declaration's S-16 binding rule (item 24).** It survives because it is not
   F-063's and never was. It traces to S-16 through `channel-token.md`, and the
   second-source sweep graded that trace CLEAN. It must be restated on assignment,
   which is better than it was, because on numbering it was unsatisfiable.
2. **D-085's substance (item 15).** Its reason is the signed check bounding the
   damage, which is PAIR-IS-pH. It never needed the pair to be CH5 and CH6, only for
   there to be a pair. Its reopener clause - if the signed check is ever removed,
   this reopens - survives intact and is now more important, because the assignment
   is a new way for the pair to end up adjacent.
3. **Claim d's observation** that G-17 and G-18 fix jugs and tubes to channels for
   life. That is still true and it is now the reason **the assignment is the only
   free axis there is.** Nothing else about the pair can be moved after C-09.

**And one survives that should not, in the state it is in.**

**D-099's frozen colour binding (item 19), and the four `colour-map-proposal.md`
items that stand behind it (items 35 to 38).**

The chain is this. `channel-token.md` said the non-adjacency rule is "declared now,
**applied once the products are assigned**". D-099 applied it before assignment,
against an inferred assignment - which is precisely what the second-source sweep
recorded on 2026-09-03 and what F-080 gated the markers on. D-105 has now removed the
inference's subject entirely, and **D-099 was explicitly not reopened.** So:

- **Colour is bound to TOKEN, frozen, permanent, one to one.**
- **Role is bound to CHANNEL at assignment, free.**
- The rule says the two pH channels shall not receive neighbouring colours.

**The constraint therefore now runs backwards.** It was: given the pH pair, choose
colours far apart. It is now: given a frozen colour map, the pH roles may only be
assigned to a token pair whose colours are not neighbouring and whose numbers are not
adjacent. **The colour map constrains the role assignment.** Nobody has written out
which token pairs satisfy that, and `channel-token.md` forbidden item 4 requires such
a set to be written out explicitly rather than computed from neighbours. I have not
computed it and will not: **"neighbouring colours" is not defined as a relation
anywhere I read**, and the proposal's own honest note says white, grey and black are
the three most likely to be confused while not being adjacent tokens.

**The live one is item 38.** `colour-map-proposal.md` says that if the available
carrier colour set comes back smaller than eight, the table is rebuilt and **"the CH5
and CH6 binding is protected first."** That instruction is addressed to whoever
receives the owner's carrier availability lookup, which `channel-token.md` still lists
as OPEN and owed by the owner through DOSING. **It is a future action that would spend
the strongest separation in a reduced palette on a pair that no longer means
anything.** Of the thirteen rewrites this is the only one with a pending action
attached to it.

**Two smaller ones, both of the naming shape**, that would re-assert the pairing with
no finding left underneath if left standing: D-083's closing sentence (item 11) and
the register's "what the software does know" (item 30). F-080 flagged the second. The
first was graded SPLIT by the second-source sweep. D-105 disposed of F-080 but did not
edit either sentence.

---

## 6. What I could not settle

Each of these is a question, per agents.md. None is an assertion.

1. **Does D-105 preserve "exactly two"?** D-105 says any channel may carry nutrient,
   pH-up or pH-down. Read strictly, that permits three pH-up channels, or zero. But
   **twenty-five surviving items assume a pair**: "the opposing pH channel" in
   `software-spec.md` 2.2.5, 5.6.6, 7.3 and 9.1.5; "at most one pH-moving channel" in
   5.2.3; "which of the two pH channels" in 6.6; S-16's constraint 1. If more than two
   pH roles were ever assigned, "the opposing pH channel" has no referent and the
   admission check in 5.2.3 still holds while 5.2.4 does not. **I cannot tell from
   D-105 whether the intent is exactly two, freely placed, or any number.** This is
   the one question in this report that could change a verdict: it is the difference
   between PAIR-IS-pH surviving as stated and PAIR-IS-pH itself needing a rewrite.
   It is the owner's to answer.
2. **Whether the controller's blocked-channels path survives as a mechanism.** D-105
   replaces the plan builder's FIXED LIST with the role setting. `channel-register.md`
   says CH5's role marking comes from the blocked-channels path. If those are the same
   list, then CH5's role marking - the one origin in this whole trace that everybody
   agreed was real - is itself the fixed list D-105 replaces, and it becomes a setting
   too. **That does not make the owner's elimination argument wrong.** It makes it an
   accurate description of the configuration as it stands today rather than a
   permanent fact, which is what D-105 already says when it calls the CH6 lookup
   optional rather than load-bearing. **Nothing in the tree shows the blocked list**;
   D-105 says the same. I did not have source or config access.
3. **Which token pairs may legally receive the two pH roles under D-099's frozen
   map.** Blocked on a definition of "neighbouring colours", which I did not find in
   `channel-token.md`, `colour-map-proposal.md` or D-099. Section 5.
4. **Whether the marker gate is enough.** F-080 and D-105 gate the MARKERS on C-09.
   But D-099 already froze the token-to-colour binding, and the colour axis is spent
   whether or not a marker has been made. **The gate protects the physical labels. It
   does not protect the axis.** Whether that matters is the owner's call and depends
   on question 3.
5. **Whether "whatever spacing the existing station run gives" is still a thing D-085
   can spend.** D-085 took the free spacing of the existing run for the pH pair. The
   run is physical and fixed; which stations hold the pH pair is now assignment-time.
   I could not settle whether that makes D-085's taken remedy conditional on the
   assignment, because Z5 is still undefined per F-067 and the wall layout is
   INTERCONNECT's, deliberately not invoked.
6. **DOSING's acid and base station hazard rule (item 55).** It is keyed to the
   product's chemistry so it survives, but the stations it constrains are known only
   after the assignment. Whether the station heights have to be built to satisfy it
   for ANY station, or whether the assignment can be made to fit the stations, is
   DOSING's and I did not attempt it.
7. **Whether audit files are corrected when superseded.** Item 62 and
   `audit/2026-09-03-decisions-impossibility-grading.md` row 55 record runs that are
   now partly superseded. I found no convention in `agents.md` either way and did not
   touch them.
8. **The silent dependency.** Searches 2 to 5 find items by wording and search 7 by
   citation. **An item that assumes the pair without using any of those words would
   not appear in this report.** The second-source sweep recorded the same limit as its
   own open question 5. I have narrowed it, not closed it.
9. **Seventeen files were reached only by grep, not read** (section 1). For those,
   what I have is the absence of a hit on ten search patterns, which is weaker than a
   read, and I am not calling them clear.

---

## 7. The one line, if only one is read

**Twenty-five of the sixty-three items need only that two channels move the probe in
opposite directions, and every one of them is a mechanism that does work. Thirteen
need adjacency or CH6, and seven of those thirteen are one file, `colour-map-proposal.md`,
and the decision that froze it. F-063 dissolves cleanly. What survives its
dissolution and should not is D-099's colour spend, which was made against an
inference, was frozen before C-09, and now runs backwards: the frozen colour map has
become a constraint on which channels may be given the pH roles.**
