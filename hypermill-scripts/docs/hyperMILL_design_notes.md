# hyperMILL Python scripts - design notes

Source of these notes: this conversation (Sept to 20 Nov 2026), the saved project memory, the delivered code (hyperMILL_automation_package.zip, last full build 10 Nov 2026, plus tool_center changes up to 12 Nov) and the logs sent back from hyperMILL. Anything marked **UNSURE** was not confirmed in the conversation or could not be checked.

Environment for every script: hyperMILL 35, inch sessions, Heller horizontal 5-axis (HF3500, HF5500, F series), SINUMERIK ONE. Scripts live in `C:\Users\Public\Documents\OPEN MIND\python`, each in its own folder with `.om\configuration.json` (StartupFile, Type Script) and `.vscode\` (interpreter `C:/Program Files/OPEN MIND/Shared/35.0/python/python.exe`, remote attach port 5678). Every script writes a log to `C:\Users\Public\Documents\OPEN MIND\<script>_log.txt`.

General rules settled across all scripts:
- No hyperMILL macros. Toolpaths are created directly with `Joblist.CreateJob` (decided 20 Oct 2026).
- The automation must work without a hyperMILL tool database. Tools are built on demand from catalog CSVs and imported into the document (16 and 20 Oct 2026).
- Feature selection and the frame each feature belongs to stay with the operator. One job must never mix features from different frames (19 Oct 2026).
- Dry run is the default wherever the script changes the document.
- Cutting data that is not the tool's own catalog data is always labelled in plain words. Borrowed numbers are never shown as the tool's own.
- hyperMILL keeps imported modules between runs, so every script reloads its library modules or loads them by file path.
- Windows reads text as cp1252 by default. Every table is opened as UTF-8 (`utf-8-sig`) since 10 Nov 2026.

---

## part_wizard_1

**What it does.** Builds the toolpath structure of a part. It creates no tools and uses no macros. Screens: machine and spindle (remembered for part_wizard_2), industry, part type, recommended setups, setups, part features, joblists to fill, material, stepover, plan summary, optional Add toolpaths, Create.

**Why it is built this way.**
- Created as `part_wizard_step1` (19 Oct 2026): the job-creating half of the feature-driven automation. Renamed part_wizard_1 later.
- Moved from macros to direct `CreateJob` on 20 Oct 2026, because macros carried generic tools and could not be controlled from Python.
- Each joblist is one setup (Op10, Op20...). It must have its frame (NCS), model and material set. Missing items are listed with "Stop and fix" or "Continue anyway".

**Rules and decisions.**
- Job settings (stock to leave, stepdown, stepover, clearance, approach) come from `tool_library\job_settings.json` for the material and operation, written with `SetCfgParameters`.
  - A formula key (`*KEY_F`) the new job carries, but the settings do not list, would override the saved value. It is set to the saved value as a constant.
  - Types without saved settings are created with hyperMILL's defaults and listed under "Check by hand".
- Jobs are named "<operation> <material>" (for example "Pocket Milling HEM Inconel 718"). part_wizard_2 reads the operation from that name and from a job file written to the temp folder (`part_wizard_1_jobs.json`).
- Add toolpaths: any of the 77 milling and drilling types in job_types.py can be added to a joblist after the plan.
- Hole feature mapping and pocket feature mapping run only when the file has no feature lists yet.
- Hole groups:
  - A group within 30 degrees of a joblist's approach axis is assigned automatically. Other groups get a drop-down to pick the joblist or Skip.
  - One hole toolpath per operation and diameter (taps and thread mills per thread), with the holes attached. The job gets the feature list's frame, because `SetFeatures` sets it.
- Opposing holes (rule settled 21 Oct 2026):
  - Two open-bottom holes (Through or Through_Hidden) of the same diameter facing each other on one axis are drilled from one side only. This applies only when the hole has an open bottom, meaning it connects through a pocket, milled or not.
  - The side kept is the one with more holes or counterbores, then the earlier joblist.
  - The drill gets a break-through length to the far side. part_wizard_2 then picks a drill that reaches the full length.
  - Threaded holes keep both sides.
- Carbide drilling gets no spot or centering before it. A Centering operation with a chamfer tool runs after drilling to chamfer the holes (16 Oct 2026).
- Boundary picture pop-ups follow, one per toolpath that needs a boundary or surface selection.
- Stock model drop-down (HEM jobs) and contour/surface selection stay manual (14 Oct 2026).

**Data sources.** strategies.py (part plans), job_settings.json, job_types.py, hole_jobs.py, machines.csv (through machine_pick), `icons\` (part and boundary pictures).

**Open / known not to work.**
- `CreateJob("DborX5")` for Boring has not been tested.
- hyperMILL keeps its own value for `*POSITION_TYPE` on drilling and centering jobs (saved 1, stays 0) and `*CONNECT_SMOOTH` on Face Mill (saved 0, stays 2).
- Opposing holes: his run on the morning of the fix still showed opposing drill features. The fix (merge_opposing) was delivered after his before and after logs. **UNSURE** whether he re-tested it in hyperMILL.
- `AUTO_STOCK_CHAIN` is off by default and not reported as tested. **UNSURE.**

**Tested in hyperMILL.**
- Lower receiver, confirmed working:
  - CreateJob for every planned type
  - the saved settings and job names
  - milling area from the joblist model
  - hole features attached
  - hole jobs on the feature-list frame
- Last log received (lower_receiver, HF3500, HSK63 DC, 16000 rpm):
  - 40 jobs created, 8 check items, 0 failures.
  - Several Op20 Centering and Simple Drilling jobs showed JobStatus.ERRORS before calculation. **UNSURE** of the cause; not resolved in the conversation.

---

## part_wizard_2

**What it does.** Puts a library tool and its cutting data in every toolpath, after part_wizard_1 and after the operator attaches pocket features and sets stock references. Screens:
1. Machine and spindle (the part_wizard_1 choice is offered first).
2. Tool manufacturer and performance level.
3. Joblists to work on.
4. Options: put tools in now (unticked = dry run), replace tools already in jobs, calculate and check afterwards.

**Why it is built this way.** Created as `part_wizard_step2` (19 Oct 2026). The operator attaches features by hand; the script scans the attached features for size and depth and imports the matching library tools.

**Rules and decisions.**
- The operation (from the part_wizard_1 job file, else the job name) sets the tool shape and the primary usage. Attached features set the size.
- Holes: diameter and depth pick the drill, chamfer mill, tap, thread mill, reamer, boring tool or helical end mill. Drills for reamed holes are under size by the ream allowance (0.016 in).
- Roughing (Pocket, Rough HEM, Rough Traditional, Arbitrary Stock, Form Pocket, 5X roughing):
  - largest first-choice end mill at or below 0.8 x the pocket diameter limit, and 0.05 in clear of it
  - flute at least the deepest pocket + 0.05 in
- Finishing and rest:
  - also no larger than 2 x the smallest pocket corner radius
  - only the reach has to clear the depth (a necked tool is fine)
- Floors (Plane): diameter limit applies. A floor corner radius turns a flat end mill into a corner radius end mill.
- No features attached: the operation's default tool size, flute at least 1 x D, and a "length not checked" note.
- Face Mill: Walter inserted face mill (2.0 in asked), else an end mill.
- Chamfer on 3D Model, Centering, deburring:
  - Walter: MC501 chamfer mill.
  - Kennametal and GARR have none in the library, so a 90 degree spot drill of theirs is used. **UNSURE** whether hyperMILL accepts a spot drill in those cycles.
- T-slot, hale, tangent (barrel), back boring, gun drilling, hole brushing: no such tools in the library; tool by hand.
- Among first-choice tools, the primary usage orders the families. The best-ranked family that has catalog cutting data is used.
- When no tool reaches the depth, the longest is used and flagged "too short".
- Library tools replace generic tools. The 16 Oct rule was to delete the generic macro tools at the end; macros were dropped on 20 Oct, so this no longer applies.
- Cutting data:
  - The usage's set, capped by the spindle max rpm.
  - Milling jobs get SpindleRPM, FeedrateXY and FeedrateZ (plunge = 0.5 x feed). Hole jobs get SpindleRPM and FeedrateZ.
  - Written with `SetTTProperty(name, float, 1)`.
- Calculate and check:
  - Calculates the joblists (`JobListSet.Run(uuid)`).
  - Sets floor stock to leave to 0 on "Bottom higher than top" and recalculates.
  - Lists jobs whose .pof file is under 12000 bytes (probably no toolpath).
- The check list names every tool whose cutting data is borrowed or standard values.

**Data sources.** All library CSVs through tool_lookup, hole_tools, hole_jobs and tool_usage; job_types.py (tool rule per operation); job_settings.json (default tool shape and size per operation).

**Open / known not to work.**
- `*JOB_CPNAME` (link the job to the tool's cutting-data set) set from Python is ignored by hyperMILL 35. `SET_TECSET_LINK` is off, and jobs keep the tool's "Rough - usage 1" link.
- Metric sessions: the script stops; the library selection is set up for inch.

**Tested in hyperMILL.**
- Lower receiver, confirmed working: tools built and attached; SpindleRPM, FeedrateXY and FeedrateZ set on the jobs.
- Offline regression before the 5 Nov container reset, tooled / flagged:
  - Walter: 22 / 3
  - Kennametal: 14 / 11
  - GARR: 21 / 4
- The last log received was a dry run that kept existing tools (0 tooled).

---

## tool_center and tool_flow (tool wizard / selector / generator / search)

**What it does.** One command (`tool_center.py`) for building library tools in the open document. The screens are in `tool_flow.py`, with `run(model, default_mat, mode)`.

The paths and how they evolved:
- Separate tool_wizard and tool_selector scripts existed first.
- 5 Nov 2026: condensed into one command with three paths: wizard, selector, and a new generator. He thinks of them as three levels:
  - level 1: Python picks the tool
  - level 2: choose from the top choices
  - level 3: the full unadulterated list
- 9 Nov 2026: a fourth path, Tool search, was added.

**Why it is built this way.**
- 5 Nov 2026: he asked that all paths show the same screens up to a certain point, so the shared screens 1 to 5 are identical:
  1. machine
  2. spindle
  3. manufacturer
  4. tool type and material (default = the joblist material)
  5. size, every limit for the type, and primary usage
- The wizard picks from the same rows the selector lists for that level, so the two always agree.
- The generator needs machine and spindle selection too, and shows ALL tools of the type and size, ordered by the material rating.
- Search (9 Nov 2026): for when he already knows the tool, e.g. Walter > md133 or Kennametal > harvi 4. He asked it to be as seamless with the other paths as possible.

**Rules and decisions.**
- Wizard:
  - one drop-down with the best first-choice tool of each performance level
  - flags in the option text: NOT 1ST CHOICE, LENGTH SHORT, nearest size, borrowed data, standard data
  - explanations go into the drop-downs (he asked for this when the wizard lost them)
- Selector:
  - level screen with family and tool counts; levels with nothing at the size are named in the window title
  - then first-choice families, family, tools, tool
- Generator:
  - no level screen
  - every family at the size, grouped by catalog rating (primary, suitable, not rated)
  - solid end mills: every size within 8 percent
- Search:
  - search box in place of the tool type
  - normalization: lower case; letters and digits only; a roman numeral I-X after a word of 2+ letters becomes a number (HARVI IV = harvi 4); "X 5" stays X5
  - scores: family/product name starts with > contains > catalog number > description
  - flat / radius / ball of one family are one match. The size screen gets a Tool type drop-down (added 9 Nov after "harvi 3" only said it contains flat, radius and ball) and corner radius (0 = square, D/2 = ball)
  - catalog-number search with 40 hits or fewer lists tools directly, except taps, thread mills and boring
  - nothing found: says whether the family is in the tables without a tool type, or which other manufacturer has it
- 12 Nov 2026: an intro message box describes the four paths and when each is most useful (text approved by him), with a "Show path descriptions at start" checkbox remembered in `tool_center_last.json`.
- Labels:
  - parenthetical comments removed from all dialog labels (10 Nov 2026) so the fields have room
  - input formats moved to the instructions file
- Display limits:
  - list message boxes are capped at 30 wrapped lines (OK button must stay on screen)
  - full lists go to the output window
  - drop-down option text is up to 130 characters
- All paths end with the cutting-data set checkboxes (end mills), Generate, then Next. Back on every screen.
- Chamfer mill (90 degree), Walter MC501 sized by large diameter Da, was restored as a tool type on 9 Nov after the unified build dropped it.

**Data sources.** tool_catalog.py (types, ratings, levels, candidate lists), tool_usage.py, `kennametal_names.csv`, all manufacturer CSVs. Remembered choices in `tool_center_last.json`. Icon: his own image (tool_center.png / .ico).

**Open / known not to work.**
- He said the list pages still need finessing to fit more useful info; deferred.
- Walter brand names (Protostar, Paradur, Prototex, Protodyn, ConeFit) are separate product lines not in the tables; Walter search works by family code only.
- Families in the tables with no tool type:
  - Walter: routers MC716/726, plunge MD344, barrel MD838/839/880, drill-mill MD780, MC500-504, PCD MP260/270/271, DA110 HSS, DC260 step drill, TC645/TMD drill thread mills, TC630 orbital thread mills
  - Kennametal: routers ROCS/ROCM, chamfered-corner end mills MDRH, F3BH, F4BJ, F5BJ, F6BJ, RUDC
- Kennametal crashed in the search path on 10 Nov (cp1252 decode of the "fi" ligature). Fixed the same day. **UNSURE** whether he re-confirmed Kennametal after the fix.

**Tested in hyperMILL.**
- Selector: built MD133-12.0W5L060D-WJ30RA (M_11047210) for M - PH with the HEM set.
- Generator: built MD177-16.0A7B080-WJ30EN (M_11063020).
- Search:
  - Walter worked
  - Kennametal failed (encoding, then fixed)
  - "harvi 3" showed the missing Tool type choice, then fixed
- Offline (fake GUI harness): all paths over every manufacturer x type x material x size, 0 failures; wizard and selector agreed on every request; every family findable by its own name.
- The 4-path intro box and the Tool type drop-down were delivered but not confirmed in hyperMILL. **UNSURE.**

---

## tool_library: tool_builder

**What it does.** Builds a hyperMILL tool from a library CSV row and imports it into the document.
- Method: take an exported tool file as a template (`template_*.xml`), change geometry and parameters, drop the `<docObject>` block, give new objGuids, import with `ToolSet.ImportTool`, rename to the designation.
- Also computes cutting data for each purpose (catalog, derived sets, rpm cap) and adds the user cutting-data sets.

**Why it is built this way.** hyperMILL's Python API cannot create tool geometry directly. A modified export imports cleanly. Importing a modified export of an existing tool creates a copy.

**Rules and decisions.**
- NC number: `nc_code(type, dia_in, variant, copy)` = 2-digit type + 4-digit diameter in thousandths + variant + copy.
  - The NC tool gets ncNumber = the number, ID = "M_<number>", name = "M_<number>". See the numbering section.
  - Numbers already used in the document are skipped (+10).
- Tool name = catalog designation.
- Tool comment:
  - non-Walter: "<manufacturer> <family> | grade | EDP <edp> | <unit> catalog"
  - Walter: "<manufacturer> <tier>"
- Manufacturer field is filled.
- Cutting-data purposes: Rough-HEM, Rough, Finish-2D-Radial, Finish-2D-Axial, Finish-Semi, Finish-3D (all "- usage 1").
  - Semi-finishing and 3D profiling sets are derived from the tool's own printed data.
  - Traditional roughing is high-feed style: ae 0.75 x D; ap 0.30 x corner radius (chip load raised by axial chip thinning, capped 2.5x) or 0.10 x D for square tools.
- Spindle max rpm (`MAX_RPM`, set from the spindle choice) caps every speed; the feed follows at the same chip load.
- Exchangeable-tip drills are built as head + Extension component (`USE_EXTENSION = True`).
- User cutting-data sets "User - 1/2/3" are added before import (see Tecsets).
- Cutting data source labels (`cut_source`): borrowed from another family, standard values, neighbouring group.
- Kennametal end mill data is picked by the tool's own grade, else labelled borrowed.
- `NO_BORROW_GRADES` (PCD, brazed, ceramic, inserted) never borrow solid carbide data.

**Data sources.**
- `material_map.csv`: hyperMILL material -> Walter group, plus a note column, e.g. the H2 note.
- `KENN_GROUP` dict: hyperMILL material -> Kennametal group.
- `walter_mill_cutting.csv`, `walter_mill_feed.csv`, `walter_vrr.csv`, `walter_drill_cutting.csv`, `kennametal_em_cutting.csv`, `kennametal_drill_cutting.csv`, `garr_*` through garr_cut.py.
- Page references in EM_TABLE_PAGE for Kennametal tables.

**Decisions with dates.**
- 16 Oct 2026: a tool built for a job gets cutting data only for the material of that job's joblist.
- "H - Hardened Steel 45-55 HRC" maps to Walter H2 with the note "Walter H2 = 52-58 HRC; slower than needed below 52". MEMM left out until its units are clear (early Nov 2026).

**Open.** Borrowed data is labelled but not verified against shop results. The ordering-code field is not written yet (see the tool page fields section).

**Tested in hyperMILL.** Tools build and import (selector, generator and part_wizard_2 logs). The User - 1/2/3 sets were delivered after probe 4. **UNSURE** whether he confirmed them in the tool dialog.

---

## tool_library: tool_lookup

**What it does.** Picks the best library tool for a request (drill, end mill shapes, chamfer, spot drill, face mill, boring, insert drill) and builds it. Used by part_wizard_2.

**Rules and decisions.**
- Selection order:
  1. First choice only: the catalog rates the tool 2 for the material's ISO group. Rated-1 tools are used only when no rated-2 tool exists at the size, marked NOT FIRST CHOICE.
  2. Highest tier: Supreme > Advance > Perform (16 Oct 2026, "always prefer best-performance tools").
  3. A tool with cutting data for the job material.
  4. The shortest tool that is long enough.
- Walter family lists per ISO group come from Walter GPS:
  - P, M, S, K from his GPS exports (ISO-STEEL, IS0_Stainless, iso_s, iso_K)
  - N and H from GPS screenshots (partial lists)
  - Aluminium (N) is narrowed to cutters rated N 2, else rated N with 3 or fewer flutes.
- Kennametal ranks by the catalog's own ISO rating. `GRADE_FALLBACK` K600 / KD1410 = aluminium grades only.
- `UNIT_PREF` = inch. Kennametal publishes separate inch and metric catalogs, and the preferred unit sorts first.
- `MANUFACTURERS` maps each manufacturer to its tables.

**Open.** Kennametal and GARR have no chamfer mills in the library.

---

## tool_library: tool_catalog

**What it does.** One set of tool-type and first-choice rules for tool_center.
- `TYPES`: each tool type's table, kind, size kind (dia / thread / bore), limits and tolerance.
- `candidates` (first choice per level).
- `all_candidates` (generator).
- `rating`, `describe_*`, `cut_text`, `source_note`, `available_types`.

**Rules and decisions.**
- Same size within 0.003 in (solid tools) or 0.01 in (inserted cutters, boring).
- A first-choice solid mill may be up to 8 percent off the requested diameter (`FIRST_CHOICE_DIA_OFF`) before a rated-1 tool of the exact size is used.
- Drills and reamers: exact size first. Spot drills and insert drills: nearest larger.
- Levels:
  - Performance (Supreme, GARR High performance)
  - Standard (Advance, GARR General purpose)
  - Low cost (Perform)
  - PCD
  - Level manufacturers: Walter and GARR. Kennametal has one level.
- `available_types` lists only types the manufacturer has tools for (9 Nov 2026).
- Chamfer mill (90 degree) type uses a row fix: size = Da from the MC501 designation, tip = table diameter.

**Open.** The tool types for the families listed under tool_center.

---

## tool_library: strategies

**What it does.** Part plans per industry and part type. Version `2026-10-14-b`.
- Industries: Aerospace (aluminum, composite, titanium, titanium and high alloy steel, stainless and high alloy steel structures, engine rotating, engine casing), Space, Defense, Mold and die, Fabrication and weldments, Medical, Automotive and motorsport, Oil gas and energy, Semiconductor and electronics, Tooling and fixtures, Robotics and optics, General industrial.
- A shape picker with icons for "not sure" parts.
- An operation catalog of 21 operations with saved settings. `DIRECT_OPS` = Swarf Curve and Swarf Surface (hyperMILL defaults).

**Why it is built this way.**
- He wanted a single wizard-style pop-up: pick industry, then part type, or a visual "not sure" picker matching the part on screen, then work through operations.
- Most parts finish in 2 or 3 setups on five-axis machines (sometimes 1; complex or warping parts 4 to 6). This is built into the setup flow.
- Part types he programs: aerospace, space, defense, weldments, injection molds, molding surface blocks, injector plates.

**Decisions.** 20 Oct 2026: over the coming months he will go through each part type's plan with coworkers to improve it. The current plans are a starting point; most parts need fewer than 9-10 toolpath types.

**Open.** These recommendations from 14 Oct 2026 are logged as pending:
- calibrate by dry-running 5-10 parts he already programmed
- cycle time per setup
- detect features from the model
- a user override JSON
- stock and fixturing as a wizard step

---

## tool_library: job_types.py

**What it does.** Every milling and drilling toolpath type the wizards can create: 77 of hyperMILL 35's 89 CreateJob codes, leaving out the 12 turning cycles.
- Per type: operation name, CreateJob code, menu group, the tool rule part_wizard_2 uses, primary usage, and default tool shape and diameter.
- Tool rules: hole, chamfer, rough, corner, floor, default, face, hand.

**Rules.** The 21 operations used by the part plans keep their own names (Rough HEM, Pocket HEM...) and have saved settings. Every other type is created with hyperMILL defaults.

**Tested in hyperMILL.** All 89 codes created successfully (probe_create_jobs). `DborX5` (Boring) is not tested in the wizard flow.

---

## tool_library: job_settings.json (with job_settings.py)

**What it does.** Job settings for every operation the wizards create, per material group and material.
- Layout: `{material group: {material: {operation: {stepover: settings}}}}`.
- Each settings block holds: `code`, `jobname`, `tool_shape`, `tool_dia_in` and `params` (`"*KEY": "value"`).
- The current file has 23 material groups (P, M, K, N, S, H subgroups, same names as material_map.csv) and 1488 operation settings.
- Stepover keys: "Percent stepover", "Distance stepover", or "" when the operation has one version.

**Why.** Replaces the macros: the same per-material job settings, written directly with `SetCfgParameters`. Edit a value in params to change what new toolpaths get.

**Data source.** **UNSURE** of the exact origin of each value. The material and operation set mirrors the macro database work (one entry per material and operation, materials such as "Ni-Hard", "Inconel 718"). Not confirmed in this session.

---

## tool_library: hole_jobs

**What it does.** Reads the mapped holes, assigns each hole group to a joblist, and creates the hole operations with a library tool per diameter. Used by both part wizards.

**Rules (settings at the top of the file).**
- Large holes: diameter 1.0 in or more gets Helical Drilling.
- Deep holes:
  - depth/diameter 5 or more: Peck Drill
  - 10 or more: gun drill, by hand
  - below 0.5: no drilling operation
- Threads: thread diameter 0.5 in or more gets Thread Milling, below that Tapping. Order: drill or peck, centering, then the thread operation.
- ISO fit holes: drill or peck, centering, reaming. The drill is under size by 0.016 in.
- Helical drilling end mill = 0.6 x hole diameter. The drill reaches hole depth + 0.3 x D (point allowance).
- Machining order: Drill, Peck Drill, Helical Drilling, Centering, Reaming, Thread Milling, Tapping.
- Feature properties read with `GetProperty`, e.g. `Hole::Front_Thread::Diameter`, `Hole::Front_Thread::Designation`, `Hole::Front_ISO-Fit::ISO-Fit_Value`.
- `read_holes` records position and bottom type. `merge_opposing` applies the opposing-holes rule (tolerances: coaxial 0.005 in, break-through extra 0.02 in).

**Tested in hyperMILL.** Hole features attached and hole jobs on the feature-list frame (lower receiver). Opposing-hole merge: see part_wizard_1 (**UNSURE** re-test).

---

## tool_library: hole_tools

**What it does.** Taps, thread mills and reamers (Walter, Kennametal, GARR reamers): selection, cutting data and tool XML.

**Rules and decisions.**
- Thread parsing for UNC/UNF/metric and MJ/UNJ (J-forms matched by standard).
- Taps:
  - prefer the tap's own grade for cutting data
  - Kennametal P0 fix
  - KHSST style mapping
  - Walter TD117/TD217 UNC and MJ/UNJ HSS taps added (early Nov 2026; `walter_taps.csv` 4030 rows)
- Thread mills: inch/J-form handling. Walter thread mills borrow TME data where the family prints none, labelled "borrowed".
- Reamers:
  - Walter Holemaking compendium data (`walter_reamer_cutting.csv`, `walter_reamer_vrr.csv`)
  - where a family prints nothing for the material group: standard values for solid carbide and HSS reamers, labelled "standard reaming values, not catalog data for this reamer, check before running" on screen, in the part_wizard_2 check list and in the tool comment

**Open.**
- Deferred: BSW taps, M4002 variants, PCD sizes.
- `TYPE_CODE = {tap: 60, reamer: 61, threadmill: 62}` does not match the M_ standard (reamer 60, cut tap 70, form tap 71, thread mill 72). See the numbering section.

---

## tool_library: garr_cut

**What it does.** GARR TOOL cutting data from the TECHNICAL catalog tables (`garr_mill_cutting.csv`, `garr_drill_cutting.csv`, `garr_reamer_cutting.csv`). The hyperMILL material is mapped to a GARR material row by `garr_material_map.csv`.

**Rules.**
- SFM = middle of the printed range. Chip load = middle of the printed range at the tool diameter, straight-line between the printed diameter columns.
- ae/ap from the guide's profile/trochoidal and slotting boxes where printed.
- HEM feed gets the radial chip-thinning correction, because the X/G, V and VRX guides state their data does not include it.
- Hardened material targets: H 45-55 HRC; other materials below 40 HRC.
- GARR first choice = series listed in the GARR RECOMMENDED catalog for the material group.

**Tested.** Offline regression only (GARR 21/4 in part_wizard_2; tool_center matrix). **UNSURE** of any GARR tool built in hyperMILL.

---

## tool_library: machine_pick

**What it does.** Machine model and spindle dialogs for the part wizards. The spindle's max rpm becomes `tool_builder.MAX_RPM`, which caps every speed (speed cut back, feed follows at the same chip load). The last choice is remembered in the temp folder (`hypermill_machine_last.json`) and offered first.

**Data.** `machines.csv`: HF3500, HF5500, F5000, F6000, F8000, F10000, F14000, F16000 and their spindles (e.g. HF3500 HSK63 DC 16000 rpm, HF5500 HSK100 DC 12000 rpm).

**Tested.** Used in every hyperMILL run (logs show the machine and spindle lines).

---

## tool_library: tool_usage

**What it does.** Orders first-choice milling tools by the operator's primary usage: Any, HEM / dynamic roughing, Traditional roughing, Slotting, Semi-finishing, Wall finishing, Floor finishing, 3D profiling. It only orders: no tool is removed and ratings are unchanged.

**Rules.**
- Score per family = manufacturer statement plus a generic geometry score 0-5:
  - catalog names this use (2): 12 + geometry
  - catalog says suitable (1): 6 + geometry
  - catalog silent: geometry only
  - catalog says not for it (0): -6 + geometry
- The catalog statement always leads.
- Generic geometry sources: Redline Tools (4/5/6 flute guide), Productivity Inc. (end mill selection), Dapra (3D finishing).
- Each usage pre-ticks its cutting-data set on the last screen.
- Applies to end mills, face mills and profile mills.

**Data.** `walter_usage.csv`, `kennametal_usage.csv`, `garr_usage.csv`.

---

## tool_order_list and tool_load_mda (also in the repo)

**tool_order_list.**
- Every tool from an operation or joblist to a CSV for ordering (manufacturer, order number and other ordering fields).
- Decision (4 Nov 2026): the tool comment is the order number, not the name; the name is an internal number.
- Order number priority: ordering code, then NC comment, then name.

**tool_load_mda** (built 12 Nov 2026, not yet run in hyperMILL).
- Source: one joblist, all joblists, or all document tools.
- Per tool: sisters (default 1, 0 = leave out) and tool life, 10 tools per screen.
- Writes `<DOC>_TOOL_LOAD.MPF` for pasting into MDA:
  - `R999=NEWT("<ID>",sister)`
  - status 2
  - Siemens tool type
  - length 1 = gage length
  - HL (`$TC_TPC5`) = gage length
  - HD (`$TC_TPC4`) = 4.0 below 4 in, else the diameter
  - tool life: `$TC_TP9=2`, `$TC_MOP13` = `$TC_MOP4` = pieces
- Proven on the control (12 Nov) with a hand-written R999/NEWT test.
- Control facts:
  - the tool list "create tool from file" loads one tool per INI file only
  - HD = `$TC_TPC4` and HL = `$TC_TPC5` (confirmed with his export)
- **UNSURE:** NEWT with his numeric/"M_" IDs, the Siemens type codes per hyperMILL type, metric conversion.

---

## 1. Tool numbering (Heller standard, from ToolNameGenerator.xlsx)

Prefix plus a number: **M_** milling, **T_** turning. Control rules:
- 32 characters max, A-Z 0-9 underscore, case sensitive (prefix stays uppercase).
- Call it quoted: `T="M_11050011"`. Unquoted, the control reads it as a number and the call fails. The post must write the name in quotes.
- Backups share the name and split on the DUPLO number.

**Milling: `M_ [TYPE 2] [DIAMETER 4] [VARIANT 1] [COPY 1]`**, example `M_11050011`.
- DIAMETER: in thousandths, four digits, leading zeros (0.375 = 0375, 1.000 = 1000).
- VARIANT (1-9): anything that makes it a different tool (nose radius, holder, coating, rougher vs finisher). Variant starts at 1.
- COPY (0-9): which physical one of that exact tool. Copies get their own codes.
- Example: M_11050010 and M_11050011 are the .030R rougher and finisher; M_11050020 is the .060R.
- The hM tool number is the digits after M_ (e.g. 10078710).
- 80s are reserved. Sub-variants inside a slot (conical vs tangent barrel, T-slot vs dovetail) split in the tool data, not the code.
- In the code only what you read at the machine or sort on: type and diameter. Everything else is a field (brand, EDP, cost, exact corner radius, coating, holder, gauge, tool life).

Milling type map:

| Family | Code | Tool |
|---|---|---|
| Solid profile mills | 10 | Flat (square) endmill |
| | 11 | Bullnose (corner-radius) endmill |
| | 12 | Ball endmill |
| | 13 | Chamfer mill |
| | 14 | Engraving / marking |
| | 15 | Taper / draft endmill |
| | 16 | Roughing (corncob) |
| | 17 | Plunge mill |
| Barrel / circle-segment | 20 | Barrel - general |
| | 21 | Barrel - conical |
| | 22 | Barrel - tangent |
| | 23 | Barrel - lens |
| | 24 | Barrel - Form-F / oval |
| Slotting / undercut / form | 30 | T-slot |
| | 31 | Dovetail |
| | 32 | Lollipop / undercut |
| | 33 | Keyseat / Woodruff |
| | 34 | Corner-rounding |
| | 35 | Form (profile) |
| Indexable milling | 40 | Face mill (indexable) |
| | 41 | Shell mill |
| | 42 | Hi-feed mill |
| | 43 | Square-shoulder / 90 deg |
| | 44 | Indexable endmill |
| | 46 | Disc / slot mill |
| | 47 | Plunge mill |
| Drilling | 50 | Carbide drill |
| | 51 | HSS / cobalt drill |
| | 52 | Insert drill |
| | 53 | Spot drill |
| | 54 | Center drill |
| | 55 | Gun / deep-hole drill |
| | 56 | Step drill |
| Hole finishing | 60 | Reamer |
| | 61 | Bore / fine-bore |
| | 62 | Countersink |
| | 63 | Counterbore |
| | 64 | Back countersink / counterbore |
| Threading | 70 | Cut tap |
| | 71 | Form tap |
| | 72 | Thread mill |
| | 73 | Helical / multi-thread mill |
| | 74 | Indexable thread mill |
| Probe / aux / special | 90 | Spindle probe |
| | 91 | Tool setter |
| | 92 | Deburr tool |
| | 99 | Unclassified / special |

**Turning: `T_ [TYPE 2] [ISO 2] [HAND 1] [VARIANT 1] [COPY 1]`**, example `T_10CNR10`.
- ISO = the 2-letter insert family, the first two letters of the ISO designation (CN = CNMG, DN = DNMG...). Non-ISO tooling: GR grooving, TH threading, FM form.
- HAND = R, L, N.
- Variant only splits within a family (grade, exact size, coating, holder length); a different family gets its own code. Copy = physical duplicate. Size, grade and coating stay in fields.

Turning type map:
- OD turning: 10 rough, 11 finish, 12 profiling, 13 back-turning, 14 shoulder / 90 deg
- Boring (ID): 20 rough, 21 finish, 22 profiling, 23 back-boring
- Facing: 30 rough, 31 finish
- Grooving / parting: 40 parting / cutoff, 41 OD grooving square, 42 OD grooving profile/form, 43 face grooving, 44 ID grooving
- Threading: 50 OD, 51 ID, 52 face / scroll
- Holemaking (turret): 60 center drill, 61 drill, 62 reamer, 63 tap (rigid)
- Form / special: 70 form tool, 71 knurling, 72 radius / chamfer form
- Probe / aux: 90 turret probe, 91 tool setter / eye, 99 special
- 80s reserved.

**Decisions from the conversation.**
- 16 Oct 2026, tool naming in automation:
  - Only tools used in a job get named.
  - The hyperMILL tool name is the manufacturer part / EDP number; the NC tool gets the M_ rule name.
  - M_ codes are not tied to an EDP: they are assigned fresh per job, so the same M_ code can be a different tool in different jobs.
- NC numbers must be unique in a document. hyperMILL refuses duplicate NC Numbers only; names and comments may repeat.
- A second assembly of the same tool with a different reach gets the next variant number, so it is a different tool number (12 Nov 2026).
- The builder writes ncNumber = digits, ID = "M_<digits>", name = "M_<digits>".

**Code vs standard: known mismatches (open).** The type codes in the catalog CSVs and `hole_tools.TYPE_CODE` do not all follow the workbook:

| Tool | Code in the data | Workbook code |
|---|---|---|
| Walter face mills | 14 | 40 |
| Walter shoulder mills | 15 | 43 |
| hi-feed / copy cutters | 16 / 17 | 42 |
| profile cutters | 19 | |
| slot mills | 21 | 46 |
| insert-tip drills | 53 | 52 |
| boring | 52 | 61 |
| spot drills | 51 / 54 | 53 / 54 |
| chamfer inserts | 18 | |
| taps | 60 | 70 / 71 |
| reamers | 61 | 60 |
| thread mills | 62 | 72 |

End mills 10/11/12, carbide drills 50 and solid chamfer mills 13 match.

**9-digit company code (UNSURE).** He mentioned his own numbering system several times, but the 9-digit format was never defined in this conversation.
- Numbers seen on his tools: 275080900 (3/4" Sandvik Dura .03 rad bullnose), 416580900 (4.2 mm drill in a holder), 147280900, 125000603 (sister 2 export).
- Job names in his hyperMILL logs carry 8-digit codes like T11015810 / T50006110.
- How the 9 digits break down (type / diameter / variant / copy) was not discussed. Do not derive it from these examples without asking him.

---

## 2. hyperMILL tool page fields

Agreed layout (12 Nov 2026), held for when holders are added. His post now reads the **ID** field (he changed it from Name), which frees Name and Comment in Common and Name and Comment in Tool for setup sheets and tool reports.

**Common (the NC tool / assembly)**
- **NC-Number** and **ID**: the same number, inherently. The post reads ID. hyperMILL refuses duplicate NC Numbers.
- **Name**: short assembly nomenclature, tool + holder, e.g. `.750 BR R.03 6FL L1.50 | HSK100 SHR .750`.
  - Tool part: diameter, type code, corner radius, flutes, cutting length. Type codes: EM flat, BR bull nose, BN ball, DR drill, SP spot drill, RM reamer, TAP with thread, TM thread mill, CH chamfer mill, FM face mill, BB boring bar.
  - Holder part: interface, style (SHR shrink, HYD hydraulic, ER collet, SW side lock, MILL milling chuck), bore.
  - Names may repeat (different reach = different number).
- **Comment**: holder detail: holder manufacturer, holder EDP / order number, holder description, e.g. `HAIMER A63.140.19 | EDP 12345678 | HSK100 shrink 3/4 x 140`.

**Tool (the cutter)**
- **Name**: the manufacturer's long name, e.g. `Kennametal HARVI III 6 flute radius end mill 3/4 x 1.50 LOC R.03 plain shank`.
- **Comment**: he said the EDP or order number. The proposal (12 Nov) puts the order number in Ordering code and uses Comment for catalog number | grade | cutting-data source, e.g. `HA3R6RA0750R150HAR030 | KCSM15A | cutting data: catalog`. He liked the dummy built this way. **UNSURE** whether that split is final.
- **Manufacturer**: filled.
- **Ordering code**: EDP / Material Number. For Kennametal the Material Number (`edp` column, e.g. 7077716) is what is used to order and must be in the tool. GARR has an `edp` column; the Walter tables have only the designation.
  - **UNSURE**: the XML parameter name `orderingCode` was a guess from the Python API listing. It has to be checked on the dummy import.

**Holder** (from his `tool_with_holder.xml`; nothing built yet)
- **Name**: the holder is named "Holder" in his export. The plan was to use the export's file name as the holder's name in the drop-down. A separate holder Name/Comment content standard was not settled. **UNSURE.**
- **Comment**: not decided. The holder detail lives in Common > Comment.

**Extension**
- The builder already uses an Extension component for exchangeable-tip drills (head + extension).
- An Extension Name standard was not discussed. **UNSURE.**

**Setup sheet columns** (agreed, he may update): T number | Assembly | Reach / Gage | Tool order # | Holder order #. Reach and gage share one column (e.g. 3.700 / 8.188); gage = holder length + reach.

**Purchase sheet columns**: Manufacturer | Order # | Tool | Catalog no. / grade / cutting data | Qty | Holder.

**Holder plan** (saved for later):
- He exports tool-with-holder XMLs (2D outline, taper removed, no 3D mounting identifiers needed) into `tool_library\holders`.
- The holder block is copied into the built tool. The holder couplings share the tool's coupling objGuid.
- The holder component goes before the tool component, with reach on the tool component.
- Holder drop-down plus stickout on the last tool_center screen, filtered by shank size and spindle interface.
- Open question to him: shank size and interface from CSV columns or from the file name.

---

## 3. Tecsets (cutting-data sets)

**Decided.**
- 16 Oct 2026: a tool built for a job gets cutting data for the material of that job's joblist only. The CSV libraries cover all material groups.
- 20 Oct 2026: the automation should work with no tool database. hyperMILL cannot create tecsets directly (only through its separate database program), so he wanted a Python way to add tecsets to tools.
- Probes 1 to 4 (early Nov 2026): a tecset cannot be added to a tool already in the document.
  - The document tool never changes.
  - `Tool.SetCfgParameters` on the `*CP_n` / `*CPITEM_x_n` keys is ignored.
  - `om.tdb` `MillingTechnology` has no constructor; copy and pickle fail.
  - Importing a modified export creates a copy, not an update.
- 5 Nov 2026: he will not do a copy/swap. Instead every tool that comes in gets three extra sets, "User - 1", "User - 2", "User - 3" (he wrote "user - 1, 2 and 3"), for easy editing in hyperMILL.
  - They are copies of the tool's catalog set, or of its invariant set when there is no catalog data.
  - Built by `tool_builder.add_user_sets` before import, with matching ncTool cutting profiles and a materials entry.
- Rules he gave (with screenshots): every tecset MUST have a material, and a tool can have only one invariant set (the set without a material). So without a job material no user sets are added.
- Purpose names in use: Rough-HEM, Rough, Finish-2D-Radial, Finish-2D-Axial, Finish-Semi, Finish-3D (all "- usage 1"), plus User - 1/2/3.
- `*JOB_CPNAME` (pointing a job at a tecset) is ignored by hyperMILL 35. Jobs get SpindleRPM / FeedrateXY / FeedrateZ set directly.

**Still open.**
- **UNSURE** whether he confirmed the User - 1/2/3 sets in hyperMILL after delivery.
- The om.tdb route was probed but not built: `Database().create/open`, `importObjects` into a separate tool database, then re-import.
- Linking jobs to a specific tecset from Python has no working method.
- The capitalisation "User - 1" vs his "user - 1" was not discussed.

---

## Macro database: required to load the ISO material classes into hyperMILL

**Why it is needed.** The ISO material classes were loaded into hyperMILL through the macro database. Every script depends on those names:
- the joblist Material field
- `material_map.csv`
- `job_settings.json`
- the tecset materials

Keep a macro database with these classes loaded in hyperMILL. Without it the material names the scripts look for do not exist in hyperMILL. This is why the macro database is kept, even though toolpaths are no longer made from macros (20 Oct 2026).

**Naming.** Materials are named "<ISO letter> - <class>", e.g. S - Nickel Based, N - Aluminum, K - Gray Cast Iron. The scripts use exactly these 23 names. Changing the wording, e.g. "S - nickel" or one "K - cast iron" for all three K classes, would also need `material_map.csv`, `job_settings.json`, `garr_material_map.csv` and `KENN_GROUP` in tool_builder.py changed to match.

**File: `macro_database\ISO_materials_dummy_macros.db`** (rebuilt 20 Nov 2026). The complete macro database from October is not in the workspace any more.
- Built from his own saved macro database (`2026mac.db`, hyperMILL 35, format version 22.0) by replacing its content.
- `Material_Group` and `Material` both hold the 23 ISO material classes:
  - P - Low Carbon Steel, P - Medium Carbon Steel, P - Alloy Steel, P - Tool Steel, P - Cast Steel
  - M - Austenitic, M - Martensitic, M - Duplex, M - PH
  - K - Gray Cast Iron, K - Ductile Iron, K - Compacted Graphite Iron
  - N - Aluminum, N - Copper, N - Brass, N - Bronze
  - S - Nickel Based, S - Iron Based, S - Cobalt Based, S - Titanium
  - H - Hardened Steel 45-55 HRC, H - Hardened Steel 55-65 HRC, H - Chilled Cast Iron
- Macros: one dummy macro per class, named "J: DUMMY | <class>", macro type "ISO material classes", machine group HF5500.
  - Each holds one job: an unchanged copy of his own saved 2D contour job (Walter MC166 12 mm tool, metric values).
  - The copy is unchanged so the job checksum (`JobParaCRC32`) stays the one hyperMILL wrote. That checksum could not be reproduced, so no job parameter was edited.
  - The macros are placeholders. Do not apply them to parts.
- **UNSURE:** the menu steps used to load the macro database were not recorded in this conversation. Load it the same way the October macro database was loaded.
- **UNSURE:** whether hyperMILL reads the classes from `Material_Group`, `Material` or both. Both are filled.
- Not tested in hyperMILL yet.

**History.**
- Started from his saved sample macros (`2026mac.db`: one 2D contour macro, then a 12-job "Drill+2D+3D+TURN" macro).
- Build order: ISO S first, then N, then stainless (M), then H, then P and K. Metric and imperial versions were kept as separate files.
- The first ISO S file used "ISO S - Inconel 718" style names. These were replaced by the "<ISO letter> - <class>" names that match his tools and jobs.
- Macro approach and retract factors are fractions of tool diameter. They stay the same in metric and imperial.
- The per-material job settings of those macros live on in `job_settings.json`. **UNSURE** of the exact carry-over.
