# AUDIT run 1: DISPLAY-BOX's sweep against MAIN-PANEL's pole budget

Returned 2026-08-30. AUDIT read exactly five files: the two returns,
interface-table.md, decisions.md and traps.md. It changed nothing and every item is
a question to BOSS. Stopped part-way.

Recorded here in full because these are open questions, not answers. BOSS's
disposition is noted per item where one has been made.

## Tier 1, where a wrong answer costs a rebuild, a relay or a rewire in a closed box

**Q1. Are G-25 and S-20 frozen against a relay that does not exist and has not been
bought?** MAIN-PANEL marks K-DRY "RELAY DOES NOT EXIST" and decisions.md says
quantities beyond the parts list are not decided, yet D-038, G-25 and S-20 all stand
on the fifth relay. *BOSS: resolved after AUDIT ran. The owner has said buy the
relays, D-044. The row stands. Recorded because the sequencing was real: two frozen
rows preceded the purchase.*

**Q2. Do the two returns agree what "the complementary pole" costs, and does
K-FILL-D have it to give?** Does complementary mean the NC throw of the same
changeover contact, which by MAIN-PANEL's own rule sits at the same potential and
costs nothing, or a fourth pole already spent on PL-G? **And do both agents know
they may be spending the same pole?** *OPEN. D-042 took the NC contact; whether that
is the same throw or another pole is MAIN-PANEL's to state.*

**Q3. Does MAIN-PANEL's PL-R/PL-Y truth table depend on the exact fact DISPLAY-BOX
says nobody has written down?** If the permissive coil positive is raw 24 V rather
than downstream of the master latch, **is "PL-R on, PL-Y on" still impossible, or is
it the ordinary reading for a permissive string open with the Pi still commanding
the contactor - a diagnosis that would send a builder to replace a healthy
contactor?** *OPEN and sharp. It couples F-019 to D-045.*

**Q4. MAIN-PANEL says it is blocked on DISPLAY-BOX for F-021. Did DISPLAY-BOX answer
it?** AUDIT can find nothing in the sweep stating the logic board's coil-drive
capability. **Is the difference between a shortfall of one relay and three still
entirely unanswered, and does DISPLAY-BOX know it owes it?** *OPEN. It does now.*

**Q5. Do the two returns agree how many relay coils the Pi actually drives, and
which relays they are?** S-09 names four coils. G-01 and G-03 make both fills float
seal-ins invisible to the Pi. MAIN-PANEL lists only K-CIRC as Pi-commanded and
**no relay anywhere carries the chiller coil drive S-09 requires.** *OPEN, and
DISPLAY-BOX reached the same contradiction independently the same day. Findings
F-027.*

**Q6. Does the VDD conductor defeat P-07, and does D-031 know it?** P-07 is closed on
the ground that the Pi survives a drop and can log it; D-031's three reasons do not
mention that the VDD conductor is a path by which a pump-box fault reaches the Pi's
supply. **Is this a consequence of a closed decision that the decision does not
carry?** *OPEN. Sharpened the same day by the short column: it is over-voltage, not
merely over-current.*

**Q7. On a watchdog reset, does the permissive drop, and must an operator then press
RESET?** The pins go high-Z, the physical pull holds the contactor off, and only
RESET re-closes the master latch. **Do the two returns agree what a watchdog reset
physically leaves behind - a system that recovers when software returns, or one that
needs a person at the panel - and is that the intended behaviour for an unattended
reset?** *OPEN, and it is a question for the owner.*

**Q8. Is "C-06" two different things?** The C-nn namespace was shared between the
interface table's cable crossings and commissioning.md, and both returns cite "C-06"
meaning different rows. T-013's shape. *FIXED by BOSS: the interface table's cable
and enclosure crossings are renamed CBL-01 to CBL-07. Findings F-026.*

**Q9. Is S-03 a measurement of a fill, or the state of a relay coil?** MAIN-PANEL
says its state IS S-03; DISPLAY-BOX reads it as a statement about the tank; G-02
calls it the only level information software has. **Given the standing rule that
software never reports commanded state as measured state, is a seal-in relay's own
coil state a measured fill or a commanded one?** *OPEN, and it bears on what
CONTROL-SOFTWARE may do with S-03.*

**Q10. If the F-017 fix lands, does the property MAIN-PANEL calls "worth keeping"
survive?** PL-G sits on K-FILL-D specifically because it agrees with S-03 by
construction. **Inverting S-03 would make them inverses. Does the lamp still mean
what the panel legend says?** *OPEN, and D-042 has now landed the inversion.*

## Tier 2

**Q11.** Shared common or pairs: do the two returns describe the same conductors?
DISPLAY-BOX says one common takes out all five coil drives; MAIN-PANEL's class C
says "coil-drive pairs". **One picture in two vocabularies, or two different
builds?** T-006 and T-007 both name this crossing as live.

**Q12.** A pull resistor owned by PUMP-BOXES and a series resistor owned by
DISPLAY-BOX **form one divider against the driver's input threshold. Has either
named the other as owing them a number? And is "series current limiting" compatible
with "low-impedance drive", or are they competing requirements?**

**Q13.** Does the 23-GPIO census predate signals created the same day? It appears to
exclude S-20 and MAIN-PANEL's optional K-CIRC and K-DRY dry contacts. **T-012: is 23
the current number, and is the binding constraint being judged against a stale
census?**

**Q14.** D-031's third reason keeps VDD live partly because "logic staying alive
keeps DIAG and INDEX meaningful", **but no row lands either at a Pi input. Is that a
capability whose wire does not exist, T-004's shape, and if they are never landed
does reason 3 still say anything?**

**Q15.** Is MAIN-PANEL asking for a promotion decisions.md has already frozen? G-24
was frozen out of that very return. **Has anyone re-read the returns against the
decisions they produced?** *Real and general. Findings F-029.*

**Q16.** Does G-24 reach a lamp that is not on a contact? PL-Y under option 2.7 is
across a rail, not a pole. **Has MAIN-PANEL's own per-lamp requirement over-scoped
itself?**

**Q17.** Is the mixed-voltage adjacent-pole question asked of K-PERM as well as
K-FILL-D? K-PERM carries two voltage classes plus PL-R. **Does an unfavourable
answer cost two relays rather than one?**

**Q18.** Does pressing RESET to test lamps do anything to the permissive? The reset
is in the hardwired chain. **Does a lamp test also command a reset attempt, and does
the lamp test need a contact block that is not the reset contact?**

## Tier 3, evidence AUDIT could not check, and vocabulary

**Q19.** Which figures in the two returns are in parts.md and which are from memory?
AUDIT was not given parts.md and lists what it could not verify: the 55.34's pole
count, its 300 mW minimum, the 1.0 A per driver, the stated reason the RTD needs no
carrier, and whether subsystems mint their own row numbers when the interface table
says BOSS owns it. *BOSS: the row numbers are BOSS's annotations added when
recording a return, not agents minting rows. The rest are in parts.md.*

**Q20.** Can a parts.md line settle the substance of an OPEN interface row without a
decision and a dated entry? Raised against S-06. *Fair. S-06 is now closed by D-048
with a dated entry, which is the right form.*

**Q21.** Does S-20 inherit S-03's numbers along with S-03's shape? **G-23 says no
figure is carried between contacts. Is "same shape" at risk of being built as "same
12.5 mA", and should the row say so more loudly?**

**Q22.** Does S-20 make G-02 false? G-02 says the Pi gets exactly one level signal.
**A flow contact that also catches a dry tank may be a second. Does G-02 need
amending the way G-09 was, or does it stand?**

**Q23.** Does DISPLAY-BOX rely on a lamp design that is not settled? Its dead-display
mitigation rests on PL-R and PL-G, **and nothing states which fill PL-G means, and
PL-R is dark when healthy.**

**Q24.** Vocabulary: "the Pi clocks eight channels" against G-06's one at a time.
Same picture sequentially, or two assumptions about concurrency?

**Q25.** Vocabulary: does "both 22.32 poles spoken for" mean the two poles of
contactor #1 or all four across both? *BOSS: it meant contactor #1's two poles. Its
pole 2 is the S-08 readback and pole 1 the rail. MAIN-PANEL's option 2.6 concerns
contactor #2 and is not foreclosed by that phrase.*

## What AUDIT would have needed and could not have

Reported as a finding about the picture. It could not check either return against
parts.md, findings.md, commissioning.md, channel-token.md or any subsystem file.

**"A picture whose authoritative source is outside the audit set cannot be checked
at all."** parts.md is authoritative under D-026 and both returns cite it
repeatedly. Q19 and Q20 are unanswerable without it.

**BOSS's disposition on that:** the constraint is deliberate and stays. AUDIT
without the authoritative source returns questions rather than assertions, which is
the point. But the run scope should name which authoritative facts a run turns on,
so BOSS can answer those directly rather than leaving them as unanswerable items.
