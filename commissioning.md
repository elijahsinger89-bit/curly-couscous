# Commissioning list

Measurements that must be made against real parts, on this build, by the owner.
None of these may come from a datasheet or from any agent's memory. A figure
that arrives without a measurement behind it is not a figure.

BOSS owns this file. An agent that needs a number it cannot derive adds a row
here through BOSS rather than assuming one.

| # | Measurement | Why it is needed | Who measures | Blocked on |
|---|---|---|---|---|
| C-01 | Delivered volume per head, per unit time and per step | Steps per millilitre. Nothing in the system measures delivered volume, so a wrong figure is invisible. G-04 | Owner | Heads mounted, tubing chosen |
| C-02 | Settling time for the tank-read verifications | F-004. A check read too early reports a healthy dose as a failure | Owner, unless DOSING and CONTROL-SOFTWARE can derive it from day tank volume and loop flow | Day tank filled, circulation running |
| C-03 | pH step per single dose, pH up and pH down separately | S-16. The attribution must exceed probe noise and drift to mean anything | Owner | C-02, probes live |
| C-04 | EC step per single dose, per EC-moving channel | S-15. Same reason as C-03 | Owner | C-02, probes live |
| C-05 | Head discharge pressure against a flowing manifold | Only needed if a pressure-based option is ever chosen. Not currently needed | Owner | Not scheduled |
| C-06 | Whether the head holds against back-siphon with the jug above the inlet | Decides whether flooded suction is safe, and whether an anti-siphon device is required | Owner, with PUMP-BOXES stating what the head is | Jug placement |
| C-07 | Loop turnover time, day tank through manifold and back | Feeds C-02 and the O-01 sequencing | Owner or derived by WATER from tank volume and circulation flow | Loop plumbed |

Not on this list, deliberately: anything that can be read off a datasheet the
owner pastes in. This file is only for what the build itself has to tell us.
