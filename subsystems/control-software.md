# CONTROL-SOFTWARE

Read first: agents.md, interface-table.md, decisions.md, traps.md.

This is the one subsystem not named for a physical thing. It shares the display
box with the Pi hardware. It is split out so the seam between them, S-12, is
written down and checkable rather than living inside one agent's head. See
decisions.md D-004.

## STANDING INSTRUCTION, 2026-08-30: THE UI IS HELD

**Do not design the touch UI. Do not ask for its requirements.** The owner has a
set of operator interface requirements, including things he wants done differently
from commercial controllers he has used, and he is deliberately withholding them
because **the fault model is still moving and he will not have a UI designed
against a moving target.**

They arrive when the fault behaviour is settled. Until then, UI statements are
limited to what a fault or a record REQUIRES of a screen, which is what the P-09
and F-004 answers already contain, and go no further.

## Scope, owned completely

The Pi application. Dose scheduling and the arithmetic that turns a requested
volume into a step count. Step commanding for eight channels. Enforcing one
pump at a time. Driving the permissive coil and evaluating the readback. Reading
the three EZO circuits. Tracking millilitres dispensed per channel against a
user-entered full-jug volume and warning on a low computed remainder. Fault
states and what each one stops. The touch UI. Logging and persistence across a
power cut.

Ends at the GPIO and I2C map, S-12. Nothing electrical.

## Out of scope

Every wire, pin, level and component. That is DISPLAY-BOX. Safety in hardware:
the permissive chain drops power without software and software may not be relied
on to do it.

## FROZEN interface slice

| ID | What is frozen |
|---|---|
| G-04 | Dose by commanding a step count and booking the volume as dispensed. Nothing measures delivered volume. Do not write code that assumes feedback exists |
| G-05 | Jug remaining volume is arithmetic against a user-entered full-jug volume, per channel. No jug sensors |
| G-06 | Only one dosing pump turns at a time. Mandatory, until a thermal measurement says otherwise |
| G-09 | Drive the permissive coil, read the auxiliary contact, and treat a mismatch between command and readback as a fault, including the welded case where the contact stays closed after the coil is dropped |
| G-01, G-02 | No level sensing. The only level input is one dry contact, day tank fill in progress |
| G-07, G-13 | A leak, an E-stop or a lost interlock drops power in hardware. Software neither causes nor prevents it, and must behave correctly when power vanishes mid-dose |
| G-10 | Probes read upstream of all injection. A reading reflects the tank, not the dose just injected |
| D-007 | There is no flow signal into the Pi. No code may wait on, poll or time out against one |
| D-009, S-15 | EC rise during a dose is the whole-loop check. It is valid only during a dose, it cannot attribute a change to a channel, and it does not move for pH up, pH down or fulvic. Read findings.md F-001 before writing any verification logic |
| D-011, S-16 | The pH probe attributes the pH up and pH down channels. Two constraints are part of the row and are not optional. First: those two channels cannot be attributed at the same time. If both fire in one batch the movements cancel and pH shows the net. Attribute whichever was commanded, and treat a batch that fires both as a FAULT CONDITION that must not read as passing. Second: it is a delayed check, see F-004 |
| D-012, F-004 | Every implicit verification reads the day tank after recirculation, so all of them are delayed by an interval nobody has measured. A check read too early reports a healthy dose as a failure. No verification logic is written until the settling time is settled |
| D-013, S-17 | Fulvic is unattributed and stays that way. Do not solve it, do not warn about it as if it were a defect |
| **G-16, D-017** | **NO AUTOMATIC RE-DOSE. EVER.** Software never tops up, retries, re-doses or corrects on its own, on any reading of any check. If a check reports no movement the batch STOPS and tells the operator, and the operator decides. This is a RULE, not a parameter: no configurable retry count, no threshold anyone can turn up, no code path that can be enabled later. It is frozen before any code exists so it cannot be argued into existence by a plausible-looking edge case. Consequence to hold on to: with this rule in place a settle-window timing error can only produce a FALSE STOP, which is loud and safe. The direction of error is chosen, not accidental |
| **D-021, S-19** | CONTROL-SOFTWARE is the DEFINITIONAL end of the channel token. It declares what channel N is. DISPLAY-BOX, INTERCONNECT, PUMP-BOXES and DOSING consume that declaration and match it. Nobody else defines it, and there is no translation table anywhere on the chain |
| parts.md, P-07 | **The Pi is powered independently, fused and NOT relay switched. It has power whenever the panel does and stays alive through a permissive drop, so it can log and alert on it.** No code may assume the Pi loses power with the system. And **nothing in the panel can power cycle the Pi**: it reboots by software or by killing the panel, so a WATCHDOG is the only recovery path |
| parts.md | **Software may never report commanded state as measured state, anywhere.** The permissive readback exists because the Pi commanding the rail off and eight drivers staying live is a real failure |
| parts.md, C-01 | The manufacturer's 1.0 ml per revolution is at NO BACK PRESSURE. Every dose here injects into a pressurised circulating manifold, so the real figure is lower by an amount nobody has measured. Dose arithmetic converts against the MEASURED figure from C-01, never the manufacturer's |
| parts.md, C-17 | Steps per millilitre is motor steps per revolution times the driver microstep factor divided by ml per revolution. The microstep factor is PUMP-BOXES' setting, recorded at C-17. Do not assume one. A file search on 2026-08-30 confirmed no file states a value and no agent has assumed one |
| D-024, S-15 | The EC check window is anchored to the dose and extends past the last commanded step by the settling interval. The old wording is corrected, not interpreted |

## Settled

- Three process measurements exist: pH, EC and temperature. There are no others.
- Doses are by volume.
- The Pi commands relays for the fill solenoid, transfer pump, circulation pump
  and chiller contactor. It reads no floats.

## Open, owned by CONTROL-SOFTWARE

- Behaviour when power is removed mid-dose: what is written before the step, so
  a resumed session knows what was actually delivered rather than what was
  planned. G-04 means there is no way to measure the truth afterwards.
- What each fault stops, and what it takes to clear it.
- Dose arithmetic: the shape of the calculation, not the numbers. Steps per
  millilitre is a calibration figure that must come from a measurement the owner
  performs, never from a datasheet and never from memory.
- Language, framework and how the UI runs on the 7 in display.
- What is logged and where it survives a power cut.
- Whether a dose may start while a day tank fill is in progress, S-03. This is a
  question for the owner, not a choice for this agent.
- S-19: declare the channel token. One identity that rides software index, pin
  map, cable core, driver, head, box, barb, tube, jug station, jug and product,
  with no translation at any point. Declare it so the other four can consume it.
  It does not need PUMP-BOXES' box division to exist first: the definition comes
  first and the box division consumes it.
- F-004 jointly with DOSING: what settling time the tank-read checks require,
  what sets it, and whether it can be derived from day tank volume and loop flow
  rate or must be measured at commissioning. If it is a measurement it goes on
  commissioning.md as C-02.
- S-14: what the fault registry actually contains, and what raises any
  circulation fault today. Answer from the code. If there is no code yet, say
  where the code lives and that you looked. Do not answer from memory and do not
  claim absence without naming what you read.

## Waiting on

| From | What |
|---|---|
| DISPLAY-BOX | The pin and address map, S-12. Nothing may be built against it until BOSS freezes it |
| Nothing | S-13 is closed. There is no flow signal into the Pi and there never was one. D-007 |
| Owner | Whether dosing during a fill is permitted |

## Do not

Do not state an EZO command, an I2C address, a library name or a Pi pin from
memory. Return the requirement and a search term. Do not invent a steps per
millilitre figure, not even as a placeholder: nothing downstream measures it, so
a wrong number is invisible until plants die.

## F-004 answer, 2026-08-30

Returned in subsystems/control-software-f004.md. Stopped part-way, not declared
finished. The verification logic is not written and will not be written until
C-02 exists, per D-012, because a placeholder in this code is invisible until it
is wrong and nothing downstream can check it.

What it produced that is now BOSS-held: commissioning row C-08, the missing probe
noise and drift band; interface S-18, the chiller as a contaminant of settle
windows; and findings F-005, the S-15 wording tension.

## P-09 answer, 2026-08-30

subsystems/control-software-p09.md. Stopped part-way. Nothing buildable: P-09,
S-07 and S-08 are all OPEN.

The framing that changes everything else: **the permissive drops on ordinary
shutdown too, so this handler runs on the NORMAL path several times a day, most
often with nothing in flight. It is not an exception handler.** A handler that
raises a loud fault on every shutdown gets switched off. Severity splits;
the record never does.

Three things to carry forward regardless of what P-09 settles:
- **The delivered fraction is a bound structure, not a number.** commanded,
  ceiling from write-ahead, floor = zero. The step index at the halt is a
  COMMANDED count and is not evidence of delivery.
- **The asymmetric readback discipline.** An apparent drop is qualified over
  samples; an apparent WELD latches on a single sample and never clears. An
  oxidising contact then produces false stops and never a missed weld, which is
  D-017's chosen direction of error applied to a different signal.
- **The watchdog is fed from the sequencer loop, never from an independent timer
  thread.** A timer that keeps ticking while the sequencer is wedged is T-014 in
  the most expensive place on this build.

## Search record, 2026-08-30, interface S-14

CONTROL-SOFTWARE was invoked with source access to answer what the fault
registry contains and how any circulation fault is raised today. Recorded here
so nobody repeats the search.

Result: no Pi application source in reach. No Python, C, service unit, config or
script that reads the EZO circuits, drives steppers or defines faults.

What was searched, including the searches that returned nothing:

| Where | How |
|---|---|
| The repo working tree | Full recursive find, all types including dotfiles. Twelve markdown files and .git, nothing else |
| The repo history, not just the tip | git ls-files, log --all --diff-filter=A, rev-list --objects --all, branch -a, show-ref, stash list, reflog --all, fsck --dangling. Every path that has ever been in this repository is one of those twelve markdown files |
| The remote | ls-remote heads and tags, and a branch listing. One branch at the same SHA. No tags |
| The machine | Listings of /, /home, /home/user, /home/claude, /home/ubuntu, /root, /mnt, /mnt/attach, /mnt/user-data, /media, /opt, /srv, /tmp, /old_root, plus df for other mounts |
| Other repos | find -xdev for .git: three, this project plus rbenv and nvm toolchains |
| Source extensions | find -xdev for py, c, cpp, h, hpp, ino, service, timer, rules, toml, yaml, yml, ini, cfg, json, sh, pruning system and toolchain trees. Only OS configuration under /etc |
| Python project files | requirements, pyproject, setup.py, Pipfile under user areas. Two, both inside bundled skills, unrelated |
| Archives | zip, tar, tar.gz, tgz, img, 7z, bak under user areas. Two, both unrelated |
| systemd units | /etc/systemd/system and /lib/systemd/system filtered for dose, dosing, ferti, pump, skid, pi-, control, circul, ezo. No matches |
| Content | grep -rIl over /home /root /mnt /srv /media /opt /usr/local /var/tmp /var/log /tmp for EZO, Atlas Scientific, peristaltic, fertigation, no-circulation, no_circulation, circulation, TMC2209, stepper, permissive, fault_registry, FaultRegistry, day tank, day_tank, PT-1000, PT1000, steps_per_ml, steps per ml, ISCCB |
| This session's own transcripts | Every hit outside the project's markdown was either an unrelated toolchain file or this session's own logs echoing the grep command line. Checked rather than counted. Self-reference, not evidence |
| The conversation itself | Every user message parsed for code markers alongside circulation, EZO, stepper, dose, fault. Zero. No source was ever pasted in |

Out of reach, named so it is not mistaken for absence:
elijahsinger89-bit/FS_Testing, private, described "First cc test", created
2026-08-29, one day before this repo. GitHub access this session is scoped to
curly-couscous only, so its contents are unknown.

Conclusion: the code may exist on the Pi, on the owner's machine, or in that
repo. This is not a claim that the project has no code. S-14 stays OPEN and
UNVERIFIED and nothing is built against it.

Marked as inference from the frozen documents, not from code, and not a finding:
if an implementation does exist, D-007 and S-13 mean it has no input that
distinguishes circulating from not-circulating at rest, and F-001 limit 1 says
the same from the other side. So any circulation fault it contains can only be
raised from EC behaviour during a dose, or from nothing. That is a question for
whoever can read the Pi.

## OPEN, routed 2026-09-03 by D-101. AUDIT RUN 3 ON YOUR DOCUMENT.

Read audit/2026-09-03-doc12-vs-frozen.md in full. 126 pairs compared, 111 clean
restatements. **The document held up. What follows is the fifteen that did not,
and one of them is expensive.**

**1. THE STRUCTURAL CLAIM THAT IS ONLY CURRENT. 2.17, 11.6, section 12, and 6.4.**

You call positive confirmation of settle-window validity structurally impossible.
**D-060 says the opposite in frozen text: flow-proving means a timing element is
definite and circulation verification stays possible.** Three things to check
against your own text:

- The support you cite, F-001 limit 1 and F-003, is about the pump AT REST. A
  settle window sits inside a RUNNING period by design, under D-063.
- **G-26 restricts what the Pi DRIVES and not what it READS.** S-18's row is the
  frozen statement of that. You respect the boundary at 4.3 and blur it at 6.4,
  where "neither commands nor observes" runs a structural half and a current half
  together.
- S-20 reports a second pole of K-DRY to the Pi, and circulation is a pole on that
  same relay under D-058. Your own Claim B concedes the voiding mechanism and then
  6.4 item 3 says flatly "not enforceable in software".

**This one is expensive rather than untidy, and the reason is not editorial.**
D-060 prices the flow-proving fork of S-05 at one timing element. **Nobody pays for
a capability they have been told is impossible.** Decline to pay and S-05 closes
level-based, and the claim becomes true retroactively. T-023.

BOSS made this worse, not you alone: D-095 banked it and C-23 copied it citing your
document. C-23 is corrected and D-095 is superseded in part. **The document is
yours to correct and BOSS has not touched it.**

**2. GRADE EVERY IMPOSSIBILITY CLAIM UNDER G-36, NEWLY FROZEN.** Structural means
a frozen rule or physics and no addition could change it. Current means what has
been bought, wired or decided so far, and a current claim NAMES WHAT WOULD CHANGE
IT. AUDIT found 24 claims: 17 structural, 6 current, 1 mixed. The six are in its
Part 2 table with the deciding sentence for each. **Two of yours already do it
correctly, 11.16 and 11.12, and 11.16 is the model: the condition that would change
it is named and the rule that survives the change is stated.**

**3. THE ONE THAT BITES IN THE BUILD. Section 3.4 and 5.2.** F-075. **3.4 says how
a channel enters OUT OF SERVICE and never how it leaves.** And 5.2's admission
check is a live token plus a non-void C-01 and C-17, and **does not include C-09.**
A channel whose driver was replaced is readmitted on a C-01 that may have been
re-measured against the wrong channel, which is the one failure S-19 and D-022 both
say passes every other check in the system.

**4. N-20 AND channel-token.md ARE BOTH STALE BY HOURS.** Both say the colours are
not bound. **D-099 bound them 2026-09-03.** The declaration is yours; BOSS does not
edit it. Note that the colour lives on the MARKER and is an identity axis on the
token, not a second token, so your forbidden list is unaffected: nothing computes
from a colour.

**5. THE REST**, in the audit file with section numbers: four DRIFT, three WIDENING,
five OMISSION. The two worth naming here are **1.2 and 1.3, where G-16 and G-19 as
you state them are WIDER than the frozen rules they cite** - widened in the safe
direction, but an implementer can cite the frozen text against you, so either the
rule moves or the document narrows. And **1.5, where 2.5.5's shipping rule traces
to D-012 and is not in D-012**; its home is D-083's recital.

**6. F-055 IS ABSENT FROM YOUR DOCUMENT** and your readback discipline, both
permissive faults and N-14 all run on the contact F-055 is about.

Write the correction in ONE pass at the end, per the invocation rule. State no
value, no pin and no part number from memory.

## F-075 HAS A DEADLINE NOW, D-102. IT DOES NOT WAIT BEHIND THE REST.

Pulled out from behind the audit backlog at the owner's instruction. **Settle it
before C-01 is ever run.**

The defect, again: **3.4 states how a channel enters OUT OF SERVICE and never how
it leaves, and 5.2's admission check is a live token plus a non-void C-01 and C-17
and does not include C-09.**

**Why the deadline is C-01 specifically.** Before C-01 runs, a channel measured
against the wrong channel is a mistake nobody has recorded. **After C-01 runs it is
an entry in channel-register.md with a token, a date and a measurement procedure
behind it, and nothing downstream can distinguish it from a correct one.** G-05
then decrements that jug against it forever, and S-19 and D-022 both say this is
the one failure that passes every other check in the system.

C-01's preconditions in commissioning.md now carry the gate.

Two things to return, and BOSS is not writing either:

1. **The exit condition from OUT OF SERVICE.** A state with an entry and no exit is
   the shape that gets exited by hand.
2. **Whether C-09 joins the admission check**, and if it does not, what else
   catches a driver replacement that voided C-01 for the wrong channel. C-09 is
   free, needs no hardware and is already a re-measure trigger for any rewiring or
   renumbering.

Write in ONE pass at the end.

## D-105, 2026-09-03. ROLE IS A PER-CHANNEL SETTING. THIS IS THE LARGEST CHANGE SINCE G-26.

Owner's requirement. **Any channel may carry nutrient, pH-up or pH-down, assigned
per channel and changeable.** The hardware always allowed it - eight identical
pumps, identical tubing, drivers and wiring, nothing physical assigning a role.
**What prevented it was software keying role to a channel number.**

**The two mechanisms that need role both already exist in your document:**

| Mechanism | Today | Under D-105 |
|---|---|---|
| The plan builder, which excludes pH from every injection group so pH runs alone and last | Reads a FIXED LIST | Reads the per-channel role setting |
| The signed pH attribution, S-16 and D-083 | Needs the expected direction for a commanded channel | Reads the per-channel role setting |

**Nothing is built against this yet.** A reach sweep is running to answer whether
it touches more than the plan builder, the attribution check, the register schema
and C-09. **Wait for it. Do not start on the assumption that those four are the
whole list.**

**THE COST, and it is named rather than absorbed.** A role that can change is a
role someone can change wrongly. **A wrong role is worse than a wrong product: it
makes the signed check expect the wrong direction, so the check CONFIRMS the error
instead of catching it.** G-32 is amended to bind on role, and C-09 now verifies
the role and not only the product.

**Two things dissolve, and note that they DISSOLVE rather than shrink:**

- **F-063.** There is no fixed pH pair to separate. **channel-token.md's S-16
  non-adjacency rule is YOURS to restate: it stops being a constraint on the token
  NUMBERING and becomes a constraint on the ASSIGNMENT - pH-up and pH-down are not
  assigned to adjacent tokens or neighbouring colours.** That is strictly better,
  because as written it was unsatisfiable without renumbering, which the
  declaration's forbidden item 2 forbids.
- **F-080 and the CH6 question.** No channel's role comes from elimination any
  more, so CH6 needs no origin. Your section 3.2, which correctly told an
  implementer not to promote the inference to a fact, is now moot in the right
  direction.

Write in ONE pass at the end, and not before the reach sweep reports.

## THE REACH SWEEP REPORTED, D-112. FIVE BREAKS. START HERE, NOT AT THE OWNER'S FOUR.

audit/2026-09-03-role-reach-sweep.md. 41 items: 5 BREAK, 24 REQUIRE CHANGE, 8
DISSOLVE, 4 SURVIVE. **The owner's four were right and were not the whole list.**

**THE SHARPEST, F-081, and it is in your own document.** C-03's signed pH step and
C-04's EC step are **role-dependent recorded data with no re-measure trigger for a
role change.** Your 2.1.8 and 2.1.9 already void C-01 on a driver change or a tube
change. **The mechanism exists and is applied to the figure whose wrongness is
LOUD, not to the one whose wrongness makes the check CONFIRM the error.**

**THE POST-C-09 GAP, and it is a SCHEDULING gap rather than a capability one.**
C-09's new question (b) is a sufficient test whenever it runs. Nothing schedules
it. Three absences, and they need three different answers:

| | Absence |
|---|---|
| No trigger | **A role change is not a case in ANY change procedure** - not channel-token.md's four cases, not the eleven re-measure trigger rows, not your 3.4 OUT OF SERVICE causes. **It lands on top of F-075, already open with D-102's deadline** |
| No invalidation | C-03 is not voided the way C-01 is |
| No detection | **Under G-32 as amended the signed check scores a wrong-role dose as PASS**, because the prediction moved with the error |

**BOSS has designed no mechanism and will not.** Return one.

**Four more from the sweep that are yours:**

- **F-085.** Section 12's "attribution for six of the eight channels" is a COUNT
  WRITTEN AS A PROPERTY and it is graded structurally impossible. Under D-105 the
  count is a consequence of assignment, so it is CURRENT. **G-38 is frozen out of
  this: a grade is only true against the tree it was graded on. Five more
  count-as-property claims are listed in the sweep.**
- **F-084.** "The fulvic channel" is a fixed identity in four files and **fulvic is
  not a value in D-105's role set.** Do not add a role value - fulvic is a PRODUCT.
  **The question is where product-specific behaviour lives now that role is its own
  field, and the owner is settling the role vocabulary. Wait for it.**
- **"Opposing" is now a TIME-VARYING SET.** An open window records which CHANNEL,
  not the role it was opened under. G-16a forbids offering the opposing channel;
  that set can change while a window is open.
- **Where role definitionally LIVES**: the register under D-057, or the
  controller's blocked-channels path, which no file in this tree shows. **Two homes
  for the field the signed check reads is one too many.**

**And F-082, which is yours because channel-token.md is yours.** The colour
constraint has REVERSED DIRECTION: colour is bound to token and frozen, role is
free at assignment, **so the frozen colour map now constrains WHICH TOKEN PAIRS MAY
TAKE THE pH ROLES. Forbidden item 4 requires that set be written out, not
computed.** Enumerate it.

Write in ONE pass at the end.

## THE ROLE VOCABULARY IS SETTLED, D-122 THROUGH D-124. FOUR INSTRUCTIONS.

**1. EXACTLY TWO IS NOT ENFORCED. The rule is CONDITIONAL, not counted.** Zero pH
channels is legal, one is legal, three is legal and foolish, **and software does
not prevent it.** What makes the count irrelevant is already true of your design:
**the signed attribution works from the ROLE, not from the pair, so it works with
one pH channel or with two.**

**Rewrite the 25 pair-assuming items to this form: "the opposing pH channel"
becomes "a channel with the opposing pH role, IF ONE IS ASSIGNED."**

**And the instruction that matters more than the rewrite: ANYTHING THAT CANNOT BE
WRITTEN THAT WAY IS A REAL DEPENDENCY ON THE PAIR. List those separately rather
than forcing them into the form. The rewrite is a TEST, and the items that fail it
are the finding.** Return that list.

**2. FULVIC IS A PRODUCT, NOT A ROLE. THERE IS NO FULVIC CHANNEL.** F-084 answered.
It is a **nutrient by role**, and not moving EC meaningfully is a **product
attribute in the channel register** under G-33.

**Struck from the files BOSS owns: interface-table.md S-17, commissioning.md C-04,
findings.md F-050 and F-078. subsystems/display-box-sweep.md is ANNOTATED, not
edited, because a returned answer is a record of what an agent said.** Strike it
from anything of yours. **Leaving one product's identity keyed to a channel would
have reintroduced exactly what D-105 dissolved.**

**3. D-123: ANY ROLE CHANGE VOIDS EVERY ROLE-DEPENDENT RECORDED FIGURE.** C-03 and
C-04 are voided by a role change exactly as C-01 is voided by a driver or tube
change. **The owner's diagnosis, and keep it in the implementation note: the
voiding was applied to the figure whose wrongness is LOUD and not to the one whose
wrongness makes the check CONFIRM the error.**

All three of D-112's absences get closed, not one: **a case in the change
procedures** - channel-token.md's cases, the re-measure trigger table, and your 3.4
OUT OF SERVICE causes; **the invalidation itself**; and **a re-measure trigger row
so the void has a route back.** C-09 is the test and it now has an event that
schedules it.

**4. D-124: UNBIND THE COLOUR, DO NOT REBIND IT.** F-082 resolved the right way.
**Colour identifies the CHANNEL and nothing more.** The pH separation becomes a
rule at ASSIGNMENT - **whatever two tokens take the pH roles must not have
neighbouring colours - checked at C-09.**

**And forbidden item 4's enumeration requirement dissolves with it.** There is no
permitted-pairs set to write out; **there is a rule checked against whatever
assignment exists. A rule is not a set.** Restate channel-token.md accordingly.

Write in ONE pass at the end.
