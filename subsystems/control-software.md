# CONTROL-SOFTWARE

Read first: agents.md, interface-table.md, decisions.md, traps.md.

This is the one subsystem not named for a physical thing. It shares the display
box with the Pi hardware. It is split out so the seam between them, S-12, is
written down and checkable rather than living inside one agent's head. See
decisions.md D-004.

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
