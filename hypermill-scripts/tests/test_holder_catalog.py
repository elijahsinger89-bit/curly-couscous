#!/usr/bin/env python3
"""Sandvik holder tables extracted from Rotating Tools 2020 (docs/catalog_extract/sandvik_2020.py):
row counts, every row usable, HSK-A only, and rows checked by hand against the catalog pages.
Run: python3 tests/test_holder_catalog.py"""
import os
import sys
import csv
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
HOLD = os.path.join(os.path.dirname(HERE), "copy_to_python_folder", "tool_library", "holders")
fails = []


def check(cond, label):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def rows(name):
    with open(os.path.join(HOLD, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(s):
    try:
        return float(str(s).replace("°", ""))
    except ValueError:
        return None


hsk, capto = rows("sandvik_hsk.csv"), rows("sandvik_capto.csv")
check(len(hsk) == 209 and len(capto) == 490, "rows: HSK %d (209), Capto %d (490)" % (len(hsk), len(capto)))
check(all(num(r["DCONMS"]) and num(r["LF"]) for r in hsk + capto), "every row has DCONMS and LF")
check(all(num(r["DCONMS"]) in (32, 40, 50, 63, 80, 100, 125, 160) for r in hsk), "HSK sizes 32-160")
check(all("A" in r["machine_side"] for r in hsk), "HSK rows are all for HSK A (A/C, A/C/T)")
check(all(r["CZCMS"].startswith("C") for r in capto), "Capto rows: machine side C3-C10")
check(all(r["ordering_code"] and r["family"] for r in hsk + capto), "every row has an order code and a family")
fam = collections.Counter(r["family"] for r in hsk)
for f in ("HSK to CoroChuck™ 930", "HSK to Weldon adaptor", "HSK to ER collet chuck", "HSK to arbor adaptor",
          "HSK to shrink fit chuck", "HSK to Coromant Capto® adaptor"):
    check(fam[f] > 0, "HSK family present: %s (%d)" % (f, fam[f]))
for f in ("Coromant Capto® to CoroChuck™ 930", "Coromant Capto® to Weldon adaptor", "Coromant Capto® to ER collet chuck",
          "Coromant Capto® to arbor adaptor", "Coromant Capto® to shrink fit chuck"):
    check(any(r["family"] == f for r in capto), "Capto family present: %s" % f)

by = dict((r["ordering_code"], r) for r in hsk + capto)
KNOWN = {    # by hand from the catalog pages
    "930-HA10-S-20-100": dict(page="388", design="Slender design", DCONWS="20.0", LSC="51", LF="100.0", LB1="16.0", LB2="49.2",
                              LB3="71.0", BD1="38.0", BD2="42.0", BD3="50.0", BHTA1="7°", RPMX="10000"),
    "930-HA04-S-08-070": dict(DCONMS="40.0", DCONWS="8.0", LSC="37", LF="70.0", LB1="11.3", LB2="35.3", LB3="50.0",
                              BD1="24.0", BD2="28.0", BD3="32.0", BHTA1="10°", RPMX="30000"),          # stacked in plain text
    "392.41020-100 20 100A": dict(family="HSK to Weldon adaptor", DCONWS="20.0", LF="100.0", LB1="5.0", LB2="71.0", LB3="100.0",
                                  BD1="42.0", BD2="52.0", BD3="100.0", BHTA1="45°", RPMX="12500"),
    "392.41014-63 16 100": dict(family="HSK to ER collet chuck", CZCWS="ER16", DSGN="2", DCONWS="17.0", LF="89.4", LB1="71.0",
                                LB2="100.0", BD1="28.0", BD2="63.0", RPMX="20500"),
    "392.41005C-4016050": dict(family="HSK to arbor adaptor", DCONWS="16.0", LF="50.0", LB1="30.0", LB2="50.0", BD1="32.0",
                               BD2="40.0", RPMX="30000"),
    "C6-390.410-100 110A": dict(family="HSK to Coromant Capto® adaptor", CZCWS="C6", DCONMS="100.0", DCONWS="63.0"),
}
for code, want in KNOWN.items():
    r = by.get(code)
    got = dict((k, r.get(k)) for k in want) if r else None
    check(r is not None and got == want, "%s as in the catalog%s" % (code, "" if got == want else ": %s" % got))
check("930-HA10-S-20-100" in by and by["930-HA10-S-20-100"]["LB4"] == "" and by["930-HA10-S-20-100"]["BD4"] == "",
      "blank cells stay blank (no LB4 / BD4 on a 3-diameter slender chuck)")

print("\n%d failed" % len(fails) if fails else "\nALL HOLDER CATALOG CHECKS PASSED")
sys.exit(1 if fails else 0)
