# AUDIT run 3: document 12 against the frozen tree, and its impossibility claims

Returned 2026-09-03. Two parts, run under the owner's scope. Questions and
classifications only. AUDIT fixed nothing and edited no other file.

## What I read, in full

`agents.md`; `audit/2026-08-30-channel-token.md` (my own run 2, for shape);
`software-spec.md` all 1154 lines; `interface-table.md`; `commissioning.md`;
`channel-token.md`; `channel-register.md`; `traps.md`; `parts.md` sections on the
pump head, the 6121 pin list, the Pi's supply, what the Pi drives and the
permissive readback; `decisions.md` - the G-rule table entire, and D-001, D-007
to D-024, D-027 to D-042, D-052, D-057, D-058, D-060, D-063, D-064, D-070,
D-075 to D-086, D-091 to D-100; `findings.md` - F-001, F-003, F-004, the F-003
reframe, F-011, F-013, F-016, F-022, F-027, F-043, F-055, F-057, F-070.

## What I did NOT read, named so nothing here rests on it

**Nothing in `subsystems/`.** Not `control-software-f004.md` or
`control-software-p09.md`, which document 12 section 1.3 supersedes and section
6.4 withdraws a claim from; not `control-software.md`, which holds the S-14
search record document 12 cites at 11.12; not `dosing-f004-wet-side.md`, named as
C-02's procedure at N-4; not `water-s18-f003.md`, named at N-9; not
`display-box.md`, `pump-boxes.md`, `main-panel-poles.md` or `interconnect.md`.
Also not read: `order.md`, `colour-map-proposal.md`.

**So every statement below about a subsystem file is one I have not checked, and
I have made none.** Where document 12 restates something whose only source is a
subsystem file, I say so rather than classifying it.

## Method note, T-021

Document 12 is a SPECIFICATION, not a state machine and not a routing layer. Its
defect families are the specification's own: a restated rule that does not match
its source, a derived rule filed among frozen ones, a stale restatement of a row
that moved, and a limitation of the present written as a property of the design.
I asked those four questions of it. I did not ask it for untested joins or
half-wired mechanisms, because it holds no mechanisms.

---

# PART 1. Pairwise, document 12 against the frozen source

126 restatements identified. **111 are clean.** The table lists every pair. Rows
marked with a section number in the last column are expanded below.

Classifications used: **RESTATEMENT** faithful, one line and nothing owed;
**DRIFT** the wording moved and the meaning moved with it; **WIDENING** document
12 forbids or claims more than the source; **NARROWING** less; **CONTRADICTION**
the two cannot both be true; **OMISSION** a load-bearing half of the source is
not carried; **STALE** faithful when written, overtaken since; **MIS-TRACE** the
rule is sound and on file, but not at the number cited.

## Counts by classification

| Classification | Count |
|---|---|
| RESTATEMENT, clean | 111 |
| DRIFT | 4 |
| WIDENING | 3 |
| OMISSION | 5 |
| CONTRADICTION | 1 |
| STALE | 1 |
| MIS-TRACE | 1 |
| **Total pairs** | **126** |

## The table

| Source ID | What the source says | What document 12 says | Class | Expanded |
|---|---|---|---|---|
| G-01, G-02 | Floats are hardwired and invisible to the Pi; the Pi gets exactly ONE level signal, a fill-in-progress dry contact | 4.4: "The only level information IN EXISTENCE is the fill-in-progress contact" | DRIFT | 1.1 |
| G-04 | No flow meters on the dosing lines; nothing measures what a head delivered | 2.1.1, 4.4: nothing measures delivered volume, ever; a dose is a commanded step count and a booked volume | RESTATEMENT | |
| G-04 | The prohibition itself: "No flow meters on the dosing lines" | Not restated as a prohibition anywhere in document 12; only its consequence is | OMISSION | 1.9 |
| G-05 | Remaining volume is arithmetic against a user-entered full-jug volume, per channel | 2.1.3, identical | RESTATEMENT | |
| G-06, C-15 | One dosing pump at a time, mandatory in software, holds until a thermal measurement says otherwise | 2.1.5: exactly one head turns at a time, a thermal constraint, mandatory until C-15 | RESTATEMENT | |
| G-07, G-13 | A leak, an E-stop or a lost interlock drops everything independent of the Pi | 2.4.1: drops MOTOR power in hardware | RESTATEMENT | |
| G-09 as amended by D-031 | The permissive removes MOTOR SUPPLY (VM) from every driver at once; it does NOT remove VDD | 2.4.2, near verbatim | RESTATEMENT | |
| G-10 | Probes sit first in line in a vertical manifold section, ahead of every injection point | 2.4.7, 6.6: probes read upstream of every injection point; a reading reflects the day tank | RESTATEMENT | |
| G-15 | The owner does all part lookups; agents return a requirement and a search term | N-3, N-20 and the whole of section 10 name a source and no value | RESTATEMENT | |
| G-16, D-017 | NO AUTOMATIC RE-DOSE, a rule not a parameter, no crash exemption | 2.2.1, 2.2.2, 2.2.4, near verbatim | RESTATEMENT | |
| G-16 laundered form | "no 'resume dose' BUTTON" | 2.2.3: "no 'resume dose' ACTION, anywhere, under any name" | WIDENING | 1.2 |
| G-16a | A louder alarm invites the forbidden correction; the corrective path must be structurally incapable, not discouraged | 2.2.5, faithful | RESTATEMENT | |
| G-17, D-018 | Jugs dedicated per channel for life | 2.6.2, faithful | RESTATEMENT | |
| G-18, D-020 | Break point at the jug; the tube stays with the channel | 2.6.3, faithful | RESTATEMENT | |
| G-19 | "No progress bar on an INTERRUPTED dose, and no delivered-fraction percentage anywhere" | 2.3.2: "No progress bar on A DOSE" | WIDENING | 1.3 |
| G-20, D-034, F-016 | Any run that turns a head records whether it completed; a calibration that did not complete is DISCARDED, not scaled | 2.3.4, 7.7, faithful and extended to primes, purges, tests and C-09 traces exactly as D-034 does | RESTATEMENT | |
| G-21, D-032 | EN unwired, drivers default enabled, software has no per-driver disable permanently and never will; the drop handler abstains rather than acts | 2.4.3: same, plus "STOP TALKING TO THEM, not shut them down" | RESTATEMENT | |
| G-25, D-038 | A no-flow CONDITION may drop the pump in hardware; a circulation VERIFICATION FAILURE may not | 2.4.9, faithful | RESTATEMENT | |
| G-26, D-052 | The panel runs without the Pi; fills, transfer, circulation and chiller on float and interlock logic; the Pi adds dosing and removes driver power | 2.4.6, near verbatim | RESTATEMENT | |
| G-32, D-083 | An expected sign comes from a MEASUREMENT, never from a label; a swap present at commissioning is baked into the reference | 2.3.3, 6.3, faithful including the residual | RESTATEMENT | |
| G-33, D-086, T-018 | Seed, capacity and poured volume are three quantities and never one column | 2.1.4, 2.3.6, N-11, faithful and applied | RESTATEMENT | |
| G-34 | A rule keyed to what a thing IS outlives a rule keyed to how big it is | 2.6.4, faithful | RESTATEMENT | |
| D-001 | Scope is tap water in through V3 | 1.2, faithful | RESTATEMENT | |
| D-007, S-13 | There is no flow signal into the Pi; the flow cell is a fitting | 2.1.2, 4.4, faithful | RESTATEMENT | |
| D-009, D-024, S-15 | EC rise is the only whole-loop check; the window is anchored to the dose and extends past the last step by the settling interval | 2.5.1, 6.5, faithful including the anchor and the extension | RESTATEMENT | |
| D-011, S-16 constraint 1 | "If both fire in one BATCH the movements cancel"; a BATCH that fires both is a fault condition | 2.5.3: "If both fire in one WINDOW" | DRIFT | 1.4 |
| D-011, S-16 constraint 1 | Constraint 1 is CONTROL-SOFTWARE's to enforce | 5.2.4 defers the window-scoped half until C-02 and says the gap "is stated in section 11"; section 11 has no such row | OMISSION | 1.10 |
| D-011, S-16 constraint 2 | A delayed check; the probe reads the tank after mixing | 2.5.1, 6.1, faithful | RESTATEMENT | |
| S-16 constraint 3, D-083 | DIRECTION-AWARE, signed movement against signed prediction; magnitude-only is a duplicate of S-15 wearing S-16's name; four outcomes with WRONG DIRECTION distinct | 2.5.2, 6.2, 6.3, faithful and argued in the source's own terms | RESTATEMENT | |
| D-012 | Every implicit verification is delayed by an unmeasured interval; routed to DOSING and CONTROL-SOFTWARE | 2.5.5: "No pass-or-fail verification logic ships until C-02 exists", traced to D-012, F-004 | MIS-TRACE | 1.5 |
| D-013, S-17 | Fulvic stays unattributed; nobody solves it | 2.5.4, 6.5, 6.6, faithful including "do not warn about it as though it were a defect" | RESTATEMENT | |
| D-014 | O-19, a flow meter on every dosing line, is off the table, not to be brought back unless something changes | Not cited. Its consequence appears at 6.6 and section 12 | OMISSION | 1.9 |
| D-017 | The direction of error is chosen, not accidental | 2.2.6, verbatim in substance | RESTATEMENT | |
| D-021, S-19 | CONTROL-SOFTWARE is the definitional end; everyone else consumes and matches; no translation at any point | 2.6.1, 3.x, faithful | RESTATEMENT | |
| D-027, D-064, S-18 | The chiller is not held off; state is RECORDED against every sample; the mechanism was "the Pi commands the contactor" and G-26 removed it | 6.4 item 4, 11.5: specified and unimplementable, field left empty rather than inferred | RESTATEMENT | |
| D-028, F-10, re-measure triggers | DOSING owns the tube and tells CONTROL-SOFTWARE C-01 is void after a change; the trigger is the tube change, not a date | 2.1.9, faithful | RESTATEMENT | |
| D-029, S-08 | There is no auxiliary block on the 22.32 and none was bought; pole 2 of the contactor carries the readback; a 25 A power pole is the readback contact | 4.2: "the position of an AUXILIARY CONTACT on the permissive contactor" | DRIFT | 1.6 |
| D-030, F-011 | Asymmetric readback discipline: DROP qualified over consecutive samples, WELD latches on a single sample and is never cleared by later samples | 2.5.6, 7.1, 7.2, faithful including the chosen direction of error | RESTATEMENT | |
| D-030, F-011 guard | Software may not solve F-011 by lengthening the filter until the nuisance stops; the fix is at the contact | 2.5.7, near verbatim | RESTATEMENT | |
| D-033, T-014 | The watchdog is fed from the sequencer and state loop, never from an independent timer thread | 2.4.10, 9.3, faithful, and the block quote is the source's own reasoning | RESTATEMENT | |
| D-042, S-03, T-016 | No dose during a fill; closed means NO FILL, open means FILLING, severed reads as filling; software cannot make a severed cable safe | 2.7.1, 2.7.2, 4.2, 7.5, faithful | RESTATEMENT | |
| D-052, S-09, F-027 | The Pi drives ONE coil, the driver permissive contactor; not the fill coils, not the transfer pump (a pole), not circulation (a pole), not the chiller (a contactor) | 4.1, 4.3, faithful and complete | RESTATEMENT | |
| D-057 | An attribute is recorded ONCE, in channel-register.md; a subsystem file may reference and may not restate | 2.6.5, 3.2, faithful and OBSERVED - no attribute value appears in document 12 | RESTATEMENT | |
| D-058 | K-CIRC is deleted; circulation is a pole on K-DRY | Not cited anywhere in document 12 | OMISSION | 1.7 |
| D-060 | Flow-proving S-05 means circulation verification STAYS POSSIBLE; level-based forecloses it permanently | 11.4 carries this faithfully | RESTATEMENT | |
| D-060 | Same | 11.6 and section 12 call positive confirmation of window validity STRUCTURAL, not pending | CONTRADICTION | 1.7 |
| D-063 | The window sits INSIDE a running period and must not span a start or a stop | 6.4 item 3: "a procedural condition ... not enforceable in software" | See 1.7 | 1.7 |
| D-064, S-18 | Nothing on file says what energises the chiller contactor coil; routed as an open question | 4.3, 11.5, faithful, and the absence claim is attributed to D-064 rather than asserted | RESTATEMENT | |
| D-070, D-093, P-09, C-18 | The datasheet neither allows, forbids, sequences nor characterises the state; it closes by measurement; running C-18 IS the decision | 1.3, 7.9.2, 11.10, 11.11, faithful | RESTATEMENT | |
| D-075, D-080 | MS1 and MS2 set by pins, never over UART; a UART-set factor reverts on a rail dip mid-batch while every instrument reads healthy | 2.4.8, faithful | RESTATEMENT | |
| D-077 | The five products are deliberately unassigned until commissioning; C-09 binds a token to a product with jugs present | 1.2, 11.15, faithful | RESTATEMENT | |
| D-086, register | The Jug column is a SEED, not a container, not what was poured | 2.1.4, N-11: "not the register's seed column and not a container capacity" | RESTATEMENT | 1.11 |
| D-091, F-057 | Nothing commands intermittent circulation; a CLOSED question with an OPEN consequence | 4.3, 6.4, faithful and the distinction is preserved | RESTATEMENT | |
| D-094 | Document 12 is the first real output | Header, faithful | RESTATEMENT | |
| D-099 | The colour map is ACCEPTED; eight token colours bound, on the marker | N-20: "Not bound" | STALE | 1.8 |
| S-03 | Circuit closed; the Pi-side input remains part of S-12 | 4.2 status column, faithful | RESTATEMENT | |
| S-05 | OPEN and deliberately held; a FLOW-proving element can subsume circulation verification, a LEVEL element can NEVER | 11.4 carries the fork; 6.4 items 2 and 3 write as though the level fork were decided | See 1.7 | 1.7 |
| S-07 | OPEN. F-019: a shorted output device may defeat G-07 depending on where the coil positive is taken from. Also F-021: whether the logic board can drive a 22.32 coil at all | 4.1, 7.1.7 carry the F-019 half exactly; the F-021 half is not carried | OMISSION | 1.12 |
| S-08 | The sense is INVERTED, contact closed means the Pi input goes LOW; G-22 chosen property | 4.2 states the readback's meaning without stating a level, correctly, since the Pi side is S-12 and OPEN | RESTATEMENT | |
| S-09 | ONE logic board output to the permissive coil and nothing else | 4.1, faithful, and BCM 18 is correctly NOT restated (S-12 is OPEN) | RESTATEMENT | |
| S-10 | A severed DIR runs a head backwards on an enabled driver while the books decrement forward; nothing measures direction or delivery | 4.1, 4.4, faithful | RESTATEMENT | |
| S-11 | EZO circuits, OPEN | 4.2, faithful | RESTATEMENT | |
| S-12 | OPEN; must be frozen in writing before either side builds | 1.2, 4.2, 11.1, N-18; document 12 states no pin and no address anywhere | RESTATEMENT | |
| S-14 | OPEN and UNVERIFIED; a search found no source in reach; not present, not absent | 11.12, faithful, and it says in terms "That is not a claim the project has no code" | RESTATEMENT | |
| S-15 | Frozen; nothing may treat it as per-channel or as valid at rest | 2.5.1, 6.6, faithful | RESTATEMENT | |
| S-17 | Closed as unattributed | 6.6, faithful | RESTATEMENT | |
| S-18 | REOPENED; three ways out, one of which is that the Pi READS a contact, "which G-26 permits since it restricts what the Pi drives and not what it reads" | 11.5 gives the blocker; the reading exit is not carried into 6.4 item 4 | See 2.x | 1.7 |
| S-19 | One token, eleven hops, no translation; verified only by C-09 | 2.6.1, 3.x, faithful | RESTATEMENT | |
| S-20 | OPEN AND NEW; a second pole of K-DRY reports to the Pi "so the VERIFICATION judgement is made in software under G-16" | 4.2, 6.4 Claim B: "a read of a PERMISSION, not of a turning pump ... can void a window and can never validate one" | NARROWING | 1.7 |
| P-07 | Pi fused and not relay switched, alive through a drop, nothing can power cycle it, watchdog is the only recovery path | 2.4.4, 2.4.5, faithful | RESTATEMENT | |
| P-09 | Closed by D-093; what a driver does with STEP asserted and VM absent remains for C-18 | 1.3, 11.11, faithful | RESTATEMENT | |
| C-01 | Delivered volume per rev against REAL BACK PRESSURE; the manufacturer figure is at none | 2.1.6, N-1, faithful | RESTATEMENT | |
| C-02 | Two numbers, t_first and t_settle; measured not derived | N-4, faithful | RESTATEMENT | |
| C-03 | Signed, the measured step IS the reference sign, never a product name | 6.3, N-6, faithful | RESTATEMENT | |
| C-04 | EC step per dose per EC-moving channel | N-7, faithful | RESTATEMENT | |
| C-07 | Feeds C-02 as a FLOOR only; one turnover is not mixing to homogeneity | N-8, faithful including "never a substitute" | RESTATEMENT | |
| C-08 | Noise and drift band on this build, in situ, over a window at least as long as the settling interval; first in the order | N-5, 6.3, faithful, including the drift half being load-bearing because the check is signed | RESTATEMENT | |
| C-09 | FIRST. The only check that catches a build-time labelling error | 1.2, 11.15, 12, faithful | RESTATEMENT | |
| C-10, C-11, C-14, C-17, C-18, C-20 | Each as written in commissioning.md | N-9, N-10, N-19, N-2, 11.10, N-16, each faithful and each naming the row rather than a value | RESTATEMENT | |
| Commissioning re-measure triggers | A driver replaced voids C-01 for that channel; CONTROL-SOFTWARE will not carry the figure across a driver change | 2.1.8, faithful, near verbatim | RESTATEMENT | |
| Commissioning ordering note | C-08, then C-02, then C-03 and C-04 | N-5, N-6, N-7, faithful | RESTATEMENT | |
| channel-token, what a channel is | Identity not component; eight given dosing paths; every physical item is an attribute | 3.1, near verbatim | RESTATEMENT | |
| channel-token, canonical form | CH1 to CH8, one written form, not ch3 not CH 3 not CH03 not #3 not 3 alone | 3.1, near verbatim | RESTATEMENT | |
| channel-token, attribute list | Box, pin, core, product, steps per ml, full-jug volume. Colour is a SEPARATE axis and is "permanent" | 3.2 adds "its role, its colour" to the list of attributes "replaceable without the channel changing" | WIDENING, and CONTRADICTION on colour | 1.13 |
| channel-token, forbidden list, 12 items | Includes #9 "Closing a gap. If a channel is retired the remaining tokens do not shift down" | 3.3 carries 8 of the 12, declared as a subset; #9 is not among them | OMISSION | 1.14 |
| channel-token, OUT OF SERVICE | The sequencer skips it; not a hardware disable; a batch that requires it STOPS | 3.4, near verbatim and correct | RESTATEMENT | |
| channel-token, change procedure | The change is made in ONE place first, every carrier agrees in the same session, and C-09 is re-run FOR ALL EIGHT | 3.4 states how a channel ENTERS out of service and never how it leaves | OMISSION | 1.15 |
| channel-token, two rules the UI owes the wall | Token on every per-channel element; character-identical to the wall | 3.5, near verbatim | RESTATEMENT | |
| channel-token, S-16 non-adjacency | pH up and pH down shall not receive adjacent tokens or neighbouring colours | Not restated in document 12 | See 1.13 | 1.13 |
| channel-register | The ONE record; role column carries one marking and one INFERENCE marked as such | 3.2: "one role marking and one inference that is marked as an inference; code must treat both as data and must not silently promote the inference" | RESTATEMENT | |
| parts.md | Do not let software report commanded state as measured state anywhere | 2.3.1, verbatim in substance | RESTATEMENT | |
| parts.md | The 1.0 ml figure is at NO back pressure; the real figure is lower and nothing measures it | 2.1.6, N-1, faithful, and no figure is repeated | RESTATEMENT | |
| parts.md | Steps per ml is motor steps per rev times microstep factor divided by ml per rev; nothing states MS1/MS2 | 2.1.7, N-2, N-3, faithful; the absence claim is grounded in C-17's recorded search | RESTATEMENT | |
| T-012 | A quantity asserted rather than derived is correct until the data moves | 2.1.7, faithful use | RESTATEMENT | |
| T-014 | A check whose condition is a literal True | 2.3.5, 2.4.10, 9.3, faithful use in both places | RESTATEMENT | |
| T-016 | Reach for the other contact, not more logic | 2.7.2, 7.5, faithful | RESTATEMENT | |
| T-018 | A seed value read as a measurement of the world | 2.1.4, 2.3.6, faithful, and 2.3.6 generalises it exactly as T-018 asks | RESTATEMENT | |
| T-019 | Partial scepticism: when you decline to estimate a term, ask what the OTHER terms rest on | 6.4 closing paragraph applies it to document 12's own refusal on C-02 | RESTATEMENT | |
| T-022 | A withdrawn claim filed under a surviving claim's label; split before qualifying | 6.4 Claim A / Claim B split, done explicitly and cited | RESTATEMENT | |
| F-001 | Three limits: only during a dose, not per-channel, nothing about pH or fulvic | 2.5.1, 6.6, faithful, and 6.6 reproduces the stalled-head case exactly | RESTATEMENT | |
| F-003, the reframe | "No sense element can verify a stopped pump" - AT REST. The first half is a SCHEDULING question, not a sensing question | 6.4 item 2 cites it for "it cannot confirm the loop is moving", a claim about a window that is by design inside a RUNNING period | DRIFT | 1.7 |
| F-004 | A check read too early reports a healthy dose as a failure | 2.5.5, 6.4 item 5, faithful | RESTATEMENT | |
| F-011 | Intermittently open on S-08 reports a welded contactor that is fine, or misses one that is not | 2.5.6, 2.5.7, 7.1 never-13, N-14, faithful | RESTATEMENT | |
| F-016 | A C-01 calibration run cut short and recorded as complete corrupts the figure every dose divides by | 2.3.4, 7.7, near verbatim | RESTATEMENT | |
| F-027 | The Pi drives one coil; S-09 was a description error | 4.3, faithful, and 4.3 says the original project description "said otherwise and was wrong" | RESTATEMENT | |
| F-043 | S-18 closed against a capability that no longer exists | 4.4, 11.5, faithful | RESTATEMENT | |
| F-055 | S-08 is a SENSE pole in a POWER relay, which G-30 forbids, and S-08 HAS NOWHERE TO MOVE | Absent from document 12 | OMISSION | 1.16 |
| F-057 | Answered: nothing commands it; the F-003 exercise run cannot happen as designed | 4.3, faithful | RESTATEMENT | |
| F-070 | The f004 window-validity precondition has no source under G-26 and D-052 | 1.3, 6.4, 12, faithful, and document 12 withdraws its own prior claim rather than reconciling it | RESTATEMENT | |

---

## Expanded entries

### 1.1 DRIFT. G-01 and G-02 against 4.4, "the only level information in existence"

**Source.** G-01: "Float switches are hardwired to relays and INVISIBLE TO THE
PI." G-02: "THE PI GETS exactly one level signal: a dry contact saying a day tank
fill is in progress. Deliberate. It is the only level information SOFTWARE has."

**Document 12, 4.4.** "Tank level. THE ONLY LEVEL INFORMATION IN EXISTENCE is the
fill-in-progress contact (G-01, G-02)."

The source scopes the claim to the Pi. Document 12 drops the scope. Read
literally the sentence is false: level information exists in the tanks, on the
floats, and in the seal-in chains, and G-01 says so in the same breath. C-11 is
a scheduled measurement of the day tank's working volume and fill band, and N-10
consumes it - so document 12 itself consumes level information that its own
sentence says does not exist.

**The question.** Is this only a sentence, or does the code shape follow it?
4.4's next clause - "software cannot know the level and must never adapt to it" -
is correct and is what G-02 supports. **The risk is a later reader taking "in
existence" at face value and concluding that a second level contact could never
be added, which G-02 does not say and which is a decision nobody has made.** One
word, "in existence" to "at the Pi", and the drift is gone.

### 1.2 WIDENING. G-16's laundered form, "button" to "action, anywhere, under any name"

**Source, G-16.** "AND THE LAUNDERED VERSION IS ALSO FORBIDDEN: no 'resume dose'
BUTTON. A remainder computed from an unknown fraction is an automatic re-dose
with a human as its trigger."

**Document 12, 2.2.3.** "There is no 'resume dose' ACTION, ANYWHERE, UNDER ANY
NAME."

Document 12 forbids more than G-16's text. **The widening is supported by G-16's
own stated reason**, which is about the remainder and not about the widget: a
menu item, an API call, a config flag or a script would each be an automatic
re-dose with a human as its trigger just as a button would.

**I do not bring this forward as a defect. I bring it forward as a question for
BOSS about which document should be amended.** Today the frozen rule is narrower
than the specification built on it. **The direction of the divergence is the
dangerous one: an implementer under pressure can cite G-16's literal text to
argue that a non-button resume is not what was frozen.** If document 12 is right,
G-16 should say "action" too.

### 1.3 WIDENING. G-19, "an interrupted dose" to "a dose"

**Source, G-19.** "No progress bar on an INTERRUPTED dose, and no
delivered-fraction percentage anywhere. A percentage computed from step index
renders a commanded count as a delivered fraction."

**Document 12, 2.3.2.** "No progress bar on A DOSE, and no delivered-fraction
percentage anywhere."

The same shape as 1.2 and the same direction. G-19's reason - a percentage from a
step index is a commanded count wearing a delivered fraction's clothes - applies
to a dose in flight exactly as it applies to an interrupted one. **G-04 makes
every step index a commanded count at all times, not only after an interruption.**

Note that document 12 is not consistent with itself about which scope it means:
7.10 applies the prohibition to a FAULT PRESENTATION, which is G-19's scope, while
2.3.2 applies it to any screen. **The residual is an operator interface showing a
live progress bar during a normal dose, defended by G-19's literal wording, and
the UI is HELD by the owner - so the question will be asked when the UI arrives
and G-19 is what will be read.**

### 1.4 DRIFT. D-011 and S-16 constraint 1, "batch" to "window"

**Source.** D-011: "If both fire in ONE BATCH the movements cancel and pH shows
the net ... A BATCH that fires both is a fault condition and the check must not
read as passing." S-16 constraint 1 uses the same word.

**Document 12, 2.5.3.** "If both fire in ONE WINDOW the movements cancel."

**These are not the same set.** A window opens at the first commanded step and
closes at a recorded outcome, extended past the last step by the settling
interval (6.5). A batch may be longer than one window. **So a batch that fires
both pH channels, separated by more than the settling interval, violates D-011
and satisfies document 12's 2.5.3.**

**Why I am not calling this a contradiction:** 5.2.3 keeps the batch-scoped form
intact as a rejection - "a plan carrying nonzero volumes on both is rejected" -
and 5.2.4 adds the window-scoped form on top. So the enforceable rule document 12
specifies is at least as strict as D-011. **The drift is confined to 2.5.3, which
is in section 2, the section whose stated purpose is that "a reader must not have
to open decisions.md to know what they may not do."** A reader who reads only
section 2 gets the narrower rule.

**The question.** Should 2.5.3 read "in one batch, and separately in one window"?
And is the batch really the right unit in D-011, or was "batch" the word available
before windows had been specified?

### 1.5 MIS-TRACE. 2.5.5's shipping rule is not in D-012

**Document 12, 2.5.5.** "Every implicit verification is delayed by an interval
nobody has measured. A check read too early reports a healthy dose as a failure.
**No pass-or-fail verification logic ships until C-02 exists.**" Trace: D-012,
F-004.

**What D-012 says.** That every implicit verification is delayed by an unmeasured
interval; that the constraint applies to EC as well as pH; and that the question
is "logged as findings.md F-004 and ROUTED to DOSING and CONTROL-SOFTWARE between
them." **D-012 routes a question. It states no shipping rule.** F-004 likewise
routes rather than rules.

**Where the rule actually lives.** D-083, in its recital of CONTROL-SOFTWARE's
answer: "D-012 means no verification logic ships until C-02 exists." That is
CONTROL-SOFTWARE's own derivation, recorded and accepted by BOSS inside a frozen
decision. **So the rule is on file and I am not challenging it. I am reporting
that section 2 promises the trace can be checked against the source, and this one
cannot be checked against the number given.**

The first paragraph of section 2 is the reason this matters: "The trace number is
alongside so it can be checked against the source, not so it has to be." A reader
who does check finds a routed question where a frozen rule was promised, and the
next inference is that the rule was invented. It was not. **The fix is one
character: D-083.**

### 1.6 DRIFT. "Auxiliary contact" for what D-029 established is pole 2

**Source.** D-029 exists to resolve F-013, and its whole content is that the word
is wrong: "There is no auxiliary block on the 22.32 and none was ever bought.
Pole 1 carries the 24 V rail out to both pump boxes ... and pole 2 was unwired
and free and NOW CARRIES THE READBACK. **So a 25 A POWER POLE IS THE READBACK
CONTACT.**" S-08's End A names it exactly: "pole 2 of the 22.32, terminals 3 and
4."

**Document 12, 4.2.** "Permissive readback. The position of an AUXILIARY CONTACT
on the permissive contactor."

`parts.md` also says "a real auxiliary contact", so document 12 inherited the
loose word from a source it was entitled to read. **But F-013 was raised
independently by two agents precisely on this word, and D-029 was written to
settle it.** Restoring the loose word in the builder-facing document puts back the
thing two agents spent a pass removing.

**Why it is more than vocabulary.** Document 12's own sentence in the same cell -
"it is not a measurement of the load conductor: a welded main pole or an open
load conductor reads whatever the aux reads" - is an argument about INDEPENDENCE
between the sensing contact and the load contact. **The two are poles of one
contactor on one armature, not an auxiliary block, and F-055 asks whether they
even share a contact volume.** The correct statement is stronger than the one
document 12 makes, and it is stronger for a reason document 12 does not give.

### 1.7 CONTRADICTION, and it is the worst finding in Part 1. Window validity is called STRUCTURAL where D-060 says it survives one fork of an OPEN row

This is one finding with four document-12 locations and five sources. I have set
it out in full because it is also the headline of Part 2.

**What document 12 claims.**

- 6.4, "What the application CANNOT do, stated plainly so nobody writes it", item
  2: "**It cannot confirm the loop is moving.** There is no flow signal and no
  observable that separates a running pump from a stopped one at rest (F-001
  limit 1, F-003)."
- 6.4 item 3: "**It cannot know a window sat inside a running period.** D-063
  requires a window not to span a start or a stop ... That is a procedural
  condition on how a batch is run and on the C-02 measurement, and **it is not
  enforceable in software.**"
- 11.6: "Any positive confirmation that a settle window was valid. **Structural,
  not pending.** ... This is not waiting on a decision; it is a property of the
  design."
- Section 12: listed first among the three things "**structurally impossible
  rather than pending**, and it should not be read as a gap waiting to close."

**What the sources say.**

1. **S-05, interface-table.md, status OPEN and deliberately held.** "A
   FLOW-proving element senses the RESULT and can also catch a dry tank, so it
   can subsume dry-run protection, while a LEVEL element senses the supply and
   can NEVER subsume circulation verification ... **Choosing a level-based answer
   here FORECLOSES the shared solution.**"
2. **D-060, frozen.** "Flow-proving means a timing element is definite and
   **CIRCULATION VERIFICATION STAYS POSSIBLE**; level-based means no timing
   element and circulation verification is foreclosed permanently."
3. **S-20, interface-table.md, OPEN AND NEW, created by D-038.** "A second pole
   of the same relay reports to the Pi **so the VERIFICATION judgement is made in
   software under G-16.**" S-20 exists for exactly the purpose document 12 says
   is structurally unavailable.
4. **D-058, frozen.** "K-CIRC is deleted, **circulation being a pole on K-DRY.**"
5. **F-003's reframe, findings.md.** "No sense element can verify a stopped pump.
   **AT REST** a flow switch reads no-flow ... So the first half of F-003 is not a
   sensing question, it is a SCHEDULING question."

**The three separate errors.**

**(a) The cited support is about the pump AT REST; the claim is about a window,
which is by design inside a RUNNING period.** F-001 limit 1 and F-003 both
concern the interval between batches, when the loop is still. D-063 establishes
that the pump runs "during a batch, during dosing, and through a settle window".
**So the one case the citations cover is the one case a settle window is never
in.** The sentence in 6.4 item 2 even ends with the source's own qualifier - "from
a stopped one AT REST" - and then the conclusion is drawn without it.

**(b) Circulation is a POLE on K-DRY, so a read of K-DRY is a read of whether the
circulation pump was energised.** D-058 deleted K-CIRC for this reason. If S-20
freezes, the Pi reads the second pole of that relay. A window during which the
relay stayed made is a window during which the pump was energised throughout;
one during which it did not is a window that spanned a start or a stop. **That is
D-063's condition exactly, and reading it is enforcement.** Document 12's Claim B
concedes the mechanism - "a window during which that relay was not made may be
voided" - which IS enforcement of D-063. **6.4 item 3 says flatly "not enforceable
in software" and does not carry the concession its own next page makes.**

**(c) Document 12 states the LEVEL fork's outcome as though S-05 were decided.**
Claim B says a frozen S-20 gives "a read of a PERMISSION, not of a turning pump,
so even then it can void a window and can never validate one." That is true of a
LEVEL element, which reads the supply. It is not true of a FLOW-proving element,
which senses the result: under flow-proving, K-DRY made means flow was proved,
and D-060 says in those words that circulation verification stays possible.
**S-05 is OPEN. Document 12 has resolved it, in the direction of the worse
outcome, and then filed the consequence under "structural".**

**Document 12 half-knows this.** 11.4 carries D-060 correctly: "S-20 is OPEN and
blocked on S-05. And a LEVEL-BASED S-05 forecloses circulation verification
permanently. Claim B in 6.4 stands or falls here." **11.4 says pending. 11.6 says
structural. They are two rows of the same section and they are about the same
capability.**

**Why this is expensive rather than untidy.** Three things:

- **D-095 has already banked it.** "The distinction that matters most - what is
  STRUCTURALLY IMPOSSIBLE rather than pending, so nobody reads it later as a gap
  waiting to close. Three things are in that last category," the first being
  positive confirmation that a settle window was valid.
- **It has already propagated.** Commissioning C-23 now reads: "**Software cannot
  catch this: under G-26 and D-052 the Pi neither commands nor observes the
  circulation pump** ... software-spec.md section 6.4 states this as a procedural
  condition on the operator and NOT ENFORCEABLE IN SOFTWARE." C-23 cites document
  12 as its authority. **The claim is now in two files, one citing the other, and
  neither cites D-060 or S-20.**
- **S-05 is a fork with a price.** D-060 makes flow-proving cost a timing element.
  A reader deciding S-05 who has been told that circulation verification is
  structurally impossible has no reason to pay for the flow-proving element -
  which forecloses it permanently, and then the claim becomes true retroactively.
  **A "currently" dressed as a "structurally" here does not merely close a door.
  It removes the reason to keep paying for the door.**

**And note what G-26 does and does not say.** S-18's row states the boundary in
terms: G-26 "restricts what the Pi DRIVES and NOT what it READS." Document 12
respects that at 4.3 and blurs it at 6.4, where "the Pi neither commands nor
observes" runs the two together. **The command half is structural. The observe
half is not, and G-26 is not the rule that makes it so.**

**Questions for BOSS.** Does 11.6 survive contact with D-060? Should 6.4 item 3
read "not enforceable in software TODAY, and enforceable through S-20 if S-05
resolves flow-proving"? Should C-23 be corrected, or does it stand as a procedural
instruction regardless? And is the S-05 decision now carrying a cost it was not
told about?

### 1.8 STALE. N-20 says the colours are not bound; D-099 bound them

**Source.** D-099, 2026-09-03: "**THE COLOUR MAP IS ACCEPTED.** colour-map-proposal.md,
as proposed", with a token-to-colour table for all eight, and: "The colour lives
on the MARKER, not on the insulation ... **It is an identity axis added to the
token, not a second token.**"

**Document 12, N-20.** "The eight token colours. Owner, via DOSING, a material
availability question (G-15). One colour per token, bound once, in one table.
Status: **Not bound.** Blocks nothing but permanent carriers."

Document 12 was written 2026-09-02 and was correct on the day. **It is wrong
today, and so is `channel-token.md`, whose axes table still reads "Colour |
DECLARED, NOT YET BOUND".** I report both because the owner's scope named
channel-token.md as a frozen source and it has the same staleness.

This is small in itself. **It is worth a line because N-20 is the only row in
section 10 whose status has changed since the document was written, and section
10 is the document's own answer to "no invented figures" - so a reader checking
section 10's discipline will check N-20 and find the tree ahead of it.** No
number needs to enter document 12: D-099 puts the colours in decisions.md and the
register is the one record.

### 1.9 OMISSION, minor. The G-04 and D-014 prohibitions are not carried, only their consequence

**Sources.** G-04: "**No flow meters on the dosing lines.** Nothing measures what
a peristaltic pump actually delivered." D-014: "O-19, a flow meter on every dosing
line, is off the table. **Not to be brought back unless something changes.** G-04
already forbade it; this is the owner declining it knowingly."

**Document 12** carries the consequence everywhere - 2.1.1, 4.4, 5.4, 6.6, 12 -
and never the prohibition. Neither G-04's ban nor D-014 appears in the document;
I extracted every ID cited in the file and D-014 is not among them.

**Why I raise it at all.** Section 12 calls "attribution for six of the eight
channels" STRUCTURALLY impossible. **That claim has two legs: a physics leg, that
eight heads inject into one stream so one EC probe cannot attribute (6.6 gives
this one), and a RULE leg, that the instrument which would attribute is forbidden
by G-04 and declined by D-014 (document 12 gives neither).** The classification is
sound. **Its second leg is not written down, and it is the leg that could move -
D-014 says "unless something changes".**

### 1.10 OMISSION. The window-scoped pH guard is deferred to a section 11 row that does not exist

**Source.** S-16's owner column: "**constraint 1 is CONTROL-SOFTWARE's to
enforce.**"

**Document 12, 5.2.4.** "No pH attribution window is open for the opposing pH
channel (5.6, 6.5). **Until C-02 exists, the window-scoped form of this check
cannot be computed and only the batch-scoped form of rule 3 is enforceable; that
gap is stated in section 11 rather than approximated.**"

I read all sixteen rows of section 11. **There is no row for it.** 11.2 covers
"any pass-or-fail verification logic at all", which is a VERDICT; the window-scoped
pH guard is an ADMISSION precondition, and document 12 itself keeps admission and
evaluation apart throughout section 5.

Document 12's own discipline is the reason this matters: 2.3.5, "never leave an
outcome slot absent", and section 11's whole premise, that an unspecified thing
gets a named blocker. **A partial deferral of a frozen obligation with a
cross-reference to nothing is the shape 2.3.5 forbids, applied to the document
rather than to the code.**

**The question.** Is the window-scoped guard blocked on C-02 alone, or also on
durable window state, which 8.1 already requires and which exists independently of
C-02? If the latter, part of the deferral may be unnecessary.

### 1.11 Not a defect, reported because it runs the other way. Document 12 is ahead of channel-register.md on G-33

`channel-register.md` opens with D-086 correctly: "The Jug column below. **A SEED
VALUE in config.yaml. NOT a container.**" Its closing table then says: "**The Jug
column is the container's NOMINAL CAPACITY, which is now known per channel.**"

Those two sentences are in one file and cannot both be true, and G-33 exists
because they were once treated as one quantity.

**Document 12 follows the corrected sentence, not the stale one.** N-11: "Poured
full-jug volume, per channel. Owner, at fill time. **Not the register's seed
column and not a container capacity.**" 2.1.4 says the three "are never one
field".

Reported because AUDIT was asked to compare pairwise and this pair disagrees with
the register rather than with document 12. **The register is the ONE record under
D-057, so the stale sentence is in the file every subsystem is told to read.**

### 1.12 OMISSION, minor. S-07's second open half

S-07 carries two open items. Document 12 carries the first exactly - F-019, where
the coil positive is taken from, and it draws the right consequence at 4.1 and
7.1.7: "nothing may assume that dropping the command removes motor supply by
itself." **It does not carry F-021, whether the logic board can drive a 22.32 coil
directly at all, "which decides whether the panel is short one relay or three".**

I do not think this belongs in document 12 - it is a panel question, not an
application question. **I report it because 4.1 says "what the command is in
series with is S-07, which is OPEN", which characterises S-07 as one question when
the row holds two.** If F-021 resolves by inserting an interposing relay, the
command the application drops is one more element away from the coil, and 7.1.7's
caveat gets longer.

### 1.13 WIDENING, with a CONTRADICTION inside it. Role and colour added to the attribute list

**Source, channel-token.md.** The attribute list is closed and enumerated:
"**Attributes, bound to the token, never identities of their own:** which box the
head sits in, which pin drives it, which core carries it, which product it doses,
its steps per millilitre from C-01, its full-jug volume under G-05. **Any of these
may change without the token changing.**" Colour is not in that list. Colour is an
AXIS, in a separate table: "One colour per token, one to one, **PERMANENT**,
identical in the UI and on the wall."

**Document 12, 3.2.** "An attribute is bound to a token and is never an identity
of its own: which box the head sits in, which pin drives it, which core carries
it, which product it doses, its steps-per-millilitre figure from C-01, its poured
jug volume under G-05, **its role, its colour.**" And 3.1: "**every one of those
is an ATTRIBUTE and every one is replaceable without the channel changing.**"

**On colour: a contradiction.** channel-token.md says permanent. Document 12 puts
it in a list whose defining property is replaceability. **D-099 has since settled
it in channel-token.md's favour and gone further: "It is an IDENTITY AXIS added to
the token, not a second token."** An identity axis is not an attribute. The
practical residual is small today because nothing computes from colour, and D-099
says nothing may. **It is not small for the carriers: 3.2 as written licenses
re-colouring a channel as an ordinary attribute edit, and channel-token.md warns
that engraving twice is rework.**

**On role: a widening with a live consequence.** The register's Role column is
real and document 12 is right that the pH set is read from it (3.2) rather than
computed. **But calling role a replaceable attribute puts it in the same class as
a pin.** It is not in the same class:

- **G-34, frozen, says the opposite in general terms:** "a rule keyed to what a
  thing IS outlives a rule keyed to how big it is ... roles are decided earlier
  and change less." T-022's closing section records that role survived the seed
  retraction while every volume-keyed conclusion fell.
- **channel-token.md binds token assignment to role:** "pH up and pH down shall
  not receive adjacent tokens and shall not receive neighbouring colours." **A
  role edit can therefore violate a token rule.** Document 12 does not restate the
  non-adjacency rule anywhere - I checked the full ID extraction and section 3 -
  and nothing in 3.2, 3.4 or 5.2 says that a change in the role column re-triggers
  anything.
- **C-03 is per-role.** N-6 is "signed pH step per dose, pH up and pH down
  separately". A channel that acquires a pH role has no C-03 reference and no
  signed prediction, and 5.2's admission rules check C-01 and C-17 and do not
  check C-03.

**This is AUDIT run 2's C21 arriving at a new item.** C21 asked whether a jug is
an attribute in the same sense as a pin, given that G-17 dedicates it for life,
and proposed a third category: bound-for-life attributes that cannot be replaced
independently. **Role and colour are two more members of that category and
document 12 has filed both in the first one.**

**The question.** Is the attribute list in 3.2 meant to be the declaration's list
plus two, and if so, which of the ten are replaceable in the sense 3.1 states?

### 1.14 OMISSION, declared. Four of the declaration's twelve forbidden items

Document 12's 3.3 says openly what it is: "These come from the declaration's
forbidden list and are the ones that bite an implementer." Eight of twelve are
carried. **I checked the four that are not:**

- **#6, the product as identity** - covered elsewhere, at 3.2 and 2.3.3, and
  covered better.
- **#7, box-local, cable-local or connector-local numbering** - covered by 3.3.5's
  "no internal driver ID alongside the token".
- **#11, deriving a token from hardware enumeration order** - partially covered by
  3.3.2 and 3.3.4. Thin, but the declaration is the one record for consumers and
  this one bites DISPLAY-BOX, not this application.
- **#9, closing a gap: "If a channel is retired the remaining tokens do not shift
  down to make the set contiguous"** - **not covered.** 3.3.6 forbids reusing a
  retired token and requires it be marked retired and never deleted; it does not
  say the SET keeps its hole.

**Only #9 concerns me, and it concerns me because of 3.3.2.** Document 12's own
rule is that per-channel state lives "in records keyed by the token, never in a
positional list of eight values". **An implementer holding a retired token as a
record with a gap is doing the right thing. An implementer who compacts the set
after a retirement has produced a positional list of seven, and 3.3.4's list of
renumbering motives does not name this one.** channel-token.md names it as its own
numbered item precisely so it cannot be reasoned past.

### 1.15 OMISSION, and the second worst finding in Part 1. Section 3.4 says how a channel enters OUT OF SERVICE and never how it leaves

**Source, channel-token.md, change procedure, universal rules for every case.**

- "The change is made in **ONE PLACE FIRST**, the channel's record, and every
  carrier is brought into agreement **in the same working session. No overnight
  partial state.**"
- "While software and the wall may disagree, the channel is **OUT OF SERVICE: THE
  SEQUENCER SKIPS IT.**"
- "**C-09 is re-run FOR ALL EIGHT CHANNELS, never for the one that changed.** A
  crossing always involves at least two channels and a partial trace cannot see
  the half it did not trace. **A partial C-09 is not a cheaper C-09, it is a
  different and much weaker test.**"

The change table then attaches per-case obligations: a head moved between boxes,
C-09 all eight plus C-01 if tubing or orientation changed; a driver replaced,
C-09 and C-01 void for that channel; a product retired, full-jug volume re-entered
and C-03 or C-04; a channel retired, C-09 for the seven that remain.

**Document 12, 3.4, in full.** It restates the entry condition and the skip, near
verbatim and correctly, including "it is not a hardware disable and does not rely
on one" and the G-16-shaped stop. **It states no exit condition.** I read 3.4,
5.2, 8.1 and section 11 looking for one.

**What the application actually enforces on the way back in.** 5.2 admission,
rule 1: the token is "a live token in the register, not retired, not out of
service". Rule 2: "every commanding channel has a valid, non-void C-01 figure and
a recorded C-17 configuration". **That is the whole of it. Nothing checks C-09.**

**So the failure mode is this.** A driver is replaced. C-01 is voided and the
channel goes out of service - both correct and both specified. The owner
re-measures C-01 for that channel and records it. **The application now sees a
live token with a valid C-01 and a recorded C-17, and admits it.** C-09 has not
been re-run for all eight. **And C-09 is the only check in the system that catches
the failure a driver replacement can introduce**, which the tree states twice:
S-19, "if the ends disagree, a head labelled N driven by software channel N+1
doses the wrong product every batch, permanently, AND PASSES EVERY CHECK"; and
D-022, "a measurement taken against a mislabelled channel is not a wrong number,
it is a right number filed against the wrong thing, and every later check
confirms it."

**The re-measurement of C-01 is itself one of those later checks.** It is a
measurement made against the channel's identity. If the driver replacement
disturbed a landing, C-01 has been re-measured against the wrong channel and the
application will divide every dose by it.

**I am not asserting the application can enforce C-09.** C-09 is an owner
procedure performed by eye and the Pi cannot witness it. **What I am reporting is
that document 12 records the entry condition of a state and not its exit, so
nothing in the specification says what makes an out-of-service channel serviceable
again, and the admission rules will readmit it on the strength of a figure whose
validity C-09 is what establishes.**

**Questions.** Is there a durable per-token "C-09 witnessed since the last change"
flag, set by an operator action, cleared by anything that sets out-of-service, and
checked at admission? 8.1 already records "which C-01/C-17 figures are void", so
the shape exists. Or is C-09 deliberately outside the application, in which case
should 3.4 say so, and say what the operator owes before returning a channel to
service? **And which document should hold the exit condition - 3.4, or the
declaration's change procedure, which has it and which document 12 says
governs?**

### 1.16 OMISSION. F-055 is absent, and it lands on the contact document 12's readback discipline runs on

**Source, F-055, findings.md, raised by MAIN-PANEL applying G-30 to a CLOSED row.**
"Pole 1 carries the 24 V rail to both pump boxes, up to 8 A of driver load: a
tier-1 arcing power pole. Pole 2 is the S-08 readback, a sense pole by function.
**They are two poles of ONE 22.32.** If the 22.32's poles share a volume the way
the 55.34's do, **S-08 is a sense pole in a power relay, which is precisely what
G-30 forbids, and the wetting circuit does not help: 45 to 55 mA was designed
against oxidation from UNDER-loading, and no burden value addresses contamination
from the neighbouring pole.**" Status: "**S-08 HAS NOWHERE TO MOVE** ... An
intermittently open readback is F-011's worst case on the one signal built to
catch the worst case. ONE LOOKUP decides it."

**Document 12 does not mention F-055.** I extracted every G, D, F, C, S, P, T,
CBL, M and N identifier in the file; F-055 is not among them, and neither is G-30.

**Why it belongs.** Document 12 builds a great deal on this one contact: 2.5.6
and 2.5.7, the asymmetric discipline; 7.1 and 7.2, both permissive faults; 7.9's
recovery preconditions, where "readback qualified closed and stable over an
interval long enough to expose an intermittency" is precondition 1; and N-14, the
readback qualification length, whose status is "Not set" and whose note is "no
measured contact behaviour exists". **F-055 says the contact behaviour may be
worse than F-011 alone implies, for a reason no filter length addresses, and that
one lookup settles it.**

Document 12 cites F-011 in all the right places, so this is not a document that
ignored the contact. **It carries the under-loading half of the risk and not the
neighbouring-pole half.** Under agents.md rule 8 I name what I read to say it is
absent: the full identifier extraction from software-spec.md, and section 11's
sixteen rows.

**The question.** Should N-14 or section 11 carry F-055 as a second input to the
qualification length, given that F-055's status names a single lookup as
decisive?

---

# PART 2. Every impossibility claim, structural or current

The owner's test, applied to each: **structural** means no addition of hardware,
wiring or software within this project's frozen rules could ever make it possible,
because a rule or physics forbids it. **Current** means it is impossible given
what has been bought, wired or decided so far, and a change already on the table
would make it possible.

I found 24 claims. **17 are structural. 6 are current. 1 is mixed.** Three of the
six current are stated by document 12 in language that reads as structural, and
one of those three is in section 12's list of things that are "structurally
impossible rather than pending".

## The table

| # | Where | The claim, quoted | Structural or current | The one sentence that decides it |
|---|---|---|---|---|
| 2.1 | 2.2.2 | "It is frozen before any code exists precisely so it cannot be argued into existence by a plausible edge case" | **STRUCTURAL** | G-16 is "a RULE, not a parameter", frozen by the owner, and only the owner can unfreeze it |
| 2.2 | 2.4.3, 4.1, 7.1.1 | "Software has no per-driver disable, permanently, and never will"; "there is no such request"; "the application cannot disable, de-energise, halt or make safe a driver" | **STRUCTURAL** | D-032: "software has no per-driver disable, permanently, and never will ... Its drop handler abstains rather than acts, permanently" |
| 2.3 | 2.7.2 | "The safety of it is in the contact selection and software cannot improve on it" | **STRUCTURAL** | T-016: "Software cannot make a severed cable safe. Contact selection can" |
| 2.4 | 4.1 | "Dropping the command does not by itself prove VM is removed" | **STRUCTURAL** | F-019: a shorted output device is not fail-safe, and S-07 is OPEN on where the coil positive is taken from - it is a statement about evidence, and no wiring makes a command into a measurement |
| 2.5 | 4.3 | "The Pi cannot start it, cannot stop it, and cannot ask for it" - the circulation pump | **STRUCTURAL** | G-26 and D-052: the Pi drives one coil, the driver permissive, and nothing else; circulation is a pole on the dry-run interlock relay |
| 2.6 | 4.3 | "Nothing commands intermittent circulation" | **CURRENT**, and correctly labelled | D-091: "there is no command path ... until one exists or the design changes" - document 12 calls it "a closed question with an open consequence", which is right |
| 2.7 | 4.4, 2.1.1 | "Delivered volume, on any channel, ever. Nothing measures it" | **STRUCTURAL, by rule** | G-04: "No flow meters on the dosing lines", reinforced by D-014 taking O-19 off the table. Not physics; a frozen owner decision, and D-014 says "unless something changes" |
| 2.8 | 4.4 | "Direction of rotation, or that a head turned at all. Nothing measures it ... no input sees it" | **CURRENT** | The 6121's printed pin list in parts.md includes INDEX, unwired; no frozen rule forbids landing it, and document 12's own 11.16 concedes "if a per-driver indication that requires actual commutation ever lands at the Pi" |
| 2.9 | 4.4 | "Flow, anywhere. There is no flow signal" | **MIXED** | Structural for the dosing lines under G-04; **current for the circulation loop**, where S-05's flow-proving fork is open and no rule bans a flow element - the two are one sentence in document 12 |
| 2.10 | 4.4, 6.4 item 2 | "Whether the circulation pump is turning"; "it cannot confirm the loop is moving" | **CURRENT** | D-060: "flow-proving means a timing element is definite and **circulation verification stays possible**" |
| 2.11 | 4.4 | "Tank level. Software cannot know the level and must never adapt to it" | **STRUCTURAL** | G-02: "The Pi gets **exactly one** level signal", and G-01 makes the floats invisible to the Pi |
| 2.12 | 4.4, 7.1.6, 7.1.8, 7.10 | "Which element of the permissive chain opened ... It yields a mismatch, never a cause"; "Never name a cause" | **CURRENT** | S-18's row: G-26 "restricts what the Pi **drives** and not what it **reads**" - there is no rule against a leak, E-stop or interlock input, only no row proposing one |
| 2.13 | 4.4, 6.4 item 4, 11.5 | "It cannot tag a sample with chiller state"; "D-027 is specified and unimplementable" | **CURRENT** | S-18's row names three ways out, the first being "the Pi READS a contact on the chiller contactor, which G-26 permits"; 11.5 correctly calls S-18 the blocker |
| 2.14 | 4.5.1 | "There is always a set of steps commanded after VM vanished and before software learned of it ... no amount of tightening removes it" | **STRUCTURAL** | Three latencies in series cannot sum to zero. This is physics and document 12 states it as such, including that faster detection "buys no safety at all" |
| 2.15 | 5.2, 5.4 | "Nothing can say how much or undo it"; the floor is "Zero ... until a subsystem returns something that narrows it" | **STRUCTURAL** for the undo; **CURRENT** for the floor, and 11.16 says so | G-04 for the first; 11.16's "nothing on **this build** can narrow it" for the second, which is the correct framing |
| 2.16 | 6.4 item 1 | "It cannot require circulation. It cannot command the pump" | **STRUCTURAL** | G-26 and D-052, same as 2.5 |
| 2.17 | 6.4 item 3 | "It cannot know a window sat inside a running period ... **it is not enforceable in software**" | **CURRENT** | D-058: "K-CIRC is deleted, **circulation being a pole on K-DRY**", and S-20 is a second pole of K-DRY reported to the Pi. See 1.7 |
| 2.18 | 6.4 item 5 | "It cannot detect the slow failure that matters most ... **The mitigation is not a sensor**" | **CURRENT** | G-04 bans flow meters on the **dosing lines** only; nothing in decisions.md bans a circulation-loop element, and document 12's own words are "which this design does not observe **by choice**" |
| 2.19 | 6.4 Claim B | A frozen S-20 "is a read of a PERMISSION, not of a turning pump, so even then it can void a window and **can never validate one**" | **CURRENT** | S-05's row: a FLOW-proving element "senses the **result**", a LEVEL element "senses the supply and can NEVER subsume circulation verification" - document 12 asserts the level fork's outcome while S-05 is OPEN |
| 2.20 | 6.6 | EC "cannot say which head delivered" | **STRUCTURAL** | F-001 limit 2: eight heads inject into one stream and one EC reading cannot attribute the change. Physics of the manifold |
| 2.21 | 6.6 | pH can say nothing "when both were commanded in one window - the movements cancel" | **STRUCTURAL** | D-011: "the movements cancel and pH shows the net". Physics of one probe reading a net |
| 2.22 | 6.6 | Fulvic: can say "Nothing", cannot say "Everything" | **STRUCTURAL, by rule** | D-013: "One unattributed channel out of eight, recorded, is acceptable. **Nobody solves it.**" S-17 closed on that basis |
| 2.23 | 7.9 | "Deliberately not required: proof that the drivers are powered. **None exists**" | **CURRENT** | No VM sense is wired and no rule forbids one; D-097 removes DIAG as the route and names C-18 as the only settler, which is a measurement not yet run |
| 2.24 | 9.3 item 1 | The watchdog's "coverage of a runaway dose is ZERO" | **STRUCTURAL** | A reset takes time and nothing controls the outputs during it. Physics, and P-07 makes the watchdog the only recovery path from a hang |

## The three that are dressed as structural, in order of cost

**First. 2.17 and 11.6 and section 12: positive confirmation that a settle window
was valid.** Set out in full at 1.7. It is the only claim in the document that
carries the word "structural" and does not earn it, and D-095 has already recorded
it as such. **The deciding sentence is D-060's: flow-proving means circulation
verification stays possible.** The door is open, the decision that closes it is
S-05, S-05 is deliberately held open, and D-060 attaches a price to keeping it
open which nobody will pay for a capability they have been told is impossible.

**Second. 2.10 and 2.18: the loop's movement and the slow failure.** These are the
same door seen from two sides. 6.4 item 5 is the more honest of the two - it says
"by choice", which is a current word - but it then rules the fix out in a sentence
of its own: "**The mitigation is not a sensor.** It is the event-driven re-measure
list in commissioning.md." **That is a design preference stated as a property.**
The re-measure list is a good mitigation and I am not arguing against it. **I am
reporting that a reader is told a sensor cannot help, when what is true is that a
sensor has not been chosen, and that one candidate for it is already an open row
with a fork that D-060 prices.**

**Third. 2.12: "Never name a cause."** The prohibition is right today and the
handler should keep it. **The justification is current, not structural: the Pi has
no leak, E-stop or interlock input because none was ever proposed, not because
anything forbids one.** S-18's row is the frozen statement that G-26 restricts
driving and not reading. **The residual is that 7.1's never-list, which is written
to be permanent, contains one item whose ground could be removed by a decision
nobody has been asked to make.** Whether it SHOULD be removed is a separate
question with real costs - more conductors, more inputs, more sweep columns - and
I am not proposing it. **I am reporting that the document does not distinguish
"the Pi has no such input" from "the Pi may not have such an input", and the
second is not on file anywhere I read.**

## Two claims where document 12 gets the distinction right, recorded so the pattern is visible

**11.16, the floor on delivered volume.** "Nothing on **this build** can narrow it.
If a per-driver indication that requires actual commutation ever lands at the Pi
it becomes the only candidate, and **even then the book decrements the ceiling**."
That is a current claim, labelled current, with the condition that would change it
named and the rule that survives the change stated. **It is the model for what 2.17
should look like.**

**11.12, S-14.** "A full search on 2026-08-30 ... found no Pi application source
in reach - not in the tree, the history, the remote, the machine or this
conversation. **That is not a claim the project has no code.**" That is T-003
observed exactly, in a document that had every incentive to assert the absence.

---

# What I could NOT settle from the tree

**1. Whether a flow-proving S-05 actually delivers window validity, or only
window invalidity.** I have established from D-060, S-05 and S-20 that document
12's "structural" is wrong. **I cannot establish what the right answer is.** The
flow-proving element's response time, its threshold, and the bypass timing D-060
makes definite all bear on whether "K-DRY made throughout the window" means "flow
was proved throughout the window", and none of the three exists. `water-s18-f003.md`
and `main-panel-poles.md` may bear on it and I did not read them. **What I can
say is that "current" and "structural" are different, and that the tree contains a
frozen sentence saying the capability stays possible.**

**2. Whether the C-09 exit condition belongs in document 12 at all.** 1.15
establishes that nothing states one. Whether the fix is an application flag, an
operator procedure, or a line in the declaration is a scoping call I do not own.

**3. What `subsystems/control-software-f004.md` and `-p09.md` actually contain.**
Document 12 section 1.3 declares them superseded as deliverables and standing as
reasoning, and names two things in them as WRONG. **I did not read either, so I
cannot confirm that the withdrawal at 6.4 covers everything in them that rested on
the same premise.** F-070's row in findings.md still reads "Not fixed", which was
true before document 12 and appears not to be now. **Someone should check whether
those two documents contain any OTHER claim resting on "the Pi commands the
circulation relay", because that premise was load-bearing enough to produce one
withdrawn precondition and may have produced others.** T-022's shape: one label,
more than one claim under it.

**4. Whether motor steps per revolution is truly not on file.** N-3 says "Not on
file". I searched every .md in the tree for "steps per revolution" and found
parts.md, commissioning.md, software-spec.md, control-software.md, pump-boxes.md
and pump-boxes-p09.md, and the last of these says "parts.md does not give it".
**No file states a value. I did not open the motor's datasheet, which is with the
owner.**

**5. Whether document 12's "three latencies in series, none of them on file"
(4.5.1) is a grounded absence claim.** C-17's search is recorded, D-064's is
recorded, D-077's is recorded, S-14's is recorded, and document 12 leans on all
four correctly. **4.5.1 and N-12 make absence claims with no named search behind
them.** They are almost certainly true and I could not confirm either without
reading files outside my scope. Under agents.md rule 8 they are the two sentences
in the document that assert from absence without naming what was read.

**6. Anything about the operator interface.** HELD by the owner. Document 12's
sections 3.5 and 7.10 state what a fault and a record require of a screen, and I
compared those against channel-token.md's "two rules the UI owes the wall" and
G-19 and found them faithful except at 1.3. **I asked no question about the UI and
this run should not be read as having examined it.**

## Where document 12 and the frozen tree agree, stated plainly and not manufactured

- **111 of 126 restatements are clean**, including every one of the hard ones: the
  asymmetric readback discipline, the ordered permissive-drop handler, the
  write-ahead direction, the four-plus-one outcome set, the direction-awareness
  argument, and G-16 in all four of its forms.
- **No pin, no address, no timing figure, no resistance, no steps-per-millilitre
  figure and no part specification appears anywhere in the document.** I extracted
  every identifier and read section 10 in full. Section 10 names twenty numbers
  and states none of them.
- **D-057 is observed rather than merely restated.** No attribute value from the
  register appears in document 12, including the two the register does hold.
- **The document corrects its own author's prior return, in public, inside
  itself** (1.3, 6.4, section 12, F-070), and applies T-022 to the correction by
  splitting Claim A from Claim B before qualifying either. **That is the trap
  observed on the same page it is cited.**
- **T-019 is applied to the document's own scepticism**: the closing paragraph of
  6.4 admits that C-08, C-03, C-04 and the detectability margin rest on evidence
  no better than the C-02 it refused to estimate, and section 10 lists them
  together for that reason.
- **And the largest agreement, which is why 1.7 is worth the space it takes:**
  every one of document 12's claims that descends from **G-26 and D-052 about what
  the Pi COMMANDS is structural and correct**. The failures are all in the second
  half - what the Pi can OBSERVE - where G-26 says nothing, and S-18's row says so
  in terms.
