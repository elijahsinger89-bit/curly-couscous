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
